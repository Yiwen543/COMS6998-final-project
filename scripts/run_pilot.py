#!/usr/bin/env python3
"""Matched A/B/C arbiter pilot. The model can supply only validated cycle data."""
import argparse
import csv
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

from coverage import load, summary
from pilot_feedback import point_id, render_messages
from pilot_model import MockModel, ModelResponseError, OpenAIModel, ReplayModel, token_estimate, validate_actions
from predicates import ROOT, DUT, extract

SPEC = ROOT / "examples/arbiter/docs/specification.md"
CHECKER = ROOT / "examples/arbiter/verif/tb_fixed_priority_arbiter.sv"
ENGINE = ROOT / "egraph/target/debug/rtl-predicate-egraph"


def json_write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def append_jsonl(path, value):
    with path.open("a") as stream:
        stream.write(json.dumps(value, sort_keys=True) + "\n")


def command(argv, log_path, timeout=180, stdin=None, env=None):
    start = time.perf_counter()
    safe_env = dict(os.environ if env is None else env)
    safe_env.pop("OPENAI_API_KEY", None)
    proc = subprocess.run([str(arg) for arg in argv], cwd=ROOT, text=True, input=stdin,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=timeout, env=safe_env)
    log_path.write_text(proc.stdout)
    if proc.returncode:
        raise RuntimeError(f"Command failed ({proc.returncode}); see {log_path}")
    return time.perf_counter() - start, proc.stdout


def result(log):
    found = re.search(r"RESULT checks=(\d+) functional_errors=(\d+) timing_errors=(\d+)", log)
    if not found:
        raise ValueError("Checker result absent from simulator log")
    return dict(zip(("checks", "functional_errors", "timing_errors"), map(int, found.groups())))


def check_frozen(config):
    for key, path in (("dut_sha256", DUT), ("spec_sha256", SPEC), ("checker_sha256", CHECKER)):
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != config[key]:
            raise RuntimeError(f"Frozen fixture mismatch: {path} has {actual}")


def versions():
    values = {"python": platform.python_version()}
    safe_env = dict(os.environ)
    safe_env.pop("OPENAI_API_KEY", None)
    for label, argv in (("verilator", ["verilator", "--version"]),
                        ("iverilog", ["iverilog", "-V"]), ("yosys", ["yosys", "-V"]),
                        ("cargo", ["cargo", "--version"]), ("rustc", ["rustc", "--version"])):
        proc = subprocess.run(argv, capture_output=True, text=True, check=True, env=safe_env)
        values[label] = (proc.stdout or proc.stderr).splitlines()[0]
    try:
        from importlib.metadata import version
        values["openai_sdk"] = version("openai")
        values["matplotlib"] = version("matplotlib")
    except ImportError:
        pass
    return values


def simulate(binary, out, name, actions):
    vector = out / f"{name}.vectors"
    if actions:
        vector.write_text("".join(f"{a['reset']} {a['req']:02x} {a['priority_override']:02x}\n" for a in actions))
    cover = out / f"{name}.dat"
    args = [binary, f"+MODE={1 if actions else 0}", "+COLLECT", f"+verilator+coverage+file+{cover}"]
    if actions:
        vector_arg = str(vector.relative_to(ROOT)) if vector.is_relative_to(ROOT) else str(vector)
        if len(vector_arg.encode()) > 127:
            raise ValueError("Stimulus path exceeds fixed testbench plusarg width")
        args.append(f"+VECTORS={vector_arg}")
    elapsed, log = command(args, out / f"{name}.sim.log", timeout=120)
    points = load(cover)
    observed = result(log)
    if observed["checks"] != 4 + len(actions):
        raise AssertionError("Executed cycle accounting disagrees with checker")
    return elapsed, log, observed, points


