`timescale 1ns/1ps
module replay;
reg i_clk=0;
always #5 i_clk=~i_clk;
reg i_reset=0,i_wr=0,i_rd=0,o_full=0,o_empty=1;
reg [7:0] i_data=0,o_data=0;
reg [4:0] o_fill=0;
wire [5:0] active,ok;
candidate_monitor monitor(.*);
string path;
integer fd,n,cycle,r,w,d,data,pf,pfull,pe,pdata,qf,qfull,qe,qdata;
initial begin
  if (!$value$plusargs("ROWS=%s",path)) $fatal(1,"Missing rows");
  fd=$fopen(path,"r");
  if(fd==0) $fatal(1,"Missing rows file");
  while (!$feof(fd)) begin
    n=$fscanf(fd,"%h %h %h %h %h %h %h %h %h %h %h %h %h\n",
      cycle,r,w,d,data,pf,pfull,pe,pdata,qf,qfull,qe,qdata);
    if(n==13) begin
      @(negedge i_clk);
      i_reset=r[0];i_wr=w[0];i_rd=d[0];i_data=data[7:0];
      o_fill=pf[4:0];o_full=pfull[0];o_empty=pe[0];o_data=pdata[7:0];
      #1;
      if(cycle>0) $display("MON %0d pre %06b %06b",cycle,active,ok);
      @(posedge i_clk);
      #1;o_fill=qf[4:0];o_full=qfull[0];o_empty=qe[0];o_data=qdata[7:0];
      #1;$display("MON %0d post %06b %06b",cycle,active,ok);
    end else if(n!=-1) $fatal(1,"Malformed rows");
  end
  $fclose(fd);$display("REPLAY_COMPLETE");$finish;
end
endmodule
