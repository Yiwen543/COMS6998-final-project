"""Typed violation monitors over an AXIS transaction-history snapshot and its sampled pins."""
from functools import lru_cache
import hashlib
import operator
import re

from egg_frame_terms import BOOL_OPS, CMP_OPS, format_term
from predicates import fold


BOOL_NAMES = frozenset("""
    rst s_valid s_last s_ready m_valid m_last m_ready h_valid h_ready h_pad h_truncate
    phase_post final_sample input_open data_done header_done
""".split())
BV_WIDTHS = {**dict.fromkeys(("s_data", "m_data", "data_byte"), 8),
             **dict.fromkeys(("h_length", "h_original_length", "input_count", "data_count",
                              "header_count", "data_index", "data_n", "header_n"), 16)}
DOMAIN_NAMES = frozenset("""
    input_count data_count header_count data_index data_n header_n
    data_done header_done input_open phase_post final_sample
""".split())
_DOMAIN_ORDER = tuple(sorted(DOMAIN_NAMES))
SCOPE = ("Two-state transaction snapshots with bounded ghost history: up to 512 frames/counts "
         "and observed beat index, 1..12 accepted bytes per present input record. "
         "Independent output cursors may overrun input history. No RTL reachability assumption.")


def _and(*terms):
    return fold("and", terms)


def _or(*terms):
    return fold("or", terms)


_DATA_ALLOWED = _and("(ult data_count input_count)", "(uge data_index 1)", "(ule data_index 8)",
                     _or("(ule data_index data_n)", "(and data_done (ule data_index 4))"))
_DATA = "(and (not rst) m_valid)"
_DATA_JUSTIFIED = _and(_DATA, _DATA_ALLOWED)
_EXPECT_LAST = _or("(eq data_index 8)",
                   _and("data_done", _or("(and (ule data_n 4) (eq data_index 4))",
                                         _and("(ugt data_n 4)", "(ult data_n 8)", "(eq data_index data_n)"))))
_HEADER_ALLOWED = "(and (ult header_count input_count) header_done)"
_HEADER = "(and (not rst) h_valid)"
_HEADER_JUSTIFIED = _and(_HEADER, _HEADER_ALLOWED)
_SHORT, _LONG = "(ult header_n 4)", "(ugt header_n 8)"
_BAD_ADJUSTED = _or(_and(_SHORT, "(ne h_length 4)"), _and(_LONG, "(ne h_length 8)"),
                    _and("(uge header_n 4)", "(ule header_n 8)", "(ne h_length header_n)"))

REFERENCES = {
    "data_entitlement": _and(_DATA, f"(not {_DATA_ALLOWED})"),
    "data_payload": _and(_DATA_JUSTIFIED, _or(_and("(ule data_index data_n)", "(ne m_data data_byte)"),
                                              _and("(ugt data_index data_n)", "(ne m_data 0)"))),
    "data_last": _and(_DATA_JUSTIFIED, f"(xor m_last {_EXPECT_LAST})"),
    "header_entitlement": _and(_HEADER, f"(not {_HEADER_ALLOWED})"),
    "header_original": _and(_HEADER_JUSTIFIED, "(ne h_original_length header_n)"),
    "header_adjusted": _and(_HEADER_JUSTIFIED, _BAD_ADJUSTED),
    "header_flags": _and(_HEADER_JUSTIFIED, _or(f"(xor h_pad {_SHORT})", f"(xor h_truncate {_LONG})")),
    "reset_clear": _and("rst", "phase_post", "(or m_valid h_valid)"),
    "drain_complete": _and("final_sample", _or("s_valid", "m_valid", "h_valid", "input_open",
                                              "(ne data_count input_count)", "(ne header_count input_count)")),
}


def _operand_width(left, right):
    if type(left) is int or type(right) is int:
        literal, typed = (left, right) if type(left) is int else (right, left)
        width = typed_width(typed)
        if width == "bool" or not 0 <= literal < (1 << width):
            raise ValueError("decimal literal needs a same-width unsigned bus operand")
        return width
    width = typed_width(left)
    if width != typed_width(right):
        raise ValueError("incompatible comparison widths")
    return width


