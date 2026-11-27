// One SMT transition advances the single physical positive-edge clock once.
// Outputs and inputs are compared immediately before successive rising edges.
module fifo_stall_formal(input clk, input rst, input s_axis_tvalid,
                         input [7:0] s_axis_tdata, input s_axis_tlast, input s_axis_tuser,
                         input m_axis_tready);
    wire s_axis_tready, m_axis_tvalid, m_axis_tlast, m_axis_tuser;
    wire [7:0] m_axis_tdata;
    axis_fifo #(.DEPTH(4), .DATA_WIDTH(8), .KEEP_ENABLE(0), .KEEP_WIDTH(1),
                .LAST_ENABLE(1), .ID_ENABLE(0), .ID_WIDTH(1), .DEST_ENABLE(0), .DEST_WIDTH(1),
                .USER_ENABLE(1), .USER_WIDTH(1), .RAM_PIPELINE(1), .OUTPUT_FIFO_ENABLE(0),
                .FRAME_FIFO(0), .PAUSE_ENABLE(0)) dut(
        .clk(clk), .rst(rst), .s_axis_tvalid(s_axis_tvalid), .s_axis_tready(s_axis_tready),
        .s_axis_tdata(s_axis_tdata), .s_axis_tlast(s_axis_tlast), .s_axis_tuser(s_axis_tuser),
        .s_axis_tkeep(1'b1), .s_axis_tid(1'b0), .s_axis_tdest(1'b0), .pause_req(1'b0),
        .m_axis_tvalid(m_axis_tvalid), .m_axis_tready(m_axis_tready), .m_axis_tdata(m_axis_tdata),
        .m_axis_tlast(m_axis_tlast), .m_axis_tuser(m_axis_tuser)
    );

    reg have_previous = 0;
    reg prev_reset, prev_valid, prev_ready, prev_last, prev_user;
    reg [7:0] prev_data;
    reg prev_source_stalled;
    reg [9:0] prev_source_payload;
    always @(posedge clk) begin
        have_previous <= 1;
        prev_reset <= rst;
        prev_valid <= m_axis_tvalid;
        prev_ready <= m_axis_tready;
        prev_data <= m_axis_tdata;
        prev_last <= m_axis_tlast;
        prev_user <= m_axis_tuser;
        prev_source_stalled <= s_axis_tvalid && !s_axis_tready;
        prev_source_payload <= {s_axis_tdata, s_axis_tlast, s_axis_tuser};
    end

    wire reset_quiet = have_previous && !prev_reset && !rst;
    wire active = reset_quiet && prev_valid && !prev_ready;
    wire valid_lost = !m_axis_tvalid;
    wire data_changed = m_axis_tdata != prev_data;
    wire last_changed = m_axis_tlast != prev_last;
    wire user_changed = m_axis_tuser != prev_user;
    always @* begin
        if (!have_previous) assume(rst);
        if (reset_quiet && prev_source_stalled) begin
            assume(s_axis_tvalid);
            assume({s_axis_tdata, s_axis_tlast, s_axis_tuser} == prev_source_payload);
        end
    end
    `include "obligations.svh"
endmodule
