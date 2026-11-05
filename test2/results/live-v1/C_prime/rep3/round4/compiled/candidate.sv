module candidate_monitor(
input wire i_clk, i_reset, i_wr, i_rd,
input wire [7:0] i_data, o_data,
input wire [4:0] o_fill,
input wire o_full, o_empty,
output wire [5:0] active, ok);
reg started = 1'b0;
reg last_reset = 1'b0;
reg [4:0] count = 5'd0;
reg [3:0] head = 4'd0;
reg [3:0] tail = 4'd0;
reg [7:0] queue_mem [0:15];

// Gate acceptance with expected occupancy, never DUT flags.
wire take_read = i_rd && (count != 5'd0);
wire take_write = i_wr && (count < 5'd16);

always @(posedge i_clk) begin
    started <= 1'b1;
    last_reset <= i_reset;
    if (i_reset) begin
        count <= 5'd0;
        head <= 4'd0;
        tail <= 4'd0;
    end else if (started) begin
        if (take_write) begin
            queue_mem[tail] <= i_data;
            tail <= tail + 4'd1;
        end
        if (take_read)
            head <= head + 4'd1;
        case ({take_write, take_read})
            2'b10: count <= count + 5'd1;
            2'b01: count <= count - 5'd1;
            default: count <= count;
        endcase
    end
end

assign active[0] = started;
assign ok[0] = (o_fill === count);

assign active[1] = started;
assign ok[1] = (o_full === (count == 5'd16));

assign active[2] = started;
assign ok[2] = (o_empty === (count == 5'd0));

assign active[3] = started && (count != 5'd0);
assign ok[3] = (count == 5'd0) ? 1'b1 : (o_data === queue_mem[head]);

assign active[4] = started;
assign ok[4] = ((o_fill <= 5'd16) === 1'b1)
            && (o_full === (o_fill == 5'd16))
            && (o_empty === (o_fill == 5'd0));

assign active[5] = started && last_reset;
assign ok[5] = (o_fill === 5'd0) && (o_full === 1'b0)
            && (o_empty === 1'b1);

endmodule
