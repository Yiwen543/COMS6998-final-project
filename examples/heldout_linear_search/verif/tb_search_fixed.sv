`timescale 1ns/1ps
module tb_search_fixed;
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

  string vector_path;
  integer fd, fields, step;
  logic pre_done;
  logic [1:0] pre_count;
  logic [5:0] pre_indices;
  logic pre_overflow;
  initial begin
    if (!$value$plusargs("VECTORS=%s", vector_path)) $fatal(1, "VECTORS missing");
    fd = $fopen(vector_path, "r");
    if (!fd) $fatal(1, "Cannot open vectors");
    step = 0;
    forever begin
      @(negedge clk);
      fields = $fscanf(fd, "%h %h %h %h %h %h %h\n", srst, start,
                       pause, key, mem_write_en, mem_write_addr, mem_write_data);
      if (fields == -1) begin
        $display("DRIVER_OK steps=%0d", step);
        $fclose(fd);
        $finish;
      end
      if (fields != 7) $fatal(1, "Malformed vector at step %0d", step);
      #1;
      pre_done = done;
      pre_count = match_count;
      pre_indices = match_indices;
      pre_overflow = match_overflow;
      @(posedge clk);
      #1;
      $display("TRACE %h %h %h %h %h %h %h %h %h", step,
               pre_done, pre_count, pre_indices, pre_overflow,
               done, match_count, match_indices, match_overflow);
      step++;
    end
  end
endmodule
