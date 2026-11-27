"""Candidate-only sufficient transaction cubes and independently replayed restricted-goal egg proofs."""
from collections.abc import Mapping
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import subprocess

import z3

from egg_frame_diagnostic_baseline import minimum_cube
from egg_frame_pc_certificate import MAX_CHARS, MAX_STEPS, TIMEOUT_SECONDS
from egg_frame_pc_cube_certificate import RULES, _apply, _checked_steps, _json, _restrict, _rules, _symbols
from egg_frame_pc_diagnosis import verify_diagnosis_record
from egg_txn_terms import BOOL_NAMES, BV_WIDTHS, DOMAIN_NAMES, abstract, format_term, parse_term, referenced_signals, sample, z3_env, z3_term
from m3_proof_dependencies import _plain


MAX_ATOMS = 16
SOLVER_MS = 2000
TYPED_SCOPE = "All well-sorted two-state transaction variables, without any domain or full-sample constraint."
SCOPE = "Signed transaction candidate with only the listed cube fixed and all other Boolean atoms free."


def _require(value, why):
    if not value:
        raise ValueError(why)


def _snapshot(candidate, values):
    _require(isinstance(values, Mapping) and set(values) <= BOOL_NAMES | BV_WIDTHS.keys(),
             "expected sampled transaction variables")
    pins = {}
    # Preserve structural context because domain-constrained completion may resolve an unknown atom.
    for name in sorted(referenced_signals(candidate) | DOMAIN_NAMES):
        value = values.get(name)
        if value is None or (type(value) is int and value == -1):
            pins[name] = None
        elif name in BOOL_NAMES:
            _require(type(value) in (bool, int) and value in (0, 1), "nonbinary transaction flag")
            pins[name] = bool(value)
        else:
            _require(type(value) is int and 0 <= value < (1 << BV_WIDTHS[name]), "transaction value outside bus width")
            pins[name] = value
    return pins


@lru_cache(maxsize=32)
def _wide_truth(source, names):
    """Construct a bit for every valuation of 13–16 independent atoms."""
    rows = 1 << len(names)
    full = (1 << rows) - 1
    columns = {}
    for i, name in enumerate(names):
        stride = 1 << i
        column = ((1 << stride) - 1) << stride
        period = 2 * stride
        while period < rows:
            column |= column << period
            period *= 2
        columns[name] = column

    def mask(node):
        if isinstance(node, str):
            if node in ("true", "false"):
                return full if node == "true" else 0
            return columns[node]
        op = node[0]
        if op == "not":
            return full ^ mask(node[1])
        a, b = mask(node[1]), mask(node[2])
        return (a & b) if op == "and" else (a | b)

    return full, mask(_plain(source)), columns


def _minimum(source, assignment):
    n = len(assignment)
    if n <= 12 or n > MAX_ATOMS:
        return minimum_cube(source, assignment, max_atoms=min(MAX_ATOMS, 12))
    full, positive, columns = _wide_truth(source, tuple(sorted(assignment)))
    known = [(name, val, columns[name] if val else full ^ columns[name])
             for name, val in sorted(assignment.items()) if val is not None]
    compatible = full
    for _, _, mask in known:
        compatible &= mask
    total, hits = compatible.bit_count(), (compatible & positive).bit_count()
    result = {"atom_count": n, "known_atom_count": len(known), "consistent_assignments": total,
              "positive_assignments": hits, "cube": None, "size": None}
    if hits < total:
        return {**result, "status": "unknown" if hits else "false"}
    for size in range(len(known) + 1):
        for subset in combinations(known, size):
            bad = full ^ positive
            for _, _, mask in subset:
                bad &= mask
            if not bad:
                return {**result, "status": "sufficient", "cube": [(k, v) for k, v, _ in subset], "size": size}
    raise AssertionError("all known literals must exclude the false rows")


def _typed_query(signed, atoms, cube):
    env = z3_env()
    literals = []
    for name, truth in cube:
        expr = z3_term(atoms[name], env)
        literals.append(expr if truth else z3.Not(expr))
    # Deliberately stronger than the protocol grading domain: only cube literals constrain the free variables.
    violation = z3.And(*literals, z3.Not(z3_term(signed, env)))
    lines = ["(set-logic QF_BV)", f"(set-option :timeout {SOLVER_MS})"]
    for name in sorted(referenced_signals(signed)):
        lines.append(f"(declare-fun {name} () {env[name].sort().sexpr()})")
    smt2 = "\n".join([*lines, f"(assert {violation.sexpr()})", "(check-sat)", ""])
    solver = z3.SolverFor("QF_BV")
    solver.from_string(smt2)
    solver.set(timeout=SOLVER_MS)
    status = solver.check()
    record = {"status": str(status), "smt2": smt2, "smt2_sha256": hashlib.sha256(smt2.encode()).hexdigest(),
              "logic": "QF_BV", "scope": TYPED_SCOPE, "timeout_ms": SOLVER_MS, "z3": z3.get_version_string()}
    if status == z3.unknown:
        record["reason_unknown"] = solver.reason_unknown()
    return record


