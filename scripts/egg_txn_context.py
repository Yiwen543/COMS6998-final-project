"""Source-selected transaction partitions and replayable contextual primitive comparison facts."""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json

import z3
from z3.z3util import get_vars

from egg_txn_terms import BV_WIDTHS, CMP_OPS, abstract, format_term, parse_term, z3_env, z3_term
from predicates import parse


SCOPE = "txn-context-v1: unrestricted two-state transaction fields with declared unsigned widths"
TIMEOUT_MS = 5000
_REVERSED = {"eq": "eq", "ne": "ne", "ult": "ugt", "ule": "uge", "ugt": "ult", "uge": "ule"}


def _digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(data).hexdigest()


def prepare(left, right):
    """Abstract both endpoints in the same primitive comparison namespace."""
    sources = []
    atoms = {}
    for text in (left, right):
        projected, bindings = abstract(parse_term(text))
        sources.append(projected)
        for name, term in bindings.items():
            rendered = format_term(term)
            if atoms.setdefault(name, rendered) != rendered:
                raise ValueError("primitive atom has conflicting typed sources")
    return {"left": left, "right": right, "abstracts": sources, "atoms": dict(sorted(atoms.items()))}


def _comparisons(node):
    """Collect only explicit primitive comparators, orienting comparisons by bus name."""
    thresholds = defaultdict(set)
    cross = set()

    def visit(term):
        if not isinstance(term, tuple):
            return
        op, *args = term
        if op in CMP_OPS:
            a, b = args
            if type(a) is int:
                op, a, b = _REVERSED[op], b, a
            if isinstance(a, str) and a in BV_WIDTHS:
                if type(b) is int:
                    thresholds[a, b].add(op)
                elif isinstance(b, str) and b in BV_WIDTHS and a != b:
                    cross.add((op, a, b) if a < b else (_REVERSED[op], b, a))
        for arg in args:
            visit(arg)

    visit(node)
    return thresholds, cross


def _select(left, right):
    (lt, lc), (rt, rc) = (_comparisons(parse_term(s)) for s in (left, right))
    cross_variables = {name for _, a, b in lc ^ rc for name in (a, b)}
    choices = []
    for variable, value in lt.keys() & rt.keys():
        lops, rops = lt[variable, value], rt[variable, value]
        a, b = lops - rops, rops - lops
        if not (a or b) and variable not in cross_variables:
            continue
        strict_change = any((op in a and inclusive in b) or (inclusive in a and op in b)
                            for op, inclusive in (("ult", "ule"), ("ugt", "uge")))
        priority = (0 if strict_change else 1 if (a | b) & {"eq", "ne"} else
                    2 if a or b else 3)
        choices.append((priority, -len(a | b), variable, value))
    if not choices:
        return None
    _, _, variable, value = min(choices)
    return {"variable": variable, "width": BV_WIDTHS[variable], "value": value}


def _check(expr):
    """Archive the submitted formula, including its declarations, and solve that exact text."""
    fields = sorted(get_vars(expr), key=lambda var: var.decl().name())
    commands = ["(set-logic QF_BV)", f"(set-option :timeout {TIMEOUT_MS})"]
    commands += [f"(declare-fun {v.decl().name()} () {v.sort().sexpr()})" for v in fields]
    commands += [f"(assert {expr.sexpr()})", "(check-sat)"]
    smt2 = "\n".join(commands) + "\n"
    solver = z3.SolverFor("QF_BV")
    solver.from_string(smt2)
    solver.set(timeout=TIMEOUT_MS)
    status = solver.check()
    record = {"status": str(status), "logic": "QF_BV", "z3": z3.get_version_string(),
              "timeout_ms": TIMEOUT_MS, "smt2": smt2, "smt2_sha256": sha256(smt2.encode()).hexdigest()}
    if status == z3.unknown:
        record["reason"] = solver.reason_unknown()
    return record, solver.model() if status == z3.sat else None


