#!/usr/bin/env python3
"""Run three isolated feedback arms on the same AXI-stream FIFO specification."""

import argparse
from functools import partial
import json
import os
from pathlib import Path
import shutil

from egg_fifo_formal import FAULTS, ROOT, SPLIT, digest
from egg_fifo_loop_feedback import feedback, review, validate_obligations
from egg_fifo_loop_provider import ProviderError, respond
from egg_fifo_loop_rtl import grade_rtl


ARMS = ("raw", "ordinary", "egg")
VISIBLE = ("original", "flip_last")
SYSTEM = (
    "Produce passive verification assertions, not changes to the RTL. "
    "Treat tool messages as observations. Follow the FIFO specification even if a weak assertion passes."
)
TASK = """Write one to four Boolean violation formulas for a pinned AXI-stream FIFO at consecutive samples before clock rising edges.
When the previous sample had TVALID=1 and TREADY=0, and neither sample is in reset, the current sample must keep TVALID=1 and keep TDATA, TLAST and TUSER unchanged. The first sample has no predecessor.
Use binary (and A B), binary (or A B) and unary (not A). The only atoms are active (the trigger specified above), valid_lost (current TVALID is 0), data_changed, last_changed and user_changed (the indicated payload field differs from the previous sample). A candidate fails when ANY of its violation formulas is true.
On the first turn report diagnosis.field="none", diagnosis.step=-1. In subsequent turns, report the field and zero-based sample for a known violation of the diagnostic probe using the previous tool feedback. If it does not establish a field and sample, use "none" and -1. Keep the assertions faithful to the specification in every turn."""
FIELDS = ("none", "TVALID", "TDATA", "TLAST", "TUSER")
SCHEMA = {
    "type": "object",
    "properties": {
        "obligations": {"type": "array", "items": {"type": "string"}},
        "diagnosis": {
            "type": "object",
            "properties": {"field": {"type": "string", "enum": list(FIELDS)}, "step": {"type": "integer"}},
            "additionalProperties": False,
            "required": ["field", "step"],
        },
    },
    "additionalProperties": False,
    "required": ["obligations", "diagnosis"],
}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def visible_only(grade):
    return {
        "bounded_states": grade["bounded_states"],
        "obligations": grade["obligations"],
        "models": {name: grade["models"][name] for name in VISIBLE},
    }


def validate_revision(output):
    if not isinstance(output, dict) or output.keys() != {"obligations", "diagnosis"}:
        raise ValueError("reply must contain obligations and diagnosis")
    diagnosis = output["diagnosis"]
    if not isinstance(diagnosis, dict) or diagnosis.keys() != {"field", "step"}:
        raise ValueError("diagnosis must contain field and step")
    field, step = diagnosis["field"], diagnosis["step"]
    if field not in FIELDS or type(step) is not int or (field == "none" and step != -1) or (
            field != "none" and step < 0):
        raise ValueError("diagnosis must use a named field with a zero-based step, or none with -1")
    validate_obligations(output["obligations"])


def assess(review_result, rtl_result, diagnosis, previous):
    models = rtl_result["models"]
    if set(models) != {"original", *FAULTS} or any(
            model["status"] not in ("PASSED", "FAILED") for model in models.values()):
        raise ValueError("RTL grader did not return a full set of conclusive statuses")
    original_passed = models["original"]["status"] == "PASSED"
    failed = sorted(fault for fault in FAULTS if models[fault]["status"] == "FAILED")
    caught = failed if original_passed else []
    diagnostic_step = None
    if previous and previous["models"]["original"]["status"] == "PASSED":
        probe = previous["models"]["flip_last"]
        atoms = probe.get("sampled_atoms") or {}
        if probe["status"] == "FAILED" and atoms.get("active") is True and atoms.get("last_changed") is True:
            diagnostic_step = probe["failed_step"]
    return {
        "equivalent": review_result["equivalent"],
        "original_bmc_passed": original_passed,
        "faults_failed": failed,
        "faults_caught": caught,
        "incorrect_assertion_passed_original": review_result["equivalent"] is False and original_passed,
        "verified_revision": review_result["equivalent"] is True and original_passed and len(caught) == len(FAULTS),
        "diagnosis_correct": (diagnosis == {"field": "TLAST", "step": diagnostic_step}
                              if diagnostic_step is not None else None),
        "diagnosis_unsupported": diagnostic_step is None and diagnosis["field"] != "none",
    }


