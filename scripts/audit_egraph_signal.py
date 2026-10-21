#!/usr/bin/env python3
"""Read-only diagnosis of the saved timer A/B/C semantic-feedback pilot."""
import argparse
import json
from collections import Counter
from pathlib import Path


def read_json(path):
    return json.loads(path.read_text())


def audit(folder):
    graph = read_json(folder / "egg-evidence.json")
    targets = read_json(folder / "mapped-predicates.json")
    prompts = {arm: read_json(folder / f"prompt-{arm}-1-1-1.json") for arm in "ABC"}
    bodies = {arm: json.loads(prompts[arm][1]["content"]) for arm in "ABC"}
    raw_keys = {"specification", "rtl", "initial_stimulus", "previous_generated_actions",
                "checker", "round", "max_new_cycles"}
    if not all({key: bodies[arm][key] for key in raw_keys} ==
               {key: bodies["A"][key] for key in raw_keys} for arm in "ABC"):
        raise AssertionError("Common prompt information differs")
    if "raw_uncovered_dut_coverage" in bodies["A"] or "egg_normalization" in bodies["B"]:
        raise AssertionError("Feedback arm leakage")
    if bodies["B"]["raw_uncovered_dut_coverage"] != bodies["C"]["raw_uncovered_dut_coverage"]:
        raise AssertionError("B/C raw coverage differs")
    roots = {target["id"]: target["eclass"] for target in graph["targets"]}
    if set(roots) != {target["id"] for target in targets}:
        raise AssertionError("Egg roots and source-mapped targets differ")
    first = bodies["C"]["egg_normalization"]
    rounds = [json.loads(line) for line in (folder / "rounds.jsonl").read_text().splitlines()]
    by_run = {(r["arm"], r["repetition"], r["round"]): r for r in rounds}
    metadata = read_json(folder / "metadata.json")
    reps = metadata["configuration"]["repetitions"]
    final = {arm: [by_run[(arm, rep, metadata["configuration"]["rounds"])]
                   for rep in range(1, reps + 1)] for arm in "ABC"}
    target = metadata["configuration"]["target_toggle_points"]
    first_target = {}
    for arm in "ABC":
        first_target[arm] = []
        for rep in range(1, reps + 1):
            hit = next((r for r in rounds if r["arm"] == arm and r["repetition"] == rep
                        and r["toggle_covered"] >= target), None)
            first_target[arm].append({"round": hit["round"], "tokens": hit["cumulative_api_tokens"],
                                      "cycles": hit["cumulative_executed_cycles"],
                                      "simulator_executions": hit["cumulative_simulator_executions"]}
                                     if hit else {"status": "not reached"})
    remaining = Counter((p["type"], p["line"], p["outcome"].split(":")[0])
                        for p in final["B"][0]["coverage_points"] if p["hits"] == 0)
    mapped_hits = {}
    for arm in "ABC":
        mapped_hits[arm] = []
        for rep in range(1, reps + 1):
            points = by_run[(arm, rep, 1)]["coverage_points"]
            hit_count = 0
            for target_row in targets:
                match = [p for p in points if p["line"] == target_row["line"]
                         and p["type"] == target_row["counter_type"]
                         and p["outcome"] == target_row["counter_outcome"]]
                if len(match) != 1:
                    raise AssertionError(f"Ambiguous source map for {target_row['id']}")
                hit_count += int(match[0]["hits"] > 0)
            mapped_hits[arm].append(hit_count)
    upper = {f"axi_rdata[{bit}]" for bit in range(16, 32)}
    remaining_upper = sum(count for (kind, _, signal), count in remaining.items()
                          if kind == "toggle" and signal in upper)
    return {
        "mode": metadata["mode"],
        "model": metadata["configuration"]["model"],
        "seed_coverage": metadata["common_initial_coverage"],
        "first_prompt_bytes": {arm: (folder / f"prompt-{arm}-1-1-1.json").stat().st_size for arm in "ABC"},
        "isolation_checked": True,
        "egg_iterations": graph["iterations"], "egg_stop_reason": graph["stop_reason"],
        "mapped_predicates": len(targets), "unique_root_eclasses": len(set(roots.values())),
        "merged_coverage_target_roots": len(targets) - len(set(roots.values())),
        "mapped_uncovered_at_seed": len(first["mapped_uncovered"]),
        "mapped_predicates_hit_after_first_round": mapped_hits,
        "unmapped_uncovered_at_seed": first["unmapped_uncovered"],
        "first_round_toggle": {arm: [by_run[(arm, rep, 1)]["toggle_covered"]
                                     for rep in range(1, reps + 1)] for arm in "ABC"},
        "final_toggle": {arm: [r["toggle_covered"] for r in final[arm]] for arm in "ABC"},
        "first_target": first_target,
        "remaining_uncovered_final_B1": len([p for p in final["B"][0]["coverage_points"] if p["hits"] == 0]),
        "remaining_upper_rdata_toggle_directions": remaining_upper,
        "total_model_calls": sum(1 for _ in (folder / "calls.jsonl").open()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.results)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
