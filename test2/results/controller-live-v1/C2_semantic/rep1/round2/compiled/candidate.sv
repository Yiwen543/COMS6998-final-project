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
output wire [5:0] active,ok);
reg seen = 1'b0;
reg reset_edge = 1'b0;
reg tracked = 1'b1;
reg [7:0] bytes_q [0:255];
reg lasts_q [0:255];
reg [15:0] lengths_q [0:127];
reg [7:0] bw = 0, br = 0;
reg [6:0] hw = 0, hr = 0;
reg [8:0] bc = 0;
reg [7:0] hc = 0;
reg [15:0] input_pos = 0;
reg ms = 0, hs = 0;
reg [8:0] held_m = 0;
reg [33:0] held_h = 0;
integer added;
integer k;
integer idx;
wire take_s = s_valid && s_ready && !rst;
wire take_m = m_valid && m_ready && !rst;
wire take_h = h_valid && h_ready && !rst;
wire enabled = seen && tracked;
wire [15:0] expected_original = lengths_q[hr];
wire [15:0] expected_length = expected_original < 4 ? 16'd4 : (expected_original > 8 ? 16'd8 : expected_original);

// All expectations come from accepted public input transactions.
// Neither response queue is advanced by the other response channel.
assign active[0] = seen && reset_edge;
assign ok[0] = !m_valid && !h_valid;
assign active[1] = enabled && m_valid;
assign ok[1] = (bc != 0) && (m_data == bytes_q[br]);
assign active[2] = enabled && m_valid;
assign ok[2] = (bc != 0) && (m_last == lasts_q[br]);
assign active[3] = enabled && h_valid;
assign ok[3] = (hc != 0) &&
    (h_original_length == expected_original) &&
    (h_length == expected_length) &&
    (h_pad == (expected_original < 4)) &&
    (h_truncate == (expected_original > 8));
assign active[4] = seen && ms && !reset_edge;
assign ok[4] = m_valid && ({m_data,m_last} == held_m);
assign active[5] = seen && hs && !reset_edge;
assign ok[5] = h_valid &&
    ({h_pad,h_truncate,h_length,h_original_length} == held_h);

always @(posedge clk) begin
    seen <= 1'b1;
    reset_edge <= rst;
    ms <= !rst && m_valid && !m_ready;
    hs <= !rst && h_valid && !h_ready;
    held_m <= {m_data,m_last};
    held_h <= {h_pad,h_truncate,h_length,h_original_length};
    if (rst) begin
        bw <= 0;
        br <= 0;
        hw <= 0;
        hr <= 0;
        bc <= 0;
        hc <= 0;
        input_pos <= 0;
        tracked <= 1'b1;
    end else if (tracked) begin
        added = 0;
        if (take_s) begin
            if (input_pos < 8) begin
                bytes_q[bw] <= s_data;
                lasts_q[bw] <= (input_pos == 7) || (s_last && input_pos >= 3);
                added = 1;
            end
            if (s_last && input_pos < 3) begin
                for (k = 1; k <= 3; k = k+1) begin
                    if (k <= 3-input_pos) begin
                        idx = (bw+k) & 255;
                        bytes_q[idx] <= 8'd0;
                        lasts_q[idx] <= (k == 3-input_pos);
                    end
                end
                added = 4-input_pos;
            end
            if (s_last) begin
                lengths_q[hw] <= input_pos+16'd1;
                hw <= hw+1'b1;
                input_pos <= 0;
            end else begin
                input_pos <= input_pos+16'd1;
            end
        end
        bw <= bw+added;
        if (take_m && bc != 0) br <= br+1'b1;
        bc <= bc+added-((take_m && bc != 0) ? 1 : 0);
        if (take_h && hc != 0) hr <= hr+1'b1;
        case ({(take_s && s_last),(take_h && hc != 0)})
            2'b10: hc <= hc+1'b1;
            2'b01: hc <= hc-1'b1;
            default: hc <= hc;
        endcase
        // Observation-budget exhaustion is not itself a DUT fault.
        // Stop using overwritten expectations until the next reset.
        if (bc+added-((take_m && bc != 0) ? 1 : 0) > 256)
            tracked <= 1'b0;
        if (take_s && s_last && hc == 128 && !(take_h && hc != 0))
            tracked <= 1'b0;
    end
end

endmodule
`default_nettype wire
