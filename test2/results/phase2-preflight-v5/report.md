# test2 phase2 offline preflight

Saved v1 evidence was read again; old experiments/tests were not rerun.

- Frozen members matched: 3486
- Saved formal statuses: {'TIMEOUT': 31, 'PASS': 12, 'FAIL': 29}
- Saved correct-control bmc/prove: {'TIMEOUT': 24}
- Saved C/B token difference: 6.523144%

## New slot calibration

One predeclared saved candidate, public correct DUT, no new candidate generation.
BMC PASS is bounded only; FAIL needs independent reference adjudication.

| Job | Status | Seconds | Model memory bits |
|---|---|---:|---:|
| always_true | PASS | 0.373 | 0 |
| always_false | FAIL | 0.260 | 0 |
| slot0 | PASS | 2.517 | 0 |
| slot1 | TIMEOUT | 11.807 | 0 |
| slot2 | TIMEOUT | 11.252 | 0 |
| slot3 | TIMEOUT | 11.312 | 256 |
| slot4 | PASS | 0.843 | 0 |
| slot5 | PASS | 0.319 | 0 |

Suite status: incomplete
New formal jobs: 8; measured seconds: 38.683

## Boundary

No API calls or new DUT simulations. No old source/reference/freeze/result changes.
Not a new effectiveness trial, not proof of monitor soundness, and not a live gate.
See docs/test2_phase2_preflight_2026-11-04.md for interpretation and remaining gates.
