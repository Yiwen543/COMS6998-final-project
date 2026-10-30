`timescale 1ns/1ps
module tb_sfifo_fixed;
  logic i_clk = 1'b0;
  always #5 i_clk = ~i_clk;

  logic i_reset = 1'b0;
  logic i_wr = 1'b0;
  logic i_rd = 1'b0;
  logic [7:0] i_data = 8'h00;
  wire o_full, o_empty;
  wire [3:0] o_fill;
  wire [7:0] o_data;

  sfifo #(.BW(8), .LGFLEN(3), .OPT_ASYNC_READ(1'b1),
          .OPT_WRITE_ON_FULL(1'b0), .OPT_READ_ON_EMPTY(1'b0)) dut (.*);

  string vector_path;
  integer fd, parsed, step;
  integer reset_hex, wr_hex, rd_hex, data_hex;
  logic [3:0] pre_fill;
  logic pre_full, pre_empty;
  logic [7:0] pre_data;

  initial begin
    if (!$value$plusargs("VECTORS=%s", vector_path)) $fatal(1, "Missing +VECTORS");
    fd = $fopen(vector_path, "r");
    if (fd == 0) $fatal(1, "Cannot open vectors");
    step = 0;
    while (!$feof(fd)) begin
      parsed = $fscanf(fd, "%h %h %h %h\n", reset_hex, wr_hex, rd_hex, data_hex);
      if (parsed == 4) begin
        @(negedge i_clk);
        i_reset = reset_hex[0];
        i_wr = wr_hex[0];
        i_rd = rd_hex[0];
        i_data = data_hex[7:0];
        #1;
        pre_fill = o_fill;
        pre_full = o_full;
        pre_empty = o_empty;
        pre_data = o_data;
        @(posedge i_clk);
        #1;
        $display("TRACE %0h %0h %0h %0h %0h %0h %0h %0h %0h",
                 step, pre_fill, pre_full, pre_empty, pre_data,
                 o_fill, o_full, o_empty, o_data);
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
