// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_fixed_priority_arbiter.h for the primary calling header

#include "Vtb_fixed_priority_arbiter__pch.h"

VlCoroutine Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__0(Vtb_fixed_priority_arbiter___024root* vlSelf);
VlCoroutine Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__1(Vtb_fixed_priority_arbiter___024root* vlSelf);
VlCoroutine Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__2(Vtb_fixed_priority_arbiter___024root* vlSelf);

void Vtb_fixed_priority_arbiter___024root___eval_initial(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_initial\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__0(vlSelf);
    Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__1(vlSelf);
    Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__2(vlSelf);
}

void Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(Vtb_fixed_priority_arbiter___024root* vlSelf, const char* __VeventDescription);
void Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(Vtb_fixed_priority_arbiter___024root* vlSelf, const char* __VeventDescription);

VlCoroutine Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__0(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT____VlemExpr_0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0__requests;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__requests = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0__overrides;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__overrides = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_1 = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_0 = 0;
    SData/*11:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0__held;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__held = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0__selected;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__selected = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant = 0;
    CData/*2:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1__requests;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__requests = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1__overrides;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__overrides = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_1 = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_0 = 0;
    SData/*11:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1__held;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__held = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1__selected;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__selected = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant = 0;
    CData/*2:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2__requests;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__requests = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2__overrides;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__overrides = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_1 = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_0 = 0;
    SData/*11:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2__held;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__held = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2__selected;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__selected = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant = 0;
    CData/*2:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3__requests;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__requests = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3__overrides;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__overrides = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_1 = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_0 = 0;
    SData/*11:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3__held;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__held = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3__selected;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__selected = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant = 0;
    CData/*2:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4__requests;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__requests = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4__overrides;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__overrides = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_1 = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_0 = 0;
    SData/*11:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4__held;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__held = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4__selected;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__selected = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant = 0;
    CData/*2:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5__requests;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__requests = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5__overrides;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__overrides = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_1 = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_0 = 0;
    SData/*11:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5__held;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__held = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5__selected;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__selected = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant = 0;
    CData/*2:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6__requests;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6__requests = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6__overrides;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6__overrides = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_1 = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_0 = 0;
    SData/*11:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6__held;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6__held = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6__selected;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6__selected = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant = 0;
    CData/*2:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7__requests;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7__requests = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7__overrides;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7__overrides = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_1 = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_0 = 0;
    SData/*11:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7__held;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7__held = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7__selected;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7__selected = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant = 0;
    CData/*2:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8__requests;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8__requests = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8__overrides;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8__overrides = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_1 = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_0 = 0;
    SData/*11:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8__held;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8__held = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8__selected;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8__selected = 0;
    CData/*7:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant = 0;
    CData/*2:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 0;
    CData/*0:0*/ __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid = 0;
    // Body
    tb_fixed_priority_arbiter__DOT____VlemExpr_0 = VL_VALUEPLUSARGS_INI(32, "MODE=%d"s, 
                                                                        vlSelfRef.tb_fixed_priority_arbiter__DOT__mode);
    if (tb_fixed_priority_arbiter__DOT____VlemExpr_0) {
        ++(vlSelf->__Vcoverage[147]);
    } else {
        ++(vlSelf->__Vcoverage[148]);
    }
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__overrides = 0U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__requests = 0U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst = 1U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__held = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__selected = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid = 0;
    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(vlSelf, 
                                                                     "@(negedge tb_fixed_priority_arbiter.clk)");
    co_await vlSelfRef.__VtrigSched_h14b1aec4__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(negedge tb_fixed_priority_arbiter.clk)", 
                                                         "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                         30);
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__held 
        = (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
            << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                       << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)));
    vlSelfRef.tb_fixed_priority_arbiter__DOT__reset 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst;
    vlSelfRef.tb_fixed_priority_arbiter__DOT__req = __Vtask_tb_fixed_priority_arbiter__DOT__step__0__requests;
    vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__0__overrides;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                         35);
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
         & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
              << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__held)))) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)))) {
            VL_WRITEF_NX("TIMING_FAIL t=%0t reset=%b req=%h override=%h\n",5, 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000)
                         , '#',1,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset)
                         , '#',8,vlSelfRef.tb_fixed_priority_arbiter__DOT__req
                         , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override));
            ++(vlSelf->__Vcoverage[112]);
        } else {
            ++(vlSelf->__Vcoverage[113]);
        }
        ++(vlSelf->__Vcoverage[114]);
    } else {
        ++(vlSelf->__Vcoverage[115]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst) {
        ++(vlSelf->__Vcoverage[121]);
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_1 = 0U;
    } else {
        ++(vlSelf->__Vcoverage[124]);
        if ((0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__overrides))) {
            ++(vlSelf->__Vcoverage[122]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_0 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__0__overrides;
        } else {
            ++(vlSelf->__Vcoverage[123]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_0 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__0__requests;
        }
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_1 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_0;
    }
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__selected 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__0____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant 
        = ((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__selected) 
           & ((IData)(1U) + (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__selected))));
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid 
        = (0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__selected));
    __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 0U;
    if ((1U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 0U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((2U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 1U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((4U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 2U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((8U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 3U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000010U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 4U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000020U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 5U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000040U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 6U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000080U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index = 7U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(vlSelf, 
                                                                     "@(posedge tb_fixed_priority_arbiter.clk)");
    co_await vlSelfRef.__VtrigSched_h14b1ae05__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge tb_fixed_priority_arbiter.clk)", 
                                                         "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                         48);
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                         49);
    vlSelfRef.tb_fixed_priority_arbiter__DOT__checks 
        = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__checks);
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant)) 
          | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid))) 
         | (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst) 
             | (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid)) 
            & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
               != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index))))) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors)))) {
            VL_WRITEF_NX("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d\n",9
                         , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__0__requests
                         , '#',8,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__overrides)
                         , '#',1,__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst
                         , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant)
                         , '#',1,vlSelfRef.tb_fixed_priority_arbiter__DOT__valid
                         , '#',3,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)
                         , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant
                         , '#',1,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid)
                         , '#',3,__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index);
            ++(vlSelf->__Vcoverage[128]);
        } else {
            ++(vlSelf->__Vcoverage[129]);
        }
        ++(vlSelf->__Vcoverage[130]);
    } else {
        ++(vlSelf->__Vcoverage[131]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst) {
        ++(vlSelf->__Vcoverage[143]);
    } else {
        if ((0U == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__overrides))) {
            if (__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid) {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                    = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                       | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index))));
                ++(vlSelf->__Vcoverage[138]);
            } else {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                    = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req));
                ++(vlSelf->__Vcoverage[139]);
            }
            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override));
            ++(vlSelf->__Vcoverage[140]);
        } else {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                   | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index))));
            ++(vlSelf->__Vcoverage[141]);
        }
        ++(vlSelf->__Vcoverage[142]);
    }
    vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 1U;
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
         & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
              << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__held)))) {
        ++(vlSelf->__Vcoverage[116]);
    }
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                      << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
         == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__held))) {
        ++(vlSelf->__Vcoverage[117]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized)))) {
        ++(vlSelf->__Vcoverage[118]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst) {
        ++(vlSelf->__Vcoverage[119]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst)))) {
        ++(vlSelf->__Vcoverage[120]);
    }
    if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index)))) {
        ++(vlSelf->__Vcoverage[132]);
    }
    if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index)))) {
        ++(vlSelf->__Vcoverage[133]);
    }
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid))) {
        ++(vlSelf->__Vcoverage[134]);
    }
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant))) {
        ++(vlSelf->__Vcoverage[135]);
    }
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant)) 
          & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid))) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_index)))) {
        ++(vlSelf->__Vcoverage[136]);
    }
    if ((((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
            == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_grant)) 
           & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
              == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid))) 
          & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst))) 
         & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__expected_valid)))) {
        ++(vlSelf->__Vcoverage[137]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst)))) {
        ++(vlSelf->__Vcoverage[144]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__0__rst) {
        ++(vlSelf->__Vcoverage[145]);
    }
    ++(vlSelf->__Vcoverage[146]);
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__overrides = 0U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__requests = 0U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst = 0U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__held = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__selected = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid = 0;
    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(vlSelf, 
                                                                     "@(negedge tb_fixed_priority_arbiter.clk)");
    co_await vlSelfRef.__VtrigSched_h14b1aec4__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(negedge tb_fixed_priority_arbiter.clk)", 
                                                         "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                         30);
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__held 
        = (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
            << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                       << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)));
    vlSelfRef.tb_fixed_priority_arbiter__DOT__reset 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst;
    vlSelfRef.tb_fixed_priority_arbiter__DOT__req = __Vtask_tb_fixed_priority_arbiter__DOT__step__1__requests;
    vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__1__overrides;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                         35);
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
         & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
              << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__held)))) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)))) {
            VL_WRITEF_NX("TIMING_FAIL t=%0t reset=%b req=%h override=%h\n",5, 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000)
                         , '#',1,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset)
                         , '#',8,vlSelfRef.tb_fixed_priority_arbiter__DOT__req
                         , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override));
            ++(vlSelf->__Vcoverage[112]);
        } else {
            ++(vlSelf->__Vcoverage[113]);
        }
        ++(vlSelf->__Vcoverage[114]);
    } else {
        ++(vlSelf->__Vcoverage[115]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst) {
        ++(vlSelf->__Vcoverage[121]);
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_1 = 0U;
    } else {
        ++(vlSelf->__Vcoverage[124]);
        if ((0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__overrides))) {
            ++(vlSelf->__Vcoverage[122]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_0 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__1__overrides;
        } else {
            ++(vlSelf->__Vcoverage[123]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_0 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__1__requests;
        }
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_1 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_0;
    }
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__selected 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__1____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant 
        = ((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__selected) 
           & ((IData)(1U) + (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__selected))));
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid 
        = (0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__selected));
    __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 0U;
    if ((1U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 0U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((2U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 1U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((4U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 2U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((8U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 3U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000010U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 4U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000020U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 5U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000040U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 6U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000080U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index = 7U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(vlSelf, 
                                                                     "@(posedge tb_fixed_priority_arbiter.clk)");
    co_await vlSelfRef.__VtrigSched_h14b1ae05__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge tb_fixed_priority_arbiter.clk)", 
                                                         "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                         48);
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                         49);
    vlSelfRef.tb_fixed_priority_arbiter__DOT__checks 
        = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__checks);
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant)) 
          | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid))) 
         | (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst) 
             | (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid)) 
            & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
               != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index))))) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors)))) {
            VL_WRITEF_NX("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d\n",9
                         , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__1__requests
                         , '#',8,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__overrides)
                         , '#',1,__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst
                         , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant)
                         , '#',1,vlSelfRef.tb_fixed_priority_arbiter__DOT__valid
                         , '#',3,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)
                         , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant
                         , '#',1,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid)
                         , '#',3,__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index);
            ++(vlSelf->__Vcoverage[128]);
        } else {
            ++(vlSelf->__Vcoverage[129]);
        }
        ++(vlSelf->__Vcoverage[130]);
    } else {
        ++(vlSelf->__Vcoverage[131]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst) {
        ++(vlSelf->__Vcoverage[143]);
    } else {
        if ((0U == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__overrides))) {
            if (__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid) {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                    = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                       | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index))));
                ++(vlSelf->__Vcoverage[138]);
            } else {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                    = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req));
                ++(vlSelf->__Vcoverage[139]);
            }
            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override));
            ++(vlSelf->__Vcoverage[140]);
        } else {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                   | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index))));
            ++(vlSelf->__Vcoverage[141]);
        }
        ++(vlSelf->__Vcoverage[142]);
    }
    vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 1U;
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
         & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
              << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__held)))) {
        ++(vlSelf->__Vcoverage[116]);
    }
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                      << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
         == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__held))) {
        ++(vlSelf->__Vcoverage[117]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized)))) {
        ++(vlSelf->__Vcoverage[118]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst) {
        ++(vlSelf->__Vcoverage[119]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst)))) {
        ++(vlSelf->__Vcoverage[120]);
    }
    if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index)))) {
        ++(vlSelf->__Vcoverage[132]);
    }
    if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index)))) {
        ++(vlSelf->__Vcoverage[133]);
    }
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid))) {
        ++(vlSelf->__Vcoverage[134]);
    }
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant))) {
        ++(vlSelf->__Vcoverage[135]);
    }
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant)) 
          & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid))) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_index)))) {
        ++(vlSelf->__Vcoverage[136]);
    }
    if ((((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
            == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_grant)) 
           & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
              == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid))) 
          & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst))) 
         & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__expected_valid)))) {
        ++(vlSelf->__Vcoverage[137]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst)))) {
        ++(vlSelf->__Vcoverage[144]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__1__rst) {
        ++(vlSelf->__Vcoverage[145]);
    }
    ++(vlSelf->__Vcoverage[146]);
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__overrides = 0U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__requests = 1U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst = 0U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__held = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__selected = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid = 0;
    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(vlSelf, 
                                                                     "@(negedge tb_fixed_priority_arbiter.clk)");
    co_await vlSelfRef.__VtrigSched_h14b1aec4__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(negedge tb_fixed_priority_arbiter.clk)", 
                                                         "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                         30);
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__held 
        = (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
            << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                       << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)));
    vlSelfRef.tb_fixed_priority_arbiter__DOT__reset 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst;
    vlSelfRef.tb_fixed_priority_arbiter__DOT__req = __Vtask_tb_fixed_priority_arbiter__DOT__step__2__requests;
    vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__2__overrides;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                         35);
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
         & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
              << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__held)))) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)))) {
            VL_WRITEF_NX("TIMING_FAIL t=%0t reset=%b req=%h override=%h\n",5, 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000)
                         , '#',1,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset)
                         , '#',8,vlSelfRef.tb_fixed_priority_arbiter__DOT__req
                         , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override));
            ++(vlSelf->__Vcoverage[112]);
        } else {
            ++(vlSelf->__Vcoverage[113]);
        }
        ++(vlSelf->__Vcoverage[114]);
    } else {
        ++(vlSelf->__Vcoverage[115]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst) {
        ++(vlSelf->__Vcoverage[121]);
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_1 = 0U;
    } else {
        ++(vlSelf->__Vcoverage[124]);
        if ((0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__overrides))) {
            ++(vlSelf->__Vcoverage[122]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_0 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__2__overrides;
        } else {
            ++(vlSelf->__Vcoverage[123]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_0 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__2__requests;
        }
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_1 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_0;
    }
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__selected 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__2____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant 
        = ((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__selected) 
           & ((IData)(1U) + (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__selected))));
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid 
        = (0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__selected));
    __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 0U;
    if ((1U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 0U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((2U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 1U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((4U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 2U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((8U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 3U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000010U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 4U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000020U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 5U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000040U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 6U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000080U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index = 7U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(vlSelf, 
                                                                     "@(posedge tb_fixed_priority_arbiter.clk)");
    co_await vlSelfRef.__VtrigSched_h14b1ae05__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge tb_fixed_priority_arbiter.clk)", 
                                                         "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                         48);
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                         49);
    vlSelfRef.tb_fixed_priority_arbiter__DOT__checks 
        = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__checks);
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant)) 
          | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid))) 
         | (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst) 
             | (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid)) 
            & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
               != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index))))) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors)))) {
            VL_WRITEF_NX("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d\n",9
                         , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__2__requests
                         , '#',8,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__overrides)
                         , '#',1,__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst
                         , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant)
                         , '#',1,vlSelfRef.tb_fixed_priority_arbiter__DOT__valid
                         , '#',3,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)
                         , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant
                         , '#',1,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid)
                         , '#',3,__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index);
            ++(vlSelf->__Vcoverage[128]);
        } else {
            ++(vlSelf->__Vcoverage[129]);
        }
        ++(vlSelf->__Vcoverage[130]);
    } else {
        ++(vlSelf->__Vcoverage[131]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst) {
        ++(vlSelf->__Vcoverage[143]);
    } else {
        if ((0U == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__overrides))) {
            if (__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid) {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                    = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                       | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index))));
                ++(vlSelf->__Vcoverage[138]);
            } else {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                    = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req));
                ++(vlSelf->__Vcoverage[139]);
            }
            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override));
            ++(vlSelf->__Vcoverage[140]);
        } else {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                   | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index))));
            ++(vlSelf->__Vcoverage[141]);
        }
        ++(vlSelf->__Vcoverage[142]);
    }
    vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 1U;
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
         & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
              << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__held)))) {
        ++(vlSelf->__Vcoverage[116]);
    }
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                      << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
         == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__held))) {
        ++(vlSelf->__Vcoverage[117]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized)))) {
        ++(vlSelf->__Vcoverage[118]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst) {
        ++(vlSelf->__Vcoverage[119]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst)))) {
        ++(vlSelf->__Vcoverage[120]);
    }
    if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index)))) {
        ++(vlSelf->__Vcoverage[132]);
    }
    if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index)))) {
        ++(vlSelf->__Vcoverage[133]);
    }
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid))) {
        ++(vlSelf->__Vcoverage[134]);
    }
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant))) {
        ++(vlSelf->__Vcoverage[135]);
    }
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant)) 
          & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid))) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_index)))) {
        ++(vlSelf->__Vcoverage[136]);
    }
    if ((((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
            == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_grant)) 
           & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
              == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid))) 
          & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst))) 
         & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__expected_valid)))) {
        ++(vlSelf->__Vcoverage[137]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst)))) {
        ++(vlSelf->__Vcoverage[144]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__2__rst) {
        ++(vlSelf->__Vcoverage[145]);
    }
    ++(vlSelf->__Vcoverage[146]);
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__overrides = 1U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__requests = 0U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst = 0U;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__held = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__selected = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 0;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid = 0;
    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(vlSelf, 
                                                                     "@(negedge tb_fixed_priority_arbiter.clk)");
    co_await vlSelfRef.__VtrigSched_h14b1aec4__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(negedge tb_fixed_priority_arbiter.clk)", 
                                                         "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                         30);
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__held 
        = (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
            << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                       << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)));
    vlSelfRef.tb_fixed_priority_arbiter__DOT__reset 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst;
    vlSelfRef.tb_fixed_priority_arbiter__DOT__req = __Vtask_tb_fixed_priority_arbiter__DOT__step__3__requests;
    vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__3__overrides;
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                         35);
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
         & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
              << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__held)))) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)))) {
            VL_WRITEF_NX("TIMING_FAIL t=%0t reset=%b req=%h override=%h\n",5, 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000)
                         , '#',1,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset)
                         , '#',8,vlSelfRef.tb_fixed_priority_arbiter__DOT__req
                         , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override));
            ++(vlSelf->__Vcoverage[112]);
        } else {
            ++(vlSelf->__Vcoverage[113]);
        }
        ++(vlSelf->__Vcoverage[114]);
    } else {
        ++(vlSelf->__Vcoverage[115]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst) {
        ++(vlSelf->__Vcoverage[121]);
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_1 = 0U;
    } else {
        ++(vlSelf->__Vcoverage[124]);
        if ((0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__overrides))) {
            ++(vlSelf->__Vcoverage[122]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_0 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__3__overrides;
        } else {
            ++(vlSelf->__Vcoverage[123]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_0 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__3__requests;
        }
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_1 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_0;
    }
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__selected 
        = __Vtask_tb_fixed_priority_arbiter__DOT__step__3____VlefCond_1;
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant 
        = ((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__selected) 
           & ((IData)(1U) + (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__selected))));
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid 
        = (0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__selected));
    __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 0U;
    if ((1U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 0U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((2U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 1U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((4U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 2U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((8U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 3U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000010U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 4U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000020U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 5U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000040U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 6U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    if ((0x00000080U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant))) {
        __Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index = 7U;
        ++(vlSelf->__Vcoverage[125]);
    } else {
        ++(vlSelf->__Vcoverage[126]);
    }
    ++(vlSelf->__Vcoverage[127]);
    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(vlSelf, 
                                                                     "@(posedge tb_fixed_priority_arbiter.clk)");
    co_await vlSelfRef.__VtrigSched_h14b1ae05__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge tb_fixed_priority_arbiter.clk)", 
                                                         "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                         48);
    co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                         nullptr, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                         49);
    vlSelfRef.tb_fixed_priority_arbiter__DOT__checks 
        = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__checks);
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant)) 
          | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid))) 
         | (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst) 
             | (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid)) 
            & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
               != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index))))) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors);
        if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors)))) {
            VL_WRITEF_NX("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d\n",9
                         , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__3__requests
                         , '#',8,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__overrides)
                         , '#',1,__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst
                         , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant)
                         , '#',1,vlSelfRef.tb_fixed_priority_arbiter__DOT__valid
                         , '#',3,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)
                         , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant
                         , '#',1,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid)
                         , '#',3,__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index);
            ++(vlSelf->__Vcoverage[128]);
        } else {
            ++(vlSelf->__Vcoverage[129]);
        }
        ++(vlSelf->__Vcoverage[130]);
    } else {
        ++(vlSelf->__Vcoverage[131]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst) {
        ++(vlSelf->__Vcoverage[143]);
    } else {
        if ((0U == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__overrides))) {
            if (__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid) {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                    = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                       | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index))));
                ++(vlSelf->__Vcoverage[138]);
            } else {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                    = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req));
                ++(vlSelf->__Vcoverage[139]);
            }
            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override));
            ++(vlSelf->__Vcoverage[140]);
        } else {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                   | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index))));
            ++(vlSelf->__Vcoverage[141]);
        }
        ++(vlSelf->__Vcoverage[142]);
    }
    vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 1U;
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
         & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
              << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__held)))) {
        ++(vlSelf->__Vcoverage[116]);
    }
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                      << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
         == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__held))) {
        ++(vlSelf->__Vcoverage[117]);
    }
    if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized)))) {
        ++(vlSelf->__Vcoverage[118]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst) {
        ++(vlSelf->__Vcoverage[119]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst)))) {
        ++(vlSelf->__Vcoverage[120]);
    }
    if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index)))) {
        ++(vlSelf->__Vcoverage[132]);
    }
    if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index)))) {
        ++(vlSelf->__Vcoverage[133]);
    }
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid))) {
        ++(vlSelf->__Vcoverage[134]);
    }
    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant))) {
        ++(vlSelf->__Vcoverage[135]);
    }
    if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
           == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant)) 
          & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid))) 
         & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
            == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_index)))) {
        ++(vlSelf->__Vcoverage[136]);
    }
    if ((((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
            == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_grant)) 
           & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
              == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid))) 
          & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst))) 
         & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__expected_valid)))) {
        ++(vlSelf->__Vcoverage[137]);
    }
    if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst)))) {
        ++(vlSelf->__Vcoverage[144]);
    }
    if (__Vtask_tb_fixed_priority_arbiter__DOT__step__3__rst) {
        ++(vlSelf->__Vcoverage[145]);
    }
    ++(vlSelf->__Vcoverage[146]);
    if (VL_UNLIKELY(((1U == vlSelfRef.tb_fixed_priority_arbiter__DOT__mode)))) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT____VlemExpr_1 
            = VL_VALUEPLUSARGS_INW(1024, "VECTORS=%s"s, 
                                   vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_path);
        if (VL_LIKELY((vlSelfRef.tb_fixed_priority_arbiter__DOT____VlemExpr_1))) {
            ++(vlSelf->__Vcoverage[149]);
        } else {
            VL_WRITEF_NX("[%0t] %%Fatal: tb_fixed_priority_arbiter.sv:79: Assertion failed in %m: MODE=1 requires +VECTORS=<file>\n",3, 'M',vlSymsp->name(),"tb_fixed_priority_arbiter", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 79, "", false);
        }
        vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_file 
            = VL_FOPEN_NN(VL_CVT_PACK_STR_NW(32, vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_path)
                          , "r"s);
        ;
        if (VL_UNLIKELY(((0U == vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_file)))) {
            VL_WRITEF_NX("[%0t] %%Fatal: tb_fixed_priority_arbiter.sv:81: Assertion failed in %m: Cannot open stimulus file\n",3, 'M',vlSymsp->name(),"tb_fixed_priority_arbiter", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 81, "", false);
        } else {
            ++(vlSelf->__Vcoverage[150]);
        }
        while (true) {
            vlSelfRef.tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__0 
                = (vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_file ? feof(VL_CVT_I_FP(vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_file)) : true);
            if (!((! vlSelfRef.tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__0))) break;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__scan_status 
                = VL_FSCANF_INX(vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_file,"%d %h %h\n",3
                                , '#',32,&(vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_reset)
                                , '#',32,&(vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_req)
                                , '#',32,&(vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_override)) ;
            if ((3U == vlSelfRef.tb_fixed_priority_arbiter__DOT__scan_status)) {
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__overrides 
                    = (0x000000ffU & vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_override);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__requests 
                    = (0x000000ffU & vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_req);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst 
                    = (1U & vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_reset);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__held = 0;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__selected = 0;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant = 0;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 0;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid = 0;
                Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(vlSelf, 
                                                                                "@(negedge tb_fixed_priority_arbiter.clk)");
                co_await vlSelfRef.__VtrigSched_h14b1aec4__0.trigger(0U, 
                                                                     nullptr, 
                                                                     "@(negedge tb_fixed_priority_arbiter.clk)", 
                                                                     "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                                     30);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__held 
                    = (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                        << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                                   << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)));
                vlSelfRef.tb_fixed_priority_arbiter__DOT__reset 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst;
                vlSelfRef.tb_fixed_priority_arbiter__DOT__req 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__4__requests;
                vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__4__overrides;
                co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                     nullptr, 
                                                     "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                     35);
                if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
                     & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                          << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                                     << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                        != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__held)))) {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors 
                        = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors);
                    if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)))) {
                        VL_WRITEF_NX("TIMING_FAIL t=%0t reset=%b req=%h override=%h\n",5, 'T',-9
                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                     , '#',1,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset)
                                     , '#',8,vlSelfRef.tb_fixed_priority_arbiter__DOT__req
                                     , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override));
                        ++(vlSelf->__Vcoverage[112]);
                    } else {
                        ++(vlSelf->__Vcoverage[113]);
                    }
                    ++(vlSelf->__Vcoverage[114]);
                } else {
                    ++(vlSelf->__Vcoverage[115]);
                }
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst) {
                    ++(vlSelf->__Vcoverage[121]);
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_1 = 0U;
                } else {
                    ++(vlSelf->__Vcoverage[124]);
                    if ((0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__overrides))) {
                        ++(vlSelf->__Vcoverage[122]);
                        __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_0 
                            = __Vtask_tb_fixed_priority_arbiter__DOT__step__4__overrides;
                    } else {
                        ++(vlSelf->__Vcoverage[123]);
                        __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_0 
                            = __Vtask_tb_fixed_priority_arbiter__DOT__step__4__requests;
                    }
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_1 
                        = __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_0;
                }
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__selected 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__4____VlefCond_1;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant 
                    = ((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__selected) 
                       & ((IData)(1U) + (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__selected))));
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid 
                    = (0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__selected));
                __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 0U;
                if ((1U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 0U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((2U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 1U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((4U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 2U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((8U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 3U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((0x00000010U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 4U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((0x00000020U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 5U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((0x00000040U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 6U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((0x00000080U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index = 7U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(vlSelf, 
                                                                                "@(posedge tb_fixed_priority_arbiter.clk)");
                co_await vlSelfRef.__VtrigSched_h14b1ae05__0.trigger(0U, 
                                                                     nullptr, 
                                                                     "@(posedge tb_fixed_priority_arbiter.clk)", 
                                                                     "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                                     48);
                co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                     nullptr, 
                                                     "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                     49);
                vlSelfRef.tb_fixed_priority_arbiter__DOT__checks 
                    = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__checks);
                if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                       != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant)) 
                      | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid))) 
                     | (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst) 
                         | (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid)) 
                        & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                           != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index))))) {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors 
                        = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors);
                    if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors)))) {
                        VL_WRITEF_NX("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d\n",9
                                     , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__4__requests
                                     , '#',8,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__overrides)
                                     , '#',1,__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst
                                     , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant)
                                     , '#',1,vlSelfRef.tb_fixed_priority_arbiter__DOT__valid
                                     , '#',3,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)
                                     , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant
                                     , '#',1,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid)
                                     , '#',3,__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index);
                        ++(vlSelf->__Vcoverage[128]);
                    } else {
                        ++(vlSelf->__Vcoverage[129]);
                    }
                    ++(vlSelf->__Vcoverage[130]);
                } else {
                    ++(vlSelf->__Vcoverage[131]);
                }
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst) {
                    ++(vlSelf->__Vcoverage[143]);
                } else {
                    if ((0U == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__overrides))) {
                        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid) {
                            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                                = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                                   | (0x01ffU & ((IData)(1U) 
                                                 << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index))));
                            ++(vlSelf->__Vcoverage[138]);
                        } else {
                            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                                = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req));
                            ++(vlSelf->__Vcoverage[139]);
                        }
                        vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                            = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override));
                        ++(vlSelf->__Vcoverage[140]);
                    } else {
                        vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                            = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                               | (0x01ffU & ((IData)(1U) 
                                             << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index))));
                        ++(vlSelf->__Vcoverage[141]);
                    }
                    ++(vlSelf->__Vcoverage[142]);
                }
                vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 1U;
                if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
                     & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                          << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                                     << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                        != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__held)))) {
                    ++(vlSelf->__Vcoverage[116]);
                }
                if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                       << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                                  << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                     == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__held))) {
                    ++(vlSelf->__Vcoverage[117]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized)))) {
                    ++(vlSelf->__Vcoverage[118]);
                }
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst) {
                    ++(vlSelf->__Vcoverage[119]);
                }
                if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst)))) {
                    ++(vlSelf->__Vcoverage[120]);
                }
                if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid) 
                     & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                        != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index)))) {
                    ++(vlSelf->__Vcoverage[132]);
                }
                if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst) 
                     & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                        != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index)))) {
                    ++(vlSelf->__Vcoverage[133]);
                }
                if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                     != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid))) {
                    ++(vlSelf->__Vcoverage[134]);
                }
                if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                     != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant))) {
                    ++(vlSelf->__Vcoverage[135]);
                }
                if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                       == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant)) 
                      & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid))) 
                     & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                        == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_index)))) {
                    ++(vlSelf->__Vcoverage[136]);
                }
                if ((((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                        == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_grant)) 
                       & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                          == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid))) 
                      & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst))) 
                     & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__expected_valid)))) {
                    ++(vlSelf->__Vcoverage[137]);
                }
                if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst)))) {
                    ++(vlSelf->__Vcoverage[144]);
                }
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__4__rst) {
                    ++(vlSelf->__Vcoverage[145]);
                }
                ++(vlSelf->__Vcoverage[146]);
                ++(vlSelf->__Vcoverage[156]);
            } else {
                vlSelfRef.tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__1 
                    = (vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_file ? feof(VL_CVT_I_FP(vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_file)) : true);
                if (VL_LIKELY((vlSelfRef.tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__1))) {
                    ++(vlSelf->__Vcoverage[153]);
                } else {
                    VL_WRITEF_NX("[%0t] %%Fatal: tb_fixed_priority_arbiter.sv:87: Assertion failed in %m: Malformed stimulus row\n",3, 'M',vlSymsp->name(),"tb_fixed_priority_arbiter", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000));
                    VL_STOP_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 87, "", false);
                }
                if ((! vlSelfRef.tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__1)) {
                    ++(vlSelf->__Vcoverage[154]);
                }
                if (vlSelfRef.tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__1) {
                    ++(vlSelf->__Vcoverage[155]);
                }
            }
            if ((! vlSelfRef.tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__0)) {
                ++(vlSelf->__Vcoverage[151]);
            }
            if (vlSelfRef.tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__0) {
                ++(vlSelf->__Vcoverage[152]);
            }
            ++(vlSelf->__Vcoverage[157]);
        }
        VL_FCLOSE_I(vlSelfRef.tb_fixed_priority_arbiter__DOT__vector_file); ++(vlSelf->__Vcoverage[166]);
    } else if ((2U == vlSelfRef.tb_fixed_priority_arbiter__DOT__mode)) {
        vlSelfRef.tb_fixed_priority_arbiter__DOT__o = 0U;
        while (VL_GTS_III(32, 0x00000100U, vlSelfRef.tb_fixed_priority_arbiter__DOT__o)) {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__r = 0U;
            while (VL_GTS_III(32, 0x00000100U, vlSelfRef.tb_fixed_priority_arbiter__DOT__r)) {
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__overrides 
                    = (0x000000ffU & vlSelfRef.tb_fixed_priority_arbiter__DOT__o);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__requests 
                    = (0x000000ffU & vlSelfRef.tb_fixed_priority_arbiter__DOT__r);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst = 0U;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__held = 0;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__selected = 0;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant = 0;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 0;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid = 0;
                Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(vlSelf, 
                                                                                "@(negedge tb_fixed_priority_arbiter.clk)");
                co_await vlSelfRef.__VtrigSched_h14b1aec4__0.trigger(0U, 
                                                                     nullptr, 
                                                                     "@(negedge tb_fixed_priority_arbiter.clk)", 
                                                                     "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                                     30);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__held 
                    = (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                        << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                                   << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)));
                vlSelfRef.tb_fixed_priority_arbiter__DOT__reset 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst;
                vlSelfRef.tb_fixed_priority_arbiter__DOT__req 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__5__requests;
                vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__5__overrides;
                co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                     nullptr, 
                                                     "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                     35);
                if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
                     & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                          << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                                     << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                        != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__held)))) {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors 
                        = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors);
                    if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)))) {
                        VL_WRITEF_NX("TIMING_FAIL t=%0t reset=%b req=%h override=%h\n",5, 'T',-9
                                     , '#',64,VL_TIME_UNITED_Q(1000)
                                     , '#',1,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset)
                                     , '#',8,vlSelfRef.tb_fixed_priority_arbiter__DOT__req
                                     , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override));
                        ++(vlSelf->__Vcoverage[112]);
                    } else {
                        ++(vlSelf->__Vcoverage[113]);
                    }
                    ++(vlSelf->__Vcoverage[114]);
                } else {
                    ++(vlSelf->__Vcoverage[115]);
                }
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst) {
                    ++(vlSelf->__Vcoverage[121]);
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_1 = 0U;
                } else {
                    ++(vlSelf->__Vcoverage[124]);
                    if ((0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__overrides))) {
                        ++(vlSelf->__Vcoverage[122]);
                        __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_0 
                            = __Vtask_tb_fixed_priority_arbiter__DOT__step__5__overrides;
                    } else {
                        ++(vlSelf->__Vcoverage[123]);
                        __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_0 
                            = __Vtask_tb_fixed_priority_arbiter__DOT__step__5__requests;
                    }
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_1 
                        = __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_0;
                }
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__selected 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__5____VlefCond_1;
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant 
                    = ((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__selected) 
                       & ((IData)(1U) + (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__selected))));
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid 
                    = (0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__selected));
                __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 0U;
                if ((1U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 0U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((2U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 1U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((4U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 2U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((8U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 3U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((0x00000010U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 4U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((0x00000020U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 5U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((0x00000040U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 6U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                if ((0x00000080U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant))) {
                    __Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index = 7U;
                    ++(vlSelf->__Vcoverage[125]);
                } else {
                    ++(vlSelf->__Vcoverage[126]);
                }
                ++(vlSelf->__Vcoverage[127]);
                Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(vlSelf, 
                                                                                "@(posedge tb_fixed_priority_arbiter.clk)");
                co_await vlSelfRef.__VtrigSched_h14b1ae05__0.trigger(0U, 
                                                                     nullptr, 
                                                                     "@(posedge tb_fixed_priority_arbiter.clk)", 
                                                                     "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                                     48);
                co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                                     nullptr, 
                                                     "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                     49);
                vlSelfRef.tb_fixed_priority_arbiter__DOT__checks 
                    = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__checks);
                if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                       != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant)) 
                      | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid))) 
                     | (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst) 
                         | (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid)) 
                        & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                           != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index))))) {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors 
                        = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors);
                    if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors)))) {
                        VL_WRITEF_NX("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d\n",9
                                     , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__5__requests
                                     , '#',8,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__overrides)
                                     , '#',1,__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst
                                     , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant)
                                     , '#',1,vlSelfRef.tb_fixed_priority_arbiter__DOT__valid
                                     , '#',3,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)
                                     , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant
                                     , '#',1,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid)
                                     , '#',3,__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index);
                        ++(vlSelf->__Vcoverage[128]);
                    } else {
                        ++(vlSelf->__Vcoverage[129]);
                    }
                    ++(vlSelf->__Vcoverage[130]);
                } else {
                    ++(vlSelf->__Vcoverage[131]);
                }
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst) {
                    ++(vlSelf->__Vcoverage[143]);
                } else {
                    if ((0U == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__overrides))) {
                        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid) {
                            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                                = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                                   | (0x01ffU & ((IData)(1U) 
                                                 << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index))));
                            ++(vlSelf->__Vcoverage[138]);
                        } else {
                            vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                                = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req));
                            ++(vlSelf->__Vcoverage[139]);
                        }
                        vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                            = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override));
                        ++(vlSelf->__Vcoverage[140]);
                    } else {
                        vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                            = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                               | (0x01ffU & ((IData)(1U) 
                                             << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index))));
                        ++(vlSelf->__Vcoverage[141]);
                    }
                    ++(vlSelf->__Vcoverage[142]);
                }
                vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 1U;
                if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
                     & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                          << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                                     << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                        != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__held)))) {
                    ++(vlSelf->__Vcoverage[116]);
                }
                if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                       << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                                  << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                     == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__held))) {
                    ++(vlSelf->__Vcoverage[117]);
                }
                if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized)))) {
                    ++(vlSelf->__Vcoverage[118]);
                }
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst) {
                    ++(vlSelf->__Vcoverage[119]);
                }
                if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst)))) {
                    ++(vlSelf->__Vcoverage[120]);
                }
                if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid) 
                     & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                        != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index)))) {
                    ++(vlSelf->__Vcoverage[132]);
                }
                if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst) 
                     & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                        != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index)))) {
                    ++(vlSelf->__Vcoverage[133]);
                }
                if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                     != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid))) {
                    ++(vlSelf->__Vcoverage[134]);
                }
                if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                     != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant))) {
                    ++(vlSelf->__Vcoverage[135]);
                }
                if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                       == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant)) 
                      & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                         == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid))) 
                     & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                        == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_index)))) {
                    ++(vlSelf->__Vcoverage[136]);
                }
                if ((((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                        == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_grant)) 
                       & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                          == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid))) 
                      & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst))) 
                     & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__expected_valid)))) {
                    ++(vlSelf->__Vcoverage[137]);
                }
                if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst)))) {
                    ++(vlSelf->__Vcoverage[144]);
                }
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__5__rst) {
                    ++(vlSelf->__Vcoverage[145]);
                }
                ++(vlSelf->__Vcoverage[146]);
                vlSelfRef.tb_fixed_priority_arbiter__DOT__r 
                    = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__r);
                ++(vlSelf->__Vcoverage[158]);
            }
            vlSelfRef.tb_fixed_priority_arbiter__DOT__o 
                = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__o);
            ++(vlSelf->__Vcoverage[159]);
        }
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__overrides = 0U;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__requests = 0x80U;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst = 0U;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__held = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__selected = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid = 0;
        Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(vlSelf, 
                                                                         "@(negedge tb_fixed_priority_arbiter.clk)");
        co_await vlSelfRef.__VtrigSched_h14b1aec4__0.trigger(0U, 
                                                             nullptr, 
                                                             "@(negedge tb_fixed_priority_arbiter.clk)", 
                                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                             30);
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__held 
            = (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                           << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)));
        vlSelfRef.tb_fixed_priority_arbiter__DOT__reset 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst;
        vlSelfRef.tb_fixed_priority_arbiter__DOT__req 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__6__requests;
        vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__6__overrides;
        co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                             nullptr, 
                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                             35);
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
             & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                  << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                             << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__held)))) {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors 
                = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors);
            if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)))) {
                VL_WRITEF_NX("TIMING_FAIL t=%0t reset=%b req=%h override=%h\n",5, 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000)
                             , '#',1,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset)
                             , '#',8,vlSelfRef.tb_fixed_priority_arbiter__DOT__req
                             , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override));
                ++(vlSelf->__Vcoverage[112]);
            } else {
                ++(vlSelf->__Vcoverage[113]);
            }
            ++(vlSelf->__Vcoverage[114]);
        } else {
            ++(vlSelf->__Vcoverage[115]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst) {
            ++(vlSelf->__Vcoverage[121]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_1 = 0U;
        } else {
            ++(vlSelf->__Vcoverage[124]);
            if ((0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__overrides))) {
                ++(vlSelf->__Vcoverage[122]);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_0 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__6__overrides;
            } else {
                ++(vlSelf->__Vcoverage[123]);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_0 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__6__requests;
            }
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_1 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_0;
        }
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__selected 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__6____VlefCond_1;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant 
            = ((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__selected) 
               & ((IData)(1U) + (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__selected))));
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid 
            = (0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__selected));
        __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 0U;
        if ((1U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 0U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((2U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 1U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((4U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 2U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((8U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 3U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000010U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 4U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000020U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 5U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000040U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 6U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000080U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index = 7U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(vlSelf, 
                                                                         "@(posedge tb_fixed_priority_arbiter.clk)");
        co_await vlSelfRef.__VtrigSched_h14b1ae05__0.trigger(0U, 
                                                             nullptr, 
                                                             "@(posedge tb_fixed_priority_arbiter.clk)", 
                                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                             48);
        co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                             nullptr, 
                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                             49);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__checks 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__checks);
        if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
               != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant)) 
              | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                 != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid))) 
             | (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst) 
                 | (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid)) 
                & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                   != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index))))) {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors 
                = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors);
            if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors)))) {
                VL_WRITEF_NX("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d\n",9
                             , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__6__requests
                             , '#',8,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__overrides)
                             , '#',1,__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst
                             , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant)
                             , '#',1,vlSelfRef.tb_fixed_priority_arbiter__DOT__valid
                             , '#',3,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)
                             , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant
                             , '#',1,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid)
                             , '#',3,__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index);
                ++(vlSelf->__Vcoverage[128]);
            } else {
                ++(vlSelf->__Vcoverage[129]);
            }
            ++(vlSelf->__Vcoverage[130]);
        } else {
            ++(vlSelf->__Vcoverage[131]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst) {
            ++(vlSelf->__Vcoverage[143]);
        } else {
            if ((0U == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__overrides))) {
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid) {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                        = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                           | (0x01ffU & ((IData)(1U) 
                                         << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index))));
                    ++(vlSelf->__Vcoverage[138]);
                } else {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                        = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req));
                    ++(vlSelf->__Vcoverage[139]);
                }
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                    = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override));
                ++(vlSelf->__Vcoverage[140]);
            } else {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                    = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                       | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index))));
                ++(vlSelf->__Vcoverage[141]);
            }
            ++(vlSelf->__Vcoverage[142]);
        }
        vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 1U;
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
             & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                  << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                             << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__held)))) {
            ++(vlSelf->__Vcoverage[116]);
        }
        if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
               << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                          << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
             == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__held))) {
            ++(vlSelf->__Vcoverage[117]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized)))) {
            ++(vlSelf->__Vcoverage[118]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst) {
            ++(vlSelf->__Vcoverage[119]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst)))) {
            ++(vlSelf->__Vcoverage[120]);
        }
        if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid) 
             & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index)))) {
            ++(vlSelf->__Vcoverage[132]);
        }
        if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst) 
             & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index)))) {
            ++(vlSelf->__Vcoverage[133]);
        }
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid))) {
            ++(vlSelf->__Vcoverage[134]);
        }
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant))) {
            ++(vlSelf->__Vcoverage[135]);
        }
        if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
               == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant)) 
              & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                 == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid))) 
             & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_index)))) {
            ++(vlSelf->__Vcoverage[136]);
        }
        if ((((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_grant)) 
               & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                  == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid))) 
              & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst))) 
             & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__expected_valid)))) {
            ++(vlSelf->__Vcoverage[137]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst)))) {
            ++(vlSelf->__Vcoverage[144]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__6__rst) {
            ++(vlSelf->__Vcoverage[145]);
        }
        ++(vlSelf->__Vcoverage[146]);
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__overrides = 0xffU;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__requests = 0xffU;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst = 1U;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__held = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__selected = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid = 0;
        Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(vlSelf, 
                                                                         "@(negedge tb_fixed_priority_arbiter.clk)");
        co_await vlSelfRef.__VtrigSched_h14b1aec4__0.trigger(0U, 
                                                             nullptr, 
                                                             "@(negedge tb_fixed_priority_arbiter.clk)", 
                                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                             30);
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__held 
            = (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                           << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)));
        vlSelfRef.tb_fixed_priority_arbiter__DOT__reset 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst;
        vlSelfRef.tb_fixed_priority_arbiter__DOT__req 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__7__requests;
        vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__7__overrides;
        co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                             nullptr, 
                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                             35);
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
             & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                  << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                             << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__held)))) {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors 
                = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors);
            if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)))) {
                VL_WRITEF_NX("TIMING_FAIL t=%0t reset=%b req=%h override=%h\n",5, 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000)
                             , '#',1,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset)
                             , '#',8,vlSelfRef.tb_fixed_priority_arbiter__DOT__req
                             , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override));
                ++(vlSelf->__Vcoverage[112]);
            } else {
                ++(vlSelf->__Vcoverage[113]);
            }
            ++(vlSelf->__Vcoverage[114]);
        } else {
            ++(vlSelf->__Vcoverage[115]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst) {
            ++(vlSelf->__Vcoverage[121]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_1 = 0U;
        } else {
            ++(vlSelf->__Vcoverage[124]);
            if ((0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__overrides))) {
                ++(vlSelf->__Vcoverage[122]);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_0 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__7__overrides;
            } else {
                ++(vlSelf->__Vcoverage[123]);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_0 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__7__requests;
            }
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_1 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_0;
        }
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__selected 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__7____VlefCond_1;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant 
            = ((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__selected) 
               & ((IData)(1U) + (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__selected))));
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid 
            = (0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__selected));
        __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 0U;
        if ((1U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 0U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((2U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 1U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((4U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 2U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((8U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 3U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000010U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 4U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000020U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 5U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000040U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 6U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000080U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index = 7U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(vlSelf, 
                                                                         "@(posedge tb_fixed_priority_arbiter.clk)");
        co_await vlSelfRef.__VtrigSched_h14b1ae05__0.trigger(0U, 
                                                             nullptr, 
                                                             "@(posedge tb_fixed_priority_arbiter.clk)", 
                                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                             48);
        co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                             nullptr, 
                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                             49);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__checks 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__checks);
        if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
               != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant)) 
              | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                 != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid))) 
             | (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst) 
                 | (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid)) 
                & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                   != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index))))) {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors 
                = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors);
            if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors)))) {
                VL_WRITEF_NX("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d\n",9
                             , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__7__requests
                             , '#',8,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__overrides)
                             , '#',1,__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst
                             , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant)
                             , '#',1,vlSelfRef.tb_fixed_priority_arbiter__DOT__valid
                             , '#',3,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)
                             , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant
                             , '#',1,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid)
                             , '#',3,__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index);
                ++(vlSelf->__Vcoverage[128]);
            } else {
                ++(vlSelf->__Vcoverage[129]);
            }
            ++(vlSelf->__Vcoverage[130]);
        } else {
            ++(vlSelf->__Vcoverage[131]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst) {
            ++(vlSelf->__Vcoverage[143]);
        } else {
            if ((0U == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__overrides))) {
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid) {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                        = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                           | (0x01ffU & ((IData)(1U) 
                                         << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index))));
                    ++(vlSelf->__Vcoverage[138]);
                } else {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                        = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req));
                    ++(vlSelf->__Vcoverage[139]);
                }
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                    = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override));
                ++(vlSelf->__Vcoverage[140]);
            } else {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                    = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                       | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index))));
                ++(vlSelf->__Vcoverage[141]);
            }
            ++(vlSelf->__Vcoverage[142]);
        }
        vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 1U;
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
             & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                  << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                             << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__held)))) {
            ++(vlSelf->__Vcoverage[116]);
        }
        if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
               << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                          << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
             == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__held))) {
            ++(vlSelf->__Vcoverage[117]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized)))) {
            ++(vlSelf->__Vcoverage[118]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst) {
            ++(vlSelf->__Vcoverage[119]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst)))) {
            ++(vlSelf->__Vcoverage[120]);
        }
        if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid) 
             & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index)))) {
            ++(vlSelf->__Vcoverage[132]);
        }
        if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst) 
             & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index)))) {
            ++(vlSelf->__Vcoverage[133]);
        }
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid))) {
            ++(vlSelf->__Vcoverage[134]);
        }
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant))) {
            ++(vlSelf->__Vcoverage[135]);
        }
        if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
               == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant)) 
              & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                 == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid))) 
             & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_index)))) {
            ++(vlSelf->__Vcoverage[136]);
        }
        if ((((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_grant)) 
               & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                  == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid))) 
              & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst))) 
             & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__expected_valid)))) {
            ++(vlSelf->__Vcoverage[137]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst)))) {
            ++(vlSelf->__Vcoverage[144]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__7__rst) {
            ++(vlSelf->__Vcoverage[145]);
        }
        ++(vlSelf->__Vcoverage[146]);
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__overrides = 0U;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__requests = 0U;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst = 0U;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__held = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__selected = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 0;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid = 0;
        Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(vlSelf, 
                                                                         "@(negedge tb_fixed_priority_arbiter.clk)");
        co_await vlSelfRef.__VtrigSched_h14b1aec4__0.trigger(0U, 
                                                             nullptr, 
                                                             "@(negedge tb_fixed_priority_arbiter.clk)", 
                                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                             30);
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__held 
            = (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                           << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)));
        vlSelfRef.tb_fixed_priority_arbiter__DOT__reset 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst;
        vlSelfRef.tb_fixed_priority_arbiter__DOT__req 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__8__requests;
        vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__8__overrides;
        co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                             nullptr, 
                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                             35);
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
             & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                  << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                             << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__held)))) {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors 
                = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors);
            if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)))) {
                VL_WRITEF_NX("TIMING_FAIL t=%0t reset=%b req=%h override=%h\n",5, 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000)
                             , '#',1,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset)
                             , '#',8,vlSelfRef.tb_fixed_priority_arbiter__DOT__req
                             , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override));
                ++(vlSelf->__Vcoverage[112]);
            } else {
                ++(vlSelf->__Vcoverage[113]);
            }
            ++(vlSelf->__Vcoverage[114]);
        } else {
            ++(vlSelf->__Vcoverage[115]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst) {
            ++(vlSelf->__Vcoverage[121]);
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_1 = 0U;
        } else {
            ++(vlSelf->__Vcoverage[124]);
            if ((0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__overrides))) {
                ++(vlSelf->__Vcoverage[122]);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_0 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__8__overrides;
            } else {
                ++(vlSelf->__Vcoverage[123]);
                __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_0 
                    = __Vtask_tb_fixed_priority_arbiter__DOT__step__8__requests;
            }
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_1 
                = __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_0;
        }
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__selected 
            = __Vtask_tb_fixed_priority_arbiter__DOT__step__8____VlefCond_1;
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant 
            = ((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__selected) 
               & ((IData)(1U) + (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__selected))));
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid 
            = (0U != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__selected));
        __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 0U;
        if ((1U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 0U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((2U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 1U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((4U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 2U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((8U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 3U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000010U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 4U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000020U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 5U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000040U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 6U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        if ((0x00000080U & (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant))) {
            __Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index = 7U;
            ++(vlSelf->__Vcoverage[125]);
        } else {
            ++(vlSelf->__Vcoverage[126]);
        }
        ++(vlSelf->__Vcoverage[127]);
        Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(vlSelf, 
                                                                         "@(posedge tb_fixed_priority_arbiter.clk)");
        co_await vlSelfRef.__VtrigSched_h14b1ae05__0.trigger(0U, 
                                                             nullptr, 
                                                             "@(posedge tb_fixed_priority_arbiter.clk)", 
                                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                                             48);
        co_await vlSelfRef.__VdlySched.delay(0x00000000000003e8ULL, 
                                             nullptr, 
                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                             49);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__checks 
            = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__checks);
        if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
               != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant)) 
              | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                 != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid))) 
             | (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst) 
                 | (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid)) 
                & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                   != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index))))) {
            vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors 
                = ((IData)(1U) + vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors);
            if (VL_UNLIKELY((VL_GTES_III(32, 4U, vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors)))) {
                VL_WRITEF_NX("FUNCTION_FAIL req=%h override=%h reset=%b got=%h/%b/%d expected=%h/%b/%d\n",9
                             , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__8__requests
                             , '#',8,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__overrides)
                             , '#',1,__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst
                             , '#',8,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant)
                             , '#',1,vlSelfRef.tb_fixed_priority_arbiter__DOT__valid
                             , '#',3,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index)
                             , '#',8,__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant
                             , '#',1,(IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid)
                             , '#',3,__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index);
                ++(vlSelf->__Vcoverage[128]);
            } else {
                ++(vlSelf->__Vcoverage[129]);
            }
            ++(vlSelf->__Vcoverage[130]);
        } else {
            ++(vlSelf->__Vcoverage[131]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst) {
            ++(vlSelf->__Vcoverage[143]);
        } else {
            if ((0U == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__overrides))) {
                if (__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid) {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                        = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req) 
                           | (0x01ffU & ((IData)(1U) 
                                         << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index))));
                    ++(vlSelf->__Vcoverage[138]);
                } else {
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req 
                        = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req));
                    ++(vlSelf->__Vcoverage[139]);
                }
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                    = (0x00000100U | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override));
                ++(vlSelf->__Vcoverage[140]);
            } else {
                vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override 
                    = ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override) 
                       | (0x01ffU & ((IData)(1U) << (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index))));
                ++(vlSelf->__Vcoverage[141]);
            }
            ++(vlSelf->__Vcoverage[142]);
        }
        vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized = 1U;
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized) 
             & ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                  << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                             << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__held)))) {
            ++(vlSelf->__Vcoverage[116]);
        }
        if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
               << 4U) | (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                          << 3U) | (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index))) 
             == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__held))) {
            ++(vlSelf->__Vcoverage[117]);
        }
        if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__initialized)))) {
            ++(vlSelf->__Vcoverage[118]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst) {
            ++(vlSelf->__Vcoverage[119]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst)))) {
            ++(vlSelf->__Vcoverage[120]);
        }
        if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid) 
             & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index)))) {
            ++(vlSelf->__Vcoverage[132]);
        }
        if (((IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst) 
             & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index)))) {
            ++(vlSelf->__Vcoverage[133]);
        }
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid))) {
            ++(vlSelf->__Vcoverage[134]);
        }
        if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
             != (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant))) {
            ++(vlSelf->__Vcoverage[135]);
        }
        if (((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
               == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant)) 
              & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                 == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid))) 
             & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index) 
                == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_index)))) {
            ++(vlSelf->__Vcoverage[136]);
        }
        if ((((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__grant) 
                == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_grant)) 
               & ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__valid) 
                  == (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid))) 
              & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst))) 
             & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__expected_valid)))) {
            ++(vlSelf->__Vcoverage[137]);
        }
        if ((1U & (~ (IData)(__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst)))) {
            ++(vlSelf->__Vcoverage[144]);
        }
        if (__Vtask_tb_fixed_priority_arbiter__DOT__step__8__rst) {
            ++(vlSelf->__Vcoverage[145]);
        }
        ++(vlSelf->__Vcoverage[146]);
        if (VL_UNLIKELY((((0x01ffU != (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req)) 
                          | (0x01ffU != (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override)))))) {
            VL_WRITEF_NX("[%0t] %%Fatal: tb_fixed_priority_arbiter.sv:99: Assertion failed in %m: Stimulus partition coverage incomplete\n",3, 'M',vlSymsp->name(),"tb_fixed_priority_arbiter", 'T',-9
                         , '#',64,VL_TIME_UNITED_Q(1000));
            VL_STOP_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 99, "", false);
        } else {
            ++(vlSelf->__Vcoverage[160]);
        }
        if ((0x01ffU != (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override))) {
            ++(vlSelf->__Vcoverage[161]);
        }
        if ((0x01ffU != (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req))) {
            ++(vlSelf->__Vcoverage[162]);
        }
        if (((0x01ffU == (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req)) 
             & (0x01ffU == (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override)))) {
            ++(vlSelf->__Vcoverage[163]);
        }
        ++(vlSelf->__Vcoverage[165]);
    } else if (VL_UNLIKELY(((0U != vlSelfRef.tb_fixed_priority_arbiter__DOT__mode)))) {
        VL_WRITEF_NX("[%0t] %%Fatal: tb_fixed_priority_arbiter.sv:100: Assertion failed in %m: Unknown MODE\n",3, 'M',vlSymsp->name(),"tb_fixed_priority_arbiter", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000));
        VL_STOP_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 100, "", false);
    } else {
        ++(vlSelf->__Vcoverage[164]);
    }
    VL_WRITEF_NX("RESULT checks=%0d functional_errors=%0d timing_errors=%0d req_classes=%h override_classes=%h\n",5
                 , '~',32,vlSelfRef.tb_fixed_priority_arbiter__DOT__checks
                 , '~',32,vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors
                 , '~',32,vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors
                 , '#',9,(IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_req)
                 , '#',9,vlSelfRef.tb_fixed_priority_arbiter__DOT__seen_override);
    if (VL_UNLIKELY(((((0U != vlSelfRef.tb_fixed_priority_arbiter__DOT__functional_errors) 
                       | (0U != vlSelfRef.tb_fixed_priority_arbiter__DOT__timing_errors)) 
                      & (! VL_TESTPLUSARGS_I("COLLECT"s)))))) {
        VL_WRITEF_NX("[%0t] %%Fatal: tb_fixed_priority_arbiter.sv:106: Assertion failed in %m: Specification violations detected\n",3, 'M',vlSymsp->name(),"tb_fixed_priority_arbiter", 'T',-9
                     , '#',64,VL_TIME_UNITED_Q(1000));
        VL_STOP_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 106, "", false);
    } else {
        ++(vlSelf->__Vcoverage[167]);
    }
    VL_FINISH_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 107, "");
    ++(vlSelf->__Vcoverage[168]);
    co_return;
}

