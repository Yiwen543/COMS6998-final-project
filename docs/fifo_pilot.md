# Stateful CVDP FIFO pilot

The fixture is the exact `rtl/sync_fifo.sv` context file from public CVDP record
`cvdp_agentic_low_power_channel_0001`, dataset revision
`5b807d945f6a99aa645f7e43a64a2115e281b4bf`. The record's task is a
low-power-channel integration, so it **does not contain a standalone FIFO
specification**. We authored the frozen, interface-level FIFO contract in
[`examples/fifo/docs/specification.md`](../examples/fifo/docs/specification.md).
The exact source and record hashes are in
[`examples/fifo/provenance.json`](../examples/fifo/provenance.json). The original
RTL remains unchanged. The source is from the official
[CVDP dataset](https://huggingface.co/datasets/nvidia/cvdp-benchmark-dataset/tree/main),
whose [NOTICE](https://huggingface.co/datasets/nvidia/cvdp-benchmark-dataset/blob/main/NOTICE)
identifies code licensing.

The experiment fixes an 8-entry, 8-bit FIFO, active-high asynchronous reset,
and the independent queue checker. Stimulus is validated JSON cycle actions
(`reset`, `push`, `pop`, `data`). Underflow and overflow are excluded by the
contract; simultaneous push and pop is allowed when nonempty, including when
full. A fixed testbench applies actions on falling edges and checks status and
valid head data before and after each rising edge. Fault-injected status and
data variants establish that the checker rejects these defect classes.

The same instrumented Verilator binary, checker, specification, four-cycle
seed, simulator settings, and DUT denominator are used for A, B, and C. A sees
the spec/RTL/seed, occupancy and checker log. B also sees every uncovered raw
DUT counter with source and outcome. C sees exactly B's raw evidence plus five
hash-guarded egg predicate mappings. At the seed, only the simultaneous-operation
case and full-pointer expression remain uncovered among those five. All 186
unmapped uncovered counters stay in the denominator and raw feedback. Egg
normalization covers only two-state, one-bit Boolean abstractions; pointer
comparisons are guarded atomic inputs. It does not rewrite FIFO state,
asynchronous reset, memory, or four-state behavior.

Run from the repository root after installing `requirements-pilot.txt`,
Verilator 5.050, Icarus, Yosys, and Rust/Cargo. Cargo builds offline using the
locked dependency graph. The default configuration is
[`configs/fifo_pilot.json`](../configs/fifo_pilot.json): three independent
repetitions per arm, four rounds, at most 32 new cycles per round, up to two
validation retries, the same `gpt-6.1-sol` model settings, and a preregistered
200/220 toggle-direction target. Never put a key in a command line, config, or
repository file; the runner reads `OPENAI_API_KEY` from the environment.

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_*pilot.py' -v
.venv/bin/python scripts/run_fifo_pilot.py --mode mock --output results/fifo_mock_new
.venv/bin/python scripts/run_fifo_pilot.py --mode live --output results/fifo_live_new
.venv/bin/python scripts/run_fifo_pilot.py --mode replay \
  --replay-calls results/fifo_live_new/calls.jsonl \
  --output results/fifo_replay_new
```

For standalone checker use, the fixed driver also runs in Icarus:

```sh
iverilog -g2012 -s tb_sync_fifo -o build/fifo.vvp \
  examples/fifo/rtl/sync_fifo.sv examples/fifo/verif/tb_sync_fifo.sv
vvp build/fifo.vvp +MODE=0
```

The completed live [report](../results/fifo_live_20261020/REPORT.md),
[round CSV](../results/fifo_live_20261020/rounds.csv),
[target-cost CSV](../results/fifo_live_20261020/target_costs.csv), and
[plot](../results/fifo_live_20261020/comparison.png) preserve the actual
outcome. All 36 accepted batches replayed with identical counters and checker
results. A separate 306-cycle directed plus seeded-random reference run reached
220/220 toggles and all nine functional bins; its actions never enter model
prompts. The common seed already covers 4/4 branch counters, so branch coverage
cannot discriminate arms on this IP. The primary outcome is therefore raw
Verilator toggle-direction counters; line, expression, branch and functional
bins remain secondary. Toggle ROI counts newly covered toggle directions per
1,000 API-reported input-plus-output tokens.

At the 200/220 target, A needed two simulator runs and 104 executed cycles in
every repetition; B and C each needed one run and 36 cycles. B and C both hit
220/220 toggles in round one in every repetition. C used 444–607 more API
tokens than B at the target, with no coverage or simulator-count advantage.
One C response in a later round failed action-length validation and was retried;
the rejected call is included in full-run API cost. No FIFO checker failures
were observed. The tiny pilot supports a raw-coverage benefit in cycles and
simulator executions, while **it does not show an E-graph benefit over raw
coverage**. API latency varied across calls, so observed wall-time differences
are descriptive. A stronger next fixture needs nested or repeated equivalent
predicates with equivalence-checked RTL variants, alongside richer FIFO control
and state conditions.
