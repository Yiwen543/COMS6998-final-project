`timescale 1ns/1ps
module literal_replay;
reg clk=0;
reg rst=0;
reg s_valid=0;
reg [7:0] s_data=0;
reg s_last=0;
reg m_ready=0;
reg h_ready=0;
wire s_ready;
wire [7:0] m_data;
wire m_valid;
wire m_last;
wire h_valid;
wire h_pad;
wire h_truncate;
wire [15:0] h_length;
wire [15:0] h_original_length;
frame_task dut(.*);
string path;integer fd,n,cycle=0;
integer v_rst,v_s_valid,v_s_data,v_s_last,v_m_ready,v_h_ready;
initial begin
 if(!$value$plusargs("INPUTS=%s",path)) $fatal(1,"Missing inputs");
 fd=$fopen(path,"r");if(!fd) $fatal(1,"Missing file");
 while(!$feof(fd)) begin
  n=$fscanf(fd,"%d %d %d %d %d %d\n",v_rst,v_s_valid,v_s_data,v_s_last,v_m_ready,v_h_ready);
  if(n==6) begin
rst=v_rst;
s_valid=v_s_valid;
s_data=v_s_data;
s_last=v_s_last;
m_ready=v_m_ready;
h_ready=v_h_ready;
   #4;$display("PRE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle,rst,s_valid,s_data,s_last,m_ready,h_ready,s_ready,m_data,m_valid,m_last,h_valid,h_pad,h_truncate,h_length,h_original_length);
   #1;clk=1;#2;
   $display("POST %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle,s_ready,m_data,m_valid,m_last,h_valid,h_pad,h_truncate,h_length,h_original_length);
   #3;clk=0;cycle=cycle+1;
  end else if(n!=-1) $fatal(1,"Malformed inputs");
 end
 $display("LITERAL_COMPLETE %0d",cycle);$finish;
end
endmodule
