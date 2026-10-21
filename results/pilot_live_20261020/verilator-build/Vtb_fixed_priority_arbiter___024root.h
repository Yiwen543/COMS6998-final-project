// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtb_fixed_priority_arbiter.h for the primary calling header

#ifndef VERILATED_VTB_FIXED_PRIORITY_ARBITER___024ROOT_H_
#define VERILATED_VTB_FIXED_PRIORITY_ARBITER___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_cov.h"
#include "verilated_covergroup.h"
#include "verilated_timing.h"


class Vtb_fixed_priority_arbiter__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtb_fixed_priority_arbiter___024root final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ tb_fixed_priority_arbiter__DOT__clk;
    CData/*0:0*/ tb_fixed_priority_arbiter__DOT__reset;
    CData/*7:0*/ tb_fixed_priority_arbiter__DOT__req;
    CData/*7:0*/ tb_fixed_priority_arbiter__DOT__priority_override;
    CData/*7:0*/ tb_fixed_priority_arbiter__DOT__grant;
    CData/*0:0*/ tb_fixed_priority_arbiter__DOT__valid;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT__grant_index;
    CData/*0:0*/ tb_fixed_priority_arbiter__DOT__initialized;
    CData/*0:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__clk;
    CData/*0:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__reset;
    CData/*7:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__req;
    CData/*7:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__priority_override;
    CData/*7:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__grant;
    CData/*0:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__valid;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__grant_index;
    CData/*0:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__initialized;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_7;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_6;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_5;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_4;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_3;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_2;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_1;
    CData/*2:0*/ tb_fixed_priority_arbiter__DOT__dut__DOT____VlemCond_0;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VstlPhaseResult;
    CData/*0:0*/ __Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__clk__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__tb_fixed_priority_arbiter__DOT__reset__0;
    CData/*0:0*/ __VactPhaseResult;
    CData/*0:0*/ __VinactPhaseResult;
    CData/*0:0*/ __VnbaPhaseResult;
    SData/*8:0*/ tb_fixed_priority_arbiter__DOT__seen_req;
    SData/*8:0*/ tb_fixed_priority_arbiter__DOT__seen_override;
    SData/*8:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__seen_req;
    SData/*8:0*/ tb_fixed_priority_arbiter__DOT____Vtogcov__seen_override;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT____VlemExpr_1;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__1;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT____VExpr_h16e95b7f__0;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__checks;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__functional_errors;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__timing_errors;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__r;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__o;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__mode;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__vector_file;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__scan_status;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__vector_reset;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__vector_req;
    IData/*31:0*/ tb_fixed_priority_arbiter__DOT__vector_override;
    VlWide<32>/*1023:0*/ tb_fixed_priority_arbiter__DOT__vector_path;
    IData/*31:0*/ __VactIterCount;
    IData/*31:0*/ __VinactIterCount;
    IData/*31:0*/ __Vi;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    VlDelayScheduler __VdlySched;
    VlTriggerScheduler __VtrigSched_h14b1aec4__0;
    VlTriggerScheduler __VtrigSched_h14b1ae05__0;

    // INTERNAL VARIABLES
    Vtb_fixed_priority_arbiter__Syms* vlSymsp;
    const char* vlNamep;
    uint32_t __Vcoverage[200]{};

    // CONSTRUCTORS
    Vtb_fixed_priority_arbiter___024root(Vtb_fixed_priority_arbiter__Syms* symsp, const char* namep);
    ~Vtb_fixed_priority_arbiter___024root();
    VL_UNCOPYABLE(Vtb_fixed_priority_arbiter___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
    void __vlCoverInsert(uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp, const char* linescovp,
        const char* fsmVarp, const char* fsmFromp, const char* fsmTop, const char* fsmTagp);
    void __vlCoverToggleInsert(int begin, int end, bool ranged, uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp);
};


#endif  // guard
