#!/usr/bin/env python3
"""Independently reconstruct a complete matched transaction-monitor synthesis trial."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

import z3

from audit_egg_fifo_live import read_archive, require
from audit_egg_frame_pc import RecordReader, compact, match, receipt_usage
from egg_frame_faults import TRACES, load_corpus
from egg_frame_pc_loop import packet_metrics
from egg_txn_certificate import diagnose, verify_certificate, verify_diagnosis_record
from egg_txn_loop import ARMS, SCHEMA, SYSTEM, TASK, fixture_revision, validate
from egg_txn_observe import COUNTERS, score_corpus
from egg_txn_terms import BOOL_NAMES, BV_WIDTHS, REFERENCES, sample, typed_oracle, validate_snapshot
from predicates import ROOT


TOKEN_FIELDS = ("input_tokens", "output_tokens", "total_tokens")
DEVELOPMENT = (("original", "original"), ("F02", "probe_A"), ("F05", "probe_B"))
PUBLIC_COUNTS = ("reference_alarms", "candidate_alarms", "missed", "false_alarm",
                 "unknown_both", "unknown_mismatch", "ineligible")


def check_model(reference, candidate, receipt, fresh):
    old, new = (z3.parse_smt2_string(record["smt2"]) for record in (receipt, fresh))
    # Keep the reference/candidate XOR bound to these exact endpoints, including
    # when their XOR is UNSAT. The separate domain assertion permits equivalent
    # encodings of the same history constraints (e.g. "= false" versus "not").
    require(len(old) == len(new) == 2 and old[1].eq(new[1]), "wrong transaction XOR endpoints")
    if not old[0].eq(new[0]):
        solver = z3.SolverFor("QF_BV")
        solver.set(timeout=5000)
        solver.add(z3.Xor(old[0], new[0]))
        require(solver.check() == z3.unsat, "changed transaction snapshot domain")
    match(receipt["status"], fresh["status"], "typed program status changed")
    match(receipt["scope"], fresh["scope"], "wrong typed domain scope")
    match(receipt["timeout_ms"], fresh["timeout_ms"], "wrong typed query budget")
    match(receipt["equivalent"], fresh["equivalent"], "inconsistent typed oracle equivalence")
    values = receipt["counterexample"]
    if receipt["status"] != "sat":
        require(all(receipt[k] is None for k in ("counterexample", "reference_value", "candidate_value")),
                "a non-SAT receipt carries a counterexample")
        return None
    require(isinstance(values, dict) and set(values) == set(BOOL_NAMES) | set(BV_WIDTHS),
            "symbolic counterexample must assign every typed pin and ghost field")
    require(all(type(values[n]) is bool for n in BOOL_NAMES) and
            all(type(values[n]) is int and 0 <= values[n] < (1 << width) for n, width in BV_WIDTHS.items()),
            "incomplete two-state assignment or ill-typed symbolic pin")
    validate_snapshot(values)
    left, right = sample(reference, values), sample(candidate, values)
    require(type(left) is bool and type(right) is bool and left != right and
            receipt["reference_value"] is left and receipt["candidate_value"] is right,
            "symbolic counterexample fails independent typed replay")
    return {"origin": "symbolic", "reference_value": left, "candidate_value": right, "values": values}


def common_packet(physical, monitors, symbolic, oracles):
    """Derive public feedback only from the three allowed designs and raw typed snapshots."""
    visible, observed = {}, {}
    for design, alias in DEVELOPMENT:
        cases = [physical["cases"][design][t] for t in TRACES]
        visible[alias] = {"cycles": sum(case["cycles"] for case in cases), "traces": len(cases),
                          "properties": {n: {k: sum(c["properties"][n][k] for c in cases) for k in PUBLIC_COUNTS}
                                         for n in REFERENCES}}
        for trace in TRACES:
            case = physical["cases"][design][trace]
            properties = case["properties"]
            for n, row in properties.items():
                mismatch = row["first_mismatch"]
                if n not in observed and mismatch is not None:
                    observed[n] = {"origin": "physical", "design": alias, "trace": trace, **mismatch}
    selected, review = {}, {}
    for n, reference in REFERENCES.items():
        choice = observed.get(n, symbolic[n])
        selected[n] = choice
        public = None
        if choice is not None:
            left, right = sample(reference, choice["values"]), sample(monitors[n], choice["values"])
            require(left is choice["reference_value"] and right is choice["candidate_value"] and
                    type(left) is bool and type(right) is bool and left != right and oracles[n]["equivalent"] is not True,
                    "selected development observation fails independent replay")
            public = {k: v for k, v in choice.items() if k != "values"}
            public["pins"] = choice["values"]
        review[n] = {"equivalent": oracles[n]["equivalent"], "typed_xor": oracles[n]["status"], "counterexample": public}
    return {"observations": selected, "public": {"visible_rtl_observations": visible, "semantic_review": review}}


def assessment(physical, oracles):
    counts = physical["totals_by_design"]
    totals = {k: sum(c[k] for c in counts.values()) for k in COUNTERS}
    faulty = sorted(name for name, c in counts.items() if name != "original" and c["reference_alarms"])
    votes = [v["equivalent"] for v in oracles.values()]
    return {**totals, "equivalent_properties": votes.count(True), "inequivalent_properties": votes.count(False),
            "unresolved_properties": votes.count(None), "reference_detectable_faults": faulty,
            "matched_reference_faults": [name for name in faulty if counts[name]["matched_alarms"]],
            "verified": all(v is True for v in votes) and not any(totals[k] for k in ("missed", "false_alarm", "unknown_mismatch"))}


class AuditEvidence:
    def __init__(self, corpus_dir):
        self.directory = Path(corpus_dir).resolve()
        self.corpus = load_corpus(self.directory)
        self.digest = json.loads((self.directory / "summary.json").read_bytes())["corpus_sha256"]
        self.scores, self.typed, self.bound, self.diagnoses = {}, {}, {}, {}

    def physical(self, monitors):
        key = compact(monitors)
        if key not in self.scores:
            self.scores[key] = score_corpus(self.corpus, monitors)
        return self.scores[key]

    def symbolic(self, monitors, oracles):
        match(sorted(oracles), sorted(REFERENCES), "incomplete nine-property oracle inventory")
        results = {}
        for n, ref in REFERENCES.items():
            pair = (ref, monitors[n])
            if pair not in self.typed:
                self.typed[pair] = typed_oracle(*pair)
            key = (*pair, compact(oracles[n]))
            if key not in self.bound:
                self.bound[key] = check_model(*pair, oracles[n], self.typed[pair])
            results[n] = self.bound[key]
        return results

    def diagnosis(self, candidate, observation):
        key = (candidate, compact(observation))
        if key not in self.diagnoses:
            self.diagnoses[key] = diagnose(candidate, observation["values"], observation["candidate_value"])
        return self.diagnoses[key]


def audit(files, corpus_dir, *, cache=None):
    data = cache or AuditEvidence(corpus_dir)
    require(data.directory == Path(corpus_dir).resolve(), "wrong physical corpus cache")
    r = RecordReader(files)
    config, summary = r.json("config.json"), r.json("summary.json")
    mode, trials, rounds, provider = (config[k] for k in ("mode", "trials", "repair_rounds", "provider"))
    match(config["schema"], 1, "invalid archive schema")
    require(config["task"] == "frame-transaction-v1" and config["arms"] == list(ARMS) and
            mode in ("fixture", "live") and type(trials) is int and 1 <= trials <= 5 and type(rounds) is int and 1 <= rounds <= 3,
            "invalid task, allocation or budget")
    require(config["corpus_sha256"] == data.digest and re.fullmatch(r"[0-9a-f]{64}", config["binary_sha256"]) and
            config["visible_designs"] == [name for name, _ in DEVELOPMENT], "source or development split mismatch")
    require(mode == "fixture" and provider is None or mode == "live" and isinstance(provider, dict) and
            provider.get("transport") == "OpenAI Responses API" and isinstance(provider.get("model"), str) and provider["model"] and
            type(provider.get("max_output_tokens")) is int and 16 <= provider["max_output_tokens"] <= 4096, "invalid provider configuration")
    matched_oracles, packets, diagnoses = {}, {}, {}
    statuses, seen, models, tiers = Counter(), set(), set(), set()
    totals = {k: Counter() for k in ("initial", *ARMS)}
    sessions, live_costs = {}, {}

    def stage(prefix, arm, output):
        try:
            monitors = validate(output)
        except ValueError as exc:
            grade, text = {"verified": False, "candidate_error": str(exc)}, "Invalid candidate: " + str(exc)
        else:
            physical = data.physical(monitors)
            match(r.json(prefix + "/physical-score.json"), physical, prefix + ": physical scoring changed")
            oracles = r.json(prefix + "/oracles.json")
            symbolic = data.symbolic(monitors, oracles)
            for n, record in oracles.items():
                key = (n, monitors[n])
                match(matched_oracles.setdefault(key, record), record, "same typed candidate received different oracle")
            common = common_packet(physical, monitors, symbolic, oracles)
            match(r.json(prefix + "/common.json"), common, prefix + ": wrong common observations")
            grade = assessment(physical, oracles)
            identity = compact(monitors)
            packet = dict(common["public"])
            match(packets.setdefault(identity, compact(packet)), compact(packet), "common feedback differs for same candidates")
            if arm != "raw":
                records = r.json(prefix + "/diagnoses.json")
                observed = {n: obs for n, obs in common["observations"].items() if obs is not None}
                match(sorted(records), sorted(observed), "wrong diagnosis property inventory")
                for n, obs in observed.items():
                    verify_diagnosis_record(records[n], data.diagnosis(monitors[n], obs))
                public = {n: d["public"] for n, d in records.items()}
                match(diagnoses.setdefault(identity, public), public, "ordinary and egg diagnoses differ for matched candidates")
                packet["candidate_diagnoses"] = public
                if arm == "egg":
                    certs = r.json(prefix + "/certificates.json")
                    match(sorted(certs), sorted(observed), "wrong certificate property inventory")
                    for n, cert in certs.items():
                        verify_certificate(records[n], cert)
                        statuses[cert["public"]["status"]] += 1
                    packet["egg_certificates"] = {n: c["public"] for n, c in certs.items()}
            text = compact(packet)
        match(r.json(prefix + "/assessment.json"), grade, prefix + ": assessment changed")
        require(r.raw(prefix + "/feedback.txt").decode() == text + "\n", prefix + ": feedback differs from public packet")
        return grade, text

    def read_call(prefix, messages, index, turn, arm):
        match(r.json(prefix + "/request.json"), {"messages": messages, "response_schema": SCHEMA},
              prefix + ": request diverges from shared initial and isolated arm history")
        response = r.json(prefix + "/response.json")
        if mode == "fixture":
            expected = {"id": f"fixture-txn-{index:03d}", "output": {"monitors": fixture_revision(turn)},
                        "dispatch_attempted": False, "usage": None}
            match(response, expected, prefix + ": changed deterministic fixture response or invented provider usage")
            require(response["id"] not in seen, "duplicate fixture response")
            seen.add(response["id"])
        else:
            usage = receipt_usage(response, mode, provider, seen)
            totals[arm].update(usage)
            models.add(response["model"])
            if response.get("service_tier"):
                tiers.add(response["service_tier"])
        return response

    blind = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": TASK}]
    delivered = Counter()
    for trial_number in range(1, trials + 1):
        trial = f"trial-{trial_number:02d}"
        call_start = (trial_number - 1) * (1 + len(ARMS) * rounds) + 1
        shared = read_call(trial + "/initial", blind, call_start, 0, "initial")
        shared_grade = r.json(trial + "/initial/assessment.json")
        arms = {}
        if mode == "live":
            live_costs[trial] = {"shared_initial": shared["usage"], "arms": {}}
        for a, arm in enumerate(ARMS):
            base = f"{trial}/{arm}"
            seed, text = stage(base + "/seed", arm, shared["output"])
            match(seed, shared_grade, "unassisted initial response was not identically graded")
            output = shared["output"]
            history, grades, metrics, usage_rows = list(blind), [], [], []
            for turn in range(1, rounds + 1):
                history.extend([{"role": "assistant", "content": json.dumps(output, sort_keys=True)},
                                {"role": "user", "content": text + "\nSubmit all nine monitors again."}])
                metrics.append(packet_metrics(text))
                if arm == "egg":
                    delivered.update({s: metrics[-1][k] for s,k in (
                        ("checked_rewrite", "egg_checked_rewrites"), ("checked_identity", "egg_checked_identities"),
                        ("unavailable", "egg_unavailable"))})
                offset = (trial_number - 1 + turn - 1) % len(ARMS)
                sequence = call_start + 1 + (turn - 1) * len(ARMS) + (a - offset) % len(ARMS)
                prefix = base + f"/round-{turn:02d}"
                receipt = read_call(prefix, history, sequence, turn, arm)
                output = receipt["output"]
                g, text = stage(prefix, arm, output)
                grades.append(g)
                if mode == "live":
                    usage_rows.append({"round": turn, "id": receipt["id"], "service_tier": receipt.get("service_tier"), "usage": receipt["usage"]})
            first = next((i for i, g in enumerate([seed, *grades]) if g["verified"]), None)
            arms[arm] = {"seed": seed, "rounds": grades, "first_verified_round": first, "delivered": metrics}
            if mode == "live":
                incremental = None if first is None else {k: sum(x["usage"][k] for x in usage_rows[:first]) for k in TOKEN_FIELDS}
                inclusive = None if first is None else {k: shared["usage"][k] + incremental[k] for k in TOKEN_FIELDS}
                live_costs[trial]["arms"][arm] = {"rounds": usage_rows, "first_verified_round": first,
                    "incremental_to_first_verified": incremental, "including_initial_to_first_verified": inclusive}
        sessions[trial] = {"initial": shared_grade, "arms": arms}
    require(len(seen) == trials * (1 + len(ARMS)*rounds) and (mode != "live" or len(models) == 1),
            "missing response, duplicate initial accounting or inconsistent live model")
    initial = dict(totals["initial"]) if mode == "live" else None
    incremental = {k: dict(totals[k]) for k in ARMS} if mode == "live" else None
    expected = {"schema": 1, "task": "frame-transaction-v1", "trials": trials, "repair_rounds": rounds, "mode": mode,
                "responses": len(seen), "provider_api_calls": len(seen) if mode == "live" else 0,
                "initial_usage": initial, "provider_usage": incremental, "sessions": sessions}
    if mode == "live":
        expected.update(requested_model=provider["model"], model=next(iter(models)))
    match(summary, expected, "summary differs from independent grading, shared initial calls or provider usage")
    require(r.used == set(files), f"unexpected archive files: {sorted(set(files)-r.used)[:5]}")
    return {"passed": True, "mode": mode, "files": len(r.used), "corpus_sha256": data.digest,
            "binary_sha256": config["binary_sha256"], "trials": trials,
            "shared_initial_responses": trials, "initial_response_deliveries": trials * len(ARMS),
            "intermediate_repair_responses_in_next_request": trials * len(ARMS) * (rounds - 1),
            "response_count": len(seen), "archived_api_calls": expected["provider_api_calls"], "new_api_calls": 0,
            "initially_verified_trials": sum(row["initial"]["verified"] for row in sessions.values()),
            "first_verified_round": {t: {a: s["first_verified_round"] for a,s in rec["arms"].items()} for t,rec in sessions.items()},
            "certificate_records": dict(statuses), "certificates_delivered": dict(delivered),
            "provider_initial_usage": initial, "provider_incremental_usage": incremental,
            "provider_total_counting_initial_once": {k: sum(v[k] for v in totals.values()) for k in TOKEN_FIELDS} if mode == "live" else None,
            "live_session_usage": live_costs if mode == "live" else None,
            "service_tiers": sorted(tiers) if mode == "live" else None, "distinct_valid_candidate_batches": len(packets)}


def read_directory(root):
    files = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(p == ".DS_Store" or p.startswith("._") for p in relative.parts):
            continue
        require(not path.is_symlink() and (path.is_file() or path.is_dir()), "unexpected archive member")
        if path.is_file():
            files[relative.as_posix()] = path.read_bytes()
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--archive", type=Path)
    group.add_argument("--run-dir", type=Path)
    ap.add_argument("--corpus", type=Path, default=ROOT / "results/milestone3/frame-faults")
    ap.add_argument("--output", type=Path, help="write to a new JSON file (default stdout)")
    args = ap.parse_args()
    files = read_directory(args.run_dir) if args.run_dir else read_archive(args.archive)
    report = json.dumps(audit(files, args.corpus), indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as dest:
            dest.write(report)
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
