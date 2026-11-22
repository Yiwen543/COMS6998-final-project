#!/usr/bin/env python3
"""Certify a pinned arbiter branch as infeasible and invalidate the waiver after an RTL edit."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from benchmark_m3_rtl import TB, TOP, raw_dut_hits
from coverage import DUT_SOURCE, load, summary
from m3_guard_inputs import solver_preamble
from m3_proof_dependencies import validate_proof_dependencies
from predicates import DUT, ROOT, fold
from run_step1 import result, write_json


PIN = "52973e366d751c9908ce1354c791b82bb49727d5c777a4369f916031c9815cc7"
OLD = "if (priority_override != 8'b00000000) begin"
NEW = "if ((priority_override != 8'b00000000) || req[7]) begin"
COUNTER = {"f": DUT_SOURCE, "l": "30", "n": "57", "t": "branch", "page": "v_branch/fixed_priority_arbiter",
           "o": "cond_else", "S": "30", "h": "TOP.tb_fixed_priority_arbiter.dut"}
KEY = tuple(sorted(COUNTER.items()))
EVIDENCE_FILES = ("premise.smt2", "premise.z3", "direct.smt2", "direct.z3", "alternate.smt2",
                  "alternate.z3", "egg-input.json", "egg-proof.json")
SCOPE = {"logic": "two-state", "ports": {"reset_pin": 1, "req": 8, "priority_override": 8},
         "process": "posedge clk or posedge reset", "branch_entry": "reset_pin == 0",
         "assumptions": [], "target": "else of the final nested override[7] conditional"}


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def guard(rtl):
    lines = rtl.splitlines()
    require(lines[12].strip() == "always @(posedge clk or posedge reset) begin" and
            lines[13].strip() == "if (reset) begin" and lines[18].strip() == "else begin",
            "event or reset scope changed")
    decisions = {OLD: "override_any", NEW: "(or override_any req7)"}
    condition = decisions.get(lines[19].strip())
    require(condition is not None, "unsupported source decision")
    cascade = "\n".join(lines[22:30])
    bits = re.findall(r"priority_override\[(\d)\] \? 3'd(\d) :", cascade)
    require(bits == [(str(i), str(i)) for i in range(8)] and lines[29].strip().endswith(" : 3'd0);"),
            "ternary priority path changed")
    disjunction = fold("or", [f"override{i}" for i, _ in bits])
    return condition, disjunction


def complete_guard(decision, rejected):
    return f"(and (not reset) (and {decision} (not {rejected})))"


def query_text(expr):
    return solver_preamble() + f"\n(assert {expr})\n(check-sat)\n"


def solve(out, name, expr, z3, *, get_inputs=False):
    script = query_text(expr)
    if get_inputs:
        script += "(get-value (reset_pin req priority_override))\n"
    (out / (name + ".smt2")).write_text(script)
    proc = subprocess.run([z3, "-smt2", "-in"], input=script, text=True, capture_output=True,
                          check=True, timeout=30)
    (out / (name + ".z3")).write_text(proc.stdout)
    lines = proc.stdout.strip().splitlines()
    require(lines and lines[0] in {"sat", "unsat"}, f"{name}: inconclusive Z3 response")
    if not get_inputs:
        require(len(lines) == 1, f"{name}: unexpected output")
        return lines[0], None
    require(lines[0] == "sat", "witness requires SAT")
    values = {k: int(v[2:], 2 if v.startswith("#b") else 16)
              for k, v in re.findall(r"\((reset_pin|req|priority_override)\s+(#[bx][0-9a-fA-F]+)\)", "\n".join(lines[1:]))}
    require(set(values) == set(SCOPE["ports"]), "incomplete SAT model")
    return lines[0], values


def proof_payload(decision, bits, premise_status):
    raw = complete_guard(decision, bits)
    alt = complete_guard(decision, "override_any")
    targets = [{"id": name, "compact": expr, "event_context": SCOPE} for name, expr in (("raw", raw), ("alt", alt))]
    rule = {"name": "override-nonzero", "left": bits, "right": "override_any", "proof_status": premise_status}
    return {"targets": targets, "verified_rules": [rule]}


def run_proof(out, binary, decision, bits, premise_status):
    payload = proof_payload(decision, bits, premise_status)
    raw = payload["targets"][0]["compact"]
    write_json(out / "egg-input.json", payload)
    p = subprocess.run([binary, "indexed"], text=True, input=json.dumps(payload), capture_output=True,
                       timeout=30, check=True)
    graph = json.loads(p.stdout)
    require(json.loads(p.stderr)["mode"] == "indexed" and graph["stop_reason"] == "Some(Saturated)", "egg did not saturate")
    a, b = graph["targets"]
    require([a["id"], b["id"]] == ["raw", "alt"] and a["eclass_before"] != b["eclass_before"] and
            a["eclass"] == b["eclass"], "missing guard merge")
    # Replay the one-step flat proof: the registered oriented rule replaces
    # exactly the rejected-bits OR; the parent activation must stay identical.
    step = complete_guard(decision, "(Rewrite=> override-nonzero override_any)")
    require(graph["rewrite_explanations"] == [{"left": "raw", "right": "alt", "explanation": raw + "\n" + step}],
            "unexpected rule, direction, endpoints, or context in proof")
    # The elapsed time is excluded from the portable certificate.
    del graph["saturation_seconds"]
    write_json(out / "egg-proof.json", graph)


def binding(rtl, point, raw_guard, engine_version):
    return {"rtl_sha256": digest(rtl.encode()), "counter": point, "source_guard": raw_guard, "scope": SCOPE,
            "coverage_tool": engine_version, "hit_threshold": 1, "atom_model_sha256": digest(solver_preamble().encode())}


def check_waiver(waiver_path, candidate_binding, hits):
    """Check a trusted issued waiver against its evidence, new context and live counter."""
    waiver = json.loads(waiver_path.read_bytes())
    issued = waiver["binding"]
    failures = [k for k in sorted(issued.keys() | candidate_binding.keys())
                if k not in issued or k not in candidate_binding or issued[k] != candidate_binding[k]]
    if type(hits) is not int or hits < 0:
        failures.append("invalid DUT counter hits")
    elif hits != 0:
        failures.append("observed target reached hit threshold")

    bits = fold("or", [f"override{i}" for i in range(8)])
    payload = proof_payload("override_any", bits, "unsat")
    direct, alternate = (t["compact"] for t in payload["targets"])
    if (type(waiver["reference_hits"]) is not int or waiver["reference_hits"] != 0 or
            issued.get("rtl_sha256") != PIN or waiver["decision"] != "two-state infeasible" or
            issued.get("counter") != COUNTER or issued.get("scope") != SCOPE or
            issued.get("source_guard") != direct or issued.get("hit_threshold") != 1 or
            issued.get("atom_model_sha256") != digest(solver_preamble().encode())):
        failures.append("unexpected issuance reference")
    digests = waiver["evidence_sha256"]
    if set(digests) != set(EVIDENCE_FILES):
        failures.append("incomplete or unexpected evidence inventory")
    files = {}
    for filename in EVIDENCE_FILES:
        evidence = waiver_path.parent / "original" / filename
        data = evidence.read_bytes() if evidence.is_file() else None
        if data is None or digest(data) != digests.get(filename):
            failures.append("evidence changed: " + filename)
        else:
            files[filename] = data
    if len(files) == len(EVIDENCE_FILES):
        # Hashes detect transport changes. Independently bind the statements,
        # solver outcomes and named proof to the exact claim being reused.
        for name, expr in [("premise", f"(distinct {bits} override_any)"), ("direct", direct), ("alternate", alternate)]:
            if files[name + ".smt2"] != query_text(expr).encode() or files[name + ".z3"].splitlines() != [b"unsat"]:
                failures.append("incorrect query or verdict: " + name)
        try:
            if json.loads(files["egg-input.json"]) != payload:
                raise ValueError("input differs from original guards and certified rule")
            checked = validate_proof_dependencies(payload, json.loads(files["egg-proof.json"]))
            if checked["checked_edges"] != 1 or checked["ground_rules"] != ["override-nonzero"]:
                raise ValueError("missing proof between the original guard and its certified alternate")
        except (ValueError, KeyError, TypeError) as exc:
            failures.append(f"invalid archived proof: {exc}")
    return failures


def replay(out, rtl, vector, verilator):
    with tempfile.TemporaryDirectory(prefix="m3-waiver-") as temp:
        work = Path(temp)
        source = work / DUT_SOURCE
        source.parent.mkdir(parents=True)
        source.write_text(rtl)
        (work / TB).parent.mkdir(parents=True)
        shutil.copyfile(ROOT / TB, work / TB)
        build = work / "obj"
        compile_proc = subprocess.run([verilator, "--cc", "--exe", "--build", "--timing", "--assert",
                                      "--coverage-line", "--coverage-toggle", "--coverage-expr", "--top-module", TOP,
                                      "--Mdir", build, "-j", "2", DUT_SOURCE, TB, ROOT / "scripts/sim_main.cpp"],
                                     cwd=work, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        if compile_proc.returncode:
            (out / "compile.log").write_text(compile_proc.stdout)
            compile_proc.check_returncode()
        (out / "witness.txt").write_text(f"{vector['reset_pin']} {vector['req']:02x} {vector['priority_override']:02x}\n")
        observations = {}
        for mode, name in [(0, "seed"), (1, "witness")]:
            command = [build / ("V" + TOP), f"+MODE={mode}", "+COLLECT", "+VECTORS=witness.txt",
                       f"+verilator+coverage+file+{name}.dat"]
            p = subprocess.run(command, cwd=out, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
            (out / (name + ".log")).write_text(p.stdout)
            p.check_returncode()
            checker = result(p.stdout)
            require(checker["checks"] == 4 + mode, "unexpected replay length")
            path = out / (name + ".dat")
            observations[name] = {"checker": checker, "target_hits": raw_dut_hits(path)[KEY],
                                  "raw_coverage": summary(load(path))}
        return observations


def benchmark(out, binary, z3, verilator):
    original_bytes = DUT.read_bytes()
    require(digest(original_bytes) == PIN, "unknown base DUT")
    original = original_bytes.decode()
    require(original.count(OLD) == 1, "parent decision is not unique")
    edited = original.replace(OLD, NEW)
    baseline_target = raw_dut_hits(ROOT / "results/step1/refined.dat")[KEY]
    require(baseline_target == 0, "archived original target already hit")
    models = {}
    waiver_path = out / "waiver.json"
    solver_version = subprocess.check_output([z3, "--version"], text=True).strip()
    coverage_version = subprocess.check_output([verilator, "--version"], text=True).strip()
    for name, rtl in [("original", original), ("edited", edited)]:
        record = out / name
        record.mkdir()
        decision, bits = guard(rtl)
        raw = complete_guard(decision, bits)
        alt = complete_guard(decision, "override_any")
        context = binding(rtl, COUNTER, raw, coverage_version)
        # Reject the old decision before submitting fresh queries for the edit.
        if name == "edited":
            differences = check_waiver(waiver_path, context, 0)
            require(differences == ["rtl_sha256", "source_guard"], "old waiver failed to invalidate")
        relation, _ = solve(record, "premise", f"(distinct {bits} override_any)", z3)
        require(relation == "unsat", "the ground rewrite lost its certification")
        run_proof(record, binary, decision, bits, relation)
        raw_status, witness = solve(record, "direct", raw, z3, get_inputs=name == "edited")
        alt_status, _ = solve(record, "alternate", alt, z3)
        require(raw_status == alt_status == ("unsat" if name == "original" else "sat"), "raw and transported results differ")
        if name == "original":
            checksums = {f: digest((record / f).read_bytes()) for f in EVIDENCE_FILES}
            write_json(waiver_path, {"binding": context, "decision": "two-state infeasible", "reference_hits": baseline_target,
                                     "evidence_sha256": checksums})
            differences = check_waiver(waiver_path, context, baseline_target)
            require(not differences, "new original certificate does not apply")
        models[name] = {"binding": context, "binding_changes_vs_waiver": differences, "waiver_applies": not differences,
                        "direct_raw": raw_status, "via_egg_alternate": alt_status, "ground_relation": relation,
                        "solver_witness": witness}
    v = models["edited"]["solver_witness"]
    require(v["reset_pin"] == 0 and v["priority_override"] == 0 and v["req"] & 128, "SAT model cannot select edited fallback")
    for name, rtl in [("original", original), ("edited", edited)]:
        observations = replay(out / name, rtl, v, verilator)
        require(observations["seed"]["target_hits"] == 0 and observations["witness"]["target_hits"] == int(name == "edited"),
                "same witness failed target-hit discrimination")
        models[name]["replay"] = observations
        final_check = check_waiver(waiver_path, models[name]["binding"], observations["witness"]["target_hits"])
        require((not final_check) == (name == "original"), "replay and certified waiver disagree")
        models[name]["post_replay_waiver_rejections"] = final_check
    write_json(out / "summary.json", {"models": models, "old_decision": OLD, "new_decision": NEW,
               "archive_sha256": digest((ROOT / "results/step1/refined.dat").read_bytes()),
               "toolchain": {"z3": solver_version, "verilator": coverage_version, "egg_binary_sha256": digest(binary.read_bytes())},
               "physical_replays": 4, "checked_edges": 18})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--output", type=Path, help="new directory for the complete experiment")
    action.add_argument("--check-waiver", type=Path, help="check a trusted waiver.json with --rtl and --coverage")
    parser.add_argument("--rtl", type=Path, help="candidate arbiter source in check mode")
    parser.add_argument("--coverage", type=Path, help="candidate Verilator .dat in check mode")
    parser.add_argument("--binary", type=Path, help="release guard_proofs_fast for the complete experiment")
    parser.add_argument("--verilator", default="verilator")
    parser.add_argument("--z3", default="z3")
    args = parser.parse_args()
    if args.check_waiver:
        if not args.rtl or not args.coverage:
            parser.error("--check-waiver requires --rtl and --coverage")
        rtl = args.rtl.read_bytes().decode()
        decision, bits = guard(rtl)
        version = subprocess.check_output([args.verilator, "--version"], text=True).strip()
        context = binding(rtl, COUNTER, complete_guard(decision, bits), version)
        failures = check_waiver(args.check_waiver, context, raw_dut_hits(args.coverage)[KEY])
        print(json.dumps({"applies": not failures, "rejections": failures}))
        raise SystemExit(int(bool(failures)))
    if not args.binary:
        parser.error("--output requires --binary")
    args.output.mkdir(parents=True, exist_ok=False)
    benchmark(args.output.resolve(), args.binary.resolve(), args.z3, args.verilator)
