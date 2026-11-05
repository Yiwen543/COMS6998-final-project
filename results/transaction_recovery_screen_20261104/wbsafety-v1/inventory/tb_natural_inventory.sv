`timescale 1ns/1ps
module tb_natural_inventory;
logic i_clk;
logic i_reset;
logic i_wb_cyc;
logic i_wb_stb;
logic i_wb_we;
logic [7:0] i_wb_addr;
logic [31:0] i_wb_data;
logic [3:0] i_wb_sel;
logic o_wb_stall;
logic o_wb_ack;
logic [31:0] o_wb_idata;
logic o_wb_err;
logic o_reset;
logic o_wb_cyc;
logic o_wb_stb;
logic o_wb_we;
logic [7:0] o_wb_addr;
logic [31:0] o_wb_data;
logic [3:0] o_wb_sel;
logic i_wb_stall;
logic i_wb_ack;
logic [31:0] i_wb_idata;
logic i_wb_err;
logic o_fault;
wbsafety #(.AW(8),.DW(32),.OPT_TIMEOUT(12),.MAX_DEPTH(8),.OPT_SELF_RESET(1)) dut(.*);
initial begin
i_clk=1'd0;
i_reset=1'd0;
i_wb_cyc=1'd0;
i_wb_stb=1'd0;
i_wb_we=1'd0;
i_wb_addr=8'd0;
i_wb_data=32'd0;
i_wb_sel=4'd0;
i_wb_stall=1'd0;
i_wb_ack=1'd0;
i_wb_idata=32'd0;
i_wb_err=1'd0;
i_reset=1;
for(integer i=0;i<8;i=i+1) begin
i_clk=0; if(i==2) i_reset=0; #5; i_clk=1; #5;
end
$display("INVENTORY_OK cycles=8"); $finish;
end
endmodule
