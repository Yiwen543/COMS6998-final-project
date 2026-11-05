module candidate_monitor(
input wire i_clk, i_reset, i_wr, i_rd,
input wire [7:0] i_data, o_data,
input wire [4:0] o_fill,
input wire o_full, o_empty,
output wire [5:0] active, ok);
reg initialized = 1'b0;
reg reset_applied = 1'b0;
reg [4:0] expected_fill = 5'd0;
reg [7:0] expected_words [0:15];
integer k;
wire take_read = i_rd && (expected_fill != 5'd0);
wire take_write = i_wr && (expected_fill < 5'd16);

// Model acceptance from specification occupancy, not observed DUT flags.
always @(posedge i_clk) begin
    if (i_reset) begin
        initialized <= 1'b1;
        expected_fill <= 5'd0;
        reset_applied <= 1'b1;
    end else begin
        reset_applied <= 1'b0;
        if (initialized) begin
            case ({take_write, take_read})
                2'b10: expected_fill <= expected_fill + 5'd1;
                2'b01: expected_fill <= expected_fill - 5'd1;
                default: expected_fill <= expected_fill;
            endcase
            if (take_read) begin
                for (k = 0; k < 15; k = k + 1)
                    expected_words[k] <= expected_words[k+1];
            end
            if (take_write) begin
                if (take_read)
                    expected_words[expected_fill - 5'd1] <= i_data;
                else
                    expected_words[expected_fill] <= i_data;
            end
        end
    end
end

assign active[0] = initialized;
assign active[1] = initialized;
assign active[2] = initialized;
assign active[3] = initialized && (expected_fill != 5'd0);
assign active[4] = initialized;
assign active[5] = initialized && reset_applied;

assign ok[0] = (o_fill === expected_fill);
assign ok[1] = (o_full === (expected_fill == 5'd16));
assign ok[2] = (o_empty === (expected_fill == 5'd0));
assign ok[3] = (expected_fill == 5'd0) ? 1'b1 : (o_data === expected_words[0]);
assign ok[4] = ((o_fill <= 5'd16) === 1'b1);
assign ok[5] = (o_fill === 5'd0) && (o_full === 1'b0) && (o_empty === 1'b1);

endmodule
