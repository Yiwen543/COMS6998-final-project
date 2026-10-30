`timescale 1ns/1ps
// Independently written behavioral queue control. Never used as the DUT in
// experimental B/C runs. Compile with SFIFO_FAULT_DATA for a single fault.
module sfifo #(
  parameter BW = 8,
  parameter LGFLEN = 3,
  parameter [0:0] OPT_ASYNC_READ = 1'b1,
  parameter [0:0] OPT_WRITE_ON_FULL = 1'b0,
  parameter [0:0] OPT_READ_ON_EMPTY = 1'b0
) (
  input wire i_clk, i_reset, i_wr,
  input wire [BW-1:0] i_data,
  output wire o_full,
  output reg [LGFLEN:0] o_fill,
  input wire i_rd,
  output wire [BW-1:0] o_data,
  output wire o_empty
);
  localparam DEPTH = 1 << LGFLEN;
  reg [BW-1:0] storage [0:DEPTH-1];
  reg [LGFLEN-1:0] head = 0, tail = 0;
  initial o_fill = 0;
  assign o_full = (o_fill == DEPTH);
  assign o_empty = (o_fill == 0);
`ifdef SFIFO_FAULT_DATA
  assign o_data = storage[head + 1'b1];
`else
  assign o_data = storage[head];
`endif
  wire accept_read = i_rd && !o_empty;
  wire accept_write = i_wr && !o_full;
`ifdef SFIFO_FAULT_ASYNC_RESET
  always @(posedge i_clk or posedge i_reset) begin
`else
  always @(posedge i_clk) begin
`endif
    if (i_reset) begin
      head <= 0;
      tail <= 0;
      o_fill <= 0;
    end else begin
      if (accept_read) head <= head + 1'b1;
      if (accept_write) begin
        storage[tail] <= i_data;
        tail <= tail + 1'b1;
      end
      case ({accept_write, accept_read})
        2'b01: o_fill <= o_fill - 1'b1;
        2'b10: o_fill <= o_fill + 1'b1;
        default: begin end
      endcase
    end
  end
endmodule
