# Controller B/C matched-cap experiment

Mode: mock. Independent finite-trace reference unchanged; all36 snapshots frozen before hidden scoring. Fixed stimuli and raw3168 coverage counters do not change across monitor rounds.

| Arm | Rep | Selected round | No alarms/unknown on correct controls | Valid distinct faults /11 observable (/12 raw) | Eligible pairs /106 | Input+output tokens through round6 |
|---|---:|---:|---|---:|---:|---:|
| B2_raw | 1 | 6 | True | 0 | 0 | None |
| B2_raw | 2 | 6 | True | 0 | 0 | None |
| B2_raw | 3 | 6 | True | 0 | 0 | None |
| C2_semantic | 1 | 6 | True | 0 | 0 | None |
| C2_semantic | 2 | 6 | True | 0 | 0 | None |
| C2_semantic | 3 | 6 | True | 0 | 0 | None |

## Predeclared strata

| Arm | Rep | Stratum | Observable / raw faults | Killed types | Eligible-pair kills / pairs |
|---|---:|---|---:|---|---:|
| B2_raw | 1 | boundary_guard | 4 / 4 | none | 0 / 40 |
| B2_raw | 1 | handshake_reset | 3 / 4 | none | 0 / 22 |
| B2_raw | 1 | payload_status | 4 / 4 | none | 0 / 44 |
| B2_raw | 2 | boundary_guard | 4 / 4 | none | 0 / 40 |
| B2_raw | 2 | handshake_reset | 3 / 4 | none | 0 / 22 |
| B2_raw | 2 | payload_status | 4 / 4 | none | 0 / 44 |
| B2_raw | 3 | boundary_guard | 4 / 4 | none | 0 / 40 |
| B2_raw | 3 | handshake_reset | 3 / 4 | none | 0 / 22 |
| B2_raw | 3 | payload_status | 4 / 4 | none | 0 / 44 |
| C2_semantic | 1 | boundary_guard | 4 / 4 | none | 0 / 40 |
| C2_semantic | 1 | handshake_reset | 3 / 4 | none | 0 / 22 |
| C2_semantic | 1 | payload_status | 4 / 4 | none | 0 / 44 |
| C2_semantic | 2 | boundary_guard | 4 / 4 | none | 0 / 40 |
| C2_semantic | 2 | handshake_reset | 3 / 4 | none | 0 / 22 |
| C2_semantic | 2 | payload_status | 4 / 4 | none | 0 / 44 |
| C2_semantic | 3 | boundary_guard | 4 / 4 | none | 0 / 40 |
| C2_semantic | 3 | handshake_reset | 3 / 4 | none | 0 / 22 |
| C2_semantic | 3 | payload_status | 4 / 4 | none | 0 / 44 |

## Actual token accounting

Generation requests: 0; unaccepted: 0; usage missing: 0; count requests during generation: 0; initial count requests:4. Failed attempts are included in cumulative tokens. Cached input/reasoning output are subsets, never added twice. Budget violations: 0. Actual prompt lengths need not be equal under matched caps.

- B2_raw: total tokens/session [None, None, None]; mean None; cost-to-all11 [{'repetition': 1, 'reached': False, 'round': None, 'tokens': None}, {'repetition': 2, 'reached': False, 'round': None, 'tokens': None}, {'repetition': 3, 'reached': False, 'round': None, 'tokens': None}].
- C2_semantic: total tokens/session [None, None, None]; mean None; cost-to-all11 [{'repetition': 1, 'reached': False, 'round': None, 'tokens': None}, {'repetition': 2, 'reached': False, 'round': None, 'tokens': None}, {'repetition': 3, 'reached': False, 'round': None, 'tokens': None}].
- C mean token change: None%.

## Formal scope

Final six candidates only. Correct source:6 slots × bmc/prove/cover ×10s;12 faults ×6 slots ×bmc ×5s. Depth24, Z3, flatten;540s declared solver caps and720s overall cap/candidate. PASS in bounded/cover modes is separate from proof. TIMEOUT/ERROR/NOT_RUN and failed induction remain unresolved. Reachable BMC witnesses are classified only by the frozen independent reference.


## Limits

Three sessions per arm on one previously inspected IP family. Descriptive comparisons only; no significance claim. C is a larger feedback package without a token-matched placebo, so this does not isolate pure E-graph semantics. All four supplied semantic groups already have development source hits; representation/guard interpretation rather than uncovered-source discovery is being tested. M08 is retained among12 raw faults with no independently confirmed fixed-trace violation. The other11 have106/144 eligible simulator/trace pairs; ineligible and unknown outcomes remain in raw records. Correct-control acceptance is finite evidence, not complete monitor soundness or proof of full design correctness. Formal assumes legal held input offers, reset, and1..12 accepted bytes per frame; no fairness/liveness proof.

Machine evidence: `audit.json`, `rounds.csv`, immutable generation release and scoring completion hashes above.
