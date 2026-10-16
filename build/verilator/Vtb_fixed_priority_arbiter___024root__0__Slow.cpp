// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_fixed_priority_arbiter.h for the primary calling header

#include "Vtb_fixed_priority_arbiter__pch.h"

void Vtb_fixed_priority_arbiter___024root___timing_ready(Vtb_fixed_priority_arbiter___024root* vlSelf);

VL_ATTR_COLD void Vtb_fixed_priority_arbiter___024root___eval_static(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_static\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_static__TOP
        vlSelfRef.tb_fixed_priority_arbiter__DOT__clk = 0U;
        ++(vlSelf->__Vcoverage[2]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__reset = 0U;
        ++(vlSelf->__Vcoverage[5]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__req = 0U;
        ++(vlSelf->__Vcoverage[22]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override = 0U;
        ++(vlSelf->__Vcoverage[39]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__checks = 0U;
        ++(vlSelf->__Vcoverage[64]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors = 0U;
        ++(vlSelf->__Vcoverage[65]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors = 0U;
        ++(vlSelf->__Vcoverage[66]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__mode = 2U;
        ++(vlSelf->__Vcoverage[67]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 0U;
        ++(vlSelf->__Vcoverage[70]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req = 0U;
        ++(vlSelf->__Vcoverage[89]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override = 0U;
        ++(vlSelf->__Vcoverage[108]);
    }
    vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0 = 0U;
    vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__reset__0 = 0U;
    Vtb_fixed_priority_arbiter___024root___timing_ready(vlSelf);
    do {
        vlSelfRef.__VactTriggeredAcc[vlSelfRef.__Vi] 
            = vlSelfRef.__VactTriggered[vlSelfRef.__Vi];
        vlSelfRef.__Vi = ((IData)(1U) + vlSelfRef.__Vi);
    } while ((0U >= vlSelfRef.__Vi));
}

VL_ATTR_COLD void Vtb_fixed_priority_arbiter___024root___eval_final(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_final\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_fixed_priority_arbiter___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtb_fixed_priority_arbiter___024root___eval_phase__stl(Vtb_fixed_priority_arbiter___024root* vlSelf);

VL_ATTR_COLD void Vtb_fixed_priority_arbiter___024root___eval_settle(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_settle\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vtb_fixed_priority_arbiter___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 2, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vtb_fixed_priority_arbiter___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vtb_fixed_priority_arbiter___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_fixed_priority_arbiter___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vtb_fixed_priority_arbiter___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vtb_fixed_priority_arbiter___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD bool Vtb_fixed_priority_arbiter___024root___eval_phase__stl(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_phase__stl\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        Vtb_fixed_priority_arbiter___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vtb_fixed_priority_arbiter___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                {
                    // Inlined CFunc: _stl_sequent__TOP__0
                    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk) 
                         ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__clk))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 0, vlSelfRef.tb_fixed_priority_arbiter__DOT__clk, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__clk);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__clk 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__clk;
                    }
                    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset) 
                         ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__reset))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 3, vlSelfRef.tb_fixed_priority_arbiter__DOT__reset, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__reset);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__reset 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__reset;
                    }
                    if ((0U != ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__req) 
                                ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__req)))) {
                        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 6, vlSelfRef.tb_fixed_priority_arbiter__DOT__req, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__req);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__req 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__req;
                    }
                    if ((0U != ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override) 
                                ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__priority_override)))) {
                        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 23, vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__priority_override);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__priority_override 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override;
                    }
                    if ((0U != ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                                ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__grant)))) {
                        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 40, vlSelfRef.tb_fixed_priority_arbiter__DOT__grant, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__grant);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__grant 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__grant;
                    }
                    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__valid))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 56, vlSelfRef.tb_fixed_priority_arbiter__DOT__valid, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__valid);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__valid 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__valid;
                    }
                    if ((0U != ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                                ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__grant_index)))) {
                        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 58, vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__grant_index);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__grant_index 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index;
                    }
                    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
                         ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__initialized))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 68, vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__initialized);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__initialized 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized;
                    }
                    if ((0U != ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                                ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__seen_req)))) {
                        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 71, vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__seen_req);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__seen_req 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req;
                    }
                    if ((0U != ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                                ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__seen_override)))) {
                        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 90, vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__seen_override);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__seen_override 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override;
                    }
                }
            }
        }
    }
    return (__VstlExecute);
}

