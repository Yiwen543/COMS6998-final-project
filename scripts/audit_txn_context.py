#!/usr/bin/env python3
"""Rebuild transaction-context proof obligations from exact typed endpoints."""
from collections import Counter, defaultdict
import argparse
import gzip
import hashlib
import json
from itertools import combinations
from pathlib import Path

import z3
from z3.z3util import get_vars

from egg_frame_terms import format_term
from egg_txn_terms import BV_WIDTHS, CMP_OPS, abstract, evaluate_term, parse_term, z3_env, z3_term
from m3_proof_dependencies import _plain
from predicates import ROOT, evaluate


SCOPE = "txn-context-v1: unrestricted two-state transaction fields with declared unsigned widths"
SWAP = {"eq": "eq", "ne": "ne", "ult": "ugt", "ugt": "ult", "ule": "uge", "uge": "ule"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _match(actual, expected, label):
    require(_json(actual) == _json(expected), f"{label} differs from the reconstructed evidence")


def bind_pair(left, right, prepared):
    """Derive each canonical primitive, including its typed polarity, from the source strings."""
    ast = [parse_term(text) for text in (left, right)]
    lowered = [abstract(node) for node in ast]
    atoms = {}
    for _, mapping in lowered:
        for key, term in mapping.items():
            require(atoms.setdefault(key, format_term(term)) == format_term(term), "canonical atom collision")
    for key, expected in (("left", left), ("right", right), ("abstracts", [entry[0] for entry in lowered]),
                          ("atoms", atoms)):
        _match(prepared[key], expected, "prepared " + key)
    return ast


def _tests(tree):
    scalar, cross = defaultdict(set), set()
    pending = [tree]
    while pending:
        node = pending.pop()
        if not isinstance(node, tuple):
            continue
        pending.extend(node[1:])
        if node[0] not in CMP_OPS:
            continue
        op, a, b = node
        if type(a) is int:
            a, b, op = b, a, SWAP[op]
        if isinstance(a, str) and a in BV_WIDTHS and type(b) is int:
            scalar[a, b].add(op)
        elif isinstance(a, str) and isinstance(b, str) and a != b and a in BV_WIDTHS and b in BV_WIDTHS:
            cross.add((op, a, b) if a < b else (SWAP[op], b, a))
    return scalar, cross


def _threshold(trees):
    (a, x), (b, y) = map(_tests, trees)
    cross = {var for _, l, r in x ^ y for var in (l, r)}
    options = []
    for key in a.keys() & b.keys():
        l, r = a[key] - b[key], b[key] - a[key]
        if not (l or r or key[0] in cross):
            continue
        strict = any((i in l and j in r) or (i in r and j in l) for i, j in (("ult", "ule"), ("ugt", "uge")))
        rank = 0 if strict else 1 if (l | r) & {"eq", "ne"} else 2 if l or r else 3
        options.append((rank, -len(l | r), key))
    if not options:
        return None
    var, k = min(options)[2]
    return {"variable": var, "width": BV_WIDTHS[var], "value": k}


def _ctx_id(guard):
    return hashlib.sha256(_json({"scope": SCOPE, "guard": guard}).encode()).hexdigest()


def _fresh(assertions):
    solver = z3.Solver()
    solver.set(timeout=5000)
    solver.add(*assertions)
    result = str(solver.check())
    require(result in ("sat", "unsat"), "independent SMT check was inconclusive")
    return result


def _receipt(receipt, assertions, required=None):
    """Bind asserted ASTs structurally. Logical equivalence alone cannot distinguish two UNSAT queries."""
    text = receipt["smt2"]
    require(isinstance(text, str), "expected SMT-LIB text")
    if "smt2_sha256" in receipt:
        _match(receipt["smt2_sha256"], hashlib.sha256(text.encode()).hexdigest(), "SMT digest")
    try:
        parsed = list(z3.parse_smt2_string(text))
    except z3.Z3Exception as exc:
        raise ValueError("invalid SMT-LIB receipt") from exc
    require(len(parsed) == len(assertions), "SMT receipt assertion count differs")
    for p, a in zip(parsed, assertions):
        if not p.eq(a):
            # The SMT-LIB pretty printer can flatten nested AND/OR nodes. Compare the
            # parsed serialization of the reconstructed query without solving it away.
            vars_by_name = {v.decl().name(): v for v in get_vars(a)}
            serialized = z3.parse_smt2_string("(assert " + a.sexpr() + ")", decls=vars_by_name)
            if not p.eq(serialized[0]):
                # The archived whole-pair oracle uses Solver.to_smt2 rather than
                # ExprRef.sexpr; its benchmark printer wraps some DISTINCT nodes
                # in "(and ... true)". Re-serialize the exact expected expression.
                printer = z3.Solver()
                printer.add(a)
                benchmark = z3.parse_smt2_string(printer.to_smt2())
                require(len(benchmark) == 1 and p.eq(benchmark[0]),
                        "SMT receipt assertions do not match the reconstructed obligation")
    status = _fresh(assertions)
    require(receipt["status"] == status and (required is None or status == required),
            "SMT status disagrees with replay")
    return status


def verify_partition(prepared, plan):
    trees = [parse_term(prepared[key]) for key in ("left", "right")]
    require(type(plan["split"]) is bool and plan["scope"] == SCOPE, "incorrect partition policy or domain")
    threshold = _threshold(trees) if plan["split"] else None
    _match(plan["threshold"], threshold, "threshold")
    guards = ["true"] if threshold is None else [
        f"({op} {threshold['variable']} {threshold['value']})" for op in ("ult", "eq", "ugt")]
    rows = plan["contexts"]
    _match([row["guard"] for row in rows], guards, "ordered branch guards")
    env = z3_env()
    formulas = [z3_term(parse_term(g), env) for g in guards]
    ids = [_ctx_id(g) for g in guards]
    _match([row["id"] for row in rows], ids, "structural context identities")
    feasible = [_receipt(row["feasibility"], [p]) == "sat" for row, p in zip(rows, formulas)]
    _receipt(plan["coverage"], [z3.Not(z3.Or(*formulas))], "unsat")
    pairs = list(combinations(range(len(rows)), 2))
    _match([item["contexts"] for item in plan["disjoint"]], [[ids[i], ids[j]] for i, j in pairs],
           "disjointness pair inventory")
    for item, (i, j) in zip(plan["disjoint"], pairs):
        _receipt(item["query"], [z3.And(formulas[i], formulas[j])], "unsat")
    return feasible


def _literal(node):
    while isinstance(node, tuple) and node[0] == "not":
        node = node[1]
    return node if isinstance(node, str) else None


def _rhs(text, atoms):
    term = _plain(text)
    base = term[1] if isinstance(term, tuple) and term[0] == "not" else term
    require(isinstance(base, str) and (base in atoms or base in ("true", "false")), "foreign fact endpoint")
    if isinstance(term, tuple):
        require(base in atoms, "negated fact endpoint must be a source atom")
    return base, isinstance(term, tuple)


def _facts(prepared, context, recorded):
    facts, receipts = recorded["facts"], recorded["receipts"]
    names = [fact["name"] for fact in facts]
    require(len(names) == len(set(names)) and set(names) == set(receipts), "fact and receipt inventories differ")
    source = prepared["atoms"]
    roots = [_literal(_plain(s)) for s in prepared["abstracts"]]
    env = z3_env()
    guard = z3_term(parse_term(context["guard"]), env)
    seen = set()
    for fact in facts:
        l = fact["left"]
        r, negated = _rhs(fact["right"], source)
        require(l in source and l.startswith("bv_") and (r in ("true", "false") or r.startswith("bv_"))
                and r != l and fact["event_context"] == context["id"] and
                fact["proof_status"] == "unsat", "invalid or cross-context primitive equality")
        expected_name = "ctx-" + hashlib.sha256(_json([context["id"], l, fact["right"]]).encode()).hexdigest()[:24]
        require(fact["name"] == expected_name, "ground rule identifier is not bound to its context and endpoints")
        endpoints = (frozenset((l, r)), negated)
        require(endpoints not in seen, "duplicate ground equality")
        seen.add(endpoints)
        if all(x is not None for x in roots):
            require(set(roots) != {l, r}, "a ground fact directly queried the two task endpoints")
            require(not (r in ("true", "false") and l in roots and set(roots) & {"true", "false"}),
                    "standalone atom compared against the task's constant target")
        typed_left = source[l]
        typed_right = source.get(r, r)
        if negated:
            typed_right = f"(not {typed_right})"
        receipt = receipts[fact["name"]]
        _match([receipt["guard"], receipt["typed_left"], receipt["typed_right"]],
               [context["guard"], typed_left, typed_right], "fact query guard/typed endpoints")
        same = z3.Xor(z3_term(parse_term(typed_left), env), z3_term(parse_term(typed_right), env))
        _receipt(receipt["query"], [z3.And(guard, same)], "unsat")


def _propositional(node):
    if isinstance(node, str):
        return z3.BoolVal(node == "true") if node in ("true", "false") else z3.Bool(node)
    op = {"and": z3.And, "or": z3.Or, "not": z3.Not}[node[0]]
    return op(*map(_propositional, node[1:]))


def _ordinary(prepared, facts, receipt):
    trees = [_plain(s) for s in prepared["abstracts"]]
    relations = [(_plain(f["left"]), _plain(f["right"])) for f in facts]
    body = z3.And(*[_propositional(a) == _propositional(b) for a, b in relations],
                  z3.Xor(*map(_propositional, trees)))
    status = _receipt(receipt, [body])
    require(receipt["equivalent"] is (status == "unsat") and receipt["vacuous"] is False,
            "ordinary decision differs from complete Boolean SMT")
    assignment = receipt["abstract_counterexample"]
    if status == "sat":
        require(isinstance(assignment, dict) and set(assignment) == set(prepared["atoms"]) and
                all(type(v) is bool for v in assignment.values()), "invalid ordinary Boolean countermodel")
        require(all(evaluate(a, assignment) == evaluate(b, assignment) for a, b in relations) and
                evaluate(trees[0], assignment) != evaluate(trees[1], assignment), "ordinary countermodel fails replay")
    else:
        require(assignment is None, "an UNSAT ordinary query carries a countermodel")
    return status == "unsat"


def _oracle(left, right, oracle):
    env = z3_env()
    a, b = map(parse_term, (left, right))
    outcome = _receipt(oracle, [z3.Xor(z3_term(a, env), z3_term(b, env))])
    require(oracle["equivalent"] is (outcome == "unsat"), "typed XOR verdict differs")
    if outcome == "sat":
        values = oracle["counterexample"]
        require(isinstance(values, dict) and values.keys() == env.keys(), "incomplete typed distinguishing witness")
        for pin, symbol in env.items():
            value = values[pin]
            valid = type(value) is bool if z3.is_bool(symbol) else type(value) is int and 0 <= value < 1 << symbol.size()
            require(valid, f"typed counterexample pin outside its declared sort: {pin}")
        x, y = [evaluate_term(t, values) for t in (a, b)]
        require(x != y and oracle["reference_value"] is x and oracle["candidate_value"] is y,
                "typed distinguishing witness fails exact endpoint replay")
    else:
        require(all(oracle[key] is None for key in ("counterexample", "reference_value", "candidate_value")),
                "UNSAT typed comparison carries counterexample values")
    return outcome


def audit_pair(left, right, prepared, plan, branches, pattern_rules):
    """Replay one archived method for a source pair; a global result needs every feasible branch."""
    from egg_txn_context_check import check_graph
    from egg_txn_context import verify_facts
    bind_pair(left, right, prepared)
    feasible = verify_partition(prepared, plan)
    contexts = plan["contexts"]
    require(len(contexts) == len(branches), "incomplete proof branch inventory")
    verdicts, ordinary_verdicts, local = [], [], []
    for context, branch, sat in zip(contexts, branches, feasible):
        _match(branch["context"], context, "ordered branch context")
        if not sat:
            require(branch.get("skipped") == "infeasible" and not any(
                key in branch for key in ("graph", "proof", "facts", "payload", "ordinary")),
                    "unreachable contexts must be accounted for explicitly")
            continue
        require("skipped" not in branch, "feasible branch must be independently checked")
        fact_data = branch["facts"]
        _facts(prepared, context, fact_data)
        # Reproduce the discovery inventory and counters in addition to replaying
        # every accepted fact above against independently reconstructed SMT.
        verify_facts(prepared, context, fact_data)
        payload = branch["payload"]
        require(set(payload) == {"context_id", "targets", "ground_rules", "pattern_rules"} and
                payload["context_id"] == context["id"], "incorrect ground graph context or payload inventory")
        _match(payload["targets"], [{"id": label, "compact": term, "event_context": context["id"]}
                                    for label, term in zip(("left", "right"), prepared["abstracts"])],
               "original abstract proof endpoints")
        _match(payload["ground_rules"], fact_data["facts"], "branch ground equality input")
        _match(payload["pattern_rules"], pattern_rules, "generic rules")
        ordinary = _ordinary(prepared, fact_data["facts"], branch["ordinary"])
        graph = branch["graph"]
        if graph is None:
            proof = {"status": "subprocess_timeout", "proved": False, "steps": [],
                     "stop": "subprocess_timeout", "used_ground_rules": []}
        else:
            proof = check_graph(payload, graph)
        _match(branch["proof"], proof, "proof verdict and steps")
        require(not proof["proved"] or ordinary, "accepted graph contradicts ordinary complete Boolean SMT")
        env = z3_env()
        delta = z3.Xor(z3_term(parse_term(left), env), z3_term(parse_term(right), env))
        guard = z3_term(parse_term(context["guard"]), env)
        typed = _fresh([z3.And(guard, delta)])
        require(typed != "sat" or not (proof["proved"] or ordinary),
                "a locally accepted proof contradicts a typed distinguishing assignment under its guard")
        local.append({"context": context["id"], "typed_xor": typed,
                      "proved": proof["proved"], "ordinary_proved": ordinary})
        verdicts.append(proof["proved"])
        ordinary_verdicts.append(ordinary)
    require(bool(verdicts), "exhaustive partition unexpectedly has no feasible branch")
    return {"proved": all(verdicts), "ordinary_proved": all(ordinary_verdicts),
            "feasible_branches": len(verdicts), "local": local}


def audit(directory, archive):
    from egg_txn_context_check import PATTERN_RULES
    from run_txn_context import SCOPE as EXPERIMENT_SCOPE, summarize, workload
    directory, archive = Path(directory), Path(archive)
    protocol = json.loads((directory / "protocol.json").read_bytes())
    expected = workload(archive)
    _match(protocol["cases"], expected, "frozen archive and control workload")
    _match(protocol["pattern_rules"], PATTERN_RULES, "frozen generic rule library")
    require(protocol["schema"] == 1 and protocol["scope"] == EXPERIMENT_SCOPE and
            protocol["archive_sha256"] == hashlib.sha256(archive.read_bytes()).hexdigest(),
            "scope, schema, or original response archive differs")
    frozen = ROOT / "docs/egg_txn_context_protocol.md"
    require(protocol["protocol_sha256"] == hashlib.sha256(frozen.read_bytes()).hexdigest(),
            "predeclared protocol hash differs")
    _match(protocol["limits"], {"iterations": 20, "enodes": 20000, "seconds": 5,
                                 "outer_timeout_seconds": 30, "smt_timeout_ms": 5000}, "proof limits")
    with gzip.open(directory / "cases.jsonl.gz", "rt") as stream:
        rows = [json.loads(line) for line in stream]
    _match([r["case"] for r in rows], expected, "ordered case records")
    checked = {"pairs": len(rows), "methods": 0, "feasible_graph_branches": 0,
               "infeasible_guards": 0, "ground_receipts": 0}
    local_counts = defaultdict(Counter)
    for row in rows:
        case = row["case"]
        left, right = case["left"], case["right"]
        status = _oracle(left, right, row["oracle"])
        require(case["expected_equivalent"] is (status == "unsat"), "frozen expectation disagrees with typed oracle")
        require(set(row["methods"]) == {"global", "contextual"}, "missing proof method")
        for name, method in row["methods"].items():
            require(method["plan"]["split"] is (name == "contextual"), "split policy swapped between methods")
            result = audit_pair(left, right, row["prepared"], method["plan"], method["branches"], PATTERN_RULES)
            for key in ("proved", "ordinary_proved"):
                _match(method[key], result[key], f"{case['id']} {name} global {key}")
                require(not result[key] or status == "unsat", "accepted global proof contradicts typed counterexample")
            checked["methods"] += 1
            checked["feasible_graph_branches"] += result["feasible_branches"]
            checked["infeasible_guards"] += len(method["branches"]) - result["feasible_branches"]
            checked["ground_receipts"] += sum(len(b["facts"]["receipts"]) for b in method["branches"] if "facts" in b)
            for branch in result["local"]:
                counts = local_counts[name]
                counts["typed_" + branch["typed_xor"]] += 1
                if status == "sat" and branch["typed_xor"] == "unsat":
                    counts["equivalent_branches_on_inequivalent_global_pairs"] += 1
                    counts["proved_equivalent_branches_on_inequivalent_global_pairs"] += branch["proved"]
                    counts["ordinary_proved_equivalent_branches_on_inequivalent_global_pairs"] += branch["ordinary_proved"]
    _match(json.loads((directory / "summary.json").read_bytes()), summarize(rows), "published case/aggregate decisions")
    return {"passed": True, **checked, "archive_sha256": protocol["archive_sha256"],
            "cases_sha256": hashlib.sha256((directory / "cases.jsonl.gz").read_bytes()).hexdigest(),
            "independent_local_typed_checks": {k: dict(v) for k, v in local_counts.items()},
            "new_api_calls": 0, "new_egg_runs": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", "--results", type=Path, required=True)
    parser.add_argument("--archive", type=Path, default=ROOT / "results/milestone3/frame-txn-live/transcript.tar.gz")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.dumps(audit(args.run_dir, args.archive), indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(report)
    else:
        print(report, end="")
