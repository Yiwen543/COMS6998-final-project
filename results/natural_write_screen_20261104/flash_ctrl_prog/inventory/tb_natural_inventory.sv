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
logic op_type_i;
logic [1:0] type_avail_i;
logic [13:0] op_err_addr_o;
logic cnt_err_o;
logic data_rdy_i;
logic [38:0] data_i;
logic data_rd_o;
logic flash_req_o;
logic [13:0] flash_addr_o;
logic flash_ovfl_o;
logic [38:0] flash_data_o;
logic flash_last_o;
logic flash_type_o;
logic flash_done_i;
logic flash_mp_err_i;
logic flash_prog_intg_err_i;
flash_ctrl_prog dut(.*);
initial begin
clk_i='0;
rst_ni='0;
op_start_i='0;
op_num_words_i='0;
op_addr_i='0;
op_addr_oob_i='0;
op_type_i='0;
type_avail_i='0;
data_rdy_i='0;
data_i='0;
flash_done_i='0;
flash_mp_err_i='0;
flash_prog_intg_err_i='0;
rst_ni=0;
for(integer i=0;i<8;i=i+1) begin
clk_i=0; if(i==2) rst_ni=1; #5; clk_i=1; #5;
end
$display("INVENTORY_OK cycles=8"); $finish;
end
endmodule