bool Vtb_fixed_priority_arbiter___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_fixed_priority_arbiter___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vtb_fixed_priority_arbiter___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge tb_fixed_priority_arbiter.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge tb_fixed_priority_arbiter.reset)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @(negedge tb_fixed_priority_arbiter.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtb_fixed_priority_arbiter___024root___ctor_var_reset(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___ctor_var_reset\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__1 = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__0 = 0;
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->tb_fixed_priority_arbiter__DOT__grant = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10542396083454964391ull);
    vlSelf->tb_fixed_priority_arbiter__DOT__valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16480540667458671505ull);
    vlSelf->tb_fixed_priority_arbiter__DOT__grant_index = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15114847631184292828ull);
    vlSelf->tb_fixed_priority_arbiter__DOT__r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17603156615100580675ull);
    vlSelf->tb_fixed_priority_arbiter__DOT__o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12437207783235608658ull);
    vlSelf->tb_fixed_priority_arbiter__DOT__vector_file = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT__scan_status = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9257211259111492858ull);
    vlSelf->tb_fixed_priority_arbiter__DOT__vector_reset = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13260438960592498359ull);
    vlSelf->tb_fixed_priority_arbiter__DOT__vector_req = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11922844821689387497ull);
    vlSelf->tb_fixed_priority_arbiter__DOT__vector_override = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1522194534986856317ull);
    VL_SCOPED_RAND_RESET_W(1024, vlSelf->tb_fixed_priority_arbiter__DOT__vector_path, __VscopeHash, 5305331582036470941ull);
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__clk = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__reset = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__req = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__priority_override = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__grant = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__valid = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__grant_index = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__initialized = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__seen_req = 0;
    vlSelf->tb_fixed_priority_arbiter__DOT____Vtogcov__seen_override = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggeredAcc[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__reset__0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
    vlSelf->__Vi = 0;
}

