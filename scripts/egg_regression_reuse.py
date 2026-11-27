"""Shared proof-edge store for context-scoped transaction monitor revisions.

This is deliberately not destructive E-Graph rollback. Every stored edge is a
portable local equational derivation. Even when traversing an old edge in a new
context, every ground dependency must be supplied and typed-certified in the
active context, and the derivation is replayed against that context's rule names.
An absent dependency is a conservative reuse miss, not a counterexample.

The caller supplies the fact layer's *validated* evidence. Standalone auditors
can additionally re-run the exact typed obligations referenced by a reuse path.
Only equivalence is represented here; directed implication is not an e-class.
"""
from collections import defaultdict, deque
from copy import deepcopy
from hashlib import sha256
import json

import z3

from egg_frame_pc_cube_certificate import _apply, _symbols
from egg_regression_facts import SCOPE, SCHEMA_SHA256, context_id
from egg_txn_context import _check, _verify_query
from egg_txn_context_check import PATTERN_RULES, _fixed_schemas
from egg_txn_terms import abstract, format_term, parse_term, z3_env, z3_term
from m3_proof_dependencies import _plain, _subterm


def _digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             allow_nan=False).encode()).hexdigest()


RULE_SHA256 = _digest(PATTERN_RULES)


def _require(condition, reason):
    if not condition:
        raise ValueError(reason)


def _abstract(source):
    compact, atoms = abstract(parse_term(source))
    return compact, {k: format_term(v) for k, v in atoms.items()}


def _validate_atoms(atoms):
    _require(isinstance(atoms, dict), "expected a typed atom inventory")
    for name, typed in atoms.items():
        compact, binding = _abstract(typed)
        _require(compact == name and binding == {name: typed}, "typed primitive binding changed")


def _merge_atoms(a, b):
    result = dict(a)
    for key, typed in b.items():
        _require(result.setdefault(key, typed) == typed, "conflicting typed atom meanings")
    return result


def _typed_literal(node, atoms):
    if isinstance(node, str) and node in {"true", "false"}:
        return node
    if isinstance(node, str) and node in atoms:
        return atoms[node]
    if isinstance(node, tuple) and len(node) == 2 and node[0] == "not" and node[1] in atoms:
        return f"(not {atoms[node[1]]})"
    raise ValueError("ground fact must bind a literal or a complemented primitive")


def _commitment(guard, row, receipt, atoms):
    """Check the binding before matching facts; SHA is not a solver proof."""
    ctx = context_id(guard)
    _require(set(row) == {"name", "left", "right", "event_context", "proof_status"}
             and row["event_context"] == ctx and row["proof_status"] == "unsat",
             "wrong-context or malformed ground dependency")
    left, right = _plain(row["left"]), _plain(row["right"])
    _require(isinstance(left, str) and left in atoms and left.startswith("bv_"),
             "left ground dependency must be a typed primitive comparison")
    _require(row["name"] == "ctx-" + _digest([ctx, row["left"], row["right"]])[:24],
             "scope- or endpoint-mismatched dependency name")
    left_typed, right_typed = _typed_literal(left, atoms), _typed_literal(right, atoms)
    _require(set(receipt) == {"guard", "typed_left", "typed_right", "query"}
             and receipt["guard"] == guard and receipt["typed_left"] == left_typed
             and receipt["typed_right"] == right_typed,
             "ground receipt detached from its typed source and guard")
    query = receipt["query"]
    _require(query["status"] == "unsat" and isinstance(query["smt2"], str) and
             query["smt2_sha256"] == sha256(query["smt2"].encode()).hexdigest(),
             "invalid ground receipt")
    return row["left"], row["right"], left_typed, right_typed


def _check_receipt(guard, receipt):
    env = z3_env()
    formula = z3.And(z3_term(parse_term(guard), env), z3.Xor(
        z3_term(parse_term(receipt["typed_left"]), env), z3_term(parse_term(receipt["typed_right"]), env)))
    fresh, _ = _check(formula)
    _require(fresh["status"] == "unsat", "ground dependency is not valid in this context")
    _verify_query(receipt["query"], fresh)


def _current(left, right, guard, evidence, prepared, *, verify_current_facts=False):
    _require(evidence["guard"] == guard and evidence["context_id"] == context_id(guard),
             "ground evidence used under a different guard")
    feasibility = evidence["feasibility"]
    _require(feasibility["status"] == "sat", "reuse requires a feasible guard, not a vacuous equivalence")
    # Bind every supplied group abstraction to its exact original typed source.
    expected_abstracts, expected_atoms = [], {}
    _require(left in prepared["sources"] and right in prepared["sources"],
             "reuse endpoints not included in the current group")
    for source in prepared["sources"]:
        compact, atoms = _abstract(source)
        expected_abstracts.append(compact)
        expected_atoms = _merge_atoms(expected_atoms, atoms)
    _require(prepared["abstracts"] == expected_abstracts and prepared["atoms"] == expected_atoms,
             "group abstraction or typed atom table changed")
    bindings = {}
    names = set()
    for row in evidence["facts"]:
        name = row["name"]
        _require(name not in names and name in evidence["receipts"], "duplicate or missing ground receipt")
        names.add(name)
        receipt = evidence["receipts"][name]
        commitment = _commitment(guard, row, receipt, expected_atoms)
        _require(commitment not in bindings, "duplicate typed ground fact")
        bindings[commitment] = (row, receipt)
        if verify_current_facts:
            _check_receipt(guard, receipt)
    _require(names == set(evidence["receipts"]), "foreign ground receipts in current context")
    if verify_current_facts:
        fresh, _ = _check(z3_term(parse_term(guard), z3_env()))
        _verify_query(feasibility, fresh)
    return {"atoms": expected_atoms, "bindings": bindings,
            "left": _abstract(left)[0], "right": _abstract(right)[0]}


