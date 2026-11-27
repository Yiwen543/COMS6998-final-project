"""Typed, scope-keyed SMT comparison for transaction violation monitors.

The reference/oracle solves each obligation in a separate QF_BV solver.  The
incremental competitor instead keeps a solver for each canonical context and
shares directional checks across later requests (including reversed pairs).
Neither treats absence of a witness or failure to prove as equivalence.
"""
from copy import deepcopy
from hashlib import sha256
import json

import z3
from z3.z3util import get_vars

from egg_txn_context import SCOPE, TIMEOUT_MS
from egg_txn_terms import BOOL_NAMES, BV_WIDTHS, evaluate_term, format_term, parse_term, z3_env, z3_term


TYPE_SIGNATURE = sha256(json.dumps({"scope": SCOPE, "bool": sorted(BOOL_NAMES),
                                    "bv": BV_WIDTHS}, sort_keys=True).encode()).hexdigest()
_DIRECTIONS = ("old_only", "new_only")


def _canonical(source):
    return format_term(parse_term(source))


def _validate_timeout(timeout_ms):
    if type(timeout_ms) is not int or timeout_ms < 1:
        raise ValueError("expected positive integer SMT timeout")


def classify(old_only, new_only):
    """Directional SAT outcomes have *violation* polarity, not assertion polarity.

    A new monitor is stronger when it flags every old violation *and* some
    additional ones.  SAT on an abstract Boolean approximation alone is not
    sufficient evidence of a true typed difference.
    """
    if old_only not in {"sat", "unsat"} or new_only not in {"sat", "unsat"}:
        return "unknown"
    return {("unsat", "unsat"): "equivalent",
            ("unsat", "sat"): "strengthened",
            ("sat", "unsat"): "weakened",
            ("sat", "sat"): "incomparable"}[(old_only, new_only)]


def _smt2(expr, timeout_ms):
    """Unambiguous, standalone transcript of the logical query actually checked."""
    fields = sorted(get_vars(expr), key=lambda v: v.decl().name())
    commands = ["(set-logic QF_BV)", f"(set-option :timeout {timeout_ms})"]
    commands.extend(f"(declare-fun {v.decl().name()} () {v.sort().sexpr()})" for v in fields)
    commands += [f"(assert {expr.sexpr()})", "(check-sat)"]
    return "\n".join(commands) + "\n"


def _witness(model, env):
    return {name: z3.is_true(model.eval(v, model_completion=True)) if z3.is_bool(v)
            else model.eval(v, model_completion=True).as_long() for name, v in sorted(env.items())}


def _replay(witness, guard, left=None, right=None):
    """Independently execute the source terms, not the lowered SMT expression."""
    if not isinstance(witness, dict) or set(witness) != BOOL_NAMES | set(BV_WIDTHS):
        raise ValueError("incomplete typed witness")
    if (any(type(witness[n]) is not bool for n in BOOL_NAMES) or
            any(type(witness[n]) is not int or not 0 <= witness[n] < (1 << w)
                for n, w in BV_WIDTHS.items())):
        raise ValueError("malformed typed witness")
    if not evaluate_term(guard, witness):
        raise ValueError("model does not satisfy its guard")
    if left is not None and (not evaluate_term(left, witness) or evaluate_term(right, witness)):
        raise ValueError("model does not replay the claimed directional difference")


def _record(solver, status, expr, env, guard, timeout_ms, left=None, right=None):
    smt2 = _smt2(expr, timeout_ms)
    witness = _witness(solver.model(), env) if status == z3.sat else None
    if witness is not None:
        _replay(witness, guard, left, right)
        if not z3.is_true(solver.model().eval(expr, model_completion=True)):
            raise ValueError("solver model does not satisfy exact query")
    r = {"status": str(status), "witness": witness, "logic": "QF_BV", "timeout_ms": timeout_ms,
         "smt2": smt2, "smt2_sha256": sha256(smt2.encode()).hexdigest(), "z3": z3.get_version_string()}
    if status == z3.unknown:
        r["reason"] = solver.reason_unknown()
    return r