@lru_cache(maxsize=8192)
def typed_width(term):
    if isinstance(term, str):
        if term in BOOL_NAMES or term in ("true", "false"):
            return "bool"
        if term in BV_WIDTHS:
            return BV_WIDTHS[term]
        raise ValueError(f"unknown transaction field {term!r}")
    if not isinstance(term, tuple) or not term:
        raise ValueError("expected a Boolean term or a typed bus")
    op, *args = term
    if op not in BOOL_OPS | CMP_OPS or len(args) != (1 if op == "not" else 2):
        raise ValueError("unsupported operator or wrong arity")
    if op in BOOL_OPS:
        if any(typed_width(arg) != "bool" for arg in args):
            raise ValueError(f"{op} requires Boolean operands")
    elif _operand_width(*args) == "bool" and op not in ("eq", "ne"):
        raise ValueError(f"{op} requires unsigned bit-vectors")
    return "bool"


@lru_cache(maxsize=2048)
def parse_term(source):
    """Parse one complete, bounded, width-checked Boolean S-expression."""
    if not isinstance(source, str) or len(source) > 262_144:
        raise ValueError("expected transaction term of at most 262144 characters")
    stream = iter(re.findall(r"\(|\)|[^()\s]+", source))

    def read(depth):
        if depth > 128:
            raise ValueError("term nesting exceeds 128 levels")
        token = next(stream, None)
        if token is None or token == ")":
            raise ValueError("expected a transaction operand")
        if token != "(":
            return int(token) if re.fullmatch("[0-9]+", token) else token
        op = next(stream, None)
        if op not in BOOL_OPS | CMP_OPS:
            raise ValueError(f"unknown operator {op!r}")
        args = tuple(read(depth + 1) for _ in range(1 if op == "not" else 2))
        if next(stream, None) != ")":
            raise ValueError(f"expected closing parenthesis after {op}")
        return (op, *args)

    term = read(0)
    if next(stream, None) is not None or typed_width(term) != "bool":
        raise ValueError("expected exactly one Boolean transaction term")
    return term


def _as_term(term):
    if isinstance(term, str):
        return parse_term(term)
    if typed_width(term) != "bool":
        raise ValueError("expected a Boolean transaction term")
    return term


@lru_cache(maxsize=8192)
def referenced_signals(term):
    if isinstance(term, tuple):
        return frozenset().union(*(referenced_signals(arg) for arg in term[1:]))
    if isinstance(term, str) and term not in ("true", "false"):
        typed_width(term)
        return frozenset((term,))
    return frozenset()


def _observed(name, value):
    if value is None or type(value) is int and value == -1:
        return None
    if name in BOOL_NAMES:
        if type(value) not in (bool, int) or value not in (0, 1):
            raise ValueError(f"invalid Boolean observation for {name}")
        return bool(value)
    if type(value) is not int or not 0 <= value < (1 << BV_WIDTHS[name]):
        raise ValueError(f"invalid unsigned observation for {name}")
    return value


def _walk(term, signal, literal, operators, width=None):
    if isinstance(term, str):
        return signal(term)
    if type(term) is int:
        return literal(term, width)
    op, *args = term
    width = _operand_width(*args) if op in CMP_OPS else "bool"
    return operators[op](*(_walk(arg, signal, literal, operators, width) for arg in args))


_PY_OPS = {"and": operator.and_, "or": operator.or_, "not": operator.not_, "xor": operator.xor,
           "eq": operator.eq, "ne": operator.ne, "ult": operator.lt, "ule": operator.le,
           "ugt": operator.gt, "uge": operator.ge}


def evaluate_term(term, env):
    """Evaluate on known two-state values. Use sample for partially unknown rows."""
    def signal(name):
        if name in ("true", "false"):
            return name == "true"
        value = _observed(name, env.get(name))
        if value is None:
            raise ValueError(f"expected concrete observation for {name}")
        return value
    return _walk(_as_term(term), signal, lambda value, width: value, _PY_OPS)


