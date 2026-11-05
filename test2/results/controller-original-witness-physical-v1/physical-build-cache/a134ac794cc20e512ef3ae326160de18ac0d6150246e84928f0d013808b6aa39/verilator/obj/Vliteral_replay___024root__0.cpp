// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vliteral_replay.h for the primary calling header

#include "Vliteral_replay__pch.h"

VlCoroutine Vliteral_replay___024root___eval_initial__TOP__Vtiming__0(Vliteral_replay___024root* vlSelf);

void Vliteral_replay___024root___eval_initial(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_initial\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vliteral_replay___024root___eval_initial__TOP__Vtiming__0(vlSelf);
}

VlCoroutine Vliteral_replay___024root___eval_initial__TOP__Vtiming__0(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ literal_replay__DOT____VlemExpr_0;
    IData/*31:0*/ literal_replay__DOT__fd;
    literal_replay__DOT__fd = 0;
    // Body
    literal_replay__DOT____VlemExpr_0 = VL_VALUEPLUSARGS_INN(64, "INPUTS=%s"s, 
                                                             vlSelfRef.literal_replay__DOT__path);
    if (VL_UNLIKELY(((! literal_replay__DOT____VlemExpr_0)))) {
        VL_WRITEF_NX("[%0t] %%Fatal: driver.sv:23: Assertion failed in %m: Missing inputs\n",3, 'M',vlSymsp->name(),"literal_replay", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000));
        VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 23, "", false);
    }
    literal_replay__DOT__fd = VL_FOPEN_NN(vlSelfRef.literal_replay__DOT__path
                                          , "r"s);
    ;
    if (VL_UNLIKELY(((1U & (~ (0U != literal_replay__DOT__fd)))))) {
        VL_WRITEF_NX("[%0t] %%Fatal: driver.sv:24: Assertion failed in %m: Missing file\n",3, 'M',vlSymsp->name(),"literal_replay", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000));
        VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 24, "", false);
    }
    while (true) {
        vlSelfRef.literal_replay__DOT____VlemExpr_1 
            = (literal_replay__DOT__fd ? feof(VL_CVT_I_FP(literal_replay__DOT__fd)) : true);
        if (!((! vlSelfRef.literal_replay__DOT____VlemExpr_1))) break;
        vlSelfRef.literal_replay__DOT__n = VL_FSCANF_INX(literal_replay__DOT__fd,"%d %d %d %d %d %d\n",6
                                                         , '#',32,&(vlSelfRef.literal_replay__DOT__v_rst)
                                                         , '#',32,&(vlSelfRef.literal_replay__DOT__v_s_valid)
                                                         , '#',32,&(vlSelfRef.literal_replay__DOT__v_s_data)
                                                         , '#',32,&(vlSelfRef.literal_replay__DOT__v_s_last)
                                                         , '#',32,&(vlSelfRef.literal_replay__DOT__v_m_ready)
                                                         , '#',32,&(vlSelfRef.literal_replay__DOT__v_h_ready)) ;
        if (VL_UNLIKELY(((6U == vlSelfRef.literal_replay__DOT__n)))) {
            vlSelfRef.literal_replay__DOT__rst = (1U 
                                                  & vlSelfRef.literal_replay__DOT__v_rst);
            vlSelfRef.literal_replay__DOT__s_valid 
                = (1U & vlSelfRef.literal_replay__DOT__v_s_valid);
            vlSelfRef.literal_replay__DOT__s_data = 
                (0x000000ffU & vlSelfRef.literal_replay__DOT__v_s_data);
            vlSelfRef.literal_replay__DOT__s_last = 
                (1U & vlSelfRef.literal_replay__DOT__v_s_last);
            vlSelfRef.literal_replay__DOT__m_ready 
                = (1U & vlSelfRef.literal_replay__DOT__v_m_ready);
            vlSelfRef.literal_replay__DOT__h_ready 
                = (1U & vlSelfRef.literal_replay__DOT__v_h_ready);
            co_await vlSelfRef.__VdlySched.delay(0x0000000000000fa0ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 
                                                 34);
            VL_WRITEF_NX("PRE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d\n",16
                         , '~',32,vlSelfRef.literal_replay__DOT__cycle
                         , '#',1,(IData)(vlSelfRef.literal_replay__DOT__rst)
                         , '#',1,vlSelfRef.literal_replay__DOT__s_valid
                         , '#',8,(IData)(vlSelfRef.literal_replay__DOT__s_data)
                         , '#',1,vlSelfRef.literal_replay__DOT__s_last
                         , '#',1,(IData)(vlSelfRef.literal_replay__DOT__m_ready)
                         , '#',1,vlSelfRef.literal_replay__DOT__h_ready
                         , '#',1,(IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)
                         , '#',8,(0x000000ffU & vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U])
                         , '#',1,(1U & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                        >> 1U)), '#',1,
                         (1U & (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                >> 8U)), '#',1,(1U 
                                                & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                                   >> 1U))
                         , '#',1,(1U & (IData)((vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                >> 0x00000021U)))
                         , '#',1,(1U & (IData)((vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                >> 0x00000020U)))
                         , '#',16,(0x0000ffffU & (IData)(
                                                         (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                          >> 0x00000010U)))
                         , '#',16,(0x0000ffffU & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U])));
            co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 
                                                 35);
            vlSelfRef.literal_replay__DOT__clk = 1U;
            co_await vlSelfRef.__VdlySched.delay(0x00000000000007d0ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 
                                                 35);
            VL_WRITEF_NX("POST %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d\n",10
                         , '~',32,vlSelfRef.literal_replay__DOT__cycle
                         , '#',1,(IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg)
                         , '#',8,(0x000000ffU & vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U])
                         , '#',1,(1U & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                        >> 1U)), '#',1,
                         (1U & (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                >> 8U)), '#',1,(1U 
                                                & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                                                   >> 1U))
                         , '#',1,(1U & (IData)((vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                >> 0x00000021U)))
                         , '#',1,(1U & (IData)((vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                >> 0x00000020U)))
                         , '#',16,(0x0000ffffU & (IData)(
                                                         (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
                                                          >> 0x00000010U)))
                         , '#',16,(0x0000ffffU & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U])));
            co_await vlSelfRef.__VdlySched.delay(0x0000000000000bb8ULL, 
                                                 nullptr, 
                                                 "/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 
                                                 37);
            vlSelfRef.literal_replay__DOT__clk = 0U;
            vlSelfRef.literal_replay__DOT__cycle = 
                ((IData)(1U) + vlSelfRef.literal_replay__DOT__cycle);
        } else if (VL_UNLIKELY(((0xffffffffU != vlSelfRef.literal_replay__DOT__n)))) {
            VL_WRITEF_NX("[%0t] %%Fatal: driver.sv:38: Assertion failed in %m: Malformed inputs\n",3, 'M',vlSymsp->name(),"literal_replay", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 38, "", false);
        }
    }
    VL_WRITEF_NX("LITERAL_COMPLETE %0d\n",1, '~',32,vlSelfRef.literal_replay__DOT__cycle);
    VL_FINISH_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 40, "");
    co_return;
}

