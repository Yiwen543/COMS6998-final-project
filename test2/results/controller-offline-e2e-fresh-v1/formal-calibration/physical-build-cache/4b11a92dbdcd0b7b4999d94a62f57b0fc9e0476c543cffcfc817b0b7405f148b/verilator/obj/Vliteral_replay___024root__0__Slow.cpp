// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vliteral_replay.h for the primary calling header

#include "Vliteral_replay__pch.h"

VL_ATTR_COLD void Vliteral_replay___024root___eval_static(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_static\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_static__TOP
        vlSelfRef.literal_replay__DOT__clk = 0U;
        vlSelfRef.literal_replay__DOT__rst = 0U;
        vlSelfRef.literal_replay__DOT__s_valid = 0U;
        vlSelfRef.literal_replay__DOT__s_data = 0U;
        vlSelfRef.literal_replay__DOT__s_last = 0U;
        vlSelfRef.literal_replay__DOT__m_ready = 0U;
        vlSelfRef.literal_replay__DOT__h_ready = 0U;
        vlSelfRef.literal_replay__DOT__cycle = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg = 0U;
    }
    vlSelfRef.__Vtrigprevexpr___TOP__literal_replay__DOT__clk__0 = 0U;
    do {
        vlSelfRef.__VactTriggeredAcc[vlSelfRef.__Vi] 
            = vlSelfRef.__VactTriggered[vlSelfRef.__Vi];
        vlSelfRef.__Vi = ((IData)(1U) + vlSelfRef.__Vi);
    } while ((0U >= vlSelfRef.__Vi));
}

VL_ATTR_COLD void Vliteral_replay___024root___eval_final(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_final\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vliteral_replay___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vliteral_replay___024root___eval_phase__stl(Vliteral_replay___024root* vlSelf);

VL_ATTR_COLD void Vliteral_replay___024root___eval_settle(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_settle\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vliteral_replay___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-offline-e2e-fresh-v1/formal-calibration/physical-build-cache/4b11a92dbdcd0b7b4999d94a62f57b0fc9e0476c543cffcfc817b0b7405f148b/verilator/driver.sv", 2, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vliteral_replay___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vliteral_replay___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vliteral_replay___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vliteral_replay___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vliteral_replay___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___trigger_anySet__stl\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

VL_ATTR_COLD void Vliteral_replay___024root___stl_sequent__TOP__0(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___stl_sequent__TOP__0\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*7:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked = 0;
    CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0;
    // Body
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int = 0U;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked 
        = vlSelfRef.literal_replay__DOT__s_data;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready 
        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
           != (8U ^ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg)));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full 
        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
           == (0x20U ^ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg)));
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
    if ((0U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = vlSelfRef.literal_replay__DOT__s_valid;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                if ((1U & (~ (IData)(vlSelfRef.literal_replay__DOT__s_last)))) {
                    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                }
            }
        }
    } else if ((1U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = vlSelfRef.literal_replay__DOT__s_valid;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                if ((1U & (~ (IData)(vlSelfRef.literal_replay__DOT__s_last)))) {
                    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                }
            }
        }
    } else if ((2U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int = 0U;
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 1U;
    } else if ((3U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg;
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = ((IData)(vlSelfRef.literal_replay__DOT__s_valid) 
               & (IData)(vlSelfRef.literal_replay__DOT__s_last));
    }
    vlSelfRef.__VdfgRegularize_hebeb780c_0_0 = ((((IData)(literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
                                                  << 4U) 
                                                 | (((2U 
                                                      & ((~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
                                                         << 1U)) 
                                                     | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg)) 
                                                    << 2U)) 
                                                | (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
                                                    << 1U) 
                                                   | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early 
        = (1U & (~ ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
                    & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
                       | ((IData)(literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
                          & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))))));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next 
        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
           & (~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready)));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
    if ((0U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
               & ((~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)) 
                  | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready)));
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.literal_replay__DOT__s_last;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg)));
                if (vlSelfRef.literal_replay__DOT__s_last) {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
                        = (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt 
                           > (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                }
            } else if (vlSelfRef.literal_replay__DOT__s_last) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                     > vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt)) {
                    if ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                    } else {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                               & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                            = VL_SHIFTR_III(1,1,32, 1U, 
                                            ((IData)(1U) 
                                             - ((IData)(4U) 
                                                - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg))));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    }
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                }
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
        }
    } else if ((1U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.literal_replay__DOT__s_last;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg)));
                if (vlSelfRef.literal_replay__DOT__s_last) {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
                        = (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt 
                           > (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                }
            } else if (vlSelfRef.literal_replay__DOT__s_last) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                     > vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt)) {
                    if ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                    } else {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                               & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                            = VL_SHIFTR_III(1,1,32, 1U, 
                                            ((IData)(1U) 
                                             - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg)));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    }
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                }
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
        }
    } else if ((2U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
        if (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                       & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg)));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
        }
    } else if ((3U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.literal_replay__DOT__s_last;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            if (vlSelfRef.literal_replay__DOT__s_last) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                       & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
        }
    }
}

VL_ATTR_COLD bool Vliteral_replay___024root___eval_phase__stl(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_phase__stl\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__stl
        vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                          & vlSelfRef.__VstlTriggered[0U]) 
                                         | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vliteral_replay___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vliteral_replay___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                Vliteral_replay___024root___stl_sequent__TOP__0(vlSelf);
            }
        }
    }
    return (__VstlExecute);
}

bool Vliteral_replay___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vliteral_replay___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vliteral_replay___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge literal_replay.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vliteral_replay___024root___ctor_var_reset(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___ctor_var_reset\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->literal_replay__DOT__n = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7125227484334641532ull);
    vlSelf->literal_replay__DOT__v_rst = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12608846879869812263ull);
    vlSelf->literal_replay__DOT__v_s_valid = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10190827314258992863ull);
    vlSelf->literal_replay__DOT__v_s_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5607591569470799842ull);
    vlSelf->literal_replay__DOT__v_s_last = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5608099317839466562ull);
    vlSelf->literal_replay__DOT__v_m_ready = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 21209906994835382ull);
    vlSelf->literal_replay__DOT__v_h_ready = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9343933735154101055ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__status_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10055171098800789705ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem[__Vi0] = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 13510889059255950084ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[__Vi0] = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 8946576505216143202ull);
    }
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem[__Vi0] = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 16827105660114398000ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[__Vi0] = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 11064524724950766643ull);
    }
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1325695986854391517ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5859915460492036389ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14049443440793936859ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11584597923299842211ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18199721345564233196ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16485875529981653429ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9837999204582187876ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8943281187363305490ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12763840557485891422ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17204507965236546729ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5211881384536439700ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18294434019621081263ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14457704054953716069ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14020331383910080036ull);
    vlSelf->literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15883118220326763620ull);
    vlSelf->__VdfgRegularize_hebeb780c_0_0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggeredAcc[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__literal_replay__DOT__clk__0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
    vlSelf->__Vi = 0;
}
