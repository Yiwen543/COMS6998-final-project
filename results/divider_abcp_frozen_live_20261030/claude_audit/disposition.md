# Claude Opus 5.5 audit disposition — 30 October 2026

The [blind review](blind-review.txt) used anonymous W/X/Y/Z aggregate data
with tools disabled. The [revealed review](reveal-review.txt) used only
Read/Glob/Grep. Both calls returned `claude-opus-5-5`; costs recorded by Claude
Code were $0.172571 and $1.3799872. The auditor's prose is an independent
analysis, not a coverage oracle. The model explicitly stated which artifacts
it did and did not inspect.

| Finding | Independent disposition |
| --- | --- |
| All 12 target rows match cumulative rounds | **Confirmed.** First 24/24 branch round and cumulative tokens, cycles, executions, and wall time match `rounds.jsonl` and `target-costs.csv`. |
| Frozen file integrity | **Confirmed for this workspace.** All 16 `files_sha256` entries in `docs/divider-frozen-pilot-2026-10-30.json` match current bytes. The manifest file's modification time precedes the first rendered prompt and call log. It was not committed as a separate Git revision before the run, so this is timestamp and hash evidence, not a signed preregistration. |
| Replay accounting | **Confirmed, with wording correction.** Every execution replays the 4-cycle seed **and all accepted history**, plus the new batch. Standard cumulative cycles are 16/36/64/100, including the seed-only run; P rep1 uses 4 rather than 8 new actions in round 3 and has 60/92 at rounds 3/4. The blind packet's short wording omitted the history clause; the frozen manifest and runner stated it correctly. |
| `branch_covered_at_stop` column name | **Confirmed presentation error.** This field is the count at the first target round, or the last observed round when not reached. Runs continued after reaching the target. The saved CSV is preserved for audit; the report describes the field accurately. |
| Placebo token matching | **Confirmed material limitation.** Its neutral *extra value* was byte-matched to C's egg JSON (8,798 versus 8,800 serialized bytes in the first prompt), but API input tokens were 6,538 for P versus 8,660 for C in rep1 round1. Thus P controls added text length in bytes, not model token load. It cannot isolate the effect of prompt-token quantity. |
| Semantic soundness and provenance | **Supported within scope.** Five groups have distinct source locations, full activation guards and identical event context within each group. Z3 pair checks were executed by `semantic_groups`; the saved C `rewrite-proof.json` reports `unsat` XOR for each Boolean rewrite. The mapped line 86 `if` counter uses the documented unique true-path rule. Seven unsupported extraction cases remain reported, and all original coverage counters remain in the denominator. Four-state and sequential equivalence are not claimed. |
| Primary target not aligned with remaining semantic groups | **Confirmed critical limitation.** All five groups are fully covered by round 2 in every arm. The sole remaining branch point is the `if` or `else` outcome at RTL line 51, outside every C group. At the deciding round C's `equivalent_uncovered_groups` is empty. The experiment measures a real frozen target, but it offers no direct mechanism for C to help with the final branch. |
| Checker and DUT defect | **Confirmed within fixed contract.** The checker computes quotient/remainder from unsigned arithmetic using only public outputs. The separately written behavioral RTL passes Icarus; its one-fault remainder mutant fails. The original RTL fails the same category on both Icarus directed control and live Verilator traces. Repeated failing cycles are one distinct `remainder` defect type. The divide-by-zero sentinel is a declared study assumption, not a benchmark-wide standard. |
| Known benchmark examples in prompts | **No supplied-vector leakage found.** None of the 10 dividend/divisor pairs listed in the CVDP task prompt appears in the common seed or any generated action across 48 calls. No rendered prompt contains the benchmark's failing-example table or repair section. Later prompts legitimately contain each arm's own earlier generated actions. The auditor itself only inspected four prompts, so this extra check was performed locally after its review. |
| Model and usage | **Confirmed.** All 48 OpenAI calls requested and returned `gpt-6.1-sol`; all were accepted at attempt 1. Reasoning/cached token fields are retained separately in call logs and not added twice to input-plus-output totals. The Claude calls used `claude-opus-5-5` exclusively. |
| Independent replay | **Confirmed after the Claude review.** The saved model actions were replayed without API calls. [Validation](../../divider_abcp_frozen_replay_20261030/validation.json) matches all 60 seed/round simulations on every original DUT point identity and hit count, checker result, and coverage summary. Replay wall/model-call costs are not pooled with live costs. |

The central conclusion remains **no observed C-over-B improvement** in
time-to-target on this single divider. Both reach 24/24 branches at round 3 in
3/3 repetitions. C incurs a larger token cost. The placebo mismatch and
target/group misalignment prevent a stronger causal interpretation. A new
design and prospectively token-matched placebo are required before claiming a
general E-graph effect.
