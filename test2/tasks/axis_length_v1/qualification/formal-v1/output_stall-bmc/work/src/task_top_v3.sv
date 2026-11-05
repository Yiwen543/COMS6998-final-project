`timescale 1ns/1ps
module frame_task(
input wire clk, rst,
input wire [7:0] s_data,
input wire s_valid, s_last,
output wire s_ready,
output wire [7:0] m_data,
output wire m_valid, m_last,
input wire m_ready,
output wire h_valid, h_pad, h_truncate,
output wire [15:0] h_length, h_original_length,
input wire h_ready);

axis_frame_length_adjust #(
    .DATA_WIDTH(8), .KEEP_ENABLE(0), .KEEP_WIDTH(1),
    .ID_ENABLE(0), .DEST_ENABLE(0), .USER_ENABLE(0)
) dut (
    .clk(clk), .rst(rst),
    .s_axis_tdata(s_data), .s_axis_tkeep(1'b1),
    .s_axis_tvalid(s_valid), .s_axis_tready(s_ready), .s_axis_tlast(s_last),
    .s_axis_tid(8'd0), .s_axis_tdest(8'd0), .s_axis_tuser(1'b0),
    .m_axis_tdata(m_data), .m_axis_tkeep(),
    .m_axis_tvalid(m_valid), .m_axis_tready(m_ready), .m_axis_tlast(m_last),
    .m_axis_tid(), .m_axis_tdest(), .m_axis_tuser(),
    .status_valid(h_valid), .status_ready(h_ready),
    .status_frame_pad(h_pad), .status_frame_truncate(h_truncate),
    .status_frame_length(h_length), .status_frame_original_length(h_original_length),
    .length_min(16'd4), .length_max(16'd8)
);
endmodule
