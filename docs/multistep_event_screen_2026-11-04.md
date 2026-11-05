# Prospective multistep-event screening — 4 November 2026

Two original integrated IP configurations were registered before elaboration,
proof, calibration or model outcomes. Neither qualifies for a new B trial:
AXI FIFO has no admitted dynamic equivalent group; the frame length adjuster
has six, but ordinary single frames already hit every group. No new B/C call
was made. This result is a task-selection finding, not evidence that C cannot
help on a qualified task.

## Registration and unchanged budget

`configs/multistep_event_screen_v1.json` SHA-256:
`938e253408d0560f6b6049e6e50461bee3cd367e1f7a2be82c831b4997cd2216`.
The original development budget remains **3 repetitions × 6 rounds × at most
64 new physical cycles**, with an eight-cycle seed. Model limits remain
`gpt-6.1-sol`, low effort, 32,000 input / 16,384 output tokens, 120 seconds,
one retry. No fresh model result was consulted to change these settings.

The unchanged B gate requires at least two repetitions to leave two groups
unfinished after round 1, and at least two to make later group progress;
all repetitions must complete with legal input. A qualifying B development
run would precede a separately frozen, fresh matched comparison. It is not
itself reused as the formal B arm.

The **new**, separately registered offline task criterion requires at least
three source-distinct groups, two nontrivial groups and three distinct
multistep event families. Each target group needs at least two seed-zero
original source counters. Ordinary input traces must leave every selected
counter unhit. Clean multistep completion, an unhit prerequisite/resolution
prefix and a same-budget control removing that prerequisite or resolution
must discriminate the target. The same shared stall/reset/ready group cannot
stand in for multiple event families. Each calibration is bounded by 384
new physical cycles. Finite controls do not prove universal unreachability.

Checker authorship remains Claude/specification-only; GPT/Codex owns driver,
stimulus and measurement. An independent reviewer may inspect RTL for
diagnosis. Checker code cannot be changed by the stimulus model. Calibration
inputs never enter model prompts. C must still wait for the independent B gate.

## Original public IPs and scope

