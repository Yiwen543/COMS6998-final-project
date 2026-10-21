// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_sync_fifo.h for the primary calling header

#include "Vtb_sync_fifo__pch.h"

VlCoroutine Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__0(Vtb_sync_fifo___024root* vlSelf);
VlCoroutine Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__1(Vtb_sync_fifo___024root* vlSelf);
VlCoroutine Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__2(Vtb_sync_fifo___024root* vlSelf);

void Vtb_sync_fifo___024root___eval_initial(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_initial\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__0(vlSelf);
    Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__1(vlSelf);
    Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__2(vlSelf);
}

void Vtb_sync_fifo___024root____VbeforeTrig_h0839a9c0__0(Vtb_sync_fifo___024root* vlSelf, const char* __VeventDescription);
void Vtb_sync_fifo___024root____VbeforeTrig_h0839b971__0(Vtb_sync_fifo___024root* vlSelf, const char* __VeventDescription);

VlCoroutine Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__0(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ tb_sync_fifo__DOT____VlemExpr_0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__0__rst;
    __Vtask_tb_sync_fifo__DOT__step__0__rst = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__0__push;
    __Vtask_tb_sync_fifo__DOT__step__0__push = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__0__pop;
    __Vtask_tb_sync_fifo__DOT__step__0__pop = 0;
    CData/*7:0*/ __Vtask_tb_sync_fifo__DOT__step__0__data;
    __Vtask_tb_sync_fifo__DOT__step__0__data = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__step__0__old_count;
    __Vtask_tb_sync_fifo__DOT__step__0__old_count = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__1__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__1__cycle_id = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__2__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__2__cycle_id = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__3__rst;
    __Vtask_tb_sync_fifo__DOT__step__3__rst = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__3__push;
    __Vtask_tb_sync_fifo__DOT__step__3__push = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__3__pop;
    __Vtask_tb_sync_fifo__DOT__step__3__pop = 0;
    CData/*7:0*/ __Vtask_tb_sync_fifo__DOT__step__3__data;
    __Vtask_tb_sync_fifo__DOT__step__3__data = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__step__3__old_count;
    __Vtask_tb_sync_fifo__DOT__step__3__old_count = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__4__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__4__cycle_id = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__5__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__5__cycle_id = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__6__rst;
    __Vtask_tb_sync_fifo__DOT__step__6__rst = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__6__push;
    __Vtask_tb_sync_fifo__DOT__step__6__push = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__6__pop;
    __Vtask_tb_sync_fifo__DOT__step__6__pop = 0;
    CData/*7:0*/ __Vtask_tb_sync_fifo__DOT__step__6__data;
    __Vtask_tb_sync_fifo__DOT__step__6__data = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__step__6__old_count;
    __Vtask_tb_sync_fifo__DOT__step__6__old_count = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__7__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__7__cycle_id = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__8__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__8__cycle_id = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__9__rst;
    __Vtask_tb_sync_fifo__DOT__step__9__rst = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__9__push;
    __Vtask_tb_sync_fifo__DOT__step__9__push = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__9__pop;
    __Vtask_tb_sync_fifo__DOT__step__9__pop = 0;
    CData/*7:0*/ __Vtask_tb_sync_fifo__DOT__step__9__data;
    __Vtask_tb_sync_fifo__DOT__step__9__data = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__step__9__old_count;
    __Vtask_tb_sync_fifo__DOT__step__9__old_count = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__10__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__10__cycle_id = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__11__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__11__cycle_id = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__12__rst;
    __Vtask_tb_sync_fifo__DOT__step__12__rst = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__12__push;
    __Vtask_tb_sync_fifo__DOT__step__12__push = 0;
    CData/*0:0*/ __Vtask_tb_sync_fifo__DOT__step__12__pop;
    __Vtask_tb_sync_fifo__DOT__step__12__pop = 0;
    CData/*7:0*/ __Vtask_tb_sync_fifo__DOT__step__12__data;
    __Vtask_tb_sync_fifo__DOT__step__12__data = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__step__12__old_count;
    __Vtask_tb_sync_fifo__DOT__step__12__old_count = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__13__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__13__cycle_id = 0;
    IData/*31:0*/ __Vtask_tb_sync_fifo__DOT__check_outputs__14__cycle_id;
    __Vtask_tb_sync_fifo__DOT__check_outputs__14__cycle_id = 0;
    // Body
    tb_sync_fifo__DOT____VlemExpr_0 = VL_VALUEPLUSARGS_INI(32, "MODE=%d"s, 
                                                           vlSelfRef.tb_sync_fifo__DOT__mode);
    if (tb_sync_fifo__DOT____VlemExpr_0) {
        ++(vlSelf->__Vcoverage[275]);
    } else {
        ++(vlSelf->__Vcoverage[276]);
    }
    __Vtask_tb_sync_fifo__DOT__step__0__data = 0U;
    __Vtask_tb_sync_fifo__DOT__step__0__pop = 0U;
    __Vtask_tb_sync_fifo__DOT__step__0__push = 0U;
    __Vtask_tb_sync_fifo__DOT__step__0__rst = 1U;
    __Vtask_tb_sync_fifo__DOT__step__0__old_count = 0;
    Vtb_sync_fifo___024root____VbeforeTrig_h0839a9c0__0(vlSelf, 
                                                        "@(negedge tb_sync_fifo.clk)");
    co_await vlSelfRef.__VtrigSched_h0839a9c0__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(negedge tb_sync_fifo.clk)", 
                                                         "examples/fifo/verif/tb_sync_fifo.sv", 
                                                         43);
    __Vtask_tb_sync_fifo__DOT__step__0__old_count = vlSelfRef.tb_sync_fifo__DOT__count;
    vlSelfRef.tb_sync_fifo__DOT__reset = __Vtask_tb_sync_fifo__DOT__step__0__rst;
    vlSelfRef.tb_sync_fifo__DOT__push_i = __Vtask_tb_sync_fifo__DOT__step__0__push;
    vlSelfRef.tb_sync_fifo__DOT__pop_i = __Vtask_tb_sync_fifo__DOT__step__0__pop;
    vlSelfRef.tb_sync_fifo__DOT__push_data_i = __Vtask_tb_sync_fifo__DOT__step__0__data;
    if (__Vtask_tb_sync_fifo__DOT__step__0__rst) {
        if (VL_LTS_III(32, 0U, __Vtask_tb_sync_fifo__DOT__step__0__old_count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000040U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[222]);
        } else {
            ++(vlSelf->__Vcoverage[223]);
        }
        vlSelfRef.tb_sync_fifo__DOT__head = 0U;
        vlSelfRef.tb_sync_fifo__DOT__tail = 0U;
        vlSelfRef.tb_sync_fifo__DOT__count = 0U;
        ++(vlSelf->__Vcoverage[232]);
    } else {
        if (VL_UNLIKELY(((((IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop) 
                           & (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                          | (((IData)(__Vtask_tb_sync_fifo__DOT__step__0__push) 
                              & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop))))))) {
            VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:55: Assertion failed in %m: Illegal FIFO action under frozen contract\n",3, 'M',vlSymsp->name(),"tb_sync_fifo.step", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 55, "", false);
        } else {
            ++(vlSelf->__Vcoverage[224]);
        }
        if ((((IData)(__Vtask_tb_sync_fifo__DOT__step__0__push) 
              & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop)))) {
            ++(vlSelf->__Vcoverage[225]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop) 
             & (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[226]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop))) {
            ++(vlSelf->__Vcoverage[227]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[228]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__push)))) {
            ++(vlSelf->__Vcoverage[229]);
        }
        if (((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop)) 
             & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[230]);
        }
        if ((1U & ((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop)) 
                   & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__push))))) {
            ++(vlSelf->__Vcoverage[231]);
        }
    }
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/fifo/verif/tb_sync_fifo.sv", 
                                         56);
    __Vtask_tb_sync_fifo__DOT__check_outputs__1__cycle_id 
        = vlSelfRef.tb_sync_fifo__DOT__checks;
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__status_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__1__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                         , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                         , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
            ++(vlSelf->__Vcoverage[207]);
        } else {
            ++(vlSelf->__Vcoverage[208]);
        }
        ++(vlSelf->__Vcoverage[209]);
    } else {
        ++(vlSelf->__Vcoverage[210]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__data_errors = 
            ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__1__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                         [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
            ++(vlSelf->__Vcoverage[214]);
        } else {
            ++(vlSelf->__Vcoverage[215]);
        }
        ++(vlSelf->__Vcoverage[216]);
    } else {
        ++(vlSelf->__Vcoverage[217]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
         != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[211]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
         != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[212]);
    }
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        ++(vlSelf->__Vcoverage[213]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        ++(vlSelf->__Vcoverage[218]);
    }
    if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
         == vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__head)])) {
        ++(vlSelf->__Vcoverage[219]);
    }
    if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
        ++(vlSelf->__Vcoverage[220]);
    }
    ++(vlSelf->__Vcoverage[221]);
    if (__Vtask_tb_sync_fifo__DOT__step__0__rst) {
        ++(vlSelf->__Vcoverage[263]);
    } else {
        if ((0U == vlSelfRef.tb_sync_fifo__DOT__count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (1U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[233]);
        } else {
            ++(vlSelf->__Vcoverage[234]);
        }
        if ((8U == vlSelfRef.tb_sync_fifo__DOT__count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (4U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[235]);
        } else {
            ++(vlSelf->__Vcoverage[236]);
        }
        if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
              & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__push))) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop)))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000080U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[237]);
        } else {
            ++(vlSelf->__Vcoverage[238]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__0__pop) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (2U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            if ((7U == vlSelfRef.tb_sync_fifo__DOT__head)) {
                vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                    = (0x00000020U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                ++(vlSelf->__Vcoverage[243]);
            } else {
                ++(vlSelf->__Vcoverage[244]);
            }
            if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                 & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__push)))) {
                vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                    = (0x00000100U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                ++(vlSelf->__Vcoverage[245]);
            } else {
                ++(vlSelf->__Vcoverage[246]);
            }
            if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                 & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__push)))) {
                ++(vlSelf->__Vcoverage[247]);
            }
            if (__Vtask_tb_sync_fifo__DOT__step__0__push) {
                ++(vlSelf->__Vcoverage[248]);
            }
            if ((1U != vlSelfRef.tb_sync_fifo__DOT__count)) {
                ++(vlSelf->__Vcoverage[249]);
            }
            ++(vlSelf->__Vcoverage[250]);
        } else {
            ++(vlSelf->__Vcoverage[251]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__0__push) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (8U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[252]);
        } else {
            ++(vlSelf->__Vcoverage[253]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__0__push) 
             & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000010U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[257]);
        } else {
            ++(vlSelf->__Vcoverage[258]);
        }
        if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
              & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__push))) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop)))) {
            ++(vlSelf->__Vcoverage[239]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__0__pop) {
            ++(vlSelf->__Vcoverage[240]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__0__push) {
            ++(vlSelf->__Vcoverage[241]);
        }
        if ((8U != vlSelfRef.tb_sync_fifo__DOT__count)) {
            ++(vlSelf->__Vcoverage[242]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__0__push) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop))) {
            ++(vlSelf->__Vcoverage[254]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__pop)))) {
            ++(vlSelf->__Vcoverage[255]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__push)))) {
            ++(vlSelf->__Vcoverage[256]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__0__push) 
             & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
            ++(vlSelf->__Vcoverage[259]);
        }
        if ((7U != vlSelfRef.tb_sync_fifo__DOT__tail)) {
            ++(vlSelf->__Vcoverage[260]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__push)))) {
            ++(vlSelf->__Vcoverage[261]);
        }
        ++(vlSelf->__Vcoverage[262]);
    }
    Vtb_sync_fifo___024root____VbeforeTrig_h0839b971__0(vlSelf, 
                                                        "@(posedge tb_sync_fifo.clk)");
    co_await vlSelfRef.__VtrigSched_h0839b971__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge tb_sync_fifo.clk)", 
                                                         "examples/fifo/verif/tb_sync_fifo.sv", 
                                                         70);
    if (__Vtask_tb_sync_fifo__DOT__step__0__rst) {
        ++(vlSelf->__Vcoverage[271]);
    } else {
        if (__Vtask_tb_sync_fifo__DOT__step__0__pop) {
            vlSelfRef.tb_sync_fifo__DOT__head = VL_MODDIVS_III(32, 
                                                               ((IData)(1U) 
                                                                + vlSelfRef.tb_sync_fifo__DOT__head), (IData)(8U));
            vlSelfRef.tb_sync_fifo__DOT__count = (vlSelfRef.tb_sync_fifo__DOT__count 
                                                  - (IData)(1U));
            ++(vlSelf->__Vcoverage[266]);
        } else {
            ++(vlSelf->__Vcoverage[267]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__0__push) {
            vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__tail)] 
                = __Vtask_tb_sync_fifo__DOT__step__0__data;
            vlSelfRef.tb_sync_fifo__DOT__tail = VL_MODDIVS_III(32, 
                                                               ((IData)(1U) 
                                                                + vlSelfRef.tb_sync_fifo__DOT__tail), (IData)(8U));
            vlSelfRef.tb_sync_fifo__DOT__count = ((IData)(1U) 
                                                  + vlSelfRef.tb_sync_fifo__DOT__count);
            ++(vlSelf->__Vcoverage[268]);
        } else {
            ++(vlSelf->__Vcoverage[269]);
        }
        ++(vlSelf->__Vcoverage[270]);
    }
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/fifo/verif/tb_sync_fifo.sv", 
                                         82);
    __Vtask_tb_sync_fifo__DOT__check_outputs__2__cycle_id 
        = vlSelfRef.tb_sync_fifo__DOT__checks;
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__status_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__2__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                         , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                         , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
            ++(vlSelf->__Vcoverage[207]);
        } else {
            ++(vlSelf->__Vcoverage[208]);
        }
        ++(vlSelf->__Vcoverage[209]);
    } else {
        ++(vlSelf->__Vcoverage[210]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__data_errors = 
            ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__2__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                         [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
            ++(vlSelf->__Vcoverage[214]);
        } else {
            ++(vlSelf->__Vcoverage[215]);
        }
        ++(vlSelf->__Vcoverage[216]);
    } else {
        ++(vlSelf->__Vcoverage[217]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
         != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[211]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
         != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[212]);
    }
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        ++(vlSelf->__Vcoverage[213]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        ++(vlSelf->__Vcoverage[218]);
    }
    if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
         == vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__head)])) {
        ++(vlSelf->__Vcoverage[219]);
    }
    if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
        ++(vlSelf->__Vcoverage[220]);
    }
    ++(vlSelf->__Vcoverage[221]);
    vlSelfRef.tb_sync_fifo__DOT__checks = ((IData)(1U) 
                                           + vlSelfRef.tb_sync_fifo__DOT__checks);
    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__rst)))) {
        ++(vlSelf->__Vcoverage[264]);
    }
    if (__Vtask_tb_sync_fifo__DOT__step__0__rst) {
        ++(vlSelf->__Vcoverage[265]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__0__rst)))) {
        ++(vlSelf->__Vcoverage[272]);
    }
    if (__Vtask_tb_sync_fifo__DOT__step__0__rst) {
        ++(vlSelf->__Vcoverage[273]);
    }
    ++(vlSelf->__Vcoverage[274]);
    __Vtask_tb_sync_fifo__DOT__step__3__data = 0x11U;
    __Vtask_tb_sync_fifo__DOT__step__3__pop = 0U;
    __Vtask_tb_sync_fifo__DOT__step__3__push = 1U;
    __Vtask_tb_sync_fifo__DOT__step__3__rst = 0U;
    __Vtask_tb_sync_fifo__DOT__step__3__old_count = 0;
    Vtb_sync_fifo___024root____VbeforeTrig_h0839a9c0__0(vlSelf, 
                                                        "@(negedge tb_sync_fifo.clk)");
    co_await vlSelfRef.__VtrigSched_h0839a9c0__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(negedge tb_sync_fifo.clk)", 
                                                         "examples/fifo/verif/tb_sync_fifo.sv", 
                                                         43);
    __Vtask_tb_sync_fifo__DOT__step__3__old_count = vlSelfRef.tb_sync_fifo__DOT__count;
    vlSelfRef.tb_sync_fifo__DOT__reset = __Vtask_tb_sync_fifo__DOT__step__3__rst;
    vlSelfRef.tb_sync_fifo__DOT__push_i = __Vtask_tb_sync_fifo__DOT__step__3__push;
    vlSelfRef.tb_sync_fifo__DOT__pop_i = __Vtask_tb_sync_fifo__DOT__step__3__pop;
    vlSelfRef.tb_sync_fifo__DOT__push_data_i = __Vtask_tb_sync_fifo__DOT__step__3__data;
    if (__Vtask_tb_sync_fifo__DOT__step__3__rst) {
        if (VL_LTS_III(32, 0U, __Vtask_tb_sync_fifo__DOT__step__3__old_count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000040U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[222]);
        } else {
            ++(vlSelf->__Vcoverage[223]);
        }
        vlSelfRef.tb_sync_fifo__DOT__head = 0U;
        vlSelfRef.tb_sync_fifo__DOT__tail = 0U;
        vlSelfRef.tb_sync_fifo__DOT__count = 0U;
        ++(vlSelf->__Vcoverage[232]);
    } else {
        if (VL_UNLIKELY(((((IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop) 
                           & (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                          | (((IData)(__Vtask_tb_sync_fifo__DOT__step__3__push) 
                              & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop))))))) {
            VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:55: Assertion failed in %m: Illegal FIFO action under frozen contract\n",3, 'M',vlSymsp->name(),"tb_sync_fifo.step", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 55, "", false);
        } else {
            ++(vlSelf->__Vcoverage[224]);
        }
        if ((((IData)(__Vtask_tb_sync_fifo__DOT__step__3__push) 
              & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop)))) {
            ++(vlSelf->__Vcoverage[225]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop) 
             & (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[226]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop))) {
            ++(vlSelf->__Vcoverage[227]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[228]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__push)))) {
            ++(vlSelf->__Vcoverage[229]);
        }
        if (((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop)) 
             & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[230]);
        }
        if ((1U & ((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop)) 
                   & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__push))))) {
            ++(vlSelf->__Vcoverage[231]);
        }
    }
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/fifo/verif/tb_sync_fifo.sv", 
                                         56);
    __Vtask_tb_sync_fifo__DOT__check_outputs__4__cycle_id 
        = vlSelfRef.tb_sync_fifo__DOT__checks;
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__status_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__4__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                         , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                         , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
            ++(vlSelf->__Vcoverage[207]);
        } else {
            ++(vlSelf->__Vcoverage[208]);
        }
        ++(vlSelf->__Vcoverage[209]);
    } else {
        ++(vlSelf->__Vcoverage[210]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__data_errors = 
            ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__4__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                         [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
            ++(vlSelf->__Vcoverage[214]);
        } else {
            ++(vlSelf->__Vcoverage[215]);
        }
        ++(vlSelf->__Vcoverage[216]);
    } else {
        ++(vlSelf->__Vcoverage[217]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
         != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[211]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
         != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[212]);
    }
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        ++(vlSelf->__Vcoverage[213]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        ++(vlSelf->__Vcoverage[218]);
    }
    if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
         == vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__head)])) {
        ++(vlSelf->__Vcoverage[219]);
    }
    if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
        ++(vlSelf->__Vcoverage[220]);
    }
    ++(vlSelf->__Vcoverage[221]);
    if (__Vtask_tb_sync_fifo__DOT__step__3__rst) {
        ++(vlSelf->__Vcoverage[263]);
    } else {
        if ((0U == vlSelfRef.tb_sync_fifo__DOT__count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (1U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[233]);
        } else {
            ++(vlSelf->__Vcoverage[234]);
        }
        if ((8U == vlSelfRef.tb_sync_fifo__DOT__count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (4U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[235]);
        } else {
            ++(vlSelf->__Vcoverage[236]);
        }
        if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
              & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__push))) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop)))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000080U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[237]);
        } else {
            ++(vlSelf->__Vcoverage[238]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__3__pop) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (2U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            if ((7U == vlSelfRef.tb_sync_fifo__DOT__head)) {
                vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                    = (0x00000020U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                ++(vlSelf->__Vcoverage[243]);
            } else {
                ++(vlSelf->__Vcoverage[244]);
            }
            if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                 & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__push)))) {
                vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                    = (0x00000100U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                ++(vlSelf->__Vcoverage[245]);
            } else {
                ++(vlSelf->__Vcoverage[246]);
            }
            if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                 & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__push)))) {
                ++(vlSelf->__Vcoverage[247]);
            }
            if (__Vtask_tb_sync_fifo__DOT__step__3__push) {
                ++(vlSelf->__Vcoverage[248]);
            }
            if ((1U != vlSelfRef.tb_sync_fifo__DOT__count)) {
                ++(vlSelf->__Vcoverage[249]);
            }
            ++(vlSelf->__Vcoverage[250]);
        } else {
            ++(vlSelf->__Vcoverage[251]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__3__push) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (8U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[252]);
        } else {
            ++(vlSelf->__Vcoverage[253]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__3__push) 
             & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000010U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[257]);
        } else {
            ++(vlSelf->__Vcoverage[258]);
        }
        if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
              & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__push))) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop)))) {
            ++(vlSelf->__Vcoverage[239]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__3__pop) {
            ++(vlSelf->__Vcoverage[240]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__3__push) {
            ++(vlSelf->__Vcoverage[241]);
        }
        if ((8U != vlSelfRef.tb_sync_fifo__DOT__count)) {
            ++(vlSelf->__Vcoverage[242]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__3__push) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop))) {
            ++(vlSelf->__Vcoverage[254]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__pop)))) {
            ++(vlSelf->__Vcoverage[255]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__push)))) {
            ++(vlSelf->__Vcoverage[256]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__3__push) 
             & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
            ++(vlSelf->__Vcoverage[259]);
        }
        if ((7U != vlSelfRef.tb_sync_fifo__DOT__tail)) {
            ++(vlSelf->__Vcoverage[260]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__push)))) {
            ++(vlSelf->__Vcoverage[261]);
        }
        ++(vlSelf->__Vcoverage[262]);
    }
    Vtb_sync_fifo___024root____VbeforeTrig_h0839b971__0(vlSelf, 
                                                        "@(posedge tb_sync_fifo.clk)");
    co_await vlSelfRef.__VtrigSched_h0839b971__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge tb_sync_fifo.clk)", 
                                                         "examples/fifo/verif/tb_sync_fifo.sv", 
                                                         70);
    if (__Vtask_tb_sync_fifo__DOT__step__3__rst) {
        ++(vlSelf->__Vcoverage[271]);
    } else {
        if (__Vtask_tb_sync_fifo__DOT__step__3__pop) {
            vlSelfRef.tb_sync_fifo__DOT__head = VL_MODDIVS_III(32, 
                                                               ((IData)(1U) 
                                                                + vlSelfRef.tb_sync_fifo__DOT__head), (IData)(8U));
            vlSelfRef.tb_sync_fifo__DOT__count = (vlSelfRef.tb_sync_fifo__DOT__count 
                                                  - (IData)(1U));
            ++(vlSelf->__Vcoverage[266]);
        } else {
            ++(vlSelf->__Vcoverage[267]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__3__push) {
            vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__tail)] 
                = __Vtask_tb_sync_fifo__DOT__step__3__data;
            vlSelfRef.tb_sync_fifo__DOT__tail = VL_MODDIVS_III(32, 
                                                               ((IData)(1U) 
                                                                + vlSelfRef.tb_sync_fifo__DOT__tail), (IData)(8U));
            vlSelfRef.tb_sync_fifo__DOT__count = ((IData)(1U) 
                                                  + vlSelfRef.tb_sync_fifo__DOT__count);
            ++(vlSelf->__Vcoverage[268]);
        } else {
            ++(vlSelf->__Vcoverage[269]);
        }
        ++(vlSelf->__Vcoverage[270]);
    }
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/fifo/verif/tb_sync_fifo.sv", 
                                         82);
    __Vtask_tb_sync_fifo__DOT__check_outputs__5__cycle_id 
        = vlSelfRef.tb_sync_fifo__DOT__checks;
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__status_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__5__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                         , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                         , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
            ++(vlSelf->__Vcoverage[207]);
        } else {
            ++(vlSelf->__Vcoverage[208]);
        }
        ++(vlSelf->__Vcoverage[209]);
    } else {
        ++(vlSelf->__Vcoverage[210]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__data_errors = 
            ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__5__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                         [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
            ++(vlSelf->__Vcoverage[214]);
        } else {
            ++(vlSelf->__Vcoverage[215]);
        }
        ++(vlSelf->__Vcoverage[216]);
    } else {
        ++(vlSelf->__Vcoverage[217]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
         != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[211]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
         != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[212]);
    }
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        ++(vlSelf->__Vcoverage[213]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        ++(vlSelf->__Vcoverage[218]);
    }
    if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
         == vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__head)])) {
        ++(vlSelf->__Vcoverage[219]);
    }
    if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
        ++(vlSelf->__Vcoverage[220]);
    }
    ++(vlSelf->__Vcoverage[221]);
    vlSelfRef.tb_sync_fifo__DOT__checks = ((IData)(1U) 
                                           + vlSelfRef.tb_sync_fifo__DOT__checks);
    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__rst)))) {
        ++(vlSelf->__Vcoverage[264]);
    }
    if (__Vtask_tb_sync_fifo__DOT__step__3__rst) {
        ++(vlSelf->__Vcoverage[265]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__3__rst)))) {
        ++(vlSelf->__Vcoverage[272]);
    }
    if (__Vtask_tb_sync_fifo__DOT__step__3__rst) {
        ++(vlSelf->__Vcoverage[273]);
    }
    ++(vlSelf->__Vcoverage[274]);
    __Vtask_tb_sync_fifo__DOT__step__6__data = 0U;
    __Vtask_tb_sync_fifo__DOT__step__6__pop = 1U;
    __Vtask_tb_sync_fifo__DOT__step__6__push = 0U;
    __Vtask_tb_sync_fifo__DOT__step__6__rst = 0U;
    __Vtask_tb_sync_fifo__DOT__step__6__old_count = 0;
    Vtb_sync_fifo___024root____VbeforeTrig_h0839a9c0__0(vlSelf, 
                                                        "@(negedge tb_sync_fifo.clk)");
    co_await vlSelfRef.__VtrigSched_h0839a9c0__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(negedge tb_sync_fifo.clk)", 
                                                         "examples/fifo/verif/tb_sync_fifo.sv", 
                                                         43);
    __Vtask_tb_sync_fifo__DOT__step__6__old_count = vlSelfRef.tb_sync_fifo__DOT__count;
    vlSelfRef.tb_sync_fifo__DOT__reset = __Vtask_tb_sync_fifo__DOT__step__6__rst;
    vlSelfRef.tb_sync_fifo__DOT__push_i = __Vtask_tb_sync_fifo__DOT__step__6__push;
    vlSelfRef.tb_sync_fifo__DOT__pop_i = __Vtask_tb_sync_fifo__DOT__step__6__pop;
    vlSelfRef.tb_sync_fifo__DOT__push_data_i = __Vtask_tb_sync_fifo__DOT__step__6__data;
    if (__Vtask_tb_sync_fifo__DOT__step__6__rst) {
        if (VL_LTS_III(32, 0U, __Vtask_tb_sync_fifo__DOT__step__6__old_count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000040U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[222]);
        } else {
            ++(vlSelf->__Vcoverage[223]);
        }
        vlSelfRef.tb_sync_fifo__DOT__head = 0U;
        vlSelfRef.tb_sync_fifo__DOT__tail = 0U;
        vlSelfRef.tb_sync_fifo__DOT__count = 0U;
        ++(vlSelf->__Vcoverage[232]);
    } else {
        if (VL_UNLIKELY(((((IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop) 
                           & (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                          | (((IData)(__Vtask_tb_sync_fifo__DOT__step__6__push) 
                              & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop))))))) {
            VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:55: Assertion failed in %m: Illegal FIFO action under frozen contract\n",3, 'M',vlSymsp->name(),"tb_sync_fifo.step", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 55, "", false);
        } else {
            ++(vlSelf->__Vcoverage[224]);
        }
        if ((((IData)(__Vtask_tb_sync_fifo__DOT__step__6__push) 
              & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop)))) {
            ++(vlSelf->__Vcoverage[225]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop) 
             & (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[226]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop))) {
            ++(vlSelf->__Vcoverage[227]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[228]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__push)))) {
            ++(vlSelf->__Vcoverage[229]);
        }
        if (((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop)) 
             & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[230]);
        }
        if ((1U & ((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop)) 
                   & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__push))))) {
            ++(vlSelf->__Vcoverage[231]);
        }
    }
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/fifo/verif/tb_sync_fifo.sv", 
                                         56);
    __Vtask_tb_sync_fifo__DOT__check_outputs__7__cycle_id 
        = vlSelfRef.tb_sync_fifo__DOT__checks;
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__status_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__7__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                         , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                         , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
            ++(vlSelf->__Vcoverage[207]);
        } else {
            ++(vlSelf->__Vcoverage[208]);
        }
        ++(vlSelf->__Vcoverage[209]);
    } else {
        ++(vlSelf->__Vcoverage[210]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__data_errors = 
            ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__7__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                         [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
            ++(vlSelf->__Vcoverage[214]);
        } else {
            ++(vlSelf->__Vcoverage[215]);
        }
        ++(vlSelf->__Vcoverage[216]);
    } else {
        ++(vlSelf->__Vcoverage[217]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
         != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[211]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
         != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[212]);
    }
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        ++(vlSelf->__Vcoverage[213]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        ++(vlSelf->__Vcoverage[218]);
    }
    if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
         == vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__head)])) {
        ++(vlSelf->__Vcoverage[219]);
    }
    if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
        ++(vlSelf->__Vcoverage[220]);
    }
    ++(vlSelf->__Vcoverage[221]);
    if (__Vtask_tb_sync_fifo__DOT__step__6__rst) {
        ++(vlSelf->__Vcoverage[263]);
    } else {
        if ((0U == vlSelfRef.tb_sync_fifo__DOT__count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (1U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[233]);
        } else {
            ++(vlSelf->__Vcoverage[234]);
        }
        if ((8U == vlSelfRef.tb_sync_fifo__DOT__count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (4U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[235]);
        } else {
            ++(vlSelf->__Vcoverage[236]);
        }
        if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
              & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__push))) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop)))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000080U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[237]);
        } else {
            ++(vlSelf->__Vcoverage[238]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__6__pop) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (2U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            if ((7U == vlSelfRef.tb_sync_fifo__DOT__head)) {
                vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                    = (0x00000020U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                ++(vlSelf->__Vcoverage[243]);
            } else {
                ++(vlSelf->__Vcoverage[244]);
            }
            if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                 & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__push)))) {
                vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                    = (0x00000100U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                ++(vlSelf->__Vcoverage[245]);
            } else {
                ++(vlSelf->__Vcoverage[246]);
            }
            if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                 & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__push)))) {
                ++(vlSelf->__Vcoverage[247]);
            }
            if (__Vtask_tb_sync_fifo__DOT__step__6__push) {
                ++(vlSelf->__Vcoverage[248]);
            }
            if ((1U != vlSelfRef.tb_sync_fifo__DOT__count)) {
                ++(vlSelf->__Vcoverage[249]);
            }
            ++(vlSelf->__Vcoverage[250]);
        } else {
            ++(vlSelf->__Vcoverage[251]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__6__push) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (8U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[252]);
        } else {
            ++(vlSelf->__Vcoverage[253]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__6__push) 
             & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000010U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[257]);
        } else {
            ++(vlSelf->__Vcoverage[258]);
        }
        if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
              & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__push))) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop)))) {
            ++(vlSelf->__Vcoverage[239]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__6__pop) {
            ++(vlSelf->__Vcoverage[240]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__6__push) {
            ++(vlSelf->__Vcoverage[241]);
        }
        if ((8U != vlSelfRef.tb_sync_fifo__DOT__count)) {
            ++(vlSelf->__Vcoverage[242]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__6__push) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop))) {
            ++(vlSelf->__Vcoverage[254]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__pop)))) {
            ++(vlSelf->__Vcoverage[255]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__push)))) {
            ++(vlSelf->__Vcoverage[256]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__6__push) 
             & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
            ++(vlSelf->__Vcoverage[259]);
        }
        if ((7U != vlSelfRef.tb_sync_fifo__DOT__tail)) {
            ++(vlSelf->__Vcoverage[260]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__push)))) {
            ++(vlSelf->__Vcoverage[261]);
        }
        ++(vlSelf->__Vcoverage[262]);
    }
    Vtb_sync_fifo___024root____VbeforeTrig_h0839b971__0(vlSelf, 
                                                        "@(posedge tb_sync_fifo.clk)");
    co_await vlSelfRef.__VtrigSched_h0839b971__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge tb_sync_fifo.clk)", 
                                                         "examples/fifo/verif/tb_sync_fifo.sv", 
                                                         70);
    if (__Vtask_tb_sync_fifo__DOT__step__6__rst) {
        ++(vlSelf->__Vcoverage[271]);
    } else {
        if (__Vtask_tb_sync_fifo__DOT__step__6__pop) {
            vlSelfRef.tb_sync_fifo__DOT__head = VL_MODDIVS_III(32, 
                                                               ((IData)(1U) 
                                                                + vlSelfRef.tb_sync_fifo__DOT__head), (IData)(8U));
            vlSelfRef.tb_sync_fifo__DOT__count = (vlSelfRef.tb_sync_fifo__DOT__count 
                                                  - (IData)(1U));
            ++(vlSelf->__Vcoverage[266]);
        } else {
            ++(vlSelf->__Vcoverage[267]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__6__push) {
            vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__tail)] 
                = __Vtask_tb_sync_fifo__DOT__step__6__data;
            vlSelfRef.tb_sync_fifo__DOT__tail = VL_MODDIVS_III(32, 
                                                               ((IData)(1U) 
                                                                + vlSelfRef.tb_sync_fifo__DOT__tail), (IData)(8U));
            vlSelfRef.tb_sync_fifo__DOT__count = ((IData)(1U) 
                                                  + vlSelfRef.tb_sync_fifo__DOT__count);
            ++(vlSelf->__Vcoverage[268]);
        } else {
            ++(vlSelf->__Vcoverage[269]);
        }
        ++(vlSelf->__Vcoverage[270]);
    }
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/fifo/verif/tb_sync_fifo.sv", 
                                         82);
    __Vtask_tb_sync_fifo__DOT__check_outputs__8__cycle_id 
        = vlSelfRef.tb_sync_fifo__DOT__checks;
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__status_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__8__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                         , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                         , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
            ++(vlSelf->__Vcoverage[207]);
        } else {
            ++(vlSelf->__Vcoverage[208]);
        }
        ++(vlSelf->__Vcoverage[209]);
    } else {
        ++(vlSelf->__Vcoverage[210]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__data_errors = 
            ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__8__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                         [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
            ++(vlSelf->__Vcoverage[214]);
        } else {
            ++(vlSelf->__Vcoverage[215]);
        }
        ++(vlSelf->__Vcoverage[216]);
    } else {
        ++(vlSelf->__Vcoverage[217]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
         != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[211]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
         != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[212]);
    }
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        ++(vlSelf->__Vcoverage[213]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        ++(vlSelf->__Vcoverage[218]);
    }
    if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
         == vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__head)])) {
        ++(vlSelf->__Vcoverage[219]);
    }
    if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
        ++(vlSelf->__Vcoverage[220]);
    }
    ++(vlSelf->__Vcoverage[221]);
    vlSelfRef.tb_sync_fifo__DOT__checks = ((IData)(1U) 
                                           + vlSelfRef.tb_sync_fifo__DOT__checks);
    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__rst)))) {
        ++(vlSelf->__Vcoverage[264]);
    }
    if (__Vtask_tb_sync_fifo__DOT__step__6__rst) {
        ++(vlSelf->__Vcoverage[265]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__6__rst)))) {
        ++(vlSelf->__Vcoverage[272]);
    }
    if (__Vtask_tb_sync_fifo__DOT__step__6__rst) {
        ++(vlSelf->__Vcoverage[273]);
    }
    ++(vlSelf->__Vcoverage[274]);
    __Vtask_tb_sync_fifo__DOT__step__9__data = 0U;
    __Vtask_tb_sync_fifo__DOT__step__9__pop = 0U;
    __Vtask_tb_sync_fifo__DOT__step__9__push = 0U;
    __Vtask_tb_sync_fifo__DOT__step__9__rst = 0U;
    __Vtask_tb_sync_fifo__DOT__step__9__old_count = 0;
    Vtb_sync_fifo___024root____VbeforeTrig_h0839a9c0__0(vlSelf, 
                                                        "@(negedge tb_sync_fifo.clk)");
    co_await vlSelfRef.__VtrigSched_h0839a9c0__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(negedge tb_sync_fifo.clk)", 
                                                         "examples/fifo/verif/tb_sync_fifo.sv", 
                                                         43);
    __Vtask_tb_sync_fifo__DOT__step__9__old_count = vlSelfRef.tb_sync_fifo__DOT__count;
    vlSelfRef.tb_sync_fifo__DOT__reset = __Vtask_tb_sync_fifo__DOT__step__9__rst;
    vlSelfRef.tb_sync_fifo__DOT__push_i = __Vtask_tb_sync_fifo__DOT__step__9__push;
    vlSelfRef.tb_sync_fifo__DOT__pop_i = __Vtask_tb_sync_fifo__DOT__step__9__pop;
    vlSelfRef.tb_sync_fifo__DOT__push_data_i = __Vtask_tb_sync_fifo__DOT__step__9__data;
    if (__Vtask_tb_sync_fifo__DOT__step__9__rst) {
        if (VL_LTS_III(32, 0U, __Vtask_tb_sync_fifo__DOT__step__9__old_count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000040U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[222]);
        } else {
            ++(vlSelf->__Vcoverage[223]);
        }
        vlSelfRef.tb_sync_fifo__DOT__head = 0U;
        vlSelfRef.tb_sync_fifo__DOT__tail = 0U;
        vlSelfRef.tb_sync_fifo__DOT__count = 0U;
        ++(vlSelf->__Vcoverage[232]);
    } else {
        if (VL_UNLIKELY(((((IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop) 
                           & (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                          | (((IData)(__Vtask_tb_sync_fifo__DOT__step__9__push) 
                              & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop))))))) {
            VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:55: Assertion failed in %m: Illegal FIFO action under frozen contract\n",3, 'M',vlSymsp->name(),"tb_sync_fifo.step", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 55, "", false);
        } else {
            ++(vlSelf->__Vcoverage[224]);
        }
        if ((((IData)(__Vtask_tb_sync_fifo__DOT__step__9__push) 
              & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop)))) {
            ++(vlSelf->__Vcoverage[225]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop) 
             & (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[226]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop))) {
            ++(vlSelf->__Vcoverage[227]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[228]);
        }
        if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__push)))) {
            ++(vlSelf->__Vcoverage[229]);
        }
        if (((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop)) 
             & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
            ++(vlSelf->__Vcoverage[230]);
        }
        if ((1U & ((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop)) 
                   & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__push))))) {
            ++(vlSelf->__Vcoverage[231]);
        }
    }
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/fifo/verif/tb_sync_fifo.sv", 
                                         56);
    __Vtask_tb_sync_fifo__DOT__check_outputs__10__cycle_id 
        = vlSelfRef.tb_sync_fifo__DOT__checks;
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__status_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__10__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                         , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                         , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
            ++(vlSelf->__Vcoverage[207]);
        } else {
            ++(vlSelf->__Vcoverage[208]);
        }
        ++(vlSelf->__Vcoverage[209]);
    } else {
        ++(vlSelf->__Vcoverage[210]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__data_errors = 
            ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__10__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                         [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
            ++(vlSelf->__Vcoverage[214]);
        } else {
            ++(vlSelf->__Vcoverage[215]);
        }
        ++(vlSelf->__Vcoverage[216]);
    } else {
        ++(vlSelf->__Vcoverage[217]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
         != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[211]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
         != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[212]);
    }
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        ++(vlSelf->__Vcoverage[213]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        ++(vlSelf->__Vcoverage[218]);
    }
    if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
         == vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__head)])) {
        ++(vlSelf->__Vcoverage[219]);
    }
    if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
        ++(vlSelf->__Vcoverage[220]);
    }
    ++(vlSelf->__Vcoverage[221]);
    if (__Vtask_tb_sync_fifo__DOT__step__9__rst) {
        ++(vlSelf->__Vcoverage[263]);
    } else {
        if ((0U == vlSelfRef.tb_sync_fifo__DOT__count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (1U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[233]);
        } else {
            ++(vlSelf->__Vcoverage[234]);
        }
        if ((8U == vlSelfRef.tb_sync_fifo__DOT__count)) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (4U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[235]);
        } else {
            ++(vlSelf->__Vcoverage[236]);
        }
        if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
              & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__push))) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop)))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000080U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[237]);
        } else {
            ++(vlSelf->__Vcoverage[238]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__9__pop) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (2U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            if ((7U == vlSelfRef.tb_sync_fifo__DOT__head)) {
                vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                    = (0x00000020U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                ++(vlSelf->__Vcoverage[243]);
            } else {
                ++(vlSelf->__Vcoverage[244]);
            }
            if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                 & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__push)))) {
                vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                    = (0x00000100U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                ++(vlSelf->__Vcoverage[245]);
            } else {
                ++(vlSelf->__Vcoverage[246]);
            }
            if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                 & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__push)))) {
                ++(vlSelf->__Vcoverage[247]);
            }
            if (__Vtask_tb_sync_fifo__DOT__step__9__push) {
                ++(vlSelf->__Vcoverage[248]);
            }
            if ((1U != vlSelfRef.tb_sync_fifo__DOT__count)) {
                ++(vlSelf->__Vcoverage[249]);
            }
            ++(vlSelf->__Vcoverage[250]);
        } else {
            ++(vlSelf->__Vcoverage[251]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__9__push) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (8U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[252]);
        } else {
            ++(vlSelf->__Vcoverage[253]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__9__push) 
             & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                = (0x00000010U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
            ++(vlSelf->__Vcoverage[257]);
        } else {
            ++(vlSelf->__Vcoverage[258]);
        }
        if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
              & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__push))) 
             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop)))) {
            ++(vlSelf->__Vcoverage[239]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__9__pop) {
            ++(vlSelf->__Vcoverage[240]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__9__push) {
            ++(vlSelf->__Vcoverage[241]);
        }
        if ((8U != vlSelfRef.tb_sync_fifo__DOT__count)) {
            ++(vlSelf->__Vcoverage[242]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__9__push) 
             & (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop))) {
            ++(vlSelf->__Vcoverage[254]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__pop)))) {
            ++(vlSelf->__Vcoverage[255]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__push)))) {
            ++(vlSelf->__Vcoverage[256]);
        }
        if (((IData)(__Vtask_tb_sync_fifo__DOT__step__9__push) 
             & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
            ++(vlSelf->__Vcoverage[259]);
        }
        if ((7U != vlSelfRef.tb_sync_fifo__DOT__tail)) {
            ++(vlSelf->__Vcoverage[260]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__push)))) {
            ++(vlSelf->__Vcoverage[261]);
        }
        ++(vlSelf->__Vcoverage[262]);
    }
    Vtb_sync_fifo___024root____VbeforeTrig_h0839b971__0(vlSelf, 
                                                        "@(posedge tb_sync_fifo.clk)");
    co_await vlSelfRef.__VtrigSched_h0839b971__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge tb_sync_fifo.clk)", 
                                                         "examples/fifo/verif/tb_sync_fifo.sv", 
                                                         70);
    if (__Vtask_tb_sync_fifo__DOT__step__9__rst) {
        ++(vlSelf->__Vcoverage[271]);
    } else {
        if (__Vtask_tb_sync_fifo__DOT__step__9__pop) {
            vlSelfRef.tb_sync_fifo__DOT__head = VL_MODDIVS_III(32, 
                                                               ((IData)(1U) 
                                                                + vlSelfRef.tb_sync_fifo__DOT__head), (IData)(8U));
            vlSelfRef.tb_sync_fifo__DOT__count = (vlSelfRef.tb_sync_fifo__DOT__count 
                                                  - (IData)(1U));
            ++(vlSelf->__Vcoverage[266]);
        } else {
            ++(vlSelf->__Vcoverage[267]);
        }
        if (__Vtask_tb_sync_fifo__DOT__step__9__push) {
            vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__tail)] 
                = __Vtask_tb_sync_fifo__DOT__step__9__data;
            vlSelfRef.tb_sync_fifo__DOT__tail = VL_MODDIVS_III(32, 
                                                               ((IData)(1U) 
                                                                + vlSelfRef.tb_sync_fifo__DOT__tail), (IData)(8U));
            vlSelfRef.tb_sync_fifo__DOT__count = ((IData)(1U) 
                                                  + vlSelfRef.tb_sync_fifo__DOT__count);
            ++(vlSelf->__Vcoverage[268]);
        } else {
            ++(vlSelf->__Vcoverage[269]);
        }
        ++(vlSelf->__Vcoverage[270]);
    }
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/fifo/verif/tb_sync_fifo.sv", 
                                         82);
    __Vtask_tb_sync_fifo__DOT__check_outputs__11__cycle_id 
        = vlSelfRef.tb_sync_fifo__DOT__checks;
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__status_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__11__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                         , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                         , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
            ++(vlSelf->__Vcoverage[207]);
        } else {
            ++(vlSelf->__Vcoverage[208]);
        }
        ++(vlSelf->__Vcoverage[209]);
    } else {
        ++(vlSelf->__Vcoverage[210]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        vlSelfRef.tb_sync_fifo__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
        vlSelfRef.tb_sync_fifo__DOT__data_errors = 
            ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
            VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                         , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__11__cycle_id
                         , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                         , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                         [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
            ++(vlSelf->__Vcoverage[214]);
        } else {
            ++(vlSelf->__Vcoverage[215]);
        }
        ++(vlSelf->__Vcoverage[216]);
    } else {
        ++(vlSelf->__Vcoverage[217]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
         != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[211]);
    }
    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
         != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
        ++(vlSelf->__Vcoverage[212]);
    }
    if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
          == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
         & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
            == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
        ++(vlSelf->__Vcoverage[213]);
    }
    if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
         & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
            [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
            != vlSelfRef.tb_sync_fifo__DOT__expected
            [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
        ++(vlSelf->__Vcoverage[218]);
    }
    if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
         [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
         == vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                   & vlSelfRef.tb_sync_fifo__DOT__head)])) {
        ++(vlSelf->__Vcoverage[219]);
    }
    if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
        ++(vlSelf->__Vcoverage[220]);
    }
    ++(vlSelf->__Vcoverage[221]);
    vlSelfRef.tb_sync_fifo__DOT__checks = ((IData)(1U) 
                                           + vlSelfRef.tb_sync_fifo__DOT__checks);
    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__rst)))) {
        ++(vlSelf->__Vcoverage[264]);
    }
    if (__Vtask_tb_sync_fifo__DOT__step__9__rst) {
        ++(vlSelf->__Vcoverage[265]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__9__rst)))) {
        ++(vlSelf->__Vcoverage[272]);
    }
    if (__Vtask_tb_sync_fifo__DOT__step__9__rst) {
        ++(vlSelf->__Vcoverage[273]);
    }
    ++(vlSelf->__Vcoverage[274]);
    if (VL_UNLIKELY(((1U == vlSelfRef.tb_sync_fifo__DOT__mode)))) {
        vlSelfRef.tb_sync_fifo__DOT____VlemExpr_1 = VL_VALUEPLUSARGS_INW(1024, "VECTORS=%s"s, 
                                                                         vlSelfRef.tb_sync_fifo__DOT__vector_path);
        if (VL_LIKELY((vlSelfRef.tb_sync_fifo__DOT____VlemExpr_1))) {
            ++(vlSelf->__Vcoverage[277]);
        } else {
            VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:96: Assertion failed in %m: MODE=1 requires +VECTORS=<file>\n",3, 'M',vlSymsp->name(),"tb_sync_fifo", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 96, "", false);
        }
        vlSelfRef.tb_sync_fifo__DOT__vector_file = VL_FOPEN_NN(
                                                               VL_CVT_PACK_STR_NW(32, vlSelfRef.tb_sync_fifo__DOT__vector_path)
                                                               , "r"s);
        ;
        if (VL_UNLIKELY(((0U == vlSelfRef.tb_sync_fifo__DOT__vector_file)))) {
            VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:98: Assertion failed in %m: Cannot open stimulus file\n",3, 'M',vlSymsp->name(),"tb_sync_fifo", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 98, "", false);
        } else {
            ++(vlSelf->__Vcoverage[278]);
        }
        while (true) {
            vlSelfRef.tb_sync_fifo__DOT____VExpr_h16e95b7f__0 
                = (vlSelfRef.tb_sync_fifo__DOT__vector_file ? feof(VL_CVT_I_FP(vlSelfRef.tb_sync_fifo__DOT__vector_file)) : true);
            if (!((! vlSelfRef.tb_sync_fifo__DOT____VExpr_h16e95b7f__0))) break;
            vlSelfRef.tb_sync_fifo__DOT__scan_status 
                = VL_FSCANF_INX(vlSelfRef.tb_sync_fifo__DOT__vector_file,"%d %d %d %h\n",4
                                , '#',32,&(vlSelfRef.tb_sync_fifo__DOT__vector_reset)
                                , '#',32,&(vlSelfRef.tb_sync_fifo__DOT__vector_push)
                                , '#',32,&(vlSelfRef.tb_sync_fifo__DOT__vector_pop)
                                , '#',32,&(vlSelfRef.tb_sync_fifo__DOT__vector_data)) ;
            if ((4U == vlSelfRef.tb_sync_fifo__DOT__scan_status)) {
                __Vtask_tb_sync_fifo__DOT__step__12__data 
                    = (0x000000ffU & vlSelfRef.tb_sync_fifo__DOT__vector_data);
                __Vtask_tb_sync_fifo__DOT__step__12__pop 
                    = (1U & vlSelfRef.tb_sync_fifo__DOT__vector_pop);
                __Vtask_tb_sync_fifo__DOT__step__12__push 
                    = (1U & vlSelfRef.tb_sync_fifo__DOT__vector_push);
                __Vtask_tb_sync_fifo__DOT__step__12__rst 
                    = (1U & vlSelfRef.tb_sync_fifo__DOT__vector_reset);
                __Vtask_tb_sync_fifo__DOT__step__12__old_count = 0;
                Vtb_sync_fifo___024root____VbeforeTrig_h0839a9c0__0(vlSelf, 
                                                                    "@(negedge tb_sync_fifo.clk)");
                co_await vlSelfRef.__VtrigSched_h0839a9c0__0.trigger(0U, 
                                                                     nullptr, 
                                                                     "@(negedge tb_sync_fifo.clk)", 
                                                                     "examples/fifo/verif/tb_sync_fifo.sv", 
                                                                     43);
                __Vtask_tb_sync_fifo__DOT__step__12__old_count 
                    = vlSelfRef.tb_sync_fifo__DOT__count;
                vlSelfRef.tb_sync_fifo__DOT__reset 
                    = __Vtask_tb_sync_fifo__DOT__step__12__rst;
                vlSelfRef.tb_sync_fifo__DOT__push_i 
                    = __Vtask_tb_sync_fifo__DOT__step__12__push;
                vlSelfRef.tb_sync_fifo__DOT__pop_i 
                    = __Vtask_tb_sync_fifo__DOT__step__12__pop;
                vlSelfRef.tb_sync_fifo__DOT__push_data_i 
                    = __Vtask_tb_sync_fifo__DOT__step__12__data;
                if (__Vtask_tb_sync_fifo__DOT__step__12__rst) {
                    if (VL_LTS_III(32, 0U, __Vtask_tb_sync_fifo__DOT__step__12__old_count)) {
                        vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                            = (0x00000040U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                        ++(vlSelf->__Vcoverage[222]);
                    } else {
                        ++(vlSelf->__Vcoverage[223]);
                    }
                    vlSelfRef.tb_sync_fifo__DOT__head = 0U;
                    vlSelfRef.tb_sync_fifo__DOT__tail = 0U;
                    vlSelfRef.tb_sync_fifo__DOT__count = 0U;
                    ++(vlSelf->__Vcoverage[232]);
                } else {
                    if (VL_UNLIKELY(((((IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop) 
                                       & (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                                      | (((IData)(__Vtask_tb_sync_fifo__DOT__step__12__push) 
                                          & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                                         & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop))))))) {
                        VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:55: Assertion failed in %m: Illegal FIFO action under frozen contract\n",3, 'M',vlSymsp->name(),"tb_sync_fifo.step", 'T',-9
                                     , '#',64,VL_TIME_UNITED_Q(1000));
                        VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 55, "", false);
                    } else {
                        ++(vlSelf->__Vcoverage[224]);
                    }
                    if ((((IData)(__Vtask_tb_sync_fifo__DOT__step__12__push) 
                          & (8U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                         & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop)))) {
                        ++(vlSelf->__Vcoverage[225]);
                    }
                    if (((IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop) 
                         & (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
                        ++(vlSelf->__Vcoverage[226]);
                    }
                    if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
                         & (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop))) {
                        ++(vlSelf->__Vcoverage[227]);
                    }
                    if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
                         & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
                        ++(vlSelf->__Vcoverage[228]);
                    }
                    if (((0U != vlSelfRef.tb_sync_fifo__DOT__count) 
                         & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__push)))) {
                        ++(vlSelf->__Vcoverage[229]);
                    }
                    if (((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop)) 
                         & (8U != vlSelfRef.tb_sync_fifo__DOT__count))) {
                        ++(vlSelf->__Vcoverage[230]);
                    }
                    if ((1U & ((~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop)) 
                               & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__push))))) {
                        ++(vlSelf->__Vcoverage[231]);
                    }
                }
                co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                     nullptr, 
                                                     "examples/fifo/verif/tb_sync_fifo.sv", 
                                                     56);
                __Vtask_tb_sync_fifo__DOT__check_outputs__13__cycle_id 
                    = vlSelfRef.tb_sync_fifo__DOT__checks;
                if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
                      != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                     | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
                        != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
                    vlSelfRef.tb_sync_fifo__DOT__functional_errors 
                        = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
                    vlSelfRef.tb_sync_fifo__DOT__status_errors 
                        = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
                    if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
                        VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                                     , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__13__cycle_id
                                     , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                                     , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                                     , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
                        ++(vlSelf->__Vcoverage[207]);
                    } else {
                        ++(vlSelf->__Vcoverage[208]);
                    }
                    ++(vlSelf->__Vcoverage[209]);
                } else {
                    ++(vlSelf->__Vcoverage[210]);
                }
                if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
                     & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                        [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
                        != vlSelfRef.tb_sync_fifo__DOT__expected
                        [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
                    vlSelfRef.tb_sync_fifo__DOT__functional_errors 
                        = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
                    vlSelfRef.tb_sync_fifo__DOT__data_errors 
                        = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
                    if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
                        VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                                     , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__13__cycle_id
                                     , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                                     , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                                     [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                                     , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                                     [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
                        ++(vlSelf->__Vcoverage[214]);
                    } else {
                        ++(vlSelf->__Vcoverage[215]);
                    }
                    ++(vlSelf->__Vcoverage[216]);
                } else {
                    ++(vlSelf->__Vcoverage[217]);
                }
                if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
                     != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
                    ++(vlSelf->__Vcoverage[211]);
                }
                if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
                     != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
                    ++(vlSelf->__Vcoverage[212]);
                }
                if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
                      == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                     & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
                        == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
                    ++(vlSelf->__Vcoverage[213]);
                }
                if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
                     & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                        [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
                        != vlSelfRef.tb_sync_fifo__DOT__expected
                        [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
                    ++(vlSelf->__Vcoverage[218]);
                }
                if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                     [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
                     == vlSelfRef.tb_sync_fifo__DOT__expected
                     [(7U & vlSelfRef.tb_sync_fifo__DOT__head)])) {
                    ++(vlSelf->__Vcoverage[219]);
                }
                if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
                    ++(vlSelf->__Vcoverage[220]);
                }
                ++(vlSelf->__Vcoverage[221]);
                if (__Vtask_tb_sync_fifo__DOT__step__12__rst) {
                    ++(vlSelf->__Vcoverage[263]);
                } else {
                    if ((0U == vlSelfRef.tb_sync_fifo__DOT__count)) {
                        vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                            = (1U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                        ++(vlSelf->__Vcoverage[233]);
                    } else {
                        ++(vlSelf->__Vcoverage[234]);
                    }
                    if ((8U == vlSelfRef.tb_sync_fifo__DOT__count)) {
                        vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                            = (4U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                        ++(vlSelf->__Vcoverage[235]);
                    } else {
                        ++(vlSelf->__Vcoverage[236]);
                    }
                    if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
                          & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__push))) 
                         & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop)))) {
                        vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                            = (0x00000080U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                        ++(vlSelf->__Vcoverage[237]);
                    } else {
                        ++(vlSelf->__Vcoverage[238]);
                    }
                    if (__Vtask_tb_sync_fifo__DOT__step__12__pop) {
                        vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                            = (2U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                        if ((7U == vlSelfRef.tb_sync_fifo__DOT__head)) {
                            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                                = (0x00000020U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                            ++(vlSelf->__Vcoverage[243]);
                        } else {
                            ++(vlSelf->__Vcoverage[244]);
                        }
                        if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__push)))) {
                            vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                                = (0x00000100U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                            ++(vlSelf->__Vcoverage[245]);
                        } else {
                            ++(vlSelf->__Vcoverage[246]);
                        }
                        if (((1U == vlSelfRef.tb_sync_fifo__DOT__count) 
                             & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__push)))) {
                            ++(vlSelf->__Vcoverage[247]);
                        }
                        if (__Vtask_tb_sync_fifo__DOT__step__12__push) {
                            ++(vlSelf->__Vcoverage[248]);
                        }
                        if ((1U != vlSelfRef.tb_sync_fifo__DOT__count)) {
                            ++(vlSelf->__Vcoverage[249]);
                        }
                        ++(vlSelf->__Vcoverage[250]);
                    } else {
                        ++(vlSelf->__Vcoverage[251]);
                    }
                    if (((IData)(__Vtask_tb_sync_fifo__DOT__step__12__push) 
                         & (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop))) {
                        vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                            = (8U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                        ++(vlSelf->__Vcoverage[252]);
                    } else {
                        ++(vlSelf->__Vcoverage[253]);
                    }
                    if (((IData)(__Vtask_tb_sync_fifo__DOT__step__12__push) 
                         & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
                        vlSelfRef.tb_sync_fifo__DOT__functional_bins 
                            = (0x00000010U | (IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
                        ++(vlSelf->__Vcoverage[257]);
                    } else {
                        ++(vlSelf->__Vcoverage[258]);
                    }
                    if ((((8U == vlSelfRef.tb_sync_fifo__DOT__count) 
                          & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__push))) 
                         & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop)))) {
                        ++(vlSelf->__Vcoverage[239]);
                    }
                    if (__Vtask_tb_sync_fifo__DOT__step__12__pop) {
                        ++(vlSelf->__Vcoverage[240]);
                    }
                    if (__Vtask_tb_sync_fifo__DOT__step__12__push) {
                        ++(vlSelf->__Vcoverage[241]);
                    }
                    if ((8U != vlSelfRef.tb_sync_fifo__DOT__count)) {
                        ++(vlSelf->__Vcoverage[242]);
                    }
                    if (((IData)(__Vtask_tb_sync_fifo__DOT__step__12__push) 
                         & (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop))) {
                        ++(vlSelf->__Vcoverage[254]);
                    }
                    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__pop)))) {
                        ++(vlSelf->__Vcoverage[255]);
                    }
                    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__push)))) {
                        ++(vlSelf->__Vcoverage[256]);
                    }
                    if (((IData)(__Vtask_tb_sync_fifo__DOT__step__12__push) 
                         & (7U == vlSelfRef.tb_sync_fifo__DOT__tail))) {
                        ++(vlSelf->__Vcoverage[259]);
                    }
                    if ((7U != vlSelfRef.tb_sync_fifo__DOT__tail)) {
                        ++(vlSelf->__Vcoverage[260]);
                    }
                    if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__push)))) {
                        ++(vlSelf->__Vcoverage[261]);
                    }
                    ++(vlSelf->__Vcoverage[262]);
                }
                Vtb_sync_fifo___024root____VbeforeTrig_h0839b971__0(vlSelf, 
                                                                    "@(posedge tb_sync_fifo.clk)");
                co_await vlSelfRef.__VtrigSched_h0839b971__0.trigger(0U, 
                                                                     nullptr, 
                                                                     "@(posedge tb_sync_fifo.clk)", 
                                                                     "examples/fifo/verif/tb_sync_fifo.sv", 
                                                                     70);
                if (__Vtask_tb_sync_fifo__DOT__step__12__rst) {
                    ++(vlSelf->__Vcoverage[271]);
                } else {
                    if (__Vtask_tb_sync_fifo__DOT__step__12__pop) {
                        vlSelfRef.tb_sync_fifo__DOT__head 
                            = VL_MODDIVS_III(32, ((IData)(1U) 
                                                  + vlSelfRef.tb_sync_fifo__DOT__head), (IData)(8U));
                        vlSelfRef.tb_sync_fifo__DOT__count 
                            = (vlSelfRef.tb_sync_fifo__DOT__count 
                               - (IData)(1U));
                        ++(vlSelf->__Vcoverage[266]);
                    } else {
                        ++(vlSelf->__Vcoverage[267]);
                    }
                    if (__Vtask_tb_sync_fifo__DOT__step__12__push) {
                        vlSelfRef.tb_sync_fifo__DOT__expected[(7U 
                                                               & vlSelfRef.tb_sync_fifo__DOT__tail)] 
                            = __Vtask_tb_sync_fifo__DOT__step__12__data;
                        vlSelfRef.tb_sync_fifo__DOT__tail 
                            = VL_MODDIVS_III(32, ((IData)(1U) 
                                                  + vlSelfRef.tb_sync_fifo__DOT__tail), (IData)(8U));
                        vlSelfRef.tb_sync_fifo__DOT__count 
                            = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__count);
                        ++(vlSelf->__Vcoverage[268]);
                    } else {
                        ++(vlSelf->__Vcoverage[269]);
                    }
                    ++(vlSelf->__Vcoverage[270]);
                }
                co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                     nullptr, 
                                                     "examples/fifo/verif/tb_sync_fifo.sv", 
                                                     82);
                __Vtask_tb_sync_fifo__DOT__check_outputs__14__cycle_id 
                    = vlSelfRef.tb_sync_fifo__DOT__checks;
                if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
                      != (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                     | ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
                        != (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
                    vlSelfRef.tb_sync_fifo__DOT__functional_errors 
                        = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
                    vlSelfRef.tb_sync_fifo__DOT__status_errors 
                        = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__status_errors);
                    if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
                        VL_WRITEF_NX("STATUS_FAIL cycle=%0d count=%0d full=%b empty=%b\n",4
                                     , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__14__cycle_id
                                     , '~',32,vlSelfRef.tb_sync_fifo__DOT__count
                                     , '#',1,(IData)(vlSelfRef.tb_sync_fifo__DOT__full_o)
                                     , '#',1,vlSelfRef.tb_sync_fifo__DOT__empty_o);
                        ++(vlSelf->__Vcoverage[207]);
                    } else {
                        ++(vlSelf->__Vcoverage[208]);
                    }
                    ++(vlSelf->__Vcoverage[209]);
                } else {
                    ++(vlSelf->__Vcoverage[210]);
                }
                if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
                     & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                        [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
                        != vlSelfRef.tb_sync_fifo__DOT__expected
                        [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
                    vlSelfRef.tb_sync_fifo__DOT__functional_errors 
                        = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__functional_errors);
                    vlSelfRef.tb_sync_fifo__DOT__data_errors 
                        = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__data_errors);
                    if (VL_UNLIKELY((VL_GTES_III(32, 5U, vlSelfRef.tb_sync_fifo__DOT__functional_errors)))) {
                        VL_WRITEF_NX("DATA_FAIL cycle=%0d head=%0d got=%h expected=%h\n",4
                                     , '~',32,__Vtask_tb_sync_fifo__DOT__check_outputs__14__cycle_id
                                     , '~',32,vlSelfRef.tb_sync_fifo__DOT__head
                                     , '#',8,vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                                     [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))]
                                     , '#',8,vlSelfRef.tb_sync_fifo__DOT__expected
                                     [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]);
                        ++(vlSelf->__Vcoverage[214]);
                    } else {
                        ++(vlSelf->__Vcoverage[215]);
                    }
                    ++(vlSelf->__Vcoverage[216]);
                } else {
                    ++(vlSelf->__Vcoverage[217]);
                }
                if (((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
                     != (8U == vlSelfRef.tb_sync_fifo__DOT__count))) {
                    ++(vlSelf->__Vcoverage[211]);
                }
                if (((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
                     != (0U == vlSelfRef.tb_sync_fifo__DOT__count))) {
                    ++(vlSelf->__Vcoverage[212]);
                }
                if ((((IData)(vlSelfRef.tb_sync_fifo__DOT__empty_o) 
                      == (0U == vlSelfRef.tb_sync_fifo__DOT__count)) 
                     & ((IData)(vlSelfRef.tb_sync_fifo__DOT__full_o) 
                        == (8U == vlSelfRef.tb_sync_fifo__DOT__count)))) {
                    ++(vlSelf->__Vcoverage[213]);
                }
                if ((VL_LTS_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count) 
                     & (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                        [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
                        != vlSelfRef.tb_sync_fifo__DOT__expected
                        [(7U & vlSelfRef.tb_sync_fifo__DOT__head)]))) {
                    ++(vlSelf->__Vcoverage[218]);
                }
                if ((vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                     [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
                     == vlSelfRef.tb_sync_fifo__DOT__expected
                     [(7U & vlSelfRef.tb_sync_fifo__DOT__head)])) {
                    ++(vlSelf->__Vcoverage[219]);
                }
                if (VL_GTES_III(32, 0U, vlSelfRef.tb_sync_fifo__DOT__count)) {
                    ++(vlSelf->__Vcoverage[220]);
                }
                ++(vlSelf->__Vcoverage[221]);
                vlSelfRef.tb_sync_fifo__DOT__checks 
                    = ((IData)(1U) + vlSelfRef.tb_sync_fifo__DOT__checks);
                if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__rst)))) {
                    ++(vlSelf->__Vcoverage[264]);
                }
                if (__Vtask_tb_sync_fifo__DOT__step__12__rst) {
                    ++(vlSelf->__Vcoverage[265]);
                }
                if ((1U & (~ (IData)(__Vtask_tb_sync_fifo__DOT__step__12__rst)))) {
                    ++(vlSelf->__Vcoverage[272]);
                }
                if (__Vtask_tb_sync_fifo__DOT__step__12__rst) {
                    ++(vlSelf->__Vcoverage[273]);
                }
                ++(vlSelf->__Vcoverage[274]);
                ++(vlSelf->__Vcoverage[284]);
            } else {
                vlSelfRef.tb_sync_fifo__DOT____VExpr_h16e95b7f__1 
                    = (vlSelfRef.tb_sync_fifo__DOT__vector_file ? feof(VL_CVT_I_FP(vlSelfRef.tb_sync_fifo__DOT__vector_file)) : true);
                if (VL_LIKELY((vlSelfRef.tb_sync_fifo__DOT____VExpr_h16e95b7f__1))) {
                    ++(vlSelf->__Vcoverage[281]);
                } else {
                    VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:104: Assertion failed in %m: Malformed stimulus row\n",3, 'M',vlSymsp->name(),"tb_sync_fifo", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000));
                    VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 104, "", false);
                }
                if ((! vlSelfRef.tb_sync_fifo__DOT____VExpr_h16e95b7f__1)) {
                    ++(vlSelf->__Vcoverage[282]);
                }
                if (vlSelfRef.tb_sync_fifo__DOT____VExpr_h16e95b7f__1) {
                    ++(vlSelf->__Vcoverage[283]);
                }
            }
            if ((! vlSelfRef.tb_sync_fifo__DOT____VExpr_h16e95b7f__0)) {
                ++(vlSelf->__Vcoverage[279]);
            }
            if (vlSelfRef.tb_sync_fifo__DOT____VExpr_h16e95b7f__0) {
                ++(vlSelf->__Vcoverage[280]);
            }
            ++(vlSelf->__Vcoverage[285]);
        }
        VL_FCLOSE_I(vlSelfRef.tb_sync_fifo__DOT__vector_file); ++(vlSelf->__Vcoverage[287]);
    } else if (VL_UNLIKELY(((0U != vlSelfRef.tb_sync_fifo__DOT__mode)))) {
        VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:107: Assertion failed in %m: Unknown MODE\n",3, 'M',vlSymsp->name(),"tb_sync_fifo", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000));
        VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 107, "", false);
    } else {
        ++(vlSelf->__Vcoverage[286]);
    }
    VL_WRITEF_NX("RESULT checks=%0d functional_errors=%0d status_errors=%0d data_errors=%0d bins=%h\n",5
                 , '~',32,vlSelfRef.tb_sync_fifo__DOT__checks
                 , '~',32,vlSelfRef.tb_sync_fifo__DOT__functional_errors
                 , '~',32,vlSelfRef.tb_sync_fifo__DOT__status_errors
                 , '~',32,vlSelfRef.tb_sync_fifo__DOT__data_errors
                 , '#',9,(IData)(vlSelfRef.tb_sync_fifo__DOT__functional_bins));
    if (VL_UNLIKELY((((0U != vlSelfRef.tb_sync_fifo__DOT__functional_errors) 
                      & (! VL_TESTPLUSARGS_I("COLLECT"s)))))) {
        VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:110: Assertion failed in %m: FIFO contract violation detected\n",3, 'M',vlSymsp->name(),"tb_sync_fifo", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000));
        VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 110, "", false);
    } else {
        ++(vlSelf->__Vcoverage[288]);
    }
    VL_FINISH_MT("examples/fifo/verif/tb_sync_fifo.sv", 111, "");
    ++(vlSelf->__Vcoverage[289]);
    co_return;
}

