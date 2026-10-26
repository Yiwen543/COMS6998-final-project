"""Prepare a label-blind, read-only audit packet from the saved queue B/C pilot.

This script never invokes a model and never changes experiment data. The emitted
packet deliberately omits the B/C mapping so an independent reviewer can first
assess the observed effect without knowing which arm received egg feedback.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULT = ROOT / "results/queue_bc_live_20261021_unsandboxed"
ARM_LABEL = {"B": "X", "C": "Y"}
ROUND_INT = (
    "repetition", "round", "branch_covered", "branch_total", "line_covered",
    "line_total", "expr_covered", "expr_total", "toggle_covered",
    "toggle_total", "cumulative_api_tokens", "cumulative_model_calls",
    "cumulative_retries", "cumulative_failed_model_attempts",
    "cumulative_simulator_executions", "cumulative_executed_cycles",
    "distinct_defect_count",
)
TARGET_INT = (
    "repetition", "target_line_points", "first_target_round",
    "line_covered_at_stop", "api_tokens", "executed_cycles",
    "simulator_executions",
)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scrub(row: dict[str, str], keys: tuple[str, ...]) -> dict[str, object]:
    if row["arm"] not in ARM_LABEL:
        raise ValueError(f"Unexpected arm: {row['arm']}")
    result: dict[str, object] = {
        "version": row["version"], "arm": ARM_LABEL[row["arm"]]
    }
    for key in keys:
        value = row[key]
        result[key] = None if value == "" else int(value)
    return result


def prepare(source: Path) -> dict[str, object]:
    round_file = source / "rounds.csv"
    target_file = source / "target_costs.csv"
    round_rows = rows(round_file)
    target_rows = rows(target_file)
    if len(target_rows) != 12 or len(round_rows) > 48:
        raise ValueError("Expected at most 48 rounds and exactly 12 target rows")
    for row in round_rows:
        if row["status"] != "ok":
            raise ValueError("A non-OK round requires separate review")
    rounds = [scrub(row, ROUND_INT) for row in round_rows]
    targets = [scrub(row, TARGET_INT) for row in target_rows]
    for source_row, target in zip(target_rows, targets):
        if source_row["status"] not in ("reached", "not reached"):
            raise ValueError("Unexpected target status")
        target["status"] = source_row["status"]
    rounds.sort(key=lambda row: (row["version"], row["arm"], row["repetition"], row["round"]))
    targets.sort(key=lambda row: (row["version"], row["arm"], row["repetition"]))
    for target in targets:
        matching = [
            row for row in rounds
            if row["version"] == target["version"]
            and row["arm"] == target["arm"]
            and row["repetition"] == target["repetition"]
            and (row["round"] == target["first_target_round"] if target["status"] == "reached"
                 else True)
        ]
        if target["status"] == "not reached":
            matching.sort(key=lambda row: row["round"])
            matching = matching[-1:]
        if len(matching) != 1:
            raise ValueError("Target row has no unique matching round")
        observed = matching[0]
        for target_key, round_key in (
            ("line_covered_at_stop", "line_covered"),
            ("api_tokens", "cumulative_api_tokens"),
            ("executed_cycles", "cumulative_executed_cycles"),
            ("simulator_executions", "cumulative_simulator_executions"),
        ):
            if target[target_key] != observed[round_key]:
                raise ValueError(f"Target/round mismatch: {target_key}")
    return {
        "scope": "One CVDP queue IP, original and equivalent RTL variant; compare X/Y only within each fixed version.",
        "blinding": "X/Y mapping withheld for first-pass effect review; labels do not identify feedback content.",
        "primary_target": "41/41 actual DUT Verilator line counters",
        "limits": "Three independent repetitions per arm/version; four refinement rounds; up to four new actions per round; six-cycle common seed replayed each execution.",
        "source_sha256": {
            "rounds.csv": digest(round_file),
            "target_costs.csv": digest(target_file),
        },
        "rounds": rounds,
        "target_costs": targets,
        "interpretation_constraints": [
            "These are independent model sessions, not deterministic matched responses.",
            "Raw DUT coverage counters must remain location-specific.",
            "The two RTL versions are one IP, not two independent designs.",
            "This aggregate packet cannot prove checker correctness, feedback isolation, or rewrite soundness; those require the raw artifacts and replay.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    packet = prepare(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote blind audit packet: {args.output}")


if __name__ == "__main__":
    main()
