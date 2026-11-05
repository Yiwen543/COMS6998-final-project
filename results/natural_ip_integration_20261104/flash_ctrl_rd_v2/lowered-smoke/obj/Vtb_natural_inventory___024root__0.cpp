// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_natural_inventory.h for the primary calling header

#include "Vtb_natural_inventory__pch.h"

VlCoroutine Vtb_natural_inventory___024root___eval_initial__TOP__Vtiming__0(Vtb_natural_inventory___024root* vlSelf);

void Vtb_natural_inventory___024root___eval_initial(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_initial\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vtb_natural_inventory___024root___eval_initial__TOP__Vtiming__0(vlSelf);
}

VlCoroutine Vtb_natural_inventory___024root___eval_initial__TOP__Vtiming__0(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ tb_natural_inventory__DOT__unnamedblk1__DOT__i;
    tb_natural_inventory__DOT__unnamedblk1__DOT__i = 0;
    // Body
    vlSelfRef.tb_natural_inventory__DOT__clk_i = 0U;
    vlSelfRef.tb_natural_inventory__DOT__op_start_i = 0U;
    vlSelfRef.tb_natural_inventory__DOT__op_num_words_i = 0U;
    vlSelfRef.tb_natural_inventory__DOT__op_addr_i = 0U;
    vlSelfRef.tb_natural_inventory__DOT__op_addr_oob_i = 0U;
    vlSelfRef.tb_natural_inventory__DOT__data_rdy_i = 0U;
    vlSelfRef.tb_natural_inventory__DOT__flash_data_i = 0ULL;
    vlSelfRef.tb_natural_inventory__DOT__flash_done_i = 0U;
    vlSelfRef.tb_natural_inventory__DOT__flash_rd_err_i = 0U;
    vlSelfRef.tb_natural_inventory__DOT__flash_mp_err_i = 0U;
    vlSelfRef.tb_natural_inventory__DOT__rst_ni = 0U;
    tb_natural_inventory__DOT__unnamedblk1__DOT__i = 0U;
    while (VL_GTS_III(32, 8U, tb_natural_inventory__DOT__unnamedblk1__DOT__i)) {
        vlSelfRef.tb_natural_inventory__DOT__clk_i = 0U;
        if ((2U == tb_natural_inventory__DOT__unnamedblk1__DOT__i)) {
            vlSelfRef.tb_natural_inventory__DOT__rst_ni = 1U;
        }
        co_await vlSelfRef.__VdlySched.delay(0x0000000000001388ULL, 
                                             nullptr, 
                                             "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/results/natural_ip_integration_20261104/flash_ctrl_rd_v2/lowered-smoke/tb_natural_inventory.sv", 
                                             38);
        vlSelfRef.tb_natural_inventory__DOT__clk_i = 1U;
        co_await vlSelfRef.__VdlySched.delay(0x0000000000001388ULL, 
                                             nullptr, 
                                             "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/results/natural_ip_integration_20261104/flash_ctrl_rd_v2/lowered-smoke/tb_natural_inventory.sv", 
                                             38);
        VL_WRITEF_NX("PORTS %0d %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h %h\n",21
                     , '~',32,tb_natural_inventory__DOT__unnamedblk1__DOT__i
                     , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__clk_i)
                     , '#',1,vlSelfRef.tb_natural_inventory__DOT__rst_ni
                     , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__op_start_i)
                     , '#',12,vlSelfRef.tb_natural_inventory__DOT__op_num_words_i
                     , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__op_done_o)
                     , '#',7,vlSelfRef.tb_natural_inventory__DOT__op_err_o
                     , '#',14,(IData)(vlSelfRef.tb_natural_inventory__DOT__op_addr_i)
                     , '#',1,vlSelfRef.tb_natural_inventory__DOT__op_addr_oob_i
                     , '#',14,(IData)(vlSelfRef.tb_natural_inventory__DOT__op_err_addr_o)
                     , '#',1,vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__err_q
                     , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__data_rdy_i)
                     , '#',39,vlSelfRef.__VdfgRegularize_hebeb780c_0_1
                     , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o)
                     , '#',1,vlSelfRef.tb_natural_inventory__DOT__flash_req_o
                     , '#',14,(0x00003fffU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__int_addr))
                     , '#',1,(1U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__int_addr) 
                                    >> 0x0000000eU))
                     , '#',39,vlSelfRef.tb_natural_inventory__DOT__flash_data_i
                     , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__flash_done_i)
                     , '#',1,vlSelfRef.tb_natural_inventory__DOT__flash_rd_err_i
                     , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__flash_mp_err_i));
        tb_natural_inventory__DOT__unnamedblk1__DOT__i 
            = ((IData)(1U) + tb_natural_inventory__DOT__unnamedblk1__DOT__i);
    }
    VL_WRITEF_NX("INVENTORY_OK cycles=8\n",0);
    VL_FINISH_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/results/natural_ip_integration_20261104/flash_ctrl_rd_v2/lowered-smoke/tb_natural_inventory.sv", 40, "");
    co_return;
}

