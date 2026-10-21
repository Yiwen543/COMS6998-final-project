# CVDP context FIFO A/B/C pilot

Mode: **mock**. Offline mock smoke test; not LLM performance evidence.

This is `sync_fifo.sv` from CVDP `cvdp_agentic_low_power_channel_0001`. CVDP provided the RTL as a low-power-channel context file, not a standalone FIFO spec. The independent FIFO contract is authored in `examples/fifo/docs/specification.md`; DEPTH=8, DATA_W=8, and overflow/underflow are excluded.

Primary outcome: Verilator DUT toggle-direction counters. The common four-cycle seed already covers all four branch counters. This FIFO cannot discriminate arms by branch coverage; expression, line, toggles and nine checker functional bins remain reported.

Preregistered toggle target: **200/220**; separate directed ceiling: **220/220**. The ceiling is never in model prompts.

| Arm | Rep | Final toggle | Line | Expr | Branch | Bins | API tokens | Cycles | Calls | Target |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 1 | 214/220 | 7/7 | 2/3 | 4/4 | 7/9 | n/a | 336 | 4 | reached round 3 |
| A | 2 | 214/220 | 7/7 | 3/3 | 4/4 | 8/9 | n/a | 336 | 4 | reached round 3 |
| A | 3 | 211/220 | 7/7 | 2/3 | 4/4 | 7/9 | n/a | 336 | 4 | reached round 3 |
| B | 1 | 214/220 | 7/7 | 2/3 | 4/4 | 7/9 | n/a | 336 | 4 | reached round 3 |
| B | 2 | 214/220 | 7/7 | 3/3 | 4/4 | 8/9 | n/a | 336 | 4 | reached round 3 |
| B | 3 | 211/220 | 7/7 | 2/3 | 4/4 | 7/9 | n/a | 336 | 4 | reached round 3 |
| C | 1 | 214/220 | 7/7 | 2/3 | 4/4 | 7/9 | n/a | 336 | 4 | reached round 3 |
| C | 2 | 214/220 | 7/7 | 3/3 | 4/4 | 8/9 | n/a | 336 | 4 | reached round 3 |
| C | 3 | 211/220 | 7/7 | 2/3 | 4/4 | 7/9 | n/a | 336 | 4 | reached round 3 |

Final paired C−B toggle-direction differences: [0, 0, 0]. Mock stimuli are arm-blind and cannot support an LLM benefit claim.

A receives specification, RTL, common stimulus, occupancy, checker failures and execution logs. B adds every uncovered raw DUT counter with source location and outcome. C receives the same raw evidence plus bounded egg-derived equivalent forms for five hash-guarded predicates, with unmapped counters disclosed. No solver or deterministic search supplies model stimulus.

Every round runs the complete generated history after a fresh four-cycle reset/initialization. Executed cycle and simulator counts include every replay; compilation, common-initial and separate ceiling costs are in metadata. Coverage is flushed even on checker failures. Repeated failed observations are counts, while defect categories are deduplicated.

Token ROI = new DUT toggle-direction counters versus the shared seed per 1,000 API-reported input+output tokens. Reasoning and cached-token fields are subsets and are not added twice. Mock token ROI is undefined.

Egg uses two-state unsigned one-bit Boolean predicates. Multi-bit pointer comparisons are atomic guarded inputs; memory, clock, reset and state transition semantics are outside combinational normalization. All original Verilator coverage counters remain separate. The five mapped predicates are only a subset; unsupported/unmapped points are explicitly listed in C feedback and retained in the raw denominator.

The FIFO has little repeated predicate redundancy, so C may have no advantage over B. A more discriminating next study should use nested/repeated equivalent predicates in equivalence-checked RTL variants, then a larger FIFO controller with full/empty, simultaneous operations, wraparound and reset transitions.

Per-call JSONL, per-round JSONL/CSV, rendered prompts, raw counter files, exact metadata, and comparison plot are adjacent to this report.
