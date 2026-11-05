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
reg seen = 0;
reg reset_edge = 0;
reg tracking = 1;
reg [6:0] wr = 0, dr = 0, hr = 0;
reg [15:0] lengths [0:63];
reg finished [0:63];
reg [63:0] bytes_q [0:63];
reg [3:0] out_pos = 0;
reg hold_m = 0, hold_h = 0;
reg [8:0] saved_m = 0;
reg [33:0] saved_h = 0;
reg [7:0] tail = 0;
integer i;
initial begin
    for (i=0; i<64; i=i+1) begin
        lengths[i] = 0;
        finished[i] = 0;
        bytes_q[i] = 0;
    end
end

wire [15:0] dl = lengths[dr[5:0]];
wire dc = finished[dr[5:0]];
wire [15:0] adjusted_dl = dl < 4 ? 16'd4 : (dl > 8 ? 16'd8 : dl);
wire data_exists = (dr != wr) || (lengths[wr[5:0]] != 0);
wire byte_known = data_exists && ((out_pos < dl && out_pos < 8) ||
                         (dc && out_pos >= dl && out_pos < 4));
wire [7:0] expected_byte = out_pos < dl ?
                          (bytes_q[dr[5:0]] >> (out_pos*8)) : 8'b0;
wire expected_last = dc ? (out_pos == adjusted_dl-1) : (out_pos == 7);
wire [15:0] hl = lengths[hr[5:0]];
wire [15:0] expected_hlen = hl < 4 ? 16'd4 : (hl > 8 ? 16'd8 : hl);
wire pending_header = hr != wr;

assign active[0] = seen && reset_edge;
assign ok[0] = !m_valid && !h_valid;
assign active[1] = seen && tracking && m_valid;
assign ok[1] = byte_known && m_data == expected_byte;
assign active[2] = seen && tracking && m_valid;
assign ok[2] = byte_known && m_last == expected_last;
assign active[3] = seen && tracking && h_valid;
assign ok[3] = pending_header && finished[hr[5:0]] &&
               h_original_length == hl && h_length == expected_hlen &&
               h_pad == (hl < 4) && h_truncate == (hl > 8);
assign active[4] = seen && !reset_edge && (hold_m || hold_h);
assign ok[4] = (!hold_m || (m_valid && {m_last,m_data} == saved_m)) &&
               (!hold_h || (h_valid && {h_pad,h_truncate,h_length,h_original_length} == saved_h));
assign active[5] = seen && tracking && !rst && tail >= 128 &&
                   !s_valid && m_ready && h_ready;
assign ok[5] = !data_exists && !pending_header && !m_valid && !h_valid;

always @(posedge clk) begin
    seen <= 1;
    reset_edge <= rst;
    if (rst) begin
        wr <= 0;
        dr <= 0;
        hr <= 0;
        out_pos <= 0;
        tracking <= 1;
        hold_m <= 0;
        hold_h <= 0;
        tail <= 0;
        for (i=0; i<64; i=i+1) begin
            lengths[i] <= 0;
            finished[i] <= 0;
            bytes_q[i] <= 0;
        end
    end else begin
        hold_m <= m_valid && !m_ready;
        hold_h <= h_valid && !h_ready;
        saved_m <= {m_last,m_data};
        saved_h <= {h_pad,h_truncate,h_length,h_original_length};
        if (!s_valid && m_ready && h_ready) begin
            if (tail != 255) tail <= tail + 1'b1;
        end else tail <= 0;
        if (s_valid && s_ready && tracking) begin
            if (lengths[wr[5:0]] < 8)
                bytes_q[wr[5:0]][lengths[wr[5:0]]*8 +: 8] <= s_data;
            lengths[wr[5:0]] <= lengths[wr[5:0]] + 1'b1;
            if (s_last) begin
                finished[wr[5:0]] <= 1;
                wr <= wr + 1'b1;
                lengths[(wr+1'b1) & 7'd63] <= 0;
                finished[(wr+1'b1) & 7'd63] <= 0;
                bytes_q[(wr+1'b1) & 7'd63] <= 0;
                if ((wr-dr == 7'd62) || (wr-hr == 7'd62)) tracking <= 0;
            end
        end
        if (m_valid && m_ready && tracking) begin
            if (m_last) begin
                dr <= dr + 1'b1;
                out_pos <= 0;
            end else if (out_pos != 15) out_pos <= out_pos + 1'b1;
        end
        if (h_valid && h_ready && tracking) hr <= hr + 1'b1;
    end
end

endmodule
`default_nettype wire
