#!/usr/bin/env python3
"""Use egg to audit alternative encodings of the actual FIFO stall assertion."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from egg_assertion_baseline import compare
from egg_fifo_formal import BUNDLED, SPLIT
from m3_proof_dependencies import validate_pattern_rules, validate_proof_dependencies


RULES = [
    {"name": "and-distribute", "left": "(and ?a (or ?b ?c))",
     "right": "(or (and ?a ?b) (and ?a ?c))"},
    {"name": "de-morgan-or", "left": "(not (or ?a ?b))", "right": "(and (not ?a) (not ?b))"},
    {"name": "de-morgan-and", "left": "(not (and ?a ?b))", "right": "(or (not ?a) (not ?b))"},
    {"name": "double-not", "left": "(not (not ?a))", "right": "?a"},
    {"name": "or-commute", "left": "(or ?a ?b)", "right": "(or ?b ?a)"},
    {"name": "or-associate", "left": "(or (or ?a ?b) ?c)", "right": "(or ?a (or ?b ?c))"},
]
SCOPE = {
    "interface": "axis_fifo.m_axis",
    "sample": "consecutive posedge clk samples; data and handshake observed before the edge",
    "model": "Boolean atoms representing sampled pins and comparisons",
}
BUDGETS = (64, 1024)
MAX_TERM_NODES = 96


def disjoin(terms):
    left, *rest = terms
    return f"(or {left} {disjoin(rest)})" if rest else left


def cases():
    lost, data, last, user = SPLIT
    payload_delta = disjoin(("data_changed", "last_changed", "user_changed"))
    fail = f"(or valid_lost {payload_delta})"
    window = "(and armed (and (not rst_prev) (not rst_now)))"
    stall = "(and valid_prev (not ready_prev))"
    expanded = f"(and (and {window} {stall}) {fail})"
    return {
        # SPLIT is also rendered as four independent assertions in the FIFO harness.
        "split_four_fields": (BUNDLED, disjoin(SPLIT), True),
        "split_balanced": (BUNDLED, f"(or (or {lost} {data}) (or {last} {user}))", True),
        "split_valid_and_payload": (BUNDLED, f"(or {lost} (and active {payload_delta}))", True),
        "negated_implication": (
            BUNDLED, f"(not (or (not active) (and (not valid_lost) (not {payload_delta}))))", True
        ),
        "expanded_trigger_split": (
            expanded, disjoin(term.replace("active", f"(and {window} {stall})") for term in SPLIT), True
        ),
        "omit_last": (BUNDLED, disjoin((lost, data, user)), False),
        "omit_user": (BUNDLED, disjoin((lost, data, last)), False),
        "use_current_ready": (
            expanded, f"(and (and {window} (and valid_prev (not ready_now))) {fail})", False
        ),
        "omit_current_reset": (
            expanded, f"(and (and (and armed (not rst_prev)) {stall}) {fail})", False
        ),
        "require_two_fields": (
            BUNDLED, f"(or {lost} (and {data} (or {last} {user})))", False
        ),
    }


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def checked_egg(binary, lhs, rhs):
    """Run only egg; return proof evidence without running an ordinary baseline."""
    validate_pattern_rules(RULES)
    payload = {"verified_rules": [], "pattern_rules": RULES, "targets": [
        {"id": "reference", "compact": lhs, "event_context": SCOPE},
        {"id": "candidate", "compact": rhs, "event_context": SCOPE},
    ]}
    proc = subprocess.run([binary], input=json.dumps(payload), capture_output=True, text=True, timeout=15)
    if proc.returncode:
        raise RuntimeError(f"egg engine exited {proc.returncode}: {proc.stderr.strip()}")
    graph = json.loads(proc.stdout)
    saturated = graph["stop_reason"] == "Some(Saturated)"
    audit = validate_proof_dependencies(payload, graph, pattern_rules=RULES) if saturated else None
    matched = False
    if saturated:
        first, second = graph["targets"]
        matched = first["eclass"] == second["eclass"]
        needs_rewrite = matched and first["eclass_before"] != second["eclass_before"]
        if needs_rewrite != bool(audit["checked_edges"]):
            raise ValueError("e-class match lacks a checked explanation")
    egg_status = "proved" if matched else "no_proof_at_saturation" if saturated else "limited"
    return {"input": payload, "egg_graph": graph, "egg_audit": audit, "egg_status": egg_status,
            "egg_proved": matched}


def check_candidate(binary, lhs, rhs, expected):
    engine = checked_egg(binary, lhs, rhs)
    baselines = [compare(lhs, rhs, RULES, budget, max_term_nodes=MAX_TERM_NODES)
                 for budget in BUDGETS]
    oracle = baselines[0]["oracle"]
    if oracle["equivalent"] is not expected or any(result["oracle"] != oracle for result in baselines):
        raise ValueError("candidate's independent truth table disagrees with experiment label")
    canonical = baselines[0]["canonical"]
    searches = {str(budget): row["search"] for budget, row in zip(BUDGETS, baselines, strict=True)}
    if not expected and (engine["egg_proved"] or canonical["proved"] or any(s["proved"] for s in searches.values())):
        raise ValueError("a search accepted an inequivalent candidate")
    return {**engine, "canonical": canonical, "tree_search": searches, "independent_oracle": oracle}


def run(binary, out):
    if out.exists() or out.is_symlink():
        raise FileExistsError(out)
    truth_rows = validate_pattern_rules(RULES)
    runs = {}
    for name, (lhs, rhs, expected) in cases().items():
        try:
            runs[name] = check_candidate(binary, lhs, rhs, expected)
        except (KeyError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
            raise ValueError(f"{name}: {exc}") from exc

    certified_split = runs["split_four_fields"]["egg_proved"]
    contract = {"bundled": BUNDLED, "split": list(SPLIT)}
    positives = [row for row in runs.values() if row["independent_oracle"]["equivalent"]]
    summary = {
        "comparison": "FIFO stall violation formula versus one candidate at a time",
        "cases": len(runs), "equivalent": len(positives), "inequivalent": len(runs) - len(positives),
        "proved_equivalent": {
            "egg": sum(row["egg_proved"] for row in positives),
            "ordinary_canonical": sum(row["canonical"]["proved"] for row in positives),
            "ordinary_bidirectional": {str(b): sum(row["tree_search"][str(b)]["proved"] for row in positives)
                                       for b in BUDGETS},
        },
        "false_proofs": 0,
        "formal_split_certified": certified_split,
        "egg_limit_stops": [name for name, row in runs.items() if row["egg_status"] == "limited"],
        "pattern_truth_table_rows": truth_rows,
        "checked_named_egg_steps": sum(row["egg_audit"]["checked_steps"] for row in positives
                                       if row["egg_audit"] is not None),
        "negative_examples": {name: row["independent_oracle"]["counterexample"] for name, row in runs.items()
                              if not row["independent_oracle"]["equivalent"]},
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".egg-fifo-forms-", dir=out.parent) as directory:
        stage = Path(directory) / "verified"
        stage.mkdir()
        for name, evidence in runs.items():
            save(stage / f"{name}.json", evidence)
        if certified_split:
            save(stage / "assertion-contract.json", contract)
        save(stage / "summary.json", summary)
        if out.exists() or out.is_symlink():
            raise FileExistsError(out)
        stage.rename(out)
    if not certified_split:
        raise ValueError("no checked egg proof for the actual four-check RTL assertion")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.binary.resolve(), args.output.resolve())
