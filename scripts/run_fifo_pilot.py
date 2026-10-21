#!/usr/bin/env python3
"""Matched A/B/C FIFO pilot, using the CVDP sync_fifo context RTL."""
import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import time
from pathlib import Path

from coverage import load, summary
from fifo_feedback import (CHECKER, DUT, INITIAL, SCHEMA, SOURCE, SPEC, extract,
                           render_messages, validate_actions)
from pilot_feedback import point_id
from pilot_model import (ModelResponseError, OpenAIModel, ReplayModel,
                         token_estimate, usage_record)
from predicates import ROOT
from run_pilot import append_jsonl, command, csv_write, json_write, versions

ENGINE = ROOT / "egraph/target/debug/rtl-predicate-egraph"
KINDS = ("branch", "line", "expr", "toggle")


def frozen(config):
    for key, path in (("dut_sha256", DUT), ("spec_sha256", SPEC), ("checker_sha256", CHECKER)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != config[key]:
            raise RuntimeError(f"Frozen fixture mismatch: {path}")


def parse_result(log):
    match = re.search(r"RESULT checks=(\d+) functional_errors=(\d+) status_errors=(\d+) data_errors=(\d+) bins=([0-9a-fA-F]+)", log)
    if not match:
        raise ValueError("FIFO checker result absent")
    if int(match[2]) != int(match[3]) + int(match[4]):
        raise AssertionError("Checker category counts do not add to functional failures")
    return {"checks": int(match[1]), "functional_errors": int(match[2]),
            "status_errors": int(match[3]), "data_errors": int(match[4]),
            "functional_bins_mask": int(match[5], 16),
            "functional_bins_covered": int(match[5], 16).bit_count(), "functional_bins_total": 9}


def simulate(binary, out, name, actions):
    vector = out / f"{name}.vectors"
    if actions:
        vector.write_text("".join(f"{a['reset']} {a['push']} {a['pop']} {a['data']:02x}\n" for a in actions))
    cover = out / f"{name}.dat"
    argv = [binary, f"+MODE={int(bool(actions))}", "+COLLECT", f"+verilator+coverage+file+{cover}"]
    if actions:
        arg = str(vector.relative_to(ROOT)) if vector.is_relative_to(ROOT) else str(vector)
        if len(arg.encode()) > 127:
            raise ValueError("Stimulus path exceeds testbench plusarg width")
        argv.append(f"+VECTORS={arg}")
    elapsed, log = command(argv, out / f"{name}.sim.log", timeout=120)
    checked = parse_result(log)
    if checked["checks"] != len(INITIAL) + len(actions):
        raise AssertionError("Cycle accounting differs from executed checker steps")
    return elapsed, log, checked, load(cover, SOURCE)


def reference_actions():
    # Separate ceiling fixture. These directed values are never rendered in a
    # model prompt, nor reused as generated action data.
    actions = [dict(reset=0, push=1, pop=0, data=255 if i % 2 else 0) for i in range(8)]
    actions += [dict(reset=0, push=0, pop=0, data=0), dict(reset=0, push=1, pop=1, data=165)]
    actions += [dict(reset=0, push=0, pop=1, data=0) for _ in range(8)]
    actions += [dict(reset=0, push=1, pop=0, data=60 + i) for i in range(3)]
    actions += [dict(reset=1, push=0, pop=0, data=0)]
    for i in range(12):
        actions += [dict(reset=0, push=1, pop=0, data=(i * 37) & 255),
                    dict(reset=0, push=0, pop=1, data=0)]
    rng = random.Random(6998)
    count = 0
    for _ in range(256):
        push, pop = rng.randrange(2), rng.randrange(2)
        if count == 0:
            pop = 0
        if count == 8 and not pop:
            push = 0
        actions.append(dict(reset=0, push=push, pop=pop, data=rng.randrange(256)))
        count += push - pop
    return actions


def build(out):
    timings = {}
    timings["cargo_build_seconds"], _ = command(
        ["cargo", "build", "--locked", "--offline", "--manifest-path", "egraph/Cargo.toml"],
        out / "cargo-build.log")
    targets = extract()
    tick = time.perf_counter()
    _, engine_output = command([ENGINE], out / "egg.log", timeout=15, stdin=json.dumps(targets))
    graph = json.loads(engine_output)
    timings["egg_preprocessing_seconds"] = time.perf_counter() - tick
    if len({t["eclass"] for t in graph["targets"]}) != len(targets) or not all(t["equivalent"] for t in graph["targets"]):
        raise AssertionError("Egg failed to keep FIFO behavioral cases distinct")
    json_write(out / "egg-evidence.json", graph)
    json_write(out / "mapped-predicates.json", targets)
    yosys = f"read_verilog -sv {SOURCE}; hierarchy -check -top sync_fifo; proc; check; write_json {out}/yosys-netlist.json"
    timings["yosys_seconds"], _ = command(["yosys", "-Q", "-T", "-p", yosys], out / "yosys.log")
    builddir = out / "verilator-build"
    timings["verilator_compile_seconds"], _ = command(
        ["verilator", "-Wno-TIMESCALEMOD", "--cc", "--exe", "--build", "--timing", "--assert",
         "--coverage-line", "--coverage-toggle", "--coverage-expr", "--top-module", "tb_sync_fifo",
         "--Mdir", builddir, "-j", "2", DUT.relative_to(ROOT), CHECKER.relative_to(ROOT),
         ROOT / "scripts/sim_main_fifo.cpp"], out / "verilator-compile.log")
    return builddir / "Vtb_sync_fifo", targets, graph, timings


class MockFIFO:
    """Arm-blind legal random data for offline infrastructure checks only."""
    def __init__(self, config):
        self.config = config

    def generate(self, messages, context):
        rng = random.Random(self.config["seed"] + 1009 * context["repetition"] + context["round"])
        count = context["occupancy"]
        actions = []
        for _ in range(self.config["max_new_cycles"]):
            reset = int(rng.randrange(45) == 0)
            if reset:
                action = dict(reset=1, push=0, pop=0, data=0)
                count = 0
            else:
                push = rng.randrange(2)
                pop = rng.randrange(2)
                if count == 0:
                    pop = 0
                if count == 8 and not pop:
                    push = 0
                action = dict(reset=0, push=push, pop=pop, data=rng.randrange(256))
                count += push - pop
            actions.append(action)
        return {"requested_model": "mock-legal-random", "returned_model": "mock-legal-random",
                "response_id": f"mock-{context['repetition']}-{context['round']}",
                "latency_seconds": 0.0, "status": "completed", "incomplete_details": None,
                "usage": usage_record(None), "output_text": json.dumps({"actions": actions}),
                "parsed": {"actions": actions}}


def target_costs(rows, config):
    result = []
    for arm in config["arms"]:
        for rep in range(1, config["repetitions"] + 1):
            sample = [r for r in rows if r["arm"] == arm and r["repetition"] == rep]
            if not sample:
                continue
            reached = next((r for r in sample if r["toggle_covered"] >= config["target_toggle_points"]), None)
            row = reached or sample[-1]
            result.append({"arm": arm, "repetition": rep, "status": "reached" if reached else "not reached",
                           "first_round": reached["round"] if reached else None,
                           "toggle_covered": row["toggle_covered"], "api_tokens": row["cumulative_api_tokens"],
                           "executed_cycles": row["cumulative_executed_cycles"],
                           "simulator_executions": row["cumulative_simulator_executions"],
                           "wall_seconds": row["cumulative_total_wall_seconds"]})
    return result


def plots(rows, out, mode, denominator):
    cache = out / "plot-cache"
    cache.mkdir(exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(cache)
    os.environ["XDG_CACHE_HOME"] = str(cache)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fields = [("cumulative_api_tokens", "API input + output tokens"),
              ("cumulative_executed_cycles", "Executed cycles, including replays"),
              ("cumulative_simulator_executions", "Simulator executions"),
              ("cumulative_total_wall_seconds", "Wall seconds")]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    colors = {"A": "#0072b2", "B": "#e69f00", "C": "#009e73"}
    for axis, (field, label) in zip(axes.flat, fields):
        if field == "cumulative_api_tokens" and mode == "mock":
            axis.text(.5, .5, "No API tokens in mock mode", ha="center", va="center", transform=axis.transAxes)
        else:
            for arm in "ABC":
                for rep in sorted({r["repetition"] for r in rows}):
                    sample = [r for r in rows if r["arm"] == arm and r["repetition"] == rep]
                    if sample and sample[0][field] is not None:
                        axis.plot([r[field] for r in sample], [r["toggle_covered"] for r in sample],
                                  marker="o", color=colors[arm], alpha=.5, label=arm if rep == 1 else None)
        axis.set_xlabel(label)
        axis.set_ylabel(f"DUT toggle directions / {denominator}")
        axis.set_ylim(0, denominator)
        axis.grid(alpha=.2)
    axes[0, 1].legend(title="Feedback")
    fig.suptitle(f"FIFO {mode} pilot: individual repetitions")
    fig.tight_layout()
    fig.savefig(out / "comparison.png", dpi=150)
    plt.close(fig)


def report(rows, config, metadata, out, mode):
    lines = ["# CVDP context FIFO A/B/C pilot", "",
             f"Mode: **{mode}**. " + ("Offline mock smoke test; not LLM performance evidence." if mode == "mock" else
                                   "Recorded model actions replayed offline." if mode == "replay" else
                                   "Live Responses API model actions."), "",
             "This is `sync_fifo.sv` from CVDP `cvdp_agentic_low_power_channel_0001`. CVDP provided the RTL as a low-power-channel context file, not a standalone FIFO spec. The independent FIFO contract is authored in `examples/fifo/docs/specification.md`; DEPTH=8, DATA_W=8, and overflow/underflow are excluded.",
             "", "Primary outcome: Verilator DUT toggle-direction counters. The common four-cycle seed already covers all four branch counters. This FIFO cannot discriminate arms by branch coverage; expression, line, toggles and nine checker functional bins remain reported.",
             "", f"Preregistered toggle target: **{config['target_toggle_points']}/220**; separate directed plus seeded-random reference run: **{metadata['reference_ceiling']['coverage']['toggle']['covered']}/220** over {metadata['reference_ceiling']['cycles']} cycles. Reference actions are never in model prompts.",
             "", "| Arm | Rep | Final toggle | Line | Expr | Branch | Bins | API tokens | Cycles | Calls | Target |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    costs = {(x["arm"], x["repetition"]): x for x in target_costs(rows, config)}
    finals = {}
    for arm in "ABC":
        for rep in range(1, config["repetitions"] + 1):
            sample = [r for r in rows if r["arm"] == arm and r["repetition"] == rep]
            if not sample:
                continue
            row = sample[-1]
            finals[(arm, rep)] = row
            cost = costs[(arm, rep)]
            lines.append(f"| {arm} | {rep} | {row['toggle_covered']}/{row['toggle_total']} | "
                         f"{row['line_covered']}/{row['line_total']} | {row['expr_covered']}/{row['expr_total']} | "
                         f"{row['branch_covered']}/{row['branch_total']} | {row['functional_bins_covered']}/9 | "
                         f"{row['cumulative_api_tokens'] if row['cumulative_api_tokens'] is not None else 'n/a'} | "
                         f"{row['cumulative_executed_cycles']} | {row['cumulative_model_calls']} | "
                         f"{cost['status']}{' round '+str(cost['first_round']) if cost['first_round'] else ''} |")
    paired = [finals[("C", r)]["toggle_covered"] - finals[("B", r)]["toggle_covered"]
              for r in range(1, config["repetitions"] + 1) if ("C", r) in finals and ("B", r) in finals]
    if paired:
        lines += ["", f"Final paired C−B toggle-direction differences: {paired}. " +
                  ("Mock stimuli are arm-blind and cannot support an LLM benefit claim." if mode == "mock" else
                   "This small pilot is descriptive, not a significance test.")]
    first_bins = {arm: [next((r["functional_bins_covered"] for r in rows
                              if r["arm"] == arm and r["repetition"] == rep and r["round"] == 1), None)
                        for rep in range(1, config["repetitions"] + 1)] for arm in "ABC"}
    lines += ["", f"First-round functional-bin counts by repetition: A {first_bins['A']}, "
              f"B {first_bins['B']}, C {first_bins['C']} (of nine). "
              "Toggle saturation does not imply that every behavioral bin was hit in that round."]
    lines += ["", "| Arm | Rep | First 200/220 round | Tokens at target | Executed cycles | Simulator runs | Wall seconds |",
              "|---|---:|---|---:|---:|---:|---:|"]
    for arm in "ABC":
        for rep in range(1, config["repetitions"] + 1):
            cost = costs.get((arm, rep))
            if cost:
                lines.append(f"| {arm} | {rep} | {cost['first_round'] if cost['first_round'] else 'not reached'} | "
                             f"{cost['api_tokens'] if cost['api_tokens'] is not None else 'n/a'} | "
                             f"{cost['executed_cycles']} | {cost['simulator_executions']} | "
                             f"{cost['wall_seconds']:.3f} |")
    pairs = [(costs[("B", r)], costs[("C", r)]) for r in range(1, config["repetitions"] + 1)
             if ("B", r) in costs and ("C", r) in costs]
    if pairs and mode != "mock":
        token_delta = [c["api_tokens"] - b["api_tokens"] for b, c in pairs]
        cycle_delta = [c["executed_cycles"] - b["executed_cycles"] for b, c in pairs]
        run_delta = [c["simulator_executions"] - b["simulator_executions"] for b, c in pairs]
        lines += ["", f"At 200/220, paired C−B differences were API tokens {token_delta}, "
                  f"executed cycles {cycle_delta}, and simulator runs {run_delta}. "
                  "C did not improve coverage or measured API-token and simulator cost over B. "
                  "Wall-time differences are descriptive because independent API calls vary in latency; C's egg preprocessing share is included."]
        a_costs = [costs[("A", r)] for r in range(1, config["repetitions"] + 1)
                   if ("A", r) in costs]
        if len(a_costs) == len(pairs):
            lines += ["", "Relative to A, B reached 200/220 with fewer executed cycles and simulator runs in every repetition, "
                      "but used more API input+output tokens. Thus raw coverage changes the resource tradeoff rather than dominating text-only on every cost axis."]
    if mode == "live":
        retry_count = sum(r["cumulative_retries"] for r in finals.values())
        failed_count = sum(r["cumulative_failed_model_attempts"] for r in finals.values())
        checker_failures = sum(r["cumulative_functional_failure_events"] for r in finals.values())
        lines += ["", f"Across live repetitions: {retry_count} model retries, {failed_count} rejected model responses, "
                  f"and {checker_failures} checker failure observations. Rejected calls and their API tokens remain in the call log and cost totals."]
    lines += ["", "A receives specification, RTL, common stimulus, occupancy, checker failures and execution logs. B adds every uncovered raw DUT counter with source location and outcome. C receives the same raw evidence plus bounded egg-derived equivalent forms for five hash-guarded predicates, with unmapped counters disclosed. No solver or deterministic search supplies model stimulus.",
              "", "Every round runs the complete generated history after a fresh four-cycle reset/initialization. Executed cycle and simulator counts include every replay; compilation, common-initial and separate ceiling costs are in metadata. Coverage is flushed even on checker failures. Repeated failed observations are counts, while defect categories are deduplicated.",
              "", "Token ROI = new DUT toggle-direction counters versus the shared seed per 1,000 API-reported input+output tokens. Reasoning and cached-token fields are subsets and are not added twice. Mock token ROI is undefined.",
              "", "Egg uses two-state unsigned one-bit Boolean predicates. Multi-bit pointer comparisons are atomic guarded inputs; memory, clock, reset and state transition semantics are outside combinational normalization. All original Verilator coverage counters remain separate. The five mapped predicates are only a subset; unsupported/unmapped points are explicitly listed in C feedback and retained in the raw denominator.",
              "", "At the shared seed, only two mapped egg predicates (simultaneous push/pop and the full-pointer conjunction) are uncovered; 186 other uncovered locations have no sound mapping and remain in the raw denominator. This FIFO has little repeated predicate redundancy, so C has no observed advantage over B here. A more discriminating next study should use nested/repeated equivalent predicates in equivalence-checked RTL variants, then a larger FIFO controller with full/empty, simultaneous operations, wraparound and reset transitions.",
              "", "Per-call JSONL, per-round JSONL/CSV, rendered prompts, raw counter files, exact metadata, and comparison plot are adjacent to this report.", ""]
    (out / "REPORT.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["live", "mock", "replay"], required=True)
    parser.add_argument("--config", default="configs/fifo_pilot.json")
    parser.add_argument("--output", required=True)
    parser.add_argument("--replay-calls")
    args = parser.parse_args()
    config = json.loads((ROOT / args.config).read_text())
    frozen(config)
    if config["arms"] != ["A", "B", "C"] or not 1 <= config["target_toggle_points"] <= 220:
        raise ValueError("Invalid preregistered configuration")
    if args.mode == "replay" and not args.replay_calls:
        parser.error("--replay-calls is required for replay")
    model = OpenAIModel(config, schema=SCHEMA, schema_name="fifo_actions") if args.mode == "live" else (
        MockFIFO(config) if args.mode == "mock" else ReplayModel(args.replay_calls))
    evidence_mode = "mock" if args.mode == "mock" or (args.mode == "replay" and model.source_mode == "mock") else args.mode
    out = (ROOT / args.output).resolve()
    out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    binary, targets, graph, timings = build(out)
    initial_seconds, initial_log, initial_checker, initial_points = simulate(binary, out, "common-initial", [])
    if initial_checker["functional_errors"]:
        raise AssertionError("Shared initial stimulus fails checker")
    ceiling_actions = reference_actions()
    validate_actions({"actions": ceiling_actions}, len(ceiling_actions), INITIAL)
    ceiling_seconds, _, ceiling_checker, ceiling_points = simulate(binary, out, "reference-ceiling", ceiling_actions)
    if ceiling_checker["functional_errors"]:
        raise AssertionError("Directed reference ceiling fails checker")
    baseline_ids = {point_id(p) for p in initial_points}
    if baseline_ids != {point_id(p) for p in ceiling_points}:
        raise AssertionError("Coverage denominator changed in ceiling")
    ref = {"coverage": summary(ceiling_points), "checker": ceiling_checker,
           "cycles": ceiling_checker["checks"], "simulator_executions": 1,
           "simulation_seconds": ceiling_seconds}
    json_write(out / "reference-ceiling.json", ref)
    if config["target_toggle_points"] > ref["coverage"]["toggle"]["covered"]:
        raise ValueError("Preregistered toggle target exceeds measured reference ceiling")
    rows = []
    calls = out / "calls.jsonl"
    rounds = out / "rounds.jsonl"
    initial_toggle = summary(initial_points)["toggle"]["covered"]
    for arm in config["arms"]:
        for rep in range(1, config["repetitions"] + 1):
            history = []
            points, checked, log = initial_points, initial_checker, initial_log
            totals = {"model_calls": 0, "failed_attempts": 0, "retries": 0,
                      "input_tokens": 0, "output_tokens": 0, "executions": 0, "cycles": 0,
                      "model_seconds": 0.0, "simulation_seconds": 0.0, "wall_seconds": 0.0,
                      "failure_events": 0, "status_failure_events": 0, "data_failure_events": 0}
            for round_no in range(1, config["rounds"] + 1):
                tick = time.perf_counter()
                messages = render_messages(arm, SPEC.read_text(), DUT.read_text(), history, checked, log,
                                           points, targets, graph, config["max_new_cycles"], round_no)
                previous = summary(points)
                accepted = None
                for attempt in range(1, config["max_retries"] + 2):
                    current_messages = list(messages)
                    if attempt > 1:
                        current_messages.append({"role": "user", "content":
                                                 f"Previous response failed validation: {failure}. Return a valid actions array."})
                    prompt_path = out / f"prompt-{arm}-{rep}-{round_no}-{attempt}.json"
                    json_write(prompt_path, current_messages)
                    byte_count = token_estimate(current_messages)
                    if byte_count > config["max_input_tokens_conservative_byte_cap"]:
                        raise RuntimeError(f"Input byte cap exceeded: {prompt_path}")
                    context = {"arm": arm, "repetition": rep, "round": round_no}
                    from fifo_feedback import occupancy
                    context["occupancy"] = occupancy(INITIAL + history)
                    totals["model_calls"] += 1
                    entry = {"arm": arm, "repetition": rep, "round": round_no,
                             "attempt": attempt, "mode": args.mode,
                             "prompt_path": prompt_path.name,
                             "prompt_conservative_byte_count": byte_count,
                             "settings": {k: config[k] for k in ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds")}}
                    fatal = None
                    call_tick = time.perf_counter()
                    try:
                        response = model.generate(current_messages, context)
                        entry.update(response)
                        usage = response["usage"]
                        if usage["input_tokens"] is not None:
                            totals["input_tokens"] += usage["input_tokens"]
                            totals["output_tokens"] += usage["output_tokens"]
                        accepted = validate_actions(response["parsed"], config["max_new_cycles"], INITIAL + history)
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
                    append_jsonl(calls, entry)
                    if fatal:
                        raise RuntimeError(f"Non-retryable model API error: {fatal}; see {calls}")
                    if accepted is not None:
                        break
                    totals["failed_attempts"] += 1
                    totals["retries"] += int(attempt <= config["max_retries"])
                if accepted is None:
                    break
                history.extend(accepted)
                seconds, log, checked, points = simulate(binary, out, f"{arm}-{rep}-{round_no}", history)
                if {point_id(p) for p in points} != baseline_ids:
                    raise AssertionError("DUT counter identity/denominator changed")
                totals["executions"] += 1
                totals["cycles"] += checked["checks"]
                totals["simulation_seconds"] += seconds
                totals["failure_events"] += checked["functional_errors"]
                totals["status_failure_events"] += checked["status_errors"]
                totals["data_failure_events"] += checked["data_errors"]
                totals["wall_seconds"] += time.perf_counter() - tick
                covered = summary(points)
                api_tokens = (totals["input_tokens"] + totals["output_tokens"] if evidence_mode != "mock" else None)
                row = {"arm": arm, "repetition": rep, "round": round_no, "status": "ok",
                       "new_actions": len(accepted), "cumulative_actions": len(history),
                       **{f"{kind}_{part}": covered[kind][part] for kind in KINDS for part in ("covered", "total")},
                       "functional_bins_covered": checked["functional_bins_covered"],
                       "functional_bins_mask": checked["functional_bins_mask"],
                       "functional_failures": checked["functional_errors"],
                       "status_failures": checked["status_errors"],
                       "data_failures": checked["data_errors"],
                       "cumulative_functional_failure_events": totals["failure_events"],
                       "cumulative_status_failure_events": totals["status_failure_events"],
                       "cumulative_data_failure_events": totals["data_failure_events"],
                       "distinct_defect_count": int(totals["status_failure_events"] > 0) + int(totals["data_failure_events"] > 0),
                       "distinct_defects": ";".join(name for name, count in
                                                    (("status_mismatch", totals["status_failure_events"]),
                                                     ("data_mismatch", totals["data_failure_events"])) if count),
                       "new_toggle_points_vs_initial": covered["toggle"]["covered"] - initial_toggle,
                       "new_toggle_points_this_round": covered["toggle"]["covered"] - previous["toggle"]["covered"],
                       "cumulative_api_input_tokens": totals["input_tokens"] if api_tokens is not None else None,
                       "cumulative_api_output_tokens": totals["output_tokens"] if api_tokens is not None else None,
                       "cumulative_api_tokens": api_tokens,
                       "token_roi_new_toggles_per_1000_tokens": round(1000 * (covered["toggle"]["covered"] - initial_toggle) / api_tokens, 6) if api_tokens else None,
                       "cumulative_model_calls": totals["model_calls"], "cumulative_retries": totals["retries"],
                       "cumulative_failed_model_attempts": totals["failed_attempts"],
                       "cumulative_simulator_executions": totals["executions"],
                       "cumulative_executed_cycles": totals["cycles"],
                       "cumulative_model_seconds": round(totals["model_seconds"], 6),
                       "cumulative_simulation_seconds": round(totals["simulation_seconds"], 6),
                       "cumulative_egg_preprocessing_seconds_amortized": round(timings["egg_preprocessing_seconds"] / config["repetitions"], 6) if arm == "C" else 0,
                       "cumulative_total_wall_seconds": round(totals["wall_seconds"] + (timings["egg_preprocessing_seconds"] / config["repetitions"] if arm == "C" else 0), 6)}
                rows.append(row)
                append_jsonl(rounds, {**row, "coverage_points": points, "checker": checked,
                                      "sim_log_path": f"{arm}-{rep}-{round_no}.sim.log"})
                print(f"{arm} rep {rep} round {round_no}: toggle {row['toggle_covered']}/{row['toggle_total']}, bins {row['functional_bins_covered']}/9", flush=True)
    csv_write(out / "rounds.csv", rows)
    csv_write(out / "target_costs.csv", target_costs(rows, config))
    git_env = dict(os.environ)
    git_env.pop("OPENAI_API_KEY", None)
    metadata = {"git_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                             capture_output=True, text=True, check=True, env=git_env).stdout.strip(),
                "fixture_hashes": {k: config[k] for k in ("dut_sha256", "spec_sha256", "checker_sha256")},
                "versions": versions(), "configuration": config, "mode": args.mode,
                "shared_setup": {**timings, "verilator_compilations": 1, "cargo_builds": 1,
                                 "yosys_invocations": 1, "common_initial_simulator_executions": 1,
                                 "common_initial_simulation_seconds": initial_seconds,
                                 "reference_ceiling_simulator_executions": 1,
                                 "reference_ceiling_simulation_seconds": ceiling_seconds},
                "common_initial_coverage": summary(initial_points), "reference_ceiling": ref,
                "elapsed_wall_seconds": time.perf_counter() - started,
                "evidence_mode": evidence_mode, "solver_or_deterministic_search_enabled": False,
                "simulator_commands": {"compile": "see verilator-compile.log; fixed command in scripts/run_fifo_pilot.py",
                                       "run": "Vtb_sync_fifo +MODE=1 +COLLECT +VECTORS=<validated actions> +verilator+coverage+file+<coverage.dat>"}}
    json_write(out / "metadata.json", metadata)
    plots(rows, out, evidence_mode, summary(initial_points)["toggle"]["total"])
    report(rows, config, metadata, out, evidence_mode)
    print(f"Output: {out}", flush=True)


if __name__ == "__main__":
    main()
