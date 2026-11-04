# Project review and minimal C experiment — 3 November 2026

> Follow-up completed later on 3 November: the [live minimal-C result](minimal_c_result_2026-11-03.md)
> and [new candidate diagnosis](ip_selection_diagnosis_2026-11-03.md) supersede
> the prospective/offline-only status in this review. The original review and
> its preregistered intent remain below for chronology.

The project has a working, replayable model-in-the-loop coverage experiment.
It has not established a repeatable C-over-B advantage. The next useful work
is to distinguish task opportunity from feedback packaging: keep B-compact,
test a relation-only minimal C on the existing FIFO as an exploratory
diagnostic, and independently qualify new natural controller/frame-FIFO IPs.
Making B less informative or choosing tasks using C outcomes would not answer
the proposal's research question.

## Progress against the proposal

| Stage | Implemented evidence | Scope still missing |
|---|---|---|
| Specification and stimulus | Pinned DUTs/specs, fixed JSON drivers, specification-based public-I/O checkers, positive/negative checker controls | Experimental models generate cycle actions, not arbitrary SV testbenches, assertions or checkers; do not report CVDP Pass@1 |
| Tool execution | Verilator DUT-only raw counters, Icarus controls, saved actions/prompts/usage, per-round accounting and independent replay | Counter semantics are tool/version dependent; high coverage does not prove correctness |
| Semantic feedback | Yosys pre-`proc` frontend; typed atom identity, complete supported activation guards, event context; bounded Rust egg; Z3 rewrite/pair checks | Restricted Boolean normalization, not general four-state or sequential RTL equivalence |
| Model comparison | A/B/P/C pilots plus latest B-full/B-compact/P-compact/C-compact ablation | Few IP families; latest FIFO is a disclosed synthetic redundancy variant; independent natural-IP generalization remains open |
| Formal and independent evaluation | Selected SBY property/cover tasks, fixed-configuration Yosys variant equivalence, earlier Claude blind and revealed audits | A complete agent-verdict benchmark, formal defect controls across designs, and R0/R1/R2 recovery experiment remain future work |

The original arbiter still preserves the upstream multi-bit-override and
reset-timing defects. Its deterministic targeted run and exhaustive ceiling
establish plumbing and checker discrimination, not model superiority. The
queue milestone found earlier C target crossings in two of six index-paired
comparisons and four ties, but all selected equivalent guards were already
covered after round 1; that observation cannot identify a semantic-group
mechanism. Divider and FIFO stress trials subsequently tied B and C at their
targets. See [milestone](milestone1_result_report.md),
[divider](divider_abcp_result_2026-10-30.md), and
[FIFO stress](sfifo_stress_abpc_result_2026-10-30.md).

## Latest measured result

The [exploratory FIFO run](sfifo_prompt_ablation_result_2026-11-03.md) has
72 accepted live generation calls, three repetitions per arm, six rounds and
eight new cycles per round. All five preregistered source counters were hit in
round 5 in every session, using 144 cumulative replayed cycles and six simulator
executions at target. Saved independent replay matches all 84 executions,
including seed runs, at every original counter and checker result.

| Arm | Target round in each repetition | Mean input + output tokens to target |
|---|---|---:|
| B-full | 5 / 5 / 5 | 36,841 |
| B-compact | 5 / 5 / 5 | 34,280 |
| P-compact | 5 / 5 / 5 | 41,799 |
| C-compact | 5 / 5 / 5 | 41,633 |

B-compact saves 7.0% while preserving every raw feedback row. C costs 21.4%
more than B-compact without a target-round, coverage or simulator-work benefit.
All arms largely follow the same fill-then-drain schedule. Separate calibration
reaches the target in 36 total cycles (seed plus four batches), so there is
only one observed round of headroom. This supports investigating scheduling
and task opportunity; it does not establish a causal explanation of the tie.
The old P matches the full C payload by actual provider token counts, but does
not show what a shorter C would do.

## Script audit and limits

