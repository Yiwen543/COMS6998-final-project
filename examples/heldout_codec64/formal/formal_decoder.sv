// Specification-derived narrow reference: a valid 66-bit decoder input with
// neither 01 nor 10 sync header must set the registered sync-error flag.
module formal_decoder (
  input logic clk_in, rst_in, decoder_data_valid_in,
  input logic [65:0] decoder_data_in
);
  wire [63:0] decoder_data_out;
  wire [7:0] decoder_control_out;
  wire sync_error, decoder_error_out;
  decoder_data_control_64b66b dut (
    .clk_in, .rst_in, .decoder_data_valid_in, .decoder_data_in,
    .decoder_data_out, .decoder_control_out, .sync_error, .decoder_error_out
  );

  reg prior_valid = 0;
  reg prior_invalid_header = 0;
  initial assume(rst_in);
  always @(posedge clk_in or posedge rst_in) begin
    if (rst_in) begin
      prior_valid <= 0;
      prior_invalid_header <= 0;
    end else begin
      prior_valid <= decoder_data_valid_in;
      prior_invalid_header <= decoder_data_in[65:64] != 2'b01 &&
                              decoder_data_in[65:64] != 2'b10;
    end
  end
  always @(posedge clk_in) begin
    if (!rst_in && prior_valid)
      assert(sync_error == prior_invalid_header);
    cover(!rst_in && prior_valid && prior_invalid_header && sync_error);
  end
endmodule
