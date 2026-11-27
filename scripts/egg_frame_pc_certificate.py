"""Build and replay bounded, candidate-only DNF certificates for a shared minimum cube."""
import base64
import hashlib
import json
import re
from pathlib import Path
import subprocess
import tempfile

from egg_assertion_baseline import _instantiate
from egg_frame_diagnostic import RULES, check_engine, clause_form, restore
from egg_frame_diagnostic_baseline import minimum_cube, parse_dnf
from egg_frame_observe import sample
from egg_frame_proof import SCOPE, typed_oracle
from egg_frame_terms import abstract, format_term, parse_term, referenced_signals
from m3_proof_dependencies import ProofChecker, _matches, _plain, _replace, _subterm, validate_pattern_rules


MAX_STEPS = 32
MAX_CHARS = 6000
TIMEOUT_SECONDS = 30
MAX_RAW_BYTES = 8 * 1024 * 1024


def _require(test, message):
    if not test:
        raise ValueError(message)


def _json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(",", ":"))


def _unavailable(reason):
    return {"status": "unavailable", "reason": reason}


def _bind(diagnosis):
    common = diagnosis["public"]
    polarity = common["candidate_value"]
    _require(type(polarity) is bool, "invalid candidate polarity")
    candidate = parse_term(diagnosis["candidate"])
    signed = candidate if polarity else ("not", candidate)
    typed = format_term(signed)
    source, atoms = abstract(signed)
    printable = {name: format_term(ast) for name, ast in atoms.items()}
    _require((typed, source, printable) == (diagnosis["typed_source"], diagnosis["source"], diagnosis["atoms"]),
             "signed candidate source or atom binding changed")
    observed = diagnosis["sample"]
    _require(observed.keys() == referenced_signals(candidate), "sample must contain precisely the candidate pins")
    values = {k: -1 if v is None else v for k, v in observed.items()}
    _require(sample(candidate, values) is polarity, "candidate polarity differs from sampled pins")
    assignment = {name: sample(atom, values) for name, atom in atoms.items()}
    _require(_json(assignment) == _json(diagnosis["assignment"]), "sampled abstract atom values differ")
    exact = minimum_cube(source, assignment)
    cube = [list(literal) for literal in exact["cube"]] if exact["cube"] is not None else None
    _require(exact["status"] == "sufficient" and _json(cube) == _json(diagnosis["cube"]),
             "supplied cube differs from exact minimum for the signed candidate")
    literals = [{"term": printable[n], "value": v} for n, v in cube]
    _require(_json(common["sufficient_literals"]) == _json(literals) and common["literal_count"] == len(cube),
             "public common diagnosis differs from the shared cube")
    typed_cube = restore(clause_form(cube), atoms)
    # source XOR (source OR cube) is SAT exactly when cube fails to imply source.
    receipt = typed_oracle(typed, f"(or {typed} {typed_cube})")["oracle"]
    _require(receipt["status"] == "unsat", "candidate cube implication failed independent typed checking")
    return typed, source, atoms, cube


def _written_cube(dnf, cube):
    """Compare actual parsed DNF terms. No dropping duplicates, adding consensus, or choosing another cube."""
    def split(node, op):
        if isinstance(node, tuple) and node[0] == op:
            yield from split(node[1], op)
            yield from split(node[2], op)
        else:
            yield node

    target = sorted((name, value) for name, value in cube)
    for clause in split(_plain(dnf), "or"):
        if clause == "true" and not target:
            return True
        literals = []
        for term in split(clause, "and"):
            negated = isinstance(term, tuple)
            if negated and (term[0] != "not" or not isinstance(term[1], str)):
                raise ValueError("extracted term contains a nonliteral")
            name = term[1] if negated else term
            if name in ("true", "false"):
                break
            literals.append((name, not negated))
        else:
            if sorted(literals) == target:
                return True
    return False


