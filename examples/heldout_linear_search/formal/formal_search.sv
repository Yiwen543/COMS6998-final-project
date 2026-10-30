// Specification-derived narrow reference: reported match count is bounded by
// MAX_MATCHES, and the controller's completion indication is a one-cycle pulse.
module formal_search (
  input logic clk, srst, start, pause, mem_write_en,
  input logic [7:0] key, mem_write_data,
  input logic [1:0] mem_write_addr
);
  wire done, match_overflow;
  wire [1:0] match_count;
  wire [3:0] match_indices;
  linear_search_top #(.DATA_WIDTH(8), .ADDR_WIDTH(2),
                      .MEM_DEPTH(4), .MAX_MATCHES(2)) dut (
    .clk, .srst, .start, .pause, .key, .mem_write_en,
    .mem_write_addr, .mem_write_data, .done, .match_count,
    .match_indices, .match_overflow
  );
  reg prior_done = 0;
  initial assume(srst);
  always @(posedge clk) begin
    if (srst) begin
      prior_done <= 0;
    end else begin
      assert(match_count <= 2);
      if (prior_done) assert(!done);
      prior_done <= done;
      cover(done);
    end
  end
endmodule
