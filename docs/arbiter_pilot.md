# Matched arbiter pilot

The experimental question is whether egg-normalized coverage feedback improves model-generated stimulus under the same cycle, call, and output-token limits. A is text/checker feedback only; B adds raw uncovered Verilator DUT points; C adds egg normalization of the 16 mapped priority winner predicates to the identical B payload. The primary comparison is C versus B. The A/B comparison tests whether raw coverage helps at all.

The frozen fixture is the CVDP fixed-priority arbiter in `examples/arbiter`. The specification requires one-hot override grants and active-high **synchronous** reset. The original DUT still assigns the whole override mask and triggers its sequential block on `posedge reset`. The checker uses a least-set-bit arithmetic oracle from the specification and checks output stability between edges. `tests/test_semantics.py` independently tests the checker with a conforming control and each isolated defect. A detected checker failure therefore remains a DUT finding; `+COLLECT` merely lets coverage flush after the finding.

The baseline's exact Icarus cross-check is `iverilog -g2012 -s tb_fixed_priority_arbiter -o build/arbiter.vvp examples/arbiter/rtl/fixed_priority_arbiter.sv examples/arbiter/verif/tb_fixed_priority_arbiter.sv` followed by `vvp build/arbiter.vvp +MODE=2 +COLLECT`. The Verilator compile uses `--cc --exe --build --timing --assert --coverage-line --coverage-toggle --coverage-expr --top-module tb_fixed_priority_arbiter` with the same DUT/checker and `scripts/sim_main.cpp`; the complete argument list is in `scripts/run_pilot.py` and its compile log. A pilot simulation passes `+MODE=1 +COLLECT +VECTORS=<validated file> +verilator+coverage+file+<raw .dat>`. The Yosys frontend pass uses `read_verilog -sv; hierarchy -check -top fixed_priority_arbiter; proc; check; write_json`. Tool versions and the frozen DUT/specification/checker SHA-256 values are recorded in each run's `metadata.json`.

The fixed driver is `tb_fixed_priority_arbiter.sv`: four common initial cycles, then validated `reset`, `req`, and `priority_override` integer actions. Inputs are driven on the falling edge and checked after the rising edge. Actions have widths 1, 8, and 8 bits. The Python validator rejects booleans, missing/extra fields, out-of-range values, empty actions, and overlong batches. The model never edits the driver, checker, RTL, or measurement code. Each round starts a fresh Verilator process and replays the four initial cycles plus every accepted action to date. Thus round 4 with four 32-cycle responses executes 132 cycles; the four processes together execute 336 cycles per repetition. Compilation and egg preprocessing are shared setup measurements; C's plot wall time includes one-third of egg preprocessing per repetition. Both the common initial run and exhaustive ceiling are outside the A/B/C simulator-execution and cycle totals.

`scripts/run_step1.py` previously demonstrated 4/11 line, 3/18 branch and 9/60 toggle coverage from the initial test, reaching 11/11, 17/18 and 60/60 with handcrafted/enum-targeted inputs. Its `predicates.witness()` enumeration is **not** used by this pilot. The old exhaustive test is a separate reference ceiling and is never given to the model. The raw 18-branch denominator retains the last ternary else outcome even though the binary guard makes it unreachable. No zero-hit location is waived. Verilator line points are block/elsif counters, not source statement counts; branch points include ternary outcomes; toggle points count individual bit directions. Expression counters are also recorded. Only `TOP.tb_fixed_priority_arbiter.dut` counters are accepted by the parser; checker and testbench counters are excluded. Initialization and reset activity are included consistently.

Yosys `read_verilog -sv; hierarchy; proc; check; write_json` verifies extraction, but the RTL-to-expression bridge is a pinned-source, SHA-guarded Python adapter rather than a general Yosys JSON translator. The Rust engine actually runs egg 0.11.0 equality saturation over unsigned one-bit Boolean terms. It applies De Morgan, double negation, and identity rewrites with 20-iteration, 20,000-node, five-second limits. The compact and expanded expression for each priority winner merge into one E-class, while 16 different winners remain separate. The class IDs, representatives, constituent nodes, rule names and source mappings are exported. Only binary/two-state combinational predicates are normalized. Four-state equivalence, timing, clock, reset, and state-transition equivalence are outside this claim. Every mapped counter retains its own raw hits; C also lists all unmapped uncovered points.

