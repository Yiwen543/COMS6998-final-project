// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vtb_fixed_priority_arbiter__pch.h"

//============================================================
// Constructors

Vtb_fixed_priority_arbiter::Vtb_fixed_priority_arbiter(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vtb_fixed_priority_arbiter__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vtb_fixed_priority_arbiter::Vtb_fixed_priority_arbiter(const char* _vcname__)
    : Vtb_fixed_priority_arbiter(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vtb_fixed_priority_arbiter::~Vtb_fixed_priority_arbiter() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vtb_fixed_priority_arbiter___024root___eval_debug_assertions(Vtb_fixed_priority_arbiter___024root* vlSelf);
#endif  // VL_DEBUG
void Vtb_fixed_priority_arbiter___024root___eval_static(Vtb_fixed_priority_arbiter___024root* vlSelf);
void Vtb_fixed_priority_arbiter___024root___eval_initial(Vtb_fixed_priority_arbiter___024root* vlSelf);
void Vtb_fixed_priority_arbiter___024root___eval_settle(Vtb_fixed_priority_arbiter___024root* vlSelf);
void Vtb_fixed_priority_arbiter___024root___eval(Vtb_fixed_priority_arbiter___024root* vlSelf);

void Vtb_fixed_priority_arbiter::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vtb_fixed_priority_arbiter::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vtb_fixed_priority_arbiter___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vtb_fixed_priority_arbiter___024root___eval_static(&(vlSymsp->TOP));
        Vtb_fixed_priority_arbiter___024root___eval_initial(&(vlSymsp->TOP));
        Vtb_fixed_priority_arbiter___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vtb_fixed_priority_arbiter___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vtb_fixed_priority_arbiter::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty() && !contextp()->gotFinish(); }

uint64_t Vtb_fixed_priority_arbiter::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vtb_fixed_priority_arbiter::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vtb_fixed_priority_arbiter___024root___eval_final(Vtb_fixed_priority_arbiter___024root* vlSelf);

VL_ATTR_COLD void Vtb_fixed_priority_arbiter::final() {
    contextp()->executingFinal(true);
    Vtb_fixed_priority_arbiter___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vtb_fixed_priority_arbiter::hierName() const { return vlSymsp->name(); }
const char* Vtb_fixed_priority_arbiter::modelName() const { return "Vtb_fixed_priority_arbiter"; }
unsigned Vtb_fixed_priority_arbiter::threads() const { return 1; }
void Vtb_fixed_priority_arbiter::prepareClone() const { contextp()->prepareClone(); }
void Vtb_fixed_priority_arbiter::atClone() const {
    contextp()->threadPoolpOnClone();
}
