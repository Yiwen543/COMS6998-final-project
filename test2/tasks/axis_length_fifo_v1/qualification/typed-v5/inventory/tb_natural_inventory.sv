`timescale 1ns/1ps
module tb_natural_inventory;
logic clk;
logic rst;
logic [7:0] s_data;
logic s_valid;
logic s_last;
logic s_ready;
logic [7:0] m_data;
logic m_valid;
logic m_last;
logic m_ready;
logic h_valid;
logic h_pad;
logic h_truncate;
logic [15:0] h_length;
logic [15:0] h_original_length;
logic h_ready;
frame_task dut(.*);
initial begin
clk=1'd0;
rst=1'd0;
s_data=8'd0;
s_valid=1'd0;
s_last=1'd0;
m_ready=1'd1;
h_ready=1'd1;
rst=1;
for(integer i=0;i<8;i=i+1) begin
clk=0; if(i==2) rst=0; #5; clk=1; #5;
end
$display("INVENTORY_OK cycles=8"); $finish;
end
endmodule