VlCoroutine Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__1(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__1\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    co_await vlSelfRef.__VdlySched.delay(0x000000003b9aca00ULL, 
                                         nullptr, "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                         110);
    VL_WRITEF_NX("[%0t] %%Fatal: tb_fixed_priority_arbiter.sv:111: Assertion failed in %m: Watchdog timeout\n",3, 'M',vlSymsp->name(),"tb_fixed_priority_arbiter", 'T',-9
                 , '#',64,VL_TIME_UNITED_Q(1000));
    VL_STOP_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 111, "", false);
    co_return;
}

VlCoroutine Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__2(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_initial__TOP__Vtiming__2\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    while (VL_LIKELY(!vlSymsp->_vm_contextp__->gotFinish())) {
        co_await vlSelfRef.__VdlySched.delay(0x0000000000001388ULL, 
                                             nullptr, 
                                             "examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 
                                             20);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__clk 
            = (1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk)));
        if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk)))) {
            ++(vlSelf->__Vcoverage[109]);
        }
        if (vlSelfRef.tb_fixed_priority_arbiter__DOT__clk) {
            ++(vlSelf->__Vcoverage[110]);
        }
        ++(vlSelf->__Vcoverage[111]);
    }
    co_return;
}

bool Vtb_fixed_priority_arbiter___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___trigger_anySet__act\n"); );
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

