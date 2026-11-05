# E-Graph Augmented RTL Verification

COMS 6998 research repository for testing whether equality-graph feedback helps
an LLM generate higher-coverage RTL stimulus at lower cost than raw coverage
feedback. The fixed DUT, specification, checker, driver and coverage accounting
are shared across A (text), B (raw coverage), P (token-matched placebo) and C
(raw coverage plus `egg` semantic groups).

**Current status (4 November 2026):** the initial CVDP arbiter integration,
stateful pilots, source-mapped typed predicate extraction, Z3-checked Boolean
rewrites, and matched live A/B/P/C trials are implemented. The controlled
divider and FIFO stress-variant trials found no repeatable C-over-B gain.
The FIFO stress variant is synthetic and does not establish generalization to
natural IP. The latest exploratory FIFO prompt ablation also tied at target
round 5 in all four arms: lossless B packing saved 7.0% of target-cost tokens,
while the full C appendix cost 21.4% more than B-compact. A fresh relation-only
minimal-C live ablation also tied at round 5 in all twelve sessions: it reduced
C's target token cost by 15.3%, but still cost 2.95% more than B-compact.
Final toggle counts differ; see the [minimal-C result](docs/minimal_c_result_2026-11-03.md)
and [IP diagnosis](docs/ip_selection_diagnosis_2026-11-03.md).

The [fresh WBXBAR B/C trial with the frozen reference checker](docs/wbxbar_reference_bc_2026-11-04.md)
has completed 36 live rounds and both evidence/accounting audits. All six sessions
hit 17/17 targets in round 1 and finish unresolved. C costs 43.34% more tokens to
target and 8.03% more in total, with tied final line/branch counts and a slightly
lower final toggle mean. C briefly leads mean toggle in rounds 2–3; this is retained
without claiming significance or an isolated semantic benefit. The run used 773,454
API tokens, 42 simulations/8,400 cycles and zero retries. Original budgets, roles
and historical results remain unchanged; the staged key was deleted.

The preceding [WBXBAR reference-checker replay](docs/wbxbar_reference_replay_2026-11-04.md)
has a separate registration and freeze. All 42 saved batches reproduce the original
pins and all 2,845 raw DUT counters, also matching the prior cancellation replay;
895 historical files remain hash-identical. The reviewed Claude checker reports
six scoped seed passes and 36 unresolved generated rounds; all six final sessions
remain unresolved. All 59 repeated original alarms have same-cycle/same-slave
post-abort unknown counterparts. More explicit unknown records do not imply more
defects. All 17 targets still occur in round 1, so this adds no C-over-B benefit.
Replay adds 42 executions/8,360 cycles, zero compilation/model calls. The original
budget and role separation remain; no fresh B/C run was launched.

The preceding [WBXBAR conformance follow-up](docs/wbxbar_conformance_gate_2026-11-04.md)
established the scoped checker gate with 58 author selftests, 127+6 control
classifications, 158 evaluated cases and fresh independent code/documentation
reviews. Cancellation timing, excluded forwarding order and other declared
unknowns are not certified. Two nonblocking documentation edge cases remain.

The [WBXBAR cancellation-checker revision](docs/wbxbar_cancel_contract_2026-11-04.md)
now has a separate Claude-authored freeze and audited replay of all 42 saved batches.
Pins and coverage are unchanged; all 18 final alarms have explicit unresolved
post-abort counterparts. The six final sessions remain unresolved, not functional
passes. Original results are preserved; no new stimulus generation was performed.

The user-authorized [exploratory WBXBAR B/C pilot](docs/wbxbar_exploratory_bc_result_2026-11-04.md)
has completed all 36 live rounds. B/C both hit all 17 original targets in round 1;
final line/branch coverage ties at 82/86 and 79/88. C used 43.30% more mean tokens
to the target. Its initial toggle coverage was higher, but final medians tied.
The run used 770,531 tokens, 42 simulations and 8,360 physical cycles, with no
retries. Independent Claude review plus unchanged-checker state tracing localizes
all 18 final routing alarms to non-head aborted-request matching; post-abort
conformance remains unresolved, with no confirmed new DUT defect. This preserves
the old screen rejection and is a known-easy control, without placebo. A separately
reviewed checker is now frozen for retrospective replay; a fresh experiment would
require its own registration. The historical records stay frozen.