def replay_public(public):
    """Replay the actual displayed trace using only its endpoints, rule definitions, and path per step."""
    expected = {"status", "candidate_value", "source", "dnf", "atoms", "cube", "rules", "steps"}
    _require(set(public) == expected and type(public["candidate_value"]) is bool, "invalid public proof packet")
    _require(len(_json(public)) <= MAX_CHARS and len(public["steps"]) <= MAX_STEPS, "public proof exceeds budget")
    rules = public["rules"]
    known = {rule["name"]: rule for rule in RULES}
    validate_pattern_rules(rules)
    _require(all(known.get(rule["name"]) == rule for rule in rules), "unexpected public rule definition")
    schemas = {rule["name"]: (_plain(rule["left"], pattern=True), _plain(rule["right"], pattern=True))
               for rule in rules}
    atoms = {}
    for name, text in public["atoms"].items():
        typed_atom = parse_term(text)
        printable, bound = abstract(typed_atom)
        _require(printable == name and bound == {name: typed_atom}, "bad typed atom mapping")
        atoms[name] = typed_atom
    cube = public["cube"]
    _require(all(isinstance(lit, list) and len(lit) == 2 and lit[0] in atoms and type(lit[1]) is bool
                 for lit in cube), "invalid public cube")
    _require(len({lit[0] for lit in cube}) == len(cube), "duplicate public cube atom")
    start = _plain(public["source"])
    current = start
    used = set()
    for step in public["steps"]:
        _require(set(step) == {"rule", "direction", "path"} and step["rule"] in schemas,
                 "unknown public rewrite")
        lhs, rhs = schemas[step["rule"]]
        _require(step["direction"] in ("forward", "reverse"), "invalid public rewrite direction")
        if step["direction"] == "reverse":
            lhs, rhs = rhs, lhs
        path = step["path"]
        _require(isinstance(path, list) and all(type(i) is int and i in (0, 1) for i in path),
                 "invalid public rewrite path")
        bindings = {}
        _require(_matches(lhs, _subterm(current, path), bindings), "public rewrite fails to match at its path")
        current = _replace(current, path, _instantiate(rhs, bindings))
        used.add(step["rule"])
    _require(set(schemas) == used and current == _plain(public["dnf"]), "displayed proof misses the endpoint")
    _require(public["status"] == ("checked_identity" if not public["steps"] else "checked_rewrite"),
             "wrong public proof kind")
    # Restoring both trees rejects invented abstract symbols even if a tampered path used them consistently.
    restored_source = parse_term(restore(public["source"], atoms))
    _require(abstract(restored_source)[1] == atoms, "extraneous public atom binding")
    restore(public["dnf"], atoms)
    parse_dnf(public["dnf"])
    _require(_written_cube(public["dnf"], cube), "displayed DNF lacks the common cube")
    return True


def _assess(diagnosis, bound, request, graph):
    typed, source, atoms, cube = bound
    _require(request == {"term": source, "pattern_rules": RULES}, "wrong candidate-only engine request")
    _require(graph["source"] == source, "different engine source")
    stop = graph["stop_reason"]
    saturated = stop == "Some(Saturated)"
    _require(saturated or re.fullmatch(r'Some\((?:(?:Time|Node|Iteration)Limit\([0-9.eE+-]+\)|Extraction(?:Time|Node|Depth)Limit)\)', stop),
             "unrecognized diagnostic stop reason")
    _require(all(type(graph[f]) is int and graph[f] > 0 for f in ("iterations", "enodes", "eclasses")),
             "invalid diagnostic graph counters")
    evidence = {"engine_request": request, "engine": graph, "signed_candidate": typed,
                "cube_implies_signed_candidate": "unsat", "checked_steps": []}
    if graph["extracted"] is None:
        _require(all(graph[f] is None for f in ("explanation", "clause_count", "literal_count")),
                 "missing extraction carries proof or costs")
        return {"public": {"status": "unavailable", "reason": "dnf_unavailable", "stop": stop}, "evidence": evidence}
    _require(saturated, "resource-limited extraction claimed an endpoint")
    extracted = graph["extracted"]
    def counts(node):
        if isinstance(node, str) or node[0] == "not":
            _require(isinstance(node, str) or isinstance(node[1], str), "nonliteral in written DNF")
            return 1, 1
        a, b = (counts(t) for t in node[1:])
        if node[0] == "and":
            _require(a[0] == b[0] == 1, "disjunction within written DNF clause")
            return 1, a[1] + b[1]
        return a[0] + b[0], a[1] + b[1]

    _require(all(type(graph[f]) is int for f in ("clause_count", "literal_count")) and
             counts(_plain(extracted)) == (graph["clause_count"], graph["literal_count"]),
             "reported DNF costs differ from the actual written tree")
    explained = _plain(source) != _plain(extracted)
    _require(explained == bool(graph["explanation"]), "changed DNF needs a full proof, identity needs none")
    try:
        checked = check_engine(typed, source, atoms, graph)
    except ValueError as exc:
        # The existing checker replays the complete flat proof FIRST. Report only
        # these exact errors from its subsequent typed obligation checks as limits.
        reason = {
            "term nesting exceeds 128 levels": "typed_depth_limit",
            "non-equivalent extracted property: unknown": "typed_solver_unknown",
            "clause is not certified sufficient: unknown": "typed_solver_unknown",
            "clause parse changed the extracted expression: unknown": "typed_solver_unknown",
        }.get(str(exc))
        if reason is None:
            raise
        if explained:
            targets = [{"id": n, "compact": t, "event_context": SCOPE} for n, t in
                       (("source", source), ("extracted", extracted))]
            checker = ProofChecker({"targets": targets, "verified_rules": [], "pattern_rules": RULES},
                                   pattern_rules=RULES)
            evidence["checked_steps"] = checker.check({"left": "source", "right": "extracted",
                                                       "explanation": graph["explanation"]})["steps"]
        return {"public": _unavailable(reason), "evidence": evidence}
    evidence["checked_steps"] = checked["checked_steps"]
    evidence["typed_checks"] = {
        "dnf": checked["typed_expression"], "source_xor_dnf": checked["equivalence"]["status"],
        "clause_union_xor_dnf": checked["scored_clause_union_equivalence"]["status"],
        "clauses": [{"term": c["clause"], "implication": c["implication"]["status"]} for c in checked["clauses"]]}
    steps = checked["checked_steps"]
    if not _written_cube(checked["extracted"], cube):
        return {"public": _unavailable("dnf_lacks_exact_common_cube"), "evidence": evidence}
    names = {step["rule"] for step in steps}
    public = {"status": "checked_rewrite" if steps else "checked_identity",
              "candidate_value": diagnosis["public"]["candidate_value"], "source": source,
              "dnf": checked["extracted"], "atoms": {k: format_term(v) for k, v in atoms.items()},
              "cube": cube, "rules": [dict(rule) for rule in RULES if rule["name"] in names], "steps": steps}
    if len(steps) > MAX_STEPS or len(_json(public)) > MAX_CHARS:
        return {"public": _unavailable("complete_proof_exceeds_budget"), "evidence": evidence}
    replay_public(public)
    return {"public": public, "evidence": evidence}


