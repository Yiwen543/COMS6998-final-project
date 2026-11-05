`timescale 1ns/1ps
module tb_natural_inventory;
logic clk_i;
logic rst_ni;
logic op_start_i;
logic [11:0] op_num_words_i;
logic op_done_o;
logic [6:0] op_err_o;
logic [13:0] op_addr_i;
logic op_addr_oob_i;
logic [13:0] op_err_addr_o;
logic cnt_err_o;
logic data_rdy_i;
logic [38:0] data_o;
logic data_wr_o;
logic flash_req_o;
logic [13:0] flash_addr_o;
logic flash_ovfl_o;
logic [38:0] flash_data_i;
logic flash_done_i;
logic flash_rd_err_i;
logic flash_mp_err_i;
flash_ctrl_rd dut(.*);
initial begin
clk_i='0;
rst_ni='0;
op_start_i='0;
op_num_words_i='0;
op_addr_i='0;
op_addr_oob_i='0;
data_rdy_i='0;
flash_data_i='0;
flash_done_i='0;
flash_rd_err_i='0;
flash_mp_err_i='0;
rst_ni=0;
for(integer i=0;i<8;i=i+1) begin
clk_i=0; if(i==2) rst_ni=1; #5; clk_i=1; #5; $display("PORTS %0d %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h", i, clk_i, rst_ni, op_start_i, op_num_words_i, op_done_o, op_err_o, op_addr_i, op_addr_oob_i, op_err_addr_o, cnt_err_o, data_rdy_i, data_o, data_wr_o, flash_req_o, flash_addr_o, flash_ovfl_o, flash_data_i, flash_done_i, flash_rd_err_i, flash_mp_err_i);
end
$display("INVENTORY_OK cycles=8"); $finish;
end
endmodule