def run_loop(*, rtl, binary, out, max_rounds, provider, grade=None, provider_mode="fixture", provider_config=None):
    if not 1 <= max_rounds <= 3 or provider_mode not in ("fixture", "live"):
        raise ValueError("expect one to three rounds and a known provider mode")
    grade = grade_rtl if grade is None else grade
    out.mkdir(parents=True)
    save(out / "config.json", {"mode": provider_mode, "arms": list(ARMS), "rounds_per_arm": max_rounds,
                                "provider": provider_config})
    histories = {arm: [{"role": "system", "content": SYSTEM}, {"role": "user", "content": TASK}]
                 for arm in ARMS}
    outcomes = {arm: [] for arm in ARMS}
    previous_visible = dict.fromkeys(ARMS)
    seen_ids = set()
    live_model = None
    for turn in range(1, max_rounds + 1):
        offset = turn - 1
        for arm in ARMS[offset:] + ARMS[:offset]:
            stage = out / arm / f"round-{turn:02d}"
            stage.mkdir(parents=True)
            messages = histories[arm]
            save(stage / "request.json", {"messages": messages, "response_schema": SCHEMA})
            try:
                response = provider([dict(message) for message in messages], SCHEMA)
            except ProviderError as exc:
                save(stage / "provider-error.json", {"error": str(exc), "receipt": exc.receipt})
                raise
            save(stage / "response.json", response)
            if not response.get("id") or response["id"] in seen_ids:
                raise ValueError("missing or repeated response ID")
            seen_ids.add(response["id"])
            if (provider_mode == "live") != (response.get("usage") is not None):
                raise ValueError("live usage is required and synthetic usage is prohibited")
            if provider_mode == "live":
                model_pair = response["requested_model"], response["model"]
                if live_model is not None and live_model != model_pair:
                    raise ValueError("provider model changed within the comparison")
                live_model = model_pair

            output = response["output"]
            try:
                validate_revision(output)
            except ValueError as exc:
                assessment = {"candidate_error": str(exc), "verified_revision": False, "diagnosis_correct": None}
                previous_visible[arm] = None
                next_feedback = "Invalid candidate. " + str(exc)
            else:
                terms = output["obligations"]
                semantic = review(terms, binary=binary, arm=arm)
                rtl_result = grade(rtl, terms, stage / "rtl")
                visible = visible_only(rtl_result)
                assessment = assess(semantic, rtl_result, output["diagnosis"], previous_visible[arm])
                save(stage / "semantic.json", semantic)
                save(stage / "rtl-result.json", rtl_result)
                next_feedback = feedback(semantic, visible, arm)
                previous_visible[arm] = visible
            save(stage / "assessment.json", assessment)
            (stage / "feedback.txt").write_text(next_feedback + "\n", encoding="utf-8")
            outcomes[arm].append(assessment)
            messages.extend([
                {"role": "assistant", "content": json.dumps(output, sort_keys=True)},
                {"role": "user", "content": next_feedback + "\nSubmit the next complete candidate and diagnosis."},
            ])

    summary = {
        "mode": provider_mode,
        "rounds_per_arm": max_rounds,
        "responses": len(seen_ids),
        "provider_api_calls": len(seen_ids) if provider_mode == "live" else 0,
        "arms": {
            arm: {
                "rounds": assessments,
                "first_verified_round": next((index for index, value in enumerate(assessments, 1)
                                              if value["verified_revision"]), None),
                "failed_spec_passed_original_count": sum(
                    value.get("incorrect_assertion_passed_original", False) for value in assessments
                ),
                "final_verified": assessments[-1]["verified_revision"],
                "diagnoses_correct": sum(value["diagnosis_correct"] is True for value in assessments),
                "diagnoses_eligible": sum(value["diagnosis_correct"] is not None for value in assessments),
            }
            for arm, assessments in outcomes.items()
        },
    }
    if provider_mode == "live":
        summary["requested_model"], summary["model"] = live_model
        summary["provider_usage"] = {}
        for arm in ARMS:
            receipts = [json.loads(path.read_bytes()) for path in sorted((out / arm).glob("round-*/response.json"))]
            summary["provider_usage"][arm] = {
                key: sum(row["usage"][key] for row in receipts)
                for key in ("input_tokens", "output_tokens", "total_tokens")
            }
    save(out / "summary.json", summary)
    return summary


