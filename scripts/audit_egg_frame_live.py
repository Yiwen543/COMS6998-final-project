#!/usr/bin/env python3
"""Offline audit of completed live frame-monitor feedback and proof records."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import z3

from audit_egg_fifo_live import read_archive, read_json, require
from egg_frame_faults import load_corpus
from egg_frame_llm import ARMS, SCHEMA, SEED, SYSTEM, TASK, _compact_semantic, assess, validate
from egg_frame_observe import score_corpus, tool_feedback
from egg_frame_terms import REFERENCES, evaluate_term, parse_term
from m3_proof_dependencies import validate_proof_dependencies
from predicates import ROOT


def same_json(left, right):
    return json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True)


def verify_query(saved, fresh):
    """Bind archived SMT text to the newly solved query, allowing solver-printer differences."""
    require(saved["status"] == fresh["status"] and saved["status"] in ("sat", "unsat"), "query verdict mismatch")
    first = z3.And(*z3.parse_smt2_string(saved["smt2"]))
    second = z3.And(*z3.parse_smt2_string(fresh["smt2"]))
    solver = z3.Solver()
    solver.set(timeout=5000)
    solver.add(z3.Xor(first, second))
    require(solver.check() == z3.unsat, "archived query differs from reconstructed query")


def verify_semantics(record, fresh, counts):
    for key in ("arm", "reference", "candidate", "equivalent"):
        require(record[key] == fresh[key], f"semantic field {key} changed")
    oracle = record["oracle"]
    verify_query(oracle, fresh["oracle"])
    counts["typed_" + oracle["status"]] += 1
    for key in ("equivalent", "counterexample", "reference_value", "candidate_value"):
        require(record[key] == oracle[key], f"archived oracle projection {key} changed")
    if oracle["status"] == "sat":
        values = record["counterexample"]
        before = evaluate_term(parse_term(record["reference"]), values)
        after = evaluate_term(parse_term(record["candidate"]), values)
        require(before != after and before == record["reference_value"] and after == record["candidate_value"],
                "typed counterexample does not replay")
    else:
        require(record["counterexample"] is None and record["reference_value"] is None and
                record["candidate_value"] is None, "counterexample for UNSAT query")
    require(record["oracle_reused"] is True, "expected the shared oracle protocol")
    if record["arm"] == "raw":
        require(record["proof"] is None and record["evidence"] is None, "unexpected raw proof")
        return

    evidence, expected = record["evidence"], fresh["evidence"]
    for key in ("abstract_terms", "atom_sources", "verified_rules"):
        require(same_json(evidence[key], expected[key]), f"certified abstraction {key} differs")
    pairs = evidence["primitive_pair_checks"]
    for pair, rebuilt in zip(pairs, expected["primitive_pair_checks"], strict=True):
        require({k: v for k, v in pair.items() if k != "queries"}
                == {k: v for k, v in rebuilt.items() if k != "queries"}, "primitive query endpoints changed")
        for query, current in zip(pair["queries"], rebuilt["queries"], strict=True):
            require(query["relation"] == current["relation"], "primitive query relation changed")
            verify_query(query, current)
            counts["primitive_" + query["status"]] += 1
    proof = record["proof"]
    require(proof == fresh["proof"], "proof verdict or steps changed on rerun")
    if record["arm"] == "ordinary":
        verify_query(evidence["abstract_xor"], expected["abstract_xor"])
        counts["ordinary_abstract_" + evidence["abstract_xor"]["status"]] += 1
        for key in ("canonical_keys", "certified_substitution"):
            require(same_json(evidence[key], expected[key]), f"ordinary {key} changed")
    else:
        require(evidence["egg_input"] == expected["egg_input"], "egg input changed")
        graph = evidence["egg_graph"]
        require(graph["stop_reason"] == "Some(Saturated)" and evidence["egg_timing"]["mode"] == "indexed",
                "expected a saturated indexed graph")
        audit = validate_proof_dependencies(evidence["egg_input"], graph)
        first, second = graph["targets"]
        require(audit == evidence["egg_audit"] and (first["eclass"] == second["eclass"]) == proof["proved"],
                "archived egg explanation audit differs")
        steps = [step for edge in audit["edges"] for step in edge["steps"]]
        require(steps == proof["steps"], "archived egg steps differ")
        counts["egg_graphs"] += 1
        counts["egg_named_steps"] += len(steps)


def usage_row(receipt, output_limit):
    source = receipt["usage"]
    result = {key: source[key] for key in ("input_tokens", "output_tokens", "total_tokens")}
    result.update(cached_tokens=source["input_tokens_details"]["cached_tokens"],
                  cache_write_tokens=source["input_tokens_details"]["cache_write_tokens"],
                  reasoning_tokens=source["output_tokens_details"]["reasoning_tokens"])
    details = source["input_tokens_details"]["cache_write_tokens_details"]
    require(all(type(v) is int and v >= 0 for v in (*result.values(), *details.values())) and
            result["input_tokens"] + result["output_tokens"] == result["total_tokens"] and
            result["cached_tokens"] + result["cache_write_tokens"] <= result["input_tokens"] and
            result["cache_write_tokens"] == sum(details.values()) and
            result["reasoning_tokens"] <= result["output_tokens"] <= output_limit, "inconsistent provider token receipt")
    return result


def audit(files, corpus_dir, binary):
    config, summary = (read_json(files, name) for name in ("config.json", "summary.json"))
    rounds = config["rounds_per_arm"]
    require(config["arms"] == list(ARMS) and config["mode"] == summary["mode"] == "live" and
            config["seed"] == SEED and config["visible_designs"] == ["original", "F02", "F05"] and
            type(rounds) is int and 1 <= rounds <= 3 and summary["rounds_per_arm"] == rounds, "bad experiment config")
    corpus = load_corpus(corpus_dir)
    source = json.loads((corpus_dir / "summary.json").read_bytes())
    require(config["corpus_sha256"] == source["corpus_sha256"], "archive and physical corpus differ")
    model, limit = config["provider"]["model"], config["provider"]["max_output_tokens"]
    require(config["provider"]["transport"] == "OpenAI Responses API", "unexpected provider")
    ids, models, tiers = set(), set(), set()
    cached_scores, shared_oracles, matched = {}, {}, {}
    archived_oracles = {}
    verified_candidates, parsed_candidates = set(), set()
    counts = Counter()
    totals, rows_by_arm, seed_grades = {}, {}, {}

    def grade_stage(arm, prefix, monitors):
        key = tuple(monitors[name] for name in REFERENCES)
        if key not in cached_scores:
            cached_scores[key] = score_corpus(corpus, monitors)
        physical = cached_scores[key]
        actual = read_json(files, prefix + "/physical-score.json")
        require(physical == actual, f"{prefix}: physical replay scoring differs")
        counts["physical_score_records"] += 1
        grade, fresh, _ = assess(monitors, binary=binary, arm=arm, physical=physical, common_oracles=shared_oracles)
        saved = read_json(files, prefix + "/semantic.json")
        require(saved.keys() == fresh.keys() == REFERENCES.keys(), f"{prefix}: wrong property inventory")
        for name, record in saved.items():
            verify_semantics(record, fresh[name], counts)
            identity = (name, monitors[name])
            oracle = record["oracle"]
            require(archived_oracles.setdefault(identity, oracle) == oracle, "shared archived oracle changed between arms")
            if arm != "raw":
                nonproof = {k: v for k, v in _compact_semantic(record).items() if k != "proof"}
                packet = {"feedback": nonproof, "rules": record["evidence"]["verified_rules"]}
                require(matched.setdefault(identity, packet) == packet, "common structured evidence changed")
        require(grade == read_json(files, prefix + "/assessment.json"), f"{prefix}: assessment differs")
        packet = {"visible_rtl_observations": tool_feedback(physical)}
        if arm != "raw":
            packet["semantic_and_proof_review"] = {name: _compact_semantic(record) for name, record in saved.items()}
        feedback_text = json.dumps(packet, sort_keys=True, separators=(",", ":"))
        require(files[prefix + "/feedback.txt"].decode() == feedback_text + "\n", f"{prefix}: feedback differs")
        return grade, feedback_text, {name: row["proof"] for name, row in saved.items()}

    for arm in ARMS:
        grade, first_feedback, _ = grade_stage(arm, arm + "/seed", SEED)
        require(grade["inequivalent_properties"] == len(REFERENCES), "frozen seed verification differs")
        seed_grades[arm] = grade
        messages = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": TASK + "\nInitial candidate (provided): " +
                     json.dumps(SEED, sort_keys=True) + "\nInitial tool feedback: " + first_feedback}]
        rows = []
        for turn in range(1, rounds + 1):
            prefix = f"{arm}/round-{turn:02d}"
            request, receipt = (read_json(files, prefix + "/" + name + ".json") for name in ("request", "response"))
            require(request == {"messages": messages, "response_schema": SCHEMA}, f"{prefix}: history differs")
            require(not any(code in json.dumps(messages) for code in ("F01", "F02", "F03", "F04", "F05", "F06")),
                    f"{prefix}: physical fault identifier leaked into prompt")
            require(receipt["id"] not in ids and isinstance(receipt["id"], str) and receipt["id"].startswith("resp_") and
                    receipt["dispatch_attempted"] is True and receipt["http_status"] == 200 and
                    receipt["status"] == "completed" and receipt["requested_model"] == model and
                    isinstance(receipt["model"], str) and receipt["model"], f"{prefix}: bad provider receipt")
            ids.add(receipt["id"])
            models.add(receipt["model"])
            tiers.add(receipt["service_tier"])
            usage = usage_row(receipt, limit)
            output = receipt["output"]
            try:
                monitors = validate(output)
            except ValueError as exc:
                grade = {"candidate_error": str(exc), "verified": False}
                feedback_text = "Invalid candidate: " + str(exc)
                require(read_json(files, prefix + "/assessment.json") == grade and
                        files[prefix + "/feedback.txt"].decode() == feedback_text + "\n" and
                        prefix + "/physical-score.json" not in files and prefix + "/semantic.json" not in files,
                        f"{prefix}: bad invalid-candidate evidence")
                proof, candidate_hash = None, None
                counts["invalid_batches"] += 1
            else:
                grade, feedback_text, proof = grade_stage(arm, prefix, monitors)
                candidate_hash = hashlib.sha256(json.dumps(monitors, sort_keys=True).encode()).hexdigest()
                parsed_candidates.add(candidate_hash)
                if grade["verified"]:
                    verified_candidates.add(candidate_hash)
            messages.extend([{"role": "assistant", "content": json.dumps(output, sort_keys=True)},
                             {"role": "user", "content": feedback_text + "\nSubmit all five monitors again."}])
            rows.append({"assessment": grade, "proof": proof, "candidate_sha256": candidate_hash, "usage": usage,
                         "feedback_utf8_bytes": len(feedback_text.encode())})
        rows_by_arm[arm] = rows
        totals[arm] = {key: sum(row["usage"][key] for row in rows) for key in rows[0]["usage"]}
        grades = [row["assessment"] for row in rows]
        first_pass = next((i for i, grade in enumerate(grades, 1) if grade["verified"]), None)
        require(summary["arms"][arm] == {"rounds": grades, "first_verified_round": first_pass} and
                summary["provider_usage"][arm] == {k: totals[arm][k] for k in
                                                   ("input_tokens", "output_tokens", "total_tokens")},
                f"{arm}: summary disagrees with receipts")
    require(summary["provider_api_calls"] == summary["responses"] == len(ids) == len(ARMS) * rounds and
            models == {summary["model"]} and summary["requested_model"] == model and
            summary["seeds"] == seed_grades, "overall summary differs")
    content_manifest = {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}
    return {"mode": "live_archive_audit", "config": config, "provider_responses_checked": len(ids),
            "returned_model": summary["model"], "reported_service_tiers": sorted(tiers),
            "scores_and_usage": rows_by_arm, "total_usage": totals, "seed_grades": seed_grades,
            "unique_legal_candidates": len(parsed_candidates), "unique_verified_candidates": len(verified_candidates),
            "first_verified_round": {arm: summary["arms"][arm]["first_verified_round"] for arm in ARMS},
            "tokens_to_first_verified": {arm: (
                sum(row["usage"]["total_tokens"] for row in rows_by_arm[arm][:summary["arms"][arm]["first_verified_round"]])
                if summary["arms"][arm]["first_verified_round"] is not None else None) for arm in ARMS},
            "semantic_and_physical_checks": dict(counts), "unique_typed_queries": len(shared_oracles),
            "file_count": len(files), "content_manifest_sha256": hashlib.sha256(
                json.dumps(content_manifest, sort_keys=True).encode()).hexdigest(), "new_api_calls": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--binary", required=True, type=Path, help="release guard_proofs_fast")
    parser.add_argument("--corpus", type=Path, default=ROOT / "results/milestone3/frame-faults")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = audit(read_archive(args.archive), args.corpus, args.binary)
    with args.output.open("x", encoding="utf-8") as file:
        file.write(json.dumps(result, sort_keys=True, indent=2) + "\n")
