#include "Vtb_sync_fifo.h"
#include "verilated.h"
#include "verilated_cov.h"
#include <memory>
int main(int argc, char** argv) {
    auto context = std::make_unique<VerilatedContext>();
    context->commandArgs(argc, argv);
    auto top = std::make_unique<Vtb_sync_fifo>(context.get());
    while (!context->gotFinish()) {
        top->eval();
        if (!top->eventsPending()) break;
        context->time(top->nextTimeSlot());
    }
    top->final();
    context->coveragep()->write();
    return context->gotFinish() ? 0 : 2;
}
