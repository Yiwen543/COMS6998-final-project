// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtb_natural_inventory.h for the primary calling header

#ifndef VERILATED_VTB_NATURAL_INVENTORY___024ROOT_H_
#define VERILATED_VTB_NATURAL_INVENTORY___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_cov.h"
#include "verilated_covergroup.h"
#include "verilated_timing.h"


class Vtb_natural_inventory__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtb_natural_inventory___024root final {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        CData/*0:0*/ tb_natural_inventory__DOT__clk;
        CData/*0:0*/ tb_natural_inventory__DOT__rst;
        CData/*0:0*/ tb_natural_inventory__DOT__s_valid;
        CData/*0:0*/ tb_natural_inventory__DOT__s_last;
        CData/*0:0*/ tb_natural_inventory__DOT__m_ready;
        CData/*0:0*/ tb_natural_inventory__DOT__h_ready;
        CData/*7:0*/ tb_natural_inventory__DOT__s_data;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__clk;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__rst;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__s_valid;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__s_last;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__m_ready;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__h_ready;
        CData/*7:0*/ tb_natural_inventory__DOT____Vtogcov__s_data;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__s_ready;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__m_valid;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__m_last;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__h_valid;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__h_pad;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__h_truncate;
        CData/*7:0*/ tb_natural_inventory__DOT____Vtogcov__m_data;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tuser;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__pause_req;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem_read_data_valid_reg;
        CData/*1:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg;
        CData/*4:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser;
        CData/*4:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pause_req;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_overflow;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg;
        CData/*3:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mem_read_data_valid_reg;
    };
    struct {
        CData/*1:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full_wr;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__pause_req;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem_read_data_valid_reg;
        CData/*1:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__pause_req;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg;
        CData/*5:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mem_read_data_valid_reg;
        CData/*1:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full_wr;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg;
        CData/*2:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg;
        CData/*2:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_user_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int;
    };
    struct {
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output;
        CData/*2:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg;
        CData/*2:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_last_word;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_data_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_keep_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_id_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_dest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_user_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_temp_to_output;
        CData/*0:0*/ __Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int__0;
        CData/*0:0*/ __VstlDidInit;
    };
    struct {
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk__0;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VinactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
        SData/*15:0*/ tb_natural_inventory__DOT____Vtogcov__h_length;
        SData/*15:0*/ tb_natural_inventory__DOT____Vtogcov__h_original_length;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length;
        SData/*8:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis;
        SData/*8:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_axis;
        SData/*8:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_original_length_next;
        IData/*31:0*/ tb_natural_inventory__DOT____VlemCond_2;
        IData/*31:0*/ tb_natural_inventory__DOT____VlemCond_1;
        IData/*31:0*/ tb_natural_inventory__DOT____VExpr_he4c3ed11__1;
        IData/*31:0*/ tb_natural_inventory__DOT____VExpr_he4c3ed11__0;
        IData/*31:0*/ tb_natural_inventory__DOT__n;
        IData/*31:0*/ tb_natural_inventory__DOT__cycle;
        IData/*31:0*/ tb_natural_inventory__DOT__head;
        IData/*31:0*/ tb_natural_inventory__DOT__tail;
        IData/*31:0*/ tb_natural_inventory__DOT__take;
        IData/*31:0*/ tb_natural_inventory__DOT__r;
        IData/*31:0*/ tb_natural_inventory__DOT__o;
        IData/*31:0*/ tb_natural_inventory__DOT__d;
        IData/*31:0*/ tb_natural_inventory__DOT__l;
        IData/*31:0*/ tb_natural_inventory__DOT__m;
        IData/*31:0*/ tb_natural_inventory__DOT__h;
        IData/*31:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt;
        IData/*31:0*/ __VactIterCount;
        IData/*31:0*/ __VinactIterCount;
        IData/*31:0*/ __Vi;
        QData/*33:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis;
        QData/*33:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata;
        QData/*33:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tdata;
        VlUnpacked<CData/*7:0*/, 512> tb_natural_inventory__DOT__data_q;
        VlUnpacked<CData/*0:0*/, 512> tb_natural_inventory__DOT__last_q;
        VlUnpacked<QData/*33:0*/, 8> tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem;
        VlUnpacked<QData/*33:0*/, 2> tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg;
        VlUnpacked<QData/*33:0*/, 2> tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg;
        VlUnpacked<SData/*8:0*/, 32> tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem;
        VlUnpacked<SData/*8:0*/, 2> tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg;
        VlUnpacked<SData/*8:0*/, 2> tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg;
    };
    struct {
        VlUnpacked<QData/*63:0*/, 2> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };
    std::string tb_natural_inventory__DOT__path;
    VlDelayScheduler __VdlySched;

    // INTERNAL VARIABLES
    Vtb_natural_inventory__Syms* vlSymsp;
    const char* vlNamep;
    uint32_t __Vcoverage[1955]{};

    // CONSTRUCTORS
    Vtb_natural_inventory___024root(Vtb_natural_inventory__Syms* symsp, const char* namep);
    ~Vtb_natural_inventory___024root();
    VL_UNCOPYABLE(Vtb_natural_inventory___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
    void __vlCoverInsert(uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp, const char* linescovp,
        const char* fsmVarp, const char* fsmFromp, const char* fsmTop, const char* fsmTagp);
    void __vlCoverToggleInsert(int begin, int end, bool ranged, uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp);
};


#endif  // guard
