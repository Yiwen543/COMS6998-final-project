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
    {
        // Inlined CFunc: _eval_initial__TOP
        ++(vlSelf->__Vcoverage[901]);
        ++(vlSelf->__Vcoverage[903]);
        ++(vlSelf->__Vcoverage[905]);
        ++(vlSelf->__Vcoverage[907]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep)))) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 161, 1U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep = 1U;
        }
        if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid))) {
            VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 163, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid = 0U;
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tuser) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 179, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tuser);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tuser = 0U;
        }
        if ((0U != (4U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min)))) {
            VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 181, 4U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min = 4U;
        }
        if ((0U != (8U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max)))) {
            VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 213, 8U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max = 8U;
        }
        ++(vlSelf->__Vcoverage[245]);
        ++(vlSelf->__Vcoverage[246]);
    }
    Vtb_natural_inventory___024root___eval_initial__TOP__Vtiming__0(vlSelf);
}

VlCoroutine Vtb_natural_inventory___024root___eval_initial__TOP__Vtiming__0(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ tb_natural_inventory__DOT____VlemExpr_0;
    IData/*31:0*/ tb_natural_inventory__DOT__fd;
    tb_natural_inventory__DOT__fd = 0;
    // Body
    tb_natural_inventory__DOT____VlemExpr_0 = VL_VALUEPLUSARGS_INN(64, "VECTORS=%s"s, 
                                                                   vlSelfRef.tb_natural_inventory__DOT__path);
    if (VL_LIKELY((tb_natural_inventory__DOT____VlemExpr_0))) {
        ++(vlSelf->__Vcoverage[130]);
    } else {
        VL_WRITEF_NX("[%0t] %%Fatal: driver.sv:13: Assertion failed in %m: missing vectors\n",3, 'M',vlSymsp->name(),"tb_natural_inventory", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000));
        VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 13, "", false);
    }
    tb_natural_inventory__DOT__fd = VL_FOPEN_NN(vlSelfRef.tb_natural_inventory__DOT__path
                                                , "r"s);
    ;
    if (VL_LIKELY(((0U != tb_natural_inventory__DOT__fd)))) {
        ++(vlSelf->__Vcoverage[131]);
    } else {
        VL_WRITEF_NX("[%0t] %%Fatal: driver.sv:14: Assertion failed in %m: missing file\n",3, 'M',vlSymsp->name(),"tb_natural_inventory", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000));
        VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 14, "", false);
    }
    while (true) {
        vlSelfRef.tb_natural_inventory__DOT____VExpr_he4c3ed11__0 
            = (tb_natural_inventory__DOT__fd ? feof(VL_CVT_I_FP(tb_natural_inventory__DOT__fd)) : true);
        if (!((! vlSelfRef.tb_natural_inventory__DOT____VExpr_he4c3ed11__0))) break;
        vlSelfRef.tb_natural_inventory__DOT__n = VL_FSCANF_INX(tb_natural_inventory__DOT__fd,"%d %d %d %d %d %d",6
                                                               , '#',32,&(vlSelfRef.tb_natural_inventory__DOT__r)
                                                               , '#',32,&(vlSelfRef.tb_natural_inventory__DOT__o)
                                                               , '#',32,&(vlSelfRef.tb_natural_inventory__DOT__d)
                                                               , '#',32,&(vlSelfRef.tb_natural_inventory__DOT__l)
                                                               , '#',32,&(vlSelfRef.tb_natural_inventory__DOT__m)
                                                               , '#',32,&(vlSelfRef.tb_natural_inventory__DOT__h)) ;
        if (VL_UNLIKELY(((6U == vlSelfRef.tb_natural_inventory__DOT__n)))) {
            if (VL_UNLIKELY((VL_LTES_III(32, 0x00000200U, vlSelfRef.tb_natural_inventory__DOT__cycle)))) {
                VL_WRITEF_NX("[%0t] %%Fatal: driver.sv:18: Assertion failed in %m: cycle cap\n",3, 'M',vlSymsp->name(),"tb_natural_inventory", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 18, "", false);
            } else {
                ++(vlSelf->__Vcoverage[134]);
            }
            vlSelfRef.tb_natural_inventory__DOT__rst 
                = (1U & vlSelfRef.tb_natural_inventory__DOT__r);
            vlSelfRef.tb_natural_inventory__DOT__m_ready 
                = (1U & vlSelfRef.tb_natural_inventory__DOT__m);
            vlSelfRef.tb_natural_inventory__DOT__h_ready 
                = (1U & vlSelfRef.tb_natural_inventory__DOT__h);
            if (vlSelfRef.tb_natural_inventory__DOT__rst) {
                vlSelfRef.tb_natural_inventory__DOT__head = 0U;
                vlSelfRef.tb_natural_inventory__DOT__tail = 0U;
                ++(vlSelf->__Vcoverage[137]);
            } else if ((0U != vlSelfRef.tb_natural_inventory__DOT__o)) {
                vlSelfRef.tb_natural_inventory__DOT__data_q[(0x000001ffU 
                                                             & vlSelfRef.tb_natural_inventory__DOT__tail)] 
                    = (0x000000ffU & vlSelfRef.tb_natural_inventory__DOT__d);
                vlSelfRef.tb_natural_inventory__DOT__last_q[(0x000001ffU 
                                                             & vlSelfRef.tb_natural_inventory__DOT__tail)] 
                    = (1U & vlSelfRef.tb_natural_inventory__DOT__l);
                vlSelfRef.tb_natural_inventory__DOT__tail 
                    = ((IData)(1U) + vlSelfRef.tb_natural_inventory__DOT__tail);
                ++(vlSelf->__Vcoverage[135]);
            } else {
                ++(vlSelf->__Vcoverage[136]);
            }
            vlSelfRef.tb_natural_inventory__DOT__s_valid 
                = ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__rst)) 
                   & VL_LTS_III(32, vlSelfRef.tb_natural_inventory__DOT__head, vlSelfRef.tb_natural_inventory__DOT__tail));
            if (vlSelfRef.tb_natural_inventory__DOT__s_valid) {
                ++(vlSelf->__Vcoverage[143]);
                vlSelfRef.tb_natural_inventory__DOT____VlemCond_1 
                    = vlSelfRef.tb_natural_inventory__DOT__data_q
                    [(0x000001ffU & vlSelfRef.tb_natural_inventory__DOT__head)];
            } else {
                ++(vlSelf->__Vcoverage[144]);
                vlSelfRef.tb_natural_inventory__DOT____VlemCond_1 = 0U;
            }
            vlSelfRef.tb_natural_inventory__DOT__s_data 
                = (0x000000ffU & vlSelfRef.tb_natural_inventory__DOT____VlemCond_1);
            if (vlSelfRef.tb_natural_inventory__DOT__s_valid) {
                ++(vlSelf->__Vcoverage[147]);
                vlSelfRef.tb_natural_inventory__DOT____VlemCond_2 
                    = vlSelfRef.tb_natural_inventory__DOT__last_q
                    [(0x000001ffU & vlSelfRef.tb_natural_inventory__DOT__head)];
            } else {
                ++(vlSelf->__Vcoverage[148]);
                vlSelfRef.tb_natural_inventory__DOT____VlemCond_2 = 0U;
            }
            vlSelfRef.tb_natural_inventory__DOT__s_last 
                = (1U & vlSelfRef.tb_natural_inventory__DOT____VlemCond_2);
            co_await vlSelfRef.__VdlySched.delay(0x0000000000000fa0ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 
                                                 23);
            vlSelfRef.tb_natural_inventory__DOT__take 
                = (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__rst)) 
                    & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)) 
                   & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg));
            VL_WRITEF_NX("PRE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d\n",16
                         , '~',32,vlSelfRef.tb_natural_inventory__DOT__cycle
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__rst)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__s_valid
                         , '#',8,(IData)(vlSelfRef.tb_natural_inventory__DOT__s_data)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__s_last
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__h_ready
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg)
                         , '#',8,vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg)
                         , '#',16,vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg
                         , '#',16,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg));
            co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 
                                                 25);
            vlSelfRef.tb_natural_inventory__DOT__clk = 1U;
            co_await vlSelfRef.__VdlySched.delay(0x0000000000000fa0ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 
                                                 25);
            VL_WRITEF_NX("POST %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d\n",10
                         , '~',32,vlSelfRef.tb_natural_inventory__DOT__cycle
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg)
                         , '#',8,vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg)
                         , '#',16,vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg
                         , '#',16,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg));
            co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 
                                                 27);
            vlSelfRef.tb_natural_inventory__DOT__clk = 0U;
            if ((0U != vlSelfRef.tb_natural_inventory__DOT__take)) {
                vlSelfRef.tb_natural_inventory__DOT__head 
                    = ((IData)(1U) + vlSelfRef.tb_natural_inventory__DOT__head);
                ++(vlSelf->__Vcoverage[153]);
            } else {
                ++(vlSelf->__Vcoverage[154]);
            }
            VL_WRITEF_NX("QUEUE %0d %0d %0d\n",3, '~',32,vlSelfRef.tb_natural_inventory__DOT__cycle
                         , '~',32,vlSelfRef.tb_natural_inventory__DOT__head
                         , '~',32,vlSelfRef.tb_natural_inventory__DOT__tail);
            vlSelfRef.tb_natural_inventory__DOT__cycle 
                = ((IData)(1U) + vlSelfRef.tb_natural_inventory__DOT__cycle);
            if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__rst)) 
                 & VL_LTS_III(32, vlSelfRef.tb_natural_inventory__DOT__head, vlSelfRef.tb_natural_inventory__DOT__tail))) {
                ++(vlSelf->__Vcoverage[138]);
            }
            if (VL_GTES_III(32, vlSelfRef.tb_natural_inventory__DOT__head, vlSelfRef.tb_natural_inventory__DOT__tail)) {
                ++(vlSelf->__Vcoverage[139]);
            }
            if (vlSelfRef.tb_natural_inventory__DOT__rst) {
                ++(vlSelf->__Vcoverage[140]);
            }
            if (vlSelfRef.tb_natural_inventory__DOT__s_valid) {
                ++(vlSelf->__Vcoverage[141]);
            }
            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
                ++(vlSelf->__Vcoverage[142]);
            }
            if (vlSelfRef.tb_natural_inventory__DOT__s_valid) {
                ++(vlSelf->__Vcoverage[145]);
            }
            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
                ++(vlSelf->__Vcoverage[146]);
            }
            if ((((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__rst)) 
                  & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)) 
                 & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg))) {
                ++(vlSelf->__Vcoverage[149]);
            }
            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg)))) {
                ++(vlSelf->__Vcoverage[150]);
            }
            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
                ++(vlSelf->__Vcoverage[151]);
            }
            if (vlSelfRef.tb_natural_inventory__DOT__rst) {
                ++(vlSelf->__Vcoverage[152]);
            }
            ++(vlSelf->__Vcoverage[158]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT____VExpr_he4c3ed11__1 
                = (tb_natural_inventory__DOT__fd ? feof(VL_CVT_I_FP(tb_natural_inventory__DOT__fd)) : true);
            if (VL_LIKELY((vlSelfRef.tb_natural_inventory__DOT____VExpr_he4c3ed11__1))) {
                ++(vlSelf->__Vcoverage[155]);
            } else {
                VL_WRITEF_NX("[%0t] %%Fatal: driver.sv:29: Assertion failed in %m: malformed vector\n",3, 'M',vlSymsp->name(),"tb_natural_inventory", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 29, "", false);
            }
            if ((! vlSelfRef.tb_natural_inventory__DOT____VExpr_he4c3ed11__1)) {
                ++(vlSelf->__Vcoverage[156]);
            }
            if (vlSelfRef.tb_natural_inventory__DOT____VExpr_he4c3ed11__1) {
                ++(vlSelf->__Vcoverage[157]);
            }
        }
        if ((! vlSelfRef.tb_natural_inventory__DOT____VExpr_he4c3ed11__0)) {
            ++(vlSelf->__Vcoverage[132]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT____VExpr_he4c3ed11__0) {
            ++(vlSelf->__Vcoverage[133]);
        }
        ++(vlSelf->__Vcoverage[159]);
    }
    VL_WRITEF_NX("DRIVER_COMPLETE %0d\n",1, '~',32,vlSelfRef.tb_natural_inventory__DOT__cycle);
    VL_FINISH_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 31, "");
    ++(vlSelf->__Vcoverage[160]);
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

