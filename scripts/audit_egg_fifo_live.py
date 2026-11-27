#!/usr/bin/env python3
"""Audit an archived completed FIFO Responses experiment without new API calls."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tarfile

from egg_assertion_baseline import truth_table, verify_path
from egg_fifo_assertion_forms import BUDGETS, MAX_TERM_NODES, RULES, SCOPE, disjoin
from egg_fifo_formal import BUNDLED, FAULTS, INPUTS, ROOT, STEPS, digest, input_rows, variants
from egg_fifo_loop import ARMS, SCHEMA, SYSTEM, TASK, assess, validate_revision, visible_only
from egg_fifo_loop_feedback import feedback
from egg_fifo_loop_rtl import candidate_assertions, sample_states
from m3_proof_dependencies import validate_pattern_rules, validate_proof_dependencies
from predicates import evaluate


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_archive(path):
    """Read regular files only; discard Mac Finder/AppleDouble metadata."""
    files = {}
    roots = set()
    total_bytes = 0
    with tarfile.open(path, "r:gz") as archive:
        for member in archive:
            name = PurePosixPath(member.name)
            require(not name.is_absolute() and ".." not in name.parts and name.parts, "unsafe archive path")
            if any(part.startswith("._") or part == ".DS_Store" for part in name.parts):
                continue
            roots.add(name.parts[0])
            if member.isdir():
                continue
            require(member.isfile() and len(name.parts) >= 2, "unexpected archive member")
            relative = "/".join(name.parts[1:])
            total_bytes += member.size
            require(relative not in files and total_bytes <= 32 * 1024 * 1024, "duplicate or oversized archive")
            files[relative] = archive.extractfile(member).read()
    require(len(roots) == 1 and "summary.json" in files and "config.json" in files, "expected one run directory")
    return files


def read_json(files, name):
    return json.loads(files[name])


def checked_semantic(semantic, terms, arm):
    combined = disjoin(terms)
    oracle = truth_table(BUNDLED, combined, max_atoms=5)
    require(oracle["checked_assignments"] == 32 and oracle["stop_reason"] == "exhaustive", "incomplete Boolean audit")
    require(semantic["arm"] == arm and semantic["obligations"] == terms and
            semantic["candidate_union"] == combined and semantic["oracle"] == oracle and
            semantic["equivalent"] == oracle["equivalent"] and
            semantic["counterexample"] == oracle["counterexample"], "archived semantic result differs")
    proof = semantic["proof"]
    evidence = semantic["evidence"]
    if arm == "raw":
        require(proof is None and evidence is None, "unexpected proof in raw arm")
        return None
    if arm == "ordinary":
        require(proof["method"] == "ordinary_bounded_tree_search" and proof["proved"] == evidence["proved"] and
                proof["stop"] == evidence["stop_reason"] and
                proof["budget_distinct_terms"] == evidence["max_terms"] == max(BUDGETS) and
                proof["max_term_nodes"] == evidence["max_term_nodes"] == MAX_TERM_NODES and
                0 <= evidence["visited_terms"] <= evidence["max_terms"], "ordinary search verdict or budget differs")
        steps = evidence["steps"]
        if proof["proved"]:
            require(verify_path(BUNDLED, combined, RULES, steps), "bad ordinary search path")
        else:
            require(not steps, "unproved ordinary search contains a proof")
        steps = [{key: step[key] for key in ("rule", "path", "direction")} for step in steps]
    else:
        payload = {"verified_rules": [], "pattern_rules": RULES, "targets": [
            {"id": "reference", "compact": BUNDLED, "event_context": SCOPE},
            {"id": "candidate", "compact": combined, "event_context": SCOPE},
        ]}
        require(evidence["input"] == payload and proof["method"] == "egg", "egg query not bound to candidate")
        graph = evidence["egg_graph"]
        require(proof["stop"] == graph["stop_reason"] and proof["proved"] == evidence["egg_proved"],
                "egg stop or proof verdict differs")
        steps = []
        if graph["stop_reason"] == "Some(Saturated)":
            audit = validate_proof_dependencies(payload, graph, pattern_rules=RULES)
            first, second = graph["targets"]
            proved = first["eclass"] == second["eclass"]
            require(audit == evidence["egg_audit"] and proved == proof["proved"], "egg proof audit differs")
            steps = [step for edge in audit["edges"] for step in edge["steps"]]
        else:
            require(not proof["proved"] and evidence["egg_audit"] is None, "limited graph credited as a proof")
    require(proof["steps"] == steps and (not proof["proved"] or oracle["equivalent"]), "proof contradicts oracle")
    return {"proved": proof["proved"], "steps": len(steps), "stop": proof["stop"]}


def verify_sampled_pins(waveform, inputs, samples):
    """Recompute the monitor atoms from the VCD's top-level pins at each SMT step."""
    field_ports = {"data_changed": "m_axis_tdata", "last_changed": "m_axis_tlast", "user_changed": "m_axis_tuser"}
    pins = set(INPUTS) | set(field_ports.values()) | {"m_axis_tvalid", "smt_step"}
    scope = []
    identifiers = {}
    values = {}
    states = {}
    for line in waveform.splitlines() + ["#end"]:
        words = line.split()
        if not words:
            continue
        if words[0] == "$scope":
            scope.append(words[2])
        elif words[0] == "$upscope":
            scope.pop()
        elif words[0] == "$var" and scope in ([], ["fifo_stall_formal"]) and words[4] in pins:
            identifiers[words[3]] = words[4]
        elif words[0].startswith("#") and "smt_step" in values:
            states[values["smt_step"]] = dict(values)
        elif words[0].startswith("b") and len(words) == 2 and words[1] in identifiers:
            values[identifiers[words[1]]] = int(words[0][1:], 2)

    for step, (inputs_row, sample) in enumerate(zip(inputs, samples, strict=True)):
        current = states[step]
        require(pins <= current.keys() and {name: current[name] for name in INPUTS} == inputs_row,
                "VCD top-level inputs disagree with the native witness")
        if step == 0:
            require(sample["active"] is False, "first sample unexpectedly has a predecessor")
            continue  # Initial monitor history is unconstrained, masked by active.
        previous = states[step - 1]
        expected = {
            "active": current["rst"] == previous["rst"] == 0 and
                      previous["m_axis_tvalid"] == 1 and previous["m_axis_tready"] == 0,
            "valid_lost": current["m_axis_tvalid"] == 0,
            **{field: current[port] != previous[port] for field, port in field_ports.items()},
        }
        require(expected == sample, "derived FIFO monitor atoms disagree with observed pins")


