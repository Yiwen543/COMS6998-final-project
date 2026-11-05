`timescale 1ns/1ps
module tb_natural_inventory;
logic clk_i;
logic rst_ni;
logic [55:0] command_i;
logic command_csid_i;
logic command_valid_i;
logic command_ready_o;
logic en_i;
logic [31:0] tx_data_i;
logic [3:0] tx_be_i;
logic tx_valid_i;
logic tx_ready_o;
logic tx_byte_select_full_o;
logic [31:0] rx_data_o;
logic rx_valid_o;
logic rx_ready_i;
logic sw_rst_i;
logic sck_o;
logic [1:0] csb_o;
logic [3:0] sd_o;
logic [3:0] sd_en_o;
logic [3:0] sd_i;
logic rx_stall_o;
logic tx_stall_o;
logic active_o;
spi_host_core #(.NumCS(2)) dut(.*);
initial begin
clk_i=1'd0;
rst_ni=1'd0;
command_i=56'd0;
command_csid_i=1'd0;
command_valid_i=1'd0;
en_i=1'd0;
tx_data_i=32'd0;
tx_be_i=4'd0;
tx_valid_i=1'd0;
rx_ready_i=1'd0;
sw_rst_i=1'd0;
sd_i=4'd0;
rst_ni=0;
for(integer i=0;i<8;i=i+1) begin
clk_i=0; if(i==2) rst_ni=1; #5; clk_i=1; #5;
end
$display("INVENTORY_OK cycles=8"); $finish;
end
endmodule
