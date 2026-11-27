"""Width-checked, two-state violation terms over two sampled AXIS frame_task pin snapshots."""
from functools import lru_cache
import hashlib
import operator
import re


_BOOL_PINS = ("rst", "s_valid", "s_ready", "s_last", "m_valid", "m_ready", "m_last",
              "h_valid", "h_ready", "h_pad", "h_truncate")
_BUS_PINS = {"s_data": 8, "m_data": 8, "h_length": 16, "h_original_length": 16}
BOOL_NAMES = frozenset(("have_prev", *_BOOL_PINS, *("prev_" + name for name in _BOOL_PINS)))
BV_WIDTHS = {**_BUS_PINS, **{"prev_" + name: width for name, width in _BUS_PINS.items()}}
BOOL_OPS = {"not", "and", "or", "xor"}
CMP_OPS = {"eq", "ne", "ult", "ule", "ugt", "uge"}


def _fold(op, *terms):
    result = terms[-1]
    for term in reversed(terms[:-1]):
        result = f"({op} {term} {result})"
    return result


def _hold(channel, payload):
    stalled = _fold("and", "have_prev", "(not prev_rst)", "(not rst)",
                    f"prev_{channel}_valid", f"(not prev_{channel}_ready)")
    lost = _fold("or", f"(not {channel}_valid)", *(f"(ne {p} prev_{p})" for p in payload))
    return f"(and {stalled} {lost})"


_HDR = "(and (not rst) h_valid)"
_SHORT = "(ult h_original_length 4)"
_LONG = "(ugt h_original_length 8)"
_IN_RANGE = "(and (uge h_original_length 4) (ule h_original_length 8))"
_WRONG_LENGTH = _fold("or", f"(and {_SHORT} (ne h_length 4))", f"(and {_LONG} (ne h_length 8))",
                      f"(and {_IN_RANGE} (ne h_length h_original_length))")
REFERENCES = {
    "data_hold": _hold("m", ("m_data", "m_last")),
    "header_hold": _hold("h", ("h_pad", "h_truncate", "h_length", "h_original_length")),
    "pad_flag": f"(and {_HDR} (xor h_pad {_SHORT}))",
    "truncate_flag": f"(and {_HDR} (xor h_truncate {_LONG}))",
    "clamped_length": f"(and {_HDR} {_WRONG_LENGTH})",
}


def _comparison_type(left, right):
    if type(left) is int or type(right) is int:
        literal, other = (left, right) if type(left) is int else (right, left)
        width = typed_width(other)
        if width == "bool" or not 0 <= literal < (1 << width):
            raise ValueError(f"unsigned decimal literal {literal} does not fit {width}")
        return width
    width = typed_width(left)
    if typed_width(right) != width:
        raise ValueError("comparison operands have different types or widths")
    return width


@lru_cache(maxsize=8192)
def typed_width(node):
    """Return 'bool' or the unsigned bus width. A standalone numeral lacks a width."""
    if isinstance(node, str):
        if node in BOOL_NAMES or node in ("true", "false"):
            return "bool"
        if node in BV_WIDTHS:
            return BV_WIDTHS[node]
        raise ValueError(f"unknown sampled pin {node!r}")
    if type(node) is int:
        raise ValueError("a decimal literal needs a bus operand to determine its width")
    if not isinstance(node, tuple) or not node:
        raise ValueError("invalid term")
    op = node[0]
    if op not in BOOL_OPS | CMP_OPS or len(node) != (2 if op == "not" else 3):
        raise ValueError("unsupported operation or wrong arity")
    if op in BOOL_OPS:
        if any(typed_width(child) != "bool" for child in node[1:]):
            raise ValueError(f"{op} requires Boolean operands")
    else:
        width = _comparison_type(node[1], node[2])
        if width == "bool" and op not in ("eq", "ne"):
            raise ValueError(f"{op} requires unsigned bit-vectors")
    return "bool"


def parse_term(source):
    """Parse a single complete Boolean S-expression, rejecting untyped literal comparisons."""
    if not isinstance(source, str):
        raise ValueError("source must be a string")
    if len(source) > 262_144:
        raise ValueError("term source exceeds 262144 characters")
    tokens = re.findall(r"\(|\)|[^\s()]+", source)
    index = 0

    def read(depth):
        nonlocal index
        if depth > 128:
            raise ValueError("term nesting exceeds 128 levels")
        if index >= len(tokens):
            raise ValueError("incomplete term")
        token = tokens[index]
        index += 1
        if token == ")":
            raise ValueError("unexpected closing parenthesis")
        if token != "(":
            return int(token) if re.fullmatch("[0-9]+", token) else token
        if index == len(tokens):
            raise ValueError("missing operator")
        op = tokens[index]
        index += 1
        if op not in BOOL_OPS | CMP_OPS:
            raise ValueError(f"unknown operator {op!r}")
        children = [read(depth + 1) for _ in range(1 if op == "not" else 2)]
        if index == len(tokens) or tokens[index] != ")":
            raise ValueError(f"expected closing parenthesis after operands of {op}")
        index += 1
        return (op, *children)

    node = read(0)
    if index != len(tokens):
        raise ValueError("unexpected trailing tokens")
    if typed_width(node) != "bool":
        raise ValueError("a violation expression must be Boolean")
    return node


def format_term(node):
    if isinstance(node, tuple):
        return "(" + " ".join((node[0], *(format_term(v) for v in node[1:]))) + ")"
    return str(node)


