#!/usr/bin/env python3
"""Compile and replay fixed JSON UART cycles against the pinned external RTL."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from coverage import load, summary
from run_midterm_fixed import ROOT, invoke, sha
from txuart_fixture import check, validate_actions, write_vectors

UPSTREAM = ROOT / "third_party/wbuart32_candidate"
SOURCE = UPSTREAM / "rtl/txuart.v"
SPEC = UPSTREAM / "doc/spec.pdf"
DRIVER = ROOT / "examples/heldout_txuart/verif/tb_txuart_fixed.sv"
PROVENANCE = ROOT / "examples/heldout_txuart/provenance.json"
TOP = "tb_txuart_fixed"


def verify_source() -> dict:
    pin = json.loads(PROVENANCE.read_text())
    if sha(SOURCE) != pin["rtl_sha256"] or sha(SPEC) != pin["specification_sha256"]:
        raise AssertionError("Pinned external TX UART RTL/specification changed")
    return pin


def compile_driver(simulator: str, output: Path):
    verify_source()
    if simulator == "verilator":
        build = output / "verilator-build"
        argv = ["verilator", "--binary", "--timing", "--coverage-line", "--coverage-toggle",
                "--coverage-expr", "-Wno-fatal", "-Wno-TIMESCALEMOD", "-Wno-WIDTHEXPAND",
                "--top-module", TOP, "--Mdir", build, "-j", "2", SOURCE, DRIVER]
        binary = build / f"V{TOP}"
    elif simulator == "iverilog":
        binary = output / f"{TOP}.vvp"
        argv = ["iverilog", "-g2012", "-s", TOP, "-o", binary, SOURCE, DRIVER]
    else:
        raise ValueError("Unknown simulator")
    seconds, _ = invoke(argv, output / "compile.log", timeout=240)
    return binary, argv, seconds


def simulate(simulator: str, binary: Path, actions: list[dict], output: Path, name: str) -> dict:
    validate_actions({"actions": actions}, len(actions))
    vectors = output / f"{name}.vectors"
    write_vectors(actions, vectors)
    raw = output / f"{name}.dat"
    argv = ([binary] if simulator == "verilator" else ["vvp", binary]) + [f"+VECTORS={vectors}"]
    if simulator == "verilator":
        argv.append(f"+verilator+coverage+file+{raw}")
    seconds, log = invoke(argv, output / f"{name}.sim.log", timeout=60)
    if f"DRIVER_OK steps={len(actions)}" not in log:
        raise ValueError("UART driver did not finish full batch")
    checked = check(actions, log)
    points = load(raw, str(SOURCE.relative_to(ROOT)), include_descendants=True) if simulator == "verilator" else []
    result = {"simulator": simulator, "steps": len(actions), "simulation_seconds": seconds,
              "checker": checked, "coverage": summary(points) if points else None,
              "raw_coverage": str(raw.relative_to(ROOT)) if points else None}
    (output / f"{name}.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--actions", required=True)
    cli.add_argument("--simulator", choices=("verilator", "iverilog"), default="verilator")
    cli.add_argument("--output", required=True)
    args = cli.parse_args()
    actions = validate_actions(json.loads((ROOT / args.actions).read_text()), 10000,
                               require_initial_reset=True)
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    binary, command, seconds = compile_driver(args.simulator, output)
    result = simulate(args.simulator, binary, actions, output, "batch")
    result.update({"compile_seconds": seconds, "compile_command": [str(x) for x in command],
                   "source_sha256": sha(SOURCE), "driver_sha256": sha(DRIVER)})
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"coverage": result["coverage"], "checker": result["checker"]}, indent=2))


if __name__ == "__main__":
    main()
