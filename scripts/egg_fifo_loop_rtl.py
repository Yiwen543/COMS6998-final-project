#!/usr/bin/env python3
"""Grade a candidate list of FIFO violation terms on the original and four control RTLs."""
import argparse
import gzip
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from time import perf_counter

from egg_fifo_formal import FIELDS, STEPS, digest, execute, input_rows, render, variants, write_json
from predicates import ROOT, evaluate, parse

ATOMS = ("active", *FIELDS)


def candidate_assertions(terms):
    if not isinstance(terms, list) or not terms or not all(isinstance(term, str) for term in terms):
        raise ValueError("Expected a nonempty list of Boolean violation terms")
    try:
        trees = [parse(term) for term in terms]
        rendered = [render(tree) for tree in trees]
    except (IndexError, RecursionError, ValueError) as exc:
        raise ValueError(f"Invalid sampled Boolean term: {exc}") from exc
    lines = [f"(* keep *) wire [4:0] loop_sample = {{{', '.join(ATOMS)}}};",
             "always @* stall_reached: cover(active);"]
    lines.extend(f"always @* check_{i}: assert(!{term});" for i, term in enumerate(rendered))
    return trees, "\n".join(lines) + "\n"


def sample_states(vcd, last):
    """Extract our explicit five-bit observation port at the SMT steps in a Yosys VCD."""
    scope = []
    ids = {}
    step = None
    bits = None
    samples = {}
    for line in vcd.splitlines():
        words = line.split()
        if line.startswith("$scope "):
            scope.append(words[2])
        elif line.startswith("$upscope "):
            scope.pop()
        elif line.startswith("$var "):
            if scope == [] and words[4] == "smt_step":
                ids["step"] = words[3]
            if scope == ["fifo_stall_formal"] and words[4] == "loop_sample" and words[2] == "5":
                ids["sample"] = words[3]
        elif line.startswith("#"):
            if step is not None and bits is not None:
                samples[step] = bits
        elif line.startswith("b") and len(words) == 2:
            if words[1] == ids.get("step"):
                step = int(words[0][1:], 2)
            elif words[1] == ids.get("sample"):
                bits = words[0][1:]
    if step is not None and bits is not None:
        samples[step] = bits
    result = []
    for i in range(last + 1):
        value = samples.get(i, "")
        if len(value) != len(ATOMS) or set(value) - {"0", "1"}:
            raise ValueError(f"Missing or incomplete sampled atoms at step {i}")
        result.append(dict(zip(ATOMS, (bit == "1" for bit in value))))
    return result


