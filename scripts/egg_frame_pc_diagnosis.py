"""Explain one observed candidate verdict using only that formula and its sampled pins."""
from collections.abc import Mapping
import hashlib
import json

from egg_frame_diagnostic_baseline import minimum_cube
from egg_frame_observe import sample
from egg_frame_terms import (
    BOOL_NAMES, BV_WIDTHS, abstract, format_term, parse_term, referenced_signals, z3_env, z3_term,
)


def _pins(node, values):
    if not isinstance(values, Mapping) or set(values) - (BOOL_NAMES | BV_WIDTHS.keys()):
        raise ValueError("expected only sampled frame_task pin values")
    result = {}
    for name in sorted(referenced_signals(node)):
        value = values.get(name)
        if value is None or type(value) is int and value == -1:
            result[name] = None
        elif name in BOOL_NAMES:
            if type(value) not in (int, bool) or value not in (0, 1):
                raise ValueError(f"invalid sampled Boolean {name}")
            result[name] = bool(value)
        else:
            if type(value) is not int or not 0 <= value < 1 << BV_WIDTHS[name]:
                raise ValueError(f"invalid sampled bit-vector {name}")
            result[name] = value
    return result


def verify_cube(typed_source, cube, values):
    """Rebind every archived literal to the signed source and check for a full-width counterexample.

    Returns the exact SMT-LIB query and its status. A SAT result refutes sufficiency.
    Duplicate, unknown or unobserved literals are rejected before solving.
    """
    import z3
    node = parse_term(typed_source)
    _, atoms = abstract(node)
    physical = {k: -1 if v is None else v for k, v in _pins(node, values).items()}
    if sample(node, physical) is not True:
        raise ValueError("signed candidate is not known true on the supplied sample")
    if not isinstance(cube, (list, tuple)):
        raise ValueError("expected a sequence of signed primitive literals")
    env = z3_env()
    constraints = []
    seen = set()
    for pair in cube:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError("expected an atom name and Boolean polarity")
        name, polarity = pair
        if not isinstance(name, str) or name not in atoms or name in seen or type(polarity) is not bool:
            raise ValueError("invalid, duplicate, or foreign candidate literal")
        if sample(atoms[name], physical) is not polarity:
            raise ValueError("cube literal does not match a known sample value")
        seen.add(name)
        expr = z3_term(atoms[name], env)
        constraints.append(expr if polarity else z3.Not(expr))

    # Only cube literals constrain this symbolic query. Fixing the whole observed
    # bus snapshot here would allow an insufficient cube to pass.
    query = z3.And(*constraints, z3.Not(z3_term(node, env)))
    timeout_ms = 2000
    commands = ["(set-logic QF_BV)", f"(set-option :timeout {timeout_ms})"]
    for name in sorted(referenced_signals(node)):
        sort = "Bool" if name in BOOL_NAMES else f"(_ BitVec {BV_WIDTHS[name]})"
        commands.append(f"(declare-fun {name} () {sort})")
    commands += [f"(assert {query.sexpr()})", "(check-sat)"]
    smt2 = "\n".join(commands) + "\n"
    solver = z3.SolverFor("QF_BV")
    solver.from_string(smt2)
    solver.set(timeout=timeout_ms)
    status = solver.check()
    receipt = {"status": str(status), "logic": "QF_BV", "z3": z3.get_version_string(),
               "timeout_ms": timeout_ms, "sampled_literals_checked": len(seen), "smt2": smt2,
               "smt2_sha256": hashlib.sha256(smt2.encode()).hexdigest()}
    if status == z3.unknown:
        receipt["reason_unknown"] = solver.reason_unknown()
    return receipt


