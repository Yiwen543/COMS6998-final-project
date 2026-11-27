`timescale 1ns/1ps
module replay_fifo;
    reg clk = 0;
    reg rst, s_axis_tvalid, s_axis_tlast, s_axis_tuser, m_axis_tready;
    reg [7:0] s_axis_tdata;
    wire s_axis_tready, m_axis_tvalid, m_axis_tlast, m_axis_tuser;
    wire [7:0] m_axis_tdata;

    axis_fifo #(
        .DEPTH(4), .DATA_WIDTH(8), .KEEP_ENABLE(0), .KEEP_WIDTH(1), .LAST_ENABLE(1),
        .ID_ENABLE(0), .ID_WIDTH(1), .DEST_ENABLE(0), .DEST_WIDTH(1),
        .USER_ENABLE(1), .USER_WIDTH(1), .RAM_PIPELINE(1),
        .OUTPUT_FIFO_ENABLE(0), .FRAME_FIFO(0), .PAUSE_ENABLE(0)
    ) dut (
        .clk(clk), .rst(rst), .s_axis_tvalid(s_axis_tvalid), .s_axis_tready(s_axis_tready),
        .s_axis_tdata(s_axis_tdata), .s_axis_tlast(s_axis_tlast), .s_axis_tuser(s_axis_tuser),
        .s_axis_tkeep(1'b1), .s_axis_tid(1'b0), .s_axis_tdest(1'b0), .pause_req(1'b0),
        .m_axis_tvalid(m_axis_tvalid), .m_axis_tready(m_axis_tready),
        .m_axis_tdata(m_axis_tdata), .m_axis_tlast(m_axis_tlast), .m_axis_tuser(m_axis_tuser)
    );

    integer fd, scan, step;
    initial begin
        fd = $fopen("witness.txt", "r");
        if (!fd) $fatal(1, "witness.txt missing");
        step = 0;
        while (!$feof(fd)) begin
            scan = $fscanf(fd, "%b %b %b %b %b %b\n", rst, s_axis_tvalid, s_axis_tdata,
                           s_axis_tlast, s_axis_tuser, m_axis_tready);
            if (scan == 6) begin
                #2;
                // Observe the settled state and current inputs before the active edge.
                $display("PRE %0d %b %b %b %b %b %b %b %b %b %b %b", step, rst,
                         s_axis_tvalid, s_axis_tdata, s_axis_tlast, s_axis_tuser, m_axis_tready,
                         s_axis_tready, m_axis_tvalid, m_axis_tdata, m_axis_tlast, m_axis_tuser);
                clk = 1; #2; clk = 0; #2;
                step = step + 1;
            end else if (!$feof(fd)) $fatal(1, "malformed input vector");
        end
        $fclose(fd);
        $display("REPLAY_COMPLETE %0d", step);
        $finish;
    end
endmodule