bool Vtb_natural_inventory___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___trigger_anySet__act\n"); );
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

void Vtb_natural_inventory___024root___act_sequent__TOP__0(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___act_sequent__TOP__0\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__cnt_hit;
    tb_natural_inventory__DOT__dut__DOT__cnt_hit = 0;
    CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__txn_done;
    tb_natural_inventory__DOT__dut__DOT__txn_done = 0;
    CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__err_sel;
    tb_natural_inventory__DOT__dut__DOT__err_sel = 0;
    // Body
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__int_addr 
        = (0x00007fffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q) 
                          + (IData)(vlSelfRef.tb_natural_inventory__DOT__op_addr_i)));
    tb_natural_inventory__DOT__dut__DOT__cnt_hit = 
        ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q) 
         >= (IData)(vlSelfRef.tb_natural_inventory__DOT__op_num_words_i));
    vlSelfRef.tb_natural_inventory__DOT__flash_req_o = 0U;
    if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
        if ((1U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
            vlSelfRef.tb_natural_inventory__DOT__flash_req_o 
                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__op_start_i) 
                   & (IData)(vlSelfRef.tb_natural_inventory__DOT__data_rdy_i));
        }
    }
    tb_natural_inventory__DOT__dut__DOT__txn_done = 
        ((IData)(vlSelfRef.tb_natural_inventory__DOT__flash_req_o) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__flash_done_i));
    vlSelfRef.tb_natural_inventory__DOT__op_done_o = 0U;
    vlSelfRef.tb_natural_inventory__DOT__data_wr_o = 0U;
    if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
        if ((1U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
            if (tb_natural_inventory__DOT__dut__DOT__txn_done) {
                if (tb_natural_inventory__DOT__dut__DOT__cnt_hit) {
                    vlSelfRef.tb_natural_inventory__DOT__op_done_o = 1U;
                }
                vlSelfRef.tb_natural_inventory__DOT__data_wr_o = 1U;
            }
        } else if ((2U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
            if (((IData)(vlSelfRef.tb_natural_inventory__DOT__data_rdy_i) 
                 & (IData)(tb_natural_inventory__DOT__dut__DOT__cnt_hit))) {
                vlSelfRef.tb_natural_inventory__DOT__op_done_o = 1U;
            }
            vlSelfRef.tb_natural_inventory__DOT__data_wr_o 
                = vlSelfRef.tb_natural_inventory__DOT__data_rdy_i;
        }
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_q;
    if ((0U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__err_q) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d = 2U;
        } else if (vlSelfRef.tb_natural_inventory__DOT__op_start_i) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d 
                = ((0x5fU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d)) 
                   | ((IData)(vlSelfRef.tb_natural_inventory__DOT__op_addr_oob_i) 
                      << 5U));
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d 
                = ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d))
                    ? 2U : 1U);
        }
    } else if ((1U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
        if (tb_natural_inventory__DOT__dut__DOT__txn_done) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d 
                = ((0x67U & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d)) 
                   | (((IData)(vlSelfRef.tb_natural_inventory__DOT__flash_mp_err_i) 
                       << 4U) | ((IData)(vlSelfRef.tb_natural_inventory__DOT__flash_rd_err_i) 
                                 << 3U)));
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d 
                = ((IData)(tb_natural_inventory__DOT__dut__DOT__cnt_hit)
                    ? 0U : ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d))
                             ? 2U : 1U));
        }
    } else if ((2U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__data_rdy_i) 
             & (IData)(tb_natural_inventory__DOT__dut__DOT__cnt_hit))) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d = 0U;
        }
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT____Vcellinp__u_cnt__clr_i 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__op_start_i) 
           & (IData)(vlSelfRef.tb_natural_inventory__DOT__op_done_o));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__ext_cnt 
        = (0x00001fffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o) 
                          + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q)));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__ext_cnt 
        = (0x00001fffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q) 
                          - (IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o)));
    vlSelfRef.tb_natural_inventory__DOT__op_err_o = 
        ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d) 
         | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_q));
    tb_natural_inventory__DOT__dut__DOT__err_sel = 
        ((IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o) 
         & (0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__op_err_o)));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_1 = ((1U 
                                                 & ((~ (IData)(tb_natural_inventory__DOT__dut__DOT__err_sel)) 
                                                    | (((IData)(vlSelfRef.tb_natural_inventory__DOT__op_err_o) 
                                                        >> 3U) 
                                                       & (IData)(tb_natural_inventory__DOT__dut__DOT__err_sel))))
                                                 ? vlSelfRef.tb_natural_inventory__DOT__flash_data_i
                                                 : 0x0000002affffffffULL);
}

