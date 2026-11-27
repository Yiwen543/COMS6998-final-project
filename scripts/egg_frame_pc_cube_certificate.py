"""Prove a signed candidate reduces to true after substituting only its observed minimum cube."""
from itertools import product
import json
from pathlib import Path
import re
import subprocess

from egg_frame_pc_certificate import MAX_CHARS, MAX_STEPS, TIMEOUT_SECONDS
from egg_frame_pc_diagnosis import diagnose, verify_diagnosis_record
from egg_frame_terms import abstract, format_term, parse_term
from m3_proof_dependencies import _matches, _pattern_variables, _plain, _replace, _subterm, _term
from predicates import evaluate


# Fixed independently of the reviewed expression and sample. No design atoms,
# reference properties, targets, distribution rules or hand-written equalities.
_TRIPLES = [
    ("and-true-left", "(and true ?a)", "?a"), ("and-true-right", "(and ?a true)", "?a"),
    ("and-false-left", "(and false ?a)", "false"), ("and-false-right", "(and ?a false)", "false"),
    ("or-false-left", "(or false ?a)", "?a"), ("or-false-right", "(or ?a false)", "?a"),
    ("or-true-left", "(or true ?a)", "true"), ("or-true-right", "(or ?a true)", "true"),
    ("not-false", "(not false)", "true"), ("not-true", "(not true)", "false"),
    ("double-not", "(not (not ?a))", "?a"),
    ("and-complement-right", "(and ?a (not ?a))", "false"),
    ("and-complement-left", "(and (not ?a) ?a)", "false"),
    ("or-complement-right", "(or ?a (not ?a))", "true"), ("or-complement-left", "(or (not ?a) ?a)", "true"),
    ("and-idempotent", "(and ?a ?a)", "?a"), ("or-idempotent", "(or ?a ?a)", "?a"),
    ("de-morgan-or", "(not (or ?a ?b))", "(and (not ?a) (not ?b))"),
    ("de-morgan-and", "(not (and ?a ?b))", "(or (not ?a) (not ?b))"),
]
RULES = [dict(name=n, left=a, right=b) for n, a, b in _TRIPLES]
SCOPE = "Signed candidate with the listed literals fixed and all remaining Boolean atoms free"
ACCEPTED_STOPS = {'Some(Other("TargetsMerged"))', "Some(Saturated)"}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _json(x):
    return json.dumps(x, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":"))


def _rules(records):
    """Forward erasure is allowed. Check every valuation of every LHS variable."""
    schemas, rows = {}, {}
    registered = {name: (a, b) for name, a, b in _TRIPLES}
    for rule in records:
        _require(isinstance(rule, dict) and set(rule) == {"name", "left", "right"}, "invalid cube rule")
        name = rule["name"]
        _require(name not in schemas and registered.get(name) == (rule["left"], rule["right"]),
                 "unexpected or duplicate cube rule")
        left, right = (_plain(rule[k], pattern=True) for k in ("left", "right"))
        variables = sorted(_pattern_variables(left))
        _require(_pattern_variables(right) <= set(variables), "rule introduced a free variable")
        for values in product((False, True), repeat=len(variables)):
            env = dict(zip(variables, values, strict=True))
            _require(evaluate(left, env) == evaluate(right, env), "rule fails a Boolean valuation")
        schemas[name] = (left, right)
        rows[name] = 1 << len(variables)
    return schemas, rows


def _symbols(node):
    if isinstance(node, str):
        return set() if node in ("true", "false") else {node}
    return set().union(*(_symbols(v) for v in node[1:]))


def _restrict(node, substitutions):
    if isinstance(node, str):
        return substitutions.get(node, node)
    return (node[0], *(_restrict(v, substitutions) for v in node[1:]))


