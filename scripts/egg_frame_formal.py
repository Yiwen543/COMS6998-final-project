#!/usr/bin/env python3
"""Check five typed frame properties on the full pinned wrapper and physically replay cover traces."""
import argparse
from collections import deque
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from egg_frame_terms import REFERENCES, parse_term, sv_term
from predicates import ROOT

ASSETS = ROOT / "examples/axis_frame_length/formal"
SOURCES = ("public/rtl/axis_fifo.v", "public/rtl/axis_frame_length_adjust.v",
           "public/rtl/axis_frame_length_adjust_fifo.v", "public/task_top_v3.sv")
PROPERTIES = ("data_hold", "header_hold", "pad_flag", "truncate_flag", "clamped_length")
COVERS = ("data_stall", "header_stall", "padded_header", "truncated_header", "length_four", "length_eight")
PINS = {"rst": 1, "s_valid": 1, "s_data": 8, "s_last": 1, "m_ready": 1, "h_ready": 1}
OUTPUTS = ("s_ready", "m_data", "m_valid", "m_last", "h_valid", "h_pad", "h_truncate", "h_length", "h_original_length")
STEPS = 24


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(cmd, work, *, check=True):
    proc = subprocess.run(cmd, cwd=work, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    if check and proc.returncode:
        raise RuntimeError(f"{cmd} exited {proc.returncode}\n{proc.stdout[-2000:]}")
    return proc


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n")


def witness_pins(path):
    trace = json.loads(path.read_bytes())
    if trace["clocks"] != [{"path": ["\\clk"], "edge": "posedge", "offset": 0}]:
        raise ValueError("Expected one rising-edge clock")
    positions, offset = {}, 0
    for sig in trace["signals"]:
        key = sig["path"][0].removeprefix("\\")
        if len(sig["path"]) == 1 and key in PINS:
            if sig["init_only"] or sig["offset"] or sig["width"] != PINS[key] or key in positions:
                raise ValueError(f"Invalid primary input declaration: {key}")
            positions[key] = offset
        offset += sig["width"]
    if positions.keys() != PINS.keys():
        raise ValueError("Missing frame_task witness pins")
    rows = []
    for state in trace["steps"]:
        bits = state["bits"][::-1]
        row = {}
        for key, start in positions.items():
            field = bits[start:start + PINS[key]][::-1]
            if len(field) != PINS[key] or set(field) - {"0", "1"}:
                raise ValueError(f"Undefined primary input {key}")
            row[key] = int(field, 2)
        rows.append(row)
    if not rows or not rows[0]["rst"]:
        raise ValueError("Missing initial reset")
    return rows


def replay(trace, goals, work, out):
    rows = witness_pins(trace)
    (work / "inputs.txt").write_text("".join(
        f"{r['rst']} {r['s_valid']} {r['s_data']:02x} {r['s_last']} {r['m_ready']} {r['h_ready']}\n" for r in rows))
    log = run(["vvp", "cover.vvp"], work).stdout
    (out / (trace.stem + ".icarus.log")).write_text(log)
    pre = [line.split()[1:] for line in log.splitlines() if line.startswith("PRE ")]
    if len(pre) != len(rows) or f"REPLAY_COMPLETE {len(rows)}\n" not in log:
        raise ValueError("Incomplete Icarus replay")
    accepted = 0
    completed = deque()
    hits = {}
    prev = {}
    for i, (encoded, stimulus) in enumerate(zip(pre, rows)):
        if int(encoded[0]) != i:
            raise ValueError("Nonconsecutive physical samples")
        val = {k: (int(v, 16) if re.fullmatch("[0-9a-fA-F]+", v) else None)
               for k, v in zip((*PINS, *OUTPUTS), encoded[1:], strict=True)}
        if {k: val[k] for k in PINS} != stimulus or (val["rst"] and val["s_valid"]):
            raise ValueError("Input/reset mismatch on replay")
        if val["rst"]:
            completed.clear()
            accepted = 0
        else:
            if val["s_valid"] and val["s_ready"] is None:
                raise ValueError("Unknown physical source handshake")
            if i and not prev["rst"]:
                if prev["s_valid"] and prev["s_ready"] == 0:
                    if any(prev[k] != val[k] for k in ("s_valid", "s_data", "s_last")):
                        raise ValueError("Illegal input change during a source stall")
                for name, valid, ready in [("data_stall", "m_valid", "m_ready"), ("header_stall", "h_valid", "h_ready")]:
                    if prev[valid] == 1 and not prev[ready]:
                        hits.setdefault(name, set()).add(i)
            if val["h_valid"] == 1:
                n = val["h_original_length"]
                # Decode real accepted TLASTs independently of the DUT's counter
                # before crediting any presentation of this length on a cover trace.
                if not completed or completed[0] != n:
                    raise ValueError("Header disagrees with completed accepted frame lengths")
                if (val["h_pad"], val["h_truncate"], val["h_length"]) != (n < 4, n > 8, min(8, max(4, n))):
                    raise ValueError("Header flags/length incorrect on cover replay")
                for name, enabled in [("padded_header", n < 4), ("truncated_header", n > 8),
                                      ("length_four", n == 4), ("length_eight", n == 8)]:
                    if enabled:
                        hits.setdefault(name, set()).add(i)
                if val["h_ready"]:
                    completed.popleft()
            if val["s_valid"] and val["s_ready"]:
                accepted += 1
                if accepted > 12:
                    raise ValueError("Cover input exceeds frame-length bound")
                if val["s_last"]:
                    completed.append(accepted)
                    accepted = 0
        prev = val
    for goal, at in goals.items():
        if at not in hits.get(goal, set()):
            raise ValueError(f"Cover {goal} not reproduced at step {at}")
    return {"steps": len(rows), "confirmed": goals, "original_witness_sha256": sha(trace.read_bytes())}


def status(proc):
    log = proc.stdout
    if proc.returncode == 0 and log.rstrip().endswith("Status: PASSED"):
        return "PASSED"
    if proc.returncode == 1 and "BMC failed!" in log and log.rstrip().endswith("Status: FAILED"):
        return "COUNTEREXAMPLE"
    if "timeout" in log.lower() or "unknown" in log.lower():
        return "INCONCLUSIVE"
    raise RuntimeError(log[-2000:])


def experiment(fixture, destination):
    manifest = json.loads((ROOT / "scripts/m3_controller_replay_manifest.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        out = work / "results"
        out.mkdir()
        inputs = {}
        for rel in SOURCES:
            raw = (fixture / rel).read_bytes()
            inputs[rel] = sha(raw)
            if inputs[rel] != manifest["sha256"][rel]:
                raise ValueError(f"Source hash differs: {rel}")
            (work / Path(rel).name).write_bytes(raw)
        for name in ("frame_properties.sv", "replay_cover.sv"):
            shutil.copyfile(ASSETS / name, work / name)
        assertions = "".join(f"{name}: assert(!({sv_term(parse_term(REFERENCES[name]))}));\n" for name in PROPERTIES)
        (out / "frame_assertions.svh").write_text(assertions)
        (work / "frame_assertions.svh").write_text(assertions)
        files = " ".join(Path(src).name for src in SOURCES)
        front = f"read_verilog -formal -sv {files} frame_properties.sv; prep -top frame_properties -flatten; chformal -lower; "
        build = (front + "design -save full; write_smt2 -wires safety.smt2; chformal -assert -remove; "
                 "write_smt2 -wires reach.smt2; design -load full; "
                 "chformal -assert -remove frame_properties/pad_flag frame_properties/truncate_flag frame_properties/clamped_length; "
                 "write_smt2 -wires holds.smt2")
        run(["yosys", "-Q", "-T", "-p", build], work)
        for file, expected in [("safety", PROPERTIES), ("reach", ()), ("holds", PROPERTIES[:2])]:
            smt = (work / f"{file}.smt2").read_text()
            if (set(re.findall(r"^; yosys-smt2-assert \d+ (\w+)", smt, re.M)) != set(expected) or
                    set(re.findall(r"^; yosys-smt2-cover \d+ (\w+)", smt, re.M)) != set(COVERS) or
                    smt.count("; yosys-smt2-assume ") != 4):
                raise ValueError(f"Unexpected elaborated property or assumption inventory: {file}")
        smtbmc = ["yosys-smtbmc", "-s", "z3", "--noprogress"]
        reach = run([*smtbmc, "-t", str(STEPS), "--timeout", "60", "-c", "--dump-yw", "cover-%.yw", "reach.smt2"], work)
        (out / "cover.log").write_text(reach.stdout)
        covered, by_file, pending = {}, {}, {}
        for line in reach.stdout.splitlines():
            goal = re.search(r"Reached cover statement in step (\d+) at frame_properties: (\w+)", line)
            if goal:
                covered[goal[2]] = pending[goal[2]] = int(goal[1])
            saved = re.search(r"Writing trace to Yosys witness file: (cover-\d+.yw)$", line)
            if saved:
                by_file[saved[1]], pending = pending, {}
        if set(covered) != set(COVERS) or pending or status(reach) != "PASSED":
            raise ValueError("Unreached cover or missing trace")
        run(["iverilog", "-g2012", "-s", "replay_cover", "-o", "cover.vvp", *files.split(), "replay_cover.sv"], work)
        replays = {}
        for name, goals in by_file.items():
            shutil.copyfile(work / name, out / name)
            replays[name] = replay(work / name, goals, work, out)

        # A bounded SAT unroll checks all five assertions at once, starting at
        # the initial state. A solver timeout is retained as a distinct outcome.
        sat_command = (front + "chformal -cover -remove; memory_map; opt; "
                       f"sat -set-assumes -seq {STEPS} -prove-asserts -timeout 90 -dump_vcd safety.vcd")
        sat = run(["yosys", "-Q", "-T", "-p", sat_command], work)
        (out / "sat.log.gz").write_bytes(gzip.compress(sat.stdout.encode(), mtime=0))
        if "SAT proof finished - no model found: SUCCESS!" in sat.stdout:
            verdict = "PASSED"
        elif "SAT proof finished - model found: FAIL!" in sat.stdout:
            verdict = "COUNTEREXAMPLE"
            shutil.copyfile(work / "safety.vcd", out / "sat-counterexample.vcd")
        elif "SAT solving finished - timeout." in sat.stdout or "SAT proof finished - timeout." in sat.stdout:
            verdict = "INCONCLUSIVE"
        else:
            raise ValueError(sat.stdout[-2000:])
        # Independent SMT encoding with a fixed global solver time budget.
        bmc = run([*smtbmc, "-t", str(STEPS), "--timeout", "15", "--dump-yw", "safety.yw", "safety.smt2"], work, check=False)
        (out / "safety-z3.log").write_text(bmc.stdout)
        bmc_status = status(bmc)
        if bmc_status == "COUNTEREXAMPLE":
            shutil.copyfile(work / "safety.yw", out / "safety.yw")
        steps = [int(s) for s in re.findall(r"Checking assertions in step (\d+)", bmc.stdout)]
        if not steps or steps != list(range(steps[-1]+1)):
            raise ValueError("Missing SMT BMC states")
        base = run([*smtbmc, "-t", "3", "--timeout", "15", "holds.smt2"], work)
        ind = run([*smtbmc, "-i", "-t", "3", "--timeout", "15", "holds.smt2"], work)
        (out / "holds-induction.log").write_text(base.stdout + "\n" + ind.stdout)
        if status(base) != "PASSED" or status(ind) != "PASSED" or "Temporal induction successful." not in ind.stdout:
            raise ValueError("Hold induction not established")
        report = {"upstream_commit": manifest["commit"], "source_sha256": inputs,
                  "harness_sha256": sha((work / "frame_properties.sv").read_bytes()),
                  "replay_bench_sha256": sha((work / "replay_cover.sv").read_bytes()),
                  "violation_terms": {k: REFERENCES[k] for k in PROPERTIES},
                  "full_wrapper": True, "data_fifo_depth": 32, "header_fifo_depth": 8,
                  "config": {"data_width": 8, "min_bytes": 4, "max_bytes": 8, "max_accepted_frame_bytes": 12},
                  "two_state": True, "bounded_states": STEPS, "all_properties_yosys_sat": verdict,
                  "all_properties_z3": {"status": bmc_status, "last_step_entered": steps[-1],
                                        "completed_unsat_states": len(steps) if bmc_status == "PASSED" else len(steps)-1,
                                        "solver_timeout_seconds": 15},
                  "inductive_hold_checks": {"properties": list(PROPERTIES[:2]), "base_states": 3,
                                            "induction": "PASSED"},
                  "cover_steps": covered, "icarus_cover_replays": replays,
                  "versions": {tool: run([tool, flag], work).stdout.splitlines()[0] for tool, flag in
                               [("yosys", "-V"), ("z3", "--version"), ("iverilog", "-V")]}}
        save_json(out / "summary.json", report)
        shutil.copytree(out, destination)
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fixture", type=Path, required=True, help="manifest-pinned frame fixture directory")
    ap.add_argument("--output", type=Path, required=True, help="new output directory")
    args = ap.parse_args()
    result = experiment(args.fixture, args.output)
    print("Full-wrapper bounded SAT:", result["all_properties_yosys_sat"])
    print("Covers:", result["cover_steps"])
