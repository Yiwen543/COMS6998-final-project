#!/usr/bin/env python3
"""Reconstruct completed proof-carrying frame-monitor conversations without a provider call."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

import z3

from audit_egg_fifo_live import read_archive, require
from egg_fifo_loop_provider import _strict_json
from egg_frame_faults import load_corpus
from egg_frame_llm import validate
from egg_frame_observe import score_corpus
from egg_frame_pc_observation import prepare_common
from egg_frame_proof import typed_oracle
from egg_frame_terms import REFERENCES
from predicates import ROOT


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def match(actual, expected, reason):
    # Distinguish a JSON integer from a Boolean (Python dict equality treats them alike).
    require(compact(actual) == compact(expected), reason)


def bound_query(archived, fresh):
    require(archived["status"] == fresh["status"], "typed XOR status changed")
    # An arbitrary UNSAT query is semantically equal to false, but is not a
    # receipt for the correct endpoints. Compare parsed assertion ASTs, not just
    # whole-query satisfiability. This tolerates SMT whitespace/let printing.
    try:
        old = z3.parse_smt2_string(archived["smt2"])
        new = z3.parse_smt2_string(fresh["smt2"])
        require(len(old) == len(new) and all(a.eq(b) for a, b in zip(old, new)),
                "archived typed XOR is not bound to the candidate")
    except z3.Z3Exception as exc:
        raise ValueError("archived typed XOR is not bound to the candidate") from exc



class AuditEvidence:
    """Memoize independent tool work, keyed by exact terms and supplied witness data."""
    def __init__(self, corpus_dir):
        self.directory = Path(corpus_dir).resolve()
        self.corpus = load_corpus(self.directory)
        self.digest = json.loads((self.directory / "summary.json").read_bytes())["corpus_sha256"]
        self.oracles, self.scores, self.common, self.diagnoses = {}, {}, {}, {}

    def physical(self, monitors):
        key = compact(monitors)
        if key not in self.scores:
            self.scores[key] = score_corpus(self.corpus, monitors)
        return self.scores[key]

    def observations(self, monitors, oracles, physical):
        require(set(oracles) == set(REFERENCES), "wrong typed oracle inventory")
        key = (compact(monitors), compact(oracles))
        if key not in self.common:
            for name, original in oracles.items():
                pair = (REFERENCES[name], monitors[name])
                if pair not in self.oracles:
                    self.oracles[pair] = typed_oracle(*pair)["oracle"]
                bound_query(original, self.oracles[pair])
            # Replays concrete SAT models at full width and searches the frozen,
            # whitelisted development traces before falling back to a symbolic model.
            self.common[key] = prepare_common(monitors, self.corpus, oracles, physical)
        return self.common[key]

    def diagnosis(self, candidate, observation):
        from egg_frame_pc_diagnosis import diagnose
        key = (candidate, compact(observation))
        if key not in self.diagnoses:
            self.diagnoses[key] = diagnose(candidate, observation["values"], observation["candidate_value"])
        return self.diagnoses[key]


def assessment(oracles, physical):
    counts = physical["totals_by_design"]
    detectable = [d for d, r in counts.items() if d != "original" and r["reference_alarms"]]
    result = {"equivalent_properties": sum(r["equivalent"] is True for r in oracles.values()),
              "inequivalent_properties": sum(r["equivalent"] is False for r in oracles.values()),
              "unresolved_properties": sum(r["equivalent"] is None for r in oracles.values()),
              "reference_detectable_faults": detectable,
              "faults_with_matched_alarms": [d for d in detectable if counts[d]["matched_alarms"]],
              "missed_reference_alarms": sum(r["missed"] for r in counts.values()),
              "extra_alarms": sum(r["false_alarm"] for r in counts.values()),
              "unknown_sample_comparisons": sum(r["unknown"] for r in counts.values())}
    result["verified"] = result["equivalent_properties"] == len(REFERENCES) and not any(
        result[k] for k in ("missed_reference_alarms", "extra_alarms", "unknown_sample_comparisons"))
    return result


def receipt_usage(receipt, mode, config, seen):
    identifier = receipt["id"]
    require(isinstance(identifier, str) and identifier and identifier not in seen, "missing or reused response ID")
    seen.add(identifier)
    if mode == "fixture":
        require(re.fullmatch(r"fixture-pc-[0-9]+", identifier) and receipt["usage"] is None and
                receipt["dispatch_attempted"] is False and receipt.get("http_status") is None,
                "fixture receipt claims provider dispatch, tokens or HTTP success")
        return None
    usage = receipt["usage"]
    require(identifier.startswith("resp_") and receipt["requested_model"] == config["model"] and
            isinstance(receipt["model"], str) and receipt["model"] and receipt["status"] == "completed" and
            receipt["http_status"] == 200 and receipt["dispatch_attempted"] is True and isinstance(usage, dict),
            "incomplete live provider receipt")
    tier = receipt.get("service_tier")
    require(tier is None or isinstance(tier, str) and tier, "invalid service tier")
    totals = {k: usage[k] for k in ("input_tokens", "output_tokens", "total_tokens")}
    require(all(type(v) is int and v >= 0 for v in totals.values()) and
            totals["total_tokens"] == totals["input_tokens"] + totals["output_tokens"] and
            totals["output_tokens"] <= config["max_output_tokens"], "invalid live token accounting")
    for details, key, bound in (("input_tokens_details", "cached_tokens", "input_tokens"),
                                ("input_tokens_details", "cache_write_tokens", "input_tokens"),
                                ("output_tokens_details", "reasoning_tokens", "output_tokens")):
        supplied = (usage.get(details) or {}).get(key)
        require(supplied is None or type(supplied) is int and 0 <= supplied <= totals[bound], "bad token subset")
    return totals


class RecordReader:
    def __init__(self, files):
        self.files = files
        self.used = set()

    def raw(self, name):
        require(name in self.files, f"missing {name}")
        self.used.add(name)
        return self.files[name]

    def json(self, name):
        return _strict_json(self.raw(name))


def audit(files, corpus_dir, binary=None, *, cache=None):
    from egg_frame_pc_loop import ARMS, SCHEMA, SYSTEM, TASK, packet_metrics
    from egg_frame_pc_seeds import SEEDS, fixture_revision
    data = cache or AuditEvidence(corpus_dir)
    require(data.directory == Path(corpus_dir).resolve(), "audit cache mismatch")
    r = RecordReader(files)
    config, summary = r.json("config.json"), r.json("summary.json")
    mode = config["mode"]
    certificate_mode = config["certificate_mode"]
    if certificate_mode == "dnf":
        from egg_frame_pc_certificate import verify_certificate
    elif certificate_mode == "cube":
        from egg_frame_pc_cube_certificate import verify_cube_certificate as verify_certificate
    else:
        raise ValueError("unknown certificate mode")
    provider = config["provider"]
    rounds, reps, profiles = config["rounds_per_arm"], config["replicates"], config["profiles"]
    require(type(config["schema"]) is int and config["schema"] == 1 and mode in ("fixture", "live") and config["arms"] == list(ARMS) and
            isinstance(profiles, list) and profiles and len(set(profiles)) == len(profiles) and set(profiles) <= set(SEEDS)
            and type(rounds) is int and 1 <= rounds <= 3 and type(reps) is int and 1 <= reps <= 5, "invalid session allocation")
    match(config["seeds"], {p: SEEDS[p] for p in profiles}, "seed changed")
    require(config["corpus_sha256"] == data.digest and config["visible_designs"] == ["original", "F02", "F05"] and
            re.fullmatch(r"[a-f0-9]{64}", config["diagnostic_binary_sha256"]), "source binding mismatch")
    require((mode == "fixture" and provider is None) or (mode == "live" and isinstance(provider, dict)
            and provider.get("transport") == "OpenAI Responses API" and isinstance(provider.get("model"), str) and provider["model"]
            and type(provider["max_output_tokens"]) is int and 16 <= provider["max_output_tokens"] <= 4096),
            "wrong provider configuration")
    matched_common, matched_diagnoses, matched_oracles = {}, {}, {}
    sessions, certificate_statuses, delivered_statuses = {}, Counter(), Counter()
    ids, models, service_tiers = set(), set(), set()
    totals = {arm: Counter() for arm in ARMS}
    live_session_usage = {} if mode == "live" else None

    def stage(arm, prefix, monitors):
        physical = data.physical(monitors)
        match(r.json(prefix + "/physical-score.json"), physical, prefix + ": physical score differs")
        oracles = r.json(prefix + "/oracles.json")
        common = data.observations(monitors, oracles, physical)
        for name, evidence in oracles.items():
            pair = (REFERENCES[name], monitors[name])
            match(matched_oracles.setdefault(pair, evidence), evidence, "different shared oracle for the same candidate")
        match(r.json(prefix + "/common.json"), common, prefix + ": development observations differ")
        grade = assessment(oracles, physical)
        match(r.json(prefix + "/assessment.json"), grade, prefix + ": assessment differs")
        identity = compact(monitors)
        packet = dict(common["public"])
        match(matched_common.setdefault(identity, packet.copy()), packet, "same candidate received different common feedback")
        if arm != "raw":
            diags = r.json(prefix + "/diagnoses.json")
            expected = {k: data.diagnosis(monitors[k], obs) for k, obs in common["observations"].items() if obs is not None}
            from egg_frame_pc_diagnosis import verify_diagnosis_record
            require(set(diags) == set(expected), prefix + ": diagnosis property inventory changed")
            for k in expected:
                verify_diagnosis_record(diags[k], expected[k])
            public = {k: diag["public"] for k, diag in diags.items()}
            match(matched_diagnoses.setdefault(identity, public), public, "ordinary/egg diagnoses differ for same candidate")
            packet["candidate_diagnoses"] = public
            if arm == "egg":
                certificates = r.json(prefix + "/certificates.json")
                require(set(certificates) == set(expected), prefix + ": certificate property inventory changed")
                for k, cert in certificates.items():
                    verify_certificate(diags[k], cert)
                    certificate_statuses[cert["public"]["status"]] += 1
                packet["egg_certificates"] = {k: cert["public"] for k, cert in certificates.items()}
        text = compact(packet)
        require(r.raw(prefix + "/feedback.txt").decode() == text + "\n", prefix + ": public feedback differs")
        require(not re.search(r"\bF0[1-6]\b", text), prefix + ": raw fault identifier in feedback")
        return grade, text

    for profile_index, profile in enumerate(profiles):
        by_trial = sessions[profile] = {}
        if live_session_usage is not None:
            live_session_usage[profile] = {}
        for trial in range(1, reps + 1):
            trial_id = f"trial-{trial:02d}"
            by_arm = by_trial[trial_id] = {}
            if live_session_usage is not None:
                live_session_usage[profile][trial_id] = {}
            for arm in ARMS:
                base = f"{profile}/{trial_id}/{arm}"
                seed = SEEDS[profile]
                grade0, text = stage(arm, base + "/seed", seed)
                messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": TASK +
                            "\nInitial candidate (provided): " + json.dumps(seed, sort_keys=True) + "\nInitial tool feedback: " + text}]
                grades, delivered, round_usage = [], [], []
                for turn in range(1, rounds + 1):
                    prefix = base + f"/round-{turn:02d}"
                    match(r.json(prefix + "/request.json"), {"messages": messages, "response_schema": SCHEMA},
                          prefix + ": dispatched history does not match own previous candidate and reconstructed feedback")
                    metrics = packet_metrics(text)
                    delivered.append(metrics)
                    if arm == "egg":
                        for status, key in (("checked_rewrite", "egg_checked_rewrites"),
                                            ("checked_identity", "egg_checked_identities"),
                                            ("unavailable", "egg_unavailable")):
                            delivered_statuses[status] += metrics[key]
                    response = r.json(prefix + "/response.json")
                    usage = receipt_usage(response, mode, provider, ids)
                    if mode == "fixture":
                        offset = (profile_index + trial - 1 + turn - 1) % len(ARMS)
                        arm_position = (list(ARMS).index(arm) - offset) % len(ARMS)
                        call_index = (((profile_index * reps + trial - 1) * rounds + turn - 1) * len(ARMS)
                                      + arm_position + 1)
                        require(response["id"] == f"fixture-pc-{call_index:03d}", "unexpected fixture dispatch order")
                        match(response["output"], {"monitors": fixture_revision(profile, turn)}, "changed fixture revision")
                    if usage is not None:
                        totals[arm].update(usage)
                        models.add(response["model"])
                        if response.get("service_tier") is not None:
                            service_tiers.add(response["service_tier"])
                        round_usage.append({"round": turn, "response_id": response["id"],
                                            "service_tier": response.get("service_tier"), "usage": response["usage"]})
                    output = response["output"]
                    try:
                        monitors = validate(output)
                    except ValueError as exc:
                        grade = {"candidate_error": str(exc), "verified": False}
                        text = "Invalid candidate: " + str(exc)
                        match(r.json(prefix + "/assessment.json"), grade, prefix + ": invalid candidate status changed")
                        require(r.raw(prefix + "/feedback.txt").decode() == text + "\n", "invalid-candidate feedback differs")
                    else:
                        grade, text = stage(arm, prefix, monitors)
                    grades.append(grade)
                    messages.extend([{"role": "assistant", "content": json.dumps(output, sort_keys=True)},
                                     {"role": "user", "content": text + "\nSubmit all five monitors again."}])
                first_verified = next((i for i, g in enumerate(grades, 1) if g["verified"]), None)
                by_arm[arm] = {"seed": grade0, "rounds": grades, "delivered": delivered,
                               "first_verified_round": first_verified}
                if live_session_usage is not None:
                    cost = None if first_verified is None else {
                        k: sum(row["usage"][k] for row in round_usage[:first_verified])
                        for k in ("input_tokens", "output_tokens", "total_tokens")}
                    live_session_usage[profile][trial_id][arm] = {
                        "rounds": round_usage, "first_verified_round": first_verified,
                        "usage_to_first_verified": cost}
    require(mode == "fixture" or len(models) == 1, "provider changed model across experimental arms")
    calculated = {"schema": 1, "mode": mode, "certificate_mode": certificate_mode, "profiles": profiles, "replicates": reps, "rounds_per_arm": rounds,
                  "responses": len(ids), "provider_api_calls": len(ids) if mode == "live" else 0, "sessions": sessions,
                  "provider_usage": {arm: dict(totals[arm]) for arm in ARMS} if mode == "live" else None}
    if mode == "live":
        calculated["requested_model"], calculated["model"] = provider["model"], next(iter(models))
    match(summary, calculated, "summary differs from reconstructed sessions or provider receipts")
    require(r.used == set(files), f"unexpected or orphaned transcript artifacts: {sorted(set(files) - r.used)[:5]}")
    return {"passed": True, "mode": mode, "certificate_mode": certificate_mode, "profiles": profiles, "sessions": len(profiles) * reps * len(ARMS),
            "responses": len(ids), "responses_consumed_in_next_request": len(profiles) * reps * len(ARMS) * (rounds - 1),
            "provider_api_calls_in_archive": calculated["provider_api_calls"], "provider_usage": calculated["provider_usage"],
            "live_session_usage": live_session_usage, "reported_service_tiers": sorted(service_tiers) if mode == "live" else None,
            "distinct_candidate_batches": len(matched_common), "distinct_structured_diagnoses": len(matched_diagnoses),
            "certificate_record_statuses": dict(certificate_statuses), "delivered_certificate_statuses": dict(delivered_statuses),
            "physical_corpus_sha256": data.digest,
            "certificates_replayed": certificate_statuses["checked_rewrite"] + certificate_statuses["checked_identity"],
            "archived_diagnostic_binary_sha256": config["diagnostic_binary_sha256"],
            "local_binary_sha256": hashlib.sha256(Path(binary).read_bytes()).hexdigest() if binary else None,
            "audited_files": len(r.used), "new_api_requests": 0}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--archive", type=Path)
    source.add_argument("--run-dir", type=Path)
    ap.add_argument("--corpus", type=Path, default=ROOT / "results/milestone3/frame-faults")
    ap.add_argument("--binary", type=Path, help="optionally record the local engine's SHA-256 (the audit replays archived proofs without it)")
    ap.add_argument("--output", type=Path, help="new JSON file (default stdout)")
    args = ap.parse_args()
    if args.run_dir:
        files = {}
        for p in args.run_dir.rglob("*"):
            relative = p.relative_to(args.run_dir)
            if any(part == ".DS_Store" or part.startswith("._") for part in relative.parts):
                continue
            require(not p.is_symlink() and (p.is_dir() or p.is_file()), "unexpected non-regular transcript member")
            if p.is_file():
                files[relative.as_posix()] = p.read_bytes()
    else:
        files = read_archive(args.archive)
    report = json.dumps(audit(files, args.corpus, args.binary), indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as out:
            out.write(report)
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