VlCoroutine Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__1(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__1\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    co_await vlSelfRef.__VdlySched.delay(0x000000003b9aca00ULL, 
                                         nullptr, "examples/fifo/verif/tb_sync_fifo.sv", 
                                         114);
    VL_WRITEF_NX("[%0t] %%Fatal: tb_sync_fifo.sv:115: Assertion failed in %m: Watchdog timeout\n",3, 'M',vlSymsp->name(),"tb_sync_fifo", 'T',-9
                 , '#',64,VL_TIME_UNITED_Q(1000));
    VL_STOP_MT("examples/fifo/verif/tb_sync_fifo.sv", 115, "", false);
    co_return;
}

VlCoroutine Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__2(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_initial__TOP__Vtiming__2\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    while (VL_LIKELY(!vlSymsp->_vm_contextp__->gotFinish())) {
        co_await vlSelfRef.__VdlySched.delay(0x0000000000001388ULL, 
                                             nullptr, 
                                             "examples/fifo/verif/tb_sync_fifo.sv", 
                                             21);
        vlSelfRef.tb_sync_fifo__DOT__clk = (1U & (~ (IData)(vlSelfRef.tb_sync_fifo__DOT__clk)));
        if ((1U & (~ (IData)(vlSelfRef.tb_sync_fifo__DOT__clk)))) {
            ++(vlSelf->__Vcoverage[204]);
        }
        if (vlSelfRef.tb_sync_fifo__DOT__clk) {
            ++(vlSelf->__Vcoverage[205]);
        }
        ++(vlSelf->__Vcoverage[206]);
    }
    co_return;
}

