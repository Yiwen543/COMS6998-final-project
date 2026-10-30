#!/usr/bin/env python3
"""Outcome-blind screen of supplied context RTL in pinned CVDP copilot slice."""
import hashlib
import json
import tempfile
from pathlib import Path

from screen_midterm_candidates import ROOT, scan_source


DATASET = ROOT / ".cache/cvdp_v1.1.0_nonagentic_code_generation_no_commercial.jsonl"
OUT = ROOT / "results/midterm_candidate_preflight/nonagentic-context-screening.json"


def main():
    raw = DATASET.read_bytes()
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    result = {"dataset_file": DATASET.name, "dataset_sha256": hashlib.sha256(raw).hexdigest(),
              "records_screened": len(rows),
              "method": "input.context RTL only; never output, harness tests, solutions, or model outcomes; Yosys pre-proc complete-guard exact candidate groups",
              "records": []}
    for row in rows:
        item = {"id": row["id"], "categories": row.get("categories", []),
                "prompt_bytes": len(row.get("input", {}).get("prompt", "").encode()),
                "sources": []}
        with tempfile.TemporaryDirectory(prefix="cvdp-nonagentic-screen-") as temp:
            for name, contents in row.get("input", {}).get("context", {}).items():
                if not name.endswith((".sv", ".v")) or not contents:
                    continue
                source = Path(temp) / Path(name).name
                source.write_text(contents)
                item["sources"].append({"field": name, "sha256": hashlib.sha256(contents.encode()).hexdigest(),
                                        **scan_source(source)})
        item["potential_group_count"] = sum(
            len(module.get("potential_groups", []))
            for source in item["sources"] for module in source.get("modules", []))
        result["records"].append(item)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("rows", len(rows), "with RTL", sum(bool(x["sources"]) for x in result["records"]))
    for item in result["records"]:
        if item["potential_group_count"]:
            print(item["id"], item["potential_group_count"])


if __name__ == "__main__":
    main()