def _result(left, right, guard, guard_receipt, directions):
    gs = guard_receipt["status"]
    relation = (classify(directions["old_only"]["status"], directions["new_only"]["status"])
                if gs == "sat" else "infeasible" if gs == "unsat" else "unknown")
    return {"left": left, "right": right, "guard": guard, "scope": SCOPE, "type_signature": TYPE_SIGNATURE,
            "guard_status": gs, "guard_query": guard_receipt, "directions": directions, "relation": relation}


def _skipped(guard_status):
    return {name: {"status": "skipped", "witness": None, "reason": f"guard {guard_status}"}
            for name in _DIRECTIONS}


def _form(env, source):
    return z3_term(parse_term(source), env)


def _difference(env, left, right):
    return z3.And(_form(env, left), z3.Not(_form(env, right)))


def _solver(timeout_ms):
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=timeout_ms)
    return solver


class IncrementalSMT:
    """Incremental typed baseline: one persistent solver per exact scope/guard.

    Cache keys include the type/scope signature and canonical typed source ASTs.
    Only definitive directional outcomes and guard satisfiability results are
    cached.  Return values are independent copies, so consumers cannot poison
    the cache by modifying an earlier result.
    """

    def __init__(self, timeout_ms=TIMEOUT_MS):
        _validate_timeout(timeout_ms)
        self.timeout_ms = timeout_ms
        self.env = z3_env()
        self._groups = {}
        self._guards = {}
        self._cache = {}
        self.counts = {"compare_calls": 0, "solver_checks": 0, "guard_checks": 0, "direction_checks": 0,
                       "cache_hits": 0, "guard_cache_hits": 0, "solver_groups": 0}

    def _group(self, guard):
        key = TYPE_SIGNATURE, guard
        if key not in self._groups:
            solver = _solver(self.timeout_ms)
            solver.add(_form(self.env, guard))
            self._groups[key] = solver
            self.counts["solver_groups"] += 1
        return self._groups[key]

    def _guard(self, guard, solver):
        key = TYPE_SIGNATURE, guard
        if key in self._guards:
            self.counts["guard_cache_hits"] += 1
            return deepcopy(self._guards[key])
        self.counts["guard_checks"] += 1
        self.counts["solver_checks"] += 1
        status = solver.check()
        receipt = _record(solver, status, _form(self.env, guard), self.env, guard, self.timeout_ms)
        if status != z3.unknown:
            self._guards[key] = deepcopy(receipt)
        return receipt

    def _direction(self, guard, left, right, solver):
        # The reverse comparison naturally looks up the same two keys in the
        # reverse order.  A shared cache never conflates the two polarities.
        key = TYPE_SIGNATURE, guard, left, right
        if key in self._cache:
            self.counts["cache_hits"] += 1
            return deepcopy(self._cache[key])
        diff = _difference(self.env, left, right)
        whole = z3.And(_form(self.env, guard), diff)
        solver.push()
        try:
            solver.add(diff)
            self.counts["direction_checks"] += 1
            self.counts["solver_checks"] += 1
            status = solver.check()
            receipt = _record(solver, status, whole, self.env, guard, self.timeout_ms, left, right)
        finally:
            solver.pop()
        if status != z3.unknown:
            self._cache[key] = deepcopy(receipt)
        return receipt

    def compare(self, left, right, guard="true"):
        left, right, guard = map(_canonical, (left, right, guard))
        self.counts["compare_calls"] += 1
        solver = self._group(guard)
        receipt = self._guard(guard, solver)
        directions = (_skipped(receipt["status"]) if receipt["status"] != "sat" else {
            "old_only": self._direction(guard, left, right, solver),
            "new_only": self._direction(guard, right, left, solver)})
        return _result(left, right, guard, receipt, directions)

    def check_direction(self, left, right, guard="true"):
        """Solve guard ∧ left ∧ ¬right only (for hybrid proof/Solver fallback).

        The caller may have independently established the other direction.
        This API never fabricates a solver receipt for such a proof; its
        counters count only actual checks and cache lookups in this method.
        """
        left, right, guard = map(_canonical, (left, right, guard))
        solver = self._group(guard)
        receipt = self._guard(guard, solver)
        direction = (self._direction(guard, left, right, solver) if receipt["status"] == "sat"
                     else _skipped(receipt["status"])["old_only"])
        return {"left": left, "right": right, "guard": guard, "scope": SCOPE,
                "type_signature": TYPE_SIGNATURE, "guard_query": receipt, "direction": direction}


