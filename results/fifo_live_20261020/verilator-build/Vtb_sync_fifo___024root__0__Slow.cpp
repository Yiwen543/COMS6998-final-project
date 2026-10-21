// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_sync_fifo.h for the primary calling header

#include "Vtb_sync_fifo__pch.h"

void Vtb_sync_fifo___024root___timing_ready(Vtb_sync_fifo___024root* vlSelf);

VL_ATTR_COLD void Vtb_sync_fifo___024root___eval_static(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_static\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_static__TOP
        vlSelfRef.tb_sync_fifo__DOT__clk = 0U;
        ++(vlSelf->__Vcoverage[2]);
        vlSelfRef.tb_sync_fifo__DOT__reset = 0U;
        ++(vlSelf->__Vcoverage[5]);
        vlSelfRef.tb_sync_fifo__DOT__push_i = 0U;
        ++(vlSelf->__Vcoverage[8]);
        vlSelfRef.tb_sync_fifo__DOT__pop_i = 0U;
        ++(vlSelf->__Vcoverage[11]);
        vlSelfRef.tb_sync_fifo__DOT__push_data_i = 0U;
        ++(vlSelf->__Vcoverage[28]);
        vlSelfRef.tb_sync_fifo__DOT__checks = 0U;
        ++(vlSelf->__Vcoverage[49]);
        vlSelfRef.tb_sync_fifo__DOT__functional_errors = 0U;
        ++(vlSelf->__Vcoverage[50]);
        vlSelfRef.tb_sync_fifo__DOT__status_errors = 0U;
        ++(vlSelf->__Vcoverage[51]);
        vlSelfRef.tb_sync_fifo__DOT__data_errors = 0U;
        ++(vlSelf->__Vcoverage[52]);
        vlSelfRef.tb_sync_fifo__DOT__head = 0U;
        ++(vlSelf->__Vcoverage[53]);
        vlSelfRef.tb_sync_fifo__DOT__tail = 0U;
        ++(vlSelf->__Vcoverage[54]);
        vlSelfRef.tb_sync_fifo__DOT__count = 0U;
        ++(vlSelf->__Vcoverage[55]);
        vlSelfRef.tb_sync_fifo__DOT__mode = 0U;
        ++(vlSelf->__Vcoverage[56]);
        vlSelfRef.tb_sync_fifo__DOT__functional_bins = 0U;
        ++(vlSelf->__Vcoverage[203]);
    }
    vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0 = 0U;
    vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__reset__0 = 0U;
    Vtb_sync_fifo___024root___timing_ready(vlSelf);
    do {
        vlSelfRef.__VactTriggeredAcc[vlSelfRef.__Vi] 
            = vlSelfRef.__VactTriggered[vlSelfRef.__Vi];
        vlSelfRef.__Vi = ((IData)(1U) + vlSelfRef.__Vi);
    } while ((0U >= vlSelfRef.__Vi));
}

