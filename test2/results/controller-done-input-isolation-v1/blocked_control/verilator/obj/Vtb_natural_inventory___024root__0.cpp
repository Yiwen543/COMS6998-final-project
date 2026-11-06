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
        if (vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 35, 0U, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready);
            vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready = 0U;
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep)))) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 161, 1U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep = 1U;
        }
        if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid))) {
            VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 163, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid = 0U;
        }
        if ((0U != (4U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min)))) {
            VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 179, 4U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min = 4U;
        }
        if ((0U != (8U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max)))) {
            VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 211, 8U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max = 8U;
        }
        ++(vlSelf->__Vcoverage[764]);
        ++(vlSelf->__Vcoverage[766]);
        ++(vlSelf->__Vcoverage[768]);
        ++(vlSelf->__Vcoverage[770]);
        ++(vlSelf->__Vcoverage[772]);
        ++(vlSelf->__Vcoverage[774]);
        ++(vlSelf->__Vcoverage[781]);
        ++(vlSelf->__Vcoverage[779]);
        ++(vlSelf->__Vcoverage[786]);
        ++(vlSelf->__Vcoverage[784]);
        if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep))) {
            VL_COV_TOGGLE_CHG_ST_I(5, vlSelf->__Vcoverage + 405, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep = 0U;
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 415, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast = 0U;
        }
        if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid))) {
            VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 417, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid = 0U;
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 433, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser = 0U;
        }
        if ((0U != (0x0000001fU & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep))))) {
            VL_COV_TOGGLE_CHG_ST_I(5, vlSelf->__Vcoverage + 503, 0x1fU, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep = 0x1fU;
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready)))) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 775, 1U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready = 1U;
        }
        ++(vlSelf->__Vcoverage[1067]);
        ++(vlSelf->__Vcoverage[1108]);
        ++(vlSelf->__Vcoverage[1109]);
        ++(vlSelf->__Vcoverage[1112]);
        ++(vlSelf->__Vcoverage[1114]);
        ++(vlSelf->__Vcoverage[1116]);
        ++(vlSelf->__Vcoverage[1121]);
        ++(vlSelf->__Vcoverage[1118]);
        ++(vlSelf->__Vcoverage[1119]);
        ++(vlSelf->__Vcoverage[1126]);
        ++(vlSelf->__Vcoverage[1123]);
        ++(vlSelf->__Vcoverage[1124]);
        ++(vlSelf->__Vcoverage[1867]);
        ++(vlSelf->__Vcoverage[1869]);
        ++(vlSelf->__Vcoverage[1871]);
        ++(vlSelf->__Vcoverage[1873]);
        ++(vlSelf->__Vcoverage[537]);
        ++(vlSelf->__Vcoverage[541]);
        ++(vlSelf->__Vcoverage[545]);
        ++(vlSelf->__Vcoverage[550]);
        ++(vlSelf->__Vcoverage[555]);
        ++(vlSelf->__Vcoverage[560]);
        ++(vlSelf->__Vcoverage[564]);
        ++(vlSelf->__Vcoverage[540]);
        ++(vlSelf->__Vcoverage[544]);
        ++(vlSelf->__Vcoverage[549]);
        ++(vlSelf->__Vcoverage[554]);
        ++(vlSelf->__Vcoverage[558]);
        ++(vlSelf->__Vcoverage[559]);
        ++(vlSelf->__Vcoverage[562]);
        ++(vlSelf->__Vcoverage[563]);
        ++(vlSelf->__Vcoverage[567]);
        ++(vlSelf->__Vcoverage[568]);
        ++(vlSelf->__Vcoverage[928]);
        ++(vlSelf->__Vcoverage[932]);
        ++(vlSelf->__Vcoverage[936]);
        ++(vlSelf->__Vcoverage[941]);
        ++(vlSelf->__Vcoverage[946]);
        ++(vlSelf->__Vcoverage[951]);
        ++(vlSelf->__Vcoverage[955]);
        ++(vlSelf->__Vcoverage[930]);
        ++(vlSelf->__Vcoverage[931]);
        ++(vlSelf->__Vcoverage[935]);
        ++(vlSelf->__Vcoverage[940]);
        ++(vlSelf->__Vcoverage[945]);
        ++(vlSelf->__Vcoverage[949]);
        ++(vlSelf->__Vcoverage[950]);
        ++(vlSelf->__Vcoverage[953]);
        ++(vlSelf->__Vcoverage[954]);
        ++(vlSelf->__Vcoverage[957]);
        ++(vlSelf->__Vcoverage[958]);
        ++(vlSelf->__Vcoverage[959]);
        ++(vlSelf->__Vcoverage[1236]);
        ++(vlSelf->__Vcoverage[1237]);
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
        VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 13, "", false);
    }
    tb_natural_inventory__DOT__fd = VL_FOPEN_NN(vlSelfRef.tb_natural_inventory__DOT__path
                                                , "r"s);
    ;
    if (VL_LIKELY(((0U != tb_natural_inventory__DOT__fd)))) {
        ++(vlSelf->__Vcoverage[131]);
    } else {
        VL_WRITEF_NX("[%0t] %%Fatal: driver.sv:14: Assertion failed in %m: missing file\n",3, 'M',vlSymsp->name(),"tb_natural_inventory", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000));
        VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 14, "", false);
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
                VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 18, "", false);
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
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 
                                                 23);
            vlSelfRef.tb_natural_inventory__DOT__take = 0U;
            VL_WRITEF_NX("PRE %0d %0d %0d %0d %0d %0d %0d 0 %0d %0d %0d %0d %0d %0d %0d %0d\n",15
                         , '~',32,vlSelfRef.tb_natural_inventory__DOT__cycle
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__rst)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__s_valid
                         , '#',8,(IData)(vlSelfRef.tb_natural_inventory__DOT__s_data)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__s_last
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__h_ready
                         , '#',8,(0x000000ffU & vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U])
                         , '#',1,(1U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                        >> 1U)), '#',1,
                         (1U & (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                >> 8U)), '#',1,(1U 
                                                & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                                   >> 1U))
                         , '#',1,(1U & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                >> 0x00000021U)))
                         , '#',1,(1U & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                >> 0x00000020U)))
                         , '#',16,(0x0000ffffU & (IData)(
                                                         (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                          >> 0x00000010U)))
                         , '#',16,(0x0000ffffU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U])));
            co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 
                                                 25);
            vlSelfRef.tb_natural_inventory__DOT__clk = 1U;
            co_await vlSelfRef.__VdlySched.delay(0x0000000000000fa0ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 
                                                 25);
            VL_WRITEF_NX("POST %0d 0 %0d %0d %0d %0d %0d %0d %0d %0d\n",9
                         , '~',32,vlSelfRef.tb_natural_inventory__DOT__cycle
                         , '#',8,(0x000000ffU & vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U])
                         , '#',1,(1U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                        >> 1U)), '#',1,
                         (1U & (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                >> 8U)), '#',1,(1U 
                                                & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                                   >> 1U))
                         , '#',1,(1U & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                >> 0x00000021U)))
                         , '#',1,(1U & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                >> 0x00000020U)))
                         , '#',16,(0x0000ffffU & (IData)(
                                                         (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                          >> 0x00000010U)))
                         , '#',16,(0x0000ffffU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U])));
            co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 
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
            ++(vlSelf->__Vcoverage[150]);
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
                VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 29, "", false);
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
    VL_FINISH_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 31, "");
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
    CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
    tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked = 0;
    // Body
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
           & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg;
    tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked 
        = vlSelfRef.tb_natural_inventory__DOT__s_data;
    ++(vlSelf->__Vcoverage[1639]);
    if ((0U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
               & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)) 
                  | (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full))));
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
        ++(vlSelf->__Vcoverage[1674]);
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
            ++(vlSelf->__Vcoverage[1640]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
            ++(vlSelf->__Vcoverage[1641]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full))) {
            ++(vlSelf->__Vcoverage[1642]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
            ++(vlSelf->__Vcoverage[1643]);
        }
        ++(vlSelf->__Vcoverage[1645]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1646]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1676]);
        }
        ++(vlSelf->__Vcoverage[1677]);
        ++(vlSelf->__Vcoverage[1678]);
    } else if ((1U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
        ++(vlSelf->__Vcoverage[1709]);
        ++(vlSelf->__Vcoverage[1680]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1681]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1711]);
        }
        ++(vlSelf->__Vcoverage[1712]);
        ++(vlSelf->__Vcoverage[1713]);
    } else if ((2U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_user_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1714]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1715]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1716]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1717]);
            }
            if ((1U >= (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                       & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg)));
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                     & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
                    ++(vlSelf->__Vcoverage[1718]);
                }
                if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                    ++(vlSelf->__Vcoverage[1719]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                    ++(vlSelf->__Vcoverage[1720]);
                }
                ++(vlSelf->__Vcoverage[1721]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                ++(vlSelf->__Vcoverage[1722]);
            }
            ++(vlSelf->__Vcoverage[1723]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
            ++(vlSelf->__Vcoverage[1724]);
        }
        ++(vlSelf->__Vcoverage[1725]);
    } else if ((3U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
        ++(vlSelf->__Vcoverage[1739]);
        ++(vlSelf->__Vcoverage[1727]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last)))) {
            ++(vlSelf->__Vcoverage[1728]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1729]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1741]);
        }
        ++(vlSelf->__Vcoverage[1742]);
        ++(vlSelf->__Vcoverage[1743]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full))) {
        ++(vlSelf->__Vcoverage[1630]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
        ++(vlSelf->__Vcoverage[1631]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[1632]);
    }
    ++(vlSelf->__Vcoverage[1744]);
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 1245, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1284, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1365, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1431, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1564, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1580, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1587, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1589, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1605, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1621, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1628, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1522, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1525, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1528, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1531, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next;
    }
    if ((0U != ((IData)(tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1316, tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1582, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int))))) {
        ++(vlSelf->__Vcoverage[1874]);
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))))) {
        ++(vlSelf->__Vcoverage[1875]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)))) {
        ++(vlSelf->__Vcoverage[1876]);
    }
    if ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
          & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int))) {
        ++(vlSelf->__Vcoverage[1877]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1878]);
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output = 0U;
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg) {
        if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
                   | (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))))) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output = 1U;
            ++(vlSelf->__Vcoverage[1879]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp = 1U;
            ++(vlSelf->__Vcoverage[1880]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)))) {
            ++(vlSelf->__Vcoverage[1881]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)))) {
            ++(vlSelf->__Vcoverage[1882]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
            ++(vlSelf->__Vcoverage[1883]);
        }
        ++(vlSelf->__Vcoverage[1886]);
    } else if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[1885]);
    } else {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output = 1U;
        ++(vlSelf->__Vcoverage[1884]);
    }
    ++(vlSelf->__Vcoverage[1887]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1755, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1818, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1860, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1862, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_temp_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1864, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_temp_to_output);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_temp_to_output 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output;
    }
}

