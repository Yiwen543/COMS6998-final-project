#!/usr/bin/env python3
"""Freeze source/checker/target/budget before FIFO A/B/P/C model calls."""
from __future__ import annotations

import json
from pathlib import Path

from run_midterm_fixed import ROOT, sha

CONFIG = ROOT / "configs/sfifo_stress_abpc_frozen.json"
SCREEN = ROOT / "results/midterm_candidate_preflight/sfifo-stress/screen.json"
OUT = ROOT / "docs/sfifo-stress-frozen-pilot-2026-10-30.json"
FILES = (
    "examples/heldout_sfifo/rtl/sfifo.v",
    "examples/heldout_sfifo_stress/rtl/sfifo.v",
    "examples/heldout_sfifo_stress/docs/specification.md",
    "examples/heldout_sfifo_stress/verif/tb_sfifo_stress_fixed.sv",
    "configs/sfifo_stress_seed.json",
    "configs/sfifo_stress_abpc_frozen.json",
    "scripts/sfifo_fixture.py",
    "scripts/build_sfifo_stress_variant.py",
    "scripts/run_sfifo_stress_fixed.py",
    "scripts/sfifo_stress_feedback.py",
    "scripts/run_sfifo_stress_experiment.py",
    "scripts/analyze_sfifo_stress_pilot.py",
    "scripts/preflight_sfifo_token_count.py",
    "scripts/token_placebo.py",
    "scripts/pilot_model.py",
    "scripts/coverage.py",
    "scripts/run_pilot.py",
    "scripts/run_midterm_fixed.py",
    "scripts/run_midterm_b_development.py",
    "scripts/preflight_heldout.py",
    "scripts/typed_predicates.py",
    "scripts/preflight_midterm_candidates.py",
    "scripts/screen_sfifo_stress.py",
    "egraph/src/main.rs",
    "egraph/Cargo.lock",
    "results/midterm_candidate_preflight/sfifo-stress/screen.json",
    "results/sfifo_stress_token_preflight_20261030/count-evidence.json",
)


def main():
    config = json.loads(CONFIG.read_text())
    screen = json.loads(SCREEN.read_text())
    if screen["late_guard_groups"] != 2 or screen["equivalence"]["status"] != "proved":
        raise AssertionError("FIFO stress design did not pass preflight")
    late = [group for group in screen["groups"] if group["late_guard"]]
    lines = sorted(member["line"] for group in late for member in group["members"])
    if lines != sorted(config["primary_target"]["source_lines"]):
        raise AssertionError("Primary target differs from independently calibrated late guards")
    if config["rounds"] * config["max_new_cycles"] < 32:
        raise AssertionError("Target is infeasible under cycle budget")
    if config["model"] != "gpt-6.1-sol" or config["arms"] != ["A", "B", "P", "C"]:
        raise AssertionError("Unexpected model or treatment order")
    manifest = {
        "scope": "pre-model-call frozen mechanism pilot; synthetic FIFO variant, not a second natural benchmark IP",
        "primary_target": config["primary_target"],
        "budget": {name: config[name] for name in
                   ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds",
                    "max_retries", "repetitions", "rounds", "max_new_cycles", "arms")},
        "boundary": "DUT, spec, checker, driver, seed, simulator and raw DUT denominator fixed; LLM emits JSON actions only",
        "seed_raw_denominator": {kind: row["total"] for kind, row in screen["seed"].items()},
        "selection_gate": {"qualifying_groups": screen["qualifying_groups"],
                           "late_guard_groups": screen["late_guard_groups"],
                           "independent_B_development": "results/sfifo_stress_b_development_live_20261030",
                           "claude_preoutcome_review": "results/sfifo_stress_claude_preaudit_20261030/review.txt"},
        "files_sha256": {name: sha(ROOT / name) for name in FILES},
    }
    if OUT.exists():
        raise FileExistsError("Frozen manifest exists; never overwrite after model calls")
    OUT.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Frozen {len(FILES)} file hashes at {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
