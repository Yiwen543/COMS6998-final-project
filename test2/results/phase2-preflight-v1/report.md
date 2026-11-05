# test2 phase2 offline preflight

Saved v1 evidence was read again; old experiments/tests were not rerun.

- Frozen members matched: 3486
- Saved formal statuses: {'TIMEOUT': 31, 'PASS': 12, 'FAIL': 29}
- Saved correct-control bmc/prove: {'TIMEOUT': 24}
- Saved C/B token difference: 6.523144%

## New slot calibration

One predeclared saved candidate, public correct DUT, no new candidate generation.
BMC PASS is bounded only; FAIL needs independent reference adjudication.

| Job | Status | Seconds |
|---|---|---:|
| always_true | TIMEOUT | 6.335 |
| always_false | FAIL | 0.269 |

Suite status: incomplete
New formal jobs: 2; measured seconds: 6.604

## Boundary

No API calls or new DUT simulations. No old source/reference/freeze/result changes.
Not a new effectiveness trial, not proof of monitor soundness, and not a live gate.
See docs/test2_phase2_preflight_2026-11-04.md for interpretation and remaining gates.
