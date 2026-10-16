# Background reading review and engineering decisions

This review connects the supplied proposal and ten accompanying background PDFs to
this milestone. The reading focus is their problem definitions, methods,
evaluation protocols and limitations relevant to the implementation; it is not
a reproduction of every paper's optimization/training stack. Extracted text and
visual inspection intermediates stay under ignored `build/readings/`.

## Proposal and verification foundation

**Completed project proposal — E-Graph-Augmented Tool-in-the-Loop Agent for
High-Coverage RTL Verification.** Source:
`project_background_reading/E_Graph_Augmented_Tool_in_the_Loop_Agent_for_High_Coverage_RTL_Verification.pdf`.
The research question concerns coverage and token efficiency from semantic
feedback. The three-way comparison is the central experimental contract:
text-only, raw coverage, and E-graph-normalized coverage. The immediate timeline
milestone is simulator/dataset setup. We implement that plus a small integration
iteration. One proposal phrase needs an implementation distinction: egg cannot
parse RTL on its own; a frontend/translation layer must supply expressions.
We expose that layer as an explicitly limited adapter rather than presenting egg
as a complete SystemVerilog frontend.

**LLM4Cov — Execution-Aware Agentic Learning for High-coverage Testbench
Generation (`2602.16953v3.pdf`).** Section 3 defines feedback as status, coverage,
and log; state includes a fixed repository, the current complete TB and current
feedback. This supports compact per-iteration artifacts rather than unbounded
conversation replay. Its execution-validated curation, coverage-ranked revisions,
policy-aware synthesis and worst-state sampling are training methods, not part
of our environment setup. Section 4 uses cid012 for 83 CVDP-ECov repositories
with a revised full-repository-visible protocol; AutoEval-ECov adapts VerilogEval.
Coverage pass thresholds and average coverage are distinct from assertion-based
bug detection. We therefore retain both execution coverage and checker status,
and do not label the cid003 arbiter result a reproduction of that benchmark.
Matched simulator budgets are necessary; cycle/token budgets are also needed
to avoid rewarding a very large single run.

**Can AI Agents Really Complete RTL-to-GDS? (`2607.17528v3.pdf`).** The paper
studies stage completion, design score, runtime/cost and Token ROI in a long
physical-design workflow. Its interface-mismatch and incomplete-artifact
observations motivate explicit exit checks, persistent artifacts, exact tool
versions and structured results. Its ROI combines a physical-design objective
with runtime/cost; our branch-points-per-1,000-tokens formula is a project-specific
adaptation, not the same numeric metric. A checker result, coverage percentage,
execution count and wall time remain separately inspectable.

**Large Language Model for Verilog Code Generation: Literature Review and the
Road Ahead (`3841636.pdf`).** The survey organizes model choices, datasets,
generation and alignment methods. Its discussion of parallel hardware semantics,
benchmark versioning, prompt sensitivity and incomparable experimental protocols
supports cycle-accurate stimulus scheduling and strict source/dataset records.
Compiling code is only one level of correctness. The independent oracle and
conforming/defective checker controls address that gap in this small example.
No cross-paper performance numbers are used as our baselines.

## Equality saturation and RTL feedback

**ASPEN — LLM-Guided E-Graph Rewriting for RTL Datapath Optimization.** The
pipeline in Section III separates verified rule proposals, rule selection,
saturation/extraction and measured PPA feedback. Proposed arithmetic rewrites
are checked with proof scripts before inclusion. Our corresponding boundary is
fixed, sound Boolean rules with independent truth-table validation, bounded
saturation and measured coverage feedback. Our objective is stimulus selection
and predicate explanation; the DUT is not rewritten for PPA. Consequently we
do not install ASPEN's complete synthesis/physical-design stack for this step.
Source: `ASPEN_LLM-Guided_E-Graph_Rewriting_for_RTL_Datapath_Optimization.pdf`.

