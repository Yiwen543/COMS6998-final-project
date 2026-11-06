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
reg seen=0, reset_edge=0;
reg [4:0] failed=0;
reg [7:0] bytes_q[0:255];
reg [3:0] lengths[0:31];
reg [4:0] iw=0,mr=0,hr=0;
reg [3:0] il=0,mp=0;
reg [5:0] data_frames=0,header_frames=0;
reg early_done=0;
reg hold_m=0,hold_h=0,hold_s=0;
reg [8:0] saved_m=0,saved_s=0;
reg [33:0] saved_h=0;
reg [7:0] tail=0;
reg [4:0] bad;
integer ml,hl,outlen,index_m;
reg expected_last;
reg [7:0] expected_data;
reg [33:0] expected_header;
wire ts=(rst===1'b0)&&(s_valid===1'b1)&&(s_ready===1'b1);
wire tm=(rst===1'b0)&&(m_valid===1'b1)&&(m_ready===1'b1);
wire th=(rst===1'b0)&&(h_valid===1'b1)&&(h_ready===1'b1);
wire finish_s=ts&&(s_last===1'b1);
wire finish_m=tm&&(m_last===1'b1);
wire add_data=finish_s&&!early_done&&!(finish_m&&(data_frames==0));
wire sub_data=finish_m&&(data_frames!=0);
wire [33:0] hv={h_pad,h_truncate,h_length,h_original_length};
always @* begin
 ml=0;
 if (data_frames!=0) ml=lengths[mr];
 else if (mr==iw && !early_done) ml=il;
 hl=0;
 if (header_frames!=0) hl=lengths[hr];
 outlen=ml;
 if(outlen<4) outlen=4;
 if(outlen>8) outlen=8;
 index_m=mr*8+mp;
 expected_data=0;
 if(mp<ml && mp<8) expected_data=bytes_q[index_m];
 expected_last=(mp==7)||((data_frames!=0)&&(mp==outlen-1));
 expected_header=0;
 if(hl<4) expected_header={1'b1,1'b0,16'd4,16'(hl)};
 else if(hl>8) expected_header={1'b0,1'b1,16'd8,16'(hl)};
 else expected_header={1'b0,1'b0,16'(hl),16'(hl)};
 bad=0;
 if(seen) begin
  if(((rst!==1'b0)&&(rst!==1'b1)) ||
     ((s_valid!==1'b0)&&(s_valid!==1'b1)) ||
     ((s_ready!==1'b0)&&(s_ready!==1'b1)) ||
     ((m_ready!==1'b0)&&(m_ready!==1'b1)) ||
     ((h_ready!==1'b0)&&(h_ready!==1'b1)) ||
     ((m_valid!==1'b0)&&(m_valid!==1'b1)) ||
     ((h_valid!==1'b0)&&(h_valid!==1'b1))) bad[4]=1;
  if(s_valid===1'b1) begin
   if((^s_data===1'bx)||((s_last!==1'b0)&&(s_last!==1'b1))) bad[4]=1;
   if(rst===1'b1) bad[4]=1;
  end
  if((rst===1'b0)&&hold_s&&((s_valid!==1'b1)||({s_last,s_data}!==saved_s))) bad[4]=1;
  if(reset_edge) begin
   if((m_valid!==1'b0)||(h_valid!==1'b0)) bad[3]=1;
  end else begin
   if(m_valid===1'b1) begin
    if((mp>=8)||((data_frames==0)&&(mp>=ml))) begin
     bad[0]=1; bad[1]=1;
    end else begin
     if((^m_data===1'bx)||(m_data!==expected_data)) bad[0]=1;
     if((m_last!==1'b0)&&(m_last!==1'b1)) bad[1]=1;
     else if(data_frames!=0 || mp==7 || mp+1<ml) begin
      if(m_last!==expected_last) bad[1]=1;
     end else if(m_last!==1'b0) bad[1]=1;
    end
   end
   if(h_valid===1'b1) begin
    if((header_frames==0)||(^hv===1'bx)||(hv!==expected_header)) bad[2]=1;
   end
   if(rst===1'b0) begin
    if(hold_m&&((m_valid!==1'b1)||({m_last,m_data}!==saved_m))) bad[3]=1;
    if(hold_h&&((h_valid!==1'b1)||(hv!==saved_h))) bad[3]=1;
   end
  end
  if(ts && il>=12) bad[4]=1;
  if(ts && il==0 && ((data_frames>=31)||(header_frames>=31))) bad[4]=1;
 end
end
always @(posedge clk) begin
 seen<=1;
 failed<=failed|bad;
 reset_edge<=(rst===1'b1);
 if(rst===1'b1) begin
  iw<=0; mr<=0; hr<=0; il<=0; mp<=0;
  data_frames<=0; header_frames<=0; early_done<=0;
  hold_m<=0; hold_h<=0; hold_s<=0; tail<=0;
 end else if(rst===1'b0) begin
  hold_m<=(m_valid===1'b1)&&(m_ready===1'b0);
  hold_h<=(h_valid===1'b1)&&(h_ready===1'b0);
  hold_s<=(s_valid===1'b1)&&(s_ready===1'b0);
  saved_m<={m_last,m_data}; saved_h<=hv; saved_s<={s_last,s_data};
  if((s_valid===1'b0)&&(m_ready===1'b1)&&(h_ready===1'b1)) begin
   if(tail<128) tail<=tail+1'b1;
  end else tail<=0;
  if(ts) begin
   if(il<8) bytes_q[iw*8+il]<=s_data;
   if(finish_s) begin
    lengths[iw]<=il+1'b1; iw<=iw+1'b1; il<=0;
   end else if(il<13) il<=il+1'b1;
  end
  if(tm) begin
   if(m_last===1'b1) begin mr<=mr+1'b1; mp<=0; end
   else if(mp<9) mp<=mp+1'b1;
  end
  if(th) hr<=hr+1'b1;
  if(finish_s) early_done<=0;
  else if(finish_m && data_frames==0) early_done<=1;
  case({add_data,sub_data})
   2'b10: data_frames<=data_frames+1'b1;
   2'b01: data_frames<=data_frames-1'b1;
   default: data_frames<=data_frames;
  endcase
  case({finish_s,th})
   2'b10: header_frames<=header_frames+1'b1;
   2'b01: if(header_frames!=0) header_frames<=header_frames-1'b1;
   default: header_frames<=header_frames;
  endcase
 end
end
wire end_good=(data_frames===6'd0)&&(header_frames===6'd0)&&
 (il===4'd0)&&(mp===4'd0)&&(early_done===1'b0)&&
 (iw===mr)&&(iw===hr)&&(s_valid===1'b0)&&
 (m_valid===1'b0)&&(h_valid===1'b0)&&(rst===1'b0)&&
 (m_ready===1'b1)&&(h_ready===1'b1)&&(tail>=32);
assign active[4:0]={5{seen}};
assign ok[4:0]=~(failed|bad);
assign active[5]=(trace_done===1'b1);
assign ok[5]=end_good;

endmodule
`default_nettype wire