void Vtb_fixed_priority_arbiter___024root___nba_sequent__TOP__1(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___nba_sequent__TOP__1\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.tb_fixed_priority_arbiter__DOT__reset) {
        ++(vlSelf->__Vcoverage[197]);
        vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 0U;
        vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 0U;
        vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 0U;
    } else {
        if ((0U != (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
            if ((1U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
                ++(vlSelf->__Vcoverage[171]);
                vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_7 = 0U;
            } else {
                ++(vlSelf->__Vcoverage[186]);
                if ((2U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
                    ++(vlSelf->__Vcoverage[172]);
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_6 = 1U;
                } else {
                    ++(vlSelf->__Vcoverage[185]);
                    if ((4U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
                        ++(vlSelf->__Vcoverage[173]);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_5 = 2U;
                    } else {
                        ++(vlSelf->__Vcoverage[184]);
                        if ((8U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
                            ++(vlSelf->__Vcoverage[174]);
                            vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_4 = 3U;
                        } else {
                            ++(vlSelf->__Vcoverage[183]);
                            if ((0x00000010U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
                                ++(vlSelf->__Vcoverage[175]);
                                vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_3 = 4U;
                            } else {
                                ++(vlSelf->__Vcoverage[182]);
                                if ((0x00000020U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
                                    ++(vlSelf->__Vcoverage[176]);
                                    vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_2 = 5U;
                                } else {
                                    ++(vlSelf->__Vcoverage[181]);
                                    if ((0x00000040U 
                                         & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
                                        ++(vlSelf->__Vcoverage[177]);
                                        vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_1 = 6U;
                                    } else {
                                        ++(vlSelf->__Vcoverage[180]);
                                        if ((0x00000080U 
                                             & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
                                            ++(vlSelf->__Vcoverage[178]);
                                            vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_0 = 7U;
                                        } else {
                                            ++(vlSelf->__Vcoverage[179]);
                                            vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_0 = 0U;
                                        }
                                        vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_1 
                                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_0;
                                    }
                                    vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_2 
                                        = vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_1;
                                }
                                vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_3 
                                    = vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_2;
                            }
                            vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_4 
                                = vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_3;
                        }
                        vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_5 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_4;
                    }
                    vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_6 
                        = vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_5;
                }
                vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_7 
                    = vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_6;
            }
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant 
                = vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 1U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index 
                = vlSelfRef.tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_7;
            if ((1U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override))) {
                ++(vlSelf->__Vcoverage[169]);
            }
            if ((1U & (~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__priority_override)))) {
                ++(vlSelf->__Vcoverage[170]);
            }
            ++(vlSelf->__Vcoverage[196]);
        } else if ((1U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__req))) {
            ++(vlSelf->__Vcoverage[195]);
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 1U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 0U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 1U;
        } else if ((2U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__req))) {
            ++(vlSelf->__Vcoverage[194]);
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 2U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 1U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 1U;
        } else if ((4U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__req))) {
            ++(vlSelf->__Vcoverage[193]);
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 4U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 2U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 1U;
        } else if ((8U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__req))) {
            ++(vlSelf->__Vcoverage[192]);
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 8U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 3U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 1U;
        } else if ((0x00000010U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__req))) {
            ++(vlSelf->__Vcoverage[191]);
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 0x10U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 4U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 1U;
        } else if ((0x00000020U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__req))) {
            ++(vlSelf->__Vcoverage[190]);
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 0x20U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 5U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 1U;
        } else if ((0x00000040U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__req))) {
            ++(vlSelf->__Vcoverage[189]);
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 0x40U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 6U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 1U;
        } else if ((0x00000080U & (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__req))) {
            ++(vlSelf->__Vcoverage[187]);
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 0x80U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 7U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 1U;
        } else {
            ++(vlSelf->__Vcoverage[188]);
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant = 0U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__grant_index = 0U;
            vlSelfRef.tb_fixed_priority_arbiter__DOT__valid = 0U;
        }
        ++(vlSelf->__Vcoverage[198]);
    }
    ++(vlSelf->__Vcoverage[199]);
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
}

