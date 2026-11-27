// One accepted input frame per synchronous reset epoch; only public wrapper pins.
module frame_txn(input clk, rst, s_valid, s_last, m_ready, h_ready,
                 input [7:0] s_data);
    wire s_ready, m_valid, m_last, h_valid, h_pad, h_truncate;
    wire [7:0] m_data;
    wire [15:0] h_original_length, h_length;
    frame_task dut(.*);

    reg started = 0;
    reg past_reset, past_stall, past_last;
    reg [7:0] past_data;
    reg completed, data_consumed, header_consumed;
    reg [3:0] accepted, sent;
    // An arbitrary constant selects one of the eight retained bytes. Proving
    // the assertion for all choices checks every output byte, with one ghost register.
    (* anyconst *) reg [2:0] byte_slot;
    reg [7:0] watched_byte;
    reg flush_pending;

    wire take = s_valid && s_ready;
    wire [3:0] adjusted = accepted < 4 ? 4 : accepted > 8 ? 8 : accepted;
    wire raw_byte = !data_consumed && sent < 8 && sent < accepted;
    wire pad_byte = !data_consumed && completed && accepted < 4 && sent >= accepted && sent < 4;
    wire permitted = raw_byte || pad_byte;
    wire header_due = completed && !header_consumed;
    wire expected_last = completed ? sent + 4'd1 == adjusted : sent == 7;

    always @(posedge clk) begin
        started <= 1;
        past_reset <= rst;
        past_stall <= s_valid && !s_ready;
        past_data <= s_data;
        past_last <= s_last;
        flush_pending <= rst && started && (h_valid || m_valid);
        if (rst) begin
            accepted <= 0;
            sent <= 0;
            completed <= 0;
            data_consumed <= 0;
            header_consumed <= 0;
        end else begin
            if (take) begin
                if (accepted == {1'b0, byte_slot}) watched_byte <= s_data;
                accepted <= accepted + 1'b1;
                if (s_last) completed <= 1;
            end
            if (m_valid && m_ready) begin
                if (m_last) data_consumed <= 1;
                else sent <= sent + 1'b1;
            end
            if (h_valid && h_ready) header_consumed <= 1;
        end
    end

    always @* begin
        if (!started) assume(rst);
        if (rst) assume(!s_valid);
        if (started && !past_reset && !rst && past_stall)
            assume(s_valid && s_data == past_data && s_last == past_last);
        if (started && !rst && (completed || accepted == 12)) assume(!s_valid);
        if (started && !rst) begin
            data_entitlement: assert(!m_valid || permitted);
            if (m_valid && permitted) begin
                data_payload: assert(pad_byte ? m_data == 0 :
                                     (sent != {1'b0, byte_slot} || m_data == watched_byte));
                data_last: assert(m_last == expected_last);
            end
            header_entitlement: assert(!h_valid || header_due);
            if (h_valid && header_due) begin
                header_original: assert(h_original_length == {12'b0, accepted});
                header_adjusted: assert(h_length == {12'b0, adjusted});
                header_flags: assert(h_pad == (accepted < 4) && h_truncate == (accepted > 8));
            end
        end
        if (started && past_reset)
            reset_clear: assert(!m_valid && !h_valid);

        retained_byte: cover(started && !rst && m_valid && raw_byte && m_data != 0);
        pad_presented: cover(started && !rst && m_valid && pad_byte);
        long_header: cover(started && !rst && h_valid && accepted > 8 && header_due);
        header_only_transfer: cover(started && !rst && m_valid && !m_ready && h_valid && h_ready);
        data_only_transfer: cover(started && !rst && m_valid && m_ready && h_valid && !h_ready);
        reset_with_pending_output: cover(started && past_reset && flush_pending && !h_valid && !m_valid);
    end
endmodule
