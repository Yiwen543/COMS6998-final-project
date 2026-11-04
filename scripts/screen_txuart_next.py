#!/usr/bin/env python3
"""Outcome-blind TX UART semantic, checker, raw-counter and reachability gate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from coverage import load
from run_midterm_fixed import ROOT, sha
from run_txuart_fixed import DRIVER, SOURCE, SPEC, compile_driver, simulate, verify_source
from semantic_candidate_scan import map_true_counter, scan

OUT = ROOT / "results/next_natural_ip_screen/txuart"
SEED = ROOT / "configs/txuart_seed.json"


def action(reset=0, brk=0, wr=0, data=0):
    return {"reset": reset, "break": brk, "wr": wr, "data": data}


def calibration_actions(seed):
    # Isolated reachability witness. Never put this list in a model prompt.
    return (seed + [action() for _ in range(38)] + [action(wr=1, data=0xa5)] +
            [action() for _ in range(26)] + [action(brk=1) for _ in range(4)] +
            [action() for _ in range(40)] + [action(wr=1, data=0x5a)] +
            [action() for _ in range(26)])


def main():
    pin = verify_source()
    OUT.mkdir(parents=True, exist_ok=True)
    semantic = scan(SOURCE, "txuart", flatten=False)
    (OUT / "semantic.json").write_text(json.dumps(semantic, indent=2) + "\n")
    binary, command, compile_seconds = compile_driver("verilator", OUT)
    seed = json.loads(SEED.read_text())["actions"]
    calibration = calibration_actions(seed)
    seed_result = simulate("verilator", binary, seed, OUT, "seed")
    calibration_result = simulate("verilator", binary, calibration, OUT, "calibration")
    if seed_result["checker"]["failures"] or calibration_result["checker"]["failures"]:
        raise AssertionError("TX UART specification checker rejected preflight")
    source_name = str(SOURCE.relative_to(ROOT))
    seed_points = load(OUT / "seed.dat", source_name, include_descendants=True)
    calibration_points = load(OUT / "calibration.dat", source_name, include_descendants=True)
    groups = []
    for group in semantic["groups"]:
        members = []
        for member in group["members"]:
            if member["case_value"] == "default":
                continue
            members.append({"id": member["id"], "line": member["line"],
                            "source_text": member["source_text"],
                            "guard": member["compact"],
                            "seed_coverage": map_true_counter(member, seed_points),
                            "calibration_coverage": map_true_counter(member, calibration_points)})
        if len(members) < 2:
            continue
        qualified = all(m["seed_coverage"]["status"] == "mapped" and
                        m["seed_coverage"]["point"]["hits"] == 0 and
                        m["calibration_coverage"]["status"] == "mapped" and
                        m["calibration_coverage"]["point"]["hits"] > 0
                        for m in members)
        groups.append({"eclass": group["eclass"], "event_context": group["event_context"],
                       "independent_z3_checks": group["independent_z3_checks"],
                       "members": members, "qualifies": qualified})
    result = {"status": "candidate_preflight_not_frozen", "upstream": pin,
              "contract_sha256": sha(ROOT / "examples/heldout_txuart/docs/contract.md"),
              "driver_sha256": sha(DRIVER), "seed_sha256": sha(SEED),
              "semantic_sha256": sha(OUT / "semantic.json"),
              "calibration_actions_sha256": hashlib.sha256(json.dumps(calibration).encode()).hexdigest(),
              "calibration_actions_withheld_from_prompts": True,
              "compile_command": [str(x) for x in command], "compile_seconds": compile_seconds,
              "seed": seed_result, "calibration": calibration_result,
              "groups": groups, "qualifying_groups": sum(g["qualifies"] for g in groups),
              "unsupported": semantic["unsupported"],
              "unresolved_aliases": semantic["unresolved_aliases"],
              "semantic_timing_seconds": semantic["seconds"]}
    (OUT / "screen.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"qualifying_groups": result["qualifying_groups"],
                      "seed": seed_result["coverage"],
                      "calibration": calibration_result["coverage"],
                      "checker": calibration_result["checker"]}, indent=2))


if __name__ == "__main__":
    main()