VL_ATTR_COLD void Vtb_sync_fifo___024root___eval_final(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_final\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_sync_fifo___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtb_sync_fifo___024root___eval_phase__stl(Vtb_sync_fifo___024root* vlSelf);

VL_ATTR_COLD void Vtb_sync_fifo___024root___eval_settle(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_settle\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vtb_sync_fifo___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("examples/fifo/verif/tb_sync_fifo.sv", 2, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vtb_sync_fifo___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vtb_sync_fifo___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_sync_fifo___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vtb_sync_fifo___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vtb_sync_fifo___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD void Vtb_sync_fifo___024root___stl_sequent__TOP__0(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___stl_sequent__TOP__0\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((((1U & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q) 
                 >> 3U)) != (1U & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q) 
                                   >> 3U))) & ((7U 
                                                & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q)) 
                                               == (7U 
                                                   & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))))) {
        ++(vlSelf->__Vcoverage[461]);
    }
    if (((7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q)) 
         != (7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q)))) {
        ++(vlSelf->__Vcoverage[462]);
    }
    if (((1U & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q) 
                >> 3U)) == (1U & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q) 
                                  >> 3U)))) {
        ++(vlSelf->__Vcoverage[463]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__clk) 
         ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__clk))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 0, vlSelfRef.tb_sync_fifo__DOT__clk, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__clk);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__clk 
            = vlSelfRef.tb_sync_fifo__DOT__clk;
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__reset) 
         ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__reset))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 3, vlSelfRef.tb_sync_fifo__DOT__reset, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__reset);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__reset 
            = vlSelfRef.tb_sync_fifo__DOT__reset;
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__push_i) 
         ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__push_i))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 6, vlSelfRef.tb_sync_fifo__DOT__push_i, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__push_i);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__push_i 
            = vlSelfRef.tb_sync_fifo__DOT__push_i;
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__pop_i) 
         ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__pop_i))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 9, vlSelfRef.tb_sync_fifo__DOT__pop_i, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__pop_i);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__pop_i 
            = vlSelfRef.tb_sync_fifo__DOT__pop_i;
    }
    if ((0U != ((IData)(vlSelfRef.tb_sync_fifo__DOT__push_data_i) 
                ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__push_data_i)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 12, vlSelfRef.tb_sync_fifo__DOT__push_data_i, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__push_data_i);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__push_data_i 
            = vlSelfRef.tb_sync_fifo__DOT__push_data_i;
    }
    if ((0U != ((IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins) 
                ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__functional_bins)))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 185, vlSelfRef.tb_sync_fifo__DOT__functional_bins, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__functional_bins);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__functional_bins 
            = vlSelfRef.tb_sync_fifo__DOT__functional_bins;
    }
    if ((0U != ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q) 
                ^ (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__rd_ptr_q)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 290, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q, vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__rd_ptr_q);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__rd_ptr_q 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q;
    }
    if ((0U != ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q) 
                ^ (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__wr_ptr_q)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 306, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q, vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__wr_ptr_q);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__wr_ptr_q 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q;
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
                ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__pop_data_o)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 29, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                               [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__pop_data_o);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__pop_data_o 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))];
    }
    vlSelfRef.tb_sync_fifo__DOT__full_o = (((1U & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q) 
                                                   >> 3U)) 
                                            != (1U 
                                                & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q) 
                                                   >> 3U))) 
                                           & ((7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q)) 
                                              == (7U 
                                                  & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q))));
    vlSelfRef.tb_sync_fifo__DOT__empty_o = ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q) 
                                            == (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q));
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__expected[0U] 
                ^ vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[0U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 57, vlSelfRef.tb_sync_fifo__DOT__expected[0U], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[0U]);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[0U] 
            = vlSelfRef.tb_sync_fifo__DOT__expected[0U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__expected[1U] 
                ^ vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[1U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 73, vlSelfRef.tb_sync_fifo__DOT__expected[1U], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[1U]);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[1U] 
            = vlSelfRef.tb_sync_fifo__DOT__expected[1U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__expected[2U] 
                ^ vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[2U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 89, vlSelfRef.tb_sync_fifo__DOT__expected[2U], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[2U]);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[2U] 
            = vlSelfRef.tb_sync_fifo__DOT__expected[2U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__expected[3U] 
                ^ vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[3U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 105, vlSelfRef.tb_sync_fifo__DOT__expected[3U], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[3U]);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[3U] 
            = vlSelfRef.tb_sync_fifo__DOT__expected[3U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__expected[4U] 
                ^ vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[4U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 121, vlSelfRef.tb_sync_fifo__DOT__expected[4U], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[4U]);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[4U] 
            = vlSelfRef.tb_sync_fifo__DOT__expected[4U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__expected[5U] 
                ^ vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[5U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 137, vlSelfRef.tb_sync_fifo__DOT__expected[5U], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[5U]);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[5U] 
            = vlSelfRef.tb_sync_fifo__DOT__expected[5U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__expected[6U] 
                ^ vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[6U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 153, vlSelfRef.tb_sync_fifo__DOT__expected[6U], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[6U]);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[6U] 
            = vlSelfRef.tb_sync_fifo__DOT__expected[6U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__expected[7U] 
                ^ vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[7U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 169, vlSelfRef.tb_sync_fifo__DOT__expected[7U], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[7U]);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__expected[7U] 
            = vlSelfRef.tb_sync_fifo__DOT__expected[7U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[0U] 
                ^ vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[0U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 322, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[0U], vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[0U]);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[0U] 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[0U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[1U] 
                ^ vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[1U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 338, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[1U], vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[1U]);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[1U] 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[1U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[2U] 
                ^ vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[2U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 354, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[2U], vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[2U]);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[2U] 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[2U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[3U] 
                ^ vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[3U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 370, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[3U], vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[3U]);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[3U] 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[3U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[4U] 
                ^ vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[4U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 386, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[4U], vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[4U]);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[4U] 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[4U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[5U] 
                ^ vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[5U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 402, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[5U], vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[5U]);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[5U] 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[5U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[6U] 
                ^ vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[6U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 418, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[6U], vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[6U]);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[6U] 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[6U];
    }
    if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[7U] 
                ^ vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[7U]))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 434, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[7U], vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[7U]);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[7U] 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[7U];
    }
    vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_rd_ptr 
        = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q;
    vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_wr_ptr 
        = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q;
    if ((1U == (((IData)(vlSelfRef.tb_sync_fifo__DOT__pop_i) 
                 << 1U) | (IData)(vlSelfRef.tb_sync_fifo__DOT__push_i)))) {
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_wr_ptr 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q)));
        ++(vlSelf->__Vcoverage[453]);
    } else if ((2U == (((IData)(vlSelfRef.tb_sync_fifo__DOT__pop_i) 
                        << 1U) | (IData)(vlSelfRef.tb_sync_fifo__DOT__push_i)))) {
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_rd_ptr 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q)));
        ++(vlSelf->__Vcoverage[454]);
    } else if ((3U == (((IData)(vlSelfRef.tb_sync_fifo__DOT__pop_i) 
                        << 1U) | (IData)(vlSelfRef.tb_sync_fifo__DOT__push_i)))) {
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_wr_ptr 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q)));
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_rd_ptr 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q)));
        ++(vlSelf->__Vcoverage[455]);
    } else {
        ++(vlSelf->__Vcoverage[456]);
    }
    ++(vlSelf->__Vcoverage[457]);
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
         ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__full_o))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 45, vlSelfRef.tb_sync_fifo__DOT__full_o, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__full_o);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__full_o 
            = vlSelfRef.tb_sync_fifo__DOT__full_o;
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
         ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__empty_o))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 47, vlSelfRef.tb_sync_fifo__DOT__empty_o, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__empty_o);
        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__empty_o 
            = vlSelfRef.tb_sync_fifo__DOT__empty_o;
    }
    if ((0U != ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_rd_ptr) 
                ^ (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_rd_ptr)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 298, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_rd_ptr, vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_rd_ptr);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_rd_ptr 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_rd_ptr;
    }
    if ((0U != ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_wr_ptr) 
                ^ (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_wr_ptr)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 314, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_wr_ptr, vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_wr_ptr);
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_wr_ptr 
            = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_wr_ptr;
    }
}

