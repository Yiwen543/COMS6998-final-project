#!/usr/bin/env python3
"""Fixed public-I/O sfifo driver, independent checker, and DUT-only coverage."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from coverage import load, summary
from run_midterm_fixed import ROOT, invoke, sha
from sfifo_fixture import check, validate_actions, write_vectors

SLUG = "heldout_sfifo"
TOP = "tb_sfifo_fixed"
SOURCE = ROOT / "examples" / SLUG / "rtl/sfifo.v"
DRIVER = ROOT / "examples" / SLUG / "verif/tb_sfifo_fixed.sv"
EXPECTED_SOURCE_SHA = "76a653781f1ecca1c1da92c4e5105ecd5d0f832b13cbfd31300ec88d9947e0c1"


def compile_driver(simulator: str, output: Path, source: Path = SOURCE):
    if source == SOURCE and sha(source) != EXPECTED_SOURCE_SHA:
        raise AssertionError("Pinned original sfifo source changed")
    if simulator == "verilator":
        build = output / "verilator-build"
        argv = ["verilator", "--binary", "--timing", "--coverage-line", "--coverage-toggle",
                "--coverage-expr", "-Wno-fatal", "-Wno-TIMESCALEMOD", "-Wno-WIDTHEXPAND",
                "--top-module", TOP, "--Mdir", build, "-j", "2", source, DRIVER]
        binary = build / f"V{TOP}"
    elif simulator == "iverilog":
        binary = output / f"{TOP}.vvp"
        argv = ["iverilog", "-g2012", "-s", TOP, "-o", binary, source, DRIVER]
    else:
        raise ValueError("Unknown simulator")
    seconds, _ = invoke(argv, output / "compile.log", timeout=240)
    return binary, argv, seconds


def simulate(simulator: str, binary: Path, actions: list[dict], output: Path,
             name: str = "batch", source: Path = SOURCE) -> dict:
    validate_actions({"actions": actions}, len(actions))
    vector = output / f"{name}.vectors"
    write_vectors(actions, vector)
    raw = output / f"{name}.dat"
    argv = ([binary] if simulator == "verilator" else ["vvp", binary]) + [f"+VECTORS={vector}"]
    if simulator == "verilator":
        argv.append(f"+verilator+coverage+file+{raw}")
    elapsed, log = invoke(argv, output / f"{name}.sim.log", timeout=90)
    if f"DRIVER_OK steps={len(actions)}" not in log:
        raise ValueError("Driver did not finish complete stimulus batch")
    checked = check(actions, log)
    points = load(raw, str(source.relative_to(ROOT)), include_descendants=True) if simulator == "verilator" else []
    result = {"simulator": simulator, "steps": len(actions), "simulation_seconds": elapsed,
              "checker": checked, "coverage": summary(points) if points else None,
              "coverage_denominator": {kind: row["total"] for kind, row in summary(points).items()},
              "raw_coverage": str(raw.relative_to(ROOT)) if points else None}
    (output / f"{name}.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actions", default="configs/sfifo_seed.json")
    parser.add_argument("--simulator", choices=("verilator", "iverilog"), default="verilator")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    actions = validate_actions(json.loads((ROOT / args.actions).read_text()), 10000)
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    binary, argv, compile_seconds = compile_driver(args.simulator, output)
    result = simulate(args.simulator, binary, actions, output)
    result.update({"compile_seconds": compile_seconds,
                   "compile_command": [str(item) for item in argv],
                   "hashes": {str(path.relative_to(ROOT)): sha(path) for path in
                              (SOURCE, DRIVER, ROOT / "scripts/sfifo_fixture.py")}})
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"coverage": result["coverage"], "checker": result["checker"]}, indent=2))


if __name__ == "__main__":
    main()
