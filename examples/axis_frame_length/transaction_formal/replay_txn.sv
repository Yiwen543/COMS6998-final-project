`timescale 1ns/1ps
module replay_txn;
    reg clk = 0, rst, s_valid, s_last, m_ready, h_ready;
    reg [7:0] s_data;
    wire s_ready, m_valid, m_last, h_valid, h_pad, h_truncate;
    wire [7:0] m_data;
    wire [15:0] h_length, h_original_length;
    frame_task dut(.*);
    integer fd, fields, cycle = 0;

    task sample(input [31:0] phase);
        $display("%0s %0d %b %b %h %b %b %b %b %h %b %b %b %b %b %h %h",
                 phase, cycle, rst, s_valid, s_data, s_last, m_ready, h_ready, s_ready,
                 m_data, m_valid, m_last, h_valid, h_pad, h_truncate, h_length, h_original_length);
    endtask

    initial begin
        fd = $fopen("inputs.txt", "r");
        if (!fd) $fatal(1, "Missing primary input vectors");
        while (!$feof(fd)) begin
            fields = $fscanf(fd, "%d %d %h %d %d %d\n", rst, s_valid, s_data, s_last, m_ready, h_ready);
            if (fields == 6) begin
                #4; sample("PRE");
                #1; clk = 1;
                #1; sample("POST");
                #3; clk = 0;
                #1; cycle = cycle + 1;
            end else if (!$feof(fd)) $fatal(1, "Invalid input vector");
        end
        $display("REPLAY_COMPLETE %0d", cycle);
        $finish;
    end
endmodule
