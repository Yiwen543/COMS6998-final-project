#!/usr/bin/env python3
"""Independent B-only UART development screen; calibration never enters prompts."""
from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import time
from pathlib import Path

from coverage import load
from pilot_model import ModelResponseError, OpenAIModel, token_estimate, usage_record
from run_midterm_b_development import KEY_FILE, append, raw_feedback
from run_midterm_fixed import ROOT, sha
from run_txuart_fixed import DRIVER, SOURCE, compile_driver, simulate, verify_source
from txuart_fixture import schema, validate_actions

DEFAULT_CONFIG = ROOT / "configs/txuart_b_development.json"
SEED = ROOT / "configs/txuart_seed.json"
CONTRACT = ROOT / "examples/heldout_txuart/docs/contract.md"
SCREEN = ROOT / "results/next_natural_ip_screen/txuart/screen.json"
INSTRUCTIONS = ("Generate only JSON cycle actions for this fixed UART public-pin specification checker. "
                "You control stimulus only. The DUT, checker, driver, coverage denominator and budget are fixed. "
                "Each action is applied before a rising edge. Maximize uncovered DUT line and branch counters "
                "including distinct source locations. A checker failure is useful evidence; do not suppress it. "
                "Return an actions array only. Do not include the fixed post-round idle drain.")


def idle():
    return {"reset": 0, "break": 0, "wr": 0, "data": 0}


def messages(seed, generated, prior, log, points, round_no, limit):
    common = {"specification": CONTRACT.read_text(),
              "rtl": {str(SOURCE.relative_to(ROOT)): SOURCE.read_text()},
              "initial_stimulus": seed, "previous_generated_actions": generated,
              "round": round_no, "max_new_cycles": limit,
              "stimulus_fields_and_widths": {"reset": "1-bit", "break": "1-bit",
                                              "wr": "1-bit", "data": "unsigned 8-bit"},
              "checker": {"checks": prior["checker"]["checks"],
                          "distinct_defects": prior["checker"]["distinct_defects"],
                          "first_failures": prior["checker"]["failures"][:8],
                          "execution_log": [line for line in log.splitlines()
                                            if line.startswith("TRACE ")][-40:]},
              "raw_uncovered_dut_coverage": raw_feedback(points, [SOURCE])}
    return [{"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": json.dumps(common, sort_keys=True)}]


class OfflineMock:
    def generate(self, _messages, context):
        rng = random.Random(6998 + 1009 * context["repetition"] + context["round"])
        actions = [{"reset": 0, "break": int(rng.randrange(20) == 0),
                    "wr": int(rng.randrange(8) == 0), "data": rng.randrange(256)}
                   for _ in range(context["limit"])]
        return {"requested_model": "mock", "returned_model": "mock", "response_id": "mock",
                "latency_seconds": 0.0, "status": "completed", "incomplete_details": None,
                "usage": usage_record(None), "output_text": json.dumps({"actions": actions}),
                "parsed": {"actions": actions}}


def group_hits(points, screen):
    index = {(p["source"], p["line"], p["column"], p["type"], p["outcome"]): p["hits"]
             for p in points}
    result = []
    for group in screen["groups"]:
        if not group["qualifies"]:
            continue
        refs = [m["seed_coverage"]["point"] for m in group["members"]]
        hits = [index[(p["source"], p["line"], p["column"], p["type"], p["outcome"])]
                for p in refs]
        result.append({"eclass": group["eclass"], "source_lines": [p["line"] for p in refs],
                       "raw_counter_hits": hits, "all_hit": all(h > 0 for h in hits)})
    return result


