#!/usr/bin/env python3
"""Recheck all published Controller proof edges after each single certificate withdrawal."""
import argparse
from collections import Counter, defaultdict, deque
from functools import cache
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

from benchmark_m3_controller import structural_keys
from m3_controller_certificates import verify_rules
from m3_proof_dependencies import ProofChecker, validate_proof_dependencies
from predicates import ROOT, parse


ARCHIVE = ROOT / "results/milestone3/engine/profile-2/reference.json"
INPUT_SHA = "00de8c887f9205c4cc79dbc235a3fc00c9793f27e8796fbea25f5093461c17a0"
ast = cache(parse)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def saturate(executable, mode, data):
    p = subprocess.run([executable, mode], input=data, capture_output=True, check=True, timeout=60)
    require(json.loads(p.stderr)["mode"] == mode, f"incorrect engine mode {mode}")
    graph = json.loads(p.stdout)
    require(graph["stop_reason"] == "Some(Saturated)", graph["stop_reason"])
    del graph["saturation_seconds"]
    return graph


def checked_saturation(payload, args):
    data = json.dumps(payload).encode()
    fresh = saturate(args.binary, "indexed", data)
    require(fresh == saturate(args.baseline_binary, "spanning", data),
            "indexed output differs from frozen v1")
    return fresh, validate_proof_dependencies(payload, fresh)


def connect(adjacency, a, b, label):
    adjacency[a].append((b, label, "forward"))
    adjacency[b].append((a, label, "reverse"))


def path_between(adjacency, source, destination):
    queue = deque([source])
    parent = {source: None}
    while queue:
        vertex = queue.popleft()
        if vertex == destination:
            path = []
            while parent[vertex] is not None:
                vertex, label, direction = parent[vertex]
                path.append([label, direction])
            return path[::-1]
        for other, label, direction in adjacency.get(vertex, ()):
            if other not in parent:
                parent[other] = (vertex, label, direction)
                queue.append(other)
    return None


def equation_graph(rules):
    adjacency = defaultdict(list)
    for r in rules:
        event = tuple(r["event_context"])
        connect(adjacency, (event, ast(r["left"])), (event, ast(r["right"])), r["name"])
    return adjacency


def target_context(target):
    return {key: target[key] for key in ("event_context", "original_event_context", "instance_scope")}


def claims_for(payload, graph):
    original = validate_proof_dependencies(payload, graph)
    targets = {t["id"]: t for t in payload["targets"]}
    require(len(targets) == 148 and original["checked_edges"] == 70, "unexpected frozen target/claim count")
    claims = []
    for i, edge in enumerate(original["edges"]):
        a, b = (targets[edge[key]] for key in ("left", "right"))
        claims.append({"claim": i, **edge, "left_context": target_context(a), "right_context": target_context(b)})
    return claims


def scenario(payload, args, original_graph, checker, claims, withdrawn):
    remaining = [r for r in payload["verified_rules"] if r["name"] != withdrawn]
    require(len(remaining) == 280, "withdrawal did not remove exactly one rule")
    allowed = {r["name"] for r in remaining}
    reduced = {**payload, "verified_rules": remaining}
    graph, evidence = checked_saturation(reduced, args)
    proof_adjacency = defaultdict(list)
    for i, edge in enumerate(evidence["edges"]):
        connect(proof_adjacency, edge["left"], edge["right"], i)
    roots = {t["id"]: t["eclass"] for t in graph["targets"]}
    targets = checker.by_id
    ordinary = equation_graph(remaining)
    ordinary_keys = dict(zip(targets, structural_keys(reduced), strict=True))
    diagnostics, fresh_support = [], {}
    counts = Counter(kept=0, repaired=0, unresolved=0, stale=0, stale_equation_paths=0,
                     stale_structural_matches=0, all_equation_paths=0, all_structural_matches=0)
    for claim, old in zip(claims, original_graph["rewrite_explanations"], strict=True):
        a, b = claim["left"], claim["right"]
        stale = withdrawn in claim["ground_rules"]
        try:
            checker.check(old, allowed_ground_rules=allowed)
        except ValueError as exc:
            if not stale or f"withdrawn rule {withdrawn!r}" not in str(exc):
                raise
        else:
            require(not stale, f"withdrew a dependency but old proof accepted: {a},{b}")
        event = tuple(targets[a]["event_context"])
        require(event == tuple(targets[b]["event_context"]), "cross-event published claim")
        ordinary_path = path_between(ordinary, (event, ast(targets[a]["compact"])),
                                     (event, ast(targets[b]["compact"])))
        structural_match = ordinary_keys[a] == ordinary_keys[b]
        proof_path = path_between(proof_adjacency, a, b)
        supported = proof_path is not None
        require(supported == (roots[a] == roots[b]), f"missing or invalid fresh proof path: {a},{b}")
        require(stale or supported, f"recomputed engine lost an independently checked old proof: {a},{b}")
        require(ordinary_path is None or supported, f"recomputed engine lost an input-equation path: {a},{b}")
        status = "kept" if not stale else ("repaired" if supported else "unresolved")
        counts[status] += 1
        counts["stale"] += int(stale)
        counts["all_equation_paths"] += int(ordinary_path is not None)
        counts["all_structural_matches"] += int(structural_match)
        if stale:
            counts["stale_equation_paths"] += int(ordinary_path is not None)
            counts["stale_structural_matches"] += int(structural_match)
        record = {"claim": claim["claim"], "status": status, "fresh_supported": supported,
                  "equation_path": ordinary_path, "structural_match": structural_match}
        if stale and supported:
            record["repair_path"] = proof_path
            for index, _ in proof_path:
                fresh_support[index] = graph["rewrite_explanations"][index]
        diagnostics.append(record)
    require(counts["stale"] + counts["kept"] == 70 and
            counts["stale"] == counts["repaired"] + counts["unresolved"], "incomplete withdrawal")
    return {"withdrawn": withdrawn, **counts, "fresh_edges": evidence["checked_edges"],
            "fresh_steps": evidence["checked_steps"], "fresh_graph_sha256": digest(graph)}, diagnostics, fresh_support


