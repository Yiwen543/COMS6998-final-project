# G1 E01 execution outcome — 2026-11-06 America/New_York

Status: **EXECUTED_PENDING_P11_SAVED_EVIDENCE_REVIEW**.
Outcome: **HALTED_DURING_FIRST_SETUP_NO_QC_EXECUTED**. This is not G1 qualification success.

The exact R02 command was invoked once under the accepted receipt. Runner exited1
and its raw stdout/stderr are empty. The first `yosys -V` job was dispatched,
then `/bin/ps` supervision raised the saved PermissionError. The supervisor
recorded ERROR, a process-group kill attempt and persistent halt. The root exit
code is null/UNKNOWN; do not invent a successful/failed Yosys version result or
say that a language control failed. No version output was collected.

| Actual root-job category | Dispatched/reserved | NOT_RUN |
|---|---:|---:|
| Setup/version | 1 ERROR | 7 |
| Compilation | 0 | 18 |
| Native BMC/activation cover | 0 | 32 |
| Physical Icarus/Verilator | 0 | 32 |

All16 QC execution outcomes are NOT_RUN, with0 physical cycles/rows and no actual
native or simulator VCD. Pre-existing analytic VCD regression fixtures remain
preparation evidence; they are not execution traces. QC07/15 ineligibility and
QC12/13 four-state exclusions remain declared scope, not observed cover results.
QC14 transport and128-cycle completion were not exercised.

The registered single pool is now halted/completed; one setup reservation remains
charged. Its recorded global monotonic window is 0.045724458s,
including runner setup/hash/parse/output work. The setup process receipt records
0.005685625s including cleanup. Empty PID
observations do not prove no children; monitoring was denied, so full child
lifecycle and root exit remain unverified. Local peak memory is unmeasured.
Unused counts32compile/32native/32physical/1024cycles/7setup are not a new grant,
permission to repair this profile, or permission to reset/restart its pool.

No source, labels, flags, cap or profile was changed after outcome. No retry,
smoke test, simulator, solver, native job, API/count/generation/Claude/key access,
network/install/delete/commit/push occurred in postprocessing. Only saved JSON,
logs/hashes and metadata are inspected; no process/signal diagnostic is retried.
The saved PermissionError identifies the execution-environment refusal.

P10B PASS_WITH_LIMITS remains execution-precheck acceptance only; frozen R02,
R01/P10 CHANGES_REQUIRED and all old evidence remain unchanged. P11 should read
the exact saved report/pool/job receipts, source and public arithmetic only,
with0 extra compiler/native/physical jobs and no refreshed budget. Hallmark use
is applicability-limited organization/critique, not an RTL or UI workflow pass.
No conclusion about E-graph or B/C efficacy, real DUT/oracle/monitor correctness,
old74 witnesses or128/unbounded completion follows from this halted setup.
