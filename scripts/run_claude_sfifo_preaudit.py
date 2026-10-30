#!/usr/bin/env python3
"""Read-only, pre-outcome Claude methods audit for the FIFO stress candidate."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from run_claude_divider_audit import KEY_FILE, validate_model
from run_claude_queue_audit import invoke
from run_midterm_fixed import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-budget-usd", default="2.00")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    prompt = f"""Conduct an independent PRE-OUTCOME methods review for a proposed
RTL verification feedback experiment. Do not edit files or run shell commands.
Use only Read/Glob/Grep. GPT has not run A, P, or C on this candidate. Do not
invent their outcomes or create stimulus vectors. Return a table of supported,
discrepancy, unresolved findings and a final go/no-go recommendation.

Read:
- {ROOT / 'examples/heldout_sfifo_stress/docs/specification.md'}
- {ROOT / 'examples/heldout_sfifo_stress/rtl/sfifo.v'}
- {ROOT / 'examples/heldout_sfifo/rtl/sfifo.v'}
- {ROOT / 'examples/heldout_sfifo_stress/verif/tb_sfifo_stress_fixed.sv'}
- {ROOT / 'scripts/sfifo_fixture.py'}
- {ROOT / 'scripts/build_sfifo_stress_variant.py'}
- {ROOT / 'scripts/sfifo_stress_feedback.py'}
- {ROOT / 'scripts/screen_sfifo_stress.py'}
- {ROOT / 'scripts/token_placebo.py'}
- {ROOT / 'results/midterm_candidate_preflight/sfifo-stress/screen.json'}
- {ROOT / 'results/midterm_candidate_preflight/sfifo-stress/original-vs-variant-equivalence.log'}
- {ROOT / 'results/sfifo_stress_b_development_live_20261030/rounds.jsonl'}

Check: (1) whether the FIFO checker is based on public specification behavior,
not DUT internals; (2) whether the transformation is synthetic and transparently
labeled, and what the Yosys equivalence proof actually establishes; (3) whether
two late guard groups really have distinct zero-hit source counters in the seed
and positive hits in independent calibration; (4) whether the B development
trial avoids immediate saturation; (5) whether A/B/P/C information boundaries
and token placebo plan are fair; (6) whether a proposed primary target requiring
all four late if-branch source counters plus at least 20/24 raw branch points
within five 8-cycle rounds is feasible, too easy, or too hard; (7) any leakage,
selection bias, or other reason the candidate should not enter a small pilot.
Do not treat the B trial as formal outcome, and do not call a constructed
variant a natural second benchmark IP. Distinguish what you inspected from
what you cannot establish with read-only tools.
"""
    (output / "prompt.txt").write_text(prompt)
    try:
        if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
            raise RuntimeError("Hidden Anthropic key missing or permissions too broad")
        os.environ["ANTHROPIC_API_KEY"] = KEY_FILE.read_text().strip()
        response = invoke(prompt, output / "response.json", "Read,Glob,Grep",
                          args.max_budget_usd, args.timeout_seconds)
        validate_model(response, "FIFO preaudit")
        (output / "review.txt").write_text(str(response.get("result", "")) + "\n")
        print(f"Claude pre-outcome audit saved at {output}")
    finally:
        os.environ.pop("ANTHROPIC_API_KEY", None)
        if KEY_FILE.exists():
            KEY_FILE.unlink()


if __name__ == "__main__":
    main()