bool Vliteral_replay___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___trigger_anySet__act\n"); );
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

void Vliteral_replay___024root___act_sequent__TOP__0(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___act_sequent__TOP__0\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*7:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked = 0;
    CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0;
    // Body
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int = 0U;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked 
        = vlSelfRef.literal_replay__DOT__s_data;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
    if ((0U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = vlSelfRef.literal_replay__DOT__s_valid;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                if ((1U & (~ (IData)(vlSelfRef.literal_replay__DOT__s_last)))) {
                    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                }
            }
        }
    } else if ((1U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = vlSelfRef.literal_replay__DOT__s_valid;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                if ((1U & (~ (IData)(vlSelfRef.literal_replay__DOT__s_last)))) {
                    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                }
            }
        }
    } else if ((2U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int = 0U;
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 1U;
    } else if ((3U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg;
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = ((IData)(vlSelfRef.literal_replay__DOT__s_valid) 
               & (IData)(vlSelfRef.literal_replay__DOT__s_last));
    }
    vlSelfRef.__VdfgRegularize_hebeb780c_0_0 = ((((IData)(literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
                                                  << 4U) 
                                                 | (((2U 
                                                      & ((~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
                                                         << 1U)) 
                                                     | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg)) 
                                                    << 2U)) 
                                                | (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
                                                    << 1U) 
                                                   | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early 
        = (1U & (~ ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
                    & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
                       | ((IData)(literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
                          & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))))));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next 
        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
           & (~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready)));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
    if ((0U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
               & ((~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)) 
                  | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready)));
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.literal_replay__DOT__s_last;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg)));
                if (vlSelfRef.literal_replay__DOT__s_last) {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
                        = (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt 
                           > (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                }
            } else if (vlSelfRef.literal_replay__DOT__s_last) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                     > vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt)) {
                    if ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                    } else {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                               & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                            = VL_SHIFTR_III(1,1,32, 1U, 
                                            ((IData)(1U) 
                                             - ((IData)(4U) 
                                                - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg))));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    }
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                }
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
        }
    } else if ((1U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.literal_replay__DOT__s_last;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg)));
                if (vlSelfRef.literal_replay__DOT__s_last) {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
                        = (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt 
                           > (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                }
            } else if (vlSelfRef.literal_replay__DOT__s_last) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                     >= vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt)) {
                    if ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                    } else {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                               & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                            = VL_SHIFTR_III(1,1,32, 1U, 
                                            ((IData)(1U) 
                                             - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg)));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    }
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                }
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
        }
    } else if ((2U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
        if (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                       & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg)));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
        }
    } else if ((3U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.literal_replay__DOT__s_last;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            if (vlSelfRef.literal_replay__DOT__s_last) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                       & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
        }
    }
}

