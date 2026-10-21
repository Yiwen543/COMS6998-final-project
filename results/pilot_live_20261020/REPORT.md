# Arbiter A/B/C pilot

Mode: **live**. Live Responses API stimuli.

A receives specification, RTL, common initial stimulus and checker logs. B adds every raw uncovered DUT point. C adds bounded egg equivalence evidence and unmapped-point disclosure to B's exact raw evidence.

| Arm | Repetition | Final branch | Line | Toggle | Distinct defects | API tokens | Cycles | Executions | Target 17/18 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 1 | 17/18 | 11/11 | 60/60 | 2 | 15055 | 336 | 4 | reached in round 1 |
| A | 2 | 17/18 | 11/11 | 60/60 | 2 | 15066 | 336 | 4 | reached in round 1 |
| A | 3 | 17/18 | 11/11 | 60/60 | 2 | 15099 | 336 | 4 | reached in round 1 |
| B | 1 | 17/18 | 11/11 | 60/60 | 2 | 19285 | 198 | 4 | reached in round 1 |
| B | 2 | 17/18 | 11/11 | 60/60 | 2 | 19290 | 197 | 4 | reached in round 1 |
| B | 3 | 17/18 | 11/11 | 60/60 | 2 | 19065 | 186 | 4 | reached in round 1 |
| C | 1 | 17/18 | 11/11 | 60/60 | 2 | 27689 | 253 | 4 | reached in round 1 |
| C | 2 | 17/18 | 11/11 | 60/60 | 2 | 26877 | 204 | 4 | reached in round 1 |
| C | 3 | 17/18 | 11/11 | 60/60 | 2 | 27289 | 229 | 4 | reached in round 1 |

Final C−B branch-point differences by matched repetition: [0, 0, 0]; range 0 to 0. This small pilot is descriptive; it does not establish statistical significance.

| Arm | Rep | First target round | Tokens at target/stop | Cycles | Executions | Wall seconds | Token ROI |
|---|---:|---|---:|---:|---:|---:|---:|
| A | 1 | 1 | 2576 | 36 | 1 | 8.840569 | 5.434783 |
| A | 2 | 1 | 2576 | 36 | 1 | 7.545242 | 5.434783 |
| A | 3 | 1 | 2576 | 36 | 1 | 7.047053 | 5.434783 |
| B | 1 | 1 | 8893 | 36 | 1 | 7.140321 | 1.574272 |
| B | 2 | 1 | 8893 | 36 | 1 | 7.633505 | 1.574272 |
| B | 3 | 1 | 8893 | 36 | 1 | 7.410992 | 1.574272 |
| C | 1 | 1 | 15774 | 31 | 1 | 6.99691 | 0.887536 |
| C | 2 | 1 | 15761 | 30 | 1 | 6.112661 | 0.888269 |
| C | 3 | 1 | 15761 | 30 | 1 | 5.946356 | 0.888269 |

At the preregistered target, paired C−B differences were API tokens [6881, 6868, 6868], executed cycles [-5, -6, -6], simulator executions [0, 0, 0], and wall seconds [-0.143411, -1.520844, -1.464636]. C's coverage did not exceed B's. Interpret wall-time differences descriptively because API latency varies across independent calls.

All rows use the original DUT, frozen specification and checker, one Verilator instrumented binary, and raw 18-point branch denominator. Line means Verilator block/elsif points; branch includes control and ternary outcomes; toggle is per-direction DUT bit transition. Expression counters are retained in JSON/CSV. Testbench counters are excluded.
Each round replays the same four-cycle reset/initial sequence followed by **all** accumulated generated actions. The measured cycles sum every replay. Each simulator process starts fresh; checker failures are collected while coverage is flushed. Common initialization and reset activity count in every round's coverage and cycles.

Token ROI = newly covered raw DUT branch points relative to the common initial run, per 1,000 API-reported input-plus-output tokens. Cached input and reasoning output details are informational subsets, not added again. Mock token ROI is undefined.

Egg normalization is limited to unsigned one-bit binary/two-state combinational winner predicates. Its six named Boolean rewrites are truth-table validated and saturated with finite limits. Distinct winner cases retain separate E-classes. Clock/reset transitions and all original coverage locations remain separate; an equivalent predicate never transfers a hit count. Yosys provides frontend/process extraction, while the RTL-to-expression bridge remains a hash-guarded, arbiter-specific source adapter.

The original DUT still violates the synchronous reset and one-hot override specification. Repeated checker failures count as two distinct categories at most. The checker was independently validated against derived conforming and single-defect controls. A fresh exhaustive ceiling is measured separately from model prompts and costs.

The arbiter has little cross-location semantic redundancy, so a C advantage is not guaranteed. A next discriminating experiment should use nested/repeated equivalent predicates with equivalence-checked RTL variants, then a FIFO with full/empty, simultaneous read/write, wraparound and reset-during-operation cases.

Exact metadata, per-call responses, rendered prompts, raw coverage files, source mappings and per-round CSV/JSONL are adjacent to this report.