def _skip(diagnosis):
    status = diagnosis["public"]["status"]
    if status == "sufficient":
        return None
    _require(status in ("unknown", "atom_limit", "sample_mismatch", "sample_unknown", "oracle_unknown"), "unknown common diagnosis status")
    return {"public": _unavailable("no_sufficient_common_cube"), "evidence": None}


def _external(bound, request, event):
    _require(request == {"term": bound[1], "pattern_rules": RULES}, "external event bound to different input")
    required = {"kind", "byte_count", "sha256", "partial_base64", "timeout_seconds", "raw_byte_limit"}
    _require(set(event) == required and event["timeout_seconds"] == TIMEOUT_SECONDS and
             event["raw_byte_limit"] == MAX_RAW_BYTES and type(event["byte_count"]) is int and
             event["byte_count"] >= 0 and re.fullmatch("[0-9a-f]{64}", event["sha256"]),
             "invalid external resource-limit receipt")
    kind, count = event["kind"], event["byte_count"]
    _require(kind == "engine_timeout" or kind == "raw_output_limit" and count > MAX_RAW_BYTES,
             "inconsistent external resource-limit cause")
    if count <= MAX_RAW_BYTES:
        data = base64.b64decode(event["partial_base64"], validate=True)
        _require(len(data) == count and hashlib.sha256(data).hexdigest() == event["sha256"],
                 "partial output does not match its receipt")
    else:
        _require(event["partial_base64"] is None, "oversized output should have only a fingerprint")
    return {"public": _unavailable(kind), "evidence": {"engine_request": request, "tool_event": event,
            "signed_candidate": bound[0], "cube_implies_signed_candidate": "unsat"}}


def certify(diagnosis, binary):
    """Run source-only egg. A timeout is a tool observation and never provides a proof."""
    skip = _skip(diagnosis)
    if skip:
        return skip
    bound = _bind(diagnosis)
    request = {"term": bound[1], "pattern_rules": [dict(rule) for rule in RULES]}
    # Keep potentially large output out of process memory until its size is known.
    with tempfile.TemporaryFile() as out:
        try:
            subprocess.run([str(Path(binary).resolve(strict=True))], input=_json(request).encode(), stdout=out,
                           stderr=subprocess.PIPE, check=True, timeout=TIMEOUT_SECONDS)
            kind = None
        except subprocess.TimeoutExpired:
            kind = "engine_timeout"
        count = out.tell()
        out.seek(0)
        if kind is None and count <= MAX_RAW_BYTES:
            return _assess(diagnosis, bound, request, json.load(out))
        fingerprint = hashlib.file_digest(out, "sha256").hexdigest()
        out.seek(0)
        partial = base64.b64encode(out.read()).decode() if count <= MAX_RAW_BYTES else None
        return _external(bound, request, {"kind": kind or "raw_output_limit", "byte_count": count,
                         "sha256": fingerprint, "partial_base64": partial, "timeout_seconds": TIMEOUT_SECONDS,
                         "raw_byte_limit": MAX_RAW_BYTES})


def verify_certificate(diagnosis, certificate):
    """Independently bind the archived graph and the entire displayed packet to the diagnosis. No binary needed."""
    expected = _skip(diagnosis)
    if expected is None:
        evidence = certificate["evidence"]
        bound = _bind(diagnosis)
        if "tool_event" in evidence:
            expected = _external(bound, evidence["engine_request"], evidence["tool_event"])
        else:
            expected = _assess(diagnosis, bound, evidence["engine_request"], evidence["engine"])
    _require(_json(expected) == _json(certificate), "archived candidate proof or public packet differs")
    return True
