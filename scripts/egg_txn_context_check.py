"""Replay a single context-scoped Boolean egg graph with certified primitive facts.

The caller binds the two input abstractions to their original typed sources and
rechecks every local fact's typed SMT receipt and the entire context partition.
The graph on its own establishes an equality conditional on its listed facts.
"""
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
import re

from egg_frame_pc_cube_certificate import RULES as CUBE_RULES, _apply, _symbols
from egg_frame_terms import format_term
from m3_proof_dependencies import _pattern_variables, _plain, _subterm, _term
from predicates import evaluate


_FROZEN = tuple((row["name"], row["left"], row["right"]) for row in CUBE_RULES) + (
    ("and-associate-right", "(and (and ?a ?b) ?c)", "(and ?a (and ?b ?c))"),
    ("or-associate-right", "(or (or ?a ?b) ?c)", "(or ?a (or ?b ?c))"),
    ("and-commute", "(and ?a ?b)", "(and ?b ?a)"),
    ("or-commute", "(or ?a ?b)", "(or ?b ?a)"),
)
PATTERN_RULES = [dict(name=name, left=left, right=right) for name, left, right in _FROZEN]
GOAL_STOP = 'Some(Other("TargetsMerged"))'
SATURATED = "Some(Saturated)"
LIMIT = re.compile(r"Some\((?:(?:Node|Iteration)Limit\([0-9]+\)|TimeLimit\([0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\))\)")


def _require(ok, reason):
    if not ok:
        raise ValueError(reason)


def _fields(item, names, reason):
    _require(isinstance(item, dict) and item.keys() == set(names), reason)


@lru_cache(maxsize=1)
def _fixed_schemas():
    schemas = {}
    for name, lhs, rhs in _FROZEN:
        left, right = _plain(lhs, pattern=True), _plain(rhs, pattern=True)
        names = sorted(_pattern_variables(left))
        _require(name not in schemas and _pattern_variables(right) <= set(names), "rule introduces an unbound variable")
        for values in product((False, True), repeat=len(names)):
            env = dict(zip(names, values, strict=True))
            _require(evaluate(left, env) == evaluate(right, env), f"unsound generic rule {name!r}")
        schemas[name] = left, right
    return schemas


def _payload(payload):
    _fields(payload, ("context_id", "targets", "pattern_rules", "ground_rules"), "unexpected context request schema")
    scope = payload["context_id"]
    _require(isinstance(scope, str) and scope.strip(), "empty context identifier")
    targets = payload["targets"]
    _require(isinstance(targets, list) and len(targets) == 2, "expected exactly two targets")
    for row in targets:
        _fields(row, ("id", "compact", "event_context"), "invalid input target")
        _require(row["id"] in ("left", "right") and row["event_context"] == scope and
                 isinstance(row["compact"], str), "cross-context or invalid target")
    ids = [row["id"] for row in targets]
    _require(sorted(ids) == ["left", "right"], "target labels must be left and right")
    endpoints = [_plain(row["compact"]) for row in targets]
    vocabulary = _symbols(endpoints[0]) | _symbols(endpoints[1])
    rows = payload["pattern_rules"]
    _require(isinstance(rows, list), "invalid pattern rule inventory")
    for row in rows:
        _fields(row, ("name", "left", "right"), "malformed generic rule")
    _require(tuple((r["name"], r["left"], r["right"]) for r in rows) == _FROZEN,
             "generic rule inventory differs from the frozen 23 rules")
    schemas = dict(_fixed_schemas())
    grounds = payload["ground_rules"]
    _require(isinstance(grounds, list), "expected context ground rule list")
    ground_names = set()
    for row in grounds:
        _fields(row, ("name", "left", "right", "event_context", "proof_status"), "malformed ground rule")
        name = row["name"]
        _require(row["event_context"] == scope and row["proof_status"] == "unsat", "wrong context or uncertified fact")
        _require(isinstance(name, str) and re.fullmatch(r"[^\s()]+", name) and name not in schemas,
                 "invalid or duplicate ground rule name")
        _require(isinstance(row["left"], str) and isinstance(row["right"], str), "invalid ground rule expression")
        identity = json.dumps([scope, row["left"], row["right"]], sort_keys=True, separators=(",", ":")).encode()
        _require(name == "ctx-" + sha256(identity).hexdigest()[:24], "fact name does not bind its context and endpoints")
        left, right = _plain(row["left"]), _plain(row["right"])
        valid_right = (isinstance(right, str) and right in vocabulary | {"true", "false"} or
                       isinstance(right, tuple) and right[0] == "not" and right[1] in vocabulary)
        _require(isinstance(left, str) and left in vocabulary and valid_right, "fact must relate original primitive leaves")
        schemas[name] = left, right
        ground_names.add(name)
    return ids, endpoints, vocabulary, schemas, ground_names


