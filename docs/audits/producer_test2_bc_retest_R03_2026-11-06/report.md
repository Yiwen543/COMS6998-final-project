# R03 P18-R1 repair — live not executed

R03 fixes the sole material finding in the exact R02 review: returned tier must
be explicitly default. Missing/null/other tiers no longer qualify or settle.
The R02 CHANGES_REQUIRED review and its null-tier counterexample are retained,
including verbatim copies in this directory. No real API/overspend was observed.

| New narrow probe | Result |
|---|---|
| Missing service_tier field | Halt before candidate acceptance/compile/next request; raw JSON retained;5910168microUSD reserve;0SETTLE |
| Explicit null tier | Same refusal and full reservation retention; null remains distinguishable from missing in raw provider JSON |
| Nondefault flex tier | Same refusal and full reservation retention |
| Explicit default,64000input/8192output | Qualifies response/settles487168microUSD upper;unused5423000released;not invoice/refund or SV correctness |

Four new probes PASS/0fail/0error,0.175137584s. Rejected caller paths retain six
NOT_RUN snapshots and972unresolved metadata records without compiler/monitor
replay or scientific grading. These are fixtures, not live model samples.
No18+1/full mock/G1/base suite was rerun. The executed-source copies match final
runtime/probe source and registration. Mechanical comparison permits only new
registration/review/EXECUTE namespaces plus the strict tier equality. Release
and supervision remain byte-identical. R02's203sealedmembers/943dependencies are
hash-verified unchanged; no old score, failure, unknown or denominator is edited.

All other method/finance/runtime limits remain: fixed B/raw and C/raw+E-graph,
one independent session/arm x3rounds on the old published benchmark; zero remote
counts; local64k ESTIMATE and actual-response qualification threshold; output8192,
max12generations,20USD API ceiling,5910168microUSD full-context dispatch reserve,
total3600s including cleanup. Same local onepass12compile/990replays/204444cycles,
0newDUT/native/setup/formal/G1/crossIP. The Claude oracle, stimulus, monitor ABI,
raw12/N10/38unknown and all prior outcomes remain. No new hidden study, placebo,
E-graph benefit, actual transport/timing/billing or hard realtime proof is claimed.

Preparation made0API/network/auth/keycontent/SV/supervisedprocess calls, with no
installation, commit or push. Key stays staged; no new budget/key is requested.
The source manifest includes the preserved prior-review snapshot, not the mutable
P18 current reviewer filename. Read phase.json,delta-verification.json and the
review prompt for exact hashes and scope. Only an accepted exact R03 delta review
plus root BC_RETEST_EXECUTE_V3 can enable the one new live root. R02 cannot run.