def evaluate_gate(rows, config, screen):
    threshold = config["acceptance"]
    repetitions = sorted({r["repetition"] for r in rows})
    first_unhit = 0
    later_progress = 0
    details = []
    for repetition in repetitions:
        rounds = [r for r in rows if r["repetition"] == repetition]
        if not rounds:
            continue
        first = sum(not g["all_hit"] for g in rounds[0]["target_groups"])
        last = sum(not g["all_hit"] for g in rounds[-1]["target_groups"])
        first_unhit += first >= 2
        later_progress += any(sum(not g["all_hit"] for g in r["target_groups"]) < first
                              for r in rounds[1:])
        details.append({"repetition": repetition, "groups_unhit_after_round_one": first,
                        "groups_unhit_final": last, "later_progress": first > last})
    passed = (screen["qualifying_groups"] >= threshold["min_qualifying_groups"] and
              first_unhit >= threshold["min_repetitions_with_two_groups_unhit_after_round_one"] and
              later_progress >= threshold["min_repetitions_with_later_group_progress"] and
              len(repetitions) == config["repetitions"])
    return {"passed": passed, "details": details, "repetitions_with_two_first_round_unhit": first_unhit,
            "repetitions_with_later_progress": later_progress,
            "preregistered_threshold": threshold}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--mode", choices=("mock", "live"), required=True)
    cli.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    config = json.loads(args.config.read_text())
    screen = json.loads(SCREEN.read_text())
    verify_source()
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    (output / "metadata.json").write_text(json.dumps({"mode": args.mode,
        "commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                                 text=True, check=True).stdout.strip(),
        "source_sha256": sha(SOURCE), "contract_sha256": sha(CONTRACT),
        "checker_sha256": sha(ROOT / "scripts/txuart_fixture.py"),
        "driver_sha256": sha(DRIVER), "screen_sha256": sha(SCREEN),
        "action_schema": schema()}, indent=2) + "\n")
    if args.mode == "live":
        if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
            raise RuntimeError("Staged OpenAI key missing or permissions too broad")
        os.environ["OPENAI_API_KEY"] = KEY_FILE.read_text().strip()
    try:
        model = (OpenAIModel(config, schema=schema(), schema_name="txuart_actions")
                 if args.mode == "live" else OfflineMock())
        seed = json.loads(SEED.read_text())["actions"]
        rows = []
        for rep in range(1, config["repetitions"] + 1):
            folder = output / f"rep{rep}"
            folder.mkdir()
            binary, command, compile_seconds = compile_driver("verilator", folder)
            prior = simulate("verilator", binary, seed, folder, "seed")
            history, generated = [], []
            points = load(folder / "seed.dat", str(SOURCE.relative_to(ROOT)), include_descendants=True)
            denominator = {(p["source"], p["line"], p["column"], p["type"], p["outcome"])
                           for p in points}
            total_cycles, executions, tokens, calls, failures = len(seed), 1, 0, 0, 0
            sim_seconds = prior["simulation_seconds"]
            last_log = folder / "seed.sim.log"
            for round_no in range(1, config["rounds"] + 1):
                current = messages(seed, generated, prior, last_log.read_text(), points,
                                   round_no, config["max_new_cycles"])
                accepted = None
                for attempt in range(1, config["max_retries"] + 2):
                    prompt = folder / f"prompt-B-{round_no}-{attempt}.json"
                    prompt.write_text(json.dumps(current, indent=2) + "\n")
                    if token_estimate(current) > config["max_input_tokens_conservative_byte_cap"]:
                        raise RuntimeError("Prompt byte cap exceeded")
                    entry = {"arm": "B", "repetition": rep, "round": round_no,
                             "attempt": attempt, "mode": args.mode,
                             "prompt": str(prompt.relative_to(output)),
                             "settings": {key: config[key] for key in
                                          ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds")}}
                    try:
                        calls += 1
                        response = model.generate(current, {"repetition": rep, "round": round_no,
                                                            "limit": config["max_new_cycles"]})
                        entry.update(response)
                        usage = response["usage"]
                        if usage["input_tokens"] is not None:
                            tokens += usage["input_tokens"] + usage["output_tokens"]
                        accepted = validate_actions(response["parsed"], config["max_new_cycles"])
                        entry["actions"] = accepted
                        entry["accepted"] = True
                    except ModelResponseError as exc:
                        entry.update(exc.record)
                        usage = exc.record["usage"]
                        if usage["input_tokens"] is not None:
                            tokens += usage["input_tokens"] + usage["output_tokens"]
                        entry["validation_failure"] = exc.reason
                    except ValueError as exc:
                        entry["validation_failure"] = str(exc)
                    except Exception as exc:
                        entry["validation_failure"] = type(exc).__name__
                        entry["http_status"] = getattr(exc, "status_code", None)
                    if not entry.get("accepted"):
                        failures += 1
                    append(output / "calls.jsonl", entry)
                    if accepted is not None:
                        break
                    current = [*current, {"role": "user", "content":
                                         "Validation failed: " + entry["validation_failure"] +
                                         ". Return only legal JSON actions."}]
                if accepted is None:
                    append(output / "rounds.jsonl", {"repetition": rep, "round": round_no,
                                                       "status": "no_valid_actions"})
                    break
                generated.extend(accepted)
                batch = accepted + [idle() for _ in range(config["drain_cycles_per_round"])]
                history.extend(batch)
                total_cycles += len(seed) + len(history)
                executions += 1
                result = simulate("verilator", binary, seed + history, folder, f"round{round_no}")
                sim_seconds += result["simulation_seconds"]
                points = load(folder / f"round{round_no}.dat", str(SOURCE.relative_to(ROOT)),
                              include_descendants=True)
                actual = {(p["source"], p["line"], p["column"], p["type"], p["outcome"])
                          for p in points}
                if actual != denominator:
                    raise AssertionError("Original DUT coverage denominator changed")
                prior = result
                last_log = folder / f"round{round_no}.sim.log"
                row = {"arm": "B", "repetition": rep, "round": round_no,
                       "new_cycles": len(accepted), "fixed_drain_cycles": config["drain_cycles_per_round"],
                       "replay_policy": "seed plus all prior batches and their drains",
                       "target_groups": group_hits(points, screen), "coverage": result["coverage"],
                       "checker": result["checker"], "api_tokens": tokens,
                       "executed_cycles": total_cycles, "simulator_executions": executions,
                       "model_calls": calls, "failed_attempts": failures,
                       "compile_seconds": compile_seconds, "simulation_seconds": sim_seconds}
                append(output / "rounds.jsonl", row)
                rows.append(row)
                print(f"UART B rep {rep} round {round_no}: unhit groups "
                      f"{sum(not g['all_hit'] for g in row['target_groups'])}", flush=True)
        gate = evaluate_gate(rows, config, screen)
        (output / "summary.json").write_text(json.dumps({"mode": args.mode,
            "purpose": config["purpose"], "gate": gate, "rows": rows}, indent=2) + "\n")
        print(json.dumps(gate, indent=2))
    finally:
        os.environ.pop("OPENAI_API_KEY", None)
        if args.mode == "live" and KEY_FILE.exists():
            KEY_FILE.unlink()


if __name__ == "__main__":
    main()
