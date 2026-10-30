# E-Graph Augmented RTL Verification

COMS 6998 research repository for testing whether equality-graph feedback helps
an LLM generate higher-coverage RTL stimulus at lower cost than raw coverage
feedback. The fixed DUT, specification, checker, driver and coverage accounting
are shared across A (text), B (raw coverage), P (token-matched placebo) and C
(raw coverage plus `egg` semantic groups).

**Current status (30 October 2026):** the initial CVDP arbiter integration,
stateful pilots, source-mapped typed predicate extraction, Z3-checked Boolean
rewrites, and matched live A/B/P/C trials are implemented. The controlled
divider and FIFO stress-variant trials found no repeatable C-over-B gain.
The FIFO stress variant is synthetic and does not establish generalization to
natural IP. Start with [project status and repository map](docs/PROJECT_STATUS.md),
then the [divider](docs/divider_abcp_result_2026-10-30.md) and
[FIFO](docs/sfifo_stress_abpc_result_2026-10-30.md) reports.

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
removal list, run `.venv/bin/python scripts/clean_generated.py`.

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
