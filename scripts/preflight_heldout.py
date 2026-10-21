"""Reproducible, no-LLM preflight for source-distinct equivalent queue guards."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from coverage import load, summary
from predicates import evaluate, parse
from typed_predicates import extract

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/heldout_queue"
ORIGINAL = EXAMPLE / "rtl/queue.sv"
VARIANT = EXAMPLE / "rtl/queue_variant.sv"
TESTBENCH = EXAMPLE / "verif/tb_queue_preflight.sv"
ENGINE = ROOT / "egraph/target/debug/rtl-predicate-egraph"
OUT = ROOT / "results/heldout_queue_preflight"


def run(argv, logfile=None, *, stdin=None, timeout=120):
    result = subprocess.run([str(x) for x in argv], input=stdin, text=True,
                            capture_output=True, cwd=ROOT, timeout=timeout)
    if logfile:
        logfile.write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv}\n{result.stderr[-1200:]}")
    return result.stdout


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_provenance():
    provenance = json.loads((EXAMPLE / "provenance.json").read_text())
    assert hash_file(ORIGINAL) == provenance["rtl_sha256"]
    assert hash_file(VARIANT) == provenance["variant_sha256"]
    assert hash_file(EXAMPLE / "docs/specification.md") == provenance["spec_sha256"]
    dataset = ROOT / ".cache" / provenance["dataset_file"]
    lock = json.loads((ROOT / "docs/heldout-dataset-lock.json").read_text())
    raw = dataset.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == lock["sha256"]
    record_line = raw.splitlines(keepends=True)[provenance["record_line"] - 1]
    assert hashlib.sha256(record_line).hexdigest() == provenance["record_sha256"]
    record = json.loads(record_line)
    assert record["id"] == provenance["id"]
    assert record["harness"]["src/queue.sv"] == ORIGINAL.read_text()
    assert record["context"]["docs/specs.md"] == (EXAMPLE / "docs/specification.md").read_text()
    return provenance


def bool_to_smt(node):
    if isinstance(node, str): return node
    op = node[0]
    if op == "not": return f"(not {bool_to_smt(node[1])})"
    if op in ("and", "or"): return f"({op} {bool_to_smt(node[1])} {bool_to_smt(node[2])})"
    raise ValueError(op)


def leaves(node):
    if isinstance(node, str): return set() if node in ("true", "false") else {node}
    return set().union(*(leaves(child) for child in node[1:]))


def z3_equivalent(left, right):
    lhs, rhs = parse(left), parse(right)
    declarations = "\n".join(f"(declare-const {atom} Bool)" for atom in sorted(leaves(lhs) | leaves(rhs)))
    script = f"(set-logic QF_UF)\n{declarations}\n(assert (xor {bool_to_smt(lhs)} {bool_to_smt(rhs)}))\n(check-sat)\n"
    answer = run(["z3", "-in"], stdin=script, timeout=10).strip()
    if answer not in ("sat", "unsat"):
        raise RuntimeError(f"unexpected Z3 result: {answer}")
    return answer == "unsat"


def verify_rewrites():
    rules = {
        "de-morgan-or": ("(not (or a b))", "(and (not a) (not b))"),
        "de-morgan-and": ("(not (and a b))", "(or (not a) (not b))"),
        "double-not": ("(not (not a))", "a"),
        "and-true": ("(and a true)", "a"),
        "and-true-left": ("(and true a)", "a"),
        "not-false": ("(not false)", "true"),
    }
    engine_source = (ROOT / "egraph/src/main.rs").read_text()
    proof = {}
    for name, (left, right) in rules.items():
        match = re.search(r'rewrite!\("' + re.escape(name) +
                          r'";\s*"([^"]+)"\s*=>\s*"([^"]+)"\)', engine_source)
        if match is None:
            raise AssertionError(f"rule absent from Rust engine: {name}")
        actual_left = match[1].replace("?a", "a").replace("?b", "b")
        actual_right = match[2].replace("?a", "a").replace("?b", "b")
        if (actual_left, actual_right) != (left, right):
            raise AssertionError(f"Rust rule {name} changed; review and revalidate its exact expression")
        left_ast, right_ast = parse(actual_left), parse(actual_right)
        for a in (False, True):
            for b in (False, True):
                assert evaluate(left_ast, {"a": a, "b": b}) == evaluate(right_ast, {"a": a, "b": b})
        assert z3_equivalent(actual_left, actual_right)
        proof[name] = {"truth_table_rows": 4, "z3_xor": "unsat"}
    return proof


def verify_typed_bitvectors():
    proofs = {}
    for width in (1, 2, 4, 16):
        # The frontend's $ne -> not($eq) bridge is valid for binary vectors
        # of equal width; signedness does not change equality in this case.
        script = (f"(set-logic QF_BV)\n(declare-const a (_ BitVec {width}))\n"
                  f"(declare-const b (_ BitVec {width}))\n"
                  "(assert (xor (not (= a b)) (distinct a b)))\n(check-sat)\n")
        answer = run(["z3", "-in"], stdin=script, timeout=10).strip()
        assert answer == "unsat"
        proofs[str(width)] = "eq/ne complement: unsat XOR"
    script = ("(set-logic QF_BV)\n(declare-const operation (_ BitVec 2))\n"
              "(assert (and (= operation #b01) (= operation #b10)))\n(check-sat)\n")
    assert run(["z3", "-in"], stdin=script, timeout=10).strip() == "unsat"
    proofs["case_01_vs_10"] = "unsat conjunction"
    return proofs


def verify_variant():
    script = (f"read_verilog -sv {ORIGINAL.relative_to(ROOT)} {VARIANT.relative_to(ROOT)}; "
              "proc; opt; memory; opt; async2sync; opt; "
              "equiv_make queue queue_variant equiv; hierarchy -top equiv; "
              "equiv_simple; equiv_induct -seq 4; equiv_status -assert")
    log = run(["yosys", "-Q", "-T", "-p", script], OUT / "variant-equivalence.log", timeout=120)
    match = re.search(r"Of those cells (\d+) are proven and 0 are unproven", log)
    if not match or "Equivalence successfully proven!" not in log:
        raise AssertionError("variant proof did not report every output/state equivalence")
    return {"command": f"yosys -Q -T -p '{script}'", "proven_cells": int(match[1]),
            "async_note": "async2sync is applied to both designs for the sequential SAT proof; both original RTL event sets are separately retained and compared"}


def compile_and_run():
    build = OUT / "verilator-build"
    command = ["verilator", "--binary", "--timing", "--coverage-line", "--coverage-toggle",
               "--coverage-expr", "-Wno-fatal", "-Wno-TIMESCALEMOD", "-Wno-WIDTHEXPAND",
               "--top-module", "tb_queue_preflight", "--Mdir", build, "-j", "2",
               ORIGINAL, VARIANT, TESTBENCH]
    run(command, OUT / "verilator-compile.log", timeout=180)
    coverage = OUT / "coverage.dat"
    output = run([build / "Vtb_queue_preflight", f"+verilator+coverage+file+{coverage}"],
                 OUT / "seed-simulation.log", timeout=30)
    assert "PREFLIGHT_OK cycles=6" in output and coverage.is_file()
    reachability = OUT / "reachability-coverage.dat"
    reach_output = run([build / "Vtb_queue_preflight", "+REACHABILITY",
                        f"+verilator+coverage+file+{reachability}"],
                       OUT / "reachability-simulation.log", timeout=30)
    assert "REACHABILITY_OK extra_cycles=2" in reach_output and reachability.is_file()
    return command, coverage, reachability


def verify_source_and_coverage(extractions, coverage, reachability):
    selected = []
    coverage_summaries = {}
    for extraction, instance in zip(extractions, ("dut", "variant")):
        source = Path(extraction["source"])
        points = load(coverage, str(source.relative_to(ROOT)), instance)
        reached_points = load(reachability, str(source.relative_to(ROOT)), instance)
        coverage_summaries[source.name] = summary(points)
        assert hash_file(source) == extraction["source_sha256"]
        for target in extraction["targets"]:
            if target["guard_depth"] != 4 or target["case_value"] not in ("2'01", "2'10"):
                continue
            line = source.read_text().splitlines()[target["line"]-1]
            literal = target["case_value"].replace("'", "'b")
            assert literal + ":" in line and target["source_mapping"] == "text_literal"
            matches = [point for point in points if point["line"] == target["line"]
                       and point["type"] == "line" and point["outcome"] == "case"]
            if len(matches) != 1:
                raise AssertionError(f"ambiguous or missing coverage source map at {source}:{target['line']}: {matches}")
            if matches[0]["hits"] != 0:
                raise AssertionError(f"preflight target already covered: {source}:{target['line']}")
            reached = [point for point in reached_points if point["line"] == target["line"]
                       and point["type"] == "line" and point["outcome"] == "case"]
            if len(reached) != 1 or reached[0]["hits"] <= 0:
                raise AssertionError(f"target not reached by independent validation: {source}:{target['line']}")
            selected.append({**target, "coverage_point": matches[0]})
    if len(selected) != 24:
        raise AssertionError(f"expected 24 verified source-distinct zero-hit targets, found {len(selected)}")
    return selected, coverage_summaries


def proof_groups(extractions, selected):
    targets = [target for extraction in extractions for target in extraction["targets"]]
    input_rows = [{"id": target["id"], "compact": target["compact"],
                   "expanded": target["compact"]} for target in targets]
    graph = json.loads(run([ENGINE], OUT / "egg.log", stdin=json.dumps(input_rows), timeout=15))
    (OUT / "egg-evidence.json").write_text(json.dumps(graph, indent=2) + "\n")
    roots = {row["id"]: row["eclass"] for row in graph["targets"]}
    grouped = defaultdict(list)
    for target in selected:
        grouped[(tuple(target["event_context"]), roots[target["id"]])].append(target)
    groups = []
    for (event, root), members in grouped.items():
        if len(members) != 12:
            raise AssertionError(f"unexpected group size {len(members)} in egg class {root}")
        base = members[0]
        checks = []
        for target in members[1:]:
            assert z3_equivalent(base["compact"], target["compact"])
            checks.append({"left": base["id"], "right": target["id"], "z3_xor": "unsat"})
        groups.append({"event_context": event, "eclass": root,
                       "case_value": base["case_value"], "members": members,
                       "independent_z3_checks": checks})
    if len(groups) != 2 or len({group["eclass"] for group in groups}) != 2:
        raise AssertionError("read/write outcomes were accidentally merged")
    groups.sort(key=lambda group: group["case_value"])
    # Concrete binary assignment shows 01 and 10 full paths are distinct.
    witness = {"\\rst_ni": 1, "\\clr_i": 0, "\\ena_i": 1,
               "\\we_i": 0, "\\re_i": 1}
    atoms = {}
    for extraction in extractions:
        atoms.update(extraction["atoms"])
    env = {}
    for name, atom in atoms.items():
        if atom["op"] == "nonzero" and atom["signal"] in witness:
            env[name] = bool(witness[atom["signal"]])
        elif atom["op"] == "case_eq" and atom["signal"] == "{ \\we_i \\re_i }":
            env[name] = (atom["value"] == 1)
        else:
            env[name] = False
    read = next(group for group in groups if group["case_value"] == "2'01")
    write = next(group for group in groups if group["case_value"] == "2'10")
    if not evaluate(parse(read["members"][0]["compact"]), env) or evaluate(parse(write["members"][0]["compact"]), env):
        raise AssertionError("read/write separation witness failed")
    return graph, groups, {"binary_inputs": {"rst_ni": 1, "clr_i": 0, "ena_i": 1,
                                              "we_i": 0, "re_i": 1}, "read_guard": True, "write_guard": False}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    provenance = verify_provenance()
    rewrites = verify_rewrites()
    bitvectors = verify_typed_bitvectors()
    variant = verify_variant()
    extractions = [extract(ORIGINAL, "queue"), extract(VARIANT, "queue_variant")]
    for extraction in extractions:
        name = Path(extraction["source"]).stem
        (OUT / f"{name}-typed-extraction.json").write_text(json.dumps(extraction, indent=2) + "\n")
    command, coverage, reachability = compile_and_run()
    selected, coverage_summaries = verify_source_and_coverage(extractions, coverage, reachability)
    graph, groups, non_equivalent_witness = proof_groups(extractions, selected)
    result = {"provenance": provenance, "variant_equivalence": variant,
              "repository": {"head_commit": run(["git", "rev-parse", "HEAD"]).strip(),
                             "worktree_clean": not bool(run(["git", "status", "--porcelain"]).strip())},
              "implementation_hashes": {"testbench_sha256": hash_file(TESTBENCH),
                                        "typed_frontend_sha256": hash_file(ROOT / "scripts/typed_predicates.py"),
                                        "preflight_runner_sha256": hash_file(ROOT / "scripts/preflight_heldout.py"),
                                        "egg_engine_source_sha256": hash_file(ROOT / "egraph/src/main.rs")},
              "rewrite_validation": rewrites,
              "bitvector_validation": bitvectors,
              "extraction": [{"source": item["source"], "source_sha256": item["source_sha256"],
                              "targets": len(item["targets"]), "unsupported": len(item["unsupported"]),
                              "yosys_version": item["yosys_version"]} for item in extractions],
              "preflight_seed": "2 reset cycles, 4 idle cycles; no clear/read/write",
              "separate_reachability_validation": "Independent run appends write-only then read-only cycles; all 24 selected counters have positive hits; actions excluded from model seed",
              "verilator_compile": " ".join(str(x) for x in command),
              "verilator_version": run(["verilator", "--version"]).strip(),
              "z3_version": run(["z3", "-version"]).strip(),
              "iverilog_version": run(["iverilog", "-V"]).splitlines()[0],
              "python_version": sys.version.split()[0],
              "coverage_summary": coverage_summaries,
              "egg": {"engine": graph["engine"], "iterations": graph["iterations"],
                      "stop_reason": graph["stop_reason"]},
              "selected_groups": groups, "read_write_distinction": non_equivalent_witness,
              "selected_zero_hit_source_counters": len(selected)}
    (OUT / "selection.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"selected_groups": [(g["case_value"], len(g["members"])) for g in groups],
                      "zero_hit_counters": len(selected), "coverage": coverage_summaries,
                      "unsupported": [len(item["unsupported"]) for item in extractions]}, indent=2))


if __name__ == "__main__":
    main()