extern const VlUnpacked<CData/*0:0*/, 32> Vliteral_replay__ConstPool__TABLE_hea75a59c_0;
extern const VlUnpacked<CData/*0:0*/, 32> Vliteral_replay__ConstPool__TABLE_h9068cabe_0;
extern const VlUnpacked<CData/*0:0*/, 32> Vliteral_replay__ConstPool__TABLE_h70871376_0;
extern const VlUnpacked<CData/*0:0*/, 32> Vliteral_replay__ConstPool__TABLE_hb0f749ab_0;
extern const VlUnpacked<CData/*0:0*/, 32> Vliteral_replay__ConstPool__TABLE_h5ebe4fc2_0;

void Vliteral_replay___024root___nba_sequent__TOP__0(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___nba_sequent__TOP__0\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
    __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg = 0;
    CData/*1:0*/ __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0;
    CData/*5:0*/ __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
    __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg = 0;
    CData/*1:0*/ __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0;
    QData/*33:0*/ __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0;
    __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 0;
    CData/*2:0*/ __VdlyDim0__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0;
    __VdlyDim0__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 0;
    CData/*0:0*/ __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 0;
    QData/*33:0*/ __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0;
    __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0;
    CData/*0:0*/ __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0;
    QData/*33:0*/ __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1;
    __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0;
    CData/*0:0*/ __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0;
    SData/*8:0*/ __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0;
    __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 0;
    CData/*4:0*/ __VdlyDim0__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0;
    __VdlyDim0__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 0;
    CData/*0:0*/ __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 0;
    SData/*8:0*/ __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0;
    __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0;
    CData/*0:0*/ __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0;
    SData/*8:0*/ __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1;
    __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0;
    CData/*0:0*/ __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0;
    // Body
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 0U;
    __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
    __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0U;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0U;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 0U;
    __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
    __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 = 0U;
    __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 0U;
    if (vlSelfRef.literal_replay__DOT__m_ready) {
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSelfRef.literal_replay__DOT__m_ready) 
         | (0U != (1U & ((~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)) 
                         >> 1U))))) {
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = ((1U & (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)) 
               | (2U & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                        << 1U)));
        __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U];
        __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0 = 1U;
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSelfRef.literal_replay__DOT__m_ready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem
            [(0x0000001fU & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg))];
        __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1 = 1U;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg) 
             != (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg)));
            __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        }
    }
    if (vlSelfRef.literal_replay__DOT__h_ready) {
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (1U & (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSelfRef.literal_replay__DOT__h_ready) 
         | (0U != (1U & ((~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)) 
                         >> 1U))))) {
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = ((1U & (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)) 
               | (2U & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg) 
                        << 1U)));
        __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U];
        __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0 = 1U;
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
    }
    if (((IData)(vlSelfRef.literal_replay__DOT__h_ready) 
         | (0U != (3U & (~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg)))))) {
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
            = (2U & (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem
            [(7U & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg))];
        __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1 = 1U;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg) 
             != (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg)));
            __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
                = (1U | (IData)(__Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg));
        }
    }
    if (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int;
    }
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg 
        = Vliteral_replay__ConstPool__TABLE_hea75a59c_0
        [vlSelfRef.__VdfgRegularize_hebeb780c_0_0];
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg 
        = ((1U & (~ (IData)(vlSelfRef.literal_replay__DOT__rst))) 
           && (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next));
    if (vlSelfRef.literal_replay__DOT__rst) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg = 0U;
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
    }
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
        = __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    if (__VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[1U] 
            = __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v0;
    }
    if (__VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg[0U] 
            = __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__m_axis_pipe_reg__v1;
    }
    if (vlSelfRef.literal_replay__DOT__rst) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg = 0U;
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg = 0U;
    }
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg 
        = __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_tvalid_pipe_reg;
    if (__VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[1U] 
            = __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v0;
    }
    if (__VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg[0U] 
            = __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__m_axis_pipe_reg__v1;
    }
    if (((~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
         & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))) {
        __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 
            = ((((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg) 
                 | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg)) 
                << 8U) | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg));
        __VdlyDim0__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 
            = (0x0000001fU & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg));
        __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0 = 1U;
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg 
            = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg)));
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg 
            = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg)));
    }
    if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready) 
         & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg))) {
        __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 
            = (((QData)((IData)((((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg) 
                                  << 1U) | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg)))) 
                << 0x00000020U) | (QData)((IData)((
                                                   ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg) 
                                                    << 0x00000010U) 
                                                   | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg)))));
        __VdlyDim0__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 
            = (7U & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg));
        __VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0 = 1U;
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg)));
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg)));
    }
    if (__VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem[__VdlyDim0__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0] 
            = __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mem__v0;
    }
    if (vlSelfRef.literal_replay__DOT__rst) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg = 0U;
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_commit_reg = 0U;
    } else {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next;
    }
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg 
        = __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg;
    if (__VdlySet__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem[__VdlyDim0__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0] 
            = __VdlyVal__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__mem__v0;
    }
    if (vlSelfRef.literal_replay__DOT__rst) {
        __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_commit_reg = 0U;
    }
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg 
        = __Vdly__literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full 
        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__wr_ptr_reg) 
           == (0x20U ^ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__rd_ptr_reg)));
    if (Vliteral_replay__ConstPool__TABLE_h9068cabe_0
        [vlSelfRef.__VdfgRegularize_hebeb780c_0_0]) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int;
    } else if (Vliteral_replay__ConstPool__TABLE_h70871376_0
               [vlSelfRef.__VdfgRegularize_hebeb780c_0_0]) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg;
    }
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg 
        = Vliteral_replay__ConstPool__TABLE_hb0f749ab_0
        [vlSelfRef.__VdfgRegularize_hebeb780c_0_0];
    if (vlSelfRef.literal_replay__DOT__rst) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__mark_frame_reg = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg = 0U;
    }
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready 
        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__wr_ptr_reg) 
           != (8U ^ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__header_fifo_inst__DOT__rd_ptr_reg)));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg 
        = ((1U & (~ (IData)(vlSelfRef.literal_replay__DOT__rst))) 
           && (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next));
    if (Vliteral_replay__ConstPool__TABLE_h5ebe4fc2_0
        [vlSelfRef.__VdfgRegularize_hebeb780c_0_0]) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tdata_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tlast_reg 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int;
    }
}

