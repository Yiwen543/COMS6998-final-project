`default_nettype none
module candidate_monitor(
input wire clk,
input wire rst,
input wire s_valid,
input wire [7:0] s_data,
input wire s_last,
input wire m_ready,
input wire h_ready,
input wire s_ready,
input wire [7:0] m_data,
input wire m_valid,
input wire m_last,
input wire h_valid,
input wire h_pad,
input wire h_truncate,
input wire [15:0] h_length,
input wire [15:0] h_original_length,
input wire trace_done,
output wire [5:0] active,ok);
reg [15:0] offered, data_frames, status_frames;
always @(posedge clk) begin
 if (rst) begin offered<=0;data_frames<=0;status_frames<=0;end
 else begin
  if(s_valid && s_ready && s_last) offered<=offered+16'd1;
  if(m_valid && m_ready && m_last) data_frames<=data_frames+16'd1;
  if(h_valid && h_ready) status_frames<=status_frames+16'd1;
 end
end
assign active={3'b000,{3{trace_done}}};
assign ok={3'b111,(status_frames>=offered),(data_frames>=offered),(!s_valid)};
endmodule
`default_nettype wire
