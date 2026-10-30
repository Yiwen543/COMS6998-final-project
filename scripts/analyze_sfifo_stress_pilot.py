#!/usr/bin/env python3
"""Audit each FIFO stress repetition, late source counter and target miss."""
from __future__ import annotations

import argparse
import csv
import json
import os

from coverage import load
from run_sfifo_stress_fixed import ROOT, SOURCE

SCREEN = ROOT / "results/midterm_candidate_preflight/sfifo-stress/screen.json"


def write_csv(path, rows):
    if not rows:
        raise ValueError("No rows")
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    run = (ROOT / args.run).resolve()
    config = json.loads((run / "config.json").read_text())
    saved = json.loads((run / "summary.json").read_text())
    screen = json.loads(SCREEN.read_text())
    calls = [json.loads(line) for line in (run / "calls.jsonl").read_text().splitlines()]
    accepted = {(r["arm"], r["repetition"], r["round"]): r for r in calls if r.get("accepted")}
    rel = str(SOURCE.relative_to(ROOT))
    target_lines = set(config.get("primary_target", {}).get("source_lines", [91, 161, 96, 179]))
    rows, group_progress = [], []
    seed_branch = screen["seed"]["branch"]["covered"]
    for item in saved["rows"]:
        arm, rep, round_no = item["arm"], item["repetition"], item["round"]
        folder = run / arm / f"rep{rep}"
        if item["status"] == "ok":
            call = accepted[(arm, rep, round_no)]
            raw = folder / f"round{round_no}-attempt{call['attempt']}.dat"
        else:
            previous = next((accepted[(arm, rep, older)] for older in range(round_no - 1, 0, -1)
                             if (arm, rep, older) in accepted), None)
            raw = (folder / f"round{previous['round']}-attempt{previous['attempt']}.dat"
                   if previous else folder / "seed.dat")
        points = load(raw, rel, include_descendants=True)
        groups = []
        for group in screen["groups"]:
            if not group["qualifies_preflight"]:
                continue
            members = []
            for member in group["members"]:
                mapped = member["seed_coverage"]
                matches = [p for p in points if
                           (p["source"], p["line"], p["column"], p["type"], p["outcome"]) ==
                           (rel, member["line"], mapped["column"], mapped["type"], mapped["outcome"])]
                if len(matches) != 1:
                    raise AssertionError("Original DUT counter identity changed")
                point = matches[0]
                members.append({"source": rel, "line": point["line"],
                                "column": point["column"], "type": point["type"],
                                "outcome": point["outcome"], "hits": point["hits"]})
            groups.append({"eclass": group["eclass_local"], "late_guard": group["late_guard"],
                           "members": members,
                           "fully_covered": all(member["hits"] > 0 for member in members)})
        late_members = [member for group in groups if group["late_guard"]
                        for member in group["members"]]
        if {member["line"] for member in late_members} != target_lines:
            raise AssertionError("Late guard target locations changed")
        late_covered = sum(member["hits"] > 0 for member in late_members)
        group_progress.append({"arm": arm, "repetition": rep, "round": round_no,
                               "fully_covered_groups": sum(group["fully_covered"] for group in groups),
                               "late_source_counters_covered": late_covered,
                               "groups": groups})
        coverage = item["coverage"]
        rows.append({"mode": saved["mode"], "arm": arm, "repetition": rep,
                     "round": round_no, "status": item["status"],
                     "line_covered": coverage["line"]["covered"],
                     "line_total": coverage["line"]["total"],
                     "branch_covered": coverage["branch"]["covered"],
                     "branch_total": coverage["branch"]["total"],
                     "expr_covered": coverage["expr"]["covered"],
                     "expr_total": coverage["expr"]["total"],
                     "toggle_covered": coverage["toggle"]["covered"],
                     "toggle_total": coverage["toggle"]["total"],
                     "fully_covered_groups": group_progress[-1]["fully_covered_groups"],
                     "late_source_counters_covered": late_covered,
                     "target_reached": late_covered == len(target_lines),
                     "cumulative_api_tokens": item["api_tokens"],
                     "cumulative_model_calls": item["model_calls"],
                     "cumulative_failed_attempts": item["failed_attempts"],
                     "cumulative_token_count_requests": item.get("token_count_requests", 0),
                     "cumulative_simulator_executions": item["simulator_executions"],
                     "cumulative_executed_cycles": item["executed_cycles"],
                     "distinct_defects": ";".join(item["checker"]["distinct_defects"]),
                     "compile_seconds": item["compile_seconds"],
                     "simulation_seconds_cumulative": item["simulation_seconds_cumulative"],
                     "egraph_preprocessing_seconds": item["egraph_preprocessing_seconds"],
                     "token_count_seconds_cumulative": item.get("token_count_seconds_cumulative", 0.0),
                     "total_wall_seconds": item["total_wall_seconds"],
                     "token_roi_branch_per_1000": round(
                         (coverage["branch"]["covered"] - seed_branch) * 1000 / item["api_tokens"], 6)
                     if item["api_tokens"] else None})
    (run / "group-progress.json").write_text(json.dumps(group_progress, indent=2) + "\n")
    write_csv(run / "rounds.csv", rows)
    targets = []
    for arm in config["arms"]:
        for rep in range(1, config["repetitions"] + 1):
            series = [row for row in rows if row["arm"] == arm and row["repetition"] == rep]
            reached = next((row for row in series if row["target_reached"]), None)
            observation = reached or (series[-1] if series else None)
            if observation is None:
                raise AssertionError("No observation for configured repetition")
            targets.append({"arm": arm, "repetition": rep,
                            "status": "reached" if reached else "not reached",
                            "first_target_round": reached["round"] if reached else "",
                            "late_source_counters_at_observation": observation["late_source_counters_covered"],
                            "branch_at_observation": observation["branch_covered"],
                            "api_tokens": observation["cumulative_api_tokens"],
                            "executed_cycles": observation["cumulative_executed_cycles"],
                            "simulator_executions": observation["cumulative_simulator_executions"],
                            "model_calls": observation["cumulative_model_calls"],
                            "failed_attempts": observation["cumulative_failed_attempts"],
                            "wall_seconds": observation["total_wall_seconds"]})
    write_csv(run / "target-costs.csv", targets)
    if saved["mode"] == "live":
        os.environ.setdefault("MPLCONFIGDIR", str(run / "mplconfig"))
        os.environ.setdefault("XDG_CACHE_HOME", str(run / "cache"))
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 2, figsize=(10, 7))
        metrics = (("cumulative_api_tokens", "API input + output tokens"),
                   ("cumulative_executed_cycles", "executed cycles incl. replay"),
                   ("cumulative_simulator_executions", "simulator executions"),
                   ("total_wall_seconds", "wall seconds"))
        colors = {"A": "tab:gray", "B": "tab:blue", "P": "tab:green", "C": "tab:orange"}
        for ax, (field, label) in zip(axes.flat, metrics):
            for arm in config["arms"]:
                for rep in range(1, config["repetitions"] + 1):
                    series = [row for row in rows if row["arm"] == arm and row["repetition"] == rep]
                    ax.plot([row[field] for row in series],
                            [row["late_source_counters_covered"] for row in series],
                            "o-", color=colors[arm], alpha=0.55,
                            label=arm if rep == 1 else None)
            ax.axhline(len(target_lines), color="black", linestyle="--", linewidth=0.8)
            ax.set(xlabel=label, ylabel="late DUT source counters (of 4)", ylim=(-0.15, 4.3))
            ax.grid(alpha=0.25)
            ax.legend()
        fig.suptitle("Frozen FIFO mechanism pilot: individual repetitions")
        fig.tight_layout()
        fig.savefig(run / "coverage-cost.png", dpi=150)
        plt.close(fig)
    print(json.dumps({"round_rows": len(rows), "target_rows": len(targets),
                      "reached": {arm: sum(t["status"] == "reached" for t in targets
                                          if t["arm"] == arm) for arm in config["arms"]}}, indent=2))


if __name__ == "__main__":
    main()