| Configuration | Pinned revision | Parameters / intended events |
|---|---|---|
| `verilog-axis/axis_frame_length_adjust_fifo` | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` | 8-bit data, KEEP disabled, data FIFO 32, header FIFO 8; padding, truncate/drain/next-frame, independent header/data pressure |
| `verilog-axi/axi_fifo` | `516bd5dadc3365b7f9e225d2af8fe0b8d804fe53` | data 32, address 16, ID 4, read/write FIFO 16, both delay features enabled; buffered write release, long bursts, read-capacity return |

Original parents and children are unchanged. Both use a posedge clock and
synchronous active-high reset. Source SHA-256 and Git blobs are verified
against pinned revisions, with README and license provenance. These are
functionally different IPs with nonoverlapping RTL, but share the upstream
author/ecosystem; the AXIS parent reuses a previously explored FIFO dependency.
They are not two statistically independent or unseen design lineages.

Public descriptions: [AXIS pinned README](https://github.com/alexforencich/verilog-axis/blob/48ff7a7e2ef782cf778d47910cf85835c64b1bce/README.md),
[AXI pinned README](https://github.com/alexforencich/verilog-axi/blob/516bd5dadc3365b7f9e225d2af8fe0b8d804fe53/README.md).
Both repositories now direct new development to Taxi. Pinned legacy sources
are used here for reproducibility, without claiming they are current releases.

## Semantic extraction and independent evidence

The new adapter is in `scripts/event_scope_semantics.py`; no prior frozen
adapter was edited. The initial frame candidate exposed two real adapter gaps:
the old assignment collector misclassified range indices/width parameters as
written storage, and static-loop evaluation lacked literal/relational cases.
The adapter now identifies actual lvalue bases, preserves ordered blocking
SSA, bounds unrolling to 64 iterations, and evaluates supported constants
with elaborated widths and signedness. It rejects loops that really modify
their induction variable or exceed the bound. Slang-proven parameter branches
are pruned only from the proof view with provenance; source counters stay in
the original denominator. Runtime predicates are not assumed constant.

| Evidence | Frame adjuster, v6 | AXI FIFO, v2 |
|---|---:|---:|
| Frontends (Slang / Verilator / Icarus / Yosys) | all pass | all pass |
| Independent combinational definition checks, UNSAT | 146 | 182 |
| Independent pmux one-hot checks, UNSAT | 19 | 9 |
| Extracted raw targets / typed supported | 154 / 150 | 83 / 83 |
| Exact mapped targets / unresolved mappings | 144 / 6 | 78 / 5 |
| Different-expression Z3-certified ground rules | 264 | 32 |
| `egg` iterations / saturation seconds | 10 / 0.3484 | 3 / 0.0027 |
| Seed-zero dynamic candidate groups / nontrivial | 6 / 6 | 0 / 0 |
| Original raw DUT counters | 3,060 | 2,903 |

`egg` performed bounded equality saturation, including six validated Boolean
rules and independently QF_BV-proven ground rules; it exported rewrite
explanations. This is not AST-string normalization or an LLM semantic summary.
Guard satisfiability is checked separately from equivalence. Original file,
line, column, polarity and instance remain attached to each coverage location.
One counter covering multiple elaborated loop iterations is aggregated only
according to its actual simulator identity, never invented as extra counters.

Proof scope is two-state combinational semantics with free FF/memory-read
cuts. It does not prove sequential behavior, reachability, four-state
equivalence or the entire checker. Definition comparison uses a separate
Yosys-cell encoding but shares the Slang frontend; common frontend errors
remain a limitation. Unsupported constructs and mappings remain explicit;
none are admitted as targets or removed from raw denominators.

The frame denominator is 110 line + 178 branch + 250 expression + 2,522 toggle
counters. AXI FIFO is 67 + 74 + 68 + 2,694 respectively. These are Verilator
counter categories, not a count of physical source lines or semantic events.
Reset/initialization is included consistently; testbench counters are excluded.

## Ordinary-operation negative filter

Before spending on a checker, `scripts/probe_frame_ordinary.py` supplies a
bounded JSON offer interface and fixed SV queue driver. A pending byte and
payload remain stable until pre-edge valid/ready; all waiting costs physical
cycles. Widths, legal fields, seed and maximum length are checked. A separate
Python queue oracle verifies actual input delivery without deriving expected
DUT outputs from RTL. There is no implicit drain or hidden clock progress.

The six ordinary cases send one frame of 1, 2, 4, 8, 16 or 20 bytes, with
limits fixed at min=4/max=16, no imposed input gaps, and both output ready
signals always high. They exercise normal short/padded, unchanged and
truncated frames, with no deliberate recovery scenario. All input offers are
delivered exactly once. Verilator/Icarus agree on meaningful public signals.
Icarus X values on invalid output payloads and pre-reset uninitialized outputs
are retained in raw traces and excluded from comparison; valid payloads and
post-reset control signals cannot be unknown.

Every one of the six candidate groups is hit by ordinary frames:

| E-class (local ID) | Distinct source locations | Example ordinary length | Separate raw counts |
|---:|---|---:|---|
| 55 | adjuster 327 if / 333 else | 2 | 8 / 8 |
| 53 | adjuster 327 else / 333 if | 16 | 11 / 11 |
| 380 | adjuster 354 if / 355 if | 2 | 5 / 5 |
| 74 | adjuster 409 if / 421 else | 1 | 16 / 16 |
| 75 | adjuster 409 else / 421 if | 1 | 8 / 8 |
| 129 | FIFO 266 if / 311 if | 1 | 4 / 4 |

These raw increment values are **not cycle counts or transaction counts**.
All 3,060 identities match the seed inventory. Unmapped or noncandidate
members of an e-class are not silently promoted into target source members.

The result is `eligible_event_groups=[]` and `reject_before_checker`. This is
a conservative **negative-only** screen: it demonstrates that the proposed
source targets are not exclusive to deliberately constructed multistep events
under these inputs. It does not certify output correctness, prove events
unreachable or claim a valid independent checker. Positive qualification would
still require Claude's checker and causal controls. With zero remaining
targets, none of that work or a new API request is justified for this scope.

## Failures, cost and checks retained

All attempts are under `results/multistep_event_screen_20261104/`:

- Frame static v1: missing legacy `proof_keep` default; v2: incorrect lvalue
  collection; v3/v4: unsupported static-loop expressions left unsafe free
  combinational values, so independent proof correctly blocked admission.
  v5 passed after adapter repairs. v6 revalidated the final adapter including
  negative signed loop bounds; both report the same six candidate groups.
  AXI v2 revalidated the final shared runner/empty-overlay metadata and agrees
  with AXI v1's zero eligible groups.
- The old helper copied an unrelated SPI dependency-overlay metadata file
  in early attempts, but the new configuration did not load that overlay.
  v5/v6 explicitly record an empty overlay tied to the new scope.
- Ordinary v1: Icarus EOF parsing was incorrectly treated as a malformed
  vector; idle invalid payload X handling was also corrected. Two executions
  reached 114 cycles. v2: both simulators completed another 114 cycles, but
  result assembly tried to index an explicitly unresolved group member.
  It stopped without admitting a target. v3 explicitly selects only qualified
  mapped members and completes all six cases. Final seed auditing found that
  its disabled KEEP input was 1 during the seed whereas static inventory used
  0. v4 matches all seed inputs exactly, then sets KEEP to 1 for ordinary data;
  all target counts and the rejection decision are unchanged. A regression
  assertion now compares every seed input to the static registration.
- Final ordinary v4: **2 compilations, 12 simulations, 774 actual cycles**;
  compile subprocess time 10.158 s, simulation subprocess time 0.404 s.
  Including failed and superseded ordinary attempts: **8 compilations,
  28 simulations, 1,776 cycles**. v1 lacks a complete timing manifest; its missing timings
  are not counted as zero.
- Static inventories are separate: four builds/runs across AXI v1/v2 and
  frame v5/v6, 32 seed cycles. Syntax/elaboration/proof commands and time
  are saved per stage, separate from model-trial simulation cost.
- Eight new tests pass: signed/static loops, induction-write and bound
  rejection, parameter versus runtime guards, mutated bit-order proof
  rejection, input/schema and trace corruption, budget/source preservation,
  negative-gate interpretation and review-packet isolation. All ten existing
  safe-driver/accounting tests also pass. Unit fixtures are not model trials.
- New screen API calls: **zero**. The separate
  [SPI failure attribution](spi_failure_attribution_2026-11-04.md) used one
  Claude call and is accounted there. No new B/C data or positive C claim.

Tool versions: Python 3.13.9, Verilator 5.050, Icarus 12.0, Slang
12.1.0+42710c788, Yosys 0.70+309, Z3 5.1.0, Cargo 1.99.0. Scope, source,
script and proof hashes are saved with results. Base repository commit:
`50d7ee83d61989017e28e981420cd58f4c5f0787`; working-tree changes are not
represented as a new commit.

## Reproduction and subsequent decision

Use fresh output directories; no key is needed:

```sh
.venv/bin/python scripts/screen_multistep_events.py --adapter constant_view --top axis_frame_length_adjust_fifo --output build/frame-screen-repro
.venv/bin/python scripts/screen_multistep_events.py --top axi_fifo --output build/axi-fifo-screen-repro
.venv/bin/python scripts/probe_frame_ordinary.py --base build/frame-screen-repro --output build/frame-ordinary-repro
.venv/bin/python -m unittest discover -s tests -p test_multistep_event_screen.py -v
.venv/bin/python -m unittest discover -s tests -p 'test_spi_core_safe_*.py' -v
```

Do not narrow B feedback, shorten the budget or use C results to rescue either
configuration. The lesson is that duplicated combinational logic, multi-module
size and reachable multistep behavior are insufficient: the **selected raw
source targets** must also distinguish the multistep behavior from normal
transactions. The next prospectively registered candidate should prioritize
packet ownership/arbitration, abort/retry or state-dependent resource return
with public contracts. Apply this inexpensive ordinary negative filter before
checker authoring, then require the independent checker and matched causal
controls for positive admission. If natural source coverage still cannot
distinguish those events, register temporal functional coverage as a separate
research extension rather than redefining the old B/C target after observing
results. It would test a different intervention and cannot replace this
project's original raw-coverage comparison.