void Vtb_natural_inventory___024root___eval_nba(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_nba\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_sequent__TOP__0
            SData/*11:0*/ __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q;
            __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q = 0;
            SData/*11:0*/ __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q;
            __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q = 0;
            __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q;
            __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q;
            if (vlSelfRef.tb_natural_inventory__DOT__rst_ni) {
                __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q 
                    = (0x00000fffU & ((((IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o) 
                                        & (0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q)))
                                        ? ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__ext_cnt) 
                                           & (- (IData)(
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o) 
                                                             & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__ext_cnt) 
                                                                >> 0x0000000cU)))))))
                                        : (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q)) 
                                      | (- (IData)((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT____Vcellinp__u_cnt__clr_i)))));
                __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q 
                    = (0x00000fffU & ((((~ (0x00000fffU 
                                            == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q))) 
                                        & (IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o))
                                        ? ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__ext_cnt) 
                                           | (- (IData)(
                                                        ((IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o) 
                                                         & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__ext_cnt) 
                                                            >> 0x0000000cU)))))
                                        : (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q)) 
                                      & (- (IData)(
                                                   (1U 
                                                    & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT____Vcellinp__u_cnt__clr_i)))))));
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q 
                    = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d;
                if (((~ (0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_q))) 
                     & (0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d)))) {
                    vlSelfRef.tb_natural_inventory__DOT__op_err_addr_o 
                        = (0x00003fffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q) 
                                          + (IData)(vlSelfRef.tb_natural_inventory__DOT__op_addr_i)));
                }
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_q 
                    = (((IData)(vlSelfRef.tb_natural_inventory__DOT__op_start_i) 
                        & (IData)(vlSelfRef.tb_natural_inventory__DOT__op_done_o))
                        ? 0U : (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d));
            } else {
                __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q = 0x00000fffU;
                __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q = 0U;
                vlSelfRef.tb_natural_inventory__DOT__op_err_addr_o = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_q = 0U;
            }
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__err_q 
                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__rst_ni) 
                   && (0x0fffU != (0x00001fffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q) 
                                                  + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q)))));
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q 
                = __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q 
                = __Vinline_0__nba_sequent__TOP__0___Vdly__tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q;
        }
    }
    if ((7ULL & vlSelfRef.__VnbaTriggered[0U])) {
        {
            // Inlined CFunc: _nba_comb__TOP__0
            CData/*0:0*/ __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__cnt_hit;
            __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__cnt_hit = 0;
            CData/*0:0*/ __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__txn_done;
            __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__txn_done = 0;
            CData/*0:0*/ __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__err_sel;
            __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__err_sel = 0;
            vlSelfRef.tb_natural_inventory__DOT__flash_req_o = 0U;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__int_addr 
                = (0x00007fffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q) 
                                  + (IData)(vlSelfRef.tb_natural_inventory__DOT__op_addr_i)));
            __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__cnt_hit 
                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q) 
                   >= (IData)(vlSelfRef.tb_natural_inventory__DOT__op_num_words_i));
            if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
                if ((1U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
                    vlSelfRef.tb_natural_inventory__DOT__flash_req_o 
                        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__op_start_i) 
                           & (IData)(vlSelfRef.tb_natural_inventory__DOT__data_rdy_i));
                }
            }
            __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__txn_done 
                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__flash_req_o) 
                   & (IData)(vlSelfRef.tb_natural_inventory__DOT__flash_done_i));
            vlSelfRef.tb_natural_inventory__DOT__op_done_o = 0U;
            vlSelfRef.tb_natural_inventory__DOT__data_wr_o = 0U;
            if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
                if ((1U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
                    if (__Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__txn_done) {
                        if (__Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__cnt_hit) {
                            vlSelfRef.tb_natural_inventory__DOT__op_done_o = 1U;
                        }
                        vlSelfRef.tb_natural_inventory__DOT__data_wr_o = 1U;
                    }
                } else if ((2U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__data_rdy_i) 
                         & __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__cnt_hit)) {
                        vlSelfRef.tb_natural_inventory__DOT__op_done_o = 1U;
                    }
                    vlSelfRef.tb_natural_inventory__DOT__data_wr_o 
                        = vlSelfRef.tb_natural_inventory__DOT__data_rdy_i;
                }
            }
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_q;
            if ((0U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
                if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__err_q) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d = 2U;
                } else if (vlSelfRef.tb_natural_inventory__DOT__op_start_i) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d 
                        = ((0x5fU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d)) 
                           | ((IData)(vlSelfRef.tb_natural_inventory__DOT__op_addr_oob_i) 
                              << 5U));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d 
                        = ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d))
                            ? 2U : 1U);
                }
            } else if ((1U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
                if (__Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__txn_done) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d 
                        = ((0x67U & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d)) 
                           | (((IData)(vlSelfRef.tb_natural_inventory__DOT__flash_mp_err_i) 
                               << 4U) | ((IData)(vlSelfRef.tb_natural_inventory__DOT__flash_rd_err_i) 
                                         << 3U)));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d 
                        = (__Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__cnt_hit
                            ? 0U : ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d))
                                     ? 2U : 1U));
                }
            } else if ((2U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_q))) {
                if (((IData)(vlSelfRef.tb_natural_inventory__DOT__data_rdy_i) 
                     & __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__cnt_hit)) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__st_d = 0U;
                }
            }
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT____Vcellinp__u_cnt__clr_i 
                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__op_start_i) 
                   & (IData)(vlSelfRef.tb_natural_inventory__DOT__op_done_o));
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__ext_cnt 
                = (0x00001fffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o) 
                                  + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q)));
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__ext_cnt 
                = (0x00001fffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q) 
                                  - (IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o)));
            vlSelfRef.tb_natural_inventory__DOT__op_err_o 
                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_d) 
                   | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__op_err_q));
            __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__err_sel 
                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__data_wr_o) 
                   & (0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__op_err_o)));
            vlSelfRef.__VdfgRegularize_hebeb780c_0_1 
                = ((1U & ((~ (IData)(__Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__err_sel)) 
                          | (((IData)(vlSelfRef.tb_natural_inventory__DOT__op_err_o) 
                              >> 3U) & __Vinline_0__nba_comb__TOP__0_tb_natural_inventory__DOT__dut__DOT__err_sel)))
                    ? vlSelfRef.tb_natural_inventory__DOT__flash_data_i
                    : 0x0000002affffffffULL);
        }
    }
}

