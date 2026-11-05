`timescale 1ns/1ps
module tb_natural_inventory;
logic clk;
logic rst;
logic [15:0] s_axis_read_desc_addr;
logic [19:0] s_axis_read_desc_len;
logic [7:0] s_axis_read_desc_tag;
logic [7:0] s_axis_read_desc_id;
logic [7:0] s_axis_read_desc_dest;
logic s_axis_read_desc_user;
logic s_axis_read_desc_valid;
logic s_axis_read_desc_ready;
logic [7:0] m_axis_read_desc_status_tag;
logic [3:0] m_axis_read_desc_status_error;
logic m_axis_read_desc_status_valid;
logic [31:0] m_axis_read_data_tdata;
logic [3:0] m_axis_read_data_tkeep;
logic m_axis_read_data_tvalid;
logic m_axis_read_data_tready;
logic m_axis_read_data_tlast;
logic [7:0] m_axis_read_data_tid;
logic [7:0] m_axis_read_data_tdest;
logic m_axis_read_data_tuser;
logic [7:0] m_axi_arid;
logic [15:0] m_axi_araddr;
logic [7:0] m_axi_arlen;
logic [2:0] m_axi_arsize;
logic [1:0] m_axi_arburst;
logic m_axi_arlock;
logic [3:0] m_axi_arcache;
logic [2:0] m_axi_arprot;
logic m_axi_arvalid;
logic m_axi_arready;
logic [7:0] m_axi_rid;
logic [31:0] m_axi_rdata;
logic [1:0] m_axi_rresp;
logic m_axi_rlast;
logic m_axi_rvalid;
logic m_axi_rready;
logic enable;
axi_dma_rd #(.ENABLE_UNALIGNED(1)) dut(.*);
initial begin
clk='0;
rst='0;
s_axis_read_desc_addr='0;
s_axis_read_desc_len='0;
s_axis_read_desc_tag='0;
s_axis_read_desc_id='0;
s_axis_read_desc_dest='0;
s_axis_read_desc_user='0;
s_axis_read_desc_valid='0;
m_axis_read_data_tready='0;
m_axi_arready='0;
m_axi_rid='0;
m_axi_rdata='0;
m_axi_rresp='0;
m_axi_rlast='0;
m_axi_rvalid='0;
enable='0;
rst=1;
for(integer i=0;i<8;i=i+1) begin
clk=0; if(i==2) rst=0; #5; clk=1; #5;
end
$display("INVENTORY_OK cycles=8"); $finish;
end
endmodule
