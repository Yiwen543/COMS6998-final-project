`timescale 1ns/1ps
module tb_queue_preflight;
  logic clk_i = 0;
  logic rst_ni = 1;
  logic clr_i = 0, ena_i = 0, we_i = 0, re_i = 0;
  logic [31:0] d_i = 0;
  wire [31:0] q_original, q_variant;
  wire empty_original, full_original, ae_original, af_original;
  wire empty_variant, full_variant, ae_variant, af_variant;

  queue dut (.rst_ni, .clk_i, .clr_i, .ena_i, .we_i, .d_i, .re_i,
             .q_o(q_original), .empty_o(empty_original), .full_o(full_original),
             .almost_empty_o(ae_original), .almost_full_o(af_original));
  queue_variant variant (.rst_ni, .clk_i, .clr_i, .ena_i, .we_i, .d_i, .re_i,
                         .q_o(q_variant), .empty_o(empty_variant), .full_o(full_variant),
                         .almost_empty_o(ae_variant), .almost_full_o(af_variant));
  always #5 clk_i = ~clk_i;

  initial begin
    // Fixed, deliberately incomplete seed. No read/write or clear is asserted.
    #1 rst_ni = 0;
    #1;
    if ({q_original, empty_original, full_original, ae_original, af_original}
        !== {q_variant, empty_variant, full_variant, ae_variant, af_variant})
      $fatal(1, "queue variant differs on asynchronous reset assertion");
    if ({q_original, empty_original, full_original, ae_original, af_original}
        !== {32'b0, 1'b1, 1'b0, 1'b1, 1'b0})
      $fatal(1, "queue asynchronous reset did not establish specified outputs");
    repeat (2) @(negedge clk_i);
    rst_ni = 1;
    repeat (4) begin
      @(posedge clk_i);
      #1;
      if ({q_original, empty_original, full_original, ae_original, af_original}
          !== {q_variant, empty_variant, full_variant, ae_variant, af_variant})
        $fatal(1, "queue variant differs under preflight seed");
    end
    if ($test$plusargs("REACHABILITY")) begin
      // Separate validation run; these actions are never part of the model seed.
      @(negedge clk_i);
      ena_i = 1; we_i = 1; re_i = 0; d_i = 32'hA5A55A5A;
      @(posedge clk_i);
      #1;
      if ({q_original, empty_original, full_original, ae_original, af_original}
          !== {q_variant, empty_variant, full_variant, ae_variant, af_variant})
        $fatal(1, "queue variant differs after write");
      @(negedge clk_i);
      we_i = 0; re_i = 1;
      @(posedge clk_i);
      #1;
      if ({q_original, empty_original, full_original, ae_original, af_original}
          !== {q_variant, empty_variant, full_variant, ae_variant, af_variant})
        $fatal(1, "queue variant differs after read");
      $display("REACHABILITY_OK extra_cycles=2");
    end
    $display("PREFLIGHT_OK cycles=6 reset=async active-low seed=idle-only");
    $finish;
  end
endmodule