The earlier [WBXBAR conditional-domain follow-up](docs/wbxbar_conditional_index_2026-11-04.md)
proves the original state-index range under its actual activation condition,
with base/induction and negative controls. All 109 definition checks pass;
8 mapped seed-zero groups (6 nontrivial) qualify statically. However, isolated
mapped/unmapped reads already hit all 17 member source counters. Forty-four
ordinary cases agree across both simulators; the unchanged ordinary gate rejects
this scope before checker/B/C. Forty-two tests and provenance checks pass; API
cost is zero. This fixes the semantic blocker without demonstrating C benefit.

The preceding [transaction/recovery screen](docs/transaction_recovery_screen_2026-11-04.md)
preregisters original Wishbone firewall/crossbar and an AXIS RAM packet switch.
Source-preserving array/instance/memory adaptations and precise Verilator shared
counter membership pass 13 new checks plus 18 regressions. Firewall has no
eligible groups; RAM switch has two trivial groups. Crossbar was blocked
by an unproved state-index bound at that stage. None qualified for checker/B/C investment;
no API calls were made, and the original budgets and SPI freezes are unchanged.

The prior [SPI failure attribution](docs/spi_failure_attribution_2026-11-04.md)
uses an independent read-only Claude review and dual-simulator single-variable
controls. It supports one probable held-CS configuration-change DUT discrepancy
with cascaded checker diagnostics; reviewer cycle errors are explicitly corrected.
The [new multistep-event screen](docs/multistep_event_screen_2026-11-04.md)
keeps the original budget and roles. AXI FIFO has no eligible static groups;
frame-length adjustment plus FIFOs has six proven groups, all hit by ordinary
single frames. Both are rejected before checker/model investment. No new B/C
run follows, and no positive C-over-B result is inferred. Eighteen focused
checks pass; all previous failures and freezes are retained.

