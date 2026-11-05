// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_natural_inventory.h for the primary calling header

#include "Vtb_natural_inventory__pch.h"

VL_ATTR_COLD void Vtb_natural_inventory___024root___eval_static(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_static\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_static__TOP
        vlSelfRef.tb_natural_inventory__DOT__clk = 0U;
        ++(vlSelf->__Vcoverage[2]);
        vlSelfRef.tb_natural_inventory__DOT__rst = 0U;
        ++(vlSelf->__Vcoverage[5]);
        vlSelfRef.tb_natural_inventory__DOT__s_valid = 0U;
        ++(vlSelf->__Vcoverage[8]);
        vlSelfRef.tb_natural_inventory__DOT__s_last = 0U;
        ++(vlSelf->__Vcoverage[11]);
        vlSelfRef.tb_natural_inventory__DOT__m_ready = 1U;
        ++(vlSelf->__Vcoverage[14]);
        vlSelfRef.tb_natural_inventory__DOT__h_ready = 1U;
        ++(vlSelf->__Vcoverage[17]);
        vlSelfRef.tb_natural_inventory__DOT__s_data = 0U;
        ++(vlSelf->__Vcoverage[34]);
        vlSelfRef.tb_natural_inventory__DOT__cycle = 0U;
        ++(vlSelf->__Vcoverage[127]);
        vlSelfRef.tb_natural_inventory__DOT__head = 0U;
        ++(vlSelf->__Vcoverage[128]);
        vlSelfRef.tb_natural_inventory__DOT__tail = 0U;
        ++(vlSelf->__Vcoverage[129]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg = 0U;
        ++(vlSelf->__Vcoverage[253]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg = 0U;
        ++(vlSelf->__Vcoverage[294]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg = 0U;
        ++(vlSelf->__Vcoverage[375]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 0U;
        ++(vlSelf->__Vcoverage[408]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg = 0U;
        ++(vlSelf->__Vcoverage[441]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 0U;
        ++(vlSelf->__Vcoverage[474]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg = 0U;
        ++(vlSelf->__Vcoverage[491]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg = 0U;
        ++(vlSelf->__Vcoverage[494]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg = 0U;
        ++(vlSelf->__Vcoverage[511]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg = 0U;
        ++(vlSelf->__Vcoverage[528]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_user_reg = 0U;
        ++(vlSelf->__Vcoverage[531]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg = 0U;
        ++(vlSelf->__Vcoverage[532]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg = 0U;
        ++(vlSelf->__Vcoverage[535]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg = 0U;
        ++(vlSelf->__Vcoverage[538]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg = 0U;
        ++(vlSelf->__Vcoverage[541]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg = 0U;
        ++(vlSelf->__Vcoverage[574]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg = 0U;
        ++(vlSelf->__Vcoverage[629]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg = 0U;
        ++(vlSelf->__Vcoverage[668]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg = 0U;
        ++(vlSelf->__Vcoverage[784]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg = 0U;
        ++(vlSelf->__Vcoverage[787]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg = 0U;
        ++(vlSelf->__Vcoverage[788]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg = 0U;
        ++(vlSelf->__Vcoverage[791]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg = 0U;
        ++(vlSelf->__Vcoverage[808]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg = 0U;
        ++(vlSelf->__Vcoverage[825]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg = 0U;
        ++(vlSelf->__Vcoverage[828]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg = 0U;
        ++(vlSelf->__Vcoverage[845]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg = 0U;
        ++(vlSelf->__Vcoverage[848]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg = 0U;
        ++(vlSelf->__Vcoverage[851]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg = 0U;
        ++(vlSelf->__Vcoverage[856]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg = 0U;
        ++(vlSelf->__Vcoverage[873]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg = 0U;
        ++(vlSelf->__Vcoverage[890]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg = 0U;
        ++(vlSelf->__Vcoverage[893]);
    }
    vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int__0 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int;
    vlSelfRef.__VactTriggered[0U] = (1ULL | vlSelfRef.__VactTriggered[0U]);
    vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk__0 = 0U;
    do {
        vlSelfRef.__VactTriggeredAcc[vlSelfRef.__Vi] 
            = vlSelfRef.__VactTriggered[vlSelfRef.__Vi];
        vlSelfRef.__Vi = ((IData)(1U) + vlSelfRef.__Vi);
    } while ((0U >= vlSelfRef.__Vi));
}

VL_ATTR_COLD void Vtb_natural_inventory___024root___eval_final(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_final\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_natural_inventory___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtb_natural_inventory___024root___eval_phase__stl(Vtb_natural_inventory___024root* vlSelf);

VL_ATTR_COLD void Vtb_natural_inventory___024root___eval_settle(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_settle\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vtb_natural_inventory___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 2, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vtb_natural_inventory___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vtb_natural_inventory___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_natural_inventory___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vtb_natural_inventory___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @([hybrid] tb_natural_inventory.dut.dut.m_axis_tvalid_int)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vtb_natural_inventory___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___trigger_anySet__stl\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((2U > n));
    return (0U);
}

VL_ATTR_COLD void Vtb_natural_inventory___024root___stl_sequent__TOP__0(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___stl_sequent__TOP__0\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__clk) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__clk))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 0, vlSelfRef.tb_natural_inventory__DOT__clk, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__clk);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__clk 
            = vlSelfRef.tb_natural_inventory__DOT__clk;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__rst) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__rst))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 3, vlSelfRef.tb_natural_inventory__DOT__rst, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__rst);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__rst 
            = vlSelfRef.tb_natural_inventory__DOT__rst;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 6, vlSelfRef.tb_natural_inventory__DOT__s_valid, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_valid 
            = vlSelfRef.tb_natural_inventory__DOT__s_valid;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_last) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_last))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 9, vlSelfRef.tb_natural_inventory__DOT__s_last, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_last);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_last 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_ready))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 12, vlSelfRef.tb_natural_inventory__DOT__m_ready, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_ready);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_ready 
            = vlSelfRef.tb_natural_inventory__DOT__m_ready;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_ready))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 15, vlSelfRef.tb_natural_inventory__DOT__h_ready, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_ready);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_ready 
            = vlSelfRef.tb_natural_inventory__DOT__h_ready;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__s_data) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_data)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 18, vlSelfRef.tb_natural_inventory__DOT__s_data, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_data);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_data 
            = vlSelfRef.tb_natural_inventory__DOT__s_data;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 35, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 37, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 39, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 41, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 43, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 45, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 47, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 63, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 95, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 247, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 262, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 343, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 409, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_data_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 475, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_data_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_data_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_keep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 492, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_keep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_keep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_id_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 495, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_id_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_id_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_dest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 512, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_dest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_dest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_user_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_user_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 529, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_user_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_user_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_user_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_user_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 627, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 785, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 792, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 809, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 826, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdata_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 829, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdata_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 846, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 849, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tlast_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 854, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tlast_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 857, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 874, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 891, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg;
    }
}

void Vtb_natural_inventory___024root___act_comb__TOP__0(Vtb_natural_inventory___024root* vlSelf);

VL_ATTR_COLD bool Vtb_natural_inventory___024root___eval_phase__stl(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_phase__stl\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__stl
        vlSelfRef.__VstlTriggered[1U] = ((0xfffffffffffffffeULL 
                                          & vlSelfRef.__VstlTriggered[1U]) 
                                         | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
        vlSelfRef.__VstlTriggered[0U] = (QData)((IData)(
                                                        ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int) 
                                                         != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int__0))));
        vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int__0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int;
        if (VL_UNLIKELY(((1U & (~ (IData)(vlSelfRef.__VstlDidInit)))))) {
            vlSelfRef.__VstlDidInit = 1U;
            vlSelfRef.__VstlTriggered[0U] = (1ULL | vlSelfRef.__VstlTriggered[0U]);
        }
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtb_natural_inventory___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vtb_natural_inventory___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[1U])) {
                Vtb_natural_inventory___024root___stl_sequent__TOP__0(vlSelf);
            }
            if ((1ULL & (vlSelfRef.__VstlTriggered[1U] 
                         | vlSelfRef.__VstlTriggered[0U]))) {
                Vtb_natural_inventory___024root___act_comb__TOP__0(vlSelf);
            }
        }
    }
    return (__VstlExecute);
}

bool Vtb_natural_inventory___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_natural_inventory___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vtb_natural_inventory___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @([hybrid] tb_natural_inventory.dut.dut.m_axis_tvalid_int)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge tb_natural_inventory.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtb_natural_inventory___024root___ctor_var_reset(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___ctor_var_reset\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->tb_natural_inventory__DOT____VExpr_he4c3ed11__1 = 0;
    vlSelf->tb_natural_inventory__DOT____VExpr_he4c3ed11__0 = 0;
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->tb_natural_inventory__DOT__n = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6239908561967623442ull);
    vlSelf->tb_natural_inventory__DOT__take = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1836513443761818133ull);
    vlSelf->tb_natural_inventory__DOT__r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1162128808370494287ull);
    vlSelf->tb_natural_inventory__DOT__o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14973208651180991037ull);
    vlSelf->tb_natural_inventory__DOT__d = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 691100840433690020ull);
    vlSelf->tb_natural_inventory__DOT__l = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3808514921670195160ull);
    vlSelf->tb_natural_inventory__DOT__m = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7175435493516528860ull);
    vlSelf->tb_natural_inventory__DOT__h = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6282745542038860661ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->tb_natural_inventory__DOT__data_q[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1931881318558800884ull);
    }
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->tb_natural_inventory__DOT__last_q[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8584831823877911435ull);
    }
    vlSelf->tb_natural_inventory__DOT____Vtogcov__clk = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__rst = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__s_valid = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__s_last = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__m_ready = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__h_ready = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__s_data = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__s_ready = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__m_valid = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__m_last = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__h_valid = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__h_pad = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__h_truncate = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__m_data = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__h_length = 0;
    vlSelf->tb_natural_inventory__DOT____Vtogcov__h_original_length = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10658861637439180827ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8740715875508745102ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7411207330767686583ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9734314749898864231ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3879370330711124191ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2108279403573324373ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3472452661040329872ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10635804088025030655ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11925926932928715012ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13291392094185448763ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14021323618065247180ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6796952062648852060ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6933138729762168993ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5272308467603521542ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12187518819035474311ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9625175692606686624ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5739934642461040397ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5915586383864275917ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6121118649162743226ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17723931636438848939ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4801557775617257660ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5386424456997801638ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10884187426972771698ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tuser = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_last_word = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tdata_masked = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_data_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_keep_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_id_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_dest_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_user_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdata_int = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_int = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_int = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tlast_int = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_int = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_int = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_int = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_early = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tready_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdata_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tkeep_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_next = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tlast_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tid_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdest_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tuser_reg = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_output = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_temp = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_temp_to_output = 0;
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int__0 = 0;
    vlSelf->__VstlDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggeredAcc[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk__0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
    vlSelf->__Vi = 0;
}

