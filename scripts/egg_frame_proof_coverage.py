#!/usr/bin/env python3
"""Frozen proof-coverage experiment on typed frame monitors, with one egg process per pair/profile."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
from statistics import median
import subprocess
import time

import z3

from audit_egg_fifo_live import read_archive
from egg_frame_proof import SCOPE, _subst, review
from egg_frame_terms import REFERENCES, format_term, parse_term, z3_env, z3_term
from m3_proof_dependencies import BUILTINS, ProofChecker, validate_pattern_rules, validate_proof_dependencies
from predicates import ROOT, parse


RESULTS = ROOT / "results/milestone3"
TIMEOUT_MS = 5000
MERGED_STOP = 'Some(Other("TargetsMerged"))'


def require(test, why):
    if not test:
        raise ValueError(why)


def rule_profiles():
    base = [dict(name=k, left=a, right=b) for k, (a, b) in BUILTINS.items()]
    assoc = base + [dict(name=f"{op}-associate-right", left=f"({op} ({op} ?a ?b) ?c)",
                         right=f"({op} ?a ({op} ?b ?c))") for op in ("and", "or")]
    ac_dist = assoc + [dict(name=f"{op}-commute", left=f"({op} ?a ?b)", right=f"({op} ?b ?a)") for op in ("and", "or")]
    for op, other in (("and", "or"), ("or", "and")):
        ac_dist.append(dict(name=f"{op}-distribute", left=f"({op} ?a ({other} ?b ?c))",
                            right=f"({other} ({op} ?a ?b) ({op} ?a ?c))"))
    return {"base": base, "assoc": assoc, "ac_dist": ac_dist}


def _rewrite_one(tree, family):
    """Select the first applicable site in preorder, including the root."""
    if not isinstance(tree, tuple):
        return None
    op, *children = tree
    if op in ("and", "or"):
        a, b = children
        other = "or" if op == "and" else "and"
        if family == "reorder" and a != b:
            return (op, b, a)
        if family == "demorgan":
            return ("not", (other, ("not", a), ("not", b)))
        if family == "reassociate":
            if isinstance(a, tuple) and a[0] == op:
                return (op, a[1], (op, a[2], b))
            if isinstance(b, tuple) and b[0] == op:
                return (op, (op, a, b[1]), b[2])
        if family == "distribute":
            if isinstance(b, tuple) and b[0] == other:
                return (other, (op, a, b[1]), (op, a, b[2]))
            if isinstance(a, tuple) and a[0] == other:
                return (other, (op, a[1], b), (op, a[2], b))
    for i, child in enumerate(children):
        replacement = _rewrite_one(child, family)
        if replacement is not None:
            return (op, *children[:i], replacement, *children[i + 1:])
    return None


def variants(reference):
    tree = parse_term(reference)
    result = {}
    for family in ("reassociate", "reorder", "demorgan", "distribute"):
        candidate = _rewrite_one(tree, family)
        if candidate is not None:
            result[family] = format_term(candidate)
    return result


def collect_cases():
    archive_file = RESULTS / "frame-monitor-loop-live/transcript.tar.gz"
    provenance = json.loads((archive_file.parent / "provenance.json").read_bytes())
    require(hashlib.sha256(archive_file.read_bytes()).hexdigest() == provenance["transcript_sha256"], "live archive changed")
    archive = read_archive(archive_file)
    config = json.loads(archive["config.json"])
    live_summary = json.loads(archive["summary.json"])
    require(config["mode"] == live_summary["mode"] == "live" and live_summary["rounds_per_arm"] == 2, "wrong source run")
    cases = {}

    def add(cohort, field, candidate, label, expected):
        reference = REFERENCES[field]
        key = (cohort, reference, candidate)
        if key not in cases:
            cases[key] = dict(cohort=cohort, field=field, reference=reference, candidate=candidate,
                              expected=expected, sources=[])
        cases[key]["sources"].append(label)

    final = json.loads(archive["egg/round-02/response.json"])["output"]["monitors"]
    saved = json.loads(archive["egg/round-02/semantic.json"])
    require(set(final) == set(saved) == set(config["seed"]) == set(REFERENCES), "archived property inventory drift")
    historical = {}
    for field, reference in REFERENCES.items():
        row = saved[field]
        require(row["reference"] == reference and row["candidate"] == final[field], "archived model pair drift")
        evidence = row["evidence"]
        audit = validate_proof_dependencies(evidence["egg_input"], evidence["egg_graph"])
        require(audit == evidence["egg_audit"], "archived proof replay failed")
        before = evidence["egg_graph"]["targets"]
        old_proved = before[0]["eclass"] == before[1]["eclass"]
        require(old_proved == row["proof"]["proved"], "archived proof flag drift")
        historical[field] = {"proved": old_proved, "checked_steps": audit["checked_steps"]}
        add("live_final", field, final[field], "live:egg/round-02", True)
        add("live_seed", field, config["seed"][field], "live:config/seed", False)
        for family, candidate in variants(reference).items():
            add("generated", field, candidate, family, True)
    for turn in (1, 2):
        f = f"egg/round-{turn:02d}/response.json"
        items = json.loads((RESULTS / "frame-monitor-loop-fixture" / f).read_bytes())["output"]["monitors"]
        require(set(items) == set(REFERENCES), "fixture inventory drift")
        for field, candidate in items.items():
            add("fixture_revisions", field, candidate, "fixture:" + f, True)
    return list(cases.values()), historical


def check_graph(payload, graph, rules, *, stop_on_merge=False):
    checker = ProofChecker(payload, pattern_rules=rules)
    require(graph["pattern_rule_count"] == len(rules) and graph["ground_rule_count"] == 0, "rule count mismatch")
    targets, rows = payload["targets"], graph["targets"]
    require(len(rows) == len(targets) == 2 and [r["id"] for r in rows] == [t["id"] for t in targets]
            and targets[0]["event_context"] == targets[1]["event_context"], "unexpected endpoints or context")
    stop = graph["stop_reason"]
    saturated = stop == "Some(Saturated)"
    require(saturated or (stop_on_merge and stop == MERGED_STOP) or re.fullmatch(r"Some\((?:TimeLimit|IterationLimit|NodeLimit)\([0-9.eE+\-]+\)\)", stop),
            f"unexpected stop reason {stop!r}")
    same = parse(targets[0]["compact"]) == parse(targets[1]["compact"])
    merged = rows[0]["eclass"] == rows[1]["eclass"]
    require(same == (rows[0]["eclass_before"] == rows[1]["eclass_before"]), "false structural identity")
    require(stop != MERGED_STOP or merged, "goal stop reported for unmerged endpoints")
    edges = graph["rewrite_explanations"]
    steps = []
    if same:
        require(merged and not edges, "structural identity has inconsistent classes or explanation")
        status = "structural_identity"
    elif merged:
        require(len(edges) == 1 and {edges[0]["left"], edges[0]["right"]} == {r["id"] for r in rows},
                "distinct merged terms lack a connecting explanation")
        steps = checker.check(edges[0])["steps"]
        require(steps, "empty proof")
        status = "checked_derivation"
    else:
        require(not edges, "unmerged terms have proof edges")
        status = "saturated_miss" if saturated else "limited"
    return {"proved": same or bool(steps), "saturated_proved": saturated and (same or bool(steps)),
            "status": status, "steps": steps, "stop": stop}


def run_profile(binary, terms, rules, *, stop_on_merge=False, scope=SCOPE):
    payload = {"verified_rules": [], "pattern_rules": rules, "targets": [
        {"id": name, "compact": term, "event_context": scope}
        for name, term in zip(("reference", "candidate"), terms, strict=True)]}
    start = time.perf_counter()
    try:
        command = [binary, "--stop-on-merge"] if stop_on_merge else [binary]
        p = subprocess.run(command, input=json.dumps(payload), text=True, capture_output=True, timeout=20)
    except subprocess.TimeoutExpired:
        return {"status": "limited", "proved": False, "saturated_proved": False, "steps": [],
                "stop": "subprocess_timeout_20s",
                "wall_seconds": time.perf_counter() - start, "graph": None}
    elapsed = time.perf_counter() - start
    p.check_returncode()
    graph = json.loads(p.stdout)
    return {**check_graph(payload, graph, rules, stop_on_merge=stop_on_merge), "wall_seconds": elapsed, "graph": graph}


def quotient_coverage(case, binary, profiles, *, early_first=False):
    result = review(case["reference"], case["candidate"], arm="ordinary", binary=None, timeout_ms=TIMEOUT_MS)
    require(result["equivalent"] is case["expected"], f"typed oracle disagrees with {case}")
    evidence = result["evidence"]
    aliases = evidence["certified_substitution"]
    sources = {k: parse_term(v) for k, v in evidence["atom_sources"].items()}
    env = z3_env()
    checks = {}
    for atom, (canonical, inverse) in aliases.items():
        if (atom, False) == (canonical, inverse):
            continue
        a, b = z3_term(sources[atom], env), z3_term(sources[canonical], env)
        query = z3.Solver()
        query.set(timeout=TIMEOUT_MS)
        query.add(z3.Xor(a, z3.Not(b) if inverse else b))
        status = str(query.check())
        require(status == "unsat", "typed substitution is not certified")
        checks[atom] = {"representative": canonical, "complement": inverse, "status": status, "smt2": query.to_smt2()}
    terms = [format_term(_subst(parse(t), aliases)) for t in evidence["abstract_terms"]]
    ordered = list(profiles.items())
    if early_first:
        ordered.reverse()
    arms = {name: run_profile(binary, terms, rules, stop_on_merge=name == "ac_dist_goal")
            for name, rules in ordered}
    require(case["expected"] or not any(a["proved"] for a in arms.values()), "false proof of a typed negative")
    return dict(**case, typed_oracle=result["oracle"], ordinary=result["proof"], quotient_terms=terms,
                primitive_rules=evidence["verified_rules"], primitive_checks=evidence["primitive_pair_checks"],
                atom_sources=evidence["atom_sources"], quotient_checks=checks, profiles=arms)


def summarize(rows, profiles):
    table = {}
    for cohort in sorted({case["cohort"] for case in rows}):
        group = [case for case in rows if case["cohort"] == cohort]
        methods = {}
        for method in profiles:
            results = [c["profiles"][method] for c in group]
            methods[method] = {"proved": sum(a["proved"] for a in results), "denominator": len(group),
                               "saturated_proved": sum(a["saturated_proved"] for a in results),
                               "resource_limited": sum(a["stop"] not in ("Some(Saturated)", MERGED_STOP) for a in results),
                               "target_stops": sum(a["stop"] == MERGED_STOP for a in results),
                               "status": dict(Counter(a["status"] for a in results)),
                               "stops": dict(Counter(a["stop"] for a in results)),
                               "checked_steps": sum(len(a["steps"]) for a in results)}
        table[cohort] = {"unique_pairs": len(group), "source_occurrences": sum(len(c["sources"]) for c in group),
                         "typed_equivalent": sum(c["typed_oracle"]["status"] == "unsat" for c in group),
                         "ordinary_proved": sum(c["ordinary"]["proved"] for c in group), "profiles": methods}
    return table


def paired_goal_metrics(rows):
    metrics = {}
    for name, expected in (("typed_positives", True), ("typed_negatives", False)):
        group = [row["profiles"] for row in rows if row["expected"] is expected]
        metrics[name] = {
            "pairs": len(group),
            "goal_faster_pairs": sum(r["ac_dist_goal"]["wall_seconds"] < r["ac_dist"]["wall_seconds"] for r in group),
            "proof_verdicts_agree": all(r["ac_dist_goal"]["proved"] == r["ac_dist"]["proved"] for r in group),
            "modes": {},
        }
        for mode in ("ac_dist", "ac_dist_goal"):
            arms = [r[mode] for r in group]
            sizes = [a["graph"]["enodes"] for a in arms if a["graph"] is not None]
            metrics[name]["modes"][mode] = {
                "median_wall_ms": median(a["wall_seconds"] * 1000 for a in arms),
                "final_graphs_observed": len(sizes), "median_final_enodes": median(sizes) if sizes else None,
            }
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True, help="release egg_assertion_forms")
    parser.add_argument("--output", type=Path, required=True, help="new results directory")
    parser.add_argument("--compare-early-stop", action="store_true",
                        help="only the broad rules: pair default and --stop-on-merge on the same binary")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    binary = args.binary.resolve(strict=True)
    profiles = rule_profiles()
    if args.compare_early_stop:
        broad = profiles["ac_dist"]
        profiles = {"ac_dist": broad, "ac_dist_goal": broad}
    cases, old = collect_cases()
    design = {"cohorts_and_exact_pairs": cases, "rules": profiles,
              "boolean_truth_rows": {k: validate_pattern_rules(v) for k, v in profiles.items()},
              "typed_z3_timeout_ms": TIMEOUT_MS, "runner_bounds": {"iterations": 20, "enodes": 20000, "seconds": 5},
              "early_stop_comparison": args.compare_early_stop,
              "external_timeout_seconds": 20, "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
              "z3_version": z3.get_version_string(), "engine_source_sha256": hashlib.sha256(
                  (ROOT / "egraph/src/bin/egg_assertion_forms.rs").read_bytes()).hexdigest()}
    (args.output / "protocol.json").write_text(json.dumps(design, indent=2) + "\n")
    rows = []
    with gzip.open(args.output / "cases.jsonl.gz", "wt", encoding="utf-8") as stream:
        for i, case in enumerate(cases):
            row = quotient_coverage(case, binary, profiles, early_first=args.compare_early_stop and i % 2 == 1)
            rows.append(row)
            stream.write(json.dumps(row, separators=(",", ":")) + "\n")
            stream.flush()
    summary = {"complete": True, "unique_pairs": len(rows), "generic_jobs": len(rows) * len(profiles),
               "archived_indexed_live_final": old, "cohorts": summarize(rows, profiles)}
    if args.compare_early_stop:
        summary["paired_goal_metrics"] = paired_goal_metrics(rows)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
