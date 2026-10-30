# Project status and repository map — 30 October 2026

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
| Evaluation | Arbiter/FIFO/timer historical pilots, queue B/C milestone, and controlled divider/FIFO stress A/B/P/C trials; Claude blind and read-only reviews | Too few independent natural IPs and near-saturated targets for a general effect estimate; free-form assertion generation and CVDP Pass@1 are not measured |

The [Milestone 1 report](milestone1_result_report.md) describes the queue B/C
trial. The latest [divider](divider_abcp_result_2026-10-30.md) and
[FIFO stress](sfifo_stress_abpc_result_2026-10-30.md) reports preserve the
four-arm trials and their limitations. The FIFO stress design is a disclosed,
equivalence-checked synthetic redundancy variant of ZipCPU `sfifo`, not a
naturally redundant held-out CVDP design. The current result is a null C-versus-B
comparison on those two controlled trials, not a refutation of E-graphs.

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
