#!/usr/bin/env python3
"""Outcome-blind typed-guard and reachability gate for a pinned CVDP divider."""
import hashlib
import json
from pathlib import Path

from coverage import load
from preflight_midterm_candidates import semantic_groups, source_point
from run_divider_fixed import ROOT, SOURCE, SOURCE_SHA, compile_driver, simulate
from run_midterm_fixed import sha

DATASET = ROOT / ".cache/cvdp_v1.1.0_nonagentic_code_generation_no_commercial.jsonl"
TASK = "cvdp_copilot_radix2_div_0001"
OUT = ROOT / "results/midterm_candidate_preflight/divider-next"


def action(**kwargs):
    return {"rst_n": 1, "start": 0, "dividend": 37, "divisor": 6} | kwargs


def mapped_true_case(target, points):
    mapping = source_point(target, points)
    if mapping["status"] == "mapped" or target["case_value"] != "1'1":
        return mapping
    source = str(SOURCE.relative_to(ROOT))
    # Verilator can put both if and else counters on one source line. An
    # explicit RTLIL 1'b1 case maps to the if path, not the else path.
    matches = [p for p in points if p["source"] == source and
               p["line"] == target["line"] and p["outcome"] == "if" and
               p["type"] in ("line", "branch")]
    if len(matches) != 1:
        return mapping
    point = matches[0]
    return {"status": "mapped", "type": point["type"], "outcome": point["outcome"],
            "line": point["line"], "column": point["column"],
            "hierarchy": point["hierarchy"], "hits": point["hits"],
            "mapping_rule": "explicit_true_case_to_unique_if_counter"}


def main():
    record = next(json.loads(line) for line in DATASET.read_text().splitlines()
                  if json.loads(line)["id"] == TASK)
    original = record["input"]["context"]["rtl/radix2_div.sv"].encode()
    if hashlib.sha256(original).hexdigest() != SOURCE_SHA or sha(SOURCE) != SOURCE_SHA:
        raise AssertionError("Original context RTL provenance mismatch")
    OUT.mkdir(parents=True, exist_ok=True)
    seed = json.loads((ROOT / "configs/divider_seed.json").read_text())["actions"]
    binary, command, seconds = compile_driver("verilator", OUT)
    seed_result = simulate("verilator", binary, seed, OUT, "seed")
    if seed_result["checker"]["failures"]:
        raise AssertionError("Common seed failed checker")
    # Reachability-only sequence, selected from arithmetic classes without
    # reading benchmark failing-vector or repair fields. Never shown to LLM.
    reach = seed + [action(start=1)] + [action() for _ in range(8)] + [
        action(start=1, dividend=0, divisor=0), action(dividend=0, divisor=0),
        action(start=1, dividend=91, divisor=13), action(rst_n=0, start=0)]
    calibration = simulate("verilator", binary, reach, OUT, "calibration")
    extraction, semantic = semantic_groups(SOURCE, OUT / "semantic.json")
    targets = {target["id"]: target for target in extraction["targets"]}
    rel = str(SOURCE.relative_to(ROOT))
    seed_points = load(OUT / "seed.dat", rel, include_descendants=True)
    calib_points = load(OUT / "calibration.dat", rel, include_descendants=True)
    groups = semantic["groups"]
    for group in groups:
        for member, target_id in zip(group["members"], group["member_ids"]):
            target = targets[target_id]
            member["seed_coverage"] = mapped_true_case(target, seed_points)
            member["calibration_coverage"] = mapped_true_case(target, calib_points)
        group["qualifies_preflight"] = all(
            member["seed_coverage"].get("status") == "mapped" and
            member["seed_coverage"]["hits"] == 0 and
            member["calibration_coverage"].get("status") == "mapped" and
            member["calibration_coverage"]["hits"] > 0
            for member in group["members"])
    result = {"task": TASK, "dataset_sha256": sha(DATASET),
              "record_sha256": hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest(),
              "source_sha256": SOURCE_SHA, "spec_sha256": sha(ROOT / "examples/heldout_divider/docs/specification.md"),
              "driver_sha256": sha(ROOT / "examples/heldout_divider/verif/tb_divider_fixed.sv"),
              "scope": "preflight only; no model outcome, no benchmark repair/failing vectors in prompts",
              "seed": seed_result["coverage"], "calibration": calibration["coverage"],
              "calibration_checker_distinct_defects": calibration["checker"]["distinct_defects"],
              "supported_targets": len(extraction["targets"]),
              "unsupported": extraction["unsupported"], "groups": groups,
              "qualifying_groups": sum(group["qualifies_preflight"] for group in groups),
              "compile_seconds": seconds, "compile_command": [str(part) for part in command]}
    (OUT / "screen.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"qualifying_groups": result["qualifying_groups"],
                      "seed": result["seed"], "calibration": result["calibration"],
                      "calibration_defects": result["calibration_checker_distinct_defects"]}, indent=2))


if __name__ == "__main__":
    main()