**SmoothE — Differentiable E-Graph Extraction (`3669940.3707262.pdf`).**
Differentiable node selection addresses extraction cost and permits richer cost
models/GPU parallelism. Completeness, child dependencies and acyclicity matter
when selecting a realizable extracted program. This milestone needs small
predicate explanations rather than an optimal hardware DAG, so egg's AST-size
extractor suffices. It does not establish optimal coverage stimulus, an optimal
DAG cost, or sequential correctness. We preserve graph structure in JSON so more
sophisticated explanation extraction can be studied later if graph size warrants it.

**e-boost — Boosted E-Graph Extraction with Adaptive Heuristics and Exact
Solving.** Fast heuristic DAG cost calculation, adaptive pruning and warm-started
exact solving address the quality/runtime tradeoff. The shared-subexpression
example explains why a locally smallest node need not give a globally best DAG.
For our goal, the cost of a useful feedback explanation might include prompt
length, shared predicates and activation effort. That is a future objective;
we do not claim greedy AST-size extraction optimizes it. Source:
`e-boost_Boosted_E-Graph_Extraction_with_Adaptive_Heuristics_and_Exact_Solving.pdf`.

**LLM-Guided Strategy Synthesis for Scalable Equality Saturation
(`2604.17364v1.pdf`).** EggMind's EqSatL makes rule partitioning, scheduling and
simplification explicit strategy choices; proof-derived motifs and tractability
feedback avoid uncontrolled e-graph growth. This supports starting with a small
reviewed rule set and explicit iteration/node/time bounds. Generated rewrite
strategies are a separate research dimension; allowing them to change in the
A/B/C stimulus experiment would confound semantic feedback attribution.

**E-ALS — Approximation-Potential-Aware E-Graph Rewriting for Approximate Logic
Synthesis (`2609.13276v1.pdf`).** The paper separates exact equivalent structural
exploration from downstream approximation and its bounded-error evaluation.
Its structural-bias observation motivates future tests on equivalent syntactic
variants. Approximate logic rewriting is outside our verification contract:
we must preserve exact Boolean meaning, and cannot merge approximately equal
predicates or use an approximation to suppress a checker failure.

**Efficient Extraction for Effectful E-graphs (`3839530.pdf`).** The distinction
between pure equivalence and effect-safe extraction, and statewalk DP's handling
of effect order, warns against discarding temporal behavior. We limit rewrites
to pure one-bit predicates; reset events, clocks and sequential dependencies stay
attached as context. An asynchronously cleared register and a synchronously
cleared register must never be equated merely because their reset-value
expressions match. FIFO temporal reachability will require a state-aware frontend
or solver, not just this Boolean adapter.

## Agentic evaluation

**HeuriGym — An Agentic Benchmark for LLM-Crafted Heuristics in Combinatorial
Optimization.** Section 3 separates execution, solution generation, correctness
verification and quality evaluation, and distinguishes demonstration refinement
from held-out testing. Its stage-based SOLVE and quality/yield metrics reinforce
separate validity and quality reporting. For us: compilation/completion, checker
validity, bug detection and coverage are separate outputs. Small-demo tuning of
the arbiter cannot establish generalization. Future A/B/C tests need unseen tasks
and identical budgets; quality of a fixed hand-authored heuristic is not model
performance. Source:
`ICLR-2026-heurigym-an-agentic-benchmark-for-llm-crafted-heuristics-in-combinatorial-optimization-Paper-Conference.pdf`.

## Practical decisions from the combined reading

- Start with Verilator coverage and Icarus portability; add Yosys as an inspected
  frontend output. No place-and-route tools are necessary for execution coverage.
- Use actual egg equality saturation. Keep behavioral partitions, equivalent
  expressions, coverage locations and temporal context as separate concepts.
- Keep original RTL and specification hashes stable across all experiments.
- Report raw point denominators, including unreachable points; never manufacture
  100% branch coverage by silently dropping a counter.
- Retain the exhaustive run as a ceiling and add the compact run for efficiency.
- Validate the checker using conforming and single-defect controls. Accumulated
  failing vectors do not equal a count of distinct bugs.
- Collect real API token usage only once model orchestration is added. The present
  reports deliberately use null token/ROI fields.

The supplied root-level CVDP/ChipNeMo/macro-placement papers are retained locally;
they are outside the eleven-PDF proposal-folder inventory reviewed above.
