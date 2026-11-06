# G1 R02 — two pre-execution infrastructure repairs

Status: PREPARED_PENDING_P10B_INCREMENTAL_REVIEW. R01/P10 CHANGES_REQUIRED
remains unchanged. These are producer repairs/self-tests, not independent closure.
No real compiler/simulator/solver/version/process job has run; no real pool exists.

The public semantics remain the single G1_PUBLIC_SINGLE_PROFILE_V1 profile.
All18 SV files, original3 input/expectation JSONs, support matrix, tool pins,
flags, job order, clock/reset/initial contract and every cap match R01. Only
namespace paths differ in the executable plan. P10's independent mathematical
label analysis is reused without claiming a new native result or rerunning it.
See the frozen R01 README for the complete public-control semantics and limits.

## P10-R1: refuse before dispatch, without refund or clock reset

Budget reservations store their absolute original root deadline bounded by the
original1195s work cutoff of the1200s pool. After persistence, remaining time is
rechecked; nonpositive/insufficient cleanup margin persists halt plus a charged,
not-dispatched NOT_RUN event. runtime rechecks after mkdir/log opening immediately
before Popen, without another persistence/preparation step in that gap. Already
expired requests are unreserved NOT_RUN. Timeout/cleanup retain the original
absolute root deadline. No reservation refund, retry, restart or new pool occurs.

R02 result artifacts live in g1-qualification-v2, but pool_state deliberately
remains the original, uncreated g1-qualification-v1/execution-state.json path.
Only one accepted implementation can create that exclusive pool. This preserves
one grant across R01/R02; it is not permission to execute either version twice.
R01 cannot pass its CHANGES_REQUIRED review gate. No old result bytes are changed.

## P10-R2: no value extrapolation past the recorded VCD span

parse_vcd records first/last recorded ticks. state_at requires each requested
observation lie inside that span before selecting a previous state. Registered
native alarm candidates also require an in-span timestamp. Missing/truncated
coverage yields explicit VCD_TIME_COVERAGE_MISSING and cannot become matched
control evidence. Full16ns analytic P10 control accepts; exact14ns truncated
counterpart rejects requiredpost15ns specifically for missing time coverage.
Unknown values remain x/z and missing signals keep their distinct refusal reasons.

inputs/p10-regressions contains exact deep copies of P10's complete/truncated
VCD and row table plus origin/SHA provenance. They are hand-constructed analytic
fixtures, not actual simulator output, reachable DUT traces or G1 qualification.

## New tests and evidence

Only regression_tests.py is the R02 test entrypoint. The copied mock_tests.py is
an unchanged historical reference and was not executed. The new14 regressions
cover save/mkdir/log deadline crossings, expired/insufficient windows, ordinary
baseline and original-deadline timeout, no refund/restart, exact VCD pair,
first/last span bounds, selected-native candidate horizon, unknown and missing
signals. Popen, process monitoring, sleep and process-group signals are mocked;
no child executable or real sleep is used. Each execution freezes its exact
source first and saves final-mutated inputs, bindings, results, logs and summary.
No R01/P10/G0 test suite or old experiment/companion is rerun.

The first new suite passed14/14; exact source and commands are in
results/g1-qualification-v2/regression-attempt1 and the R02 handoff package.
All old negative results and P10 original counterexamples remain immutable.
SV syntax, native process lifecycle and dual-simulator ABI remain unexercised.

## Incremental gate and unchanged limits

The coordinator sends this fixed R02 package to the existing P10B reviewer.
Required review phase begins P10; input_identity binds the new producer manifest
and registration. The later non-secret EXECUTE receipt uses
preparation_manifest_sha256 for R02, plus registration/source_manifest/grant
SHA and exact accepted P10B review path/SHA. No EXECUTE receipt exists now.

Same32native(depth8/10s),32physical(1024cycles,32perrun/2s),32logical compile
jobs(20s) and1200s total pool; planned18compile batches/32native/32physical,
128cycles/8setup. P10-N1 accepts batch/root accounting only with all internal
compiler children within root/global costs and raw logs; not18 OS processes.
There is no repair-profile/new execution allowance. Independent post-review
reads saved evidence without another tool budget.

QC07/15 vacuity, QC12/13 four-state exclusions, QC08/09 phase separation,
QC14 transport-only marker, no128/unbounded/real-oracle claims, all historical
P04/P05/P06/P05-N1/F1/selected-sample/category/H1/H2/L1/billing limits remain.
Hallmark is recorded for applicability/fixed-input/ranked/minimal-change
organization only, not a UI workflow or RTL correctness certification.
No API/count/model/Claude/key/network/install/delete/commit/push or G2–G5.
