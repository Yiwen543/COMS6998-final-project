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
        ++(vlSelf->__Vcoverage[766]);
        ++(vlSelf->__Vcoverage[768]);
        ++(vlSelf->__Vcoverage[770]);
        ++(vlSelf->__Vcoverage[772]);
        ++(vlSelf->__Vcoverage[774]);
        ++(vlSelf->__Vcoverage[776]);
        ++(vlSelf->__Vcoverage[783]);
        ++(vlSelf->__Vcoverage[781]);
        ++(vlSelf->__Vcoverage[788]);
        ++(vlSelf->__Vcoverage[786]);
        if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep))) {
            VL_COV_TOGGLE_CHG_ST_I(5, vlSelf->__Vcoverage + 407, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep = 0U;
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 417, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast = 0U;
        }
        if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid))) {
            VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 419, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid = 0U;
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 435, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser = 0U;
        }
        if ((0U != (0x0000001fU & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep))))) {
            VL_COV_TOGGLE_CHG_ST_I(5, vlSelf->__Vcoverage + 505, 0x1fU, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep = 0x1fU;
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready)))) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 777, 1U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready = 1U;
        }
        ++(vlSelf->__Vcoverage[1069]);
        ++(vlSelf->__Vcoverage[1110]);
        ++(vlSelf->__Vcoverage[1111]);
        ++(vlSelf->__Vcoverage[1114]);
        ++(vlSelf->__Vcoverage[1116]);
        ++(vlSelf->__Vcoverage[1118]);
        ++(vlSelf->__Vcoverage[1123]);
        ++(vlSelf->__Vcoverage[1120]);
        ++(vlSelf->__Vcoverage[1121]);
        ++(vlSelf->__Vcoverage[1128]);
        ++(vlSelf->__Vcoverage[1125]);
        ++(vlSelf->__Vcoverage[1126]);
        ++(vlSelf->__Vcoverage[1894]);
        ++(vlSelf->__Vcoverage[1896]);
        ++(vlSelf->__Vcoverage[1898]);
        ++(vlSelf->__Vcoverage[1900]);
        ++(vlSelf->__Vcoverage[539]);
        ++(vlSelf->__Vcoverage[543]);
        ++(vlSelf->__Vcoverage[547]);
        ++(vlSelf->__Vcoverage[552]);
        ++(vlSelf->__Vcoverage[557]);
        ++(vlSelf->__Vcoverage[562]);
        ++(vlSelf->__Vcoverage[566]);
        ++(vlSelf->__Vcoverage[542]);
        ++(vlSelf->__Vcoverage[546]);
        ++(vlSelf->__Vcoverage[551]);
        ++(vlSelf->__Vcoverage[556]);
        ++(vlSelf->__Vcoverage[560]);
        ++(vlSelf->__Vcoverage[561]);
        ++(vlSelf->__Vcoverage[564]);
        ++(vlSelf->__Vcoverage[565]);
        ++(vlSelf->__Vcoverage[569]);
        ++(vlSelf->__Vcoverage[570]);
        ++(vlSelf->__Vcoverage[930]);
        ++(vlSelf->__Vcoverage[934]);
        ++(vlSelf->__Vcoverage[938]);
        ++(vlSelf->__Vcoverage[943]);
        ++(vlSelf->__Vcoverage[948]);
        ++(vlSelf->__Vcoverage[953]);
        ++(vlSelf->__Vcoverage[957]);
        ++(vlSelf->__Vcoverage[932]);
        ++(vlSelf->__Vcoverage[933]);
        ++(vlSelf->__Vcoverage[937]);
        ++(vlSelf->__Vcoverage[942]);
        ++(vlSelf->__Vcoverage[947]);
        ++(vlSelf->__Vcoverage[951]);
        ++(vlSelf->__Vcoverage[952]);
        ++(vlSelf->__Vcoverage[955]);
        ++(vlSelf->__Vcoverage[956]);
        ++(vlSelf->__Vcoverage[959]);
        ++(vlSelf->__Vcoverage[960]);
        ++(vlSelf->__Vcoverage[961]);
        ++(vlSelf->__Vcoverage[1238]);
        ++(vlSelf->__Vcoverage[1239]);
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
            vlSelfRef.tb_natural_inventory__DOT__take 
                = (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__rst)) 
                    & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)) 
                   & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg));
            VL_WRITEF_NX("PRE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d\n",16
                         , '~',32,vlSelfRef.tb_natural_inventory__DOT__cycle
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__rst)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__s_valid
                         , '#',8,(IData)(vlSelfRef.tb_natural_inventory__DOT__s_data)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__s_last
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)
                         , '#',1,vlSelfRef.tb_natural_inventory__DOT__h_ready
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)
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
            VL_WRITEF_NX("POST %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d\n",10
                         , '~',32,vlSelfRef.tb_natural_inventory__DOT__cycle
                         , '#',1,(IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)
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
            if ((((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__rst)) 
                  & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)) 
                 & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg))) {
                ++(vlSelf->__Vcoverage[149]);
            }
            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)))) {
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
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 0U;
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
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
    tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked 
        = vlSelfRef.tb_natural_inventory__DOT__s_data;
    ++(vlSelf->__Vcoverage[1673]);
    if ((0U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
               & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)) 
                  | (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full))));
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_valid;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[1679]);
            ++(vlSelf->__Vcoverage[1680]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[1678]);
            ++(vlSelf->__Vcoverage[1680]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1681]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1682]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1683]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1684]);
            }
            if ((1U >= (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg)));
                if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
                        = (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt 
                           > (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                         & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
                        ++(vlSelf->__Vcoverage[1685]);
                    }
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                        ++(vlSelf->__Vcoverage[1686]);
                    }
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                        ++(vlSelf->__Vcoverage[1687]);
                    }
                    ++(vlSelf->__Vcoverage[1688]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                    ++(vlSelf->__Vcoverage[1689]);
                }
                ++(vlSelf->__Vcoverage[1702]);
            } else {
                if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                         > vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt)) {
                        if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                            ++(vlSelf->__Vcoverage[1693]);
                        } else {
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                                   & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                                = VL_SHIFTR_III(1,1,32, 1U, 
                                                ((IData)(1U) 
                                                 - 
                                                 ((IData)(4U) 
                                                  - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg))));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                            if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                                 & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
                                ++(vlSelf->__Vcoverage[1690]);
                            }
                            if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                                ++(vlSelf->__Vcoverage[1691]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                                ++(vlSelf->__Vcoverage[1692]);
                            }
                            ++(vlSelf->__Vcoverage[1694]);
                        }
                        ++(vlSelf->__Vcoverage[1698]);
                    } else {
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
                            ++(vlSelf->__Vcoverage[1695]);
                        }
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                            ++(vlSelf->__Vcoverage[1696]);
                        }
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                            ++(vlSelf->__Vcoverage[1697]);
                        }
                        ++(vlSelf->__Vcoverage[1699]);
                    }
                    ++(vlSelf->__Vcoverage[1700]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
                    ++(vlSelf->__Vcoverage[1701]);
                }
                ++(vlSelf->__Vcoverage[1703]);
            }
            ++(vlSelf->__Vcoverage[1704]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
            ++(vlSelf->__Vcoverage[1705]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
            ++(vlSelf->__Vcoverage[1674]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
            ++(vlSelf->__Vcoverage[1675]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full))) {
            ++(vlSelf->__Vcoverage[1676]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
            ++(vlSelf->__Vcoverage[1677]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[1706]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1707]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[1708]);
        }
        ++(vlSelf->__Vcoverage[1709]);
    } else if ((1U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_valid;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[1710]);
            ++(vlSelf->__Vcoverage[1712]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1713]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1714]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1715]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1716]);
            }
            if ((1U >= (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg)));
                if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
                        = (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt 
                           > (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                         & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
                        ++(vlSelf->__Vcoverage[1717]);
                    }
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                        ++(vlSelf->__Vcoverage[1718]);
                    }
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                        ++(vlSelf->__Vcoverage[1719]);
                    }
                    ++(vlSelf->__Vcoverage[1720]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                    ++(vlSelf->__Vcoverage[1721]);
                }
                ++(vlSelf->__Vcoverage[1734]);
            } else {
                if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                         > vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt)) {
                        if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                                = (0x0000ffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                            ++(vlSelf->__Vcoverage[1725]);
                        } else {
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                                = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                                   & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                                = VL_SHIFTR_III(1,1,32, 1U, 
                                                ((IData)(1U) 
                                                 - (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg)));
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                            if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                                 & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
                                ++(vlSelf->__Vcoverage[1722]);
                            }
                            if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                                ++(vlSelf->__Vcoverage[1723]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                                ++(vlSelf->__Vcoverage[1724]);
                            }
                            ++(vlSelf->__Vcoverage[1726]);
                        }
                        ++(vlSelf->__Vcoverage[1730]);
                    } else {
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
                            ++(vlSelf->__Vcoverage[1727]);
                        }
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                            ++(vlSelf->__Vcoverage[1728]);
                        }
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                            ++(vlSelf->__Vcoverage[1729]);
                        }
                        ++(vlSelf->__Vcoverage[1731]);
                    }
                    ++(vlSelf->__Vcoverage[1732]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
                    ++(vlSelf->__Vcoverage[1733]);
                }
                ++(vlSelf->__Vcoverage[1735]);
            }
            ++(vlSelf->__Vcoverage[1736]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
            ++(vlSelf->__Vcoverage[1737]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[1738]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1739]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[1740]);
        }
        ++(vlSelf->__Vcoverage[1741]);
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
                ++(vlSelf->__Vcoverage[1742]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1743]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1744]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1745]);
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
                    ++(vlSelf->__Vcoverage[1746]);
                }
                if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                    ++(vlSelf->__Vcoverage[1747]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                    ++(vlSelf->__Vcoverage[1748]);
                }
                ++(vlSelf->__Vcoverage[1749]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                ++(vlSelf->__Vcoverage[1750]);
            }
            ++(vlSelf->__Vcoverage[1751]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
            ++(vlSelf->__Vcoverage[1752]);
        }
        ++(vlSelf->__Vcoverage[1753]);
    } else if ((3U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = ((IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid) 
               & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last));
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__s_last;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int = 0U;
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[1758]);
            ++(vlSelf->__Vcoverage[1759]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[1757]);
            ++(vlSelf->__Vcoverage[1759]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            if (vlSelfRef.tb_natural_inventory__DOT__s_last) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 1U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                       & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                     & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
                    ++(vlSelf->__Vcoverage[1760]);
                }
                if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                    ++(vlSelf->__Vcoverage[1761]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                    ++(vlSelf->__Vcoverage[1762]);
                }
                ++(vlSelf->__Vcoverage[1763]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                ++(vlSelf->__Vcoverage[1764]);
            }
            ++(vlSelf->__Vcoverage[1765]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
            ++(vlSelf->__Vcoverage[1766]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last))) {
            ++(vlSelf->__Vcoverage[1754]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last)))) {
            ++(vlSelf->__Vcoverage[1755]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1756]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[1767]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1768]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[1769]);
        }
        ++(vlSelf->__Vcoverage[1770]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full))) {
        ++(vlSelf->__Vcoverage[1664]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
        ++(vlSelf->__Vcoverage[1665]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[1666]);
    }
    ++(vlSelf->__Vcoverage[1771]);
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 1247, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_last_word))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1253, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_last_word);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_last_word 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1288, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1369, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1435, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1600, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1616, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1623, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1625, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1641, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1657, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1662, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1526, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1529, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1532, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1535, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_original_length_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1568, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_original_length_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_original_length_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next;
    }
    if ((0U != ((IData)(tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1320, tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1618, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int))))) {
        ++(vlSelf->__Vcoverage[1901]);
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))))) {
        ++(vlSelf->__Vcoverage[1902]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)))) {
        ++(vlSelf->__Vcoverage[1903]);
    }
    if ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
          & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int))) {
        ++(vlSelf->__Vcoverage[1904]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1905]);
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
            ++(vlSelf->__Vcoverage[1906]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp = 1U;
            ++(vlSelf->__Vcoverage[1907]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)))) {
            ++(vlSelf->__Vcoverage[1908]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)))) {
            ++(vlSelf->__Vcoverage[1909]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
            ++(vlSelf->__Vcoverage[1910]);
        }
        ++(vlSelf->__Vcoverage[1913]);
    } else if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[1912]);
    } else {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output = 1U;
        ++(vlSelf->__Vcoverage[1911]);
    }
    ++(vlSelf->__Vcoverage[1914]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1782, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1845, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1887, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1889, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_temp_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1891, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_temp_to_output);
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
    ++(vlSelf->__Vcoverage[874]);
    ++(vlSelf->__Vcoverage[1214]);
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
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[875]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[876]);
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
        ++(vlSelf->__Vcoverage[877]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[878]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[880]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[881]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)) 
         & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U))) {
        ++(vlSelf->__Vcoverage[882]);
    }
    ++(vlSelf->__Vcoverage[883]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem
            [(7U & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg))];
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 1U;
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[885]);
        } else {
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg)));
            ++(vlSelf->__Vcoverage[884]);
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty)))) {
            ++(vlSelf->__Vcoverage[886]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[888]);
        }
        ++(vlSelf->__Vcoverage[889]);
    } else {
        ++(vlSelf->__Vcoverage[890]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg = 0U;
        ++(vlSelf->__Vcoverage[895]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[896]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[891]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[892]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[893]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)) 
         & (3U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[894]);
    }
    ++(vlSelf->__Vcoverage[897]);
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[1215]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[1216]);
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
        ++(vlSelf->__Vcoverage[1217]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[1218]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[1220]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[1221]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
         & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U))) {
        ++(vlSelf->__Vcoverage[1222]);
    }
    ++(vlSelf->__Vcoverage[1223]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem
            [(0x0000001fU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg))];
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 1U;
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[1225]);
        } else {
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg)));
            ++(vlSelf->__Vcoverage[1224]);
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty)))) {
            ++(vlSelf->__Vcoverage[1226]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[1228]);
        }
        ++(vlSelf->__Vcoverage[1229]);
    } else {
        ++(vlSelf->__Vcoverage[1230]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg = 0U;
        ++(vlSelf->__Vcoverage[1235]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1236]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[1231]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[1232]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[1233]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
         & (3U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[1234]);
    }
    ++(vlSelf->__Vcoverage[1237]);
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
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg 
        = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next;
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
        VL_COV_TOGGLE_CHG_ST_I(2, vlSelf->__Vcoverage + 737, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg);
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
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 437, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tdata);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tdata 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U] 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 601, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U];
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 669, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]);
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
        VL_COV_TOGGLE_CHG_ST_I(2, vlSelf->__Vcoverage + 1040, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg);
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
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1091, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((0U != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U] 
                ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1004, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U];
    }
    if ((0U != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1022, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 517, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 900, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 271, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 273, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 275, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 307, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 525, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 589, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg = 0U;
    ++(vlSelf->__Vcoverage[792]);
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg))) {
        ++(vlSelf->__Vcoverage[849]);
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis;
        __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 
            = (7U & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg));
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 1U;
        ++(vlSelf->__Vcoverage[852]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg)));
        if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)) 
                   & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg))))) {
            ++(vlSelf->__Vcoverage[853]);
        }
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg)));
        ++(vlSelf->__Vcoverage[856]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg)))) {
            ++(vlSelf->__Vcoverage[857]);
        }
        ++(vlSelf->__Vcoverage[865]);
    } else {
        ++(vlSelf->__Vcoverage[859]);
        ++(vlSelf->__Vcoverage[861]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg)))) {
            ++(vlSelf->__Vcoverage[862]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg) {
            ++(vlSelf->__Vcoverage[863]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
            ++(vlSelf->__Vcoverage[864]);
        }
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg))) {
        ++(vlSelf->__Vcoverage[866]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[867]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[868]);
    }
    ++(vlSelf->__Vcoverage[870]);
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[871]);
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
        ++(vlSelf->__Vcoverage[872]);
    }
    ++(vlSelf->__Vcoverage[794]);
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[795]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[796]);
    }
    ++(vlSelf->__Vcoverage[873]);
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 912, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 988, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg = 0U;
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)))) {
            ++(vlSelf->__Vcoverage[1129]);
        }
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg 
            = (1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)));
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg) {
            ++(vlSelf->__Vcoverage[1130]);
        }
        ++(vlSelf->__Vcoverage[1131]);
    } else {
        ++(vlSelf->__Vcoverage[1132]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1189]);
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis;
        __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 
            = (0x0000001fU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg));
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 1U;
        ++(vlSelf->__Vcoverage[1192]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg 
            = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg)));
        if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
                   & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg))))) {
            ++(vlSelf->__Vcoverage[1193]);
        }
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg 
            = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg)));
        ++(vlSelf->__Vcoverage[1196]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg)))) {
            ++(vlSelf->__Vcoverage[1197]);
        }
        ++(vlSelf->__Vcoverage[1205]);
    } else {
        ++(vlSelf->__Vcoverage[1199]);
        ++(vlSelf->__Vcoverage[1201]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg)))) {
            ++(vlSelf->__Vcoverage[1202]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg) {
            ++(vlSelf->__Vcoverage[1203]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
            ++(vlSelf->__Vcoverage[1204]);
        }
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1206]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)))) {
        ++(vlSelf->__Vcoverage[1207]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[1208]);
    }
    ++(vlSelf->__Vcoverage[1210]);
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[1211]);
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
        ++(vlSelf->__Vcoverage[1212]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1133]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)))) {
        ++(vlSelf->__Vcoverage[1135]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[1136]);
    }
    ++(vlSelf->__Vcoverage[1213]);
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
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 533, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_overflow);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_overflow 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 535, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 537, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 748, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 751, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 754, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 757, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg;
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 339, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 580, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg) 
           == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg));
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 571, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
    }
    if ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
          == (8U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg))) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full_wr))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 746, 
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
        ++(vlSelf->__Vcoverage[1772]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1773]);
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
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word) {
        ++(vlSelf->__Vcoverage[1774]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_user_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int;
    } else {
        ++(vlSelf->__Vcoverage[1775]);
    }
    ++(vlSelf->__Vcoverage[1776]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 924, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 926, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 928, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1051, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1054, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1060, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1057, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 975, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg) 
           == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg));
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 962, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
    }
    if ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
          == (0x20U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg))) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full_wr))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1049, 
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
        ++(vlSelf->__Vcoverage[1917]);
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
        ++(vlSelf->__Vcoverage[1915]);
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
        ++(vlSelf->__Vcoverage[1916]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp) {
        ++(vlSelf->__Vcoverage[1918]);
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
        ++(vlSelf->__Vcoverage[1919]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[1920]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1921]);
    }
    ++(vlSelf->__Vcoverage[1922]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 744, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty;
    }
    if ((1U ^ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) 
               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 269, 
                               (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)), vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready 
            = (1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 742, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1047, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty;
    }
    if ((1U ^ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 263, 
                               (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)), vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready 
            = (1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)));
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1045, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 1240, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1255, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1336, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1402, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 35, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 267, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_data_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1468, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_data_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_data_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_keep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1485, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_keep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_keep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_id_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1488, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_id_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_id_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_dest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1505, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_dest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_dest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_user_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_user_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1522, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_user_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_user_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_user_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_user_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1778, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1785, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1802, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1819, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1822, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1839, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1847, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1850, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1867, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1884, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 245, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg;
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) {
        ++(vlSelf->__Vcoverage[1088]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg) {
        ++(vlSelf->__Vcoverage[1089]);
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg))))) {
        ++(vlSelf->__Vcoverage[1090]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 265, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis 
        = ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) 
             | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)) 
            << 8U) | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg));
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1620, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 261, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1842, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_axis)))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1070, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_axis);
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
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1659, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early);
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
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1659, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early);
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