def _guard_id(guard):
    return _digest({"guard": guard, "scope": SCOPE})


def contexts(left, right, *, split):
    """Certify coverage/disjointness on unrestricted words, independent of both target verdicts."""
    if type(split) is not bool:
        raise ValueError("expected Boolean split switch")
    # Parse even when the no-split policy is selected.
    parse_term(left)
    parse_term(right)
    threshold = _select(left, right) if split else None
    guards = ["true"] if threshold is None else [
        f"({op} {threshold['variable']} {threshold['value']})" for op in ("ult", "eq", "ugt")]
    env = z3_env()
    formulas = [z3_term(parse_term(g), env) for g in guards]
    branches = [{"id": _guard_id(g), "guard": g, "feasibility": _check(v)[0]} for g, v in zip(guards, formulas)]
    coverage = _check(z3.Not(z3.Or(*formulas)))[0]
    disjoint = [{"contexts": [branches[i]["id"], branches[j]["id"]],
                 "query": _check(z3.And(formulas[i], formulas[j]))[0]}
                for i, j in combinations(range(len(guards)), 2)]
    if (coverage["status"] != "unsat" or any(p["query"]["status"] != "unsat" for p in disjoint)
            or any(c["feasibility"]["status"] not in ("sat", "unsat") for c in branches)):
        raise ValueError("could not independently certify partition and classify every guard")
    return {"scope": SCOPE, "split": split, "threshold": threshold, "contexts": branches,
            "coverage": coverage, "disjoint": disjoint}


def _check_prepared(prepared):
    if not isinstance(prepared, dict) or not isinstance(prepared.get("left"), str) or not isinstance(prepared.get("right"), str):
        raise ValueError("expected both transaction sources")
    if prepared != prepare(prepared["left"], prepared["right"]):
        raise ValueError("abstract endpoints or typed atom table changed")


def _verify_query(record, expected):
    """Match saved assertion ASTs with the fresh query; the SAT label alone has no authority."""
    if (not isinstance(record, dict) or record.keys() != expected.keys()
            or not isinstance(record.get("smt2"), str) or not isinstance(record.get("z3"), str) or not record["z3"]
            or record["smt2_sha256"] != sha256(record["smt2"].encode()).hexdigest()
            or any(record[k] != expected[k] for k in expected if k not in ("smt2", "smt2_sha256", "z3"))):
        raise ValueError("SMT receipt metadata or status mismatch")
    try:
        old = z3.parse_smt2_string(record["smt2"])
        fresh = z3.parse_smt2_string(expected["smt2"])
    except z3.Z3Exception as exc:
        raise ValueError("invalid SMT receipt") from exc
    if len(old) != 1 or len(fresh) != 1 or not old[0].eq(fresh[0]):
        raise ValueError("archived SMT assertion does not match its source obligation")


def _checked_branch(context, env):
    if not isinstance(context, dict) or set(context) != {"id", "guard", "feasibility"}:
        raise ValueError("expected one certified context")
    guard = context["guard"]
    if not isinstance(guard, str) or context["id"] != _guard_id(guard):
        raise ValueError("changed guard or context identifier")
    node = parse_term(guard)
    if guard != "true" and not (
        isinstance(node, tuple) and node[0] in ("ult", "eq", "ugt") and len(node) == 3 and
        isinstance(node[1], str) and node[1] in BV_WIDTHS and type(node[2]) is int and format_term(node) == guard
    ):
        raise ValueError("context is not an allowed unsigned threshold guard")
    formula = z3_term(node, env)
    fresh, _ = _check(formula)
    if fresh["status"] not in ("sat", "unsat"):
        raise ValueError("unknown context feasibility")
    _verify_query(context["feasibility"], fresh)
    return formula


