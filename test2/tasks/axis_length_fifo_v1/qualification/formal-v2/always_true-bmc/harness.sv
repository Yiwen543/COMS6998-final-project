module formal_top(input wire clk);
(* anyseq *) reg rst,s_valid,s_last,m_ready,h_ready;
(* anyseq *) reg [7:0] s_data;
wire s_ready,m_valid,m_last,h_valid,h_pad,h_truncate;
wire [7:0] m_data;wire [15:0] h_length,h_original_length;
frame_task dut(.*);
reg past=0;
always @(posedge clk) begin
 if(!past) assume(rst);
 assume(!rst || !s_valid);
 if(past && !$past(rst) && $past(s_valid && !s_ready) && !rst)
  assume(s_valid && s_data==$past(s_data) && s_last==$past(s_last));
 past<=1;
 if(past) assert(1);
 cover(past);
end
endmodule
