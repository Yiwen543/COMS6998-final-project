`timescale 1ns/1ps
module tb_sync_fifo;
    localparam integer DEPTH = 8;
    reg clk = 0, reset = 0;
    reg push_i = 0, pop_i = 0;
    reg [7:0] push_data_i = 0;
    wire [7:0] pop_data_o;
    wire full_o, empty_o;
    integer checks = 0, functional_errors = 0, status_errors = 0, data_errors = 0;
    integer head = 0, tail = 0, count = 0;
    integer mode = 0, vector_file, scan_status;
    integer vector_reset, vector_push, vector_pop, vector_data;
    reg [7:0] expected [0:DEPTH-1];
    reg [8:0] functional_bins = 0;
    reg [1023:0] vector_path;

    sync_fifo #(.DEPTH(DEPTH), .DATA_W(8)) dut (
        .clk(clk), .reset(reset), .push_i(push_i), .push_data_i(push_data_i),
        .pop_i(pop_i), .pop_data_o(pop_data_o), .full_o(full_o), .empty_o(empty_o)
    );
    always #5 clk = ~clk;

    task automatic check_outputs(input integer cycle_id);
        begin
            if (empty_o !== (count == 0) || full_o !== (count == DEPTH)) begin
                functional_errors = functional_errors + 1;
                status_errors = status_errors + 1;
                if (functional_errors <= 5)
                    $display("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b", cycle_id, count, full_o, empty_o);
            end
            if (count > 0 && pop_data_o !== expected[head]) begin
                functional_errors = functional_errors + 1;
                data_errors = data_errors + 1;
                if (functional_errors <= 5)
                    $display("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h", cycle_id, head, pop_data_o, expected[head]);
            end
        end
    endtask

    task automatic step(input reg rst, input reg push, input reg pop, input reg [7:0] data);
        integer old_count;
        begin
            @(negedge clk);
            old_count = count;
            reset = rst;
            push_i = push;
            pop_i = pop;
            push_data_i = data;
            if (rst) begin
                if (old_count > 0) functional_bins[6] = 1'b1;
                head = 0;
                tail = 0;
                count = 0;
            end else if ((pop && count == 0) || (push && count == DEPTH && !pop))
                $fatal(1, "Illegal FIFO action under frozen contract");
            #1;
            check_outputs(checks);
            if (!rst) begin
                if (count == 0) functional_bins[0] = 1'b1;
                if (count == DEPTH) functional_bins[2] = 1'b1;
                if (count == DEPTH && !push && !pop) functional_bins[7] = 1'b1;
                if (pop) begin
                    functional_bins[1] = 1'b1;
                    if (head == DEPTH-1) functional_bins[5] = 1'b1;
                    if (count == 1 && !push) functional_bins[8] = 1'b1;
                end
                if (push && pop) functional_bins[3] = 1'b1;
                if (push && tail == DEPTH-1) functional_bins[4] = 1'b1;
            end
            @(posedge clk);
            if (!rst) begin
                if (pop) begin
                    head = (head + 1) % DEPTH;
                    count = count - 1;
                end
                if (push) begin
                    expected[tail] = data;
                    tail = (tail + 1) % DEPTH;
                    count = count + 1;
                end
            end
            #1;
            check_outputs(checks);
            checks = checks + 1;
        end
    endtask

    initial begin
        if ($value$plusargs("MODE=%d", mode)) begin end
        step(1, 0, 0, 8'h00);
        step(0, 1, 0, 8'h11);
        step(0, 0, 1, 8'h00);
        step(0, 0, 0, 8'h00);
        if (mode == 1) begin
            if (!$value$plusargs("VECTORS=%s", vector_path))
                $fatal(1, "MODE=1 requires +VECTORS=<file>");
            vector_file = $fopen(vector_path, "r");
            if (vector_file == 0) $fatal(1, "Cannot open stimulus file");
            while (!$feof(vector_file)) begin
                scan_status = $fscanf(vector_file, "%d %d %d %h\n",
                                      vector_reset, vector_push, vector_pop, vector_data);
                if (scan_status == 4)
                    step(vector_reset[0], vector_push[0], vector_pop[0], vector_data[7:0]);
                else if (!$feof(vector_file)) $fatal(1, "Malformed stimulus row");
            end
            $fclose(vector_file);
        end else if (mode != 0) $fatal(1, "Unknown MODE");
        $display("RESULT checks=%0d functional_errors=%0d status_errors=%0d data_errors=%0d bins=%h", checks, functional_errors, status_errors, data_errors, functional_bins);
        if (functional_errors != 0 && !$test$plusargs("COLLECT"))
            $fatal(1, "FIFO contract violation detected");
        $finish;
    end
    initial begin
        #1000000;
        $fatal(1, "Watchdog timeout");
    end
endmodule
