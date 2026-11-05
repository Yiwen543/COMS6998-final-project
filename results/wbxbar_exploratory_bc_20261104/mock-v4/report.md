# WBXBAR B/C result — mock

Run status: completed. Model generation requests: 0; token-count requests: 0.
Simulation executions: 42; physical cycles: 8400; compilations: 2.

| Arm | Rep | Raw target round | Checker-complete target round | Final branch points |
|---|---:|---|---|---:|
| B | 1 | not reached | not reached | 36 |
| B | 2 | not reached | not reached | 36 |
| B | 3 | not reached | not reached | 36 |
| C | 1 | not reached | not reached | 36 |
| C | 2 | not reached | not reached | 36 |
| C | 3 | not reached | not reached | 36 |

All failed and not-reached sessions are retained. Raw attainment is distinct from a checker-complete batch. Pending/ambiguous/error-boundary observations do not become verified passes. Repeated diagnostics are not distinct defect types.

Token ROI = newly hit original DUT branch points since the seed / API-reported input-plus-output tokens × 1,000. Cached input and reasoning output are subsets, not added twice. Unknown usage remains flagged in raw logs.

This is a known-easy-target exploratory comparison, with three sessions per arm and no length placebo. No statistical significance or isolated semantic benefit can be claimed from it. Ordinary offline traffic already reaches all targets. Active session time excludes other interleaved sessions and shared compilation; full wall/compile/preprocessing accounting is in metadata.json.

**These are offline checks, not evidence about LLM coverage performance.**
