`timescale 1ns/1ps
module tb_natural_inventory;
reg clk=0,rst=0,s_valid=0,s_last=0,m_ready=1,h_ready=1;
reg [7:0] s_data=0;
wire s_ready,m_valid,m_last,h_valid,h_pad,h_truncate;
wire [7:0] m_data;
wire [15:0] h_length,h_original_length;
frame_task dut(.*);
integer fd,n,cycle=0,head=0,tail=0,take,r,o,d,l,m,h;
reg [7:0] data_q[0:511];reg last_q[0:511];
string path;
initial begin
 if(!$value$plusargs("VECTORS=%s",path)) $fatal(1,"missing vectors");
 fd=$fopen(path,"r");if(!fd) $fatal(1,"missing file");
 while(!$feof(fd)) begin
  n=$fscanf(fd,"%d %d %d %d %d %d",r,o,d,l,m,h);
  if(n==6) begin
   if(cycle>=512) $fatal(1,"cycle cap");
   rst=r;m_ready=m;h_ready=h;
   if(rst) begin head=0;tail=0;end
   else if(o) begin data_q[tail]=d;last_q[tail]=l;tail=tail+1;end
   s_valid=(!rst && head<tail);s_data=s_valid?data_q[head]:0;s_last=s_valid?last_q[head]:0;
   #4;take=(!rst && s_valid && s_ready);
   $display("PRE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle,rst,s_valid,s_data,s_last,m_ready,h_ready,s_ready,m_data,m_valid,m_last,h_valid,h_pad,h_truncate,h_length,h_original_length);
   #1;clk=1;#4;
   $display("POST %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle,s_ready,m_data,m_valid,m_last,h_valid,h_pad,h_truncate,h_length,h_original_length);
   #1;clk=0;if(take) head=head+1;
   $display("QUEUE %0d %0d %0d",cycle,head,tail);cycle=cycle+1;
  end else if(!$feof(fd)) $fatal(1,"malformed vector");
 end
 $display("DRIVER_COMPLETE %0d",cycle);$finish;
end
endmodule
