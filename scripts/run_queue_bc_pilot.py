#!/usr/bin/env python3
"""Matched B/C pilot on two separately frozen CVDP queue RTL versions."""
import argparse
import hashlib
import json
import os
import random
import re
import statistics
import subprocess
import time

from coverage import load, summary
from pilot_feedback import point_id
from pilot_model import ModelResponseError, OpenAIModel, token_estimate, usage_record
from predicates import ROOT
from preflight_heldout import z3_equivalent
from queue_feedback import CHECKER, INITIAL, SCHEMA, SPEC, VERSIONS, render_messages, validate_actions
from queue_reference import actions as reference_actions
from run_pilot import append_jsonl, command, csv_write, json_write, versions as tool_versions
from typed_predicates import extract

ENGINE = ROOT / "build/queue-cargo/debug/rtl-predicate-egraph"
KINDS = ("branch", "line", "expr", "toggle")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen(config):
    files = {"spec_sha256": SPEC, "checker_sha256": CHECKER,
             "feedback_sha256": ROOT / "scripts/queue_feedback.py",
             "engine_sha256": ROOT / "egraph/src/main.rs",
             "driver_sha256": ROOT / "scripts/sim_main_queue.cpp",
             "original_sha256": VERSIONS["original"][0],
             "variant_sha256": VERSIONS["variant"][0]}
    for key, path in files.items():
        if digest(path) != config[key]:
            raise RuntimeError(f"Frozen file changed: {path}")
    if config["arms"] != ["B", "C"] or config["versions"] != ["original", "variant"]:
        raise ValueError("Expected fixed B/C arms and both RTL versions")
    if not 1 <= config["target_line_points"] <= 41:
        raise ValueError("Invalid line target")


def parse_result(log):
    match = re.search(r"RESULT checks=(\d+) data_errors=(\d+) occupancy_errors=(\d+) reset_errors=(\d+) clear_errors=(\d+) enable_errors=(\d+)", log)
    if match is None:
        raise ValueError("Queue checker result missing")
    keys = ("checks", "data_errors", "occupancy_errors", "reset_errors", "clear_errors", "enable_errors")
    result = dict(zip(keys, map(int, match.groups())))
    result["functional_errors"] = sum(result[key] for key in keys[1:])
    result["distinct_defects"] = [key.removesuffix("_errors") for key in keys[1:] if result[key]]
    return result


def simulate(binary, folder, name, actions, source):
    vector = folder / f"{name}.vectors"
    if actions:
        vector.write_text("".join(f"{a['reset_n']} {a['clear']} {a['enable']} {a['write']} {a['read']} {a['data']:08x}\n" for a in actions))
    cover = folder / f"{name}.dat"
    args = [binary, f"+MODE={int(bool(actions))}", "+COLLECT", f"+verilator+coverage+file+{cover}"]
    if actions:
        path = str(vector.relative_to(ROOT)) if vector.is_relative_to(ROOT) else str(vector)
        if len(path.encode()) > 127:
            raise ValueError("Vector path exceeds fixed testbench plusarg width")
        args.append(f"+VECTORS={path}")
    seconds, log = command(args, folder / f"{name}.sim.log", timeout=120)
    checked = parse_result(log)
    if checked["checks"] != len(INITIAL) + len(actions):
        raise AssertionError("Simulator cycle accounting mismatch")
    return seconds, log, checked, load(cover, str(source.relative_to(ROOT)))


