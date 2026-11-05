module wbxbar_range_formal(
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

// No input/protocol assumptions; preserve original initial values. No mindex reset.
for (genvar n=0;n<2;n=n+1) begin: monitor
 wire [1:0] index_value = dut.mindex[n];
 wire active = dut.mgrant[n];
 wire [2:0] request_value = dut.request[n];
 wire [2:0] grant_value = dut.grant[n];
 wire selected = active && !grant_value[2];
 always @(posedge i_clk) begin
`ifdef CHECK_COVER
  cover(active && index_value==0);
  cover(active && index_value==1);
  cover(active && index_value==2);
  cover(selected && index_value==0);
  cover(selected && index_value==1);
`elsif CHECK_UNCONDITIONAL
  assert(index_value<=2);
`elsif CHECK_FALSE
  assert(!selected || index_value==0);
`else
  assert(!selected || index_value<=2);
`ifdef CHECK_HELPERS
  assert((request_value & (request_value-3'd1))==0);
  assert((grant_value & (grant_value-3'd1))==0);
  assert(active == (|grant_value));
  assert(!selected || grant_value==(3'b001 << index_value));
`endif
`endif
 end
end
endmodule
