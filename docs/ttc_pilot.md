# CVDP lite timer pilot and strategy revision

The fixture is the exact `ttc_counter_lite.sv` RTL and companion specification
from the NVIDIA CVDP `cvdp_agentic_ttc_lite_0007` hard record at dataset revision
`5b807d945f6a99aa645f7e43a64a2115e281b4bf`. The raw record, RTL, and
specification hashes are in [`examples/ttc_timer/provenance.json`](../examples/ttc_timer/provenance.json).
The original RTL is preserved. Unlike the previous CVDP FIFO context fixture,
this record supplies a timer-specific natural-language specification.

The experiment holds the original DUT, specification, checker, five-cycle seed,
simulation settings, coverage counter denominator, and model settings fixed.
Only validated JSON cycle actions vary: `reset`, `write`, `read`, `addr`, `data`.
The fixed driver samples them before rising edges. The checker models the
specified 16-bit count, divide-by-(prescaler+1), match/reload, registered reads,
and interrupt. It checks synchronous reset before the next rising edge. Reads
and writes in the same action, and bus access during reset, are excluded.
Counter/interrupt timing choices not fully specified in prose are disclosed in
the [report](../results/ttc_live_20261020/REPORT.md). A temporary Icarus control
with only the reset sensitivity changed passes the same directed sequence,
whereas the pinned original reports two timing failures; the corrected control
is not the experimental DUT.

This is an improved feedback challenge over the FIFO: the seed covers only
25/266 timer toggle-direction counters, 11/14 branch counters, and 12/23 line
counters. The independent directed calibration sequence covers 206/266 toggles;
its actions are not exposed to the model. The 180/266 coverage target was
registered in [`configs/ttc_pilot.json`](../configs/ttc_pilot.json) before live
calls. Three independent repetitions per arm, four refinement rounds, at most
16 new cycles per round, two validation retries, and identical `gpt-6.1-sol`
settings were used. Each round replays all prior generated actions after the
five-cycle seed. Cycle totals count those replays; one complete batch is
simulated per accepted round. The simulator flushes coverage on checker failure.

The proposal's workflow maps directly to this pilot: the model generates
stimulus from the specification and RTL; Verilator supplies line, branch,
expression, and bit-direction toggle counters; B receives uncovered raw points;
C receives the same points plus egg-normalized, source-mapped predicate guards;
the model refines stimulus for the next round. The primary C-versus-B comparison
isolates the added semantic feedback, and A-versus-B tests raw coverage feedback.
The fixed checker prevents model-edited verification logic from confounding the
result. This is a stimulus-generation proxy for the proposal's broader
testbench-generation and Pass@1 goals; it does not measure Pass@1 of generated
SystemVerilog testbenches.

The semantic bridge currently handles eight **manually source-mapped** Boolean
guards. It runs actual bounded egg equality saturation, merges each equivalent
De Morgan/double-negation form, and records the resulting E-classes and E-nodes.
The read-status and write-status paths share a typed address guard but are not
merged as full expressions. Four-bit address comparisons and the 16-bit
count-match comparison are atomic Boolean inputs. Clock/reset events, state
transitions, arithmetic, four-state semantics, and most toggle points are
outside the proven normalization. Yosys lowering succeeds, but the timer
predicate extraction is not yet automatically generated from the Yosys netlist.
The mapped expressions represent local Boolean subguards; some enclosing
enable/prescaler and priority conditions are visible in the raw RTL but are not
normalized as part of those egg roots. Thus C is not a full semantic model of
timer branch reachability, and the next frontend must carry each complete
activation context explicitly.
All unsupported coverage points stay in B and C raw feedback and the unmodified
denominator.

The completed live [report](../results/ttc_live_20261020/REPORT.md),
[per-round CSV](../results/ttc_live_20261020/rounds.csv),
[target-cost CSV](../results/ttc_live_20261020/target_costs.csv), and
[plot](../results/ttc_live_20261020/comparison.png) contain the comparison.
The saved live responses were replayed offline: all 36 accepted rounds reproduced
their exact DUT counter arrays and checker outcomes.
B and C both finish at 234/266 toggles in every repetition. All remaining
32 toggle-direction points are the upper 16 bits of `axi_rdata`, which every
read path and reset drive to zero in this two-state RTL. C's first-round
C-minus-B differences were +5, -1, and -23; it used more API tokens at the
180-point target in every repetition, with identical one-call/one-execution/
21-cycle cost there. This pilot does not support an E-graph advantage. B reaches
the target in the first round in all repetitions; A needs two or three rounds,
but A uses substantially fewer API tokens because it lacks the long raw-counter
prompt. The comparison is descriptive, not statistically significant.

To make the next test more discriminating while staying on the proposal's
workflow, first automate RTL-to-predicate translation and prove source/width/
guard mappings with equivalence-checked RTL variants that have nested or
repeated Boolean predicates. Then use those variants for matched B/C runs with
a target below saturation and report both coverage and token/simulator cost.
The timer's remaining uncovered points should not be used as a target for an
LLM or egg, because they are structurally constant. A later CVDP FIFO controller
with full/empty, simultaneous operations, pointer wrap, and reset during
operation can extend the stateful evaluation; the existing simple FIFO context
is too easy for branch coverage.

Run from the repository root after installing `requirements-pilot.txt` and
Verilator, Icarus, Yosys, Rust/Cargo. Keep the API key in the environment, not
in files or command arguments. Output directories must be new:

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/run_ttc_pilot.py --mode mock --output results/ttc_mock_new
.venv/bin/python scripts/run_ttc_pilot.py --mode live --output results/ttc_live_new
.venv/bin/python scripts/run_ttc_pilot.py --mode replay \
  --replay-calls results/ttc_live_new/calls.jsonl \
  --output results/ttc_replay_new
```

Standalone Icarus checker:

```sh
iverilog -g2012 -s tb_ttc_counter_lite -o build/ttc.vvp \
  examples/ttc_timer/rtl/ttc_counter_lite.sv \
  examples/ttc_timer/verif/tb_ttc_counter_lite.sv
vvp build/ttc.vvp +MODE=0
```
