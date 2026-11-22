#!/usr/bin/env python3
"""Check egg 0.11 flat Boolean guard proofs and extract the rules actually used."""
import argparse
from functools import cache
import json
from pathlib import Path
import re


BUILTINS = {
    "de-morgan-or": ("(not (or ?a ?b))", "(and (not ?a) (not ?b))"),
    "de-morgan-and": ("(not (and ?a ?b))", "(or (not ?a) (not ?b))"),
    "double-not": ("(not (not ?a))", "?a"),
    "and-true": ("(and ?a true)", "?a"),
    "and-true-left": ("(and true ?a)", "?a"),
    "not-false": ("(not false)", "true"),
}
ARITY = {"not": 1, "and": 2, "or": 2}
DIRECTION = {"Rewrite=>": "forward", "Rewrite<=": "reverse"}


def _term(line, *, pattern=False):
    tokens = re.findall(r'\(|\)|[^\s()]+', line)
    index = 0
    annotations = []

    def read(path):
        nonlocal index
        if index >= len(tokens):
            raise ValueError("truncated expression")
        token = tokens[index]
        index += 1
        if token != "(":
            if token == ")" or token in DIRECTION or token.startswith("Rewrite"):
                raise ValueError(f"invalid atom {token!r}")
            if token.startswith("?") and (not pattern or not re.fullmatch(r"\?[A-Za-z_][A-Za-z0-9_]*", token)):
                raise ValueError(f"unexpected pattern variable {token!r}")
            return token
        if index >= len(tokens):
            raise ValueError("expected operator")
        op = tokens[index]
        index += 1
        if op in DIRECTION:
            if index >= len(tokens) or tokens[index] in ("(", ")"):
                raise ValueError("missing rewrite rule name")
            name = tokens[index]
            index += 1
            annotations.append((path, DIRECTION[op], name))
            value = read(path)
        elif op in ARITY:
            value = (op, *(read((*path, i)) for i in range(ARITY[op])))
        else:
            raise ValueError(f"unknown proof operator {op!r}")
        if index >= len(tokens) or tokens[index] != ")":
            raise ValueError(f"wrong arity or missing closing parenthesis for {op}")
        index += 1
        return value

    result = read(())
    if index != len(tokens):
        raise ValueError("trailing expression tokens")
    return result, annotations


def _plain(text, *, pattern=False):
    value, annotations = _term(text, pattern=pattern)
    if annotations:
        raise ValueError("unexpected annotation in original expression or rule definition")
    return value


def _subterm(tree, path):
    for step in path:
        if not isinstance(tree, tuple) or step + 1 >= len(tree):
            raise ValueError("annotation path is absent in previous term")
        tree = tree[step + 1]
    return tree


def _replace(tree, path, value):
    if not path:
        return value
    i = path[0] + 1
    return (*tree[:i], _replace(tree[i], path[1:], value), *tree[i + 1:])


def _matches(pattern, term, bindings):
    if isinstance(pattern, str):
        if pattern.startswith("?"):
            return bindings.setdefault(pattern, term) == term
        return pattern == term
    return (isinstance(term, tuple) and term[0] == pattern[0] and
            all(_matches(p, t, bindings) for p, t in zip(pattern[1:], term[1:], strict=True)))


