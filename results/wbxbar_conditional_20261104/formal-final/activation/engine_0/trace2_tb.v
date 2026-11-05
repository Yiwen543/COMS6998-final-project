`ifndef VERILATOR
module testbench;
  reg [4095:0] vcdfile;
  reg clock;
`else
module testbench(input clock, output reg genclock);
  initial genclock = 1;
`endif
  reg genclock = 1;
  reg [31:0] cycle = 0;
  reg [0:0] PI_i_reset;
  reg [1:0] PI_i_serr;
  reg [7:0] PI_i_msel;
  reg [1:0] PI_i_sack;
  reg [63:0] PI_i_mdata;
  reg [0:0] PI_i_clk;
  reg [1:0] PI_i_mcyc;
  reg [1:0] PI_i_sstall;
  reg [1:0] PI_i_mstb;
  reg [63:0] PI_i_sdata;
  reg [15:0] PI_i_maddr;
  reg [1:0] PI_i_mwe;
  wbxbar_range_formal UUT (
    .i_reset(PI_i_reset),
    .i_serr(PI_i_serr),
    .i_msel(PI_i_msel),
    .i_sack(PI_i_sack),
    .i_mdata(PI_i_mdata),
    .i_clk(PI_i_clk),
    .i_mcyc(PI_i_mcyc),
    .i_sstall(PI_i_sstall),
    .i_mstb(PI_i_mstb),
    .i_sdata(PI_i_sdata),
    .i_maddr(PI_i_maddr),
    .i_mwe(PI_i_mwe)
  );
`ifndef VERILATOR
  initial begin
    if ($value$plusargs("vcd=%s", vcdfile)) begin
      $dumpfile(vcdfile);
      $dumpvars(0, testbench);
    end
    #5 clock = 0;
    while (genclock) begin
      #5 clock = 0;
      #5 clock = 1;
    end
  end
`endif
  initial begin
`ifndef VERILATOR
    #1;
