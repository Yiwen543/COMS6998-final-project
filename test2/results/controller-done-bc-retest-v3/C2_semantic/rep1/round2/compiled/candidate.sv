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
reg started = 0;
reg reset_post = 0;
reg [5:0] bad = 0;
reg [6:0] iw = 0, dr = 0, hr = 0;
reg [3:0] ilen = 0, dp = 0;
reg [63:0] bytes_q [0:63];
reg [3:0] lengths [0:63];
reg complete_q [0:63];
reg ms = 0, hs = 0;
reg [8:0] saved_m = 0;
reg [33:0] saved_h = 0;
reg [5:0] check_now;
reg [3:0] dl, out_len;
reg [7:0] expected_byte;
reg expected_last, data_available, header_available;
reg [33:0] expected_header;
integer k;
wire [5:0] wi = iw[5:0];
wire [5:0] di = dr[5:0];
wire [5:0] hi = hr[5:0];
wire [6:0] data_distance = iw-dr;
wire [6:0] header_distance = iw-hr;

always @* begin
    check_now = 6'b111111;
    dl = 0;
    out_len = 0;
    expected_byte = 0;
    expected_last = 0;
    data_available = 0;
    header_available = 0;
    expected_header = 0;
    if (started) begin
        if ((dr != iw) || (ilen != 0)) begin
            dl = lengths[di];
            if (dl < 4) out_len = 4;
            else if (dl > 8) out_len = 8;
            else out_len = dl;
            if ((dp < dl && dp < 8) ||
                (complete_q[di] === 1'b1 && dp < out_len)) begin
                data_available = 1;
                if (dp < dl && dp < 8)
                    expected_byte = bytes_q[di] >> (dp*8);
                else expected_byte = 0;
                if (complete_q[di] === 1'b1)
                    expected_last = (dp == out_len-1);
                else expected_last = (dp == 7);
            end
        end
        if (hr != iw) begin
            header_available = (complete_q[hi] === 1'b1);
            if (lengths[hi] < 4)
                expected_header = {1'b1,1'b0,16'd4,12'd0,lengths[hi]};
            else if (lengths[hi] > 8)
                expected_header = {1'b0,1'b1,16'd8,12'd0,lengths[hi]};
            else
                expected_header = {1'b0,1'b0,12'd0,lengths[hi],12'd0,lengths[hi]};
        end
        if (m_valid === 1'b1) begin
            if (!data_available || ((^expected_byte) === 1'bx) ||
                m_data !== expected_byte || m_last !== expected_last)
                check_now[0] = 0;
        end else if (m_valid !== 1'b0) check_now[0] = 0;
        if (h_valid === 1'b1) begin
            if (!header_available || ((^expected_header) === 1'bx) ||
                {h_pad,h_truncate,h_length,h_original_length} !== expected_header)
                check_now[1] = 0;
        end else if (h_valid !== 1'b0) check_now[1] = 0;
        if (ms && !reset_post) begin
            if (m_valid !== 1'b1 || {m_data,m_last} !== saved_m ||
                ((^{m_data,m_last}) === 1'bx)) check_now[2] = 0;
        end
        if (hs && !reset_post) begin
            if (h_valid !== 1'b1 ||
                {h_pad,h_truncate,h_length,h_original_length} !== saved_h ||
                ((^{h_pad,h_truncate,h_length,h_original_length}) === 1'bx))
                check_now[3] = 0;
        end
        if (reset_post && (m_valid !== 1'b0 || h_valid !== 1'b0))
            check_now[4] = 0;
        if (s_ready !== 1'b0 && s_ready !== 1'b1) check_now[4] = 0;
        if (trace_done === 1'b1) begin
            if (s_valid !== 1'b0 || m_valid !== 1'b0 || h_valid !== 1'b0 ||
                ilen != 0 || dr != iw || hr != iw || dp != 0 ||
                rst !== 1'b0) check_now[5] = 0;
        end
    end
end

assign active[0] = started;
assign active[1] = started;
assign active[2] = started;
assign active[3] = started;
assign active[4] = started;
assign active[5] = started && (trace_done === 1'b1);
assign ok = check_now & ~bad;

always @(posedge clk) begin
    if (started) bad <= bad | ~check_now;
    reset_post <= (rst === 1'b1);
    if (rst === 1'b1) begin
        started <= 1;
        iw <= 0;
        dr <= 0;
        hr <= 0;
        ilen <= 0;
        dp <= 0;
        ms <= 0;
        hs <= 0;
        for (k=0;k<64;k=k+1) begin
            lengths[k] <= 0;
            complete_q[k] <= 0;
            bytes_q[k] <= 0;
        end
    end else if (started && rst === 1'b0) begin
        ms <= (m_valid === 1'b1 && m_ready !== 1'b1);
        hs <= (h_valid === 1'b1 && h_ready !== 1'b1);
        saved_m <= {m_data,m_last};
        saved_h <= {h_pad,h_truncate,h_length,h_original_length};
        if (m_valid === 1'b1 && m_ready === 1'b1 && data_available) begin
            if (expected_last) begin
                dr <= dr+1'b1;
                dp <= 0;
            end else dp <= dp+1'b1;
        end
        if (h_valid === 1'b1 && h_ready === 1'b1 && header_available)
            hr <= hr+1'b1;
        if (s_valid === 1'b1 && s_ready === 1'b1) begin
            if (data_distance >= 64 || header_distance >= 64 || ilen >= 12 ||
                (s_last !== 1'b0 && s_last !== 1'b1) ||
                ((^s_data) === 1'bx)) begin
                bad[4] <= 1;
            end else begin
                if (ilen == 0) begin
                    bytes_q[wi] <= {56'd0,s_data};
                    complete_q[wi] <= 0;
                end else if (ilen < 8)
                    bytes_q[wi][ilen*8 +: 8] <= s_data;
                lengths[wi] <= ilen+1'b1;
                if (s_last === 1'b1) begin
                    complete_q[wi] <= 1;
                    iw <= iw+1'b1;
                    ilen <= 0;
                end else ilen <= ilen+1'b1;
            end
        end
    end else if (started) begin
        bad[4] <= 1;
    end
end

endmodule
`default_nettype wire