The [SPI_HOST semantic repair and B trial](docs/spi_semantic_repair_2026-11-04.md)
extends the original preflight with typed combinational SSA, independent
Yosys-cell checks and Z3-certified ground rules saturated by egg. Two
nontrivial seed-uncovered groups now qualify, with 186 exact source mappings.
However, all three live B repetitions hit all nine qualified groups in round 1;
the development gate rejects a formal A/B/C/P run. All 94 tests pass. This
repairs an extraction gap without establishing a C-over-B benefit.
The [role-separated event follow-up](docs/spi_role_separated_events_2026-11-04.md)
now freezes a Claude-authored offline checker against GPT-authored calibration
and independent controls (10/12 detected, two explicitly outside scope).
It witnesses backpressure recovery, reset/restart and CSID switching, and
retains a dual-simulator configuration-switch discrepancy. The [I2C follow-up](docs/i2c_role_separated_preflight_2026-11-04.md) certifies
nine nontrivial pairs and freezes a Claude-authored offline write checker with
a GPT/Codex bus driver. Three multistep events are reachable, but none adds a
late-specific equivalent source group over ordinary writing. The offline gate
therefore withholds B; no new B/C performance trial has started.
The [READB extension](docs/i2c_read_preflight_2026-11-04.md) adds the fixed read
driver, separately Claude-authored checker and dual-simulator controls. Three
read event families complete, but all 25 reached equivalent source groups are
already reached by ordinary read/write; B remains disabled. AXI DMA and flash
controller follow-up probes are retained as unqualified candidates, with explicit
expression/mapping and dependency blockers. Checker limitations and the rejected
first version are preserved.
The [natural-IP integration follow-up](docs/natural_ip_integration_2026-11-04.md)
closes the Flash source dependency set and adds statement-position SSA, typed
shifts/slices and independent Yosys checks for both read submodules. It maps
64/68 DMA and 25/29 Flash guards while retaining every original DUT counter.
Neither fixed read configuration supplies a seed-zero dynamic equivalent group;
no checker/model trial follows. Original Flash SV still exceeds Icarus support;
the separately labeled lowered-netlist reset smoke agrees with Verilator.
The [fixed write-scope follow-up](docs/natural_write_scope_preflight_2026-11-04.md)
adds instance-qualified port aliases, complete supported activation guards,
bounded loop expansion and independent memory-read address checks. Original
AXI write / Flash program / Flash arbiter yield 0 / 1 / 0 eligible dynamic
equivalent groups, below the unchanged gate. All 35 relevant checks pass and a
fresh reproduction preserves every raw counter identity and hit. No new checker
or live-model trial has started; the two Flash units count as one IP family.
The [real-parent integration screen](docs/real_parent_screen_2026-11-04.md)
preregisters original AXI DMA, SPI core and AXI-Lite I2C parents. AXI still has
zero qualifying groups; I2C has explicit adapter blockers. SPI core has 20
seed-zero source groups (9 nontrivial), a fixed public-pin JSON driver and
matching Verilator/Icarus calibration traces. Ordinary controls already reach
16 groups; TX/RX recovery shares one stall group. This admits independent
checker construction only, not B; 45 relevant preflight checks pass.
The subsequent [independent SPI core checker audit](docs/spi_core_checker_audit_2026-11-04.md)
completed one Claude author call and one fresh review ($1.580242 total). Four
independent positives pass, but pinned core documentation and actual RTL disagree
on byte order; pending-CSID handling and TX-stall event accounting also block
checker freezing. Post-review causal input and hardware-reset controls pass.
A reviewer underflow claim was contradicted by full raw traces and is explicitly
corrected. Seven new control/packing checks pass; B remains disabled.
The [contract repair follow-up](docs/spi_core_contract_repair_2026-11-04.md)
resolves the byte-order boundary using pinned upstream interface intent and
register-to-core mapping. Claude's second checker fixes byte order and pending
CSID, but independent mode controls and a fresh review still find CPOL idle-edge
and TX-starvation event errors. Missing required events now fail the measurement
gate. Thirty new simulator executions preserve all 3,107 DUT counters; the next
Claude repair packet was then prepared; B/C remained disabled at that stage.
The latest [checker v4 and limited freeze](docs/spi_core_checker_freeze_2026-11-04.md)
repairs CPOL and recovery-event accounting through Claude-only patches and
independent GPT controls. Three multistep event families and 17 reachable source
groups (8 nontrivial) now qualify under the original budget. Full mock/replay
agree exactly, with no live evidence inferred from either. The independent
integrated-core [B trial](docs/spi_core_b_development_2026-11-04.md) completed
18 live calls: two repetitions legally reached all targets in rounds 4/3, but
the third withdrew a pending command. Its raw hits remain in the report; the
all-repetitions-valid gate fails and no C/A/B/P trial follows. Input transport
reliability is now an explicit blocker; no budget was shortened or failure dropped.
Unsupported software-reset/dummy completion, the same-CSID specification
disagreement and limited checker evidence are retained.
The separate [safe-offer driver registration](docs/spi_core_safe_driver_2026-11-04.md)
now holds command/TX valid and payload until public-pin handshakes, with all
waiting charged to the original budget. Thirteen dual-simulator controls,
four actual faulty-SV controls, ten focused tests and full mock/replay pass.
Claude accepted the limited B freeze after two read-only audits ($0.909992).
The fresh [3×6×64 B run](docs/spi_core_safe_b_development_2026-11-04.md) completed
18 calls with no input violations: all three repetitions had only FULLCYC group
51 left after round 1 and hit all targets in round 2. It fails the unchanged
discrimination gate, so C remains disabled. Final checker verdicts are pass/fail/fail;
two extra Icarus replays reproduce the failures without resolving DUT versus
checker/spec attribution. Ordinary calibration covers 16/17 groups, and the
remaining stall group does not establish recovery completion. The old direct-pin
trial is preserved separately. No C benefit is inferred.
Start with [project status and repository map](docs/PROJECT_STATUS.md), the
[November review and next experiment](docs/project_review_2026-11-03.md), and the
[prompt-ablation result](docs/sfifo_prompt_ablation_result_2026-11-03.md).

The starter milestone below uses an immutable CVDP arbiter, a specification-based
SystemVerilog checker, real Verilator coverage, and a small `egg`
predicate-normalization feedback loop.

The first run is deliberately small. Actual uncovered DUT counters are joined to
source-mapped predicates, equivalent predicate forms are normalized by `egg`, and
a deterministic witness generator supplies targeted stimulus for a second run.
An exhaustive run provides a reference ceiling. This initial integration
experiment is hand-authored. Matched model-driven A/B/C pilots now cover the
arbiter, a stateful CVDP FIFO context module, and the CVDP lite timer;
see [FIFO pilot](docs/fifo_pilot.md) and [timer pilot](docs/ttc_pilot.md).