void Vtb_fixed_priority_arbiter___024root___timing_ready(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___timing_ready\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((4ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready("@(negedge tb_fixed_priority_arbiter.clk)");
    }
    if ((1ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready("@(posedge tb_fixed_priority_arbiter.clk)");
    }
}

void Vtb_fixed_priority_arbiter___024root___timing_resume(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___timing_resume\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VtrigSched_h14b1aec4__0.moveToResumeQueue(
                                                          "@(negedge tb_fixed_priority_arbiter.clk)");
    vlSelfRef.__VtrigSched_h14b1ae05__0.moveToResumeQueue(
                                                          "@(posedge tb_fixed_priority_arbiter.clk)");
    vlSelfRef.__VtrigSched_h14b1aec4__0.resume("@(negedge tb_fixed_priority_arbiter.clk)");
    vlSelfRef.__VtrigSched_h14b1ae05__0.resume("@(posedge tb_fixed_priority_arbiter.clk)");
    if ((8ULL & vlSelfRef.__VactTriggered[0U])) {
        vlSelfRef.__VdlySched.resume();
    }
}

void Vtb_fixed_priority_arbiter___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___trigger_orInto__act_vec_vec\n"); );
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
VL_ATTR_COLD void Vtb_fixed_priority_arbiter___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vtb_fixed_priority_arbiter___024root___eval_phase__act(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_phase__act\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VactExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        (((vlSelfRef.__VdlySched.awaitingCurrentTime() 
                                                           << 3U) 
                                                          | (((~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk)) 
                                                              & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0)) 
                                                             << 2U)) 
                                                         | ((((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__reset) 
                                                              & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__reset__0))) 
                                                             << 1U) 
                                                            | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk) 
                                                               & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0)))))));
        vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0 
            = vlSelfRef.tb_fixed_priority_arbiter__DOT__clk;
        vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__reset__0 
            = vlSelfRef.tb_fixed_priority_arbiter__DOT__reset;
    }
    Vtb_fixed_priority_arbiter___024root___timing_ready(vlSelf);
    Vtb_fixed_priority_arbiter___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VactTriggered, vlSelfRef.__VactTriggeredAcc);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtb_fixed_priority_arbiter___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vtb_fixed_priority_arbiter___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    __VactExecute = Vtb_fixed_priority_arbiter___024root___trigger_anySet__act(vlSelfRef.__VactTriggered);
    if (__VactExecute) {
        vlSelfRef.__VactTriggeredAcc.fill(0ULL);
        Vtb_fixed_priority_arbiter___024root___timing_resume(vlSelf);
        {
            // Inlined CFunc: _eval_act
            if ((8ULL & vlSelfRef.__VactTriggered[0U])) {
                {
                    // Inlined CFunc: _act_sequent__TOP__0
                    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk) 
                         ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__clk))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 0, vlSelfRef.tb_fixed_priority_arbiter__DOT__clk, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__clk);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__clk 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__clk;
                    }
                }
            }
            if ((0x000000000000000dULL & vlSelfRef.__VactTriggered[0U])) {
                {
                    // Inlined CFunc: _act_comb__TOP__0
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
    return (__VactExecute);
}

bool Vtb_fixed_priority_arbiter___024root___eval_phase__inact(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_phase__inact\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VinactExecute;
    // Body
    __VinactExecute = vlSelfRef.__VdlySched.awaitingZeroDelay();
    if (__VinactExecute) {
        VL_FATAL_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 2, "", "ZERODLY: Design Verilated with '--no-sched-zero-delay', but #0 delay executed at runtime");
    }
    return (__VinactExecute);
}