def verify_partition(plan, prepared):
    _check_prepared(prepared)
    if not isinstance(plan, dict) or type(plan.get("split")) is not bool:
        raise ValueError("invalid partition")
    expected = contexts(prepared["left"], prepared["right"], split=plan["split"])
    if (plan.keys() != expected.keys() or any(plan[k] != expected[k] for k in ("scope", "split", "threshold"))
            or not isinstance(plan["contexts"], list) or len(plan["contexts"]) != len(expected["contexts"])
            or not isinstance(plan["disjoint"], list) or len(plan["disjoint"]) != len(expected["disjoint"])):
        raise ValueError("partition differs from deterministic source-selected cases")
    _verify_query(plan["coverage"], expected["coverage"])
    for old, new in zip(plan["contexts"], expected["contexts"]):
        if (not isinstance(old, dict) or old.keys() != new.keys()
                or old["id"] != new["id"] or old["guard"] != new["guard"]):
            raise ValueError("partition guard differs from its source-selected guard")
        _verify_query(old["feasibility"], new["feasibility"])
    for old, new in zip(plan["disjoint"], expected["disjoint"]):
        if not isinstance(old, dict) or old.keys() != new.keys() or old["contexts"] != new["contexts"]:
            raise ValueError("partition disjointness endpoints changed")
        _verify_query(old["query"], new["query"])
    return True


def _root_literal(text):
    term = parse(text)
    while isinstance(term, tuple) and term[0] == "not":
        term = term[1]
    return term if isinstance(term, str) else None


def certify_facts(prepared, context):
    """Select a signed forest of primitive BV facts. Each emitted edge has its own typed XOR proof."""
    _check_prepared(prepared)
    env = z3_env()
    guard = _checked_branch(context, env)
    facts, receipts = [], {}
    counts = {"eligible_atoms": 0, "constant_queries": 0, "pair_queries": 0,
              "skipped_direct_pairs": 0, "sat": 0, "unsat": 0, "unknown": 0}
    sources = prepared["atoms"]
    atoms = {key: z3_term(parse_term(source), env) for key, source in sources.items() if key.startswith("bv_")}
    counts["eligible_atoms"] = len(atoms)
    result = {"facts": facts, "receipts": receipts, "counts": counts}
    if context["feasibility"]["status"] == "unsat":
        return result
    roots = {_root_literal(s) for s in prepared["abstracts"]}

    def certify(left, right, right_source, formula, counter):
        counts[counter] += 1
        record, _ = _check(z3.And(guard, z3.Xor(atoms[left], formula)))
        counts[record["status"]] += 1
        if record["status"] != "unsat":
            return False
        name = "ctx-" + _digest([context["id"], left, right])[:24]
        if name in receipts:
            raise ValueError("ground rule identifier collision")
        facts.append({"name": name, "left": left, "right": right,
                      "event_context": context["id"], "proof_status": "unsat"})
        receipts[name] = {"guard": context["guard"], "typed_left": sources[left],
                          "typed_right": right_source, "query": record}
        return True

    remaining = []
    for atom in atoms:
        if atom in roots and roots & {"true", "false"}:
            # Checking either polarity against a constant would query the direct literal goal.
            counts["skipped_direct_pairs"] += 1
            remaining.append(atom)
            continue
        for fixed in (True, False):
            text = "true" if fixed else "false"
            if certify(atom, text, text, z3.BoolVal(fixed), "constant_queries"):
                break
        else:
            remaining.append(atom)

    # Members relate directly to the first representative of a signed class; queries
    # between two known members add no new information. Constants have already left.
    representatives = []
    for atom in remaining:
        for rep in representatives:
            if roots == {atom, rep}:
                counts["skipped_direct_pairs"] += 1
                continue
            if certify(atom, rep, sources[rep], atoms[rep], "pair_queries"):
                break
            if certify(atom, f"(not {rep})", f"(not {sources[rep]})", z3.Not(atoms[rep]), "pair_queries"):
                break
        else:
            representatives.append(atom)
    return result