## Quick start

The tools are installed and tested on this Mac. From this directory:

```sh
make doctor
make test
make step1
```

After local runs, `make clean-generated` removes rebuildable compiler output
and plot caches while retaining raw experimental evidence. To preview the
removal list, run `.venv/bin/python scripts/clean_generated.py`. The cleaner
preserves the pinned `build/tools` runtime and private credential staging area.

A fresh macOS environment needs Homebrew and Xcode Command Line Tools:

```sh
brew bundle --file Brewfile
make setup
make test
make step1
```

`make setup` creates `.venv` and builds the locked Rust dependencies. The starter
uses only Python's standard library; live pilots use the packages in
`requirements-pilot.txt`. Cargo uses the configured user cache. Once fetched,
`make step1` builds Cargo offline. The starter needs no API key, Docker,
commercial EDA license, or remote LLM call. On Linux install Python 3.12+,
C++20-capable GCC/Clang,
make, Icarus, Yosys, Rust/Cargo, and Verilator with `--coverage-expr` (tested 5.050).
Older distro Verilator versions may lack that flag or use different counter maps;
the adapter deliberately fails when an expected mapping is missing.

Homebrew formula versions change; Brewfile is a dependency manifest, not a binary
lock. [environment-lock.json](docs/environment-lock.json) records this tested
machine; Cargo.lock locks Rust packages. Exact published results require the
recorded tools and counter definitions. CI validates the Boolean bridge and checker
with Icarus; the full Verilator run is invoked locally with `make step1`.

## Measured starter result

| Test | Checked cycles | Line points | Branch points | Toggle points | Detected defect types |
|---|---:|---:|---:|---:|---|
| Small initial | 4 | 4/11 | 3/18 | 9/60 | none |
| Targeted refinement | 22 | 11/11 | 17/18 | 60/60 | override and reset |
| Exhaustive reference | 65,543 | 11/11 | 17/18 | 60/60 | override and reset |

Three Verilator executions produce these rows. A fourth execution with Icarus
independently reproduces the exhaustive checker counts. Test-suite control runs
are additional validation executions and are excluded from this experiment's
four-execution count. Build time is recorded in logs; per-run wall time measures
simulation process time. `checks` counts sampled rising edges; elapsed simulation
also includes startup/drive scheduling. It is not an API token count.

The sole remaining raw branch is the last override ternary's `else`. It is
unreachable with a nonzero eight-bit override and all lower/last bits zero. It
remains in the denominator: branch coverage is **94.444%, not 100%**. Line coverage
means Verilator's block/elsif counters, not a statement-by-statement percentage.
Toggle points include both directions of the DUT ports, including clock/reset.
Expression counters are also retained in the machine-readable result.

The upstream solution is intentionally unchanged and violates its supplied spec:

- Multi-bit overrides are copied to `grant`, which must be one-hot.
- Reset clears asynchronously; the specification requires synchronous reset.

The refined test reports one functional failure and one timing failure. The
exhaustive test reports 63,232 functional failures and one timing failure. These
are repeated detections of two defect types. Standalone testbench execution exits
nonzero. The coverage runner uses `+COLLECT` to finish collecting counters while
retaining a failing checker status in the report.

## Repository map

```text
examples/arbiter/          Original specification, RTL, upstream TB, provenance/licenses
  verif/tb_fixed_priority_arbiter.sv   Independent generated checker/stimulus
prompts/step1.md           Reusable initial generation prompt
scripts/predicates.py     Hash-guarded arbiter adapter and Boolean witness search
scripts/coverage.py       DUT-only coverage parser and source-preserving join
scripts/run_step1.py      Compile, initial/refined/exhaustive runs, Icarus, Yosys
scripts/sim_main.cpp      Timed Verilator runner with explicit coverage flush
egraph/                   Real Rust egg engine; Cargo.toml and Cargo.lock
tests/                    Predicate truth tables, graph/schema and checker controls
docs/                     Reading review, workflow, tool/dataset records
results/step1/            Raw counters, feedback, E-graph, logs, report, assembled prompt
build/, .cache/, .venv/    Ignored local intermediate/runtime files
third_party/              Ignored pinned CVDP checkout used during setup
project_background_reading/  Existing local papers/proposal; not republished
```

