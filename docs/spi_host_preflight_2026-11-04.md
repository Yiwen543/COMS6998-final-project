# SPI_HOST controller preflight — 4 November 2026

**Historical v1 screen.** A separately preserved
[semantic repair and B development follow-up](spi_semantic_repair_2026-11-04.md)
subsequently proves two nontrivial groups, but all three B repetitions hit the
qualified targets in round 1. The original observations below remain unchanged;
the follow-up still rejects proceeding to a formal A/B/C/P comparison.

**Decision: do not start live B or A/B/C/placebo.** The new adapter, fixed JSON
driver, scoped specification checker and calibration work. However, the
supported original RTL contains **zero qualifying nontrivial rewrite groups**.
The already-written [next-IP gate](next_ip_screen_2026-11-03.md#next-go-no-go-procedure)
requires at least two before another model call. No API key was read and no
OpenAI or Anthropic request was made for this preflight. This is a candidate
screening result, not a new B-versus-C result.

## Fixed boundary and implementation

1. **Pin the source and public specification.** This is the original lowRISC
   OpenTitan `spi_host_fsm`, revision
   `0ea5236fe749e70ba18f56ba19c4be982ef46da7`, `NumCS=2`. DUT SHA-256 is
   `5324b93183a0475c5e955b76a7b1e9c1c9739e810a70d213491c5657837ee47c`.
   The reference text is the pinned upstream `theory_of_operation.md` and
   `registers.md`. The [local contract](../examples/heldout_spi_host/contract.md)
   is explicitly a scoped interpretation, not an upstream-written spec. The
   controller boundary excludes the bus/register interface, command FIFO and
   serial payload datapath. Original RTL was not edited; fault controls use
   separately named disposable copies.
2. **Preserve typed source predicates.** `slang_guard_adapter.py` consumes the
   elaborated Slang AST, retaining source spans, widths, signedness, all nested
   conditions, earlier case-arm exclusions and procedural edge context.
   `unique case` does not justify removing priority guards. Vector operations
   remain typed opaque atoms. Four-state comparisons and unsupported syntax
   fail closed. A predicate reading a variable assigned with blocking assignment
   in the same procedure requires SSA and is not promoted.
3. **Keep temporal context outside egg.** The adapter distinguishes
   combinational logic, `posedge clk_i`, and `negedge rst_ni`. Independently,
   all 26 Slang/Yosys `$aldff` cells have their positive clock and negative
   asynchronous reset connections checked. The child serial-clock flop needs
   two explicit, width-preserving `$buf` aliases; their evidence is saved.
   General child-instance and generate-block guard extraction remains
   unsupported (two entries). This is not complete hierarchy support.
4. **Normalize and prove only supported relations.** The existing Rust
   `egg 0.11.0` engine runs six Boolean rules with 20 iterations, 20,000 nodes
   and a five-second bound. Z3 proves each rule and checks merged guards by
   Boolean XOR unsatisfiability. This proves Boolean identities over typed
   opaque atoms; it does not prove arithmetic or sequential equivalence.
   The control fixture merges `a && b` and `!(!a || !b)` under the same full
   guard, while keeping different reset contexts and case values separate.
5. **Join original counters exactly.** All 109 supported targets map to
   Verilator counters by original file, line, column, type and true-path
   polarity. The adapter accounts for AST member/operator/colon token positions
   and Verilator's `line/elsif` versus `branch/if` representation. There is no
   line-only fallback. Each original location retains its own hit count; shared
   E-classes never transfer coverage. Unsupported hierarchy is still represented
   in the raw top-file denominator.
6. **Use a fixed cycle driver and public-pin scoreboard.** Nineteen JSON fields
   carry reset, enable, valid, command fields and TX/RX readiness. Every field,
   width and legal speed/direction combination is checked. Inputs change while
   the clock is low, with public outputs sampled before and after the rising
   edge; this observes asynchronous reset before the edge. The scoreboard uses
   accepted command lengths, byte/last counts, selected serial edge counts,
   serial polarity/minimum half-period, reset and stall/pause properties. It
   never reads internal DUT states or extracted guards. A batch executes fully
   before checker analysis, so DUT failures cannot prevent coverage flushing.

## Observed qualification result

| Stage | Result |
|---|---:|
| Supported typed targets | 109 |
| Exact original-counter mappings | 109 / 109 |
| Source-distinct same-context semantic groups | 10 |
| Groups with at least two seed-zero, calibrated source counters | 7 |
| Qualifying groups requiring egg rewriting to merge different expressions | **0** |
| Static gate | **Rejected: requires ≥2 nontrivial groups** |
| Live B repetitions / A/B/C/P repetitions | **0 / 0** |

The seven seed-zero groups contain respectively 13, 13, 6, 2, 6, 4 and 2 source
counters. They concern command selection/capture, software reset, valid command,
stall, paused FSM and new-command counter loading. Several describe related
parts of the same event; seven groups should not be read as seven independent
hard temporal tasks. Their input predicates are already identical before egg.

The raw denominator is fixed at **57 line, 160 branch, 246 expression and
836 toggle points** (1,299 total). These are Verilator Coverage-3 meanings,
not physical source-line counts or transaction coverage. Initialization/reset
activity is included; testbench and separate `prim_flop_en` source counters are
excluded. Generated CSB scopes originating in the top file remain included.

| Raw DUT points | Shared 8-cycle seed | Union of separate calibration runs |
|---|---:|---:|
| Line | 23 / 57 | 53 / 57 |
| Branch | 79 / 160 | 160 / 160 |
| Expression | 107 / 246 | 245 / 246 |
| Toggle | 22 / 836 | 494 / 836 |

Calibration comprises 34 sequences plus the seed, totaling 5,725 cycles per
simulator. It exercises standard/dual/quad, all CPOL/CPHA combinations, read,
write and legal bidirectional transfers, dummy clocks, clock division, CS hold,
full-cycle selection, pause/stall, software abort and asynchronous abort.
The longest sequence is 204 cycles, within the proposed 384-cycle development
budget. **All 35 complete public traces agree between Verilator and Icarus**,
and all pass the scoped checker. Calibration sequences are excluded from model
prompt construction. Their coverage union is not a model-run result, a single
384-cycle schedule, or proof of all reachable behavior.

## Checker validation and limitations

A hand-authored legal public trace, independent of DUT simulation, passes the
scoreboard. Mutated public traces test reset, chip-select, last-flag, missing
edges, unexpected transfers, stall suppression and illegal command handshakes.
Three separately compiled single-fault RTL controls are detected:

| Injected defect | Repeated checker failures | Distinct observed categories |
|---|---:|---|
| Force last-write flag low | 1 | segment-last flag |
| Invert serial-clock output | 4 | asynchronous reset; serial idle polarity |
| Remove write suppression during stall | 30 | stall control; readiness; unexpected byte; segment-last flag |

These are **three injected defects**, not 35 defects. One injected defect can
produce multiple symptoms. All three complete their batches and produce raw
coverage files. The original DUT stays unchanged.

The checker does not establish serial payload correctness, exact sample/shift
phase, exact CS lead/trail/idle delays, or liveness. Incomplete end-of-budget
transactions are reported, not treated as a proof or automatically called a
DUT bug. Overlapping CSID/configuration switches are explicitly outside the
initial checker scope; protocol/scope violations are distinct from DUT defects.
No independent human/Claude review or formal proof of this new checker has
occurred. Those remain prerequisites to a stronger correctness claim.

## Runner and accounting checks

`run_spi_host_b_development.py` reuses the official Responses adapter, saves
rendered B-only prompts, validates actions, preserves request/retry/token
records and replays cumulative stimulus from the same seed. Live mode checks
static qualification and frozen artifact hashes **before reading credentials
or creating an API client**. The saved live-guard check refuses this candidate.
Mock mode is explicitly unable to qualify a candidate.

The retained mock smoke test has two refinement rounds, three simulator
executions and 48 executed cycles (8 + 16 + 24); API calls are zero and token
usage is null. Mock idle actions are not a B development result. The proposed
live limits are three repetitions, six rounds, up to 64 new cycles/round,
`gpt-6.1-sol` with low reasoning, 32k input-token cap, 16,384 output tokens,
120-second timeout and one retry. No formal A/B/C/P target/budget was frozen.

Retained SPI validation evidence comprises 35 Verilator calibration runs, 35
Icarus cross-checks, three mutant runs and three final mock runs: 76 executions,
12,070 cycles, all offline. Earlier developmental checks added one 204-cycle
stall replay, two earlier 48-cycle mock runs, and one 184-cycle Icarus probe; these are
validation overhead, never pooled with a model pilot. Whole-repository tests
also execute their own separate controls.

The initial full repository test run exposed a historical queue smoke-test
freeze mismatch: the engine had previously gained timing telemetry after that
live experiment was frozen. The mock test now pins the current engine only in
its temporary configuration; a new test verifies that the historical freeze
still rejects engine drift. Historical live configuration/results were not
changed. The initial failure and subsequent test logs are retained.
The final `make test` run passes all **87 tests**. The final guarded mock also
archives the exact input configuration and screen so later preflight updates
cannot erase its selection provenance.

Versions: Verilator 5.050, Icarus 12.0, Slang 12.1.0+42710c788, isolated Yosys
0.70+309 (`bd3168b1a`), Z3 5.1.0, egg 0.11.0, OpenAI Python SDK 2.54.0.
Repository base commit is `c71a3e580646d08fb6496c742b7b42b711179b36`; the
new work is uncommitted. Artifact hashes, versions, source mappings, proof
evidence and all counts are under
[`results/spi_host_preflight_20261104`](../results/spi_host_preflight_20261104/).
This execution measured approximately 0.05 seconds for Slang, 0.20 seconds
for egg saturation and 0.002 seconds for extraction/JSON construction. It does
not identify extraction optimization as a performance bottleneck.

## Reproduction and next decision

Run from the repository root, with the pinned source checkout and installed
toolchain. Use new output directories for fresh evidence:

```sh
.venv/bin/python scripts/calibrate_spi_host.py --output build/spi-cal-new
.venv/bin/python scripts/calibrate_spi_host.py --simulator iverilog --output build/spi-icarus-new
.venv/bin/python scripts/preflight_spi_host.py --calibration build/spi-cal-new --output build/spi-screen-new
.venv/bin/python scripts/validate_spi_host_checker.py --output build/spi-controls-new
.venv/bin/python scripts/run_spi_host_b_development.py --mode mock --output build/spi-mock-new
make test
```

The following live command intentionally stops at the current static gate:

```sh
.venv/bin/python scripts/run_spi_host_b_development.py --mode live --output build/spi-live-gate-new
```

Do not lower the gate just to produce a C win. This boundary is useful as a
controller/clock/reset/checker regression. For the next generalization candidate,
first inspect deeper transaction/rollback/backpressure predicates or extend
typed combinational aliases and child-module guard support with independent
proofs. Re-screen source-distinct *different* expressions before paying for B.
A larger IP alone does not create such relationships. Once a candidate passes
static/checker/reachability gates, run the prewritten independent B progress
gate, then freeze and run A/B/C and token-matched placebo without selecting on
C outcomes.

## Repository cleanup

Removed the superseded one-off offline-preview script, 18 regenerated preview
prompt copies and the verified 501 MiB installation archive. Kept the original
source prompts, preview summary, live experiments, renderer/tests, installed
toolchain and its provenance. Also removed 59 generated/cache paths; initial
cleanup reclaimed 594,945,216 bytes (0.554 GiB). The cleaner now preserves
`build/tools`, `build/private`, saved evidence and the built egg engine rather
than deleting `build/` wholesale. A final cache pass after tests is separately
logged. Useful dated methodology/negative-result Markdown remains: deleting it
would remove the selection rationale. Exact removals and hashes are recorded in
[`results/repository_cleanup_20261104`](../results/repository_cleanup_20261104/).