def checked_rtl(files, prefix, grade, terms, source_hashes, harness_hash, witnesses):
    folder = prefix + "/rtl/"
    trees, assertion_text = candidate_assertions(terms)
    require(grade == read_json(files, folder + "summary.json"), "duplicated RTL result differs")
    require(grade["bounded_states"] == STEPS and grade["obligations"] == terms and
            grade["rtl_sha256"] == source_hashes["original"] and grade["harness_sha256"] == harness_hash and
            grade["assertions_sha256"] == digest(assertion_text.encode()) and
            files[folder + "obligations.svh"].decode() == assertion_text, "RTL/monitor source binding differs")
    require(set(grade["models"]) == set(source_hashes), "RTL grading inventory differs")
    cover = files[folder + "original/cover.log"].decode()
    reached = re.findall(r"Reached cover statement in step (\d+) at fifo_stall_formal: stall_reached", cover)
    require(reached == [str(grade["original_stall_cover_step"])] and cover.rstrip().endswith("Status: PASSED"),
            "missing original stall cover")

    witness_samples = 0
    for design, row in grade["models"].items():
        require(row["rtl_sha256"] == source_hashes[design], "RTL variant hash differs")
        log = files[folder + design + "/smtbmc.log"].decode()
        status = row["status"]
        require(status in ("PASSED", "FAILED") and log.rstrip().endswith(f"Status: {status}"),
                "RTL status differs from SMTBMC")
        expected_end = STEPS - 1 if status == "PASSED" else row["failed_step"]
        require(type(expected_end) is int and 0 <= expected_end < STEPS, "invalid failure step")
        steps = [int(step) for step in re.findall(r"Checking assertions in step (\d+)", log)]
        indices = sorted(int(i) for i in re.findall(r"Assert failed in fifo_stall_formal: check_(\d+)\s*$", log, re.M))
        require(steps == list(range(expected_end + 1)) and indices == row["failed_indices"] and
                all(line in log for line in row["log_excerpt"]), "SMTBMC log trace differs")
        if status == "PASSED":
            require(not indices and row["failed_step"] is None and row["witness"] is None, "inconsistent pass")
            continue
        require(indices and "BMC failed!" in log, "no failing assertion in BMC evidence")
        native_path = design + "/counterexample.yw"
        require(row["witness"] == native_path and row["input_rows"] == design + "/inputs.json" and
                row["waveform"] == design + "/trace.vcd.gz", "unexpected witness artifact path")
        native = files[folder + native_path]
        require(digest(native) == row["witness_sha256"], "YW hash differs")
        inputs = input_rows(json.loads(native))
        require(inputs == read_json(files, folder + row["input_rows"]) and len(inputs) == expected_end + 1,
                "YW inputs disagree with decoded trace")
        waveform = gzip.decompress(files[folder + row["waveform"]]).decode()
        samples = sample_states(waveform, expected_end)
        verify_sampled_pins(waveform, inputs, samples)
        violations = [[i for i, term in enumerate(trees) if evaluate(term, sample)] for sample in samples]
        require(not any(violations[:-1]) and violations[-1] == indices and
                samples[-1] == row["sampled_atoms"], "candidate AST and witness samples disagree")
        witnesses[design].add(digest(native))
        witness_samples += len(samples)
    return witness_samples