def audit_unresolved(claims, indices, args):
    # Independent final grading only. These answers are never added back as rewrite rules.
    selected = [claims[i] for i in sorted(indices)]
    if not selected:
        return []
    archive = (args.screen_dir / "pairs.smt2").read_text()
    preamble, _ = archive.split("(push)\n", 1)
    queries = [f"(push)\n(assert (xor {c['left']} {c['right']}))\n(check-sat)\n(pop)\n"
               for c in selected]
    result = subprocess.run([args.z3, "-in", "-smt2"], input=preamble + "".join(queries), text=True,
                            capture_output=True, check=True, timeout=120)
    statuses = result.stdout.splitlines()
    require(len(statuses) == len(selected) and all(s == "unsat" for s in statuses),
            f"unchanged Controller oracle failed to confirm old targets: {statuses}")
    return [{"claim": c["claim"], "left": c["left"], "right": c["right"], "xor": status}
            for c, status in zip(selected, statuses, strict=True)]


def run(args):
    data = (args.screen_dir / "egg-input.json").read_bytes()
    require(hashlib.sha256(data).hexdigest() == INPUT_SHA, "wrong Controller archive")
    payload = json.loads(data)
    certificates = verify_rules(args.screen_dir, args.z3)
    original_graph, _ = checked_saturation(payload, args)
    archived = json.loads(ARCHIVE.read_text())
    del archived["saturation_seconds"]
    require(original_graph == archived, "full proof graph differs from published Controller result")
    checker = ProofChecker(payload)
    claims = claims_for(payload, original_graph)
    names = [r["name"] for r in payload["verified_rules"]]
    require(len(names) == len(set(names)) == len(certificates["results"]) == 281, "rule inventory drift")
    require(set(names) == set(certificates["results"]), "unqualified rule name")
    save(args.output / "claims.json", claims)
    totals, scenario_counts = Counter(), Counter()
    distinct = defaultdict(set)
    example = None
    with (args.output / "scenarios.jsonl").open("x") as rows, gzip.GzipFile(
            args.output / "claims-by-withdrawal.jsonl.gz", "xb", mtime=0) as detail:
        for name in names:
            row, diagnostics, support = scenario(payload, args, original_graph, checker, claims, name)
            rows.write(json.dumps(row) + "\n")
            detail_row = {"withdrawn": name, "claims": diagnostics, "repair_edges": support}
            detail.write((json.dumps(detail_row, separators=(",", ":")) + "\n").encode())
            for key in ("stale", "kept", "repaired", "unresolved", "stale_equation_paths", "stale_structural_matches",
                        "all_equation_paths", "all_structural_matches", "fresh_edges", "fresh_steps"):
                totals[key] += row[key]
            for key in ("stale", "repaired", "unresolved"):
                scenario_counts[key] += int(row[key] > 0)
            for d in diagnostics:
                distinct[d["status"]].add(d["claim"])
                if d["status"] != "repaired":
                    continue
                # A prespecified illustrative preference; all records are published.
                rank = (d["equation_path"] is None, len(d["repair_path"]) > 1)
                if example is None or rank > example[0]:
                    i = d["claim"]
                    example = rank, {"withdrawn": name, "published_claim": claims[i], "old_proof": original_graph["rewrite_explanations"][i],
                                     **d, "repair_edges": {j: support[j] for j, _ in d["repair_path"]}}
    if example is not None:
        save(args.output / "repair-example.json", example[1])
    direct = audit_unresolved(claims, distinct["unresolved"], args)
    save(args.output / "unresolved-qfbv.json", direct)
    result = {"complete": True, "unresolved_original_qfbv_unsat": len(direct), "scenarios": len(names), "claim_scenarios": len(names) * len(claims),
              "source_sha256": INPUT_SHA, "indexed_sha256": hashlib.sha256(args.binary.read_bytes()).hexdigest(),
              "v1_sha256": hashlib.sha256(args.baseline_binary.read_bytes()).hexdigest(),
              "certificate_files_sha256": certificates["sha256"], "z3": certificates["z3"],
              "full_proof_graph_sha256": digest(original_graph), "original_proofs": len(claims),
              "original_distinct_ground_dependencies": len({n for c in claims for n in c["ground_rules"]}),
              "cross_instance_claims": sum(c["left_context"]["instance_scope"] != c["right_context"]["instance_scope"] for c in claims),
              "cross_original_event_claims": sum(c["left_context"]["original_event_context"] != c["right_context"]["original_event_context"] for c in claims),
              "totals": dict(totals), "scenarios_with": dict(scenario_counts),
              "distinct_claims_by_status": {s: len(ids) for s, ids in distinct.items()}}
    save(args.output / "summary.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screen-dir", required=True, type=Path, help="pinned typed-v5/screen with SMT and query order")
    parser.add_argument("--binary", required=True, type=Path, help="indexed guard_proofs_fast")
    parser.add_argument("--baseline-binary", required=True, type=Path, help="pristine v1 guard_proofs_fast")
    parser.add_argument("--output", required=True, type=Path, help="fresh results directory")
    parser.add_argument("--z3", default="z3")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    try:
        run(args)
    except Exception as exc:
        save(args.output / "failure.json", {"error": str(exc)})
        raise
