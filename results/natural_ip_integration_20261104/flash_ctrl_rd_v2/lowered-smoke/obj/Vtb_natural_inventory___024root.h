// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtb_natural_inventory.h for the primary calling header

#ifndef VERILATED_VTB_NATURAL_INVENTORY___024ROOT_H_
#define VERILATED_VTB_NATURAL_INVENTORY___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vtb_natural_inventory__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtb_natural_inventory___024root final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ tb_natural_inventory__DOT__clk_i;
    CData/*0:0*/ tb_natural_inventory__DOT__rst_ni;
    CData/*0:0*/ tb_natural_inventory__DOT__op_start_i;
    CData/*0:0*/ tb_natural_inventory__DOT__op_done_o;
    CData/*6:0*/ tb_natural_inventory__DOT__op_err_o;
    CData/*0:0*/ tb_natural_inventory__DOT__op_addr_oob_i;
    CData/*0:0*/ tb_natural_inventory__DOT__data_rdy_i;
    CData/*0:0*/ tb_natural_inventory__DOT__data_wr_o;
    CData/*0:0*/ tb_natural_inventory__DOT__flash_req_o;
    CData/*0:0*/ tb_natural_inventory__DOT__flash_done_i;
    CData/*0:0*/ tb_natural_inventory__DOT__flash_rd_err_i;
    CData/*0:0*/ tb_natural_inventory__DOT__flash_mp_err_i;
    CData/*1:0*/ tb_natural_inventory__DOT__dut__DOT__st_q;
    CData/*1:0*/ tb_natural_inventory__DOT__dut__DOT__st_d;
    CData/*6:0*/ tb_natural_inventory__DOT__dut__DOT__op_err_q;
    CData/*6:0*/ tb_natural_inventory__DOT__dut__DOT__op_err_d;
    CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT____Vcellinp__u_cnt__clr_i;
    CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__err_q;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VstlPhaseResult;
    CData/*0:0*/ __Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk_i__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__tb_natural_inventory__DOT__rst_ni__0;
    CData/*0:0*/ __VactPhaseResult;
    CData/*0:0*/ __VinactPhaseResult;
    CData/*0:0*/ __VnbaPhaseResult;
    SData/*11:0*/ tb_natural_inventory__DOT__op_num_words_i;
    SData/*13:0*/ tb_natural_inventory__DOT__op_addr_i;
    SData/*13:0*/ tb_natural_inventory__DOT__op_err_addr_o;
    SData/*14:0*/ tb_natural_inventory__DOT__dut__DOT__int_addr;
    SData/*12:0*/ tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__ext_cnt;
    SData/*11:0*/ tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__0__KET____DOT__cnt_unforced_q;
    SData/*12:0*/ tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__ext_cnt;
    SData/*11:0*/ tb_natural_inventory__DOT__dut__DOT__u_cnt__DOT__gen_cnts__BRA__1__KET____DOT__cnt_unforced_q;
    IData/*31:0*/ __VactIterCount;
    IData/*31:0*/ __VinactIterCount;
    IData/*31:0*/ __Vi;
    QData/*38:0*/ tb_natural_inventory__DOT__flash_data_i;
    QData/*38:0*/ __VdfgRegularize_hebeb780c_0_1;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    VlDelayScheduler __VdlySched;

    // INTERNAL VARIABLES
    Vtb_natural_inventory__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vtb_natural_inventory___024root(Vtb_natural_inventory__Syms* symsp, const char* namep);
    ~Vtb_natural_inventory___024root();
    VL_UNCOPYABLE(Vtb_natural_inventory___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
