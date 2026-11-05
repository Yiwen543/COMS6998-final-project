module candidate_monitor(
input wire i_clk, i_reset, i_wr, i_rd,
input wire [7:0] i_data, o_data,
input wire [4:0] o_fill,
input wire o_full, o_empty,
output wire [5:0] active, ok);
reg valid = 1'b0;
reg [4:0] count = 5'd0;
reg [3:0] head = 4'd0, tail = 4'd0;
reg [7:0] words [0:15];
reg reset_result = 1'b0;
wire take_read = i_rd && (count != 0);
wire take_write = i_wr && (count < 16);

// Independent specification state; DUT status never controls acceptance.
always @(posedge i_clk) begin
  if (i_reset) begin
    valid <= 1'b1;
    count <= 5'd0;
    head <= 4'd0;
    tail <= 4'd0;
    reset_result <= 1'b1;
  end else if (valid) begin
    reset_result <= 1'b0;
    if (take_write) begin
      words[tail] <= i_data;
      tail <= tail + 1'b1;
    end
    if (take_read)
      head <= head + 1'b1;
    case ({take_write, take_read})
      2'b10: count <= count + 1'b1;
      2'b01: count <= count - 1'b1;
      default: count <= count;
    endcase
  end
end

assign active[0] = valid;
assign ok[0] = (o_fill === count);
assign active[1] = valid;
assign ok[1] = (o_full === (count == 16));
assign active[2] = valid;
assign ok[2] = (o_empty === (count == 0));
assign active[3] = valid && (count != 0);
assign ok[3] = (o_data === words[head]);
assign active[4] = valid;
assign ok[4] = ((o_fill <= 5'd16) === 1'b1)
             && (o_full === (o_fill == 5'd16))
             && (o_empty === (o_fill == 5'd0));
assign active[5] = valid && reset_result;
assign ok[5] = (o_fill === 5'd0) && (o_full === 1'b0)
             && (o_empty === 1'b1);

endmodule
