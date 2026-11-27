"""Frozen semantic-regression workload (actual archive and explicitly authored controls).

Each request compares two *violation* predicates in a single current scope.
Strengthening therefore means every old alarm is still reported and at least
one additional alarm is possible.  ``previous_guard`` is only version-history
metadata, never an additional assumption in the current query.  No solver
verdict participates in case selection or in computing the expected labels.
"""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from audit_egg_fifo_live import read_archive
from egg_regression_facts import SCOPE, SCHEMA_SHA256, context_id
from egg_txn_terms import REFERENCES, parse_term, referenced_signals
from predicates import ROOT


ARCHIVE = ROOT / "results/milestone3/frame-txn-live/transcript.tar.gz"
ARCHIVE_INVENTORY_SHA256 = "d516f3063cb0c2354c842c572c92a6a8c4505bdadca217ce6b6d4b26999a914b"
ARMS = ("raw", "ordinary", "egg")
PROPERTIES = tuple(sorted(REFERENCES))
RELATIONS = ("equivalent", "strengthened", "weakened", "incomparable", "unknown")
GUARDS = tuple(f"({op} data_n 4)" for op in ("ult", "eq", "ugt"))
POLARITY = "violation predicate (true means alarm); old implies new = stronger assertion"
TYPED_SCHEMA_SHA256 = SCHEMA_SHA256


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _archive_inventory(files):
    paths = sorted(p for p in files if p == "config.json" or p.endswith(("/response.json", "/request.json")))
    rows = [[p, sha256(files[p]).hexdigest()] for p in paths]
    _require(len(paths) == 43, "expected frozen configuration and 21 request/response pairs")
    return sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()


def load_versions(archive):
    """Read all 21 actual Responses receipts; no synthetic new model responses.

    Pin request/response/config member *content*, so the equivalent original
    Mac archive with AppleDouble metadata or the cleaned archive both work.
    """
    files = read_archive(Path(archive))
    _require(_archive_inventory(files) == ARCHIVE_INVENTORY_SHA256,
             "archived request/response inventory differs from the frozen source")
    config = json.loads(files["config.json"])
    _require(config["mode"] == "live" and config["task"] == "frame-transaction-v1"
             and config["trials"] == 3 and config["repair_rounds"] == 2
             and tuple(config["arms"]) == ARMS, "wrong archive task or design")
    versions, receipts = {}, set()
    for trial in range(1, 4):
        paths = [f"trial-{trial:02d}/initial"] + [
            f"trial-{trial:02d}/{arm}/round-{r:02d}" for arm in ARMS for r in (1, 2)
        ]
        for prefix in paths:
            response_path = prefix + "/response.json"
            request_path = prefix + "/request.json"
            response = json.loads(files[response_path])
            _require(response["dispatch_attempted"] is True and response["http_status"] == 200
                     and response["status"] == "completed" and response["model"] == config["provider"]["model"]
                     and isinstance(response["usage"], dict), "expected a real completed model receipt")
            _require(isinstance(response["id"], str) and response["id"] not in receipts, "repeated response ID")
            receipts.add(response["id"])
            monitors = response["output"]["monitors"]
            _require(set(monitors) == set(PROPERTIES), "missing or extra transaction monitor")
            for text in monitors.values():
                parse_term(text)
            versions[prefix] = {
                "monitors": monitors,
                "source": response_path,
                "response_id": response["id"],
                "request_sha256": sha256(files[request_path]).hexdigest(),
                "response_sha256": sha256(files[response_path]).hexdigest(),
            }
    _require(len(receipts) == 21, "unexpected number of completed model versions")
    return versions


def _modified(version, prop, text, label):
    """Derived version, explicitly distinct from archived model output."""
    return {"source": f"controlled:{label}:from:{version['source']}#{prop}",
            "monitors": {prop: text}, "response_id": None,
            "request_sha256": None, "response_sha256": None}


