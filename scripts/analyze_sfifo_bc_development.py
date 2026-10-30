#!/usr/bin/env python3
"""Summarize live/mock sfifo B/C development without collapsing source counters."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

from coverage import load
from run_midterm_fixed import ROOT
from run_sfifo_fixed import SOURCE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    run = (ROOT / args.run).resolve()
    summary = json.loads((run / "summary.json").read_text())
    semantic = json.loads((run / "C/semantic.json").read_text())
    source = str(SOURCE.relative_to(ROOT))
    groups = semantic["groups"]
    calls = [json.loads(line) for line in (run / "calls.jsonl").read_text().splitlines()]
    accepted = {(row["arm"], row["round"]): row for row in calls if row.get("accepted")}
    rows = []
    progress = []
    for row in summary["rows"]:
        arm, round_no = row["arm"], row["round"]
        call = accepted[(arm, round_no)]
        raw = run / arm / f"round{round_no}-attempt{call['attempt']}.dat"
        points = load(raw, source, include_descendants=True)
        by_line = {p["line"]: p for p in points if p["type"] == "line" and
                   p["outcome"] == "case" and p["line"] in (90, 91, 156, 157)}
        group_rows = []
        for group in groups:
            members = []
            for member in group["members"]:
                point = by_line[member["line"]]
                members.append({"source": source, "line": point["line"],
                                "column": point["column"], "type": point["type"],
                                "outcome": point["outcome"], "hits": point["hits"]})
            group_rows.append({"eclass": group["eclass_local"], "members": members,
                               "fully_covered": all(m["hits"] > 0 for m in members)})
        progress.append({"arm": arm, "round": round_no, "groups": group_rows,
                         "fully_covered_groups": sum(g["fully_covered"] for g in group_rows),
                         "total_groups": len(group_rows)})
        rows.append({"mode": summary["mode"], "arm": arm, "round": round_no,
                     "line_covered": row["coverage"]["line"]["covered"],
                     "line_total": row["coverage"]["line"]["total"],
                     "branch_covered": row["coverage"]["branch"]["covered"],
                     "branch_total": row["coverage"]["branch"]["total"],
                     "toggle_covered": row["coverage"]["toggle"]["covered"],
                     "toggle_total": row["coverage"]["toggle"]["total"],
                     "fully_covered_groups": progress[-1]["fully_covered_groups"],
                     "api_tokens": row["api_tokens"],
                     "executed_cycles": row["executed_cycles"],
                     "simulator_executions": row["simulator_executions"],
                     "model_calls": row["model_calls"],
                     "failed_attempts": row["failed_attempts"],
                     "distinct_defects": ";".join(row["checker"]["distinct_defects"]),
                     "compile_seconds": row["compile_seconds"],
                     "simulation_seconds_cumulative": row["simulation_seconds_cumulative"],
                     "egraph_preprocessing_seconds": row["egraph_preprocessing_seconds"],
                     "total_wall_seconds": row["total_wall_seconds"]})
    (run / "group-progress.json").write_text(json.dumps(progress, indent=2) + "\n")
    with (run / "comparison.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    if summary["mode"] == "live":
        os.environ.setdefault("MPLCONFIGDIR", str(run / "mplconfig"))
        os.environ.setdefault("XDG_CACHE_HOME", str(run / "cache"))
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
        for arm, color in (("B", "tab:blue"), ("C", "tab:orange")):
            arm_rows = [r for r in rows if r["arm"] == arm]
            axes[0].plot([r["api_tokens"] for r in arm_rows],
                         [r["branch_covered"] for r in arm_rows], "o-", color=color, label=arm)
            axes[1].plot([r["executed_cycles"] for r in arm_rows],
                         [r["toggle_covered"] for r in arm_rows], "o-", color=color, label=arm)
        axes[0].set(xlabel="API input + output tokens", ylabel="DUT branch points (of 14)")
        axes[1].set(xlabel="Executed cycles, including replay", ylabel="DUT toggle directions (of 204)")
        for ax in axes:
            ax.grid(alpha=0.25)
            ax.legend()
        fig.suptitle("sfifo B/C development trial (one session per arm)")
        fig.tight_layout()
        fig.savefig(run / "comparison.png", dpi=150)
        plt.close(fig)
    print(json.dumps({"mode": summary["mode"], "rows": len(rows),
                      "group_progress": [(p["arm"], p["round"], p["fully_covered_groups"])
                                         for p in progress]}, indent=2))


if __name__ == "__main__":
    main()
