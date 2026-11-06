`timescale 1ns/1ps
module physical_tb;
  reg clk=1'b0;
  reg [2:0] step=3'd7;
  wire [3:0] a,b; wire rst,en,valid;
  wire [3:0] q[0:15]; wire active[0:15],ok[0:15];
  integer qc,k; reg marker=1'b0,obs_phase=1'b0;
  reg [2047:0] trace_file;
  stimulus st(step,a,b,rst,en,valid);
  generate genvar g; for(g=0;g<16;g=g+1) begin: units
    control #(.ID(g)) u(clk,rst,en,valid,step,a,b,q[g],active[g],ok[g]);
  end endgenerate
  initial begin
    if(!$value$plusargs("QC=%d",qc)) $fatal(1,"missing QC");
    if(qc<0 || qc>15) $fatal(1,"bad QC");
    if(!$value$plusargs("TRACE=%s",trace_file)) $fatal(1,"missing TRACE");
    $dumpfile(trace_file); $dumpvars(0,physical_tb);
    // Establish step0 after time-zero processes are active, before pre1000ps.
    #0.001; // 1ps startup, no clock edge
    for(k=0;k<4;k=k+1) begin
      step=k[2:0]; marker=1'b0; obs_phase=1'b0;
      if(k==0) #0.999; else #1; // first pre stays at1000ps
      $display("OBS qc=%0d cycle=%0d phase=pre tick=%0t q=%b active=%b ok=%b marker=%b a=%b b=%b rst=%b en=%b valid=%b",qc,k,$time,q[qc],active[qc],ok[qc],marker,a,b,rst,en,valid);
      #1 clk=1'b1;
      #1; obs_phase=1'b1; if(qc==14 && k==3) marker=1'b1;
      $display("OBS qc=%0d cycle=%0d phase=post tick=%0t q=%b active=%b ok=%b marker=%b a=%b b=%b rst=%b en=%b valid=%b",qc,k,$time,q[qc],active[qc],ok[qc],marker,a,b,rst,en,valid);
      #1 clk=1'b0;
    end
    $display("END qc=%0d cycles=4 posedges=4",qc); $finish;
  end
endmodule