def _schemas(rows):
    schemas = dict(_fixed_schemas())
    for row in rows:
        _require(row["name"] not in schemas, "duplicate or conflicting proof rule")
        schemas[row["name"]] = (_plain(row["left"]), _plain(row["right"]))
    return schemas


def _replay(left, right, steps, schemas, vocabulary):
    current = _plain(left)
    _require(isinstance(steps, list) and _symbols(current) <= vocabulary,
             "invalid step list or foreign source atom")
    used = _symbols(current)
    reverse = []
    for step in steps:
        # Apply first, which validates exact schema, direction, path and local binding.
        following = _apply(current, step, schemas, vocabulary)
        old = _subterm(current, step["path"])
        reverse.append({"rule": step["rule"], "direction": {"forward": "reverse", "reverse": "forward"}[step["direction"]],
                        "path": step["path"].copy(), "replacement": format_term(old)})
        used |= _symbols(following)
        current = following
    _require(current == _plain(right), "proof's final endpoint differs from its original source")
    reverse.reverse()
    return used, reverse


def _record(entry_id, record, scope):
    _require(entry_id == "proof-" + _digest(record), "stored proof content does not match its ID")
    _require(set(record) == {"scope", "schema_sha256", "rule_sha256", "guard", "context_id", "left", "right",
                             "abstracts", "atoms", "steps", "dependencies"}
             and record["scope"] == scope and record["schema_sha256"] == SCHEMA_SHA256
             and record["rule_sha256"] == RULE_SHA256 and record["context_id"] == context_id(record["guard"]),
             "stored proof scope or rule inventory changed")
    _validate_atoms(record["atoms"])
    for i, side in enumerate(("left", "right")):
        compact, atoms = _abstract(record[side])
        _require(compact == record["abstracts"][i] and all(record["atoms"].get(k) == v for k, v in atoms.items()),
                 "stored typed endpoints or atom binding changed")
    rows, bindings = [], {}
    for dependency in record["dependencies"]:
        _require(set(dependency) == {"rule", "receipt"}, "malformed stored dependency")
        row, receipt = dependency["rule"], dependency["receipt"]
        commitment = _commitment(record["guard"], row, receipt, record["atoms"])
        _require(row["name"] not in bindings, "duplicate stored dependency")
        rows.append(row)
        bindings[row["name"]] = commitment
    _require(record["steps"] and {s["rule"] for s in record["steps"]} - _fixed_schemas().keys() == bindings.keys(),
             "missing or unused stored ground dependencies")
    _replay(*record["abstracts"], record["steps"], _schemas(rows), set(record["atoms"]))
    return bindings


def _evaluate_edge(entry_id, record, source, guard, current, scope):
    if record["left"] == source:
        direction = "forward"
    elif record["right"] == source:
        direction = "reverse"
    else:
        raise ValueError("attempted proof path with disconnected endpoints")
    bindings = _record(entry_id, record, scope)
    missing = sorted(name for name, commitment in bindings.items() if commitment not in current["bindings"])
    if missing:
        return None, {"entry_id": entry_id, "old_guard": record["guard"], "new_guard": guard,
                      "missing_current_dependencies": missing}
    remapping = {name: current["bindings"][commitment][0]["name"] for name, commitment in bindings.items()}
    rows = [current["bindings"][commitment][0] for commitment in bindings.values()]
    atoms = _merge_atoms(current["atoms"], record["atoms"])
    steps = [{**s, "rule": remapping.get(s["rule"], s["rule"])} for s in record["steps"]]
    schemas = _schemas(rows)
    _, reverse = _replay(*record["abstracts"], steps, schemas, set(atoms))
    target = record["right"] if direction == "forward" else record["left"]
    if direction == "reverse":
        steps = reverse
        _replay(*reversed(record["abstracts"]), steps, schemas, set(atoms))
    return {"entry_id": entry_id, "direction": direction, "left": source, "right": target,
            "old_guard": record["guard"], "new_guard": guard, "steps": steps,
            "used_ground_rules": sorted(remapping.values())}, None


def _result(status, edges=(), reasons=()):
    return {"proved": status in ("identity", "reused", "revalidated"), "status": status,
            "edges": list(edges), "used_ground_rules": sorted({n for e in edges for n in e["used_ground_rules"]}),
            "reasons": list(reasons)}


