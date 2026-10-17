`timescale 1ns/1ps
module tb;
reg [7:0] data_in; reg [2:0] shift_bits; reg left_right; wire [7:0] data_out;
barrel_shifter dut(.*);
integer fd, n, a, b, c, count;
initial begin
  count=0; fd=$fopen("vectors.txt", "r");
  if (!fd) $fatal(1, "missing vectors");
  while (!$feof(fd)) begin
    n=$fscanf(fd, "%d %d %d\n", a,b,c);
    if (n==3) begin
      data_in=a; shift_bits=b; left_right=c; #2;
      $display("TRACE %0d %0d", count, data_out); count=count+1;
    end
  end
  $fclose(fd); $display("DONE %0d", count); $finish;
end
endmodule