Start with [the report](results/step1/REPORT.md), [verification plan](examples/arbiter/verification_plan.md),
[workflow](docs/workflow.md), and [reading review](docs/readings.md).
`make prompt` assembles the three concrete inputs and reusable prompt into
`results/step1/initial-prompt.md`. `results/step1/feedback.json` contains uncovered
source counters, normalized roots, guards, and concrete suggested inputs.

The [26 October milestone report draft](docs/milestone_2026-10-26.md) compares
the saved A/B/C pilots, explains the current C-versus-B ceiling, and includes a
primary-source literature matrix. The [Claude Code cross-check protocol](docs/claude_queue_crosscheck.md)
specifies a blinded first-pass audit and independent replay checks.

## Standalone testbench

```sh
iverilog -g2012 -s tb_fixed_priority_arbiter -o build/arbiter.vvp \
  examples/arbiter/rtl/fixed_priority_arbiter.sv \
  examples/arbiter/verif/tb_fixed_priority_arbiter.sv
vvp build/arbiter.vvp
```

Default mode is exhaustive and requires no external stimulus file. Expected:
`RESULT checks=65543 functional_errors=63232 timing_errors=1`, followed by a fatal
specification-violation status. `+MODE=0` runs the four-cycle initial test.
`+MODE=1 +VECTORS=<path>` is an optional feedback-run mode.

## Scope and provenance

The fixture is `cvdp_agentic_fixed_arbiter_0001`, **cid003 code generation**, from
the pinned [official GitHub example](https://github.com/NVlabs/cvdp_benchmark/tree/8e894cf74414ab1eaea1e2b4e80a02f123df07b6/example_dataset).
Its spec and reconstructed solution are hash-recorded in `examples/arbiter/provenance.json`.
The public [Hugging Face dataset](https://huggingface.co/datasets/nvidia/cvdp-benchmark-dataset)
was also inspected at a pinned revision: it has the same RTL in the different
`cvdp_agentic_fixed_arbiter_0010` enhancement task, not the starter's original spec.
See `docs/dataset-lock.json`; do not silently substitute those tasks.
`python3 scripts/fetch_dataset.py` optionally retrieves that hash-verified public
file into ignored `build/`; the checked-in starter runs without it.

CVDP does not provide an E-graph for this example. `egg` is an equality-saturation
library, not a SystemVerilog parser. Our adapter supports this pinned priority
chain and pure two-state Boolean predicates only. Yosys successfully lowers the
RTL and emits a JSON netlist for the next frontend stage; that netlist is not yet
the source of the predicate adapter. E-graph output includes actual E-classes and
E-nodes; 16 distinct winning predicates each have two equivalent forms. Reset
event semantics remain metadata, outside Boolean rewriting.

No Pass@1, model superiority, token saving, or general RTL support is claimed.
The matched A/B/C pilots have been executed; see the [arbiter report](results/pilot_live_20261020/REPORT.md),
[FIFO report](results/fifo_live_20261020/REPORT.md), and
[timer report](results/ttc_live_20261020/REPORT.md). The timer provides a harder,
stateful coverage challenge but shows no repeatable C-over-B gain; its final
toggle plateau includes 32 structurally constant output-bit directions. A
faithful follow-up needs typed predicate extraction, repeated equivalent
predicates, and equivalence-checked RTL variants. The first restricted Yosys
pre-`proc` typed-guard frontend and a
source-verified held-out CVDP queue variant pair are available in the
[queue preflight report](docs/heldout_queue_preflight.md). A matched live B/C
pilot on that pair is in the [queue report](results/queue_bc_live_20261021_unsandboxed/REPORT.md).
The requested GPT-6 Sol rerun and Claude Code Opus 5.5 cross-review are in the
[Milestone 1 result report](docs/milestone1_result_report.md) and the
[two-page P1-style PDF](output/pdf/milestone1.pdf). Its 48 live model calls and
48 independent replayed rounds are separately archived under
[`results/queue_bc_gpt6sol_20261026/`](results/queue_bc_gpt6sol_20261026/).
See [the evaluation
contract](docs/workflow.md) and the [paper-to-pilot reproduction
audit](docs/egraph_reproduction_audit.md).

Background papers and the proposal are grouped in `project_background_reading/`.
NVIDIA example code is Apache-2.0 and its specification is CC BY 4.0;
attribution and license are preserved in `examples/arbiter/`. New project code
is MIT licensed.
