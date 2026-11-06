// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VLITERAL_REPLAY__SYMS_H_
#define VERILATED_VLITERAL_REPLAY__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vliteral_replay.h"

// INCLUDE MODULE CLASSES
#include "Vliteral_replay___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vliteral_replay__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vliteral_replay* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vliteral_replay___024root      TOP;

    // CONSTRUCTORS
    Vliteral_replay__Syms(VerilatedContext* contextp, const char* namep, Vliteral_replay* modelp);
    ~Vliteral_replay__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard
