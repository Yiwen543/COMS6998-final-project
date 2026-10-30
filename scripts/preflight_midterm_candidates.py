#!/usr/bin/env python3
"""Outcome-blind semantic/coverage preflight for two independent CVDP IPs.

The calibration stimuli establish reachability only. They are not a model seed,
not a checker, and never appear in experimental prompts.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path

from coverage import load, summary
from preflight_heldout import verify_rewrites, verify_typed_bitvectors, z3_equivalent
from typed_predicates import extract


ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "docs/midterm-candidate-lock.json").read_text())
ENGINE = ROOT / "egraph/target/debug/rtl-predicate-egraph"
OUT = ROOT / "results/midterm_candidate_preflight"
BUILDS = ROOT / "build/midterm_candidate_preflight"
SETUPS = {
    "heldout_codec64": {
        "top": "top_64b66b_codec", "tb": "tb_codec_preflight",
        "semantic_modules": ["decoder_data_control_64b66b", "encoder_control_64b66b", "encoder_data_64b66b"],
    },
    "heldout_linear_search": {
        "top": "linear_search_top", "tb": "tb_search_preflight",
        "semantic_modules": ["linear_search_ctrl", "linear_search_datapath"],
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tool_version(argv):
    proc = subprocess.run(argv, text=True, capture_output=True, check=True)
    return (proc.stdout or proc.stderr).splitlines()[0]


def run(argv, *, stdin=None, timeout=180, log=None):
    proc = subprocess.run([str(x) for x in argv], cwd=ROOT, input=stdin,
                          text=True, capture_output=True, timeout=timeout)
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(proc.stdout + proc.stderr)
    if proc.returncode:
        raise RuntimeError(f"{argv[0]} failed ({proc.returncode}): {proc.stderr[-1000:]}")
    return proc.stdout


def verify_files(candidate, folder):
    provenance = json.loads((folder / "provenance.json").read_text())
    if provenance["record_sha256"] != candidate["record_sha256"]:
        raise ValueError("Candidate provenance mismatch")
    sources = []
    for field, digest in candidate["fields"].items():
        name = Path(field).name
        path = folder / ("rtl" if field.startswith("harness/") else "docs") / name
        if sha(path) != digest:
            raise ValueError(f"Candidate file modified: {path}")
        if path.suffix in (".sv", ".v"):
            sources.append(path)
    return sorted(sources)


def semantic_groups(source, output):
    extraction = extract(source, source.stem)
    targets = extraction["targets"]
    payload = [{"id": t["id"], "compact": t["compact"], "expanded": t["compact"]}
               for t in targets]
    if not payload:
        return extraction, {"groups": [], "graph": None}
    graph = json.loads(run([ENGINE], stdin=json.dumps(payload), timeout=15))
    roots = {t["id"]: t["eclass"] for t in graph["targets"]}
    candidates = defaultdict(list)
    for target in targets:
        if target["kind"] == "explicit_case" and target["guard_depth"] >= 2:
            candidates[(tuple(target["event_context"]), roots[target["id"]])].append(target)
    groups = []
    for (events, eclass), members in candidates.items():
        if len({(m["line"], m["column"]) for m in members}) < 2:
            continue
        if not all(z3_equivalent(members[0]["compact"], m["compact"]) for m in members[1:]):
            raise AssertionError(f"Unproved egg merge in {source}")
        groups.append({"eclass_local": eclass, "event_context": list(events),
                       "reference_guard": members[0]["compact"],
                       "member_ids": [m["id"] for m in members],
                       "members": [{"line": m["line"], "column": m["column"],
                                    "case_value": m["case_value"],
                                    "source_mapping": m["source_mapping"],
                                    "guard_depth": m["guard_depth"]} for m in members],
                       "z3_pair_checks": len(members) - 1})
    output.write_text(json.dumps({"source": str(source.relative_to(ROOT)),
                                  "source_sha256": extraction["source_sha256"],
                                  "extraction": extraction, "egg": graph,
                                  "groups": groups}, indent=2) + "\n")
    return extraction, {"groups": groups, "graph": graph}


def coverage_for_sources(dat, sources):
    points = []
    for source in sources:
        points.extend(load(dat, str(source.relative_to(ROOT)), include_descendants=True))
    return points


def source_point(target, points):
    same_line = [p for p in points if p["source"] == str(Path(target["source"]).relative_to(ROOT))
                 and p["line"] == target["line"]]
    matches = [p for p in same_line if p["type"] == "line"]
    if not matches:
        # Verilator instruments some if/else-if source lines only as branch
        # outcomes. A true-path branch is a valid but distinct counter type.
        matches = [p for p in same_line if p["type"] == "branch" and p["outcome"] == "if"]
    if len(matches) != 1:
        return {"status": "unmapped_or_ambiguous", "matching_points": len(matches)}
    point = matches[0]
    return {"status": "mapped", "type": point["type"], "outcome": point["outcome"],
            "line": point["line"], "column": point["column"],
            "hierarchy": point["hierarchy"], "hits": point["hits"]}


def main():
    if not ENGINE.is_file():
        raise FileNotFoundError("Build the pinned egg engine with: cargo build --offline --manifest-path egraph/Cargo.toml")
    if sha(ROOT / ".cache" / LOCK["dataset_file"]) != LOCK["dataset_sha256"]:
        raise ValueError("Pinned CVDP dataset hash mismatch")
    OUT.mkdir(parents=True, exist_ok=True)
    BUILDS.mkdir(parents=True, exist_ok=True)
    evidence = {"status": "candidate preflight only; no specification checker or LLM outcome",
                "dataset_sha256": LOCK["dataset_sha256"],
                "tool_versions": {"verilator": tool_version(["verilator", "--version"]),
                                  "iverilog": tool_version(["iverilog", "-V"]),
                                  "yosys": tool_version(["yosys", "-V"]),
                                  "z3": tool_version(["z3", "--version"])},
                "implementation_sha256": {"extractor": sha(ROOT / "scripts/typed_predicates.py"),
                                          "egg_source": sha(ROOT / "egraph/src/main.rs"),
                                          "preflight": sha(Path(__file__))},
                "rewrite_validation": verify_rewrites(),
                "bitvector_validation": verify_typed_bitvectors(),
                "ips": []}
    for candidate in LOCK["candidates"]:
        slug = candidate["slug"]
        folder = ROOT / "examples" / slug
        setup = SETUPS[slug]
        sources = verify_files(candidate, folder)
        result_dir = OUT / slug
        result_dir.mkdir(parents=True, exist_ok=True)
        extracts = []
        group_rows = []
        for module in setup["semantic_modules"]:
            source = folder / "rtl" / f"{module}.sv"
            extraction, semantic = semantic_groups(source, result_dir / f"{module}-semantic.json")
            extracts.append(extraction)
            for group in semantic["groups"]:
                group_rows.append({"source": str(source.relative_to(ROOT)), **group})
        tb = next((folder / "verif").glob("tb_*_preflight.sv"))
        build = BUILDS / slug
        compile_cmd = ["verilator", "--binary", "--timing", "--coverage-line",
                       "--coverage-toggle", "--coverage-expr", "-Wno-fatal",
                       "-Wno-TIMESCALEMOD", "-Wno-WIDTHEXPAND",
                       "--top-module", setup["tb"], "--Mdir", build, "-j", "2",
                       *sources, tb]
        run(compile_cmd, timeout=240, log=result_dir / "compile.log")
        binary = build / f"V{setup['tb']}"
        seed = result_dir / "seed.dat"
        calibration = result_dir / "calibration.dat"
        seed_log = run([binary, f"+verilator+coverage+file+{seed}"], timeout=30,
                       log=result_dir / "seed.log")
        calib_log = run([binary, "+CALIBRATE", f"+verilator+coverage+file+{calibration}"],
                        timeout=30, log=result_dir / "calibration.log")
        if "PREFLIGHT_SEED_OK" not in seed_log or "PREFLIGHT_CALIBRATION_OK" not in calib_log:
            raise AssertionError("Preflight did not complete")
        seed_points = coverage_for_sources(seed, sources)
        calib_points = coverage_for_sources(calibration, sources)
        by_id = {t["id"]: t for extraction in extracts for t in extraction["targets"]}
        for group in group_rows:
            for member in group["members"]:
                target = next(t for t in (by_id[i] for i in group["member_ids"])
                              if t["line"] == member["line"] and t["column"] == member["column"])
                member["seed_coverage"] = source_point(target, seed_points)
                member["calibration_coverage"] = source_point(target, calib_points)
            group["qualifies_preflight"] = all(
                m["seed_coverage"]["status"] == "mapped" and
                m["seed_coverage"]["hits"] == 0 and
                m["calibration_coverage"]["status"] == "mapped" and
                m["calibration_coverage"]["hits"] > 0 for m in group["members"])
        ip = {"id": candidate["id"], "slug": slug, "categories": candidate["categories"],
              "spec_sha256": candidate["fields"]["context/docs/specification.md"],
              "source_sha256": {str(s.relative_to(ROOT)): sha(s) for s in sources},
              "testbench_sha256": sha(tb), "compile_command": [str(x) for x in compile_cmd],
              "seed_coverage": summary(seed_points), "calibration_coverage": summary(calib_points),
              "semantic_extraction": [{"module": Path(e["source"]).stem,
                                       "targets": len(e["targets"]),
                                       "unsupported": len(e["unsupported"])} for e in extracts],
              "groups": group_rows,
              "qualifying_group_count": sum(g["qualifies_preflight"] for g in group_rows)}
        if not ip["qualifying_group_count"]:
            raise AssertionError(f"No seed-uncovered, reachable, source-mapped group in {slug}")
        evidence["ips"].append(ip)
        print(f"{slug}: {len(group_rows)} groups, seed={ip['seed_coverage']}, calibration={ip['calibration_coverage']}")
    (OUT / "selection.json").write_text(json.dumps(evidence, indent=2) + "\n")


if __name__ == "__main__":
    main()