def _residual(source, atoms, cube):
    original = _plain(source)
    _require(isinstance(atoms, dict) and set(atoms) == _symbols(original), "wrong original atom inventory")
    for name, typed in atoms.items():
        leaf = parse_term(typed)
        abstracted, mapping = abstract(leaf)
        _require(abstracted == name and mapping == {name: leaf}, "invalid primitive atom binding")
    substitutions = {}
    _require(isinstance(cube, list), "missing signed cube")
    for lit in cube:
        _require(isinstance(lit, list) and len(lit) == 2 and isinstance(lit[0], str)
                 and lit[0] in atoms and lit[0] not in substitutions and type(lit[1]) is bool,
                 "invalid, duplicate, or foreign cube literal")
        substitutions[lit[0]] = "true" if lit[1] else "false"
    return format_term(_restrict(original, substitutions))


def _bound(diagnosis):
    """Recompute the exact minimum and independently rerun the full-width implication via diagnose."""
    fresh = diagnose(diagnosis["candidate"], diagnosis["sample"], diagnosis["public"]["candidate_value"])
    verify_diagnosis_record(diagnosis, fresh)
    if fresh["public"]["status"] != "sufficient":
        return None
    receipt = diagnosis["oracle"]["typed_implication"]
    _require(receipt["status"] == "unsat" and fresh["oracle"]["signed_source_at_sample"] is True,
             "typed cube implication or observed candidate polarity unverified")
    return {**{k: fresh[k] for k in ("source", "atoms", "cube")},
            "candidate_value": fresh["public"]["candidate_value"],
            "restricted_source": _residual(fresh["source"], fresh["atoms"], fresh["cube"]),
            "typed_smt2_sha256": receipt["smt2_sha256"]}


def _apply(current, step, schemas, vocabulary):
    _require(isinstance(step, dict) and set(step) == {"rule", "direction", "path", "replacement"},
             "invalid cube proof step")
    _require(step["rule"] in schemas and step["direction"] in ("forward", "reverse"), "unknown rewrite/direction")
    path = step["path"]
    _require(isinstance(path, list) and all(type(i) is int and i in (0, 1) for i in path),
             "invalid rewrite path")
    old = _subterm(current, path)
    new = _plain(step["replacement"])
    _require(_symbols(new) <= vocabulary, "proof introduces a foreign design atom")
    lhs, rhs = schemas[step["rule"]]
    if step["direction"] == "reverse":
        lhs, rhs = rhs, lhs
    # A reversed erasing rule may introduce ?a. Bind it on the explicit new
    # subtree, and still require every repeated occurrence to agree.
    bindings = {}
    _require(_matches(lhs, old, bindings) and _matches(rhs, new, bindings), "rewrite failed local substitution")
    return _replace(current, path, new)


def _checked_steps(source, explanation, schemas):
    start = _plain(source)
    if explanation is None:
        _require(start == "true", "changed expression without an explanation")
        return []
    _require(isinstance(explanation, str) and explanation.strip(), "missing flat explanation")
    lines = explanation.splitlines()
    _require(_plain(lines[0]) == start, "flat proof starts at a different restricted candidate")
    current, vocabulary, steps = start, _symbols(start), []
    for line in lines[1:]:
        after, annotations = _term(line)
        _require(len(annotations) == 1, "expected one named rewrite per flat proof step")
        path, direction, name = annotations[0]
        step = {"rule": name, "direction": direction, "path": list(path),
                "replacement": format_term(_subterm(after, path))}
        _require(_apply(current, step, schemas, vocabulary) == after, "rewrite changed a different subterm")
        current = after
        steps.append(step)
    _require(current == "true", "flat proof did not finish at true")
    return steps


def replay_public_cube(public):
    """Replay the exact displayed compact certificate, using only its contents and fixed Boolean axioms."""
    keys = {"method", "status", "scope", "candidate_value", "source", "atoms", "cube",
            "restricted_source", "target", "steps", "rules"}
    _require(isinstance(public, dict) and set(public) == keys and public["method"] == "restricted_cube"
             and public["scope"] == SCOPE and public["target"] == "true"
             and type(public["candidate_value"]) is bool, "invalid cube certificate packet")
    steps = public["steps"]
    _require(isinstance(steps, list) and len(steps) <= MAX_STEPS and len(_json(public)) <= MAX_CHARS,
             "complete displayed proof exceeds budget")
    _require(public["status"] == ("checked_rewrite" if steps else "checked_identity"), "wrong certificate kind")
    residual = _residual(public["source"], public["atoms"], public["cube"])
    _require(residual == public["restricted_source"], "wrong substitutions in restricted source")
    schemas, _ = _rules(public["rules"])
    current = _plain(residual)
    vocabulary = _symbols(current)
    for step in steps:
        current = _apply(current, step, schemas, vocabulary)
    _require({s["rule"] for s in steps} == set(schemas) and current == "true", "incomplete rule list or proof")
    return True


