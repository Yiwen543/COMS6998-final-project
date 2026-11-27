#!/usr/bin/env python3
"""Matched feedback experiment on typed monitors and actual frame-adjuster observations."""

import argparse
from functools import partial
import json
import os
from pathlib import Path

from egg_fifo_loop_provider import ProviderError, respond
from egg_frame_faults import load_corpus
from egg_frame_observe import parse_monitors, score_corpus, tool_feedback
from egg_frame_proof import review, typed_oracle
from egg_frame_terms import REFERENCES, abstract, parse_term, referenced_signals
from predicates import ROOT


ARMS = ("raw", "ordinary", "egg")
SEED = {
    "data_hold": "(and (and have_prev (and (not prev_rst) (not rst))) "
                 "(and (and prev_m_valid (not m_ready)) "
                 "(or (not m_valid) (or (ne m_data prev_m_data) (ne m_last prev_m_last)))))",
    "header_hold": "(and (and have_prev (and (not prev_rst) (not rst))) "
                   "(and (and prev_h_valid (not prev_h_ready)) "
                   "(or (not h_valid) (or (ne h_pad prev_h_pad) "
                   "(or (ne h_truncate prev_h_truncate) (ne h_length prev_h_length))))))",
    "pad_flag": "(and (and (not rst) h_valid) (xor h_pad (ule h_original_length 4)))",
    "truncate_flag": "(and (and (not rst) h_valid) (xor h_truncate (uge h_original_length 8)))",
    "clamped_length": "(and (and (not rst) h_valid) (ne h_length h_original_length))",
}

SYSTEM = ("You verify the original RTL specification using passive assertion monitors. "
          "Revise the five violation formulas using the feedback; never change the RTL or the specification.")
TASK = """The public frame_task wraps AXI Frame Length Adjuster with an 8-bit data FIFO and a separate header FIFO.
Samples are just before consecutive rising edges. have_prev is false at the first sample. rst is synchronous.
data_hold: if the previous output data sample was valid but not ready, with reset low at both samples, the current sample must preserve m_valid=1, m_data and m_last.
header_hold: the same obligation for h_valid/h_ready, all four header payload fields h_pad,h_truncate,h_length,h_original_length.
pad_flag and truncate_flag: at every valid header presentation outside reset, the pad flag is exactly original_length<4, and truncate flag exactly original_length>8.
clamped_length: at every valid header presentation outside reset, h_length is the original length limited to the inclusive range [4,8].
Write a violation expression for each property: the Boolean result means an assertion fails. Use actual named pins, prefix prev_ for the previous sample, and have_prev.
Boolean operators are binary and, or, xor and unary not. Comparisons eq, ne work for same-typed operands. Unsigned ult, ule, ugt, uge compare same-width buses; decimal literals take the width of the bus operand. Boolean constants are true,false.
Boolean pins: rst,s_valid,s_ready,s_last,m_valid,m_ready,m_last,h_valid,h_ready,h_pad,h_truncate.
Unsigned buses: s_data,m_data (8 bits), h_length,h_original_length (16 bits). The prev_ pins have the same types.
Output all five revised monitors. Candidate alarm samples and transaction checker feedback are from actual observed RTL; an independent specification judge also grades every revision. The two-state symbolic comparison, when supplied, is a semantic comparison and does not on its own establish RTL reachability."""
SCHEMA = {
    "type": "object", "properties": {
        "monitors": {
            "type": "object", "properties": {name: {"type": "string"} for name in REFERENCES},
            "required": list(REFERENCES), "additionalProperties": False,
        },
    }, "required": ["monitors"], "additionalProperties": False,
}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def validate(output):
    if not isinstance(output, dict) or output.keys() != {"monitors"}:
        raise ValueError("reply must be an object with exactly the monitors field")
    terms = parse_monitors(output["monitors"])
    for name, term in terms.items():
        _, atoms = abstract(term)
        if sum(isinstance(atom, tuple) for atom in atoms.values()) > 24:
            raise ValueError(f"{name}: at most 24 distinct primitive comparisons")
    return output["monitors"]


def _compact_semantic(record):
    result = {"equivalent": record["equivalent"], "typed_xor": record["oracle"]["status"]}
    if record["counterexample"] is not None:
        names = referenced_signals(parse_term(record["reference"])) | referenced_signals(parse_term(record["candidate"]))
        result["counterexample"] = {"pins": {name: record["counterexample"][name] for name in sorted(names)},
                                    "reference_violation": record["reference_value"],
                                    "candidate_violation": record["candidate_value"]}
    proof = record["proof"]
    evidence = record["evidence"]
    if proof is not None:
        atoms = evidence["atom_sources"]
        # Both structured arms receive these same leaf-equality statements.
        typed_rules = []
        for rule in evidence["verified_rules"][:8]:
            right = rule["right"]
            right = f"(not {atoms[right[5:-1]]})" if right.startswith("(not ") else atoms[right]
            typed_rules.append({"rule": rule["name"], "left": atoms[rule["left"]], "right": right})
        result["certified_leaf_equalities"] = typed_rules
        result["proof"] = {"method": proof["method"], "proved": proof["proved"], "stop": proof["stop"],
                           "total_steps": len(proof["steps"]), "first_steps": proof["steps"][:4]}
    return result


