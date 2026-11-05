`timescale 1ns/1ps
// Offer-per-cycle driver. Public ready only; no expected DUT outputs or internal drives.
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
reg [31:0] v_cmd_offer;
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
reg [31:0] v_tx_offer;
reg [31:0] v_rx_ready;
reg [31:0] v_sd;

localparam integer Capacity=392;
command_t incoming;
command_t cmd_mem [0:Capacity-1];
reg csid_mem [0:Capacity-1];
reg [31:0] tx_mem [0:Capacity-1];
reg [3:0] be_mem [0:Capacity-1];
integer cmd_ids [0:Capacity-1];
integer tx_ids [0:Capacity-1];
integer ch=0,ct=0,th=0,tt=0;
integer cmd_added,tx_added,cmd_taken,tx_taken;
integer cmd_offered=0,tx_offered=0,cmd_accepted=0,tx_accepted=0,cmd_cancelled=0,tx_cancelled=0;
reg cmd_fire,tx_fire;
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
got=$fscanf(fd,"%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n",v_rst_n,v_enable,v_sw_reset,v_cmd_offer,v_csid,v_speed,v_write,v_read,v_length,v_keep_cs,v_clkdiv,v_idle,v_lead,v_trail,v_full_cycle,v_cpha,v_cpol,v_tx_data,v_tx_be,v_tx_offer,v_rx_ready,v_sd);
if(got==22) begin

if(cycle>=Capacity) $fatal(1,"Physical cycle cap");
rst_ni=v_rst_n[0];en_i=v_enable[0];sw_rst_i=v_sw_reset[0];
rx_ready_i=v_rx_ready[0];sd_i=v_sd[3:0];
cmd_added=-1;tx_added=-1;cmd_taken=-1;tx_taken=-1;
if(!rst_ni) begin
  if(v_cmd_offer || v_tx_offer) $fatal(1,"Offer during reset");
  cmd_cancelled=cmd_cancelled+ct-ch;tx_cancelled=tx_cancelled+tt-th;
  ch=0;ct=0;th=0;tt=0;
  command_i='0;command_csid_i=0;tx_data_i=0;tx_be_i=0;
end else begin
  if(v_cmd_offer) begin
    if(ct>=Capacity) $fatal(1,"Command queue overflow");
incoming.segment.speed=v_speed[1:0];
incoming.segment.cmd_wr_en=v_write[0:0];
incoming.segment.cmd_rd_en=v_read[0:0];
incoming.segment.len=v_length[19:0];
incoming.segment.csaat=v_keep_cs[0:0];
incoming.configopts.clkdiv=v_clkdiv[15:0];
incoming.configopts.csnidle=v_idle[3:0];
incoming.configopts.csnlead=v_lead[3:0];
incoming.configopts.csntrail=v_trail[3:0];
incoming.configopts.full_cyc=v_full_cycle[0:0];
incoming.configopts.cpha=v_cpha[0:0];
incoming.configopts.cpol=v_cpol[0:0];

    cmd_mem[ct]=incoming;csid_mem[ct]=v_csid[0];cmd_ids[ct]=cycle;
    ct=ct+1;cmd_offered=cmd_offered+1;cmd_added=cycle;
  end
  if(v_tx_offer) begin
    if(tt>=Capacity) $fatal(1,"TX queue overflow");
    tx_mem[tt]=v_tx_data;be_mem[tt]=v_tx_be[3:0];tx_ids[tt]=cycle;
    tt=tt+1;tx_offered=tx_offered+1;tx_added=cycle;
  end
end
command_valid_i=(ct>ch);tx_valid_i=(tt>th);
if(command_valid_i) begin command_i=cmd_mem[ct-1];command_csid_i=csid_mem[ct-1];end
if(tx_valid_i) begin tx_data_i=tx_mem[th];tx_be_i=be_mem[th];end
#4;
cmd_fire=command_valid_i && command_ready_o;
tx_fire=tx_valid_i && tx_ready_o;
$write("TRACE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle,rst_ni,en_i,sw_rst_i,command_valid_i,command_csid_i,command_i.segment.speed,command_i.segment.cmd_wr_en,command_i.segment.cmd_rd_en,command_i.segment.len,command_i.segment.csaat,command_i.configopts.clkdiv,command_i.configopts.csnidle,command_i.configopts.csnlead,command_i.configopts.csntrail,command_i.configopts.full_cyc,command_i.configopts.cpha,command_i.configopts.cpol,tx_data_i,tx_be_i,tx_valid_i,rx_ready_i,sd_i,command_ready_o,tx_ready_o,tx_byte_select_full_o,rx_data_o,rx_valid_o,sck_o,csb_o,sd_o,sd_en_o,rx_stall_o,tx_stall_o,active_o);
#1;clk_i=1;#4;
$display(" %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",command_ready_o,tx_ready_o,tx_byte_select_full_o,rx_data_o,rx_valid_o,sck_o,csb_o,sd_o,sd_en_o,rx_stall_o,tx_stall_o,active_o);

if(cmd_fire) begin cmd_taken=cmd_ids[ch];ch=ch+1;cmd_accepted=cmd_accepted+1;end
if(tx_fire) begin tx_taken=tx_ids[th];th=th+1;tx_accepted=tx_accepted+1;end
if(cmd_offered!=cmd_accepted+cmd_cancelled+ct-ch) $fatal(1,"Command conservation");
if(tx_offered!=tx_accepted+tx_cancelled+tt-th) $fatal(1,"TX conservation");
$display("QUEUE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle,cmd_added,tx_added,cmd_taken,tx_taken,ct-ch,tt-th,cmd_offered,tx_offered,cmd_accepted,tx_accepted,cmd_cancelled,tx_cancelled);
#1;clk_i=0;cycle=cycle+1;
end else if(got!=-1) $fatal(1,"Malformed vectors");
end
$fclose(fd);$display("DRIVER_OK steps=%0d",cycle);$finish;
end
endmodule
