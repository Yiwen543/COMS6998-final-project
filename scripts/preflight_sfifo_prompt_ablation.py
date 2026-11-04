#!/usr/bin/env python3
"""Outcome-blind five-counter target and prompt-load preflight; no API calls."""
from __future__ import annotations

import json
from pathlib import Path

from coverage import load, summary
from run_midterm_fixed import ROOT, sha
from run_sfifo_stress_fixed import SOURCE, DRIVER
from semantic_candidate_scan import map_true_counter
from sfifo_prompt_ablation_feedback import messages_for, pack_raw, unpack_raw
from sfifo_stress_feedback import raw_feedback

OUT = ROOT / "results/sfifo_prompt_ablation_preflight"
SEMANTIC = OUT / "semantic.json"
CONFIG = ROOT / "configs/sfifo_prompt_ablation_exploratory.json"
SEED_RAW = ROOT / "results/midterm_candidate_preflight/sfifo-stress/seed.dat"
CAL_RAW = ROOT / "results/midterm_candidate_preflight/sfifo-stress/calibration.dat"


def main():
    config = json.loads(CONFIG.read_text())
    semantic = json.loads(SEMANTIC.read_text())
    if sha(SOURCE) != semantic["source_sha256"]:
        raise AssertionError("Semantic source hash mismatch")
    source = str(SOURCE.relative_to(ROOT))
    seed_points = load(SEED_RAW, source, include_descendants=True)
    cal_points = load(CAL_RAW, source, include_descendants=True)
    target_sets = [{91, 161}, {96, 129, 179}]
    targets = []
    for group in semantic["groups"]:
        lines = {member["line"] for member in group["members"]}
        if lines not in target_sets:
            continue
        if not group["requires_egg_rewrite_to_merge"]:
            raise AssertionError("Target group merged before egg rewrite")
        members = []
        for member in group["members"]:
            seed = map_true_counter(member, seed_points)
            cal = map_true_counter(member, cal_points)
            if seed["status"] != "mapped" or cal["status"] != "mapped":
                raise AssertionError("Target source counter is not uniquely mapped")
            a, b = seed["point"], cal["point"]
            if ((a["type"], a["outcome"], a["hits"] > 0, b["hits"] > 0) !=
                    ("branch", "if", False, True)):
                raise AssertionError(f"Target fails original-counter reachability: {member['line']}")
            members.append({"line": member["line"], "source": a["source"],
                            "column": a["column"], "type": a["type"],
                            "outcome": a["outcome"], "seed_hits": a["hits"],
                            "calibration_hits": b["hits"],
                            "complete_guard": member["compact"]})
        targets.append({"eclass": group["eclass"], "event_context": group["event_context"],
                        "distinct_input_expressions": group["distinct_input_expressions"],
                        "z3_pair_checks": group["independent_z3_checks"],
                        "members": members})
    if ({frozenset(m["line"] for m in group["members"]) for group in targets} !=
            {frozenset(s) for s in target_sets}):
        raise AssertionError("Expected two late source-distinct groups")
    if sorted(config["primary_target"]["source_lines"]) != sorted(set().union(*target_sets)):
        raise AssertionError("Config target differs from preflight")
    raw = raw_feedback(seed_points)
    packed = pack_raw(raw)
    if unpack_raw(packed) != raw:
        raise AssertionError("Raw feedback is not lossless")
    dummy = {"checker": {"checks": 4, "distinct_defects": [], "failures": []}}
    full = messages_for("B_full", [], dummy, "", seed_points, semantic, 1, 8)
    compact = messages_for("B_compact", [], dummy, "", seed_points, semantic, 1, 8)
    c_prompt = messages_for("C_compact", [], dummy, "", seed_points, semantic, 1, 8)
    files = [SOURCE, DRIVER, ROOT / "scripts/sfifo_fixture.py",
             ROOT / "examples/heldout_sfifo_stress/docs/specification.md",
             ROOT / "configs/sfifo_stress_seed.json", CONFIG, SEMANTIC, Path(__file__),
             ROOT / "scripts/sfifo_prompt_ablation_feedback.py",
             ROOT / "scripts/run_sfifo_prompt_ablation.py", SEED_RAW, CAL_RAW]
    record = {"status": "exploratory_ablation_preflight_not_confirmatory",
              "source_sha256": sha(SOURCE), "config": config,
              "target_groups": targets, "seed_coverage": summary(seed_points),
              "calibration_coverage": summary(cal_points),
              "raw_seed_uncovered_points": len(raw),
              "raw_feedback_bytes": len(json.dumps(raw).encode()),
              "losslessly_packed_feedback_bytes": len(json.dumps(packed).encode()),
              "prompt_bytes": {"B_full": len(full[1]["content"].encode()),
                               "B_compact": len(compact[1]["content"].encode()),
                               "C_compact": len(c_prompt[1]["content"].encode())},
              "source_counter_denominator": len(seed_points),
              "unsupported_extraction": len(semantic["unsupported"]),
              "unresolved_aliases": len(semantic["unresolved_aliases"]),
              "files_sha256": {str(path.relative_to(ROOT)): sha(path) for path in files}}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "selection.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({key: record[key] for key in
                      ("status", "prompt_bytes", "source_counter_denominator",
                       "raw_seed_uncovered_points")}, indent=2))


if __name__ == "__main__":
    main()