def verify_facts(prepared, context, result):
    fresh = certify_facts(prepared, context)
    if (not isinstance(result, dict) or result.keys() != fresh.keys() or result["facts"] != fresh["facts"]
            or result["counts"] != fresh["counts"] or not isinstance(result["receipts"], dict)
            or result["receipts"].keys() != fresh["receipts"].keys()):
        raise ValueError("local rule inventory or discovery accounting changed")
    for name, check in fresh["receipts"].items():
        saved = result["receipts"][name]
        if (not isinstance(saved, dict) or saved.keys() != check.keys()
                or any(saved[k] != check[k] for k in ("guard", "typed_left", "typed_right"))):
            raise ValueError("local rule is not bound to its typed sources and context")
        _verify_query(saved["query"], check["query"])
    return True


def _proposition(term):
    if isinstance(term, str):
        if term in ("true", "false"):
            return z3.BoolVal(term == "true")
        return z3.Bool(term)
    op, *args = term
    return {"and": z3.And, "or": z3.Or, "not": z3.Not}[op](*(_proposition(arg) for arg in args))


def ordinary(prepared, context, result):
    """Complete propositional solver over the same certified ground facts and endpoints."""
    _check_prepared(prepared)
    env = z3_env()
    _checked_branch(context, env)
    # The caller can audit all discovery counts with verify_facts. Independently check
    # each actual premise here so an arbitrary typed equation cannot enter this baseline.
    assumptions = []
    roots = {_root_literal(s) for s in prepared["abstracts"]}
    if context["feasibility"]["status"] == "unsat" and result["facts"]:
        raise ValueError("empty context must carry zero facts")
    for fact in result["facts"]:
        name, left, right = fact["name"], fact["left"], fact["right"]
        rhs = parse(right)
        endpoint = _root_literal(right)
        if (left not in prepared["atoms"] or not left.startswith("bv_")
                or endpoint is None or endpoint == left
                or endpoint not in ("true", "false") and (endpoint not in prepared["atoms"] or not endpoint.startswith("bv_"))
                or roots == {left, endpoint} or left in roots and roots & {"true", "false"}
                or name != "ctx-" + _digest([context["id"], left, right])[:24]):
            raise ValueError("propositional premise is outside the admitted primitive fragment")
        if isinstance(rhs, tuple):
            if rhs[0] != "not" or not isinstance(rhs[1], str) or rhs[1] not in prepared["atoms"]:
                raise ValueError("invalid signed local fact")
            typed_right = f"(not {prepared['atoms'][rhs[1]]})"
        elif rhs in ("true", "false"):
            typed_right = rhs
        else:
            typed_right = prepared["atoms"][rhs]
        receipt = result["receipts"][name]
        if (fact["event_context"] != context["id"] or fact["proof_status"] != "unsat"
                or receipt["guard"] != context["guard"] or receipt["typed_left"] != prepared["atoms"][left]
                or receipt["typed_right"] != typed_right):
            raise ValueError("unbound propositional premise")
        proof, _ = _check(z3.And(z3_term(parse_term(context["guard"]), env),
                                 z3.Xor(z3_term(parse_term(receipt["typed_left"]), env),
                                        z3_term(parse_term(typed_right), env))))
        _verify_query(receipt["query"], proof)
        if proof["status"] != "unsat":
            raise ValueError("unverified propositional premise")
        assumptions.append(_proposition(left) == _proposition(rhs))

    a, b = (_proposition(parse(s)) for s in prepared["abstracts"])
    empty = context["feasibility"]["status"] == "unsat"
    expr = z3.BoolVal(False) if empty else z3.And(*assumptions, z3.Xor(a, b))
    query, model = _check(expr)
    counterexample = None
    if model is not None:
        counterexample = {k: z3.is_true(model.eval(z3.Bool(k), model_completion=True)) for k in prepared["atoms"]}
    return {**query, "equivalent": {"sat": False, "unsat": True}.get(query["status"]),
            "abstract_counterexample": counterexample, "vacuous": empty}
