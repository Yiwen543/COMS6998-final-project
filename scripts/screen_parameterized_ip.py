#!/usr/bin/env python3
"""Static candidate screen with explicit elaboration parameters; no LLM outcomes."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import time
from collections import defaultdict
from pathlib import Path

from preflight_heldout import ENGINE, ROOT, verify_rewrites, z3_equivalent
from semantic_candidate_scan import _z3_priority_proof
from typed_predicates import RTLIL


def extract_configured(sources, top, parameters, output):
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z_0-9]*", top):
        raise ValueError("Unsupported top identifier")
    if any(not re.fullmatch(r"[a-zA-Z_][a-zA-Z_0-9]*", k) or type(v) is not int for k, v in parameters.items()):
        raise ValueError("Only named integer parameters are supported")
    output.mkdir(parents=True, exist_ok=True)
    paths = [p.resolve() for p in sources]
    il = output.resolve() / "preproc.il"
    opts = " ".join(f"-chparam {k} {v}" for k, v in sorted(parameters.items()))
    script = (f'read_verilog -sv {" ".join(shlex.quote(str(p)) for p in paths)}; '
              f'hierarchy -check -top {top} {opts}; flatten; write_rtlil {shlex.quote(str(il))}')
    (output / "extract.ys").write_text(script + "\n")
    command = subprocess.run(["yosys", "-Q", "-T", "-p", script], text=True, capture_output=True, timeout=90)
    (output / "extract.log").write_text(command.stdout + command.stderr)
    if command.returncode:
        return None, {"status": "frontend_blocked", "returncode": command.returncode,
                      "detail": command.stderr[-2000:]}
    text = il.read_text()
    # This also catches a silently ignored/misspelled override.
    block = re.search(r"^module \\" + re.escape(top) + r"\n(.*?)(?=^module |\Z)", text, re.M | re.S)
    if not block:
        raise AssertionError("Elaborated top not found")
    observed = {}
    for name, expected in parameters.items():
        match = re.search(r"^  parameter \\" + re.escape(name) + r" (\d+)\s*$", block[1], re.M)
        if match is None or int(match[1]) != expected:
            raise AssertionError(f"Parameter override not verified: {name}")
        observed[name] = int(match[1])
    extraction = RTLIL(text, paths).extract()
    return extraction, {"status": "elaborated", "verified_parameters": observed,
                        "command": script, "rtlil_sha256": hashlib.sha256(text.encode()).hexdigest()}


def normalize(extraction):
    rewrites = verify_rewrites()
    priority = [_z3_priority_proof(x) for x in extraction["priority_simplifications"]]
    payload = [{"id": x["id"], "compact": x["compact"], "expanded": x["compact"]}
               for x in extraction["targets"]]
    proc = subprocess.run([str(ENGINE)], input=json.dumps(payload), text=True,
                          capture_output=True, timeout=20, check=True)
    graph = json.loads(proc.stdout)
    roots = {x["id"]: x["eclass"] for x in graph["targets"]}
    buckets = defaultdict(list)
    for x in extraction["targets"]:
        buckets[(tuple(x["event_context"]), roots[x["id"]])].append(x)
    groups = []
    for (events, eclass), members in buckets.items():
        if len({(m["source"],m["line"],m["column"]) for m in members}) < 2:
            continue
        if not all(z3_equivalent(members[0]["compact"], m["compact"]) for m in members[1:]):
            raise AssertionError("Unproved egg merge")
        groups.append({"event_context": events, "eclass": eclass,
            "nontrivial": len({m["compact"] for m in members}) > 1,
            "z3_pair_checks": len(members)-1, "members": members})
    return {"groups": groups, "rewrite_checks": rewrites, "priority_checks": priority,
            "egg": graph, "proof_scope": "Boolean skeleton over typed atoms; two-state only"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    results = []
    for candidate in manifest["candidates"]:
        out = args.output / candidate["id"]
        sources = [ROOT / p for p in candidate["sources"]]
        for path, expected in candidate["sha256"].items():
            if hashlib.sha256((ROOT/path).read_bytes()).hexdigest() != expected:
                raise AssertionError(f"Pinned source changed: {path}")
        started = time.perf_counter()
        extraction, status = extract_configured(sources, candidate["top"], candidate["parameters"], out)
        record = {"candidate": candidate, "extraction_status": status,
                  "qualification": "not_qualified_pending_raw_source_mapping_checker_and_reachability"}
        if extraction is not None:
            record["extraction"] = extraction
            record["normalization"] = normalize(extraction)
        record["seconds"] = time.perf_counter() - started
        (out / "screen.json").write_text(json.dumps(record, indent=2)+"\n")
        groups = record.get("normalization", {}).get("groups", [])
        summary = {"id": candidate["id"], "status": status["status"],
                   "groups": len(groups), "nontrivial_groups": sum(g["nontrivial"] for g in groups),
                   "unsupported": len(extraction["unsupported"]) if extraction else None,
                   "qualification": record["qualification"]}
        results.append(summary)
        print(json.dumps(summary), flush=True)
    (args.output / "summary.json").write_text(json.dumps({"mode": "static_no_model_calls", "candidates": results}, indent=2)+"\n")


if __name__ == "__main__":
    main()
