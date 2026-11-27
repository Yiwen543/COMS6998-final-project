#!/usr/bin/env python3
"""Check an AXI FIFO backpressure obligation against a split Boolean specification."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from predicates import ROOT, parse

FIELDS = ("valid_lost", "data_changed", "last_changed", "user_changed")
BUNDLED = "(and active (or valid_lost (or data_changed (or last_changed user_changed))))"
SPLIT = tuple(f"(and active {name})" for name in FIELDS)
FAULTS = dict(drop_valid="valid_lost", flip_data="data_changed", flip_last="last_changed", flip_user="user_changed")
INPUTS = {"rst": 1, "s_axis_tvalid": 1, "s_axis_tdata": 8, "s_axis_tlast": 1, "s_axis_tuser": 1,
          "m_axis_tready": 1}
STEPS = 12


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def variants(source):
    """Change one output pipeline register on a stall; reset retains precedence."""
    anchor = "    if (rst) begin\n        rd_ptr_reg <= {ADDR_WIDTH+1{1'b0}};"
    if source.count(anchor) != 1:
        raise ValueError("Missing unique output-pipeline read/reset anchor")
    changes = {"drop_valid": "m_axis_tvalid_pipe_reg[RAM_PIPELINE] <= 1'b0;"}
    for name, index in [("flip_data", "0"), ("flip_last", "LAST_OFFSET"), ("flip_user", "USER_OFFSET")]:
        lhs = f"m_axis_pipe_reg[RAM_PIPELINE][{index}]"
        changes[name] = f"{lhs} <= ~{lhs};"
    return {"original": source, **{name: source.replace(anchor, "    if (m_axis_tvalid && !m_axis_tready) "
                                                        + statement + "\n" + anchor)
                                  for name, statement in changes.items()}}


def render(ast):
    """Only the Boolean grammar shared with the egg run enters the SV assertion."""
    if isinstance(ast, str):
        if ast not in (*FIELDS, "active"):
            raise ValueError(f"Unexpected property atom {ast}")
        return ast
    op, *args = ast
    if op == "not":
        return f"(!{render(args[0])})"
    sign = {"and": "&&", "or": "||"}[op]
    return f"({render(args[0])} {sign} {render(args[1])})"


def assertions(mode):
    if mode == "cover":
        return "always @* stall_reached: cover(active);\n"
    terms = (("bundled", BUNDLED),) if mode == "bundled" else zip(FIELDS, SPLIT)
    return "".join(f"always @* check_{name}: assert(!{render(parse(text))});\n"
                   for name, text in terms if mode in ("bundled", "split", name))


def input_rows(witness):
    """Decode concrete top-level pins, ignoring solver-initialized internal memory."""
    clocks = witness.get("clocks")
    if clocks != [{"path": ["\\clk"], "edge": "posedge", "offset": 0}]:
        raise ValueError("Expected one rising-edge clock")
    rows = []
    width_total = sum(s["width"] for s in witness["signals"])
    for entry in witness["steps"]:
        if len(entry["bits"]) > width_total:
            raise ValueError("Malformed witness row")
        # The YW format omits high unknown bits, often within initial RAM.
        bits = entry["bits"].rjust(width_total, "?")
        row = {}
        for sig in witness["signals"]:
            width = sig["width"]
            value, bits = bits[-width:], bits[:-width]
            if not sig["init_only"] and len(sig["path"]) == 1:
                name = sig["path"][0].removeprefix("\\")
                if name == "clk":
                    continue
                if (name in row or width != INPUTS.get(name) or sig["offset"] or
                        any(digit not in "01" for digit in value)):
                    raise ValueError(f"Missing or ambiguous witness input {name}")
                row[name] = int(value, 2)
        if bits or row.keys() != INPUTS.keys():
            raise ValueError("Incomplete top-level pin witness")
        rows.append(row)
    if not rows or not rows[0]["rst"]:
        raise ValueError("Witness does not start in reset")
    return rows


def execute(cmd, work, expected=0):
    proc = subprocess.run(cmd, cwd=work, text=True, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
    if proc.returncode != expected:
        raise RuntimeError(f"{cmd} exited {proc.returncode}\n{proc.stdout}")
    return proc.stdout


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def check_mode(work, results, design, mode):
    from time import perf_counter
    exprs = assertions(mode)
    (work / "obligations.svh").write_text(exprs)
    execute(["yosys", "-Q", "-T", "-p",
             "read_verilog -formal -sv axis_fifo.v stall.sv; prep -top fifo_stall_formal -flatten; "
             "chformal -lower; write_smt2 -wires fifo.smt2"], work)
    model = (work / "fifo.smt2").read_text()
    names = re.findall(r"^; yosys-smt2-assert \d+ (\w+)", model, re.M)
    covers = re.findall(r"^; yosys-smt2-cover \d+ (\w+)", model, re.M)
    expected = [] if mode == "cover" else [f"check_{n}" for n in (FIELDS if mode == "split" else (mode,))]
    if (sorted(names) != sorted(expected) or covers != (["stall_reached"] if mode == "cover" else [])
            or model.count("; yosys-smt2-assume ") != 3):
        raise ValueError(f"Unexpected elaborated property or assumption inventory in {mode}")
    fault = FAULTS.get(design)
    negative = fault is not None and mode in ("bundled", "split", fault)
    capture = mode == "cover" or (negative and mode in ("bundled", "split"))
    name = f"{mode}.yw"
    cmd = ["yosys-smtbmc", "-s", "z3", "-t", str(STEPS), "--noprogress"]
    options = ["-c"] if mode == "cover" else []
    if capture:
        options.extend(["--dump-yw", name])
    start = perf_counter()
    log = execute([*cmd, *options, "fifo.smt2"], work, expected=int(negative))
    elapsed = perf_counter() - start
    status = "FAILED" if negative else "PASSED"
    if not log.rstrip().endswith(f"Status: {status}"):
        raise ValueError(log)
    out = {"status": status, "emitted_assertions": names, "bmc_or_cover_seconds": elapsed}
    if mode == "cover":
        reached = re.search(r"Reached cover statement in step (\d+) at fifo_stall_formal: stall_reached", log)
        if not reached:
            raise ValueError(log)
        out["cover_step"] = int(reached[1])
    if negative:
        found = re.findall(r"Assert failed in fifo_stall_formal: check_(\w+)", log)
        if found != ["bundled" if mode == "bundled" else fault]:
            raise ValueError(f"Unexpected failing property {found} for {design}/{mode}")
        out["failed_assertions"] = found
        out["failed_step"] = int(re.findall(r"Checking assertions in step (\d+)", log)[-1])
    if capture:
        shutil.copyfile(work / name, results / name)
        out["witness"] = name
        if negative:
            inputs = input_rows(json.loads((work / name).read_bytes()))
            if len(inputs) != out["failed_step"] + 1:
                raise ValueError("Witness and failing step disagree")
            write_json(results / f"{mode}.inputs.json", inputs)
    if design == "original" and mode in ("bundled", "split"):
        start = perf_counter()
        induction = execute([*cmd, "-i", "fifo.smt2"], work)
        out["induction_seconds"] = perf_counter() - start
        if not induction.rstrip().endswith("Status: PASSED") or "Temporal induction successful." not in induction:
            raise ValueError(induction)
        out["temporal_induction"] = "PASSED"
        log += "\n" + induction
    return out, log


def run(rtl, out):
    manifest = json.loads((ROOT / "scripts/m3_controller_replay_manifest.json").read_text())
    raw = rtl.read_bytes()
    if digest(raw) != manifest["sha256"]["public/rtl/axis_fifo.v"]:
        raise ValueError("axis_fifo.v hash differs from the pinned fixture")
    harness = ROOT / "examples/axis_fifo/formal/stall.sv"
    models = variants(raw.decode())
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        bundle = work / "results"
        bundle.mkdir()
        forms = bundle / "assertions"
        forms.mkdir()
        modes = ["bundled", "split", "cover", *FIELDS]
        for mode in modes:
            (forms / f"{mode}.svh").write_text(assertions(mode))
        shutil.copyfile(harness, work / "stall.sv")
        report = {"upstream_commit": manifest["commit"], "rtl_sha256": digest(raw),
                  "harness_sha256": digest(harness.read_bytes()), "bounded_states": STEPS,
                  "clock": "Inputs and outputs sampled immediately before each rising edge",
                  "forms": {"bundled": BUNDLED, "split": list(SPLIT)},
                  "versions": {name: execute([name, flag], work).splitlines()[0] for name, flag in
                               [("yosys", "-V"), ("z3", "--version")]}, "models": {}}
        for design, src in models.items():
            (work / "axis_fifo.v").write_text(src)
            result = {"rtl_sha256": digest(src.encode()), "standalone": {}}
            case_dir = bundle / design
            case_dir.mkdir()
            logs = []
            for mode in modes:
                row, log = check_mode(work, case_dir, design, mode)
                container = result["standalone"] if mode in FIELDS else result
                container[mode] = row
                logs.append(f"=== {mode} ===\n{log}")
            (case_dir / "smtbmc.log").write_text("\n".join(logs))
            report["models"][design] = result
        write_json(bundle / "summary.json", report)
        shutil.copytree(bundle, out)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rtl", type=Path, required=True, help="hash-pinned public/rtl/axis_fifo.v")
    parser.add_argument("--output", type=Path, required=True, help="new results directory")
    args = parser.parse_args()
    summary = run(args.rtl, args.output)
    print(f"{len(summary['models'])} RTLs checked, {STEPS} states per bounded query")