def semantic_setup(folder):
    tick = time.perf_counter()
    extractions = {version: extract(*VERSIONS[version]) for version in VERSIONS}
    all_targets = [target for item in extractions.values() for target in item["targets"]]
    payload = [{"id": row["id"], "compact": row["compact"], "expanded": row["compact"]}
               for row in all_targets]
    _, output = command([ENGINE], folder / "egg.log", timeout=15, stdin=json.dumps(payload))
    graph = json.loads(output)
    roots = {row["id"]: row["eclass"] for row in graph["targets"]}
    groups = {}
    for target in all_targets:
        if target["guard_depth"] == 4 and target["case_value"] in ("2'01", "2'10"):
            key = (roots[target["id"]], tuple(target["event_context"]))
            groups.setdefault(key, []).append(target)
    if len(groups) != 2 or sorted(len(g) for g in groups.values()) != [12, 12]:
        raise AssertionError("Expected two distinct 12-location full-guard groups")
    if {g[0]["case_value"] for g in groups.values()} != {"2'01", "2'10"}:
        raise AssertionError("Read/write cases improperly grouped")
    for members in groups.values():
        if not all(z3_equivalent(members[0]["compact"], member["compact"]) for member in members[1:]):
            raise AssertionError("An egg group failed independent Z3 proof")
    json_write(folder / "egg-evidence.json", graph)
    json_write(folder / "typed-predicates.json", extractions)
    return extractions, all_targets, graph, time.perf_counter() - tick


def compile_version(folder, version):
    source, top = VERSIONS[version]
    build = folder / "verilator-build"
    argv = ["verilator", "--cc", "--exe", "--build", "--timing", "--assert",
            "--coverage-line", "--coverage-toggle", "--coverage-expr",
            "-Wno-fatal", "-Wno-TIMESCALEMOD", "-Wno-WIDTHEXPAND",
            f"-DDUT_MODULE={top}", "--top-module", "tb_queue_pilot", "--Mdir", build,
            "-j", "2", source.relative_to(ROOT), CHECKER.relative_to(ROOT),
            ROOT / "scripts/sim_main_queue.cpp"]
    seconds, _ = command(argv, folder / "verilator-compile.log", timeout=180)
    return build / "Vtb_queue_pilot", seconds, argv


class MockQueue:
    """Arm-blind legal smoke stimulus; never evidence of model performance."""
    def __init__(self, config): self.config = config

    def generate(self, messages, context):
        rng = random.Random(self.config["seed"] + context["repetition"] * 1009 + context["round"])
        prior = json.loads(messages[1]["content"])["previous_generated_actions"]
        count = 0
        for action in prior:
            if not action["reset_n"] or action["clear"]: count = 0
            elif action["enable"]: count += action["write"] - action["read"]
        actions = []
        for _ in range(self.config["max_new_cycles"]):
            if rng.randrange(30) == 0:
                action = dict(reset_n=0, clear=0, enable=0, write=0, read=0, data=0)
                count = 0
            else:
                op = rng.choice(["idle", "write", "read", "both", "hold", "clear"])
                if op == "write" and count == 3: op = "read"
                if op == "read" and count == 0: op = "write"
                action = dict(reset_n=1, clear=int(op == "clear"), enable=int(op != "hold"),
                              write=int(op in ("write", "both", "hold")),
                              read=int(op in ("read", "both", "hold")), data=rng.getrandbits(32))
                if op == "clear": count = 0
                elif op == "write": count += 1
                elif op == "read": count -= 1
            actions.append(action)
        return {"requested_model": "mock-legal-random", "returned_model": "mock-legal-random",
                "response_id": f"mock-{context['version']}-{context['repetition']}-{context['round']}",
                "latency_seconds": 0.0, "status": "completed", "incomplete_details": None,
                "usage": usage_record(None), "output_text": json.dumps({"actions": actions}),
                "parsed": {"actions": actions}}


class ReplayQueue:
    def __init__(self, path):
        self.calls = {}
        modes = set()
        for line in open(path, encoding="utf-8"):
            call = json.loads(line)
            if call.get("accepted"):
                self.calls[(call["version"], call["arm"], call["repetition"], call["round"])] = call
                modes.add(call["mode"])
        if len(modes) != 1: raise ValueError("Replay source must have one mode")
        self.source_mode = modes.pop()

    def generate(self, messages, context):
        call = self.calls[(context["version"], context["arm"], context["repetition"], context["round"])]
        return {"requested_model": call["requested_model"], "returned_model": call["returned_model"],
                "response_id": call["response_id"], "latency_seconds": 0.0,
                "status": "completed", "incomplete_details": None, "usage": call["usage"],
                "output_text": json.dumps({"actions": call["actions"]}),
                "parsed": {"actions": call["actions"]}}