class ProofChecker:
    """Compile the Boolean rule table once and replay any number of raw egg edges."""

    def __init__(self, payload):
        terms = cache(_plain)  # local to this proof graph
        rules = {name: (terms(lhs, pattern=True), terms(rhs, pattern=True)) for name, (lhs, rhs) in BUILTINS.items()}
        rule_context = {}
        for rule in payload["verified_rules"]:
            name = rule["name"]
            if not isinstance(name, str) or not re.fullmatch(r"[^\s()]+", name) or name in rules:
                raise ValueError(f"invalid or duplicate rule name {name!r}")
            if rule["proof_status"] != "unsat":
                raise ValueError(f"uncertified rule {name!r}")
            rules[name] = (terms(rule["left"]), terms(rule["right"]))
            if "event_context" in rule:
                rule_context[name] = rule["event_context"]
        self.terms = terms
        self.rules = rules
        self.rule_context = rule_context
        self.by_id = {t["id"]: t for t in payload["targets"]}
        if len(self.by_id) != len(payload["targets"]):
            raise ValueError("duplicate target ID")

    def check(self, edge, allowed_ground_rules=None):
        """Check one original edge or alternate intermediate edge independently of class IDs."""
        left, right = edge["left"], edge["right"]
        if left not in self.by_id or right not in self.by_id or left == right:
            raise ValueError(f"unknown or equal proof endpoints {left!r}, {right!r}")
        context = self.by_id[left].get("event_context")
        if context != self.by_id[right].get("event_context"):
            raise ValueError(f"proof crosses event contexts {left!r}, {right!r}")
        lines = edge["explanation"].splitlines()
        if len(lines) < 2:
            raise ValueError(f"missing rewrite step for {left!r}, {right!r}")
        previous = self.terms(lines[0])
        if previous != self.terms(self.by_id[left]["compact"]):
            raise ValueError(f"wrong start of proof {left!r}, {right!r}")
        steps = []
        for number, line in enumerate(lines[1:], start=1):
            current, annotations = _term(line)
            if len(annotations) != 1:
                raise ValueError(f"expected exactly one rewrite annotation in step {number}")
            path, direction, name = annotations[0]
            if name not in self.rules or (name in self.rule_context and self.rule_context[name] != context):
                raise ValueError(f"unknown or inapplicable rule {name!r} in step {number}")
            if allowed_ground_rules is not None and name not in BUILTINS and name not in allowed_ground_rules:
                raise ValueError(f"withdrawn rule {name!r} in step {number}")
            lhs, rhs = self.rules[name]
            if direction == "reverse":
                lhs, rhs = rhs, lhs
            old, new = _subterm(previous, path), _subterm(current, path)
            bindings = {}
            if (not _matches(lhs, old, bindings) or not _matches(rhs, new, bindings) or
                    _replace(previous, path, new) != current):
                raise ValueError(f"rewrite {name!r} at path {path} does not justify step {number}")
            steps.append({"rule": name, "direction": direction, "path": list(path)})
            previous = current
        if previous != self.terms(self.by_id[right]["compact"]):
            raise ValueError(f"wrong end of proof {left!r}, {right!r}")
        names = {s["rule"] for s in steps}
        ground, builtin = names - BUILTINS.keys(), names & BUILTINS.keys()
        return {"left": left, "right": right, "steps": steps,
                "ground_rules": sorted(ground), "builtin_rules": sorted(builtin)}


