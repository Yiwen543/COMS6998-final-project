#!/usr/bin/env python3
"""Measure six verification arms on the pinned arbiter, including two real RTL replays per arm."""
import argparse
import hashlib
import json
import platform
import statistics
import subprocess
import time
from pathlib import Path

from coverage import DUT_SOURCE, join, load, summary
from m3_guard_inputs import generate
from predicates import DUT, ROOT, _atom_tables, extract, witness, witness_fast
from run_step1 import result, run, write_json


ARMS = ("raw-scalar", "spanning-scalar", "indexed-scalar", "raw-fast", "spanning-fast", "indexed-fast")
TB = Path("examples/arbiter/verif/tb_fixed_priority_arbiter.sv")
TOP = "tb_fixed_priority_arbiter"
REFERENCE = ROOT / "results/step1"
PROBES = [(0, 255, 0), (0, 128, 3), (1, 255, 255), (0, 0, 0)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def source_payload(targets):
    forms = []
    for target in targets:
        for name, key in [("source", "compact"), ("alternate", "expanded")]:
            forms.append({
                "id": f"{target['id']}/{name}", "compact": target[key], "source_target": target["id"],
                "source": target["source"], "line": target["line"],
                "event_context": {k: target[k] for k in ("event", "reset_context", "width", "logic")},
            })
    return {"targets": forms, "verified_rules": []}


def normalize(targets, mode, binary, certified):
    if mode == "raw":
        return {"targets": [{"id": t["id"], "representative": t["compact"]} for t in targets]}, None, None
    payload = certified if certified is not None else source_payload(targets)
    source = {t["id"]: t["compact"] for t in targets}
    inputs = payload["targets"]
    for form in inputs:
        if form["id"].endswith("/source"):
            require(form["compact"] == source[form["source_target"]], "certificate/source mismatch")
    p = subprocess.run([binary, mode], input=json.dumps(payload), text=True, capture_output=True,
                       check=True, timeout=60)
    timing = json.loads(p.stderr)
    require(isinstance(timing, dict) and timing.get("mode") == mode,
            f"guard engine did not report requested mode {mode!r}: {p.stderr.strip()}")
    graph = json.loads(p.stdout)
    require(graph["stop_reason"] == "Some(Saturated)", f"{mode} stopped at {graph['stop_reason']}")
    require(graph["ground_rule_count"] == len(payload["verified_rules"]), "rule count changed")
    require([t["id"] for t in graph["targets"]] == [f["id"] for f in inputs], "lost or reordered forms")
    roots = {t["id"]: t for t in graph["targets"]}
    normalized, classes, expected_edges = [], set(), set()
    for target_id in source:
        a, b = (roots[f"{target_id}/{name}"] for name in ("source", "alternate"))
        require(a["eclass"] == b["eclass"] and a["representative"] == b["representative"],
                f"{target_id} forms did not normalize together")
        require(a["eclass"] not in classes, f"{target_id} merged with a distinct priority path")
        classes.add(a["eclass"])
        normalized.append({"id": target_id, "representative": a["representative"]})
        if a["eclass_before"] != b["eclass_before"]:
            expected_edges.add(frozenset((a["id"], b["id"])))
    evidence = graph["rewrite_explanations"]
    require(all(e["explanation"].strip() for e in evidence), "empty egg explanation")
    require(len(evidence) == len(expected_edges) and
            {frozenset((e["left"], e["right"])) for e in evidence} == expected_edges,
            "incomplete or unexpected proof edges")
    return {"targets": normalized}, graph, timing


def replay(simulator, folder, name, mode):
    flags = ["+VECTORS=vectors.txt"] if mode == 1 else []
    # Relative filenames also avoid truncation by the fixed-size SV plusarg buffer.
    command = [simulator, f"+MODE={mode}", "+COLLECT", f"+verilator+coverage+file+{name}.dat", *flags]
    p = subprocess.run(command, cwd=folder, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=60)
    (folder / f"{name}.log").write_text(p.stdout)
    p.check_returncode()
    return load(folder / f"{name}.dat"), p.stdout


def observation(points, log):
    return {"checker": result(log), "events": [line for line in log.splitlines()
            if line.startswith(("FUNCTION_FAIL ", "TIMING_FAIL ", "RESULT "))],
            "points": sorted(points, key=lambda point: json.dumps(point, sort_keys=True))}


def trial(arm, binary, simulator, folder, certified):
    mode, policy = arm.split("-")
    search = witness_fast if policy == "fast" else witness
    if policy == "fast":
        _atom_tables.cache_clear()  # Charge lazy truth table construction to every fast trial.
    start = time.perf_counter()
    targets = extract()
    after_extract = time.perf_counter()
    initial, init_log = replay(simulator, folder, "initial", 0)
    after_initial = time.perf_counter()
    normalized, graph, engine_timing = normalize(targets, mode, binary, certified)
    feedback = join(targets, normalized, initial)
    after_normalize = time.perf_counter()
    witnesses, vectors = {}, []
    for row in feedback:
        if row["uncovered"]:
            vector = search(row["representative"])
            require(vector is not None, f"uncovered target {row['id']} has no legal witness")
            witnesses[row["id"]] = list(vector)
            if vector not in vectors:
                vectors.append(vector)
    vectors.extend(PROBES)
    vector_text = "".join(f"{rst} {req:02x} {over:02x}\n" for rst, req, over in vectors)
    (folder / "vectors.txt").write_text(vector_text)
    after_witness = time.perf_counter()
    refined, refined_log = replay(simulator, folder, "refined", 1)
    require(all(f["hits"] > 0 for f in join(targets, normalized, refined)), "unhit refined target")
    quality = {"initial": observation(initial, init_log), "refined": observation(refined, refined_log),
               "witnesses": witnesses, "vector_text": vector_text}
    end = time.perf_counter()
    timing = {"wall_seconds": end - start, "frontend_seconds": after_extract - start,
              "initial_seconds": after_initial - after_extract, "normalization_join_seconds": after_normalize - after_initial,
              "witness_vectors_seconds": after_witness - after_normalize, "refined_grading_seconds": end - after_witness}
    return timing, quality, graph, engine_timing


def raw_dut_hits(path):
    """Compare every Verilator identity field, including page, independent of row order."""
    counters = {}
    for row in path.read_text().splitlines()[1:]:
        if not row.strip():
            continue
        metadata, hits = row.rsplit("' ", 1)
        fields = dict(part.split("\x02", 1) for part in metadata.split("\x01")[1:])
        source = fields.get("f", "").replace("\\", "/")
        if source != DUT_SOURCE and not source.endswith("/" + DUT_SOURCE):
            continue
        if not fields.get("h", "").endswith(".dut"):
            continue
        fields["f"] = DUT_SOURCE
        key = tuple(sorted(fields.items()))
        require(key not in counters, f"{path}: duplicate DUT counter {key!r}")
        counters[key] = int(hits)
    require(counters, f"{path}: missing DUT counters")
    return counters


def check_archived_replay(path, live, archive):
    require(live["events"] == archive["events"], f"{path}: historical checker events changed")
    require(live["points"] == archive["points"] and raw_dut_hits(path) == archive["raw_dut_hits"],
            f"{path}: historical DUT counter identity or hit count changed")


def archived_quality(directory):
    feedback = json.loads((directory / "feedback.json").read_text())
    witnesses = {r["id"]: [r["suggested_stimulus"][k] for k in ("reset", "req", "priority_override")]
                 for r in feedback if r["uncovered"]}
    quality = {"vector_text": (directory / "targeted-vectors.txt").read_text(), "witnesses": witnesses}
    for name in ("initial", "refined"):
        path = directory / f"{name}.dat"
        quality[name] = observation(load(path), (directory / f"{name}.log").read_text())
        quality[name]["raw_dut_hits"] = raw_dut_hits(path)
    return quality


def benchmark(args):
    out = args.output.resolve()
    versions = {"verilator": subprocess.check_output(["verilator", "--version"], text=True).strip(),
                "python": platform.python_version(), "platform": platform.platform()}
    build = out / "verilator-build"
    compile_seconds, _ = run(["verilator", "--cc", "--exe", "--build", "--timing", "--assert",
                              "--coverage-line", "--coverage-toggle", "--coverage-expr", "--top-module", TOP,
                              "--Mdir", build, "-j", "2", DUT.relative_to(ROOT), TB, ROOT / "scripts/sim_main.cpp"],
                             out / "compile.log")
    simulator = build / f"V{TOP}"
    baseline = (args.baseline_binary or args.binary).resolve()
    candidate = args.binary.resolve()
    certified, cert_seconds = None, 0.0
    if args.profile == "certified":
        start = time.perf_counter()
        generate(out / "certification", args.z3)
        certified = json.loads((out / "certification/ground.json").read_bytes())
        cert_seconds = time.perf_counter() - start
    frozen = certified if certified is not None else source_payload(extract())
    (out / "guard-input.json").write_text(json.dumps(frozen))
    setup = {"versions": versions, "dut_compile_seconds": compile_seconds, "certification_seconds": cert_seconds,
             "sha256": {"rtl": file_hash(DUT), "testbench": file_hash(ROOT / TB), "runner": file_hash(ROOT / "scripts/sim_main.cpp"),
                        "simulator": file_hash(simulator), "spanning_binary": file_hash(baseline),
                        "indexed_binary": file_hash(candidate)}}
    setup["sha256"]["guard_input"] = file_hash(out / "guard-input.json")
    write_json(out / "setup.json", setup)
    archive = archived_quality(args.reference_dir)
    rows, quality_reference, proof_reference = [], None, None
    for repeat in range(args.repeats):
        arms = ARMS[repeat % len(ARMS):] + ARMS[:repeat % len(ARMS)]
        for position, arm in enumerate(arms):
            folder = out / f"r{repeat:02d}-{arm}"
            folder.mkdir()
            binary = baseline if arm.startswith("spanning-") else candidate
            timing, quality, graph, engine_timing = trial(arm, binary, simulator, folder, certified)
            if quality_reference is None:
                quality_reference = quality
                write_json(out / "quality.json", quality)
            require(quality == quality_reference, f"{folder.name}: differs from live raw-scalar reference")
            require(quality["vector_text"] == archive["vector_text"] and quality["witnesses"] == archive["witnesses"],
                    f"{folder.name}: historical witnesses or vectors changed")
            for name in ("initial", "refined"):
                check_archived_replay(folder / f"{name}.dat", quality[name], archive[name])
            proof_hash = None
            if graph is not None:
                # Compare every field including explanation endpoints and full proof text, removing only the timer.
                del graph["saturation_seconds"]
                if proof_reference is None:
                    proof_reference = graph
                    write_json(out / "proofs.json", graph)
                require(graph == proof_reference, f"{folder.name}: differs from spanning proof reference")
                proof_hash = digest(graph)
            row = {"repeat": repeat, "position": position, "arm": arm, **timing,
                   "engine_timing": engine_timing, "quality_sha256": digest(quality), "proof_sha256": proof_hash}
            rows.append(row)
            with (out / "trials.jsonl").open("a") as f:
                f.write(json.dumps(row) + "\n")
    medians = {a: {k: statistics.median(r[k] for r in rows if r["arm"] == a)
                   for k in rows[0] if k.endswith("_seconds")} for a in ARMS}
    archived_points = {name: quality_reference[name]["points"] == archive[name]["points"]
                       for name in ("initial", "refined")}
    summary_record = {
        "profile": args.profile, "repeats": args.repeats, "completed_trials": len(rows),
        "physical_replays": 2 * len(rows), "checked_edges": len(rows) * sum(
            quality_reference[k]["checker"]["checks"] for k in ("initial", "refined")),
        "medians_seconds": medians, "setup": setup, "matched_live_raw_quality": True,
        "archived_full_counter_parity": archived_points, "quality_sha256": digest(quality_reference),
        "proof_sha256": digest(proof_reference),
        "replay": {k: {"checker": quality_reference[k]["checker"], "coverage": summary(quality_reference[k]["points"])}
                   for k in ("initial", "refined")},
    }
    write_json(out / "summary.json", summary_record)
    print(f"{len(rows)} matched trials, {2 * len(rows)} Verilator replays. Results in {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True, help="release guard_proofs_fast with indexed mode")
    parser.add_argument("--baseline-binary", type=Path, help="separate fast-v1 binary for spanning")
    parser.add_argument("--output", type=Path, required=True, help="fresh directory for build, raw trials and summary")
    parser.add_argument("--profile", choices=("source", "certified"), default="source")
    parser.add_argument("--reference-dir", type=Path, default=REFERENCE,
                        help="archived Step 1 checker, witness and counter files")
    parser.add_argument("--z3", default="z3", help="Z3 executable for certifying the optional ground rules")
    parser.add_argument("--repeats", type=int, default=6)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    args.output.mkdir(parents=True, exist_ok=False)
    try:
        benchmark(args)
    except Exception as error:
        write_json(args.output / "failure.json", {"error": repr(error)})
        raise
