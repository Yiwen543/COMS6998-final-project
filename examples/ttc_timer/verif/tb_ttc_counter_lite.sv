`timescale 1ns/1ps
module tb_ttc_counter_lite;
    reg clk = 0, reset = 0, axi_write_en = 0, axi_read_en = 0;
    reg [3:0] axi_addr = 0;
    reg [31:0] axi_wdata = 0;
    wire [31:0] axi_rdata;
    wire interrupt;
    integer checks = 0, read_errors = 0, interrupt_errors = 0, timing_errors = 0;
    integer mode = 0, vector_file, scan_status;
    integer v_reset, v_write, v_read, v_addr, v_data;
    reg [1023:0] vector_path;
    reg [15:0] ref_count = 0, ref_match = 0, ref_reload = 0;
    reg [3:0] ref_prescaler = 0, ref_divider = 0;
    reg ref_enable = 0, ref_interval = 0, ref_irq_enable = 0;
    reg ref_match_pending = 0, ref_interrupt = 0;
    reg [31:0] ref_rdata = 0;
    reg [15:0] old_count, old_match;
    reg [3:0] old_divider, old_prescaler;
    reg old_enable, old_interval, old_irq_enable, old_match_pending, old_interrupt;
    reg [31:0] before_rdata;
    reg before_interrupt;

    ttc_counter_lite dut (
        .clk(clk), .reset(reset), .axi_addr(axi_addr), .axi_wdata(axi_wdata),
        .axi_write_en(axi_write_en), .axi_read_en(axi_read_en),
        .axi_rdata(axi_rdata), .interrupt(interrupt)
    );
    always #5 clk = ~clk;

    task automatic step(input reg rst, input reg wr, input reg rd,
                        input reg [3:0] addr, input reg [31:0] data);
        begin
            if (wr && rd) $fatal(1, "Simultaneous read/write is outside frozen contract");
            if (rst && (wr || rd)) $fatal(1, "Bus access during reset is outside frozen contract");
            @(negedge clk);
            before_rdata = axi_rdata;
            before_interrupt = interrupt;
            reset = rst;
            axi_write_en = wr;
            axi_read_en = rd;
            axi_addr = addr;
            axi_wdata = data;
            #1;
            // The supplied specification requires synchronous reset. Check
            // externally visible outputs before the next rising edge.
            if (rst && checks > 0 &&
                (axi_rdata !== before_rdata || interrupt !== before_interrupt)) begin
                timing_errors = timing_errors + 1;
                if (timing_errors <= 5)
                    $display("TIMING_FAIL cycle=%0d before_rdata=%h now=%h before_irq=%b now=%b",
                             checks, before_rdata, axi_rdata, before_interrupt, interrupt);
            end
            old_count = ref_count;
            old_match = ref_match;
            old_divider = ref_divider;
            old_prescaler = ref_prescaler;
            old_enable = ref_enable;
            old_interval = ref_interval;
            old_irq_enable = ref_irq_enable;
            old_match_pending = ref_match_pending;
            old_interrupt = ref_interrupt;
            @(posedge clk);
            if (rst) begin
                ref_count = 0;
                ref_match = 0;
                ref_reload = 0;
                ref_prescaler = 0;
                ref_divider = 0;
                ref_enable = 0;
                ref_interval = 0;
                ref_irq_enable = 0;
                ref_match_pending = 0;
                ref_interrupt = 0;
                ref_rdata = 0;
            end else begin
                // Independent arithmetic/reference-state model. All reads and
                // timer decisions use the values from before this edge.
                if (old_enable) begin
                    if (old_divider == old_prescaler) begin
                        ref_divider = 0;
                        if (old_interval && old_match_pending)
                            ref_count = ref_reload;
                        else if (old_count != old_match)
                            ref_count = old_count + 16'd1;
                    end else ref_divider = old_divider + 4'd1;
                end
                ref_match_pending = (old_count == old_match);
                if (old_match_pending && old_irq_enable)
                    ref_interrupt = 1;
                else if (wr && addr == 4'h4)
                    ref_interrupt = 0;
                if (rd) begin
                    case (addr)
                        4'h0: ref_rdata = {16'b0, old_count};
                        4'h1: ref_rdata = {16'b0, old_match};
                        4'h2: ref_rdata = {16'b0, ref_reload};
                        4'h3: ref_rdata = {29'b0, old_irq_enable, old_interval, old_enable};
                        4'h4: ref_rdata = {31'b0, old_interrupt};
                        4'h5: ref_rdata = {28'b0, old_prescaler};
                        default: ref_rdata = 0;
                    endcase
                end
                if (wr) begin
                    case (addr)
                        4'h1: ref_match = data[15:0];
                        4'h2: ref_reload = data[15:0];
                        4'h3: begin
                            ref_enable = data[0];
                            ref_interval = data[1];
                            ref_irq_enable = data[2];
                        end
                        4'h5: ref_prescaler = data[3:0];
                        default: ;
                    endcase
                end
            end
            #1;
            if (axi_rdata !== ref_rdata) begin
                read_errors = read_errors + 1;
                if (read_errors <= 5)
                    $display("READ_FAIL cycle=%0d addr=%h got=%h expected=%h",
                             checks, addr, axi_rdata, ref_rdata);
            end
            if (interrupt !== ref_interrupt) begin
                interrupt_errors = interrupt_errors + 1;
                if (interrupt_errors <= 5)
                    $display("IRQ_FAIL cycle=%0d got=%b expected=%b",
                             checks, interrupt, ref_interrupt);
            end
            checks = checks + 1;
        end
    endtask

    initial begin
        if ($value$plusargs("MODE=%d", mode)) begin end
        step(1, 0, 0, 4'h0, 32'h0);
        step(0, 1, 0, 4'h1, 32'h4);
        step(0, 1, 0, 4'h3, 32'h5);
        step(0, 0, 1, 4'h1, 32'h0);
        step(0, 0, 0, 4'h0, 32'h0);
        if (mode == 1) begin
            if (!$value$plusargs("VECTORS=%s", vector_path))
                $fatal(1, "MODE=1 requires +VECTORS=<file>");
            vector_file = $fopen(vector_path, "r");
            if (vector_file == 0) $fatal(1, "Cannot open vectors");
            while (!$feof(vector_file)) begin
                scan_status = $fscanf(vector_file, "%d %d %d %h %h\n",
                                      v_reset, v_write, v_read, v_addr, v_data);
                if (scan_status == 5)
                    step(v_reset[0], v_write[0], v_read[0], v_addr[3:0], v_data[31:0]);
                else if (!$feof(vector_file)) $fatal(1, "Malformed vector row");
            end
            $fclose(vector_file);
        end else if (mode != 0) $fatal(1, "Unknown mode");
        $display("RESULT checks=%0d read_errors=%0d interrupt_errors=%0d timing_errors=%0d",
                 checks, read_errors, interrupt_errors, timing_errors);
        if ((read_errors + interrupt_errors + timing_errors) != 0 && !$test$plusargs("COLLECT"))
            $fatal(1, "Timer contract violation detected");
        $finish;
    end
    initial begin
        #1000000;
        $fatal(1, "Watchdog timeout");
    end
endmodule
