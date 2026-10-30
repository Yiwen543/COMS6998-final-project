#!/usr/bin/env python3
"""Outcome-blind semantic and reachability screen of ZipCPU's pinned FIFO."""
import hashlib
import json
import subprocess
from pathlib import Path

from coverage import load, summary
from preflight_midterm_candidates import ROOT, run, semantic_groups, source_point


COMMIT = "2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b"
UPSTREAM = "https://github.com/ZipCPU/wb2axip"
FOLDER = ROOT / "build/external_wb2axip"
SOURCE = FOLDER / "rtl/sfifo.v"
OUT = ROOT / "results/midterm_candidate_preflight/external-sfifo"
BUILD = ROOT / "build/midterm_external_sfifo"
TB = """`timescale 1ns/1ps
module tb_sfifo_screen;
  logic i_clk = 0;
  always #5 i_clk = ~i_clk;
  logic i_reset = 1, i_wr = 0, i_rd = 0;
  logic [7:0] i_data = 0;
  wire o_full, o_empty;
  wire [3:0] o_fill;
  wire [7:0] o_data;
  sfifo #(.BW(8), .LGFLEN(3), .OPT_ASYNC_READ(1'b1),
          .OPT_WRITE_ON_FULL(1'b0), .OPT_READ_ON_EMPTY(1'b0)) dut (.*);
  initial begin
    repeat (2) @(negedge i_clk);
    i_reset = 0;
    repeat (4) @(negedge i_clk);
    if ($test$plusargs("CALIBRATE")) begin
      // Separate source reachability only. Never sent to any model.
      i_wr = 1;
      for (int j=0; j<8; j++) begin
        i_data = 8'(j+1);
        @(negedge i_clk);
      end
      i_wr = 0; i_rd = 1;
      repeat (8) @(negedge i_clk);
      i_wr = 1; i_rd = 0; i_data = 8'h55;
      repeat (3) @(negedge i_clk);
      i_rd = 1; i_data = 8'haa;
      repeat (3) @(negedge i_clk);
      i_wr = 0; i_rd = 0; i_reset = 1;
      @(negedge i_clk);
      $display("SFIFO_CALIBRATION_OK");
    end else $display("SFIFO_SEED_OK");
    $finish;
  end
endmodule
"""


def main():
    head = subprocess.run(["git", "-C", FOLDER, "rev-parse", "HEAD"], text=True,
                          capture_output=True, check=True).stdout.strip()
    if head != COMMIT:
        raise ValueError("External FIFO checkout changed")
    OUT.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    tb = BUILD / "tb_sfifo_screen.sv"
    tb.write_text(TB)
    extraction, semantic = semantic_groups(SOURCE, OUT / "semantic.json")
    groups = semantic["groups"]
    vbuild = BUILD / "verilator-build"
    run(["verilator", "--binary", "--timing", "--coverage-line", "--coverage-toggle",
         "--coverage-expr", "-Wno-fatal", "-Wno-TIMESCALEMOD", "-Wno-WIDTHEXPAND",
         "--top-module", "tb_sfifo_screen", "--Mdir", vbuild, "-j", "2", SOURCE, tb],
        log=OUT / "compile.log", timeout=240)
    binary = vbuild / "Vtb_sfifo_screen"
    seed = OUT / "seed.dat"
    calibration = OUT / "calibration.dat"
    if "SFIFO_SEED_OK" not in run([binary, f"+verilator+coverage+file+{seed}"], log=OUT / "seed.log"):
        raise AssertionError("Seed incomplete")
    if "SFIFO_CALIBRATION_OK" not in run([binary, "+CALIBRATE", f"+verilator+coverage+file+{calibration}"],
                                         log=OUT / "calibration.log"):
        raise AssertionError("Calibration incomplete")
    rel = str(SOURCE.relative_to(ROOT))
    seed_points = load(seed, rel, include_descendants=True)
    calibration_points = load(calibration, rel, include_descendants=True)
    targets = {t["id"]: t for t in extraction["targets"]}
    for group in groups:
        for member, target_id in zip(group["members"], group["member_ids"]):
            target = targets[target_id]
            member["seed_coverage"] = source_point(target, seed_points)
            member["calibration_coverage"] = source_point(target, calibration_points)
        group["qualifies_preflight"] = all(
            m["seed_coverage"]["status"] == "mapped" and m["seed_coverage"]["hits"] == 0 and
            m["calibration_coverage"]["status"] == "mapped" and m["calibration_coverage"]["hits"] > 0
            for m in group["members"])
    result = {"upstream": UPSTREAM, "commit": COMMIT,
              "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "testbench_sha256": hashlib.sha256(tb.read_bytes()).hexdigest(),
              "scope": "candidate screen only; original source, binary/two-state guards, no functional checker",
              "supported_targets": len(extraction["targets"]),
              "unsupported": extraction["unsupported"],
              "seed_coverage": summary(seed_points), "calibration_coverage": summary(calibration_points),
              "groups": groups,
              "qualifying_groups": sum(g["qualifies_preflight"] for g in groups)}
    (OUT / "screen.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"groups": len(groups), "qualifying": result["qualifying_groups"],
                      "seed": result["seed_coverage"], "calibration": result["calibration_coverage"]}, indent=2))


if __name__ == "__main__":
    main()
