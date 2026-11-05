module formal_top(input wire i_clk);
(* anyseq *) reg i_reset, i_wr, i_rd;
(* anyseq *) reg [7:0] i_data;
wire [7:0] o_data; wire [4:0] o_fill; wire o_full,o_empty;
wire [5:0] active,ok;
sfifo #(.BW(8),.LGFLEN(4),.OPT_ASYNC_READ(1),.OPT_WRITE_ON_FULL(0),.OPT_READ_ON_EMPTY(0)) dut(.*);
candidate_monitor monitor(.*);
reg initialized=0;
always @(posedge i_clk) begin
  if(!initialized) assume(i_reset);
  assume(!i_reset || (!i_wr && !i_rd));
  initialized<=1;
  if(initialized) begin
    assert((active & ~ok)==0);
    cover(active[0]);cover(active[1]);cover(active[2]);
    cover(active[3]);cover(active[4]);cover(active[5]);
  end
end
endmodule
