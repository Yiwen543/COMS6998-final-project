#!/usr/bin/env python3
"""Join development B raw counters to prequalified source-distinct groups."""
import argparse
import json
from pathlib import Path

from coverage import load
from run_midterm_fixed import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    run = (ROOT / args.run).resolve()
    selection = json.loads((ROOT / "results/midterm_candidate_preflight/selection.json").read_text())
    calls = [json.loads(line) for line in (run / "calls.jsonl").read_text().splitlines()]
    results = []
    for ip, slug in (("codec", "heldout_codec64"), ("search", "heldout_linear_search")):
        candidate = next(item for item in selection["ips"] if item["slug"] == slug)
        groups = [group for group in candidate["groups"] if group["qualifies_preflight"]]
        sources = sorted((ROOT / "examples" / slug / "rtl").glob("*.sv"))
        for call in calls:
            if call["ip"] != ip or not call["accepted"]:
                continue
            dat = run / ip / f"round{call['round']}-attempt{call['attempt']}.dat"
            points = [p for source in sources for p in
                      load(dat, str(source.relative_to(ROOT)), include_descendants=True)]
            indexed = {(p["source"], p["line"], p["column"], p["type"], p["outcome"]): p["hits"]
                       for p in points}
            group_results = []
            for group in groups:
                hits = []
                for member in group["members"]:
                    mapping = member["seed_coverage"]
                    key = (group["source"], member["line"], mapping["column"],
                           mapping["type"], mapping["outcome"])
                    hits.append(indexed[key] > 0)
                group_results.append({"source": group["source"],
                                      "lines": [m["line"] for m in group["members"]],
                                      "covered_members": sum(hits), "total_members": len(hits)})
            results.append({"ip": ip, "round": call["round"],
                            "fully_covered_groups": sum(g["covered_members"] == g["total_members"]
                                                        for g in group_results),
                            "total_groups": len(group_results), "groups": group_results})
    (run / "semantic-group-progress.json").write_text(json.dumps({"scope": "development B only",
                                                                   "rows": results}, indent=2) + "\n")
    for row in results:
        print(row["ip"], row["round"], row["fully_covered_groups"], row["total_groups"])


if __name__ == "__main__":
    main()
