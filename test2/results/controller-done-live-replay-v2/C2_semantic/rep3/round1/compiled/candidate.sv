`default_nettype none
module candidate_monitor(
input wire clk,
input wire rst,
input wire s_valid,
input wire [7:0] s_data,
input wire s_last,
input wire m_ready,
input wire h_ready,
input wire s_ready,
input wire [7:0] m_data,
input wire m_valid,
input wire m_last,
input wire h_valid,
input wire h_pad,
input wire h_truncate,
input wire [15:0] h_length,
input wire [15:0] h_original_length,
input wire trace_done,
output wire [5:0] active,ok);
// Private, bounded transaction scoreboard. No DUT timing model is used.
reg armed = 1'b0;
reg [5:0] bad = 0;
reg [5:0] wp = 0, dp = 0, hp = 0;
reg [3:0] di = 0;
reg [63:0] bytes_q [0:63];
reg [3:0] length_q [0:63];
reg complete_q [0:63];
reg used_q [0:63];
reg data_done_q [0:63];
reg hdr_done_q [0:63];
reg reset_q = 0;
reg ms = 0, hs = 0;
reg [8:0] saved_m = 0;
reg [33:0] saved_h = 0;
reg [7:0] tail = 0;
reg [5:0] fail_now;
reg [3:0] out_len;
reg [7:0] expected_byte;
reg byte_available, expected_last;
reg pending;
integer k;
integer r;

always @* begin
    fail_now = 0;
    pending = 0;
    out_len = 0;
    expected_byte = 0;
    byte_available = 0;
    expected_last = 0;
    for (k=0; k<64; k=k+1) begin
        if (used_q[k] === 1'b1) begin
            if (data_done_q[k] !== 1'b1 || hdr_done_q[k] !== 1'b1 || complete_q[k] !== 1'b1)
                pending = 1;
        end
    end
    if (armed) begin
        if (rst !== 1'b0 && rst !== 1'b1) fail_now[4] = 1;
        if (m_valid !== 1'b0 && m_valid !== 1'b1) fail_now[4] = 1;
        if (h_valid !== 1'b0 && h_valid !== 1'b1) fail_now[4] = 1;
        if (s_ready !== 1'b0 && s_ready !== 1'b1) fail_now[4] = 1;
        if (s_valid !== 1'b0 && s_valid !== 1'b1) fail_now[4] = 1;
        if (m_ready !== 1'b0 && m_ready !== 1'b1) fail_now[4] = 1;
        if (h_ready !== 1'b0 && h_ready !== 1'b1) fail_now[4] = 1;
        if (s_valid === 1'b1 && s_ready === 1'b1 && rst === 1'b0) begin
            if ((^s_data) === 1'bx || (s_last !== 1'b0 && s_last !== 1'b1)) fail_now[4] = 1;
        end
        if (reset_q) begin
            if (m_valid !== 1'b0 || h_valid !== 1'b0) fail_now[4] = 1;
        end
        if (rst === 1'b0) begin
            if (ms && (m_valid !== 1'b1 || {m_last,m_data} !== saved_m)) fail_now[3] = 1;
            if (hs && (h_valid !== 1'b1 || {h_pad,h_truncate,h_length,h_original_length} !== saved_h)) fail_now[3] = 1;
        end
        // Presentation checks apply even if the sink is blocked, and even
        // at a pre-reset observation. Reset only cancels at its edge.
        if (used_q[dp] === 1'b1 && data_done_q[dp] === 1'b0) begin
            if (length_q[dp] < 4) out_len = 4;
            else if (length_q[dp] > 8) out_len = 8;
            else out_len = length_q[dp];
            if (di < 8 && di < length_q[dp]) begin
                byte_available = 1;
                expected_byte = bytes_q[dp][di*8 +: 8];
            end else if (complete_q[dp] === 1'b1 && di < out_len) begin
                byte_available = 1;
                expected_byte = 0;
            end
            if (complete_q[dp] === 1'b1) expected_last = (di == out_len-1);
            else expected_last = (di == 7);
        end
        if (m_valid === 1'b1) begin
            if (!byte_available || (^m_data) === 1'bx || m_data !== expected_byte) fail_now[0] = 1;
            if (!byte_available || m_last !== expected_last) fail_now[1] = 1;
        end
        if (h_valid === 1'b1) begin
            if (used_q[hp] !== 1'b1 || complete_q[hp] !== 1'b1 || hdr_done_q[hp] !== 1'b0) begin
                fail_now[2] = 1;
            end else begin
                if (h_original_length !== {12'd0,length_q[hp]}) fail_now[2] = 1;
                if (h_pad !== (length_q[hp] < 4)) fail_now[2] = 1;
                if (h_truncate !== (length_q[hp] > 8)) fail_now[2] = 1;
                if (length_q[hp] < 4) begin
                    if (h_length !== 16'd4) fail_now[2] = 1;
                end else if (length_q[hp] > 8) begin
                    if (h_length !== 16'd8) fail_now[2] = 1;
                end else if (h_length !== {12'd0,length_q[hp]}) fail_now[2] = 1;
            end
        end
        if (trace_done === 1'b1) begin
            if (pending || s_valid !== 1'b0 || m_valid !== 1'b0 || h_valid !== 1'b0 || rst !== 1'b0 || tail < 32)
                fail_now[5] = 1;
        end
    end
end

assign active = armed ? 6'b111111 : (trace_done === 1'b1 ? 6'b100000 : 6'b000000);
assign ok = ~(bad | fail_now | ((!armed && trace_done === 1'b1) ? 6'b100000 : 6'b000000));

always @(posedge clk) begin
    if (armed) bad <= bad | fail_now;
    reset_q <= (rst === 1'b1);
    if (rst === 1'b1) begin
        armed <= 1;
        wp <= 0;
        dp <= 0;
        hp <= 0;
        di <= 0;
        ms <= 0;
        hs <= 0;
        tail <= 0;
        for (r=0; r<64; r=r+1) begin
            bytes_q[r] <= 0;
            length_q[r] <= 0;
            complete_q[r] <= 0;
            used_q[r] <= 0;
            data_done_q[r] <= 1;
            hdr_done_q[r] <= 1;
        end
    end else if (armed && rst === 1'b0) begin
        ms <= (m_valid === 1'b1 && m_ready === 1'b0);
        hs <= (h_valid === 1'b1 && h_ready === 1'b0);
        saved_m <= {m_last,m_data};
        saved_h <= {h_pad,h_truncate,h_length,h_original_length};
        if (s_valid === 1'b0 && m_ready === 1'b1 && h_ready === 1'b1) begin
            if (tail < 128) tail <= tail + 1'b1;
        end else tail <= 0;
        if (m_valid === 1'b1 && m_ready === 1'b1) begin
            if (m_last === 1'b1) begin
                data_done_q[dp] <= 1;
                dp <= dp + 1'b1;
                di <= 0;
            end else if (di < 8) di <= di + 1'b1;
            else bad[1] <= 1;
        end
        if (h_valid === 1'b1 && h_ready === 1'b1) begin
            hdr_done_q[hp] <= 1;
            hp <= hp + 1'b1;
        end
        if (s_valid === 1'b1 && s_ready === 1'b1) begin
            // A completed slot can be recycled only after both independent
            // channels have consumed it. Overflow is never silently accepted.
            if (used_q[wp] !== 1'b1 || complete_q[wp] === 1'b1) begin
                if (used_q[wp] === 1'b1 && (data_done_q[wp] !== 1'b1 || hdr_done_q[wp] !== 1'b1)) bad[4] <= 1;
                used_q[wp] <= 1;
                complete_q[wp] <= (s_last === 1'b1);
                length_q[wp] <= 1;
                bytes_q[wp] <= {56'd0,s_data};
                data_done_q[wp] <= 0;
                hdr_done_q[wp] <= 0;
            end else begin
                if (length_q[wp] < 8) bytes_q[wp][length_q[wp]*8 +: 8] <= s_data;
                if (length_q[wp] < 12) length_q[wp] <= length_q[wp] + 1'b1;
                else bad[4] <= 1;
                if (s_last === 1'b1) complete_q[wp] <= 1;
            end
            if (s_last === 1'b1) wp <= wp + 1'b1;
        end
    end
end

endmodule
`default_nettype wire