def referenced_signals(node):
    """Return the exact current/previous signal names used by a validated AST."""
    if isinstance(node, tuple):
        return frozenset().union(*(referenced_signals(child) for child in node[1:]))
    if isinstance(node, str) and node not in ("true", "false"):
        typed_width(node)
        return frozenset((node,))
    return frozenset()


def _walk(node, atom, literal, apply, hint=None):
    if type(node) is int:
        return literal(node, hint)
    if isinstance(node, str):
        return atom(node)
    op, *children = node
    operand_type = _comparison_type(*children) if op in CMP_OPS else "bool"
    return apply(op, [_walk(v, atom, literal, apply, operand_type) for v in children], operand_type)


def evaluate_term(node, env):
    """Evaluate sampled pin values; Python integers outside a pin's declared width are rejected."""
    if typed_width(node) != "bool":
        raise ValueError("a violation expression must be Boolean")

    def value(name):
        if name in ("true", "false"):
            return name == "true"
        if name not in env:
            raise ValueError(f"missing sampled pin {name}")
        v = env[name]
        if name in BOOL_NAMES:
            if type(v) not in (int, bool) or v not in (0, 1):
                raise ValueError(f"nonbinary sampled pin {name}")
            return bool(v)
        if type(v) is not int or not 0 <= v < 1 << BV_WIDTHS[name]:
            raise ValueError(f"sampled bus value outside declared width for {name}")
        return v

    operations = {"and": operator.and_, "or": operator.or_, "xor": operator.xor, "not": operator.not_,
                  "eq": operator.eq, "ne": operator.ne, "ult": operator.lt, "ule": operator.le,
                  "ugt": operator.gt, "uge": operator.ge}
    return _walk(node, value, lambda v, width: v, lambda op, args, typ: operations[op](*args))


def z3_env():
    """Unrestricted symbolic current and previous pin samples; clocks/reset rules live in each term."""
    import z3
    return {**{name: z3.Bool(name) for name in sorted(BOOL_NAMES)},
            **{name: z3.BitVec(name, width) for name, width in BV_WIDTHS.items()}}


def z3_term(node, env):
    """Produce a QF_BV Boolean formula over the supplied shared Z3 pin environment."""
    import z3
    if typed_width(node) != "bool":
        raise ValueError("a violation expression must be Boolean")

    def value(name):
        if name in ("true", "false"):
            return z3.BoolVal(name == "true")
        v = env[name]
        if name in BOOL_NAMES:
            if not z3.is_bool(v):
                raise ValueError(f"expected Z3 Bool for {name}")
        elif not z3.is_bv(v) or v.size() != BV_WIDTHS[name]:
            raise ValueError(f"wrong Z3 bit-vector width for {name}")
        return v

    operations = {"and": z3.And, "or": z3.Or, "xor": z3.Xor, "not": z3.Not,
                  "eq": operator.eq, "ne": operator.ne, "ult": z3.ULT, "ule": z3.ULE,
                  "ugt": z3.UGT, "uge": z3.UGE}
    return _walk(node, value, z3.BitVecVal, lambda op, args, typ: operations[op](*args))


def sv_term(node):
    """Produce an SV expression over bare sampled identifiers and explicitly sized bus literals."""
    if typed_width(node) != "bool":
        raise ValueError("a violation expression must be Boolean")
    signs = {"and": "&&", "or": "||", "xor": "^", "eq": "==", "ne": "!=",
             "ult": "<", "ule": "<=", "ugt": ">", "uge": ">="}

    def apply(op, args, typ):
        if op == "not":
            return f"(!{args[0]})"
        left, right = args
        if op in ("ult", "ule", "ugt", "uge"):
            left, right = f"$unsigned({left})", f"$unsigned({right})"
        return f"({left} {signs[op]} {right})"

    return _walk(node, lambda name: {"true": "1'b1", "false": "1'b0"}.get(name, name),
                 lambda value, width: f"{width}'d{value}", apply)


def abstract(node):
    """Return a Boolean prefix term and the typed source of each primitive Bool atom."""
    if typed_width(node) != "bool":
        raise ValueError("a violation expression must be Boolean")
    predicates = {}

    def combine(op, *terms):
        # XOR/XNOR are lowered into the engine's existing language. Reject excessive
        # expansion before serializing a deeply nested chain into an exponential string.
        if len(op) + 2 + len(terms) + sum(map(len, terms)) > 262_144:
            raise ValueError("Boolean abstraction exceeds 256 KiB")
        return "(" + " ".join((op, *terms)) + ")"

    def lower(t):
        if isinstance(t, str):
            if t not in ("true", "false"):
                predicates[t] = t
            return t
        op, *children = t
        if op in CMP_OPS and _comparison_type(*children) != "bool":
            left, right = children
            if op in ("ugt", "uge"):
                op = {"ugt": "ult", "uge": "ule"}[op]
                left, right = right, left
            negate = op == "ne"
            if op in ("eq", "ne"):
                op = "eq"
                left, right = sorted((left, right), key=format_term)
            canonical = (op, left, right)
            atom = "bv_" + hashlib.sha256(format_term(canonical).encode()).hexdigest()[:24]
            if predicates.setdefault(atom, canonical) != canonical:
                raise ValueError("distinct comparisons have the same predicate identifier")
            return combine("not", atom) if negate else atom
        args = [lower(child) for child in children]
        if op in ("xor", "eq", "ne"):
            left, right = args
            difference = combine("or", combine("and", left, combine("not", right)),
                                 combine("and", combine("not", left), right))
            return combine("not", difference) if op == "eq" else difference
        return combine(op, *args)

    return lower(node), predicates
