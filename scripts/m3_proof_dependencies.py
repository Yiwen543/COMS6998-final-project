#!/usr/bin/env python3
"""Check egg 0.11 flat Boolean guard proofs and extract the rules actually used."""
import argparse
from functools import cache
from itertools import product
import json
from pathlib import Path
import re

from predicates import evaluate


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


def _pattern_variables(term):
    if isinstance(term, str):
        if term in ("true", "false"):
            return set()
        if term.startswith("?"):
            return {term}
        raise ValueError(f"design atom {term!r} in generic Boolean pattern")
    return set().union(*(_pattern_variables(child) for child in term[1:]))


def _compile_pattern_rules(pattern_rules):
    """Check each schema universally over its own Boolean variables before use."""
    if not isinstance(pattern_rules, list):
        raise ValueError("generic pattern_rules must be a JSON list")
    rules, rows = {}, {}
    for record in pattern_rules:
        if (not isinstance(record, dict) or set(record) != {"name", "left", "right"} or
                any(not isinstance(value, str) for value in record.values())):
            raise ValueError("generic rule must contain string name, left and right")
        name = record["name"]
        if not re.fullmatch(r"[^\s()]+", name) or name in rules:
            raise ValueError(f"invalid or duplicate generic rule name {name!r}")
        lhs, rhs = (_plain(record[side], pattern=True) for side in ("left", "right"))
        variables = sorted(_pattern_variables(lhs))
        if set(variables) != _pattern_variables(rhs):
            raise ValueError(f"different variable sets in bidirectional rule {name!r}")
        for assignment in product((False, True), repeat=len(variables)):
            env = dict(zip(variables, assignment, strict=True))
            if evaluate(lhs, env) != evaluate(rhs, env):
                raise ValueError(f"unsound Boolean rule {name!r} for {env}")
        rules[name] = (lhs, rhs)
        rows[name] = 1 << len(variables)
    return rules, rows


def validate_pattern_rules(pattern_rules):
    """Return the number of exhaustively verified Boolean valuations for each named rule."""
    _, rows = _compile_pattern_rules(pattern_rules)
    return rows


def _context_id(context):
    # JSON Booleans and integers are distinct scope values, even though Python
    # considers True == 1 and False == 0. Match egg's typed JSON grouping.
    return json.dumps(context, sort_keys=True, separators=(",", ":"), allow_nan=False)


class ProofChecker:
    """Compile the Boolean rule table once and replay any number of raw egg edges."""

    def __init__(self, payload, *, pattern_rules=None):
        terms = cache(_plain)  # local to this proof graph
        if "pattern_rules" in payload and (pattern_rules is None or pattern_rules != payload["pattern_rules"]):
            raise ValueError("supplied generic rule inventory does not match payload")
        self.pattern_mode = pattern_rules is not None
        if self.pattern_mode:
            if payload.get("verified_rules") != []:
                raise ValueError("generic assertion proofs require an empty list of ground rules")
            if not payload["targets"] or any(not isinstance(t.get("id"), str) or t.get("event_context") is None
                                             for t in payload["targets"]):
                raise ValueError("generic assertion targets require string IDs and explicit event contexts")
            rules, self.pattern_rows = _compile_pattern_rules(pattern_rules)
            self.builtin_names = set()
            ground_rules = []
        else:
            rules = {name: (terms(lhs, pattern=True), terms(rhs, pattern=True)) for name, (lhs, rhs) in BUILTINS.items()}
            self.pattern_rows = {}
            self.builtin_names = set(BUILTINS)
            ground_rules = payload["verified_rules"]
        self.ground_names = set()
        rule_context = {}
        for rule in ground_rules:
            name = rule["name"]
            if not isinstance(name, str) or not re.fullmatch(r"[^\s()]+", name) or name in rules:
                raise ValueError(f"invalid or duplicate rule name {name!r}")
            if rule["proof_status"] != "unsat":
                raise ValueError(f"uncertified rule {name!r}")
            rules[name] = (terms(rule["left"]), terms(rule["right"]))
            self.ground_names.add(name)
            if "event_context" in rule:
                rule_context[name] = _context_id(rule["event_context"])
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
        context = _context_id(self.by_id[left].get("event_context"))
        if context != _context_id(self.by_id[right].get("event_context")):
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
            if allowed_ground_rules is not None and name in self.ground_names and name not in allowed_ground_rules:
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
        result = {"left": left, "right": right, "steps": steps,
                  "ground_rules": sorted(names & self.ground_names), "builtin_rules": sorted(names & self.builtin_names)}
        if self.pattern_mode:
            result["pattern_rules"] = sorted(names & self.pattern_rows.keys())
        return result


def validate_proof_dependencies(payload, graph, *, pattern_rules=None):
    """Replay named local rewrites, check endpoint connectivity, and return JSON-safe dependencies.

    Validity of each supplied ground equality is a separate certification obligation.
    This checker verifies proofs between input targets. Egg does not emit a proof from
    each target to its extracted representative in this schema.
    """
    checker = ProofChecker(payload, pattern_rules=pattern_rules)
    if checker.pattern_mode:
        if "pattern_rules" in graph and graph["pattern_rules"] != pattern_rules:
            raise ValueError("engine returned a different generic rule inventory")
        if "pattern_rule_count" in graph and graph["pattern_rule_count"] != len(checker.pattern_rows):
            raise ValueError("changed generic pattern rule count")
    if graph["stop_reason"] != "Some(Saturated)" or graph["ground_rule_count"] != len(checker.ground_names):
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
        if any(type(root) is not int or root < 0 for root in (old, new)):
            raise ValueError(f"invalid e-class identity for {target_id!r}")
        term = checker.terms(target["compact"])
        if term_roots.setdefault(term, old) != old or root_terms.setdefault(old, term) != term:
            raise ValueError("pre-saturation class disagrees with an input expression")
        if post_roots.setdefault(old, new) != new:
            raise ValueError("structurally identical endpoints left their shared class")
        context = _context_id(target.get("event_context"))
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
        if (a["eclass"] != b["eclass"] or a["eclass_before"] == b["eclass_before"] or
                _context_id(by_id[left].get("event_context")) != _context_id(by_id[right].get("event_context"))):
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
    audit = {"edges": edges, "ground_rules": sorted(used_ground), "builtin_rules": sorted(used_builtin),
             "checked_edges": len(edges), "checked_steps": sum(len(edge["steps"]) for edge in edges)}
    if checker.pattern_mode:
        audit["pattern_rules"] = sorted({name for edge in edges for name in edge["pattern_rules"]})
        audit["pattern_truth_table_rows"] = checker.pattern_rows
    return audit


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
    patterns = payload.get("pattern_rules")
    audit = validate_proof_dependencies(payload, graph, pattern_rules=patterns)
    if args.using_rule is None and args.edge is None:
        print(json.dumps(audit, indent=2))
    else:
        targets = {t["id"]: t for t in payload["targets"]}
        names = (set(audit["pattern_truth_table_rows"]) if patterns is not None else
                 set(BUILTINS) | {r["name"] for r in payload["verified_rules"]})
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