VL_ATTR_COLD void Vtb_fixed_priority_arbiter___024root___configure_coverage(Vtb_fixed_priority_arbiter___024root* vlSelf, bool first) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___configure_coverage\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    (void)first;  // Prevent unused variable warning
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 0, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 3, 9, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "clk");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 2, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 3, 15, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "3", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 2, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 3, 15, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "3", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 3, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 3, 18, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "reset");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 5, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 3, 26, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "3", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 5, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 3, 26, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "3", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 6, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 4, 15, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "req");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 22, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 4, 21, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "4", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 22, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 4, 21, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "4", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 23, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 4, 24, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "priority_override");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 39, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 4, 44, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "4", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 39, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 4, 44, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "4", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 40, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 5, 16, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "grant");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 56, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 6, 10, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "valid");
    vlSelf->__vlCoverToggleInsert(0, 2, 1, vlSelf->__Vcoverage + 58, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 7, 16, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "grant_index");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 64, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 8, 22, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "8", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 64, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 8, 22, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "8", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 65, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 8, 45, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "8", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 65, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 8, 45, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "8", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 66, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 8, 64, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "8", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 66, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 8, 64, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "8", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 67, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 9, 26, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 67, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 9, 26, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "9", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 68, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 11, 9, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "initialized");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 70, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 11, 23, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "11", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 70, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 11, 23, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "11", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 8, 1, vlSelf->__Vcoverage + 71, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 12, 15, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "seen_req");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 89, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 12, 26, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "12", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 89, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 12, 26, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "12", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 8, 1, vlSelf->__Vcoverage + 90, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 12, 29, ".tb_fixed_priority_arbiter", "v_toggle/tb_fixed_priority_arbiter", "seen_override");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 108, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 12, 45, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "12", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 108, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 12, 45, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "12", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 109, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 20, 21, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(clk==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 109, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 20, 21, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(clk==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 110, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 20, 21, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(clk==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 110, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 20, 21, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(clk==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 111, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 20, 5, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "20", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 111, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 20, 5, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "20", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 112, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 38, 17, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "38-40", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 112, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 38, 17, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "38-40", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 113, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 38, 18, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 113, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 38, 18, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 114, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 13, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "36-37", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 114, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 13, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "36-37", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 115, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 14, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 115, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 14, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 116, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 29, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(initialized==1 && ({32'h1{{{grant, valid}, grant_index}}} !== held)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 116, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 29, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(initialized==1 && ({32'h1{{{grant, valid}, grant_index}}} !== held)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 117, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 29, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(({32'h1{{{grant, valid}, grant_index}}} !== held)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 117, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 29, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(({32'h1{{{grant, valid}, grant_index}}} !== held)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 118, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 29, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(initialized==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 118, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 36, 29, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(initialized==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 119, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 24, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 119, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 24, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 120, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 24, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 120, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 24, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 121, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 30, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "cond_then", "42", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 121, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 30, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "cond_then", "42", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 122, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 58, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "cond_then", "42", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 122, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 58, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "cond_then", "42", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 123, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 59, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "cond_else", "42", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 123, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 59, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "cond_else", "42", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 124, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 31, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 124, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 42, 31, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 125, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 47, 17, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "47", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 125, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 47, 17, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "47", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 126, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 47, 18, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 126, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 47, 18, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 127, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 46, 13, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "46", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 127, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 46, 13, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "46", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 128, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 54, 17, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "54-57", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 128, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 54, 17, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "54-57", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 129, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 54, 18, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 129, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 54, 18, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 130, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 13, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "51-53", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 130, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 13, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "51-53", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 131, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 14, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 131, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 14, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 132, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(expected_valid==1 && (grant_index !== expected_index)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 132, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(expected_valid==1 && (grant_index !== expected_index)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 133, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==1 && (grant_index !== expected_index)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 133, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==1 && (grant_index !== expected_index)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 134, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((valid !== expected_valid)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 134, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((valid !== expected_valid)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 135, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((grant !== expected_grant)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 135, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((grant !== expected_grant)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 136, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((grant !== expected_grant)==0 && (valid !== expected_valid)==0 && (grant_index !== expected_index)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 136, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((grant !== expected_grant)==0 && (valid !== expected_valid)==0 && (grant_index !== expected_index)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 137, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((grant !== expected_grant)==0 && (valid !== expected_valid)==0 && rst==0 && expected_valid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 137, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 51, 70, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((grant !== expected_grant)==0 && (valid !== expected_valid)==0 && rst==0 && expected_valid==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 138, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 61, 21, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "61", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 138, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 61, 21, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "61", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 139, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 61, 22, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "62", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 139, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 61, 22, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "62", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 140, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 60, 17, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "60,63", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 140, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 60, 17, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "60,63", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 141, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 60, 18, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "64", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 141, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 60, 18, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "64", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 142, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 59, 13, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "59", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 142, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 59, 13, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "59", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 143, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 59, 14, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 143, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 59, 14, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 144, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 59, 17, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 144, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 59, 17, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 145, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 59, 17, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 145, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 59, 17, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 146, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 22, 20, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "22,24-35,42-46,48-50,66", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 146, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 22, 20, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "22,24-35,42-46,48-50,66", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 147, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 71, 9, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "71", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 147, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 71, 9, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "if", "71", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 148, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 71, 10, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 148, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 71, 10, ".tb_fixed_priority_arbiter", "v_branch/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 149, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 78, 14, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 149, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 78, 14, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 150, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 81, 14, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 150, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 81, 14, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 151, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 82, 20, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "($feof(vector_file)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 151, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 82, 20, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "($feof(vector_file)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 152, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 82, 20, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "($feof(vector_file)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 152, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 82, 20, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "($feof(vector_file)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 153, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 87, 23, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 153, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 87, 23, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 154, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 87, 26, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "($feof(vector_file)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 154, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 87, 26, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "($feof(vector_file)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 155, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 87, 26, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "($feof(vector_file)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 155, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 87, 26, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "($feof(vector_file)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 156, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 85, 17, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "elsif", "85-86", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 156, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 85, 17, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "elsif", "85-86", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 157, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 82, 13, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "82-84", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 157, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 82, 13, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "82-84", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 158, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 93, 17, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "93-94", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 158, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 93, 17, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "93-94", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 159, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 92, 13, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "92-93", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 159, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 92, 13, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "92-93", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 160, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 98, 14, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 160, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 98, 14, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 161, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 98, 37, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((seen_override !== 9'h1ff)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 161, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 98, 37, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((seen_override !== 9'h1ff)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 162, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 98, 37, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((seen_req !== 9'h1ff)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 162, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 98, 37, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((seen_req !== 9'h1ff)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 163, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 98, 37, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((seen_req !== 9'h1ff)==0 && (seen_override !== 9'h1ff)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 163, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 98, 37, ".tb_fixed_priority_arbiter", "v_expr/tb_fixed_priority_arbiter", "((seen_req !== 9'h1ff)==0 && (seen_override !== 9'h1ff)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 164, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 100, 19, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 164, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 100, 19, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 165, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 90, 18, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "elsif", "90,92,95-97", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 165, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 90, 18, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "elsif", "90,92,95-97", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 166, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 77, 9, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "elsif", "77,80,89", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 166, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 77, 9, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "elsif", "77,80,89", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 167, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 105, 10, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 167, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 105, 10, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 168, first, true, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 70, 5, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "70,73-76,101-102,107", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 168, first, false, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 70, 5, ".tb_fixed_priority_arbiter", "v_line/tb_fixed_priority_arbiter", "block", "70,73-76,101-102,107", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 0, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 3, 11, ".tb_fixed_priority_arbiter.dut", "v_toggle/fixed_priority_arbiter", "clk");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 3, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 4, 11, ".tb_fixed_priority_arbiter.dut", "v_toggle/fixed_priority_arbiter", "reset");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 6, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 5, 17, ".tb_fixed_priority_arbiter.dut", "v_toggle/fixed_priority_arbiter", "req");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 23, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 6, 17, ".tb_fixed_priority_arbiter.dut", "v_toggle/fixed_priority_arbiter", "priority_override");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 40, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 8, 22, ".tb_fixed_priority_arbiter.dut", "v_toggle/fixed_priority_arbiter", "grant");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 56, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 9, 16, ".tb_fixed_priority_arbiter.dut", "v_toggle/fixed_priority_arbiter", "valid");
    vlSelf->__vlCoverToggleInsert(0, 2, 1, vlSelf->__Vcoverage + 58, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 10, 22, ".tb_fixed_priority_arbiter.dut", "v_toggle/fixed_priority_arbiter", "grant_index");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 169, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 23, 50, ".tb_fixed_priority_arbiter.dut", "v_expr/fixed_priority_arbiter", "(priority_override[0]==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 169, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 23, 50, ".tb_fixed_priority_arbiter.dut", "v_expr/fixed_priority_arbiter", "(priority_override[0]==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 170, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 23, 50, ".tb_fixed_priority_arbiter.dut", "v_expr/fixed_priority_arbiter", "(priority_override[0]==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 170, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 23, 50, ".tb_fixed_priority_arbiter.dut", "v_expr/fixed_priority_arbiter", "(priority_override[0]==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 171, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 23, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "23", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 171, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 23, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "23", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 172, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 24, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "24", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 172, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 24, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "24", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 173, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 25, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "25", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 173, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 25, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "25", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 174, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 26, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "26", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 174, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 26, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "26", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 175, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 27, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "27", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 175, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 27, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "27", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 176, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 28, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "28", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 176, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 28, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "28", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 177, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 29, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "29", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 177, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 29, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "29", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 178, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 30, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "30", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 178, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 30, 56, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_then", "30", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 179, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 30, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "30", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 179, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 30, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "30", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 180, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 29, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 180, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 29, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 181, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 28, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 181, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 28, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 182, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 27, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 182, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 27, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 183, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 26, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 183, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 26, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 184, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 25, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 184, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 25, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 185, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 24, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 185, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 24, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 186, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 23, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 186, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 23, 57, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 187, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 67, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "if", "67-70", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 187, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 67, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "if", "67-70", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 188, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 67, 19, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "else", "72-75", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 188, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 67, 19, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "else", "72-75", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 189, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 62, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "62-65", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 189, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 62, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "62-65", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 190, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 57, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "57-60", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 190, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 57, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "57-60", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 191, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 52, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "52-55", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 191, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 52, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "52-55", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 192, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 47, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "47-50", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 192, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 47, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "47-50", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 193, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 42, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "42-45", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 193, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 42, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "42-45", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 194, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 37, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "37-40", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 194, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 37, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "37-40", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 195, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 32, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "32-35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 195, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 32, 18, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "32-35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 196, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 20, 13, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "20-23", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 196, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 20, 13, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "elsif", "20-23", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 197, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 14, 9, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "if", "14-17", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 197, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 14, 9, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "if", "14-17", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 198, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 14, 10, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "else", "19", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 198, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 14, 10, ".tb_fixed_priority_arbiter.dut", "v_branch/fixed_priority_arbiter", "else", "19", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 199, first, true, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 13, 5, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "block", "13", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 199, first, false, "examples/arbiter/rtl/fixed_priority_arbiter.sv", 13, 5, ".tb_fixed_priority_arbiter.dut", "v_line/fixed_priority_arbiter", "block", "13", "", "", "", "");
}
