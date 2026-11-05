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
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 124, 1U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep = 1U;
        }
        if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid))) {
            VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 126, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid = 0U;
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tuser) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 142, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tuser);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tuser = 0U;
        }
        if ((0U != (4U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min)))) {
            VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 144, 4U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min = 4U;
        }
        if ((0U != (8U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max)))) {
            VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 176, 8U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max = 8U;
        }
        ++(vlSelf->__Vcoverage[729]);
        ++(vlSelf->__Vcoverage[731]);
        ++(vlSelf->__Vcoverage[733]);
        ++(vlSelf->__Vcoverage[735]);
        ++(vlSelf->__Vcoverage[737]);
        ++(vlSelf->__Vcoverage[739]);
        ++(vlSelf->__Vcoverage[746]);
        ++(vlSelf->__Vcoverage[744]);
        ++(vlSelf->__Vcoverage[751]);
        ++(vlSelf->__Vcoverage[749]);
        if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep))) {
            VL_COV_TOGGLE_CHG_ST_I(5, vlSelf->__Vcoverage + 370, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tkeep = 0U;
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 380, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tlast = 0U;
        }
        if ((0U != (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid))) {
            VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 382, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tid = 0U;
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 398, 0U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tuser = 0U;
        }
        if ((0U != (0x0000001fU & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep))))) {
            VL_COV_TOGGLE_CHG_ST_I(5, vlSelf->__Vcoverage + 468, 0x1fU, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tkeep = 0x1fU;
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready)))) {
            VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 740, 1U, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__pipe_ready = 1U;
        }
        ++(vlSelf->__Vcoverage[1032]);
        ++(vlSelf->__Vcoverage[1073]);
        ++(vlSelf->__Vcoverage[1074]);
        ++(vlSelf->__Vcoverage[1077]);
        ++(vlSelf->__Vcoverage[1079]);
        ++(vlSelf->__Vcoverage[1081]);
        ++(vlSelf->__Vcoverage[1086]);
        ++(vlSelf->__Vcoverage[1083]);
        ++(vlSelf->__Vcoverage[1084]);
        ++(vlSelf->__Vcoverage[1091]);
        ++(vlSelf->__Vcoverage[1088]);
        ++(vlSelf->__Vcoverage[1089]);
        ++(vlSelf->__Vcoverage[1857]);
        ++(vlSelf->__Vcoverage[1859]);
        ++(vlSelf->__Vcoverage[1861]);
        ++(vlSelf->__Vcoverage[1863]);
        ++(vlSelf->__Vcoverage[502]);
        ++(vlSelf->__Vcoverage[506]);
        ++(vlSelf->__Vcoverage[510]);
        ++(vlSelf->__Vcoverage[515]);
        ++(vlSelf->__Vcoverage[520]);
        ++(vlSelf->__Vcoverage[525]);
        ++(vlSelf->__Vcoverage[529]);
        ++(vlSelf->__Vcoverage[505]);
        ++(vlSelf->__Vcoverage[509]);
        ++(vlSelf->__Vcoverage[514]);
        ++(vlSelf->__Vcoverage[519]);
        ++(vlSelf->__Vcoverage[523]);
        ++(vlSelf->__Vcoverage[524]);
        ++(vlSelf->__Vcoverage[527]);
        ++(vlSelf->__Vcoverage[528]);
        ++(vlSelf->__Vcoverage[532]);
        ++(vlSelf->__Vcoverage[533]);
        ++(vlSelf->__Vcoverage[893]);
        ++(vlSelf->__Vcoverage[897]);
        ++(vlSelf->__Vcoverage[901]);
        ++(vlSelf->__Vcoverage[906]);
        ++(vlSelf->__Vcoverage[911]);
        ++(vlSelf->__Vcoverage[916]);
        ++(vlSelf->__Vcoverage[920]);
        ++(vlSelf->__Vcoverage[895]);
        ++(vlSelf->__Vcoverage[896]);
        ++(vlSelf->__Vcoverage[900]);
        ++(vlSelf->__Vcoverage[905]);
        ++(vlSelf->__Vcoverage[910]);
        ++(vlSelf->__Vcoverage[914]);
        ++(vlSelf->__Vcoverage[915]);
        ++(vlSelf->__Vcoverage[918]);
        ++(vlSelf->__Vcoverage[919]);
        ++(vlSelf->__Vcoverage[922]);
        ++(vlSelf->__Vcoverage[923]);
        ++(vlSelf->__Vcoverage[924]);
        ++(vlSelf->__Vcoverage[1201]);
        ++(vlSelf->__Vcoverage[1202]);
    }
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
    vlSelfRef.tb_natural_inventory__DOT__clk = 0U;
    vlSelfRef.tb_natural_inventory__DOT__s_data = 0U;
    vlSelfRef.tb_natural_inventory__DOT__s_valid = 0U;
    vlSelfRef.tb_natural_inventory__DOT__s_last = 0U;
    vlSelfRef.tb_natural_inventory__DOT__m_ready = 1U;
    vlSelfRef.tb_natural_inventory__DOT__h_ready = 1U;
    vlSelfRef.tb_natural_inventory__DOT__rst = 1U;
    tb_natural_inventory__DOT__unnamedblk1__DOT__i = 0U;
    while (VL_GTS_III(32, 8U, tb_natural_inventory__DOT__unnamedblk1__DOT__i)) {
        vlSelfRef.tb_natural_inventory__DOT__clk = 0U;
        if ((2U == tb_natural_inventory__DOT__unnamedblk1__DOT__i)) {
            vlSelfRef.tb_natural_inventory__DOT__rst = 0U;
            ++(vlSelf->__Vcoverage[120]);
        } else {
            ++(vlSelf->__Vcoverage[121]);
        }
        co_await vlSelfRef.__VdlySched.delay(0x0000000000001388ULL, 
                                             nullptr, 
                                             "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_fifo_v1/qualification/typed-v5/inventory/tb_natural_inventory.sv", 
                                             30);
        vlSelfRef.tb_natural_inventory__DOT__clk = 1U;
        co_await vlSelfRef.__VdlySched.delay(0x0000000000001388ULL, 
                                             nullptr, 
                                             "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_fifo_v1/qualification/typed-v5/inventory/tb_natural_inventory.sv", 
                                             30);
        tb_natural_inventory__DOT__unnamedblk1__DOT__i 
            = ((IData)(1U) + tb_natural_inventory__DOT__unnamedblk1__DOT__i);
        ++(vlSelf->__Vcoverage[122]);
    }
    VL_WRITEF_NX("INVENTORY_OK cycles=8\n",0);
    VL_FINISH_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_fifo_v1/qualification/typed-v5/inventory/tb_natural_inventory.sv", 32, "");
    ++(vlSelf->__Vcoverage[123]);
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
    ++(vlSelf->__Vcoverage[1636]);
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
            ++(vlSelf->__Vcoverage[1642]);
            ++(vlSelf->__Vcoverage[1643]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[1641]);
            ++(vlSelf->__Vcoverage[1643]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1644]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1645]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1646]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1647]);
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
                        ++(vlSelf->__Vcoverage[1648]);
                    }
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                        ++(vlSelf->__Vcoverage[1649]);
                    }
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                        ++(vlSelf->__Vcoverage[1650]);
                    }
                    ++(vlSelf->__Vcoverage[1651]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                    ++(vlSelf->__Vcoverage[1652]);
                }
                ++(vlSelf->__Vcoverage[1665]);
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
                            ++(vlSelf->__Vcoverage[1656]);
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
                                ++(vlSelf->__Vcoverage[1653]);
                            }
                            if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                                ++(vlSelf->__Vcoverage[1654]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                                ++(vlSelf->__Vcoverage[1655]);
                            }
                            ++(vlSelf->__Vcoverage[1657]);
                        }
                        ++(vlSelf->__Vcoverage[1661]);
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
                            ++(vlSelf->__Vcoverage[1658]);
                        }
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                            ++(vlSelf->__Vcoverage[1659]);
                        }
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                            ++(vlSelf->__Vcoverage[1660]);
                        }
                        ++(vlSelf->__Vcoverage[1662]);
                    }
                    ++(vlSelf->__Vcoverage[1663]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
                    ++(vlSelf->__Vcoverage[1664]);
                }
                ++(vlSelf->__Vcoverage[1666]);
            }
            ++(vlSelf->__Vcoverage[1667]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
            ++(vlSelf->__Vcoverage[1668]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
            ++(vlSelf->__Vcoverage[1637]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
            ++(vlSelf->__Vcoverage[1638]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full))) {
            ++(vlSelf->__Vcoverage[1639]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
            ++(vlSelf->__Vcoverage[1640]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[1669]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1670]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[1671]);
        }
        ++(vlSelf->__Vcoverage[1672]);
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
            ++(vlSelf->__Vcoverage[1673]);
            ++(vlSelf->__Vcoverage[1675]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1676]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1677]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1678]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1679]);
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
                        ++(vlSelf->__Vcoverage[1680]);
                    }
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                        ++(vlSelf->__Vcoverage[1681]);
                    }
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                        ++(vlSelf->__Vcoverage[1682]);
                    }
                    ++(vlSelf->__Vcoverage[1683]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                    ++(vlSelf->__Vcoverage[1684]);
                }
                ++(vlSelf->__Vcoverage[1697]);
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
                            ++(vlSelf->__Vcoverage[1688]);
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
                                ++(vlSelf->__Vcoverage[1685]);
                            }
                            if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                                ++(vlSelf->__Vcoverage[1686]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                                ++(vlSelf->__Vcoverage[1687]);
                            }
                            ++(vlSelf->__Vcoverage[1689]);
                        }
                        ++(vlSelf->__Vcoverage[1693]);
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
                            ++(vlSelf->__Vcoverage[1690]);
                        }
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                            ++(vlSelf->__Vcoverage[1691]);
                        }
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                            ++(vlSelf->__Vcoverage[1692]);
                        }
                        ++(vlSelf->__Vcoverage[1694]);
                    }
                    ++(vlSelf->__Vcoverage[1695]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
                    ++(vlSelf->__Vcoverage[1696]);
                }
                ++(vlSelf->__Vcoverage[1698]);
            }
            ++(vlSelf->__Vcoverage[1699]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
            ++(vlSelf->__Vcoverage[1700]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[1701]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1702]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[1703]);
        }
        ++(vlSelf->__Vcoverage[1704]);
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
                ++(vlSelf->__Vcoverage[1705]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1706]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[1707]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[1708]);
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
                    ++(vlSelf->__Vcoverage[1709]);
                }
                if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                    ++(vlSelf->__Vcoverage[1710]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                    ++(vlSelf->__Vcoverage[1711]);
                }
                ++(vlSelf->__Vcoverage[1712]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                ++(vlSelf->__Vcoverage[1713]);
            }
            ++(vlSelf->__Vcoverage[1714]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
            ++(vlSelf->__Vcoverage[1715]);
        }
        ++(vlSelf->__Vcoverage[1716]);
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
            ++(vlSelf->__Vcoverage[1721]);
            ++(vlSelf->__Vcoverage[1722]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[1720]);
            ++(vlSelf->__Vcoverage[1722]);
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
                    ++(vlSelf->__Vcoverage[1723]);
                }
                if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
                    ++(vlSelf->__Vcoverage[1724]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early)))) {
                    ++(vlSelf->__Vcoverage[1725]);
                }
                ++(vlSelf->__Vcoverage[1726]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                ++(vlSelf->__Vcoverage[1727]);
            }
            ++(vlSelf->__Vcoverage[1728]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
            ++(vlSelf->__Vcoverage[1729]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last))) {
            ++(vlSelf->__Vcoverage[1717]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last)))) {
            ++(vlSelf->__Vcoverage[1718]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1719]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[1730]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[1731]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[1732]);
        }
        ++(vlSelf->__Vcoverage[1733]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full))) {
        ++(vlSelf->__Vcoverage[1627]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)))) {
        ++(vlSelf->__Vcoverage[1628]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[1629]);
    }
    ++(vlSelf->__Vcoverage[1734]);
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 1210, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_last_word))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1216, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_last_word);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_last_word 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1251, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1332, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1398, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1563, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdata_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1579, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1586, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1588, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1604, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1620, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1625, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1489, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_valid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1492, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_pad_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1495, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_truncate_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1498, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_length_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_original_length_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1531, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_original_length_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__status_frame_original_length_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next;
    }
    if ((0U != ((IData)(tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1283, tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__s_axis_tdata_masked 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1581, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int))))) {
        ++(vlSelf->__Vcoverage[1864]);
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))))) {
        ++(vlSelf->__Vcoverage[1865]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)))) {
        ++(vlSelf->__Vcoverage[1866]);
    }
    if ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
          & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int))) {
        ++(vlSelf->__Vcoverage[1867]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1868]);
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
            ++(vlSelf->__Vcoverage[1869]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp = 1U;
            ++(vlSelf->__Vcoverage[1870]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)))) {
            ++(vlSelf->__Vcoverage[1871]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)))) {
            ++(vlSelf->__Vcoverage[1872]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
            ++(vlSelf->__Vcoverage[1873]);
        }
        ++(vlSelf->__Vcoverage[1876]);
    } else if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[1875]);
    } else {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output = 1U;
        ++(vlSelf->__Vcoverage[1874]);
    }
    ++(vlSelf->__Vcoverage[1877]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1745, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1808, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1850, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_output 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_output;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1852, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_int_to_temp 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_temp_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1854, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_temp_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__store_axis_temp_to_output);
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
    ++(vlSelf->__Vcoverage[837]);
    ++(vlSelf->__Vcoverage[1177]);
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
        ++(vlSelf->__Vcoverage[838]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[839]);
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
        ++(vlSelf->__Vcoverage[840]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[841]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[843]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[844]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)) 
         & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U))) {
        ++(vlSelf->__Vcoverage[845]);
    }
    ++(vlSelf->__Vcoverage[846]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem
            [(7U & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg))];
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 1U;
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[848]);
        } else {
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg)));
            ++(vlSelf->__Vcoverage[847]);
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty)))) {
            ++(vlSelf->__Vcoverage[849]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[851]);
        }
        ++(vlSelf->__Vcoverage[852]);
    } else {
        ++(vlSelf->__Vcoverage[853]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg = 0U;
        ++(vlSelf->__Vcoverage[858]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[859]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[854]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[855]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[856]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)) 
         & (3U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[857]);
    }
    ++(vlSelf->__Vcoverage[860]);
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[1178]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[1179]);
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
        ++(vlSelf->__Vcoverage[1180]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    } else {
        ++(vlSelf->__Vcoverage[1181]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[1183]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[1184]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
         & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U))) {
        ++(vlSelf->__Vcoverage[1185]);
    }
    ++(vlSelf->__Vcoverage[1186]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem
            [(0x0000001fU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg))];
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 1U;
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[1188]);
        } else {
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg)));
            ++(vlSelf->__Vcoverage[1187]);
            __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty)))) {
            ++(vlSelf->__Vcoverage[1189]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty) {
            ++(vlSelf->__Vcoverage[1191]);
        }
        ++(vlSelf->__Vcoverage[1192]);
    } else {
        ++(vlSelf->__Vcoverage[1193]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg = 0U;
        ++(vlSelf->__Vcoverage[1198]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1199]);
    }
    if ((1U & (~ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U)))) {
        ++(vlSelf->__Vcoverage[1194]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[1195]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[1196]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
         & (3U == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))) {
        ++(vlSelf->__Vcoverage[1197]);
    }
    ++(vlSelf->__Vcoverage[1200]);
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
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 48, 
                               ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                >> 1U), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid 
            = (1U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                     >> 1U));
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(2, vlSelf->__Vcoverage + 700, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    }
    if ((1U & ((IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                        >> 0x00000021U)) ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 50, (IData)(
                                                                    (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                                     >> 0x00000021U)), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad 
            = (1U & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                             >> 0x00000021U)));
    }
    if ((1U & ((IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                        >> 0x00000020U)) ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 52, (IData)(
                                                                    (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                                     >> 0x00000020U)), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate 
            = (1U & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                             >> 0x00000020U)));
    }
    if ((0U != (0x0000ffffU & ((IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                        >> 0x00000010U)) 
                               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length))))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 54, (IData)(
                                                                     (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                                      >> 0x00000010U)), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length 
            = (0x0000ffffU & (IData)((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                      >> 0x00000010U)));
    }
    if ((0U != (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U]) 
                               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length))))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 86, (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U]), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length 
            = (0x0000ffffU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U]));
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tdata))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 400, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tdata);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_tdata 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U] 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 564, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U];
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 632, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((IData)((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U) ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 42, 
                               ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                >> 1U), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid 
            = (1U & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                     >> 1U));
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(2, vlSelf->__Vcoverage + 1003, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_tvalid_pipe_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    }
    if ((0U != (0x000000ffU & (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data))))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 26, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data 
            = (0x000000ffU & vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U]);
    }
    if ((1U & ((vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                >> 8U) ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 44, 
                               (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                >> 8U), vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last 
            = (1U & (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                     >> 8U));
    }
    if ((0U != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis)))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1054, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((0U != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U] 
                ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 967, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[0U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U];
    }
    if ((0U != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 985, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U], vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__m_axis_pipe_reg[1U] 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U];
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 480, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 863, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 234, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 236, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 238, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 270, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 488, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_depth_commit 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__depth_commit_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 552, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__rd_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg = 0U;
    ++(vlSelf->__Vcoverage[755]);
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg))) {
        ++(vlSelf->__Vcoverage[812]);
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis;
        __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 
            = (7U & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg));
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 1U;
        ++(vlSelf->__Vcoverage[815]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg)));
        if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)) 
                   & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg))))) {
            ++(vlSelf->__Vcoverage[816]);
        }
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg)));
        ++(vlSelf->__Vcoverage[819]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg)))) {
            ++(vlSelf->__Vcoverage[820]);
        }
        ++(vlSelf->__Vcoverage[828]);
    } else {
        ++(vlSelf->__Vcoverage[822]);
        ++(vlSelf->__Vcoverage[824]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg)))) {
            ++(vlSelf->__Vcoverage[825]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg) {
            ++(vlSelf->__Vcoverage[826]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
            ++(vlSelf->__Vcoverage[827]);
        }
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg))) {
        ++(vlSelf->__Vcoverage[829]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[830]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[831]);
    }
    ++(vlSelf->__Vcoverage[833]);
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[834]);
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
        ++(vlSelf->__Vcoverage[835]);
    }
    ++(vlSelf->__Vcoverage[757]);
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[758]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[759]);
    }
    ++(vlSelf->__Vcoverage[836]);
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 875, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_depth_commit 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__depth_commit_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 951, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__rd_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg = 0U;
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg = 0U;
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)))) {
            ++(vlSelf->__Vcoverage[1092]);
        }
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg 
            = (1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)));
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg) {
            ++(vlSelf->__Vcoverage[1093]);
        }
        ++(vlSelf->__Vcoverage[1094]);
    } else {
        ++(vlSelf->__Vcoverage[1095]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1152]);
        __VdlyVal__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis;
        __VdlyDim0__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 
            = (0x0000001fU & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg));
        __VdlySet__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 1U;
        ++(vlSelf->__Vcoverage[1155]);
        __Vdly__tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg 
            = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg)));
        if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
                   & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg))))) {
            ++(vlSelf->__Vcoverage[1156]);
        }
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg 
            = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg)));
        ++(vlSelf->__Vcoverage[1159]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg)))) {
            ++(vlSelf->__Vcoverage[1160]);
        }
        ++(vlSelf->__Vcoverage[1168]);
    } else {
        ++(vlSelf->__Vcoverage[1162]);
        ++(vlSelf->__Vcoverage[1164]);
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg)))) {
            ++(vlSelf->__Vcoverage[1165]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg) {
            ++(vlSelf->__Vcoverage[1166]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
            ++(vlSelf->__Vcoverage[1167]);
        }
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1169]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)))) {
        ++(vlSelf->__Vcoverage[1170]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[1171]);
    }
    ++(vlSelf->__Vcoverage[1173]);
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[1174]);
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
        ++(vlSelf->__Vcoverage[1175]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[1096]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)))) {
        ++(vlSelf->__Vcoverage[1098]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) {
        ++(vlSelf->__Vcoverage[1099]);
    }
    ++(vlSelf->__Vcoverage[1176]);
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
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 496, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_overflow);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_overflow 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__overflow_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 498, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_bad_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__bad_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 500, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__status_good_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__good_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 711, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 714, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__drop_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__drop_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 717, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__mark_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mark_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 720, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__send_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__send_frame_reg;
    }
    if ((0ULL != (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis 
                  ^ vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata))) {
        VL_COV_TOGGLE_CHG_ST_Q(34, vlSelf->__Vcoverage + 302, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__s_axis_tdata 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__s_axis;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 543, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg) 
           == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg));
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(4, vlSelf->__Vcoverage + 534, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__wr_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
    }
    if ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
          == (8U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg))) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full_wr))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 709, 
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
        ++(vlSelf->__Vcoverage[1735]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1736]);
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
        ++(vlSelf->__Vcoverage[1737]);
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
        ++(vlSelf->__Vcoverage[1738]);
    }
    ++(vlSelf->__Vcoverage[1739]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 887, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_overflow 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__overflow_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 889, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_bad_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__bad_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 891, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__status_good_frame 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__good_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1014, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1017, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__drop_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__drop_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1023, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__send_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__send_frame_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1020, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__mark_frame_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 938, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_commit_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty 
        = ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg) 
           == (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg));
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(6, vlSelf->__Vcoverage + 925, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__wr_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
    }
    if ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
          == (0x20U ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg))) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full_wr))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1012, 
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
        ++(vlSelf->__Vcoverage[1880]);
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
        ++(vlSelf->__Vcoverage[1878]);
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
        ++(vlSelf->__Vcoverage[1879]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_axis_int_to_temp) {
        ++(vlSelf->__Vcoverage[1881]);
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
        ++(vlSelf->__Vcoverage[1882]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[1883]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[1884]);
    }
    ++(vlSelf->__Vcoverage[1885]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 707, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__empty 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__empty;
    }
    if ((1U ^ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) 
               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 232, 
                               (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)), vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_ready 
            = (1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full)));
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 705, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT____Vtogcov__full 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__full;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1010, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__empty 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__empty;
    }
    if ((1U ^ ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
               ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready)))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 226, 
                               (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)), vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tready 
            = (1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)));
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1008, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__full 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 1203, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__state_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1218, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__frame_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1299, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__short_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 1365, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__long_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 24, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 230, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_data_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1431, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_data_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_data_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_keep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1448, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_keep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_keep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_id_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1451, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_id_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_id_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_id_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_dest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1468, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_dest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_dest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_dest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_user_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_user_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1485, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_user_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_user_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__last_word_user_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_user_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1741, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1748, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1765, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1782, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tuser_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1785, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1802, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tkeep_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1810, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1813, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 1830, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1847, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tuser_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 208, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tdata 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg;
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) {
        ++(vlSelf->__Vcoverage[1051]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg) {
        ++(vlSelf->__Vcoverage[1052]);
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg))))) {
        ++(vlSelf->__Vcoverage[1053]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 228, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tlast 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg;
    }
    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis 
        = ((((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) 
             | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)) 
            << 8U) | (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg));
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1583, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 224, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__fifo_axis_tvalid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1805, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__temp_m_axis_tvalid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_axis)))) {
        VL_COV_TOGGLE_CHG_ST_I(9, vlSelf->__Vcoverage + 1033, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__s_axis, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT____Vtogcov__s_axis);
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
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 2, vlSelfRef.tb_natural_inventory__DOT__rst, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__rst);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__rst 
                            = vlSelfRef.tb_natural_inventory__DOT__rst;
                    }
                    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__s_data) 
                                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_data)))) {
                        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 4, vlSelfRef.tb_natural_inventory__DOT__s_data, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_data);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_data 
                            = vlSelfRef.tb_natural_inventory__DOT__s_data;
                    }
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_valid))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 20, vlSelfRef.tb_natural_inventory__DOT__s_valid, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_valid);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_valid 
                            = vlSelfRef.tb_natural_inventory__DOT__s_valid;
                    }
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_last) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_last))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 22, vlSelfRef.tb_natural_inventory__DOT__s_last, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_last);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_last 
                            = vlSelfRef.tb_natural_inventory__DOT__s_last;
                    }
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_ready))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 46, vlSelfRef.tb_natural_inventory__DOT__m_ready, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_ready);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_ready 
                            = vlSelfRef.tb_natural_inventory__DOT__m_ready;
                    }
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_ready))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 118, vlSelfRef.tb_natural_inventory__DOT__h_ready, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_ready);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_ready 
                            = vlSelfRef.tb_natural_inventory__DOT__h_ready;
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
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1622, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early);
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
        VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_fifo_v1/qualification/typed-v5/inventory/tb_natural_inventory.sv", 2, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
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
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 2, vlSelfRef.tb_natural_inventory__DOT__rst, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__rst);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__rst 
                            = vlSelfRef.tb_natural_inventory__DOT__rst;
                    }
                    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__s_data) 
                                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_data)))) {
                        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 4, vlSelfRef.tb_natural_inventory__DOT__s_data, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_data);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_data 
                            = vlSelfRef.tb_natural_inventory__DOT__s_data;
                    }
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_valid))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 20, vlSelfRef.tb_natural_inventory__DOT__s_valid, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_valid);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_valid 
                            = vlSelfRef.tb_natural_inventory__DOT__s_valid;
                    }
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_last) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_last))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 22, vlSelfRef.tb_natural_inventory__DOT__s_last, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_last);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_last 
                            = vlSelfRef.tb_natural_inventory__DOT__s_last;
                    }
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_ready))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 46, vlSelfRef.tb_natural_inventory__DOT__m_ready, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_ready);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_ready 
                            = vlSelfRef.tb_natural_inventory__DOT__m_ready;
                    }
                    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready) 
                         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_ready))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 118, vlSelfRef.tb_natural_inventory__DOT__h_ready, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_ready);
                        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_ready 
                            = vlSelfRef.tb_natural_inventory__DOT__h_ready;
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
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 1622, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT____Vtogcov__m_axis_tready_int_early);
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
            VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_fifo_v1/qualification/typed-v5/inventory/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_fifo_v1/qualification/typed-v5/inventory/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vtb_natural_inventory___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_fifo_v1/qualification/typed-v5/inventory/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
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
