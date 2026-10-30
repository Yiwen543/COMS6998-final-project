`timescale 1ns/1ps
module tb_decoder_reset_preclock;
  logic clk_in = 0, rst_in = 1, decoder_data_valid_in = 0;
  logic [65:0] decoder_data_in = 0;
  wire [63:0] decoder_data_out;
  wire [7:0] decoder_control_out;
  wire sync_error, decoder_error_out;
  decoder_data_control_64b66b dut (
    .clk_in, .rst_in, .decoder_data_valid_in, .decoder_data_in,
    .decoder_data_out, .decoder_control_out, .sync_error, .decoder_error_out
  );
  initial begin
    #2 rst_in = 0;
    decoder_data_valid_in = 1;
    decoder_data_in = {2'b00, 64'b0};
    #3 clk_in = 1;
    #1 if (sync_error !== 1) $fatal(1, "Invalid-header setup failed");
    clk_in = 0;
    #2 rst_in = 1;  // Assert strictly between clock rising edges.
    #1 if (sync_error !== 0) $fatal(1, "Reset did not clear before next clock");
    $display("ASYNC_RESET_OBSERVED codec decoder");
    $finish;
  end
endmodule
