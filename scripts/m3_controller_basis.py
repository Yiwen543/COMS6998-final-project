#!/usr/bin/env python3
"""Requalify reduced sets of Controller rules with original QF_BV obligations, egg and RTL."""
import argparse
from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from benchmark_guard_proofs_fast import components
from benchmark_m3_controller import (
    TRACES, check_observation, digest, plan, require, save, scan, structural_keys,
)
from m3_controller_certificates import verify_rules
from m3_controller_replay import SCREEN, build, check_file, replay
from m3_proof_dependencies import validate_proof_dependencies
from predicates import evaluate, parse


class Congruence:
    """Ordinary ground congruence on a fixed, hash-consed DAG of seen subterms."""

    def __init__(self, terms):
        self.parent = list(range(len(terms)))
        self.nodes = [(i, term[0], tuple(terms[child] for child in term[1:]))
                      for term, i in terms.items() if isinstance(term, tuple)]

    def root(self, i):
        while i != self.parent[i]:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def merge(self, a, b):
        a, b = self.root(a), self.root(b)
        if a == b:
            return False
        self.parent[b] = a
        return True

    def close(self):
        changed = True
        while changed:
            changed = False
            seen = {}
            for index, op, children in self.nodes:
                key = (op, *(self.root(child) for child in children))
                prior = seen.setdefault(key, index)
                if prior != index and self.merge(prior, index):
                    changed = True


def forest_basis(payload):
    """Retain independent input-order edges, then drop edges made redundant later."""
    targets = payload["targets"]
    roots = structural_keys({"targets": targets, "verified_rules": []})
    terms = {}

    def intern(tree):
        if tree not in terms:
            if isinstance(tree, tuple):
                for child in tree[1:]:
                    intern(child)
            terms[tree] = len(terms)
        return terms[tree]

    target_roots = {t["id"]: intern(root) for t, root in zip(targets, roots, strict=True)}
    endpoints = {}
    for rule in payload["verified_rules"]:
        a, b = rule["source_ids"]
        endpoints[rule["name"]] = target_roots[a], target_roots[b]

    cc = Congruence(terms)
    selected = []
    for name, (a, b) in endpoints.items():
        if cc.merge(a, b):
            selected.append(name)
            cc.close()
    forest_size = len(selected)
    for name in reversed(selected.copy()):
        trial = Congruence(terms)
        for other in selected:
            if other != name:
                trial.merge(*endpoints[other])
        trial.close()
        a, b = endpoints[name]
        if trial.root(a) == trial.root(b):
            selected.remove(name)
    return selected, forest_size


def run_engine(binary, payload, directory):
    directory.mkdir()
    save(directory / "egg-input.json", payload)
    job = subprocess.run([binary, "indexed"], input=json.dumps(payload).encode(),
                         capture_output=True, check=True, timeout=60)
    graph = json.loads(job.stdout)
    (directory / "egg.json").write_bytes(job.stdout)
    require(json.loads(job.stderr)["mode"] == "indexed", "wrong engine mode for rule subset")
    require(graph["stop_reason"] == "Some(Saturated)", "rule subset did not saturate")
    require(graph["ground_rule_count"] == len(payload["verified_rules"]), "rule count disagrees")
    require([t["id"] for t in graph["targets"]] == [t["id"] for t in payload["targets"]],
            "egg returned different source targets")
    return graph


def partitions(payload, graph):
    groups = defaultdict(list)
    for t in graph["targets"]:
        groups[t["eclass"]].append(t["id"])
    scoped = plan(payload["targets"], [t["eclass"] for t in graph["targets"]])
    return {"all_roots": sorted(sorted(g) for g in groups.values()),
            "same_scope": sorted(sorted(t["id"] for t in g) for g in scoped),
            "proof_components": components(graph)}


def target_fingerprint(graph, parts):
    # Class IDs and direct proof texts depend on insertion order. The stable
    # contract is group membership, all representatives, and proof connectivity.
    return digest({"partitions": parts, "representatives": [
        [t["id"], t["representative"]] for t in graph["targets"]]})


