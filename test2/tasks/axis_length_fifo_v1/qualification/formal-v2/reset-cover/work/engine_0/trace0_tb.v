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
    // UUT.$auto$async2sync.\cc:116:execute$4470  = 1'b1;
    UUT._witness_.anyinit_procdff_4321 = 1'b1;
    UUT._witness_.anyinit_procdff_4322 = 1'b0;
    UUT._witness_.anyinit_procdff_4323 = 8'b00000000;
    UUT._witness_.anyinit_procdff_4324 = 1'b0;
    UUT._witness_.anyinit_procdff_4326 = 1'b1;
    UUT.dut.dut.axis_frame_length_adjust_inst.long_counter_reg = 16'b0000000000000000;
    UUT.dut.dut.axis_frame_length_adjust_inst.m_axis_tlast_reg = 1'b0;
    UUT.dut.dut.axis_frame_length_adjust_inst.m_axis_tready_int_reg = 1'b0;
    UUT.dut.dut.axis_frame_length_adjust_inst.m_axis_tvalid_reg = 1'b0;
    UUT.dut.dut.axis_frame_length_adjust_inst.s_axis_tready_reg = 1'b0;
    UUT.dut.dut.axis_frame_length_adjust_inst.short_counter_reg = 16'b0000000000000000;
    UUT.dut.dut.axis_frame_length_adjust_inst.state_reg = 3'b000;
    UUT.dut.dut.axis_frame_length_adjust_inst.status_valid_reg = 1'b0;
    UUT.dut.dut.axis_frame_length_adjust_inst.temp_m_axis_tlast_reg = 1'b0;
    UUT.dut.dut.axis_frame_length_adjust_inst.temp_m_axis_tvalid_reg = 1'b0;
    UUT.dut.dut.frame_fifo_inst.drop_frame_reg = 1'b0;
    UUT.dut.dut.frame_fifo_inst.m_axis_tvalid_pipe_reg = 2'b00;
    UUT.dut.dut.frame_fifo_inst.mark_frame_reg = 1'b0;
    UUT.dut.dut.frame_fifo_inst.rd_ptr_reg = 6'b000000;
    UUT.dut.dut.frame_fifo_inst.s_frame_reg = 1'b0;
    UUT.dut.dut.frame_fifo_inst.wr_ptr_commit_reg = 6'b000000;
    UUT.dut.dut.frame_fifo_inst.wr_ptr_reg = 6'b000000;
    UUT.dut.dut.header_fifo_inst.drop_frame_reg = 1'b0;
    UUT.dut.dut.header_fifo_inst.m_axis_tvalid_pipe_reg = 2'b00;
    UUT.dut.dut.header_fifo_inst.mark_frame_reg = 1'b0;
    UUT.dut.dut.header_fifo_inst.rd_ptr_reg = 4'b0000;
    UUT.dut.dut.header_fifo_inst.s_frame_reg = 1'b0;
    UUT.dut.dut.header_fifo_inst.wr_ptr_commit_reg = 4'b0000;
    UUT.dut.dut.header_fifo_inst.wr_ptr_reg = 4'b0000;
    UUT.past = 1'b0;

    // state 0
    UUT.s_valid = 1'b0;
    UUT.m_ready = 1'b0;
    UUT.h_ready = 1'b0;
    UUT.rst = 1'b1;
    UUT.s_data = 8'b00000000;
    UUT.s_last = 1'b0;
  end
  always @(posedge clock) begin
    // state 1
    if (cycle == 0) begin
      UUT.s_valid <= 1'b0;
      UUT.m_ready <= 1'b0;
      UUT.h_ready <= 1'b0;
      UUT.rst <= 1'b0;
      UUT.s_data <= 8'b00000000;
      UUT.s_last <= 1'b0;
    end

    // state 2
    if (cycle == 1) begin
      UUT.s_valid <= 1'b1;
      UUT.m_ready <= 1'b0;
      UUT.h_ready <= 1'b0;
      UUT.rst <= 1'b0;
      UUT.s_data <= 8'b00000000;
      UUT.s_last <= 1'b0;
    end

    genclock <= cycle < 2;
    cycle <= cycle + 1;
  end
endmodule
