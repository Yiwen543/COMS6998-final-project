#!/usr/bin/env python3
"""Replay the fixed arbiter seed with witnesses and specification probes independently enabled."""
import argparse
import gzip
import json
import re
import subprocess
import tempfile
from pathlib import Path

from benchmark_m3_rtl import PROBES, TB, TOP, file_hash, observation, replay, require
from coverage import join, summary
from predicates import DUT, ROOT, extract
from run_step1 import write_json


def run_ablation(rtl_run, out):
    setup = json.loads((rtl_run / "setup.json").read_text())
    reference = json.loads((rtl_run / "quality.json").read_text())
    simulator = (rtl_run / "verilator-build" / f"V{TOP}").resolve()
    for name, path in {"simulator": simulator, "rtl": DUT, "testbench": ROOT / TB,
                       "runner": ROOT / "scripts/sim_main.cpp"}.items():
        require(file_hash(path) == setup["sha256"][name], f"{name} hash differs from RTL run")

    targets = extract()
    witnesses = [tuple(reference["witnesses"][t["id"]]) for t in targets if t["id"] in reference["witnesses"]]
    witnesses = list(dict.fromkeys(witnesses))  # The feedback loop deduplicates equal vector triples.
    arms = {"seed": [], "witnesses": witnesses, "probes": PROBES, "combined": witnesses + PROBES}
    report = {"verilator": setup["versions"]["verilator"],
              "iverilog": subprocess.check_output(["iverilog", "-V"], text=True, stderr=subprocess.DEVNULL,
                                                  timeout=10).splitlines()[0],
              "sha256": {k: setup["sha256"][k] for k in ("rtl", "testbench", "runner", "simulator")},
              "frozen_quality_sha256": file_hash(rtl_run / "quality.json"),
              "witnesses_by_target_reset_req_override": reference["witnesses"],
              "probes_reset_req_override": PROBES,
              "runs_per_arm": {"verilator": 1, "icarus": 1}, "arms": {}}
    with tempfile.TemporaryDirectory() as tmp:
        vvp = Path(tmp) / "arbiter.vvp"
        subprocess.run(["iverilog", "-g2012", "-s", TOP, "-o", vvp, DUT.relative_to(ROOT), TB],
                       cwd=ROOT, check=True, capture_output=True, timeout=60)
        for arm, vectors in arms.items():
            folder = out / arm
            folder.mkdir()
            vector_text = "".join(f"{rst} {req:02x} {over:02x}\n" for rst, req, over in vectors)
            if arm == "combined":
                require(vector_text == reference["vector_text"], "combined order differs from frozen run")
            (folder / "vectors.txt").write_text(vector_text)
            mode = 1 if vectors else 0
            points, verilator_log = replay(simulator, folder, "verilator", mode)
            obs = observation(points, verilator_log)
            flags = ["+VECTORS=vectors.txt"] if vectors else []
            icarus = subprocess.run(["vvp", vvp, f"+MODE={mode}", "+COLLECT", *flags], cwd=folder,
                                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
            (folder / "icarus.log").write_text(icarus.stdout)
            icarus.check_returncode()
            require(obs["events"] == observation([], icarus.stdout)["events"], f"checker disagreement in {arm}")
            require(obs["checker"]["checks"] == reference["initial"]["checker"]["checks"] + len(vectors),
                    f"incomplete stimulus replay in {arm}")
            if arm in ("seed", "combined"):
                key = "initial" if arm == "seed" else "refined"
                require(obs == reference[key], f"{arm} differs from frozen point counts or checker")
            failures = []
            for event in obs["events"]:
                if event.startswith("RESULT "):
                    continue
                fields = dict(re.findall(r"\b(reset|req|override)=([0-9a-fA-F]+)\b", event))
                pins = tuple(int(fields[k], 16) for k in ("reset", "req", "override"))
                hits = [i for i, vector in enumerate(vectors, 1) if vector == pins]
                require(len(hits) == 1, f"ambiguous extra-vector attribution for {event}")
                failures.append({"event": event, "extra_vector_1based": hits[0]})
            require(len(failures) == obs["checker"]["functional_errors"] + obs["checker"]["timing_errors"],
                    f"truncated failure log in {arm}")
            rows = join(targets, {"targets": targets}, points)
            report["arms"][arm] = {"checker": obs["checker"], "coverage": summary(points),
                                   "covered_source_guards": [r["id"] for r in rows if r["hits"]],
                                   "failures": failures}
            raw = folder / "verilator.dat"
            (folder / "verilator.dat.gz").write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
            raw.unlink()
    write_json(out / "summary.json", report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rtl-run", type=Path, required=True, help="completed benchmark_m3_rtl.py output with build")
    parser.add_argument("--output", type=Path, required=True, help="new directory for the four replay pairs")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    run_ablation(args.rtl_run, args.output)
