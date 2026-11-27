#!/usr/bin/env python3
"""Replay native SMT counterexamples on the unchanged FIFO and the corresponding RTL control."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from predicates import ROOT


BENCH = ROOT / "examples/axis_fifo/formal/replay_fifo.sv"
PINS = {"rst": 1, "s_axis_tvalid": 1, "s_axis_tdata": 8, "s_axis_tlast": 1, "s_axis_tuser": 1, "m_axis_tready": 1}
OUTPUTS = {"s_axis_tready": 1, "m_axis_tvalid": 1, "m_axis_tdata": 8, "m_axis_tlast": 1, "m_axis_tuser": 1}
CONTROL = {"drop_valid": "valid_lost", "flip_data": "data_changed", "flip_last": "last_changed", "flip_user": "user_changed"}
HELD_FIELDS = {"valid_lost": "m_axis_tvalid", "data_changed": "m_axis_tdata",
               "last_changed": "m_axis_tlast", "user_changed": "m_axis_tuser"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def input_rows(witness):
    """Decode only external ports from packed YW, without forcing initial memory/register state."""
    require(witness["format"] == "Yosys Witness Trace", "unexpected solver witness format")
    require(witness["clocks"] == [{"path": ["\\clk"], "edge": "posedge", "offset": 0}],
            "unexpected solver clock")
    loc = {}
    offset = 0
    for signal in witness["signals"]:
        path, width = signal["path"], signal["width"]
        if len(path) == 1 and path[0].removeprefix("\\") in PINS:
            name = path[0].removeprefix("\\")
            require(not signal["init_only"] and signal["offset"] == 0 and width == PINS[name] and name not in loc,
                    f"unsupported witness port layout: {name}")
            loc[name] = offset
        offset += width
    require(loc.keys() == PINS.keys(), f"missing primary input(s): {PINS.keys() - loc.keys()}")
    rows = []
    for step in witness["steps"]:
        low_first = step["bits"][::-1]
        row = {}
        for pin, width in PINS.items():
            raw = low_first[loc[pin]:loc[pin] + width][::-1]
            require(len(raw) == width and set(raw) <= {"0", "1"}, f"unknown/incomplete YW input {pin}: {raw}")
            row[pin] = int(raw, 2)
        rows.append(row)
    require(len(rows) >= 2 and rows[0]["rst"] == 1, "witness must begin in reset")
    return rows


def physical_replay(binary, rows, folder):
    folder.mkdir()
    (folder / "witness.txt").write_text("".join(
        " ".join(format(r[name], f"0{width}b") for name, width in PINS.items()) + "\n" for r in rows))
    proc = subprocess.run(["vvp", binary], cwd=folder, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=30)
    (folder / "icarus.log").write_text(proc.stdout)
    proc.check_returncode()
    lines = proc.stdout.splitlines()
    require(f"REPLAY_COMPLETE {len(rows)}" in lines, "simulation did not finish the witness")
    samples = []
    for line in lines:
        if not line.startswith("PRE "):
            continue
        _, index, *fields = line.split()
        i = len(samples)
        require(int(index) == i < len(rows), "nonconsecutive physical witness samples")
        sample = dict(zip((*PINS, *OUTPUTS), fields, strict=True))
        for pin, width in (PINS | OUTPUTS).items():
            require(len(sample[pin]) == width and set(sample[pin]) <= set("01xz"), f"malformed {pin} at {i}")
        for name, width in PINS.items():
            require(sample[name] == format(rows[i][name], f"0{width}b"), f"{name} differs at step {i}")
        samples.append(sample)
    require(len(samples) == len(rows), "missing physical witness rows")
    return samples


def known(sample, names, step):
    for name in names:
        require(set(sample[name]) <= {"0", "1"}, f"inconclusive: {name} is {sample[name]} at active step {step}")


def inspect(samples):
    held = []
    for i in range(1, len(samples)):
        old, new = samples[i-1], samples[i]
        if old["rst"] == "1" or new["rst"] == "1":
            continue
        if old["s_axis_tvalid"] == "1":
            known(old, ("s_axis_tready",), i-1)
            if old["s_axis_tready"] == "0":
                for pin in ("s_axis_tvalid", "s_axis_tdata", "s_axis_tlast", "s_axis_tuser"):
                    require(old[pin] == new[pin], f"illegal source: {pin} changed after stall at {i-1}")
        known(old, ("m_axis_tvalid",), i-1)
        if old["m_axis_tvalid"] != "1" or old["m_axis_tready"] != "0":
            continue
        pins = HELD_FIELDS.values()
        known(old, pins, i-1)
        known(new, pins, i)
        changed = [prop for prop, pin in HELD_FIELDS.items() if old[pin] != new[pin]]
        held.append({"step": i, "violated": changed,
                     "previous": {pin: old[pin] for pin in (*pins, "m_axis_tready", "rst")},
                     "current": {pin: new[pin] for pin in (*pins, "m_axis_tready", "rst")}})
    return held


def witness_files(summary, name, source, candidate_grade):
    model = summary["models"][name]
    if candidate_grade:
        prop = CONTROL[name]
        sample = {"active": True, **{field: field == prop for field in HELD_FIELDS}}
        require(model["status"] == "FAILED" and model["sampled_atoms"] == sample and
                model["witness"] == f"{name}/counterexample.yw" and model["input_rows"] == f"{name}/inputs.json",
                f"candidate result lacks an isolated {prop} failure")
        yw = source / name / "counterexample.yw"
        require(sha(yw.read_bytes()) == model["witness_sha256"], f"changed candidate witness for {name}")
        yield "candidate", model, yw, source / name / "inputs.json"
    else:
        for stem in ("bundled", "split"):
            diagnosis = model[stem]
            expected = "bundled" if stem == "bundled" else CONTROL[name]
            require(diagnosis["status"] == "FAILED" and diagnosis["failed_assertions"] == [expected] and
                    diagnosis["witness"] == stem + ".yw", f"missing native solver failure for {name}/{stem}")
            yield stem, diagnosis, source / name / (stem + ".yw"), source / name / (stem + ".inputs.json")


def experiment(rtl, formal, out, candidate_grade=False):
    from egg_fifo_formal import variants
    manifest = json.loads((ROOT / "scripts/m3_controller_replay_manifest.json").read_text())
    data = rtl.read_bytes()
    require(sha(data) == manifest["sha256"]["public/rtl/axis_fifo.v"], "unexpected FIFO source hash")
    evidence = (formal / "summary.json").read_bytes()
    results = json.loads(evidence)
    require(results["rtl_sha256"] == sha(data), "formal and replay source identities differ")
    if candidate_grade:
        require(results["models"]["original"]["status"] == "PASSED", "candidate fails original FIFO")
    else:
        require(results["upstream_commit"] == manifest["commit"], "unexpected formal source commit")
    cases = variants(data.decode())
    require(cases.keys() == {"original", *CONTROL}, "unexpected native control variants")
    report = {"rtl_sha256": sha(data), "source_commit": manifest["commit"], "bench_sha256": sha(BENCH.read_bytes()),
              "formal_summary_sha256": sha(evidence),
              "iverilog": subprocess.check_output(["iverilog", "-V"], text=True, stderr=subprocess.DEVNULL).splitlines()[0],
              "witnesses": []}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        binaries = {}
        for name, text in cases.items():
            require(results["models"][name]["rtl_sha256"] == sha(text.encode()), f"formal RTL hash mismatch: {name}")
            case = tmp / name
            case.mkdir()
            (case / "axis_fifo.v").write_text(text)
            binaries[name] = case / "fifo.vvp"
            subprocess.run(["iverilog", "-g2012", "-s", "replay_fifo", "-o", binaries[name], "axis_fifo.v", BENCH],
                           cwd=case, capture_output=True, check=True, timeout=30)
        for name, prop in CONTROL.items():
            for stem, diagnosis, yw, inputs in witness_files(results, name, formal, candidate_grade):
                rows = input_rows(json.loads(yw.read_bytes()))
                require(rows == json.loads(inputs.read_bytes()), f"decoded inputs differ from solver witness for {name}/{stem}")
                pair = {}
                for design in ("original", name):
                    samples = physical_replay(binaries[design], rows, out / f"{name}-{stem}-{design}")
                    pair[design] = inspect(samples)
                base = {s["step"]: s["violated"] for s in pair["original"]}
                require(not any(base.values()), f"original failed on {name}/{stem}")
                failed = [s["step"] for s in pair[name] if prop in s["violated"]]
                require(failed and all(i in base for i in failed), f"unconfirmed paired {prop} on {name}/{stem}")
                violations = [(s["step"], s["violated"]) for s in pair[name] if s["violated"]]
                require(violations == [(diagnosis["failed_step"], [prop])] and failed[0] + 1 == len(rows),
                        f"solver and physical first failure step/field differ on {name}/{stem}")
                report["witnesses"].append({"control": name, "query": stem, "property": prop, "steps": len(rows),
                                            "first_physical_failure": failed[0], "yw_sha256": sha(yw.read_bytes()),
                                            "control_rtl_sha256": sha(cases[name].encode()), "stalls": pair})
    report["physical_replays"] = 2 * len(report["witnesses"])
    (out / "summary.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rtl", type=Path, required=True, help="manifest-pinned public/rtl/axis_fifo.v")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--formal-run", type=Path, help="egg_fifo_formal output with native counterexamples")
    source.add_argument("--candidate-grade", type=Path,
                        help="one candidate round's rtl directory with all four isolated failure witnesses")
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    experiment(args.rtl, args.formal_run or args.candidate_grade, args.output, candidate_grade=args.candidate_grade is not None)
