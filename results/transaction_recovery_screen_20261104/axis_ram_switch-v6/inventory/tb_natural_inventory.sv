`timescale 1ns/1ps
module tb_natural_inventory;
logic clk;
logic rst;
logic [15:0] s_axis_tdata;
logic [1:0] s_axis_tkeep;
logic [1:0] s_axis_tvalid;
logic [1:0] s_axis_tready;
logic [1:0] s_axis_tlast;
logic [3:0] s_axis_tid;
logic [3:0] s_axis_tdest;
logic [1:0] s_axis_tuser;
logic [15:0] m_axis_tdata;
logic [1:0] m_axis_tkeep;
logic [1:0] m_axis_tvalid;
logic [1:0] m_axis_tready;
logic [1:0] m_axis_tlast;
logic [5:0] m_axis_tid;
logic [1:0] m_axis_tdest;
logic [1:0] m_axis_tuser;
logic [1:0] status_overflow;
logic [1:0] status_bad_frame;
logic [1:0] status_good_frame;
axis_ram_switch #(.S_COUNT(2),.M_COUNT(2),.S_DATA_WIDTH(8),.M_DATA_WIDTH(8),.S_KEEP_ENABLE(0),.M_KEEP_ENABLE(0),.S_KEEP_WIDTH(1),.M_KEEP_WIDTH(1),.S_ID_WIDTH(2),.M_ID_WIDTH(3),.M_DEST_WIDTH(1),.S_DEST_WIDTH(2),.ID_ENABLE(1),.UPDATE_TID(1),.FIFO_DEPTH(32),.CMD_FIFO_DEPTH(4),.SPEEDUP(1),.DROP_BAD_FRAME(1),.DROP_WHEN_FULL(0),.ARB_TYPE_ROUND_ROBIN(1),.RAM_PIPELINE(2)) dut(.*);
initial begin
clk=1'd0;
rst=1'd0;
s_axis_tdata=16'd0;
s_axis_tkeep=2'd0;
s_axis_tvalid=2'd0;
s_axis_tlast=2'd0;
s_axis_tid=4'd0;
s_axis_tdest=4'd0;
s_axis_tuser=2'd0;
m_axis_tready=2'd3;
rst=1;
for(integer i=0;i<8;i=i+1) begin
clk=0; if(i==2) rst=0; #5; clk=1; #5;
end
$display("INVENTORY_OK cycles=8"); $finish;
end
endmodule
