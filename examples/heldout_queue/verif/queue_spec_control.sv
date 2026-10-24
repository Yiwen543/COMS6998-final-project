// Independent behavioral control for checking the checker; never a pilot DUT.
module queue_spec_control #(
  parameter DEPTH = 4, DBITS = 32,
  parameter ALMOST_EMPTY_THRESHOLD = 1,
  parameter ALMOST_FULL_THRESHOLD = 4
) (
  input logic rst_ni, clk_i, clr_i, ena_i, we_i,
  input logic [DBITS-1:0] d_i,
  input logic re_i,
  output logic [DBITS-1:0] q_o,
  output logic empty_o, full_o, almost_empty_o, almost_full_o
);
  localparam integer CAPACITY = DEPTH - 1;
  logic [DBITS-1:0] data [0:DEPTH-1];
  integer count = 0;
  integer i;
  always @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      count <= 0;
      for (i = 0; i < DEPTH; i = i + 1) data[i] <= 0;
    end else if (clr_i) begin
      count <= 0;
      for (i = 0; i < DEPTH; i = i + 1) data[i] <= 0;
    end else if (ena_i) begin
      case ({we_i, re_i})
        2'b10: begin
          data[count] <= d_i;
          count <= count + 1;
        end
        2'b01: begin
          for (i = 0; i < DEPTH-1; i = i + 1) data[i] <= data[i+1];
          data[DEPTH-1] <= 0;
          count <= count - 1;
        end
        2'b11: begin
          for (i = 0; i < DEPTH-1; i = i + 1) data[i] <= data[i+1];
          data[DEPTH-1] <= 0;
          if (count == 0) data[0] <= d_i;
          else data[count-1] <= d_i;
        end
        default: ;
      endcase
    end
  end
  assign q_o = data[0];
  assign empty_o = count == 0;
  assign full_o = count == CAPACITY;
  assign almost_empty_o = count <= ALMOST_EMPTY_THRESHOLD;
  assign almost_full_o = count >= CAPACITY-1;
endmodule