def assess(monitors, *, binary, arm, physical, common_oracles=None):
    results = {}
    for name, reference in REFERENCES.items():
        candidate = monitors[name]
        common = None
        if common_oracles is not None:
            key = (reference, candidate)
            if key not in common_oracles:
                common_oracles[key] = typed_oracle(reference, candidate)
            common = common_oracles[key]
        results[name] = review(reference, candidate, binary=binary, arm=arm, common=common)
    counts = physical["totals_by_design"]
    reference_faults = [name for name, row in counts.items() if name != "original" and row["reference_alarms"]]
    detected = [name for name in reference_faults if counts[name]["matched_alarms"]]
    grade = {
        "equivalent_properties": sum(row["equivalent"] is True for row in results.values()),
        "inequivalent_properties": sum(row["equivalent"] is False for row in results.values()),
        "unresolved_properties": sum(row["equivalent"] is None for row in results.values()),
        "proofs_found": (sum(row["proof"]["proved"] for row in results.values()) if arm != "raw" else None),
        "reference_detectable_faults": reference_faults,
        "faults_with_matched_alarms": detected,
        "missed_reference_alarms": sum(row["missed"] for row in counts.values()),
        "extra_alarms": sum(row["false_alarm"] for row in counts.values()),
        "unknown_sample_comparisons": sum(row["unknown"] for row in counts.values()),
    }
    grade["verified"] = (grade["equivalent_properties"] == len(REFERENCES) and
                         grade["missed_reference_alarms"] == grade["extra_alarms"] ==
                         grade["unknown_sample_comparisons"] == 0)
    packet = {"visible_rtl_observations": tool_feedback(physical)}
    if arm != "raw":
        packet["semantic_and_proof_review"] = {name: _compact_semantic(row) for name, row in results.items()}
    return grade, results, json.dumps(packet, sort_keys=True, separators=(",", ":"))


def run(*, corpus_dir, binary, out, provider, mode, rounds, provider_config=None):
    if mode not in ("fixture", "live") or not 1 <= rounds <= 3:
        raise ValueError("invalid mode or round count")
    corpus = load_corpus(corpus_dir)
    out.mkdir(parents=True)
    source = json.loads((corpus_dir / "summary.json").read_bytes())
    save(out / "config.json", {"mode": mode, "arms": list(ARMS), "rounds_per_arm": rounds,
                               "provider": provider_config, "corpus_sha256": source["corpus_sha256"],
                               "seed": SEED, "visible_designs": ["original", "F02", "F05"]})
    parse_monitors(SEED)
    cached_scores = {}
    common_oracles = {}
    matched_structured_feedback = {}

    def grade_candidate(monitors, arm, path):
        key = tuple(monitors[name] for name in REFERENCES)
        if key not in cached_scores:
            cached_scores[key] = score_corpus(corpus, monitors)
        physical = cached_scores[key]
        grade, evidence, packet = assess(monitors, binary=binary, arm=arm, physical=physical,
                                         common_oracles=common_oracles)
        save(path / "physical-score.json", physical)
        save(path / "semantic.json", evidence)
        save(path / "assessment.json", grade)
        (path / "feedback.txt").write_text(packet + "\n", encoding="utf-8")
        # Only the proof method may change for an exactly matched candidate.
        if arm != "raw":
            shared = json.loads(packet)["semantic_and_proof_review"]
            for name, detail in shared.items():
                key = (name, monitors[name])
                nonproof = {"feedback": {field: value for field, value in detail.items() if field != "proof"},
                            "rules": evidence[name]["evidence"]["verified_rules"]}
                if matched_structured_feedback.setdefault(key, nonproof) != nonproof:
                    raise ValueError(f"{name}: matched structured arms received different common evidence")
        return grade, packet

    histories, records, seeds = {}, {}, {}
    for arm in ARMS:
        path = out / arm / "seed"
        path.mkdir(parents=True)
        grade, packet = grade_candidate(SEED, arm, path)
        if grade["inequivalent_properties"] != len(REFERENCES):
            raise ValueError("the frozen seed no longer exhibits all five semantic errors")
        seeds[arm] = grade
        histories[arm] = [{"role": "system", "content": SYSTEM},
                          {"role": "user", "content": TASK + "\nInitial candidate (provided): " +
                           json.dumps(SEED, sort_keys=True) + "\nInitial tool feedback: " + packet}]
        records[arm] = []

    seen_ids = set()
    models = set()
    for turn in range(1, rounds + 1):
        offset = (turn - 1) % len(ARMS)
        for arm in ARMS[offset:] + ARMS[:offset]:
            path = out / arm / f"round-{turn:02d}"
            path.mkdir()
            history = histories[arm]
            save(path / "request.json", {"messages": history, "response_schema": SCHEMA})
            try:
                response = provider([dict(message) for message in history], SCHEMA)
            except ProviderError as exc:
                save(path / "provider-error.json", {"error": str(exc), "receipt": exc.receipt})
                raise
            save(path / "response.json", response)
            if not response.get("id") or response["id"] in seen_ids:
                raise ValueError("missing/repeated response ID")
            seen_ids.add(response["id"])
            if (mode == "live") != (response.get("usage") is not None):
                raise ValueError("live usage must be real and fixture must have none")
            if mode == "live":
                models.add((response["requested_model"], response["model"]))
                if len(models) != 1:
                    raise ValueError("models changed within the experiment")
            output = response["output"]
            try:
                monitors = validate(output)
            except ValueError as exc:
                grade = {"candidate_error": str(exc), "verified": False}
                packet = "Invalid candidate: " + str(exc)
                save(path / "assessment.json", grade)
                (path / "feedback.txt").write_text(packet + "\n", encoding="utf-8")
            else:
                grade, packet = grade_candidate(monitors, arm, path)
            history.extend([{"role": "assistant", "content": json.dumps(output, sort_keys=True)},
                            {"role": "user", "content": packet + "\nSubmit all five monitors again."}])
            records[arm].append(grade)

    summary = {"mode": mode, "rounds_per_arm": rounds, "responses": len(seen_ids),
               "provider_api_calls": len(seen_ids) if mode == "live" else 0,
               "seeds": seeds, "arms": {arm: {"rounds": rows, "first_verified_round":
                   next((i for i, row in enumerate(rows, 1) if row["verified"]), None)}
                   for arm, rows in records.items()}}
    if mode == "live":
        summary["requested_model"], summary["model"] = next(iter(models))
        totals = {}
        for arm in ARMS:
            receipts = [json.loads(path.read_bytes())["usage"] for path in sorted((out / arm).glob("round-*/response.json"))]
            totals[arm] = {key: sum(row[key] for row in receipts) for key in ("input_tokens", "output_tokens", "total_tokens")}
        summary["provider_usage"] = totals
    save(out / "summary.json", summary)
    return summary


