#!/usr/bin/env python3
"""Fixed divider B development or matched A/B/placebo/C experiment."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from coverage import load
from divider_feedback import messages_for
from divider_fixture import schema, validate_actions
from pilot_feedback import point_id
from pilot_model import ModelResponseError, OpenAIModel, ReplayModel, token_estimate, usage_record
from preflight_heldout import verify_rewrites
from preflight_midterm_candidates import semantic_groups
from run_midterm_b_development import KEY_FILE, append
from run_midterm_fixed import ROOT, sha
from run_pilot import versions
from run_divider_fixed import DRIVER, SOURCE, SOURCE_SHA, compile_driver, simulate

DEFAULT_CONFIG = ROOT / "configs/divider_b_development.json"
SEED = ROOT / "configs/divider_seed.json"
SPEC = ROOT / "examples/heldout_divider/docs/specification.md"
SCREEN = ROOT / "results/midterm_candidate_preflight/divider-next/screen.json"


class OfflineMock:
    """Arm-blind legal actions; infrastructure smoke, not LLM evidence."""
    def generate(self, messages, context):
        idle = {"rst_n": 1, "start": 0, "dividend": 55, "divisor": 7}
        round_no, limit = context["round"], context["limit"]
        if round_no == 1:
            actions = [{**idle, "start": 1}] + [idle.copy() for _ in range(limit - 1)]
        else:
            actions = [idle.copy() for _ in range(limit)]
        return {"requested_model": "mock-arm-blind", "returned_model": "mock-arm-blind",
                "response_id": "mock", "latency_seconds": 0.0, "status": "completed",
                "incomplete_details": None, "usage": usage_record(None),
                "output_text": json.dumps({"actions": actions}),
                "parsed": {"actions": actions}}


def points_for(raw):
    return load(raw, str(SOURCE.relative_to(ROOT)), include_descendants=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("mock", "live", "replay"), required=True)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--output", required=True)
    parser.add_argument("--replay-source", help="Calls JSONL from a previous run")
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    config = json.loads(config_path.read_text())
    if (config["model"] != "gpt-6.1-sol" or not config["arms"] or
            len(set(config["arms"])) != len(config["arms"]) or
            any(arm not in ("A", "B", "P", "C") for arm in config["arms"])):
        raise ValueError("Unexpected model or arms")
    if sha(SOURCE) != SOURCE_SHA:
        raise AssertionError("Pinned divider source changed")
    if "primary_target" in config:
        frozen = json.loads((ROOT / "docs/divider-frozen-pilot-2026-10-30.json").read_text())
        for name, expected in frozen["files_sha256"].items():
            if sha(ROOT / name) != expected:
                raise AssertionError(f"Frozen experiment file changed: {name}")
        if config["primary_target"] != frozen["primary_target"]:
            raise AssertionError("Frozen coverage target changed")
    if args.mode == "replay" and not args.replay_source:
        raise ValueError("Replay requires --replay-source")
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    screen = json.loads(SCREEN.read_text())
    if screen["source_sha256"] != SOURCE_SHA:
        raise AssertionError("Semantic preflight source changed")
    hashes = {str(path.relative_to(ROOT)): sha(path) for path in
              (SOURCE, SPEC, DRIVER, SEED, SCREEN, config_path, Path(__file__),
               ROOT / "scripts/divider_feedback.py", ROOT / "scripts/divider_fixture.py")}
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
                            capture_output=True, check=True).stdout.strip()
    (output / "metadata.json").write_text(json.dumps({"mode": args.mode, "commit": commit,
                                                       "hashes": hashes, "versions": versions(),
                                                       "schema": schema(), "limits": config}, indent=2) + "\n")
    rows = []
    try:
        if args.mode == "live":
            if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
                raise RuntimeError("Staged OpenAI key missing or permissions too broad")
            os.environ["OPENAI_API_KEY"] = KEY_FILE.read_text().strip()
        replay = ReplayModel(args.replay_source) if args.mode == "replay" else None
        for arm in config["arms"]:
            for repetition in range(1, config["repetitions"] + 1):
                started = time.perf_counter()
                folder = output / arm / f"rep{repetition}"
                folder.mkdir(parents=True)
                model = (OpenAIModel(config, schema=schema(), schema_name="divider_actions")
                         if args.mode == "live" else replay if replay else OfflineMock())
                binary, compile_command, compile_seconds = compile_driver("verilator", folder)
                seed = validate_actions(json.loads(SEED.read_text()), 10000)
                seed_result = simulate("verilator", binary, seed, folder, "seed")
                if seed_result["checker"]["failures"]:
                    raise AssertionError("Common seed fails independent checker")
                points = points_for(folder / "seed.dat")
                denominator = {point_id(p) for p in points}
                semantic = None
                egg_seconds = 0.0
                if arm in ("P", "C"):
                    egg_start = time.perf_counter()
                    proof = verify_rewrites()
                    semantic_groups(SOURCE, folder / "semantic.json")
                    semantic = json.loads((folder / "semantic.json").read_text())
                    egg_seconds = time.perf_counter() - egg_start
                    (folder / "rewrite-proof.json").write_text(json.dumps(proof, indent=2) + "\n")
                history = []
                prior = seed_result
                last_log = folder / "seed.sim.log"
                calls = failed_attempts = 0
                executions, cycles, tokens = 1, len(seed), 0
                model_seconds = 0.0
                simulation_seconds = seed_result["simulation_seconds"]
                for round_no in range(1, config["rounds"] + 1):
                    messages = messages_for(arm, history, prior, last_log.read_text(),
                                            points, semantic, screen if semantic else None,
                                            round_no, config["max_new_cycles"])
                    accepted = None
                    for attempt in range(1, config["max_retries"] + 2):
                        prompt = folder / f"prompt-{arm}-{round_no}-{attempt}.json"
                        prompt.write_text(json.dumps(messages, indent=2) + "\n")
                        if token_estimate(messages) > config["max_input_tokens_conservative_byte_cap"]:
                            raise RuntimeError("Prompt byte cap exceeded")
                        entry = {"arm": arm, "repetition": repetition, "round": round_no,
                                 "attempt": attempt, "mode": args.mode,
                                 "prompt": str(prompt.relative_to(output)),
                                 "prompt_bytes": token_estimate(messages),
                                 "settings": {key: config[key] for key in
                                              ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds")}}
                        call_start = time.perf_counter()
                        try:
                            calls += 1
                            response = model.generate(messages, {"arm": arm, "repetition": repetition,
                                                                  "round": round_no,
                                                                  "limit": config["max_new_cycles"]})
                            entry.update(response)
                            model_seconds += response["latency_seconds"]
                            usage = response["usage"]
                            if usage["input_tokens"] is not None:
                                tokens += usage["input_tokens"] + usage["output_tokens"]
                            candidate = validate_actions(response["parsed"], config["max_new_cycles"],
                                                         require_initial_reset=False)
                            entry["actions"] = candidate
                            entry["simulated"] = True
                            name = f"round{round_no}-attempt{attempt}"
                            executions += 1
                            cycles += len(seed) + len(history) + len(candidate)
                            sim_start = time.perf_counter()
                            try:
                                candidate_result = simulate("verilator", binary, seed + history + candidate,
                                                            folder, name)
                            finally:
                                simulation_seconds += time.perf_counter() - sim_start
                            candidate_points = points_for(folder / f"{name}.dat")
                            if {point_id(p) for p in candidate_points} != denominator:
                                raise AssertionError("DUT coverage denominator changed")
                            accepted = candidate
                            prior, points = candidate_result, candidate_points
                            last_log = folder / f"{name}.sim.log"
                            entry["accepted"] = True
                        except ModelResponseError as exc:
                            entry.update(exc.record)
                            model_seconds += exc.record["latency_seconds"]
                            usage = exc.record["usage"]
                            if usage["input_tokens"] is not None:
                                tokens += usage["input_tokens"] + usage["output_tokens"]
                            entry["accepted"] = False
                            entry["validation_failure"] = exc.reason
                        except ValueError as exc:
                            entry["accepted"] = False
                            entry["validation_failure"] = str(exc)
                        except AssertionError:
                            raise
                        except Exception as exc:
                            entry["accepted"] = False
                            entry["validation_failure"] = type(exc).__name__
                            entry["http_status"] = getattr(exc, "status_code", None)
                            entry["request_id"] = getattr(exc, "request_id", None)
                        entry["call_wall_seconds"] = time.perf_counter() - call_start
                        if not entry["accepted"]:
                            failed_attempts += 1
                        append(output / "calls.jsonl", entry)
                        if accepted is not None:
                            break
                        messages = [*messages, {"role": "user", "content":
                                                "The response failed validation: " + entry["validation_failure"] +
                                                ". Return only legal JSON actions."}]
                    if accepted is None:
                        terminal = {"arm": arm, "repetition": repetition, "round": round_no,
                                    "status": "no_valid_actions", "coverage": prior["coverage"],
                                    "checker": prior["checker"], "api_tokens": tokens,
                                    "executed_cycles": cycles, "simulator_executions": executions,
                                    "model_calls": calls, "failed_attempts": failed_attempts,
                                    "compile_seconds": compile_seconds,
                                    "simulation_seconds_cumulative": simulation_seconds,
                                    "egraph_preprocessing_seconds": egg_seconds,
                                    "model_seconds_cumulative": model_seconds,
                                    "total_wall_seconds": time.perf_counter() - started}
                        append(output / "rounds.jsonl", terminal)
                        rows.append(terminal)
                        break
                    history.extend(accepted)
                    row = {"arm": arm, "repetition": repetition, "round": round_no,
                           "status": "ok", "coverage": prior["coverage"], "checker": prior["checker"],
                           "api_tokens": tokens, "executed_cycles": cycles,
                           "simulator_executions": executions, "model_calls": calls,
                           "failed_attempts": failed_attempts,
                           "compile_seconds": compile_seconds,
                           "simulation_seconds_cumulative": simulation_seconds,
                           "egraph_preprocessing_seconds": egg_seconds,
                           "model_seconds_cumulative": model_seconds,
                           "total_wall_seconds": time.perf_counter() - started}
                    append(output / "rounds.jsonl", row)
                    rows.append(row)
                    print(f"{arm} rep {repetition} round {round_no}: "
                          f"line {prior['coverage']['line']['covered']}/{prior['coverage']['line']['total']}, "
                          f"branch {prior['coverage']['branch']['covered']}/{prior['coverage']['branch']['total']}, "
                          f"defects {prior['checker']['distinct_defects']}", flush=True)
        (output / "summary.json").write_text(json.dumps({"mode": args.mode,
                                                         "purpose": config["purpose"],
                                                         "rows": rows}, indent=2) + "\n")
    finally:
        os.environ.pop("OPENAI_API_KEY", None)
        if args.mode == "live" and KEY_FILE.exists():
            KEY_FILE.unlink()


if __name__ == "__main__":
    main()
