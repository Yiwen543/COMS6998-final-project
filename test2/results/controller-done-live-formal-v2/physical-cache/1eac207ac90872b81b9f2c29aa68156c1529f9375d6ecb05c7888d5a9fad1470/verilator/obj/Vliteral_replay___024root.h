// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vliteral_replay.h for the primary calling header

#ifndef VERILATED_VLITERAL_REPLAY___024ROOT_H_
#define VERILATED_VLITERAL_REPLAY___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vliteral_replay__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vliteral_replay___024root final {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        CData/*0:0*/ literal_replay__DOT__clk;
        CData/*0:0*/ literal_replay__DOT__rst;
        CData/*0:0*/ literal_replay__DOT__s_valid;
        CData/*7:0*/ literal_replay__DOT__s_data;
        CData/*0:0*/ literal_replay__DOT__s_last;
        CData/*0:0*/ literal_replay__DOT__m_ready;
        CData/*0:0*/ literal_replay__DOT__h_ready;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__status_ready;
        CData/*3:0*/ literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
        CData/*3:0*/ literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg;
        CData/*3:0*/ literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg;
        CData/*1:0*/ literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
        CData/*5:0*/ literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
        CData/*5:0*/ literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg;
        CData/*5:0*/ literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg;
        CData/*1:0*/ literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full;
        CData/*2:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg;
        CData/*2:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word;
        CData/*7:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next;
        CData/*7:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg;
        CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg;
        CData/*4:0*/ __VdfgRegularize_hebeb780c_0_0;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__literal_replay__DOT__clk__0;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VinactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
        SData/*15:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next;
        IData/*31:0*/ literal_replay__DOT____VlemExpr_1;
        IData/*31:0*/ literal_replay__DOT__n;
        IData/*31:0*/ literal_replay__DOT__cycle;
        IData/*31:0*/ literal_replay__DOT__v_rst;
        IData/*31:0*/ literal_replay__DOT__v_s_valid;
        IData/*31:0*/ literal_replay__DOT__v_s_data;
        IData/*31:0*/ literal_replay__DOT__v_s_last;
        IData/*31:0*/ literal_replay__DOT__v_m_ready;
        IData/*31:0*/ literal_replay__DOT__v_h_ready;
        IData/*31:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt;
        IData/*31:0*/ __VactIterCount;
    };
    struct {
        IData/*31:0*/ __VinactIterCount;
        IData/*31:0*/ __Vi;
        VlUnpacked<QData/*33:0*/, 8> literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem;
        VlUnpacked<QData/*33:0*/, 2> literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg;
        VlUnpacked<SData/*8:0*/, 32> literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem;
        VlUnpacked<SData/*8:0*/, 2> literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };
    std::string literal_replay__DOT__path;
    VlDelayScheduler __VdlySched;

    // INTERNAL VARIABLES
    Vliteral_replay__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vliteral_replay___024root(Vliteral_replay__Syms* symsp, const char* namep);
    ~Vliteral_replay___024root();
    VL_UNCOPYABLE(Vliteral_replay___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