bool Vtb_sync_fifo___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___trigger_anySet__act\n"); );
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

void Vtb_sync_fifo___024root___act_comb__TOP__0(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___act_comb__TOP__0\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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

void Vtb_sync_fifo___024root___nba_sequent__TOP__0(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___nba_sequent__TOP__0\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*7:0*/ __VdlyVal__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0;
    __VdlyVal__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0 = 0;
    CData/*2:0*/ __VdlyDim0__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0;
    __VdlyDim0__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0 = 0;
    CData/*0:0*/ __VdlySet__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0;
    __VdlySet__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0 = 0;
    // Body
    __VdlySet__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0 = 0U;
    if (vlSelfRef.tb_sync_fifo__DOT__push_i) {
        ++(vlSelf->__Vcoverage[458]);
        __VdlyVal__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0 
            = vlSelfRef.tb_sync_fifo__DOT__push_data_i;
        __VdlyDim0__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0 
            = (7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q));
        __VdlySet__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0 = 1U;
    } else {
        ++(vlSelf->__Vcoverage[459]);
    }
    ++(vlSelf->__Vcoverage[460]);
    if (__VdlySet__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0) {
        vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem[__VdlyDim0__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0] 
            = __VdlyVal__tb_sync_fifo__DOT__dut__DOT__fifo_mem__v0;
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
}

void Vtb_sync_fifo___024root___nba_comb__TOP__0(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___nba_comb__TOP__0\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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
}

void Vtb_sync_fifo___024root___eval_nba(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_nba\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vtb_sync_fifo___024root___nba_sequent__TOP__0(vlSelf);
    }
    if ((8ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _act_sequent__TOP__0
            if (((IData)(vlSelfRef.tb_sync_fifo__DOT__clk) 
                 ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__clk))) {
                VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 0, vlSelfRef.tb_sync_fifo__DOT__clk, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__clk);
                vlSelfRef.tb_sync_fifo__DOT____Vtogcov__clk 
                    = vlSelfRef.tb_sync_fifo__DOT__clk;
            }
        }
    }
    if ((0x000000000000000dULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vtb_sync_fifo___024root___nba_comb__TOP__0(vlSelf);
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__2
            if (vlSelfRef.tb_sync_fifo__DOT__reset) {
                ++(vlSelf->__Vcoverage[450]);
                vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q = 0U;
                vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q = 0U;
            } else {
                ++(vlSelf->__Vcoverage[451]);
                vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q 
                    = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_rd_ptr;
                vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q 
                    = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__nxt_wr_ptr;
            }
            ++(vlSelf->__Vcoverage[452]);
            if ((0U != ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q) 
                        ^ (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__wr_ptr_q)))) {
                VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 306, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q, vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__wr_ptr_q);
                vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__wr_ptr_q 
                    = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q;
            }
            if ((((1U & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q) 
                         >> 3U)) != (1U & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q) 
                                           >> 3U))) 
                 & ((7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q)) 
                    == (7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))))) {
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
            if ((0U != ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q) 
                        ^ (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__rd_ptr_q)))) {
                VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 290, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q, vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__rd_ptr_q);
                vlSelfRef.tb_sync_fifo__DOT__dut__DOT____Vtogcov__rd_ptr_q 
                    = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q;
            }
            vlSelfRef.tb_sync_fifo__DOT__full_o = (
                                                   ((1U 
                                                     & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q) 
                                                        >> 3U)) 
                                                    != 
                                                    (1U 
                                                     & ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q) 
                                                        >> 3U))) 
                                                   & ((7U 
                                                       & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q)) 
                                                      == 
                                                      (7U 
                                                       & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q))));
            vlSelfRef.tb_sync_fifo__DOT__empty_o = 
                ((IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q) 
                 == (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__wr_ptr_q));
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
        }
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_comb__TOP__1
            if ((0U != (vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                        [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))] 
                        ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__pop_data_o)))) {
                VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 29, vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                                       [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))], vlSelfRef.tb_sync_fifo__DOT____Vtogcov__pop_data_o);
                vlSelfRef.tb_sync_fifo__DOT____Vtogcov__pop_data_o 
                    = vlSelfRef.tb_sync_fifo__DOT__dut__DOT__fifo_mem
                    [(7U & (IData)(vlSelfRef.tb_sync_fifo__DOT__dut__DOT__rd_ptr_q))];
            }
        }
    }
    if ((0x000000000000000fULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_comb__TOP__2
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
    }
}

