#!/usr/bin/env python3
"""Independent B-only development screen of candidate saturation.

Uses the fixed public-I/O driver/checker. Calibration vectors and formal
witnesses are never included in prompts. This output must not be pooled with
held-out A/B/C repetitions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
import time
from pathlib import Path

from coverage import load, summary
from midterm_fixture import SPECS, check, schema, validate_actions
from pilot_feedback import point_id
from pilot_model import ModelResponseError, OpenAIModel, token_estimate, usage_record
from run_midterm_fixed import ROOT, SETUPS, compile_driver, invoke, sha, simulate
from run_pilot import versions


KEY_FILE = ROOT / "build/private/midterm-openai-key"
DEFAULT_CONFIG = ROOT / "configs/midterm_b_development.json"
INSTRUCTIONS = """Generate only JSON cycle actions for the fixed specification checker. You may change stimulus only. The DUT, checker, clock/reset driver, coverage denominator, and budget are fixed. Each action is applied before a rising edge. Maximize uncovered DUT line and branch counters, including distinct source locations, within the cycle limit. A checker finding on faulty RTL is useful evidence; do not suppress it. Avoid undefined/illegal protocol actions. Return JSON only with an actions array and no prose."""


def append(path, row):
    with path.open("a") as stream:
        stream.write(json.dumps(row, sort_keys=True) + "\n")


def raw_feedback(points, sources):
    lines = {str(path.relative_to(ROOT)): path.read_text().splitlines() for path in sources}
    return [{"source": p["source"], "line": p["line"], "column": p["column"],
             "counter_type": p["type"], "outcome": p["outcome"], "hits": p["hits"],
             "source_text": lines[p["source"]][p["line"] - 1].strip()}
            for p in points if p["hits"] == 0 and p["type"] in ("line", "branch", "expr")]


def messages_for(ip, actions, checked, log, points, sources, round_no, limit):
    slug, _ = SETUPS[ip]
    folder = ROOT / "examples" / slug
    common = {"specification": (folder / "docs/specification.md").read_text(),
              "rtl": {str(source.relative_to(ROOT)): source.read_text() for source in sources},
              "initial_stimulus": json.loads((ROOT / f"configs/midterm_{ip}_seed.json").read_text())["actions"],
              "previous_generated_actions": actions, "round": round_no, "max_new_cycles": limit,
              "stimulus_fields_and_widths": SPECS[ip],
              "checker": {"checks": checked["checker"]["checks"],
                          "distinct_defects": checked["checker"]["distinct_defects"],
                          "first_failures": checked["checker"]["failures"][:8],
                          "execution_log": [line for line in log.splitlines() if line.startswith("TRACE ")][-40:]},
              "raw_uncovered_dut_coverage": raw_feedback(points, sources)}
    extra = ("Codec: enc_data and dec_word are unsigned 64-bit and 66-bit integers; "
             "dec_word upper two bits are the sync header. Reset is specified synchronous. "
             "The decoder valid input enables a one-cycle registered result." if ip == "codec" else
             "Search: DATA_WIDTH=8, ADDR_WIDTH=3, MEM_DEPTH=8, MAX_MATCHES=2. "
             "Initialize all eight addresses with write_en before start; start is a one-cycle pulse. "
             "Hold key stable during search. Do not write while search is active. "
             "Pause/resume and overflow are legal. Reset is specified synchronous.")
    return [{"role": "system", "content": INSTRUCTIONS + "\n" + extra},
            {"role": "user", "content": json.dumps(common, sort_keys=True)}]


class OfflineMock:
    """Arm-blind smoke data; not evidence of LLM performance."""
    def generate(self, messages, context):
        rng = random.Random(6998 + 1009 * context["round"])
        if context["ip"] == "codec":
            actions = [dict(reset=0, enc_data=rng.getrandbits(64), enc_control=0,
                            dec_valid=1, dec_word=(1 << 64) | rng.getrandbits(64))
                       for _ in range(context["limit"])]
        else:
            zero = dict(reset=0, start=0, pause=0, key=90, write_en=0, write_addr=0, write_data=0)
            if context["limit"] <= 8:
                if context["round"] == 1:
                    actions = [dict(zero, write_en=1, write_addr=i, write_data=i)
                               for i in range(context["limit"])]
                elif context["round"] == 2:
                    actions = [dict(zero, start=1)] + [dict(zero) for _ in range(context["limit"] - 1)]
                else:
                    actions = [dict(zero) for _ in range(context["limit"])]
            else:
                actions = [dict(zero, write_en=1, write_addr=i, write_data=i) for i in range(8)]
                actions += [dict(zero, start=1)]
                actions += [dict(zero) for _ in range(max(0, context["limit"] - len(actions)))]
        return {"requested_model": "mock", "returned_model": "mock", "response_id": "mock",
                "latency_seconds": 0.0, "status": "completed", "incomplete_details": None,
                "usage": usage_record(None), "output_text": json.dumps({"actions": actions}),
                "parsed": {"actions": actions}}


def current_points(ip, dat, sources):
    return [p for source in sources for p in load(dat, str(source.relative_to(ROOT)), include_descendants=True)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("mock", "live"), required=True)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    config = json.loads(config_path.read_text())
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    lock = json.loads((ROOT / "docs/midterm-candidate-lock.json").read_text())
    hashes = {}
    for candidate in lock["candidates"]:
        for field, expected in candidate["fields"].items():
            path = ROOT / "examples" / candidate["slug"] / (
                "rtl" if field.startswith("harness/") else "docs") / Path(field).name
            if sha(path) != expected:
                raise AssertionError(f"Pinned CVDP fixture changed: {path}")
            hashes[str(path.relative_to(ROOT))] = expected
        slug, top = SETUPS["codec" if candidate["slug"] == "heldout_codec64" else "search"]
        driver = ROOT / "examples" / slug / "verif" / f"{top}.sv"
        hashes[str(driver.relative_to(ROOT))] = sha(driver)
    for path in (ROOT / "scripts/midterm_fixture.py", Path(__file__), config_path):
        hashes[str(path.relative_to(ROOT))] = sha(path)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
                            capture_output=True, check=True).stdout.strip()
    (output / "metadata.json").write_text(json.dumps({"mode": args.mode, "commit": commit,
                                                       "hashes": hashes, "versions": versions(),
                                                       "action_schemas": {ip: schema(ip) for ip in config["ips"]}},
                                                      indent=2) + "\n")
    if args.mode == "live":
        if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
            raise RuntimeError("Staged OpenAI key missing or permissions too broad")
        os.environ["OPENAI_API_KEY"] = KEY_FILE.read_text().strip()
    rows = []
    experiment_start = time.perf_counter()
    try:
        for ip in config["ips"]:
            model = (OpenAIModel(config, schema=schema(ip), schema_name=f"midterm_{ip}_actions")
                     if args.mode == "live" else OfflineMock())
            folder = output / ip
            folder.mkdir()
            binary, sources, driver, compile_argv, compile_seconds = compile_driver(ip, "verilator", folder)
            seed = json.loads((ROOT / f"configs/midterm_{ip}_seed.json").read_text())["actions"]
            seed_result = simulate(ip, "verilator", binary, sources, seed, folder, "seed")
            if seed_result["checker"]["failures"]:
                raise AssertionError("Common seed fails fixed specification checker")
            denominator = {point_id(p) for p in current_points(ip, folder / "seed.dat", sources)}
            history = []
            prior = seed_result
            last_log_path = folder / "seed.sim.log"
            points = current_points(ip, folder / "seed.dat", sources)
            total_tokens = 0
            total_cycles = len(seed)
            executions = 1
            model_calls = 0
            failed_attempts = 0
            model_seconds = 0.0
            simulation_seconds = seed_result["simulation_seconds"]
            for round_no in range(1, config["rounds"] + 1):
                current = messages_for(ip, history, prior, last_log_path.read_text(), points,
                                       sources, round_no, config["max_new_cycles"])
                accepted = None
                for attempt in range(1, config["max_retries"] + 2):
                    prompt = folder / f"prompt-B-{round_no}-{attempt}.json"
                    prompt.write_text(json.dumps(current, indent=2) + "\n")
                    if token_estimate(current) > config["max_input_tokens_conservative_byte_cap"]:
                        raise RuntimeError("Prompt byte cap exceeded")
                    entry = {"ip": ip, "arm": "B", "round": round_no, "attempt": attempt,
                             "mode": args.mode, "prompt": str(prompt.relative_to(output)),
                             "prompt_bytes": token_estimate(current),
                             "settings": {key: config[key] for key in
                                          ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds")}}
                    call_start = time.perf_counter()
                    try:
                        model_calls += 1
                        response = model.generate(current, {"ip": ip, "round": round_no, "limit": config["max_new_cycles"]})
                        entry.update(response)
                        model_seconds += response["latency_seconds"]
                        usage = response["usage"]
                        if usage["input_tokens"] is not None:
                            total_tokens += usage["input_tokens"] + usage["output_tokens"]
                        candidate = validate_actions(ip, response["parsed"], config["max_new_cycles"])
                        name = f"round{round_no}-attempt{attempt}"
                        entry["actions"] = candidate
                        entry["simulated"] = True
                        executions += 1
                        total_cycles += len(seed) + len(history) + len(candidate)
                        sim_start = time.perf_counter()
                        try:
                            candidate_result = simulate(ip, "verilator", binary, sources,
                                                        seed + history + candidate, folder, name)
                        finally:
                            simulation_seconds += time.perf_counter() - sim_start
                        candidate_points = current_points(ip, folder / f"{name}.dat", sources)
                        if {point_id(p) for p in candidate_points} != denominator:
                            raise AssertionError("DUT coverage denominator changed")
                        accepted = candidate
                        prior = candidate_result
                        points = candidate_points
                        last_log_path = folder / f"{name}.sim.log"
                        entry["accepted"] = True
                    except ModelResponseError as exc:
                        entry.update(exc.record)
                        model_seconds += exc.record["latency_seconds"]
                        usage = exc.record["usage"]
                        if usage["input_tokens"] is not None:
                            total_tokens += usage["input_tokens"] + usage["output_tokens"]
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
                    current = [*current, {"role": "user", "content":
                                         "The response failed validation: " + entry["validation_failure"] +
                                         ". Return only legal JSON actions."}]
                if accepted is None:
                    append(output / "rounds.jsonl", {"ip": ip, "round": round_no, "status": "no_valid_actions"})
                    break
                history.extend(accepted)
                row = {"ip": ip, "arm": "B", "round": round_no,
                       "coverage": prior["coverage"], "checker": prior["checker"],
                       "api_tokens": total_tokens, "executed_cycles": total_cycles,
                       "simulator_executions": executions, "model_calls": model_calls,
                       "failed_attempts": failed_attempts, "compile_seconds": compile_seconds,
                       "simulation_seconds_cumulative": simulation_seconds,
                       "model_seconds_cumulative": model_seconds,
                       "total_wall_seconds": time.perf_counter() - experiment_start}
                append(output / "rounds.jsonl", row)
                rows.append(row)
                print(f"{ip} B round {round_no}: line {prior['coverage']['line']['covered']}/{prior['coverage']['line']['total']}, "
                      f"branch {prior['coverage']['branch']['covered']}/{prior['coverage']['branch']['total']}, "
                      f"defects {prior['checker']['distinct_defects']}")
        (output / "summary.json").write_text(json.dumps({"mode": args.mode, "purpose": config["purpose"],
                                                         "rows": rows}, indent=2) + "\n")
    finally:
        os.environ.pop("OPENAI_API_KEY", None)
        if args.mode == "live" and KEY_FILE.exists():
            KEY_FILE.unlink()


if __name__ == "__main__":
    main()
