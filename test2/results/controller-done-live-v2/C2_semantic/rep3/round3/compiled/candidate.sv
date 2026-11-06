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
reg armed=0;
reg [5:0] bad=0;
reg [5:0] wp=0,dp=0,hp=0;
reg [3:0] di=0;
reg [63:0] bytes_q[0:63];
reg [3:0] len_q[0:63];
reg used_q[0:63], complete_q[0:63], dd_q[0:63], hd_q[0:63];
reg reset_q=0, ms=0, hs=0;
reg [8:0] sm=0;
reg [33:0] sh=0;
reg [7:0] tail=0;
reg [5:0] f;
reg pending,available,elast;
reg [7:0] eb;
reg [3:0] olen;
integer k,r;
always @* begin
 f=0; pending=0; available=0; elast=0; eb=0; olen=0;
 for(k=0;k<64;k=k+1) begin
  if(used_q[k]===1'b1 && (complete_q[k]!==1'b1 || dd_q[k]!==1'b1 || hd_q[k]!==1'b1)) pending=1;
 end
 if(armed) begin
  if((rst!==1'b0 && rst!==1'b1) || (s_valid!==1'b0 && s_valid!==1'b1) || (s_ready!==1'b0 && s_ready!==1'b1) || (m_valid!==1'b0 && m_valid!==1'b1) || (h_valid!==1'b0 && h_valid!==1'b1) || (m_ready!==1'b0 && m_ready!==1'b1) || (h_ready!==1'b0 && h_ready!==1'b1)) f[4]=1;
  if(rst===1'b0 && s_valid===1'b1 && s_ready===1'b1) begin
   if((^s_data)===1'bx || (s_last!==1'b0 && s_last!==1'b1)) f[4]=1;
  end
  if(reset_q && (m_valid!==1'b0 || h_valid!==1'b0)) f[4]=1;
  if(rst===1'b0) begin
   if(ms && (m_valid!==1'b1 || {m_last,m_data}!==sm)) f[3]=1;
   if(hs && (h_valid!==1'b1 || {h_pad,h_truncate,h_length,h_original_length}!==sh)) f[3]=1;
  end
  if(used_q[dp]===1'b1 && dd_q[dp]===1'b0) begin
   if(len_q[dp]<4) olen=4;
   else if(len_q[dp]>8) olen=8;
   else olen=len_q[dp];
   if(di<8 && di<len_q[dp]) begin
    available=1; eb=bytes_q[dp][di*8 +: 8];
   end else if(complete_q[dp]===1'b1 && di<olen) begin
    available=1; eb=0;
   end
   if(complete_q[dp]===1'b1) elast=(di==olen-1);
   else elast=(di==7);
  end
  if(m_valid===1'b1) begin
   if(!available || (^m_data)===1'bx || m_data!==eb) f[0]=1;
   if(!available || m_last!==elast) f[1]=1;
  end
  if(h_valid===1'b1) begin
   if(used_q[hp]!==1'b1 || complete_q[hp]!==1'b1 || hd_q[hp]!==1'b0) f[2]=1;
   else begin
    if(h_original_length!=={12'd0,len_q[hp]} || h_pad!==(len_q[hp]<4) || h_truncate!==(len_q[hp]>8)) f[2]=1;
    if(len_q[hp]<4) begin if(h_length!==16'd4) f[2]=1; end
    else if(len_q[hp]>8) begin if(h_length!==16'd8) f[2]=1; end
    else if(h_length!=={12'd0,len_q[hp]}) f[2]=1;
   end
  end
  if(trace_done===1'b1) begin
   if(pending || s_valid!==1'b0 || m_valid!==1'b0 || h_valid!==1'b0 || rst!==1'b0 || m_ready!==1'b1 || h_ready!==1'b1 || tail<32) f[5]=1;
  end
 end
end
assign active=armed ? 6'b111111 : ((trace_done===1'b1) ? 6'b100000 : 6'b000000);
assign ok=~(bad | f | ((!armed && trace_done===1'b1) ? 6'b100000 : 6'b000000));
always @(posedge clk) begin
 if(armed) bad<=bad|f;
 reset_q<=(rst===1'b1);
 if(rst===1'b1) begin
  armed<=1; wp<=0; dp<=0; hp<=0; di<=0; ms<=0; hs<=0; tail<=0;
  for(r=0;r<64;r=r+1) begin
   bytes_q[r]<=0; len_q[r]<=0; used_q[r]<=0; complete_q[r]<=0; dd_q[r]<=1; hd_q[r]<=1;
  end
 end else if(armed && rst===1'b0) begin
  ms<=(m_valid===1'b1 && m_ready===1'b0);
  hs<=(h_valid===1'b1 && h_ready===1'b0);
  sm<={m_last,m_data}; sh<={h_pad,h_truncate,h_length,h_original_length};
  if(s_valid===1'b0 && m_ready===1'b1 && h_ready===1'b1) begin
   if(tail<128) tail<=tail+1'b1;
  end else tail<=0;
  if(m_valid===1'b1 && m_ready===1'b1) begin
   if(m_last===1'b1) begin dd_q[dp]<=1; dp<=dp+1'b1; di<=0; end
   else if(di<8) di<=di+1'b1;
   else bad[1]<=1;
  end
  if(h_valid===1'b1 && h_ready===1'b1) begin hd_q[hp]<=1; hp<=hp+1'b1; end
  if(s_valid===1'b1 && s_ready===1'b1) begin
   if(used_q[wp]!==1'b1 || complete_q[wp]===1'b1) begin
    if(used_q[wp]===1'b1 && (dd_q[wp]!==1'b1 || hd_q[wp]!==1'b1)) bad[4]<=1;
    used_q[wp]<=1; complete_q[wp]<=(s_last===1'b1); len_q[wp]<=1;
    bytes_q[wp]<={56'd0,s_data}; dd_q[wp]<=0; hd_q[wp]<=0;
   end else begin
    if(len_q[wp]<8) bytes_q[wp][len_q[wp]*8 +: 8]<=s_data;
    if(len_q[wp]<12) len_q[wp]<=len_q[wp]+1'b1;
    else bad[4]<=1;
    if(s_last===1'b1) complete_q[wp]<=1;
   end
   if(s_last===1'b1) wp<=wp+1'b1;
  end
 end
end

endmodule
`default_nettype wire
