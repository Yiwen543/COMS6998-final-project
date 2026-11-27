"""Independent replay of explicit pair proofs from a shared, single-context egg graph.

The caller must reconstruct all original typed target bindings, certify the union of
primitive ground rules under this one guard, and verify the guard's context/scope.
A graph/class ID alone is not a certificate. Only requested edges with replayed
proofs (or exact structural identity) are accepted here. Facts may reference the
larger certified group vocabulary even in a graph containing only two targets.
"""
from hashlib import sha256
import json
import re

from egg_frame_pc_cube_certificate import _symbols
from egg_txn_context_check import (_FROZEN, _fields, _fixed_schemas, _replay, _require,
                                    GOAL_STOP, LIMIT, SATURATED, PATTERN_RULES)
from m3_proof_dependencies import _plain


def _atom(term):
    return (isinstance(term, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", term)
            and term not in ("true", "false", "and", "or", "not")
            and not term.startswith("Rewrite"))


def _payload(payload):
    _fields(payload, ("context_id", "targets", "pattern_rules", "ground_rules", "pairs"),
            "unexpected regression request schema")
    scope = payload["context_id"]
    _require(isinstance(scope, str) and scope.strip(), "empty context identifier")
    targets = payload["targets"]
    _require(isinstance(targets, list) and len(targets) >= 2, "expected at least two targets")
    endpoints = {}
    vocabulary = set()
    for row in targets:
        _fields(row, ("id", "compact", "event_context"), "invalid input target")
        name = row["id"]
        _require(isinstance(name, str) and name.strip() and name not in endpoints and
                 row["event_context"] == scope and isinstance(row["compact"], str),
                 "cross-context, invalid or duplicate target")
        endpoints[name] = _plain(row["compact"])
        leaves = _symbols(endpoints[name])
        _require(all(_atom(leaf) for leaf in leaves), "target contains invalid Boolean atom")
        vocabulary.update(leaves)
    pairs = payload["pairs"]
    _require(isinstance(pairs, list) and pairs, "expected explicit pairs")
    checked_pairs, seen_pairs = [], set()
    for pair in pairs:
        _require(isinstance(pair, list) and len(pair) == 2 and
                 all(isinstance(k, str) and k in endpoints for k in pair) and pair[0] != pair[1],
                 "invalid pair endpoints")
        _require(frozenset(pair) not in seen_pairs, "duplicate unordered pair")
        seen_pairs.add(frozenset(pair))
        checked_pairs.append(tuple(pair))
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
        _require(row["event_context"] == scope and row["proof_status"] == "unsat",
                 "wrong context or uncertified fact")
        _require(isinstance(name, str) and re.fullmatch(r"[^\s()]+", name) and name not in schemas,
                 "invalid or duplicate ground rule name")
        _require(isinstance(row["left"], str) and isinstance(row["right"], str),
                 "invalid ground rule expression")
        identity = json.dumps([scope, row["left"], row["right"]], sort_keys=True, separators=(",", ":")).encode()
        _require(name == "ctx-" + sha256(identity).hexdigest()[:24],
                 "fact name does not bind its context and endpoints")
        left, right = _plain(row["left"]), _plain(row["right"])
        valid_right = ((_atom(right) or right in ("true", "false")) if isinstance(right, str) else
                       isinstance(right, tuple) and right[0] == "not" and _atom(right[1]))
        _require(_atom(left) and valid_right, "fact must relate primitive leaves or constants")
        vocabulary.update(_symbols(left) | _symbols(right))
        schemas[name] = left, right
        ground_names.add(name)
    return endpoints, checked_pairs, vocabulary, schemas, ground_names


def check_graph(payload, graph):
    """Return {(left_id, right_id): independently replayed proof record}.

    Unknown graph/limit/miss does not prove disequality; explicit typed SMT
    direction checks (outside this module) establish genuine differences.
    """
    endpoints, pairs, vocabulary, schemas, ground_names = _payload(payload)
    if graph is None:
        return {pair: {"proved": False, "steps": [], "status": "no_graph", "stop": None,
                       "used_ground_rules": []} for pair in pairs}
    _fields(graph, ("engine", "context_id", "stop_reason", "iterations", "enodes", "eclasses", "pattern_rule_count",
                    "ground_rule_count", "targets", "rewrite_explanations"), "unexpected regression graph schema")
    _require(graph["context_id"] == payload["context_id"] and graph["engine"] == "egg 0.11.0",
             "wrong engine or graph context")
    for k in ("iterations", "enodes", "eclasses", "pattern_rule_count", "ground_rule_count"):
        _require(type(graph[k]) is int and graph[k] >= 0, "invalid native graph counter")
    _require(graph["pattern_rule_count"] == len(_FROZEN) and graph["ground_rule_count"] == len(ground_names),
             "native rule counts differ from request")
    stop = graph["stop_reason"]
    _require(isinstance(stop, str) and (stop in (GOAL_STOP, SATURATED) or LIMIT.fullmatch(stop)),
             "unknown graph stop reason")
    rows = graph["targets"]
    _require(isinstance(rows, list) and len(rows) == len(endpoints), "missing target class records")
    classes, by_ast, by_initial_class, final_of_initial = {}, {}, {}, {}
    for (name, term), row in zip(endpoints.items(), rows, strict=True):
        _fields(row, ("id", "eclass_before", "eclass"), "invalid target class record")
        _require(row["id"] == name and all(type(row[k]) is int and row[k] >= 0
                                           for k in ("eclass_before", "eclass")),
                 "wrong target or invalid class id")
        before, after = row["eclass_before"], row["eclass"]
        _require(by_ast.setdefault(term, before) == before and by_initial_class.setdefault(before, term) == term,
                 "inconsistent initial structural identity")
        _require(final_of_initial.setdefault(before, after) == after, "structurally identical class was split")
        classes[name] = after
    _require(stop != GOAL_STOP or all(classes[a] == classes[b] for a,b in pairs),
             "goal stop without all requested target merges")
    edges = graph["rewrite_explanations"]
    _require(isinstance(edges, list), "invalid edge list")
    explanations = {}
    requested = set(pairs)
    for edge in edges:
        _fields(edge, ("left", "right", "explanation"), "unexpected explanation edge schema")
        _require(isinstance(edge["left"], str) and isinstance(edge["right"], str),
                 "invalid explanation endpoints")
        pair = (edge["left"], edge["right"])
        _require(pair in requested and pair not in explanations, "unrequested, reversed or duplicate explanation")
        explanations[pair] = edge
    results = {}
    for pair in pairs:
        a, b = pair
        identical = endpoints[a] == endpoints[b]
        merged = classes[a] == classes[b]
        steps = []
        if identical:
            _require(merged and pair not in explanations, "structural identity has inconsistent evidence")
            status = "structural_identity"
        elif merged:
            _require(pair in explanations, "merged distinct terms require one complete explanation")
            steps = _replay(explanations[pair], list(pair), [endpoints[a], endpoints[b]], schemas, vocabulary)
            status = "checked_derivation"
        else:
            _require(pair not in explanations, "unexpected proof for unmerged terms")
            status = "saturated_miss" if stop == SATURATED else "limited"
        results[pair] = {"proved": identical or bool(steps), "steps": steps, "status": status, "stop": stop,
                         "used_ground_rules": sorted({s["rule"] for s in steps} & ground_names)}
    return results
