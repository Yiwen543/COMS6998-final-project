#!/usr/bin/env python3
"""Compare a saved queue pilot with independent frozen-driver replay."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


KEY = ("version", "arm", "repetition", "round")
STABLE = ("status", "new_actions", "cumulative_actions",
          "branch_covered", "branch_total", "line_covered", "line_total",
          "expr_covered", "expr_total", "toggle_covered", "toggle_total",
          "functional_failures", "data_errors", "occupancy_errors",
          "reset_errors", "clear_errors", "enable_errors",
          "cumulative_failure_events", "distinct_defect_count", "distinct_defects",
          "new_line_points_vs_initial", "new_branch_points_vs_initial",
          "new_line_points_this_round", "cumulative_api_input_tokens",
          "cumulative_api_output_tokens", "cumulative_api_tokens",
          "token_roi_new_lines_per_1000_tokens",
          "token_roi_new_branches_per_1000_tokens", "cumulative_model_calls",
          "cumulative_retries", "cumulative_failed_model_attempts",
          "cumulative_simulator_executions", "cumulative_executed_cycles")


def read_rows(path: Path) -> dict[tuple[str, ...], dict]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    result = {tuple(row[field] for field in KEY): row for row in rows}
    if len(result) != len(rows):
        raise AssertionError("Duplicate round key")
    return result


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(live: Path, replay: Path) -> dict:
    lrows, rrows = read_rows(live / "rounds.csv"), read_rows(replay / "rounds.csv")
    if lrows.keys() != rrows.keys():
        raise AssertionError("Replay round keys differ")
    for key in lrows:
        for field in STABLE:
            if lrows[key][field] != rrows[key][field]:
                raise AssertionError(f"Replay mismatch at {key}: {field}")
    ldat = {str(path.relative_to(live)): digest(path) for path in live.glob("*/*.dat")}
    rdat = {str(path.relative_to(replay)): digest(path) for path in replay.glob("*/*.dat")}
    if ldat != rdat:
        raise AssertionError("Raw DUT coverage .dat files differ")
    return {"status": "verified", "rounds_compared": len(lrows),
            "stable_fields_per_round": len(STABLE),
            "raw_coverage_files_byte_identical": len(ldat),
            "live_rounds_sha256": digest(live / "rounds.csv"),
            "replay_rounds_sha256": digest(replay / "rounds.csv"),
            "timing_fields_excluded": True,
            "coverage_sources": "DUT-only Verilator Coverage-3 .dat files"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.live.resolve(), args.replay.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
