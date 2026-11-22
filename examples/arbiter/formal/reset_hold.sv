// One SMT transition is half a physical clock period. Drive inputs in the
// low phase and hold them through the rising edge, as in the replay bench.
module reset_hold(input reset, input [7:0] req, input [7:0] priority_override);
    reg clk = 0;
    reg [1:0] startup = 0;
    reg prev_reset;
    reg [7:0] prev_req, prev_override;
    reg [11:0] prev_outputs;
    wire [7:0] grant;
    wire valid;
    wire [2:0] grant_index;
    wire [11:0] outputs = {grant, valid, grant_index};

    fixed_priority_arbiter dut(.*);

    always @($global_clock) begin
        clk <= !clk;
        if (startup < 2) startup <= startup + 1'b1;
        prev_reset <= reset;
        prev_req <= req;
        prev_override <= priority_override;
        prev_outputs <= outputs;
    end

    always @* begin
        if (startup < 2) assume(reset); // Initialize through the first rising edge.
        if (clk) assume({reset, req, priority_override} ==
                        {prev_reset, prev_req, prev_override});
        if (startup == 2 && !clk && !prev_reset && reset && prev_outputs[3]) begin
            cover(1'b1); // A granted request is followed by a low-phase reset.
            assert(outputs == prev_outputs);
        end
    end
endmodule
