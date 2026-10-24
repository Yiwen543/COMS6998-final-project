`timescale 1ns/1ps
`ifndef DUT_MODULE
`define DUT_MODULE queue
`endif
module tb_queue_pilot;
  localparam integer DEPTH = 4;
  localparam integer CAPACITY = DEPTH - 1;
  logic clk_i = 0, rst_ni = 1, clr_i = 0, ena_i = 0, we_i = 0, re_i = 0;
  logic [31:0] d_i = 0;
  wire [31:0] q_o;
  wire empty_o, full_o, almost_empty_o, almost_full_o;
  integer checks = 0, data_errors = 0, occupancy_errors = 0;
  integer reset_errors = 0, clear_errors = 0, enable_errors = 0;
  integer count = 0, vector_file, scan_status, mode = 0;
  integer v_reset_n, v_clear, v_enable, v_write, v_read;
  logic [31:0] v_data;
  logic [31:0] expected [0:CAPACITY-1];
  logic [31:0] before_q;
  logic before_empty, before_full;
  reg [1023:0] vector_path;

  `DUT_MODULE #(.DEPTH(DEPTH), .DBITS(32)) dut (
    .rst_ni, .clk_i, .clr_i, .ena_i, .we_i, .d_i, .re_i,
    .q_o, .empty_o, .full_o, .almost_empty_o, .almost_full_o
  );
  always #5 clk_i = ~clk_i;

  task automatic check_outputs(input integer cycle_id);
    begin
      if (empty_o !== (count == 0) || full_o !== (count == CAPACITY)) begin
        occupancy_errors = occupancy_errors + 1;
        if (occupancy_errors <= 5)
          $display("OCCUPANCY_FAIL cycle=%0d count=%0d empty=%b full=%b", cycle_id, count, empty_o, full_o);
      end
      if (count > 0 && q_o !== expected[0]) begin
        data_errors = data_errors + 1;
        if (data_errors <= 5)
          $display("DATA_FAIL cycle=%0d count=%0d got=%h expected=%h", cycle_id, count, q_o, expected[0]);
      end
    end
  endtask

  task automatic step(input logic reset_n, clear, enable, write_en, read_en,
                      input logic [31:0] data);
    integer j, old_count;
    begin
      @(negedge clk_i);
      old_count = count;
      before_q = q_o;
      before_empty = empty_o;
      before_full = full_o;
      rst_ni = reset_n;
      clr_i = clear;
      ena_i = enable;
      we_i = write_en;
      re_i = read_en;
      d_i = data;
      if (reset_n && !clear && enable) begin
        if (write_en && !read_en && count >= CAPACITY)
          $fatal(1, "Illegal write-only at full queue");
        if (read_en && !write_en && count == 0)
          $fatal(1, "Illegal read-only at empty queue");
      end
      #1;
      if (!reset_n) begin
        if (q_o !== 0 || empty_o !== 1 || full_o !== 0 ||
            almost_empty_o !== 1 || almost_full_o !== 0) begin
          reset_errors = reset_errors + 1;
          if (reset_errors <= 5)
            $display("RESET_FAIL cycle=%0d q=%h empty=%b full=%b", checks, q_o, empty_o, full_o);
        end
      end else if (clear && checks > 0 &&
                   (q_o !== before_q || empty_o !== before_empty || full_o !== before_full)) begin
        clear_errors = clear_errors + 1;
        if (clear_errors <= 5) $display("CLEAR_FAIL cycle=%0d changed_before_edge", checks);
      end
      @(posedge clk_i);
      if (!reset_n || clear) begin
        count = 0;
        for (j = 0; j < CAPACITY; j = j + 1) expected[j] = 0;
      end else if (enable) begin
        if (write_en && read_en) begin
          if (count > 0) begin
            for (j = 0; j < CAPACITY-1; j = j + 1) expected[j] = expected[j+1];
            expected[count-1] = data;
          end
          // At empty, q_o exposes data, but no valid item is retained.
        end else if (read_en) begin
          for (j = 0; j < CAPACITY-1; j = j + 1) expected[j] = expected[j+1];
          count = count - 1;
        end else if (write_en) begin
          expected[count] = data;
          count = count + 1;
        end
      end
      #1;
      check_outputs(checks);
      if (reset_n && !clear && enable && write_en && read_en && old_count == 0 && q_o !== data) begin
        data_errors = data_errors + 1;
        if (data_errors <= 5)
          $display("DATA_FAIL cycle=%0d empty_simultaneous got=%h expected=%h", checks, q_o, data);
      end
      if (!reset_n || clear) begin
        if (q_o !== 0 || empty_o !== 1 || full_o !== 0 ||
            almost_empty_o !== 1 || almost_full_o !== 0) begin
          if (!reset_n) reset_errors = reset_errors + 1;
          else clear_errors = clear_errors + 1;
          if (reset_errors + clear_errors <= 5)
            $display("%s_FAIL cycle=%0d after_edge", reset_n ? "CLEAR" : "RESET", checks);
        end
      end
      if (reset_n && !clear && !enable &&
          (q_o !== before_q || empty_o !== before_empty || full_o !== before_full)) begin
        enable_errors = enable_errors + 1;
        if (enable_errors <= 5) $display("ENABLE_FAIL cycle=%0d hold_violation", checks);
      end
      checks = checks + 1;
    end
  endtask

  initial begin
    if ($value$plusargs("MODE=%d", mode)) begin end
    step(0, 0, 0, 0, 0, 0);
    step(0, 0, 0, 0, 0, 0);
    repeat (4) step(1, 0, 0, 0, 0, 0);
    if (mode == 1) begin
      if (!$value$plusargs("VECTORS=%s", vector_path)) $fatal(1, "Missing vector path");
      vector_file = $fopen(vector_path, "r");
      if (vector_file == 0) $fatal(1, "Cannot open vectors");
      while (!$feof(vector_file)) begin
        scan_status = $fscanf(vector_file, "%d %d %d %d %d %h\n",
                              v_reset_n, v_clear, v_enable, v_write, v_read, v_data);
        if (scan_status == 6)
          step(v_reset_n[0], v_clear[0], v_enable[0], v_write[0], v_read[0], v_data);
        else if (!$feof(vector_file)) $fatal(1, "Malformed vector row");
      end
      $fclose(vector_file);
    end else if (mode != 0) $fatal(1, "Unknown mode");
    $display("RESULT checks=%0d data_errors=%0d occupancy_errors=%0d reset_errors=%0d clear_errors=%0d enable_errors=%0d",
             checks, data_errors, occupancy_errors, reset_errors, clear_errors, enable_errors);
    if (data_errors + occupancy_errors + reset_errors + clear_errors + enable_errors != 0 &&
        !$test$plusargs("COLLECT")) $fatal(1, "Queue specification violation");
    $finish;
  end
  initial begin
    #1000000;
    $fatal(1, "Watchdog timeout");
  end
endmodule
