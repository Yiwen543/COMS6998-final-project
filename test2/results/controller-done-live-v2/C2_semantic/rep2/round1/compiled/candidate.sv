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
// Private, bounded specification scoreboard. No DUT state is referenced.
reg armed = 1'b0;
reg reset_post = 1'b0;
reg [5:0] bad = 0;
reg [5:0] fail_now;
reg [6:0] iw = 0, dr = 0, hr = 0;
reg [3:0] ip = 0, dp = 0;
reg [63:0] bytes_q [0:63];
reg [3:0] size_q [0:63];
reg [63:0] complete_q = 0;
reg ms = 0, hs = 0;
reg [8:0] saved_m = 0;
reg [33:0] saved_h = 0;
reg [7:0] tail = 0;
wire [6:0] data_distance = iw-dr;
wire [6:0] header_distance = iw-hr;
wire data_exists = (data_distance != 0) || (ip != 0);
wire header_exists = header_distance != 0;
reg [3:0] dn, out_len;
reg [7:0] expected_byte;
reg expected_last, byte_known;
reg [15:0] hn, hl;
reg [33:0] expected_header;
integer k;

always @* begin
    dn = 0;
    if (data_distance != 0) dn = size_q[dr[5:0]];
    else dn = ip;
    if (dn < 4) out_len = 4;
    else if (dn > 8) out_len = 8;
    else out_len = dn;
    byte_known = 0;
    expected_byte = 0;
    expected_last = 0;
    if (data_exists && dp < 8) begin
        if (dp < dn) begin
            byte_known = 1;
            expected_byte = bytes_q[dr[5:0]][dp*8 +: 8];
        end else if (data_distance != 0 && dp < out_len) begin
            byte_known = 1;
            expected_byte = 0;
        end
        if (dp == 7) expected_last = 1;
        else if (data_distance != 0) expected_last = (dp == out_len-1);
    end
    hn = 0;
    hl = 0;
    expected_header = 0;
    if (header_exists) begin
        hn = {12'd0,size_q[hr[5:0]]};
        if (hn < 4) hl = 4;
        else if (hn > 8) hl = 8;
        else hl = hn;
        expected_header = {(hn < 4),(hn > 8),hl,hn};
    end

    fail_now = 0;
    if (armed) begin
        // Presented outputs are checked even when their sinks are blocked.
        if (m_valid !== 1'b0 && m_valid !== 1'b1) fail_now[0] = 1;
        if (m_valid === 1'b1) begin
            if (!byte_known) fail_now[0] = 1;
            else begin
                if ((^m_data === 1'bx) || (^expected_byte === 1'bx) ||
                    m_data !== expected_byte) fail_now[0] = 1;
                if (m_last !== expected_last) fail_now[0] = 1;
            end
        end
        if (h_valid !== 1'b0 && h_valid !== 1'b1) fail_now[1] = 1;
        if (h_valid === 1'b1) begin
            if (!header_exists) fail_now[1] = 1;
            else if ((^{h_pad,h_truncate,h_length,h_original_length} === 1'bx) ||
                {h_pad,h_truncate,h_length,h_original_length} !== expected_header)
                fail_now[1] = 1;
        end
        // The previous edge's blocked response must survive into this sample.
        if (!reset_post) begin
            if (ms && (m_valid !== 1'b1 ||
                {m_data,m_last} !== saved_m || ^{m_data,m_last} === 1'bx))
                fail_now[2] = 1;
            if (hs && (h_valid !== 1'b1 ||
                {h_pad,h_truncate,h_length,h_original_length} !== saved_h ||
                ^{h_pad,h_truncate,h_length,h_original_length} === 1'bx))
                fail_now[2] = 1;
        end
        if (reset_post && (m_valid !== 1'b0 || h_valid !== 1'b0))
            fail_now[3] = 1;
        // Meaningful accepted input observations and bounded inventory.
        if (rst !== 1'b0 && rst !== 1'b1) fail_now[4] = 1;
        if (rst === 1'b0) begin
            if (s_valid !== 1'b0 && s_valid !== 1'b1) fail_now[4] = 1;
            if (s_valid === 1'b1) begin
                if (s_ready !== 1'b0 && s_ready !== 1'b1) fail_now[4] = 1;
                if (s_ready === 1'b1) begin
                    if ((^s_data === 1'bx) ||
                        (s_last !== 1'b0 && s_last !== 1'b1)) fail_now[4] = 1;
                    if (ip >= 12 || (ip == 11 && s_last !== 1'b1)) fail_now[4] = 1;
                    if (data_distance >= 63 || header_distance >= 63) fail_now[4] = 1;
                end
            end
            if (m_valid === 1'b1 && m_ready !== 1'b0 && m_ready !== 1'b1)
                fail_now[4] = 1;
            if (h_valid === 1'b1 && h_ready !== 1'b0 && h_ready !== 1'b1)
                fail_now[4] = 1;
        end
        if (trace_done === 1'b1) begin
            if (tail < 32 || rst !== 1'b0 || s_valid !== 1'b0 ||
                m_valid !== 1'b0 || h_valid !== 1'b0 ||
                ip != 0 || dp != 0 || iw != dr || iw != hr)
                fail_now[5] = 1;
        end
    end
end

always @(posedge clk) begin
    armed <= 1;
    if (armed) bad <= bad | fail_now;
    reset_post <= (rst === 1'b1);
    if (rst === 1'b1) begin
        iw <= 0;
        dr <= 0;
        hr <= 0;
        ip <= 0;
        dp <= 0;
        complete_q <= 0;
        ms <= 0;
        hs <= 0;
        tail <= 0;
    end else if (rst === 1'b0) begin
        if (s_valid === 1'b0 && m_ready === 1'b1 && h_ready === 1'b1) begin
            if (tail != 255) tail <= tail+1'b1;
        end else tail <= 0;
        ms <= (m_valid === 1'b1 && m_ready === 1'b0);
        hs <= (h_valid === 1'b1 && h_ready === 1'b0);
        saved_m <= {m_data,m_last};
        saved_h <= {h_pad,h_truncate,h_length,h_original_length};
        if (s_valid === 1'b1 && s_ready === 1'b1 && ip < 12 &&
            data_distance < 63 && header_distance < 63) begin
            if (ip < 8) bytes_q[iw[5:0]][ip*8 +: 8] <= s_data;
            if (s_last === 1'b1) begin
                size_q[iw[5:0]] <= ip+1'b1;
                complete_q[iw[5:0]] <= 1;
                iw <= iw+1'b1;
                ip <= 0;
            end else ip <= ip+1'b1;
        end
        if (m_valid === 1'b1 && m_ready === 1'b1 && byte_known) begin
            if (expected_last) begin
                dr <= dr+1'b1;
                dp <= 0;
            end else dp <= dp+1'b1;
        end
        if (h_valid === 1'b1 && h_ready === 1'b1 && header_exists)
            hr <= hr+1'b1;
    end
end

assign active[0] = armed;
assign active[1] = armed;
assign active[2] = armed;
assign active[3] = armed;
assign active[4] = armed;
assign active[5] = armed && ((trace_done === 1'b1) || bad[5]);
assign ok = ~(bad | fail_now);

endmodule
`default_nettype wire
