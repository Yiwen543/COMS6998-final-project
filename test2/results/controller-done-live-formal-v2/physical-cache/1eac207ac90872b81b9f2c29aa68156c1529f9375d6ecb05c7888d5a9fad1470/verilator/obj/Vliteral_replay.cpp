// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vliteral_replay__pch.h"

//============================================================
// Constructors

Vliteral_replay::Vliteral_replay(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vliteral_replay__Syms(contextp(), _vcname__, this)}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vliteral_replay::Vliteral_replay(const char* _vcname__)
    : Vliteral_replay(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vliteral_replay::~Vliteral_replay() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vliteral_replay___024root___eval_debug_assertions(Vliteral_replay___024root* vlSelf);
#endif  // VL_DEBUG
void Vliteral_replay___024root___eval_static(Vliteral_replay___024root* vlSelf);
void Vliteral_replay___024root___eval_initial(Vliteral_replay___024root* vlSelf);
void Vliteral_replay___024root___eval_settle(Vliteral_replay___024root* vlSelf);
void Vliteral_replay___024root___eval(Vliteral_replay___024root* vlSelf);

void Vliteral_replay::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vliteral_replay::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vliteral_replay___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vliteral_replay___024root___eval_static(&(vlSymsp->TOP));
        Vliteral_replay___024root___eval_initial(&(vlSymsp->TOP));
        Vliteral_replay___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vliteral_replay___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vliteral_replay::eventsPending() { return !vlSymsp->TOP.__VdlySched.empty() && !contextp()->gotFinish(); }

uint64_t Vliteral_replay::nextTimeSlot() { return vlSymsp->TOP.__VdlySched.nextTimeSlot(); }

//============================================================
// Utilities

const char* Vliteral_replay::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vliteral_replay___024root___eval_final(Vliteral_replay___024root* vlSelf);

VL_ATTR_COLD void Vliteral_replay::final() {
    contextp()->executingFinal(true);
    Vliteral_replay___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vliteral_replay::hierName() const { return vlSymsp->name(); }
const char* Vliteral_replay::modelName() const { return "Vliteral_replay"; }
unsigned Vliteral_replay::threads() const { return 1; }
void Vliteral_replay::prepareClone() const { contextp()->prepareClone(); }
void Vliteral_replay::atClone() const {
    contextp()->threadPoolpOnClone();
}