def diagnose(candidate, values, candidate_value):
    """Find an exact minimum compatible Boolean cube; independently prove its typed implication."""
    _require(type(candidate_value) is bool, "expected a Boolean candidate decision")
    original = parse_term(candidate)
    signed = original if candidate_value else ("not", original)
    source, atoms = abstract(signed)
    pins = _snapshot(signed, values)
    observed = sample(signed, pins)
    assignment = {name: sample(node, pins) for name, node in sorted(atoms.items())}
    public = {"status": "sample_unknown" if observed is None else "sample_mismatch",
              "candidate_value": candidate_value, "literal_count": None, "sufficient_literals": []}
    oracle = {"status": "not_run", "signed_source_at_sample": observed, "max_atoms": MAX_ATOMS,
              "minimum_cube": None, "typed_implication": None}
    result = {"candidate": candidate, "typed_source": format_term(signed), "source": source,
              "atoms": {name: format_term(node) for name, node in atoms.items()}, "sample": pins,
              "assignment": assignment, "cube": None, "public": public, "oracle": oracle}
    if observed is not True:
        return result
    minimum = _minimum(source, assignment)
    oracle["minimum_cube"] = {k: v for k, v in minimum.items() if k != "cube"}
    if minimum["status"] != "sufficient":
        _require(minimum["status"] != "false", "typed transaction sample contradicts Boolean abstraction")
        public["status"] = minimum["status"]
        return result
    cube = [[name, truth] for name, truth in minimum["cube"]]
    _require(all(assignment[name] is truth for name, truth in cube), "cube contains an unobserved literal")
    receipt = _typed_query(signed, atoms, cube)
    oracle.update(status=receipt["status"], typed_implication=receipt)
    _require(receipt["status"] != "sat", "cube fails unrestricted typed implication")
    if receipt["status"] != "unsat":
        public["status"] = "oracle_unknown"
        return result
    result["cube"] = cube
    public.update(status="sufficient", literal_count=len(cube),
                  sufficient_literals=[{"term": format_term(atoms[k]), "value": v} for k, v in cube])
    return result


def _residual(source, atoms, cube):
    ast = _plain(source)
    _require(isinstance(atoms, dict) and _symbols(ast) == set(atoms), "wrong transaction atom inventory")
    for name, typed in atoms.items():
        atom = parse_term(typed)
        _require(abstract(atom) == (name, {name: atom}), "wrong typed transaction atom binding")
    substitutions = {}
    _require(isinstance(cube, list), "missing transaction cube")
    for literal in cube:
        _require(isinstance(literal, list) and len(literal) == 2, "invalid transaction literal")
        name, truth = literal
        _require(type(name) is str and name in atoms and name not in substitutions and type(truth) is bool,
                 "invalid, duplicate, or foreign transaction cube literal")
        substitutions[name] = "true" if truth else "false"
    return format_term(_restrict(ast, substitutions))


def _bound(diagnosis):
    fresh = diagnose(diagnosis["candidate"], diagnosis["sample"], diagnosis["public"]["candidate_value"])
    verify_diagnosis_record(diagnosis, fresh)
    if fresh["public"]["status"] != "sufficient":
        return None
    bound = {k: fresh[k] for k in ("source", "atoms", "cube")}
    return {**bound, "candidate_value": fresh["public"]["candidate_value"],
            "restricted_source": _residual(**bound),
            "typed_smt2_sha256": diagnosis["oracle"]["typed_implication"]["smt2_sha256"]}