void Vtb_natural_inventory___024root___act_comb__TOP__0(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___act_comb__TOP__0\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked;
    tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked = 0;
    // Body
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early 
        = (1U & ((~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg) 
                     | ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int) 
                        & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg)))) 
                 | (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)));
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_early))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 666, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_early);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_early 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg) 
           & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg;
    tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked 
        = vlSelfRef.tb_natural_inventory__DOT__s_data;
    ++(vlSelf->__Vcoverage[680]);
    if ((0U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
               & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg)) 
                  | (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)));
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_valid;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 4U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 8U;
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[686]);
            ++(vlSelf->__Vcoverage[687]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[685]);
            ++(vlSelf->__Vcoverage[687]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[688]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[689]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[690]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[691]);
            }
            if ((1U >= (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg)));
                if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next 
                        = (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt 
                           > (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next = 8U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 4U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 8U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                         & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
                        ++(vlSelf->__Vcoverage[692]);
                    }
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                        ++(vlSelf->__Vcoverage[693]);
                    }
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                        ++(vlSelf->__Vcoverage[694]);
                    }
                    ++(vlSelf->__Vcoverage[695]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 3U;
                    ++(vlSelf->__Vcoverage[696]);
                }
                ++(vlSelf->__Vcoverage[709]);
            } else {
                if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg) 
                         > vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt)) {
                        if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg))) {
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg)));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 2U;
                            ++(vlSelf->__Vcoverage[700]);
                        } else {
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next = 4U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
                                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                                   & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int 
                                = VL_SHIFTR_III(1,1,32, 1U, 
                                                ((IData)(1U) 
                                                 - 
                                                 ((IData)(4U) 
                                                  - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg))));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 4U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 8U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
                            if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                                 & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
                                ++(vlSelf->__Vcoverage[697]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                                ++(vlSelf->__Vcoverage[698]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                                ++(vlSelf->__Vcoverage[699]);
                            }
                            ++(vlSelf->__Vcoverage[701]);
                        }
                        ++(vlSelf->__Vcoverage[705]);
                    } else {
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next = 1U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                               & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready));
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 4U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 8U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
                        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                             & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
                            ++(vlSelf->__Vcoverage[702]);
                        }
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                            ++(vlSelf->__Vcoverage[703]);
                        }
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                            ++(vlSelf->__Vcoverage[704]);
                        }
                        ++(vlSelf->__Vcoverage[706]);
                    }
                    ++(vlSelf->__Vcoverage[707]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 1U;
                    ++(vlSelf->__Vcoverage[708]);
                }
                ++(vlSelf->__Vcoverage[710]);
            }
            ++(vlSelf->__Vcoverage[711]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
            ++(vlSelf->__Vcoverage[712]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
            ++(vlSelf->__Vcoverage[681]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg)))) {
            ++(vlSelf->__Vcoverage[682]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
            ++(vlSelf->__Vcoverage[683]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
            ++(vlSelf->__Vcoverage[684]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[713]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[714]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[715]);
        }
        ++(vlSelf->__Vcoverage[716]);
    } else if ((1U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_valid;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[717]);
            ++(vlSelf->__Vcoverage[719]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[720]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[721]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[722]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[723]);
            }
            if ((1U >= (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg)));
                if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next 
                        = (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt 
                           > (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next = 8U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 4U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 8U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                         & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
                        ++(vlSelf->__Vcoverage[724]);
                    }
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                        ++(vlSelf->__Vcoverage[725]);
                    }
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                        ++(vlSelf->__Vcoverage[726]);
                    }
                    ++(vlSelf->__Vcoverage[727]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 3U;
                    ++(vlSelf->__Vcoverage[728]);
                }
                ++(vlSelf->__Vcoverage[741]);
            } else {
                if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg) 
                         > vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt)) {
                        if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg))) {
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg)));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 2U;
                            ++(vlSelf->__Vcoverage[732]);
                        } else {
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next = 4U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
                                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                                   & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int 
                                = VL_SHIFTR_III(1,1,32, 1U, 
                                                ((IData)(1U) 
                                                 - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg)));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 4U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 8U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
                            if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                                 & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
                                ++(vlSelf->__Vcoverage[729]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                                ++(vlSelf->__Vcoverage[730]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                                ++(vlSelf->__Vcoverage[731]);
                            }
                            ++(vlSelf->__Vcoverage[733]);
                        }
                        ++(vlSelf->__Vcoverage[737]);
                    } else {
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next = 1U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                               & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready));
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 4U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 8U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
                        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                             & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
                            ++(vlSelf->__Vcoverage[734]);
                        }
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                            ++(vlSelf->__Vcoverage[735]);
                        }
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                            ++(vlSelf->__Vcoverage[736]);
                        }
                        ++(vlSelf->__Vcoverage[738]);
                    }
                    ++(vlSelf->__Vcoverage[739]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 1U;
                    ++(vlSelf->__Vcoverage[740]);
                }
                ++(vlSelf->__Vcoverage[742]);
            }
            ++(vlSelf->__Vcoverage[743]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 1U;
            ++(vlSelf->__Vcoverage[744]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[745]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[746]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[747]);
        }
        ++(vlSelf->__Vcoverage[748]);
    } else if ((2U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_user_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int = 0U;
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[749]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[750]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[751]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[752]);
            }
            if ((1U >= (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next = 4U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                       & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready));
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg)));
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 4U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 8U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
                if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                     & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
                    ++(vlSelf->__Vcoverage[753]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                    ++(vlSelf->__Vcoverage[754]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                    ++(vlSelf->__Vcoverage[755]);
                }
                ++(vlSelf->__Vcoverage[756]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 2U;
                ++(vlSelf->__Vcoverage[757]);
            }
            ++(vlSelf->__Vcoverage[758]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 2U;
            ++(vlSelf->__Vcoverage[759]);
        }
        ++(vlSelf->__Vcoverage[760]);
    } else if ((3U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int 
            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid) 
               & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last));
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int = 0U;
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[765]);
            ++(vlSelf->__Vcoverage[766]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[764]);
            ++(vlSelf->__Vcoverage[766]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg)));
            if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next = 8U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                      + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                       & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready));
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 4U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 8U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
                if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
                     & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
                    ++(vlSelf->__Vcoverage[767]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                    ++(vlSelf->__Vcoverage[768]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                    ++(vlSelf->__Vcoverage[769]);
                }
                ++(vlSelf->__Vcoverage[770]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 3U;
                ++(vlSelf->__Vcoverage[771]);
            }
            ++(vlSelf->__Vcoverage[772]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 3U;
            ++(vlSelf->__Vcoverage[773]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last))) {
            ++(vlSelf->__Vcoverage[761]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last)))) {
            ++(vlSelf->__Vcoverage[762]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[763]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[774]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[775]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[776]);
        }
        ++(vlSelf->__Vcoverage[777]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg) 
         & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
        ++(vlSelf->__Vcoverage[671]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[672]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[673]);
    }
    ++(vlSelf->__Vcoverage[778]);
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 254, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_last_word))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 260, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_last_word);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_last_word 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 295, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 376, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 442, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdata_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 607, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdata_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdata_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 623, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tlast_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 630, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tlast_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 632, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 648, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 664, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tready_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 669, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tready_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 533, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 536, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 539, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 542, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 575, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next;
    }
    if ((0U != ((IData)(tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tdata_masked)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 327, tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tdata_masked);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tdata_masked 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 625, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int;
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int))))) {
        ++(vlSelf->__Vcoverage[908]);
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg))))) {
        ++(vlSelf->__Vcoverage[909]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[910]);
    }
    if ((((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
          & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int))) {
        ++(vlSelf->__Vcoverage[911]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[912]);
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output = 0U;
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg) {
        if ((1U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready) 
                   | (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg))))) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output = 1U;
            ++(vlSelf->__Vcoverage[913]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp = 1U;
            ++(vlSelf->__Vcoverage[914]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg)))) {
            ++(vlSelf->__Vcoverage[915]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
            ++(vlSelf->__Vcoverage[916]);
        }
        if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg))) {
            ++(vlSelf->__Vcoverage[917]);
        }
        ++(vlSelf->__Vcoverage[920]);
    } else if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output = 1U;
        ++(vlSelf->__Vcoverage[918]);
    } else {
        ++(vlSelf->__Vcoverage[919]);
    }
    ++(vlSelf->__Vcoverage[921]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 789, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 852, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 894, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_output);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_output 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_temp))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 896, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_temp);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_temp 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_temp_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 898, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_temp_to_output);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_temp_to_output 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output;
    }
}

