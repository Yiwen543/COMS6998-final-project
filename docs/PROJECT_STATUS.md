# Project status and repository map — 4 November 2026

## Research contract

The proposal asks whether execution coverage and E-graph-normalized semantic
feedback improve an LLM's RTL verification coverage and Token ROI over text-only
and raw-coverage feedback. The controlled comparison is **C versus B**; A versus
B tests the value of coverage feedback. P is an added token-matched placebo for
prompt-length effects. Coverage always refers to original DUT source counters,
not the number of E-classes. The independent specification checker, RTL, JSON
driver, simulator options and denominator are fixed within each trial.

| Proposal stage | Current evidence | Remaining boundary |
| --- | --- | --- |
| Initial stimulus and structural parsing | CVDP arbiter starter; Yosys pre-`proc` typed guards; Rust `egg` with bounded saturation and Z3-checked two-state rewrites | Unsupported SystemVerilog expressions remain explicit; this is not a general RTL semantic model |
| Coverage-guided execution | Verilator DUT-only line, branch, expression and toggle counters; Icarus checker controls; fixed JSON cycle driver and independent replay | Tool-specific counter meanings and unreachable points remain in the raw denominator |
| E-graph refinement | Frozen A/B/P/C model feedback and saved prompts, API usage, cycles and simulator calls | No general C-over-B gain has been shown |
| Evaluation | Arbiter/FIFO/timer historical pilots, queue B/C milestone, controlled divider/FIFO stress A/B/P/C trials, and exploratory B-full/B-compact/P/C prompt ablation; Claude reviews of earlier frozen trials | Too few independent natural IPs and near-saturated targets for a general effect estimate; free-form assertion generation and CVDP Pass@1 are not measured |

The [Milestone 1 report](milestone1_result_report.md) describes the queue B/C
trial. The latest [divider](divider_abcp_result_2026-10-30.md) and
[FIFO stress](sfifo_stress_abpc_result_2026-10-30.md) reports preserve the
four-arm trials and their limitations. The FIFO stress design is a disclosed,
equivalence-checked synthetic redundancy variant of ZipCPU `sfifo`, not a
naturally redundant held-out CVDP design. The current result is a null C-versus-B
comparison on those two controlled trials, not a refutation of E-graphs.

The [3 November exploratory prompt ablation](sfifo_prompt_ablation_result_2026-11-03.md)
used the same synthetic FIFO with an expanded five-source-counter target.
All 12 sessions reached it in round 5. B-compact retained all raw evidence and
saved 7.0% of target-cost tokens; C-compact cost 21.4% more than B-compact
without improving target rounds. Here "C-compact" packs the **B base** but still
includes the full semantic appendix. The new minimal-C renderer shortens that
appendix; its [18 archived-prompt previews](../results/minimal_c_preview_20261103/preview.json)
are offline artifacts with zero model calls, not new model results.

The subsequent [minimal-C live ablation](minimal_c_result_2026-11-03.md) used
fresh interleaved B-compact/C-full/C-min/P-min sessions. All twelve reached
the target in round 5. C-min reduced C-full's token cost by 15.3%, but remained
2.95% above B-compact. All 72 calls and 84 replayed simulations were validated;
final toggle counts vary and are reported separately. Failure retention,
per-request counting and own-trajectory placebo matching are implemented in
the new runner. This supersedes the earlier offline-only status.

The [natural-IP screen](next_ip_screen_2026-11-03.md) rejected TX UART after
three B repetitions reached all five groups by round 2 and failed the
preregistered first-round gate. The codec was already saturated in round 1.
AXI VFIFO encoder and flattened linear-search groups remain provisional;
OpenTitan candidates require frontend/source-map work. No new pair of
independent natural IPs has passed every gate.

A [parameterized follow-up screen](ip_selection_diagnosis_2026-11-03.md)
found no nontrivial supported groups in the selected natural frame-FIFO
configuration. An isolated checksum-verified OSS CAD Suite now elaborates
the original OpenTitan SPI_HOST FSM. The subsequent
[SPI preflight](spi_host_preflight_2026-11-04.md) implements the Slang typed AST
adapter with 109 exact source-counter joins and 26 clock/reset connection checks.
Its fixed JSON driver and scoped specification checker pass 35 identical public
traces on Verilator and Icarus and detect three injected single faults. Seven
seed-zero groups were calibrated, but none required a rewrite in that first
adapter. The [semantic repair and live B follow-up](spi_semantic_repair_2026-11-04.md)
adds typed combinational SSA and independent Yosys-cell proofs (68 definitions),
then saturates Z3-certified design-specific rules in egg. It maps 186 of 199
targets and finds two qualified nontrivial groups among nine qualified source
groups. All three B repetitions hit all nine groups in round 1, so the original
development gate fails and no formal A/B/C/P trial follows. The live run has
18 successful generation calls, 21 simulations, 2,346 replay cycles and 388,818
API tokens; 94 repository tests and the saved-evidence recheck pass. General
hierarchical guards, exact sample timing and full formal checker validation
remain open. This is B-only screening evidence, not a C-effect estimate.

