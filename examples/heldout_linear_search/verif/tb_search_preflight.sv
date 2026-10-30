`timescale 1ns/1ps
module tb_search_preflight;
  logic clk = 0;
  always #5 clk = ~clk;
  logic srst = 1;
  logic start = 0, pause = 0;
  logic [7:0] key = 0;
  logic mem_write_en = 0;
  logic [2:0] mem_write_addr = 0;
  logic [7:0] mem_write_data = 0;
  logic done;
  logic [1:0] match_count;
  logic [5:0] match_indices;
  logic match_overflow;

  linear_search_top #(.DATA_WIDTH(8), .ADDR_WIDTH(3),
                      .MEM_DEPTH(8), .MAX_MATCHES(2)) dut (
    .clk, .srst, .start, .pause, .key, .mem_write_en,
    .mem_write_addr, .mem_write_data, .done, .match_count,
    .match_indices, .match_overflow
  );

  initial begin
    repeat (2) @(negedge clk);
    srst = 0;
    repeat (4) @(negedge clk);
    if ($test$plusargs("CALIBRATE")) begin
      // Separate reachability calibration. These vectors are never model input.
      key = 8'h5a;
      mem_write_en = 1;
      mem_write_addr = 0;
      mem_write_data = key;
      @(negedge clk);
      mem_write_addr = 1;
      @(negedge clk);
      mem_write_en = 0;
      start = 1;
      @(negedge clk);
      start = 0;
      pause = 1;
      repeat (3) @(negedge clk);
      pause = 0;
      repeat (14) @(negedge clk);
      $display("PREFLIGHT_CALIBRATION_OK");
    end else begin
      $display("PREFLIGHT_SEED_OK cycles=6");
    end
    $finish;
  end
endmodule