def audit(files, rtl):
    config, archived = (read_json(files, x) for x in ("config.json", "summary.json"))
    rounds = config["rounds_per_arm"]
    require(config["mode"] == "live" and config["arms"] == list(ARMS) and type(rounds) is int and 1 <= rounds <= 3,
            "expected a completed live three-arm run")
    require(config["provider"]["transport"] == "OpenAI Responses API", "unexpected provider transport")
    require(archived["mode"] == "live" and archived["rounds_per_arm"] == rounds, "inconsistent run summary")
    requested_model = config["provider"]["model"]
    output_cap = config["provider"]["max_output_tokens"]
    raw_rtl = rtl.read_bytes()
    manifest = json.loads((ROOT / "scripts/m3_controller_replay_manifest.json").read_bytes())
    require(digest(raw_rtl) == manifest["sha256"]["public/rtl/axis_fifo.v"], "unpinned FIFO")
    source_hashes = {name: digest(text.encode()) for name, text in variants(raw_rtl.decode()).items()}
    harness_hash = digest((ROOT / "examples/axis_fifo/formal/stall.sv").read_bytes())
    validate_pattern_rules(RULES)

    ids, model_names, service_tiers = set(), set(), set()
    unique_candidates = set()
    witnesses = {name: set() for name in FAULTS}
    usage, scores = {}, {}
    witness_samples = 0
    for arm in ARMS:
        messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": TASK}]
        usage[arm], scores[arm] = [], []
        previous = None
        for turn in range(1, rounds + 1):
            prefix = f"{arm}/round-{turn:02d}"
            request, response, semantic, grade, assessment = [
                read_json(files, prefix + "/" + name + ".json") for name in
                ("request", "response", "semantic", "rtl-result", "assessment")
            ]
            require(request == {"messages": messages, "response_schema": SCHEMA}, f"{prefix}: wrong history/schema")
            require(response["dispatch_attempted"] is True and response["http_status"] == 200 and
                    response["status"] == "completed" and response["requested_model"] == requested_model and
                    isinstance(response["id"], str) and response["id"].startswith("resp_") and
                    response["id"] not in ids and isinstance(response["model"], str) and response["model"],
                    f"{prefix}: missing or duplicated provider completion receipt")
            ids.add(response["id"])
            model_names.add(response["model"])
            service_tiers.add(response["service_tier"])
            counts = response["usage"]
            keys = ("input_tokens", "output_tokens", "total_tokens")
            require(all(type(counts[key]) is int and counts[key] >= 0 for key in keys) and
                    counts["input_tokens"] + counts["output_tokens"] == counts["total_tokens"] and
                    counts["output_tokens"] <= output_cap, f"{prefix}: invalid token accounting")
            row = {key: counts[key] for key in keys}
            for key, detail in (("cached_tokens", "input_tokens_details"), ("cache_write_tokens", "input_tokens_details"),
                                ("reasoning_tokens", "output_tokens_details")):
                value = counts.get(detail, {}).get(key)
                bound = counts["output_tokens" if detail == "output_tokens_details" else "input_tokens"]
                require(type(value) is int and 0 <= value <= bound, f"{prefix}: missing/bad detail {key}")
                row[key] = value
            usage[arm].append(row)
            output = response["output"]
            validate_revision(output)
            terms = output["obligations"]
            unique_candidates.add(tuple(terms))
            proof = checked_semantic(semantic, terms, arm)
            witness_samples += checked_rtl(files, prefix, grade, terms, source_hashes, harness_hash, witnesses)
            checked_score = assess(semantic, grade, output["diagnosis"], previous)
            require(assessment == checked_score, f"{prefix}: saved grading disagrees")
            visible = visible_only(grade)
            next_feedback = feedback(semantic, visible, arm)
            require(files[prefix + "/feedback.txt"].decode() == next_feedback + "\n", f"{prefix}: bad feedback")
            messages.extend([
                {"role": "assistant", "content": json.dumps(output, sort_keys=True)},
                {"role": "user", "content": next_feedback + "\nSubmit the next complete candidate and diagnosis."},
            ])
            previous = visible
            scores[arm].append({"assessment": checked_score, "proof": proof, "output": output,
                                "feedback_utf8_bytes": len(next_feedback.encode())})

    require(archived["provider_api_calls"] == archived["responses"] == len(ids) == len(ARMS) * rounds and
            archived["requested_model"] == requested_model and model_names == {archived["model"]},
            "overall provider accounting disagreement")
    totals = {arm: {key: sum(row[key] for row in rows) for key in rows[0]} for arm, rows in usage.items()}
    for arm in ARMS:
        arm_scores = [row["assessment"] for row in scores[arm]]
        first_pass = next((i for i, row in enumerate(arm_scores, 1) if row["verified_revision"]), None)
        expected = {
            "rounds": arm_scores, "first_verified_round": first_pass, "final_verified": arm_scores[-1]["verified_revision"],
            "diagnoses_correct": sum(s["diagnosis_correct"] is True for s in arm_scores),
            "diagnoses_eligible": sum(s["diagnosis_correct"] is not None for s in arm_scores),
            "failed_spec_passed_original_count": sum(s["incorrect_assertion_passed_original"] for s in arm_scores),
        }
        require(archived["arms"][arm] == expected and
                archived["provider_usage"][arm] == {k: totals[arm][k] for k in keys}, f"{arm}: summary mismatch")
    content_manifest = {path: hashlib.sha256(data).hexdigest() for path, data in files.items()}
    return {"mode": "live_archive_audit", "config": config, "provider_responses_checked": len(ids),
            "returned_model": archived["model"], "reported_service_tiers": sorted(service_tiers),
            "round_usage": usage, "total_usage": totals, "scores": scores,
            "unique_ordered_candidates": len(unique_candidates), "bmc_logs_checked": len(ids) * len(source_hashes),
            "cover_logs_checked": len(ids), "witness_samples_checked": witness_samples,
            "unique_yw_by_design": {name: len(hashes) for name, hashes in witnesses.items()},
            "file_count": len(files), "content_manifest_sha256": digest(json.dumps(content_manifest, sort_keys=True).encode()),
            "new_api_calls": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--rtl", required=True, type=Path, help="pinned public/rtl/axis_fifo.v")
    parser.add_argument("--output", required=True, type=Path, help="new JSON output file")
    args = parser.parse_args()
    result = audit(read_archive(args.archive), args.rtl)
    with args.output.open("x", encoding="utf-8") as file:
        file.write(json.dumps(result, sort_keys=True, indent=2) + "\n")