void Vtb_natural_inventory___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void Vtb_natural_inventory___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vtb_natural_inventory___024root___eval_phase__act(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_phase__act\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VactExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        ((vlSelfRef.__VdlySched.awaitingCurrentTime() 
                                                          << 2U) 
                                                         | ((((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__rst_ni)) 
                                                              & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__rst_ni__0)) 
                                                             << 1U) 
                                                            | ((IData)(vlSelfRef.tb_natural_inventory__DOT__clk_i) 
                                                               & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk_i__0)))))));
        vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk_i__0 
            = vlSelfRef.tb_natural_inventory__DOT__clk_i;
        vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__rst_ni__0 
            = vlSelfRef.tb_natural_inventory__DOT__rst_ni;
    }
    Vtb_natural_inventory___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtb_natural_inventory___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vtb_natural_inventory___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Vtb_natural_inventory___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        {
            // Inlined CFunc: _timing_resume
            if ((4ULL & vlSelfRef.__VactTriggered[0U])) {
                vlSelfRef.__VdlySched.resume();
            }
        }
        {
            // Inlined CFunc: _eval_act
            if ((4ULL & vlSelfRef.__VactTriggered[0U])) {
                Vtb_natural_inventory___024root___act_sequent__TOP__0(vlSelf);
            }
        }
    }
    return (__VactExecute);
}

bool Vtb_natural_inventory___024root___eval_phase__inact(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_phase__inact\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/results/natural_ip_integration_20261104/flash_ctrl_rd_v2/lowered-smoke/tb_natural_inventory.sv", 2, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Vtb_natural_inventory___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vtb_natural_inventory___024root___eval_phase__nba(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_phase__nba\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vtb_natural_inventory___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vtb_natural_inventory___024root___eval_nba(vlSelf);
        Vtb_natural_inventory___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vtb_natural_inventory___024root___eval(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vtb_natural_inventory___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/results/natural_ip_integration_20261104/flash_ctrl_rd_v2/lowered-smoke/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/results/natural_ip_integration_20261104/flash_ctrl_rd_v2/lowered-smoke/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vtb_natural_inventory___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/results/natural_ip_integration_20261104/flash_ctrl_rd_v2/lowered-smoke/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
                }
                vlSelfRef.__VactIterCount = ((IData)(1U) 
                                             + vlSelfRef.__VactIterCount);
                vlSelfRef.__VactPhaseResult = Vtb_natural_inventory___024root___eval_phase__act(vlSelf);
            } while (vlSelfRef.__VactPhaseResult);
            vlSelfRef.__VinactPhaseResult = Vtb_natural_inventory___024root___eval_phase__inact(vlSelf);
        } while (vlSelfRef.__VinactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vtb_natural_inventory___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vtb_natural_inventory___024root___eval_debug_assertions(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_debug_assertions\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
