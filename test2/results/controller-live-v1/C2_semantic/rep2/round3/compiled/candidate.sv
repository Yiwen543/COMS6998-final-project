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
reg started = 0, reset_edge = 0;
reg [5:0] bad = 0;
reg [7:0] wr_seq = 0, data_seq = 0, hdr_seq = 0;
reg [3:0] in_len = 0, data_pos = 0;
reg [63:0] frame_bytes [0:63];
reg [3:0] frame_len [0:63];
reg tracking = 1;
reg m_hold = 0, h_hold = 0;
reg [7:0] held_data = 0;
reg held_last = 0;
reg [33:0] held_header = 0;
reg [5:0] enable_check, pass_check;
reg data_exists, data_complete, byte_known;
reg [7:0] data_distance;
reg [3:0] known_len, adjusted_len;
reg [7:0] expected_byte;
reg expected_last;
reg [3:0] status_len, status_adjusted;
integer k;
initial begin
    for (k=0; k<64; k=k+1) begin
        frame_bytes[k] = 0;
        frame_len[k] = 0;
    end
end

always @* begin
    data_distance = wr_seq - data_seq;
    data_complete = (data_distance != 0) && (data_distance < 64);
    data_exists = data_complete || ((data_seq == wr_seq) && (in_len != 0));
    known_len = data_complete ? frame_len[data_seq[5:0]] :
                ((data_seq == wr_seq) ? in_len : 4'd0);
    adjusted_len = known_len < 4 ? 4 : (known_len > 8 ? 8 : known_len);
    byte_known = data_exists && ((data_pos < known_len && data_pos < 8) ||
                  (data_complete && data_pos < adjusted_len));
    expected_byte = 0;
    if (data_pos < known_len && data_pos < 8)
        expected_byte = frame_bytes[data_seq[5:0]][data_pos*8 +: 8];
    expected_last = data_complete ? (data_pos == adjusted_len-1) : (data_pos == 7);
    status_len = frame_len[hdr_seq[5:0]];
    status_adjusted = status_len < 4 ? 4 : (status_len > 8 ? 8 : status_len);

    enable_check = 0;
    pass_check = 6'b111111;
    enable_check[0] = started && reset_edge;
    pass_check[0] = !m_valid && !h_valid;
    enable_check[1] = started && !reset_edge && tracking && m_valid;
    pass_check[1] = byte_known && (m_data == expected_byte);
    enable_check[2] = started && !reset_edge && tracking && m_valid;
    pass_check[2] = byte_known && (m_last == expected_last);
    enable_check[3] = started && !reset_edge && tracking && h_valid;
    pass_check[3] = (hdr_seq != wr_seq) &&
                    (h_original_length == {12'b0,status_len}) &&
                    (h_length == {12'b0,status_adjusted}) &&
                    (h_pad == (status_len < 4)) &&
                    (h_truncate == (status_len > 8));
    enable_check[4] = started && !reset_edge && m_hold;
    pass_check[4] = m_valid && (m_data == held_data) && (m_last == held_last);
    enable_check[5] = started && !reset_edge && h_hold;
    pass_check[5] = h_valid &&
        ({h_pad,h_truncate,h_length,h_original_length} == held_header);
end
assign active = enable_check | bad;
assign ok = pass_check & ~bad;

always @(posedge clk) begin
    bad <= bad | (enable_check & ~pass_check);
    reset_edge <= rst;
    if (rst) begin
        started <= 1;
        wr_seq <= 0;
        data_seq <= 0;
        hdr_seq <= 0;
        in_len <= 0;
        data_pos <= 0;
        tracking <= 1;
        m_hold <= 0;
        h_hold <= 0;
    end else begin
        m_hold <= m_valid && !m_ready;
        h_hold <= h_valid && !h_ready;
        held_data <= m_data;
        held_last <= m_last;
        held_header <= {h_pad,h_truncate,h_length,h_original_length};
        if (started && tracking) begin
            if (s_valid && s_ready) begin
                if (in_len < 8)
                    frame_bytes[wr_seq[5:0]][in_len*8 +: 8] <= s_data;
                frame_len[wr_seq[5:0]] <= in_len + 1'b1;
                if (s_last) begin
                    wr_seq <= wr_seq + 1'b1;
                    in_len <= 0;
                    if (((wr_seq + 8'd1 - data_seq) >= 64) ||
                        ((wr_seq + 8'd1 - hdr_seq) >= 64))
                        tracking <= 0;
                end else begin
                    in_len <= in_len + 1'b1;
                end
            end
            if (m_valid && m_ready && byte_known) begin
                if (expected_last) begin
                    data_seq <= data_seq + 1'b1;
                    data_pos <= 0;
                end else begin
                    data_pos <= data_pos + 1'b1;
                end
            end
            if (h_valid && h_ready && hdr_seq != wr_seq)
                hdr_seq <= hdr_seq + 1'b1;
        end
    end
end

endmodule
`default_nettype wire
