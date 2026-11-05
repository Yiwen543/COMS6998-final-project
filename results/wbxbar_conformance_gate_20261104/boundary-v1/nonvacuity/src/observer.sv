module wbxbar_quiet_observer(
input wire i_clk,
input wire i_reset,
input wire [1:0] i_mcyc,
input wire [1:0] i_mstb,
input wire [1:0] i_mwe,
input wire [15:0] i_maddr,
input wire [63:0] i_mdata,
input wire [7:0] i_msel,
output wire [1:0] o_mstall,
output wire [1:0] o_mack,
output wire [63:0] o_mdata,
output wire [1:0] o_merr,
output wire [1:0] o_scyc,
output wire [1:0] o_sstb,
output wire [1:0] o_swe,
output wire [15:0] o_saddr,
output wire [63:0] o_sdata,
output wire [7:0] o_ssel,
input wire [1:0] i_sstall,
input wire [1:0] i_sack,
input wire [63:0] i_sdata,
input wire [1:0] i_serr
);
wbxbar #(.NM(2),.NS(2),.AW(8),.DW(32),.SLAVE_ADDR(4096),.SLAVE_MASK(61680),.LGMAXBURST(3),.OPT_TIMEOUT(16),.OPT_STARVATION_TIMEOUT(1),.OPT_DBLBUFFER(1),.OPT_LOWPOWER(1)) dut(.*);

// No input assumptions. Original transition system; FORMAL define is disabled.
// This observes a version-specific pin implication, not request cancellation.
reg past_valid = 1'b0;
always @(posedge i_clk) begin
    past_valid <= 1'b1;
`ifdef OBS_COVER
    cover(past_valid && $past(i_mcyc != 0) && i_mcyc == 0 && o_scyc != 0);
    cover(past_valid && $past(i_mcyc == 0) && i_mcyc != 0 && o_scyc == 0);
`elsif OBS_INSTANT
    if (past_valid && i_mcyc == 0) assert(o_scyc == 0 && o_sstb == 0);
`else
    if (past_valid && $past(i_mcyc == 0)) assert(o_scyc == 0 && o_sstb == 0);
`endif
end
endmodule
