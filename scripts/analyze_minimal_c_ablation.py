#!/usr/bin/env python3
"""Retain every planned session, including interruptions and exhausted retries."""
from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
from pathlib import Path

from run_minimal_c_ablation import usage_totals, write


def ledger(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def summarize(run):
    meta = json.loads((run / "metadata.json").read_text())
    cfg = meta["limits"]
    rounds, calls, counts = (ledger(run / f"{name}.jsonl") for name in ("rounds", "calls", "count-requests"))
    matches = ledger(run / "placebo-matches.jsonl")
    if meta["mode"] == "live" and any(x["absolute_delta"] > cfg["placebo_tolerance_tokens"] for x in matches):
        raise AssertionError("Unmatched placebo")
    sessions = []
    for arm in cfg["arms"]:
        for rep in range(1, cfg["repetitions"]+1):
            rows = sorted((x for x in rounds if x["arm"] == arm and x["repetition"] == rep), key=lambda x: x["round"])
            first = next((x for x in rows if x["target_reached"]), None)
            seed = run / arm / f"rep{rep}" / "seed-summary.json"
            last = rows[-1] if rows else json.loads(seed.read_text()) if seed.exists() else None
            chosen = first or last
            related = [x for x in calls if x["arm"] == arm and x["repetition"] == rep]
            complete = [x["round"] for x in rows] == list(range(1, cfg["rounds"]+1)) and all(x["status"] == "ok" for x in rows)
            totals = usage_totals(related)
            row = {"arm": arm, "repetition": rep, "session_complete": complete,
                   "last_status": last["status"] if last else "not_started",
                   "rounds_recorded": len(rows), "target_reached": first is not None,
                   "first_target_round": first["round"] if first else "not reached",
                   "tokens_at_target_or_last": chosen["api_tokens"] if chosen else None,
                   "cycles_at_target_or_last": chosen["executed_cycles"] if chosen else None,
                   "executions_at_target_or_last": chosen["simulator_executions"] if chosen else None,
                   "wall_at_target_or_last": chosen["total_wall_seconds"] if chosen else None,
                   "target_points_at_target_or_last": sum(x["hits"] > 0 for x in chosen["target_hits"]) if chosen else None,
                   "branch_covered_at_target_or_last": chosen["coverage"]["branch"]["covered"] if chosen else None,
                   "all_generation_calls": len(related),
                   "all_failed_attempts": sum(not x.get("accepted", False) for x in related),
                   "all_known_api_tokens": totals["api_tokens"],
                   "calls_with_unknown_usage": totals["calls_with_unknown_usage"],
                   "count_requests": sum(x["arm"] == arm and x["repetition"] == rep for x in counts)}
            if not first:  # Count all failed-request costs, including after the last measured row.
                row["tokens_at_target_or_last"] = totals["api_tokens"]
            row["known_branch_token_roi_at_target_or_last"] = ((row["branch_covered_at_target_or_last"] -
                json.loads(seed.read_text())["coverage"]["branch"]["covered"]) * 1000 / row["tokens_at_target_or_last"]
                if chosen and seed.exists() and row["tokens_at_target_or_last"] and totals["calls_with_unknown_usage"] == 0 else None)
            sessions.append(row)
    arm_summary = {}
    for arm in cfg["arms"]:
        sample = [x for x in sessions if x["arm"] == arm]
        values = [x["tokens_at_target_or_last"] for x in sample if x["tokens_at_target_or_last"] is not None]
        arm_summary[arm] = {"target_rounds": [x["first_target_round"] for x in sample],
            "not_reached": sum(not x["target_reached"] for x in sample),
            "incomplete_sessions": sum(not x["session_complete"] for x in sample),
            "mean_known_tokens_at_target_or_last": statistics.mean(values) if values else None,
            "stdev_known_tokens_at_target_or_last": statistics.stdev(values) if len(values)>1 else None}
    return {"mode": meta["mode"], "limits": cfg, "sessions": sessions, "arms": arm_summary,
            "generation_calls": len(calls), "failed_attempts": sum(not x.get("accepted", False) for x in calls),
            **usage_totals(calls), "count_requests": len(counts),
            "failed_count_requests": sum(not x["ok"] for x in counts),
            "max_placebo_delta": max((x["absolute_delta"] for x in matches), default=None)}, rounds


def main(run, plot=True):
    result, rows = summarize(run)
    write(run / "comparison.json", result)
    with (run / "sessions.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(result["sessions"][0]))
        w.writeheader()
        w.writerows(result["sessions"])
    flat = []
    for row in rows:
        item = {k: v for k, v in row.items() if k not in ("coverage", "checker", "target_hits")}
        item["target_points"] = sum(x["hits"] > 0 for x in row["target_hits"])
        item["defect_categories"] = ",".join(row["checker"]["distinct_defects"])
        item["checker_failures"] = len(row["checker"]["failures"])
        for kind, stats in row["coverage"].items():
            item[f"{kind}_covered"] = stats["covered"]
            item[f"{kind}_total"] = stats["total"]
        flat.append(item)
    if flat:
        with (run / "rounds.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(flat[0]))
            w.writeheader()
            w.writerows(flat)
    if plot and result["mode"] == "live" and rows:
        os.environ.setdefault("MPLCONFIGDIR", str(run / "plot-cache"))
        os.environ.setdefault("MPLBACKEND", "Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 2, figsize=(11, 7))
        colors = dict(zip(result["limits"]["arms"], ("#2675a8", "#b44646", "#38844c", "#b08a22")))
        for ax, (key, label) in zip(axes.flat, (("api_tokens", "Reported generation tokens"),
                ("executed_cycles", "Executed cycles with replay"), ("simulator_executions", "Simulations"),
                ("total_wall_seconds", "Active session seconds (shared compile excluded)"))):
            for arm in result["limits"]["arms"]:
                for rep in range(1, result["limits"]["repetitions"]+1):
                    sample = [x for x in rows if x["arm"] == arm and x["repetition"] == rep]
                    if sample:
                        ax.plot([x[key] for x in sample], [sum(h["hits"]>0 for h in x["target_hits"]) for x in sample],
                                color=colors[arm], alpha=.65, marker=".", label=arm if rep==1 else None)
            ax.set_xlabel(label)
            ax.set_ylabel("Covered original target counters / 5")
            ax.grid(alpha=.2)
        axes[0, 0].legend()
        fig.suptitle("Exploratory minimal C — individual repetitions")
        fig.tight_layout()
        fig.savefig(run / "coverage-cost.png", dpi=160)
        plt.close(fig)
    print(json.dumps(result["arms"], indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    args = parser.parse_args()
    main(args.run.resolve())