VL_ATTR_COLD bool Vtb_sync_fifo___024root___eval_phase__stl(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_phase__stl\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
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
        Vtb_sync_fifo___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vtb_sync_fifo___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                Vtb_sync_fifo___024root___stl_sequent__TOP__0(vlSelf);
            }
        }
    }
    return (__VstlExecute);
}

bool Vtb_sync_fifo___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_sync_fifo___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vtb_sync_fifo___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge tb_sync_fifo.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge tb_sync_fifo.reset)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @(negedge tb_sync_fifo.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @([true] __VdlySched.awaitingCurrentTime())\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtb_sync_fifo___024root___ctor_var_reset(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___ctor_var_reset\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->tb_sync_fifo__DOT____VExpr_h16e95b7f__1 = 0;
    vlSelf->tb_sync_fifo__DOT____VExpr_h16e95b7f__0 = 0;
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->tb_sync_fifo__DOT__full_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 245993597004212799ull);
    vlSelf->tb_sync_fifo__DOT__empty_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6666768703079776426ull);
    vlSelf->tb_sync_fifo__DOT__vector_file = 0;
    vlSelf->tb_sync_fifo__DOT__scan_status = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15593128739217490805ull);
    vlSelf->tb_sync_fifo__DOT__vector_reset = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1502153985841994657ull);
    vlSelf->tb_sync_fifo__DOT__vector_push = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3004755942434901482ull);
    vlSelf->tb_sync_fifo__DOT__vector_pop = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5753606656425232485ull);
    vlSelf->tb_sync_fifo__DOT__vector_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12811433909708958365ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->tb_sync_fifo__DOT__expected[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13684625732814171235ull);
    }
    VL_SCOPED_RAND_RESET_W(1024, vlSelf->tb_sync_fifo__DOT__vector_path, __VscopeHash, 14006869321987963490ull);
    vlSelf->tb_sync_fifo__DOT____Vtogcov__clk = 0;
    vlSelf->tb_sync_fifo__DOT____Vtogcov__reset = 0;
    vlSelf->tb_sync_fifo__DOT____Vtogcov__push_i = 0;
    vlSelf->tb_sync_fifo__DOT____Vtogcov__pop_i = 0;
    vlSelf->tb_sync_fifo__DOT____Vtogcov__push_data_i = 0;
    vlSelf->tb_sync_fifo__DOT____Vtogcov__pop_data_o = 0;
    vlSelf->tb_sync_fifo__DOT____Vtogcov__full_o = 0;
    vlSelf->tb_sync_fifo__DOT____Vtogcov__empty_o = 0;
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->tb_sync_fifo__DOT____Vtogcov__expected[__Vi0] = 0;
    }
    vlSelf->tb_sync_fifo__DOT____Vtogcov__functional_bins = 0;
    vlSelf->tb_sync_fifo__DOT__dut__DOT__rd_ptr_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6972563995730434465ull);
    vlSelf->tb_sync_fifo__DOT__dut__DOT__nxt_rd_ptr = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16658714708753991204ull);
    vlSelf->tb_sync_fifo__DOT__dut__DOT__wr_ptr_q = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7636225199302824410ull);
    vlSelf->tb_sync_fifo__DOT__dut__DOT__nxt_wr_ptr = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11250110918027148268ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->tb_sync_fifo__DOT__dut__DOT__fifo_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16374158336429082054ull);
    }
    vlSelf->tb_sync_fifo__DOT__dut__DOT____Vtogcov__rd_ptr_q = 0;
    vlSelf->tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_rd_ptr = 0;
    vlSelf->tb_sync_fifo__DOT__dut__DOT____Vtogcov__wr_ptr_q = 0;
    vlSelf->tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_wr_ptr = 0;
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggeredAcc[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__reset__0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
    vlSelf->__Vi = 0;
}

