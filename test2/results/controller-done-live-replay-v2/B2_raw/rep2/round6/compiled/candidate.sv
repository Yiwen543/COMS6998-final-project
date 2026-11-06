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
reg started=0, reset_post=0, lost=0;
reg [5:0] failed=0;
reg [7:0] bytes_q[0:63][0:7];
reg [3:0] length_q[0:63];
reg complete_q[0:63];
reg [6:0] write_seq=0, data_seq=0, header_seq=0;
reg [3:0] data_pos=0;
reg data_hold=0, header_hold=0;
reg [8:0] saved_data;
reg [33:0] saved_header;
reg [5:0] violation;
reg data_available, boundary_known, expected_last;
reg [7:0] expected_data;
reg [3:0] adjusted_length;
reg [7:0] tail_count=0;
wire [5:0] wi=write_seq[5:0];
wire [5:0] di=data_seq[5:0];
wire [5:0] hi=header_seq[5:0];
wire [6:0] data_distance=write_seq-data_seq;
wire [6:0] header_distance=write_seq-header_seq;
integer i;

always @* begin
    violation=0;
    data_available=0;
    boundary_known=0;
    expected_last=0;
    expected_data=0;
    adjusted_length=0;
    if (started && !lost) begin
        if (data_distance<64 && length_q[di]!=0) begin
            if (data_pos<length_q[di] && data_pos<8) begin
                data_available=1;
                expected_data=bytes_q[di][data_pos[2:0]];
            end else if (complete_q[di] && length_q[di]<4 && data_pos<4) begin
                data_available=1;
                expected_data=0;
            end
            if (data_pos<3) begin
                boundary_known=1;
                expected_last=0;
            end else if (data_pos==7) begin
                boundary_known=1;
                expected_last=1;
            end else if (complete_q[di]) begin
                boundary_known=1;
                expected_last=(data_pos+1==length_q[di]);
                if (length_q[di]<4) expected_last=(data_pos==3);
            end else if (length_q[di]>data_pos+1) begin
                boundary_known=1;
                expected_last=0;
            end
        end
        if (!reset_post) begin
            if (m_valid==1'b1) begin
                violation[0]=!data_available;
                if (data_available) violation[0]=!(m_data==expected_data);
                if (boundary_known) violation[1]=!(m_last==expected_last);
                else violation[1]=1'bx;
            end else if (m_valid!==1'b0) begin
                violation[0]=1'bx;
                violation[1]=1'bx;
            end
            if (h_valid==1'b1) begin
                if (!(header_distance<64 && complete_q[hi])) violation[2]=1;
                else begin
                    adjusted_length=length_q[hi];
                    if (length_q[hi]<4) adjusted_length=4;
                    if (length_q[hi]>8) adjusted_length=8;
                    violation[2]=!((h_original_length=={12'd0,length_q[hi]}) &&
                        (h_length=={12'd0,adjusted_length}) &&
                        (h_pad==(length_q[hi]<4)) &&
                        (h_truncate==(length_q[hi]>8)));
                end
            end else if (h_valid!==1'b0) violation[2]=1'bx;
        end
        if (rst==1'b0) begin
            if (data_hold) violation[3]=!((m_valid==1'b1) && ({m_last,m_data}==saved_data));
            if (header_hold) violation[3]=violation[3] | !((h_valid==1'b1) &&
                ({h_pad,h_truncate,h_length,h_original_length}==saved_header));
        end
        if (reset_post) violation[4]=!((m_valid==1'b0) && (h_valid==1'b0));
    end
    if (trace_done==1'b1) begin
        violation[5]=!((s_valid==1'b0) && (m_valid==1'b0) && (h_valid==1'b0) &&
            (data_seq==write_seq) && (header_seq==write_seq) && (length_q[wi]==0));
        if (lost || !started) violation[5]=violation[5] | 1'bx;
        if (tail_count<32) violation[5]=violation[5] | 1'bx;
    end
end

assign active=started ? 6'b111111 : 6'b000000;
assign ok=~(failed | violation | {6{lost ? 1'bx : 1'b0}});

always @(posedge clk) begin
    started<=1;
    if (started) failed<=failed | violation;
    reset_post<=rst;
    if (rst===1'b0 && s_valid===1'b0 && m_ready===1'b1 && h_ready===1'b1) begin
        if (tail_count<255) tail_count<=tail_count+1'b1;
    end else tail_count<=0;
    if (rst==1'b1) begin
        write_seq<=0;
        data_seq<=0;
        header_seq<=0;
        data_pos<=0;
        lost<=0;
        data_hold<=0;
        header_hold<=0;
        for (i=0;i<64;i=i+1) begin
            length_q[i]<=0;
            complete_q[i]<=0;
        end
    end else if (rst==1'b0 && started) begin
        data_hold<=(m_valid && !m_ready);
        header_hold<=(h_valid && !h_ready);
        saved_data<={m_last,m_data};
        saved_header<={h_pad,h_truncate,h_length,h_original_length};
        if (!lost) begin
            if (m_valid==1'b1 && m_ready==1'b1) begin
                if (data_available && boundary_known) begin
                    if (expected_last) begin
                        data_seq<=data_seq+1'b1;
                        data_pos<=0;
                    end else data_pos<=data_pos+1'b1;
                end
            end
            if (h_valid==1'b1 && h_ready==1'b1 && header_distance<64 && complete_q[hi])
                header_seq<=header_seq+1'b1;
            if ((m_valid==1'b1 && m_ready!==1'b0 && m_ready!==1'b1) ||
                (h_valid==1'b1 && h_ready!==1'b0 && h_ready!==1'b1)) lost<=1;
            if (s_valid==1'b1 && s_ready==1'b1) begin
                if (data_distance>=63 || header_distance>=63 || length_q[wi]>=12) lost<=1;
                else begin
                    if (length_q[wi]<8) bytes_q[wi][length_q[wi][2:0]]<=s_data;
                    length_q[wi]<=length_q[wi]+1'b1;
                    if (s_last==1'b1) begin
                        complete_q[wi]<=1;
                        write_seq<=write_seq+1'b1;
                        length_q[(write_seq+1'b1)&7'd63]<=0;
                        complete_q[(write_seq+1'b1)&7'd63]<=0;
                    end else if (s_last!==1'b0) lost<=1;
                end
            end else if ((s_valid!==1'b0 && s_valid!==1'b1) ||
                (s_valid==1'b1 && s_ready!==1'b0 && s_ready!==1'b1)) lost<=1;
        end
    end else if (rst!==1'b0) lost<=1;
end

endmodule
`default_nettype wire