void Vtb_fixed_priority_arbiter___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vtb_fixed_priority_arbiter___024root___eval_phase__nba(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_phase__nba\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vtb_fixed_priority_arbiter___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_nba
            if ((8ULL & vlSelfRef.__VnbaTriggered[0U])) {
                {
                    // Inlined CFunc: _act_sequent__TOP__0
                    if (((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk) 
                         ^ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__clk))) {
                        VL_COV_TOGGLE_CHG_ST_I(1, vlSelf->__Vcoverage + 0, vlSelfRef.tb_fixed_priority_arbiter__DOT__clk, vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__clk);
                        vlSelfRef.tb_fixed_priority_arbiter__DOT____Vtogcov__clk 
                            = vlSelfRef.tb_fixed_priority_arbiter__DOT__clk;
                    }
                }
            }
            if ((0x000000000000000dULL & vlSelfRef.__VnbaTriggered[0U])) {
                {
                    // Inlined CFunc: _act_comb__TOP__0
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
            if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vtb_fixed_priority_arbiter___024root___nba_sequent__TOP__1(vlSelf);
            }
        }
        Vtb_fixed_priority_arbiter___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vtb_fixed_priority_arbiter___024root___eval(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vtb_fixed_priority_arbiter___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 2, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VinactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VinactIterCount)))) {
                VL_FATAL_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 2, "", "DIDNOTCONVERGE: Inactive region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VinactIterCount = ((IData)(1U) 
                                           + vlSelfRef.__VinactIterCount);
            vlSelfRef.__VactIterCount = 0U;
            do {
                if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                    Vtb_fixed_priority_arbiter___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                    VL_FATAL_MT("examples/arbiter/verif/tb_fixed_priority_arbiter.sv", 2, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
                }
                vlSelfRef.__VactIterCount = ((IData)(1U) 
                                             + vlSelfRef.__VactIterCount);
                vlSelfRef.__VactPhaseResult = Vtb_fixed_priority_arbiter___024root___eval_phase__act(vlSelf);
            } while (vlSelfRef.__VactPhaseResult);
            vlSelfRef.__VinactPhaseResult = Vtb_fixed_priority_arbiter___024root___eval_phase__inact(vlSelf);
        } while (vlSelfRef.__VinactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vtb_fixed_priority_arbiter___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

void Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0(Vtb_fixed_priority_arbiter___024root* vlSelf, const char* __VeventDescription) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1aec4__0\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    VlUnpacked<QData/*63:0*/, 1> __VTmp;
    // Body
    __VTmp[0U] = (QData)((IData)(((((~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk)) 
                                    & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0)) 
                                   << 2U) | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk) 
                                             & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0))))));
    vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0 
        = vlSelfRef.tb_fixed_priority_arbiter__DOT__clk;
    if ((1ULL & __VTmp[0U])) {
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
    }
    if ((4ULL & __VTmp[0U])) {
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
    }
    vlSelfRef.__VactTriggeredAcc[0U] = (vlSelfRef.__VactTriggeredAcc[0U] 
                                        | __VTmp[0U]);
}

void Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0(Vtb_fixed_priority_arbiter___024root* vlSelf, const char* __VeventDescription) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root____VbeforeTrig_h14b1ae05__0\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    VlUnpacked<QData/*63:0*/, 1> __VTmp;
    // Body
    __VTmp[0U] = (QData)((IData)(((((~ (IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk)) 
                                    & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0)) 
                                   << 2U) | ((IData)(vlSelfRef.tb_fixed_priority_arbiter__DOT__clk) 
                                             & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0))))));
    vlSelfRef.__Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0 
        = vlSelfRef.tb_fixed_priority_arbiter__DOT__clk;
    if ((1ULL & __VTmp[0U])) {
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1ae05__0.ready(__VeventDescription);
    }
    if ((4ULL & __VTmp[0U])) {
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
        vlSelfRef.__VtrigSched_h14b1aec4__0.ready(__VeventDescription);
    }
    vlSelfRef.__VactTriggeredAcc[0U] = (vlSelfRef.__VactTriggeredAcc[0U] 
                                        | __VTmp[0U]);
}

#ifdef VL_DEBUG
void Vtb_fixed_priority_arbiter___024root___eval_debug_assertions(Vtb_fixed_priority_arbiter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb_fixed_priority_arbiter___024root___eval_debug_assertions\n"); );
    Vtb_fixed_priority_arbiter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}
#endif  // VL_DEBUG
