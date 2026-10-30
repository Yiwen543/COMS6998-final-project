#!/usr/bin/env python3
"""Preserve every fixed-divider repetition and target miss in CSV/plots."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

from coverage import load
from run_divider_fixed import ROOT, SOURCE

SCREEN = ROOT / "results/midterm_candidate_preflight/divider-next/screen.json"


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
    branch_target = config.get("primary_target", {}).get("covered", 24)
    rel = str(SOURCE.relative_to(ROOT))
    rows = []
    group_progress = []
    for item in saved["rows"]:
        arm, rep, round_no = item["arm"], item["repetition"], item["round"]
        folder = run / arm / f"rep{rep}"
        if item["status"] == "ok":
            call = accepted[(arm, rep, round_no)]
            raw = folder / f"round{round_no}-attempt{call['attempt']}.dat"
        else:
            prior = next((accepted[(arm, rep, earlier)] for earlier in range(round_no - 1, 0, -1)
                          if (arm, rep, earlier) in accepted), None)
            raw = (folder / f"round{prior['round']}-attempt{prior['attempt']}.dat"
                   if prior else folder / "seed.dat")
        points = load(raw, rel, include_descendants=True)
        groups = []
        for group in screen["groups"]:
            if not group["qualifies_preflight"]:
                continue
            members = []
            for member in group["members"]:
                mapping = member["seed_coverage"]
                matches = [p for p in points if
                           (p["source"], p["line"], p["column"], p["type"], p["outcome"]) ==
                           (rel, member["line"], mapping["column"], mapping["type"], mapping["outcome"])]
                if len(matches) != 1:
                    raise AssertionError("Source counter mapping changed")
                point = matches[0]
                members.append({"source": rel, "line": point["line"], "column": point["column"],
                                "type": point["type"], "outcome": point["outcome"],
                                "hits": point["hits"]})
            groups.append({"eclass": group["eclass_local"], "members": members,
                           "fully_covered": all(m["hits"] > 0 for m in members)})
        group_progress.append({"arm": arm, "repetition": rep, "round": round_no,
                               "fully_covered_groups": sum(g["fully_covered"] for g in groups),
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
                     "cumulative_api_tokens": item["api_tokens"],
                     "cumulative_model_calls": item["model_calls"],
                     "cumulative_failed_attempts": item["failed_attempts"],
                     "cumulative_simulator_executions": item["simulator_executions"],
                     "cumulative_executed_cycles": item["executed_cycles"],
                     "distinct_defects": ";".join(item["checker"]["distinct_defects"]),
                     "compile_seconds": item["compile_seconds"],
                     "simulation_seconds_cumulative": item["simulation_seconds_cumulative"],
                     "egraph_preprocessing_seconds": item["egraph_preprocessing_seconds"],
                     "total_wall_seconds": item["total_wall_seconds"],
                     "token_roi_branch_per_1000": round(
                         (coverage["branch"]["covered"] - 7) * 1000 / item["api_tokens"], 6)
                     if item["api_tokens"] else None})
    (run / "group-progress.json").write_text(json.dumps(group_progress, indent=2) + "\n")
    write_csv(run / "rounds.csv", rows)
    targets = []
    for arm in config["arms"]:
        for rep in range(1, config["repetitions"] + 1):
            matching = [row for row in rows if row["arm"] == arm and row["repetition"] == rep]
            reached = next((row for row in matching if row["branch_covered"] >= branch_target), None)
            stop = reached or (matching[-1] if matching else None)
            if stop is None:
                seed = json.loads((run / arm / f"rep{rep}/seed.json").read_text())
                branch_covered = seed["coverage"]["branch"]["covered"]
                targets.append({"arm": arm, "repetition": rep, "status": "not reached",
                                "target_branch_points": branch_target, "first_target_round": "",
                                "branch_covered_at_stop": branch_covered, "api_tokens": 0,
                                "executed_cycles": 4, "simulator_executions": 1,
                                "wall_seconds": ""})
            else:
                targets.append({"arm": arm, "repetition": rep,
                                "status": "reached" if reached else "not reached",
                                "target_branch_points": branch_target,
                                "first_target_round": reached["round"] if reached else "",
                                "branch_covered_at_stop": stop["branch_covered"],
                                "api_tokens": stop["cumulative_api_tokens"],
                                "executed_cycles": stop["cumulative_executed_cycles"],
                                "simulator_executions": stop["cumulative_simulator_executions"],
                                "wall_seconds": stop["total_wall_seconds"]})
    write_csv(run / "target-costs.csv", targets)
    if saved["mode"] == "live":
        os.environ.setdefault("MPLCONFIGDIR", str(run / "mplconfig"))
        os.environ.setdefault("XDG_CACHE_HOME", str(run / "cache"))
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 2, figsize=(10, 7))
        metrics = (("cumulative_api_tokens", "API input + output tokens"),
                   ("cumulative_executed_cycles", "executed cycles, including replay"),
                   ("cumulative_simulator_executions", "simulator executions"),
                   ("total_wall_seconds", "wall seconds"))
        colors = {"A": "tab:gray", "B": "tab:blue", "P": "tab:green", "C": "tab:orange"}
        for ax, (field, label) in zip(axes.flat, metrics):
            for arm in config["arms"]:
                for rep in range(1, config["repetitions"] + 1):
                    series = [r for r in rows if r["arm"] == arm and r["repetition"] == rep]
                    if not series:
                        continue
                    ax.plot([r[field] for r in series], [r["branch_covered"] for r in series],
                            "o-", color=colors[arm], alpha=0.55,
                            label=arm if rep == 1 else None)
            ax.axhline(branch_target, color="black", linestyle="--", linewidth=0.8)
            ax.set(xlabel=label, ylabel=f"DUT branch points (of {branch_target})")
            ax.grid(alpha=0.25)
            ax.legend()
        fig.suptitle("Frozen divider pilot: individual repetitions")
        fig.tight_layout()
        fig.savefig(run / "coverage-cost.png", dpi=150)
        plt.close(fig)
    print(json.dumps({"round_rows": len(rows), "target_rows": len(targets),
                      "reached": {arm: sum(t["status"] == "reached" for t in targets
                                          if t["arm"] == arm) for arm in config["arms"]}}, indent=2))


if __name__ == "__main__":
    main()
