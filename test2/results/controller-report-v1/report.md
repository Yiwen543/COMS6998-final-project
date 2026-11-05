# Controller B/C matched-cap experiment

Mode: live. Independent finite-trace reference unchanged; all36 snapshots frozen before hidden scoring. Fixed stimuli and raw3168 coverage counters do not change across monitor rounds.

| Arm | Rep | Selected round | No alarms/unknown on correct controls | Valid distinct faults /11 observable (/12 raw) | Eligible pairs /106 | Input+output tokens through round6 |
|---|---:|---:|---|---:|---:|---:|
| B2_raw | 1 | 6 | True | 11 | 106 | 301681 |
| B2_raw | 2 | 6 | True | 11 | 106 | 301636 |
| B2_raw | 3 | 6 | True | 11 | 106 | 304374 |
| C2_semantic | 1 | 6 | True | 11 | 106 | 322887 |
| C2_semantic | 2 | 6 | True | 11 | 106 | 324124 |
| C2_semantic | 3 | 6 | True | 11 | 106 | 323479 |

## Predeclared strata

| Arm | Rep | Stratum | Observable / raw faults | Killed types | Eligible-pair kills / pairs |
|---|---:|---|---:|---|---:|
| B2_raw | 1 | boundary_guard | 4 / 4 | M01, M02, M03, M04 | 40 / 40 |
| B2_raw | 1 | handshake_reset | 3 / 4 | M05, M06, M07 | 22 / 22 |
| B2_raw | 1 | payload_status | 4 / 4 | M09, M10, M11, M12 | 44 / 44 |
| B2_raw | 2 | boundary_guard | 4 / 4 | M01, M02, M03, M04 | 40 / 40 |
| B2_raw | 2 | handshake_reset | 3 / 4 | M05, M06, M07 | 22 / 22 |
| B2_raw | 2 | payload_status | 4 / 4 | M09, M10, M11, M12 | 44 / 44 |
| B2_raw | 3 | boundary_guard | 4 / 4 | M01, M02, M03, M04 | 40 / 40 |
| B2_raw | 3 | handshake_reset | 3 / 4 | M05, M06, M07 | 22 / 22 |
| B2_raw | 3 | payload_status | 4 / 4 | M09, M10, M11, M12 | 44 / 44 |
| C2_semantic | 1 | boundary_guard | 4 / 4 | M01, M02, M03, M04 | 40 / 40 |
| C2_semantic | 1 | handshake_reset | 3 / 4 | M05, M06, M07 | 22 / 22 |
| C2_semantic | 1 | payload_status | 4 / 4 | M09, M10, M11, M12 | 44 / 44 |
| C2_semantic | 2 | boundary_guard | 4 / 4 | M01, M02, M03, M04 | 40 / 40 |
| C2_semantic | 2 | handshake_reset | 3 / 4 | M05, M06, M07 | 22 / 22 |
| C2_semantic | 2 | payload_status | 4 / 4 | M09, M10, M11, M12 | 44 / 44 |
| C2_semantic | 3 | boundary_guard | 4 / 4 | M01, M02, M03, M04 | 40 / 40 |
| C2_semantic | 3 | handshake_reset | 3 / 4 | M05, M06, M07 | 22 / 22 |
| C2_semantic | 3 | payload_status | 4 / 4 | M09, M10, M11, M12 | 44 / 44 |

## Actual token accounting

Generation requests: 36; unaccepted: 0; usage missing: 0; count requests during generation: 36; initial count requests:8, including the retained over-cap first representation. Failed attempts are included in cumulative tokens. Cached input/reasoning output are subsets, never added twice. Budget violations: 0. Actual prompt lengths need not be equal under matched caps.

- B2_raw: total tokens/session [301681, 301636, 304374]; mean 302563.6666666667; cost-to-all11 [{'repetition': 1, 'reached': True, 'round': 1, 'tokens': 49074}, {'repetition': 2, 'reached': True, 'round': 1, 'tokens': 48826}, {'repetition': 3, 'reached': True, 'round': 1, 'tokens': 49457}].
- C2_semantic: total tokens/session [322887, 324124, 323479]; mean 323496.6666666667; cost-to-all11 [{'repetition': 1, 'reached': True, 'round': 1, 'tokens': 52382}, {'repetition': 2, 'reached': True, 'round': 1, 'tokens': 52483}, {'repetition': 3, 'reached': True, 'round': 1, 'tokens': 52722}].
- C mean token change: 6.91854386569879%.

## Formal scope

Final six candidates only. Correct source:6 slots × bmc/prove/cover ×10s;12 faults ×6 slots ×bmc ×5s. Depth24, Z3, flatten;540s declared solver caps and720s overall cap/candidate. PASS in bounded/cover modes is separate from proof. TIMEOUT/ERROR/NOT_RUN and failed induction remain unresolved. Reachable BMC witnesses are classified only by the frozen independent reference.

- B2_raw rep1: {'TIMEOUT': 84, 'PASS': 5, 'FAIL': 1}; witness classifications {}; wall 631.291778750252s.
- B2_raw rep2: {'TIMEOUT': 74, 'PASS': 6, 'FAIL': 10}; witness classifications {'reference_confirmed_DUT_violation_on_this_trace': 10}; wall 569.6313840420917s.
- B2_raw rep3: {'TIMEOUT': 88, 'PASS': 2}; witness classifications {}; wall 668.6776194586419s.
- C2_semantic rep1: {'TIMEOUT': 76, 'PASS': 6, 'FAIL': 8}; witness classifications {'reference_confirmed_DUT_violation_on_this_trace': 8}; wall 581.3582015424035s.
- C2_semantic rep2: {'TIMEOUT': 79, 'PASS': 6, 'FAIL': 5}; witness classifications {'reference_confirmed_DUT_violation_on_this_trace': 5}; wall 612.0552097922191s.
- C2_semantic rep3: {'TIMEOUT': 72, 'PASS': 8, 'FAIL': 10}; witness classifications {'reference_confirmed_DUT_violation_on_this_trace': 10}; wall 563.2997553329915s.

## Limits

Three sessions per arm on one previously inspected IP family. Descriptive comparisons only; no significance claim. C is a larger feedback package without a token-matched placebo, so this does not isolate pure E-graph semantics. All four supplied semantic groups already have development source hits; representation/guard interpretation rather than uncovered-source discovery is being tested. M08 is retained among12 raw faults with no independently confirmed fixed-trace violation. The other11 have106/144 eligible simulator/trace pairs; ineligible and unknown outcomes remain in raw records. Correct-control acceptance is finite evidence, not complete monitor soundness or proof of full design correctness. Formal assumes legal held input offers, reset, and1..12 accepted bytes per frame; no fairness/liveness proof.

Machine evidence: `audit.json`, `rounds.csv`, immutable generation release and scoring completion hashes above.
