`timescale 1ns/1ps
module tb_txuart_fixed;
  reg i_clk = 0;
  reg i_reset = 0;
  reg [30:0] i_setup = 31'h40000002;
  reg i_break = 0;
  reg i_wr = 0;
  reg [7:0] i_data = 0;
  reg i_cts_n = 1;
  wire o_uart_tx;
  wire o_busy;
  integer fd, got, cycle;
  integer reset_value, break_value, wr_value, data_value;
  reg pre_busy;

  txuart #(.INITIAL_SETUP(31'h40000002)) dut (
    .i_clk(i_clk), .i_reset(i_reset), .i_setup(i_setup),
    .i_break(i_break), .i_wr(i_wr), .i_data(i_data),
    .i_cts_n(i_cts_n), .o_uart_tx(o_uart_tx), .o_busy(o_busy)
  );

  initial begin
    if (!$value$plusargs("VECTORS=%s", vector_path)) $fatal(1, "VECTORS missing");
    fd = $fopen(vector_path, "r");
    if (fd == 0) $fatal(1, "cannot open vectors");
    cycle = 0;
    while (!$feof(fd)) begin
      got = $fscanf(fd, "%d %d %d %d\n", reset_value, break_value, wr_value, data_value);
      if (got == 4) begin
        i_reset = reset_value[0];
        i_break = break_value[0];
        i_wr = wr_value[0];
        i_data = data_value[7:0];
        #1;
        pre_busy = o_busy;
        i_clk = 1;
        #1;
        $display("TRACE %0d %0d %0d %0d %0d %0d %0d %0d",
                 cycle, i_reset, i_break, i_wr, i_data, pre_busy, o_busy, o_uart_tx);
        i_clk = 0;
        #1;
        cycle = cycle + 1;
      end
    end
    $fclose(fd);
    $display("DRIVER_OK steps=%0d", cycle);
    $finish;
  end
  string vector_path;
endmodule