def diagnose(candidate, values, candidate_value):
    """Find an independently sufficient explanation of this observed candidate verdict.

    A false observed verdict is explained by the negated candidate. Only a
    sufficient result carries a cube. Its size is minimal in the independent
    Boolean-atom model; the full-width solver separately checks soundness.
    """
    if type(candidate_value) is not bool:
        raise ValueError("candidate_value must be an observed Boolean verdict")
    parsed = parse_term(candidate)
    signed = parsed if candidate_value else ("not", parsed)
    typed_source = format_term(signed)
    source, atoms = abstract(signed)
    pins = _pins(signed, values)
    physical = {k: -1 if v is None else v for k, v in pins.items()}
    observed = sample(signed, physical)
    assignment = {name: sample(node, physical) for name, node in sorted(atoms.items())}
    public = {"status": "sample_unknown" if observed is None else "sample_mismatch",
              "candidate_value": candidate_value, "literal_count": None, "sufficient_literals": []}
    oracle = {"status": "not_run", "signed_source_at_sample": observed,
              "minimum_cube": None, "typed_implication": None}
    result = {"candidate": candidate, "typed_source": typed_source, "source": source,
              "atoms": {k: format_term(v) for k, v in sorted(atoms.items())}, "sample": pins,
              "assignment": assignment, "cube": None, "public": public, "oracle": oracle}
    if observed is not True:
        return result
    minimum = minimum_cube(source, assignment)
    oracle["minimum_cube"] = {k: v for k, v in minimum.items() if k != "cube"}
    if minimum["status"] != "sufficient":
        # Exact partial typed observations can be true even when the independent
        # Boolean abstraction admits both outcomes (e.g. correlated bus comparisons).
        if minimum["status"] == "false":
            raise ValueError("candidate abstraction contradicts its determinate physical verdict")
        public["status"] = minimum["status"]
        return result
    cube = [[name, polarity] for name, polarity in minimum["cube"]]
    if minimum["size"] != len(cube):
        raise ValueError("minimum-cube certificate size mismatch")
    receipt = verify_cube(typed_source, cube, pins)
    oracle.update(status=receipt["status"], typed_implication=receipt)
    if receipt["status"] == "sat":
        raise ValueError("proposed cube does not imply the signed candidate")
    if receipt["status"] != "unsat":
        public["status"] = "oracle_unknown"
        return result
    result["cube"] = cube
    public.update(status="sufficient", literal_count=len(cube),
                  sufficient_literals=[{"term": format_term(atoms[k]), "value": v} for k, v in cube])
    return result


def verify_diagnosis_record(archived, fresh):
    """Bind a saved diagnosis to a fresh one, tolerating SMT printer differences only.

    A universally UNSAT unrelated query is *not* a valid receipt for this cube.
    Parse the assertion ASTs before comparing, so let aliases and whitespace
    can vary across pinned Z3 builds without weakening the endpoint binding.
    """
    import z3

    def canon(value):
        return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)

    if set(archived) != set(fresh) or any(canon(archived[k]) != canon(fresh[k]) for k in fresh if k != "oracle"):
        raise ValueError("diagnosis not bound to the exact candidate and observation")
    old, new = archived["oracle"], fresh["oracle"]
    if set(old) != set(new) or any(canon(old[k]) != canon(new[k]) for k in new if k != "typed_implication"):
        raise ValueError("diagnosis oracle changed")
    a, b = old["typed_implication"], new["typed_implication"]
    if a is None or b is None:
        if a != b:
            raise ValueError("typed implication receipt changed")
        return True
    if (set(a) != set(b) or not isinstance(a.get("z3"), str) or not a["z3"] or
        any(canon(a[k]) != canon(b[k]) for k in b if k not in ("smt2", "smt2_sha256", "z3")) or
        not isinstance(a.get("smt2"), str) or hashlib.sha256(a["smt2"].encode()).hexdigest() != a["smt2_sha256"]):
        raise ValueError("typed implication receipt changed")
    try:
        old_ast = z3.parse_smt2_string(a["smt2"])
        new_ast = z3.parse_smt2_string(b["smt2"])
        identical = len(old_ast) == len(new_ast) and all(x.eq(y) for x, y in zip(old_ast, new_ast))
    except z3.Z3Exception as exc:
        raise ValueError("typed implication receipt changed") from exc
    if not identical:
        raise ValueError("typed implication receipt changed: assertion AST differs")
    return True
