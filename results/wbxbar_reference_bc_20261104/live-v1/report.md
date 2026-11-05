# WBXBAR B/C result — live

Run status: completed. Model generation requests: 36; token-count requests: 36.
Simulation executions: 42; physical cycles: 8400; compilations: 2.

| Arm | Rep | Raw target round | Checker-complete target round | Final branch points |
|---|---:|---|---|---:|
| B | 1 | 1 | not reached | 79 |
| B | 2 | 1 | not reached | 79 |
| B | 3 | 1 | not reached | 79 |
| C | 1 | 1 | not reached | 79 |
| C | 2 | 1 | not reached | 79 |
| C | 3 | 1 | not reached | 79 |

All failed and not-reached sessions are retained. Raw attainment is distinct from a checker-complete batch. Pending/ambiguous/error-boundary observations do not become verified passes. Repeated diagnostics are not distinct defect types.

Token ROI = newly hit original DUT branch points since the seed / API-reported input-plus-output tokens × 1,000. Cached input and reasoning output are subsets, not added twice. Unknown usage remains flagged in raw logs.

This is a known-easy-target exploratory comparison, with three sessions per arm and no length placebo. No statistical significance or isolated semantic benefit can be claimed from it. Ordinary offline traffic already reaches all targets. Active session time excludes other interleaved sessions and shared compilation; full wall/compile/preprocessing accounting is in metadata.json.

## Frozen reference-checker outcomes

| Arm | Rep | Final verdict | Unknown records | Failure instances |
|---|---:|---|---:|---:|
| B | 1 | unresolved | 15 | 0 |
| B | 2 | unresolved | 11 | 0 |
| B | 3 | unresolved | 8 | 0 |
| C | 1 | unresolved | 16 | 0 |
| C | 2 | unresolved | 15 | 0 |
| C | 3 | unresolved | 21 | 0 |

Full unknown lists, property statuses and scope counts remain in each batch result and rounds JSONL. They are never recoded as passes. Final diagnostics are not independently established DUT defects.
