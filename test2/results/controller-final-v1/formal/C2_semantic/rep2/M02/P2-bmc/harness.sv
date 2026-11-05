module formal_top(input wire clk);
(* anyseq *) reg rst,s_valid,s_last,m_ready,h_ready;
(* anyseq *) reg [7:0] s_data;
(* keep *) wire s_ready,m_valid,m_last,h_valid,h_pad,h_truncate;
(* keep *) wire [7:0] m_data;
(* keep *) wire [15:0] h_length,h_original_length;
wire [5:0] active,ok;
frame_task dut(.*);
candidate_monitor monitor(.*);
reg past=0;
reg [3:0] frame_bytes=0;
always @(posedge clk) begin
 if(!past) assume(rst);
 assume(!rst || !s_valid);
 if(past && !$past(rst) && $past(s_valid && !s_ready) && !rst)
  assume(s_valid && s_data==$past(s_data) && s_last==$past(s_last));
 if(rst) frame_bytes<=0;
 else if(s_valid && s_ready) begin
  assume(frame_bytes<11 || s_last);
  if(s_last) frame_bytes<=0; else frame_bytes<=frame_bytes+1;
 end
 past<=1;
 if(past) begin
  assert(!active[2] || ok[2]);
  cover(active[2]);
 end
end
endmodule
