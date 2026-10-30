#!/usr/bin/env python3
"""Outcome-blind guard screen of pinned noncommercial agentic CVDP slice."""
import hashlib
import json
import tempfile
from pathlib import Path

from screen_midterm_candidates import ROOT, scan_source


DATASET = ROOT / ".cache/cvdp_v1.1.0_agentic_code_generation_no_commercial.jsonl"
OUT = ROOT / "results/midterm_candidate_preflight/extended-screening.json"


def main():
    raw = DATASET.read_bytes()
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    result = {"dataset_file": DATASET.name, "dataset_sha256": hashlib.sha256(raw).hexdigest(),
              "records_screened": len(rows),
              "method": "harness RTL plus context rtl/src files (never testbench/patch), Yosys pre-proc per module, exact complete-guard groups at >=2 source positions; candidate filter, not full egg proof",
              "records": []}
    for row in rows:
        item = {"id": row["id"], "categories": row.get("categories", []),
                "spec_files": [name for name in row.get("context", {})
                               if name.endswith(".md") and ("spec" in name.lower() or "fifo" in name.lower())],
                "sources": []}
        with tempfile.TemporaryDirectory(prefix="cvdp-ext-screen-") as temp:
            sources = list(row.get("harness", {}).items()) + [
                (name, contents) for name, contents in row.get("context", {}).items()
                if name.startswith(("rtl/", "src/"))]
            for name, contents in sources:
                if not name.endswith((".sv", ".v")):
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
    print("rows", len(rows))
    for item in result["records"]:
        if "fifo" in item["id"] or item["potential_group_count"] >= 2:
            print(item["id"], "groups", item["potential_group_count"], "specs", item["spec_files"])


if __name__ == "__main__":
    main()
