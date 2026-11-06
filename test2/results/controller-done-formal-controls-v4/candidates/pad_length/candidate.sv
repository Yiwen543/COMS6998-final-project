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
assign active={5'b00000,(h_valid && !rst)};assign ok={5'b11111,(!h_pad || h_length==16'd4)};
endmodule
`default_nettype wire