VL_ATTR_COLD void Vtb_sync_fifo___024root___configure_coverage(Vtb_sync_fifo___024root* vlSelf, bool first) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___configure_coverage\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    (void)first;  // Prevent unused variable warning
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 0, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 4, 9, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "clk");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 2, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 4, 15, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "4", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 2, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 4, 15, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "4", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 3, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 4, 18, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "reset");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 5, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 4, 26, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "4", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 5, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 4, 26, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "4", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 6, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 5, 9, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "push_i");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 8, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 5, 18, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "5", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 8, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 5, 18, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "5", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 9, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 5, 21, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "pop_i");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 11, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 5, 29, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "5", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 11, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 5, 29, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "5", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 12, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 6, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "push_data_i");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 28, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 6, 29, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "6", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 28, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 6, 29, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "6", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 29, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 7, 16, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "pop_data_o");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 45, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 8, 10, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "full_o");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 47, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 8, 18, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "empty_o");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 49, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 9, 22, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 49, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 9, 22, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 50, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 9, 45, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 50, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 9, 45, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 51, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 9, 64, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 51, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 9, 64, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 52, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 9, 81, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 52, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 9, 81, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "9", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 53, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 10, 20, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "10", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 53, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 10, 20, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "10", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 54, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 10, 30, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "10", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 54, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 10, 30, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "10", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 55, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 10, 41, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "10", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 55, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 10, 41, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "10", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 56, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 11, 20, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "11", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 56, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 11, 20, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "11", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 57, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 13, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "expected[0]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 73, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 13, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "expected[1]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 89, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 13, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "expected[2]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 105, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 13, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "expected[3]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 121, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 13, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "expected[4]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 137, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 13, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "expected[5]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 153, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 13, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "expected[6]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 169, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 13, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "expected[7]");
    vlSelf->__vlCoverToggleInsert(0, 8, 1, vlSelf->__Vcoverage + 185, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 14, 15, ".tb_sync_fifo", "v_toggle/tb_sync_fifo", "functional_bins");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 203, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 14, 33, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "14", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 203, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 14, 33, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "14", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 204, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 21, 21, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(clk==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 204, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 21, 21, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(clk==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 205, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 21, 21, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(clk==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 205, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 21, 21, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(clk==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 206, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 21, 5, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "21", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 206, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 21, 5, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "21", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 207, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 28, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "28-29", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 207, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 28, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "28-29", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 208, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 28, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 208, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 28, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 209, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 25, 13, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "25-27", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 209, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 25, 13, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "25-27", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 210, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 25, 14, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 210, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 25, 14, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 211, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 25, 42, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((full_o !== (count == DEPTH))==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 211, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 25, 42, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((full_o !== (count == DEPTH))==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 212, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 25, 42, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((empty_o !== (count == 32'sh0))==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 212, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 25, 42, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((empty_o !== (count == 32'sh0))==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 213, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 25, 42, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((empty_o !== (count == 32'sh0))==0 && (full_o !== (count == DEPTH))==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 213, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 25, 42, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((empty_o !== (count == 32'sh0))==0 && (full_o !== (count == DEPTH))==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 214, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 34, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "34-35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 214, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 34, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "34-35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 215, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 34, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 215, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 34, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 216, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 31, 13, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "31-33", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 216, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 31, 13, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "31-33", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 217, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 31, 14, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 217, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 31, 14, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 218, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 31, 27, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count > 32'sh0)==1 && (pop_data_o !== (expected[head[2:0]]))==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 218, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 31, 27, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count > 32'sh0)==1 && (pop_data_o !== (expected[head[2:0]]))==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 219, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 31, 27, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((pop_data_o !== (expected[head[2:0]]))==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 219, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 31, 27, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((pop_data_o !== (expected[head[2:0]]))==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 220, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 31, 27, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count > 32'sh0)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 220, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 31, 27, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count > 32'sh0)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 221, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 23, 20, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "23-24", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 221, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 23, 20, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "23-24", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 222, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 50, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "50", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 222, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 50, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "50", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 223, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 50, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 223, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 50, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 224, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 54, 23, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 224, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 54, 23, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 225, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1 && (count == DEPTH)==1 && pop==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 225, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1 && (count == DEPTH)==1 && pop==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 226, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==1 && (count == 32'sh0)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 226, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==1 && (count == 32'sh0)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 227, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh0)==0 && pop==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 227, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh0)==0 && pop==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 228, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh0)==0 && (count == DEPTH)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 228, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh0)==0 && (count == DEPTH)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 229, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh0)==0 && push==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 229, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh0)==0 && push==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 230, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==0 && (count == DEPTH)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 230, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==0 && (count == DEPTH)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 231, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==0 && push==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 231, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 54, 46, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==0 && push==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 232, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 49, 13, ".tb_sync_fifo", "v_line/tb_sync_fifo", "elsif", "49,51-53", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 232, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 49, 13, ".tb_sync_fifo", "v_line/tb_sync_fifo", "elsif", "49,51-53", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 233, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 59, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "59", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 233, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 59, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "59", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 234, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 59, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 234, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 59, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 235, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 60, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "60", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 235, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 60, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "60", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 236, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 60, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 236, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 60, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 237, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 61, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "61", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 237, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 61, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "61", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 238, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 61, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 238, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 61, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 239, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 61, 45, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == DEPTH)==1 && push==0 && pop==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 239, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 61, 45, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == DEPTH)==1 && push==0 && pop==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 240, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 61, 45, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 240, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 61, 45, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 241, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 61, 45, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 241, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 61, 45, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 242, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 61, 45, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == DEPTH)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 242, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 61, 45, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == DEPTH)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 243, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 64, 21, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "64", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 243, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 64, 21, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "64", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 244, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 64, 22, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 244, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 64, 22, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 245, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 65, 21, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "65", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 245, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 65, 21, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "65", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 246, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 65, 22, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 246, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 65, 22, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 247, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 65, 36, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh1)==1 && push==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 247, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 65, 36, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh1)==1 && push==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 248, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 65, 36, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 248, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 65, 36, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 249, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 65, 36, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh1)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 249, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 65, 36, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((count == 32'sh1)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 250, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 62, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "62-63", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 250, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 62, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "62-63", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 251, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 62, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 251, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 62, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 252, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 67, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "67", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 252, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 67, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "67", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 253, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 67, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 253, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 67, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 254, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 67, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1 && pop==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 254, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 67, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1 && pop==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 255, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 67, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 255, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 67, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(pop==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 256, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 67, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 256, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 67, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 257, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 68, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "68", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 257, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 68, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "68", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 258, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 68, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 258, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 68, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 259, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 68, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1 && (tail == (DEPTH - 32'sh1))==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 259, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 68, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==1 && (tail == (DEPTH - 32'sh1))==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 260, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 68, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((tail == (DEPTH - 32'sh1))==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 260, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 68, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "((tail == (DEPTH - 32'sh1))==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 261, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 68, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 261, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 68, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(push==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 262, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 58, 13, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "58", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 262, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 58, 13, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "58", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 263, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 58, 14, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 263, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 58, 14, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 264, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 58, 17, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(rst==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 264, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 58, 17, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(rst==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 265, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 58, 17, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 265, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 58, 17, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 266, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 72, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "72-74", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 266, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 72, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "72-74", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 267, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 72, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 267, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 72, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 268, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 76, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "76-79", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 268, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 76, 17, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "76-79", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 269, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 76, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 269, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 76, 18, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 270, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 71, 13, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "71", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 270, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 71, 13, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "71", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 271, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 71, 14, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 271, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 71, 14, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 272, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 71, 17, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(rst==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 272, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 71, 17, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(rst==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 273, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 71, 17, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 273, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 71, 17, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "(rst==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 274, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 40, 20, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "40-48,56-57,70,82-84", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 274, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 40, 20, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "40-48,56-57,70,82-84", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 275, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 89, 9, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "89", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 275, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 89, 9, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "if", "89", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 276, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 89, 10, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 276, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 89, 10, ".tb_sync_fifo", "v_branch/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 277, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 95, 14, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 277, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 95, 14, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 278, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 98, 14, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 278, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 98, 14, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 279, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 99, 20, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "($feof(vector_file)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 279, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 99, 20, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "($feof(vector_file)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 280, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 99, 20, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "($feof(vector_file)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 280, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 99, 20, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "($feof(vector_file)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 281, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 104, 23, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 281, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 104, 23, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 282, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 104, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "($feof(vector_file)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 282, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 104, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "($feof(vector_file)==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 283, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 104, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "($feof(vector_file)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 283, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 104, 26, ".tb_sync_fifo", "v_expr/tb_sync_fifo", "($feof(vector_file)==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 284, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 102, 17, ".tb_sync_fifo", "v_line/tb_sync_fifo", "elsif", "102-103", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 284, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 102, 17, ".tb_sync_fifo", "v_line/tb_sync_fifo", "elsif", "102-103", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 285, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 99, 13, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "99-101", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 285, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 99, 13, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "99-101", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 286, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 107, 19, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 286, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 107, 19, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 287, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 94, 9, ".tb_sync_fifo", "v_line/tb_sync_fifo", "elsif", "94,97,106", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 287, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 94, 9, ".tb_sync_fifo", "v_line/tb_sync_fifo", "elsif", "94,97,106", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 288, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 109, 10, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 288, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 109, 10, ".tb_sync_fifo", "v_line/tb_sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 289, first, true, "examples/fifo/verif/tb_sync_fifo.sv", 88, 5, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "88,90-93,108,111", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 289, first, false, "examples/fifo/verif/tb_sync_fifo.sv", 88, 5, ".tb_sync_fifo", "v_line/tb_sync_fifo", "block", "88,90-93,108,111", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 0, first, true, "examples/fifo/rtl/sync_fifo.sv", 5, 28, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "clk");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 3, first, true, "examples/fifo/rtl/sync_fifo.sv", 6, 28, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "reset");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 6, first, true, "examples/fifo/rtl/sync_fifo.sv", 8, 28, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "push_i");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 12, first, true, "examples/fifo/rtl/sync_fifo.sv", 9, 28, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "push_data_i");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 9, first, true, "examples/fifo/rtl/sync_fifo.sv", 11, 28, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "pop_i");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 29, first, true, "examples/fifo/rtl/sync_fifo.sv", 12, 28, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "pop_data_o");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 45, first, true, "examples/fifo/rtl/sync_fifo.sv", 14, 28, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "full_o");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 47, first, true, "examples/fifo/rtl/sync_fifo.sv", 15, 28, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "empty_o");
    vlSelf->__vlCoverToggleInsert(0, 3, 1, vlSelf->__Vcoverage + 290, first, true, "examples/fifo/rtl/sync_fifo.sv", 20, 19, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "rd_ptr_q");
    vlSelf->__vlCoverToggleInsert(0, 3, 1, vlSelf->__Vcoverage + 298, first, true, "examples/fifo/rtl/sync_fifo.sv", 20, 29, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "nxt_rd_ptr");
    vlSelf->__vlCoverToggleInsert(0, 3, 1, vlSelf->__Vcoverage + 306, first, true, "examples/fifo/rtl/sync_fifo.sv", 21, 19, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "wr_ptr_q");
    vlSelf->__vlCoverToggleInsert(0, 3, 1, vlSelf->__Vcoverage + 314, first, true, "examples/fifo/rtl/sync_fifo.sv", 21, 29, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "nxt_wr_ptr");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 322, first, true, "examples/fifo/rtl/sync_fifo.sv", 24, 22, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "fifo_mem[0]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 338, first, true, "examples/fifo/rtl/sync_fifo.sv", 24, 22, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "fifo_mem[1]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 354, first, true, "examples/fifo/rtl/sync_fifo.sv", 24, 22, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "fifo_mem[2]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 370, first, true, "examples/fifo/rtl/sync_fifo.sv", 24, 22, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "fifo_mem[3]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 386, first, true, "examples/fifo/rtl/sync_fifo.sv", 24, 22, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "fifo_mem[4]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 402, first, true, "examples/fifo/rtl/sync_fifo.sv", 24, 22, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "fifo_mem[5]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 418, first, true, "examples/fifo/rtl/sync_fifo.sv", 24, 22, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "fifo_mem[6]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 434, first, true, "examples/fifo/rtl/sync_fifo.sv", 24, 22, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "fifo_mem[7]");
    vlSelf->__vlCoverToggleInsert(0, 7, 1, vlSelf->__Vcoverage + 29, first, true, "examples/fifo/rtl/sync_fifo.sv", 25, 22, ".tb_sync_fifo.dut", "v_toggle/sync_fifo", "fifo_pop_data");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 450, first, true, "examples/fifo/rtl/sync_fifo.sv", 31, 5, ".tb_sync_fifo.dut", "v_branch/sync_fifo", "if", "31-33", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 450, first, false, "examples/fifo/rtl/sync_fifo.sv", 31, 5, ".tb_sync_fifo.dut", "v_branch/sync_fifo", "if", "31-33", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 451, first, true, "examples/fifo/rtl/sync_fifo.sv", 31, 6, ".tb_sync_fifo.dut", "v_branch/sync_fifo", "else", "34-36", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 451, first, false, "examples/fifo/rtl/sync_fifo.sv", 31, 6, ".tb_sync_fifo.dut", "v_branch/sync_fifo", "else", "34-36", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 452, first, true, "examples/fifo/rtl/sync_fifo.sv", 30, 3, ".tb_sync_fifo.dut", "v_line/sync_fifo", "block", "30", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 452, first, false, "examples/fifo/rtl/sync_fifo.sv", 30, 3, ".tb_sync_fifo.dut", "v_line/sync_fifo", "block", "30", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 453, first, true, "examples/fifo/rtl/sync_fifo.sv", 48, 12, ".tb_sync_fifo.dut", "v_line/sync_fifo", "case", "48-49", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 453, first, false, "examples/fifo/rtl/sync_fifo.sv", 48, 12, ".tb_sync_fifo.dut", "v_line/sync_fifo", "case", "48-49", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 454, first, true, "examples/fifo/rtl/sync_fifo.sv", 50, 12, ".tb_sync_fifo.dut", "v_line/sync_fifo", "case", "50-51", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 454, first, false, "examples/fifo/rtl/sync_fifo.sv", 50, 12, ".tb_sync_fifo.dut", "v_line/sync_fifo", "case", "50-51", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 455, first, true, "examples/fifo/rtl/sync_fifo.sv", 52, 12, ".tb_sync_fifo.dut", "v_line/sync_fifo", "case", "52-55", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 455, first, false, "examples/fifo/rtl/sync_fifo.sv", 52, 12, ".tb_sync_fifo.dut", "v_line/sync_fifo", "case", "52-55", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 456, first, true, "examples/fifo/rtl/sync_fifo.sv", 57, 7, ".tb_sync_fifo.dut", "v_line/sync_fifo", "case", "57", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 456, first, false, "examples/fifo/rtl/sync_fifo.sv", 57, 7, ".tb_sync_fifo.dut", "v_line/sync_fifo", "case", "57", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 457, first, true, "examples/fifo/rtl/sync_fifo.sv", 41, 3, ".tb_sync_fifo.dut", "v_line/sync_fifo", "block", "41,43-45,47", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 457, first, false, "examples/fifo/rtl/sync_fifo.sv", 41, 3, ".tb_sync_fifo.dut", "v_line/sync_fifo", "block", "41,43-45,47", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 458, first, true, "examples/fifo/rtl/sync_fifo.sv", 63, 5, ".tb_sync_fifo.dut", "v_branch/sync_fifo", "if", "63-64", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 458, first, false, "examples/fifo/rtl/sync_fifo.sv", 63, 5, ".tb_sync_fifo.dut", "v_branch/sync_fifo", "if", "63-64", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 459, first, true, "examples/fifo/rtl/sync_fifo.sv", 63, 6, ".tb_sync_fifo.dut", "v_branch/sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 459, first, false, "examples/fifo/rtl/sync_fifo.sv", 63, 6, ".tb_sync_fifo.dut", "v_branch/sync_fifo", "else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 460, first, true, "examples/fifo/rtl/sync_fifo.sv", 62, 3, ".tb_sync_fifo.dut", "v_line/sync_fifo", "block", "62", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 460, first, false, "examples/fifo/rtl/sync_fifo.sv", 62, 3, ".tb_sync_fifo.dut", "v_line/sync_fifo", "block", "62", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 461, first, true, "examples/fifo/rtl/sync_fifo.sv", 70, 58, ".tb_sync_fifo.dut", "v_expr/sync_fifo", "((wr_ptr_q[PTR_W[1:0]+:1] != rd_ptr_q[PTR_W[1:0]+:1])==1 && (wr_ptr_q[2:0] == rd_ptr_q[2:0])==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 461, first, false, "examples/fifo/rtl/sync_fifo.sv", 70, 58, ".tb_sync_fifo.dut", "v_expr/sync_fifo", "((wr_ptr_q[PTR_W[1:0]+:1] != rd_ptr_q[PTR_W[1:0]+:1])==1 && (wr_ptr_q[2:0] == rd_ptr_q[2:0])==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 462, first, true, "examples/fifo/rtl/sync_fifo.sv", 70, 58, ".tb_sync_fifo.dut", "v_expr/sync_fifo", "((wr_ptr_q[2:0] == rd_ptr_q[2:0])==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 462, first, false, "examples/fifo/rtl/sync_fifo.sv", 70, 58, ".tb_sync_fifo.dut", "v_expr/sync_fifo", "((wr_ptr_q[2:0] == rd_ptr_q[2:0])==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 463, first, true, "examples/fifo/rtl/sync_fifo.sv", 70, 58, ".tb_sync_fifo.dut", "v_expr/sync_fifo", "((wr_ptr_q[PTR_W[1:0]+:1] != rd_ptr_q[PTR_W[1:0]+:1])==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 463, first, false, "examples/fifo/rtl/sync_fifo.sv", 70, 58, ".tb_sync_fifo.dut", "v_expr/sync_fifo", "((wr_ptr_q[PTR_W[1:0]+:1] != rd_ptr_q[PTR_W[1:0]+:1])==0) => 0", "", "", "", "", "");
}