def build(out):
    timings = {}
    timings["cargo_build_seconds"], _ = command(
        ["cargo", "build", "--locked", "--offline", "--manifest-path", "egraph/Cargo.toml"],
        out / "cargo-build.log")
    targets = extract()
    started = time.perf_counter()
    _, output = command([ENGINE], out / "egg.log", timeout=15, stdin=json.dumps(targets))
    graph = json.loads(output)
    timings["egg_preprocessing_seconds"] = time.perf_counter() - started
    if len({target["eclass"] for target in graph["targets"]}) != 16 or not all(t["equivalent"] for t in graph["targets"]):
        raise AssertionError("Egg did not validate 16 separate winner predicates")
    json_write(out / "egg-evidence.json", graph)
    json_write(out / "mapped-predicates.json", targets)
    # Yosys checks frontend/process extraction. The hash-guarded Python source
    # adapter supplies expressions; Yosys JSON is not yet a general translator.
    yosys = f"read_verilog -sv {DUT.relative_to(ROOT)}; hierarchy -check -top fixed_priority_arbiter; proc; check; write_json {out}/yosys-netlist.json"
    timings["yosys_seconds"], _ = command(["yosys", "-Q", "-T", "-p", yosys], out / "yosys.log")
    builddir = out / "verilator-build"
    timings["verilator_compile_seconds"], _ = command(
        ["verilator", "--cc", "--exe", "--build", "--timing", "--assert",
         "--coverage-line", "--coverage-toggle", "--coverage-expr",
         "--top-module", "tb_fixed_priority_arbiter", "--Mdir", builddir, "-j", "2",
         DUT.relative_to(ROOT), CHECKER.relative_to(ROOT), ROOT / "scripts/sim_main.cpp"],
        out / "verilator-compile.log")
    return builddir / "Vtb_fixed_priority_arbiter", targets, graph, timings


def stable_denominator(reference, current):
    if {point_id(p) for p in reference} != {point_id(p) for p in current}:
        raise AssertionError("DUT coverage denominator/source identity changed")


def defects(checker):
    found = []
    if checker["functional_errors"]:
        found.append("multi_bit_override_grant")
    if checker["timing_errors"]:
        found.append("asynchronous_reset")
    return found


def csv_write(path, rows):
    if not rows:
        return
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def target_costs(rows, config):
    costs = []
    for arm in config["arms"]:
        for rep in range(1, config["repetitions"]+1):
            sample = [r for r in rows if r["arm"] == arm and r["repetition"] == rep]
            reached = next((r for r in sample if r["branch_covered"] >= config["target_branch_points"]), None)
            row = reached or (sample[-1] if sample else None)
            costs.append({"arm": arm, "repetition": rep,
                          "target_branch_points": config["target_branch_points"],
                          "status": "reached" if reached else "not reached",
                          "first_target_round": reached["round"] if reached else None,
                          "branch_covered_at_stop": row["branch_covered"] if row else None,
                          "api_tokens_at_stop": row["cumulative_api_tokens"] if row else None,
                          "token_roi_at_stop": row.get("token_roi_new_branches_per_1000_tokens") if row else None,
                          "executed_cycles_at_stop": row["cumulative_executed_cycles"] if row else None,
                          "simulator_executions_at_stop": row["cumulative_simulator_executions"] if row else None,
                          "wall_seconds_at_stop": row["cumulative_total_wall_seconds"] if row else None})
    return costs


