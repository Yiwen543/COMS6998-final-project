//      // verilator_coverage annotation
        `timescale 1ns/1ps
        module tb_fixed_priority_arbiter;
 065544     reg clk = 0, reset = 0;
 032770     reg [7:0] req = 0, priority_override = 0;
 000256     wire [7:0] grant;
 000002     wire valid;
 000171     wire [2:0] grant_index;
 000001     integer checks = 0, functional_errors = 0, timing_errors = 0;
 000001     integer r, o, mode = 2;
            integer vector_file, scan_status, vector_reset, vector_req, vector_override;
~000001     reg initialized = 0;
~000001     reg [8:0] seen_req = 0, seen_override = 0;
            reg [1023:0] vector_path;
        
            fixed_priority_arbiter dut (
                .clk(clk), .reset(reset), .req(req),
                .priority_override(priority_override), .grant(grant),
                .valid(valid), .grant_index(grant_index)
            );
 131087     always #5 clk = ~clk;
        
 065543     task automatic step(input reg rst, input reg [7:0] requests,
                                input reg [7:0] overrides);
 065543         reg [11:0] held;
 065543         reg [7:0] selected, expected_grant;
 065543         reg [2:0] expected_index;
 065543         reg expected_valid;
 065543         integer bit_index;
 065543         begin
 065543             @(negedge clk);
 065543             held = {grant, valid, grant_index};
 065543             reset = rst;
 065543             req = requests;
 065543             priority_override = overrides;
 065543             #1;
~065542             if (initialized && {grant, valid, grant_index} !== held) begin
 000001                 timing_errors = timing_errors + 1;
~000001                 if (timing_errors <= 4)
 000001                     $display("TIMING_FAIL t=%0t reset=%b req=%h override=%h",
 000001                              $time, reset, req, priority_override);
                    end
 065543             selected = rst ? 8'h00 : ((overrides != 0) ? overrides : requests);
 065543             expected_grant = selected & (~selected + 8'd1);
 065543             expected_valid = (selected != 0);
 065543             expected_index = 0;
 524344             for (bit_index = 0; bit_index < 8; bit_index = bit_index + 1)
 458806                 if (expected_grant[bit_index]) expected_index = bit_index[2:0];
 065543             @(posedge clk);
 065543             #1;
 065543             checks = checks + 1;
~063232             if (grant !== expected_grant || valid !== expected_valid ||
 063232                 ((rst || expected_valid) && grant_index !== expected_index)) begin
 063232                 functional_errors = functional_errors + 1;
 063228                 if (functional_errors <= 4)
 000004                     $display("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d",
 000004                              requests, overrides, rst, grant, valid, grant_index,
 000004                              expected_grant, expected_valid, expected_index);
                    end
 065541             if (!rst) begin
 065281                 if (overrides == 0) begin
 000257                     if (expected_valid) seen_req[{1'b0, expected_index}] = 1'b1;
 000003                     else seen_req[8] = 1'b1;
 000260                     seen_override[8] = 1'b1;
 065281                 end else seen_override[{1'b0, expected_index}] = 1'b1;
                    end
 065543             initialized = 1;
                end
            endtask
        
 000001     initial begin
~000001         if ($value$plusargs("MODE=%d", mode)) begin end
                // A small starting test intentionally leaves priority paths uncovered.
 000001         step(1, 8'h00, 8'h00);
 000001         step(0, 8'h00, 8'h00);
 000001         step(0, 8'h01, 8'h00);
 000001         step(0, 8'h00, 8'h01);
%000000         if (mode == 1) begin
%000000             if (!$value$plusargs("VECTORS=%s", vector_path))
                        $fatal(1, "MODE=1 requires +VECTORS=<file>");
%000000             vector_file = $fopen(vector_path, "r");
%000000             if (vector_file == 0) $fatal(1, "Cannot open stimulus file");
%000000             while (!$feof(vector_file)) begin
%000000                 scan_status = $fscanf(vector_file, "%d %h %h\n",
%000000                                       vector_reset, vector_req, vector_override);
%000000                 if (scan_status == 3)
%000000                     step(vector_reset[0], vector_req[7:0], vector_override[7:0]);
%000000                 else if (!$feof(vector_file)) $fatal(1, "Malformed stimulus row");
                    end
%000000             $fclose(vector_file);
 000001         end else if (mode == 2) begin
                    // Exhaustive binary input pairs: a reference ceiling, not a cheap test.
 000256             for (o = 0; o < 256; o = o + 1)
 065536                 for (r = 0; r < 256; r = r + 1)
 065536                     step(0, r[7:0], o[7:0]);
 000001             step(0, 8'h80, 8'h00);
 000001             step(1, 8'hff, 8'hff);
 000001             step(0, 8'h00, 8'h00);
~000001             if (seen_req !== 9'h1ff || seen_override !== 9'h1ff)
                        $fatal(1, "Stimulus partition coverage incomplete");
%000000         end else if (mode != 0) $fatal(1, "Unknown MODE");
 000001         $display("RESULT checks=%0d functional_errors=%0d timing_errors=%0d req_classes=%h override_classes=%h",
 000001                  checks, functional_errors, timing_errors, seen_req, seen_override);
                // Collection mode preserves all counters despite a detected DUT defect.
                // Standalone execution fails loudly by default on any specification error.
 000001         if ((functional_errors != 0 || timing_errors != 0) && !$test$plusargs("COLLECT"))
                    $fatal(1, "Specification violations detected");
 000001         $finish;
            end
            initial begin
                #1000000;
                $fatal(1, "Watchdog timeout");
            end
        endmodule
        
