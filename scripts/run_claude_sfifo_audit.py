#!/usr/bin/env python3
"""Blind aggregate and revealed read-only Claude audit of frozen FIFO pilot."""
from __future__ import annotations

import argparse
import csv
import json
import os

from run_claude_divider_audit import KEY_FILE, validate_model
from run_claude_queue_audit import invoke
from run_midterm_fixed import ROOT, sha

LABELS = {"A": "W", "B": "X", "P": "Z", "C": "Y"}


def csv_rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def prepare(source):
    rounds = csv_rows(source / "rounds.csv")
    targets = csv_rows(source / "target-costs.csv")
    if len(rounds) != 72 or len(targets) != 12:
        raise ValueError("Expected 72 rounds and 12 target observations")
    if any(row["status"] != "ok" for row in rounds):
        raise ValueError("Non-OK round needs separate blinded presentation")
    round_keys = ("repetition", "round", "line_covered", "line_total",
                  "branch_covered", "branch_total", "expr_covered", "expr_total",
                  "toggle_covered", "toggle_total", "late_source_counters_covered",
                  "target_reached", "cumulative_api_tokens", "cumulative_model_calls",
                  "cumulative_failed_attempts", "cumulative_token_count_requests",
                  "cumulative_simulator_executions", "cumulative_executed_cycles",
                  "total_wall_seconds")
    target_keys = ("repetition", "status", "first_target_round",
                   "late_source_counters_at_observation", "branch_at_observation",
                   "api_tokens", "executed_cycles", "simulator_executions",
                   "model_calls", "failed_attempts", "wall_seconds")
    return {"scope": "one disclosed synthetic-equivalence depth-16 FIFO variant; four anonymous feedback arms",
            "blinding": "W/X/Y/Z feedback contents and mapping withheld",
            "target": "four original Verilator branch/if source counters representing two late equivalent guard events",
            "limits": "3 independent sessions per arm; 6 rounds; at most 8 new cycles per round; 4-cycle seed and accepted history replayed",
            "source_sha256": {name: sha(source / name) for name in ("rounds.csv", "target-costs.csv")},
            "rounds": [{"arm": LABELS[row["arm"]], **{key: row[key] for key in round_keys}}
                       for row in rounds],
            "target_costs": [{"arm": LABELS[row["arm"]], **{key: row[key] for key in target_keys}}
                             for row in targets],
            "interpretation_constraints": [
                "The target consists of two events observed at four separate source counters.",
                "Independent model sessions need not give independent or diverse responses.",
                "Repeated checker failures are not distinct defect categories.",
                "This blinded packet cannot prove checker validity or treatment isolation.",
                "Do not infer statistical significance or general E-graph utility from three repetitions."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="results/sfifo_stress_abpc_frozen_live_20261030")
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-budget-usd", default="5.00")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    source = (ROOT / args.source).resolve()
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    packet = prepare(source)
    packet["rounds"].sort(key=lambda row: (row["arm"], row["repetition"], int(row["round"])))
    packet["target_costs"].sort(key=lambda row: (row["arm"], row["repetition"]))
    (output / "blind-packet.json").write_text(json.dumps(packet, indent=2) + "\n")
    try:
        if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
            raise RuntimeError("Hidden Anthropic key missing or permissions too broad")
        os.environ["ANTHROPIC_API_KEY"] = KEY_FILE.read_text().strip()
        blind_prompt = (
            "As a skeptical independent methodologist, review this anonymous W/X/Y/Z "
            "RTL-verification pilot. Recompute all first-target costs from cumulative "
            "rounds, including sessions that did not reach the target. Compare raw "
            "coverage, two-event target, tokens, cycles, executions and wall time. "
            "Identify ceiling/floor effects and arithmetic discrepancies. Do not infer "
            "which arm had semantic feedback. Three repetitions are descriptive only. "
            "Distinguish data-supported findings from unknown methods questions.\n\n" +
            json.dumps(packet, separators=(",", ":")))
        (output / "blind-prompt.txt").write_text(blind_prompt)
        blind = invoke(blind_prompt, output / "blind-response.json", "",
                       args.max_budget_usd, args.timeout_seconds)
        validate_model(blind, "FIFO blind")
        (output / "blind-review.txt").write_text(str(blind.get("result", "")) + "\n")

        reveal_prompt = f"""Read-only post-outcome audit of the completed FIFO pilot.
The blind labels were W=A (text), X=B (raw coverage), Z=P (B plus neutral
provider-token-matched appendix), Y=C (B plus bounded egg/Z3 guard groups).
Read the blind review at {output / 'blind-review.txt'}. Do not edit or run commands.

Inspect at least these artifacts:
- {ROOT / 'docs/sfifo-stress-frozen-pilot-2026-10-30.json'}
- {ROOT / 'docs/sfifo_stress_preaudit_disposition_2026-10-30.md'}
- {ROOT / 'configs/sfifo_stress_abpc_frozen.json'}
- {ROOT / 'examples/heldout_sfifo_stress/docs/specification.md'}
- {ROOT / 'examples/heldout_sfifo_stress/README.md'}
- {ROOT / 'scripts/sfifo_fixture.py'}
- {ROOT / 'scripts/run_sfifo_stress_fixed.py'}
- {ROOT / 'scripts/sfifo_stress_feedback.py'}
- {ROOT / 'scripts/token_placebo.py'}
- {ROOT / 'scripts/run_sfifo_stress_experiment.py'}
- {ROOT / 'results/midterm_candidate_preflight/sfifo-stress/screen.json'}
- {ROOT / 'results/sfifo_stress_abpc_frozen_replay_20261030/validation.json'}
- {source / 'calls.jsonl'}
- {source / 'rounds.jsonl'}
- {source / 'target-costs.csv'}
- {source / 'placebo-token-counts.jsonl'}
- sampled rendered prompts under {source / 'A'}, {source / 'B'}, {source / 'P'}, {source / 'C'}

Check: frozen file/settings/target/driver/checker/coverage denominator; P uses
its own trajectory and matches hypothetical C-style same-trajectory input
tokens; actual API usage matches P's count; A/B/C feedback isolation; complete
typed guards, clock/reset scope and separate source counters; unsupported and
unmerged expressions retained; target costs and failures; no calibration
actions in prompts; no invented benchmark repair vectors; exact requested and
returned model IDs; three-repetition variability; and interpretation of C
versus B and P. The constructed FIFO variant is a mechanism test, not a second
natural benchmark IP. State exact files inspected and unresolved questions.
Your audit does not replace Verilator counters or formal proof.
"""
        (output / "reveal-prompt.txt").write_text(reveal_prompt)
        reveal = invoke(reveal_prompt, output / "reveal-response.json", "Read,Glob,Grep",
                        args.max_budget_usd, args.timeout_seconds)
        validate_model(reveal, "FIFO revealed")
        (output / "reveal-review.txt").write_text(str(reveal.get("result", "")) + "\n")
        print(f"Claude FIFO audit saved at {output}")
    finally:
        os.environ.pop("ANTHROPIC_API_KEY", None)
        if KEY_FILE.exists():
            KEY_FILE.unlink()


if __name__ == "__main__":
    main()
