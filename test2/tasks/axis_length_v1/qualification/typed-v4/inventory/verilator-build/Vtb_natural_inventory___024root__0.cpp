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
        ++(vlSelf->__Vcoverage[864]);
        ++(vlSelf->__Vcoverage[866]);
        ++(vlSelf->__Vcoverage[868]);
        ++(vlSelf->__Vcoverage[870]);
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
        ++(vlSelf->__Vcoverage[208]);
        ++(vlSelf->__Vcoverage[209]);
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
                                             "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/qualification/typed-v4/inventory/tb_natural_inventory.sv", 
                                             30);
        vlSelfRef.tb_natural_inventory__DOT__clk = 1U;
        co_await vlSelfRef.__VdlySched.delay(0x0000000000001388ULL, 
                                             nullptr, 
                                             "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/qualification/typed-v4/inventory/tb_natural_inventory.sv", 
                                             30);
        tb_natural_inventory__DOT__unnamedblk1__DOT__i 
            = ((IData)(1U) + tb_natural_inventory__DOT__unnamedblk1__DOT__i);
        ++(vlSelf->__Vcoverage[122]);
    }
    VL_WRITEF_NX("INVENTORY_OK cycles=8\n",0);
    VL_FINISH_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/qualification/typed-v4/inventory/tb_natural_inventory.sv", 32, "");
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
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 629, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_early);
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
    ++(vlSelf->__Vcoverage[643]);
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
            ++(vlSelf->__Vcoverage[649]);
            ++(vlSelf->__Vcoverage[650]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[648]);
            ++(vlSelf->__Vcoverage[650]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[651]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[652]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[653]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[654]);
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
                        ++(vlSelf->__Vcoverage[655]);
                    }
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                        ++(vlSelf->__Vcoverage[656]);
                    }
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                        ++(vlSelf->__Vcoverage[657]);
                    }
                    ++(vlSelf->__Vcoverage[658]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 3U;
                    ++(vlSelf->__Vcoverage[659]);
                }
                ++(vlSelf->__Vcoverage[672]);
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
                            ++(vlSelf->__Vcoverage[663]);
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
                                ++(vlSelf->__Vcoverage[660]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                                ++(vlSelf->__Vcoverage[661]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                                ++(vlSelf->__Vcoverage[662]);
                            }
                            ++(vlSelf->__Vcoverage[664]);
                        }
                        ++(vlSelf->__Vcoverage[668]);
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
                            ++(vlSelf->__Vcoverage[665]);
                        }
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                            ++(vlSelf->__Vcoverage[666]);
                        }
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                            ++(vlSelf->__Vcoverage[667]);
                        }
                        ++(vlSelf->__Vcoverage[669]);
                    }
                    ++(vlSelf->__Vcoverage[670]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 1U;
                    ++(vlSelf->__Vcoverage[671]);
                }
                ++(vlSelf->__Vcoverage[673]);
            }
            ++(vlSelf->__Vcoverage[674]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 0U;
            ++(vlSelf->__Vcoverage[675]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready))) {
            ++(vlSelf->__Vcoverage[644]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg)))) {
            ++(vlSelf->__Vcoverage[645]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg) 
             & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
            ++(vlSelf->__Vcoverage[646]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
            ++(vlSelf->__Vcoverage[647]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[676]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[677]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[678]);
        }
        ++(vlSelf->__Vcoverage[679]);
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
            ++(vlSelf->__Vcoverage[680]);
            ++(vlSelf->__Vcoverage[682]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg)));
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[683]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[684]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[685]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[686]);
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
                        ++(vlSelf->__Vcoverage[687]);
                    }
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                          + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                        ++(vlSelf->__Vcoverage[688]);
                    }
                    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                        ++(vlSelf->__Vcoverage[689]);
                    }
                    ++(vlSelf->__Vcoverage[690]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int = 0U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word = 1U;
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 3U;
                    ++(vlSelf->__Vcoverage[691]);
                }
                ++(vlSelf->__Vcoverage[704]);
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
                            ++(vlSelf->__Vcoverage[695]);
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
                                ++(vlSelf->__Vcoverage[692]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                                ++(vlSelf->__Vcoverage[693]);
                            }
                            if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                                ++(vlSelf->__Vcoverage[694]);
                            }
                            ++(vlSelf->__Vcoverage[696]);
                        }
                        ++(vlSelf->__Vcoverage[700]);
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
                            ++(vlSelf->__Vcoverage[697]);
                        }
                        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next 
                            = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                                              + vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt));
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                            ++(vlSelf->__Vcoverage[698]);
                        }
                        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                            ++(vlSelf->__Vcoverage[699]);
                        }
                        ++(vlSelf->__Vcoverage[701]);
                    }
                    ++(vlSelf->__Vcoverage[702]);
                } else {
                    vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 1U;
                    ++(vlSelf->__Vcoverage[703]);
                }
                ++(vlSelf->__Vcoverage[705]);
            }
            ++(vlSelf->__Vcoverage[706]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 1U;
            ++(vlSelf->__Vcoverage[707]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[708]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[709]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[710]);
        }
        ++(vlSelf->__Vcoverage[711]);
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
                ++(vlSelf->__Vcoverage[712]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next = 0U;
                ++(vlSelf->__Vcoverage[713]);
            }
            if ((1U < (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg))) {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg) 
                                      - (IData)(1U)));
                ++(vlSelf->__Vcoverage[714]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next = 0U;
                ++(vlSelf->__Vcoverage[715]);
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
                    ++(vlSelf->__Vcoverage[716]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                    ++(vlSelf->__Vcoverage[717]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                    ++(vlSelf->__Vcoverage[718]);
                }
                ++(vlSelf->__Vcoverage[719]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 2U;
                ++(vlSelf->__Vcoverage[720]);
            }
            ++(vlSelf->__Vcoverage[721]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 2U;
            ++(vlSelf->__Vcoverage[722]);
        }
        ++(vlSelf->__Vcoverage[723]);
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
            ++(vlSelf->__Vcoverage[728]);
            ++(vlSelf->__Vcoverage[729]);
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt = 1U;
            ++(vlSelf->__Vcoverage[727]);
            ++(vlSelf->__Vcoverage[729]);
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
                    ++(vlSelf->__Vcoverage[730]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
                    ++(vlSelf->__Vcoverage[731]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early)))) {
                    ++(vlSelf->__Vcoverage[732]);
                }
                ++(vlSelf->__Vcoverage[733]);
            } else {
                vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 3U;
                ++(vlSelf->__Vcoverage[734]);
            }
            ++(vlSelf->__Vcoverage[735]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next = 3U;
            ++(vlSelf->__Vcoverage[736]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last))) {
            ++(vlSelf->__Vcoverage[724]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_last)))) {
            ++(vlSelf->__Vcoverage[725]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[726]);
        }
        if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid))) {
            ++(vlSelf->__Vcoverage[737]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__s_valid)))) {
            ++(vlSelf->__Vcoverage[738]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg)))) {
            ++(vlSelf->__Vcoverage[739]);
        }
        ++(vlSelf->__Vcoverage[740]);
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg) 
         & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__h_ready)))) {
        ++(vlSelf->__Vcoverage[634]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__h_ready) {
        ++(vlSelf->__Vcoverage[635]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg)))) {
        ++(vlSelf->__Vcoverage[636]);
    }
    ++(vlSelf->__Vcoverage[741]);
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 217, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_last_word))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 223, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_last_word);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_last_word 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 258, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 339, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 405, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdata_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 570, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdata_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdata_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 586, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tlast_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 593, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tlast_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tlast_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 595, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_int)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 611, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 627, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tready_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 632, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tready_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tready_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 496, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 499, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 502, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 505, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length_next)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 538, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next;
    }
    if ((0U != ((IData)(tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tdata_masked)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 290, tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tdata_masked);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tdata_masked 
            = tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tdata_masked;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_int))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 588, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_int);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_int 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int;
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int))))) {
        ++(vlSelf->__Vcoverage[871]);
    }
    if ((1U & ((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg)) 
               & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg))))) {
        ++(vlSelf->__Vcoverage[872]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        ++(vlSelf->__Vcoverage[873]);
    }
    if ((((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
          & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int))) {
        ++(vlSelf->__Vcoverage[874]);
    }
    if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
         & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg))) {
        ++(vlSelf->__Vcoverage[875]);
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
            ++(vlSelf->__Vcoverage[876]);
        } else {
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next 
                = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int;
            vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp = 1U;
            ++(vlSelf->__Vcoverage[877]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg)))) {
            ++(vlSelf->__Vcoverage[878]);
        }
        if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
            ++(vlSelf->__Vcoverage[879]);
        }
        if (((~ (IData)(vlSelfRef.tb_natural_inventory__DOT__m_ready)) 
             & (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg))) {
            ++(vlSelf->__Vcoverage[880]);
        }
        ++(vlSelf->__Vcoverage[883]);
    } else if (vlSelfRef.tb_natural_inventory__DOT__m_ready) {
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output = 1U;
        ++(vlSelf->__Vcoverage[881]);
    } else {
        ++(vlSelf->__Vcoverage[882]);
    }
    ++(vlSelf->__Vcoverage[884]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 752, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_next))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 815, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_next);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_next 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 857, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_output);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_output 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_temp))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 859, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_temp);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_temp 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_temp_to_output))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 861, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_temp_to_output);
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
        ++(vlSelf->__Vcoverage[887]);
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
        ++(vlSelf->__Vcoverage[885]);
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
        ++(vlSelf->__Vcoverage[886]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp) {
        ++(vlSelf->__Vcoverage[888]);
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
        ++(vlSelf->__Vcoverage[889]);
    }
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[890]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[891]);
    }
    ++(vlSelf->__Vcoverage[892]);
    if (vlSelfRef.tb_natural_inventory__DOT__rst) {
        ++(vlSelf->__Vcoverage[742]);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg = 0U;
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg = 0U;
    } else {
        ++(vlSelf->__Vcoverage[743]);
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
        ++(vlSelf->__Vcoverage[744]);
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
        ++(vlSelf->__Vcoverage[745]);
    }
    ++(vlSelf->__Vcoverage[746]);
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 50, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_pad 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 52, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_truncate 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 54, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 86, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_original_length 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 26, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_data 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 748, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 44, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_last 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 755, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 772, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 789, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdata_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 792, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdata_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdata_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tkeep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 809, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tkeep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tkeep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tlast_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 817, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tlast_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tlast_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tid_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 820, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 837, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tuser_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 854, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tuser_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tuser_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 590, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 42, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__m_valid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 812, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(3, vlSelf->__Vcoverage + 210, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 225, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 306, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(16, vlSelf->__Vcoverage + 372, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 24, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__s_ready 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 48, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg, vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid);
        vlSelfRef.tb_natural_inventory__DOT____Vtogcov__h_valid 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_data_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 438, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_data_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_data_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_keep_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 455, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_keep_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_keep_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_id_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 458, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_id_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_id_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg;
    }
    if ((0U != ((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg) 
                ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_dest_reg)))) {
        VL_COV_TOGGLE_CHG_ST_I(8, vlSelf->__Vcoverage + 475, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_dest_reg);
        vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_dest_reg 
            = vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg;
    }
    if (((IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_user_reg) 
         ^ (IData)(vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_user_reg))) {
        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 492, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_user_reg, vlSelfRef.tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_user_reg);
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
        VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/qualification/typed-v4/inventory/tb_natural_inventory.sv", 2, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
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
            VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/qualification/typed-v4/inventory/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/qualification/typed-v4/inventory/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vtb_natural_inventory___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/tasks/axis_length_v1/qualification/typed-v4/inventory/tb_natural_inventory.sv", 2, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
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