## Reproduce

From the nested repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-pilot.txt
cargo fetch --locked --manifest-path egraph/Cargo.toml
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/run_pilot.py --mode mock --output results/pilot_mock_new
```

For a live run, set `OPENAI_API_KEY` in the shell environment without putting it in a file in this repository, then run:

```sh
.venv/bin/python scripts/run_pilot.py --mode live --output results/pilot_live_new
```

The requested model defaults to `gpt-6.1-sol`; the runner rejects a different returned model rather than silently accepting it. It uses the official OpenAI Python SDK Responses API with `store=False`, low reasoning effort, strict JSON schema, a 4,096-token response cap, a conservative 64,000-byte prompt cap, 90-second timeout, and at most two retries. `max_input_tokens_conservative_byte_cap` is a local UTF-8 byte bound, **not** an API-reported token measurement. API input and output usage are the measured tokens. Cached input and reasoning output are subsets shown separately and never added to the total again. The token ROI is `1000 × (covered branch points − common-initial covered branch points) / cumulative API input-plus-output tokens`.

Replay a completed call log through a fresh compiled simulator, without another API call:

```sh
.venv/bin/python scripts/run_pilot.py --mode replay --replay-calls results/pilot_live_new/calls.jsonl --output results/pilot_replay_new
```

`configs/arbiter_pilot.json` preregisters three repetitions per arm, four rounds per repetition, 32 new actions per round, and a target of 17/18 raw branch points. Each arm/repetition is a new stateless model session. Identical initial conditions do not make model responses deterministic. The mock generator is deliberately arm-blind and its tokens are null; its matched results prove only that the accounting and feedback partitions work. A tiny pilot cannot establish statistical significance. If C and B tie or neither reaches target, the next experiment should use nested/repeated equivalent predicates and equivalence-checked RTL variants, followed by a FIFO with full/empty, simultaneous read/write, pointer wraparound and reset-during-operation cases.

Outputs include `metadata.json` (commit, hashes, tool versions, settings and shared costs), `calls.jsonl` (per attempt/request/response), `rounds.jsonl` and `rounds.csv`, `target_costs.csv` (first cost at the preregistered target or an explicit `not reached`), fully rendered `prompt-*.json`, `*.vectors`, simulator logs, raw `.dat` counters, `egg-evidence.json`, `yosys-netlist.json`, `reference-ceiling.json`, `comparison.png`, and `REPORT.md`. The logs contain model inputs/outputs and DUT data but never the API credential.

## Live pilot observed on 2026-10-20

`results/pilot_live_20261020/` contains the full 3 × 3 × 4 live run: 36 accepted `gpt-6.1-sol` Responses API calls, zero invalid responses/retries, 36 experimental simulator executions, and 2,275 executed cycles including replays. The independent simulator run in `results/pilot_live_replay_20261020/` reproduced all 36 checker outcomes and every raw DUT counter exactly without new API calls. The common initial run was 3/18 branch points, and the fresh exhaustive ceiling was 17/18.

Every arm and repetition reached the preregistered 17/18 target in the first round and ended at 11/11 line and 60/60 toggle points. At first target, A used 2,576 API tokens and 36 cycles in each repetition; B used 8,893 tokens and 36 cycles; C used 15,774/15,761/15,761 tokens and 31/30/30 cycles. All required one simulator execution. C therefore saved 5–6 executed cycles relative to B, but consumed 6,881/6,868/6,868 more input-plus-output tokens and achieved no additional coverage or reduction in simulator executions. Token ROI at first target was 1.574 newly covered branch points per 1,000 tokens for B versus about 0.888 for C. A was cheaper than both, showing that this small arbiter saturates before raw coverage guidance becomes useful. Wall times differed across independent model calls and provide no reliable causal conclusion from three repetitions.

The checker observed 642 functional and 216 timing failure events across all 36 replayed simulator executions. These are repeated observations of **two** distinct DUT defect types: multi-bit override grants and asynchronous reset. The pilot does not establish statistical significance or generalize beyond the pinned arbiter. Its next discriminating test should be the nested/repeated equivalent-predicate RTL variants, then the FIFO scenarios described above.
