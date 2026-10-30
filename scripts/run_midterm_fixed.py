#!/usr/bin/env python3
"""Compile fixed public-I/O drivers and check a JSON stimulus batch.

This is a verifier, not a stimulus generator. It always runs every action and
retains the raw trace/coverage even when the specification checker fails.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

from coverage import load, summary
from midterm_fixture import check, validate_actions, write_vectors


ROOT = Path(__file__).resolve().parents[1]
SETUPS = {
    "codec": ("heldout_codec64", "tb_codec_fixed"),
    "search": ("heldout_linear_search", "tb_search_fixed"),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invoke(argv, log, timeout=180):
    start = time.perf_counter()
    proc = subprocess.run([str(value) for value in argv], cwd=ROOT,
                          text=True, capture_output=True, timeout=timeout)
    elapsed = time.perf_counter() - start
    log.write_text(proc.stdout + proc.stderr)
    if proc.returncode:
        raise RuntimeError(f"Command failed ({proc.returncode}); inspect {log}")
    return elapsed, proc.stdout + proc.stderr


def compile_driver(ip, simulator, output):
    slug, top = SETUPS[ip]
    folder = ROOT / "examples" / slug
    sources = sorted((folder / "rtl").glob("*.sv"))
    driver = folder / "verif" / f"{top}.sv"
    if simulator == "verilator":
        build = output / "verilator-build"
        argv = ["verilator", "--binary", "--timing", "--coverage-line",
                "--coverage-toggle", "--coverage-expr", "-Wno-fatal",
                "-Wno-TIMESCALEMOD", "-Wno-WIDTHEXPAND", "--top-module", top,
                "--Mdir", build, "-j", "2", *sources, driver]
        binary = build / f"V{top}"
    else:
        binary = output / f"{top}.vvp"
        argv = ["iverilog", "-g2012", "-s", top, "-o", binary, *sources, driver]
    seconds, _ = invoke(argv, output / "compile.log", timeout=240)
    return binary, sources, driver, argv, seconds


def simulate(ip, simulator, binary, sources, actions, output, name="batch"):
    vector = output / f"{name}.vectors"
    write_vectors(ip, actions, vector)
    raw = output / f"{name}.dat"
    argv = ([binary] if simulator == "verilator" else ["vvp", binary]) + [f"+VECTORS={vector}"]
    if simulator == "verilator":
        argv.append(f"+verilator+coverage+file+{raw}")
    seconds, log = invoke(argv, output / f"{name}.sim.log", timeout=90)
    if f"DRIVER_OK steps={len(actions)}" not in log:
        raise ValueError("Driver failed to execute complete batch")
    checked = check(ip, actions, log)
    points = []
    if simulator == "verilator":
        for source in sources:
            points.extend(load(raw, str(source.relative_to(ROOT)), include_descendants=True))
    result = {"ip": ip, "simulator": simulator, "steps": len(actions),
              "simulation_seconds": seconds, "checker": checked,
              "coverage": summary(points) if points else None,
              "coverage_denominator": {kind: item["total"] for kind, item in summary(points).items()},
              "raw_coverage": str(raw.relative_to(ROOT)) if points else None}
    (output / f"{name}.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ip", choices=SETUPS, required=True)
    parser.add_argument("--actions", required=True, help="JSON file with an actions array")
    parser.add_argument("--simulator", choices=("verilator", "iverilog"), default="verilator")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    actions = validate_actions(args.ip, json.loads(Path(args.actions).read_text()), 10000)
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    binary, sources, driver, argv, compile_seconds = compile_driver(args.ip, args.simulator, output)
    result = simulate(args.ip, args.simulator, binary, sources, actions, output)
    result["compile_seconds"] = compile_seconds
    result["compile_command"] = [str(value) for value in argv]
    result["hashes"] = {str(path.relative_to(ROOT)): sha(path) for path in [*sources, driver, Path(__file__), ROOT / "scripts/midterm_fixture.py"]}
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"coverage": result["coverage"], "checker": result["checker"]}, indent=2))


if __name__ == "__main__":
    main()
