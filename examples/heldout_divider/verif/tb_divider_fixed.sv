`timescale 1ns/1ps
module tb_divider_fixed;
  logic clk = 1'b0;
  always #5 clk = ~clk;
  logic rst_n = 1'b1;
  logic start = 1'b0;
  logic [7:0] dividend = 0, divisor = 1;
  wire [7:0] quotient, remainder;
  wire done;
  radix2_div dut (.*);

  string vector_path;
  integer fd, parsed, step;
  integer reset_hex, start_hex, dividend_hex, divisor_hex;
  logic [7:0] pre_q, pre_r;
  logic pre_done;
  initial begin
    if (!$value$plusargs("VECTORS=%s", vector_path)) $fatal(1, "Missing +VECTORS");
    fd = $fopen(vector_path, "r");
    if (fd == 0) $fatal(1, "Cannot open vectors");
    step = 0;
    while (!$feof(fd)) begin
      parsed = $fscanf(fd, "%h %h %h %h\n", reset_hex, start_hex, dividend_hex, divisor_hex);
      if (parsed == 4) begin
        @(negedge clk);
        rst_n = reset_hex[0];
        start = start_hex[0];
        dividend = dividend_hex[7:0];
        divisor = divisor_hex[7:0];
        #1;
        pre_q = quotient;
        pre_r = remainder;
        pre_done = done;
        @(posedge clk);
        #1;
        $display("TRACE %0h %0h %0h %0h %0h %0h %0h",
                 step, pre_q, pre_r, pre_done, quotient, remainder, done);
        step = step + 1;
      end else if (parsed != -1) begin
        $fatal(1, "Malformed vector at step %0d", step);
      end
    end
    $fclose(fd);
    $display("DRIVER_OK steps=%0d", step);
    $finish;
  end
endmodule
