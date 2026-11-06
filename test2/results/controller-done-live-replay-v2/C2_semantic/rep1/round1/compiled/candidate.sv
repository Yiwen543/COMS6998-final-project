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
// Bounded public-pin scoreboard. Queue heads describe presented beats,
// not merely beats for which the consumer happens to be ready.
reg seen = 0;
reg reset_edge = 0;
reg [5:0] failed = 0;
reg [7:0] data_q [0:127];
reg last_q [0:127];
reg [6:0] dw = 0, dr = 0;
reg [7:0] dc = 0;
reg [33:0] hdr_q [0:31];
reg [4:0] hw = 0, hr = 0;
reg [5:0] hc = 0;
reg [3:0] in_len = 0;
reg hold_m = 0, hold_h = 0, hold_s = 0;
reg [8:0] saved_m = 0;
reg [33:0] saved_h = 0;
reg [8:0] saved_s = 0;
reg [7:0] tail = 0;
reg [5:0] bad;
integer k;
integer add_data;
integer length_now;
reg [15:0] adjusted;
wire take_s = (rst === 1'b0) && (s_valid === 1'b1) && (s_ready === 1'b1);
wire take_m = (rst === 1'b0) && (m_valid === 1'b1) && (m_ready === 1'b1);
wire take_h = (rst === 1'b0) && (h_valid === 1'b1) && (h_ready === 1'b1);
wire [33:0] header_value = {h_pad,h_truncate,h_length,h_original_length};

always @* begin
    length_now = in_len + 1;
    add_data = 0;
    adjusted = 16'd8;
    if (length_now < 4) adjusted = 16'd4;
    else if (length_now <= 8) adjusted = length_now;
    if (take_s) begin
        if (in_len < 8) add_data = 1;
        if ((s_last === 1'b1) && (length_now < 4))
            add_data = 5-length_now;
    end
end

always @* begin
    bad = 0;
    if (seen) begin
        // Known controls are required even when payload is disabled.
        if (((rst !== 1'b0) && (rst !== 1'b1)) ||
            ((s_valid !== 1'b0) && (s_valid !== 1'b1)) ||
            ((s_ready !== 1'b0) && (s_ready !== 1'b1)) ||
            ((m_ready !== 1'b0) && (m_ready !== 1'b1)) ||
            ((h_ready !== 1'b0) && (h_ready !== 1'b1)) ||
            ((m_valid !== 1'b0) && (m_valid !== 1'b1)) ||
            ((h_valid !== 1'b0) && (h_valid !== 1'b1))) bad[4] = 1;
        if (s_valid === 1'b1) begin
            if ((^s_data === 1'bx) ||
                ((s_last !== 1'b0) && (s_last !== 1'b1))) bad[4] = 1;
            if (rst === 1'b1) bad[4] = 1;
        end
        if ((rst === 1'b0) && hold_s &&
            ((s_valid !== 1'b1) || ({s_last,s_data} !== saved_s))) bad[4] = 1;
        if (reset_edge) begin
            if ((m_valid !== 1'b0) || (h_valid !== 1'b0)) bad[3] = 1;
        end else begin
            if (m_valid === 1'b1) begin
                if (dc == 0) begin
                    bad[0] = 1;
                    bad[1] = 1;
                end else begin
                    if ((^m_data === 1'bx) || (m_data !== data_q[dr])) bad[0] = 1;
                    if (((m_last !== 1'b0) && (m_last !== 1'b1)) ||
                        (m_last !== last_q[dr])) bad[1] = 1;
                end
            end
            if (h_valid === 1'b1) begin
                if ((hc == 0) || (^header_value === 1'bx)) bad[2] = 1;
                else if (header_value !== hdr_q[hr]) bad[2] = 1;
            end
            if (rst === 1'b0) begin
                if (hold_m && ((m_valid !== 1'b1) ||
                    ({m_last,m_data} !== saved_m))) bad[3] = 1;
                if (hold_h && ((h_valid !== 1'b1) ||
                    (header_value !== saved_h))) bad[3] = 1;
            end
        end
        if (take_s && (length_now > 12)) bad[4] = 1;
        // Exhaustion never silently overwrites a live obligation.
        if (take_s && (dc + add_data > 128)) bad[4] = 1;
        if (take_s && (s_last === 1'b1) && (hc == 32) && !take_h) bad[4] = 1;
    end
end

always @(posedge clk) begin
    seen <= 1;
    failed <= failed | bad;
    reset_edge <= (rst === 1'b1);
    if (rst === 1'b1) begin
        dw <= 0; dr <= 0; dc <= 0;
        hw <= 0; hr <= 0; hc <= 0;
        in_len <= 0;
        hold_m <= 0; hold_h <= 0; hold_s <= 0;
        tail <= 0;
    end else if (rst === 1'b0) begin
        hold_m <= (m_valid === 1'b1) && (m_ready === 1'b0);
        hold_h <= (h_valid === 1'b1) && (h_ready === 1'b0);
        hold_s <= (s_valid === 1'b1) && (s_ready === 1'b0);
        saved_m <= {m_last,m_data};
        saved_h <= header_value;
        saved_s <= {s_last,s_data};
        if ((s_valid === 1'b0) && (m_ready === 1'b1) && (h_ready === 1'b1)) begin
            if (tail < 128) tail <= tail + 1'b1;
        end else tail <= 0;
        if (take_s) begin
            if (in_len < 8) begin
                data_q[dw] <= s_data;
                last_q[dw] <= (in_len == 7) || ((s_last === 1'b1) && (length_now >= 4));
            end
            if ((s_last === 1'b1) && (length_now < 4)) begin
                for (k=1; k<4; k=k+1) begin
                    if (k <= 4-length_now) begin
                        data_q[(dw+k)&127] <= 0;
                        last_q[(dw+k)&127] <= (k == 4-length_now);
                    end
                end
            end
            dw <= dw + add_data;
            if (s_last === 1'b1) begin
                hdr_q[hw] <= { (length_now < 4), (length_now > 8), adjusted, 16'(length_now) };
                hw <= hw + 1'b1;
                in_len <= 0;
            end else if (in_len < 15) in_len <= in_len + 1'b1;
        end
        if (take_m && (dc != 0)) dr <= dr + 1'b1;
        if (take_h && (hc != 0)) hr <= hr + 1'b1;
        dc <= dc + add_data - ((take_m && (dc != 0)) ? 1 : 0);
        hc <= hc + ((take_s && (s_last === 1'b1)) ? 1 : 0)
                 - ((take_h && (hc != 0)) ? 1 : 0);
    end
end

wire end_bad = (dc != 0) || (hc != 0) || (in_len != 0) ||
               (s_valid !== 1'b0) || (m_valid !== 1'b0) || (h_valid !== 1'b0) ||
               (rst !== 1'b0) || (m_ready !== 1'b1) || (h_ready !== 1'b1) ||
               (tail < 32);
assign active[4:0] = {5{seen}};
assign active[5] = (trace_done === 1'b1);
assign ok[4:0] = ~(failed[4:0] | bad[4:0]);
// No clock is required after the final-post marker.
assign ok[5] = !end_bad;

endmodule
`default_nettype wire