def target_costs(rows, config):
    costs = []
    for version in config["versions"]:
        for arm in config["arms"]:
            for rep in range(1, config["repetitions"] + 1):
                sample = [row for row in rows if (row["version"], row["arm"], row["repetition"]) == (version, arm, rep)]
                reached = next((row for row in sample if row["line_covered"] >= config["target_line_points"]), None)
                last = reached or (sample[-1] if sample else None)
                costs.append({"version": version, "arm": arm, "repetition": rep,
                              "target_line_points": config["target_line_points"],
                              "status": "reached" if reached else "not reached",
                              "first_target_round": reached["round"] if reached else None,
                              "line_covered_at_stop": last["line_covered"] if last else None,
                              "api_tokens": last["cumulative_api_tokens"] if last else None,
                              "executed_cycles": last["cumulative_executed_cycles"] if last else None,
                              "simulator_executions": last["cumulative_simulator_executions"] if last else None,
                              "wall_seconds": last["cumulative_total_wall_seconds"] if last else None})
    return costs


def plot(rows, output, mode):
    cache = output / "plot-cache"
    cache.mkdir(exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(cache)
    os.environ["XDG_CACHE_HOME"] = str(cache)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    axes_spec = (("cumulative_api_tokens", "API input + output tokens"),
                 ("cumulative_executed_cycles", "Executed cycles"),
                 ("cumulative_simulator_executions", "Simulator executions"),
                 ("cumulative_total_wall_seconds", "Wall seconds"))
    for version in ("original", "variant"):
        fig, axes = plt.subplots(2, 2, figsize=(11, 8))
        for ax, (xfield, label) in zip(axes.flat, axes_spec):
            if xfield == "cumulative_api_tokens" and mode == "mock":
                ax.text(.5, .5, "No API tokens in mock mode", ha="center", va="center", transform=ax.transAxes)
            else:
                for arm, color in (("B", "#d55e00"), ("C", "#0072b2")):
                    for rep in sorted({r["repetition"] for r in rows}):
                        sample = [r for r in rows if (r["version"], r["arm"], r["repetition"]) == (version, arm, rep)]
                        if sample:
                            ax.plot([r[xfield] for r in sample], [r["line_covered"] for r in sample],
                                    marker="o", color=color, alpha=.55, label=arm if rep == 1 else None)
            ax.set_xlabel(label)
            ax.set_ylabel("DUT line/case points / 41")
            ax.set_ylim(0, 41)
            ax.grid(alpha=.2)
        if rows:
            axes[0, 1].legend(title="Feedback")
        fig.suptitle(f"{version} queue: {mode} B/C pilot")
        fig.tight_layout()
        fig.savefig(output / f"comparison-{version}.png", dpi=150)
        plt.close(fig)


def write_report(rows, config, metadata, output, mode):
    costs = target_costs(rows, config)
    lines = ["# Held-out CVDP queue matched B/C pilot", "", f"Mode: **{mode}**.", "",
             "Two independently frozen RTL versions of one IP are compared within-version. B gets every raw uncovered DUT counter; C gets the identical raw array plus egg/Z3-verified full-guard groups. No witness input or calibration sequence enters prompts.",
             "", f"Preregistered line target: {config['target_line_points']}/41. Three repetitions, four rounds, at most {config['max_new_cycles']} new cycles per round. Each run replays all accepted actions after the same six-cycle reset/idle seed; all replay cycles and simulator executions are counted.",
             "", "| Version | Arm | Rep | Final line | Branch | Toggle | Distinct defects | API tokens | Cycles | Calls | Target |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for cost in costs:
        sample = [r for r in rows if (r["version"], r["arm"], r["repetition"]) ==
                  (cost["version"], cost["arm"], cost["repetition"])]
        if not sample: continue
        final = sample[-1]
        lines.append(f"| {cost['version']} | {cost['arm']} | {cost['repetition']} | {final['line_covered']}/{final['line_total']} | {final['branch_covered']}/{final['branch_total']} | {final['toggle_covered']}/{final['toggle_total']} | {final['distinct_defect_count']} | {final['cumulative_api_tokens'] or 'N/A'} | {final['cumulative_executed_cycles']} | {final['cumulative_model_calls']} | {cost['status']} |")
    lines += ["", "| Version | B final line mean (range) | C final line mean (range) | B reached target | C reached target | C − B mean line |",
              "|---|---:|---:|---:|---:|---:|"]
    for version in config["versions"]:
        by_arm = {arm: [next((row for row in reversed(rows) if
                             (row["version"], row["arm"], row["repetition"]) == (version, arm, rep)), None)
                        for rep in range(1, config["repetitions"] + 1)]
                  for arm in config["arms"]}
        samples = {arm: [row["line_covered"] for row in by_arm[arm] if row] for arm in config["arms"]}
        fmt = lambda values: f"{statistics.mean(values):.2f} ({min(values)}–{max(values)})" if values else "N/A"
        reached = {arm: sum(item["status"] == "reached" for item in costs if
                            item["version"] == version and item["arm"] == arm) for arm in config["arms"]}
        difference = statistics.mean(samples["C"]) - statistics.mean(samples["B"]) if all(samples.values()) else None
        delta = f"{difference:+.2f}" if difference is not None else "N/A"
        lines.append(f"| {version} | {fmt(samples['B'])} | {fmt(samples['C'])} | {reached['B']}/{config['repetitions']} | {reached['C']}/{config['repetitions']} | {delta} |")
    lines += ["", "| Version | Arm | Mean tokens to line target | Mean branch ROI / 1k tokens | Mean cycles | Mean simulations | Mean wall seconds |",
              "|---|---|---:|---:|---:|---:|---:|"]
    for version in config["versions"]:
        for arm in config["arms"]:
            reached = [item for item in costs if item["version"] == version and
                       item["arm"] == arm and item["status"] == "reached"]
            if reached:
                mean = lambda field: statistics.mean(item[field] for item in reached)
                tokens = f"{mean('api_tokens'):.0f}" if all(item["api_tokens"] is not None for item in reached) else "N/A"
                roi_values = [row["token_roi_new_branches_per_1000_tokens"] for row in rows
                              if row["version"] == version and row["arm"] == arm and
                              any(item["repetition"] == row["repetition"] and
                                  item["first_target_round"] == row["round"] for item in reached)
                              and row["token_roi_new_branches_per_1000_tokens"] is not None]
                roi = f"{statistics.mean(roi_values):.4f}" if roi_values else "N/A"
                lines.append(f"| {version} | {arm} | {tokens} | {roi} | {mean('executed_cycles'):.0f} | {mean('simulator_executions'):.0f} | {mean('wall_seconds'):.2f} |")
            else:
                lines.append(f"| {version} | {arm} | not reached | not reached | not reached | not reached | not reached |")
    if mode == "live" and rows:
        by_round = {(row["version"], row["arm"], row["repetition"], row["round"]): row for row in rows}
        toggle_deltas = [by_round[(version, "C", rep, rnd)]["toggle_covered"] -
                         by_round[(version, "B", rep, rnd)]["toggle_covered"]
                         for version in config["versions"] for rep in range(1, config["repetitions"]+1)
                         for rnd in range(1, config["rounds"]+1)]
        lines += ["", f"Across {len(toggle_deltas)} paired rounds, C had more toggle points in {sum(delta > 0 for delta in toggle_deltas)}, fewer in {sum(delta < 0 for delta in toggle_deltas)}, and the same count in {sum(delta == 0 for delta in toggle_deltas)}."]
        calls_path = output / "calls.jsonl"
        if calls_path.exists():
            accepted = []
            with calls_path.open() as stream:
                for line in stream:
                    call = json.loads(line)
                    if call.get("accepted"):
                        accepted.append(call)
            actions = {(call["version"], call["arm"], call["repetition"], call["round"]): call["actions"]
                       for call in accepted}
            pairs = [(actions[(version, "B", rep, rnd)], actions[(version, "C", rep, rnd)])
                     for version in config["versions"] for rep in range(1, config["repetitions"]+1)
                     for rnd in range(1, config["rounds"]+1)
                     if (version, "B", rep, rnd) in actions and (version, "C", rep, rnd) in actions]
            if pairs:
                lines += ["", f"Paired B/C action batches were identical in {sum(b == c for b, c in pairs)}/{len(pairs)} round pairs; differing stimulus did not necessarily change measured coverage."]
        all_reached = all(item["status"] == "reached" for item in costs)
        same_rounds = all(next(item for item in costs if (item["version"], item["arm"], item["repetition"]) ==
                               (version, "B", rep))["first_target_round"] ==
                          next(item for item in costs if (item["version"], item["arm"], item["repetition"]) ==
                               (version, "C", rep))["first_target_round"]
                          for version in config["versions"] for rep in range(1, config["repetitions"]+1))
        if all_reached and same_rounds:
            deltas = [next(item for item in costs if (item["version"], item["arm"], item["repetition"]) ==
                           (version, "C", rep))["api_tokens"] -
                      next(item for item in costs if (item["version"], item["arm"], item["repetition"]) ==
                           (version, "B", rep))["api_tokens"]
                      for version in config["versions"] for rep in range(1, config["repetitions"]+1)]
            lines += ["", f"C did not improve line-target attainment: all paired runs reached the target in the same round. C used {statistics.mean(deltas):.0f} more API tokens on average to reach it (paired range {min(deltas)}–{max(deltas)}). Wall time varied by run. This is a descriptive pilot result, not a statistical-significance claim."]
    if not rows:
        lines += ["", "No valid model responses were accepted, so no DUT stimulus round ran and B/C coverage cannot be compared."]
    lines += ["", "This run is an infrastructure smoke test, **not an LLM outcome**." if mode == "mock" else
              "Individual repetitions are descriptive; the pilot is too small for statistical significance.",
              "", "The checker asserts valid front data, empty/full, asynchronous reset, synchronous clear, and enable hold against a separate occupancy model. The CVDP prose does not pin down almost-empty/full timing thresholds; those flags are checked on reset/clear and otherwise observed without functional verdict.",
              "", "Coverage means the number of Verilator Coverage-3 DUT counters with hits > 0: line includes case/block/elsif source points; branch has separate if/else outcomes; expression has reported Boolean outcomes; toggle has separate bit 0→1/1→0 transitions. Testbench counters are excluded. A shared egg class does not transfer a hit between source lines. Expression denominators differ across the two RTL versions, so compare B with C only within the same version. Token ROI is newly covered branch points per 1,000 API-reported input-plus-output tokens; mock mode has no API token ROI.",
              "", "The typed extraction and egg rewrites cover binary/two-state combinational activation guards only. Each version has 49 extracted targets and 18 unsupported expressions; their records remain in typed-predicates.json. Event context remains separate; every unmapped raw coverage point stays in the prompt and denominator. The common reset/idle seed is replayed in each simulation and counted in executed cycles. The directed ceiling is a separate calibration outside model prompts and arm costs.",
              "", "All source hashes, tool/model settings, simulator commands, common seed, separate calibration ceiling, per-call logs, saved prompts, raw coverage files, round JSONL/CSV, target costs, and comparison plots are adjacent to this report."]
    output.joinpath("REPORT.md").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("mock", "live", "replay"), required=True)
    parser.add_argument("--config", default="configs/queue_bc_pilot.json")
    parser.add_argument("--output", required=True)
    parser.add_argument("--replay-calls")
    args = parser.parse_args()
    config = json.loads((ROOT / args.config).read_text())
    frozen(config)
    if args.mode == "replay" and not args.replay_calls:
        parser.error("--replay-calls required")
    model = (OpenAIModel(config, schema=SCHEMA, schema_name="queue_actions") if args.mode == "live" else
             MockQueue(config) if args.mode == "mock" else ReplayQueue(args.replay_calls))
    evidence_mode = "mock" if args.mode == "mock" or (args.mode == "replay" and model.source_mode == "mock") else args.mode
    output = (ROOT / args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    cargo_seconds, _ = command(["cargo", "build", "--locked", "--offline", "--manifest-path", "egraph/Cargo.toml",
                                "--target-dir", "build/queue-cargo"],
                               output / "cargo-build.log")
    extractions, all_targets, graph, egg_seconds = semantic_setup(output)
    rows, setups = [], {}
    for version in config["versions"]:
        folder = output / version
        folder.mkdir()
        source, _ = VERSIONS[version]
        binary, compile_seconds, compile_argv = compile_version(folder, version)
        initial_seconds, initial_log, initial_checked, initial_points = simulate(binary, folder, "common-initial", [], source)
        if initial_checked["functional_errors"]:
            raise AssertionError("Common seed fails the independent checker")
        reference = reference_actions()
        validate_actions({"actions": reference}, len(reference))
        ceiling_seconds, _, ceiling_checked, ceiling_points = simulate(binary, folder, "reference-ceiling", reference, source)
        denominator = {point_id(p) for p in initial_points}
        if denominator != {point_id(p) for p in ceiling_points}:
            raise AssertionError("Coverage denominator changed")
        if summary(ceiling_points)["line"]["covered"] < config["target_line_points"]:
            raise ValueError("Preregistered target exceeds separate directed ceiling")
        targets = extractions[version]["targets"]
        selected = [t for t in targets if t["guard_depth"] == 4 and t["case_value"] in ("2'01", "2'10")]
        if len(selected) != 12:
            raise AssertionError("Selected source map changed")
        # This check is performed before any model call for either arm.
        for target in selected:
            matches = [p for p in initial_points if p["line"] == target["line"] and
                       p["type"] == "line" and p["outcome"] == "case"]
            if len(matches) != 1 or matches[0]["hits"]:
                raise AssertionError("Selected counter missing or covered by seed")
        setups[version] = {"compile_seconds": compile_seconds, "compile_command": [str(x) for x in compile_argv],
                           "initial_simulation_seconds": initial_seconds,
                           "initial_coverage": summary(initial_points),
                           "reference_ceiling_simulation_seconds": ceiling_seconds,
                           "reference_ceiling": {"coverage": summary(ceiling_points), "checker": ceiling_checked,
                                                 "cycles": ceiling_checked["checks"]}}
        json_write(folder / "reference-ceiling.json", setups[version]["reference_ceiling"])
        seed_line = summary(initial_points)["line"]["covered"]
        seed_branch = summary(initial_points)["branch"]["covered"]
        for arm in config["arms"]:
            for rep in range(1, config["repetitions"] + 1):
                history = []
                points, checked, log = initial_points, initial_checked, initial_log
                totals = dict(calls=0, retries=0, failed_attempts=0, input_tokens=0, output_tokens=0,
                              executions=0, cycles=0, model_seconds=0.0, simulation_seconds=0.0,
                              wall_seconds=0.0, failures={key: 0 for key in
                              ("data_errors", "occupancy_errors", "reset_errors", "clear_errors", "enable_errors")})
                for round_no in range(1, config["rounds"] + 1):
                    tick = time.perf_counter()
                    messages = render_messages(arm, source, history, checked, log, points,
                                               targets, graph, extractions[version]["atoms"],
                                               config["max_new_cycles"], round_no, targets)
                    previous = summary(points)
                    accepted = None
                    for attempt in range(1, config["max_retries"] + 2):
                        current = list(messages)
                        if attempt > 1:
                            current.append({"role": "user", "content":
                                            f"Previous response failed validation: {failure}. Return valid cycle actions."})
                        prompt = output / f"prompt-{version}-{arm}-{rep}-{round_no}-{attempt}.json"
                        json_write(prompt, current)
                        size = token_estimate(current)
                        if size > config["max_input_tokens_conservative_byte_cap"]:
                            raise RuntimeError(f"Prompt byte cap exceeded: {prompt}")
                        context = {"version": version, "arm": arm, "repetition": rep, "round": round_no}
                        totals["calls"] += 1
                        entry = {**context, "attempt": attempt, "mode": args.mode, "prompt_path": prompt.name,
                                 "prompt_conservative_byte_count": size,
                                 "settings": {key: config[key] for key in
                                              ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds")}}
                        fatal = None
                        call_tick = time.perf_counter()
                        try:
                            response = model.generate(current, context)
                            entry.update(response)
                            usage = response["usage"]
                            if usage["input_tokens"] is not None:
                                totals["input_tokens"] += usage["input_tokens"]
                                totals["output_tokens"] += usage["output_tokens"]
                            accepted = validate_actions(response["parsed"], config["max_new_cycles"], history)
                            entry["actions"] = accepted
                            entry["accepted"] = True
                        except ModelResponseError as exc:
                            entry.update(exc.record)
                            usage = exc.record["usage"]
                            if usage["input_tokens"] is not None:
                                totals["input_tokens"] += usage["input_tokens"]
                                totals["output_tokens"] += usage["output_tokens"]
                            failure = exc.reason
                            entry.update({"accepted": False, "validation_failure": failure})
                        except ValueError as exc:
                            failure = str(exc)
                            entry.update({"accepted": False, "validation_failure": failure})
                        except Exception as exc:
                            failure = type(exc).__name__
                            entry.update({"accepted": False, "error_type": failure})
                            if failure in {"AuthenticationError", "PermissionDeniedError", "NotFoundError", "BadRequestError"}:
                                fatal = failure
                        entry["attempt_wall_seconds"] = time.perf_counter() - call_tick
                        totals["model_seconds"] += entry["attempt_wall_seconds"]
                        append_jsonl(output / "calls.jsonl", entry)
                        if fatal: raise RuntimeError(f"Non-retryable API error: {fatal}; see calls.jsonl")
                        if accepted is not None: break
                        totals["failed_attempts"] += 1
                        totals["retries"] += int(attempt <= config["max_retries"])
                    if accepted is None:
                        append_jsonl(output / "failed-rounds.jsonl", {**context, "status": "no_valid_model_response"})
                        continue
                    history.extend(accepted)
                    seconds, log, checked, points = simulate(binary, folder, f"{arm}-{rep}-{round_no}", history, source)
                    if {point_id(p) for p in points} != denominator:
                        raise AssertionError("DUT counter identity changed")
                    totals["executions"] += 1
                    totals["cycles"] += checked["checks"]
                    totals["simulation_seconds"] += seconds
                    for key in totals["failures"]: totals["failures"][key] += checked[key]
                    totals["wall_seconds"] += time.perf_counter() - tick
                    cover = summary(points)
                    tokens = totals["input_tokens"] + totals["output_tokens"] if evidence_mode != "mock" else None
                    categories = [key.removesuffix("_errors") for key, n in totals["failures"].items() if n]
                    row = {**context, "status": "ok", "new_actions": len(accepted), "cumulative_actions": len(history),
                           **{f"{kind}_{part}": cover[kind][part] for kind in KINDS for part in ("covered", "total")},
                           "functional_failures": checked["functional_errors"],
                           **{key: checked[key] for key in totals["failures"]},
                           "cumulative_failure_events": sum(totals["failures"].values()),
                           "distinct_defect_count": len(categories), "distinct_defects": ";".join(categories),
                           "new_line_points_vs_initial": cover["line"]["covered"] - seed_line,
                           "new_branch_points_vs_initial": cover["branch"]["covered"] - seed_branch,
                           "new_line_points_this_round": cover["line"]["covered"] - previous["line"]["covered"],
                           "cumulative_api_input_tokens": totals["input_tokens"] if tokens is not None else None,
                           "cumulative_api_output_tokens": totals["output_tokens"] if tokens is not None else None,
                           "cumulative_api_tokens": tokens,
                           "token_roi_new_lines_per_1000_tokens": round(1000*(cover["line"]["covered"]-seed_line)/tokens, 6) if tokens else None,
                           "token_roi_new_branches_per_1000_tokens": round(1000*(cover["branch"]["covered"]-seed_branch)/tokens, 6) if tokens else None,
                           "cumulative_model_calls": totals["calls"], "cumulative_retries": totals["retries"],
                           "cumulative_failed_model_attempts": totals["failed_attempts"],
                           "cumulative_simulator_executions": totals["executions"],
                           "cumulative_executed_cycles": totals["cycles"],
                           "cumulative_model_seconds": round(totals["model_seconds"], 6),
                           "cumulative_simulation_seconds": round(totals["simulation_seconds"], 6),
                           "cumulative_compilation_seconds_amortized": round(compile_seconds/(2*config["repetitions"]), 6),
                           "cumulative_seed_seconds_amortized": round(initial_seconds/(2*config["repetitions"]), 6),
                           "cumulative_egg_preprocessing_seconds_amortized": round(egg_seconds/(2*config["repetitions"]), 6) if arm == "C" else 0,
                           "cumulative_total_wall_seconds": round(totals["wall_seconds"] +
                               (compile_seconds+initial_seconds)/(2*config["repetitions"]) +
                               (egg_seconds/(2*config["repetitions"]) if arm == "C" else 0), 6)}
                    rows.append(row)
                    append_jsonl(output / "rounds.jsonl", {**row, "coverage_points": points, "checker": checked,
                                  "sim_log_path": f"{version}/{arm}-{rep}-{round_no}.sim.log"})
                    print(f"{version} {arm} rep {rep} round {round_no}: line {row['line_covered']}/41", flush=True)
    csv_write(output / "rounds.csv", rows)
    csv_write(output / "target_costs.csv", target_costs(rows, config))
    git_env = dict(os.environ)
    git_env.pop("OPENAI_API_KEY", None)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                            text=True, check=True, env=git_env).stdout.strip()
    metadata = {"git_commit": commit, "configuration": config, "mode": args.mode,
                "evidence_mode": evidence_mode, "versions": tool_versions(),
                "shared_setup": {"cargo_build_seconds": cargo_seconds,
                                 "egg_preprocessing_seconds": egg_seconds,
                                 "compilations": 2, "common_initial_executions": 2,
                                 "reference_ceiling_executions": 2},
                "version_setups": setups, "elapsed_wall_seconds": time.perf_counter()-started,
                "solver_or_deterministic_search_in_prompts": False,
                "checker_contract": "valid front data; empty/full with capacity DEPTH-1; asynchronous reset; synchronous clear; enable hold; almost flags only on reset/clear",
                "replay_policy": "fresh simulator process per round, repeat six-cycle seed and all accumulated actions",
                "token_roi_definition": "newly covered DUT branch points since common seed per 1000 API-reported input-plus-output tokens; cached and reasoning subcounts are included in totals and never added again",
                "amortization_policy": "per-version compilation and seed simulation split evenly across six B/C repetitions; egg preprocessing split across six C repetitions; separate directed ceiling excluded",
                "semantic_mapping": {version: {"targets": len(item["targets"]),
                                                "unsupported": len(item["unsupported"])}
                                     for version, item in extractions.items()},
                "raw_denominators_preserved": True}
    json_write(output / "metadata.json", metadata)
    plot(rows, output, evidence_mode)
    write_report(rows, config, metadata, output, evidence_mode)
    print(f"Output: {output}", flush=True)


if __name__ == "__main__":
    main()
