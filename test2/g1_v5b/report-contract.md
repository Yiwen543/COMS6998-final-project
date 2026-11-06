# R05B report contract (g1.public_run_report version 3)

`jobs` contains only the72 newly planned roots. `reused_jobs` separately contains
10 exact old jobs with `new_execution=false` and their original process result.
Reused QC01 cover retains the original NOT_REACHED label inside `original_job`.
Its new `native_evidence` separately records raw tool FAILED,exit1,activation
REACHED and assertion FAILED. No tool failure is rewritten as PASSED.

Native `target_judgment` means only a separately registered public-control target
matched. `qualification_credit=false` throughout preparation. BMC compares its
finite assertion status to the original BMC expectation. Cover compares explicit
activation to the unchanged single `cover(active)` intention;legacy label bytes
are retained. Known positive BMC controls allow no cover assertion failure;QC01
always-false negative control requires the observed cover assertion failure.
Other negative/unsupported controls retain cover trace assertion outcomes as
raw diagnostics;BMC remains their separately registered assertion judgment.
No absence of failure is an unbounded assertion proof.

Unknown,malformed,missing,contradictory,timeout or unresolved native evidence never
meets a target. Reached trace requires the reported source ID,registered sampled
activation and pinned native VCD terminal sentinel. An explicit UNREACHED report
is scoped to the configured finite invocation,not a proof of unreachability.
Physical rows,VCD phase binding,guards,4clock edges and finalpost marker retain
the original contract. Eligibility/vacuity/four-state/128-completion exclusions
remain in every public-control result;none is promoted to realDUT/oracle evidence.

The authoritative final resource record is the new execution-state ledger,not
its earlier report snapshot. It inherits all E01/E02/E03 counts and checkpoints.
No new execution may start without exact P16 acceptance and coordinator EXECUTE.
