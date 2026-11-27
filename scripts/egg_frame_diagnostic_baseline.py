"""Ordinary DNF and shortest sufficient reasons over independent sampled Boolean atoms.

Each literal is (atom, polarity). A clause is their conjunction and a DNF is a tuple
of clauses. The empty clause is true, so ((),) is true and () is false. Unknown
values are missing, None or -1; their possible completions are never constrained.
"""
from collections.abc import Mapping
from functools import lru_cache
from itertools import combinations

from predicates import evaluate, parse


@lru_cache(maxsize=128)
def _parsed(source):
    if not isinstance(source, str):
        raise ValueError("expected Boolean expression text")
    try:
        tree = parse(source)
    except (IndexError, RecursionError) as exc:
        raise ValueError("malformed or excessively nested Boolean expression") from exc
    atoms = set()
    pending = [tree]
    while pending:
        item = pending.pop()
        if isinstance(item, tuple):
            pending.extend(item[1:])
        elif item in ("and", "or", "not", "(", ")") or item.startswith("?"):
            raise ValueError(f"invalid Boolean atom {item!r}")
        elif item not in ("true", "false"):
            atoms.add(item)
    return tree, tuple(sorted(atoms))


def _minimal_clauses(clauses):
    """Drop duplicates and supersets; retained clauses form an antichain."""
    buckets = {}
    for clause in sorted(set(clauses), key=len):
        if any(shorter <= clause for size, bucket in buckets.items() if size < len(clause)
               for shorter in bucket):
            continue
        buckets.setdefault(len(clause), []).append(clause)
    return tuple(c for bucket in buckets.values() for c in bucket)


@lru_cache(maxsize=128)
def dnf(source):
    """Push negations to atoms, distribute conjunctions, and normalize the clauses."""
    tree, _ = _parsed(source)

    @lru_cache(maxsize=None)
    def visit(node, negated):
        if isinstance(node, str):
            if node in ("true", "false"):
                return (frozenset(),) if (node == "true") != negated else ()
            return (frozenset(((node, not negated),)),)
        if node[0] == "not":
            return visit(node[1], not negated)
        left = visit(node[1], negated)
        right = visit(node[2], negated)
        if (node[0] == "or") != negated:
            return _minimal_clauses((*left, *right))
        product = (a | b for a in left for b in right
                   if not any((name, not polarity) in b for name, polarity in a))
        return _minimal_clauses(product)

    normalized = (tuple(sorted(clause)) for clause in visit(tree, False))
    return tuple(sorted(normalized, key=lambda clause: (len(clause), clause)))


@lru_cache(maxsize=128)
def parse_dnf(source):
    """Accept only an OR of ANDs of literals; a literal may be negated once."""
    tree, _ = _parsed(source)

    def check(node, in_clause=False):
        if isinstance(node, str):
            return
        op, *args = node
        if op == "not" and isinstance(args[0], str):
            return
        if op == "and" or (op == "or" and not in_clause):
            for arg in args:
                check(arg, in_clause or op == "and")
            return
        raise ValueError("expected DNF with AND clauses and single signed literals")

    check(tree)
    return dnf(source)


def _observed(assignment, name):
    value = assignment.get(name)
    if value is None or (type(value) is int and value == -1):
        return None
    if type(value) not in (bool, int) or value not in (0, 1):
        raise ValueError(f"invalid sampled value for {name!r}")
    return bool(value)


def evaluate_clause(clause, assignment):
    """Return False on any contradictory known literal, None if literals remain unknown."""
    unknown = False
    for name, polarity in clause:
        value = _observed(assignment, name)
        if value is None:
            unknown = True
        elif value != polarity:
            return False
    return None if unknown else True


def evaluate_dnf(clauses, assignment):
    """Three-valued evaluation per written clause. An uncovered partial assignment can be unknown."""
    unknown = False
    for clause in clauses:
        value = evaluate_clause(clause, assignment)
        if value is True:
            return True
        if value is None:
            unknown = True
    return None if unknown else False


@lru_cache(maxsize=128)
def _truth_masks(source):
    """Build bitsets independently by evaluating the input AST on every Boolean valuation."""
    tree, atoms = _parsed(source)
    if len(atoms) > 12:
        raise ValueError("truth masks support at most 12 Boolean atoms")
    rows = 1 << len(atoms)
    full = (1 << rows) - 1
    true_rows = 0
    columns = [0] * len(atoms)
    for row in range(rows):
        env = {name: bool(row & (1 << i)) for i, name in enumerate(atoms)}
        bit = 1 << row
        if evaluate(tree, env):
            true_rows |= bit
        for i, name in enumerate(atoms):
            if env[name]:
                columns[i] |= bit
    return full, true_rows, tuple(columns)


@lru_cache(maxsize=8192)
def _shortest(source, known, positive):
    atoms = _parsed(source)[1]
    full, true_rows, columns = _truth_masks(source)
    compatible = full
    literals = []
    for i, name in enumerate(atoms):
        if known & (1 << i):
            polarity = bool(positive & (1 << i))
            rows = columns[i] if polarity else full ^ columns[i]
            literals.append(((name, polarity), rows))
            compatible &= rows
    positive_count = (compatible & true_rows).bit_count()
    completions = compatible.bit_count()
    if positive_count != completions:
        return ("false" if positive_count == 0 else "unknown", None, completions, positive_count)

    # Fewest observed literals first. The first certificate at each depth is the
    # lexicographically first by atom, independently of original formula layout.
    false_rows = full ^ true_rows
    for size in range(len(literals) + 1):
        for subset in combinations(literals, size):
            possible_false = false_rows
            for _, allowed in subset:
                possible_false &= allowed
            if possible_false == 0:
                return "sufficient", tuple(lit for lit, _ in subset), completions, positive_count
    raise AssertionError("known literals failed to certify their own positive completion set")


def minimum_cube(source, assignment, *, max_atoms=12):
    """Find a smallest subset of known literals that forces the *source* true on all completions.

    Returns status (sufficient, false, unknown, atom_limit), cube, size, atom_count,
    known_atom_count, and full-assignment counts consistent with the observation.
    A false or mixed partial observation has no sufficient compatible cube. A
    tautology has a size-zero cube, even with all values unknown.
    """
    if type(max_atoms) is not int or not 0 <= max_atoms <= 12:
        raise ValueError("max_atoms must be an integer in [0, 12]")
    if not isinstance(assignment, Mapping):
        raise ValueError("assignment must map atom names to sampled values")
    _, atoms = _parsed(source)
    known = positive = 0
    for i, name in enumerate(atoms):
        value = _observed(assignment, name)
        if value is not None:
            known |= 1 << i
            if value:
                positive |= 1 << i
    status, cube, completions, hits = "atom_limit", None, None, None
    if len(atoms) <= max_atoms:
        status, cube, completions, hits = _shortest(source, known, positive)
    return {"status": status, "cube": cube, "size": None if cube is None else len(cube),
            "atom_count": len(atoms), "known_atom_count": known.bit_count(),
            "consistent_assignments": completions, "positive_assignments": hits}
