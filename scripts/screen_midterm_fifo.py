#!/usr/bin/env python3
"""Second-stage CVDP async FIFO screen with hierarchy flattened before proc.

This is a candidate screen only. It deliberately does not use model outcomes,
benchmark patches, or benchmark testbenches.
"""
from __future__ import annotations

import hashlib
import json
import argparse
import subprocess
from pathlib import Path

from coverage import load, summary
from preflight_heldout import z3_equivalent
from typed_predicates import RTLIL, group_candidates


ROOT = Path(__file__).resolve().parents[1]
PIN = ROOT / ".cache/cvdp_v1.1.0_agentic_code_generation_commercial.jsonl"
OUT = ROOT / "results/midterm_candidate_preflight"
IDS = ("cvdp_agentic_async_fifo_compute_ram_application_0003",
       "cvdp_agentic_async_fifo_compute_ram_application_0004")
TB = """`timescale 1ns/1ps
module tb_async_fifo_screen;
  logic i_wr_clk = 0, i_rd_clk = 0;
  always #5 i_wr_clk = ~i_wr_clk;
  always #7 i_rd_clk = ~i_rd_clk;
  logic i_wr_rst_n = 0, i_rd_rst_n = 0;
  logic i_wr_en = 0, i_rd_en = 0;
  logic [7:0] i_wr_data = 0;
  wire o_fifo_full, o_fifo_empty;
  wire [7:0] o_rd_data;
  async_fifo #(.p_data_width(8), .p_addr_width(3)) dut (.*);
  initial begin
    repeat (2) @(negedge i_rd_clk);
    i_wr_rst_n = 1; i_rd_rst_n = 1;
    repeat (4) @(negedge i_rd_clk);
    $display("FIFO_SEED_OK");
    $finish;
  end
endmodule
"""


def run(argv, log, stdin=None, timeout=180):
    proc = subprocess.run([str(value) for value in argv], cwd=ROOT, input=stdin,
                          text=True, capture_output=True, timeout=timeout)
    log.write_text(proc.stdout + proc.stderr)
    if proc.returncode:
        raise RuntimeError(f"Command failed: {log}")
    return proc.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=IDS, default=IDS[0])
    args = parser.parse_args()
    task_id = args.task
    build = ROOT / "build" / f"midterm_async_fifo_screen_{task_id[-4:]}"
    build.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    record_line = next(line for line in PIN.read_text().splitlines()
                       if json.loads(line)["id"] == task_id)
    row = json.loads(record_line)
    source = build / "async_fifo.sv"
    source.write_text(row["harness"]["src/async_fifo.sv"])
    tb = build / "tb_async_fifo_screen.sv"
    tb.write_text(TB)
    rtlil = build / "flattened.il"
    run(["yosys", "-Q", "-T", "-q", "-p",
         f"read_verilog -sv {source}; hierarchy -check -top async_fifo; flatten; write_rtlil {rtlil}"],
        build / "yosys.log")
    extracted = RTLIL(rtlil.read_text(), source).extract()
    engine = ROOT / "egraph/target/debug/rtl-predicate-egraph"
    payload = [{"id": t["id"], "compact": t["compact"], "expanded": t["compact"]}
               for t in extracted["targets"]]
    graph = json.loads(run([engine], build / "egg.log", json.dumps(payload), timeout=15))
    roots = {target["id"]: target["eclass"] for target in graph["targets"]}
    candidates = group_candidates(extracted, min_depth=1)
    vbuild = build / "verilator-build"
    run(["verilator", "--binary", "--timing", "--coverage-line", "--coverage-toggle",
         "--coverage-expr", "-Wno-fatal", "-Wno-TIMESCALEMOD", "-Wno-WIDTHEXPAND",
         "--top-module", "tb_async_fifo_screen", "--Mdir", vbuild, "-j", "2", source, tb],
        build / "compile.log", timeout=240)
    dat = OUT / f"fifo-{task_id[-4:]}-seed.dat"
    seed_log = run([vbuild / "Vtb_async_fifo_screen", f"+verilator+coverage+file+{dat}"],
                   OUT / f"fifo-{task_id[-4:]}-seed.log", timeout=30)
    if "FIFO_SEED_OK" not in seed_log:
        raise AssertionError("FIFO seed did not finish")
    points = load(dat, str(source), include_descendants=True)
    groups = []
    for members in candidates:
        if not all(roots[m["id"]] == roots[members[0]["id"]] and
                   z3_equivalent(members[0]["compact"], m["compact"]) for m in members[1:]):
            raise AssertionError("Unverified FIFO equivalence")
        mapped = []
        for member in members:
            same = [p for p in points if p["line"] == member["line"] and
                    p["type"] in ("line", "branch")]
            line_points = [p for p in same if p["type"] == "line"]
            if len(line_points) == 1:
                same = line_points
            elif not line_points:
                same = [p for p in same if p["type"] == "branch" and p["outcome"] == "if"]
            mapped.append({"line": member["line"], "status": "mapped" if len(same) == 1 else "unmapped_or_ambiguous",
                           "hits": same[0]["hits"] if len(same) == 1 else None})
        groups.append({"eclass": roots[members[0]["id"]], "guard": members[0]["compact"],
                       "event_context": members[0]["event_context"], "depth": members[0]["guard_depth"],
                       "members": mapped,
                       "seed_uncovered": all(m["status"] == "mapped" and m["hits"] == 0 for m in mapped)})
    result = {"id": task_id, "scope": "flattened hierarchy, binary/two-state supported guards; candidate screen only",
              "dataset_sha256": hashlib.sha256(PIN.read_bytes()).hexdigest(),
              "record_sha256": hashlib.sha256(record_line.encode()).hexdigest(),
              "rtl_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "spec_sha256": hashlib.sha256(row["context"]["docs/fifo.md"].encode()).hexdigest(),
              "supported_targets": len(extracted["targets"]), "unsupported": extracted["unsupported"],
              "seed_coverage": summary(points), "groups": groups,
              "qualifying_seed_uncovered_groups": sum(g["seed_uncovered"] for g in groups),
              "limitation": "No functional checker or calibrated reachability run; source-mapped reset groups are covered by seed."}
    (OUT / f"fifo-hierarchical-screen-{task_id[-4:]}.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"supported_targets": result["supported_targets"],
                      "groups": len(groups), "seed_uncovered_groups": result["qualifying_seed_uncovered_groups"],
                      "coverage": result["seed_coverage"]}, indent=2))


if __name__ == "__main__":
    main()