def _unavailable(reason, evidence=None):
    return {"public": {"status": "unavailable", "reason": reason}, "evidence": evidence}


def _assess(bound, request, graph, transport):
    expected = {"term": bound["restricted_source"], "pattern_rules": RULES}
    _require(_json(request) == _json(expected), "engine request differs from restricted signed source")
    schemas, rows = _rules(RULES)
    evidence = {"engine_request": request, "engine": graph, "transport": transport,
                "cube_implies_signed_candidate": "unsat", "typed_smt2_sha256": bound["typed_smt2_sha256"],
                "rule_truth_table_rows": rows}
    if transport == "timeout":
        _require(graph is None, "recorded process timeout must not supply a graph")
        evidence["timeout_seconds"] = TIMEOUT_SECONDS
        return _unavailable("engine_process_timeout", evidence)
    _require(transport == "completed" and isinstance(graph, dict), "invalid engine transport or graph")
    _require(set(graph) == {"source", "target", "merged", "stop_reason", "explanation", "iterations",
                            "enodes", "eclasses"}, "unexpected engine graph schema")
    source = expected["term"]
    _require(graph["source"] == source and graph["target"] == "true" and type(graph["merged"]) is bool,
             "wrong engine endpoints or merge flag")
    _require(all(type(graph[k]) is int and graph[k] >= 0 for k in ("iterations", "eclasses", "enodes")),
             "invalid engine counters")
    stop = graph["stop_reason"]
    limited = stop not in ACCEPTED_STOPS
    if limited:
        _require(isinstance(stop, str) and re.fullmatch(r"Some\((?:Time|Node|Iteration)Limit\([^()]+\)\)", stop),
                 "unknown engine termination reason")
    if not graph["merged"]:
        _require((limited or stop == "Some(Saturated)") and graph["explanation"] is None and source != "true",
                 "inconsistent engine merge or proof")
        return _unavailable("engine_resource_limit" if limited else "goal_not_proved", evidence)
    steps = _checked_steps(source, graph["explanation"], schemas)
    evidence["checked_steps"] = steps
    used = {s["rule"] for s in steps}
    public = {"method": "restricted_cube", "status": "checked_rewrite" if steps else "checked_identity",
              "scope": SCOPE, **{k: bound[k] for k in ("candidate_value", "source", "atoms", "cube", "restricted_source")},
              "target": "true", "rules": [r.copy() for r in RULES if r["name"] in used], "steps": steps}
    if len(steps) > MAX_STEPS or len(_json(public)) > MAX_CHARS:
        return _unavailable("complete_proof_exceeds_budget", evidence)
    replay_public_cube(public)
    return {"public": public, "evidence": evidence}


def certify_cube(diagnosis, binary):
    """Run egg on exactly the restricted signed candidate and audit its proof before publication."""
    bound = _bound(diagnosis)
    if bound is None:
        return _unavailable("no_sufficient_common_cube")
    request = {"term": bound["restricted_source"], "pattern_rules": RULES}
    try:
        proc = subprocess.run([str(Path(binary).resolve(strict=True))], input=_json(request),
                              capture_output=True, text=True, check=True, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        return _assess(bound, request, None, "timeout")
    return _assess(bound, request, json.loads(proc.stdout), "completed")


def verify_cube_certificate(diagnosis, cert):
    """Rebind sample and exact cube, recheck the typed implication and replay the archived proof without egg."""
    bound = _bound(diagnosis)
    if bound is None:
        expected = _unavailable("no_sufficient_common_cube")
    else:
        evidence = cert["evidence"]
        expected = _assess(bound, evidence["engine_request"], evidence["engine"], evidence["transport"])
    _require(_json(expected) == _json(cert), "archived certificate differs from checked evidence")
    return True