def z3_env():
    import z3
    return {**{name: z3.Bool(name) for name in sorted(BOOL_NAMES)},
            **{name: z3.BitVec(name, width) for name, width in BV_WIDTHS.items()}}


def z3_term(term, env):
    import z3

    def signal(name):
        if name in ("true", "false"):
            return z3.BoolVal(name == "true")
        value = env[name]
        if name in BOOL_NAMES:
            if not z3.is_bool(value):
                raise ValueError(f"expected Z3 Bool for {name}")
        elif not z3.is_bv(value) or value.size() != BV_WIDTHS[name]:
            raise ValueError(f"wrong bit-vector width for {name}")
        return value

    ops = {**_PY_OPS, "and": z3.And, "or": z3.Or, "not": z3.Not, "xor": z3.Xor,
           "ult": z3.ULT, "ule": z3.ULE, "ugt": z3.UGT, "uge": z3.UGE}
    return _walk(_as_term(term), signal, z3.BitVecVal, ops)


def abstract(term):
    """Return AND/OR/NOT text and canonical typed Boolean leaves for independent proof replay."""
    atoms = {}

    def emit(op, *args):
        if sum(map(len, args)) + len(args) + len(op) + 2 > 262_144:
            raise ValueError("Boolean abstraction exceeds 256 KiB")
        return f"({op} {' '.join(args)})"

    def lower(node):
        if isinstance(node, str):
            if node not in ("true", "false"):
                atoms[node] = node
            return node
        op, *args = node
        if op in CMP_OPS and _operand_width(*args) != "bool":
            left, right = args
            if op in ("ugt", "uge"):
                op = {"ugt": "ult", "uge": "ule"}[op]
                left, right = right, left
            negated = op == "ne"
            if op in ("eq", "ne"):
                op = "eq"
                left, right = sorted((left, right), key=format_term)
            atom = (op, left, right)
            name = "bv_" + hashlib.sha256(format_term(atom).encode()).hexdigest()[:24]
            if atoms.setdefault(name, atom) != atom:
                raise ValueError("canonical atom identifier collision")
            return emit("not", name) if negated else name
        children = [lower(arg) for arg in args]
        if op in ("xor", "eq", "ne"):
            a, b = children
            different = emit("or", emit("and", a, emit("not", b)), emit("and", emit("not", a), b))
            return emit("not", different) if op == "eq" else different
        return emit(op, *children)

    return lower(_as_term(term)), atoms


def _domain_conditions(e, le, lt, negate):
    """Shared concrete and BV relations. Counts are bounded before cursor+1 can wrap."""
    for name in ("input_count", "data_count", "header_count", "data_index"):
        yield le(e[name], 512)
    yield le(1, e["data_index"])
    yield negate(e["input_open"]) | (e["input_count"] != 0)
    yield negate(e["final_sample"]) | e["phase_post"]
    for channel in ("data", "header"):
        cursor, n = e[channel + "_count"], e[channel + "_n"]
        present = lt(cursor, e["input_count"])
        newest_open = e["input_open"] & (cursor + 1 == e["input_count"])
        yield le(n, 12)
        yield (n != 0) == present
        yield e[channel + "_done"] == (present & negate(newest_open))
    # Both cursors name the same accepted-input record in this case.
    yield (e["data_count"] != e["header_count"]) | (e["data_n"] == e["header_n"])


def domain(env):
    """Structural ghost-history constraints; all sampled DUT output pins remain free."""
    import z3
    return z3.And(*_domain_conditions(env, z3.ULE, z3.ULT, z3.Not))


def _symbolic_with(bindings):
    import z3
    env = z3_env()
    for name, value in bindings:
        if value is not None:
            env[name] = z3.BoolVal(value) if name in BOOL_NAMES else z3.BitVecVal(value, BV_WIDTHS[name])
    return env


def _satisfiable(expr):
    import z3
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=5000)
    solver.add(expr)
    status = solver.check()
    if status == z3.unknown:
        raise RuntimeError(f"snapshot consistency query was inconclusive: {solver.reason_unknown()}")
    return status == z3.sat


