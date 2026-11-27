#!/usr/bin/env python3
"""Bound eight transaction obligations on the pinned full frame_task and replay native witnesses."""
import argparse
import gzip
import json
from pathlib import Path
import re
import runpy
import shutil
from tempfile import TemporaryDirectory

from egg_frame_faults import FAULTS, edit
from egg_frame_formal import OUTPUTS, PINS, SOURCES, run, sha, witness_pins
from m3_controller_replay import MAPPING, check_file
from predicates import ROOT


ASSETS = ROOT / "examples/axis_frame_length/transaction_formal"
CHECKER = "reference/frozen-v2/checker.py"
STEPS = 18
PROPERTIES = ("data_entitlement", "data_payload", "data_last", "header_entitlement",
              "header_original", "header_adjusted", "header_flags", "reset_clear")
COVERS = ("retained_byte", "pad_presented", "long_header", "header_only_transfer",
          "data_only_transfer", "reset_with_pending_output")
CONTROLS = ("F01", "F06")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build(work, fixture, design, out):
    work.mkdir()
    out.mkdir()
    fault = next((f for f in FAULTS if f.id == design), None)
    hashes = {}
    for rel in SOURCES:
        raw = check_file(fixture, rel)
        if fault and rel == fault.source:
            raw = edit(fixture, fault).encode()
        (work / Path(rel).name).write_bytes(raw)
        hashes[rel] = sha(raw)
    for name in ("frame_txn.sv", "replay_txn.sv"):
        shutil.copyfile(ASSETS / name, work / name)
    sources = [Path(src).name for src in SOURCES]
    front = ("read_verilog -formal -sv " + " ".join(sources) + " frame_txn.sv; " +
             "prep -top frame_txn -flatten; chformal -lower; ")
    proc = run(["yosys", "-Q", "-T", "-p", front + "write_smt2 -wires txn.smt2"], work)
    (out / "elaboration.log.gz").write_bytes(gzip.compress(proc.stdout.encode(), mtime=0))
    model = (work / "txn.smt2").read_text()
    for field, expected in (("assert", PROPERTIES), ("cover", COVERS)):
        labels = re.findall(r"^; yosys-smt2-" + field + r" \d+ (\w+)$", model, re.M)
        require(len(labels) == len(expected) and set(labels) == set(expected), f"unexpected {field} inventory")
    require(model.count("; yosys-smt2-assume ") == 4, "environment assumptions changed")
    require(len(re.findall(r"^; yosys-smt2-anyconst .* 3 .* byte_slot$", model, re.M)) == 1,
            "missing universal three-bit byte index")
    run(["iverilog", "-g2012", "-s", "replay_txn", "-o", "replay.vvp", *sources, "replay_txn.sv"], work)
    return front, hashes


def replay(witness, work, output, check_rows):
    stimulus = witness_pins(witness)
    (work / "inputs.txt").write_text("".join(
        f"{v['rst']} {v['s_valid']} {v['s_data']:02x} {v['s_last']} {v['m_ready']} {v['h_ready']}\n"
        for v in stimulus))
    log = run(["vvp", "replay.vvp"], work).stdout
    output.write_text(log)
    lines = [line.split() for line in log.splitlines() if line.startswith(("PRE ", "POST "))]
    require(len(lines) == 2 * len(stimulus) and f"REPLAY_COMPLETE {len(stimulus)}\n" in log,
            "incomplete Icarus trace")
    rows = []
    for i, pins in enumerate(stimulus):
        row = {"cycle": i, "inputs": pins}
        for j, phase in enumerate(("PRE", "POST")):
            values = lines[2 * i + j]
            require(values[:2] == [phase, str(i)], "physical replay clock alignment changed")
            decoded = {k: int(v, 16) if re.fullmatch(r"[0-9a-fA-F]+", v) else -1
                       for k, v in zip((*PINS, *OUTPUTS), values[2:], strict=True)}
            require({k: decoded[k] for k in PINS} == pins, "physical pins differ from solver inputs")
            row[phase.lower()] = {k: decoded[k] for k in OUTPUTS}
        rows.append(row)
    checker = check_rows(rows, require_drained=False)
    return rows, checker


