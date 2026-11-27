"""Check AXIS frame violation terms with full-width Z3, ordinary Boolean reasoning or indexed egg."""
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time

import z3

from egg_assertion_baseline import canonical_key
from egg_frame_terms import abstract, evaluate_term, format_term, parse_term, z3_env, z3_term
from m3_proof_dependencies import validate_proof_dependencies
from predicates import parse


SCOPE = "frame_task current and previous rising-edge pin samples, unrestricted two-state values"


def _check(formula, timeout_ms):
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    solver.add(formula)
    status = solver.check()
    record = {"status": str(status), "smt2": solver.to_smt2()}
    if status == z3.unknown:
        record["reason"] = solver.reason_unknown()
    return record, solver.model() if status == z3.sat else None


def _oracle(left, right, env, timeout_ms):
    a, b = z3_term(left, env), z3_term(right, env)
    record, model = _check(z3.Xor(a, b), timeout_ms)
    record.update(equivalent={"sat": False, "unsat": True}.get(record["status"]),
                  counterexample=None, reference_value=None, candidate_value=None)
    if model is not None:
        values = {}
        for name, pin in env.items():
            value = model.eval(pin, model_completion=True)
            values[name] = z3.is_true(value) if z3.is_bool(pin) else value.as_long()
        lv, rv = evaluate_term(left, values), evaluate_term(right, values)
        if lv == rv or (lv, rv) != tuple(z3.is_true(model.eval(x, model_completion=True)) for x in (a, b)):
            raise ValueError("typed counterexample did not replay on the sampled pins")
        record.update(counterexample=values, reference_value=lv, candidate_value=rv)
    return record


@dataclass(frozen=True)
class _OracleReceipt(Mapping):
    reference: str
    candidate: str
    timeout_ms: int
    oracle_seconds: float
    _serialized: str

    def __getitem__(self, key):
        if key == "oracle":
            # Return independently mutable JSON for each consumer. No arm can alter
            # another arm's future counterexample through a shared nested dict.
            return json.loads(self._serialized)
        if key in ("reference", "candidate", "timeout_ms", "oracle_seconds"):
            return getattr(self, key)
        raise KeyError(key)

    def __iter__(self):
        return iter(("reference", "candidate", "timeout_ms", "oracle_seconds", "oracle"))

    def __len__(self):
        return 5


def typed_oracle(reference: str, candidate: str, *, timeout_ms: int = 5000) -> Mapping:
    """Run one full-width query and bind its original answer to exact source strings and budget."""
    if type(timeout_ms) is not int or timeout_ms < 1:
        raise ValueError("expected a positive solver timeout")
    start = time.perf_counter()
    data = _oracle(parse_term(reference), parse_term(candidate), z3_env(), timeout_ms)
    return _OracleReceipt(reference, candidate, timeout_ms, time.perf_counter() - start, json.dumps(data))


def _literal(node):
    while isinstance(node, tuple) and node[0] == "not":
        node = node[1]
    return node if isinstance(node, str) else None


def _certify_atoms(atoms, trees, env, timeout_ms, *, lower=z3_term, scope=SCOPE):
    # Every candidate rule relates two distinct primitive bit-vector comparisons.
    # Include neither Boolean subexpressions nor the two complete target literals.
    roots = {_literal(tree) for tree in trees}
    values = {name: lower(atom, env) for name, atom in sorted(atoms.items())
              if isinstance(atom, tuple) and atom[0] in ("eq", "ult", "ule")}
    rules, checks = [], []
    for i, (left, right) in enumerate(combinations(values, 2)):
        check = {"left": left, "right": right, "queries": []}
        checks.append(check)
        if roots == {left, right}:
            check["skipped"] = "would compare the complete target literals"
            continue
        a, b = values[left], values[right]
        for relation, violation in (("equal", z3.Xor(a, b)), ("complement", a == b)):
            query, _ = _check(violation, timeout_ms)
            check["queries"].append({"relation": relation, **query})
            if query["status"] == "unsat":
                rule = {"name": f"typed-{relation}-{i}", "left": left,
                        "right": right if relation == "equal" else f"(not {right})",
                        "proof_status": "unsat", "event_context": scope}
                rules.append(rule)
                check["certified_rule"] = rule["name"]
                break
    return rules, checks


def _quotient(rules):
    neighbors = defaultdict(list)
    for rule in rules:
        right = parse(rule["right"])
        invert = isinstance(right, tuple)
        left, right = rule["left"], right[1] if invert else right
        neighbors[left].append((right, invert))
        neighbors[right].append((left, invert))
    aliases = {}
    for representative in sorted(neighbors):
        if representative in aliases:
            continue
        work = [(representative, False)]
        while work:
            name, parity = work.pop()
            if name in aliases:
                if aliases[name] != (representative, parity):
                    raise ValueError("inconsistent signed comparison certificates")
                continue
            aliases[name] = (representative, parity)
            work.extend((n, parity != inverted) for n, inverted in neighbors[name])
    return aliases


