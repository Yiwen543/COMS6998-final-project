# Why the current timer B/C pilot did not show an E-graph benefit

This audit compares the supplied proposal and background papers with the saved
`ttc_counter_lite_0007` live pilot. It is a **post hoc mechanism audit**, not a
new preregistered trial or a claim of statistical significance. Its machine-
readable numbers are in
[`results/ttc_live_20261020/egraph-signal-audit.json`](../results/ttc_live_20261020/egraph-signal-audit.json).

## Which paper result are we trying to reproduce?

The project proposal (`project_background_reading/E_Graph_Augmented_Tool_in_the_Loop_Agent_for_High_Coverage_RTL_Verification.pdf`,
Sections III-IV) proposes the *new* A/B/C test: A gets text/log feedback; B also
gets raw uncovered coverage; C gets B's evidence normalized and grouped through
an E-graph. It predicts possible coverage and token-efficiency gains but gives no
previous measured B-versus-C result to reproduce.

`LLM4Cov` (`project_background_reading/2602.16953v3.pdf`, Sections 3-4 and
Appendix B) does not use E-graphs. Its gain comes from an execution-aware
training pipeline: simulate full generated testbenches, select low-coverage
intermediate states, keep coverage-improving transitions, and progressively
fine-tune a smaller student. It evaluates 83 cid012 CVDP-ECov repositories and
156 AutoEval-ECov tasks; agentic evaluation uses three refinement rounds and
reports threshold pass rate/average coverage with five samples. Its reported
metrics use Xcelium/IMC, different models, full-testbench generation, and a
large training corpus. Our single fixed-driver JSON-stimulus pilot is not a
replication of its training or benchmark numbers. Its reproducible insight for
our study is the controlled feedback loop, execution-validity accounting,
matched simulator-call budget, and early-round measurement.

`SmoothE` (`project_background_reading/3669940.3707262.pdf`) optimizes the
*extraction algorithm*: choose a valid low-cost DAG from an existing E-graph,
including shared subexpressions, using a differentiable relaxation. Its outcome
is extraction cost/time, not verification coverage or LLM stimulus quality.
`ASPEN` (`project_background_reading/ASPEN_LLM-Guided_E-Graph_Rewriting_for_RTL_Datapath_Optimization.pdf`,
Sections III-IV) uses an LLM to propose/select proven rewrite rules, runs
equality saturation over datapath expressions, extracts candidate RTL, and
iterates using synthesized PPA feedback. It checks final RTL equivalence.
Its LLM guides the E-graph; it does not test an E-graph feedback prompt that
guides an LLM to verify RTL. Its useful engineering lessons are to prove rules,
preserve typed expression semantics, map feedback to actual graph nodes, and
ablate rule selection and feedback separately. Reproducing ASPEN's numeric PPA
results would require its egglog/rule stack and commercial synthesis flow, and
would answer a different research question.

## What the saved B/C run actually measured

The exact original DUT, specification, checker, seed, model, driver, coverage
denominator, per-round cycle limit, and simulator settings were frozen across
arms. The 3x4 live run used `gpt-6.1-sol`; every accepted response was replayed
offline with identical checker and DUT counters. The saved first-round prompts
are 11,252 bytes (A), 81,060 (B), and 89,379 (C). Prompt isolation holds:
all shared fields are identical, and B/C have identical raw coverage arrays.

However, C's semantic increment is weak for this design:

1. The timer adapter manually writes eight local Boolean predicates after a
   source-hash check. Yosys emits a JSON netlist, but those eight predicates
   are not extracted from it. The egg run genuinely saturates in three
   iterations, yet all eight coverage-target roots stay in **eight distinct
   E-classes**. Each root merges only its own De Morgan/double-negation form;
   no two separate uncovered coverage locations are grouped as equivalent.
   Shared `addr_status` and `match_flag` child atoms are dependencies, not
   equivalent full read/write or reload/interrupt guards.
2. At the seed, 8 uncovered locations are mapped, while 250 are unmapped,
   including 241 toggle-direction counters. In first-round B and C, **all
   eight mapped locations are already hit** in every repetition. Therefore
   there is no later unresolved mapped predicate for C to explain.
