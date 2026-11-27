#!/usr/bin/env python3
"""Remove context-only nonconstant primitive relations from the real exact-four data_last branches."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

from egg_txn_context import ordinary, prepare, verify_facts, verify_partition
from egg_txn_context_check import PATTERN_RULES, check_graph
from egg_txn_terms import evaluate_term, parse_term
from predicates import evaluate, parse
from run_txn_context import BINARY_TIMEOUT, require, typed_oracle


GUARD = "(eq data_n 4)"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_abstract_counterexample(prepared, retained, answer):
    if answer["status"] != "sat":
        return
    model = answer["abstract_counterexample"]
    require(set(model) == set(prepared["atoms"]) and all(type(v) is bool for v in model.values()),
            "incomplete propositional counterexample")
    require(all(evaluate(parse(f["left"]), model) == evaluate(parse(f["right"]), model) for f in retained),
            "Boolean model violates a retained premise")
    left, right = map(parse, prepared["abstracts"])
    require(evaluate(left, model) != evaluate(right, model), "Boolean model fails to distinguish targets")


def ablate(case, branch, prepared, binary):
    ctx = branch["context"]
    full = branch["facts"]
    require(ctx["guard"] == GUARD and ctx["feasibility"]["status"] == "sat", "wrong guard")
    verify_facts(prepared, ctx, full)
    original = branch["payload"]
    targets = [{"id": name, "compact": text, "event_context": ctx["id"]}
               for name, text in zip(("left", "right"), prepared["abstracts"], strict=True)]
    require(original == {"context_id": ctx["id"], "targets": targets, "pattern_rules": PATTERN_RULES,
                         "ground_rules": full["facts"]}, "source graph input not bound to this branch")
    before = check_graph(original, branch["graph"])
    require(before == branch["proof"], "original checked proof differs")
    ordinary_before = ordinary(prepared, ctx, full)
    require(ordinary_before["status"] == branch["ordinary"]["status"], "original Boolean result differs")
    retained = []
    removed = []
    globally_valid = []
    for fact in full["facts"]:
        if fact["right"] in ("true", "false"):
            retained.append(fact)
            continue
        certificate = full["receipts"][fact["name"]]
        left, right = certificate["typed_left"], certificate["typed_right"]
        global_xor = typed_oracle(left, right)
        if global_xor["status"] == "unsat":
            retained.append(fact)
            globally_valid.append({"fact": fact["name"], "typed_xor": global_xor})
        else:
            require(global_xor["status"] == "sat", "global status of a proposed removal is unresolved")
            sample = global_xor["counterexample"]
            require(evaluate_term(parse_term(left), sample) != evaluate_term(parse_term(right), sample) and
                    evaluate_term(parse_term(GUARD), sample) is False, "global counterexample failed typed replay")
            removed.append({"fact": fact, "local_certificate": certificate, "global_xor": global_xor})
    payload = {**original, "ground_rules": retained}
    verified = {f["name"]: full["receipts"][f["name"]] for f in retained}
    ordinary_after = ordinary(prepared, ctx, {"facts": retained, "receipts": verified})
    check_abstract_counterexample(prepared, retained, ordinary_after)
    try:
        proc = subprocess.run([binary], input=json.dumps(payload), text=True, capture_output=True,
                              check=True, timeout=BINARY_TIMEOUT)
    except subprocess.TimeoutExpired:
        graph = None
        proof = {"status": "subprocess_timeout", "proved": False, "steps": [], "stop": "subprocess_timeout",
                 "used_ground_rules": []}
    else:
        graph = json.loads(proc.stdout)
        proof = check_graph(payload, graph)
    require(not proof["proved"] or ordinary_after["status"] != "sat", "checked proof contradicts Boolean countermodel")
    return {"case": case, "context": ctx, "prepared": prepared, "removed": removed,
            "retained_unconditional": globally_valid, "retained_local_receipts": verified,
            "before": {"graph": branch["graph"], "proof": before, "ordinary": branch["ordinary"]},
            "after": {"payload": payload, "graph": graph, "proof": proof, "ordinary": ordinary_after}}


def run(source, binary):
    protocol = json.loads((source / "protocol.json").read_bytes())
    require(protocol["pattern_rules"] == PATTERN_RULES and protocol["binary_sha256"] == digest(binary),
            "different native engine or pattern inventory from main study")
    require((source / "summary.json").is_file(), "main experiment is incomplete")
    rows, omitted = [], []
    with gzip.open(source / "cases.jsonl.gz", "rt", encoding="utf8") as stream:
        finished = list(map(json.loads, stream))
    require([row["case"] for row in finished] == protocol["cases"], "source case inventory differs")
    for row in finished:
        case = row["case"]
        if case["property"] != "data_last" or case["cohort"] != "real":
            continue
        prepared = prepare(case["left"], case["right"])
        require(prepared == row["prepared"], "source data_last pair differs from archived targets")
        require(typed_oracle(case["left"], case["right"])["status"] == row["oracle"]["status"] == "unsat",
                "full typed endpoints are not verified equivalent")
        method = row["methods"]["contextual"]
        plan = method["plan"]
        verify_partition(plan, prepared)
        require([b["context"] for b in method["branches"]] == plan["contexts"], "branch inventory differs")
        matches = [b for b in method["branches"] if b["context"]["guard"] == GUARD]
        if matches:
            require(len(matches) == 1, "duplicate equality branch")
            rows.append(ablate(case, matches[0], prepared, binary))
        else:
            omitted.append({"id": case["id"], "trial_pairs": case["trial_pairs"],
                            "selected_guards": [c["guard"] for c in plan["contexts"]]})
    require(len(rows) + len(omitted) == 3, "expected all three distinct real data_last pairs")
    summary = {"experiment": "post-hoc scoped primitive-fact removal", "guard": GUARD,
               "selection": "all feasible exact-four branches of real data_last pairs in original partition",
               "removed_when": "nonconstant pair fact and unrestricted typed XOR is SAT",
               "api_calls": 0, "binary_sha256": digest(binary), "protocol_sha256": digest(source / "protocol.json"),
               "source_cases_sha256": digest(source / "cases.jsonl.gz"), "eligible": len(rows), "ineligible": omitted,
               "removed_fact_occurrences": sum(len(r["removed"]) for r in rows),
               "removed_distinct_typed_relations": len({(f["local_certificate"]["typed_left"],
                   f["local_certificate"]["typed_right"]) for r in rows for f in r["removed"]}),
               "status": {arm: {"egg": dict(Counter(r[arm]["proof"]["status"] for r in rows)),
                                "ordinary": dict(Counter(r[arm]["ordinary"]["status"] for r in rows))}
                          for arm in ("before", "after")}}
    return summary, rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, required=True, help="completed main context experiment directory")
    p.add_argument("--binary", required=True, type=Path, help="exact egg_context_forms binary used by main run")
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    summary, rows = run(args.source, args.binary.resolve(strict=True))
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    with gzip.open(args.output / "cases.jsonl.gz", "wt", encoding="utf8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps(summary["status"], sort_keys=True))


if __name__ == "__main__":
    main()
