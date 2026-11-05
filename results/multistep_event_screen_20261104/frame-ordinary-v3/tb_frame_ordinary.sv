`timescale 1ns/1ps
module tb_frame_ordinary;
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

integer fd,nread,cycle,head,tail,accepted,pre_accept;
integer r_rst,r_offer,r_data,r_last,r_user,r_dr,r_hr;
reg [7:0] data_q[0:391]; reg last_q[0:391];reg user_q[0:391];
string vectors;
initial begin
clk=0;
rst=0;
s_axis_tdata=0;
s_axis_tkeep=0;
s_axis_tvalid=0;
s_axis_tlast=0;
s_axis_tid=0;
s_axis_tdest=0;
s_axis_tuser=0;
m_axis_hdr_ready=0;
m_axis_tready=0;
length_min=0;
length_max=0;
cycle=0;head=0;tail=0;accepted=0;
length_min=4;length_max=16;s_axis_tkeep=1;
if (!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"missing vectors");
fd=$fopen(vectors,"r"); if (!fd) $fatal(1,"cannot open vectors");
while (!$feof(fd)) begin
 nread=$fscanf(fd,"%d %d %d %d %d %d %d",r_rst,r_offer,r_data,r_last,r_user,r_dr,r_hr);
 if(nread==7) begin
  if(cycle>=392) $fatal(1,"cycle limit");
  rst=r_rst;m_axis_tready=r_dr;m_axis_hdr_ready=r_hr;
  if(rst) begin head=0;tail=0;end
  else if(r_offer) begin
   if(tail>=392) $fatal(1,"queue overflow");
   data_q[tail]=r_data;last_q[tail]=r_last;user_q[tail]=r_user;tail=tail+1;
  end
  s_axis_tvalid=(!rst && head<tail);
  s_axis_tdata=s_axis_tvalid?data_q[head]:0;
  s_axis_tlast=s_axis_tvalid?last_q[head]:0;
  s_axis_tuser=s_axis_tvalid?user_q[head]:0;
  #4;
  pre_accept=(!rst && s_axis_tvalid && s_axis_tready);
$display("PRE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d", cycle,rst,s_axis_tdata,s_axis_tkeep,s_axis_tvalid,s_axis_tlast,s_axis_tid,s_axis_tdest,s_axis_tuser,m_axis_hdr_ready,m_axis_tready,length_min,length_max,s_axis_tready,m_axis_hdr_valid,m_axis_hdr_pad,m_axis_hdr_truncate,m_axis_hdr_length,m_axis_hdr_original_length,m_axis_tdata,m_axis_tkeep,m_axis_tvalid,m_axis_tlast,m_axis_tid,m_axis_tdest,m_axis_tuser);
  #1;clk=1;#4;
$display("POST %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d", cycle,s_axis_tready,m_axis_hdr_valid,m_axis_hdr_pad,m_axis_hdr_truncate,m_axis_hdr_length,m_axis_hdr_original_length,m_axis_tdata,m_axis_tkeep,m_axis_tvalid,m_axis_tlast,m_axis_tid,m_axis_tdest,m_axis_tuser);
  #1;clk=0;
  if(pre_accept) begin head=head+1;accepted=accepted+1;end
  $display("QUEUE %0d %0d %0d %0d",cycle,head,tail,accepted);
  cycle=cycle+1;
 end else if(!$feof(fd)) $fatal(1,"bad vector");
end
$display("DRIVER_OK steps=%0d",cycle);$finish;
end
endmodule
