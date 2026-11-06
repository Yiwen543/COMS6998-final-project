# Final-post marker monitor contract v1

Use the unchanged public DUT pins in specification.md and the supplied module header.
The passive monitor additionally observes readonly trace_done:0 at every pre sample
and all post samples except the final post sample, where it is1. No extra rising
edge follows this marker. Enable finite-end checks combinationally from trace_done
and private state already updated by the final edge. The marker is evaluator
metadata, not a DUT input, truth label, reset or stimulus modification.

Development evaluations require drained=true,min_tail32; final evaluations use
drained=true,min_tail128. Definite failures and unknowns retain their independent
reference meanings; a short tail is never automatically accepted. A presented
valid safety failure is distinct from end-only response/input completion failure.
Independent reference inputs remain exactly the original six inputs/nine outputs;
the marker does not modify the Claude reference function or DUT specification.

Six active/ok slots,body<=16000UTF8bytes,state<=8192bits; readonly public pins,
posedge clk only, no hierarchy/files/assumptions/system calls. Short formal safety
projection explicitly sets trace_done=0 and cannot prove finite completion.
