#!/usr/bin/env python3
"""Replay the two live AXIS hold misses with conjunction associativity as the only egg rule."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from audit_egg_fifo_live import read_archive, require
from egg_frame_proof import SCOPE, typed_oracle
from egg_frame_terms import REFERENCES, abstract, parse_term
from m3_proof_dependencies import validate_pattern_rules, validate_proof_dependencies


RULES = [{"name": "and-associate-right", "left": "(and (and ?a ?b) ?c)", "right": "(and ?a (and ?b ?c))"}]
HOLDS = {"data_hold", "header_hold"}


def run(read, binary):
    digests = {}

    def record(name):
        data = read(name)
        digests[name] = hashlib.sha256(data).hexdigest()
        return json.loads(data)

    summary = record("summary.json")
    require(summary["mode"] == "live" and summary["rounds_per_arm"] == 2, "expected the two-round live run")
    live, cases = [], {}
    for i in (1, 2):
        prefix = f"egg/round-{i:02d}"
        answer = record(f"{prefix}/response.json")["output"]["monitors"]
        rows = record(f"{prefix}/semantic.json")
        require(set(rows) == set(answer) == set(REFERENCES), "unexpected monitor inventory")
        outcomes = {}
        for name, reference in REFERENCES.items():
            row = rows[name]
            require((row["arm"], row["reference"], row["candidate"]) == ("egg", reference, answer[name]),
                    "typed terms differ from sources")
            evidence = row["evidence"]
            payload, graph = evidence["egg_input"], evidence["egg_graph"]
            targets = [{"id": role, "compact": abstract(parse_term(src))[0], "event_context": SCOPE}
                       for role, src in (("reference", reference), ("candidate", answer[name]))]
            require(targets == payload["targets"] and evidence["egg_timing"]["mode"] == "indexed",
                    "archive is not the indexed run on these two same-scope typed terms")
            audit = validate_proof_dependencies(payload, graph)
            left, right = graph["targets"]
            proved = left["eclass"] == right["eclass"]
            outcomes[name] = {"proved": proved, "checked_steps": audit["checked_steps"]}
            require(audit == evidence["egg_audit"] and row["proof"]["proved"] is proved and
                    row["equivalent"] is True and row["oracle"]["status"] == "unsat", "live outcome differs")
            if name in HOLDS:
                require(not proved and payload["verified_rules"] == [], "expected an original uncoupled hold miss")
                binding = {"reference": reference, "candidate": answer[name], "targets": targets}
                require(cases.setdefault(name, binding) == binding, "rounds contain different hold candidates")
            else:
                require(proved and reference == answer[name] and audit["checked_steps"] == 0,
                        "other live properties are expected to be identical")
        require(summary["arms"]["egg"]["rounds"][i-1]["proofs_found"] == sum(v["proved"] for v in outcomes.values()),
                "archived summary differs from the audited graphs")
        live.append({"round": i, "properties": outcomes})

    valuations = validate_pattern_rules(RULES)
    output = {}
    for name, case in cases.items():
        require(typed_oracle(case["reference"], case["candidate"])["oracle"]["status"] == "unsat",
                "hold expressions differ under the independent full-width oracle")
        payload = {"targets": case["targets"], "verified_rules": [], "pattern_rules": RULES}
        proc = subprocess.run([binary], input=json.dumps(payload), text=True, capture_output=True,
                              check=True, timeout=20)
        graph = json.loads(proc.stdout)
        audit = validate_proof_dependencies(payload, graph, pattern_rules=RULES)
        require(audit["checked_edges"] == 1 and audit["checked_steps"] > 0 and
                audit["pattern_rules"] == [RULES[0]["name"]], "missing checked associativity derivation")
        output[name] = {"reference": case["reference"], "candidate": case["candidate"], "full_typed_xor": "unsat",
                        "egg_input": payload, "egg_graph": graph, "checked_proof": audit}

    return {"scope": "post-hoc control on the two unique hold pairs missed by indexed egg in both live rounds",
            "live_indexed": {"binary": "guard_proofs_fast indexed", "rounds": live},
            "post_hoc": {"binary": "egg_assertion_forms", "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
                         "pattern_rules": RULES, "ground_rules": [], "rule_truth_table_rows": valuations,
                         "proved_holds": len(output), "hold_pairs": output},
            "source_file_sha256": digests}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--archive", type=Path, help="original live frame Responses .tar.gz archive")
    source.add_argument("--run-dir", type=Path, help="extracted live run directory containing summary.json")
    parser.add_argument("--binary", required=True, type=Path, help="release egg_assertion_forms binary")
    parser.add_argument("--output", type=Path, help="write result and proofs as JSON (stdout by default)")
    args = parser.parse_args()
    if args.archive is not None:
        read = read_archive(args.archive).__getitem__
    else:
        def read(name):
            return (args.run_dir / name).read_bytes()
    result = run(read, args.binary.resolve(strict=True))
    report = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(report, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
