#!/usr/bin/env python3
"""Outcome-blind equivalence, typed guard, source and reachability preflight."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from coverage import load
from preflight_heldout import verify_rewrites
from preflight_midterm_candidates import semantic_groups, source_point
from run_midterm_fixed import ROOT, sha
from run_sfifo_stress_fixed import DRIVER, ORIGINAL, SOURCE, compile_driver, simulate

OUT = ROOT / "results/midterm_candidate_preflight/sfifo-stress"
SEED = ROOT / "configs/sfifo_stress_seed.json"


def action(**kwargs):
    return {"reset": 0, "wr": 0, "rd": 0, "data": 0} | kwargs


def prove_variant() -> dict:
    settings = "-set BW 8 -set LGFLEN 4 -set OPT_ASYNC_READ 1 -set OPT_WRITE_ON_FULL 0 -set OPT_READ_ON_EMPTY 0 sfifo"
    program = (f"read_verilog -sv -D YOSYS {ORIGINAL}; chparam {settings}; rename sfifo gold; "
               f"read_verilog -sv -D YOSYS {SOURCE}; chparam {settings}; rename sfifo gate; "
               "proc; memory; equiv_make gold gate equiv; hierarchy -top equiv; "
               "equiv_simple; equiv_induct -seq 24; equiv_status -assert")
    command = ["yosys", "-Q", "-T", "-p", program]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
    log = result.stdout + result.stderr
    path = OUT / "original-vs-variant-equivalence.log"
    path.write_text(log)
    if result.returncode or "Equivalence successfully proven!" not in log:
        raise AssertionError("FIFO original/variant formal equivalence failed")
    return {"status": "proved", "command": command,
            "log_sha256": sha(path),
            "scope": "Yosys equiv_make and equiv_simple proved all 157 paired cells at fixed 8-bit depth-16 parameters; equiv_induct had zero unproven cells. Two-state state correspondence, not a complete specification or four-state proof."}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if SOURCE.read_text() != __import__("build_sfifo_stress_variant").build():
        raise AssertionError("FIFO variant differs from recorded transformation recipe")
    equivalence = prove_variant()
    rewrite = verify_rewrites()
    (OUT / "rewrite-proof.json").write_text(json.dumps(rewrite, indent=2) + "\n")
    seed = json.loads(SEED.read_text())["actions"]
    binary, command, compile_seconds = compile_driver("verilator", OUT, SOURCE)
    seed_result = simulate("verilator", binary, seed, OUT, "seed", SOURCE)
    if seed_result["checker"]["failures"]:
        raise AssertionError("Common seed fails checker")
    # Reachability-only ceiling, excluded from all LLM prompts.
    calibration = seed + [action(wr=1, data=17 + i) for i in range(16)] + [
        action(rd=1) for _ in range(16)]
    calibration_result = simulate("verilator", binary, calibration, OUT, "calibration", SOURCE)
    if calibration_result["checker"]["failures"]:
        raise AssertionError("Independent checker failed calibration")
    extraction, semantic = semantic_groups(SOURCE, OUT / "semantic.json")
    targets = {target["id"]: target for target in extraction["targets"]}
    source = str(SOURCE.relative_to(ROOT))
    seed_points = load(OUT / "seed.dat", source, include_descendants=True)
    calibration_points = load(OUT / "calibration.dat", source, include_descendants=True)
    groups = semantic["groups"]
    for group in groups:
        for member, target_id in zip(group["members"], group["member_ids"]):
            target = targets[target_id]
            member["seed_coverage"] = source_point(target, seed_points)
            member["calibration_coverage"] = source_point(target, calibration_points)
        group["qualifies_preflight"] = all(
            member["seed_coverage"].get("status") == "mapped" and
            member["seed_coverage"]["hits"] == 0 and
            member["calibration_coverage"].get("status") == "mapped" and
            member["calibration_coverage"]["hits"] > 0
            for member in group["members"])
        group["late_guard"] = group["qualifies_preflight"] and all(
            targets[target_id]["guard_depth"] >= 3 for target_id in group["member_ids"])
    result = {"subject": "disclosed equivalence stress variant of independent ZipCPU FIFO",
              "original_sha256": sha(ORIGINAL), "variant_sha256": sha(SOURCE),
              "recipe_sha256": sha(ROOT / "scripts/build_sfifo_stress_variant.py"),
              "driver_sha256": sha(DRIVER), "checker_sha256": sha(ROOT / "scripts/sfifo_fixture.py"),
              "spec_sha256": sha(ROOT / "examples/heldout_sfifo_stress/docs/specification.md"),
              "seed_sha256": sha(SEED), "equivalence": equivalence,
              "rewrite_proof_sha256": sha(OUT / "rewrite-proof.json"),
              "seed": seed_result["coverage"], "calibration": calibration_result["coverage"],
              "calibration_action_count": len(calibration),
              "calibration_actions_withheld": True,
              "supported_targets": len(extraction["targets"]),
              "unsupported": extraction["unsupported"], "groups": groups,
              "qualifying_groups": sum(g["qualifies_preflight"] for g in groups),
              "late_guard_groups": sum(g["late_guard"] for g in groups),
              "compile_seconds": compile_seconds, "compile_command": [str(x) for x in command]}
    (OUT / "screen.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"equivalence": equivalence["status"],
                      "qualifying_groups": result["qualifying_groups"],
                      "late_guard_groups": result["late_guard_groups"],
                      "seed": result["seed"], "calibration": result["calibration"]}, indent=2))


if __name__ == "__main__":
    main()
