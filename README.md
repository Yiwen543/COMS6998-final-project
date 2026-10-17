# VS Code EDA and stimulus agent

Open COMS6998-final-project.code-workspace in VS Code.
Use Terminal → Run Task to check tools, run the EDA feedback experiment,
preview agent requests, or start a one-call model smoke test.
The build shortcut runs the EDA experiment. See docs/vscode_cn.md.

## Stimulus-agent implementation

This local checkout adds a bounded LLM stimulus loop on the upstream arbiter.
Start with [the Chinese agent guide](docs/agent_quickstart_cn.md).
The upstream commit and copy scope are recorded in SOURCE_SNAPSHOT.json.
The implementation preserves the upstream DUT and adds reviewed multi-module adapters.

Offline checks (no API key or EDA tools):

```sh
python3 -m unittest discover -s tests -p test_agent.py -v
python3 scripts/run_agent.py --dry-run --group C --output results/agent-preview/new-C
```

The original milestone documentation follows.

# E-Graph Augmented RTL Verification

Reproducible first milestone for the COMS 6998 proposal: an immutable CVDP arbiter,
a specification-based SystemVerilog checker, real Verilator coverage, and a small
`egg` predicate-normalization feedback loop.

The first run is deliberately small. Actual uncovered DUT counters are joined to
source-mapped predicates, equivalent predicate forms are normalized by `egg`, and
a deterministic witness generator supplies targeted stimulus for a second run.
An exhaustive run provides a reference ceiling. This integration experiment is
hand-authored; the model-driven A/B/C evaluation is future work.

## Quick start

The tools are installed and tested on this Mac. From this directory:

```sh
make doctor
make test
make step1
```

A fresh macOS environment needs Homebrew and Xcode Command Line Tools:

```sh
brew bundle --file Brewfile
make setup
make test
make step1
```

`make setup` creates `.venv` and builds the locked Rust dependencies. Python uses
only its standard library. Cargo caches stay in `.cache/cargo`. Once fetched,
`make step1` builds Cargo offline. No API key, Docker, commercial EDA license, or
remote LLM call is needed. On Linux install Python 3.12+, C++20-capable GCC/Clang,
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
The next research milestone replaces deterministic witness refinement with matched
A/B/C agent runs, then adds a stateful FIFO and wider frontend support. See
[the evaluation contract](docs/workflow.md).

Original papers remain where supplied and are ignored by Git. NVIDIA example
code is Apache-2.0 and its specification is CC BY 4.0; attribution and license
are preserved in `examples/arbiter/`. New project code is MIT licensed.

### CVDP multi-module validation

Three additional pinned, immutable CVDP context RTLs are supported: barrel shifter,
Caesar cipher, and universal shift register. Run VS Code task **7. 运行 CVDP 多模块 EDA 对照**
or `make cvdp`. Tasks 8/9 preview or run the bounded Agent on a selected module.
See [CVDP integration instructions](docs/cvdp_modules_cn.md) and
[measured EDA report](results/cvdp-suite-20261017/REPORT.md).
These are real local EDA validations with deterministic C/D witness controls;
no live LLM benefit or official CVDP-ECov score is claimed.