def qualify(args):
    """Materialize and recheck a published subset without processing the full rule list in egg or Z3."""
    fixture, output = args.fixture.resolve(), args.output
    directory = Path(__file__).resolve().parents[1] / "results/milestone3/proof-basis"
    benchmark = json.loads((directory / "summary.json").read_bytes())
    profile = benchmark["profiles"][args.qualify]
    data = check_file(fixture, SCREEN / "egg-input.json")
    require(profile["exact_target_parity"] and hashlib.sha256(data).hexdigest() == benchmark["input_sha256"],
            "the prequalified rule set is only valid on the pinned exact input")
    payload = json.loads(data)
    names = set(profile["selected_rule_names"])
    retained = [r for r in payload["verified_rules"] if r["name"] in names]
    require(len(retained) == len(names) == profile["retained_rules"], "invalid published selection")
    subset = {**payload, "verified_rules": retained}
    # Only the chosen hypotheses enter Z3, even though archive indices and digest
    # validation need access to the original immutable inventory.
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    cert = verify_rules(fixture / SCREEN, selected_names=names)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        stage = Path(tmp) / "verified"
        graph = run_engine(args.binary.resolve(), subset, stage)
        dependencies = validate_proof_dependencies(subset, graph)
        require(set(dependencies["ground_rules"]) <= set(cert["results"]), "uncertified proof dependency")
        actual = target_fingerprint(graph, partitions(subset, graph))
        require(actual == benchmark["full_target_fingerprint"], "full target quality fingerprint changed")
        proof_hash = digest(graph["rewrite_explanations"])
        if args.qualify == "proof_dependencies":
            require(proof_hash == benchmark["full_explanations_sha256"], "archived explanation text changed")
        save(stage / "certificates.json", cert)
        save(stage / "qualification.json", {"profile": args.qualify, "rule_obligations_unsat": cert["rule_queries"],
            "checked_explanations": len(dependencies["edges"]), "full_target_fingerprint": actual,
            "explanations_sha256": proof_hash,
            "egg_binary_sha256": hashlib.sha256(args.binary.read_bytes()).hexdigest()})
        stage.rename(output)


def check_representatives(graph, prefix, output, records, source_answers):
    # This independent audit is reported separately from retained-rule recertification.
    queries = [prefix]
    targets = graph["targets"]
    for t in targets:
        queries.append(f"(push)\n(assert (xor {t['id']} {t['representative']}))\n(check-sat)\n(pop)\n")
    smt = "".join(queries)
    (output / "representatives.smt2").write_text(smt)
    checked = subprocess.run(["z3", "-in", "-smt2"], input=smt, text=True, capture_output=True,
                             check=True, timeout=120)
    require(checked.stdout.splitlines() == ["unsat"] * len(targets),
            "representative failed independent full-domain QF_BV equivalence")
    answers = {t["id"]: None for t in targets}
    asts = [parse(t["representative"]) for t in targets]
    checked_rows = 0
    for trace in TRACES:
        rec = records[trace]
        require(rec["target_ids"] == list(answers), "physical target order mismatch")
        for cycle in rec["eligible_cycles"]:
            env = dict(zip(rec["atom_ids"], (b == "1" for b in rec["atom_rows"][cycle]), strict=True))
            bits = "".join("1" if evaluate(ast, env) else "0" for ast in asts)
            require(bits == rec["rows"][cycle], f"representative mismatch against RTL at {trace}/{cycle}")
            for t, bit in zip(targets, bits, strict=True):
                if bit == "1" and answers[t["id"]] is None:
                    answers[t["id"]] = [trace, cycle]
            checked_rows += 1
    require(answers == source_answers, "representative changed earliest legal RTL witness")
    return {"qfbv_unsat": len(targets), "eligible_pre_rows": checked_rows,
            "target_bits_compared": checked_rows * len(targets), "earliest_answers_sha256": digest(answers)}


