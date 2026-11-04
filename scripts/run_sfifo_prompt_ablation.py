#!/usr/bin/env python3
"""Exploratory matched B-full/B-compact/placebo/C-compact FIFO prompt ablation."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from coverage import load
from pilot_feedback import point_id
from pilot_model import ModelResponseError, OpenAIModel, ReplayModel, token_estimate, usage_record
from run_midterm_b_development import KEY_FILE, append
from run_midterm_fixed import ROOT, sha
from run_pilot import versions
from run_sfifo_stress_fixed import SOURCE, compile_driver, simulate
from sfifo_fixture import schema, validate_actions
from sfifo_prompt_ablation_feedback import messages_for
from token_placebo import match_placebo

CONFIG = ROOT / "configs/sfifo_prompt_ablation_exploratory.json"
SEED = ROOT / "configs/sfifo_stress_seed.json"
SEMANTIC = ROOT / "results/sfifo_prompt_ablation_preflight/semantic.json"
SELECTION = ROOT / "results/sfifo_prompt_ablation_preflight/selection.json"
ARMS = ("B_full", "B_compact", "P_compact", "C_compact")


def points_for(raw: Path):
    return load(raw, str(SOURCE.relative_to(ROOT)), include_descendants=True)


def target_hits(points: list[dict], config: dict) -> list[dict]:
    target = config["primary_target"]
    hits = []
    for line in target["source_lines"]:
        rows = [point for point in points if point["line"] == line and
                point["type"] == target["counter_type"] and
                point["outcome"] == target["outcome"]]
        if len(rows) != 1:
            raise AssertionError(f"Target has {len(rows)} original counters at source line {line}")
        hits.append({"line": line, "hits": rows[0]["hits"]})
    return hits


class OfflineMock:
    def generate(self, _messages, context):
        # Arm-blind infrastructure smoke; never labeled as model evidence.
        idle = {"reset": 0, "wr": 0, "rd": 0, "data": 0}
        actions = [{**idle, "wr": 1, "data": 55}] + [idle.copy() for _ in range(context["limit"] - 1)]
        return {"requested_model": "mock", "returned_model": "mock",
                "response_id": f"mock-{context['repetition']}-{context['round']}",
                "latency_seconds": 0.0, "status": "completed", "incomplete_details": None,
                "usage": usage_record(None), "output_text": json.dumps({"actions": actions}),
                "parsed": {"actions": actions}}


def validate_lock(config: dict, semantic: dict) -> dict:
    if config["model"] != "gpt-6.1-sol" or tuple(config["arms"]) != ARMS:
        raise ValueError("Unexpected model or exploratory arm order")
    lock = json.loads(SELECTION.read_text())
    if lock["config"] != config or sha(SOURCE) != lock["source_sha256"]:
        raise AssertionError("Preflight/config/source differs from exploratory lock")
    for relative, expected in lock["files_sha256"].items():
        if sha(ROOT / relative) != expected:
            raise AssertionError(f"Preflight hash changed: {relative}")
    if semantic["source_sha256"] != sha(SOURCE):
        raise AssertionError("Semantic extraction source differs from DUT")
    return lock


def make_prompt(arm, history, prior, log, points, semantic, round_no, config,
                model, mode):
    if arm == "P_compact":
        c_messages = messages_for("C_compact", history, prior, log, points,
                                  semantic, round_no, config["max_new_cycles"])
        if mode == "live":
            return match_placebo(c_messages, model.count_input_tokens,
                                 tolerance=config["placebo_tolerance_tokens"]), c_messages
        return match_placebo(c_messages, lambda messages: sum(len(m["content"]) for m in messages),
                             tolerance=2), c_messages
    return (messages_for(arm, history, prior, log, points, semantic,
                         round_no, config["max_new_cycles"]), None), None


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--mode", choices=("mock", "live", "replay"), required=True)
    cli.add_argument("--output", required=True)
    cli.add_argument("--replay-source")
    args = cli.parse_args()
    if args.mode == "replay" and not args.replay_source:
        raise ValueError("Replay requires --replay-source")
    config = json.loads(CONFIG.read_text())
    semantic = json.loads(SEMANTIC.read_text())
    lock = validate_lock(config, semantic)
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    (output / "metadata.json").write_text(json.dumps({"mode": args.mode,
        "purpose": config["purpose"], "commit": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True,
            check=True).stdout.strip(), "versions": versions(),
        "selection_sha256": sha(SELECTION), "files_sha256": lock["files_sha256"],
        "schema": schema(), "limits": config}, indent=2) + "\n")
    if args.mode == "live":
        if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
            raise RuntimeError("Staged OpenAI key missing or permissions too broad")
        os.environ["OPENAI_API_KEY"] = KEY_FILE.read_text().strip()
    rows = []
    try:
        replay = ReplayModel(args.replay_source) if args.mode == "replay" else None
        for arm in ARMS:
            for repetition in range(1, config["repetitions"] + 1):
                started = time.perf_counter()
                folder = output / arm / f"rep{repetition}"
                folder.mkdir(parents=True)
                model = (OpenAIModel(config, schema=schema(), schema_name="sfifo_prompt_ablation_actions")
                         if args.mode == "live" else replay if replay else OfflineMock())
                binary, compile_command, compile_seconds = compile_driver("verilator", folder)
                seed = validate_actions(json.loads(SEED.read_text()), 10000)
                prior = simulate("verilator", binary, seed, folder, "seed")
                if prior["checker"]["failures"]:
                    raise AssertionError("Common seed fails fixed checker")
                points = points_for(folder / "seed.dat")
                denominator = {point_id(point) for point in points}
                if len(denominator) != lock["source_counter_denominator"]:
                    raise AssertionError("Original DUT coverage denominator changed")
                history = []
                last_log = folder / "seed.sim.log"
                executions, cycles, tokens, calls, failed_attempts = 1, len(seed), 0, 0, 0
                sim_seconds = prior["simulation_seconds"]
                model_seconds = count_seconds = 0.0
                count_requests = 0
                for round_no in range(1, config["rounds"] + 1):
                    count_start = time.perf_counter()
                    (messages, placebo), c_messages = make_prompt(
                        arm, history, prior, last_log.read_text(), points,
                        semantic, round_no, config, model, args.mode)
                    if placebo:
                        count_seconds += time.perf_counter() - count_start
                        count_requests += placebo["count_requests"]
                        append(output / "placebo-token-counts.jsonl",
                               {"arm": arm, "repetition": repetition,
                                "round": round_no, "attempt": 1, "mode": args.mode, **placebo})
                    accepted = None
                    for attempt in range(1, config["max_retries"] + 2):
                        prompt = folder / f"prompt-{arm}-{round_no}-{attempt}.json"
                        prompt.write_text(json.dumps(messages, indent=2) + "\n")
                        if token_estimate(messages) > config["max_input_tokens_conservative_byte_cap"]:
                            raise RuntimeError("Prompt conservative byte cap exceeded")
                        entry = {"arm": arm, "repetition": repetition, "round": round_no,
                                 "attempt": attempt, "mode": args.mode,
                                 "prompt": str(prompt.relative_to(output)),
                                 "prompt_bytes": token_estimate(messages),
                                 "settings": {k: config[k] for k in
                                              ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds")}}
                        if placebo:
                            entry["placebo_token_count"] = placebo
                        call_start = time.perf_counter()
                        try:
                            calls += 1
                            response = model.generate(messages, {"arm": arm,
                                        "repetition": repetition, "round": round_no,
                                        "limit": config["max_new_cycles"]})
                            entry.update(response)
                            model_seconds += response["latency_seconds"]
                            usage = response["usage"]
                            if usage["input_tokens"] is not None:
                                tokens += usage["input_tokens"] + usage["output_tokens"]
                            if (arm == "P_compact" and args.mode == "live" and
                                    abs(usage["input_tokens"] - placebo["placebo_input_tokens"]) >
                                    config["placebo_tolerance_tokens"]):
                                raise AssertionError("Count-only and generation input usage differ")
                            candidate = validate_actions(response["parsed"],
                                                         config["max_new_cycles"],
                                                         require_initial_reset=False)
                            entry["actions"] = candidate
                            entry["simulated"] = True
                            name = f"round{round_no}-attempt{attempt}"
                            executions += 1
                            cycles += len(seed) + len(history) + len(candidate)
                            result = simulate("verilator", binary, seed + history + candidate,
                                              folder, name)
                            sim_seconds += result["simulation_seconds"]
                            candidate_points = points_for(folder / f"{name}.dat")
                            if {point_id(point) for point in candidate_points} != denominator:
                                raise AssertionError("Original DUT denominator changed")
                            accepted = candidate
                            prior, points = result, candidate_points
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
                        note = {"role": "user", "content": "Validation failed: " +
                                entry["validation_failure"] + ". Return only legal JSON actions."}
                        if arm == "P_compact":
                            c_messages = [*c_messages, note]
                            count_start = time.perf_counter()
                            messages, placebo = match_placebo(
                                c_messages, model.count_input_tokens if args.mode == "live" else
                                lambda m: sum(len(x["content"]) for x in m),
                                tolerance=config["placebo_tolerance_tokens"])
                            count_seconds += time.perf_counter() - count_start
                            count_requests += placebo["count_requests"]
                            append(output / "placebo-token-counts.jsonl",
                                   {"arm": arm, "repetition": repetition,
                                    "round": round_no, "attempt": attempt+1,
                                    "mode": args.mode, **placebo})
                        else:
                            messages = [*messages, note]
                    if accepted is not None:
                        history.extend(accepted)
                    row = {"arm": arm, "repetition": repetition, "round": round_no,
                           "status": "ok" if accepted is not None else "no_valid_actions",
                           "target_hits": target_hits(points, config),
                           "target_reached": all(x["hits"] > 0 for x in target_hits(points, config)),
                           "coverage": prior["coverage"], "checker": prior["checker"],
                           "api_tokens": tokens, "executed_cycles": cycles,
                           "simulator_executions": executions, "model_calls": calls,
                           "failed_attempts": failed_attempts,
                           "token_count_requests": count_requests,
                           "token_count_seconds_cumulative": count_seconds,
                           "compile_seconds": compile_seconds,
                           "simulation_seconds_cumulative": sim_seconds,
                           "model_seconds_cumulative": model_seconds,
                           "total_wall_seconds": time.perf_counter() - started}
                    append(output / "rounds.jsonl", row)
                    rows.append(row)
                    print(f"{arm} rep {repetition} round {round_no}: "
                          f"target {sum(x['hits'] > 0 for x in row['target_hits'])}/5, "
                          f"branch {prior['coverage']['branch']['covered']}/{prior['coverage']['branch']['total']}",
                          flush=True)
                    if accepted is None:
                        break
        (output / "summary.json").write_text(json.dumps({"mode": args.mode,
              "purpose": config["purpose"], "rows": rows}, indent=2) + "\n")
    finally:
        os.environ.pop("OPENAI_API_KEY", None)
        if args.mode == "live" and KEY_FILE.exists():
            KEY_FILE.unlink()


if __name__ == "__main__":
    main()
