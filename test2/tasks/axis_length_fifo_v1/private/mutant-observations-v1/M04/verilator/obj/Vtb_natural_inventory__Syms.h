// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VTB_NATURAL_INVENTORY__SYMS_H_
#define VERILATED_VTB_NATURAL_INVENTORY__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vtb_natural_inventory.h"

// INCLUDE MODULE CLASSES
#include "Vtb_natural_inventory___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vtb_natural_inventory__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vtb_natural_inventory* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vtb_natural_inventory___024root TOP;

    // COVERAGE
    uint32_t __Vcoverage[1925];

    // CONSTRUCTORS
    Vtb_natural_inventory__Syms(VerilatedContext* contextp, const char* namep, Vtb_natural_inventory* modelp);
    ~Vtb_natural_inventory__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
