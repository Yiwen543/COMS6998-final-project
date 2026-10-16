// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VTB_FIXED_PRIORITY_ARBITER__SYMS_H_
#define VERILATED_VTB_FIXED_PRIORITY_ARBITER__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vtb_fixed_priority_arbiter.h"

// INCLUDE MODULE CLASSES
#include "Vtb_fixed_priority_arbiter___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vtb_fixed_priority_arbiter__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vtb_fixed_priority_arbiter* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vtb_fixed_priority_arbiter___024root TOP;

    // COVERAGE
    uint32_t __Vcoverage[200];

    // CONSTRUCTORS
    Vtb_fixed_priority_arbiter__Syms(VerilatedContext* contextp, const char* namep, Vtb_fixed_priority_arbiter* modelp);
    ~Vtb_fixed_priority_arbiter__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
