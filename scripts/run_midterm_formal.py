#!/usr/bin/env python3
"""Run the first, deliberately narrow specification-property references."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/midterm_candidate_preflight"
RUNS = {
    "heldout_codec64": ("decoder_sync_error.sby", "formal_decoder.sv"),
    "heldout_linear_search": ("search_safety.sby", "formal_search.sv"),
}


def version(argv):
    proc = subprocess.run(argv, text=True, capture_output=True, check=True)
    return (proc.stdout or proc.stderr).splitlines()[0]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    evidence = {"scope": "first narrow specification properties; not complete IP correctness",
                "versions": {"sby": version(["sby", "--version"]),
                             "z3": version(["z3", "--version"]),
                             "yosys": version(["yosys", "-V"])},
                "runs": []}
    for slug, (job_name, harness_name) in RUNS.items():
        formal_dir = ROOT / "examples" / slug / "formal"
        for task in ("bmc", "cover", "prove"):
            build = ROOT / "build" / f"midterm_formal_{slug}_{task}"
            cmd = ["sby", "-f", "-d", str(build), job_name, task]
            proc = subprocess.run(cmd, cwd=formal_dir, text=True,
                                  capture_output=True, timeout=90)
            log = OUT / f"{slug}-{task}.log"
            log.write_text(proc.stdout + proc.stderr)
            status_file = build / "status"
            status = status_file.read_text().split()[0] if status_file.exists() else "ERROR"
            entry = {"ip": slug, "task": task, "command": cmd,
                     "sby_file_sha256": hashlib.sha256((formal_dir / job_name).read_bytes()).hexdigest(),
                     "harness_sha256": hashlib.sha256((formal_dir / harness_name).read_bytes()).hexdigest(),
                     "status": status, "exit_code": proc.returncode,
                     "cover_reached": "reached cover statement" in (proc.stdout + proc.stderr),
                     "log": str(log.relative_to(ROOT))}
            traces = []
            for index, source in enumerate(sorted(build.glob("engine_*/trace*.vcd"))):
                target = OUT / f"{slug}-{task}-trace{index}.vcd"
                shutil.copyfile(source, target)
                traces.append({"path": str(target.relative_to(ROOT)),
                               "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
            entry["traces"] = traces
            evidence["runs"].append(entry)
            print(f"{slug} {task}: {status}")
    (OUT / "formal-results.json").write_text(json.dumps(evidence, indent=2) + "\n")
    if any(row["status"] != "PASS" or row["exit_code"] for row in evidence["runs"]):
        raise SystemExit("One or more formal tasks did not pass; inspect formal-results.json")


if __name__ == "__main__":
    main()
