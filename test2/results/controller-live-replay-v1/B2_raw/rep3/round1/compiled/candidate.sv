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
reg past_reset = 1'b0;
reg hold_m = 1'b0, hold_h = 1'b0;
reg [8:0] saved_m = 0;
reg [33:0] saved_h = 0;
reg tracking = 1'b1;
reg [63:0] bytes_q [0:63];
reg [3:0] lengths [0:63];
reg complete_q [0:63];
reg live_m [0:63];
reg live_h [0:63];
reg [5:0] wr = 0, rd_m = 0, rd_h = 0;
reg [3:0] in_pos = 0, out_pos = 0;
reg [7:0] quiet = 0;
integer i;
reg justified;
reg expected_last;
reg [7:0] expected_byte;
reg [3:0] adjusted_m, adjusted_h;
reg drained;
initial begin
    for (i=0; i<64; i=i+1) begin
        bytes_q[i] = 0;
        lengths[i] = 0;
        complete_q[i] = 0;
        live_m[i] = 0;
        live_h[i] = 0;
    end
end

always @* begin
    adjusted_m = lengths[rd_m];
    if (lengths[rd_m] < 4) adjusted_m = 4;
    else if (lengths[rd_m] > 8) adjusted_m = 8;
    adjusted_h = lengths[rd_h];
    if (lengths[rd_h] < 4) adjusted_h = 4;
    else if (lengths[rd_h] > 8) adjusted_h = 8;
    justified = 1'b0;
    expected_byte = 0;
    expected_last = 1'b0;
    if (live_m[rd_m] && out_pos < 8) begin
        if (out_pos < lengths[rd_m]) begin
            justified = 1'b1;
            expected_byte = bytes_q[rd_m][out_pos*8 +: 8];
        end else if (complete_q[rd_m] && out_pos < adjusted_m) begin
            justified = 1'b1;
            expected_byte = 0;
        end
        if (complete_q[rd_m]) begin
            if (out_pos >= adjusted_m) justified = 1'b0;
            expected_last = (out_pos == adjusted_m-1);
        end else begin
            expected_last = (out_pos == 7);
        end
    end
    drained = (in_pos == 0);
    for (integer k=0; k<64; k=k+1)
        if (live_m[k] || live_h[k]) drained = 1'b0;
end

assign active[0] = seen && (past_reset || (tracking && quiet == 128));
assign ok[0] = past_reset ? (!m_valid && !h_valid && !s_ready) :
                            (drained && !m_valid && !h_valid);
assign active[1] = seen && hold_m;
assign ok[1] = m_valid && ({m_last,m_data} == saved_m);
assign active[2] = seen && hold_h;
assign ok[2] = h_valid && ({h_pad,h_truncate,h_length,h_original_length} == saved_h);
assign active[3] = seen && tracking && !past_reset && m_valid;
assign ok[3] = justified && (m_data == expected_byte);
assign active[4] = seen && tracking && !past_reset && m_valid;
assign ok[4] = justified && (m_last == expected_last);
assign active[5] = seen && tracking && !past_reset && h_valid;
assign ok[5] = live_h[rd_h] && complete_q[rd_h] &&
               (h_original_length == {12'b0,lengths[rd_h]}) &&
               (h_length == {12'b0,adjusted_h}) &&
               (h_pad == (lengths[rd_h] < 4)) &&
               (h_truncate == (lengths[rd_h] > 8));

always @(posedge clk) begin
    seen <= 1'b1;
    past_reset <= rst;
    hold_m <= !rst && m_valid && !m_ready;
    hold_h <= !rst && h_valid && !h_ready;
    saved_m <= {m_last,m_data};
    saved_h <= {h_pad,h_truncate,h_length,h_original_length};
    if (rst) begin
        tracking <= 1'b1;
        wr <= 0;
        rd_m <= 0;
        rd_h <= 0;
        in_pos <= 0;
        out_pos <= 0;
        quiet <= 0;
        for (integer j=0; j<64; j=j+1) begin
            lengths[j] <= 0;
            complete_q[j] <= 0;
            live_m[j] <= 0;
            live_h[j] <= 0;
        end
    end else begin
        if (!s_valid && m_ready && h_ready) begin
            if (quiet < 128) quiet <= quiet + 1'b1;
        end else quiet <= 0;
        if (tracking) begin
            if (m_valid && m_ready) begin
                if (m_last) begin
                    live_m[rd_m] <= 0;
                    rd_m <= rd_m + 1'b1;
                    out_pos <= 0;
                end else if (out_pos < 15) out_pos <= out_pos + 1'b1;
            end
            if (h_valid && h_ready) begin
                live_h[rd_h] <= 0;
                rd_h <= rd_h + 1'b1;
            end
            if (s_valid && s_ready) begin
                if (in_pos == 0) begin
                    if (live_m[wr] || live_h[wr]) tracking <= 0;
                    live_m[wr] <= 1;
                    live_h[wr] <= 1;
                    complete_q[wr] <= 0;
                end
                if (in_pos < 8) bytes_q[wr][in_pos*8 +: 8] <= s_data;
                lengths[wr] <= in_pos + 1'b1;
                if (s_last) begin
                    complete_q[wr] <= 1;
                    wr <= wr + 1'b1;
                    in_pos <= 0;
                end else if (in_pos < 14) in_pos <= in_pos + 1'b1;
            end
        end
    end
end

endmodule
`default_nettype wire
