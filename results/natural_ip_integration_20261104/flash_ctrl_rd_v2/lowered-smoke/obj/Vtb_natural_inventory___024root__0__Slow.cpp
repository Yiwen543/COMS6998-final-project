// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_natural_inventory.h for the primary calling header

#include "Vtb_natural_inventory__pch.h"

VL_ATTR_COLD void Vtb_natural_inventory___024root___eval_static(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_static\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk_i__0 
        = vlSelfRef.tb_natural_inventory__DOT__clk_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__rst_ni__0 
        = vlSelfRef.tb_natural_inventory__DOT__rst_ni;
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
VL_ATTR_COLD void Vtb_natural_inventory___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
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
            VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/results/natural_ip_integration_20261104/flash_ctrl_rd_v2/lowered-smoke/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vtb_natural_inventory___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vtb_natural_inventory___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_natural_inventory___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vtb_natural_inventory___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vtb_natural_inventory___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
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
    } while ((1U > n));
    return (0U);
}

void Vtb_natural_inventory___024root___act_sequent__TOP__0(Vtb_natural_inventory___024root* vlSelf);

VL_ATTR_COLD bool Vtb_natural_inventory___024root___eval_phase__stl(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_phase__stl\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        Vtb_natural_inventory___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vtb_natural_inventory___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                Vtb_natural_inventory___024root___act_sequent__TOP__0(vlSelf);
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
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge tb_natural_inventory.clk_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(negedge tb_natural_inventory.rst_ni)\n");
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
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->tb_natural_inventory__DOT__clk_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1801604704134556980ull);
    vlSelf->tb_natural_inventory__DOT__rst_ni = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9811793661626798439ull);
    vlSelf->tb_natural_inventory__DOT__op_start_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16177336379631696024ull);
    vlSelf->tb_natural_inventory__DOT__op_num_words_i = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 4550177683754376002ull);
    vlSelf->tb_natural_inventory__DOT__op_done_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4442613554537577577ull);
    vlSelf->tb_natural_inventory__DOT__op_err_o = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 9754072040276913349ull);
    vlSelf->tb_natural_inventory__DOT__op_addr_i = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 11316392135784855283ull);
    vlSelf->tb_natural_inventory__DOT__op_addr_oob_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2459938913998569379ull);
    vlSelf->tb_natural_inventory__DOT__op_err_addr_o = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 8803754801705502913ull);
    vlSelf->tb_natural_inventory__DOT__data_rdy_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13252862839293026406ull);
    vlSelf->tb_natural_inventory__DOT__data_wr_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4223094267737956707ull);
    vlSelf->tb_natural_inventory__DOT__flash_req_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4077643629101086107ull);
    vlSelf->tb_natural_inventory__DOT__flash_data_i = VL_SCOPED_RAND_RESET_Q(39, __VscopeHash, 4233432257215957045ull);
    vlSelf->tb_natural_inventory__DOT__flash_done_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7409855323857853059ull);
    vlSelf->tb_natural_inventory__DOT__flash_rd_err_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3742668964366915640ull);
    vlSelf->tb_natural_inventory__DOT__flash_mp_err_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17471029619114434626ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__st_q = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14672114143309565686ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__st_d = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3588151127721687000ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__int_addr = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 15431372099991418182ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__op_err_q = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 15078420027960177462ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__op_err_d = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 11876716719210920127ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT____Vcellinp__u_cnt__clr_i = 0;
    vlSelf->tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__err_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11621326965702005121ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__ext_cnt = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 10064337935426159853ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 6582571439539882199ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__ext_cnt = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 8806967186335702579ull);
    vlSelf->tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 3203648406303292349ull);
    vlSelf->__VdfgRegularize_hebeb780c_0_1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggeredAcc[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__rst_ni__0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
    vlSelf->__Vi = 0;
}
