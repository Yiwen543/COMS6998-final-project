// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vtb_natural_inventory__pch.h"

//============================================================
// Constructors

Vtb_natural_inventory::Vtb_natural_inventory(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vtb_natural_inventory__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vtb_natural_inventory::Vtb_natural_inventory(const char* _vcname__)
    : Vtb_natural_inventory(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vtb_natural_inventory::~Vtb_natural_inventory() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vtb_natural_inventory___024root___eval_debug_assertions(Vtb_natural_inventory___024root* vlSelf);
#endif  // VL_DEBUG
void Vtb_natural_inventory___024root___eval_static(Vtb_natural_inventory___024root* vlSelf);
void Vtb_natural_inventory___024root___eval_initial(Vtb_natural_inventory___024root* vlSelf);
void Vtb_natural_inventory___024root___eval_settle(Vtb_natural_inventory___024root* vlSelf);
void Vtb_natural_inventory___024root___eval(Vtb_natural_inventory___024root* vlSelf);

void Vtb_natural_inventory::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vtb_natural_inventory::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vtb_natural_inventory___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vtb_natural_inventory___024root___eval_static(&(vlSymsp->TOP));
        Vtb_natural_inventory___024root___eval_initial(&(vlSymsp->TOP));
        Vtb_natural_inventory___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vtb_natural_inventory___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vtb_natural_inventory::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty() && !contextp()->gotFinish(); }

uint64_t Vtb_natural_inventory::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vtb_natural_inventory::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vtb_natural_inventory___024root___eval_final(Vtb_natural_inventory___024root* vlSelf);

VL_ATTR_COLD void Vtb_natural_inventory::final() {
    contextp()->executingFinal(true);
    Vtb_natural_inventory___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vtb_natural_inventory::hierName() const { return vlSymsp->name(); }
const char* Vtb_natural_inventory::modelName() const { return "Vtb_natural_inventory"; }
unsigned Vtb_natural_inventory::threads() const { return 1; }
void Vtb_natural_inventory::prepareClone() const { contextp()->prepareClone(); }
void Vtb_natural_inventory::atClone() const {
    contextp()->threadPoolpOnClone();
}
