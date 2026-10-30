# Midterm fixed checker and B development screen — 30 October 2026

## Boundary implemented

The two pinned CVDP source sets and their supplied specifications remain byte
identical to [`midterm-candidate-lock.json`](midterm-candidate-lock.json). The
model action boundary is an exact JSON `actions` array. The fixed parser
rejects unknown fields, booleans used as integers, out-of-range values, and
overlong batches. `codec` actions contain `reset`, 64-bit `enc_data`, 8-bit
`enc_control`, `dec_valid`, and 66-bit `dec_word`. `search` actions contain
`reset`, `start`, `pause`, 8-bit `key`, `write_en`, 3-bit `write_addr`, and 8-bit
`write_data`; `start` is separate from writes and pause. Both drivers apply
actions between clock edges, log public outputs before and after the active
edge, and contain no expected-output logic. The Python checker reads only
these public traces. Verilator Coverage-3 excludes the testbench and retains
separate source counters. Icarus runs the same fixed drivers without coverage.

[`midterm_fixture.py`](../scripts/midterm_fixture.py) is specification based,
with an explicit **limited scoring scope**:

* Codec: synchronous reset timing and zero values; unconstrained data-mode
  encoding (`01` header and unchanged 64-bit word); control-mode header `10`
  and four unambiguous type-field encodings; valid decoder data header (`01`)
  and raw 64-bit value; registered sync-error behavior; listed type-field to
  control-mask mapping; one exact decoded control payload (`0x78`); invalid
  type-field error; and output hold when decoder valid is low. The supplied
  prose is not precise enough to derive every 64-bit
  decoded control payload or every malformed-payload error independently.
  Those subcases remain unresolved and are not scored as passes.
* Search: memory must be initialized before `start`; key stays stable and
  writes are excluded during a search. For MEM_DEPTH=8 and MAX_MATCHES=2,
  the model computes match addresses from its own memory image, expects count,
  first two indices, overflow, one-cycle `done` after the specified traversal
  and read latency, pause delays, and synchronous reset behavior. Reset
  invalidates the checker memory image, requiring reinitialization before a
  later search. The exact completion timing interpretation is reviewed
  against the prose and one independent known-good scenario; it remains a
  declared assumption to revisit before the held-out freeze.

The original codec RTL is **not** assumed correct. A separate development
sequence triggers `decoder_data` and `reset_timing` categories; these are two
distinct defect types, regardless of repeated cycle failures. A separate
search sequence with initialized memory, three matches, pause/resume, and
overflow passes the checker and reaches 32/32 line and 26/26 branch counters.
Synthetic known-correct reference traces and one-fault altered traces are in
[`test_midterm_fixture.py`](../tests/test_midterm_fixture.py); these validate
checker discrimination but are not a separately proven correct RTL control.
The previous narrow SBY properties also remain separate from a full IP proof.

## B development policy and current evidence

[`run_midterm_b_development.py`](../scripts/run_midterm_b_development.py)
reuses the existing Responses API adapter, with fixed `gpt-6.1-sol`, one
independent model session per IP, two rounds, up to 32 new cycles per round,
and at most one response retry. Each attempt saves the complete rendered
prompt, request settings, response/usage fields when received, validation
result, raw simulation log, and coverage. Every accepted batch replays the
common seed and all earlier actions; cycle and execution accounting includes
replays and failed simulated attempts. The B prompt has the supplied spec,
original RTL, common seed, previous model actions, checker findings, public
trace, and **raw uncovered line/branch/expression points** with source text.
Toggle counts are measured but individual toggle points are not sent in this
development screen because the codec has 2,074 toggle directions. This
selection policy must be frozen identically for B, C, and placebo later.
No e-graph groups, formal witnesses, or reachability calibration sequences
appear in B prompts.

The [`mock development run`](../results/midterm_b_development_mock_20261030/summary.json)
is an offline integration test only. Its generated actions ignore feedback
and cannot answer the research question. The first
[`live development attempt`](../results/midterm_b_development_live_20261030/summary.json)
received **zero model responses**: sandbox DNS blocked `api.openai.com`, and
all four attempts were logged as `APIConnectionError`. An uncredentialed
request outside that sandbox reached the OpenAI endpoint and received the
expected 401. The staged key was deleted automatically. No coverage outcome
from that failed attempt is attributed to the LLM.

The subsequent [network-enabled 32-cycle B run](../results/midterm_b_development_live_network_20261030/summary.json)
returned the requested `gpt-6.1-sol` model. In its first generated batch,
codec reached 109/109 line and 95/96 branch points; search reached 32/32 line
and 26/26 branch points. These are development observations, not an A/B/C
comparison. [Prefix replay](../results/midterm_b_development_live_network_20261030/prefix_analysis/prefixes.json)
shows that codec's eight prequalified equivalent groups were all covered by
the first eight model actions. Search's single group was covered by the first
16 actions. Thus the original 32-cycle budget is too generous to test the
specific benefit of C's group information.

An **independent** [8-cycle/round B development run](../results/midterm_b_development_short_live_20261030/summary.json)
used four rounds, the same model and common seeds, and a fresh model session.
Coverage is cumulative under full seed-plus-history replay:

