// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtb_natural_inventory.h for the primary calling header

#ifndef VERILATED_VTB_NATURAL_INVENTORY___024ROOT_H_
#define VERILATED_VTB_NATURAL_INVENTORY___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_cov.h"
#include "verilated_covergroup.h"
#include "verilated_timing.h"


class Vtb_natural_inventory__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtb_natural_inventory___024root final {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        CData/*0:0*/ tb_natural_inventory__DOT__clk;
        CData/*0:0*/ tb_natural_inventory__DOT__rst;
        CData/*7:0*/ tb_natural_inventory__DOT__s_data;
        CData/*0:0*/ tb_natural_inventory__DOT__s_valid;
        CData/*0:0*/ tb_natural_inventory__DOT__s_last;
        CData/*0:0*/ tb_natural_inventory__DOT__m_ready;
        CData/*0:0*/ tb_natural_inventory__DOT__h_ready;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__clk;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__rst;
        CData/*7:0*/ tb_natural_inventory__DOT____Vtogcov__s_data;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__s_valid;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__s_last;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__s_ready;
        CData/*7:0*/ tb_natural_inventory__DOT____Vtogcov__m_data;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__m_valid;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__m_last;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__m_ready;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__h_valid;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__h_pad;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__h_truncate;
        CData/*0:0*/ tb_natural_inventory__DOT____Vtogcov__h_ready;
        CData/*2:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_reg;
        CData/*2:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__state_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_last_word;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_data_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_keep_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_id_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_dest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__last_word_user_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_valid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_pad_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_truncate_next;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_int;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_int;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tready_int_early;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__s_axis_tready_next;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdata_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tkeep_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tlast_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tid_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tdest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tuser_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdata_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tkeep_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tvalid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tlast_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tid_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tdest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__temp_m_axis_tuser_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_output;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_int_to_temp;
    };
    struct {
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__store_axis_temp_to_output;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tkeep;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tid;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tuser;
        CData/*2:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_reg;
        CData/*2:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__state_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_last_word;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tdata_masked;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_data_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_keep_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_id_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_dest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__last_word_user_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_valid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_pad_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_truncate_next;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdata_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tlast_int;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_int;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_int;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tready_int_early;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__s_axis_tready_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tkeep_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tvalid_next;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tid_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tdest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__m_axis_tuser_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdata_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tkeep_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tvalid_next;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tlast_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tid_reg;
        CData/*7:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tdest_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__temp_m_axis_tuser_reg;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_output;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_int_to_temp;
        CData/*0:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__store_axis_temp_to_output;
        CData/*0:0*/ __Vtrigprevexpr___TOP__tb_natural_inventory__DOT__dut__DOT__dut__DOT__m_axis_tvalid_int__0;
        CData/*0:0*/ __VstlDidInit;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__tb_natural_inventory__DOT__clk__0;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VinactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
        SData/*15:0*/ tb_natural_inventory__DOT____Vtogcov__h_length;
        SData/*15:0*/ tb_natural_inventory__DOT____Vtogcov__h_original_length;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__frame_ptr_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__short_counter_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__long_counter_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_length_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__status_frame_original_length_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_min;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__length_max;
    };
    struct {
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__frame_ptr_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__short_counter_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_reg;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__long_counter_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_length_next;
        SData/*15:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT____Vtogcov__status_frame_original_length_next;
        IData/*31:0*/ tb_natural_inventory__DOT__dut__DOT__dut__DOT__word_cnt;
        IData/*31:0*/ __VactIterCount;
        IData/*31:0*/ __VinactIterCount;
        IData/*31:0*/ __Vi;
        VlUnpacked<QData/*63:0*/, 2> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggeredAcc;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };
    VlDelayScheduler __VdlySched;

    // INTERNAL VARIABLES
    Vtb_natural_inventory__Syms* vlSymsp;
    const char* vlNamep;
    uint32_t __Vcoverage[893]{};

    // CONSTRUCTORS
    Vtb_natural_inventory___024root(Vtb_natural_inventory__Syms* symsp, const char* namep);
    ~Vtb_natural_inventory___024root();
    VL_UNCOPYABLE(Vtb_natural_inventory___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
    void __vlCoverInsert(uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp, const char* linescovp,
        const char* fsmVarp, const char* fsmFromp, const char* fsmTop, const char* fsmTagp);
    void __vlCoverToggleInsert(int begin, int end, bool ranged, uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp);
};


#endif  // guard
