`timescale 1ns/1ps
module formal_top(input wire clk);
  reg [2:0] cycle=3'd0;
  wire [3:0] a,b,q; wire rst,en,valid;
  (* keep *) wire active,ok;
  (* keep *) wire projected_trace_done=1'b0;
  stimulus st(cycle,a,b,rst,en,valid);
  control #(.ID(14)) u(clk,rst,en,valid,cycle,a,b,q,active,ok);
  (* keep *) reg [2:0] sampled_cycle=3'd0;
  (* keep *) reg [3:0] sampled_q=4'd0;
  (* keep *) reg sampled_active=1'b0, sampled_ok=1'b1;
  always @(posedge clk) begin
    if(cycle<3'd7) cycle<=cycle+3'd1;
    sampled_cycle<=cycle; sampled_q<=q;
    sampled_active<=active; sampled_ok<=ok;
    assert(!active || ok);
    cover(active);
  end
endmodule
