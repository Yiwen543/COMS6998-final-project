#!/usr/bin/env python3
"""Freeze hashes and target after independent B development gate."""
import hashlib
import json
import subprocess

from coverage import load
from run_divider_fixed import ROOT, SOURCE
from run_midterm_fixed import sha

OUT = ROOT / "docs/divider-frozen-pilot-2026-10-30.json"
SCREEN = ROOT / "results/midterm_candidate_preflight/divider-next/screen.json"
BDEV = ROOT / "results/divider_b_development_mapping_v2_live_20261030"
CONFIG = ROOT / "configs/divider_abcp_frozen.json"
FILES = [
    "examples/heldout_divider/rtl/radix2_div.sv",
    "examples/heldout_divider/docs/specification.md",
    "examples/heldout_divider/verif/tb_divider_fixed.sv",
    "configs/divider_seed.json", "configs/divider_abcp_frozen.json",
    "scripts/divider_fixture.py", "scripts/divider_feedback.py",
    "scripts/run_divider_fixed.py", "scripts/run_divider_experiment.py",
    "scripts/typed_predicates.py", "scripts/preflight_midterm_candidates.py",
    "scripts/screen_divider_next.py", "egraph/src/main.rs",
    "tests/rtl/divider_reference.sv", "tests/test_divider_fixture.py",
    "results/midterm_candidate_preflight/divider-next/screen.json",
]


def main():
    config = json.loads(CONFIG.read_text())
    screen = json.loads(SCREEN.read_text())
    if config["arms"] != ["A", "B", "P", "C"] or config["repetitions"] != 3:
        raise AssertionError("Expected four-arm, three-repetition freeze")
    if screen["qualifying_groups"] != 5:
        raise AssertionError("Expected five source-mapped equivalent groups")
    calls = [json.loads(line) for line in (BDEV / "calls.jsonl").read_text().splitlines()]
    first = next(call for call in calls if call.get("accepted") and call["round"] == 1)
    rel = str(SOURCE.relative_to(ROOT))
    points = load(BDEV / "B/rep1" / f"round1-attempt{first['attempt']}.dat", rel,
                  include_descendants=True)
    group_progress = []
    for group in screen["groups"]:
        if not group["qualifies_preflight"]:
            continue
        hits = []
        for member in group["members"]:
            mapping = member["seed_coverage"]
            match = [p for p in points if
                     (p["line"], p["column"], p["type"], p["outcome"]) ==
                     (member["line"], mapping["column"], mapping["type"], mapping["outcome"])]
            if len(match) != 1:
                raise AssertionError("Frozen group mapping not unique")
            hits.append(match[0]["hits"])
        group_progress.append({"eclass": group["eclass_local"],
                               "lines": [m["line"] for m in group["members"]],
                               "first_round_hits": hits, "covered": all(hits)})
    if sum(row["covered"] for row in group_progress) != 4:
        raise AssertionError("B development gate changed")
    summary = json.loads((BDEV / "summary.json").read_text())
    rows = summary["rows"]
    if not (rows[0]["coverage"]["branch"]["covered"] == 20 and
            rows[2]["coverage"]["branch"]["covered"] == 24):
        raise AssertionError("B development coverage changed")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.strip()
    manifest = {"status": "frozen before A/B/placebo/C calls", "commit": commit,
                "subject": "one CVDP 8-bit radix2 divider task; not two independent IPs",
                "primary_comparison": "C versus B",
                "secondary_comparisons": ["B versus A", "P versus B"],
                "primary_target": config["primary_target"],
                "denominator_policy": "original DUT counters, unchanged on checker failure; zero-hit points retained",
                "common_seed_cycles": 4,
                "replay_policy": "each simulation replays seed and accepted history plus new actions",
                "limits": {k: config[k] for k in
                           ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds",
                            "max_retries", "repetitions", "rounds", "max_new_cycles")},
                "selection_gate": {"qualified_groups": 5,
                                   "B_first_round_fully_covered_groups": 4,
                                   "B_first_round_branch": "20/24",
                                   "B_first_full_branch_round": 3,
                                   "group_progress": group_progress,
                                   "development_run": str(BDEV.relative_to(ROOT))},
                "files_sha256": {name: sha(ROOT / name) for name in FILES},
                "development_evidence_sha256": {str(p.relative_to(ROOT)): sha(p) for p in
                                                (BDEV / "summary.json", BDEV / "calls.jsonl")}}
    OUT.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"manifest": str(OUT.relative_to(ROOT)),
                      "sha256": sha(OUT), "selected_groups": len(group_progress)}, indent=2))


if __name__ == "__main__":
    main()