void Vliteral_replay___024root___nba_comb__TOP__0(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___nba_comb__TOP__0\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*7:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked = 0;
    CData/*0:0*/ literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0;
    // Body
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int = 0U;
    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked 
        = vlSelfRef.literal_replay__DOT__s_data;
    if ((0U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = vlSelfRef.literal_replay__DOT__s_valid;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                if ((1U & (~ (IData)(vlSelfRef.literal_replay__DOT__s_last)))) {
                    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                }
            }
        }
    } else if ((1U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = vlSelfRef.literal_replay__DOT__s_valid;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                if ((1U & (~ (IData)(vlSelfRef.literal_replay__DOT__s_last)))) {
                    literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 0U;
                }
            }
        }
    } else if ((2U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int = 1U;
    } else if ((3U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int 
            = ((IData)(vlSelfRef.literal_replay__DOT__s_valid) 
               & (IData)(vlSelfRef.literal_replay__DOT__s_last));
    }
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early 
        = (1U & (~ ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full) 
                    & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
                       | ((IData)(literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
                          & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg))))));
    vlSelfRef.__VdfgRegularize_hebeb780c_0_0 = ((((IData)(literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_int) 
                                                  << 4U) 
                                                 | (((2U 
                                                      & ((~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__frame_fifo_inst__DOT__full)) 
                                                         << 1U)) 
                                                     | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg)) 
                                                    << 2U)) 
                                                | (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__temp_m_axis_tvalid_reg) 
                                                    << 1U) 
                                                   | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tvalid_reg)));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next 
        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg) 
           & (~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready)));
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_reg;
    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
        = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_reg;
    if ((0U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
               & ((~ (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_reg)) 
                  | (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready)));
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.literal_replay__DOT__s_last;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg)));
                if (vlSelfRef.literal_replay__DOT__s_last) {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
                        = (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt 
                           > (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                }
            } else if (vlSelfRef.literal_replay__DOT__s_last) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                     > vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt)) {
                    if ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                    } else {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                               & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                            = VL_SHIFTR_III(1,1,32, 1U, 
                                            ((IData)(1U) 
                                             - ((IData)(4U) 
                                                - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg))));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    }
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                }
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
        }
    } else if ((1U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tdata_masked;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.literal_replay__DOT__s_last;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg)));
                if (vlSelfRef.literal_replay__DOT__s_last) {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next 
                        = (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt 
                           > (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
                }
            } else if (vlSelfRef.literal_replay__DOT__s_last) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                     >= vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt)) {
                    if ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__store_last_word = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
                    } else {
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                            = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                               & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                            = VL_SHIFTR_III(1,1,32, 1U, 
                                            ((IData)(1U) 
                                             - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg)));
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    }
                } else {
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                        = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                           & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
                    vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                        = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                          + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                }
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 1U;
        }
    } else if ((2U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next = 0U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int = 1U;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 0U;
        if (vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_reg) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next 
                = ((1U < (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg))
                    ? (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_reg) 
                                      - (IData)(1U)))
                    : 0U);
            if ((1U >= (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg))) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 4U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                       & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
                    = VL_SHIFTR_III(1,1,32, 1U, ((IData)(1U) 
                                                 - (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_reg)));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 2U;
        }
    } else if ((3U == (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_reg))) {
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tdata_int 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_data_reg;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tkeep_int 
            = vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__last_word_keep_reg;
        vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tlast_int 
            = vlSelfRef.literal_replay__DOT__s_last;
        if (((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_reg) 
             & (IData)(vlSelfRef.literal_replay__DOT__s_valid))) {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt = 1U;
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg)));
            if (vlSelfRef.literal_replay__DOT__s_last) {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_valid_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_pad_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_truncate_next = 1U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_length_next = 8U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__status_frame_original_length_next 
                    = (0x0000ffffU & ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_reg) 
                                      + vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__word_cnt));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__s_axis_tready_next 
                    = ((IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__m_axis_tready_int_early) 
                       & (IData)(vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__status_ready));
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__frame_ptr_next = 0U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__short_counter_next = 4U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__long_counter_next = 8U;
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 0U;
            } else {
                vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
            }
        } else {
            vlSelfRef.literal_replay__DOT__dut__DOT__dut__DOT__axis_frame_length_adjust_inst__DOT__state_next = 3U;
        }
    }
}

