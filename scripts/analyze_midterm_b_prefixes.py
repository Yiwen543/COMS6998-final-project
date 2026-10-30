#!/usr/bin/env python3
"""Replay live development B first-round prefixes; never used as held-out data."""
import argparse
import json
from pathlib import Path

from coverage import load
from run_midterm_fixed import ROOT, SETUPS, simulate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    run = (ROOT / args.run).resolve()
    calls = [json.loads(line) for line in (run / "calls.jsonl").read_text().splitlines()]
    output = run / "prefix_analysis"
    output.mkdir(exist_ok=True)
    selection = json.loads((ROOT / "results/midterm_candidate_preflight/selection.json").read_text())
    rows = []
    for ip in ("codec", "search"):
        call = next(row for row in calls if row["ip"] == ip and row["round"] == 1 and row["accepted"])
        seed = json.loads((ROOT / f"configs/midterm_{ip}_seed.json").read_text())["actions"]
        slug, top = SETUPS[ip]
        folder = run / ip
        binary = folder / "verilator-build" / f"V{top}"
        sources = sorted((ROOT / "examples" / slug / "rtl").glob("*.sv"))
        selected = next(item for item in selection["ips"] if item["slug"] == slug)
        groups = [group for group in selected["groups"] if group["qualifies_preflight"]]
        target = output / ip
        target.mkdir(exist_ok=True)
        for count in (1, 2, 4, 8, 16, 24, 32):
            if count > len(call["actions"]):
                continue
            result = simulate(ip, "verilator", binary, sources, seed + call["actions"][:count],
                              target, f"prefix{count}")
            dat = target / f"prefix{count}.dat"
            points = [point for source in sources for point in
                      load(dat, str(source.relative_to(ROOT)), include_descendants=True)]
            indexed = {(p["source"], p["line"], p["column"], p["type"], p["outcome"]): p["hits"]
                       for p in points}
            group_hits = []
            for group in groups:
                hits = []
                for member in group["members"]:
                    mapping = member["seed_coverage"]
                    key = (group["source"], member["line"], mapping["column"],
                           mapping["type"], mapping["outcome"])
                    hits.append(indexed[key] > 0)
                group_hits.append({"lines": [m["line"] for m in group["members"]],
                                   "covered_members": sum(hits), "total_members": len(hits)})
            rows.append({"ip": ip, "generated_cycles": count, "total_cycles": len(seed) + count,
                         "coverage": result["coverage"],
                         "distinct_defects": result["checker"]["distinct_defects"],
                         "qualifying_groups": group_hits,
                         "fully_covered_groups": sum(g["covered_members"] == g["total_members"]
                                                     for g in group_hits)})
    (output / "prefixes.json").write_text(json.dumps({"scope": "development B first-round replay only",
                                                      "rows": rows}, indent=2) + "\n")
    for row in rows:
        print(row["ip"], row["generated_cycles"],
              row["coverage"]["line"]["covered"], row["coverage"]["branch"]["covered"])


if __name__ == "__main__":
    main()