void Vtb_natural_inventory___024root___nba_sequent__TOP__0(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___nba_sequent__TOP__0\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next;
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output) {
        ++(vlSelf->__Vcoverage[924]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int;
    } else if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output) {
        ++(vlSelf->__Vcoverage[922]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg;
    } else {
        ++(vlSelf->__Vcoverage[923]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp) {
        ++(vlSelf->__Vcoverage[925]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int;
    } else {
        ++(vlSelf->__Vcoverage[926]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[927]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[928]);
    }
    ++(vlSelf->__Vcoverage[929]);
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[779]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[780]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next;
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word) {
        ++(vlSelf->__Vcoverage[781]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_user_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int;
    } else {
        ++(vlSelf->__Vcoverage[782]);
    }
    ++(vlSelf->__Vcoverage[783]);
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
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 47, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 785, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 39, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg;
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
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 627, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 37, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 849, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg;
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
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 35, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 41, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg;
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
                                                         | ((((IData)(vlSelfRef.tb_natural_inventory__DOT__clk) 
                                                              & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk__0))) 
                                                             << 1U) 
                                                            | ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int__0))))));
        vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int__0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int;
        vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk__0 
            = vlSelfRef.tb_natural_inventory__DOT__clk;
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
                {
                    // Inlined CFunc: _act_sequent__TOP__0
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
                }
            }
            if ((5ULL & vlSelfRef.__VactTriggered[0U])) {
                Vtb_natural_inventory___024root___act_comb__TOP__0(vlSelf);
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
        VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 2, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
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
        {
            // Inlined CFunc: _eval_nba
            if ((2ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vtb_natural_inventory___024root___nba_sequent__TOP__0(vlSelf);
            }
            if ((4ULL & vlSelfRef.__VnbaTriggered[0U])) {
                {
                    // Inlined CFunc: _act_sequent__TOP__0
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
                }
            }
            if ((7ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vtb_natural_inventory___024root___act_comb__TOP__0(vlSelf);
            }
        }
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
            VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 2, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 2, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vtb_natural_inventory___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/public/driver.sv", 2, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
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
