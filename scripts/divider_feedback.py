"""A/B/C/placebo feedback with source-preserving typed divider guards."""
from __future__ import annotations

import json

from divider_fixture import FIELDS
from run_divider_fixed import ROOT, SOURCE
from run_midterm_fixed import sha

INSTRUCTIONS = """Generate only JSON cycle actions for the fixed 8-bit divider specification checker. You may change stimulus only. The DUT, checker, clock/reset driver, coverage denominator, and cycle budget are fixed. Each action is applied before a rising edge. Maximize uncovered DUT line and branch counters, including distinct source locations, within the cycle limit. Keep dividend and divisor stable while an operation is pending; do not assert start while busy. A checker finding on faulty RTL is useful evidence; do not suppress it. Return JSON only with an actions array and no prose."""


def raw_feedback(points):
    lines = SOURCE.read_text().splitlines()
    return [{"source": p["source"], "line": p["line"], "column": p["column"],
             "counter_type": p["type"], "outcome": p["outcome"],
             "hits": p["hits"], "source_text": lines[p["line"] - 1].strip()}
            for p in points if p["hits"] == 0 and p["type"] in ("line", "branch", "expr")]


def egg_feedback(semantic, screen, points):
    if sha(SOURCE) != semantic["source_sha256"] or sha(SOURCE) != screen["source_sha256"]:
        raise AssertionError("E-graph source hash mismatch")
    source = str(SOURCE.relative_to(ROOT))
    if semantic["source"] != source:
        raise AssertionError("Stale E-graph source path")
    target_by_id = {t["id"]: t for t in semantic["extraction"]["targets"]}
    class_nodes = {c["id"]: c["nodes"] for c in semantic["egg"]["eclasses"]}
    groups = []
    for group in screen["groups"]:
        if not group["qualifies_preflight"]:
            continue
        members = []
        for member, target_id in zip(group["members"], group["member_ids"]):
            mapped = member["seed_coverage"]
            matches = [p for p in points if p["source"] == source and
                       (p["line"], p["column"], p["type"], p["outcome"]) ==
                       (member["line"], mapped["column"], mapped["type"], mapped["outcome"])]
            if len(matches) != 1:
                raise AssertionError(f"Coverage mapping changed at {member['line']}")
            target = target_by_id[target_id]
            members.append({"source": source, "line": member["line"],
                            "column": mapped["column"], "counter_type": mapped["type"],
                            "outcome": mapped["outcome"], "hits": matches[0]["hits"],
                            "original_guard": target["compact"],
                            "case_value": target["case_value"],
                            "source_mapping": target["source_mapping"]})
        if any(member["hits"] == 0 for member in members):
            groups.append({"eclass": group["eclass_local"],
                           "event_context": group["event_context"],
                           "complete_activation_guard": group["reference_guard"],
                           "members": members,
                           "eclass_nodes": class_nodes[group["eclass_local"]],
                           "z3_pair_checks": group["z3_pair_checks"]})
    return {"engine": semantic["egg"]["engine"],
            "iterations": semantic["egg"]["iterations"],
            "stop_reason": semantic["egg"]["stop_reason"],
            "semantics": "Unsigned typed two-state combinational guards only; full activation, source and asynchronous-reset/clock event context preserved. No four-state or state-transition equivalence claim. Original coverage locations remain separate.",
            "source_sha256": semantic["source_sha256"],
            "atoms": semantic["extraction"]["atoms"],
            "equivalent_uncovered_groups": groups,
            "unsupported_extraction": semantic["extraction"]["unsupported"]}


def placebo_for(egg):
    # Match the UTF-8 byte length of C's extra JSON value while providing no
    # predicate IDs, source lines, behavioral relationships, or witnesses.
    target = len(json.dumps(egg, sort_keys=True).encode("utf-8"))
    prefix = "Neutral formatting appendix. No additional verification evidence. "
    return (prefix * ((target // len(prefix)) + 1))[:target]


def messages_for(arm, actions, result, log, points, semantic, screen, round_no, limit):
    if arm not in ("A", "B", "P", "C"):
        raise ValueError("Unknown arm")
    payload = {"specification": (ROOT / "examples/heldout_divider/docs/specification.md").read_text(),
               "rtl": {str(SOURCE.relative_to(ROOT)): SOURCE.read_text()},
               "initial_stimulus": json.loads((ROOT / "configs/divider_seed.json").read_text())["actions"],
               "previous_generated_actions": actions, "round": round_no,
               "max_new_cycles": limit, "stimulus_fields_and_widths": FIELDS,
               "checker": {"checks": result["checker"]["checks"],
                           "distinct_defects": result["checker"]["distinct_defects"],
                           "first_failures": result["checker"]["failures"][:8],
                           "execution_log": [line for line in log.splitlines()
                                             if line.startswith("TRACE ")][-40:]}}
    if arm in ("B", "P", "C"):
        payload["raw_uncovered_dut_coverage"] = raw_feedback(points)
    if arm in ("P", "C"):
        if semantic is None or screen is None:
            raise ValueError("Placebo and C require fixed semantic length evidence")
        enriched = egg_feedback(semantic, screen, points)
        if arm == "C":
            payload["egg_normalization"] = enriched
        else:
            payload["neutral_length_matched_appendix"] = placebo_for(enriched)
    return [{"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": json.dumps(payload, sort_keys=True)}]
