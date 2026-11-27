#!/usr/bin/env python3
"""Ordinary Boolean assertion baselines over named, already-sampled binary signals."""
import argparse
from itertools import product
import json
from pathlib import Path

from predicates import evaluate, parse


def _atoms(node):
    if isinstance(node, str):
        return set() if node in ("true", "false") else {node}
    return set().union(*(_atoms(child) for child in node[1:]))


def _parse(text, *, pattern=False):
    try:
        tree = parse(text)
    except IndexError as exc:
        raise ValueError("incomplete Boolean expression") from exc
    for atom in _atoms(tree):
        if atom in ("and", "or", "not", ")", "(") or (atom.startswith("?") and (not pattern or len(atom) == 1)):
            raise ValueError(f"invalid Boolean atom {atom!r}")
    return tree


def _text(node):
    if isinstance(node, str):
        return node
    return "(" + " ".join([node[0], *(_text(child) for child in node[1:])]) + ")"


def _truth_table(left, right, max_atoms):
    names = sorted(_atoms(left) | _atoms(right))
    if max_atoms < 0:
        raise ValueError("max_atoms must be nonnegative")
    result = {"atoms": names, "equivalent": None, "checked_assignments": 0,
              "unequal_assignments": None, "counterexample": None, "left_value": None, "right_value": None}
    if len(names) > max_atoms:
        return {**result, "stop_reason": "atom_limit"}
    mismatches = 0
    for values in product((False, True), repeat=len(names)):
        env = dict(zip(names, values, strict=True))
        lv, rv = evaluate(left, env), evaluate(right, env)
        if lv != rv:
            if not mismatches:
                result.update(counterexample=env, left_value=lv, right_value=rv)
            mismatches += 1
    return {**result, "equivalent": mismatches == 0, "checked_assignments": 1 << len(names),
            "unequal_assignments": mismatches, "stop_reason": "exhaustive"}


def truth_table(left, right, *, max_atoms=12):
    """Exhaust every independent binary valuation, retaining the first mismatch and its count."""
    return _truth_table(_parse(left), _parse(right), max_atoms)


def _canonical(node, negated=False):
    """Negation-normal form with associative, commutative, idempotent and constant reductions."""
    if isinstance(node, str):
        if not negated:
            return node
        if node in ("true", "false"):
            return "false" if node == "true" else "true"
        return ("not", node)
    op = node[0]
    if op == "not":
        return _canonical(node[1], not negated)
    if negated:
        op = {"and": "or", "or": "and"}[op]
    identity, annihilator = ("true", "false") if op == "and" else ("false", "true")
    operands = set()
    for child in node[1:]:
        normalized = _canonical(child, negated)
        if normalized == annihilator:
            return annihilator
        if normalized == identity:
            continue
        if isinstance(normalized, tuple) and normalized[0] == op:
            operands.update(normalized[1:])
        else:
            operands.add(normalized)
    if any(("not", term) in operands for term in operands):
        return annihilator
    # Absorb x AND (x OR y), and its dual, on already normalized operands.
    other = "or" if op == "and" else "and"
    absorbed = {term for term in operands if isinstance(term, tuple) and term[0] == other
                and any(child in operands for child in term[1:])}
    operands -= absorbed
    ordered = sorted(operands, key=_text)
    if not ordered:
        return identity
    if len(ordered) == 1:
        return ordered[0]
    return (op, *ordered)


def canonical_key(expression):
    """Deterministic serialization of the normalized n-ary key; distributivity is omitted."""
    return _text(_canonical(_parse(expression)))


def _match(pattern, node, bindings):
    if isinstance(pattern, str):
        if pattern.startswith("?"):
            if pattern not in bindings:
                bindings[pattern] = node
            return bindings[pattern] == node
        return pattern == node
    return (isinstance(node, tuple) and pattern[0] == node[0] and
            all(_match(child, value, bindings) for child, value in zip(pattern[1:], node[1:], strict=True)))


def _instantiate(pattern, bindings):
    if isinstance(pattern, str):
        return bindings.get(pattern, pattern)
    return (pattern[0], *(_instantiate(child, bindings) for child in pattern[1:]))


def _library(rules, max_atoms):
    names = set()
    rewrites = []
    for rule in rules:
        name = rule["name"]
        if not isinstance(name, str) or not name or name in names:
            raise ValueError(f"empty or duplicate rule name {name!r}")
        names.add(name)
        left, right = (_parse(rule[k], pattern=True) for k in ("left", "right"))
        oracle = _truth_table(left, right, max_atoms)
        if oracle["equivalent"] is not True or rule.get("proof_status", "unsat") != "unsat":
            raise ValueError(f"unverified Boolean rewrite {name!r}: {oracle}")
        for direction, src, dst in [("forward", left, right), ("reverse", right, left)]:
            # An unbound variable on the replacement side cannot be instantiated.
            missing = {v for v in _atoms(dst) - _atoms(src) if v.startswith("?")}
            if not missing:
                rewrites.append((name, direction, src, dst))
    return rewrites


def _positions(node, path=()):
    yield path, node
    if isinstance(node, tuple):
        for i, child in enumerate(node[1:]):
            yield from _positions(child, (*path, i))


def _replace(node, path, new):
    if not path:
        return new
    args = list(node[1:])
    i = path[0]
    args[i] = _replace(args[i], path[1:], new)
    return (node[0], *args)


def _size(node):
    return 1 if isinstance(node, str) else 1 + sum(_size(n) for n in node[1:])


