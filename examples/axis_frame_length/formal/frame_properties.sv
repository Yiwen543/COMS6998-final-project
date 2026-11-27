// Samples immediately before consecutive rising edges of the unmodified frame_task.
module frame_properties(input clk, input rst, input s_valid, input [7:0] s_data,
                        input s_last, input m_ready, input h_ready);
    wire s_ready, m_valid, m_last, h_valid, h_pad, h_truncate;
    wire [7:0] m_data;
    wire [15:0] h_length, h_original_length;
    frame_task dut(.*);

    reg have_prev = 0;
    reg prev_rst, prev_s_valid, prev_s_ready, prev_s_last;
    reg prev_m_valid, prev_m_ready, prev_m_last;
    reg prev_h_valid, prev_h_ready, prev_h_pad, prev_h_truncate;
    reg [7:0] prev_s_data, prev_m_data;
    reg [15:0] prev_h_length, prev_h_original_length;
    reg [3:0] accepted = 0;
    wire take = s_valid && s_ready;
    always @(posedge clk) begin
        have_prev <= 1;
        prev_rst <= rst;
        {prev_s_valid, prev_s_ready, prev_s_data, prev_s_last} <= {s_valid, s_ready, s_data, s_last};
        {prev_m_valid, prev_m_ready, prev_m_data, prev_m_last} <= {m_valid, m_ready, m_data, m_last};
        {prev_h_valid, prev_h_ready, prev_h_pad, prev_h_truncate, prev_h_length, prev_h_original_length}
            <= {h_valid, h_ready, h_pad, h_truncate, h_length, h_original_length};
        if (rst || (take && s_last)) accepted <= 0;
        else if (take) accepted <= accepted + 1'b1;
    end

    wire reset_quiet = have_prev && !prev_rst && !rst;
    wire present = !rst && h_valid;
    always @* begin
        if (!have_prev) assume(rst);
        if (rst) assume(!s_valid);
        if (reset_quiet && prev_s_valid && !prev_s_ready)
            assume(s_valid && {s_data, s_last} == {prev_s_data, prev_s_last});
        // Each accepted beat is one byte. A twelfth unfinished byte may remain
        // stalled indefinitely or be flushed by reset. A thirteenth is excluded.
        if (!rst && take) assume(accepted < 4'd12);

        `include "frame_assertions.svh"

        data_stall: cover(reset_quiet && (prev_m_valid && !prev_m_ready));
        header_stall: cover(reset_quiet && (prev_h_valid && !prev_h_ready));
        padded_header: cover(present && h_pad && h_original_length < 16'd4);
        truncated_header: cover(present && h_truncate && h_original_length > 16'd8);
        length_four: cover(present && h_original_length == 16'd4);
        length_eight: cover(present && h_original_length == 16'd8);
    end
endmodule
