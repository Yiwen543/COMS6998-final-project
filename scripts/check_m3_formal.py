#!/usr/bin/env python3
"""Bounded and inductive reset-hold checks, with concrete Icarus replay."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "examples/arbiter"
STEPS = 8


def run(command, work, rc=0):
    proc = subprocess.run(command, cwd=work, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=120)
    if proc.returncode != rc:
        raise RuntimeError(f"{command} exited {proc.returncode}\n{proc.stdout}")
    return proc.stdout


def smtbmc(work, model, options, failure=False):
    log = run(["yosys-smtbmc", "-s", "z3", "-t", str(STEPS), "--noprogress",
               *options, model], work, rc=int(failure))
    status = "FAILED" if failure else "PASSED"
    if not log.rstrip().endswith(f"Status: {status}"):
        raise RuntimeError(f"Unrecognized solver result\n{log}")
    return log


def input_rows(witness):
    """Yosys packs the first listed signal in the least significant bits."""
    signals = witness["signals"]
    widths = {"reset": 1, "req": 8, "priority_override": 8}
    names = [s["path"][0].removeprefix("\\") for s in signals]
    if len(names) != len(widths) or set(names) != widths.keys():
        raise ValueError(f"Unexpected input ports in witness: {names}")
    for name, s in zip(names, signals):
        if len(s["path"]) != 1 or s["offset"] or s["init_only"] or s["width"] != widths[name]:
            raise ValueError(f"Unexpected witness declaration for {name}")
    rows = []
    for entry in witness["steps"]:
        bits = entry["bits"]
        if len(bits) != sum(widths.values()) or any(b not in "01" for b in bits):
            raise ValueError(f"Incomplete binary input row: {bits}")
        row = {}
        for name in names:
            width = widths[name]
            row[name] = int(bits[-width:], 2)
            bits = bits[:-width]
        rows.append(row)
    return rows


def replay(work, model, rows):
    run(["iverilog", "-g2012", "-s", "replay_reset_hold", "-o", "replay.vvp",
         model + ".sv", "replay_reset_hold.sv"], work)
    log = run(["vvp", "replay.vvp", "+VECTORS=witness.txt"], work)
    if f"REPLAY_STEPS={len(rows)}\n" not in log:
        raise RuntimeError(f"Incomplete replay\n{log}")
    return [dict(step=int(step), before_hex=before, after_hex=after)
            for step, before, after in re.findall(
                r"^ACTIVATION step=(\d+) before=([0-9a-f]{3}) after=([0-9a-f]{3})$", log, re.M)]


def check(work):
    source = (CASE / "rtl/fixed_priority_arbiter.sv").read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    if digest != json.loads((CASE / "provenance.json").read_text())["rtl_sha256"]:
        raise ValueError("Arbiter RTL hash differs from provenance")
    original = b"@(posedge clk or posedge reset)"
    if source.count(original) != 1:
        raise ValueError("Could not identify the reset-only control edit")
    (work / "original.sv").write_bytes(source)
    (work / "sync_control.sv").write_bytes(source.replace(original, b"@(posedge clk)"))
    for name in ("reset_hold.sv", "replay_reset_hold.sv"):
        shutil.copyfile(CASE / "formal" / name, work / name)

    results = {}
    for model in ("original", "sync_control"):
        run(["yosys", "-Q", "-T", "-p",
             f"read_verilog -formal -sv {model}.sv reset_hold.sv; prep -top reset_hold; "
             "clk2fflogic; chformal -lower; write_smt2 -wires safety.smt2; "
             "chformal -assert -remove; write_smt2 -wires reach.smt2"], work)
        reach = smtbmc(work, "reach.smt2", ["-c"])
        cover = re.search(r"Reached cover statement in step (\d+)", reach)
        if not cover:
            raise RuntimeError(f"Missing activation cover\n{reach}")
        result = {"cover_step": int(cover[1])}
        results[model] = result
        if model == "original":
            log = smtbmc(work, "safety.smt2", ["--dump-yw", "counterexample.yw"], failure=True)
            if "Assert failed in reset_hold" not in log:
                raise RuntimeError(log)
            result["bmc"] = "counterexample"
            failed_step = int(re.findall(r"Checking assertions in step (\d+)", log)[-1])
            result["failed_step"] = failed_step
        else:
            smtbmc(work, "safety.smt2", [])
            induction = smtbmc(work, "safety.smt2", ["-i"])
            if "Temporal induction successful" not in induction:
                raise RuntimeError(induction)
            result.update(bmc="passed", temporal_induction="passed")

    witness = (work / "counterexample.yw").read_bytes()
    rows = input_rows(json.loads(witness))
    if not rows or len(rows) != failed_step + 1:
        raise RuntimeError("Witness length disagrees with failed step")
    vectors = "".join(f"{r['reset']} {r['req']:02x} {r['priority_override']:02x}\n" for r in rows)
    (work / "witness.txt").write_text(vectors)
    for model, result in results.items():
        acts = replay(work, model, rows)
        if [a["step"] for a in acts] != [failed_step]:
            raise RuntimeError(f"{model} replay missed the formal activation: {acts}")
        held = acts[0]["before_hex"] == acts[0]["after_hex"]
        if held != (model == "sync_control"):
            raise RuntimeError(f"{model} replay disagrees with formal safety result: {acts}")
        result["icarus_activation"] = acts[0]
    if (results["original"]["icarus_activation"]["before_hex"] !=
            results["sync_control"]["icarus_activation"]["before_hex"]):
        raise RuntimeError("Models disagree before reset assertion")
    report = {"rtl_sha256": digest, "smt_steps": STEPS, "unit": "half clock period",
              "versions": {tool: run([tool, flag], work).splitlines()[0] for tool, flag in
                           [("yosys", "-V"), ("z3", "--version"), ("iverilog", "-V")]},
              "models": results, "counterexample_inputs": rows}
    return report, witness


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    output = parser.parse_args().output
    with tempfile.TemporaryDirectory() as tmp:
        report, witness = check(Path(tmp))
    output.mkdir(parents=True, exist_ok=True)
    (output / "counterexample.yw").write_bytes(witness)
    (output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["models"], indent=2))


if __name__ == "__main__":
    main()
