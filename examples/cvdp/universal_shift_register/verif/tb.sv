`timescale 1ns/1ps
module tb;
reg clk, rst; reg [1:0] mode_sel; reg shift_dir,serial_in; reg [7:0] parallel_in;
wire [7:0] q; wire serial_out;
universal_shift_register dut(.*);
integer fd,n,a,b,c,d,e,count;
initial begin
  clk=0; rst=0; mode_sel=0; shift_dir=0; serial_in=0; parallel_in=0;
  count=0; fd=$fopen("vectors.txt", "r");
  if (!fd) $fatal(1, "missing vectors");
  while (!$feof(fd)) begin
    n=$fscanf(fd, "%d %d %d %d %d\n",a,b,c,d,e);
    if(n==5) begin
      clk=0; rst=a; mode_sel=b; shift_dir=c; serial_in=d; parallel_in=e;
      #2; clk=1; #2;
      $display("TRACE %0d %0d %0d",count,q,serial_out); count=count+1;
      clk=0; #2;
    end
  end
  $fclose(fd); $display("DONE %0d",count); $finish;
end
endmodule
