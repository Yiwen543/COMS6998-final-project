`timescale 1ns/1ps
module tb;
reg [7:0] input_char; reg [3:0] key; wire [7:0] output_char;
caesar_cipher dut(.*);
integer fd,n,a,b,count;
initial begin
  count=0; fd=$fopen("vectors.txt", "r");
  if (!fd) $fatal(1, "missing vectors");
  while (!$feof(fd)) begin
    n=$fscanf(fd, "%d %d\n",a,b);
    if(n==2) begin
      input_char=a; key=b; #2;
      $display("TRACE %0d %0d",count,output_char); count=count+1;
    end
  end
  $fclose(fd); $display("DONE %0d",count); $finish;
end
endmodule