The [role-separated event milestone](spi_role_separated_events_2026-11-04.md)
adds a separately authored Claude checker with unchanged SV driver/RTL and
GPT-authored private calibration. Independent controls caught checker errors
that its own tests missed; only exact Claude patches were applied. The final
scoped checker passes independent positive controls and detects 10/12 retained
external mutation controls (two outside declared scope), with a fresh Claude review.
Three event families have clean calibrated examples; same-CS configuration
switching remains a reproduced spec/implementation discrepancy, not qualified
event evidence. The subsequent [I2C role-separated preflight](i2c_role_separated_preflight_2026-11-04.md)
certifies all nine different-expression pairs, binds their 18 source counters,
and maps 218/268 predicate targets. A Claude-authored scoped write-mode checker
and fixed GPT/Codex bus driver validate three multistep events on both simulators.
However, all 18 reachable equivalent source groups already execute in an ordinary
one-byte write; zero late-specific groups qualify. No I2C B or C run was started. Formal A/B/C readiness stays false: temporal-event/source
bindings and independent-IP qualification remain unresolved. See
`examples/heldout_spi_host_events/freeze.json` and
`results/spi_host_event_checker_20261104/accounting.json` for the exact boundary
and development costs; those costs are separate from stimulus-model pilots.

The [READB/read-ACK extension](i2c_read_preflight_2026-11-04.md) adds a separate
read-capable driver and Claude-authored scoped checker. Independent controls
caught and repaired same-row push/flush ordering, with the failed version
retained. Nine calibration traces agree between simulators; multi-byte reads,
RCONT chaining and read/restart are witnessed. All 25 reached equivalent groups
(three nontrivial) already execute in ordinary read/write controls: zero new
multistep-specific groups qualify. B/C remain unrun, budgets unchanged. The
checker rejects nine protocol mutations, but one extra-STOP verdict remains
misclassified as invalid; no full fault-attribution or formal guarantee follows.
Twenty I2C-focused checks and the frozen smoke replay pass. AXI DMA legacy
`always @*` extraction and an exact-source flash-controller dependency probe
provide two separate follow-up families, not two qualified benchmarks.

Open-source formal work is underway: the [candidate preflight](midterm_candidate_preflight_2026-10-30.md)
records SymbiYosys BMC/cover/prove tasks on selected fixed candidates, and the
FIFO stress report records fixed-configuration Yosys equivalence. These claims
are scoped to their saved assumptions and configurations; neither coverage nor
finite-depth BMC is a complete correctness proof.

## Canonical locations

| Directory | Keep | Regenerate or discard |
| --- | --- | --- |
| `examples/` | Pinned RTL, specifications, fixed drivers/checkers and provenance | Local compiled simulation products |
| `scripts/`, `egraph/src/`, `egraph/Cargo.lock`, `configs/`, `tests/` | Pipeline, rewrite engine, frozen settings, automated checks | Python bytecode and Cargo `target/` |
| `docs/`, `output/pdf/` | Proposal mapping, dated reports, freeze manifests and submitted milestone PDF | Temporary PDF render files |
| `results/` | Historical live evidence, raw DUT counters, accepted actions, rendered prompts, summaries, plots, replay validations and Claude audit dispositions | `verilator-build/`, `plot-cache/`, `mplconfig/`, `cache/` |
| `build/`, `.cache/`, `.venv/` | Local working environment only; all Git-ignored | Disposable compilation and download output; never commit credentials |
| `project_background_reading/`, `third_party/` | Original readings and pinned external source checkout | Finder metadata |

Older mock and development results remain where reports cite them. They are
labelled as mock/development and never pooled with formal live results. The
clean-up removes disposable compiler objects and caches without altering saved
prompts, call envelopes, original coverage data or frozen experiment settings.

## Next experiment

Keep the two tracks separate: use the known FIFO for the exploratory
minimal-C packaging diagnostic, and qualify new natural IPs for generalization.
The [project review](project_review_2026-11-03.md) records the proposed arms,
remaining runner checks, candidate shortlist, and limits of the current
Boolean-skeleton Z3 proofs. A shorter appendix alone is not evidence of better
coverage or an extraction-algorithm bottleneck.

Screen at least two **natural**, independent FIFO/controller IPs for multiple
seed-uncovered, source-distinct, complete activation guards that are genuinely
equivalent after typed normalization. Establish independent specification
checkers, legal-input assumptions, formal or calibrated reachability and an
outcome-blind target. Reject only immediate B saturation in a separate
development gate. Freeze source/checker/driver/denominator and budgets before
the A/B/P/C trial. Preserve failures and unreachable raw points, and include a
read-only independent audit. A larger or multi-module IP alone is not a
selection criterion.

## Local verification

From the repository root, `make doctor`, `make test`, and `make step1` exercise
the starter without API keys. `make test` builds the pinned Rust engine offline
and runs the expanded Python suite. The dated result
reports contain exact replay commands for the controlled pilots. New live calls
require separately staged credentials and a new output directory.
