// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vliteral_replay.h for the primary calling header

#include "Vliteral_replay__pch.h"

void Vliteral_replay___024root___ctor_var_reset(Vliteral_replay___024root* vlSelf);

Vliteral_replay___024root::Vliteral_replay___024root(Vliteral_replay__Syms* symsp, const char* namep)
    : __VdlySched{*symsp->_vm_contextp__}
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vliteral_replay___024root___ctor_var_reset(this);
}

void Vliteral_replay___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vliteral_replay___024root::~Vliteral_replay___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