@lru_cache(maxsize=8192)
def _check_structural(bindings):
    if all(v is not None for v in bindings):
        legal = all(_domain_conditions(dict(zip(_DOMAIN_ORDER, bindings)), operator.le, operator.lt, operator.not_))
    else:
        legal = _satisfiable(domain(_symbolic_with(zip(_DOMAIN_ORDER, bindings))))
    if not legal:
        raise ValueError("sample has no completion within the transaction snapshot domain")


def _structural_bindings(values):
    return tuple(_observed(k, values.get(k)) for k in _DOMAIN_ORDER)


def validate_snapshot(values):
    """Raise on a foreign field, invalid pin value, or infeasible (possibly partial) history."""
    for name, value in values.items():
        if name not in BOOL_NAMES and name not in BV_WIDTHS:
            raise ValueError(f"unknown transaction field {name!r}")
        _observed(name, value)
    _check_structural(_structural_bindings(values))
    return True


@lru_cache(maxsize=65536)
def _projected_sample(term, bindings, structural):
    if all(v is not None for _, v in bindings):
        return evaluate_term(term, dict(bindings))
    import z3
    merged = dict(zip(_DOMAIN_ORDER, structural)) if structural else {}
    merged.update(bindings)
    env = _symbolic_with(merged.items())
    expr = z3.simplify(z3_term(term, env))
    if z3.is_true(expr):
        return True
    if z3.is_false(expr):
        return False
    legal = domain(env) if structural else z3.BoolVal(True)
    positive = _satisfiable(z3.And(legal, expr))
    negative = _satisfiable(z3.And(legal, z3.Not(expr)))
    if not positive and not negative:
        raise ValueError("sample has no completion within the transaction snapshot domain")
    return None if positive and negative else positive


def sample(term, values):
    """Exact verdict on all domain-consistent completions. Missing, None and -1 denote X."""
    term = _as_term(term)
    structural = _structural_bindings(values)
    _check_structural(structural)
    bindings = tuple((k, _observed(k, values.get(k))) for k in sorted(referenced_signals(term)))
    # Known ghost fields already passed the domain. It can only influence the verdict
    # when a referenced ghost is unknown (all non-ghost signals are unconstrained).
    needs_domain = any(k in DOMAIN_NAMES and v is None for k, v in bindings)
    return _projected_sample(term, bindings, structural if needs_domain else ())


def typed_oracle(reference, candidate, *, timeout_ms=5000):
    """Check reference XOR candidate in the structural domain; independently replay a SAT model."""
    import z3
    if type(timeout_ms) is not int or timeout_ms < 1:
        raise ValueError("expected a positive solver timeout")
    ref, cand = _as_term(reference), _as_term(candidate)
    env = z3_env()
    a, b = z3_term(ref, env), z3_term(cand, env)
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=timeout_ms)
    solver.add(domain(env), z3.Xor(a, b))
    status = solver.check()
    result = {"status": str(status), "equivalent": {"sat": False, "unsat": True}.get(str(status)),
              "scope": SCOPE, "z3": z3.get_version_string(), "timeout_ms": timeout_ms,
              "smt2": solver.to_smt2(), "counterexample": None, "reference_value": None, "candidate_value": None}
    if status == z3.unknown:
        result["reason"] = solver.reason_unknown()
    if status == z3.sat:
        model = solver.model()
        values = {}
        for name, var in env.items():
            value = model.eval(var, model_completion=True)
            values[name] = z3.is_true(value) if z3.is_bool(var) else value.as_long()
        validate_snapshot(values)
        verdicts = evaluate_term(ref, values), evaluate_term(cand, values)
        if verdicts[0] == verdicts[1] or verdicts != tuple(z3.is_true(model.eval(v)) for v in (a, b)):
            raise RuntimeError("transaction counterexample failed independent concrete replay")
        result.update(counterexample=values, reference_value=verdicts[0], candidate_value=verdicts[1])
    return result