void Vtb_sync_fifo___024root___timing_ready(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___timing_ready\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((4ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready("@(negedge tb_sync_fifo.clk)");
    }
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VtrigSched_h0839b971__0.ready("@(posedge tb_sync_fifo.clk)");
    }
}

void Vtb_sync_fifo___024root___timing_resume(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___timing_resume\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VtrigSched_h0839a9c0__0.moveToResumeQueue(
                                                          "@(negedge tb_sync_fifo.clk)");
    vlSelfRef.__VtrigSched_h0839b971__0.moveToResumeQueue(
                                                          "@(posedge tb_sync_fifo.clk)");
    vlSelfRef.__VtrigSched_h0839a9c0__0.resume("@(negedge tb_sync_fifo.clk)");
    vlSelfRef.__VtrigSched_h0839b971__0.resume("@(posedge tb_sync_fifo.clk)");
    if ((8ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VdlySched.resume();
    }
}

void Vtb_sync_fifo___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((0U >= n));
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtb_sync_fifo___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vtb_sync_fifo___024root___eval_phase__act(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_phase__act\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VactExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        (((vlSelfRef.__VdlySched.awaitingCurrentTime() 
                                                           << 3U) 
                                                          | (((~ (IData)(vlSelfRef.tb_sync_fifo__DOT__clk)) 
                                                              & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0)) 
                                                             << 2U)) 
                                                         | ((((IData)(vlSelfRef.tb_sync_fifo__DOT__reset) 
                                                              & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__reset__0))) 
                                                             << 1U) 
                                                            | ((IData)(vlSelfRef.tb_sync_fifo__DOT__clk) 
                                                               & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0)))))));
        vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0 
            = vlSelfRef.tb_sync_fifo__DOT__clk;
        vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__reset__0 
            = vlSelfRef.tb_sync_fifo__DOT__reset;
    }
    Vtb_sync_fifo___024root___timing_ready(vlSelf);
    Vtb_sync_fifo___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtb_sync_fifo___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vtb_sync_fifo___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Vtb_sync_fifo___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        Vtb_sync_fifo___024root___timing_resume(vlSelf);
        {
            // Inlined CFunc: _eval_act
            if ((8ULL & vlSelfRef.__VactTriggered[0U])) {
                {
                    // Inlined CFunc: _act_sequent__TOP__0
                    if (((IData)(vlSelfRef.tb_sync_fifo__DOT__clk) 
                         ^ (IData)(vlSelfRef.tb_sync_fifo__DOT____Vtogcov__clk))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 0, vlSelfRef.tb_sync_fifo__DOT__clk, vlSelfRef.tb_sync_fifo__DOT____Vtogcov__clk);
                        vlSelfRef.tb_sync_fifo__DOT____Vtogcov__clk 
                            = vlSelfRef.tb_sync_fifo__DOT__clk;
                    }
                }
            }
            if ((0x000000000000000dULL & vlSelfRef.__VactTriggered[0U])) {
                Vtb_sync_fifo___024root___act_comb__TOP__0(vlSelf);
            }
        }
    }
    return (__VactExecute);
}

