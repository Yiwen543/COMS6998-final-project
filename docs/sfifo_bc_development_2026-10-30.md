# ZipCPU sfifo: fixed checker and matched B/C development trial

Date: 30 October 2026. This is a **development screen**, not a held-out
multi-repetition effectiveness result.

## Frozen boundary and independent checker

The original public-domain ZipCPU `sfifo.v` is copied without changes to
[`examples/heldout_sfifo/rtl/sfifo.v`](../examples/heldout_sfifo/rtl/sfifo.v),
from `wb2axip` commit `2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b`.
Its SHA-256 is `76a653781f1ecca1c1da92c4e5105ecd5d0f832b13cbfd31300ec88d9947e0c1`.
The [separately written contract](../examples/heldout_sfifo/docs/specification.md)
fixes 8-bit words, depth 8, asynchronous front read, and rejects writes on
full and reads on empty. It defines simultaneous operations by pre-edge
acceptance. Reset is synchronous; read/write during reset is outside this
contract. Empty output data is unspecified and never checked.

The [JSON schema and checker](../scripts/sfifo_fixture.py) use only public
pre-edge and post-edge signals. The [fixed driver](../examples/heldout_sfifo/verif/tb_sfifo_fixed.sv)
contains no expected values. The first stimulus action resets the FIFO.
Action validation rejects unknown fields, booleans, out-of-range values,
reset with read/write, and overlong batches. Original RTL passes the directed
queue scenario under both Verilator and Icarus. An independently written
[behavioral reference RTL](../tests/rtl/sfifo_reference.sv) passes, while its
single data-order and asynchronous-reset mutants fail the checker. This validates the checker on the
specified interface; it is not a full formal proof of the DUT.

## Semantic evidence and feedback isolation

The earlier [preflight](../results/midterm_candidate_preflight/external-sfifo/screen.json)
found two typed, complete, source-distinct binary guards: pop-only at lines
90/156 and push-only at lines 91/157. Each pair shares an egg e-class and
passes an independent Z3 pair check; the two cases remain **different**
e-classes. Both pairs were untouched by the common reset/idle seed and
reached by separate calibration stimulus. Three extracted cases lack source
mappings and are reported as unsupported. The calibration stimulus and
formal witnesses are absent from model prompts.

Both arms receive the same specification, original RTL, seed, action schema,
checker findings, execution trace, and original uncovered line/branch/expr
counters. C additionally receives the [egg-derived group evidence](../scripts/sfifo_feedback.py),
including atoms, bounded-saturation e-class nodes, full activation guards,
source locations, and original per-location hits. It makes only a two-state
combinational equivalence claim. The driver, DUT, checker, simulator options,
coverage denominator, feedback selection policy, and model settings are
identical across arms. Every round replays seed plus all accepted actions;
the full batch finishes before new feedback is rendered. There is one
independent, stateless Responses session per arm. No solver stimulus or
deterministic search is used.

## Live development outcome

The requested and returned model were both `gpt-6.1-sol`, with low reasoning,
8,192 maximum output tokens, a 90-second timeout, and at most one retry. Each
arm ran four rounds with at most eight new cycles per round. All eight model
responses were accepted on the first try. The common seed was four cycles.
The raw DUT denominator remained 18 line, 14 branch, 12 expression, and 204
toggle directions. Functional checker failures: zero in both arms.

| Arm | Round | Line | Branch | Toggle | Equivalent groups | API tokens cumulative | Executed cycles cumulative |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B | 1 | 18/18 | 12/14 | 77/204 | 2/2 | 6,457 | 16 |
| B | 2 | 18/18 | 12/14 | 109/204 | 2/2 | 12,608 | 36 |
| B | 3 | 18/18 | 12/14 | 120/204 | 2/2 | 19,023 | 64 |
| B | 4 | 18/18 | 12/14 | 134/204 | 2/2 | 25,798 | 100 |
| C | 1 | 18/18 | 12/14 | 79/204 | 2/2 | 7,621 | 16 |
| C | 2 | 18/18 | 12/14 | 115/204 | 2/2 | 14,323 | 36 |
| C | 3 | 18/18 | 12/14 | 126/204 | 2/2 | 21,281 | 64 |
| C | 4 | 18/18 | 12/14 | 146/204 | 2/2 | 28,659 | 100 |

Each arm compiled once and executed five complete simulations, including the
seed. Final B compilation/simulation/model/wall times were 2.73/0.17/14.39/
17.66 seconds; C times were 2.53/0.21/14.94/18.01 seconds, with 0.30 seconds
of C egg preprocessing included in wall time. Each arm newly covered three
branch points over the nine-point seed baseline by round 1. The first-round
Token ROI, defined as new DUT branch points per 1,000 API-reported input plus
output tokens, was 0.465 for B and 0.394 for C. Both arms reached 12/14
branches and 18/18 lines in round 1. A target of all 14 branch points was
**not reached** in either arm; the two zeros remain in the raw denominator
without an unreachability claim. C's final toggle count was 12 directions
higher, while using 2,861 more API tokens. One stochastic repetition per arm
cannot establish that egg caused that difference.

The [per-call JSONL](../results/sfifo_bc_development_live_20261030/calls.jsonl),
[per-round JSONL](../results/sfifo_bc_development_live_20261030/rounds.jsonl),
[CSV](../results/sfifo_bc_development_live_20261030/comparison.csv),
[source-location group progress](../results/sfifo_bc_development_live_20261030/group-progress.json),
and [plot](../results/sfifo_bc_development_live_20261030/comparison.png)
retain the underlying evidence. Mock output is stored only under `build/`
and is excluded from this result. The hidden staged key was deleted by the
runner after the live calls.

## Interpretation and next gate

Both equivalent groups are triggered by ordinary write/read traffic and B
reaches them in its first batch. This FIFO therefore tests the plumbing and
checker, but does not give C time to exploit semantic redundancy. Keep this
negative development result. Before a held-out A/B/C/placebo experiment,
select a deeper FIFO/controller with multiple source-distinct equivalent
uncovered guards that survive an independent B development screen, then
freeze the target and budget. Retain this design as a functional and prompt
isolation control. The original CVDP async FIFO candidates did not pass the
seed-uncovered guard gate in the current extractor; this does not prove they
have no other semantic redundancy.

## Reproduce

```sh
.venv/bin/python -B scripts/run_sfifo_fixed.py --simulator verilator --output build/recheck-sfifo-verilator
.venv/bin/python -B scripts/run_sfifo_fixed.py --simulator iverilog --output build/recheck-sfifo-icarus
.venv/bin/python -B -m unittest discover -s tests -p 'test_sfifo_*.py' -v
.venv/bin/python -B scripts/run_sfifo_bc_development.py --mode mock --output build/recheck-sfifo-bc-mock
.venv/bin/python -B scripts/analyze_sfifo_bc_development.py --run results/sfifo_bc_development_live_20261030
```

For a new live development run, first hide-stage the key with
`scripts/stage_midterm_openai_key.py`, then use a fresh output directory:

```sh
.venv/bin/python -B scripts/run_sfifo_bc_development.py --mode live --output results/sfifo_bc_development_live_NEW
```
