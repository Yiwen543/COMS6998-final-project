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
  wire [0:0] PI_clk = clock;
  formal_top UUT (
    .clk(PI_clk)
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
    // UUT.$auto$async2sync.\cc:107:execute$3472  = 1'b0;
    // UUT.$auto$async2sync.\cc:116:execute$3476  = 1'b1;
    UUT._witness_.anyinit_procdff_3453 = 1'b1;
    UUT._witness_.anyinit_procdff_3454 = 1'b0;
    UUT._witness_.anyinit_procdff_3455 = 8'b00000000;
    UUT._witness_.anyinit_procdff_3456 = 1'b0;
    UUT.dut.dut.long_counter_reg = 16'b0000000000000000;
    UUT.dut.dut.m_axis_tready_int_reg = 1'b0;
    UUT.dut.dut.m_axis_tvalid_reg = 1'b0;
    UUT.dut.dut.s_axis_tready_reg = 1'b0;
    UUT.dut.dut.short_counter_reg = 16'b0000000000000000;
    UUT.dut.dut.state_reg = 3'b000;
    UUT.dut.dut.status_valid_reg = 1'b0;
    UUT.dut.dut.temp_m_axis_tvalid_reg = 1'b0;
    UUT.past = 1'b0;

    // state 0
    UUT.s_valid = 1'b0;
    UUT.m_ready = 1'b0;
    UUT.rst = 1'b1;
    UUT.s_data = 8'b00000000;
    UUT.h_ready = 1'b0;
    UUT.s_last = 1'b0;
  end
  always @(posedge clock) begin
    // state 1
    if (cycle == 0) begin
      UUT.s_valid <= 1'b0;
      UUT.m_ready <= 1'b0;
      UUT.rst <= 1'b0;
      UUT.s_data <= 8'b00000000;
      UUT.h_ready <= 1'b0;
      UUT.s_last <= 1'b0;
    end

    // state 2
    if (cycle == 1) begin
      UUT.s_valid <= 1'b1;
      UUT.m_ready <= 1'b0;
      UUT.rst <= 1'b0;
      UUT.s_data <= 8'b00000000;
      UUT.h_ready <= 1'b0;
      UUT.s_last <= 1'b0;
    end

    genclock <= cycle < 2;
    cycle <= cycle + 1;
  end
endmodule
