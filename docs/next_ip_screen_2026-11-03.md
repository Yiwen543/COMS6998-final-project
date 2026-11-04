# Next IP screen and extraction-bottleneck audit — 3 November 2026

This is **candidate selection and an independent B development run**, not a new
A/B/P/C result. The previously frozen divider and FIFO comparisons remain the
only held-out comparisons. No C outcome was inspected to select these designs.

## Reproducible candidate disposition

| Independent IP and public specification | Static semantic evidence | Independent reachability / B gate | Decision |
|---|---|---|---|
| CVDP `cvdp_agentic_64b66b_codec_0007`, supplied spec and exact pinned RTL in `docs/midterm-candidate-lock.json` | Eight source-mapped, seed-zero, calibrated groups under the earlier frontend | Existing independent B short trial hit all eight in round 1 (`results/midterm_b_development_short_live_20261030/semantic-group-progress.json`) | Reject for this comparison: immediate saturation |
| ZipCPU `txuart.v` at `f43a6b83c3a70fb2ac0696a45c5545b233fb860b`, upstream `doc/spec.pdf` | Five non-reset groups with two or more distinct original DUT source counters each, egg/Z3 checked; all seed-zero, all reached by separate legal calibration | Three independent live B repetitions: each had only one group unhit after round 1 and all groups hit by round 2 | Reject under preregistered B gate; also all five groups are AST-identical before egg |
| Alex Forencich `axi_vfifo_enc.v` at `516bd5dadc3365b7f9e225d2af8fe0b8d804fe53` | Six source-distinct groups under current parser, only one merges different input ASTs; that group lands on assignment/end lines 621/631, and 76 cases remain unsupported | No independent module-specific specification/checker or unambiguous raw-counter/reachability gate yet | Provisional only, **not** eligible for model trial |

A separate multi-file, flattened extraction of CVDP's previously screened
linear-search controller/datapath finds four provisional source groups and 19
whole-wire alias links, versus its earlier one qualifying same-module group.
All four have identical input ASTs within each group. Some source anchors are
`else` lines shared with deeper branches, so they need an unambiguous raw
counter and complete-guard audit before they can become targets. The evidence
is in `results/next_natural_ip_screen/cvdp_linear_search_flatten/semantic.json`.

ZipCPU's TX and RX UART and FIFO are modules from one upstream project, so we
did not count them as three independent IPs. The current frontend finds only
two groups in RX UART and two in its FIFO, mostly reset or broad control paths.
OpenTitan's documented `prim_fifo_sync`/`prim_packer_fifo` remain independent
public candidates, but direct Yosys Verilog parsing cannot resolve their
SystemVerilog packages. Translating through `sv2v` without a verified original
source map would break the raw-location requirement. Neither was promoted.

## TX UART preflight

The original upstream RTL and spec are retained in the ignored checkout,
with hashes in `examples/heldout_txuart/provenance.json`. The fixed 8N1,
two-clock-per-baud contract is documented in `examples/heldout_txuart/docs/contract.md`.
The JSON interface accepts `reset`, `break`, `wr` (one bit each), and `data`
(unsigned byte). The public-pin checker decodes start/data/stop bits and
compares each accepted byte without reading DUT internal state. It accepts the
original on a 140-cycle independent calibration in both Verilator and Icarus;
an isolated data-bit inversion mutant is rejected on two bytes. Calibration
vectors are absent from every B prompt.

The initial four-cycle seed covers 8/24 DUT branch, 26/53 DUT line, 14/42 DUT
expression, and 38/384 DUT toggle points. Calibration covers 21/24, 45/53,
34/42, and 126/384 respectively. The five qualified source-line groups are
202/399 (break), 209/409 (BREAK state), 213/413 (IDLE state), 215/417
(accepted write), and 274/289/333 (ready/busy). The full source-counter
records, including zero and positive hit counts, are in
`results/next_natural_ip_screen/txuart/screen.json`. Each source counter remains
separate in the raw denominator and the B target accounting.

The frontend now records equal-width whole-wire aliases, including flattened
hierarchical port aliases across multiple RTL source files, and proves
disjoint exact case-arm priority with
Z3. It retains signedness/width/type in atom identities, complete supported
activation paths, process clock/reset event context, and original source
coordinates. Binary/two-state semantics are the only claimed equivalence.
Unsupported cases, partial aliases, and ambiguous source mappings are saved
rather than treated as proved. TX has 23 unsupported cases and 10 unresolved
partial connections; the AXI encoder has 76 and 12. The six Rust egg rules are
independently Z3 checked, saturation is bounded, and every merged candidate
pair receives a separate Z3 equivalence check. The original Verilator source
counters are joined only when a unique true-path point exists.

## Preregistered B result

