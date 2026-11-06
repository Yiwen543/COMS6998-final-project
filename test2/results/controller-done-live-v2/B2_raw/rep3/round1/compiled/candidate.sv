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
// Bounded, specification-level queues; neither channel depends on the other.
reg seen = 0;
reg reset_post = 0;
reg [5:0] failed = 0;
reg [8:0] bytes_q [0:255];
reg [33:0] hdr_q [0:63];
reg [15:0] bw = 0, br = 0, hw = 0, hr = 0;
reg [4:0] in_len = 0;
reg mh = 0, hh = 0;
reg [8:0] saved_m = 0;
reg [33:0] saved_h = 0;
reg [5:0] live;
wire [15:0] bn = bw-br;
wire [15:0] hn = hw-hr;
wire [33:0] hp = {h_pad,h_truncate,h_length,h_original_length};
integer k;
integer add_b;
integer length_now;
integer out_length;

always @* begin
    live = 6'b111111;
    if (seen) begin
        // Presented-valid safety is checked even without a handshake.
        if (m_valid !== 1'b0 && m_valid !== 1'b1) live[0] = 0;
        if (m_valid === 1'b1) begin
            if (bn == 0 || bn > 256) live[0] = 0;
            else if (({m_last,m_data} == bytes_q[br[7:0]]) !== 1'b1)
                live[0] = 0;
        end
        if (h_valid !== 1'b0 && h_valid !== 1'b1) live[1] = 0;
        if (h_valid === 1'b1) begin
            if (hn == 0 || hn > 64) live[1] = 0;
            else if ((hp == hdr_q[hr[5:0]]) !== 1'b1) live[1] = 0;
        end
        if (rst === 1'b0) begin
            if (mh && ((m_valid === 1'b1) &&
                (({m_last,m_data} == saved_m) === 1'b1)) !== 1'b1)
                live[2] = 0;
            if (hh && ((h_valid === 1'b1) &&
                ((hp == saved_h) === 1'b1)) !== 1'b1)
                live[2] = 0;
        end
        // This flag describes the most recently executed synchronous edge.
        if (reset_post) begin
            if (m_valid !== 1'b0 || h_valid !== 1'b0) live[3] = 0;
        end
    end
    if (trace_done === 1'b1) begin
        if (bn != 0 || hn != 0 || in_len != 0 ||
            s_valid !== 1'b0 || m_valid !== 1'b0 || h_valid !== 1'b0)
            live[5] = 0;
    end
end

assign active = {trace_done === 1'b1,seen,seen,seen,seen,seen};
assign ok = live & ~failed;

always @(posedge clk) begin
    seen <= 1;
    failed <= failed | ~live;
    reset_post <= (rst === 1'b1);
    if (rst === 1'b1) begin
        bw <= 0; br <= 0; hw <= 0; hr <= 0;
        in_len <= 0;
        mh <= 0; hh <= 0;
    end else if (rst === 1'b0) begin
        mh <= (m_valid === 1'b1 && m_ready !== 1'b1);
        hh <= (h_valid === 1'b1 && h_ready !== 1'b1);
        saved_m <= {m_last,m_data};
        saved_h <= hp;
        if (m_valid === 1'b1 && m_ready === 1'b1 && bn != 0)
            br <= br+1'b1;
        if (h_valid === 1'b1 && h_ready === 1'b1 && hn != 0)
            hr <= hr+1'b1;
        if (s_valid === 1'b1 && s_ready === 1'b1) begin
            length_now = in_len+1;
            add_b = 0;
            if (length_now <= 8) begin
                if (bn < 253) begin
                    bytes_q[bw[7:0]] <= {
                        (length_now == 8 || (s_last === 1'b1 && length_now >= 4)),s_data};
                    add_b = 1;
                    if (s_last === 1'b1 && length_now < 4) begin
                        for (k=1;k<4;k=k+1) begin
                            if (k <= 4-length_now)
                                bytes_q[(bw+k)&255] <= {(k == 4-length_now),8'd0};
                        end
                        add_b = 5-length_now;
                    end
                    bw <= bw+add_b;
                end else failed[4] <= 1;
            end
            if (s_last !== 1'b0 && s_last !== 1'b1) failed[4] <= 1;
            if ((^s_data) !== 1'b0 && (^s_data) !== 1'b1) failed[4] <= 1;
            if (length_now > 12) failed[4] <= 1;
            if (s_last === 1'b1) begin
                in_len <= 0;
                out_length = length_now < 4 ? 4 : (length_now > 8 ? 8 : length_now);
                if (hn < 64) begin
                    hdr_q[hw[5:0]] <= { (length_now < 4), (length_now > 8),
                        16'(out_length),16'(length_now)};
                    hw <= hw+1'b1;
                end else failed[4] <= 1;
            end else if (in_len < 31) in_len <= in_len+1'b1;
        end
        if (s_valid !== 1'b0 && s_valid !== 1'b1) failed[4] <= 1;
        if (s_valid === 1'b1 && s_ready !== 1'b0 && s_ready !== 1'b1)
            failed[4] <= 1;
        if (m_valid === 1'b1 && m_ready !== 1'b0 && m_ready !== 1'b1)
            failed[4] <= 1;
        if (h_valid === 1'b1 && h_ready !== 1'b0 && h_ready !== 1'b1)
            failed[4] <= 1;
    end else failed[4] <= 1;
end

endmodule
`default_nettype wire