class ProofStore:
    """Store checked derivations, not native class identifiers or solver verdicts."""

    def __init__(self, scope=SCOPE):
        _require(scope == SCOPE, "unsupported typed semantic scope")
        self.scope = scope
        self.entries = {}

    def add(self, left, right, guard, evidence, prepared, proof):
        if not proof["proved"]:
            return None
        current = _current(left, right, guard, evidence, prepared)
        by_name = {r["name"]: (r, s) for r, s in current["bindings"].values()}
        names = sorted({s["rule"] for s in proof["steps"]} - _fixed_schemas().keys())
        _require(names == proof["used_ground_rules"] and all(n in by_name for n in names),
                 "edge has a detached or misstated ground-rule dependency")
        rows = [by_name[n][0] for n in names]
        used, _ = _replay(current["left"], current["right"], proof["steps"], _schemas(rows), set(current["atoms"]))
        if not proof["steps"]:
            return None  # Structural identity can always be checked directly.
        for row in rows:
            used |= _symbols(_plain(row["left"])) | _symbols(_plain(row["right"]))
        record = {"scope": self.scope, "schema_sha256": SCHEMA_SHA256, "rule_sha256": RULE_SHA256,
                  "guard": guard, "context_id": context_id(guard), "left": left, "right": right,
                  "abstracts": [current["left"], current["right"]], "atoms": dict(sorted((k, current["atoms"][k]) for k in used)),
                  "steps": proof["steps"], "dependencies": [{"rule": by_name[n][0], "receipt": by_name[n][1]} for n in names]}
        entry_id = "proof-" + _digest(record)
        _record(entry_id, record, self.scope)
        self.entries.setdefault(entry_id, deepcopy(record))
        return entry_id

    def lookup(self, left, right, guard, evidence, prepared):
        current = _current(left, right, guard, evidence, prepared)
        if current["left"] == current["right"]:
            return _result("identity")
        adjacency = defaultdict(list)
        for entry_id, rec in self.entries.items():
            adjacency[rec["left"]].append(entry_id)
            adjacency[rec["right"]].append(entry_id)
        # Prioritize a path of already in-scope proofs, then try additionally
        # permitted cross-context edges. Breadth-first search minimizes edge count,
        # not total flat-proof length; it is deterministic under ID tie-breaking.
        blocked = {}
        for cross in (False, True):
            seen = {left}
            queue = deque([(left, [])])
            while queue:
                source, prefix = queue.popleft()
                for entry_id in sorted(adjacency[source]):
                    rec = self.entries[entry_id]
                    if not cross and rec["guard"] != guard:
                        continue
                    target = rec["right"] if rec["left"] == source else rec["left"]
                    if target in seen:
                        continue
                    edge, reason = _evaluate_edge(entry_id, rec, source, guard, current, self.scope)
                    if edge is None:
                        blocked[entry_id] = reason
                        continue
                    path = [*prefix, edge]
                    if target == right:
                        return _result("reused" if all(e["old_guard"] == guard for e in path) else "revalidated", path)
                    seen.add(target)
                    queue.append((target, path))
        # Distinguish an old topological path blocked by removed evidence from
        # a completely new/disconnected request. No claim of inequivalence.
        seen, queue = {left}, deque([left])
        while queue:
            source = queue.popleft()
            for entry_id in adjacency[source]:
                rec = self.entries[entry_id]
                target = rec["right"] if rec["left"] == source else rec["left"]
                if target == right:
                    _require(blocked, "internal proof search inconsistency")
                    return _result("blocked", reasons=[blocked[e] for e in sorted(blocked)])
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        return _result("miss")


def verify_reuse(left, right, guard, evidence, prepared, result, entries, scope=SCOPE, *, verify_current_facts=False):
    """Verify positive path evidence independently of its creator/search decisions.

    A failed lookup carries no semantic finding. This verifier cannot prove
    that no better proof exists. Use the prefix store when auditing a miss.
    """
    _require(scope == SCOPE, "unsupported typed semantic scope")
    current = _current(left, right, guard, evidence, prepared, verify_current_facts=verify_current_facts)
    _require(result.keys() == {"proved", "status", "edges", "used_ground_rules", "reasons"}, "malformed reuse record")
    if result["status"] == "identity":
        _require(current["left"] == current["right"] and result == _result("identity"), "false identity reuse")
    elif result["status"] in ("reused", "revalidated"):
        cursor, edges = left, []
        for stored in result["edges"]:
            _require(stored["entry_id"] in entries, "unknown prior proof ID")
            edge, _ = _evaluate_edge(stored["entry_id"], entries[stored["entry_id"]], cursor, guard, current, scope)
            _require(edge is not None and edge == stored, "path edge differs from the checked current-context derivation")
            edges.append(edge)
            cursor = edge["right"]
        status = "reused" if all(e["old_guard"] == guard for e in edges) else "revalidated"
        _require(edges and cursor == right and result == _result(status, edges), "proof path does not connect the exact requested endpoints")
    elif result["status"] in ("miss", "blocked"):
        _require(result == _result(result["status"], reasons=result["reasons"]) and
                 bool(result["reasons"]) == (result["status"] == "blocked"), "invalid reuse miss record")
    else:
        raise ValueError("unknown reuse status")
    return True