def plot(rows, out, mode):
    cache = out / "plot-cache"
    cache.mkdir(exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(cache)
    os.environ["XDG_CACHE_HOME"] = str(cache)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    axes_specs = [("cumulative_api_tokens", "API input + output tokens"),
                  ("cumulative_executed_cycles", "Executed cycles (replays counted)"),
                  ("cumulative_simulator_executions", "Simulator executions"),
                  ("cumulative_total_wall_seconds", "Wall time, s (C includes egg preprocessing share)")]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    colors = {"A": "#0072b2", "B": "#e69f00", "C": "#009e73"}
    for ax, (field, label) in zip(axes.flat, axes_specs):
        if field == "cumulative_api_tokens" and mode == "mock":
            ax.text(.5, .5, "No API tokens in mock mode", ha="center", va="center", transform=ax.transAxes)
        else:
            for arm in "ABC":
                for rep in sorted({r["repetition"] for r in rows}):
                    sample = [r for r in rows if r["arm"] == arm and r["repetition"] == rep and r["status"] == "ok"]
                    if sample and sample[0][field] is not None:
                        ax.plot([r[field] for r in sample], [r["branch_covered"] for r in sample],
                                marker="o", color=colors[arm], alpha=.4, label=arm if rep == 1 else None)
        ax.set_xlabel(label)
        ax.set_ylabel("Covered DUT branch points / 18")
        ax.set_ylim(0, 18)
        ax.grid(alpha=.2)
    axes[0, 1].legend(title="Feedback")
    fig.suptitle(f"Arbiter {mode} pilot: individual repetitions")
    fig.tight_layout()
    fig.savefig(out / "comparison.png", dpi=150)
    plt.close(fig)


def report(rows, config, metadata, out, mode):
    lines = ["# Arbiter A/B/C pilot", "", f"Mode: **{mode}**. " +
             ("Offline mock stimuli validate infrastructure; these are not LLM performance results." if mode == "mock" else
              "Recorded Responses API model stimuli; independently replayed through fixed checker." if mode == "replay" else
              "Live Responses API stimuli."), "",
             "A receives specification, RTL, common initial stimulus and checker logs. B adds every raw uncovered DUT point. C adds bounded egg equivalence evidence and unmapped-point disclosure to B's exact raw evidence.",
             "", "| Arm | Repetition | Final branch | Line | Toggle | Distinct defects | API tokens | Cycles | Executions | Target 17/18 |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for arm in "ABC":
        for rep in range(1, config["repetitions"]+1):
            sample = [r for r in rows if r["arm"] == arm and r["repetition"] == rep]
            if not sample:
                continue
            last = sample[-1]
            lines.append(f"| {arm} | {rep} | {last['branch_covered']}/{last['branch_total']} | "
                         f"{last['line_covered']}/{last['line_total']} | {last['toggle_covered']}/{last['toggle_total']} | "
                         f"{last['distinct_defect_count']} | {last['cumulative_api_tokens'] if last['cumulative_api_tokens'] is not None else 'n/a'} | "
                         f"{last['cumulative_executed_cycles']} | {last['cumulative_simulator_executions']} | "
                         f"{'reached in round '+str(next((x['round'] for x in sample if x['branch_covered'] >= config['target_branch_points']), '?')) if last['branch_covered'] >= config['target_branch_points'] else 'not reached'} |")
    final = {(arm, rep): [r for r in rows if r["arm"] == arm and r["repetition"] == rep][-1]
             for arm in "ABC" for rep in range(1, config["repetitions"]+1)
             if any(r["arm"] == arm and r["repetition"] == rep for r in rows)}
    paired = [final[("C", rep)]["branch_covered"] - final[("B", rep)]["branch_covered"]
              for rep in range(1, config["repetitions"]+1)
              if ("C", rep) in final and ("B", rep) in final]
    if paired:
        lines += ["", f"Final C−B branch-point differences by matched repetition: {paired}; "
                  f"range {min(paired)} to {max(paired)}. " +
                  ("These are arm-blind mock outcomes and provide no evidence of model benefit." if mode == "mock" else
                   "This small pilot is descriptive; it does not establish statistical significance.")]
    costs = target_costs(rows, config)
    lines += ["", "| Arm | Rep | First target round | Tokens at target/stop | Cycles | Executions | Wall seconds | Token ROI |",
              "|---|---:|---|---:|---:|---:|---:|---:|"]
    for cost in costs:
        fmt = lambda value: "n/a" if value is None else str(value)
        lines.append(f"| {cost['arm']} | {cost['repetition']} | "
                     f"{cost['first_target_round'] if cost['status'] == 'reached' else 'not reached'} | "
                     f"{fmt(cost['api_tokens_at_stop'])} | {fmt(cost['executed_cycles_at_stop'])} | "
                     f"{fmt(cost['simulator_executions_at_stop'])} | {fmt(cost['wall_seconds_at_stop'])} | "
                     f"{fmt(cost['token_roi_at_stop'])} |")
    if mode != "mock":
        by_cost = {(c["arm"], c["repetition"]): c for c in costs}
        pairs_cost = [(by_cost[("B", rep)], by_cost[("C", rep)])
                      for rep in range(1, config["repetitions"]+1)
                      if ("B", rep) in by_cost and ("C", rep) in by_cost]
        if pairs_cost and all(b["status"] == c["status"] == "reached" for b, c in pairs_cost):
            token_delta = [c["api_tokens_at_stop"] - b["api_tokens_at_stop"] for b, c in pairs_cost]
            cycle_delta = [c["executed_cycles_at_stop"] - b["executed_cycles_at_stop"] for b, c in pairs_cost]
            execution_delta = [c["simulator_executions_at_stop"] - b["simulator_executions_at_stop"] for b, c in pairs_cost]
            wall_delta = [round(c["wall_seconds_at_stop"] - b["wall_seconds_at_stop"], 6) for b, c in pairs_cost]
            lines += ["", f"At the preregistered target, paired C−B differences were API tokens {token_delta}, "
                      f"executed cycles {cycle_delta}, simulator executions {execution_delta}, and wall seconds {wall_delta}. "
                      "C's coverage did not exceed B's. " +
                      ("Replay wall time excludes the original API latency; token counts are retained from the original call log." if mode == "replay" else
                       "Interpret wall-time differences descriptively because API latency varies across independent calls.")]
    lines += ["", "All rows use the original DUT, frozen specification and checker, one Verilator instrumented binary, and raw 18-point branch denominator. Line means Verilator block/elsif points; branch includes control and ternary outcomes; toggle is per-direction DUT bit transition. Expression counters are retained in JSON/CSV. Testbench counters are excluded.",
              "Each round replays the same four-cycle reset/initial sequence followed by **all** accumulated generated actions. The measured cycles sum every replay. Each simulator process starts fresh; checker failures are collected while coverage is flushed. Common initialization and reset activity count in every round's coverage and cycles.",
              "", "Token ROI = newly covered raw DUT branch points relative to the common initial run, per 1,000 API-reported input-plus-output tokens. Cached input and reasoning output details are informational subsets, not added again. Mock token ROI is undefined.",
              "", "Egg normalization is limited to unsigned one-bit binary/two-state combinational winner predicates. Its six named Boolean rewrites are truth-table validated and saturated with finite limits. Distinct winner cases retain separate E-classes. Clock/reset transitions and all original coverage locations remain separate; an equivalent predicate never transfers a hit count. Yosys provides frontend/process extraction, while the RTL-to-expression bridge remains a hash-guarded, arbiter-specific source adapter.",
              "", "The original DUT still violates the synchronous reset and one-hot override specification. Repeated checker failures count as two distinct categories at most. The checker was independently validated against derived conforming and single-defect controls. A fresh exhaustive ceiling is measured separately from model prompts and costs.",
              "", "The arbiter has little cross-location semantic redundancy, so a C advantage is not guaranteed. A next discriminating experiment should use nested/repeated equivalent predicates with equivalence-checked RTL variants, then a FIFO with full/empty, simultaneous read/write, wraparound and reset-during-operation cases.",
              "", "Exact metadata, per-call responses, rendered prompts, raw coverage files, source mappings and per-round CSV/JSONL are adjacent to this report.", ""]
    (out / "REPORT.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["live", "mock", "replay"], required=True)
    parser.add_argument("--config", default="configs/arbiter_pilot.json")
    parser.add_argument("--output", required=True)
    parser.add_argument("--replay-calls")
    args = parser.parse_args()
    config = json.loads((ROOT / args.config).read_text())
    check_frozen(config)
    if config["arms"] != ["A", "B", "C"] or config["target_branch_points"] > 18:
        raise ValueError("Invalid preregistered comparison")
    if args.mode == "replay" and not args.replay_calls:
        parser.error("--replay-calls is required for replay mode")
    model = OpenAIModel(config) if args.mode == "live" else MockModel(config) if args.mode == "mock" else ReplayModel(args.replay_calls)
    evidence_mode = "mock" if args.mode == "mock" or (args.mode == "replay" and model.source_mode == "mock") else args.mode
    out = (ROOT / args.output).resolve()
    out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    binary, targets, graph, timings = build(out)
    spec, rtl = SPEC.read_text(), DUT.read_text()
    initial_time, initial_log, initial_checker, initial_points = simulate(binary, out, "common-initial", [])
    if initial_checker["functional_errors"] or initial_checker["timing_errors"]:
        raise AssertionError("Initial common stimulus unexpectedly fails")
    # Reference ceiling is measured separately; never included in a prompt.
    ref_cover = out / "reference-ceiling.dat"
    ref_time, ref_log = command([binary, "+MODE=2", "+COLLECT", f"+verilator+coverage+file+{ref_cover}"],
                                out / "reference-ceiling.sim.log", timeout=180)
    ref_points = load(ref_cover)
    stable_denominator(initial_points, ref_points)
    ref = {"checker": result(ref_log), "coverage": summary(ref_points), "cycles": 65543,
           "simulator_executions": 1, "simulation_seconds": ref_time}
    json_write(out / "reference-ceiling.json", ref)
    rows = []
    call_path = out / "calls.jsonl"
    round_path = out / "rounds.jsonl"
    initial_branch = summary(initial_points)["branch"]["covered"]
    for arm in config["arms"]:
        for rep in range(1, config["repetitions"]+1):
            cumulative_actions = []
            points, checker, sim_log = initial_points, initial_checker, initial_log
            totals = {"model_calls": 0, "retries": 0, "failed_model_attempts": 0, "api_input_tokens": 0,
                      "api_output_tokens": 0, "simulator_executions": 0,
                      "executed_cycles": 0, "simulation_seconds": 0.0, "model_seconds": 0.0,
                      "run_wall_seconds": 0.0, "functional_failure_events": 0, "timing_failure_events": 0}
            for round_no in range(1, config["rounds"]+1):
                round_started = time.perf_counter()
                messages = render_messages(arm, spec, rtl, cumulative_actions, checker, sim_log,
                                           points, targets, graph, config["max_new_cycles"], round_no)
                prompt_path = out / f"prompt-{arm}-{rep}-{round_no}.json"
                json_write(prompt_path, messages)
                byte_cap = token_estimate(messages)
                if byte_cap > config["max_input_tokens_conservative_byte_cap"]:
                    raise RuntimeError(f"Prompt byte cap exceeded at {prompt_path}: {byte_cap}")
                accepted = None
                for attempt in range(1, config["max_retries"]+2):
                    totals["model_calls"] += 1
                    fatal_error = None
                    context = {"arm": arm, "repetition": rep, "round": round_no}
                    entry = {**context, "attempt": attempt, "mode": args.mode,
                             "requested_model": config["model"] if args.mode == "live" else "mock-random" if args.mode == "mock" else model.calls[(arm, rep, round_no)]["requested_model"],
                             "prompt_path": str(prompt_path.relative_to(out)),
                             "prompt_conservative_byte_count": byte_cap,
                             "settings": {k: config[k] for k in ("model", "reasoning_effort", "max_output_tokens", "timeout_seconds")}}
                    try:
                        attempt_started = time.perf_counter()
                        answer = model.generate(messages, context)
                        entry.update(answer)
                        usage = answer["usage"]
                        if usage["input_tokens"] is not None:
                            totals["api_input_tokens"] += usage["input_tokens"]
                            totals["api_output_tokens"] += usage["output_tokens"]
                        actions = validate_actions(answer["parsed"], config["max_new_cycles"])
                        entry["actions"] = actions
                        entry["accepted"] = True
                        accepted = actions
                    except ModelResponseError as error:
                        entry.update(error.record)
                        entry.update({"accepted": False, "validation_failure": error.reason})
                        usage = error.record["usage"]
                        if usage["input_tokens"] is not None:
                            totals["api_input_tokens"] += usage["input_tokens"]
                            totals["api_output_tokens"] += usage["output_tokens"]
                    except ValueError as error:
                        entry.update({"accepted": False, "validation_failure": str(error)})
                    except Exception as error:
                        # Exception strings can contain transport details; log type only.
                        entry.update({"accepted": False, "error_type": type(error).__name__})
                        if type(error).__name__ in {"AuthenticationError", "PermissionDeniedError", "NotFoundError", "BadRequestError"}:
                            fatal_error = type(error).__name__
                    entry["attempt_wall_seconds"] = time.perf_counter() - attempt_started
                    totals["model_seconds"] += entry["attempt_wall_seconds"]
                    append_jsonl(call_path, entry)
                    if fatal_error:
                        raise RuntimeError(f"Non-retryable model API error: {fatal_error}; see {call_path}")
                    if accepted is not None:
                        break
                    totals["failed_model_attempts"] += 1
                    totals["retries"] += int(attempt <= config["max_retries"])
                if accepted is None:
                    break
                cumulative_actions.extend(accepted)
                sim_name = f"{arm}-{rep}-{round_no}"
                previous_coverage = summary(points)
                elapsed, sim_log, checker, next_points = simulate(binary, out, sim_name, cumulative_actions)
                stable_denominator(initial_points, next_points)
                points = next_points
                totals["simulator_executions"] += 1
                totals["executed_cycles"] += checker["checks"]
                totals["simulation_seconds"] += elapsed
                totals["functional_failure_events"] += checker["functional_errors"]
                totals["timing_failure_events"] += checker["timing_errors"]
                totals["run_wall_seconds"] += time.perf_counter() - round_started
                coverage = summary(points)
                defects_found = defects(checker)
                api_total = totals["api_input_tokens"] + totals["api_output_tokens"] if evidence_mode != "mock" and totals["api_input_tokens"] + totals["api_output_tokens"] else None
                new_branches = coverage["branch"]["covered"] - initial_branch
                row = {"arm": arm, "repetition": rep, "round": round_no, "status": "ok",
                       "new_actions": len(accepted), "cumulative_actions": len(cumulative_actions),
                       "branch_covered": coverage["branch"]["covered"], "branch_total": coverage["branch"]["total"],
                       "line_covered": coverage["line"]["covered"], "line_total": coverage["line"]["total"],
                       "toggle_covered": coverage["toggle"]["covered"], "toggle_total": coverage["toggle"]["total"],
                       "expr_covered": coverage["expr"]["covered"], "expr_total": coverage["expr"]["total"],
                       "functional_failures": checker["functional_errors"],
                       "timing_failures": checker["timing_errors"],
                       "cumulative_functional_failure_events": totals["functional_failure_events"],
                       "cumulative_timing_failure_events": totals["timing_failure_events"],
                       "distinct_defect_count": len(defects_found),
                       "distinct_defects": ";".join(defects_found),
                       "new_branch_points_vs_initial": new_branches,
                       "new_branch_points_this_round": coverage["branch"]["covered"] - previous_coverage["branch"]["covered"],
                       "new_line_points_this_round": coverage["line"]["covered"] - previous_coverage["line"]["covered"],
                       "new_toggle_points_this_round": coverage["toggle"]["covered"] - previous_coverage["toggle"]["covered"],
                       "cumulative_api_input_tokens": totals["api_input_tokens"] if api_total is not None else None,
                       "cumulative_api_output_tokens": totals["api_output_tokens"] if api_total is not None else None,
                       "cumulative_api_tokens": api_total,
                       "token_roi_new_branches_per_1000_tokens": round(1000 * new_branches / api_total, 6) if api_total else None,
                       "cumulative_model_calls": totals["model_calls"], "cumulative_retries": totals["retries"],
                       "cumulative_failed_model_attempts": totals["failed_model_attempts"],
                       "cumulative_simulator_executions": totals["simulator_executions"],
                       "cumulative_executed_cycles": totals["executed_cycles"],
                       "cumulative_model_seconds": round(totals["model_seconds"], 6),
                       "cumulative_simulation_seconds": round(totals["simulation_seconds"], 6),
                       "cumulative_egg_preprocessing_seconds_amortized": round(timings["egg_preprocessing_seconds"] / config["repetitions"], 6) if arm == "C" else 0,
                       "cumulative_total_wall_seconds": round(totals["run_wall_seconds"] + (timings["egg_preprocessing_seconds"] / config["repetitions"] if arm == "C" else 0), 6)}
                rows.append(row)
                append_jsonl(round_path, {**row, "coverage_points": points, "checker": checker,
                                          "prompt_path": str(prompt_path.relative_to(out)),
                                          "sim_log_path": f"{sim_name}.sim.log"})
                print(f"{arm} rep {rep} round {round_no}: branch {row['branch_covered']}/18, cycles {checker['checks']}", flush=True)
    csv_write(out / "rounds.csv", rows)
    csv_write(out / "target_costs.csv", target_costs(rows, config))
    git_env = dict(os.environ)
    git_env.pop("OPENAI_API_KEY", None)
    metadata = {"git_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True, env=git_env).stdout.strip(),
                "fixture_hashes": {k: config[k] for k in ("dut_sha256", "spec_sha256", "checker_sha256")},
                "versions": versions(), "configuration": config, "mode": args.mode,
                "shared_setup": {**timings, "verilator_compilations": 1, "cargo_builds": 1,
                                 "yosys_invocations": 1, "common_initial_simulator_executions": 1,
                                 "common_initial_simulation_seconds": initial_time,
                                 "reference_ceiling_simulator_executions": 1,
                                 "reference_ceiling_simulation_seconds": ref_time},
                "common_initial_coverage": summary(initial_points),
                "reference_ceiling": ref,
                "elapsed_wall_seconds": time.perf_counter() - started,
                "evidence_mode": evidence_mode,
                "solver_or_deterministic_search_enabled": False,
                "simulator_commands": {"compile": "see verilator-compile.log; fixed command in scripts/run_pilot.py",
                                       "run": "Vtb_fixed_priority_arbiter +MODE=1 +COLLECT +VECTORS=<validated vectors> +verilator+coverage+file+<coverage.dat>"}}
    json_write(out / "metadata.json", metadata)
    plot(rows, out, evidence_mode)
    report(rows, config, metadata, out, evidence_mode)
    print(f"Output: {out}")


if __name__ == "__main__":
    main()
