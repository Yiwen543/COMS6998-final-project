# G1 R03 continuation preparation

Status: **PREPARED_PENDING_P12_INCREMENTAL_REVIEW**. Producer repairs and pure
mock evidence only. No real R03 setup/version, compiler, solver, physical
simulation, process scan, or pool/attempt-lock creation has occurred.

The coordinator's hash-bound continuation decision routes one reasonable retry
within the original grant. It does not enlarge resources or permissions. The
immutable E01 pool remains halted/completed: setup1 consumed, one ERROR,
89 NOT_RUN jobs and all16 QC NOT_RUN. Version/root exit remain UNKNOWN. P11
accepted integrity with limits and required the process-inventory repair;
neither E01 nor this preparation qualifies G1.

## Owned process group and optional inventory

The registered runner passes no inventory callback and never dispatches ps or
another external inventory command. Its receipt records known predecessor
PermissionError, exact pool hash, attempts0 and inventory_complete=false.
Optional inventory errors are separately exercised only through injected mocks.
Normal root exit is independently observed by poll/wait; inventory failure
does not manufacture or erase it.

Popen start_new_session establishes the owned root PID/PGID. Absolute deadlines,
root poll/wait, owned-group probe, killpg and cleanup remain mandatory. Required
API failures retain explicit errors and fatal/unresolved status. A missing owned
group at its probe is not a complete process census. This does not guarantee
containment of detached/adversarial descendants, whole-host accounting, or OS
hard realtime. Blocking fsync, scheduling and cleanup can overrun; every observed
overrun must fail closed rather than receive successful qualification credit.

## One cumulative allocation

Original caps remain32 compile roots/20s,32 BMC+cover/10s/depth8,32 physical
runs/2s/max32cycles each,1024 physical cycles and1200 cumulative execution-window
seconds. The stricter setup8/2s cap remains. E01 measured window is
0.04572445806115866s. Its conservative allocation charge is2s, not measured
spend. R03 therefore receives at most1198s, with work cutoff1193s. The current
clock origin precedes exclusive attempt-claim persistence and never resets.

The new exclusive ledger inherits reserved.setup=1 and remaining setup7;
attempt_reserved starts0. Prior measured time, conservative charge and current
elapsed checkpoints are separate. Missing/drifting predecessors, false prior0,
expanded remaining allowance/caps, old review receipts and duplicate starts
are refused. Old pool bytes are never reopened or changed. Final ledger
persistence is inside the current window: a post-write cap crossing durably
halts and causes runner failure. The final ledger is authoritative if an
earlier report was serialized before that halt. Timing fields are checkpoint
observations; persisting an observed failure cannot undo an OS overrun.

The plan has89 jobs:7 setup,18 logical compile batches,32 native and32 physical
jobs/128 cycles. Only setup-make is omitted. Make path/hash and version argv are
retained; its version is NOT_REPROBED_TO_PRESERVE_CUMULATIVE_SETUP_CAP. All other
native/physical/compile flags and order match R02 after namespace normalization.
Logical compilation batches include their internal compiler children and logs
inside root/global limits;18 batches does not mean18 OS processes.

## Fixed semantics and retained regressions

All24 protected semantic/reference materials from the R02 change map are
byte-identical:18 SV files,3 original input/expectation JSONs, support matrix,
legacy contracts.py and mock_tests.py. The latter two remain unexecuted archival
references. The real runner imports continuation_contracts.py. observations.py
and exact P10 analytic full/truncated VCD fixtures also remain unchanged.
P10's mathematical labels are reused as limited prior review, not new native
qualification. No Claude oracle, real DUT, hidden data, model prompt or score
is modified.

Pure suites freeze Python sources before execution and save final-mutated
inputs, SHA bindings, result JSON and unittest logs in new result directories:

| Saved suite | Tests | Failures | Meaning |
|---|---:|---:|---|
| continuation-attempt1 |27|0|Initial new inventory/cumulative/gate mocks|
| continuation-attempt2 |28|1|Added final-persistence boundary exposes defect|
| continuation-attempt3 |28|0|Final repaired Python source, durable-halt assertion|
| deadline-horizon-attempt1 |14|0|Before final-persistence repair|
| deadline-horizon-attempt2 |14|0|Retained P10 deadline/horizon regressions on final source|

These111 pure test case invocations include the retained failure. Only the final
28+14 are final-source passing evidence. Popen, signals, inventory and runtime
sleep are mocked; these are not model samples or physical/native executions.
No old R01/R02/G0 suite, experiment or companion audit was rerun.

## Exact next gate and limits

The coordinator sends this sealed package to the existing P12 reviewer. No real
EXECUTE receipt exists now. A later receipt must have record_kind
G1_EXECUTE_CONTINUATION_AFTER_P12, stage EXECUTE, exact registration,
source-manifest, original grant, preparation-manifest, continuation-decision
and predecessor-pool hashes, plus p12_review_path/p12_review_sha256. The accepted
P12 review must bind producer_manifest_sha256, registration_sha256 and
continuation_decision_sha256 in input_identity. Old P10/P11 acceptance cannot
start R03. The existing grant needs no repeated user permission/key question.

QC07/15 vacuity earns no correctness/completion credit; QC12/13 four-state
equivalence remains unsupported; QC08/09 native delayed-pre and physical
pre/post stay distinct; QC14 is final-post transport only. No128-cycle or
unbounded completion, real DUT/oracle/monitor soundness, attribution of all74
old unreproduced witnesses, or C-benefit claim follows. Old540 statuses,
11/11 ties, unknowns, negative results, billing and P04/P05/P06/P05-N1/F1/H1/H2/L1
limits remain. No G2–G5, API/count/generation/Claude/key/network/install/delete,
git add/reset/commit/push, new agent or chat is part of R03 preparation.