`endif
    // UUT.$auto$async2sync.\cc:107:execute$830  = 1'b0;
    // UUT.$auto$async2sync.\cc:116:execute$798  = 1'b1;
    // UUT.$auto$async2sync.\cc:116:execute$804  = 1'b1;
    // UUT.$auto$async2sync.\cc:116:execute$810  = 1'b1;
    // UUT.$auto$async2sync.\cc:116:execute$816  = 1'b1;
    // UUT.$auto$async2sync.\cc:116:execute$822  = 1'b1;
    // UUT.$auto$async2sync.\cc:116:execute$828  = 1'b1;
    // UUT.$auto$async2sync.\cc:116:execute$834  = 1'b1;
    // UUT.$auto$async2sync.\cc:116:execute$840  = 1'b1;
    // UUT.$auto$async2sync.\cc:116:execute$846  = 1'b1;
    // UUT.$auto$async2sync.\cc:116:execute$852  = 1'b1;
    UUT.dut.\ARBITRATE_REQUESTS[0] .MINDEX_MULTIPLE_SLAVES.r_mindex = 2'b00;
    UUT.dut.\ARBITRATE_REQUESTS[0] .r_grant = 3'b000;
    UUT.dut.\ARBITRATE_REQUESTS[0] .r_mgrant = 1'b0;
    UUT.dut.\ARBITRATE_REQUESTS[1] .MINDEX_MULTIPLE_SLAVES.r_mindex = 2'b10;
    UUT.dut.\ARBITRATE_REQUESTS[1] .r_grant = 3'b000;
    UUT.dut.\ARBITRATE_REQUESTS[1] .r_mgrant = 1'b0;
    UUT.dut.CHECK_TIMEOUT.\FOREACH_MASTER_PORT[0] .deadlock_timer = 4'b0000;
    UUT.dut.CHECK_TIMEOUT.\FOREACH_MASTER_PORT[0] .r_timed_out = 1'b0;
    UUT.dut.CHECK_TIMEOUT.\FOREACH_MASTER_PORT[1] .deadlock_timer = 4'b0000;
    UUT.dut.CHECK_TIMEOUT.\FOREACH_MASTER_PORT[1] .r_timed_out = 1'b0;
    UUT.dut.\COUNT_PENDING_TRANSACTIONS[0] .lclpending = 3'b000;
    UUT.dut.\COUNT_PENDING_TRANSACTIONS[0] .r_empty = 1'b1;
    UUT.dut.\COUNT_PENDING_TRANSACTIONS[0] .r_full = 1'b0;
    UUT.dut.\COUNT_PENDING_TRANSACTIONS[0] .r_nearfull = 1'b0;
    UUT.dut.\COUNT_PENDING_TRANSACTIONS[1] .lclpending = 3'b000;
    UUT.dut.\COUNT_PENDING_TRANSACTIONS[1] .r_empty = 1'b1;
    UUT.dut.\COUNT_PENDING_TRANSACTIONS[1] .r_full = 1'b0;
    UUT.dut.\COUNT_PENDING_TRANSACTIONS[1] .r_nearfull = 1'b0;
    UUT.dut.\DECODE_REQUEST[0] .adcd.o_addr = 8'b00000000;
    UUT.dut.\DECODE_REQUEST[0] .adcd.o_data = 37'b0000000000000000000000000000000000000;
    UUT.dut.\DECODE_REQUEST[0] .adcd.o_decode = 3'b000;
    UUT.dut.\DECODE_REQUEST[0] .adcd.o_valid = 1'b0;
    UUT.dut.\DECODE_REQUEST[0] .iskid.LOGIC.r_data = 45'b000000000000000000000000000000000000000000000;
    UUT.dut.\DECODE_REQUEST[0] .iskid.LOGIC.r_valid = 1'b0;
    UUT.dut.\DECODE_REQUEST[1] .adcd.o_addr = 8'b00000000;
    UUT.dut.\DECODE_REQUEST[1] .adcd.o_data = 37'b0000000000000000000000000000000000000;
    UUT.dut.\DECODE_REQUEST[1] .adcd.o_decode = 3'b000;
    UUT.dut.\DECODE_REQUEST[1] .adcd.o_valid = 1'b0;
    UUT.dut.\DECODE_REQUEST[1] .iskid.LOGIC.r_data = 45'b000000000000000000000000000000000000000000000;
    UUT.dut.\DECODE_REQUEST[1] .iskid.LOGIC.r_valid = 1'b0;
    UUT.dut.DOUBLE_BUFFERRED_STALL.\FOREACH_MASTER_PORT[0] .r_mack = 1'b0;
    UUT.dut.DOUBLE_BUFFERRED_STALL.\FOREACH_MASTER_PORT[0] .r_merr = 1'b0;
    UUT.dut.DOUBLE_BUFFERRED_STALL.\FOREACH_MASTER_PORT[1] .r_mack = 1'b0;
    UUT.dut.DOUBLE_BUFFERRED_STALL.\FOREACH_MASTER_PORT[1] .r_merr = 1'b0;
    UUT.dut.\GEN_CYC_STB[0] .r_scyc = 1'b0;
    UUT.dut.\GEN_CYC_STB[0] .r_sstb = 1'b0;
    UUT.dut.\GEN_CYC_STB[1] .r_scyc = 1'b0;
    UUT.dut.\GEN_CYC_STB[1] .r_sstb = 1'b0;
    UUT.dut.\GEN_SINDEX[0] .SINDEX_MORE_THAN_ONE_MASTER.r_sindex = 1'b1;
    UUT.dut.\GEN_SINDEX[1] .SINDEX_MORE_THAN_ONE_MASTER.r_sindex = 1'b1;
    UUT.dut.J.\GEN_DOWNSTREAM[0] .r_saddr = 8'b00000000;
    UUT.dut.J.\GEN_DOWNSTREAM[0] .r_sdata = 32'b00000000000000000000000000000000;
    UUT.dut.J.\GEN_DOWNSTREAM[0] .r_ssel = 4'b0000;
    UUT.dut.J.\GEN_DOWNSTREAM[0] .r_swe = 1'b0;
    UUT.dut.J.\GEN_DOWNSTREAM[1] .r_saddr = 8'b00000000;
    UUT.dut.J.\GEN_DOWNSTREAM[1] .r_sdata = 32'b00000000000000000000000000000000;
    UUT.dut.J.\GEN_DOWNSTREAM[1] .r_ssel = 4'b0000;
    UUT.dut.J.\GEN_DOWNSTREAM[1] .r_swe = 1'b0;
    UUT.dut.\SLAVE_GRANT[0] .r_sgrant = 1'b0;
    UUT.dut.\SLAVE_GRANT[1] .r_sgrant = 1'b0;
    UUT.dut.o_mdata = 64'b0000000000000000000000000000000000000000000000000000000000000000;

    // state 0
    PI_i_reset = 1'b0;
    PI_i_serr = 2'b00;
    PI_i_msel = 8'b00100000;
    PI_i_sack = 2'b00;
    PI_i_mdata = 64'b0000000000000000000000000000000100000000000000000000000000000000;
    PI_i_clk = 1'b0;
    PI_i_mcyc = 2'b11;
    PI_i_sstall = 2'b00;
    PI_i_mstb = 2'b11;
    PI_i_sdata = 64'b0000000000000000000000000000000000000000000000000000000000000000;
    PI_i_maddr = 16'b1001000000100000;
    PI_i_mwe = 2'b01;
  end
  always @(posedge clock) begin
    // state 1
    if (cycle == 0) begin
      PI_i_reset <= 1'b0;
      PI_i_serr <= 2'b00;
      PI_i_msel <= 8'b00000000;
      PI_i_sack <= 2'b00;
      PI_i_mdata <= 64'b1000000000000000000000000000000000000000000000000000000010000000;
      PI_i_clk <= 1'b0;
      PI_i_mcyc <= 2'b11;
      PI_i_sstall <= 2'b00;
      PI_i_mstb <= 2'b00;
      PI_i_sdata <= 64'b0000000000000000000000000000000000000000000000000000000000000000;
      PI_i_maddr <= 16'b0000000000000000;
      PI_i_mwe <= 2'b11;
    end

    // state 2
    if (cycle == 1) begin
      PI_i_reset <= 1'b1;
      PI_i_serr <= 2'b00;
      PI_i_msel <= 8'b00000000;
      PI_i_sack <= 2'b00;
      PI_i_mdata <= 64'b0000000000000000000000000000000000000000000000000000000000000000;
      PI_i_clk <= 1'b0;
      PI_i_mcyc <= 2'b00;
      PI_i_sstall <= 2'b00;
      PI_i_mstb <= 2'b00;
      PI_i_sdata <= 64'b0000000000000000000000000000000000000000000000000000000000000000;
      PI_i_maddr <= 16'b0001000000010000;
      PI_i_mwe <= 2'b00;
    end

    // state 3
    if (cycle == 2) begin
      PI_i_reset <= 1'b0;
      PI_i_serr <= 2'b00;
      PI_i_msel <= 8'b00100000;
      PI_i_sack <= 2'b00;
      PI_i_mdata <= 64'b0000000000000000000000000000000100000000000000000000000000000000;
      PI_i_clk <= 1'b0;
      PI_i_mcyc <= 2'b11;
      PI_i_sstall <= 2'b00;
      PI_i_mstb <= 2'b00;
      PI_i_sdata <= 64'b0000000000000000000000000000000000000000000000000000000000000000;
      PI_i_maddr <= 16'b1001000000100000;
      PI_i_mwe <= 2'b01;
    end

    genclock <= cycle < 3;
    cycle <= cycle + 1;
  end
endmodule
