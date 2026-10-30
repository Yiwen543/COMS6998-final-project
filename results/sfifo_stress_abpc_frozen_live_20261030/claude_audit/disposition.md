# Claude FIFO audit disposition — 30 October 2026

The [blind review](blind-review.txt) received only anonymous W/X/Y/Z
aggregate rows, with tools disabled. The [revealed review](reveal-review.txt)
used only Read/Glob/Grep and did not edit files, execute commands or compute
hashes. Both calls requested and returned `claude-opus-5-5`. The auditor's
analysis is independent prose, not the coverage oracle; original Verilator
counters and formal evidence remain authoritative.

| Claude finding | Independent disposition |
| --- | --- |
| All 12 first-target rows and per-round arithmetic | **Confirmed.** The first round with four late source counters matches `target-costs.csv` in every run. All 72 accepted actions contain eight cycles, with no retry. Actual replayed cycles are 16, 36, 64, 100, 144 and 196; model calls are 1–6 and simulator runs 2–7. |
| C versus B | **Confirmed.** Both reached target in round 5 in 3/3 repetitions, with 144 executed cycles and six simulator runs. Mean API input-plus-output tokens at first target: B 36,784; C 43,293, a 17.7% increase. No C-over-B performance gain is observed on this variant. |
| P's exact token matching | **Confirmed.** The 18 P prompts have a one-token absolute gap to same-trajectory C-style prompts, and each generation usage input count equals the provider count. The 54 count endpoint calls are separate from the 72 model generation calls and their usage; count latency is included in P wall time. The official count-only preflight used three additional count requests and zero model generations, excluded from pilot costs. |
| Frozen boundary and prompt isolation | **Confirmed with independent reconstruction.** `boundary-audit.json` verified all 27 frozen file hashes and rebuilt every one of 72 saved prompts from its own preceding actions, checker trace, original coverage and semantic data. It found A without coverage, B with raw only, P with raw plus neutral filler from its own trajectory, C with the same raw selection plus egg evidence, and no calibration text. The manifest mtime precedes the first prompt mtime; the manifest was not independently committed before calls, so this is not signed preregistration. |
| Checker and replay | **Confirmed.** The fixed stress harness passes `capacity=16`; original RTL, variant and independent behavioral control pass directed public-I/O checks, while a data-order mutant fails. Offline replay matched all 84 seed/round simulations on every original DUT counter identity and hit count, checker result and coverage summary. Correct RTL yielded zero checker failures; the runner's fault-control test shows failures are detectable. |
| Residual branch/expression points | **Supported by fixed-parameter source.** Uncovered branch `cond_then` points at lines 118 and 185 correspond to `OPT_WRITE_ON_FULL=0` and `OPT_READ_ON_EMPTY=0` option paths. They remain in the raw 24/16 denominators. No denominator waiver was applied. |
| Similar unmerged expressions | **Partly confirmed, partly corrected.** The pure-write case at line 128 and its near-full `if` at line 129 appear semantically related to grouped lines 95/178 and 96/179. The current frontend does not prove their *complete* guards equal because case-priority atoms are opaque, so they are not added to C's groups. Lines 133 and 165 are the simultaneous read/write cases and have **different activation guards** from pure write/read; they must not be called equivalent to those groups. All of these source counters remain in raw coverage. |
| Sampling, caching and run order | **Confirmed as limitations.** No temperature or random seed setting was supplied; the same model/settings were used for all arms. API output often repeats across sessions. Arms ran sequentially A/B/P/C, and cached input usage appears in some responses; the API-reported total input tokens already includes cached tokens, so detail fields are not added again. Wall time is confounded by run order, API latency and P's 54 count requests. |
| P's neutrality and retry path | **Open limitations.** The filler key and text explicitly say it contains no verification evidence, which may change model behavior. No live retry occurred, so the retry rematching path has only offline code/tests, not live evidence. |
| Semantic scope | **Confirmed within bounds.** Egg groups retain typed atoms, full activation, source counters and positive-edge/synchronous-reset context; Z3 pair checks and Boolean rewrite proofs are saved in preflight. This is two-state combinational normalization only. The Yosys equivalence proof establishes fixed-configuration state correspondence for the synthetic variant, not four-state or full-spec correctness. |

The blind review correctly warned that four source counters represent two
events, and that round/cycle/execution metrics are linked by the fixed batch
and replay policy. The revealed review rightly attributed the single P
round-6 observation to an early reset in that session, but one such session
cannot establish a semantic advantage for C. This is a negative result for a
single disclosed synthetic mechanism test, with no statistical or
natural-design generalization.