| Component | Files | Finding and action |
|---|---|---|
| Coverage and driver | `coverage.py`, fixed candidate runners/checkers | Preserve original locations/counters and the reset/replay policy. Keep independent replay as the measurement check; Claude prose is not the counter oracle. |
| Frontend | `typed_predicates.py`, `semantic_candidate_scan.py` | Multi-file whole-wire aliases and exact binary case priority now work. Partial aliases, unsupported expressions and ambiguous mappings remain explicit. Add one parameter manifest shared by extraction, simulation and formal tasks before parameterized candidates. |
| Old broad screens | `screen_cvdp_extended.py`, `screen_cvdp_nonagentic.py` | Per-module/default-parameter/exact-repeat screens are narrower than the new frontend. Their negative records are not proof that those IPs lack useful semantic groups. |
| Source mapping | `semantic_candidate_scan.map_true_counter` | Unique line/type/outcome matching is not a general proof of guard-to-counter correspondence. Audit columns, branch polarity, nested/default cases and hierarchy for each promoted site; ambiguous sites stay unresolved. |
| Rewrites/proof | `egraph/src/main.rs`, `preflight_heldout.py` | Real bounded egg uses six Boolean rules and AstSize extraction. Most pair proofs treat typed atoms as independent Booleans. Separate bounded-width eq/ne and case-priority proofs do not establish arbitrary arithmetic RTL-to-IR equivalence. |
| Prompt construction | `sfifo_prompt_ablation_feedback.py` | B packing round-trips the raw rows. Current C still sends typed atoms, representatives, E-nodes and unsupported/mapping diagnostics even after useful groups disappear. This is a packaging opportunity, not yet an observed model benefit. |
| Experiment/accounting | `run_sfifo_prompt_ablation.py`, `analyze_sfifo_prompt_ablation.py` | Fixed arm order confounds wall-clock comparisons. Analyzer requires complete round sets, while exhausted retries can truncate a session. Before a new runner, retain incomplete sessions and all failure costs; use predeclared blocked/interleaved arm order. Current 72-call run had no retries or missing rows. |

The local TX UART profile measured about 0.201 s for egg saturation and under
0.001 s for representative/JSON extraction, versus about 19,087 API input
tokens per B request. It does not justify replacing AstSize with a complex
exact extractor yet. Measure frontend time, saturation, extraction, serialized
semantic tokens, model latency and missed supported groups separately. A
parser failing to expose useful guards is a different bottleneck from a large
E-graph having expensive representative selection.

## Minimal C prepared offline

[`minimal_c_feedback.py`](../scripts/minimal_c_feedback.py) consumes existing
proved C evidence. It keeps the B-compact payload and system instructions
unchanged and replaces only `egg_normalization` with:

- The two-state, context-scoped equivalence claim and no-transfer-of-hits rule.
- Original source, line, column, counter type/polarity and measured hit count.
- Groups of equivalent complete activation guards, with event context.

It adds no stimulus hints, target-event labels, solver witnesses or calibration.
The first prompt retains groups `{91,161}` and `{96,129,179}`: five distinct
branch/`if` counters. All five remain in the evaluation target and raw
denominator. The appendix follows the existing uncovered-group selection policy:
five sites initially, two once near-full is covered, zero when both groups are
covered. Keeping all five in later prompts would be another intervention.

Proof details, typed atoms, full guard expressions and source-mapping evidence
remain in the original saved semantic artifacts. Minimal C is a **relation-only
distillation**, not a lossless encoding of the complete C appendix. Full RTL
and the losslessly packed B evidence remain available to the model. The claim
is restricted to those listed sites; no completeness claim is made about omitted
or unsupported predicates.

The [preview manifest](../results/minimal_c_preview_20261103/preview.json)
records 18 archived prompts and their hashes. First-round appendix size changes
from **4,477 to 687 bytes** (84.7% reduction); combined message content changes
from **22,518 to 18,728 bytes** (16.8%). These are bytes, not API token counts.
There were **zero new model calls**. Old C actions are not minimal-C outputs
and cannot provide minimal-C coverage results. The historical frozen runner
and results were not edited to create this preview.

From the repository root:

```sh
.venv/bin/python -m unittest tests.test_minimal_c_feedback -q
```

Repository cleanup on 4 November removed the one-off preview generator and its
18 regenerated prompt copies after the live minimal-C experiment superseded
them. The preview manifest, original source prompts, renderer and tests remain;
no actual model-call evidence was removed.

## Proposed live diagnostic and interpretation

Use fresh, independent sessions on the same frozen FIFO boundary and five
source-counter target. Keep the six-round/eight-cycle/model-setting limits;
three repetitions give a descriptive pilot, not a significance claim. Do not
reuse historical C actions or compare new minimal C only to historical B.

| New arm | Information | Comparison |
|---|---|---|
| B-compact | Unchanged compact raw evidence | Common baseline |
| C-full | B-compact + existing full semantic appendix | Reproduces previous C treatment |
| C-min | B-compact + minimal relations/counters | C-min vs B tests the useful relation payload; C-min vs full C tests packaging |
| P-min | B-compact + neutral filler matched to C-min on P's own trajectory | Controls added length without supplying relations |

Before live execution, integrate the renderer into a **new** runner/config,
freeze hashes, check common-field isolation on divergent own trajectories,
use actual provider counts for P, and test invalid-output/timeout exhaustion.
Keep unmatched or failed count requests, incomplete sessions and their costs
in the results. Record shared preprocessing separately from per-session cost.
Use API input/output counts with cached/reasoning details as subsets, and count
all replayed cycles, failed attempts and simulator executions. A byte cap is
not an observed input-token count.

