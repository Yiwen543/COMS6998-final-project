`timescale 1ns/1ps
module tb_natural_inventory;
logic i_clk;
logic i_reset;
logic [1:0] i_mcyc;
logic [1:0] i_mstb;
logic [1:0] i_mwe;
logic [15:0] i_maddr;
logic [63:0] i_mdata;
logic [7:0] i_msel;
logic [1:0] o_mstall;
logic [1:0] o_mack;
logic [63:0] o_mdata;
logic [1:0] o_merr;
logic [1:0] o_scyc;
logic [1:0] o_sstb;
logic [1:0] o_swe;
logic [15:0] o_saddr;
logic [63:0] o_sdata;
logic [7:0] o_ssel;
logic [1:0] i_sstall;
logic [1:0] i_sack;
logic [63:0] i_sdata;
logic [1:0] i_serr;
logic r_rst;
logic [1:0] r_offer;
logic [15:0] r_addr;
logic [63:0] r_data;
logic [1:0] r_we;
logic [7:0] r_sel;
logic [1:0] r_slave_error;
wbxbar #(.NM(2),.NS(2),.AW(8),.DW(32),.SLAVE_ADDR(4096),.SLAVE_MASK(61680),.LGMAXBURST(3),.OPT_TIMEOUT(16),.OPT_STARVATION_TIMEOUT(1),.OPT_DBLBUFFER(1),.OPT_LOWPOWER(1)) dut(.*);

integer cooldown[0:1];
integer fd,nread,cycle,m,head[0:1],tail[0:1],pending[0:1],accepted[0:1],returned[0:1];
reg [7:0] addrq[0:1][0:391];reg [31:0] dataq[0:1][0:391];reg weq[0:1][0:391];reg [3:0] selq[0:1][0:391];
reg [1:0] previous_slave,pre_master,pre_response,pre_slave,pre_error;reg [63:0] response_data;string vectors;
initial begin
i_clk=0;
i_reset=0;
i_mcyc=0;
i_mstb=0;
i_mwe=0;
i_maddr=0;
i_mdata=0;
i_msel=0;
i_sstall=0;
i_sack=0;
i_sdata=0;
i_serr=0;
cycle=0;previous_slave=0;response_data=0;
for(m=0;m<2;m=m+1) begin head[m]=0;tail[m]=0;pending[m]=0;accepted[m]=0;returned[m]=0;cooldown[m]=0;end
if(!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"missing vectors");
fd=$fopen(vectors,"r");if(!fd) $fatal(1,"cannot open vectors");
while(!$feof(fd)) begin
 nread=$fscanf(fd,"%h %h %h %h %h %h %h",r_rst,r_offer,r_addr,r_data,r_we,r_sel,r_slave_error);
 if(nread==7) begin
  if(cycle>=392) $fatal(1,"cycle limit");
  i_reset=r_rst;i_mcyc=0;i_mstb=0;i_maddr=0;i_mdata=0;i_mwe=0;i_msel=0;i_sstall=0;
  for(m=0;m<2;m=m+1) begin
   if(r_rst) begin head[m]=0;tail[m]=0;pending[m]=0;accepted[m]=0;returned[m]=0;cooldown[m]=0;end
   else if(r_offer[m]) begin
    if(tail[m]>=392) $fatal(1,"queue overflow");
    addrq[m][tail[m]]=r_addr[m*8+:8];dataq[m][tail[m]]=r_data[m*32+:32];weq[m][tail[m]]=r_we[m];selq[m][tail[m]]=r_sel[m*4+:4];tail[m]=tail[m]+1;
   end
   i_mcyc[m]=!r_rst && cooldown[m]==0 && (head[m]<tail[m] || pending[m]>0);
   i_mstb[m]=!r_rst && cooldown[m]==0 && head[m]<tail[m];
   if(i_mstb[m]) begin i_maddr[m*8+:8]=addrq[m][head[m]];i_mdata[m*32+:32]=dataq[m][head[m]];i_mwe[m]=weq[m][head[m]];i_msel[m*4+:4]=selq[m][head[m]];end
  end
  for(m=0;m<2;m=m+1) if(cooldown[m]>0) cooldown[m]=cooldown[m]-1;
  if(r_rst) begin previous_slave=0;response_data=0;end
  i_sack=previous_slave & ~r_slave_error & o_scyc & {2{!r_rst}};
  i_serr=previous_slave & r_slave_error & o_scyc & {2{!r_rst}};
  i_sdata=response_data;
  #4;
  pre_master=i_mcyc & i_mstb & ~o_mstall;
  pre_response=i_mcyc & (o_mack | o_merr);pre_error=i_mcyc & o_merr;
  pre_slave=o_scyc & o_sstb & ~i_sstall & {2{!r_rst}};
$display("PRE %0d %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h",cycle,i_reset,i_mcyc,i_mstb,i_mwe,i_maddr,i_mdata,i_msel,i_sstall,i_sack,i_sdata,i_serr,o_mstall,o_mack,o_mdata,o_merr,o_scyc,o_sstb,o_swe,o_saddr,o_sdata,o_ssel);
  for(m=0;m<2;m=m+1) response_data[m*32+:32]=32'ha55a0000 | {24'd0,o_saddr[m*8+:8]};
  #1;i_clk=1;#4;
$display("POST %0d %h %h %h %h %h %h %h %h %h %h",cycle,o_mstall,o_mack,o_mdata,o_merr,o_scyc,o_sstb,o_swe,o_saddr,o_sdata,o_ssel);
  #1;i_clk=0;
  for(m=0;m<2;m=m+1) begin
   if(pre_master[m]) begin head[m]=head[m]+1;accepted[m]=accepted[m]+1;end
   if(pre_response[m]) returned[m]=returned[m]+1;
   pending[m]=pending[m]+(pre_master[m]?1:0)-(pre_response[m]?1:0);
   if(pending[m]<0) begin $display("DUT_DIAGNOSTIC orphan_response cycle=%0d master=%0d",cycle,m);pending[m]=0;end
   if(pre_error[m]) begin pending[m]=0;cooldown[m]=1;end
   $display("QUEUE %0d %0d %0d %0d %0d %0d %0d",cycle,m,head[m],tail[m],pending[m],accepted[m],returned[m]);
  end
  previous_slave=pre_slave;cycle=cycle+1;
 end else if(!$feof(fd)) $fatal(1,"bad vector");
end
for(m=0;m<2;m=m+1) $display("PENDING %0d %0d %0d",m,tail[m]-head[m],pending[m]);
$display("DRIVER_OK steps=%0d",cycle);$finish;
end
endmodule
