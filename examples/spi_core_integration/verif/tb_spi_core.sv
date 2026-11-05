`timescale 1ns/1ps
// Fixed public-input replay; no expected DUT outputs or hierarchical drives.
module tb_spi_core;
import spi_host_cmd_pkg::*;
logic clk_i=0;
command_t command_i;
logic rst_ni;
logic en_i;
logic sw_rst_i;
logic command_valid_i;
logic command_csid_i;
logic [31:0] tx_data_i;
logic [3:0] tx_be_i;
logic tx_valid_i;
logic rx_ready_i;
logic [3:0] sd_i;
wire command_ready_o;
wire tx_ready_o;
wire tx_byte_select_full_o;
wire [31:0] rx_data_o;
wire rx_valid_o;
wire sck_o;
wire [1:0] csb_o;
wire [3:0] sd_o;
wire [3:0] sd_en_o;
wire rx_stall_o;
wire tx_stall_o;
wire active_o;
spi_host_core #(.NumCS(2)) dut(.*);
integer fd,got,cycle;
string vector_path;
reg [31:0] v_rst_n;
reg [31:0] v_enable;
reg [31:0] v_sw_reset;
reg [31:0] v_valid;
reg [31:0] v_csid;
reg [31:0] v_speed;
reg [31:0] v_write;
reg [31:0] v_read;
reg [31:0] v_length;
reg [31:0] v_keep_cs;
reg [31:0] v_clkdiv;
reg [31:0] v_idle;
reg [31:0] v_lead;
reg [31:0] v_trail;
reg [31:0] v_full_cycle;
reg [31:0] v_cpha;
reg [31:0] v_cpol;
reg [31:0] v_tx_data;
reg [31:0] v_tx_be;
reg [31:0] v_tx_valid;
reg [31:0] v_rx_ready;
reg [31:0] v_sd;
initial begin
command_i=0;
rst_ni=1;
en_i=0;
sw_rst_i=0;
command_valid_i=0;
command_csid_i=0;
tx_data_i=0;
tx_be_i=0;
tx_valid_i=0;
rx_ready_i=0;
sd_i=0;
if (!$value$plusargs("VECTORS=%s",vector_path)) $fatal(1,"VECTORS missing");
fd=$fopen(vector_path,"r"); if(!fd) $fatal(1,"Cannot open vectors");
// Let the initial inactive reset settle before the first asserted-reset action.
// No clock edge or additional stimulus cycle is inserted here.
cycle=0; #1;
while(!$feof(fd)) begin
got=$fscanf(fd,"%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n",v_rst_n,v_enable,v_sw_reset,v_valid,v_csid,v_speed,v_write,v_read,v_length,v_keep_cs,v_clkdiv,v_idle,v_lead,v_trail,v_full_cycle,v_cpha,v_cpol,v_tx_data,v_tx_be,v_tx_valid,v_rx_ready,v_sd);
if(got==22) begin
rst_ni=v_rst_n[0:0];
en_i=v_enable[0:0];
sw_rst_i=v_sw_reset[0:0];
command_valid_i=v_valid[0:0];
command_csid_i=v_csid[0:0];
command_i.segment.speed=v_speed[1:0];
command_i.segment.cmd_wr_en=v_write[0:0];
command_i.segment.cmd_rd_en=v_read[0:0];
command_i.segment.len=v_length[19:0];
command_i.segment.csaat=v_keep_cs[0:0];
command_i.configopts.clkdiv=v_clkdiv[15:0];
command_i.configopts.csnidle=v_idle[3:0];
command_i.configopts.csnlead=v_lead[3:0];
command_i.configopts.csntrail=v_trail[3:0];
command_i.configopts.full_cyc=v_full_cycle[0:0];
command_i.configopts.cpha=v_cpha[0:0];
command_i.configopts.cpol=v_cpol[0:0];
tx_data_i=v_tx_data[31:0];
tx_be_i=v_tx_be[3:0];
tx_valid_i=v_tx_valid[0:0];
rx_ready_i=v_rx_ready[0:0];
sd_i=v_sd[3:0];
#4;
$write("TRACE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle,v_rst_n,v_enable,v_sw_reset,v_valid,v_csid,v_speed,v_write,v_read,v_length,v_keep_cs,v_clkdiv,v_idle,v_lead,v_trail,v_full_cycle,v_cpha,v_cpol,v_tx_data,v_tx_be,v_tx_valid,v_rx_ready,v_sd,command_ready_o,tx_ready_o,tx_byte_select_full_o,rx_data_o,rx_valid_o,sck_o,csb_o,sd_o,sd_en_o,rx_stall_o,tx_stall_o,active_o);
#1; clk_i=1; #4;
$display(" %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",command_ready_o,tx_ready_o,tx_byte_select_full_o,rx_data_o,rx_valid_o,sck_o,csb_o,sd_o,sd_en_o,rx_stall_o,tx_stall_o,active_o);
#1;clk_i=0;cycle=cycle+1;
end else if(got!=-1) $fatal(1,"Malformed vectors");
end
$fclose(fd);$display("DRIVER_OK steps=%0d",cycle);$finish;
end
endmodule
