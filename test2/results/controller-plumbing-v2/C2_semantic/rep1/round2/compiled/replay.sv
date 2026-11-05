`timescale 1ns/1ps
module replay;
reg clk=0;
reg rst=0;
reg s_valid=0;
reg [7:0] s_data=0;
reg s_last=0;
reg m_ready=0;
reg h_ready=0;
reg s_ready=0;
reg [7:0] m_data=0;
reg m_valid=0;
reg m_last=0;
reg h_valid=0;
reg h_pad=0;
reg h_truncate=0;
reg [15:0] h_length=0;
reg [15:0] h_original_length=0;
wire [5:0] active,ok;
candidate_monitor monitor(.*);
string path;
integer fd,n;
integer cycle,v_rst,v_s_valid,v_s_data,v_s_last,v_m_ready,v_h_ready,pre_s_ready,pre_m_data,pre_m_valid,pre_m_last,pre_h_valid,pre_h_pad,pre_h_truncate,pre_h_length,pre_h_original_length,post_s_ready,post_m_data,post_m_valid,post_m_last,post_h_valid,post_h_pad,post_h_truncate,post_h_length,post_h_original_length;
initial begin
 if(!$value$plusargs("ROWS=%s",path)) $fatal(1,"Missing rows");
 fd=$fopen(path,"r");if(!fd) $fatal(1,"Missing file");
 while(!$feof(fd)) begin
  n=$fscanf(fd,"%h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h\n",cycle,v_rst,v_s_valid,v_s_data,v_s_last,v_m_ready,v_h_ready,pre_s_ready,pre_m_data,pre_m_valid,pre_m_last,pre_h_valid,pre_h_pad,pre_h_truncate,pre_h_length,pre_h_original_length,post_s_ready,post_m_data,post_m_valid,post_m_last,post_h_valid,post_h_pad,post_h_truncate,post_h_length,post_h_original_length);
  if(n==25) begin
rst=v_rst;
s_valid=v_s_valid;
s_data=v_s_data;
s_last=v_s_last;
m_ready=v_m_ready;
h_ready=v_h_ready;
s_ready=pre_s_ready;
m_data=pre_m_data;
m_valid=pre_m_valid;
m_last=pre_m_last;
h_valid=pre_h_valid;
h_pad=pre_h_pad;
h_truncate=pre_h_truncate;
h_length=pre_h_length;
h_original_length=pre_h_original_length;
   #4;if(cycle>0) $display("MON %0d pre %06b %06b",cycle,active,ok);
   #1;clk=1;#1;
s_ready=post_s_ready;
m_data=post_m_data;
m_valid=post_m_valid;
m_last=post_m_last;
h_valid=post_h_valid;
h_pad=post_h_pad;
h_truncate=post_h_truncate;
h_length=post_h_length;
h_original_length=post_h_original_length;
   #1;$display("MON %0d post %06b %06b",cycle,active,ok);
   #3;clk=0;
  end else if(n!=-1) $fatal(1,"Malformed rows");
 end
 $display("REPLAY_COMPLETE");$finish;
end
endmodule
