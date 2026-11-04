#!/usr/bin/env python3
"""Outcome-blind, two-state egg/Z3 guard screen for one pinned RTL top.

No calibration vector, solver witness, or model response is an input here.
All generated evidence is intended for candidate selection, not C feedback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from collections import defaultdict
from pathlib import Path

from preflight_heldout import ENGINE, ROOT, z3_equivalent, verify_rewrites
from typed_predicates import extract


def map_true_counter(member: dict, points: list[dict]) -> dict:
    """Join an explicit true guard to exactly one original DUT source counter."""
    source = str(Path(member["source"]).resolve().relative_to(ROOT))
    same = [p for p in points if p["source"] == source and p["line"] == member["line"]]
    for counter_type, outcomes in (("line", ("if", "elsif", "case")),
                                   ("branch", ("if", "cond_then"))):
        candidates = [p for p in same if p["type"] == counter_type and p["outcome"] in outcomes]
        if len(candidates) == 1:
            return {"status": "mapped", "point": candidates[0]}
        if len(candidates) > 1:
            return {"status": "ambiguous", "reason": "multiple true-path counters on source line",
                    "candidates": candidates}
    return {"status": "unmapped", "reason": "no unique true-path original DUT counter",
            "candidates": same}


def _z3_priority_proof(item: dict) -> str:
    width = item["width"]
    if width < 1:
        raise ValueError("zero-width case")
    all_prior = sorted({value for arm in item["prior_cases"] for value in arm})
    # The frontend records exact decimal values for every prior arm. Parse
    # current source literals with the same function used by extraction.
    from typed_predicates import _literal
    current = sorted({_literal(raw)[1] for raw in item["case"].split()})
    def choice(values):
        return "(or " + " ".join(f"(= s (_ bv{value} {width}))" for value in values) + ")"
    smt = (f"(set-logic QF_BV)\n(declare-const s (_ BitVec {width}))\n"
           f"(assert (and {choice(all_prior)} {choice(current)}))\n(check-sat)\n")
    result = subprocess.run(["z3", "-in"], input=smt, text=True,
                            capture_output=True, timeout=10, check=True).stdout.strip()
    if result != "unsat":
        raise AssertionError(f"case-priority simplification not proven: {item} => {result}")
    return result


def scan(source: Path | list[Path], top: str, *, flatten: bool) -> dict:
    sources = [source.resolve()] if isinstance(source, Path) else [p.resolve() for p in source]
    started = time.perf_counter()
    proof = verify_rewrites()
    rewrite_seconds = time.perf_counter() - started
    started = time.perf_counter()
    extracted = extract(sources, top, flatten=flatten)
    frontend_seconds = time.perf_counter() - started
    started = time.perf_counter()
    priority_proofs = [_z3_priority_proof(item) for item in extracted["priority_simplifications"]]
    priority_seconds = time.perf_counter() - started
    payload = [{"id": row["id"], "compact": row["compact"], "expanded": row["compact"]}
               for row in extracted["targets"]]
    started = time.perf_counter()
    if payload:
        proc = subprocess.run([str(ENGINE)], input=json.dumps(payload), text=True,
                              capture_output=True, cwd=ROOT, timeout=20, check=True)
        graph = json.loads(proc.stdout)
    else:
        graph = {"targets": [], "eclasses": [], "iterations": 0, "stop_reason": "no_targets"}
    egg_seconds = time.perf_counter() - started
    if len(graph["targets"]) != len(payload):
        raise AssertionError("egg target count mismatch")
    roots = {row["id"]: row["eclass"] for row in graph["targets"]}
    representatives = {row["id"]: row["representative"] for row in graph["targets"]}
    class_nodes = {row["id"]: row["nodes"] for row in graph["eclasses"]}
    buckets = defaultdict(list)
    for row in extracted["targets"]:
        buckets[(tuple(row["event_context"]), roots[row["id"]])].append(row)
    started = time.perf_counter()
    groups = []
    for (events, eclass), members in buckets.items():
        if len({(m["source"], m["line"], m["column"]) for m in members}) < 2:
            continue
        reference = members[0]
        for member in members[1:]:
            if not z3_equivalent(reference["compact"], member["compact"]):
                raise AssertionError(f"egg merge failed independent Z3 check: {reference['id']} {member['id']}")
        groups.append({"eclass": eclass, "event_context": list(events),
                       "representative": representatives[reference["id"]],
                       "eclass_nodes": class_nodes[eclass],
                       "distinct_input_expressions": len({m["compact"] for m in members}),
                       "requires_egg_rewrite_to_merge": len({m["compact"] for m in members}) > 1,
                       "member_ids": [m["id"] for m in members],
                       "members": [{key: m[key] for key in ("id", "source", "line", "column",
                                                               "source_text", "compact", "guard_depth",
                                                               "case_value", "source_mapping", "event_context")}
                                   for m in members],
                       "independent_z3_checks": len(members)-1,
                       "status": "semantic_only_pending_raw_counter_and_reachability"})
    z3_pair_seconds = time.perf_counter() - started
    return {"schema": "semantic_candidate_scan_v1", "source": str(sources[0]),
            "source_sha256": hashlib.sha256(sources[0].read_bytes()).hexdigest(),
            "sources": extracted["sources"],
            "top": top, "flatten": flatten,
            "semantics": "binary/two-state; full process event context; original source locations separate",
            "rewrite_proofs": proof, "priority_proofs": priority_proofs,
            "alias_evidence": extracted["alias_evidence"],
            "unresolved_aliases": extracted["unresolved_aliases"],
            "priority_simplifications": extracted["priority_simplifications"],
            "unsupported": extracted["unsupported"], "atoms": extracted["atoms"],
            "targets": extracted["targets"], "groups": groups,
            "egg": {"engine": graph.get("engine"), "iterations": graph["iterations"],
                    "stop_reason": graph["stop_reason"],
                    "eclass_count": len(graph["eclasses"]),
                    "enode_count": sum(len(c["nodes"]) for c in graph["eclasses"]),
                    "timing_seconds": graph.get("timing_seconds")},
            "seconds": {"rewrite_z3": rewrite_seconds, "frontend_yosys_extract": frontend_seconds,
                        "priority_z3": priority_seconds, "egg_saturation_and_astsize": egg_seconds,
                        "pair_z3": z3_pair_seconds}}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("source", type=Path, nargs="+")
    cli.add_argument("--top", required=True)
    cli.add_argument("--flatten", action="store_true")
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    result = scan(args.source, args.top, flatten=args.flatten)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"groups": len(result["groups"]), "targets": len(result["targets"]),
                      "unsupported": len(result["unsupported"]),
                      "unresolved_aliases": len(result["unresolved_aliases"]),
                      "seconds": result["seconds"]}, indent=2))


if __name__ == "__main__":
    main()