void Vliteral_replay___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void Vliteral_replay___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vliteral_replay___024root___eval_phase__act(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_phase__act\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VactExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        ((vlSelfRef.__VdlySched.awaitingCurrentTime() 
                                                          << 1U) 
                                                         | ((IData)(vlSelfRef.literal_replay__DOT__clk) 
                                                            & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__literal_replay__DOT__clk__0))))));
        vlSelfRef.__Vtrigprevexpr___TOP__literal_replay__DOT__clk__0 
            = vlSelfRef.literal_replay__DOT__clk;
    }
    Vliteral_replay___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vliteral_replay___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vliteral_replay___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Vliteral_replay___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        {
            // Inlined CFunc: _timing_resume
            if ((2ULL & vlSelfRef.__VactTriggered[0U])) {
                vlSelfRef.__VdlySched.resume();
            }
        }
        {
            // Inlined CFunc: _eval_act
            if ((2ULL & vlSelfRef.__VactTriggered[0U])) {
                Vliteral_replay___024root___act_sequent__TOP__0(vlSelf);
            }
        }
    }
    return (__VactExecute);
}

bool Vliteral_replay___024root___eval_phase__inact(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_phase__inact\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 2, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Vliteral_replay___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vliteral_replay___024root___eval_phase__nba(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_phase__nba\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vliteral_replay___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_nba
            if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vliteral_replay___024root___nba_sequent__TOP__0(vlSelf);
            }
            if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vliteral_replay___024root___nba_comb__TOP__0(vlSelf);
            }
        }
        Vliteral_replay___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vliteral_replay___024root___eval(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vliteral_replay___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 2, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 2, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vliteral_replay___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/controller-original-witness-physical-v1/physical-build-cache/a134ac794cc20e512ef3ae326160de18ac0d6150246e84928f0d013808b6aa39/verilator/driver.sv", 2, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
                }
                vlSelfRef.__VactIterCount = ((IData)(1U) 
                                             + vlSelfRef.__VactIterCount);
                vlSelfRef.__VactPhaseResult = Vliteral_replay___024root___eval_phase__act(vlSelf);
            } while (vlSelfRef.__VactPhaseResult);
            vlSelfRef.__VinactPhaseResult = Vliteral_replay___024root___eval_phase__inact(vlSelf);
        } while (vlSelfRef.__VinactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vliteral_replay___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vliteral_replay___024root___eval_debug_assertions(Vliteral_replay___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vliteral_replay___024root___eval_debug_assertions\n"); );
    Vliteral_replay__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