def evaluate_basis(args):
    fixture, binary, out = args.fixture.resolve(), args.binary.resolve(), args.output
    out.mkdir(parents=True, exist_ok=False)
    screen = fixture / SCREEN
    payload = json.loads(check_file(fixture, SCREEN / "egg-input.json"))
    rule_names = [r["name"] for r in payload["verified_rules"]]
    ids = [t["id"] for t in payload["targets"]]
    require(len(ids) == 148 and len(set(rule_names)) == len(rule_names) == 281, "wrong frozen workload")
    full_cert = verify_rules(screen)
    prefix = check_file(fixture, SCREEN / "pairs.smt2").decode().split("(push)\n", 1)[0]

    # Compare physical evidence directly, including raw counters, registered public
    # observations and original target/atom rows, against the published Controller run.
    simulator = build(fixture, out / "build")
    records = {t: check_observation(replay(fixture, simulator, t, out / "rtl" / t), ids, t) for t in TRACES}
    reference = args.controller_results
    with gzip.open(reference / "records.json.gz", "rt") as f:
        require(records == json.load(f), "fresh RTL replay differs from checked-in Controller observations")
    answers = json.loads((reference / "answers.json").read_text())
    require(scan(records, ids) == answers, "fresh RTL scan differs from checked-in answers")

    full = run_engine(binary, payload, out / "full")
    full_parts = partitions(payload, full)
    all_reps = [t["representative"] for t in full["targets"]]
    full_edges = {(e["left"], e["right"]): e["explanation"] for e in full["rewrite_explanations"]}
    validation = validate_proof_dependencies(payload, full)
    deps = set(validation["ground_rules"])
    forest, before_pruning = forest_basis(payload)
    selections = {"full": rule_names, "proof_dependencies": [n for n in rule_names if n in deps],
                  "ordinary_forest": forest, "zero_control": []}
    profiles = {}
    for mode, names in selections.items():
        full_mode = mode == "full"
        selected = set(names)
        subset = {**payload, "verified_rules": [r for r in payload["verified_rules"] if r["name"] in selected]}
        # Re-use the already completed full recomputation only for that reference arm.
        certificates = full_cert if full_mode else verify_rules(screen, selected_names=selected)
        require(set(certificates["results"]) == selected, "recertification did not cover the exact retained rules")
        graph = full if full_mode else run_engine(binary, subset, out / mode)
        proofs = validation if full_mode else validate_proof_dependencies(subset, graph)
        require(set(proofs["ground_rules"]) <= selected, "new proof relies on a removed rule")
        parts = partitions(subset, graph)
        parity = {k: groups == full_parts[k] for k, groups in parts.items()}
        changed = [t["id"] for t, rep in zip(graph["targets"], all_reps, strict=True) if t["representative"] != rep]
        quality = check_representatives(graph, prefix, out / mode, records, answers)
        edges = {(e["left"], e["right"]): e["explanation"] for e in graph["rewrite_explanations"]}
        profiles[mode] = {
            "selected_rule_names": names, "retained_rules": len(names),
            "omitted_of_281": len(rule_names) - len(names), "retained_rule_obligations_unsat": certificates["rule_queries"],
            "all_target_classes": len(parts["all_roots"]), "same_scope_groups": len(parts["same_scope"]),
            "retained_proof_edges": len(proofs["edges"]), "new_proof_dependency_count": len(proofs["ground_rules"]),
            "full_endpoint_pairs_retained": len(edges.keys() & full_edges.keys()),
            "full_explanations_retained_verbatim": sum(full_edges.get(pair) == text for pair, text in edges.items()),
            "explanations_sha256": digest(graph["rewrite_explanations"]),
            "matches_full_partitions": parity, "different_representative_ids": changed,
            "exact_target_parity": all(parity.values()) and not changed, "representative_audit": quality,
        }
    require(profiles["full"]["exact_target_parity"], "invalid all-rule reference")
    require(not profiles["zero_control"]["matches_full_partitions"]["same_scope"],
            "zero-rule sensitivity control unexpectedly preserved the full partition")
    summary = {"input_sha256": hashlib.sha256(check_file(fixture, SCREEN / "egg-input.json")).hexdigest(),
               "full_target_fingerprint": target_fingerprint(full, full_parts),
               "full_explanations_sha256": digest(full["rewrite_explanations"]),
               "egg_binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(), "z3": full_cert["z3"],
               "rule_selection": "Fixed upstream order. Ordinary forest uses Boolean normalization, congruence on seen subterms, reverse deletion of implied edges.",
               "ordinary_forest_edges_before_reverse_deletion": before_pruning,
               "finite_witness_scope": "Three common fresh original RTL replays, all public development traces; settled PRE after first reset.",
               "fresh_rtl_replays": len(TRACES), "physical_edges": sum(TRACES.values()),
               "checker": {t: r["checker"] for t, r in records.items()},
               "full_run_records_sha256": digest(records), "finite_hits": sum(hit is not None for hit in answers.values()),
               "total_targets": len(ids), "profiles": profiles}
    save(out / "summary.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    parser.add_argument("--qualify", choices=["ordinary_forest", "proof_dependencies"],
                        help="only requalify the exact saved subset; emits reusable egg-input.json")
    parser.add_argument("--controller-results", type=Path,
                        default=Path(__file__).resolve().parents[1] / "results/milestone3/controller")
    args = parser.parse_args()
    if args.qualify:
        qualify(args)
    else:
        result = evaluate_basis(args)
        for profile, data in result["profiles"].items():
            print(profile, data["retained_rules"], data["same_scope_groups"], data["exact_target_parity"])
