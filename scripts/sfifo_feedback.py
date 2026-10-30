"""Matched raw B and egg-enriched C feedback for fixed ZipCPU sfifo."""
from __future__ import annotations

import json

from run_midterm_fixed import ROOT, sha
from run_sfifo_fixed import SOURCE
from sfifo_fixture import FIELDS

INSTRUCTIONS = """Generate only JSON cycle actions for the fixed FIFO specification checker. You may change stimulus only. The DUT, checker, clock/reset driver, coverage denominator, and cycle budget are fixed. Each action is applied before a rising edge. Maximize uncovered DUT line and branch counters, including distinct source locations, within the cycle limit. A checker finding on faulty RTL is useful evidence; do not suppress it. Return JSON only with an actions array and no prose."""


def raw_feedback(points: list[dict]) -> list[dict]:
    lines = SOURCE.read_text().splitlines()
    return [{"source": point["source"], "line": point["line"],
             "column": point["column"], "counter_type": point["type"],
             "outcome": point["outcome"], "hits": point["hits"],
             "source_text": lines[point["line"] - 1].strip()}
            for point in points if point["hits"] == 0 and
            point["type"] in ("line", "branch", "expr")]


def egg_feedback(semantic: dict, points: list[dict]) -> dict:
    if sha(SOURCE) != semantic["source_sha256"]:
        raise AssertionError("E-graph extraction does not match fixed DUT bytes")
    source = str(SOURCE.relative_to(ROOT))
    if semantic["source"] != source:
        raise AssertionError("E-graph extraction has stale source provenance")
    eclasses = {row["id"]: row["nodes"] for row in semantic["egg"]["eclasses"]}
    targets = {row["id"]: row for row in semantic["extraction"]["targets"]}
    coverage = {(p["line"], p["column"], p["type"], p["outcome"]): p
                for p in points if p["source"] == source}
    groups = []
    for group in semantic["groups"]:
        members = []
        for target_id in group["member_ids"]:
            target = targets[target_id]
            candidates = [p for key, p in coverage.items()
                          if key[0] == target["line"] and key[2] == "line"]
            if len(candidates) != 1:
                raise AssertionError(f"Unmapped or ambiguous source line {target['line']}")
            point = candidates[0]
            members.append({"source": source, "line": target["line"],
                            "column": point["column"], "counter_type": point["type"],
                            "outcome": point["outcome"], "hits": point["hits"],
                            "case_value": target["case_value"],
                            "original_guard": target["compact"],
                            "source_mapping": target["source_mapping"]})
        if any(member["hits"] == 0 for member in members):
            groups.append({"eclass": group["eclass_local"],
                           "event_context": group["event_context"],
                           "complete_activation_guard": group["reference_guard"],
                           "members": members, "eclass_nodes": eclasses[group["eclass_local"]],
                           "z3_pair_checks": group["z3_pair_checks"]})
    return {"engine": semantic["egg"]["engine"],
            "stop_reason": semantic["egg"]["stop_reason"],
            "iterations": semantic["egg"]["iterations"],
            "source_sha256": semantic["source_sha256"],
            "semantics": "Unsigned typed two-state combinational predicates only; clock/reset and complete guards preserved. No four-state or sequential equivalence claim. Source counters remain separate.",
            "atoms": semantic["extraction"]["atoms"],
            "equivalent_uncovered_groups": groups,
            "unsupported_extraction": semantic["extraction"]["unsupported"]}


def messages_for(arm: str, actions: list[dict], result: dict, log: str,
                 points: list[dict], semantic: dict | None, round_no: int, limit: int) -> list[dict]:
    if arm not in ("B", "C"):
        raise ValueError("Unknown arm")
    payload = {"specification": (ROOT / "examples/heldout_sfifo/docs/specification.md").read_text(),
               "rtl": {str(SOURCE.relative_to(ROOT)): SOURCE.read_text()},
               "initial_stimulus": json.loads((ROOT / "configs/sfifo_seed.json").read_text())["actions"],
               "previous_generated_actions": actions, "round": round_no,
               "max_new_cycles": limit, "stimulus_fields_and_widths": FIELDS,
               "checker": {"checks": result["checker"]["checks"],
                           "distinct_defects": result["checker"]["distinct_defects"],
                           "first_failures": result["checker"]["failures"][:8],
                           "execution_log": [line for line in log.splitlines()
                                             if line.startswith("TRACE ")][-40:]},
               "raw_uncovered_dut_coverage": raw_feedback(points)}
    if arm == "C":
        if semantic is None:
            raise ValueError("C requires verified egg extraction")
        payload["egg_normalization"] = egg_feedback(semantic, points)
    return [{"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": json.dumps(payload, sort_keys=True)}]
