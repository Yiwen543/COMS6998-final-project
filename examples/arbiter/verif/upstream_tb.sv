`timescale 1ns / 1ps

module fixed_priority_arbiter_tb;

    // Parameters
    localparam CLK_PERIOD = 10; // Clock period (10ns)

    // Signals
    reg clk;
    reg reset;
    reg [7:0] req;
    reg [7:0] priority_override;
    wire [7:0] grant;
    wire valid;
    wire [2:0] grant_index;

    // Instantiate the DUT (Device Under Test)
    fixed_priority_arbiter uut (
        .clk(clk),
        .reset(reset),
        .req(req),
        .priority_override(priority_override),
        .grant(grant),
        .valid(valid),
        .grant_index(grant_index)
    );

    // Clock Generation
    always #(CLK_PERIOD / 2) clk = ~clk;  

    initial begin
        clk = 0;
        reset = 1;
        req = 8'b00000000;
        priority_override = 8'b00000000;

        #(2 * CLK_PERIOD);
        reset = 0;
        $display("Test: Reset complete\n");

        req = 8'b00001000; 
        #(CLK_PERIOD);
        if (grant == 8'b00001000 && grant_index == 3'd3 && valid == 1'b1)
            $display("Test Case 1 Passed: Single request granted correctly.");
        else
            $display("ERROR: Test Case 1 Failed - Incorrect grant behavior.");

        req = 8'b00111000; 
        #(CLK_PERIOD);
        if (grant == 8'b00001000 && grant_index == 3'd3 && valid == 1'b1)
            $display("Test Case 2 Passed: Multiple requests handled with fixed priority.");
        else
            $display("ERROR: Test Case 2 Failed - Incorrect priority handling.");

        priority_override = 8'b00010000; 
        #(CLK_PERIOD);
        if (grant == 8'b00010000 && grant_index == 3'd4 && valid == 1'b1)
            $display("Test Case 3 Passed: Priority override successful.");
        else
            $display("ERROR: Test Case 3 Failed - Priority override did not work.");

        req = 8'b00000000;
        priority_override = 8'b00000000;
        #(CLK_PERIOD);
        if (grant == 8'b00000000 && grant_index == 3'd0 && valid == 1'b0)
            $display("Test Case 4 Passed: No requests scenario handled correctly.");
        else
            $display("ERROR: Test Case 4 Failed - Incorrect handling of no requests.");

        req = 8'b10000001; // Requests on index 0 and 7
        #(CLK_PERIOD);
        if (grant == 8'b00000001 && grant_index == 3'd0 && valid == 1'b1)
            $display("Test Case 5 Passed: Highest priority request wins correctly.");
        else
            $display("ERROR: Test Case 5 Failed - Incorrect priority decision.");

        req = 8'b00000010; // Request on index 1
        #(CLK_PERIOD);
        if (grant == 8'b00000010 && grant_index == 3'd1 && valid == 1'b1)
            $display("Test Case 6 Passed: Grant updates dynamically.");
        else
            $display("ERROR: Test Case 6 Failed - Grant did not update correctly.");

        priority_override = 8'b00100000; 
        #(CLK_PERIOD);
        if (grant == 8'b00100000 && grant_index == 3'd5 && valid == 1'b1)
            $display("Test Case 7 Passed: Priority override worked dynamically.");
        else
            $display("ERROR: Test Case 7 Failed - Priority override not applied correctly.");

        $display("All test cases completed.");
        $finish;
    end

    initial begin
        $monitor("Time=%0t | reset=%b | req=%b | priority_override=%b | grant=%b | valid=%b | grant_index=%d",
                 $time, reset, req, priority_override, grant, valid, grant_index);
    end

endmodule