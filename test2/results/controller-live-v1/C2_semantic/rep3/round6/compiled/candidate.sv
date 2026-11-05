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
reg seen=0, reset_edge=0, epoch=0, tracking=1;
reg [15:0] wr_frame=0, data_frame=0, hdr_frame=0;
reg [3:0] input_length=0, data_offset=0;
reg [63:0] frame_bytes [0:63];
reg [3:0] frame_length [0:63];
reg data_hold=0, hdr_hold=0;
reg [8:0] held_data=0;
reg [33:0] held_header=0;
reg [7:0] quiet_tail=0;
wire [33:0] header_now={h_pad,h_truncate,h_length,h_original_length};
wire input_fire=s_valid && s_ready && !rst;
wire data_fire=m_valid && m_ready && !rst;
wire hdr_fire=h_valid && h_ready && !rst;
wire [15:0] data_distance=wr_frame-data_frame;
wire [15:0] hdr_distance=wr_frame-hdr_frame;
wire completed_data_frame=(data_distance!=0) && !data_distance[15];
wire current_data_frame=(data_frame==wr_frame);
wire data_available=completed_data_frame || (current_data_frame && input_length!=0);
wire [3:0] known_length=completed_data_frame ? frame_length[data_frame[5:0]] : input_length;
wire [3:0] adjusted_length=known_length<4 ? 4 : (known_length>8 ? 8 : known_length);
wire byte_justified=data_available && data_offset<8 &&
 ((data_offset<known_length) || (completed_data_frame && data_offset<4));
wire [7:0] expected_byte=data_offset<known_length ?
 (frame_bytes[data_frame[5:0]] >> (data_offset*8)) : 8'd0;
wire expected_last=(data_offset==7) ||
 (completed_data_frame && data_offset==adjusted_length-1);
wire status_available=(hdr_distance!=0) && !hdr_distance[15];
wire [3:0] status_length=frame_length[hdr_frame[5:0]];
wire [15:0] status_adjusted=status_length<4 ? 16'd4 :
 (status_length>8 ? 16'd8 : {12'd0,status_length});
wire tail_check=quiet_tail>=128;
wire data_drained=(input_length==0) && (data_frame==wr_frame) && !m_valid;
wire status_drained=(hdr_frame==wr_frame) && !h_valid;
assign active[0]=seen && reset_edge;
assign ok[0]=!m_valid && !h_valid;
assign active[1]=seen && epoch && !reset_edge && data_hold;
assign ok[1]=m_valid && ({m_last,m_data}==held_data);
assign active[2]=seen && epoch && !reset_edge && hdr_hold;
assign ok[2]=h_valid && (header_now==held_header);
assign active[3]=seen && epoch && tracking && !reset_edge && (m_valid || tail_check);
assign ok[3]=(!m_valid || byte_justified) && (!tail_check || data_drained);
assign active[4]=seen && epoch && tracking && !reset_edge && m_valid && byte_justified;
assign ok[4]=(m_data==expected_byte) && (m_last==expected_last);
assign active[5]=seen && epoch && tracking && !reset_edge && (h_valid || tail_check);
assign ok[5]=(!tail_check || status_drained) && (!h_valid ||
 (status_available && (h_original_length=={12'd0,status_length}) &&
 (h_length==status_adjusted) && (h_pad==(status_length<4)) &&
 (h_truncate==(status_length>8))));
always @(posedge clk) begin
 seen<=1;
 reset_edge<=rst;
 if (rst) begin
  epoch<=1;
  tracking<=1;
  wr_frame<=0;
  data_frame<=0;
  hdr_frame<=0;
  input_length<=0;
  data_offset<=0;
  data_hold<=0;
  hdr_hold<=0;
  quiet_tail<=0;
 end else begin
  data_hold<=m_valid && !m_ready;
  hdr_hold<=h_valid && !h_ready;
  held_data<={m_last,m_data};
  held_header<=header_now;
  if (s_valid || !m_ready || !h_ready) quiet_tail<=0;
  else if (quiet_tail<255) quiet_tail<=quiet_tail+1'b1;
  if (epoch && tracking) begin
   // Disable bounded scoreboarding before live storage can alias.
   if ((!data_distance[15] && data_distance>=63) ||
       (!hdr_distance[15] && hdr_distance>=63)) tracking<=0;
   if (input_fire) begin
    if (input_length<8)
     frame_bytes[wr_frame[5:0]][input_length*8 +: 8]<=s_data;
    if (s_last) begin
     frame_length[wr_frame[5:0]]<=input_length+1'b1;
     wr_frame<=wr_frame+1'b1;
     input_length<=0;
    end else if (input_length<12) input_length<=input_length+1'b1;
    else tracking<=0;
   end
   // Response readers retire independently and only on transfers.
   if (data_fire && byte_justified) begin
    if (expected_last) begin
     data_frame<=data_frame+1'b1;
     data_offset<=0;
    end else data_offset<=data_offset+1'b1;
   end
   if (hdr_fire && status_available) hdr_frame<=hdr_frame+1'b1;
  end
 end
end

endmodule
`default_nettype wire
