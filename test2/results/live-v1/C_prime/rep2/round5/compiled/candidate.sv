module candidate_monitor(
input wire i_clk, i_reset, i_wr, i_rd,
input wire [7:0] i_data, o_data,
input wire [4:0] o_fill,
input wire o_full, o_empty,
output wire [5:0] active, ok);
reg seen_reset;
reg last_reset;
reg [4:0] expected_fill;
reg [3:0] head, tail;
reg [7:0] words [0:15];
wire take_read = i_rd && (expected_fill != 0);
wire take_write = i_wr && (expected_fill < 16);

initial begin
    seen_reset = 1'b0;
    last_reset = 1'b0;
    expected_fill = 0;
    head = 0;
    tail = 0;
end

always @(posedge i_clk) begin
    last_reset <= i_reset;
    if (i_reset) begin
        seen_reset <= 1'b1;
        expected_fill <= 0;
        head <= 0;
        tail <= 0;
    end else if (seen_reset) begin
        if (take_write) begin
            words[tail] <= i_data;
            tail <= tail + 4'd1;
        end
        if (take_read)
            head <= head + 4'd1;
        case ({take_write, take_read})
            2'b10: expected_fill <= expected_fill + 5'd1;
            2'b01: expected_fill <= expected_fill - 5'd1;
            default: expected_fill <= expected_fill;
        endcase
    end
end

assign active[0] = seen_reset;
assign ok[0] = (o_fill === expected_fill);
assign active[1] = seen_reset;
assign ok[1] = (o_full === (expected_fill == 5'd16));
assign active[2] = seen_reset;
assign ok[2] = (o_empty === (expected_fill == 5'd0));
assign active[3] = seen_reset && (expected_fill != 0);
assign ok[3] = (o_data === words[head]);
assign active[4] = seen_reset && last_reset;
assign ok[4] = (o_fill === 5'd0) && (o_full === 1'b0) && (o_empty === 1'b1);
assign active[5] = seen_reset;
assign ok[5] = ((o_fill <= 5'd16) === 1'b1)
             && (o_full === (o_fill == 5'd16))
             && (o_empty === (o_fill == 5'd0));

endmodule
