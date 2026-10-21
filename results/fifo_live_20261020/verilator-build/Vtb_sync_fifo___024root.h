// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtb_sync_fifo.h for the primary calling header

#ifndef VERILATED_VTB_SYNC_FIFO___024ROOT_H_
#define VERILATED_VTB_SYNC_FIFO___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_cov.h"
#include "verilated_covergroup.h"
#include "verilated_timing.h"


class Vtb_sync_fifo__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtb_sync_fifo___024root final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ tb_sync_fifo__DOT__clk;
    CData/*0:0*/ tb_sync_fifo__DOT__reset;
    CData/*0:0*/ tb_sync_fifo__DOT__push_i;
    CData/*0:0*/ tb_sync_fifo__DOT__pop_i;
    CData/*7:0*/ tb_sync_fifo__DOT__push_data_i;
    CData/*0:0*/ tb_sync_fifo__DOT__full_o;
    CData/*0:0*/ tb_sync_fifo__DOT__empty_o;
    CData/*0:0*/ tb_sync_fifo__DOT____Vtogcov__clk;
    CData/*0:0*/ tb_sync_fifo__DOT____Vtogcov__reset;
    CData/*0:0*/ tb_sync_fifo__DOT____Vtogcov__push_i;
    CData/*0:0*/ tb_sync_fifo__DOT____Vtogcov__pop_i;
    CData/*7:0*/ tb_sync_fifo__DOT____Vtogcov__push_data_i;
    CData/*7:0*/ tb_sync_fifo__DOT____Vtogcov__pop_data_o;
    CData/*0:0*/ tb_sync_fifo__DOT____Vtogcov__full_o;
    CData/*0:0*/ tb_sync_fifo__DOT____Vtogcov__empty_o;
    CData/*3:0*/ tb_sync_fifo__DOT__dut__DOT__rd_ptr_q;
    CData/*3:0*/ tb_sync_fifo__DOT__dut__DOT__nxt_rd_ptr;
    CData/*3:0*/ tb_sync_fifo__DOT__dut__DOT__wr_ptr_q;
    CData/*3:0*/ tb_sync_fifo__DOT__dut__DOT__nxt_wr_ptr;
    CData/*3:0*/ tb_sync_fifo__DOT__dut__DOT____Vtogcov__rd_ptr_q;
    CData/*3:0*/ tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_rd_ptr;
    CData/*3:0*/ tb_sync_fifo__DOT__dut__DOT____Vtogcov__wr_ptr_q;
    CData/*3:0*/ tb_sync_fifo__DOT__dut__DOT____Vtogcov__nxt_wr_ptr;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VstlPhaseResult;
    CData/*0:0*/ __Vtrigprevexpr___TOP__tb_sync_fifo__DOT__clk__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__tb_sync_fifo__DOT__reset__0;
    CData/*0:0*/ __VactPhaseResult;
    CData/*0:0*/ __VinactPhaseResult;
    CData/*0:0*/ __VnbaPhaseResult;
    SData/*8:0*/ tb_sync_fifo__DOT__functional_bins;
    SData/*8:0*/ tb_sync_fifo__DOT____Vtogcov__functional_bins;
    IData/*31:0*/ tb_sync_fifo__DOT____VlemExpr_1;
    IData/*31:0*/ tb_sync_fifo__DOT____VExpr_h16e95b7f__1;
    IData/*31:0*/ tb_sync_fifo__DOT____VExpr_h16e95b7f__0;
    IData/*31:0*/ tb_sync_fifo__DOT__checks;
    IData/*31:0*/ tb_sync_fifo__DOT__functional_errors;
    IData/*31:0*/ tb_sync_fifo__DOT__status_errors;
    IData/*31:0*/ tb_sync_fifo__DOT__data_errors;
    IData/*31:0*/ tb_sync_fifo__DOT__head;
    IData/*31:0*/ tb_sync_fifo__DOT__tail;
    IData/*31:0*/ tb_sync_fifo__DOT__count;
    IData/*31:0*/ tb_sync_fifo__DOT__mode;
    IData/*31:0*/ tb_sync_fifo__DOT__vector_file;
    IData/*31:0*/ tb_sync_fifo__DOT__scan_status;
    IData/*31:0*/ tb_sync_fifo__DOT__vector_reset;
    IData/*31:0*/ tb_sync_fifo__DOT__vector_push;
    IData/*31:0*/ tb_sync_fifo__DOT__vector_pop;
    IData/*31:0*/ tb_sync_fifo__DOT__vector_data;
    VlWide<32>/*1023:0*/ tb_sync_fifo__DOT__vector_path;
    IData/*31:0*/ __VactIterCount;
    IData/*31:0*/ __VinactIterCount;
    IData/*31:0*/ __Vi;
    VlUnpacked<CData/*7:0*/, 8> tb_sync_fifo__DOT__expected;
    VlUnpacked<CData/*7:0*/, 8> tb_sync_fifo__DOT____Vtogcov__expected;
    VlUnpacked<CData/*7:0*/, 8> tb_sync_fifo__DOT__dut__DOT__fifo_mem;
    VlUnpacked<CData/*7:0*/, 8> tb_sync_fifo__DOT__dut__DOT____Vtogcov__fifo_mem;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    VlDelayScheduler __VdlySched;
    VlTriggerScheduler __VtrigSched_h0839a9c0__0;
    VlTriggerScheduler __VtrigSched_h0839b971__0;

    // INTERNAL VARIABLES
    Vtb_sync_fifo__Syms* vlSymsp;
    const char* vlNamep;
    uint32_t __Vcoverage[464]{};

    // CONSTRUCTORS
    Vtb_sync_fifo___024root(Vtb_sync_fifo__Syms* symsp, const char* namep);
    ~Vtb_sync_fifo___024root();
    VL_UNCOPYABLE(Vtb_sync_fifo___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
    void __vlCoverInsert(uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp, const char* linescovp,
        const char* fsmVarp, const char* fsmFromp, const char* fsmTop, const char* fsmTagp);
    void __vlCoverToggleInsert(int begin, int end, bool ranged, uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp);
};


#endif  // guard
