# CVDP context FIFO A/B/C pilot

Mode: **live**. Live Responses API model actions.

This is `sync_fifo.sv` from CVDP `cvdp_agentic_low_power_channel_0001`. CVDP provided the RTL as a low-power-channel context file, not a standalone FIFO spec. The independent FIFO contract is authored in `examples/fifo/docs/specification.md`; DEPTH=8, DATA_W=8, and overflow/underflow are excluded.

Primary outcome: Verilator DUT toggle-direction counters. The common four-cycle seed already covers all four branch counters. This FIFO cannot discriminate arms by branch coverage; expression, line, toggles and nine checker functional bins remain reported.

Preregistered toggle target: **200/220**; separate directed plus seeded-random reference run: **220/220** over 306 cycles. Reference actions are never in model prompts.

| Arm | Rep | Final toggle | Line | Expr | Branch | Bins | API tokens | Cycles | Calls | Target |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 1 | 219/220 | 7/7 | 3/3 | 4/4 | 9/9 | 13002 | 336 | 4 | reached round 2 |
| A | 2 | 219/220 | 7/7 | 3/3 | 4/4 | 9/9 | 12986 | 336 | 4 | reached round 2 |
| A | 3 | 220/220 | 7/7 | 3/3 | 4/4 | 9/9 | 12884 | 336 | 4 | reached round 2 |
| B | 1 | 220/220 | 7/7 | 3/3 | 4/4 | 9/9 | 28875 | 336 | 4 | reached round 1 |
| B | 2 | 220/220 | 7/7 | 3/3 | 4/4 | 9/9 | 28933 | 336 | 4 | reached round 1 |
| B | 3 | 220/220 | 7/7 | 3/3 | 4/4 | 9/9 | 28900 | 336 | 4 | reached round 1 |
| C | 1 | 220/220 | 7/7 | 3/3 | 4/4 | 9/9 | 29711 | 336 | 4 | reached round 1 |
| C | 2 | 220/220 | 7/7 | 3/3 | 4/4 | 9/9 | 33704 | 336 | 5 | reached round 1 |
| C | 3 | 220/220 | 7/7 | 3/3 | 4/4 | 9/9 | 29729 | 336 | 4 | reached round 1 |

Final paired C−B toggle-direction differences: [0, 0, 0]. This small pilot is descriptive, not a significance test.

First-round functional-bin counts by repetition: A [9, 9, 9], B [9, 8, 8], C [8, 8, 8] (of nine). Toggle saturation does not imply that every behavioral bin was hit in that round.

| Arm | Rep | First 200/220 round | Tokens at target | Executed cycles | Simulator runs | Wall seconds |
|---|---:|---|---:|---:|---:|---:|
| A | 1 | 2 | 5056 | 104 | 2 | 26.919 |
| A | 2 | 2 | 4941 | 104 | 2 | 22.765 |
| A | 3 | 2 | 4956 | 104 | 2 | 24.454 |
| B | 1 | 1 | 17926 | 36 | 1 | 13.202 |
| B | 2 | 1 | 18056 | 36 | 1 | 16.871 |
| B | 3 | 1 | 18049 | 36 | 1 | 17.847 |
| C | 1 | 1 | 18533 | 36 | 1 | 12.995 |
| C | 2 | 1 | 18522 | 36 | 1 | 12.383 |
| C | 3 | 1 | 18493 | 36 | 1 | 12.077 |

At 200/220, paired C−B differences were API tokens [607, 466, 444], executed cycles [0, 0, 0], and simulator runs [0, 0, 0]. C did not improve coverage or measured API-token and simulator cost over B. Wall-time differences are descriptive because independent API calls vary in latency; C's egg preprocessing share is included.

Relative to A, B reached 200/220 with fewer executed cycles and simulator runs in every repetition, but used more API input+output tokens. Thus raw coverage changes the resource tradeoff rather than dominating text-only on every cost axis.

Across live repetitions: 1 model retries, 1 rejected model responses, and 0 checker failure observations. Rejected calls and their API tokens remain in the call log and cost totals.

A receives specification, RTL, common stimulus, occupancy, checker failures and execution logs. B adds every uncovered raw DUT counter with source location and outcome. C receives the same raw evidence plus bounded egg-derived equivalent forms for five hash-guarded predicates, with unmapped counters disclosed. No solver or deterministic search supplies model stimulus.

Every round runs the complete generated history after a fresh four-cycle reset/initialization. Executed cycle and simulator counts include every replay; compilation, common-initial and separate ceiling costs are in metadata. Coverage is flushed even on checker failures. Repeated failed observations are counts, while defect categories are deduplicated.

Token ROI = new DUT toggle-direction counters versus the shared seed per 1,000 API-reported input+output tokens. Reasoning and cached-token fields are subsets and are not added twice. Mock token ROI is undefined.

Egg uses two-state unsigned one-bit Boolean predicates. Multi-bit pointer comparisons are atomic guarded inputs; memory, clock, reset and state transition semantics are outside combinational normalization. All original Verilator coverage counters remain separate. The five mapped predicates are only a subset; unsupported/unmapped points are explicitly listed in C feedback and retained in the raw denominator.

At the shared seed, only two mapped egg predicates (simultaneous push/pop and the full-pointer conjunction) are uncovered; 186 other uncovered locations have no sound mapping and remain in the raw denominator. This FIFO has little repeated predicate redundancy, so C has no observed advantage over B here. A more discriminating next study should use nested/repeated equivalent predicates in equivalence-checked RTL variants, then a larger FIFO controller with full/empty, simultaneous operations, wraparound and reset transitions.

Per-call JSONL, per-round JSONL/CSV, rendered prompts, raw counter files, exact metadata, and comparison plot are adjacent to this report.
