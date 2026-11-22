`timescale 1ns/1ps
module replay_reset_hold;
    reg clk = 0, reset = 0;
    reg [7:0] req = 0, priority_override = 0;
    wire [7:0] grant;
    wire valid;
    wire [2:0] grant_index;
    wire [11:0] outputs = {grant, valid, grant_index};
    fixed_priority_arbiter dut(.*);

    integer fd, count = 0, rc;
    reg next_reset, sampled_reset;
    reg [7:0] next_req, next_override;
    reg [11:0] sampled_outputs;
    string path;

    initial begin
        if (!$value$plusargs("VECTORS=%s", path)) $fatal(1, "Missing witness");
        fd = $fopen(path, "r");
        if (!fd) $fatal(1, "Cannot read witness");
        while (!$feof(fd)) begin
            rc = $fscanf(fd, "%d %h %h\n", next_reset, next_req, next_override);
            if (rc == 3) begin
                sampled_reset = reset;
                sampled_outputs = outputs;
                clk = count % 2;
                #1;
                if (clk && {reset, req, priority_override} !==
                           {next_reset, next_req, next_override})
                    $fatal(1, "Inputs changed at a rising edge");
                {reset, req, priority_override} = {next_reset, next_req, next_override};
                #1;
                if (count >= 2 && !clk && !sampled_reset && reset && sampled_outputs[3]) begin
                    if ((^sampled_outputs === 1'bx) || (^outputs === 1'bx))
                        $fatal(1, "Unknown sampled outputs");
                    $display("ACTIVATION step=%0d before=%03h after=%03h",
                             count, sampled_outputs, outputs);
                end
                count = count + 1;
            end else if (!$feof(fd)) $fatal(1, "Malformed witness");
        end
        $fclose(fd);
        $display("REPLAY_STEPS=%0d", count);
        $finish;
    end
endmodule
