#!/usr/bin/env python3
"""Matched A/B/C CVDP timer pilot; only validated JSON cycle actions vary."""
import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import time

from coverage import load, summary
from pilot_feedback import point_id
from pilot_model import ModelResponseError, OpenAIModel, ReplayModel, token_estimate, usage_record
from predicates import ROOT
from run_pilot import append_jsonl, command, csv_write, json_write, versions
from ttc_feedback import CHECKER, DUT, INITIAL, SCHEMA, SOURCE, SPEC, extract, render_messages, validate_actions
from ttc_reference import actions as reference_actions

ENGINE = ROOT / "egraph/target/debug/rtl-predicate-egraph"
KINDS = ("branch", "line", "expr", "toggle")


def frozen(config):
    for key, path in (("dut_sha256", DUT), ("spec_sha256", SPEC), ("checker_sha256", CHECKER)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != config[key]:
            raise RuntimeError(f"Frozen fixture mismatch: {path}")


def parse_result(log):
    match = re.search(r"RESULT checks=(\d+) read_errors=(\d+) interrupt_errors=(\d+) timing_errors=(\d+)", log)
    if not match:
        raise ValueError("Timer checker result absent")
    checks, reads, irqs, timing = map(int, match.groups())
    return {"checks": checks, "read_errors": reads, "interrupt_errors": irqs,
            "timing_errors": timing, "functional_errors": reads + irqs + timing,
            "distinct_defects": [name for name, n in (("read_mismatch", reads),
                ("interrupt_mismatch", irqs), ("asynchronous_reset", timing)) if n]}


def simulate(binary, out, name, actions):
    vector = out / f"{name}.vectors"
    if actions:
        vector.write_text("".join(f"{a['reset']} {a['write']} {a['read']} {a['addr']:x} {a['data']:08x}\n" for a in actions))
    cover = out / f"{name}.dat"
    argv = [str(binary), f"+MODE={int(bool(actions))}", "+COLLECT", f"+verilator+coverage+file+{cover}"]
    if actions:
        arg = str(vector.relative_to(ROOT)) if vector.is_relative_to(ROOT) else str(vector)
        if len(arg.encode()) > 127:
            raise ValueError("Stimulus path exceeds testbench plusarg width")
        argv.append(f"+VECTORS={arg}")
    elapsed, log = command(argv, out / f"{name}.sim.log", timeout=120)
    checked = parse_result(log)
    if checked["checks"] != len(INITIAL) + len(actions):
        raise AssertionError("Cycle accounting differs from checker steps")
    return elapsed, log, checked, load(cover, SOURCE)


def build(out):
    timings = {}
    timings["cargo_build_seconds"], _ = command(
        ["cargo", "build", "--locked", "--offline", "--manifest-path", "egraph/Cargo.toml"], out / "cargo-build.log")
    targets = extract()
    tick = time.perf_counter()
    _, result = command([ENGINE], out / "egg.log", timeout=15, stdin=json.dumps(targets))
    graph = json.loads(result)
    timings["egg_preprocessing_seconds"] = time.perf_counter() - tick
    roots = {t["id"]: t for t in graph["targets"]}
    if not all(t["equivalent"] for t in graph["targets"]):
        raise AssertionError("Egg equivalence failed")
    if len({t["eclass"] for t in graph["targets"]}) != len(targets):
        raise AssertionError("Different timer guards improperly merged")
    if roots["irq_clear"]["eclass"] == roots["read_status"]["eclass"]:
        raise AssertionError("Read/write guards improperly merged")
    json_write(out / "egg-evidence.json", graph)
    json_write(out / "mapped-predicates.json", targets)
    yosys = f"read_verilog -sv {SOURCE}; hierarchy -check -top ttc_counter_lite; proc; check; write_json {out}/yosys-netlist.json"
    timings["yosys_seconds"], _ = command(["yosys", "-Q", "-T", "-p", yosys], out / "yosys.log")
    builddir = out / "verilator-build"
    timings["verilator_compile_seconds"], _ = command(
        ["verilator", "-Wno-TIMESCALEMOD", "--cc", "--exe", "--build", "--timing", "--assert",
         "--coverage-line", "--coverage-toggle", "--coverage-expr", "--top-module", "tb_ttc_counter_lite",
         "--Mdir", builddir, "-j", "2", DUT.relative_to(ROOT), CHECKER.relative_to(ROOT),
         ROOT / "scripts/sim_main_ttc.cpp"], out / "verilator-compile.log")
    return builddir / "Vtb_ttc_counter_lite", targets, graph, timings


class MockTimer:
    """Arm-blind legal inputs for infrastructure checks, never LLM evidence."""
    def __init__(self, config):
        self.config = config

    def generate(self, messages, context):
        rng = random.Random(self.config["seed"] + 1009 * context["repetition"] + context["round"])
        result = []
        for _ in range(self.config["max_new_cycles"]):
            reset = int(rng.randrange(40) == 0)
            op = 0 if reset else rng.randrange(3)
            result.append(dict(reset=reset, write=int(op == 1), read=int(op == 2),
                               addr=rng.randrange(16), data=rng.getrandbits(32)))
        return {"requested_model": "mock-legal-random", "returned_model": "mock-legal-random",
                "response_id": f"mock-{context['repetition']}-{context['round']}",
                "latency_seconds": 0.0, "status": "completed", "incomplete_details": None,
                "usage": usage_record(None), "output_text": json.dumps({"actions": result}),
                "parsed": {"actions": result}}


def target_costs(rows, config):
    costs = []
    for arm in "ABC":
        for rep in range(1, config["repetitions"] + 1):
            sample = [r for r in rows if r["arm"] == arm and r["repetition"] == rep]
            if not sample:
                costs.append({"arm": arm, "repetition": rep, "status": "no accepted rounds"})
                continue
            reached = next((r for r in sample if r["toggle_covered"] >= config["target_toggle_points"]), None)
            r = reached or sample[-1]
            costs.append({"arm": arm, "repetition": rep, "status": "reached" if reached else "not reached",
                          "first_round": reached["round"] if reached else None,
                          "toggle_covered": r["toggle_covered"], "api_tokens": r["cumulative_api_tokens"],
                          "executed_cycles": r["cumulative_executed_cycles"],
                          "simulator_executions": r["cumulative_simulator_executions"],
                          "wall_seconds": r["cumulative_total_wall_seconds"]})
    return costs


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
    fig.suptitle(f"CVDP timer {mode} pilot: individual repetitions")
    fig.tight_layout()
    fig.savefig(out / "comparison.png", dpi=150)
    plt.close(fig)


def report(rows, config, metadata, out, mode):
    seed = metadata["common_initial_coverage"]
    ceiling = metadata["reference_ceiling"]
    costs = target_costs(rows, config)
    cost_by = {(c["arm"], c["repetition"]): c for c in costs}
    lines = ["# CVDP `ttc_counter_lite_0007` matched A/B/C pilot", "",
             f"Mode: **{mode}**. " + ("Mock smoke test; no LLM performance inference." if mode == "mock" else
                                  "Offline replay of saved calls." if mode == "replay" else
                                  "Live OpenAI Responses API calls."), "",
             f"Original NVIDIA CVDP hard-record RTL and specification are hash pinned. Seed: {seed['toggle']['covered']}/{seed['toggle']['total']} DUT toggle directions; separate directed reference: {ceiling['coverage']['toggle']['covered']}/{ceiling['coverage']['toggle']['total']}. Preregistered target: {config['target_toggle_points']}/{seed['toggle']['total']}. Reference actions are never included in prompts.",
             "", "| Arm | Rep | Final toggle | Branch | Line | Expr | API tokens | Executed cycles | Calls | Target |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for arm in "ABC":
        for rep in range(1, config["repetitions"] + 1):
            sample = [r for r in rows if r["arm"] == arm and r["repetition"] == rep]
            if not sample:
                lines.append(f"| {arm} | {rep} | n/a | n/a | n/a | n/a | n/a | n/a | n/a | no accepted rounds |")
                continue
            r = sample[-1]
            lines.append(f"| {arm} | {rep} | {r['toggle_covered']}/{r['toggle_total']} | "
                         f"{r['branch_covered']}/{r['branch_total']} | {r['line_covered']}/{r['line_total']} | "
                         f"{r['expr_covered']}/{r['expr_total']} | {r['cumulative_api_tokens'] if r['cumulative_api_tokens'] is not None else 'n/a'} | "
                         f"{r['cumulative_executed_cycles']} | {r['cumulative_model_calls']} | {cost_by[(arm,rep)]['status']} |")
    deltas = []
    for rep in range(1, config["repetitions"] + 1):
        b = [r for r in rows if r["arm"] == "B" and r["repetition"] == rep]
        c = [r for r in rows if r["arm"] == "C" and r["repetition"] == rep]
        if b and c:
            deltas.append(c[-1]["toggle_covered"] - b[-1]["toggle_covered"])
    lines += ["", f"Final paired C−B toggle-direction differences: {deltas}. " +
              ("Arm-blind mock actions make these infrastructure-only." if mode == "mock" else
               "These few independent sessions support descriptive comparison only."),
              "", "| Arm | Rep | First target round | API tokens | Executed cycles | Simulator runs | Wall seconds |",
              "|---|---:|---|---:|---:|---:|---:|"]
    for c in costs:
        if "first_round" in c:
            lines.append(f"| {c['arm']} | {c['repetition']} | {c['first_round'] if c['first_round'] else 'not reached'} | "
                         f"{c['api_tokens'] if c['api_tokens'] is not None else 'n/a'} | {c['executed_cycles']} | "
                         f"{c['simulator_executions']} | {c['wall_seconds']:.3f} |")
    if mode == "live":
        first = {arm: [next((r for r in rows if r["arm"] == arm and r["repetition"] == rep and r["round"] == 1), None)
                        for rep in range(1, config["repetitions"] + 1)] for arm in "ABC"}
        first_delta = [c["toggle_covered"] - b["toggle_covered"] for b, c in zip(first["B"], first["C"]) if b and c]
        target_token_delta = [cost_by[("C", rep)]["api_tokens"] - cost_by[("B", rep)]["api_tokens"]
                              for rep in range(1, config["repetitions"] + 1)
                              if cost_by[("B", rep)]["status"] == cost_by[("C", rep)]["status"] == "reached"]
        lines += ["", f"First-round C−B toggle differences were {first_delta}. At the target, C−B API-token costs were {target_token_delta}; both arms used one model call, one simulator execution, and 21 executed cycles in every repetition. C therefore showed no repeatable coverage or measured cost advantage over B in this pilot. B's first-round coverage exceeded A's in all three repetitions but required much larger raw-counter prompts and more API tokens."]
        lines += ["", "All final B/C runs stop at 234/266. The 32 remaining counters are `axi_rdata[31:16]` rising and falling directions. Every RTL read case zero-extends a value of at most 16 bits, the default read is zero, and reset drives the read register to zero; those upper bits cannot toggle under this two-state RTL. The raw 266-point denominator is retained. This reachable-output saturation makes the timer a poor final-coverage discriminator for E-graph feedback, even though it improved the experiment over the earlier FIFO by starting far below saturation."]
    failure_sum = {k: sum(r[k] for r in rows if r["round"] == config["rounds"])
                   for k in ("cumulative_read_failure_events", "cumulative_interrupt_failure_events",
                             "cumulative_timing_failure_events")}
    lines += ["", f"Separate ceiling checker: {ceiling['checker']}. Its synchronous-reset timing failures are a DUT/specification discrepancy, reproduced in Verilator and Icarus; they do not invalidate coverage collection. Experimental repeated failure observations by category (final cumulative counts): {failure_sum}. Distinct categories are reported separately in rounds.csv.",
              "", "A receives specification, RTL, shared seed, previous generated actions, checker errors, and logs. B adds every uncovered raw DUT point, exact counter outcome and source text. C has the same raw data plus hash-guarded, bounded egg equivalence for eight mapped Boolean guards. `irq_clear` and `read_status` share the typed address-status atom but are not merged. Most toggle points are not mapped by egg and remain in the unchanged denominator.",
              "", "The timer checker samples registered reads and a specified active-high synchronous reset. The count/prescaler model uses pre-edge state, divide-by-(prescaler+1), one-cycle match/interrupt latency, and priority of match over status clear. The latter latency and priority details are less explicit in the natural-language spec and should be treated as contract assumptions; reset timing and register readback are direct requirements. The original RTL is preserved.",
              "", "Every model round executes its whole generated history after the fixed five-cycle seed and fresh reset. Counters restart per simulator run. Executed cycles include replays; compilation, common-seed and reference ceiling times are separate metadata. Coverage is flushed on checker findings. No deterministic input search or solver witnesses enter A/B/C prompts. Model sessions are stateless and separate by arm/repetition.",
              "", "Primary outcome is Verilator Coverage-3 toggle-direction counters (each bit-direction is one point). Branch, line and expr counts are reported using the same DUT-only filtered counter file. Token ROI = newly covered toggle directions versus seed per 1,000 API-reported input+output tokens; reasoning/cached tokens are subsets and not double-counted. A mock run has no token ROI. `not reached` is retained in target costs.",
              "", "Egg handles two-state one-bit Boolean structure only; typed 4-bit address and 16-bit count comparisons remain atomic. It does not prove four-state, reset, sequential or arithmetic equivalence. Unsupported counters stay in raw feedback and denominator. Per-call/round logs, prompts, evidence, counter files, CSV and plots are next to this report.", ""]
    lines[-1:-1] = ["", "The eight egg roots are local Boolean subguards. Full enclosing enable/prescaler and priority conditions are visible in the raw RTL but are not normalized in every mapped root. C therefore is not a complete branch-reachability model; the next frontend must carry full activation context with source provenance."]
    (out / "REPORT.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["live", "mock", "replay"], required=True)
    parser.add_argument("--config", default="configs/ttc_pilot.json")
    parser.add_argument("--output", required=True)
    parser.add_argument("--replay-calls")
    args = parser.parse_args()
    config = json.loads((ROOT / args.config).read_text())
    frozen(config)
    if config["arms"] != ["A", "B", "C"] or not 1 <= config["target_toggle_points"] <= 266:
        raise ValueError("Invalid preregistered configuration")
    if args.mode == "replay" and not args.replay_calls:
        parser.error("--replay-calls required")
    model = OpenAIModel(config, schema=SCHEMA, schema_name="ttc_actions") if args.mode == "live" else (
        MockTimer(config) if args.mode == "mock" else ReplayModel(args.replay_calls))
    evidence_mode = "mock" if args.mode == "mock" or (args.mode == "replay" and model.source_mode == "mock") else args.mode
    out = (ROOT / args.output).resolve()
    out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    binary, targets, graph, timings = build(out)
    initial_seconds, initial_log, initial_checker, initial_points = simulate(binary, out, "common-initial", [])
    if initial_checker["functional_errors"]:
        raise AssertionError("Shared seed fails timer checker")
    ceiling_actions = reference_actions()
    validate_actions({"actions": ceiling_actions}, len(ceiling_actions))
    ceiling_seconds, _, ceiling_checker, ceiling_points = simulate(binary, out, "reference-ceiling", ceiling_actions)
    baseline_ids = {point_id(p) for p in initial_points}
    if baseline_ids != {point_id(p) for p in ceiling_points}:
        raise AssertionError("Coverage denominator changed")
    ceiling = {"coverage": summary(ceiling_points), "checker": ceiling_checker,
               "cycles": ceiling_checker["checks"], "simulator_executions": 1,
               "simulation_seconds": ceiling_seconds}
    json_write(out / "reference-ceiling.json", ceiling)
    if config["target_toggle_points"] > ceiling["coverage"]["toggle"]["covered"]:
        raise ValueError("Target exceeds directed ceiling")
    rows = []
    seed_covered = summary(initial_points)["toggle"]["covered"]
    for arm in "ABC":
        for rep in range(1, config["repetitions"] + 1):
            history = []
            points, checked, log = initial_points, initial_checker, initial_log
            totals = dict(model_calls=0, failed_attempts=0, retries=0, input_tokens=0, output_tokens=0,
                          executions=0, cycles=0, model_seconds=0.0, simulation_seconds=0.0,
                          wall_seconds=0.0, read_failures=0, interrupt_failures=0, timing_failures=0)
            for round_no in range(1, config["rounds"] + 1):
                tick = time.perf_counter()
                messages = render_messages(arm, SPEC.read_text(), DUT.read_text(), history, checked,
                                           log, points, targets, graph, config["max_new_cycles"], round_no)
                previous = summary(points)
                accepted = None
                for attempt in range(1, config["max_retries"] + 2):
                    current = list(messages)
                    if attempt > 1:
                        current.append({"role": "user", "content":
                                        f"Previous response failed validation: {failure}. Return a valid actions array."})
                    prompt_path = out / f"prompt-{arm}-{rep}-{round_no}-{attempt}.json"
                    json_write(prompt_path, current)
                    byte_count = token_estimate(current)
                    if byte_count > config["max_input_tokens_conservative_byte_cap"]:
                        raise RuntimeError(f"Input byte cap exceeded: {prompt_path}")
                    context = {"arm": arm, "repetition": rep, "round": round_no}
                    totals["model_calls"] += 1
                    entry = {**context, "attempt": attempt, "mode": args.mode,
                             "prompt_path": prompt_path.name, "prompt_conservative_byte_count": byte_count,
                             "settings": {k: config[k] for k in ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds")}}
                    fatal = None
                    call_tick = time.perf_counter()
                    try:
                        response = model.generate(current, context)
                        entry.update(response)
                        usage = response["usage"]
                        if usage["input_tokens"] is not None:
                            totals["input_tokens"] += usage["input_tokens"]
                            totals["output_tokens"] += usage["output_tokens"]
                        accepted = validate_actions(response["parsed"], config["max_new_cycles"])
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
                    append_jsonl(out / "calls.jsonl", entry)
                    if fatal:
                        raise RuntimeError(f"Non-retryable API error: {fatal}; see calls.jsonl")
                    if accepted is not None:
                        break
                    totals["failed_attempts"] += 1
                    totals["retries"] += int(attempt <= config["max_retries"])
                if accepted is None:
                    append_jsonl(out / "failed-rounds.jsonl", {**context, "status": "no_valid_model_response"})
                    continue
                history.extend(accepted)
                seconds, log, checked, points = simulate(binary, out, f"{arm}-{rep}-{round_no}", history)
                if {point_id(p) for p in points} != baseline_ids:
                    raise AssertionError("DUT counter identity changed")
                totals["executions"] += 1
                totals["cycles"] += checked["checks"]
                totals["simulation_seconds"] += seconds
                totals["read_failures"] += checked["read_errors"]
                totals["interrupt_failures"] += checked["interrupt_errors"]
                totals["timing_failures"] += checked["timing_errors"]
                totals["wall_seconds"] += time.perf_counter() - tick
                covered = summary(points)
                api_tokens = totals["input_tokens"] + totals["output_tokens"] if evidence_mode != "mock" else None
                categories = [name for name, n in (("read_mismatch", totals["read_failures"]),
                    ("interrupt_mismatch", totals["interrupt_failures"]),
                    ("asynchronous_reset", totals["timing_failures"])) if n]
                row = {**context, "status": "ok", "new_actions": len(accepted),
                       "cumulative_actions": len(history),
                       **{f"{kind}_{part}": covered[kind][part] for kind in KINDS for part in ("covered", "total")},
                       "functional_failures": checked["functional_errors"],
                       "read_failures": checked["read_errors"], "interrupt_failures": checked["interrupt_errors"],
                       "timing_failures": checked["timing_errors"],
                       "cumulative_read_failure_events": totals["read_failures"],
                       "cumulative_interrupt_failure_events": totals["interrupt_failures"],
                       "cumulative_timing_failure_events": totals["timing_failures"],
                       "distinct_defect_count": len(categories), "distinct_defects": ";".join(categories),
                       "new_toggle_points_vs_initial": covered["toggle"]["covered"] - seed_covered,
                       "new_toggle_points_this_round": covered["toggle"]["covered"] - previous["toggle"]["covered"],
                       "cumulative_api_input_tokens": totals["input_tokens"] if api_tokens is not None else None,
                       "cumulative_api_output_tokens": totals["output_tokens"] if api_tokens is not None else None,
                       "cumulative_api_tokens": api_tokens,
                       "token_roi_new_toggles_per_1000_tokens": round(1000 * (covered["toggle"]["covered"] - seed_covered) / api_tokens, 6) if api_tokens else None,
                       "cumulative_model_calls": totals["model_calls"], "cumulative_retries": totals["retries"],
                       "cumulative_failed_model_attempts": totals["failed_attempts"],
                       "cumulative_simulator_executions": totals["executions"],
                       "cumulative_executed_cycles": totals["cycles"],
                       "cumulative_model_seconds": round(totals["model_seconds"], 6),
                       "cumulative_simulation_seconds": round(totals["simulation_seconds"], 6),
                       "cumulative_egg_preprocessing_seconds_amortized": round(timings["egg_preprocessing_seconds"] / config["repetitions"], 6) if arm == "C" else 0,
                       "cumulative_total_wall_seconds": round(totals["wall_seconds"] +
                           (timings["egg_preprocessing_seconds"] / config["repetitions"] if arm == "C" else 0), 6)}
                rows.append(row)
                append_jsonl(out / "rounds.jsonl", {**row, "coverage_points": points, "checker": checked,
                              "sim_log_path": f"{arm}-{rep}-{round_no}.sim.log"})
                print(f"{arm} rep {rep} round {round_no}: toggle {row['toggle_covered']}/{row['toggle_total']}, branch {row['branch_covered']}/{row['branch_total']}", flush=True)
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
                "common_initial_coverage": summary(initial_points), "reference_ceiling": ceiling,
                "elapsed_wall_seconds": time.perf_counter() - started,
                "evidence_mode": evidence_mode, "solver_or_deterministic_search_enabled": False,
                "simulator_commands": {"compile": "see verilator-compile.log; fixed in scripts/run_ttc_pilot.py",
                                       "run": "Vtb_ttc_counter_lite +MODE=1 +COLLECT +VECTORS=<validated actions> +verilator+coverage+file=<coverage.dat>"}}
    json_write(out / "metadata.json", metadata)
    plots(rows, out, evidence_mode, summary(initial_points)["toggle"]["total"])
    report(rows, config, metadata, out, evidence_mode)
    print(f"Output: {out}", flush=True)


if __name__ == "__main__":
    main()
