#!/usr/bin/env python3
"""Fixed depth-16 FIFO driver with the existing public-I/O queue checker."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from coverage import load, summary
from run_midterm_fixed import ROOT, invoke, sha
from sfifo_fixture import check, validate_actions, write_vectors

SOURCE = ROOT / "examples/heldout_sfifo_stress/rtl/sfifo.v"
ORIGINAL = ROOT / "examples/heldout_sfifo/rtl/sfifo.v"
DRIVER = ROOT / "examples/heldout_sfifo_stress/verif/tb_sfifo_stress_fixed.sv"
CAPACITY = 16
TOP = "tb_sfifo_stress_fixed"


def compile_driver(simulator: str, output: Path, source: Path = SOURCE):
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
             name: str, source: Path = SOURCE) -> dict:
    validate_actions({"actions": actions}, len(actions))
    vectors = output / f"{name}.vectors"
    write_vectors(actions, vectors)
    raw = output / f"{name}.dat"
    argv = ([binary] if simulator == "verilator" else ["vvp", binary]) + [f"+VECTORS={vectors}"]
    if simulator == "verilator":
        argv.append(f"+verilator+coverage+file+{raw}")
    seconds, log = invoke(argv, output / f"{name}.sim.log", timeout=90)
    if f"DRIVER_OK steps={len(actions)}" not in log:
        raise ValueError("Driver did not finish the full batch")
    checked = check(actions, log, capacity=CAPACITY)
    points = load(raw, str(source.relative_to(ROOT)), include_descendants=True) if simulator == "verilator" else []
    result = {"simulator": simulator, "steps": len(actions), "simulation_seconds": seconds,
              "checker": checked, "coverage": summary(points) if points else None,
              "raw_coverage": str(raw.relative_to(ROOT)) if points else None}
    (output / f"{name}.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actions", default="configs/sfifo_stress_seed.json")
    parser.add_argument("--simulator", choices=("verilator", "iverilog"), default="verilator")
    parser.add_argument("--source", choices=("variant", "original"), default="variant")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source = SOURCE if args.source == "variant" else ORIGINAL
    actions = validate_actions(json.loads((ROOT / args.actions).read_text()), 10000)
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    binary, argv, seconds = compile_driver(args.simulator, output, source)
    result = simulate(args.simulator, binary, actions, output, "batch", source)
    result.update({"compile_seconds": seconds,
                   "compile_command": [str(item) for item in argv],
                   "hashes": {str(path.relative_to(ROOT)): sha(path) for path in
                              (source, DRIVER, ROOT / "scripts/sfifo_fixture.py")}})
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"coverage": result["coverage"], "checker": result["checker"]}, indent=2))


if __name__ == "__main__":
    main()
