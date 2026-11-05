// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtb_natural_inventory.h for the primary calling header

#include "Vtb_natural_inventory__pch.h"

void Vtb_natural_inventory___024root___ctor_var_reset(Vtb_natural_inventory___024root* vlSelf);

Vtb_natural_inventory___024root::Vtb_natural_inventory___024root(Vtb_natural_inventory__Syms* symsp, const char* namep)
    : __VdlySched{*symsp->_vm_contextp__}
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vtb_natural_inventory___024root___ctor_var_reset(this);
}

void Vtb_natural_inventory___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vtb_natural_inventory___024root::~Vtb_natural_inventory___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
