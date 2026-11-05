`timescale 1ns/1ps
module tb_natural_inventory;
logic i_clk;
logic i_reset;
logic [1:0] i_mcyc;
logic [1:0] i_mstb;
logic [1:0] i_mwe;
logic [15:0] i_maddr;
logic [63:0] i_mdata;
logic [7:0] i_msel;
logic [1:0] o_mstall;
logic [1:0] o_mack;
logic [63:0] o_mdata;
logic [1:0] o_merr;
logic [1:0] o_scyc;
logic [1:0] o_sstb;
logic [1:0] o_swe;
logic [15:0] o_saddr;
logic [63:0] o_sdata;
logic [7:0] o_ssel;
logic [1:0] i_sstall;
logic [1:0] i_sack;
logic [63:0] i_sdata;
logic [1:0] i_serr;
wbxbar #(.NM(2),.NS(2),.AW(8),.DW(32),.SLAVE_ADDR(4096),.SLAVE_MASK(61680),.LGMAXBURST(3),.OPT_TIMEOUT(16),.OPT_STARVATION_TIMEOUT(1),.OPT_DBLBUFFER(1),.OPT_LOWPOWER(1)) dut(.*);
initial begin
i_clk=1'd0;
i_reset=1'd0;
i_mcyc=2'd0;
i_mstb=2'd0;
i_mwe=2'd0;
i_maddr=16'd0;
i_mdata=64'd0;
i_msel=8'd0;
i_sstall=2'd0;
i_sack=2'd0;
i_sdata=64'd0;
i_serr=2'd0;
i_reset=1;
for(integer i=0;i<8;i=i+1) begin
i_clk=0; if(i==2) i_reset=0; #5; i_clk=1; #5;
end
$display("INVENTORY_OK cycles=8"); $finish;
end
endmodule