def _subst(node, aliases):
    if isinstance(node, str):
        representative, invert = aliases.get(node, (node, False))
        return ("not", representative) if invert else representative
    return (node[0], *(_subst(arg, aliases) for arg in node[1:]))


def _prop(node):
    if isinstance(node, str):
        if node in ("true", "false"):
            return z3.BoolVal(node == "true")
        return z3.Bool(node)
    return {"and": z3.And, "or": z3.Or, "not": z3.Not}[node[0]](*(_prop(arg) for arg in node[1:]))


def _ordinary(trees, rules, timeout_ms):
    aliases = _quotient(rules)
    a, b = (_subst(t, aliases) for t in trees)
    keys = [canonical_key(format_term(t)) for t in (a, b)]
    # Keep the complete propositional query even on a canonically identical pair.
    # It knows only independent Booleans and the explicitly certified substitutions.
    query, _ = _check(z3.Xor(_prop(a), _prop(b)), timeout_ms)
    if keys[0] == keys[1] and query["status"] == "sat":
        raise ValueError("canonical keys disagree with the propositional query")
    proved = keys[0] == keys[1] or query["status"] == "unsat"
    return ({"method": "ordinary", "proved": proved, "stop": query["status"], "steps": [],
             "canonical_match": keys[0] == keys[1]},
            {"canonical_keys": keys, "abstract_xor": query, "certified_substitution": aliases})


def _egg(binary, payload):
    process = subprocess.run([str(Path(binary).resolve(strict=True)), "indexed"], input=json.dumps(payload),
                             text=True, capture_output=True, check=True, timeout=30)
    graph, timing = json.loads(process.stdout), json.loads(process.stderr)
    if timing["mode"] != "indexed" or graph["ground_rule_count"] != len(payload["verified_rules"]):
        raise ValueError("unexpected egg mode or certified rule count")
    if [t["id"] for t in graph["targets"]] != [t["id"] for t in payload["targets"]]:
        raise ValueError("egg returned different target IDs")
    stop = graph["stop_reason"]
    audit, proved, steps = None, False, []
    if stop == "Some(Saturated)":
        audit = validate_proof_dependencies(payload, graph)
        left, right = graph["targets"]
        proved = left["eclass"] == right["eclass"]
        steps = [step for edge in audit["edges"] for step in edge["steps"]]
    elif not any(stop.startswith("Some(" + limit + "(") for limit in ("TimeLimit", "NodeLimit", "IterationLimit")):
        raise ValueError(f"unrecognized egg stop reason {stop!r}")
    return ({"method": "egg", "proved": proved, "stop": stop, "steps": steps},
            {"egg_input": payload, "egg_graph": graph, "egg_audit": audit, "egg_timing": timing})


def review(reference: str, candidate: str, *, binary: Path, arm: str, timeout_ms: int = 5000,
           common: Mapping | None = None) -> dict:
    """Report common full typed semantics separately from the arm's proof on abstract comparisons."""
    if arm not in ("raw", "ordinary", "egg") or type(timeout_ms) is not int or timeout_ms < 1:
        raise ValueError("expected raw, ordinary or egg and a positive solver timeout")
    receipt = typed_oracle(reference, candidate, timeout_ms=timeout_ms) if common is None else common
    if (not isinstance(receipt, _OracleReceipt) or
            (receipt.reference, receipt.candidate, receipt.timeout_ms) != (reference, candidate, timeout_ms)):
        raise ValueError("common oracle receipt is not bound to this reference, candidate and timeout")
    oracle = receipt["oracle"]
    proof, evidence = None, None
    start = time.perf_counter()
    if arm != "raw":
        (a, left_atoms), (b, right_atoms) = abstract(parse_term(reference)), abstract(parse_term(candidate))
        if any(left_atoms[k] != right_atoms[k] for k in left_atoms.keys() & right_atoms.keys()):
            raise ValueError("Boolean atom collision across the two violation expressions")
        atoms = {**left_atoms, **right_atoms}
        trees = (parse(a), parse(b))
        rules, checks = _certify_atoms(atoms, trees, z3_env(), timeout_ms)
        if arm == "ordinary":
            proof, method_data = _ordinary(trees, rules, timeout_ms)
        else:
            targets = [{"id": name, "compact": term, "event_context": SCOPE}
                       for name, term in (("reference", a), ("candidate", b))]
            proof, method_data = _egg(binary, {"targets": targets, "verified_rules": rules})
        if proof["proved"] and oracle["equivalent"] is False:
            raise ValueError("abstract proof contradicts a replayed full-width typed counterexample")
        evidence = {"abstract_terms": [a, b], "atom_sources": {k: format_term(t) for k, t in atoms.items()},
                    "verified_rules": rules, "primitive_pair_checks": checks, **method_data}
    return {"arm": arm, "reference": reference, "candidate": candidate, "oracle": oracle,
            **{key: oracle[key] for key in ("equivalent", "counterexample", "reference_value", "candidate_value")},
            "proof": proof, "evidence": evidence, "oracle_seconds": receipt.oracle_seconds,
            "oracle_reused": common is not None,
            "method_seconds": time.perf_counter() - start if arm != "raw" else 0.0}