`configs/txuart_b_development.json` was written before live model calls. The
acceptance rule required at least three qualifying groups; in at least two of
three independent B repetitions, at least two groups had to remain unhit after
round 1, with later group progress in at least two repetitions. Each session
had six rounds, at most 16 new cycles per round, and a fixed 24-idle-cycle
post-round drain. Every round replays the seed and all prior actions and drains.
The exact prompt, action schema, model settings, calls, cycles, retries, raw
coverage, and source-group hits are saved in
`results/next_natural_ip_screen/txuart/b_dev_live_20261103/`.

All 18 calls returned the requested `gpt-6.1-sol`, passed JSON validation,
and were simulated. Across repetitions 1/2/3, the number of unhit groups after
round 1 was **1/1/1** and after round 2 **0/0/0**. B reached 14/24 branch and
37/53 line after round 1, 20/24 branch and 45/53 line after round 2, and
21/24 branch and 45/53 line after round 6. The checker reported no defects.
The 18 calls consumed 343,568 API-reported input tokens and 7,109 output
tokens in total; 21 simulator executions replayed 2,604 total cycles across
the three repetitions. Compilation took 9.37 s summed over the three
independent builds and simulation 0.74 s summed over all executions. These
are separate from any count-only endpoint. The 18 API calls took 144.63 s in
reported model latency. Cached input tokens (59,726) and reasoning output
tokens (2,213) are subsets of the API totals above, not extra tokens. The
preregistered gate **failed**. The hidden key was deleted after the run.

## What is actually limiting this experiment?

The TX UART group inputs are already identical strings before equality
saturation: zero of the five qualified groups need an egg rewrite to merge.
Thus a C prompt would mostly restate relationships visible to B in the RTL
and raw uncovered locations. A positive C-over-B result on this DUT would not
isolate egg normalization, and the observed rapid B saturation leaves little
room for an improvement. The AXI encoder has one nontrivial AST merge, but its
source mapping and specification gate are unresolved. These are **measured
extraction/task bottlenecks**, not evidence that egg cannot help in general.

The new Rust timing fields separate bounded saturation from representative/
JSON extraction. On TX the in-process saturation took about 0.201 s,
representative/JSON construction under 0.001 s; Yosys/frontend extraction
took about 0.044 s, rewrite proofs about 0.063 s, and pair checks about
0.100 s in one local scan. Wall time and debug builds vary. In contrast,
the B requests averaged about 19,087 input tokens each, because full RTL and
raw uncovered source points were repeated. C prompt length must be diagnosed
against API-counted tokens and a token-matched placebo, not inferred from
serialized byte length or the 0.2-second local egg step.

## Next go/no-go procedure

1. Before another model call, demand at least two **independent** qualified
   source-pair groups per new candidate whose *input* expressions differ and
   merge only after egg rewrites. Keep the three-event/three-group preference.
   Record source mapping and unsupported paths. Do not turn expression
   equality into shared source coverage.
2. For each remaining public SPEC+RTL candidate, create an independently
   reviewed checker and fixed JSON driver. Prove or calibrate reachable target
   counters within the exact cycle budget, including stateful events. Keep
   calibration and solver witnesses out of prompts.
3. Run the same prospective B gate on two to three independent sessions.
   Reject immediate saturation and no-progress candidates. Preserve every
   rejection. Only then freeze targets and run A/B/C plus API-token-matched
   placebo under identical resource limits.
4. Diagnose C with an ablation: B; B plus original C serialization without
   group relations; B plus proven group relations with minimal wording; full
   C. Record API-counted prompt tokens, saturation/profile time, model latency,
   target hit rounds, cycles, executions, and raw DUT counters. This separates
   missed extraction, prompt load, and task ceiling. Such ablations are
   exploratory and must be labeled separately from the primary C-versus-B
   comparison.

The requested formal A/B/P/C run was **not** started because no newly screened
pair of independent IPs passed the predeclared development gate. Selecting
targets after seeing these B outcomes would contaminate that comparison.

## Reproduce the new screen

From the repository root, fetch the ignored external checkouts at the pinned
commits if they are absent:

```sh
git clone https://github.com/ZipCPU/wbuart32.git third_party/wbuart32_candidate
git -C third_party/wbuart32_candidate checkout f43a6b83c3a70fb2ac0696a45c5545b233fb860b
git clone https://github.com/alexforencich/verilog-axi.git third_party/verilog_axi_candidate
git -C third_party/verilog_axi_candidate checkout 516bd5dadc3365b7f9e225d2af8fe0b8d804fe53
cargo build --manifest-path egraph/Cargo.toml
.venv/bin/python -m unittest tests.test_typed_predicates tests.test_semantic_candidate_scan tests.test_txuart_b_development tests.test_txuart_fixture
.venv/bin/python scripts/screen_txuart_next.py
.venv/bin/python scripts/run_txuart_b_development.py --mode mock --output build/txuart-b-mock-new
```

The live result is already archived; reproducing it requires a separately
staged OpenAI key and a **new** output directory. The run command is
`.venv/bin/python -B scripts/run_txuart_b_development.py --mode live --output results/next_natural_ip_screen/txuart/b_dev_live_NEW`.