def _fresh_query(expr, env, guard, timeout_ms, left=None, right=None):
    # Intentionally solve the standalone text (no shared push/pop state or
    # memoized results), so this is an independent execution of the obligation.
    solver = _solver(timeout_ms)
    solver.from_string(_smt2(expr, timeout_ms))
    status = solver.check()
    return _record(solver, status, expr, env, guard, timeout_ms, left, right)


def fresh_compare(left, right, guard="true", *, timeout_ms=TIMEOUT_MS):
    """Fresh full-width oracle; never uses incremental answers or Egg facts."""
    _validate_timeout(timeout_ms)
    left, right, guard = map(_canonical, (left, right, guard))
    env = z3_env()
    g = _form(env, guard)
    receipt = _fresh_query(g, env, guard, timeout_ms)
    if receipt["status"] == "sat":
        directions = {name: _fresh_query(z3.And(g, _difference(env, a, b)), env, guard, timeout_ms, a, b)
                      for name, a, b in (("old_only", left, right), ("new_only", right, left))}
    else:
        directions = _skipped(receipt["status"])
    return _result(left, right, guard, receipt, directions)


def _verify_receipt(actual, expected, guard, left=None, right=None):
    if not isinstance(actual, dict) or actual.keys() != expected.keys():
        raise ValueError("malformed SMT query receipt")
    if actual["smt2_sha256"] != sha256(actual["smt2"].encode()).hexdigest():
        raise ValueError("SMT2 hash mismatch")
    if any(actual[k] != expected[k] for k in expected if k not in {"witness", "z3", "reason"}):
        raise ValueError("scope, source obligation, or independently solved status changed")
    if not isinstance(actual["z3"], str) or not actual["z3"]:
        raise ValueError("missing solver version")
    if actual["status"] == "sat":
        _replay(actual["witness"], guard, left, right)
    elif actual["witness"] is not None:
        raise ValueError("non-SAT receipt has a witness")


def verify_result(left, right, guard, result, *, timeout_ms=TIMEOUT_MS):
    """Re-solve exact typed sources and check each archived query and SAT witness.

    A different valid SAT model is acceptable.  Byte-for-byte SMT2 identity
    binds the receipt to the canonical source formula; a self-consistent hash
    alone is not evidence that the right obligation was checked.
    """
    expected = fresh_compare(left, right, guard, timeout_ms=timeout_ms)
    if not isinstance(result, dict) or result.keys() != expected.keys() or any(
            result[k] != expected[k] for k in expected if k not in {"guard_query", "directions"}):
        raise ValueError("SMT result metadata or classification changed")
    a, b, g = expected["left"], expected["right"], expected["guard"]
    _verify_receipt(result["guard_query"], expected["guard_query"], g)
    if result["guard_status"] != "sat":
        if result["directions"] != expected["directions"]:
            raise ValueError("infeasible or unresolved guard did not skip both directions")
    else:
        if not isinstance(result["directions"], dict) or set(result["directions"]) != set(_DIRECTIONS):
            raise ValueError("missing or unexpected direction")
        for name, l, r in (("old_only", a, b), ("new_only", b, a)):
            _verify_receipt(result["directions"][name], expected["directions"][name], g, l, r)
    return True


def verify_direction(left, right, guard, result, *, timeout_ms=TIMEOUT_MS):
    """Audit one typed fallback query, independent of any other direction."""
    left, right, guard = map(_canonical, (left, right, guard))
    env = z3_env()
    g = _form(env, guard)
    receipt = _fresh_query(g, env, guard, timeout_ms)
    fields = {"left": left, "right": right, "guard": guard, "scope": SCOPE, "type_signature": TYPE_SIGNATURE}
    if (not isinstance(result, dict) or set(result) != set(fields) | {"guard_query", "direction"} or
            any(result[k] != v for k, v in fields.items())):
        raise ValueError("typed direction receipt metadata changed")
    _verify_receipt(result["guard_query"], receipt, guard)
    if receipt["status"] == "sat":
        expected = _fresh_query(z3.And(g, _difference(env, left, right)), env, guard, timeout_ms, left, right)
        _verify_receipt(result["direction"], expected, guard, left, right)
    elif result["direction"] != _skipped(receipt["status"])["old_only"]:
        raise ValueError("direction not skipped on infeasible/unresolved guard")
    return True
