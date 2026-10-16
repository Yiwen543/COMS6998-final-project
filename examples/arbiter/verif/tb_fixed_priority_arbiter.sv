`timescale 1ns/1ps
module tb_fixed_priority_arbiter;
    reg clk = 0, reset = 0;
    reg [7:0] req = 0, priority_override = 0;
    wire [7:0] grant;
    wire valid;
    wire [2:0] grant_index;
    integer checks = 0, functional_errors = 0, timing_errors = 0;
    integer r, o, mode = 2;
    integer vector_file, scan_status, vector_reset, vector_req, vector_override;
    reg initialized = 0;
    reg [8:0] seen_req = 0, seen_override = 0;
    reg [1023:0] vector_path;

    fixed_priority_arbiter dut (
        .clk(clk), .reset(reset), .req(req),
        .priority_override(priority_override), .grant(grant),
        .valid(valid), .grant_index(grant_index)
    );
    always #5 clk = ~clk;

    task automatic step(input reg rst, input reg [7:0] requests,
                        input reg [7:0] overrides);
        reg [11:0] held;
        reg [7:0] selected, expected_grant;
        reg [2:0] expected_index;
        reg expected_valid;
        integer bit_index;
        begin
            @(negedge clk);
            held = {grant, valid, grant_index};
            reset = rst;
            req = requests;
            priority_override = overrides;
            #1;
            if (initialized && {grant, valid, grant_index} !== held) begin
                timing_errors = timing_errors + 1;
                if (timing_errors <= 4)
                    $display("TIMING_FAIL t=%0t reset=%b req=%h override=%h",
                             $time, reset, req, priority_override);
            end
            selected = rst ? 8'h00 : ((overrides != 0) ? overrides : requests);
            expected_grant = selected & (~selected + 8'd1);
            expected_valid = (selected != 0);
            expected_index = 0;
            for (bit_index = 0; bit_index < 8; bit_index = bit_index + 1)
                if (expected_grant[bit_index]) expected_index = bit_index[2:0];
            @(posedge clk);
            #1;
            checks = checks + 1;
            if (grant !== expected_grant || valid !== expected_valid ||
                ((rst || expected_valid) && grant_index !== expected_index)) begin
                functional_errors = functional_errors + 1;
                if (functional_errors <= 4)
                    $display("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d",
                             requests, overrides, rst, grant, valid, grant_index,
                             expected_grant, expected_valid, expected_index);
            end
            if (!rst) begin
                if (overrides == 0) begin
                    if (expected_valid) seen_req[{1'b0, expected_index}] = 1'b1;
                    else seen_req[8] = 1'b1;
                    seen_override[8] = 1'b1;
                end else seen_override[{1'b0, expected_index}] = 1'b1;
            end
            initialized = 1;
        end
    endtask

    initial begin
        if ($value$plusargs("MODE=%d", mode)) begin end
        // A small starting test intentionally leaves priority paths uncovered.
        step(1, 8'h00, 8'h00);
        step(0, 8'h00, 8'h00);
        step(0, 8'h01, 8'h00);
        step(0, 8'h00, 8'h01);
        if (mode == 1) begin
            if (!$value$plusargs("VECTORS=%s", vector_path))
                $fatal(1, "MODE=1 requires +VECTORS=<file>");
            vector_file = $fopen(vector_path, "r");
            if (vector_file == 0) $fatal(1, "Cannot open stimulus file");
            while (!$feof(vector_file)) begin
                scan_status = $fscanf(vector_file, "%d %h %h\n",
                                      vector_reset, vector_req, vector_override);
                if (scan_status == 3)
                    step(vector_reset[0], vector_req[7:0], vector_override[7:0]);
                else if (!$feof(vector_file)) $fatal(1, "Malformed stimulus row");
            end
            $fclose(vector_file);
        end else if (mode == 2) begin
            // Exhaustive binary input pairs: a reference ceiling, not a cheap test.
            for (o = 0; o < 256; o = o + 1)
                for (r = 0; r < 256; r = r + 1)
                    step(0, r[7:0], o[7:0]);
            step(0, 8'h80, 8'h00);
            step(1, 8'hff, 8'hff);
            step(0, 8'h00, 8'h00);
            if (seen_req !== 9'h1ff || seen_override !== 9'h1ff)
                $fatal(1, "Stimulus partition coverage incomplete");
        end else if (mode != 0) $fatal(1, "Unknown MODE");
        $display("RESULT checks=%0d functional_errors=%0d timing_errors=%0d req_classes=%h override_classes=%h",
                 checks, functional_errors, timing_errors, seen_req, seen_override);
        // Collection mode preserves all counters despite a detected DUT defect.
        // Standalone execution fails loudly by default on any specification error.
        if ((functional_errors != 0 || timing_errors != 0) && !$test$plusargs("COLLECT"))
            $fatal(1, "Specification violations detected");
        $finish;
    end
    initial begin
        #1000000;
        $fatal(1, "Watchdog timeout");
    end
endmodule