3. B/C both reach the preregistered 180/266 toggle target in one call, one
   simulation, and 21 executed cycles in every repetition. C uses 2,187-2,479
   more API tokens at that point. First-round C-minus-B toggle differences are
   +5, -1, and -23; these independent responses do not show a stable benefit.
4. All final B/C runs reach 234/266 and all 14 branch, 23 line, and 9
   expression counters. The remaining 32 toggle directions are the upper
   16 bits of `axi_rdata`, whose RTL assignments always zero-extend or reset to
   zero. This source-implied two-state ceiling remains in the raw denominator.
   Neither arm can improve those counters with stimulus alone.
5. C receives equivalent spellings, but no coverage-aware explanation cost
   function, no complete enclosing enable/prescaler/priority path guards,
   and no state-transition reachability. Egg's `AstSize` representative is a
   compact syntax tree, not a measured estimate of which stimulus will reach
   an uncovered branch. This differs from both the proposal's envisioned
   structural bottleneck feedback and the extraction objectives in the
   optimization papers.

These facts support a narrow conclusion: the *current C implementation on the
current timer* did not add enough discriminating information beyond B. They do
not show that sound E-graph feedback cannot help verification agents.

## Reproduce this diagnosis without new model calls

From the repository root, with the existing toolchain and saved results:

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_ttc_pilot.py' -v
.venv/bin/python scripts/audit_egraph_signal.py results/ttc_live_20261020 \
  --output results/ttc_live_20261020/egraph-signal-audit.json
```

Inspect the three `prompt-*-1-1-1.json` files, `mapped-predicates.json`,
`egg-evidence.json`, `rounds.jsonl`, `target_costs.csv`, and the resulting audit
JSON. The script fails if shared prompts differ, A/B/C coverage evidence leaks,
or egg target IDs do not match the reviewed source map. It counts root-class
merges, mapped first-round hits, remaining raw counters, and target cost from
saved simulator output. For a full offline rerun of the 36 saved model actions,
use the replay command in [`docs/ttc_pilot.md`](ttc_pilot.md). New API calls are
unnecessary to reproduce the diagnosis.

## A faithful next test of the proposal's distinct hypothesis

1. **Build a typed frontend before more model trials.** Translate original RTL
   expressions and complete activation contexts from a reviewed AST/IR into a
   width- and signedness-aware Boolean/bit-vector representation. Keep clock,
   reset, state, source span, branch polarity, and each raw counter separate.
   Prove each rewrite under the declared two-state semantics; formally check
   RTL variants where possible. Do not equate different behavioral cases or
   assume a counter is hit because an equivalent predicate is hit elsewhere.
2. **Preflight candidate tasks without inspecting model outcomes.** Choose
   CVDP cid012 designs or equivalence-checked variants with multiple
   source-distinct equivalent predicates, nontrivial nested guards, and a
   reachable coverage target that raw feedback does not hit immediately.
   Quantify source-location groups, mapped uncovered points, and saturation
   headroom before live calls. Retain unreachable points in raw totals and
   report a separately justified reachable-target analysis.
3. **Run the same proposal A/B/C arms on held-out tasks.** Keep the checker,
   model/version, context, token and simulator budgets, seeds, and stopping
   rule fixed. C must receive exactly B's raw evidence plus validated
   equivalence groups, full path guards, and source provenance. Give neither
   arm solver witnesses or hand-written target vectors. Keep independent
   model sessions and record prompt sizes, calls, failures, coverage, cycles,
   wall time, and API-reported tokens.
4. **Test the mechanism, not just the endpoint.** Before live execution,
   require at least one uncovered E-class spanning distinct source predicates
   and a bounded explanation that identifies a meaningful common guard.
   Measure when those grouped locations become hit, coverage at each call,
   and token/cycle cost to a preregistered target. A length-matched placebo
   feedback arm can test whether any apparent C gain comes merely from more
   prompt text. Repeat across several designs and syntactic variants; report
   paired descriptive results and uncertainty without promising a positive
   outcome.

This preserves the proposal's central C-versus-B question while avoiding an
unsupported inference from LLM4Cov, SmoothE, or ASPEN. It also identifies an
engineering gate: until C has verified cross-location equivalence and complete
guards that B lacks, another expensive live timer run is unlikely to isolate
an E-graph effect.
