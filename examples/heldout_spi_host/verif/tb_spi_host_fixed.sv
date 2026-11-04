`timescale 1ns/1ps
module tb_spi_host_fixed;
  import spi_host_cmd_pkg::*;
  logic clk_i = 0;
  command_t command_i;
  logic rst_ni = 1;
  logic en_i = 0;
  logic sw_rst_i = 0;
  logic command_valid_i = 0;
  logic command_csid_i = 0;
  logic sr_wr_ready_i = 0;
  logic sr_rd_ready_i = 0;
  wire command_ready_o;
  wire sck_o;
  wire [1:0] csb_o;
  wire [3:0] sd_en_o;
  wire last_read_o;
  wire last_write_o;
  wire wr_en_o;
  wire rd_en_o;
  wire sample_en_o;
  wire shift_en_o;
  wire [1:0] speed_o;
  wire full_cyc_o;
  wire rx_stall_o;
  wire tx_stall_o;
  wire active_o;
  integer fd, got, cycle;
  string vector_path;
  integer v_rst_n, v_enable, v_sw_reset, v_valid, v_csid, v_speed, v_write, v_read, v_length, v_keep_cs, v_clkdiv, v_idle, v_lead, v_trail, v_full_cycle, v_cpha, v_cpol, v_tx_ready, v_rx_ready;
  spi_host_fsm #(.NumCS(2)) dut (
    .clk_i(clk_i),
    .command_i(command_i),
    .rst_ni(rst_ni),
    .en_i(en_i),
    .sw_rst_i(sw_rst_i),
    .command_valid_i(command_valid_i),
    .command_csid_i(command_csid_i),
    .sr_wr_ready_i(sr_wr_ready_i),
    .sr_rd_ready_i(sr_rd_ready_i),
    .command_ready_o(command_ready_o),
    .sck_o(sck_o),
    .csb_o(csb_o),
    .sd_en_o(sd_en_o),
    .last_read_o(last_read_o),
    .last_write_o(last_write_o),
    .wr_en_o(wr_en_o),
    .rd_en_o(rd_en_o),
    .sample_en_o(sample_en_o),
    .shift_en_o(shift_en_o),
    .speed_o(speed_o),
    .full_cyc_o(full_cyc_o),
    .rx_stall_o(rx_stall_o),
    .tx_stall_o(tx_stall_o),
    .active_o(active_o)
  );
  initial begin
    command_i = '0;
    if (!$value$plusargs("VECTORS=%s", vector_path)) $fatal(1, "VECTORS missing");
    fd = $fopen(vector_path, "r");
    if (!fd) $fatal(1, "Cannot open vectors");
    cycle = 0;
    while (!$feof(fd)) begin
      got = $fscanf(fd, "%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n", v_rst_n, v_enable, v_sw_reset, v_valid, v_csid, v_speed, v_write, v_read, v_length, v_keep_cs, v_clkdiv, v_idle, v_lead, v_trail, v_full_cycle, v_cpha, v_cpol, v_tx_ready, v_rx_ready);
      if (got == 19) begin
        rst_ni = v_rst_n[0:0];
        en_i = v_enable[0:0];
        sw_rst_i = v_sw_reset[0:0];
        command_valid_i = v_valid[0:0];
        command_csid_i = v_csid[0:0];
        command_i.segment.speed = v_speed[1:0];
        command_i.segment.cmd_wr_en = v_write[0:0];
        command_i.segment.cmd_rd_en = v_read[0:0];
        command_i.segment.len = v_length[19:0];
        command_i.segment.csaat = v_keep_cs[0:0];
        command_i.configopts.clkdiv = v_clkdiv[15:0];
        command_i.configopts.csnidle = v_idle[3:0];
        command_i.configopts.csnlead = v_lead[3:0];
        command_i.configopts.csntrail = v_trail[3:0];
        command_i.configopts.full_cyc = v_full_cycle[0:0];
        command_i.configopts.cpha = v_cpha[0:0];
        command_i.configopts.cpol = v_cpol[0:0];
        sr_wr_ready_i = v_tx_ready[0:0];
        sr_rd_ready_i = v_rx_ready[0:0];
        #2;
        $write("TRACE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d", cycle, v_rst_n, v_enable, v_sw_reset, v_valid, v_csid, v_speed, v_write, v_read, v_length, v_keep_cs, v_clkdiv, v_idle, v_lead, v_trail, v_full_cycle, v_cpha, v_cpol, v_tx_ready, v_rx_ready, command_ready_o, sck_o, csb_o, sd_en_o, last_read_o, last_write_o, wr_en_o, rd_en_o, sample_en_o, shift_en_o, speed_o, full_cyc_o, rx_stall_o, tx_stall_o, active_o);
        #1; clk_i = 1;
        #1;
        $display(" %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d", command_ready_o, sck_o, csb_o, sd_en_o, last_read_o, last_write_o, wr_en_o, rd_en_o, sample_en_o, shift_en_o, speed_o, full_cyc_o, rx_stall_o, tx_stall_o, active_o);
        #1; clk_i = 0;
        cycle = cycle + 1;
      end else if (got != -1) $fatal(1, "Malformed vectors");
    end
    $fclose(fd);
    $display("DRIVER_OK steps=%0d", cycle);
    $finish;
  end
endmodule
