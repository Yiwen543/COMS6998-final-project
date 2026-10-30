`timescale 1ns/1ps
module tb_codec_fixed;
  logic clk_in = 0;
  always #5 clk_in = ~clk_in;
  logic rst_in = 1;
  logic [63:0] enc_data_in = 0;
  logic [7:0] enc_control_in = 0;
  logic dec_data_valid_in = 0;
  logic [65:0] dec_data_in = 0;
  logic [65:0] enc_data_out;
  logic [63:0] dec_data_out;
  logic [7:0] dec_control_out;
  logic dec_sync_error, dec_error_out;
  top_64b66b_codec dut (.*);

  string vector_path;
  integer fd, fields, step;
  logic [65:0] pre_enc;
  logic [63:0] pre_data;
  logic [7:0] pre_control;
  logic pre_sync, pre_error;
  initial begin
    if (!$value$plusargs("VECTORS=%s", vector_path)) $fatal(1, "VECTORS missing");
    fd = $fopen(vector_path, "r");
    if (!fd) $fatal(1, "Cannot open vectors");
    step = 0;
    forever begin
      @(negedge clk_in);
      fields = $fscanf(fd, "%h %h %h %h %h\n", rst_in, enc_data_in,
                       enc_control_in, dec_data_valid_in, dec_data_in);
      if (fields == -1) begin
        $display("DRIVER_OK steps=%0d", step);
        $fclose(fd);
        $finish;
      end
      if (fields != 5) $fatal(1, "Malformed vector at step %0d", step);
      #1;
      pre_enc = enc_data_out;
      pre_data = dec_data_out;
      pre_control = dec_control_out;
      pre_sync = dec_sync_error;
      pre_error = dec_error_out;
      @(posedge clk_in);
      #1;
      $display("TRACE %h %h %h %h %h %h %h %h %h %h %h", step,
               pre_enc, pre_data, pre_control, pre_sync, pre_error,
               enc_data_out, dec_data_out, dec_control_out, dec_sync_error, dec_error_out);
      step++;
    end
  end
endmodule