def validate_proof_dependencies(payload, graph):
    """Replay named local rewrites, check endpoint connectivity, and return JSON-safe dependencies.

    Validity of each supplied ground equality is a separate certification obligation.
    This checker verifies proofs between input targets. Egg does not emit a proof from
    each target to its extracted representative in this schema.
    """
    checker = ProofChecker(payload)
    if graph["stop_reason"] != "Some(Saturated)" or graph["ground_rule_count"] != len(payload["verified_rules"]):
        raise ValueError("incomplete graph or changed supplied rule count")

    targets = payload["targets"]
    by_id = checker.by_id
    outputs = {t["id"]: t for t in graph["targets"]}
    if len(by_id) != len(targets) or [t["id"] for t in graph["targets"]] != list(by_id):
        raise ValueError("missing, duplicate or reordered proof targets")
    # Before the first rewrite only identical trees can share an e-class.
    term_roots, root_terms, post_roots, groups = {}, {}, {}, {}
    for target_id, target in by_id.items():
        old, new = (outputs[target_id][k] for k in ("eclass_before", "eclass"))
        term = checker.terms(target["compact"])
        if term_roots.setdefault(term, old) != old or root_terms.setdefault(old, term) != term:
            raise ValueError("pre-saturation class disagrees with an input expression")
        if post_roots.setdefault(old, new) != new:
            raise ValueError("structurally identical endpoints left their shared class")
        context = json.dumps(target.get("event_context"), sort_keys=True)
        groups.setdefault((new, context), []).append(target_id)

    # Validate each claimed transition at its unique marked subtree, keeping the
    # surrounding context unchanged and using one substitution on both sides.
    edges = []
    parents = {name: name for name in by_id}

    def component(name):
        while parents[name] != name:
            parents[name] = parents[parents[name]]
            name = parents[name]
        return name

    used_ground, used_builtin, seen_edges = set(), set(), set()
    for edge in graph["rewrite_explanations"]:
        left, right = edge["left"], edge["right"]
        if left not in by_id or right not in by_id:
            raise ValueError(f"unknown proof endpoint {left!r}, {right!r}")
        a, b = outputs[left], outputs[right]
        context = by_id[left].get("event_context")
        if a["eclass"] != b["eclass"] or a["eclass_before"] == b["eclass_before"] or context != by_id[right].get("event_context"):
            raise ValueError(f"ineligible proof endpoints {left!r}, {right!r}")
        pair = frozenset((left, right))
        if pair in seen_edges:
            raise ValueError(f"duplicate proof edge {left!r}, {right!r}")
        seen_edges.add(pair)
        checked = checker.check(edge)
        used_ground.update(checked["ground_rules"])
        used_builtin.update(checked["builtin_rules"])
        edges.append(checked)
        parents[component(right)] = component(left)
    for members in groups.values():
        if len({outputs[name]["eclass_before"] for name in members}) > 1 and len({component(name) for name in members}) != 1:
            raise ValueError(f"missing proof connectivity for {members}")
    return {"edges": edges, "ground_rules": sorted(used_ground), "builtin_rules": sorted(used_builtin),
            "checked_edges": len(edges), "checked_steps": sum(len(edge["steps"]) for edge in edges)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="egg guard input with certified rules")
    parser.add_argument("--graph", type=Path, required=True, help="spanning or indexed result JSON")
    query = parser.add_mutually_exclusive_group()
    query.add_argument("--using-rule", help="find stored proofs that cite this rule")
    query.add_argument("--edge", nargs=2, metavar=("TARGET_A", "TARGET_B"),
                       help="inspect the checked steps for this stored pair of endpoints")
    args = parser.parse_args()
    payload = json.loads(args.input.read_bytes())
    graph = json.loads(args.graph.read_bytes())
    audit = validate_proof_dependencies(payload, graph)
    if args.using_rule is None and args.edge is None:
        print(json.dumps(audit, indent=2))
    else:
        targets = {t["id"]: t for t in payload["targets"]}
        names = set(BUILTINS) | {r["name"] for r in payload["verified_rules"]}
        if args.using_rule is not None and args.using_rule not in names:
            parser.error("unknown rule")
        if args.edge is not None:
            # CLI arguments are text; JSON literals also address numeric IDs.
            # Explicitly quoting a JSON string selects "1" when both 1 and "1" exist.
            by_json = {json.dumps(target): target for target in targets}
            selected = []
            for value in args.edge:
                if value in by_json:
                    selected.append(by_json[value])
                elif value in targets:
                    selected.append(value)
                else:
                    parser.error(f"unknown target: {value}")
            args.edge = selected
        rows = []
        for edge, raw in zip(audit["edges"], graph["rewrite_explanations"], strict=True):
            if args.edge is not None and set(args.edge) != {edge["left"], edge["right"]}:
                continue
            if args.using_rule is not None and not any(s["rule"] == args.using_rule for s in edge["steps"]):
                continue
            locations = [{k: targets[t][k] for k in ("id", "source", "line", "event_context", "instance_scope")
                          if k in targets[t]} for t in (edge["left"], edge["right"])]
            rows.append({**edge, "locations": locations, "proof": raw["explanation"].splitlines()})
        print(json.dumps({"stored_edges_checked": audit["checked_edges"], "matching_edges": len(rows),
                          "matches": rows}, indent=2))
