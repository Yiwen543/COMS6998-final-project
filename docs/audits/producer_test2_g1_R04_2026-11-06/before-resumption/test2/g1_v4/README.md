# G1 R04 — conditional startup repair preparation

Status: PREPARED_PENDING_PHYSICAL33_APPROVAL_AND_P14. No real R04 setup, compile,
native or physical job has run. No pool/attempt lock or approved amendment exists.
G1 remains BLOCKED/NOT_QUALIFIED from P13. The parent is already asking about the
physical cap; this preparation does not repeat that question or assume approval.

## Minimal physical source candidate

Among18 SV files only physical_tb.sv changes. step starts7. At positive1ps the
first loop sets step0, giving a nonzero-time transition after startup processes
are active. The first wait is999ps, later waits remain1ns. Source arithmetic
keeps pre1000/5000/9000/13000ps,edges2000/6000/10000/14000ps,post3000/7000/11000/
15000ps,end16000ps and four posedges. There is no #0 dependency,extra DUT clock,
X-to0 replacement,skipped row or changed finalpost marker. Inputs0..3 and labels
are unchanged. Startup step7 is outside observations/clock edges and is not an
additional scored input cycle.

This is a source-based candidate,not a measured fix. Neither Icarus nor Verilator
has compiled/run this version. Syntax,positive-delay scheduling and full dual
row/VCD agreement still need authorized physical qualification. E02's X rows,
failed physical run and all costs remain immutable.

## Explicit native reuse

common.sv,all16 formal harnesses and23 prior semantic/reference materials stay
byte-identical. observations.py and runtime.py also match R03. native-reuse.json
binds unchanged sources,input tables,labels,profile,depth8,tool pins,old frontend
and native argv,the exact QC00 SMT,raw logs/receipts/cover VCD and P12/E02/P13
identities. The old frontend reads common.sv and QC00_formal.sv,not physical_tb.

native_reuse.py accepts only this exact saved prefix:compile-QC00 and QC00 BMC+
cover become REUSED_FROM_E02,never new root jobs. Original costs are already in
prior counters/time;rejected QC00 physical is never reused. Changed common/SMT/
depth/pins refuse. This is a conditional native-only reuse check,not QC00 full
qualification or a new independent trial. If reuse fails,no automatic rerun:
full fresh native would require cumulative34 rather than32 (+2 approval).

## Resource proposal,not authority

| Resource | Already consumed | New plan | Cumulative | Existing cap |
|---|---:|---:|---:|---:|
| setup |8|0|8|8|
| logical compile roots |3|17|20|32|
| native BMC+cover |2|30|32|32|
| physical runs |1|32|33|32|
| physical cycles |4|128|132|1024|

The plan has79 new roots:15formal builds+2shared physical builds,30native and
32physical. It omits all version queries and the3 explicitly reused QC00 jobs.
All remaining flags/order match R03 after namespace normalization. E02 versions
are reused as saved text/help knownness;make stays NOT_REPROBED,smtbmc version
UNKNOWN. Internal compiler children are within root/global costs,not extra
unreported batches;complete child census is unavailable.

Physical33 is a pending proposal. Original caps still authorize only32;at least
one extra is needed because E02's physical run was rejected. No extra diagnostic
or failure allowance is hidden in the plan. Proposed cumulative charge8 seconds
covers prior charged checkpoint7.151973249856383;it is not measured spend. Prior
actual cumulative checkpoint5.197697583120316 stays separate. Proposed current
window1192/work1187 retains total1200 and no rebasing. budget.py differs from R03
only in its attempt-id;mandatory runtime/deadline/final-save protections remain.

## Conditional gate and tests

runner.py refuses missing/unapproved physical33 amendment/continuation before
claim/pool. Only a later exact P14 acceptance binding actual approval hashes and
coordinator receipt may route execution. authority-requirements.json in the R04
audit documents the absent external records. Proposed caps/constants,source
manifests or a preliminary code-only P14 review cannot grant execution. Current
registration SHA fields for future approvals are null;the actual receipt and
P14 must bind the eventual exact external files. This is a trusted local
coordinator convention,not cryptographic user/provider authentication.

16 pure tests PASS:source timing arithmetic,23 unchanged dependencies,strict
saved native reuse and drift refusal,resource lower bound,missing/unapproved
approval/missing P14/old receipt refusals,actual-entry0claim,and synthetic X-row
rejection. Every test freezes its source and final-mutated inputs/results/logs;
Popen/run/killpg/sleep are forbidden mocks. They do not establish SV scheduling,
new native/physical ABI,approved-entry success,positive Budget integration or
full end-to-end execution. Old111 mocks and all old experiments were preserved,
not rerun. The final new Python/registration/plan/reuse sources match that suite;
README/schema are explanatory metadata.

Next: existing P14 incremental preparation review. Actual approved continuation
and exact bound review/EXECUTE are still required. No real probes or new pool
before that checkpoint. No OS hard realtime/full child census,128/unbounded
completion,real DUT/oracle/monitor soundness,C effect,explanation of74 witnesses
or billing conclusion follows. QC07/15 vacuity,QC12/13 four-state exclusion,
QC14 transport and all old unknown/timeouts/scores/P04/P05/P06/P05-N1/F1/H1/H2/L1
limits remain. No paid API/key/network/install/delete/index/commit/push/PPT,
G2–G5 or new agent/chat is part of this preparation.
