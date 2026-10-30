#!/usr/bin/env python3
"""Record an outcome-blind, deliberately restricted screen of all 68 CVDP rows.

The screen discovers candidates only. It does not establish coverage, checker
validity, or LLM performance; the selected IPs undergo stricter preflight.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

from typed_predicates import RTLIL, group_candidates


ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "docs/midterm-candidate-lock.json").read_text())
OUT = ROOT / "results/midterm_candidate_preflight/screening.json"


def scan_source(source: Path):
    with tempfile.TemporaryDirectory(prefix="midterm-rtlil-") as folder:
        rtlil = Path(folder) / "model.il"
        proc = subprocess.run(["yosys", "-Q", "-T", "-q", "-p",
                               f"read_verilog -sv {source}; write_rtlil {rtlil}"],
                              text=True, capture_output=True, timeout=30)
        if proc.returncode:
            return {"status": "unsupported_yosys", "reason": proc.stderr[-300:]}
        text = rtlil.read_text()
        starts = [m.start() for m in re.finditer(r"^module ", text, re.M)]
        modules = []
        for i, start in enumerate(starts):
            block = text[start:starts[i + 1] if i + 1 < len(starts) else None]
            try:
                extraction = RTLIL(block, source).extract()
                groups = group_candidates(extraction, min_depth=2)
                modules.append({"name": block.splitlines()[0][7:],
                                "supported_targets": len(extraction["targets"]),
                                "unsupported_cases": len(extraction["unsupported"]),
                                "potential_groups": [{"size": len(g),
                                                      "lines": [t["line"] for t in g],
                                                      "case_value": g[0]["case_value"],
                                                      "guard_depth": g[0]["guard_depth"],
                                                      "event_context": g[0]["event_context"]} for g in groups]})
            except (ValueError, IndexError, KeyError) as exc:
                modules.append({"name": block.splitlines()[0][7:],
                                "status": "unsupported_frontend", "reason": str(exc)[:300]})
        return {"status": "parsed", "modules": modules}


def main():
    raw = (ROOT / ".cache" / LOCK["dataset_file"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != LOCK["dataset_sha256"]:
        raise ValueError("Pinned dataset hash mismatch")
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if len(rows) != 68:
        raise ValueError("Expected 68 pinned CVDP rows")
    results = []
    for row in rows:
        sources = [(name, contents) for name, contents in row.get("harness", {}).items()
                   if name.endswith((".sv", ".v"))]
        has_spec = "docs/specification.md" in row.get("context", {})
        if not has_spec:
            has_spec = "docs/specs.md" in row.get("context", {})
        item = {"id": row["id"], "categories": row.get("categories", []),
                "has_standalone_spec_document": has_spec,
                "source_files": [name for name, _ in sources], "sources": []}
        with tempfile.TemporaryDirectory(prefix="cvdp-midterm-screen-") as folder:
            for name, contents in sources:
                path = Path(folder) / Path(name).name
                path.write_text(contents)
                item["sources"].append({"field": name, **scan_source(path)})
        item["potential_group_count"] = sum(
            len(module.get("potential_groups", []))
            for source in item["sources"] for module in source.get("modules", []))
        results.append(item)
    output = {"dataset_sha256": LOCK["dataset_sha256"], "records_screened": len(results),
              "rule": "harness RTL only; Yosys pre-proc per file/module; full guard exact matches at >=2 distinct source locations, depth >=2 and identical process event set; standalone spec document noted separately",
              "limitation": "Exact-string groups are a candidate filter, not a complete e-graph screen. Unsupported frontend cases and absent groups do not prove semantic redundancy absent.",
              "results": results}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"records": len(results),
                      "with_potential_groups": [r["id"] for r in results if r["potential_group_count"]],
                      "selected": [c["id"] for c in LOCK["candidates"]]}, indent=2))


if __name__ == "__main__":
    main()
