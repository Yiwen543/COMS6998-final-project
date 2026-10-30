#!/usr/bin/env python3
"""Fixed divider driver, public-I/O checker, and DUT-only Verilator coverage."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from coverage import load, summary
from divider_fixture import check, validate_actions, write_vectors
from run_midterm_fixed import ROOT, invoke, sha

SOURCE = ROOT / "examples/heldout_divider/rtl/radix2_div.sv"
DRIVER = ROOT / "examples/heldout_divider/verif/tb_divider_fixed.sv"
SOURCE_SHA = "64f9f4f2f8adece3b8630e8e14c1a8774c307def39ffc79655f978ef6ca77e30"
TOP = "tb_divider_fixed"


def compile_driver(simulator, output, source=SOURCE):
    if source == SOURCE and sha(source) != SOURCE_SHA:
        raise AssertionError("Pinned divider RTL changed")
    if simulator == "verilator":
        build = output / "verilator-build"
        command = ["verilator", "--binary", "--timing", "--coverage-line", "--coverage-toggle",
                   "--coverage-expr", "-Wno-fatal", "-Wno-TIMESCALEMOD", "-Wno-WIDTHEXPAND",
                   "--top-module", TOP, "--Mdir", build, "-j", "2", source, DRIVER]
        binary = build / f"V{TOP}"
    elif simulator == "iverilog":
        binary = output / f"{TOP}.vvp"
        command = ["iverilog", "-g2012", "-s", TOP, "-o", binary, source, DRIVER]
    else:
        raise ValueError("Unknown simulator")
    seconds, _ = invoke(command, output / "compile.log", timeout=240)
    return binary, command, seconds


def simulate(simulator, binary, actions, output, name="batch", source=SOURCE):
    validate_actions({"actions": actions}, len(actions))
    vectors = output / f"{name}.vectors"
    write_vectors(actions, vectors)
    raw = output / f"{name}.dat"
    command = ([binary] if simulator == "verilator" else ["vvp", binary]) + [f"+VECTORS={vectors}"]
    if simulator == "verilator":
        command.append(f"+verilator+coverage+file+{raw}")
    seconds, log = invoke(command, output / f"{name}.sim.log", timeout=90)
    if f"DRIVER_OK steps={len(actions)}" not in log:
        raise ValueError("Driver did not finish batch")
    checked = check(actions, log)
    points = load(raw, str(source.relative_to(ROOT)), include_descendants=True) if simulator == "verilator" else []
    result = {"simulator": simulator, "steps": len(actions), "simulation_seconds": seconds,
              "checker": checked, "coverage": summary(points) if points else None,
              "coverage_denominator": {kind: row["total"] for kind, row in summary(points).items()},
              "raw_coverage": str(raw.relative_to(ROOT)) if points else None}
    (output / f"{name}.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actions", default="configs/divider_seed.json")
    parser.add_argument("--simulator", choices=("verilator", "iverilog"), default="verilator")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    actions = validate_actions(json.loads((ROOT / args.actions).read_text()), 10000)
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    binary, command, compilation_seconds = compile_driver(args.simulator, output)
    result = simulate(args.simulator, binary, actions, output)
    result.update({"compile_seconds": compilation_seconds,
                   "compile_command": [str(item) for item in command],
                   "hashes": {str(path.relative_to(ROOT)): sha(path) for path in
                              (SOURCE, DRIVER, ROOT / "scripts/divider_fixture.py")}})
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"coverage": result["coverage"], "checker": result["checker"]}, indent=2))


if __name__ == "__main__":
    main()