def workload(archive=ARCHIVE):
    """Return an ordered frozen list of explicit per-property comparisons.

    Round 0 compares first→second and second→third independent initial suites;
    round 1 requests first→third (a separate, potentially transitive query).
    Rounds 2/3 replay the genuine chronological same-arm revisions.  Initial
    comparisons are *not* actual successive LLM revisions.  The last rounds
    are prospective functional monitor controls, not API calls or model errors.
    """
    versions = load_versions(archive)
    initials = [versions[f"trial-{t:02d}/initial"] for t in (1, 2, 3)]
    rows = []

    def add(cohort, round_number, prop, left, right, relation, guard="true", *, previous_guard=None, control=None):
        _require(relation in RELATIONS and prop in PROPERTIES, "invalid fixed workload label")
        previous_guard = guard if previous_guard is None else previous_guard
        for formula in (left["monitors"][prop], right["monitors"][prop], guard, previous_guard):
            parse_term(formula)
        scope_id = context_id(guard)
        rows.append({
            "id": f"R{len(rows) + 1:04d}", "cohort": cohort, "round": round_number,
            "property": prop, "left": left["monitors"][prop], "right": right["monitors"][prop],
            "guard": guard, "previous_guard": previous_guard, "left_guard": previous_guard,
            "scope": SCOPE, "scope_id": scope_id, "previous_scope_id": context_id(previous_guard),
            "typed_schema_sha256": TYPED_SCHEMA_SHA256,
            "scope_changed": previous_guard != guard, "group": f"{round_number}:{scope_id}",
            "expected_relation": relation, "polarity": POLARITY, "control": control,
            "left_source": left["source"], "right_source": right["source"],
            "left_response_id": left["response_id"], "right_response_id": right["response_id"],
            "left_request_sha256": left["request_sha256"], "right_request_sha256": right["request_sha256"],
            "left_response_sha256": left["response_sha256"], "right_response_sha256": right["response_sha256"],
        })

    # Full-domain baseline; known equivalent labels are inherited from the prior
    # independent full-width transaction audit, not recomputed to choose cases.
    # Separate contextual checks use a predeclared exhaustive N<4,N=4,N>4 split.
    for round_number, pairs in ((0, ((0, 1), (1, 2))), (1, ((0, 2),))):
        for i, j in pairs:
            for prop in PROPERTIES:
                add("real_initial", round_number, prop, initials[i], initials[j], "equivalent")
            for guard in GUARDS:
                add("real_context", round_number, "data_last", initials[i], initials[j], "equivalent", guard)

    # Every actual revision in all three arms and three trials, including the
    # unchanged output. Repeated identical transitions are actual occurrences,
    # not independent responses or proof-discovery opportunities.
    for r in (1, 2):
        for trial in (1, 2, 3):
            for arm in ARMS:
                prefix = f"trial-{trial:02d}/{arm}"
                old = versions[f"trial-{trial:02d}/initial"] if r == 1 else versions[prefix + "/round-01"]
                new = versions[prefix + f"/round-{r:02d}"]
                _require(old["monitors"] == new["monitors"], "unexpected genuine revision in the frozen no-change archive")
                for prop in PROPERTIES:
                    add("real_history", r + 1, prop, old, new, "equivalent")

    # Predeclared strict weakening of every monitor: introduce an extra ready
    # gate which is not in its archived source.  It suppresses existing alarms
    # when ready=0.  The inverse chronological update restores the original
    # predicate and strengthens it.  This is a synthetic control, not a claim
    # that an actual model did this or that the witness is reachable in RTL.
    first = initials[0]
    weakened = {}
    for prop in PROPERTIES:
        gate = "m_ready" if prop.startswith("data_") else "h_ready" if prop.startswith("header_") else "s_ready"
        old = first["monitors"][prop]
        _require(gate not in referenced_signals(parse_term(old)), "controlled weakening gate already occurs in old formula")
        version = _modified(first, prop, f"(and {old} {gate})", f"extra-{gate}-gate")
        weakened[prop] = version
        add("controlled_revision", 4, prop, first, version, "weakened", control=f"extra-{gate}-gate")

    tlast = first["monitors"]["data_last"]
    _require(tlast.count("(uge data_n 4)") == 1, "exact-four control anchor changed")
    gap = _modified(first, "data_last", tlast.replace("(uge data_n 4)", "(ugt data_n 4)"), "exact-four-gap")
    # Dropping the equality boundary in an XOR monitor can add and remove
    # alarms, rather than simply weakening the property in one direction.
    add("controlled_revision", 4, "data_last", first, gap, "incomparable", control="exact-four-gap")
    for guard, relation in zip(GUARDS, ("equivalent", "incomparable", "equivalent"), strict=True):
        add("controlled_scope", 4, "data_last", first, gap, relation, guard, control="localize-exact-four-gap")

    reset = first["monitors"]["reset_clear"]
    _require(reset.count("phase_post") == 1, "reset phase control anchor changed")
    wrong_phase = _modified(first, "reset_clear", reset.replace("phase_post", "(not phase_post)"), "wrong-sampling-phase")
    add("controlled_revision", 4, "reset_clear", first, wrong_phase, "incomparable", control="wrong-sampling-phase")

    for prop in PROPERTIES:
        add("controlled_revision", 5, prop, weakened[prop], first, "strengthened", control="restore-original-alarm")

    # Scoped-proof lifecycle: identical endpoints, scope N=4 → N=5 → N=4.
    # A proof that (I=N) equals (I=4) under the initial scope must NOT survive
    # the switch to five. The reference current comparison is always evaluated
    # under the *new* scope, even if an older proof is present. On returning to
    # the original scope a correctly keyed cache may safely recover it.
    _require(tlast.count("(eq data_index data_n)") == 1, "fixed-index control anchor changed")
    fixed = _modified(first, "data_last", tlast.replace("(eq data_index data_n)", "(eq data_index 4)"), "fixed-index-four")
    g4, g5 = "(eq data_n 4)", "(eq data_n 5)"
    add("controlled_scope", 5, "data_last", first, fixed, "equivalent", g4, control="certify-at-four")
    add("controlled_scope", 6, "data_last", first, fixed, "incomparable", g5, previous_guard=g4, control="scope-edit-four-to-five")
    add("controlled_scope", 7, "data_last", first, fixed, "equivalent", g4, previous_guard=g5, control="restore-four-scope")

    _require(len(rows) == 224 and len({c["id"] for c in rows}) == len(rows), "frozen workload cardinality changed")
    _require(all(a["round"] <= b["round"] for a, b in zip(rows, rows[1:])), "round order changed")
    return rows


def inventory(rows):
    """Report actual occurrences separately from scoped derived queries/controls."""
    result = {}
    for cohort in sorted({c["cohort"] for c in rows}):
        group = [c for c in rows if c["cohort"] == cohort]
        result[cohort] = {
            "requests": len(group),
            "identical_source_formulas": sum(c["left"] == c["right"] for c in group),
            "different_endpoint_pairs": len({(c["property"], c["guard"], c["left"], c["right"]) for c in group}),
            "scope_edits": sum(c["scope_changed"] for c in group),
            "relation_counts": dict(Counter(c["expected_relation"] for c in group)),
        }
    return {"new_api_calls": 0, "original_response_receipts": 21, "independent_llm_initial_suites": 3,
            "cohorts": result, "total_requests": len(rows),
            "archive_inventory_sha256": ARCHIVE_INVENTORY_SHA256}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive", type=Path, default=ARCHIVE)
    p.add_argument("--output", type=Path, help="Write all frozen requests to JSON (optional)")
    args = p.parse_args()
    requests = workload(args.archive)
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(requests, stream, indent=2, sort_keys=True)
            stream.write("\n")
    print(json.dumps(inventory(requests), indent=2, sort_keys=True))
