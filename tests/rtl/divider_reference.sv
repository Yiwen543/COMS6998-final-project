`timescale 1ns/1ps
// Behavioral arithmetic control, independent of the iterative DUT algorithm.
// Compile with DIVIDER_FAULT_REMAINDER for a single arithmetic fault.
module radix2_div (
  input wire clk, rst_n, start,
  input wire [7:0] dividend, divisor,
  output reg [7:0] quotient = 0, remainder = 0,
  output reg done = 0
);
  reg busy = 0;
  reg [3:0] remaining = 0;
  reg [7:0] saved_dividend = 0, saved_divisor = 1;
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      quotient <= 0;
      remainder <= 0;
      done <= 0;
      busy <= 0;
      remaining <= 0;
    end else begin
      done <= 0;
      if (start && !busy) begin
        if (divisor == 0) begin
          quotient <= 8'hff;
          remainder <= 8'hff;
          done <= 1;
        end else begin
          saved_dividend <= dividend;
          saved_divisor <= divisor;
          quotient <= 0;
          busy <= 1;
          remaining <= 8;
        end
      end else if (busy) begin
        if (remaining == 1) begin
          quotient <= saved_dividend / saved_divisor;
`ifdef DIVIDER_FAULT_REMAINDER
          remainder <= (saved_dividend % saved_divisor) + 1'b1;
`else
          remainder <= saved_dividend % saved_divisor;
`endif
          done <= 1;
          busy <= 0;
        end
        remaining <= remaining - 1'b1;
      end
    end
  end
endmodule
