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
// Private, bounded transaction scoreboard. No DUT timing model is used.
reg seen = 1'b0;
reg [5:0] bad = 0;
reg [7:0] produce = 0, consume_m = 0, consume_h = 0;
reg [3:0] nbyte [0:31];
reg complete [0:31];
reg [63:0] bytes [0:31];
reg [3:0] position = 0;
reg hold_m = 0, hold_h = 0;
reg [8:0] saved_m = 0;
reg [33:0] saved_h = 0;
reg reset_sample = 0;
reg [7:0] tail = 0;
reg [5:0] err;
reg [7:0] expected_byte;
reg expected_last;
reg [3:0] out_length;
reg [15:0] status_length;
wire [4:0] wi = produce[4:0];
wire [4:0] mi = consume_m[4:0];
wire [4:0] hi = consume_h[4:0];
wire take_s = (rst === 1'b0) && (s_valid === 1'b1) && (s_ready === 1'b1);
wire take_m = (rst === 1'b0) && (m_valid === 1'b1) && (m_ready === 1'b1);
wire take_h = (rst === 1'b0) && (h_valid === 1'b1) && (h_ready === 1'b1);
integer k;
always @* begin
    err = 0;
    expected_byte = 0;
    expected_last = 0;
    out_length = 0;
    status_length = 0;
    if (seen) begin
        // All presented responses, not just handshakes, require justification.
        if ((m_valid !== 1'b0) && (m_valid !== 1'b1)) err[4] = 1;
        if ((h_valid !== 1'b0) && (h_valid !== 1'b1)) err[4] = 1;
        if ((s_ready !== 1'b0) && (s_ready !== 1'b1)) err[4] = 1;
        if (m_valid === 1'b1) begin
            if (complete[mi] === 1'b1) begin
                if (nbyte[mi] < 4) out_length = 4;
                else if (nbyte[mi] > 8) out_length = 8;
                else out_length = nbyte[mi];
            end else out_length = nbyte[mi] > 8 ? 8 : nbyte[mi];
            if ((position >= out_length) || (out_length == 0) ||
                ((consume_m == produce) && (nbyte[mi] == 0))) begin
                err[0] = 1;
                err[1] = 1;
            end else begin
                if (position < nbyte[mi] && position < 8)
                    expected_byte = bytes[mi][position*8 +: 8];
                else expected_byte = 0;
                if ((^expected_byte === 1'bx) || (m_data !== expected_byte)) err[0] = 1;
                // The eighth byte is always the final retained byte. Shorter
                // ends are justified only by an accepted input last.
                expected_last = (position == 7) ||
                    ((complete[mi] === 1'b1) && (position + 1 == out_length));
                if (m_last !== expected_last) err[1] = 1;
            end
        end
        if (h_valid === 1'b1) begin
            if ((consume_h == produce) || (complete[hi] !== 1'b1)) err[2] = 1;
            else begin
                if (nbyte[hi] < 4) status_length = 4;
                else if (nbyte[hi] > 8) status_length = 8;
                else status_length = {12'b0,nbyte[hi]};
                if (h_original_length !== {12'b0,nbyte[hi]}) err[2] = 1;
                if (h_length !== status_length) err[2] = 1;
                if (h_pad !== (nbyte[hi] < 4)) err[2] = 1;
                if (h_truncate !== (nbyte[hi] > 8)) err[2] = 1;
            end
        end
        if (hold_m && !reset_sample) begin
            if ((m_valid !== 1'b1) || ({m_last,m_data} !== saved_m) ||
                (^saved_m === 1'bx)) err[3] = 1;
        end
        if (hold_h && !reset_sample) begin
            if ((h_valid !== 1'b1) ||
                ({h_pad,h_truncate,h_length,h_original_length} !== saved_h) ||
                (^saved_h === 1'bx)) err[3] = 1;
        end
        if (reset_sample) begin
            if ((m_valid !== 1'b0) || (h_valid !== 1'b0)) err[4] = 1;
        end
    end
    if (trace_done === 1'b1) begin
        if (!seen || tail < 32 || (rst !== 1'b0) ||
            (s_valid !== 1'b0) || (m_valid !== 1'b0) || (h_valid !== 1'b0) ||
            (consume_m != produce) || (consume_h != produce) ||
            (nbyte[wi] !== 4'd0)) err[5] = 1;
    end
end
assign active = {trace_done === 1'b1,{5{seen}}};
assign ok = ~(bad | err);
always @(posedge clk) begin
    bad <= bad | err;
    reset_sample <= (rst === 1'b1);
    if (rst === 1'b1) begin
        seen <= 1;
        produce <= 0;
        consume_m <= 0;
        consume_h <= 0;
        position <= 0;
        hold_m <= 0;
        hold_h <= 0;
        tail <= 0;
        for (k=0;k<32;k=k+1) begin
            nbyte[k] <= 0;
            complete[k] <= 0;
            bytes[k] <= 0;
        end
    end else if (seen && rst === 1'b0) begin
        hold_m <= (m_valid === 1'b1) && (m_ready === 1'b0);
        hold_h <= (h_valid === 1'b1) && (h_ready === 1'b0);
        saved_m <= {m_last,m_data};
        saved_h <= {h_pad,h_truncate,h_length,h_original_length};
        if ((s_valid === 1'b0) && (m_ready === 1'b1) && (h_ready === 1'b1)) begin
            if (tail < 128) tail <= tail + 1'b1;
        end else tail <= 0;
        if (take_s) begin
            if (nbyte[wi] < 8) bytes[wi][nbyte[wi]*8 +: 8] <= s_data;
            if (nbyte[wi] < 12) nbyte[wi] <= nbyte[wi] + 1'b1;
            else bad[4] <= 1;
            if ((s_last !== 1'b0) && (s_last !== 1'b1)) bad[4] <= 1;
            if (s_last === 1'b1) begin
                complete[wi] <= 1;
                produce <= produce + 1'b1;
                nbyte[(produce+1'b1)&8'd31] <= 0;
                complete[(produce+1'b1)&8'd31] <= 0;
                bytes[(produce+1'b1)&8'd31] <= 0;
            end
        end
        if (take_m) begin
            if (m_last === 1'b1) begin
                consume_m <= consume_m + 1'b1;
                position <= 0;
            end else if (position < 8) position <= position + 1'b1;
        end
        if (take_h) consume_h <= consume_h + 1'b1;
    end
end

endmodule
`default_nettype wire
