"""Source-preserving A/B/C feedback for the disclosed FIFO stress variant."""
from __future__ import annotations

import json

from run_midterm_fixed import ROOT, sha
from run_sfifo_stress_fixed import SOURCE
from sfifo_fixture import FIELDS

INSTRUCTIONS = """Generate only JSON cycle actions for the fixed depth-16 FIFO specification checker. You may change stimulus only. The DUT, checker, clock/reset driver, coverage denominator, and cycle budget are fixed. Each action is applied before a rising edge. Maximize uncovered DUT line and branch counters, including distinct source locations, within the cycle limit. A checker finding on faulty RTL is useful evidence; do not suppress it. Return JSON only with an actions array and no prose."""
SPEC = ROOT / "examples/heldout_sfifo_stress/docs/specification.md"
SEED = ROOT / "configs/sfifo_stress_seed.json"


def raw_feedback(points: list[dict]) -> list[dict]:
    lines = SOURCE.read_text().splitlines()
    return [{"source": point["source"], "line": point["line"],
             "column": point["column"], "counter_type": point["type"],
             "outcome": point["outcome"], "hits": point["hits"],
             "source_text": lines[point["line"] - 1].strip()}
            for point in points if point["hits"] == 0 and
            point["type"] in ("line", "branch", "expr")]


def egg_feedback(semantic: dict, screen: dict, points: list[dict]) -> dict:
    if sha(SOURCE) != semantic["source_sha256"] or sha(SOURCE) != screen["variant_sha256"]:
        raise AssertionError("E-graph extraction or screen does not match pinned DUT")
    source = str(SOURCE.relative_to(ROOT))
    if semantic["source"] != source:
        raise AssertionError("E-graph source path mismatch")
    eclasses = {row["id"]: row["nodes"] for row in semantic["egg"]["eclasses"]}
    targets = {row["id"]: row for row in semantic["extraction"]["targets"]}
    groups = []
    for group in screen["groups"]:
        # Show mapped groups from source/egg/Z3 evidence; calibration is used
        # only to select the DUT and never to filter C's live feedback.
        if not all(m["seed_coverage"].get("status") == "mapped" for m in group["members"]):
            continue
        members = []
        for member, target_id in zip(group["members"], group["member_ids"]):
            mapped = member["seed_coverage"]
            matches = [p for p in points if p["source"] == source and
                       (p["line"], p["column"], p["type"], p["outcome"]) ==
                       (member["line"], mapped["column"], mapped["type"], mapped["outcome"])]
            if len(matches) != 1:
                raise AssertionError(f"Original source counter changed: {member['line']}")
            target = targets[target_id]
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
                           "eclass_nodes": eclasses[group["eclass_local"]],
                           "z3_pair_checks": group["z3_pair_checks"]})
    return {"engine": semantic["egg"]["engine"],
            "iterations": semantic["egg"]["iterations"],
            "stop_reason": semantic["egg"]["stop_reason"],
            "semantics": "Typed two-state combinational guards only; complete activation, source and synchronous reset/clock context preserved. Original counters remain separate. No four-state or state-transition equivalence claim.",
            "source_sha256": semantic["source_sha256"],
            "atoms": semantic["extraction"]["atoms"],
            "equivalent_uncovered_groups": groups,
            "unsupported_extraction": semantic["extraction"]["unsupported"]}


def messages_for(arm: str, actions: list[dict], result: dict, log: str,
                 points: list[dict], semantic: dict | None, screen: dict | None,
                 round_no: int, limit: int) -> list[dict]:
    if arm not in ("A", "B", "C"):
        raise ValueError("Unknown feedback arm")
    payload = {"specification": SPEC.read_text(),
               "rtl": {str(SOURCE.relative_to(ROOT)): SOURCE.read_text()},
               "initial_stimulus": json.loads(SEED.read_text())["actions"],
               "previous_generated_actions": actions,
               "round": round_no, "max_new_cycles": limit,
               "stimulus_fields_and_widths": FIELDS,
               "checker": {"checks": result["checker"]["checks"],
                           "distinct_defects": result["checker"]["distinct_defects"],
                           "first_failures": result["checker"]["failures"][:8],
                           "execution_log": [line for line in log.splitlines()
                                             if line.startswith("TRACE ")][-40:]}}
    if arm in ("B", "C"):
        payload["raw_uncovered_dut_coverage"] = raw_feedback(points)
    if arm == "C":
        if semantic is None or screen is None:
            raise ValueError("C requires proven semantic extraction and screen")
        payload["egg_normalization"] = egg_feedback(semantic, screen, points)
    return [{"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": json.dumps(payload, sort_keys=True)}]
