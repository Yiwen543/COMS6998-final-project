#!/usr/bin/env python3
"""Persist independent Z3 checks for selected queue egg equivalence groups."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from preflight_heldout import z3_equivalent


def export(result: Path) -> dict:
    extraction = json.loads((result / "typed-predicates.json").read_text())
    graph = json.loads((result / "egg-evidence.json").read_text())
    roots = {item["id"]: item["eclass"] for item in graph["targets"]}
    groups: dict[tuple, list] = {}
    for version, item in extraction.items():
        for target in item["targets"]:
            if target["guard_depth"] == 4 and target["case_value"] in ("2'01", "2'10"):
                key = (roots[target["id"]], tuple(target["event_context"]))
                groups.setdefault(key, []).append({"version": version, **target})
    if len(groups) != 2 or sorted(len(m) for m in groups.values()) != [12, 12]:
        raise AssertionError("Selected egg groups changed")
    output = []
    for (eclass, events), members in sorted(groups.items()):
        ref = members[0]
        proofs = []
        for member in members[1:]:
            equivalent = z3_equivalent(ref["compact"], member["compact"])
            if not equivalent:
                raise AssertionError(f"Z3 disagreement: {ref['id']} vs {member['id']}")
            proofs.append({"reference_id": ref["id"], "member_id": member["id"],
                           "reference_source": ref["source"],
                           "reference_line": ref["line"],
                           "member_source": member["source"],
                           "member_line": member["line"],
                           "equivalent_binary_boolean": True})
        output.append({"eclass": eclass, "event_context": list(events),
                       "case_value": ref["case_value"], "reference_guard": ref["compact"],
                       "member_count": len(members), "pair_proofs": proofs})
    if {row["case_value"] for row in output} != {"2'01", "2'10"} or \
            output[0]["eclass"] == output[1]["eclass"]:
        raise AssertionError("Read and write cases were merged")
    return {"semantics": "two-state combinational Boolean guards only",
            "proof_method": "Z3 independently checks equivalence of each member to its group's reference guard",
            "total_pair_proofs": sum(len(row["pair_proofs"]) for row in output),
            "groups": output,
            "four_state_or_sequential_equivalence_claimed": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    proof = export(args.result)
    args.output.write_text(json.dumps(proof, indent=2) + "\n")
    print(f"Persisted {proof['total_pair_proofs']} Z3 pair proofs: {args.output}")


if __name__ == "__main__":
    main()
