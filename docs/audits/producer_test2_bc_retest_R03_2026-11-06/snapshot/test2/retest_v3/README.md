# R03: explicit returned tier repair

Prepared for an exact P18 delta precheck, then a separate root EXECUTE. No live
API, key read/hash, network probe or SystemVerilog run occurred in preparation.
R02 remains sealed with its CHANGES_REQUIRED review and counterexample intact.

The only behavior change is `returned_service_tier == 'default'`. A missing,
null or other returned tier halts before candidate acceptance, compilation or
another request. The entire5910168microUSD reservation and provider JSON remain;
there is no SETTLE journal entry. Explicit default64000input/8192output still
settles487168microUSD, an upper estimate rather than an invoice or refund.

Runtime source was mechanically copied from R02 with new registration/review/
EXECUTE namespaces. Release and supervision are byte-identical. Prompts, model,
zero remote counts, local estimates, financial policy, USD20 ceiling, max12
generations/output8192, total3600s and one-pass local caps remain unchanged.
This is the same known published old-benchmark B/C1session/arm x3rounds retest;
no new hidden set, placebo or C benefit is established. Claude oracle and fixed
stimuli remain unchanged; all old failures and raw12/N10/38unknown remain.

`tier_probes.py` ran four synthetic delta checks only. Three exercise the early
halt via the unchanged caller, with no accepted candidate, compiler or replay;
one checks the explicit-default response/settlement. They are not model samples,
a complete mock/replay or independent scientific scores. R01/R02 full suites,
G1, physics and actual transport were not rerun. Inspect saved evidence instead
of repeating completed checks for context.

The future gated entry is `test2/retest_v3/cli.py`; its live run root is
`test2/results/controller-done-bc-retest-v3`. Exact review scope must be
`BC_RETEST_V3_EXACT_PRECHECK`; exact root receipt kind must be
`BC_RETEST_EXECUTE_V3`. No receipt is created by preparation. The staged key is
retained; another key request or additional budget is unnecessary for this repair.