def _replay(edge, ids, endpoints, schemas, vocabulary):
    _fields(edge, ("left", "right", "explanation"), "unexpected explanation edge schema")
    _require([edge["left"], edge["right"]] == ids, "wrong or reversed native edge endpoints")
    _require(isinstance(edge["explanation"], str) and edge["explanation"].strip(), "missing flat explanation")
    lines = edge["explanation"].splitlines()
    current = _plain(lines[0])
    _require(current == endpoints[0], "proof does not start at the original first target")
    steps = []
    for line in lines[1:]:
        following, annotations = _term(line)
        _require(len(annotations) == 1, "expected exactly one named rewrite per step")
        path, direction, name = annotations[0]
        step = {"rule": name, "path": list(path), "direction": direction,
                "replacement": format_term(_subterm(following, path))}
        # _apply binds the pattern on both sides to the same environment. For a
        # reversed erasing rule it also reads the witness from the NEW subtree.
        _require(_apply(current, step, schemas, vocabulary) == following, "rewrite changed another subtree")
        current = following
        steps.append(step)
    _require(steps and current == endpoints[1], "missing proof or incorrect final original endpoint")
    return steps


def check_graph(payload, graph):
    """Validate native provenance and replay the exact derivation, even on a resource stop."""
    ids, endpoints, vocabulary, schemas, ground_names = _payload(payload)
    if graph is None:
        return {"proved": False, "steps": [], "status": "no_graph", "stop": None, "used_ground_rules": []}
    _fields(graph, ("engine", "context_id", "stop_reason", "iterations", "enodes", "eclasses", "pattern_rule_count",
                    "ground_rule_count", "targets", "rewrite_explanations"), "unexpected context graph schema")
    _require(graph["context_id"] == payload["context_id"] and graph["engine"] == "egg 0.11.0", "wrong engine or graph context")
    for k in ("iterations", "enodes", "eclasses", "pattern_rule_count", "ground_rule_count"):
        _require(type(graph[k]) is int and graph[k] >= 0, "invalid native graph counter")
    _require(graph["pattern_rule_count"] == len(_FROZEN) and graph["ground_rule_count"] == len(ground_names),
             "native rule counts differ from request")
    stop = graph["stop_reason"]
    _require(isinstance(stop, str) and (stop in (GOAL_STOP, SATURATED) or LIMIT.fullmatch(stop)),
             "unknown graph stop reason")
    rows = graph["targets"]
    _require(isinstance(rows, list) and len(rows) == 2, "missing target class records")
    for name, row in zip(ids, rows, strict=True):
        _fields(row, ("id", "eclass_before", "eclass"), "invalid target class record")
        _require(row["id"] == name and all(type(row[k]) is int and row[k] >= 0 for k in ("eclass_before", "eclass")),
                 "wrong target or invalid class id")
    identical = endpoints[0] == endpoints[1]
    merged = rows[0]["eclass"] == rows[1]["eclass"]
    _require(identical == (rows[0]["eclass_before"] == rows[1]["eclass_before"]), "inconsistent initial structural identity")
    _require(stop != GOAL_STOP or merged, "goal stop without target merge")
    edges = graph["rewrite_explanations"]
    _require(isinstance(edges, list), "invalid edge list")
    steps = []
    if identical:
        _require(merged and not edges, "structural identity has inconsistent evidence")
        status = "structural_identity"
    elif merged:
        _require(len(edges) == 1, "merged distinct terms require one complete explanation")
        steps = _replay(edges[0], ids, endpoints, schemas, vocabulary)
        status = "checked_derivation"
    else:
        _require(not edges, "unexpected proof for unmerged terms")
        status = "saturated_miss" if stop == SATURATED else "limited"
    return {"proved": identical or bool(steps), "steps": steps, "status": status, "stop": stop,
            "used_ground_rules": sorted({s["rule"] for s in steps} & ground_names)}
