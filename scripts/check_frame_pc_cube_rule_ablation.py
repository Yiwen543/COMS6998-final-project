#!/usr/bin/env python3
"""Repeat every offered fixture cube query after removing only the two De Morgan rules."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

from audit_egg_fifo_live import read_archive, require
from egg_frame_pc_certificate import MAX_CHARS, MAX_STEPS, TIMEOUT_SECONDS
from egg_frame_pc_cube_certificate import (
    RULES, SCOPE, _bound, _checked_steps, _json, _rules, replay_public_cube, verify_cube_certificate,
)


def check(bound, graph, rules, schemas):
    term = bound["restricted_source"]
    require(graph["source"] == term and graph["target"] == "true" and type(graph["merged"]) is bool,
            "engine returned an unrelated target")
    if not graph["merged"]:
        require(graph["explanation"] is None, "proof returned without a merge")
        return {"proved": False, "fits": False, "steps": None, "public_chars": None}
    steps = _checked_steps(term, graph["explanation"], schemas)
    names = {s["rule"] for s in steps}
    public = {"method": "restricted_cube", "status": "checked_rewrite" if steps else "checked_identity",
              "scope": SCOPE, **{k: bound[k] for k in ("candidate_value", "source", "atoms", "cube", "restricted_source")},
              "target": "true", "rules": [r for r in rules if r["name"] in names], "steps": steps}
    chars = len(_json(public))
    fits = len(steps) <= MAX_STEPS and chars <= MAX_CHARS
    if fits:
        replay_public_cube(public)
    return {"proved": True, "fits": fits, "steps": len(steps), "public_chars": chars,
            "used_rules": sorted(names), "checked_steps": steps}


def run(read, binary):
    source_hashes = {}

    def get(name):
        data = read(name)
        source_hashes[name] = hashlib.sha256(data).hexdigest()
        return data

    config = json.loads(get("config.json"))
    require(config["mode"] == "fixture" and config["certificate_mode"] == "cube" and
            config["replicates"] == 1 and config["rounds_per_arm"] == 2 and
            set(config["profiles"]) == {"historical", "mixed", "corner"}, "expected the matched cube fixture")
    removed = {"de-morgan-and", "de-morgan-or"}
    retained = [r for r in RULES if r["name"] not in removed]
    require(len(RULES) == 19 and len(retained) == 17, "review rule inventory drift")
    full_schemas, _ = _rules(RULES)
    schemas, truth_rows = _rules(retained)
    counter = Counter()
    cases = []
    for profile in config["profiles"]:
        root = f"{profile}/trial-01/egg"
        for round_id, stage in enumerate(("seed", "round-01"), start=1):
            prefix = f"{root}/{stage}"
            certs = json.loads(get(f"{prefix}/certificates.json"))
            diagnoses = json.loads(get(f"{prefix}/diagnoses.json"))
            feedback = get(f"{prefix}/feedback.txt").decode().strip()
            messages = json.loads(get(f"{root}/round-{round_id:02d}/request.json"))["messages"]
            require(feedback in messages[-1]["content"] and
                    json.loads(feedback)["egg_certificates"] == {k: c["public"] for k, c in certs.items()} and
                    certs.keys() == diagnoses.keys(), "stage does not match actually dispatched fixture request")
            for name, cert in sorted(certs.items()):
                d = diagnoses[name]
                verify_cube_certificate(d, cert)
                bound = _bound(d)
                term = bound["restricted_source"]
                baseline = cert["evidence"]
                require(baseline["engine_request"] == {"term": term, "pattern_rules": RULES},
                        "original query used different rules or source")
                original = check(bound, baseline["engine"], RULES, full_schemas)
                require(original["fits"] == (cert["public"]["status"] != "unavailable"), "19-rule budget differs")
                request = {"term": term, "pattern_rules": retained}
                proc = subprocess.run([binary], input=_json(request), text=True, capture_output=True,
                                      check=True, timeout=TIMEOUT_SECONDS)
                graph = json.loads(proc.stdout)
                changed = check(bound, graph, retained, schemas)
                for arm, outcome in (("19", original), ("17", changed)):
                    counter[f"proved_{arm}"] += int(outcome["proved"])
                    counter[f"within_budget_{arm}"] += int(outcome["fits"])
                counter["gained"] += int(not original["fits"] and changed["fits"])
                counter["lost"] += int(original["fits"] and not changed["fits"])
                cases.append({"profile": profile, "stage": stage, "request_round": round_id, "property": name,
                              "typed_candidate": d["candidate"], **{k: bound[k] for k in
                                  ("candidate_value", "source", "atoms", "cube", "restricted_source")},
                              "baseline_19": original, "ablation_17": changed, "graph_17": graph})
    require(len(cases) == 24, "expected 24 delivered mismatch opportunities")
    summary = {"experiment": "post-hoc two-rule deletion on already delivered fixture inputs",
               "api_calls": 0, "opportunities": len(cases),
               "unique_restricted_sources": len({r["restricted_source"] for r in cases}), **dict(counter),
               "rule_count": len(retained), "removed_rules": sorted(removed), "rules": retained,
               "typed_rule_truth_rows": truth_rows, "max_steps": MAX_STEPS, "max_public_chars": MAX_CHARS,
               "runner_iter_limit": 20, "runner_node_limit": 20000, "runner_seconds": 5,
               "process_timeout_seconds": TIMEOUT_SECONDS, "source_file_sha256": source_hashes,
               "archived_binary_sha256": config["diagnostic_binary_sha256"],
               "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest()}
    return summary, cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--run-dir", type=Path)
    src.add_argument("--archive", type=Path)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.archive is not None:
        read = read_archive(args.archive).__getitem__
    else:
        def read(name):
            return (args.run_dir / name).read_bytes()
    summary, cases = run(read, args.binary.resolve(strict=True))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    (args.output / "cases.jsonl").write_text("".join(_json(r) + "\n" for r in cases))
    print(f"19 rules {summary['within_budget_19']}/{len(cases)}, 17 rules {summary['within_budget_17']}/{len(cases)}")


if __name__ == "__main__":
    main()