def coverage(rows):
    """Reconstruct the cover conditions solely from input/output pins on Icarus."""
    accepted = sent = 0
    completed = data_consumed = header_consumed = False
    flushed = False
    hits = {name: [] for name in COVERS}
    for i, row in enumerate(rows):
        pins, o = row["inputs"], row["pre"]
        m, h = o["m_valid"], o["h_valid"]
        if flushed and m == h == 0:
            hits["reset_with_pending_output"].append(i)
        flushed = bool(i and pins["rst"] and (m == 1 or h == 1))
        if pins["rst"]:
            accepted = sent = 0
            completed = data_consumed = header_consumed = False
            continue
        require(not pins["s_valid"] or (not completed and accepted < 12), "source exceeds single-frame scope")
        conditions = {
            "retained_byte": m == 1 and not data_consumed and sent < min(accepted, 8) and o["m_data"] > 0,
            "pad_presented": m == 1 and not data_consumed and completed and accepted <= sent < 4,
            "long_header": h == 1 and completed and not header_consumed and accepted > 8,
            "header_only_transfer": m == 1 and not pins["m_ready"] and h == 1 and pins["h_ready"],
            "data_only_transfer": m == 1 and pins["m_ready"] and h == 1 and not pins["h_ready"],
        }
        for name, reached in conditions.items():
            if reached:
                hits[name].append(i)
        if pins["s_valid"] and o["s_ready"] == 1:
            accepted += 1
            completed = bool(pins["s_last"])
        if m == 1 and pins["m_ready"]:
            if o["m_last"] == 1:
                data_consumed = True
            else:
                sent += 1
        if h == 1 and pins["h_ready"]:
            header_consumed = True
    return hits


def covers(work, out, check_rows):
    cmd = ["yosys-smtbmc", "-s", "z3", "--noprogress", "--timeout", "30", "-t", str(STEPS),
           "-c", "--dump-yw", "cover-%.yw", "txn.smt2"]
    log = run(cmd, work).stdout
    (out / "covers.log").write_text(log)
    require(log.rstrip().endswith("Status: PASSED"), "cover search incomplete")
    goals, pending = {}, {}
    for line in log.splitlines():
        goal = re.search(r"Reached cover statement in step (\d+) at frame_txn: (\w+)$", line)
        if goal:
            pending[goal[2]] = int(goal[1])
        saved = re.search(r"Writing trace to Yosys witness file: (cover-\d+\.yw)$", line)
        if saved:
            require(bool(pending), "missing cover name")
            witness = work / saved[1]
            shutil.copyfile(witness, out / saved[1])
            rows, checker = replay(witness, work, out / (witness.stem + ".icarus.log"), check_rows)
            require(checker["verdict"] == "PASS", f"cover replay failed frozen transaction checker: {checker}")
            hits = coverage(rows)
            for name, step in pending.items():
                require(step in hits[name] and name not in goals, f"cover {name} did not replay at {step}")
                goals[name] = {"step": step, "witness": saved[1], "cycles": len(rows), "checker": checker["verdict"]}
            pending.clear()
    require(set(goals) == set(COVERS) and not pending, "missing cover witness")
    return goals