def bmc(work, result_dir, design, trees):
    cmd = ["yosys-smtbmc", "-s", "z3", "-t", str(STEPS), "--noprogress",
           "--dump-yw", "counterexample.yw", "--dump-vcd", "trace.vcd", "candidate.smt2"]
    start = perf_counter()
    proc = subprocess.run(cmd, cwd=work, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
    log = proc.stdout
    elapsed = perf_counter() - start
    (result_dir / "smtbmc.log").write_text(log)
    passed = proc.returncode == 0 and log.rstrip().endswith("Status: PASSED")
    failed = proc.returncode == 1 and log.rstrip().endswith("Status: FAILED") and "BMC failed!" in log
    if not (passed or failed):
        raise RuntimeError(f"Inconclusive BMC result on {design}, exit {proc.returncode}: {log[-1000:]}")
    steps = [int(s) for s in re.findall(r"Checking assertions in step (\d+)", log)]
    if not steps or steps != list(range(steps[-1] + 1)) or steps[-1] >= STEPS or (passed and len(steps) != STEPS):
        raise RuntimeError(f"Incomplete BMC step accounting on {design}: {steps}")
    row = {"status": "PASSED" if passed else "FAILED", "failed_indices": [], "failed_step": None,
           "sampled_atoms": None, "witness": None, "bmc_seconds": elapsed}
    messages = re.findall(
        r"^##\s+\S+\s+(Checking assertions in step \d+\.\.|Assert failed in "
        r"fifo_stall_formal: check_\d+|Status: (?:PASSED|FAILED))\s*$",
        log, re.M,
    )
    checks = [line for line in messages if line.startswith("Checking assertions")]
    failures = [line for line in messages if line.startswith("Assert failed")]
    verdict = f"Status: {row['status']}"
    if not checks or verdict not in messages or (failed and not failures):
        raise RuntimeError(f"SMTBMC excerpt is incomplete on {design}")
    row["log_excerpt"] = [checks[-1], *failures[:1], verdict]
    if passed:
        return row
    found = sorted(int(i) for i in re.findall(r"Assert failed in fifo_stall_formal: check_(\d+)\s*$", log, re.M))
    fail_step = steps[-1]
    waveform = (work / "trace.vcd").read_bytes()
    states = sample_states(waveform.decode(), fail_step)
    violations = [[i for i, tree in enumerate(trees) if evaluate(tree, state)] for state in states]
    if not found or any(violations[:-1]) or violations[-1] != found:
        raise ValueError(f"Solver and independent term evaluation disagree on {design}: {found}, {violations}")
    raw = (work / "counterexample.yw").read_bytes()
    rows = input_rows(json.loads(raw))
    if len(rows) != fail_step + 1:
        raise ValueError(f"Witness length differs from first failure on {design}")
    (result_dir / "counterexample.yw").write_bytes(raw)
    (result_dir / "trace.vcd.gz").write_bytes(gzip.compress(waveform, mtime=0))
    write_json(result_dir / "inputs.json", rows)
    row.update(failed_indices=found, failed_step=fail_step, sampled_atoms=states[-1],
               witness=f"{design}/counterexample.yw", witness_sha256=digest(raw),
               input_rows=f"{design}/inputs.json", waveform=f"{design}/trace.vcd.gz")
    return row


def grade_rtl(rtl: Path, obligations: list[str], out: Path) -> dict:
    """One 12-state BMC per RTL and one independent antecedent cover on the original."""
    trees, sv = candidate_assertions(obligations)
    raw = rtl.read_bytes()
    manifest = json.loads((ROOT / "scripts/m3_controller_replay_manifest.json").read_text())
    if digest(raw) != manifest["sha256"]["public/rtl/axis_fifo.v"]:
        raise ValueError("FIFO RTL differs from the pinned source")
    harness = ROOT / "examples/axis_fifo/formal/stall.sv"
    out.mkdir(parents=True, exist_ok=True)
    result = {"bounded_states": STEPS, "obligations": obligations, "rtl_sha256": digest(raw),
              "harness_sha256": digest(harness.read_bytes()), "assertions_sha256": digest(sv.encode()),
              "models": {}}
    # Reserve this run before emitting anything, including on concurrent retries.
    with (out / "obligations.svh").open("x") as output:
        output.write(sv)
    for design, text in variants(raw.decode()).items():
        folder = out / design
        folder.mkdir()
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            shutil.copyfile(harness, work / "stall.sv")
            (work / "obligations.svh").write_text(sv)
            (work / "axis_fifo.v").write_text(text)
            # Preserve names even when two obligations simplify to identical logic.
            synth = ("read_verilog -formal -sv axis_fifo.v stall.sv; setattr -set keep 1 t:$check; "
                     "prep -top fifo_stall_formal -flatten; chformal -lower; write_smt2 -wires candidate.smt2")
            if design == "original":
                synth += "; chformal -assert -remove; write_smt2 -wires cover.smt2"
            execute(["yosys", "-Q", "-T", "-p", synth], work)
            model = (work / "candidate.smt2").read_text()
            names = re.findall(r"^; yosys-smt2-assert \d+ (\w+)", model, re.M)
            if (sorted(names) != sorted(f"check_{i}" for i in range(len(trees))) or
                    model.count("; yosys-smt2-assume ") != 3):
                raise RuntimeError(f"Candidate assertions or input assumptions lost during synthesis on {design}")
            if design == "original":
                cover = execute(["yosys-smtbmc", "-s", "z3", "-t", str(STEPS), "--noprogress",
                                 "-c", "cover.smt2"], work)
                (folder / "cover.log").write_text(cover)
                reached = re.search(r"Reached cover statement in step (\d+) at fifo_stall_formal: stall_reached", cover)
                if not reached or not cover.rstrip().endswith("Status: PASSED"):
                    raise RuntimeError(f"Stall activation not established: {cover}")
                result["original_stall_cover_step"] = int(reached[1])
            row = bmc(work, folder, design, trees)
            row["rtl_sha256"] = digest(text.encode())
            result["models"][design] = row
    write_json(out / "summary.json", result)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rtl", type=Path, required=True)
    ap.add_argument("--obligations", type=Path, required=True, help="JSON array of candidate violation terms")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    graded = grade_rtl(args.rtl, json.loads(args.obligations.read_bytes()), args.output)
    print({design: row["status"] for design, row in graded["models"].items()})
