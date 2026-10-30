`timescale 1ns/1ps
module tb_codec_preflight;
  logic clk_in = 0;
  always #5 clk_in = ~clk_in;
  logic rst_in = 1;
  logic [63:0] enc_data_in = 0;
  logic [7:0] enc_control_in = 0;
  logic [65:0] enc_data_out;
  logic dec_data_valid_in = 0;
  logic [65:0] dec_data_in = 0;
  logic [63:0] dec_data_out;
  logic [7:0] dec_control_out;
  logic dec_sync_error, dec_error_out;

  top_64b66b_codec dut (
    .clk_in, .rst_in, .enc_data_in, .enc_control_in, .enc_data_out,
    .dec_data_valid_in, .dec_data_in, .dec_data_out, .dec_control_out,
    .dec_sync_error, .dec_error_out
  );

  initial begin
    repeat (2) @(negedge clk_in);
    rst_in = 0;
    repeat (4) @(negedge clk_in);
    if ($test$plusargs("CALIBRATE")) begin
      // Separate reachability calibration. These vectors are never model input.
      enc_control_in = 8'hff;
      enc_data_in = 64'h0707070707070707;
      dec_data_valid_in = 1;
      dec_data_in = {2'b10, 8'h1e, 56'h0};
      @(negedge clk_in);
      enc_control_in = 8'h1f;
      enc_data_in = 64'h112233fb07070707;
      dec_data_in = {2'b10, 8'h33, 56'h0};
      @(negedge clk_in);
      enc_control_in = 8'h01;
      enc_data_in = 64'h1234567890abccfb;
      dec_data_in = {2'b01, 64'h1234567890abcdef};
      @(negedge clk_in);
      enc_control_in = 8'h00;
      dec_data_valid_in = 0;
      repeat (2) @(negedge clk_in);
      $display("PREFLIGHT_CALIBRATION_OK");
    end else begin
      $display("PREFLIGHT_SEED_OK cycles=6");
    end
    $finish;
  end
endmodule
