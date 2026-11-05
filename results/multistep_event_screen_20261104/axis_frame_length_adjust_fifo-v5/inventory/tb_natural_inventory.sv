`timescale 1ns/1ps
module tb_natural_inventory;
logic clk;
logic rst;
logic [7:0] s_axis_tdata;
logic s_axis_tkeep;
logic s_axis_tvalid;
logic s_axis_tready;
logic s_axis_tlast;
logic [7:0] s_axis_tid;
logic [7:0] s_axis_tdest;
logic s_axis_tuser;
logic m_axis_hdr_valid;
logic m_axis_hdr_ready;
logic m_axis_hdr_pad;
logic m_axis_hdr_truncate;
logic [15:0] m_axis_hdr_length;
logic [15:0] m_axis_hdr_original_length;
logic [7:0] m_axis_tdata;
logic m_axis_tkeep;
logic m_axis_tvalid;
logic m_axis_tready;
logic m_axis_tlast;
logic [7:0] m_axis_tid;
logic [7:0] m_axis_tdest;
logic m_axis_tuser;
logic [15:0] length_min;
logic [15:0] length_max;
axis_frame_length_adjust_fifo #(.DATA_WIDTH(8),.KEEP_ENABLE(0),.KEEP_WIDTH(1),.ID_ENABLE(0),.ID_WIDTH(8),.DEST_ENABLE(0),.DEST_WIDTH(8),.USER_ENABLE(1),.USER_WIDTH(1),.FRAME_FIFO_DEPTH(32),.HEADER_FIFO_DEPTH(8)) dut(.*);
initial begin
clk=1'd0;
rst=1'd0;
s_axis_tdata=8'd0;
s_axis_tkeep=1'd0;
s_axis_tvalid=1'd0;
s_axis_tlast=1'd0;
s_axis_tid=8'd0;
s_axis_tdest=8'd0;
s_axis_tuser=1'd0;
m_axis_hdr_ready=1'd1;
m_axis_tready=1'd1;
length_min=16'd4;
length_max=16'd16;
rst=1;
for(integer i=0;i<8;i=i+1) begin
clk=0; if(i==2) rst=0; #5; clk=1; #5;
end
$display("INVENTORY_OK cycles=8"); $finish;
end
endmodule