def _neighbors(node, rules):
    for path, part in _positions(node):
        for name, direction, src, dst in rules:
            bindings = {}
            if _match(src, part, bindings):
                rewritten = _instantiate(dst, bindings)
                if rewritten != part:
                    yield _replace(node, path, rewritten), (name, direction, path)


def _path(parents, end, *, invert):
    steps = []
    node = end
    while parents[node] is not None:
        prior, (rule, direction, path) = parents[node]
        before, after = (node, prior) if invert else (prior, node)
        if invert:
            direction = "reverse" if direction == "forward" else "forward"
        steps.append({"rule": rule, "direction": direction, "path": list(path),
                      "before": _text(before), "after": _text(after)})
        node = prior
    return steps if invert else list(reversed(steps))


def verify_path(left, right, rules, steps):
    """Check named rule, orientation, exact subterm, outside context, and both endpoints."""
    rule_table = {r["name"]: tuple(_parse(r[k], pattern=True) for k in ("left", "right")) for r in rules}
    current = _parse(left)
    for step in steps:
        if current != _parse(step["before"]) or step["direction"] not in ("forward", "reverse"):
            raise ValueError("invalid search proof continuity or direction")
        after = _parse(step["after"])
        src, dst = rule_table[step["rule"]]
        if step["direction"] == "reverse":
            src, dst = dst, src
        before_part, after_part = current, after
        for i in step["path"]:
            if (type(i) is not int or not isinstance(before_part, tuple) or not isinstance(after_part, tuple)
                    or not 0 <= i < min(len(before_part), len(after_part)) - 1):
                raise ValueError("invalid search proof subterm path")
            before_part, after_part = before_part[i + 1], after_part[i + 1]
        env = {}
        if (not _match(src, before_part, env) or not _match(dst, after_part, env)
                or _replace(current, step["path"], after_part) != after):
            raise ValueError("search proof changed a term outside the certified rewrite")
        current = after
    if current != _parse(right):
        raise ValueError("search proof missed requested endpoint")
    return True


def term_search(left, right, rules, budget=1000, *, max_term_nodes=64, oracle_max_atoms=12):
    """Bidirectional local rewrite search. A term or size cutoff gives an inconclusive result."""
    if budget < 0 or max_term_nodes < 1:
        raise ValueError("nonnegative term budget and positive expression-size bound required")
    rewrites = _library(rules, oracle_max_atoms)
    left, right = _parse(left), _parse(right)
    counts = {"visited_terms": 0, "expanded_terms": 0, "examined_rewrites": 0,
              "max_terms": budget, "max_term_nodes": max_term_nodes}

    def result(reason, steps=None):
        return {**counts, "proved": steps is not None, "stop_reason": reason, "steps": steps or []}

    if max(_size(left), _size(right)) > max_term_nodes:
        return result("term_size")
    if budget < len({left, right}):
        return result("term_budget")
    if left == right:
        counts["visited_terms"] = 1
        return result("identical", [])
    counts["visited_terms"] = 2
    parents = [{left: None}, {right: None}]
    front = [[left], [right]]
    blocked_size = blocked_count = False
    side = 1
    while front[0] or front[1]:
        if front[0] and front[1]:
            side = (1 - side) if len(front[0]) == len(front[1]) else int(len(front[1]) < len(front[0]))
        else:
            side = 0 if front[0] else 1
        layer = front[side]
        front[side] = []
        for current in layer:
            counts["expanded_terms"] += 1
            for neighbor, action in _neighbors(current, rewrites):
                counts["examined_rewrites"] += 1
                if neighbor in parents[side]:
                    continue
                if _size(neighbor) > max_term_nodes:
                    blocked_size = True
                    continue
                if neighbor in parents[1 - side]:
                    parents[side][neighbor] = (current, action)
                    route = _path(parents[0], neighbor, invert=False) + _path(parents[1], neighbor, invert=True)
                    verify_path(_text(left), _text(right), rules, route)
                    return result("joined", route)
                if counts["visited_terms"] >= budget:
                    blocked_count = True
                    continue
                parents[side][neighbor] = (current, action)
                front[side].append(neighbor)
                counts["visited_terms"] += 1
    return result("term_budget" if blocked_count else "term_size" if blocked_size else "exhausted")


def compare(left, right, rules, budget=1000, *, max_term_nodes=64, oracle_max_atoms=12):
    """Run two ordinary provers and an independent exhaustive truth-table oracle."""
    lk, rk = canonical_key(left), canonical_key(right)
    canonical = {"proved": lk == rk, "left_key": lk, "right_key": rk}
    search = term_search(left, right, rules, budget, max_term_nodes=max_term_nodes, oracle_max_atoms=oracle_max_atoms)
    oracle = truth_table(left, right, max_atoms=oracle_max_atoms)
    if oracle["equivalent"] is False and (canonical["proved"] or search["proved"]):
        raise ValueError("ordinary proof contradicted the exhaustive truth table")
    return {"canonical": canonical, "search": search, "oracle": oracle}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--left", required=True)
    cli.add_argument("--right", required=True)
    cli.add_argument("--rules", required=True, type=Path, help="JSON list of named pattern equalities")
    cli.add_argument("--budget", type=int, default=1000)
    cli.add_argument("--max-term-nodes", type=int, default=64)
    cli.add_argument("--oracle-max-atoms", type=int, default=12)
    args = cli.parse_args()
    print(json.dumps(compare(args.left, args.right, json.loads(args.rules.read_bytes()), args.budget,
                             max_term_nodes=args.max_term_nodes, oracle_max_atoms=args.oracle_max_atoms), indent=2))
