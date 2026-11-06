# G1 R04: positive-time startup repair, pending P14

This version is sealed preparation, not completed G1 qualification. Only
`sources/physical_tb.sv` changes among the 18 SV files: initialize step to 7,
then establish step 0 at 1ps before observation. First wait is 999ps. The original
pre/edge/post ticks, four rising edges, finalpost marker, labels and inputs remain.
The first-row initialization explanation is source-supported, not yet verified
by a repaired simulator run. No X substitution or omitted first row is allowed.

E02 native QC00 compile/BMC/cover can be explicitly reused only with exact source,
SMT, arguments, depth8, tools and raw evidence bindings in `native-reuse.json`.
These are REUSED_FROM_E02, not new trials or physical qualification. The rejected
E02 Icarus trace and every original cost remain immutable.

The already-approved physical33 amendment/continuation and user source are bound
in registration_v4; no new authority is synthesized here. New plan:0 setup,
17 compile,30 native,32 physical,128 cycles. Cumulative if completed:8 setup,
20 compile,32 native,33 physical,132 cycles. Current window<=1192s, inherited
allocation charge8s within1200s;old measured5.197697583s and charged7.151973250s
stay separate. No physical retry reserve exists. If native reuse is invalid,
stop:full rerun would need cumulative34 native,exceeding32 by2.

`r04_tests.py --record <new-path>` runs pure checks with subprocess/signals/sleep
blocked;it cannot establish SV scheduling or dual-simulator agreement. Original
16-case preparation-attempt1 remains;resumed final-source checks are separate.

Next checkpoint:existing independent P14 reviews final source/registration/
preparation manifest plus exact actual amendment/continuation hashes. Only then
may the coordinator issue a new exact EXECUTE receipt. No new pool or lock yet.
No API,keys,installation,cross-IP or scientific conclusion is authorized here.
QC07/15 vacuity,QC12/13 four-state projection,QC14 transport-only and no128-cycle
completion limits remain. See the R04 audit report and P14 checklist.