def control(work, out, original, check_rows):
    cmd = ["yosys-smtbmc", "-s", "z3", "--noprogress", "--timeout", "30", "-t", str(STEPS),
           "--dump-yw", "counterexample.yw", "txn.smt2"]
    result = run(cmd, work, check=False)
    (out / "bmc.log").write_text(result.stdout)
    require(result.returncode == 1 and result.stdout.rstrip().endswith("Status: FAILED"),
            f"expected a finite control counterexample: {result.stdout[-600:]}")
    failed = re.findall(r"Assert failed in frame_txn: (\w+)$", result.stdout, re.M)
    step = int(re.findall(r"Checking assertions in step (\d+)", result.stdout)[-1])
    require(bool(failed) and set(failed) <= set(PROPERTIES), "missing failing property labels")
    w = out / "counterexample.yw"
    shutil.copyfile(work / w.name, w)
    rows, changed = replay(w, work, out / "counterexample-control.icarus.log", check_rows)
    _, clean = replay(w, original, out / "counterexample-original.icarus.log", check_rows)
    require(changed["verdict"] == "FAIL" and clean["verdict"] == "PASS", "physical differential failed")
    require(len(rows) == step + 1, "counterexample length differs from solver step")
    # The frozen checker reports specific header field names inside its status_payload
    # category. A reset post-edge obligation is sampled at PRE on the next formal tick.
    categories = {"data_entitlement": ("data_premature", "data_spurious"), "data_payload": ("data_payload",),
                  "data_last": ("data_last",), "header_entitlement": ("status_premature_or_spurious",),
                  "header_original": ("status_payload",), "header_adjusted": ("status_payload",),
                  "header_flags": ("status_payload",), "reset_clear": ("reset_clear",)}
    fields = {"header_original": ("h_original_length",), "header_adjusted": ("h_length",),
              "header_flags": ("h_pad", "h_truncate")}
    for label in failed:
        cycle, phase = (step - 1, "post") if label == "reset_clear" else (step, "pre")
        require(any(f["category"] in categories[label] and (f["cycle"], f["phase"]) == (cycle, phase)
                    and (label not in fields or any(name in f["detail"] for name in fields[label]))
                    for f in changed["failures"]), f"{label}: native failure absent at formal sample")
    return {"status": "COUNTEREXAMPLE", "step": step, "properties": failed,
            "same_inputs_original_checker": clean, "same_inputs_control_checker": changed}


def experiment(fixture, out):
    require(not out.exists(), f"output already exists: {out}")
    out.mkdir(parents=True)
    checker_sha = sha(check_file(fixture, CHECKER))
    check_rows = runpy.run_path(str(fixture / CHECKER))["check_rows"]
    summary = {"upstream_commit": MAPPING["commit"], "states": STEPS, "properties": list(PROPERTIES),
               "assumptions": ["initial reset", "s_valid low during reset", "source stable through an input stall "
                               "when reset stays low", "one input frame per reset epoch and at most 12 accepted bytes"],
               "data_witness": "universal three-bit retained byte index; input data and both sink ready pins symbolic",
               "reset_sampling": "state after a synchronous reset edge is observed at the following PRE",
               "drain": "outside the bounded safety harness; no final sample or fairness assumption",
               "assets_sha256": {p.name: sha(p.read_bytes()) for p in ASSETS.glob("*.sv")},
               "physical_checker_sha256": checker_sha, "designs": {}}
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        for design in ("original", *CONTROLS):
            work, case = root / design, out / design
            front, hashes = build(work, fixture, design, case)
            row = {"source_sha256": hashes}
            summary["designs"][design] = row
            if design == "original":
                sat = (front + "chformal -cover -remove; memory_map; opt; " +
                       f"sat -set-assumes -seq {STEPS} -prove-asserts -timeout 90 -dump_vcd original-fail.vcd")
                result = run(["yosys", "-Q", "-T", "-p", sat], work)
                (case / "safety.log.gz").write_bytes(gzip.compress(result.stdout.encode(), mtime=0))
                if (work / "original-fail.vcd").exists():
                    shutil.copyfile(work / "original-fail.vcd", case / "original-fail.vcd")
                row["status"] = ("PASSED" if "SAT proof finished - no model found: SUCCESS!" in result.stdout
                                 else "COUNTEREXAMPLE" if "SAT proof finished - model found: FAIL!" in result.stdout
                                 else "INCONCLUSIVE")
                row["covers"] = covers(work, case, check_rows)
            else:
                row.update(control(work, case, root / "original", check_rows))
        summary["tools"] = {tool: run([tool, arg], root).stdout.splitlines()[0] for tool, arg in (
            ("yosys", "-V"), ("z3", "--version"), ("iverilog", "-V"))}
    save(out / "summary.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="fresh evidence directory")
    args = parser.parse_args()
    report = experiment(args.fixture.resolve(), args.output.resolve())
    for key, result in report["designs"].items():
        print(key, result["status"], result.get("properties", ""))
    raise SystemExit(0 if report["designs"]["original"]["status"] == "PASSED" else 1)