| IP | Round | DUT line | DUT branch | DUT toggle | API tokens cumulative | Executed cycles cumulative | Fully covered candidate groups |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| codec | 1 | 62/109 | 41/96 | 1331/2074 | 30,997 | 16 | 8/8 |
| codec | 2 | 99/109 | 62/96 | 1419/2074 | 54,404 | 36 | 8/8 |
| codec | 3 | 103/109 | 79/96 | 1636/2074 | 73,364 | 64 | 8/8 |
| codec | 4 | 103/109 | 96/96 | 1642/2074 | 91,030 | 100 | 8/8 |
| search | 1 | 20/32 | 9/26 | 46/334 | 8,421 | 16 | 0/1 |
| search | 2 | 31/32 | 20/26 | 113/334 | 17,318 | 36 | 1/1 |
| search | 3 | 32/32 | 26/26 | 140/334 | 24,424 | 64 | 1/1 |
| search | 4 | 32/32 | 26/26 | 146/334 | 38,695 | 100 | 1/1 |

The group counts are joined back to **original source counters**, not treated
as a replacement denominator; see [semantic-group-progress.json](../results/midterm_b_development_short_live_20261030/semantic-group-progress.json).
Search's fourth accepted batch required one retry, which is included in the
five model calls and its total token count. The codec checker repeatedly
reported `decoder_data` (one distinct defect category in that run). The
search checker reported no defect. The token counts are API-reported input
plus output tokens; cached/reasoning details are retained in the call logs,
not added again. Neither IP has yet passed the predeclared "B does not
immediately solve the semantically redundant targets" screen. The short
codec run retained uncovered line points, but all C-relevant groups were
already covered in its first round. No held-out A/B/C/placebo experiment is
claimed from these trials.

## FIFO selection gate

[`screen_midterm_fifo.py`](../scripts/screen_midterm_fifo.py) reads both pinned
CVDP async FIFO task versions' original `src/async_fifo.sv` and `docs/fifo.md`, then
flattens the hierarchy **before** Yosys `proc`. It checks supported typed
predicates with the Rust egg engine and Z3, maps source locations to raw
Verilator counters, and runs a shared dual-clock reset/idle seed. The
[`FIFO 0003 result`](../results/midterm_candidate_preflight/fifo-hierarchical-screen-0003.json)
and [`FIFO 0004 result`](../results/midterm_candidate_preflight/fifo-hierarchical-screen-0004.json)
each have 14 supported targets and two unsupported memory cases without source
mapping. It finds two source-distinct equivalent groups, both active-low
reset guards in the pointer modules. Both groups are already covered by the
seed (line pairs 340/305 and 251/211), leaving **zero qualifying uncovered
groups**. It compiles under Icarus and passes Verilator lint with width
warnings. It is a valuable deeper FIFO functional case but does **not** yet
qualify as an e-graph-effectiveness task under the preregistered criterion.

An external source search identified the public-domain
[ZipCPU `sfifo.v`](https://github.com/ZipCPU/wb2axip/blob/master/rtl/sfifo.v),
pinned to commit `2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b`.
The [source-preserving preflight](../results/midterm_candidate_preflight/external-sfifo/screen.json)
finds two source-distinct equivalent guard groups: push-only (`2'b01`, lines
90/156) and pop-only (`2'b10`, lines 91/157). Both pairs are seed-uncovered
and reached by a separate calibration run. Their e-classes remain separate.
The seed covers 14/18 line and 9/14 branch points; the calibration reaches
18/18 line and 12/14 branch points. Three extracted case targets lack source
mappings, and no independent functional checker or B development trial exists
for this IP yet. It is a **provisional** FIFO candidate, not a frozen task.

## Gates remaining before held-out A/B/C/placebo

1. Treat codec and search as development controls for the 32-cycle budget;
   their B trials saturate too quickly. For the 8-cycle budget, codec's
   semantically redundant groups still saturate in round 1, while search's
   only group is reached in round 2. Keep all trial data and do not relabel
   these as held-out C wins or losses.
2. Resolve the limited checker scope and completion timing assumptions in a
   reviewed checker contract. Add known-correct and single-fault **RTL**
   controls, plus SBY references, before labeling any whole-IP verdict.
3. Build a specification-derived fixed checker and JSON driver for the
   provisional ZipCPU FIFO, add correct/faulty RTL controls, then conduct
   independent B development trials. Seek another independent IP with
   multiple nontrivial groups. The CVDP async FIFO does not pass the current
   semantic gate; its dual-clock checker and pointer synchronization
   assumptions would need their own fixed contract if retained for a
   functional-verification study.
4. Freeze checker, driver, target, raw denominator, feedback selection,
   A/B/C/placebo prompt lengths, budgets, and hashes. Run independent held-out
   repetitions and report all misses, costs, and distinct defects.

## Reproduce without model access

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_midterm_fixed.py --ip codec --actions configs/midterm_codec_seed.json --output build/recheck-codec
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_midterm_fixed.py --ip search --actions configs/midterm_search_seed.json --output build/recheck-search
PYTHONDONTWRITEBYTECODE=1 python3 scripts/screen_midterm_fifo.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/screen_midterm_fifo.py --task cvdp_agentic_async_fifo_compute_ram_application_0004
PYTHONDONTWRITEBYTECODE=1 python3 scripts/screen_external_sfifo.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/analyze_midterm_b_groups.py --run results/midterm_b_development_short_live_20261030
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_midterm_fixture.py' -v
```

Use a fresh `--output` directory for each run. The live B command, once a key
has been hidden-staged, is:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/run_midterm_b_development.py --mode live --output results/midterm_b_development_live_NEW
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/run_midterm_b_development.py --mode live --config configs/midterm_b_development_short.json --output results/midterm_b_development_short_live_NEW
```
