`timescale 1ns/1ps
module replay_cover;
    reg clk = 0, rst, s_valid, s_last, m_ready, h_ready;
    reg [7:0] s_data;
    wire s_ready, m_valid, m_last, h_valid, h_pad, h_truncate;
    wire [7:0] m_data;
    wire [15:0] h_length, h_original_length;
    frame_task dut(.*);
    integer fd, n, step = 0;
    initial begin
        fd = $fopen("inputs.txt", "r");
        if (!fd) $fatal(1, "Missing cover witness");
        while (!$feof(fd)) begin
            n = $fscanf(fd, "%d %d %h %d %d %d\n", rst, s_valid, s_data, s_last, m_ready, h_ready);
            if (n == 6) begin
                #4;
                $display("PRE %0d %b %b %h %b %b %b %b %h %b %b %b %b %b %h %h",
                         step, rst, s_valid, s_data, s_last, m_ready, h_ready, s_ready,
                         m_data, m_valid, m_last, h_valid, h_pad, h_truncate, h_length, h_original_length);
                #1 clk = 1;
                #4 clk = 0;
                #1;
                step = step + 1;
            end else if (!$feof(fd)) $fatal(1, "Malformed input row");
        end
        $display("REPLAY_COMPLETE %0d", step);
        $fclose(fd);
        $finish;
    end
endmodule
