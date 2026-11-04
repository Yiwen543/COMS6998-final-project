# Exploratory FIFO prompt-load ablation — 3 November 2026

This run asks whether losslessly shortening raw B feedback changes the
previous C-versus-B null result. It is **exploratory**: the same disclosed
ZipCPU-derived depth-16 FIFO stress variant and its earlier frozen outcomes
were known. Do not pool these sessions with the 30 October confirmatory
A/B/placebo/C pilot or interpret a positive outcome as independent replication.

## Candidate and frozen boundary

The fixed RTL is `examples/heldout_sfifo_stress/rtl/sfifo.v` (SHA-256
`309bf3231693e5f468a00c9b2ef8e9f02f7fc4728c3592a7932d520ba53b9289`),
an explicitly disclosed equivalence-proved redundancy variant of the public
FIFO. The existing specification, public-I/O checker, JSON cycle schema,
Verilator driver, 4-cycle seed, 8-bit/depth-16 configuration, and coverage
settings were reused unchanged. The prior independent B development trial
passed its prospective non-first-round-saturation gate, unlike the newly
screened UART and codec. The selection lock and every file hash are in
[`selection.json`](../results/sfifo_prompt_ablation_preflight/selection.json).

The updated Yosys pre-`proc` frontend, bounded Rust egg engine and independent
Z3 checks found two relevant groups whose **input expressions differ** and
need egg rewrites to merge. Group 1 is a read-pointer wrap pure-read event at
source lines 91/161. Group 2 is a near-full pure-write event at lines
96/129/179; line 129 became supported after an exact, Z3-proved case-priority
simplification. All five distinct Verilator branch/`if` counters are zero in
the seed and positive in the separate 36-cycle, checker-passing calibration.
Calibration actions and formal witnesses were never rendered into prompts.
The scanner reports two unsupported guards, one unresolved partial alias, and
additional nontrivial groups whose source counters are not uniquely mapped;
those are disclosed but not promoted. All 400 original DUT source counters
stay in the denominator, including unproven-unreachable points. Clock/reset
event context, typed atoms, complete supported activation guards, and source
locations remain attached; equivalence is binary/two-state only.

## Four prompt treatments

[`configs/sfifo_prompt_ablation_exploratory.json`](../configs/sfifo_prompt_ablation_exploratory.json)
was locked before live calls: three independent repetitions per arm, six
rounds, at most eight new cycles per round, same `gpt-6.1-sol` low-reasoning
settings and retry/timeout caps. Every round fully replays the seed and prior
actions. The five branch counters above are the preregistered target; the raw
coverage denominator does not change.

| Arm | Additional model-visible feedback |
| --- | --- |
| B-full | Original list of uncovered DUT counters, with source, line, column, type, outcome, hits and source text. |
| B-compact | Exactly the same list in a reversible source/line dictionary and point table. A round-trip assertion checks every point. |
| P-compact | B-compact plus neutral filler matched against a C-style prompt built on P's own trajectory, using the OpenAI Responses input-token count endpoint. |
| C-compact | B-compact plus the two egg/Z3-proved, raw-mapped nontrivial groups and explicit unsupported/mapping evidence. |

All arms received the same full specification, full RTL, seed, own actions,
checker status and execution trace. B-compact and C-compact share exactly the
same raw-counter representation. The fixed first-round prompt user content
was 21,247 bytes for B-full, 17,430 for B-compact, and 21,930 for C-compact;
API-reported tokens, not bytes, are the cost measurement. Reordering or
omitting RTL was outside this ablation.

## Live result

All **72** generation calls requested and returned `gpt-6.1-sol`, completed,
passed JSON validation on the first attempt and executed the complete batch.
No checker defect was reported. All 12 sessions reached five of five target
source counters in **round 5** and 22/24 DUT branch points at that round.
The first event reached three of five target counters in round 3 in every
session. The four arms had the same 144 executed replayed cycles and six
simulator executions at first target in every repetition.

| Arm | First target round, repetitions 1/2/3 | API input + output tokens at first target, repetitions 1/2/3 | Mean tokens | Mean branch-point Token ROI¹ |
| --- | --- | --- | ---: | ---: |
| B-full | 5 / 5 / 5 | 36,825 / 36,807 / 36,891 | 36,841 | 0.299 |
| B-compact | 5 / 5 / 5 | 34,228 / 34,184 / 34,429 | 34,280 | 0.321 |
| P-compact | 5 / 5 / 5 | 41,700 / 41,863 / 41,833 | 41,799 | 0.263 |
| C-compact | 5 / 5 / 5 | 41,626 / 41,652 / 41,622 | 41,633 | 0.264 |

