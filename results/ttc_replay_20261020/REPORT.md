# CVDP `ttc_counter_lite_0007` matched A/B/C pilot

Mode: **replay**. Offline replay of saved calls.

Original NVIDIA CVDP hard-record RTL and specification are hash pinned. Seed: 25/266 DUT toggle directions; separate directed reference: 206/266. Preregistered target: 180/266. Reference actions are never included in prompts.

| Arm | Rep | Final toggle | Branch | Line | Expr | API tokens | Executed cycles | Calls | Target |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 1 | 229/266 | 14/14 | 23/23 | 9/9 | 16419 | 180 | 4 | reached |
| A | 2 | 198/266 | 14/14 | 23/23 | 9/9 | 16137 | 180 | 4 | reached |
| A | 3 | 226/266 | 14/14 | 23/23 | 9/9 | 16021 | 180 | 4 | reached |
| B | 1 | 234/266 | 14/14 | 23/23 | 9/9 | 48076 | 180 | 4 | reached |
| B | 2 | 234/266 | 14/14 | 23/23 | 9/9 | 47870 | 180 | 4 | reached |
| B | 3 | 234/266 | 14/14 | 23/23 | 9/9 | 47715 | 180 | 4 | reached |
| C | 1 | 234/266 | 14/14 | 23/23 | 9/9 | 50853 | 180 | 4 | reached |
| C | 2 | 234/266 | 14/14 | 23/23 | 9/9 | 51199 | 180 | 4 | reached |
| C | 3 | 234/266 | 14/14 | 23/23 | 9/9 | 52485 | 180 | 4 | reached |

Final paired C−B toggle-direction differences: [0, 0, 0]. These few independent sessions support descriptive comparison only.

| Arm | Rep | First target round | API tokens | Executed cycles | Simulator runs | Wall seconds |
|---|---:|---|---:|---:|---:|---:|
| A | 1 | 2 | 7372 | 58 | 2 | 0.024 |
| A | 2 | 2 | 7152 | 58 | 2 | 0.017 |
| A | 3 | 3 | 11331 | 111 | 3 | 0.024 |
| B | 1 | 1 | 25539 | 21 | 1 | 0.008 |
| B | 2 | 1 | 25667 | 21 | 1 | 0.008 |
| B | 3 | 1 | 25790 | 21 | 1 | 0.008 |
| C | 1 | 1 | 28018 | 21 | 1 | 0.198 |
| C | 2 | 1 | 28123 | 21 | 1 | 0.198 |
| C | 3 | 1 | 27977 | 21 | 1 | 0.198 |

Separate ceiling checker: {'checks': 159, 'distinct_defects': ['asynchronous_reset'], 'functional_errors': 2, 'interrupt_errors': 0, 'read_errors': 0, 'timing_errors': 2}. Its synchronous-reset timing failures are a DUT/specification discrepancy, reproduced in Verilator and Icarus; they do not invalidate coverage collection. Experimental repeated failure observations by category (final cumulative counts): {'cumulative_read_failure_events': 0, 'cumulative_interrupt_failure_events': 0, 'cumulative_timing_failure_events': 12}. Distinct categories are reported separately in rounds.csv.

A receives specification, RTL, shared seed, previous generated actions, checker errors, and logs. B adds every uncovered raw DUT point, exact counter outcome and source text. C has the same raw data plus hash-guarded, bounded egg equivalence for eight mapped Boolean guards. `irq_clear` and `read_status` share the typed address-status atom but are not merged. Most toggle points are not mapped by egg and remain in the unchanged denominator.

The timer checker samples registered reads and a specified active-high synchronous reset. The count/prescaler model uses pre-edge state, divide-by-(prescaler+1), one-cycle match/interrupt latency, and priority of match over status clear. The latter latency and priority details are less explicit in the natural-language spec and should be treated as contract assumptions; reset timing and register readback are direct requirements. The original RTL is preserved.

Every model round executes its whole generated history after the fixed five-cycle seed and fresh reset. Counters restart per simulator run. Executed cycles include replays; compilation, common-seed and reference ceiling times are separate metadata. Coverage is flushed on checker findings. No deterministic input search or solver witnesses enter A/B/C prompts. Model sessions are stateless and separate by arm/repetition.

Primary outcome is Verilator Coverage-3 toggle-direction counters (each bit-direction is one point). Branch, line and expr counts are reported using the same DUT-only filtered counter file. Token ROI = newly covered toggle directions versus seed per 1,000 API-reported input+output tokens; reasoning/cached tokens are subsets and not double-counted. A mock run has no token ROI. `not reached` is retained in target costs.

Egg handles two-state one-bit Boolean structure only; typed 4-bit address and 16-bit count comparisons remain atomic. It does not prove four-state, reset, sequential or arithmetic equivalence. Unsupported counters stay in raw feedback and denominator. Per-call/round logs, prompts, evidence, counter files, CSV and plots are next to this report.

The eight egg roots are local Boolean subguards. Full enclosing enable/prescaler and priority conditions are visible in the raw RTL but are not normalized in every mapped root. C therefore is not a complete branch-reachability model; the next frontend must carry full activation context with source provenance.
