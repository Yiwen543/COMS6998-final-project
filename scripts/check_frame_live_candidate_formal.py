#!/usr/bin/env python3
"""Post-hoc bounded RTL check of the actual verified replies in the live frame experiment."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from audit_egg_fifo_live import read_archive, require
from egg_frame_formal import ASSETS, COVERS, PROPERTIES, ROOT, SOURCES, STEPS


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def render_candidate(text):
    """Independently parse sampled signal expressions and emit unsigned SystemVerilog."""
    require(isinstance(text, str) and 0 < len(text) <= 2400, "invalid monitor text")
    tokens = iter(re.findall(r"\(|\)|[^\s()]+", text))
    widths = {"m_data": 8, "s_data": 8, "h_length": 16, "h_original_length": 16}
    flags = {"rst", "s_valid", "s_ready", "s_last", "m_valid", "m_ready", "m_last",
             "h_valid", "h_ready", "h_pad", "h_truncate"}
    comparisons = {"eq": "==", "ne": "!=", "ult": "<", "ugt": ">", "uge": ">=", "ule": "<="}

    def read():
        token = next(tokens, None)
        require(token is not None, "incomplete expression")
        if token != "(":
            if token in ("true", "false"):
                return "bool", "1'b1" if token == "true" else "1'b0"
            if re.fullmatch("[0-9]+", token):
                return "literal", int(token)
            pin = token.removeprefix("prev_")
            if pin in widths:
                return widths[pin], token
            require(token == "have_prev" or pin in flags, f"unknown sampled pin: {token}")
            return "bool", token
        op = next(tokens, None)
        left_type, left = read()
        if op == "not":
            require(left_type == "bool" and next(tokens, None) == ")", "invalid not")
            return "bool", f"(~({left}))"
        right_type, right = read()
        require(next(tokens, None) == ")", "expected binary operator and closing parenthesis")
        if op in ("and", "or", "xor"):
            require(left_type == right_type == "bool", "wrong Boolean operand types")
            sign = {"and": "&", "or": "|", "xor": "^"}[op]
        else:
            require(op in comparisons, f"unknown comparison: {op}")
            sign = comparisons[op]
            if left_type == "literal":
                require(isinstance(right_type, int) and left < 2**right_type, "ill-sized left literal")
                left_type, left = right_type, f"{right_type}'d{left}"
            if right_type == "literal":
                require(isinstance(left_type, int) and right < 2**left_type, "ill-sized right literal")
                right_type, right = left_type, f"{left_type}'d{right}"
            require(left_type == right_type and (op in ("eq", "ne") or isinstance(left_type, int)),
                    "ill-typed comparison")
        return "bool", f"(({left}) {sign} ({right}))"

    sort, expr = read()
    require(sort == "bool" and next(tokens, None) is None, "non-Boolean result or trailing tokens")
    return expr


def submitted_candidates(read):
    config = json.loads(read("config.json"))
    require(config["mode"] == "live" and config["arms"] == ["raw", "ordinary", "egg"] and
            type(config["rounds_per_arm"]) is int and 1 <= config["rounds_per_arm"] <= 3,
            "unexpected live archive configuration")
    candidates, rejected = {}, {}
    for arm in config["arms"]:
        for index in range(1, config["rounds_per_arm"] + 1):
            label = f"{arm}/round-{index:02d}"
            reply = read(f"{label}/response.json")
            terms = json.loads(reply)["output"]["monitors"]
            score = json.loads(read(f"{label}/assessment.json"))
            try:
                require(isinstance(terms, dict) and set(terms) == set(PROPERTIES), "wrong property inventory")
                assertions = "".join(f"{name}: assert(!({render_candidate(terms[name])}));\n" for name in PROPERTIES)
            except (ValueError, RecursionError) as exc:
                require("candidate_error" in score, f"independent parser disagrees for {label}: {exc}")
                rejected[label] = {"recorded_error": score["candidate_error"], "response_sha256": sha(reply)}
                continue
            require(score.get("verified") is True, f"expected a verified parseable candidate: {label}")
            key = sha(json.dumps(terms, sort_keys=True).encode())
            case = candidates.setdefault(key, {"terms": terms, "assertions": assertions, "responses": {}})
            case["responses"][label] = sha(reply)
    require(candidates, "no submitted candidates to check")
    return candidates, rejected


def execute(command, work):
    proc = subprocess.run(command, cwd=work, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=180)
    require(proc.returncode == 0, f"{command} failed: {proc.stdout[-2000:]}")
    return proc.stdout


def verify(work, out, candidate):
    out.mkdir()
    assertions = candidate["assertions"]
    for folder in (work, out):
        (folder / "frame_assertions.svh").write_text(assertions)
    files = " ".join(Path(s).name for s in SOURCES)
    front = (f"read_verilog -formal -sv {files} frame_properties.sv; "
             "prep -top frame_properties -flatten; chformal -lower; ")
    emit = (front + "write_smt2 -wires all.smt2; chformal -assert -remove "
            "frame_properties/pad_flag frame_properties/truncate_flag frame_properties/clamped_length; "
            "write_smt2 -wires holds.smt2")
    execute(["yosys", "-Q", "-T", "-p", emit], work)
    for file, names in [("all", PROPERTIES), ("holds", PROPERTIES[:2])]:
        model = (work / f"{file}.smt2").read_text()
        require(set(re.findall(r"^; yosys-smt2-assert \d+ (\w+)", model, re.M)) == set(names) and
                set(re.findall(r"^; yosys-smt2-cover \d+ (\w+)", model, re.M)) == set(COVERS) and
                model.count("; yosys-smt2-assume ") == 4, "unexpected elaborated property inventory")
    sat = execute(["yosys", "-Q", "-T", "-p", front + "chformal -cover -remove; memory_map; opt; "
                   f"sat -set-assumes -seq {STEPS} -prove-asserts -timeout 120"], work)
    (out / "candidate-sat.log.gz").write_bytes(gzip.compress(sat.encode(), mtime=0))
    require("SAT proof finished - no model found: SUCCESS!" in sat, f"bounded SAT failed: {sat[-1500:]}")
    smt = ["yosys-smtbmc", "-s", "z3", "--noprogress", "--timeout", "30", "-t", "3"]
    base = execute([*smt, "holds.smt2"], work)
    induction = execute([*smt, "-i", "holds.smt2"], work)
    (out / "candidate-holds.log").write_text(base + "\n" + induction)
    require(base.rstrip().endswith("Status: PASSED") and "Temporal induction successful." in induction and
            induction.rstrip().endswith("Status: PASSED"), "candidate hold checks not established")
    return {"responses_sha256": candidate["responses"], "terms": candidate["terms"],
            "assertions_sha256": sha(assertions.encode()), "bounded_states": STEPS,
            "bounded_safety": "PASSED", "assertions": list(PROPERTIES),
            "induction_properties": list(PROPERTIES[:2]), "induction_base_states": 3,
            "temporal_induction": "PASSED"}


def run(archive, fixture, output):
    files = None if archive.is_dir() else read_archive(archive)
    read = (lambda name: (archive / name).read_bytes()) if files is None else files.__getitem__
    candidates, rejected = submitted_candidates(read)
    pinned = json.loads((ROOT / "scripts/m3_controller_replay_manifest.json").read_bytes())
    reference = json.loads((ROOT / "results/milestone3/frame-formal/summary.json").read_bytes())
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        out = work / "result"
        out.mkdir()
        hashes = {}
        for src in SOURCES:
            raw = (fixture / src).read_bytes()
            hashes[src] = sha(raw)
            require(hashes[src] == pinned["sha256"][src] == reference["source_sha256"][src],
                    f"frame fixture differs: {src}")
            (work / Path(src).name).write_bytes(raw)
        harness = (ASSETS / "frame_properties.sv").read_bytes()
        require(sha(harness) == reference["harness_sha256"], "reference harness differs")
        (work / "frame_properties.sv").write_bytes(harness)
        results = {key: verify(work, out / key, c) for key, c in candidates.items()}
        summary = {"method": "Post-hoc full-wrapper check of unique, verified, submitted monitoring expressions",
                   "archive_summary_sha256": sha(read("summary.json")), "upstream_commit": pinned["commit"],
                   "source_sha256": hashes, "harness_sha256": sha(harness), "rejected_replies": rejected,
                   "unique_verified_candidates": len(results), "results": results,
                   "tools": {tool: execute([tool, flag], work).splitlines()[0]
                             for tool, flag in [("yosys", "-V"), ("z3", "--version")]},
                   "new_model_calls": 0, "new_physical_simulations": 0}
        (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        shutil.copytree(out, output)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True, help="live run directory or tar.gz")
    parser.add_argument("--fixture", type=Path, required=True, help="verified frame_task fixture directory")
    parser.add_argument("--output", type=Path, required=True, help="new results directory")
    args = parser.parse_args()
    report = run(args.archive, args.fixture, args.output)
    print("Verified distinct submitted candidates:", report["unique_verified_candidates"])