void Vtb_natural_inventory___024root___nba_sequent__TOP__0(Vtb_natural_inventory___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_natural_inventory___024root___nba_sequent__TOP__0\n"); );
    Vtb_natural_inventory__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg = 0;
    CData/*1:0*/ __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0;
    CData/*3:0*/ __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg = 0;
    CData/*5:0*/ __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg = 0;
    CData/*1:0*/ __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0;
    CData/*5:0*/ __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg = 0;
    QData/*33:0*/ __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0;
    __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 0;
    CData/*2:0*/ __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0;
    __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 0;
    CData/*0:0*/ __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 0;
    QData/*33:0*/ __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0;
    __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0;
    CData/*0:0*/ __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0;
    QData/*33:0*/ __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1;
    __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0;
    CData/*0:0*/ __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0;
    SData/*8:0*/ __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0;
    __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 0;
    CData/*4:0*/ __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0;
    __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 0;
    CData/*0:0*/ __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 0;
    SData/*8:0*/ __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0;
    __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0;
    CData/*0:0*/ __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0;
    SData/*8:0*/ __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1;
    __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0;
    CData/*0:0*/ __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0;
    // Body
    ++(vlSelf->__Vcoverage[872]);
    ++(vlSelf->__Vcoverage[1212]);
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0U;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0U;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0U;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0U;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 0U;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
    __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 0U;
    __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[873]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[874]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready) 
         | (0U != (1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)) 
                         >> 1U))))) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = ((1U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)) 
               | (2U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                        << 1U)));
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U];
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 = 1U;
        ++(vlSelf->__Vcoverage[875]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[876]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[878]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[879]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)) 
         & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U))) {
        ++(vlSelf->__Vcoverage[880]);
    }
    ++(vlSelf->__Vcoverage[881]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem
            [(7U & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg))];
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 1U;
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[883]);
        } else {
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg)));
            ++(vlSelf->__Vcoverage[882]);
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty)))) {
            ++(vlSelf->__Vcoverage[884]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[886]);
        }
        ++(vlSelf->__Vcoverage[887]);
    } else {
        ++(vlSelf->__Vcoverage[888]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg = 0U;
        ++(vlSelf->__Vcoverage[893]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[894]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[889]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[890]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[891]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)) 
         & (3U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[892]);
    }
    ++(vlSelf->__Vcoverage[895]);
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[1213]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[1214]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready) 
         | (0U != (1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)) 
                         >> 1U))))) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = ((1U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)) 
               | (2U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                        << 1U)));
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U];
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 = 1U;
        ++(vlSelf->__Vcoverage[1215]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[1216]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[1218]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[1219]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
         & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U))) {
        ++(vlSelf->__Vcoverage[1220]);
    }
    ++(vlSelf->__Vcoverage[1221]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem
            [(0x0000001fU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg))];
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 1U;
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[1223]);
        } else {
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg)));
            ++(vlSelf->__Vcoverage[1222]);
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty)))) {
            ++(vlSelf->__Vcoverage[1224]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[1226]);
        }
        ++(vlSelf->__Vcoverage[1227]);
    } else {
        ++(vlSelf->__Vcoverage[1228]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg = 0U;
        ++(vlSelf->__Vcoverage[1233]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1234]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[1229]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[1230]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[1231]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
         & (3U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[1232]);
    }
    ++(vlSelf->__Vcoverage[1235]);
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg 
        = (0x0000000fU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
                          - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg)));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg 
        = (0x0000003fU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
                          - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg)));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg 
        = (0x0000000fU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg) 
                          - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg)));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg 
        = (0x0000003fU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg) 
                          - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg)));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
        = __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    if (__VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
            = __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0;
    }
    if (__VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U] 
            = __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
        = __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    if (__VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
            = __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0;
    }
    if (__VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U] 
            = __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg 
        = __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg 
        = __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg;
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 305, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
    }
    if ((IData)((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U) ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 41, 
                               ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                >> 1U), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid 
            = (1U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                     >> 1U));
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(2, vlSelf->__Vcoverage + 735, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    }
    if ((1U & ((IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                        >> 0x00000021U)) ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 43, (IData)(
                                                                    (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                                     >> 0x00000021U)), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad 
            = (1U & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                             >> 0x00000021U)));
    }
    if ((1U & ((IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                        >> 0x00000020U)) ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 45, (IData)(
                                                                    (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                                     >> 0x00000020U)), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate 
            = (1U & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                             >> 0x00000020U)));
    }
    if ((0U != (0x0000ffffU & ((IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                        >> 0x00000010U)) 
                               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length))))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 63, (IData)(
                                                                     (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                                      >> 0x00000010U)), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length 
            = (0x0000ffffU & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                      >> 0x00000010U)));
    }
    if ((0U != (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U]) 
                               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length))))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 95, (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U]), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length 
            = (0x0000ffffU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U]));
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tdata))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 435, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tdata);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tdata 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U] 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 599, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U];
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 667, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((IData)((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U) ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 37, 
                               ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                >> 1U), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid 
            = (1U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                     >> 1U));
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(2, vlSelf->__Vcoverage + 1038, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    }
    if ((1U & ((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                >> 8U) ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 39, 
                               (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                >> 8U), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last 
            = (1U & (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                     >> 8U));
    }
    if ((0U != (0x000000ffU & (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data))))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 47, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data 
            = (0x000000ffU & vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U]);
    }
    if ((0U != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis)))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1089, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((0U != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U] 
                ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1002, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U];
    }
    if ((0U != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1020, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 515, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 898, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 269, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 271, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 273, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 523, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 587, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg = 0U;
    ++(vlSelf->__Vcoverage[790]);
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg))) {
        ++(vlSelf->__Vcoverage[847]);
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis;
        __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 
            = (7U & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg));
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 1U;
        ++(vlSelf->__Vcoverage[850]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg)));
        if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)) 
                   & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg))))) {
            ++(vlSelf->__Vcoverage[851]);
        }
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg)));
        ++(vlSelf->__Vcoverage[854]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg)))) {
            ++(vlSelf->__Vcoverage[855]);
        }
        ++(vlSelf->__Vcoverage[863]);
    } else {
        ++(vlSelf->__Vcoverage[857]);
        ++(vlSelf->__Vcoverage[859]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg)))) {
            ++(vlSelf->__Vcoverage[860]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg) {
            ++(vlSelf->__Vcoverage[861]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
            ++(vlSelf->__Vcoverage[862]);
        }
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg))) {
        ++(vlSelf->__Vcoverage[864]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[865]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[866]);
    }
    ++(vlSelf->__Vcoverage[868]);
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[869]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[870]);
    }
    ++(vlSelf->__Vcoverage[792]);
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[793]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[794]);
    }
    ++(vlSelf->__Vcoverage[871]);
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 910, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 986, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg = 0U;
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)))) {
            ++(vlSelf->__Vcoverage[1127]);
        }
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg 
            = (1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)));
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg) {
            ++(vlSelf->__Vcoverage[1128]);
        }
        ++(vlSelf->__Vcoverage[1129]);
    } else {
        ++(vlSelf->__Vcoverage[1130]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1187]);
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis;
        __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 
            = (0x0000001fU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg));
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 1U;
        ++(vlSelf->__Vcoverage[1190]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg 
            = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg)));
        if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
                   & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg))))) {
            ++(vlSelf->__Vcoverage[1191]);
        }
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg 
            = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg)));
        ++(vlSelf->__Vcoverage[1194]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg)))) {
            ++(vlSelf->__Vcoverage[1195]);
        }
        ++(vlSelf->__Vcoverage[1203]);
    } else {
        ++(vlSelf->__Vcoverage[1197]);
        ++(vlSelf->__Vcoverage[1199]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg)))) {
            ++(vlSelf->__Vcoverage[1200]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg) {
            ++(vlSelf->__Vcoverage[1201]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
            ++(vlSelf->__Vcoverage[1202]);
        }
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1204]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)))) {
        ++(vlSelf->__Vcoverage[1205]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[1206]);
    }
    ++(vlSelf->__Vcoverage[1208]);
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[1209]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1210]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1131]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)))) {
        ++(vlSelf->__Vcoverage[1133]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[1134]);
    }
    ++(vlSelf->__Vcoverage[1211]);
    if (__VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem[__VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0] 
            = __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis 
        = (((QData)((IData)((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg) 
                              << 1U) | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg)))) 
            << 0x00000020U) | (QData)((IData)((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg) 
                                                << 0x00000010U) 
                                               | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg)))));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg 
        = __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
    if (__VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem[__VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0] 
            = __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg 
        = __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_overflow))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 531, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_overflow);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_overflow 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 533, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 535, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 746, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 749, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 752, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 755, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg;
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 337, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 578, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg) 
           == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg));
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 569, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
    }
    if ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
          == (8U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg))) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full_wr))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 744, 
                               ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
                                == (8U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg))), vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full_wr);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full_wr 
            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
               == (8U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg)));
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
           == (8U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg)));
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[1745]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1746]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next;
    }
    ++(vlSelf->__Vcoverage[1748]);
    ++(vlSelf->__Vcoverage[1749]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 922, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 924, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 926, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1049, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1052, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1058, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1055, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 973, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg) 
           == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg));
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 960, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
    }
    if ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
          == (0x20U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg))) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full_wr))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1047, 
                               ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
                                == (0x20U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg))), vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full_wr);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full_wr 
            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
               == (0x20U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg)));
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
           == (0x20U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg)));
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next;
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output) {
        ++(vlSelf->__Vcoverage[1890]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int;
    } else if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output) {
        ++(vlSelf->__Vcoverage[1888]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg;
    } else {
        ++(vlSelf->__Vcoverage[1889]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp) {
        ++(vlSelf->__Vcoverage[1891]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int;
    } else {
        ++(vlSelf->__Vcoverage[1892]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[1893]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1894]);
    }
    ++(vlSelf->__Vcoverage[1895]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 742, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty;
    }
    if ((1U ^ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) 
               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 267, 
                               (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)), vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready 
            = (1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 740, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1045, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty;
    }
    if ((1U ^ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 261, 
                               (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)), vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready 
            = (1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)));
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1043, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1625, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 1238, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1251, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1332, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1398, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 265, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1751, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1758, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1775, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1792, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1795, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1812, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1820, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1823, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1840, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1857, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 243, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg;
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) {
        ++(vlSelf->__Vcoverage[1086]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg) {
        ++(vlSelf->__Vcoverage[1087]);
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg))))) {
        ++(vlSelf->__Vcoverage[1088]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 263, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis 
        = ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) 
             | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)) 
            << 8U) | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg));
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1584, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 259, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1815, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_axis)))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1068, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_axis);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_axis 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis;
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
                                                            | ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int__0))))));
        vlSelfRef.__Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int__0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
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
            if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
                {
                    // Inlined CFunc: _act_sequent__TOP__1
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early 
                        = (1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
                                    & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
                                       | ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
                                          & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))))));
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1623, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early);
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early 
                            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
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
        VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 2, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
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
            if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
                {
                    // Inlined CFunc: _act_sequent__TOP__1
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early 
                        = (1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
                                    & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
                                       | ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
                                          & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))))));
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1623, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early);
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early 
                            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
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
            VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 2, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 2, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vtb_natural_inventory___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_done_v1/public/driver.sv", 2, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
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
