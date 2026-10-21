"""Conservative, outcome-blind screen of the pinned local CVDP JSONL."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

from preflight_heldout import ENGINE, ROOT, z3_equivalent
from typed_predicates import extract


def screen_record(record):
    source_fields = [(name, contents) for name, contents in record.get("harness", {}).items()
                     if name.endswith((".sv", ".v"))]
    base = {"id": record["id"], "categories": record.get("categories", []),
            "source_files": [name for name, _ in source_fields]}
    if len(source_fields) != 1:
        return {**base, "status": "unsupported_source_count", "qualifying_groups": []}
    name, contents = source_fields[0]
    with tempfile.TemporaryDirectory(prefix="cvdp-screen-") as folder:
        source = Path(folder) / Path(name).name
        source.write_text(contents)
        try:
            result = extract(source, source.stem)
            targets = [{"id": t["id"], "compact": t["compact"], "expanded": t["compact"]}
                       for t in result["targets"]]
            if not targets:
                return {**base, "status": "no_supported_targets", "qualifying_groups": [],
                        "unsupported_cases": len(result["unsupported"])}
            engine = subprocess.run([str(ENGINE)], input=json.dumps(targets), text=True,
                                    capture_output=True, cwd=ROOT, timeout=15)
            if engine.returncode:
                raise RuntimeError(engine.stderr[-500:])
            graph = json.loads(engine.stdout)
            roots = {row["id"]: row["eclass"] for row in graph["targets"]}
            groups = defaultdict(list)
            for target in result["targets"]:
                if target["kind"] == "explicit_case" and target["guard_depth"] >= 4:
                    groups[(tuple(target["event_context"]), roots[target["id"]])].append(target)
            qualifying = []
            for (events, root), members in groups.items():
                if len({(t["line"], t["column"]) for t in members}) < 2:
                    continue
                if not all(z3_equivalent(members[0]["compact"], t["compact"]) for t in members[1:]):
                    raise AssertionError(f"egg group lacks independent proof: {record['id']}")
                qualifying.append({"eclass_local": root, "event_context": events,
                                   "case_value": members[0]["case_value"],
                                   "source_lines": [t["line"] for t in members],
                                   "members": len(members), "guard_depth": members[0]["guard_depth"]})
            return {**base, "status": "qualifies" if qualifying else "no_qualifying_group",
                    "supported_targets": len(result["targets"]),
                    "unsupported_cases": len(result["unsupported"]),
                    "qualifying_groups": qualifying}
        except (RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
            return {**base, "status": "unsupported_frontend_or_engine",
                    "reason": str(exc)[:500], "qualifying_groups": []}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path,
                        default=ROOT / ".cache/cvdp_v1.1.0_agentic_code_generation_commercial.jsonl")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "results/heldout_queue_preflight/screening.json")
    args = parser.parse_args()
    raw = args.dataset.read_bytes()
    lock = json.loads((ROOT / "docs/heldout-dataset-lock.json").read_text())
    digest = hashlib.sha256(raw).hexdigest()
    if digest != lock["sha256"]:
        raise ValueError(f"screening dataset SHA-256 mismatch: {digest}")
    records = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if len(records) != lock["records"]:
        raise ValueError("screening dataset record count mismatch")
    results = [screen_record(record) for record in records]
    output = {"dataset": str(args.dataset), "dataset_sha256": digest,
              "records_screened": len(records),
              "rule": "single-source RTL; supported Yosys pre-proc path; explicit case guard depth >=4; same process event set; >=2 distinct source locations; shared egg class; independent Z3 XOR-unsat",
              "note": "This restricted screen can miss qualifying designs; failure to qualify is not proof of no semantic redundancy.",
              "results": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"records_screened": len(records),
                      "qualifiers": [r["id"] for r in results if r["status"] == "qualifies"],
                      "unsupported": sum(r["status"].startswith("unsupported") for r in results)}, indent=2))


if __name__ == "__main__":
    main()