VL_ATTR_COLD void Vtb_natural_inventory___024root___configure_coverage(Vtb_natural_inventory___024root* vlSelf, bool first) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___configure_coverage\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    (void)first;  // Prevent unused variable warning
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 0, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 5, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "clk");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 2, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 9, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 2, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 9, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 3, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 11, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "rst");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 5, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 15, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 5, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 15, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 6, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 17, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "s_valid");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 8, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 25, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 8, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 25, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 9, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 27, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "s_last");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 11, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 34, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 11, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 34, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 12, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 36, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "m_ready");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 14, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 44, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 14, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 44, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 15, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 46, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "h_ready");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 17, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 54, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 17, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 3, 54, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "3", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 18, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 4, 11, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "s_data");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 34, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 4, 18, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "4", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 34, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 4, 18, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "4", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 35, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 5, 6, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "s_ready");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 37, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 5, 14, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "m_valid");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 39, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 5, 22, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "m_last");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 41, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 5, 29, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "h_valid");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 43, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 5, 37, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "h_pad");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 45, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 5, 43, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "h_truncate");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 47, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 6, 12, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "m_data");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 63, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 7, 13, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "h_length");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 95, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 7, 22, ".tb_natural_inventory", "v_toggle/tb_natural_inventory", "h_original_length");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 127, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 9, 20, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 127, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 9, 20, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 128, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 9, 27, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 128, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 9, 27, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 129, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 9, 34, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 129, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 9, 34, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 130, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 13, 3, ".tb_natural_inventory", "v_line/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 130, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 13, 3, ".tb_natural_inventory", "v_line/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 131, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 14, 23, ".tb_natural_inventory", "v_line/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 131, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 14, 23, ".tb_natural_inventory", "v_line/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 132, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 15, 8, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "($feof(fd)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 132, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 15, 8, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "($feof(fd)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 133, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 15, 8, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "($feof(fd)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 133, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 15, 8, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "($feof(fd)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 134, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 18, 5, ".tb_natural_inventory", "v_line/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 134, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 18, 5, ".tb_natural_inventory", "v_line/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 135, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 21, 9, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "if", "21", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 135, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 21, 9, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "if", "21", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 136, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 21, 10, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 136, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 21, 10, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 137, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 20, 4, ".tb_natural_inventory", "v_line/tb_natural_inventory", "elsif", "20", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 137, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 20, 4, ".tb_natural_inventory", "v_line/tb_natural_inventory", "elsif", "20", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 138, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 18, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(rst==0 && (head < tail)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 138, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 18, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(rst==0 && (head < tail)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 139, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 18, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "((head < tail)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 139, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 18, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "((head < tail)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 140, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 18, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 140, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 18, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 141, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 39, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 141, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 39, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 142, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 39, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 142, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 39, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 143, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 53, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "cond_then", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 143, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 53, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "cond_then", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 144, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 54, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "cond_else", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 144, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 54, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "cond_else", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 145, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 69, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 145, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 69, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 146, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 69, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 146, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 69, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 147, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 83, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "cond_then", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 147, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 83, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "cond_then", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 148, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 84, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "cond_else", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 148, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 22, 84, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "cond_else", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 149, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 23, 29, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(rst==0 && s_valid==1 && s_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 149, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 23, 29, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(rst==0 && s_valid==1 && s_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 150, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 23, 29, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 150, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 23, 29, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 151, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 23, 29, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 151, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 23, 29, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(s_valid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 152, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 23, 29, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 152, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 23, 29, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 153, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 27, 13, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "if", "27", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 153, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 27, 13, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "if", "27", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 154, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 27, 14, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 154, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 27, 14, ".tb_natural_inventory", "v_branch/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 155, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 29, 13, ".tb_natural_inventory", "v_line/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 155, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 29, 13, ".tb_natural_inventory", "v_line/tb_natural_inventory", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 156, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 29, 15, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "($feof(fd)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 156, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 29, 15, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "($feof(fd)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 157, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 29, 15, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "($feof(fd)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 157, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 29, 15, ".tb_natural_inventory", "v_expr/tb_natural_inventory", "($feof(fd)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 158, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 17, 3, ".tb_natural_inventory", "v_line/tb_natural_inventory", "elsif", "17,19,22-28", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 158, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 17, 3, ".tb_natural_inventory", "v_line/tb_natural_inventory", "elsif", "17,19,22-28", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 159, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 15, 2, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "15-16", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 159, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 15, 2, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "15-16", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 160, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 12, 1, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "12,14,31", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 160, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 12, 1, ".tb_natural_inventory", "v_line/tb_natural_inventory", "block", "12,14,31", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 0, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 3, 12, ".tb_natural_inventory.dut", "v_toggle/frame_task", "clk");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 3, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 3, 17, ".tb_natural_inventory.dut", "v_toggle/frame_task", "rst");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 18, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 4, 18, ".tb_natural_inventory.dut", "v_toggle/frame_task", "s_data");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 6, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 5, 12, ".tb_natural_inventory.dut", "v_toggle/frame_task", "s_valid");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 9, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 5, 21, ".tb_natural_inventory.dut", "v_toggle/frame_task", "s_last");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 35, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 6, 13, ".tb_natural_inventory.dut", "v_toggle/frame_task", "s_ready");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 47, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 7, 19, ".tb_natural_inventory.dut", "v_toggle/frame_task", "m_data");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 37, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 8, 13, ".tb_natural_inventory.dut", "v_toggle/frame_task", "m_valid");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 39, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 8, 22, ".tb_natural_inventory.dut", "v_toggle/frame_task", "m_last");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 12, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 9, 12, ".tb_natural_inventory.dut", "v_toggle/frame_task", "m_ready");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 41, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 10, 13, ".tb_natural_inventory.dut", "v_toggle/frame_task", "h_valid");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 43, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 10, 22, ".tb_natural_inventory.dut", "v_toggle/frame_task", "h_pad");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 45, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 10, 29, ".tb_natural_inventory.dut", "v_toggle/frame_task", "h_truncate");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 63, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 11, 20, ".tb_natural_inventory.dut", "v_toggle/frame_task", "h_length");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 95, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 11, 30, ".tb_natural_inventory.dut", "v_toggle/frame_task", "h_original_length");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 15, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/task_top_v3.sv", 12, 12, ".tb_natural_inventory.dut", "v_toggle/frame_task", "h_ready");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 0, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 57, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "clk");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 3, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 58, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "rst");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 18, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 63, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tdata");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 161, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 64, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tkeep");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 6, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 65, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tvalid");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 35, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 66, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tready");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 9, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 67, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tlast");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 163, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 68, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tid");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 163, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 69, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tdest");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 179, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 70, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tuser");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 47, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 75, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tdata");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 161, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 76, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tkeep");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 37, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 77, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tvalid");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 12, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 78, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tready");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 39, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 79, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tlast");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 163, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 80, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tid");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 163, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 81, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tdest");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 179, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 82, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tuser");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 41, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 87, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_valid");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 15, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 88, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_ready");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 43, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 89, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_pad");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 45, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 90, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_truncate");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 63, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 91, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_length");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 95, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 92, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_original_length");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 181, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 97, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "length_min");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 213, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 98, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "length_max");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 245, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 106, 6, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 245, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 106, 6, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 246, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 105, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "105", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 246, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 105, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "105", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 2, 1, vlSelf->__Vcoverage + 247, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 119, 11, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "state_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 253, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 119, 23, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "119", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 253, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 119, 23, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "119", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 2, 1, vlSelf->__Vcoverage + 254, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 119, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "state_next");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 260, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 122, 5, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "store_last_word");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 262, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 124, 12, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "frame_ptr_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 294, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 124, 28, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "124", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 294, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 124, 28, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "124", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 295, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 124, 35, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "frame_ptr_next");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 327, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 126, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tdata_masked");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 343, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 129, 12, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "short_counter_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 375, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 129, 32, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "129", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 375, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 129, 32, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "129", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 376, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 129, 39, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "short_counter_next");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 408, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 129, 60, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "129", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 408, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 129, 60, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "129", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 409, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 130, 12, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "long_counter_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 441, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 130, 31, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "130", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 441, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 130, 31, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "130", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 442, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 130, 38, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "long_counter_next");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 474, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 130, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "130", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 474, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 130, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "130", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 475, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 132, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "last_word_data_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 491, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 132, 54, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "132", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 491, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 132, 54, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "132", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 492, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 133, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "last_word_keep_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 494, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 133, 54, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "133", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 494, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 133, 54, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "133", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 495, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 134, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "last_word_id_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 511, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 134, 52, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "134", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 511, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 134, 52, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "134", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 512, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 135, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "last_word_dest_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 528, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 135, 54, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "135", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 528, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 135, 54, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "135", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 529, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 136, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "last_word_user_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 531, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 136, 54, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "136", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 531, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 136, 54, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "136", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 41, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 138, 5, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_valid_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 532, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 138, 24, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "138", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 532, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 138, 24, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "138", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 533, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 138, 30, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_valid_next");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 43, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 139, 5, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_pad_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 535, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 139, 28, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "139", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 535, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 139, 28, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "139", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 536, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 139, 34, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_pad_next");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 45, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 140, 5, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_truncate_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 538, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 140, 33, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "140", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 538, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 140, 33, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "140", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 539, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 140, 39, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_truncate_next");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 63, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 141, 12, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_length_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 541, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 141, 38, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "141", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 541, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 141, 38, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "141", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 542, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 141, 45, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_length_next");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 95, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 142, 12, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_original_length_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 574, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 142, 47, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "142", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 574, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 142, 47, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "142", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 15, 1, vlSelf->__Vcoverage + 575, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 142, 54, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "status_frame_original_length_next");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 607, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 145, 23, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tdata_int");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 623, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 146, 23, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tkeep_int");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 625, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 147, 23, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tvalid_int");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 627, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 148, 23, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tready_int_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 629, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 148, 47, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "148", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 629, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 148, 47, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "148", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 630, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 149, 23, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tlast_int");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 632, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 150, 23, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tid_int");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 648, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 151, 23, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tdest_int");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 664, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 152, 23, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tuser_int");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 666, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 153, 23, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tready_int_early");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 35, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 155, 5, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tready_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 668, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 155, 25, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "155", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 668, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 155, 25, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "155", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 669, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 155, 31, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "s_axis_tready_next");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 671, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 186, 42, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_valid_reg==1 && status_ready==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 671, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 186, 42, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_valid_reg==1 && status_ready==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 672, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 186, 42, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 672, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 186, 42, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 673, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 186, 42, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_valid_reg==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 673, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 186, 42, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_valid_reg==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 674, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 194, 85, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tkeep[i[0]+:1]==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 674, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 194, 85, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tkeep[i[0]+:1]==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 675, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 194, 85, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tkeep[i[0]+:1]==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 675, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 194, 85, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tkeep[i[0]+:1]==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 676, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 194, 103, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "194", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 676, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 194, 103, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "194", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 677, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 194, 104, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "194", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 677, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 194, 104, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "194", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 678, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 193, 9, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "193-194", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 678, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 193, 9, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "193-194", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 679, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 192, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "192-193", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 679, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 192, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "192-193", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 680, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 192, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "196-197", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 680, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 192, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "196-197", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 681, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 204, 58, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 681, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 204, 58, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 682, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 204, 58, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_valid_reg==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 682, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 204, 58, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_valid_reg==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 683, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 204, 58, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_valid_reg==1 && status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 683, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 204, 58, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_valid_reg==1 && status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 684, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 204, 58, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 684, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 204, 58, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 685, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 222, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "222", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 685, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 222, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "222", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 686, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 222, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 686, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 222, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 687, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 220, 17, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "220", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 687, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 220, 17, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "220", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 688, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 226, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "226-227", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 688, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 226, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "226-227", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 689, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 226, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "228-229", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 689, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 226, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "228-229", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 690, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 232, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "232-233", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 690, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 232, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "232-233", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 691, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 232, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "234-235", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 691, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 232, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "234-235", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 692, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 246, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 692, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 246, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 693, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 246, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 693, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 246, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 694, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 246, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 694, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 246, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 695, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 240, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "240-250", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 695, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 240, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "240-250", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 696, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 240, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "251-254", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 696, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 240, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "251-254", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 697, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 272, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 697, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 272, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 698, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 272, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 698, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 272, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 699, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 272, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 699, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 272, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 700, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 260, 29, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "260-266", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 700, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 260, 29, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "260-266", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 701, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 260, 30, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "267-277", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 701, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 260, 30, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "267-277", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 702, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 285, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 702, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 285, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 703, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 285, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 703, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 285, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 704, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 285, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 704, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 285, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 705, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 259, 25, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "259", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 705, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 259, 25, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "259", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 706, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 259, 26, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "279-289", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 706, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 259, 26, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "279-289", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 707, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 257, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "257-258", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 707, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 257, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "257-258", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 708, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 257, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "291-292", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 708, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 257, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "291-292", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 709, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 238, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "238-239", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 709, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 238, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "238-239", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 710, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 238, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "256", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 710, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 238, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "256", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 711, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 13, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "217,219-220,224", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 711, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 13, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "217,219-220,224", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 712, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "295-296", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 712, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "295-296", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 713, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==1 && s_axis_tvalid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 713, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==1 && s_axis_tvalid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 714, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 714, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 715, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 715, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 217, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 716, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 201, 19, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "case", "201,204,206-212,214-215", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 716, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 201, 19, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "case", "201,204,206-212,214-215", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 717, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 317, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "317", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 717, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 317, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "317", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 718, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 317, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 718, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 317, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 719, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 315, 17, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "315", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 719, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 315, 17, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "315", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 720, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 321, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "321-322", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 720, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 321, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "321-322", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 721, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 321, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "323-324", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 721, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 321, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "323-324", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 722, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 327, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "327-328", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 722, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 327, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "327-328", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 723, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 327, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "329-330", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 723, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 327, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "329-330", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 724, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 341, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 724, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 341, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 725, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 341, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 725, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 341, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 726, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 341, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 726, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 341, 70, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 727, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 335, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "335-345", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 727, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 335, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "335-345", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 728, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 335, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "346-349", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 728, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 335, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "346-349", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 729, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 367, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 729, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 367, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 730, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 367, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 730, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 367, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 731, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 367, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 731, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 367, 78, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 732, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 355, 29, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "355-361", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 732, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 355, 29, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "355-361", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 733, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 355, 30, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "362-372", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 733, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 355, 30, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "362-372", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 734, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 380, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 734, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 380, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 735, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 380, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 735, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 380, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 736, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 380, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 736, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 380, 74, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 737, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 354, 25, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "354", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 737, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 354, 25, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "354", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 738, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 354, 26, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "374-384", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 738, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 354, 26, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "374-384", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 739, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 352, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "352-353", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 739, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 352, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "352-353", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 740, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 352, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "386-387", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 740, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 352, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "386-387", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 741, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 333, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "333-334", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 741, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 333, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "333-334", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 742, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 333, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "351", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 742, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 333, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "351", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 743, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 13, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "312,314-315,319", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 743, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 13, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "312,314-315,319", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 744, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "390-391", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 744, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "390-391", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 745, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==1 && s_axis_tvalid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 745, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==1 && s_axis_tvalid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 746, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 746, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 747, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 747, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 312, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 748, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 299, 23, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "case", "299,302,304-310", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 748, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 299, 23, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "case", "299,302,304-310", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 749, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 409, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "409-410", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 749, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 409, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "409-410", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 750, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 409, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "411-412", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 750, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 409, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "411-412", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 751, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 415, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "415-416", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 751, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 415, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "415-416", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 752, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 415, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "417-418", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 752, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 415, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "417-418", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 753, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 426, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 753, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 426, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 754, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 426, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 754, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 426, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 755, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 426, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 755, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 426, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 756, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 421, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "421-432", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 756, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 421, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "421-432", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 757, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 421, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "433-434", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 757, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 421, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "433-434", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 758, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 406, 13, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "406-407", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 758, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 406, 13, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "406-407", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 759, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 406, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "436-437", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 759, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 406, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "436-437", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 760, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 394, 18, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "case", "394,396,398-404", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 760, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 394, 18, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "case", "394,396,398-404", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 761, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 446, 47, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==1 && s_axis_tlast==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 761, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 446, 47, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==1 && s_axis_tlast==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 762, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 446, 47, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tlast==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 762, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 446, 47, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tlast==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 763, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 446, 47, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 763, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 446, 47, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 764, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 456, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "456", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 764, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 456, 21, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "456", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 765, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 456, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 765, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 456, 22, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 766, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 454, 17, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "454", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 766, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 454, 17, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "454", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 767, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 466, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 767, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 466, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==1 && status_ready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 768, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 466, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 768, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 466, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(status_ready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 769, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 466, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 769, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 466, 66, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready_int_early==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 770, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 460, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "460-470", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 770, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 460, 17, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "460-470", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 771, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 460, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "471-472", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 771, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 460, 18, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "471-472", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 772, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 13, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "452-454,458", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 772, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 13, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "452-454,458", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 773, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "474-475", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 773, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "474-475", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 774, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==1 && s_axis_tvalid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 774, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==1 && s_axis_tvalid==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 775, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 775, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tvalid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 776, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 776, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 452, 31, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(s_axis_tready==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 777, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 440, 23, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "case", "440,442,444-450", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 777, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 440, 23, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "case", "440,442,444-450", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 778, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 166, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "166-167,169,171,173-174,176-182,184,186-190,200", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 778, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 166, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "166-167,169,171,173-174,176-182,184,186-190,200", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 779, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 482, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "482-488", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 779, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 482, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "482-488", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 780, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 482, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "489-490,492,494-495,497,499", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 780, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 482, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "489-490,492,494-495,497,499", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 781, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 507, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "507-512", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 781, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 507, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "507-512", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 782, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 507, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 782, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 507, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 783, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 481, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "481,502-505", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 783, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 481, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "481,502-505", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 47, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 517, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tdata_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 784, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 517, 53, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "517", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 784, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 517, 53, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "517", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 785, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 518, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tkeep_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 787, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 518, 53, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "518", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 787, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 518, 53, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "518", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 37, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 519, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tvalid_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 788, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 519, 42, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "519", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 788, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 519, 42, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "519", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 789, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 519, 48, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tvalid_next");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 39, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 520, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tlast_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 791, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 520, 42, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "520", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 791, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 520, 42, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "520", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 792, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 521, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tid_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 808, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 521, 51, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "521", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 808, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 521, 51, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "521", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 809, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 522, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tdest_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 825, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 522, 53, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "522", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 825, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 522, 53, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "522", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 826, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 523, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "m_axis_tuser_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 828, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 523, 53, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "523", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 828, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 523, 53, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "523", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 829, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 525, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "temp_m_axis_tdata_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 845, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 525, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "525", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 845, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 525, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "525", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 846, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 526, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "temp_m_axis_tkeep_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 848, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 526, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "526", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 848, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 526, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "526", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 849, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 527, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "temp_m_axis_tvalid_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 851, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 527, 47, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "527", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 851, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 527, 47, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "527", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 852, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 527, 53, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "temp_m_axis_tvalid_next");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 854, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 528, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "temp_m_axis_tlast_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 856, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 528, 47, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "528", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 856, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 528, 47, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "528", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 857, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 529, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "temp_m_axis_tid_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 873, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 529, 56, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "529", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 873, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 529, 56, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "529", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 874, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 530, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "temp_m_axis_tdest_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 890, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 530, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "530", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 890, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 530, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "530", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 1, vlSelf->__Vcoverage + 891, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 531, 22, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "temp_m_axis_tuser_reg");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 893, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 531, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "531", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 893, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 531, 58, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "531", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 894, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 534, 5, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "store_axis_int_to_output");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 896, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 535, 5, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "store_axis_int_to_temp");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 898, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 536, 5, ".tb_natural_inventory.dut.dut", "v_toggle/axis_frame_length_adjust__pi1", "store_axis_temp_to_output");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 900, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 539, 38, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "539", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 900, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 539, 38, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "539", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 901, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 539, 39, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "539", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 901, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 539, 39, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "539", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 902, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 542, 38, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "542", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 902, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 542, 38, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "542", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 903, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 542, 39, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "542", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 903, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 542, 39, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "542", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 904, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 543, 38, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "543", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 904, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 543, 38, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "543", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 905, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 543, 39, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "543", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 905, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 543, 39, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "543", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 906, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 544, 38, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "544", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 906, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 544, 38, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_then", "544", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 907, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 544, 39, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "544", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 907, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 544, 39, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "cond_else", "544", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 908, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(temp_m_axis_tvalid_reg==0 && m_axis_tvalid_int==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 908, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(temp_m_axis_tvalid_reg==0 && m_axis_tvalid_int==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 909, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(temp_m_axis_tvalid_reg==0 && m_axis_tvalid_reg==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 909, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(temp_m_axis_tvalid_reg==0 && m_axis_tvalid_reg==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 910, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 910, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 911, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==0 && m_axis_tvalid_reg==1 && m_axis_tvalid_int==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 911, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==0 && m_axis_tvalid_reg==1 && m_axis_tvalid_int==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 912, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==0 && temp_m_axis_tvalid_reg==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 912, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 547, 48, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==0 && temp_m_axis_tvalid_reg==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 913, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 9, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "560,562-563", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 913, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 9, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "560,562-563", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 914, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 10, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "564,566-567", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 914, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 10, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "564,566-567", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 915, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 27, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tvalid_reg==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 915, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 27, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tvalid_reg==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 916, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 27, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 916, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 27, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 917, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 27, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==0 && m_axis_tvalid_reg==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 917, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 560, 27, ".tb_natural_inventory.dut.dut", "v_expr/axis_frame_length_adjust__pi1", "(m_axis_tready==0 && m_axis_tvalid_reg==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 918, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 569, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "569,571-573", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 918, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 569, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "569,571-573", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 919, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 569, 15, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 919, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 569, 15, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 920, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 558, 5, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "elsif", "558", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 920, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 558, 5, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "elsif", "558", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 921, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 549, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "549,551-552,554-556", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 921, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 549, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "549,551-552,554-556", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 922, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 590, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "590-596", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 922, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 590, 14, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "590-596", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 923, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 590, 15, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 923, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 590, 15, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 924, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 583, 5, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "elsif", "583-589", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 924, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 583, 5, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "elsif", "583-589", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 925, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 599, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "599-605", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 925, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 599, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "599-605", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 926, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 599, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 926, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 599, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 927, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 608, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "608-611", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 927, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 608, 5, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "if", "608-611", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 928, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 608, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 928, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 608, 6, ".tb_natural_inventory.dut.dut", "v_branch/axis_frame_length_adjust__pi1", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 929, first, true, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 577, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "577-580", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 929, first, false, "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/rtl/axis_frame_length_adjust.v", 577, 1, ".tb_natural_inventory.dut.dut", "v_line/axis_frame_length_adjust__pi1", "block", "577-580", "", "", "", "");
}