bool Vtb_sync_fifo___024root___eval_phase__inact(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_phase__inact\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("examples/fifo/verif/tb_sync_fifo.sv", 2, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Vtb_sync_fifo___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vtb_sync_fifo___024root___eval_phase__nba(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_phase__nba\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vtb_sync_fifo___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vtb_sync_fifo___024root___eval_nba(vlSelf);
        Vtb_sync_fifo___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vtb_sync_fifo___024root___eval(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vtb_sync_fifo___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("examples/fifo/verif/tb_sync_fifo.sv", 2, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("examples/fifo/verif/tb_sync_fifo.sv", 2, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vtb_sync_fifo___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("examples/fifo/verif/tb_sync_fifo.sv", 2, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
                }
                vlSelfRef.__VactIterCount = ((IData)(1U) 
                                             + vlSelfRef.__VactIterCount);
                vlSelfRef.__VactPhaseResult = Vtb_sync_fifo___024root___eval_phase__act(vlSelf);
            } while (vlSelfRef.__VactPhaseResult);
            vlSelfRef.__VinactPhaseResult = Vtb_sync_fifo___024root___eval_phase__inact(vlSelf);
        } while (vlSelfRef.__VinactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vtb_sync_fifo___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

void Vtb_sync_fifo___024root____VbeforeTrig_h0839a9c0__0(Vtb_sync_fifo___024root* vlSelf, const char* __VeventDescription) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root____VbeforeTrig_h0839a9c0__0\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    VlUnpacked<QData/*63:0*/, 1> __VTmp;
    // Body
    __VTmp[0U] = (QData)((IData)(((((~ (IData)(vlSelfRef.tb_sync_fifo__DOT__clk)) 
                                    & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0)) 
                                   << 2U) | ((IData)(vlSelfRef.tb_sync_fifo__DOT__clk) 
                                             & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0))))));
    vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0 
        = vlSelfRef.tb_sync_fifo__DOT__clk;
    if ((1ULL & __VTmp[0U])) {
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
    }
    if ((4ULL & __VTmp[0U])) {
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
    }
    vlSelfRef.__VactTriggeredAcc[0U] = (vlSelfRef.__VactTriggeredAcc[0U] 
                                        | __VTmp[0U]);
}

void Vtb_sync_fifo___024root____VbeforeTrig_h0839b971__0(Vtb_sync_fifo___024root* vlSelf, const char* __VeventDescription) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root____VbeforeTrig_h0839b971__0\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    VlUnpacked<QData/*63:0*/, 1> __VTmp;
    // Body
    __VTmp[0U] = (QData)((IData)(((((~ (IData)(vlSelfRef.tb_sync_fifo__DOT__clk)) 
                                    & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0)) 
                                   << 2U) | ((IData)(vlSelfRef.tb_sync_fifo__DOT__clk) 
                                             & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0))))));
    vlSelfRef.__Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0 
        = vlSelfRef.tb_sync_fifo__DOT__clk;
    if ((1ULL & __VTmp[0U])) {
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839b971__0.ready(__VeventDescription);
    }
    if ((4ULL & __VTmp[0U])) {
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h0839a9c0__0.ready(__VeventDescription);
    }
    vlSelfRef.__VactTriggeredAcc[0U] = (vlSelfRef.__VactTriggeredAcc[0U] 
                                        | __VTmp[0U]);
}

#ifdef VL_DEBUG
void Vtb_sync_fifo___024root___eval_debug_assertions(Vtb_sync_fifo___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_sync_fifo___024root___eval_debug_assertions\n"); );
    Vtb_sync_fifo__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
