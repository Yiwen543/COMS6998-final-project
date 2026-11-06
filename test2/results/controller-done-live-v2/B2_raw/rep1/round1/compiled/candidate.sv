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
// Independent specification queues; no DUT implementation state is modeled.
reg armed = 0;
reg reset_post = 0;
reg [5:0] saved_ok = 6'b111111;
reg [7:0] bytes_q [0:127];
reg lasts_q [0:127];
reg [33:0] headers_q [0:31];
reg [6:0] bw = 0, br = 0;
reg [5:0] bc = 0;
reg [4:0] hw = 0, hr = 0;
reg [5:0] hc = 0;
reg [3:0] in_len = 0;
reg overflow = 0;
reg ms = 0, hs = 0, ss = 0;
reg [8:0] mp;
reg [33:0] hp;
reg [8:0] sp;
reg [7:0] tail = 0;
reg [5:0] check_now;
integer k;
integer add_bytes;
integer out_length;
reg [7:0] next_count;
wire [33:0] header_now = {h_pad,h_truncate,h_length,h_original_length};
wire [8:0] data_now = {m_last,m_data};
wire [8:0] source_now = {s_last,s_data};

always @* begin
    check_now = 6'b111111;
    if (armed) begin
        // Presented responses are checked even when their ready is low.
        check_now[0] = ((m_valid == 0) || (m_valid == 1));
        if (m_valid !== 1'b0) begin
            if (bc == 0) check_now[0] = (m_valid == 0);
            else check_now[0] = check_now[0] &
                (m_data == bytes_q[br]) & (m_last == lasts_q[br]);
        end
        check_now[1] = ((h_valid == 0) || (h_valid == 1));
        if (h_valid !== 1'b0) begin
            if (hc == 0) check_now[1] = (h_valid == 0);
            else check_now[1] = check_now[1] & (header_now == headers_q[hr]);
        end
        if (!reset_post && rst !== 1'b1) begin
            if (ms) check_now[2] = check_now[2] & (m_valid == 1) & (data_now == mp);
            if (hs) check_now[2] = check_now[2] & (h_valid == 1) & (header_now == hp);
        end
        if (reset_post) begin
            check_now[3] = (m_valid == 0) & (h_valid == 0);
        end
        check_now[4] = ((rst == 0) || (rst == 1)) &
                      ((s_valid == 0) || (s_valid == 1)) &
                      ((s_ready == 0) || (s_ready == 1)) &
                      ((m_ready == 0) || (m_ready == 1)) &
                      ((h_ready == 0) || (h_ready == 1));
        if (rst === 1'b1) check_now[4] = check_now[4] & (s_valid == 0);
        if (rst !== 1'b1 && ss)
            check_now[4] = check_now[4] & (s_valid == 1) & (source_now == sp);
        if (rst === 1'b0 && s_valid === 1'b1 && s_ready === 1'b1) begin
            check_now[4] = check_now[4] & ((s_last == 0) || (s_last == 1)) &
                          ((^s_data) == (^s_data));
            if (in_len == 11) check_now[4] = check_now[4] & (s_last == 1);
        end
        if (overflow) check_now[5] = 1'bx;
        if (trace_done === 1'b1) begin
            check_now[5] = check_now[5] & (rst == 0) & (s_valid == 0) &
                (m_valid == 0) & (h_valid == 0) & (in_len == 0) &
                (bc == 0) & (hc == 0);
            // A short quiet tail does not establish finite completion.
            if (tail < 32 && check_now[5] !== 1'b0) check_now[5] = 1'bx;
        end
    end
end
assign active = {6{armed}};
assign ok = saved_ok & check_now;

always @(posedge clk) begin
    armed <= 1'b1;
    saved_ok <= saved_ok & check_now;
    reset_post <= (rst === 1'b1);
    if (rst === 1'b1) begin
        bw <= 0; br <= 0; bc <= 0;
        hw <= 0; hr <= 0; hc <= 0;
        in_len <= 0;
        ms <= 0; hs <= 0; ss <= 0;
        tail <= 0;
        overflow <= 0;
    end else if (rst === 1'b0) begin
        ms <= (m_valid === 1'b1 && m_ready === 1'b0);
        hs <= (h_valid === 1'b1 && h_ready === 1'b0);
        ss <= (s_valid === 1'b1 && s_ready === 1'b0);
        mp <= data_now;
        hp <= header_now;
        sp <= source_now;
        if (s_valid === 1'b0 && m_ready === 1'b1 && h_ready === 1'b1) begin
            if (tail != 255) tail <= tail + 1'b1;
        end else tail <= 0;
        add_bytes = 0;
        if (s_valid === 1'b1 && s_ready === 1'b1) begin
            if (in_len < 8) add_bytes = 1;
            if (s_last === 1'b1 && in_len < 3) add_bytes = 4-in_len;
            if (bc + add_bytes <= 63) begin
                if (in_len < 8) begin
                    bytes_q[bw] <= s_data;
                    lasts_q[bw] <= (in_len == 7) ? 1'b1 :
                        ((in_len >= 3) ? s_last : 1'b0);
                end
                for (k=1; k<4; k=k+1) begin
                    if (k < add_bytes) begin
                        bytes_q[(bw+k)&127] <= 0;
                        lasts_q[(bw+k)&127] <= (k == add_bytes-1);
                    end
                end
                bw <= bw + add_bytes;
            end else overflow <= 1;
            if (s_last === 1'b1) begin
                out_length = in_len+1;
                if (out_length < 4) out_length = 4;
                if (out_length > 8) out_length = 8;
                if (hc < 32) begin
                    headers_q[hw] <= { (in_len < 3), (in_len >= 8),
                        16'(out_length), 16'(in_len+1) };
                    hw <= hw + 1'b1;
                end else overflow <= 1;
                in_len <= 0;
            end else if (in_len < 12) in_len <= in_len + 1'b1;
            else overflow <= 1;
        end
        next_count = bc + add_bytes;
        if (m_valid === 1'b1 && m_ready === 1'b1 && bc != 0) begin
            br <= br + 1'b1;
            next_count = next_count - 1;
        end
        if (next_count <= 63) bc <= next_count[5:0];
        else overflow <= 1;
        case ({(s_valid === 1'b1 && s_ready === 1'b1 && s_last === 1'b1),
               (h_valid === 1'b1 && h_ready === 1'b1 && hc != 0)})
            2'b10: if (hc < 32) hc <= hc+1'b1;
            2'b01: hc <= hc-1'b1;
            default: hc <= hc;
        endcase
        if (h_valid === 1'b1 && h_ready === 1'b1 && hc != 0) hr <= hr+1'b1;
    end else begin
        saved_ok <= saved_ok & check_now & 6'bxxxxxx;
    end
end

endmodule
`default_nettype wire
