#!/usr/bin/env python3
"""Compare all unordered same-property pairs of actual unassisted transaction-monitor outputs."""
import argparse
from collections import Counter
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path

import z3

from audit_egg_fifo_live import read_archive, require
from egg_frame_proof import _certify_atoms, _check, _ordinary, _quotient, _subst
from egg_frame_proof_coverage import rule_profiles, run_profile
from egg_txn_terms import REFERENCES, abstract, format_term, parse_term, z3_env, z3_term
from m3_proof_dependencies import validate_pattern_rules
from predicates import parse


SCOPE = "Transaction variables at one two-state snapshot, with unrestricted values at their declared widths."
TIMEOUT_MS = 5000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def typed_xor(left, right, env):
    a, b = (z3_term(parse_term(t), env) for t in (left, right))
    record, _ = _check(z3.Xor(a, b), TIMEOUT_MS)
    return record


def pair_analysis(texts, profiles, binary, env):
    (a, left), (b, right) = [abstract(parse_term(t)) for t in texts]
    require(all(left[k] == right[k] for k in left.keys() & right.keys()), "typed atom name collision")
    atoms = {**left, **right}
    trees = [parse(a), parse(b)]
    rules, checks = _certify_atoms(atoms, trees, env, TIMEOUT_MS, lower=z3_term, scope=SCOPE)
    aliases = _quotient(rules)
    # Check every effective replacement too, including transitive signed representatives.
    receipts = {}
    for name, (rep, inverse) in aliases.items():
        if name != rep or inverse:
            x, y = z3_term(atoms[name], env), z3_term(atoms[rep], env)
            receipt, _ = _check(z3.Xor(x, z3.Not(y) if inverse else y), TIMEOUT_MS)
            require(receipt["status"] == "unsat", "uncertified replacement")
            receipts[name] = {"representative": rep, "inverse": inverse, **receipt}
    quotient = [format_term(_subst(tree, aliases)) for tree in trees]
    ordinary, ordinary_evidence = _ordinary(trees, rules, TIMEOUT_MS)
    typed = typed_xor(*texts, env)
    arms = {key: run_profile(binary, quotient, inventory, stop_on_merge=True, scope=SCOPE)
            for key, inventory in profiles.items()}
    if typed["status"] == "sat":
        require(not ordinary["proved"] and not any(r["proved"] for r in arms.values()), "typed counterexample contradicts proof")
    return {"texts": texts, "typed_xor": typed, "abstract_terms": [a, b], "quotient_terms": quotient,
            "typed_atoms": {k: format_term(v) for k, v in atoms.items()}, "certified_rules": rules,
            "primitive_queries": checks, "substitution_checks": receipts,
            "ordinary": {**ordinary, **ordinary_evidence}, "egg": arms}


def summarize(cases):
    methods = {}
    for profile in rule_profiles():
        results = [r["egg"][profile] for r in cases]
        methods[profile] = {"status": dict(Counter(v["status"] for v in results)),
                            "checked_steps": sum(len(v["steps"]) for v in results),
                            "stops": dict(Counter(v["stop"] for v in results))}
    return {"unique_nonidentical_pairs": len(cases),
            "nonidentical_occurrences": sum(len(r["trials"]) for r in cases),
            "typed_xor_status": dict(Counter(r["typed_xor"]["status"] for r in cases)),
            "ordinary_abstract_xor": dict(Counter(r["ordinary"]["abstract_xor"]["status"] for r in cases)),
            "ordinary_canonical_matches": sum(r["ordinary"]["canonical_match"] for r in cases),
            "profiles": methods}


def analyze(archive, binary):
    files = read_archive(archive)
    config = json.loads(files["config.json"])
    require(config["mode"] == "live" and config["task"] == "frame-transaction-v1" and config["trials"] == 3,
            "expected the three-trial live transaction experiment")
    data, hashes = {}, {}
    for i in range(1, config["trials"] + 1):
        name = f"trial-{i:02d}/initial/response.json"
        response = json.loads(files[name])
        require(response["status"] == "completed" and response["id"], f"incomplete initial response in {name}")
        props = response["output"]["monitors"]
        require(set(props) == set(REFERENCES), "live property inventory differs")
        data[i] = props
        hashes[name] = digest(files[name])
    env = z3_env()
    grades, pairs, identity = {}, {}, []
    for name, reference in sorted(REFERENCES.items()):
        for trial, props in data.items():
            grades.setdefault((name, props[name]), []).append(trial)
        for i, j in combinations(data, 2):
            left, right = sorted((data[i][name], data[j][name]))
            if left == right:
                identity.append({"property": name, "trials": [i, j], "text": left})
            else:
                pairs.setdefault((name, left, right), []).append([i, j])
    grade_rows = [{"property": k, "text": t, "reference": REFERENCES[k], "trials": ids,
                   "typed_xor": typed_xor(REFERENCES[k], t, env)} for (k, t), ids in grades.items()]
    profiles = rule_profiles()
    truth_rows = {k: validate_pattern_rules(v) for k, v in profiles.items()}
    cases = [{"property": k, "trials": ids, **pair_analysis([a,b], profiles, binary, env)}
             for (k, a, b), ids in pairs.items()]
    summary = {"analysis": "post-hoc initial-output pair comparison; no live model feedback", "scope": SCOPE,
               "limits": {"iterations": 20, "enodes": 20000, "saturation_seconds": 5,
                          "outer_timeout_seconds": 20, "smt_timeout_ms": TIMEOUT_MS, "stop_on_merge": True},
               "archive_sha256": digest(archive.read_bytes()), "response_sha256": hashes,
               "engine_sha256": digest(binary.read_bytes()), "z3": z3.get_version_string(),
               "rules": profiles, "rule_truth_table_rows": truth_rows, "reference_comparisons": len(grade_rows),
               "reference_slots": sum(map(len, grades.values())),
               "reference_xor_status": dict(Counter(g["typed_xor"]["status"] for g in grade_rows)),
               "text_identity_occurrences": len(identity), "identities": identity, **summarize(cases)}
    return summary, grade_rows, cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--binary", required=True, type=Path, help="egg_assertion_forms supporting --stop-on-merge")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    summary, grades, cases = analyze(args.archive, args.binary.resolve(strict=True))
    args.output.mkdir(parents=True, exist_ok=False)
    for filename, rows in [("candidate-reference.jsonl.gz", grades), ("pairs.jsonl.gz", cases)]:
        with gzip.open(args.output / filename, "wt", encoding="utf8") as f:
            for row in rows:
                f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"ordinary": summary["ordinary_abstract_xor"], "egg": summary["profiles"]}, indent=2))


if __name__ == "__main__":
    main()
