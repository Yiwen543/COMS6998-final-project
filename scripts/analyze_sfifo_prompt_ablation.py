#!/usr/bin/env python3
"""Descriptive, non-confirmatory analysis of the FIFO prompt-load ablation."""
from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict
from pathlib import Path

from run_midterm_fixed import ROOT


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--run", type=Path, required=True)
    args = cli.parse_args()
    run = (ROOT / args.run).resolve()
    metadata = json.loads((run / "metadata.json").read_text())
    rows = [json.loads(line) for line in (run / "rounds.jsonl").read_text().splitlines()]
    calls = [json.loads(line) for line in (run / "calls.jsonl").read_text().splitlines()]
    by_session = defaultdict(list)
    for row in rows:
        by_session[(row["arm"], row["repetition"])].append(row)
    limits = metadata["limits"]
    expected = {(arm, rep) for arm in limits["arms"]
                for rep in range(1, limits["repetitions"] + 1)}
    if set(by_session) != expected:
        raise AssertionError("Incomplete session set")
    first_target = []
    for key, session in sorted(by_session.items()):
        session.sort(key=lambda row: row["round"])
        if [row["round"] for row in session] != list(range(1, limits["rounds"] + 1)):
            raise AssertionError(f"Incomplete round set: {key}")
        first = next((row for row in session if row["target_reached"]), None)
        chosen = first or session[-1]
        first_target.append({"arm": key[0], "repetition": key[1],
            "first_target_round": first["round"] if first else "not reached",
            "target_reached": bool(first),
            "target_points_covered": sum(item["hits"] > 0 for item in chosen["target_hits"]),
            "branch_covered": chosen["coverage"]["branch"]["covered"],
            "branch_total": chosen["coverage"]["branch"]["total"],
            "line_covered": chosen["coverage"]["line"]["covered"],
            "line_total": chosen["coverage"]["line"]["total"],
            "api_tokens": chosen["api_tokens"],
            "executed_cycles": chosen["executed_cycles"],
            "simulator_executions": chosen["simulator_executions"],
            "model_calls": chosen["model_calls"],
            "failed_attempts": chosen["failed_attempts"],
            "total_wall_seconds": chosen["total_wall_seconds"],
            "distinct_defects": ",".join(chosen["checker"]["distinct_defects"])})
    round_fields = ["arm", "repetition", "round", "status", "target_reached",
                    "target_points_covered", "line_covered", "line_total",
                    "branch_covered", "branch_total", "expr_covered", "expr_total",
                    "toggle_covered", "toggle_total", "api_tokens", "executed_cycles",
                    "simulator_executions", "model_calls", "failed_attempts",
                    "token_count_requests", "compile_seconds", "simulation_seconds_cumulative",
                    "model_seconds_cumulative", "total_wall_seconds"]
    with (run / "rounds.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=round_fields)
        writer.writeheader()
        for row in rows:
            out = {key: row[key] for key in round_fields if key in row}
            out["target_points_covered"] = sum(x["hits"] > 0 for x in row["target_hits"])
            for kind in ("line", "branch", "expr", "toggle"):
                out[f"{kind}_covered"] = row["coverage"][kind]["covered"]
                out[f"{kind}_total"] = row["coverage"][kind]["total"]
            writer.writerow(out)
    with (run / "first-target.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(first_target[0]))
        writer.writeheader()
        writer.writerows(first_target)
    p_counts = [json.loads(line) for line in (run / "placebo-token-counts.jsonl").read_text().splitlines()]
    if metadata["mode"] == "live":
        if any(x["absolute_delta"] > limits["placebo_tolerance_tokens"] for x in p_counts):
            raise AssertionError("Placebo token match exceeded tolerance")
        for call in calls:
            if call["arm"] == "P_compact" and call.get("accepted"):
                if (abs(call["usage"]["input_tokens"] -
                        call["placebo_token_count"]["placebo_input_tokens"]) >
                        limits["placebo_tolerance_tokens"]):
                    raise AssertionError("Placebo generation usage mismatched count")
    by_arm = defaultdict(list)
    for row in first_target:
        by_arm[row["arm"]].append(row)
    summary = {"mode": metadata["mode"], "purpose": limits["purpose"],
               "sessions": first_target,
               "arms": {arm: {"target_rounds": [x["first_target_round"] for x in samples],
                              "not_reached": sum(not x["target_reached"] for x in samples),
                              "mean_api_tokens_at_target_or_final":
                                  sum(x["api_tokens"] for x in samples)/len(samples),
                              "mean_branch_covered_at_target_or_final":
                                  sum(x["branch_covered"] for x in samples)/len(samples)}
                        for arm, samples in by_arm.items()},
               "model_calls": len(calls),
               "failed_attempts": sum(not x.get("accepted", False) for x in calls),
               "input_tokens": sum((x.get("usage") or {}).get("input_tokens") or 0 for x in calls),
               "output_tokens": sum((x.get("usage") or {}).get("output_tokens") or 0 for x in calls),
               "cached_input_tokens_subset": sum((x.get("usage") or {}).get("cached_input_tokens") or 0 for x in calls),
               "reasoning_output_tokens_subset": sum((x.get("usage") or {}).get("reasoning_output_tokens") or 0 for x in calls),
               "placebo_count_requests": sum(x["count_requests"] for x in p_counts),
               "placebo_max_input_token_delta": max((x["absolute_delta"] for x in p_counts), default=None)}
    (run / "comparison.json").write_text(json.dumps(summary, indent=2) + "\n")
    if metadata["mode"] == "live":
        mpl_cache = ROOT / "build/mplcache"
        xdg_cache = ROOT / "build/xdgcache"
        mpl_cache.mkdir(parents=True, exist_ok=True)
        xdg_cache.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("MPLCONFIGDIR", str(mpl_cache))
        os.environ.setdefault("XDG_CACHE_HOME", str(xdg_cache))
        os.environ.setdefault("MPLBACKEND", "Agg")
        import matplotlib.pyplot as plt
        metrics = [("api_tokens", "API input + output tokens"),
                   ("executed_cycles", "Executed cycles including replays"),
                   ("simulator_executions", "Simulator executions"),
                   ("total_wall_seconds", "Wall seconds")]
        fig, axes = plt.subplots(2, 2, figsize=(11, 7))
        colors = {"B_full": "#777777", "B_compact": "#2077b4",
                  "P_compact": "#9b7d18", "C_compact": "#c9473b"}
        for ax, (key, label) in zip(axes.flat, metrics):
            for arm in limits["arms"]:
                sessions = [by_session[(arm, rep)] for rep in range(1, limits["repetitions"] + 1)]
                for session in sessions:
                    ax.plot([0] + [row[key] for row in session],
                            [0] + [sum(x["hits"] > 0 for x in row["target_hits"]) for row in session],
                            color=colors[arm], alpha=0.28, linewidth=1)
                ax.plot([sum(session[i][key] for session in sessions)/len(sessions)
                         for i in range(limits["rounds"])],
                        [sum(sum(x["hits"] > 0 for x in session[i]["target_hits"])
                             for session in sessions)/len(sessions)
                         for i in range(limits["rounds"])],
                        color=colors[arm], label=arm, linewidth=2)
            ax.set_xlabel(label)
            ax.set_ylabel("Mean covered target source counters (of 5)")
            ax.grid(alpha=0.2)
        axes[0, 0].legend(fontsize=8)
        fig.suptitle("Exploratory FIFO prompt ablation: raw source counters")
        fig.tight_layout()
        fig.savefig(run / "coverage-cost.png", dpi=160)
        plt.close(fig)
    print(json.dumps(summary["arms"], indent=2))


if __name__ == "__main__":
    main()