def replay_public(public):
    """Reconstruct the substituted transaction term and every disclosed local rewrite down to true."""
    fields = {"method", "scope", "status", "candidate_value", "source", "atoms", "cube", "restricted_source",
              "target", "rules", "steps"}
    _require(set(public) == fields and public["method"] == "restricted_cube" and public["scope"] == SCOPE and
             type(public["candidate_value"]) is bool and public["target"] == "true", "invalid transaction proof")
    steps = public["steps"]
    _require(isinstance(steps, list) and len(steps) <= MAX_STEPS and len(_json(public)) <= MAX_CHARS,
             "full transaction proof exceeds feedback budget")
    _require(public["status"] == ("checked_rewrite" if steps else "checked_identity"), "wrong proof kind")
    residual = _residual(public["source"], public["atoms"], public["cube"])
    _require(residual == public["restricted_source"], "changed restricted transaction term")
    schemas, _ = _rules(public["rules"])
    current = _plain(residual)
    vocabulary = _symbols(current)
    for step in steps:
        current = _apply(current, step, schemas, vocabulary)
    _require(current == "true" and {step["rule"] for step in steps} == set(schemas), "incomplete transaction proof")
    return True


def _unavailable(reason, evidence=None):
    return {"public": {"status": "unavailable", "reason": reason}, "evidence": evidence}


def _assess(bound, request, graph, transport):
    _require(request == {"term": bound["restricted_source"], "pattern_rules": RULES},
             "unexpected restricted transaction query")
    schemas, rows = _rules(RULES)
    evidence = {"engine_request": request, "engine": graph, "transport": transport,
                "typed_smt2_sha256": bound["typed_smt2_sha256"], "typed_scope": TYPED_SCOPE,
                "cube_implies_signed_candidate": "unsat", "rule_truth_table_rows": rows}
    if transport == "timeout":
        _require(graph is None, "timeout carries a purported complete graph")
        evidence["timeout_seconds"] = TIMEOUT_SECONDS
        return _unavailable("engine_process_timeout", evidence)
    fields = {"source", "target", "merged", "stop_reason", "explanation", "enodes", "eclasses", "iterations"}
    _require(transport == "completed" and isinstance(graph, dict) and set(graph) == fields and
             graph["source"] == request["term"] and graph["target"] == "true" and type(graph["merged"]) is bool,
             "unexpected transaction cube graph or target")
    _require(all(type(graph[k]) is int and graph[k] > 0 for k in ("enodes", "eclasses", "iterations")),
             "invalid graph counters")
    stop = graph["stop_reason"]
    limited = bool(re.fullmatch(r"Some\((?:Time|Node|Iteration)Limit\([0-9eE.+-]+\)\)", stop))
    _require(limited or stop in ('Some(Other("TargetsMerged"))', "Some(Saturated)"), "unknown egg stop reason")
    if not graph["merged"]:
        _require((limited or stop == "Some(Saturated)") and graph["explanation"] is None and
                 graph["source"] != "true", "inconsistent nonmerge evidence")
        return _unavailable("engine_resource_limit" if limited else "goal_not_proved", evidence)
    steps = _checked_steps(graph["source"], graph["explanation"], schemas)
    evidence["checked_steps"] = steps
    used = {s["rule"] for s in steps}
    public = {"method": "restricted_cube", "scope": SCOPE, "status": "checked_rewrite" if steps else "checked_identity",
              **{k: bound[k] for k in ("source", "atoms", "cube", "candidate_value", "restricted_source")},
              "target": "true", "rules": [dict(r) for r in RULES if r["name"] in used], "steps": steps}
    if len(steps) > MAX_STEPS or len(_json(public)) > MAX_CHARS:
        return _unavailable("complete_proof_exceeds_budget", evidence)
    replay_public(public)
    return {"public": public, "evidence": evidence}


def certify(diagnosis, binary):
    bound = _bound(diagnosis)
    if bound is None:
        return _unavailable("no_sufficient_common_cube")
    request = {"term": bound["restricted_source"], "pattern_rules": [dict(rule) for rule in RULES]}
    try:
        proc = subprocess.run([str(Path(binary).resolve(strict=True))], input=_json(request), capture_output=True,
                              text=True, check=True, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        return _assess(bound, request, None, "timeout")
    return _assess(bound, request, json.loads(proc.stdout), "completed")


def verify_certificate(diagnosis, cert):
    """Bind the archived SMT receipt to this exact input, then replay the complete real egg result and public packet."""
    bound = _bound(diagnosis)
    if bound is None:
        expected = _unavailable("no_sufficient_common_cube")
    else:
        evidence = cert["evidence"]
        expected = _assess(bound, evidence["engine_request"], evidence["engine"], evidence["transport"])
    _require(_json(expected) == _json(cert), "transaction certificate differs from bound evidence")
    return True
