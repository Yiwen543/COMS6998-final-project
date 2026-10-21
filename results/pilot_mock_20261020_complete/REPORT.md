# Arbiter A/B/C pilot

Mode: **mock**. Offline mock stimuli validate infrastructure; these are not LLM performance results.

A receives specification, RTL, common initial stimulus and checker logs. B adds every raw uncovered DUT point. C adds bounded egg equivalence evidence and unmapped-point disclosure to B's exact raw evidence.

| Arm | Repetition | Final branch | Line | Toggle | Distinct defects | API tokens | Cycles | Executions | Target 17/18 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 1 | 13/18 | 8/11 | 60/60 | 2 | n/a | 336 | 4 | not reached |
| A | 2 | 16/18 | 10/11 | 60/60 | 2 | n/a | 336 | 4 | not reached |
| A | 3 | 13/18 | 8/11 | 60/60 | 2 | n/a | 336 | 4 | not reached |
| B | 1 | 13/18 | 8/11 | 60/60 | 2 | n/a | 336 | 4 | not reached |
| B | 2 | 16/18 | 10/11 | 60/60 | 2 | n/a | 336 | 4 | not reached |
| B | 3 | 13/18 | 8/11 | 60/60 | 2 | n/a | 336 | 4 | not reached |
| C | 1 | 13/18 | 8/11 | 60/60 | 2 | n/a | 336 | 4 | not reached |
| C | 2 | 16/18 | 10/11 | 60/60 | 2 | n/a | 336 | 4 | not reached |
| C | 3 | 13/18 | 8/11 | 60/60 | 2 | n/a | 336 | 4 | not reached |

Final C−B branch-point differences by matched repetition: [0, 0, 0]; range 0 to 0. These are arm-blind mock outcomes and provide no evidence of model benefit.

| Arm | Rep | First target round | Tokens at target/stop | Cycles | Executions | Wall seconds | Token ROI |
|---|---:|---|---:|---:|---:|---:|---:|
| A | 1 | not reached | n/a | 336 | 4 | 0.025299 | n/a |
| A | 2 | not reached | n/a | 336 | 4 | 0.03047 | n/a |
| A | 3 | not reached | n/a | 336 | 4 | 0.019161 | n/a |
| B | 1 | not reached | n/a | 336 | 4 | 0.018473 | n/a |
| B | 2 | not reached | n/a | 336 | 4 | 0.018365 | n/a |
| B | 3 | not reached | n/a | 336 | 4 | 0.022404 | n/a |
| C | 1 | not reached | n/a | 336 | 4 | 0.17522 | n/a |
| C | 2 | not reached | n/a | 336 | 4 | 0.176294 | n/a |
| C | 3 | not reached | n/a | 336 | 4 | 0.175407 | n/a |

All rows use the original DUT, frozen specification and checker, one Verilator instrumented binary, and raw 18-point branch denominator. Line means Verilator block/elsif points; branch includes control and ternary outcomes; toggle is per-direction DUT bit transition. Expression counters are retained in JSON/CSV. Testbench counters are excluded.
Each round replays the same four-cycle reset/initial sequence followed by **all** accumulated generated actions. The measured cycles sum every replay. Each simulator process starts fresh; checker failures are collected while coverage is flushed. Common initialization and reset activity count in every round's coverage and cycles.

Token ROI = newly covered raw DUT branch points relative to the common initial run, per 1,000 API-reported input-plus-output tokens. Cached input and reasoning output details are informational subsets, not added again. Mock token ROI is undefined.

Egg normalization is limited to unsigned one-bit binary/two-state combinational winner predicates. Its six named Boolean rewrites are truth-table validated and saturated with finite limits. Distinct winner cases retain separate E-classes. Clock/reset transitions and all original coverage locations remain separate; an equivalent predicate never transfers a hit count. Yosys provides frontend/process extraction, while the RTL-to-expression bridge remains a hash-guarded, arbiter-specific source adapter.

The original DUT still violates the synchronous reset and one-hot override specification. Repeated checker failures count as two distinct categories at most. The checker was independently validated against derived conforming and single-defect controls. A fresh exhaustive ceiling is measured separately from model prompts and costs.

The arbiter has little cross-location semantic redundancy, so a C advantage is not guaranteed. A next discriminating experiment should use nested/repeated equivalent predicates with equivalence-checked RTL variants, then a FIFO with full/empty, simultaneous read/write, wraparound and reset-during-operation cases.

Exact metadata, per-call responses, rendered prompts, raw coverage files, source mappings and per-round CSV/JSONL are adjacent to this report.