¹ Newly covered original DUT branch points over the 11-point seed, per 1,000
API-reported input-plus-output tokens. The numerator is 11 for every row.

B-compact used **7.0% fewer tokens** than B-full at the same target round.
C-compact used **21.4% more tokens** than B-compact, with no coverage,
cycle or execution advantage. P-compact likewise reached the same round.
Its own-trajectory provider counts differed from corresponding C-style
input counts by at most one token; all 18 P generation inputs agreed with
their count-only records within the two-token gate. There were 54 separate
count-only requests, excluded from generation-token ROI but included in P wall
time. Across all arms, generation usage was 544,608 input and 13,522 output
tokens. Cached input (81,801) and reasoning output are subsets, never added
again. Individual wall times varied; C's lower mean wall time in this tiny
sample cannot be attributed to semantic feedback when target rounds and
simulator work are identical.

Round 2 and 3 actions in most sessions filled the FIFO; rounds 4 and 5 drained
it. Different JSON actions often produced the same high-level write/write/
read/read sequence. The separate calibration reaches the five counters in
36 total cycles, corresponding to four eight-cycle rounds after the seed, so
there was one round of practical headroom; none of the arms used it. This
suggests the model's stimulus schedule, rather than prompt encoding alone,
limited this particular result. It does **not** prove that e-graph feedback is
ineffective on other RTL.

## Evidence and validation

- [Per-call JSONL](../results/sfifo_prompt_ablation_live_20261103/calls.jsonl),
  [per-round JSONL](../results/sfifo_prompt_ablation_live_20261103/rounds.jsonl),
  [first-target CSV](../results/sfifo_prompt_ablation_live_20261103/first-target.csv),
  [round CSV](../results/sfifo_prompt_ablation_live_20261103/rounds.csv), and
  [comparison JSON](../results/sfifo_prompt_ablation_live_20261103/comparison.json)
  retain individual results and target misses (there were none).
- [Cost curves](../results/sfifo_prompt_ablation_live_20261103/coverage-cost.png)
  show target source counters versus API tokens, cycles, executions and wall
  time. Prompt JSON files are saved per call.
- [Replay validation](../results/sfifo_prompt_ablation_live_20261103/replay-validation.json)
  matched all **84** live seed/round simulations on every original DUT source
  counter and hit count, checker result and coverage summary.
- The hidden OpenAI key was deleted after the live run. No Anthropic call was
  used for this exploratory ablation.

## Interpretation and next discriminating experiment

This ablation finds a real **token-efficiency benefit from lossless B packing**
but **no observed C-over-B coverage benefit**. The compact format retained all
raw points, so it did not intentionally handicap B. A longer C prompt could
still mask useful semantics; the matched placebo isolates length only
imperfectly because neutral text can affect model behavior. Three repetitions
with similar action patterns do not justify a significance claim.

For the next independent test, screen a deeper public SPEC+RTL controller or
FIFO for several reachable, source-mapped **nontrivial** egg merges with more
than one viable stimulus schedule and at least one target that B does not
reach at the same round in every development repetition. Freeze that design
before C outcomes. A further exploratory ablation can hold B-compact fixed
and compare full C with a **minimal** C containing only the two proven group
relations and their original counters; this tests whether C's long semantic
serialization is itself the prompt bottleneck. The primary C-versus-B result
must still use identical common information and retain all raw DUT counters.

## Reproduce without another model call

```sh
.venv/bin/python -m unittest tests.test_sfifo_prompt_ablation -q
.venv/bin/python scripts/preflight_sfifo_prompt_ablation.py
.venv/bin/python scripts/run_sfifo_prompt_ablation.py --mode mock --output build/sfifo_prompt_ablation_mock_NEW
.venv/bin/python scripts/analyze_sfifo_prompt_ablation.py --run results/sfifo_prompt_ablation_live_20261103
.venv/bin/python scripts/run_sfifo_prompt_ablation.py --mode replay --output build/sfifo_prompt_ablation_replay_NEW --replay-source results/sfifo_prompt_ablation_live_20261103/calls.jsonl
.venv/bin/python scripts/validate_sfifo_stress_replay.py --live results/sfifo_prompt_ablation_live_20261103 --replay build/sfifo_prompt_ablation_replay_NEW
```

The live directory is immutable evidence for this exploratory run. A new
live experiment needs a fresh staged API key and a new output directory.