def fixture_provider():
    """Predefined equivalent candidates; exercises typed leaf certificates, never models learning."""
    calls = 0

    def reply(messages, _schema):
        nonlocal calls
        calls += 1
        turn = len(messages) // 2
        monitors = {name: text.replace("(ult h_original_length 4)", "(ule h_original_length 3)")
                              .replace("(ugt h_original_length 8)", "(uge h_original_length 9)")
                    for name, text in REFERENCES.items()}
        if turn >= 2:
            monitors["clamped_length"] = monitors["clamped_length"].replace(
                "(and (uge h_original_length 4) (ule h_original_length 8))",
                "(not (or (ule h_original_length 3) (uge h_original_length 9)))")
        return {"id": f"fixture-frame-{calls:02d}", "output": {"monitors": monitors}, "usage": None}

    return reply


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=ROOT / "results/milestone3/frame-faults")
    parser.add_argument("--binary", type=Path, required=True, help="release guard_proofs_fast")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rounds", type=int, choices=(1, 2, 3), default=2)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fixture", action="store_true")
    group.add_argument("--live", action="store_true")
    parser.add_argument("--model", help="one model for all three live arms")
    parser.add_argument("--reasoning-effort", choices=("minimal", "low", "medium", "high"))
    parser.add_argument("--max-output-tokens", type=int, default=3072)
    args = parser.parse_args()
    if args.live and (not args.model or not os.environ.get("OPENAI_API_KEY", "").strip()):
        parser.error("--live requires an API model and OPENAI_API_KEY")
    if not 16 <= args.max_output_tokens <= 4096:
        parser.error("--max-output-tokens must be in 16..4096")
    if not args.binary.is_file():
        parser.error("build guard_proofs_fast first")
    provider = partial(respond, model=args.model, max_output_tokens=args.max_output_tokens,
                       reasoning_effort=args.reasoning_effort) if args.live else fixture_provider()
    config = ({"model": args.model, "reasoning_effort": args.reasoning_effort,
               "max_output_tokens": args.max_output_tokens, "transport": "OpenAI Responses API"} if args.live else None)
    result = run(corpus_dir=args.corpus.resolve(), binary=args.binary.resolve(), out=args.output, provider=provider,
                 mode="live" if args.live else "fixture", rounds=args.rounds, provider_config=config)
    print(f"{result['responses']} {result['mode']} responses, {result['provider_api_calls']} provider calls")
