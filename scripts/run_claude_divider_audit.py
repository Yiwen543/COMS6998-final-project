#!/usr/bin/env python3
"""Two-stage blind then read-only Claude Code audit of frozen divider pilot."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

from run_claude_queue_audit import invoke
from run_midterm_fixed import ROOT, sha

KEY_FILE = ROOT / "build/private/anthropic-crosscheck-key"
LABELS = {"A": "W", "B": "X", "P": "Z", "C": "Y"}


def csv_rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def prepare(source):
    rounds = csv_rows(source / "rounds.csv")
    targets = csv_rows(source / "target-costs.csv")
    if len(rounds) != 48 or len(targets) != 12:
        raise ValueError("Expected all 48 completed rounds and 12 targets")
    if any(row["status"] != "ok" for row in rounds):
        raise ValueError("Non-OK round needs separate blinded presentation")
    safe_round_keys = ("repetition", "round", "line_covered", "line_total",
                       "branch_covered", "branch_total", "expr_covered", "expr_total",
                       "toggle_covered", "toggle_total", "fully_covered_groups",
                       "cumulative_api_tokens", "cumulative_model_calls",
                       "cumulative_failed_attempts", "cumulative_simulator_executions",
                       "cumulative_executed_cycles", "total_wall_seconds")
    safe_target_keys = ("repetition", "status", "target_branch_points", "first_target_round",
                        "branch_covered_at_stop", "api_tokens", "executed_cycles",
                        "simulator_executions", "wall_seconds")
    packet_rounds = [{"arm": LABELS[row["arm"]],
                      **{key: row[key] for key in safe_round_keys}} for row in rounds]
    packet_targets = [{"arm": LABELS[row["arm"]],
                       **{key: row[key] for key in safe_target_keys}} for row in targets]
    packet_rounds.sort(key=lambda row: (row["arm"], row["repetition"], int(row["round"])))
    packet_targets.sort(key=lambda row: (row["arm"], row["repetition"]))
    return {"scope": "one fixed 8-bit CVDP divider; four anonymous feedback arms",
            "blinding": "W/X/Y/Z feedback contents and mapping withheld",
            "target": "24/24 original DUT Verilator branch points",
            "limits": "3 independent repetitions per arm; 4 rounds, at most 8 new cycles per round; 4-cycle seed replayed on each execution",
            "source_sha256": {name: sha(source / name) for name in
                              ("rounds.csv", "target-costs.csv")},
            "rounds": packet_rounds, "target_costs": packet_targets,
            "interpretation_constraints": [
                "These are independent model sessions, not deterministic paired responses.",
                "Repeated checker failures are not distinct defect categories.",
                "This blinded packet cannot prove checker validity or feedback isolation.",
                "Do not infer a causal advantage or statistical significance from three repetitions.",
                "The four labels do not identify feedback contents."]}


def validate_model(payload, stage):
    models = set((payload.get("modelUsage") or {}).keys())
    if models != {"claude-opus-5-5"}:
        raise RuntimeError(f"{stage}: returned model usage not exclusively claude-opus-5-5: {sorted(models)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="results/divider_abcp_frozen_live_20261030")
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-budget-usd", default="3.00")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    source = (ROOT / args.source).resolve()
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    packet = prepare(source)
    (output / "blind-packet.json").write_text(json.dumps(packet, indent=2) + "\n")
    try:
        if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
            raise RuntimeError("Hidden Anthropic key missing or permissions too broad")
        os.environ["ANTHROPIC_API_KEY"] = KEY_FILE.read_text().strip()
        blind_prompt = (
            "Review this anonymous W/X/Y/Z matched RTL-verification pilot as a skeptical "
            "methodologist. Recompute target costs from cumulative rounds. Compare each "
            "anonymous arm on raw coverage, tokens, cycles, executions, wall time, and "
            "variability. Identify ceiling effects and arithmetic discrepancies. Do not "
            "infer which arm received semantic feedback. Do not claim significance from "
            "three repetitions. The packet cannot establish checker validity or prompt "
            "isolation. Return concise, concrete findings.\n\n" +
            json.dumps(packet, separators=(",", ":")))
        (output / "blind-prompt.txt").write_text(blind_prompt)
        blind = invoke(blind_prompt, output / "blind-response.json", "",
                       args.max_budget_usd, args.timeout_seconds)
        validate_model(blind, "blind")
        (output / "blind-review.txt").write_text(str(blind.get("result", "")) + "\n")

        reveal_prompt = f"""Independently audit this completed RTL-verification pilot.
The blind labels were W=A (text only), X=B (raw coverage), Z=P (B plus neutral
length-matched appendix), Y=C (B plus bounded egg and Z3-checked guard groups).
Stage 1 is saved at {output / 'blind-review.txt'}. Do not edit any file.

Inspect read-only artifacts at {source}, and these frozen sources:
- {ROOT / 'docs/divider-frozen-pilot-2026-10-30.json'}
- {ROOT / 'configs/divider_abcp_frozen.json'}
- {ROOT / 'examples/heldout_divider/docs/specification.md'}
- {ROOT / 'scripts/divider_fixture.py'}
- {ROOT / 'scripts/divider_feedback.py'}
- {ROOT / 'scripts/run_divider_experiment.py'}
- {ROOT / 'results/midterm_candidate_preflight/divider-next/screen.json'}
- {ROOT / 'tests/test_divider_fixture.py'}

Check, citing exact files/rows where possible: (1) frozen DUT/spec/checker/
driver/seed/settings/denominator across arms; (2) common prompt fields,
A absence of coverage, B/P/C identical raw coverage selection, P's lack of
semantic relations and byte-length match to C extra feedback; (3) typed full
guards, clock/reset context, Z3 pair checks, unsupported mapping and separate
source counters; (4) every API call/retry, cumulative replay cycles and
simulator executions, target costs, and coverage on checker failures;
(5) arithmetic checker independent control and original DUT remainder defect;
(6) observed C versus B result and threats to validity. Look for any leakage
of calibration vectors, known benchmark failing vectors, or repair text into
experimental prompts. Do not execute commands or edit files. Your review
cannot replace the simulator's raw counters; distinguish inspected evidence
from unresolved questions. Return a concise structured audit with supported,
discrepancy, or unresolved labels for each material finding.
"""
        (output / "reveal-prompt.txt").write_text(reveal_prompt)
        reveal = invoke(reveal_prompt, output / "reveal-response.json", "Read,Glob,Grep",
                        args.max_budget_usd, args.timeout_seconds)
        validate_model(reveal, "reveal")
        (output / "reveal-review.txt").write_text(str(reveal.get("result", "")) + "\n")
        print(f"Claude audit saved at {output}")
    finally:
        os.environ.pop("ANTHROPIC_API_KEY", None)
        if KEY_FILE.exists():
            KEY_FILE.unlink()


if __name__ == "__main__":
    main()
