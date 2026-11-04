#!/usr/bin/env python3
"""Fresh interleaved minimal-C ablation with durable failure/cost accounting."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

from minimal_c_feedback import common_payload, minimal_c_messages
from pilot_feedback import point_id
from pilot_model import ModelResponseError, OpenAIModel, token_estimate
from run_midterm_b_development import KEY_FILE, append
from run_midterm_fixed import ROOT, sha
from run_pilot import versions
from run_sfifo_prompt_ablation import (CONFIG as OLD_CONFIG, SEED, SEMANTIC,
    SELECTION, OfflineMock, points_for, target_hits, validate_lock)
from run_sfifo_stress_fixed import compile_driver, simulate
from sfifo_fixture import schema, validate_actions
from sfifo_prompt_ablation_feedback import messages_for
from token_placebo import match_placebo

CONFIG = ROOT / "configs/sfifo_minimal_c_exploratory.json"
ARMS = ("B_compact", "C_full", "C_min", "P_min")


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def schedule(config):
    arms = config["arms"]
    return [(arm, rep, rnd) for rnd in range(1, config["rounds"] + 1)
            for rep in range(1, config["repetitions"] + 1)
            for arm in (arms[(rnd+rep-2) % len(arms):] + arms[:(rnd+rep-2) % len(arms)])]


def prompt_for(arm, state, semantic, rnd, config):
    common = (state["history"], state["prior"], state["log"].read_text(),
              state["points"], semantic, rnd, config["max_new_cycles"])
    b = messages_for("B_compact", *common)
    full = messages_for("C_compact", *common)
    minimal = minimal_c_messages(full)
    if common_payload(b) != common_payload(full) or common_payload(b) != common_payload(minimal):
        raise AssertionError("Feedback isolation failed")
    if b[0] != full[0] or b[0] != minimal[0]:
        raise AssertionError("Base instructions differ")
    return b if arm == "B_compact" else full if arm == "C_full" else minimal


def error_record(exc):
    # Do not serialize exception messages/headers that may contain credentials.
    return {"error_type": type(exc).__name__,
            "http_status": getattr(exc, "status_code", None),
            "request_id": getattr(exc, "request_id", None)}


def usage_totals(calls):
    result = {k: 0 for k in ("input_tokens", "output_tokens", "cached_input_tokens", "reasoning_output_tokens")}
    unknown = 0
    for call in calls:
        usage = call.get("usage") or {}
        if usage.get("input_tokens") is None or usage.get("output_tokens") is None:
            unknown += 1
        for key in result:
            result[key] += usage.get(key) or 0
    result["api_tokens"] = result["input_tokens"] + result["output_tokens"]
    result["calls_with_unknown_usage"] = unknown
    return result


def snapshot(state, config, rnd, status):
    totals = usage_totals(state["calls"])
    hits = target_hits(state["points"], config)
    return {"arm": state["arm"], "repetition": state["rep"], "round": rnd,
            "status": status, "target_hits": hits, "target_reached": all(x["hits"] > 0 for x in hits),
            "coverage": state["prior"]["coverage"], "checker": state["prior"]["checker"],
            **totals, "model_calls": len(state["calls"]),
            "failed_attempts": sum(not x.get("accepted", False) for x in state["calls"]),
            "simulator_executions": state["executions"], "executed_cycles": state["cycles"],
            "scheduled_cycles": state["scheduled_cycles"],
            "simulation_seconds_cumulative": state["sim_seconds"],
            "model_seconds_cumulative": sum(x["request_wall_seconds"] for x in state["calls"]),
            "token_count_requests": len(state["counts"]),
            "token_count_seconds_cumulative": sum(x["wall_seconds"] for x in state["counts"]),
            "total_wall_seconds": state["active_seconds"],
            "wall_policy": "active session time, excludes shared compilation and interleaved waiting"}


def count_logged(state, model, messages, output, context, mode):
    digest = hashlib.sha256(json.dumps(messages, sort_keys=True).encode()).hexdigest()
    path = output / "count-inputs" / f"{digest}.json"
    if not path.exists():
        write(path, messages)
    record = {**context, "mode": mode, "prompt_sha256": digest,
              "prompt": str(path.relative_to(output)), "ok": False}
    started = time.perf_counter()
    try:
        value = model.count_input_tokens(messages) if mode == "live" else token_estimate(messages)
        record.update(ok=True, input_tokens=value,
                      method="provider" if mode == "live" else "mock_bytes_not_tokens")
        return value
    except Exception as exc:
        record.update(error_record(exc))
        raise
    finally:
        record["wall_seconds"] = time.perf_counter() - started
        state["counts"].append(record)
        append(output / "count-requests.jsonl", record)


def one_round(state, model, binary, seed, semantic, config, output, rnd, mode):
    started = time.perf_counter()
    status = "no_valid_actions"
    base = prompt_for(state["arm"], state, semantic, rnd, config)
    for attempt in range(1, config["max_retries"] + 2):
        context = {"arm": state["arm"], "repetition": state["rep"], "round": rnd,
                   "attempt": attempt, "limit": config["max_new_cycles"]}
        prefix = f"round{rnd}-attempt{attempt}"
        used_counts = 0
        def counted(messages):
            nonlocal used_counts
            used_counts += 1
            if used_counts > config["max_count_requests_per_attempt"]:
                raise RuntimeError("Count budget exhausted")
            return count_logged(state, model, messages, output, context, mode)
        placebo = None
        try:
            if state["arm"] == "P_min":
                messages, placebo = match_placebo(base, counted,
                    tolerance=config["placebo_tolerance_tokens"],
                    max_counts=config["max_count_requests_per_attempt"] - 1)
                input_count = placebo["placebo_input_tokens"]
                write(state["folder"] / f"{prefix}-shadow-minimal.json", base)
                append(output / "placebo-matches.jsonl", {**context, **placebo, "mode": mode})
            else:
                messages = base
                input_count = counted(messages)
            if token_estimate(messages) > config["max_input_bytes"]:
                raise ValueError("Input byte cap")
            if mode == "live" and input_count > config["max_input_tokens"]:
                raise ValueError("Input token cap")
        except Exception as exc:
            append(output / "failures.jsonl", {**context, "stage": "prompt_count", **error_record(exc)})
            status = "prompt_count_failed"
            break
        prompt = state["folder"] / f"{prefix}-prompt.json"
        write(prompt, messages)
        entry = {**context, "mode": mode, "prompt": str(prompt.relative_to(output)),
                 "input_count": input_count if mode == "live" else None,
                 "settings": {k: config[k] for k in ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds")},
                 "placebo": placebo, "accepted": False, "simulated": False}
        response, actions = None, None
        call_start = time.perf_counter()
        try:
            response = model.generate(messages, context)
            entry.update(response)
        except ModelResponseError as exc:
            entry.update(exc.record)
            entry["validation_failure"] = exc.reason
        except Exception as exc:
            entry.update(error_record(exc))
            entry["validation_failure"] = "request_failed"
        entry["request_wall_seconds"] = time.perf_counter() - call_start
        if response is not None:
            try:
                actual = (response.get("usage") or {}).get("input_tokens")
                if mode == "live" and (actual is None or abs(actual-input_count) > config["placebo_tolerance_tokens"]):
                    raise AssertionError("Provider count disagrees with generation input usage")
                actions = validate_actions(response["parsed"], config["max_new_cycles"], require_initial_reset=False)
                entry["actions"] = actions
            except ValueError as exc:
                entry["validation_failure"] = str(exc)
            except AssertionError:
                entry["validation_failure"] = "input_count_mismatch"
                status = "measurement_failed"
        if actions is not None:
            batch = seed + state["history"] + actions
            state["executions"] += 1
            state["scheduled_cycles"] += len(batch)
            sim_started = time.perf_counter()
            try:
                result = simulate("verilator", binary, batch, state["folder"], prefix)
                points = points_for(state["folder"] / f"{prefix}.dat")
                if {point_id(p) for p in points} != state["denominator"]:
                    raise AssertionError("Coverage denominator changed")
                state["cycles"] += len(batch)
                state["prior"], state["points"] = result, points
                state["log"] = state["folder"] / f"{prefix}.sim.log"
                state["history"].extend(actions)
                entry.update(accepted=True, simulated=True, simulation_prefix=prefix)
                status = "ok"
            except Exception as exc:
                log = state["folder"] / f"{prefix}.sim.log"
                state["cycles"] += sum(line.startswith("TRACE ") for line in log.read_text().splitlines()) if log.exists() else 0
                entry.update(error_record(exc), simulation_prefix=prefix,
                             validation_failure="simulation_or_measurement_failed", simulation_attempted=True)
                status = "measurement_failed"
            state["sim_seconds"] += time.perf_counter() - sim_started
        state["calls"].append(entry)
        append(output / "calls.jsonl", entry)
        if entry["accepted"] or status == "measurement_failed":
            break
        if attempt <= config["max_retries"]:
            base = [*base, {"role": "user", "content": "Validation failed: " +
                entry["validation_failure"] + ". Return only legal JSON actions."}]
    state["active_seconds"] += time.perf_counter() - started
    if status != "ok":
        state["terminal"] = status
    row = snapshot(state, config, rnd, status)
    append(output / "rounds.jsonl", row)
    print(f"{state['arm']} rep{state['rep']} round{rnd}: {status}, target "
          f"{sum(x['hits'] > 0 for x in row['target_hits'])}/5", flush=True)
    return row


def run(config, output, mode, config_path=CONFIG):
    semantic = json.loads(SEMANTIC.read_text())
    lock = validate_lock(json.loads(OLD_CONFIG.read_text()), semantic)
    if tuple(config["arms"]) != ARMS or config["primary_target"]["source_lines"] != lock["config"]["primary_target"]["source_lines"]:
        raise ValueError("Unexpected arms/targets")
    output.mkdir(parents=True, exist_ok=False)
    files = set(lock["files_sha256"]) | {str(config_path.relative_to(ROOT)),
        "scripts/run_minimal_c_ablation.py", "scripts/minimal_c_feedback.py",
        "scripts/analyze_minimal_c_ablation.py", "scripts/pilot_model.py", "scripts/token_placebo.py",
        str(SEMANTIC.relative_to(ROOT)), str(SELECTION.relative_to(ROOT))}
    metadata = {"mode": mode, "limits": config, "schema": schema(),
                "schema_name": "sfifo_prompt_ablation_actions", "versions": versions(),
                "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "files_sha256": {p: sha(ROOT / p) for p in sorted(files)},
                "schedule": schedule(config), "semantic_preprocessing": {
                    "cached": True, "original_timings": semantic.get("seconds"),
                    "policy": "shared preflight, not repeatedly charged to arms"}}
    write(output / "metadata.json", metadata)
    # Create durable ledgers even if no generation is possible.
    for name in ("calls", "rounds", "count-requests", "placebo-matches", "failures"):
        (output / f"{name}.jsonl").touch()
    states = {}
    started = time.perf_counter()
    try:
        if mode == "live":
            if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
                raise RuntimeError("Staged key missing or permissions too broad")
            os.environ["OPENAI_API_KEY"] = KEY_FILE.read_text().strip()
        shared = output / "shared"
        shared.mkdir()
        binary, command, seconds = compile_driver("verilator", shared)
        write(output / "shared-setup.json", {"compilations": 1, "compile_seconds": seconds,
            "command": [str(x) for x in command], "policy": config["measurement_policy"]})
        seed = validate_actions(json.loads(SEED.read_text()), 10000)
        models = {}
        for rep in range(1, config["repetitions"] + 1):
            for arm in config["arms"]:
                folder = output / arm / f"rep{rep}"
                folder.mkdir(parents=True)
                t = time.perf_counter()
                prior = simulate("verilator", binary, seed, folder, "seed")
                points = points_for(folder / "seed.dat")
                denominator = {point_id(p) for p in points}
                if len(denominator) != lock["source_counter_denominator"] or prior["checker"]["failures"]:
                    raise AssertionError("Seed checker or denominator mismatch")
                state = {"arm": arm, "rep": rep, "folder": folder, "prior": prior,
                    "points": points, "denominator": denominator, "log": folder / "seed.sim.log",
                    "history": [], "calls": [], "counts": [], "executions": 1,
                    "cycles": len(seed), "scheduled_cycles": len(seed), "terminal": None,
                    "sim_seconds": prior["simulation_seconds"], "active_seconds": time.perf_counter()-t}
                states[(arm, rep)] = state
                models[(arm, rep)] = OpenAIModel(config, schema=schema(), schema_name="sfifo_prompt_ablation_actions") if mode == "live" else OfflineMock()
                write(folder / "seed-summary.json", snapshot(state, config, 0, "seed"))
        for arm, rep, rnd in schedule(config):
            state = states[(arm, rep)]
            if state["terminal"]:
                continue
            one_round(state, models[(arm, rep)], binary, seed, semantic, config, output, rnd, mode)
    finally:
        write(output / "completion.json", {"total_wall_seconds": time.perf_counter()-started,
            "sessions": [{"arm": arm, "repetition": rep, "terminal": s["terminal"],
                          "model_calls": len(s["calls"])} for (arm, rep), s in states.items()]})
        if mode == "live":
            os.environ.pop("OPENAI_API_KEY", None)
            if KEY_FILE.exists():
                KEY_FILE.unlink()


def replay(source, output):
    metadata = json.loads((source / "metadata.json").read_text())
    for p, expected in metadata["files_sha256"].items():
        if sha(ROOT / p) != expected:
            raise AssertionError(f"Replay source hash changed: {p}")
    output.mkdir(parents=True, exist_ok=False)
    binary, command, seconds = compile_driver("verilator", output)
    calls = [json.loads(x) for x in (source / "calls.jsonl").read_text().splitlines()]
    seed = validate_actions(json.loads(SEED.read_text()), 10000)
    compared = 0
    for arm in metadata["limits"]["arms"]:
        for rep in range(1, metadata["limits"]["repetitions"]+1):
            folder = output / arm / f"rep{rep}"
            original = source / arm / f"rep{rep}"
            if not (original / "seed.json").exists():
                continue
            folder.mkdir(parents=True)
            history = []
            selected = [x for x in calls if x["arm"] == arm and x["repetition"] == rep and x.get("accepted")]
            for call in [None, *selected]:
                name = "seed" if call is None else call["simulation_prefix"]
                if call:
                    history.extend(call["actions"])
                result = simulate("verilator", binary, seed+history, folder, name)
                old = json.loads((original / f"{name}.json").read_text())
                if result["checker"] != old["checker"] or result["coverage"] != old["coverage"]:
                    raise AssertionError(f"Replay mismatch: {arm}/{rep}/{name}")
                if points_for(folder/f"{name}.dat") != points_for(original/f"{name}.dat"):
                    raise AssertionError("Raw counter replay mismatch")
                compared += 1
    record = {"mode": "offline_replay", "model_calls": 0, "status": "matched",
              "comparisons": compared, "compile_seconds": seconds,
              "scope": "all successful saved simulations including each seed; all original source counters/hits, coverage and checker"}
    write(output / "validation.json", record)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--mode", choices=("mock", "live", "replay"), required=True)
    cli.add_argument("--config", type=Path, default=CONFIG)
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--replay-source", type=Path)
    args = cli.parse_args()
    if args.mode == "replay":
        if not args.replay_source:
            cli.error("Replay requires --replay-source")
        replay(args.replay_source.resolve(), args.output.resolve())
    else:
        path = args.config.resolve()
        run(json.loads(path.read_text()), args.output.resolve(), args.mode, path)
