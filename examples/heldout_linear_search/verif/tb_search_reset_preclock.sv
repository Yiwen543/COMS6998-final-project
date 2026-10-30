`timescale 1ns/1ps
module tb_search_reset_preclock;
  logic clk = 0, srst = 1, start = 0, pause = 0, search_done = 0;
  wire enable, done;
  linear_search_ctrl dut (
    .clk, .srst, .start, .pause, .search_done, .enable, .done
  );
  initial begin
    #1 clk = 1;
    #1 clk = 0;
    srst = 0;
    start = 1;
    #1 clk = 1;
    #1 clk = 0;
    start = 0;
    search_done = 1;
    #1 clk = 1;
    #1 clk = 0;
    search_done = 0;
    #1 if (done !== 1) $fatal(1, "Completion setup failed");
    srst = 1;  // Assert strictly between clock rising edges.
    #1 if (done !== 0) $fatal(1, "Reset did not clear before next clock");
    $display("ASYNC_RESET_OBSERVED search controller");
    $finish;
  end
endmodule
