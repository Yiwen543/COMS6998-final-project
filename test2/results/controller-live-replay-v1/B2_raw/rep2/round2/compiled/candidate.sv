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
reg hold_m = 1'b0, hold_h = 1'b0;
reg [8:0] saved_m = 0;
reg [33:0] saved_h = 0;
reg [63:0] bytes_q [0:63];
reg [3:0] length_q [0:63];
reg [7:0] input_seq = 0, data_seq = 0, header_seq = 0;
reg [3:0] input_length = 0, data_position = 0;
reg tracking = 1'b1;
reg [7:0] drain_tail = 0;
wire [7:0] data_distance = input_seq-data_seq;
wire [7:0] header_distance = input_seq-header_seq;
wire data_exists = data_distance != 0 || input_length != 0;
wire header_exists = header_distance != 0;
// For an unfinished frame use the live accepted-prefix length, never stale RAM.
wire [3:0] dl = data_distance != 0 ? length_q[data_seq[5:0]] : input_length;
wire dc = data_distance != 0;
wire [3:0] adjusted_dl = dl < 4 ? 4 : (dl > 8 ? 8 : dl);
wire [3:0] hl = length_q[header_seq[5:0]];
wire [15:0] adjusted_hl = hl < 4 ? 16'd4 : (hl > 8 ? 16'd8 : {12'd0,hl});
wire byte_known = data_exists && data_position < 8 &&
 ((data_position < dl) || (dc && data_position < adjusted_dl));
reg [7:0] expected_byte;
always @* begin
 expected_byte = 0;
 if (data_position < dl && data_position < 8)
  expected_byte = bytes_q[data_seq[5:0]][data_position*8 +: 8];
end
wire last_known = byte_known && (dc || data_position == 7 || data_position+1 < dl);
wire expected_last = data_position == 7 || (dc && data_position+1 == adjusted_dl);
wire drained_check = drain_tail >= 128;
wire drained = input_length == 0 && data_distance == 0 &&
 header_distance == 0 && data_position == 0 && !m_valid && !h_valid;
assign active[0] = seen && reset_edge;
assign ok[0] = !m_valid && !h_valid;
assign active[1] = seen && !reset_edge && hold_m;
assign ok[1] = m_valid && {m_last,m_data} == saved_m;
assign active[2] = seen && !reset_edge && hold_h;
assign ok[2] = h_valid && {h_pad,h_truncate,h_length,h_original_length} == saved_h;
assign active[3] = seen && !reset_edge && tracking && m_valid;
assign ok[3] = byte_known && m_data == expected_byte;
assign active[4] = seen && !reset_edge && tracking && h_valid;
assign ok[4] = header_exists && h_original_length == {12'd0,hl} &&
 h_length == adjusted_hl && h_pad == (hl < 4) && h_truncate == (hl > 8);
assign active[5] = seen && !reset_edge && tracking && (m_valid || drained_check);
assign ok[5] = (!m_valid || (byte_known && (last_known ? m_last == expected_last : !m_last))) &&
 (!drained_check || drained);
always @(posedge clk) begin
 seen <= 1'b1;
 reset_edge <= rst;
 hold_m <= !rst && m_valid && !m_ready;
 hold_h <= !rst && h_valid && !h_ready;
 saved_m <= {m_last,m_data};
 saved_h <= {h_pad,h_truncate,h_length,h_original_length};
 if (rst) begin
  input_seq <= 0;
  data_seq <= 0;
  header_seq <= 0;
  input_length <= 0;
  data_position <= 0;
  tracking <= 1'b1;
  drain_tail <= 0;
 end else begin
  if (!s_valid && m_ready && h_ready) begin
   if (drain_tail < 128) drain_tail <= drain_tail+1'b1;
  end else drain_tail <= 0;
  if (tracking) begin
   // Capacity exhaustion disables semantic history checks rather than aliasing entries.
   if (data_distance >= 63 || header_distance >= 63) tracking <= 1'b0;
   if (s_valid && s_ready) begin
    if (input_length < 8)
     bytes_q[input_seq[5:0]][input_length*8 +: 8] <= s_data;
    length_q[input_seq[5:0]] <= input_length+1'b1;
    if (s_last) begin
     input_seq <= input_seq+1'b1;
     input_length <= 0;
    end else begin
     if (input_length < 12) input_length <= input_length+1'b1;
     else tracking <= 1'b0;
    end
   end
   if (m_valid && m_ready && byte_known) begin
    if (expected_last && last_known) begin
     data_seq <= data_seq+1'b1;
     data_position <= 0;
    end else data_position <= data_position+1'b1;
   end
   if (h_valid && h_ready && header_exists)
    header_seq <= header_seq+1'b1;
  end
 end
end

endmodule
`default_nettype wire