def fixture_provider():
    calls = 0

    def next_fixture(messages, _schema):
        nonlocal calls
        calls += 1
        turn = len(messages) // 2
        # The scripted reply sequence is identical for all arms, by construction.
        obligations = [term for term in SPLIT if term != "(and active last_changed)"] if turn == 1 else list(SPLIT)
        diagnosis = {"field": "TLAST", "step": 5} if turn >= 3 else {"field": "none", "step": -1}
        return {"id": f"fixture-{calls:02d}", "output": {"obligations": obligations, "diagnosis": diagnosis},
                "usage": None, "model": None}

    return next_fixture


def preflight(rtl, binary):
    manifest = json.loads((ROOT / "scripts/m3_controller_replay_manifest.json").read_bytes())
    if not rtl.is_file() or digest(rtl.read_bytes()) != manifest["sha256"]["public/rtl/axis_fifo.v"]:
        raise ValueError("supply the hash-pinned public/rtl/axis_fifo.v fixture")
    if not binary.is_file() or not os.access(binary, os.X_OK):
        raise ValueError("build egg_assertion_forms and supply its executable path")
    missing = [name for name in ("yosys", "yosys-smtbmc", "z3") if not shutil.which(name)]
    if missing:
        raise ValueError("missing local tools: " + ", ".join(missing))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--rtl", required=True, type=Path)
    cli.add_argument("--binary", required=True, type=Path)
    cli.add_argument("--output", required=True, type=Path)
    cli.add_argument("--rounds", type=int, choices=range(1, 4), default=3)
    mode = cli.add_mutually_exclusive_group(required=True)
    mode.add_argument("--fixture", action="store_true", help="scripted responses, real local tools, no API")
    mode.add_argument("--live", action="store_true", help="up to nine real Responses API calls")
    cli.add_argument("--model", help="required for --live; same model for all arms")
    cli.add_argument("--reasoning-effort", choices=("minimal", "low", "medium", "high"),
                     help="reasoning setting for all live arms; omit for the provider default")
    cli.add_argument("--max-output-tokens", type=int, default=1024, help="live cap per response")
    args = cli.parse_args()
    if args.live and (not args.model or not os.environ.get("OPENAI_API_KEY", "").strip()):
        cli.error("--live requires --model and OPENAI_API_KEY in the environment")
    if args.fixture and args.reasoning_effort is not None:
        cli.error("--reasoning-effort applies to --live only")
    if not 16 <= args.max_output_tokens <= 4096:
        cli.error("--max-output-tokens must be in 16..4096")
    try:
        preflight(args.rtl, args.binary)
    except ValueError as exc:
        cli.error(str(exc))
    provider = (partial(respond, model=args.model, max_output_tokens=args.max_output_tokens,
                        reasoning_effort=args.reasoning_effort)
                if args.live else fixture_provider())
    provider_config = ({"transport": "OpenAI Responses API", "model": args.model,
                        "max_output_tokens": args.max_output_tokens, "reasoning_effort": args.reasoning_effort}
                       if args.live else None)
    result = run_loop(rtl=args.rtl.resolve(), binary=args.binary.resolve(), out=args.output,
                      max_rounds=args.rounds, provider=provider, provider_mode="live" if args.live else "fixture",
                      provider_config=provider_config)
    print(f"{result['responses']} {result['mode']} responses, {result['provider_api_calls']} provider calls")
