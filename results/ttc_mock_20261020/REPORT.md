# CVDP `ttc_counter_lite_0007` matched A/B/C pilot

Mode: **mock**. Mock smoke test; no LLM performance inference.

Original NVIDIA CVDP hard-record RTL and specification are hash pinned. Seed: 25/266 DUT toggle directions; separate directed reference: 206/266. Preregistered target: 180/266. Reference actions are never included in prompts.

| Arm | Rep | Final toggle | Branch | Line | Expr | API tokens | Executed cycles | Calls | Target |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 1 | 107/266 | 13/14 | 17/23 | 8/9 | n/a | 180 | 4 | not reached |
| A | 2 | 140/266 | 13/14 | 19/23 | 8/9 | n/a | 180 | 4 | not reached |
| A | 3 | 102/266 | 12/14 | 22/23 | 8/9 | n/a | 180 | 4 | not reached |
| B | 1 | 107/266 | 13/14 | 17/23 | 8/9 | n/a | 180 | 4 | not reached |
| B | 2 | 140/266 | 13/14 | 19/23 | 8/9 | n/a | 180 | 4 | not reached |
| B | 3 | 102/266 | 12/14 | 22/23 | 8/9 | n/a | 180 | 4 | not reached |
| C | 1 | 107/266 | 13/14 | 17/23 | 8/9 | n/a | 180 | 4 | not reached |
| C | 2 | 140/266 | 13/14 | 19/23 | 8/9 | n/a | 180 | 4 | not reached |
| C | 3 | 102/266 | 12/14 | 22/23 | 8/9 | n/a | 180 | 4 | not reached |

Final paired C−B toggle-direction differences: [0, 0, 0]. Arm-blind mock actions make these infrastructure-only.

| Arm | Rep | First target round | API tokens | Executed cycles | Simulator runs | Wall seconds |
|---|---:|---|---:|---:|---:|---:|
| A | 1 | not reached | n/a | 180 | 4 | 0.032 |
| A | 2 | not reached | n/a | 180 | 4 | 0.030 |
| A | 3 | not reached | n/a | 180 | 4 | 0.030 |
| B | 1 | not reached | n/a | 180 | 4 | 0.033 |
| B | 2 | not reached | n/a | 180 | 4 | 0.033 |
| B | 3 | not reached | n/a | 180 | 4 | 0.042 |
| C | 1 | not reached | n/a | 180 | 4 | 0.180 |
| C | 2 | not reached | n/a | 180 | 4 | 0.179 |
| C | 3 | not reached | n/a | 180 | 4 | 0.179 |

Separate ceiling checker: {'checks': 159, 'distinct_defects': ['asynchronous_reset'], 'functional_errors': 2, 'interrupt_errors': 0, 'read_errors': 0, 'timing_errors': 2}. Its synchronous-reset timing failures are a DUT/specification discrepancy, reproduced in Verilator and Icarus; they do not invalidate coverage collection. Experimental repeated failure observations by category (final cumulative counts): {'cumulative_read_failure_events': 0, 'cumulative_interrupt_failure_events': 0, 'cumulative_timing_failure_events': 15}. Distinct categories are reported separately in rounds.csv.

A receives specification, RTL, shared seed, previous generated actions, checker errors, and logs. B adds every uncovered raw DUT point, exact counter outcome and source text. C has the same raw data plus hash-guarded, bounded egg equivalence for eight mapped Boolean guards. `irq_clear` and `read_status` share the typed address-status atom but are not merged. Most toggle points are not mapped by egg and remain in the unchanged denominator.

The timer checker samples registered reads and a specified active-high synchronous reset. The count/prescaler model uses pre-edge state, divide-by-(prescaler+1), one-cycle match/interrupt latency, and priority of match over status clear. The latter latency and priority details are less explicit in the natural-language spec and should be treated as contract assumptions; reset timing and register readback are direct requirements. The original RTL is preserved.

Every model round executes its whole generated history after the fixed five-cycle seed and fresh reset. Counters restart per simulator run. Executed cycles include replays; compilation, common-seed and reference ceiling times are separate metadata. Coverage is flushed on checker findings. No deterministic input search or solver witnesses enter A/B/C prompts. Model sessions are stateless and separate by arm/repetition.

Primary outcome is Verilator Coverage-3 toggle-direction counters (each bit-direction is one point). Branch, line and expr counts are reported using the same DUT-only filtered counter file. Token ROI = newly covered toggle directions versus seed per 1,000 API-reported input+output tokens; reasoning/cached tokens are subsets and not double-counted. A mock run has no token ROI. `not reached` is retained in target costs.

Egg handles two-state one-bit Boolean structure only; typed 4-bit address and 16-bit count comparisons remain atomic. It does not prove four-state, reset, sequential or arithmetic equivalence. Unsupported counters stay in raw feedback and denominator. Per-call/round logs, prompts, evidence, counter files, CSV and plots are next to this report.

The eight egg roots are local Boolean subguards. Full enclosing enable/prescaler and priority conditions are visible in the raw RTL but are not normalized in every mapped root. C therefore is not a complete branch-reachability model; the next frontend must carry full activation context with source provenance.