C-min versus C-full changes detail and presentation as well as length. Even
if C-min wins, call that a **packaging benefit**, not proof that token length
alone caused the difference. If it matters to distinguish length, preregister
an additional C-min-padded arm: identical minimal semantic information padded
to full-C input tokens computed on its own trajectory. Neutral filler itself
can affect attention, so report that intervention explicitly.

- Earlier targets for C-min than B and P-min would support useful semantic
  grouping on this fixture; independent natural IPs would still be required.
- A C-min/full-C tie with fewer tokens demonstrates cost savings only.
- All arms tying again would limit this FIFO's diagnostic value; do not keep
  weakening B or modifying the target until C wins.

The new renderer is ready for offline use. The fresh live integration and
counted-token experiment are **not yet executed**.

## Finding two independent natural IPs

Prefer competing reachable temporal events over source length or depth alone.
The existing UART failed its preregistered B gate and its five groups were
already AST-identical before egg. The codec saturated in round 1. AXI VFIFO
encoder has only one nontrivial provisional merge and unresolved mappings/spec
boundary. These should not be promoted as qualified heldouts. See the
[complete screening record](next_ip_screen_2026-11-03.md).

Two next screening priorities are:

1. **AXI-stream frame FIFO** from the independent Alex Forencich lineage.
   Public [README](https://github.com/alexforencich/verilog-axis/blob/master/README.md)
   and [RTL](https://github.com/alexforencich/verilog-axis/blob/master/rtl/axis_fifo.v)
   document frame mode, bad/oversize-frame handling and pause controls. Screen
   a predeclared frame/pause configuration for commit versus rollback,
   backpressure and frame-boundary pause/resume. The old repository is
   superseded by `fpganinja/taxi`; a pinned original may be used for frontend
   compatibility, but a taxi derivative is not another independent IP. Audit
   the public contract before using it as a checker oracle. No qualifying
   groups are asserted yet.
2. **OpenTitan SPI_HOST core/controller** from a separate lineage. Its public
   [operation specification](https://opentitan.org/book/hw/ip/spi_host/doc/theory_of_operation.html)
   describes command segments and TX-empty/RX-full stalls: the controller
   preserves chip-select and pauses the serial clock until transfer can resume.
   Screen command completion, stall/resume and reset/abort paths. First prove
   compilation and original-source mapping through packages; then define a
   documented core interface with legal command/FIFO handshakes before a
   full bus wrapper. Component results must not be called full-IP verification.

For each candidate, freeze revision, source/spec hashes, module dependency
list, parameters, defines, clocks and resets. Run the same elaborated config
in Yosys, Verilator and formal tools. Prefer at least **three distinct events**
with at least two original sites each, including at least two nontrivial
groups requiring egg rewrites. Count trivial AST duplicates separately; merely
instantiating the same module twice does not supply independent IPs.

Review every promoted guard's typing, priority exclusions, activation context
and raw counter mapping. Establish the public-I/O checker independently,
exercise correct and single-fault controls, and calibrate or formally cover
each target within the budget. Keep all witnesses out of prompts. Save bounded
cover depth and assumptions without calling them full proofs.

Preregister the B-compact development gate before calls: in at least two of
three repetitions, at least two event groups remain incomplete after round 1,
and later rounds show measurable target progress in at least two repetitions.
Also require at least one batch of independently demonstrated reachable
headroom, so pure latency cannot force every arm to the same round. Keep
failure/no-progress/immediate-saturation exclusions with reasons. This selects
a stated hard-task population, not an unbiased sample of all IPs. Do not inspect
C outcomes during selection or change targets after B outcomes.

Only after two independent designs pass should the natural-IP A/B/P/C protocol
be frozen. Report every repetition and not-reached outcome, source coverage,
target rounds, API tokens, executed cycles and simulator counts. Claude can
review the protocol before outcomes, recompute blinded summaries and challenge
mapping/checker claims; tool proofs, controls and replay remain the evidence.

## Review provenance

This review inspected proposal/milestone text, current scripts/configs, saved
live summaries/prompts/replay checks, candidate records and primary candidate
documentation. Repository HEAD is `c71a3e580646d08fb6496c742b7b42b711179b36`;
the working tree also contains uncommitted November frontend and ablation
work. Historical freeze manifests, not HEAD alone, identify those runs.
No new paid API request, formal proof campaign or Claude review was performed
for this review. Thirteen focused tests passed across the new renderer,
frontend alias/case-priority checks, FIFO packing/isolation and UART checker/B
gate checks. All 18 preview payloads preserve the common B fields and exact
group/source/context/hit tuples. Local links and tracked diff whitespace were
also checked.
