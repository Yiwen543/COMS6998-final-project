# Fixed queue B/C pilot

This experiment compares raw DUT coverage feedback (B) with the same raw
feedback enriched by egg-normalized, complete activation guards (C). It runs
the CVDP queue source and its separately frozen, formally equivalent RTL
variant. Comparisons are **within each version**; the two versions are not
independent design samples. The experiment does not use solver-generated
stimulus or the directed reference sequence in either prompt.

The immutable simulator boundary is the selected RTL file, the CVDP
specification, `verif/tb_queue_pilot.sv`, Verilator coverage options, and the
six-cycle reset/idle seed. The model can return only JSON `actions` with
integer fields `reset_n`, `clear`, `enable`, `write`, `read` (all 0/1), and
`data` (0 through 2^32−1). One action occupies one clock cycle. Invalid
fields, widths, sequence lengths, write-only at full, and read-only at empty
are rejected before simulation. Reset and clear dominate operations; an
inactive enable holds state. Each round starts a fresh simulator process and
replays the seed plus all accepted actions so far.

The scoreboard is an abstract list of valid words and an occupancy count,
independent of queue pointers and implementation registers. It checks front
data only when valid, empty/full, immediate active-low reset, synchronous
clear, and enable hold. The CVDP prose says full uses an internal threshold
but does not specify the formula numerically; this fixed DEPTH=4 contract
defines usable capacity as three words. The prose also does not pin down the
cycle-level almost-empty/full threshold convention. Those two flags are
checked on reset and clear but otherwise reported without a pass/fail
verdict. `verif/queue_spec_control.sv` is a separate behavioral control for
fault-injection tests and never an experimental DUT.

The pilot is frozen at three repetitions per arm and version, four rounds,
four new cycles per round, 4,096 maximum output tokens, the same conservative
input byte cap and model settings, a 90-second request timeout, and at most
two retries. The preregistered target is 41/41 Verilator DUT line/case
counters. A separate directed calibration reaches the target and is excluded
from prompts. The four-cycle cap was set after an arm-blind mock preflight
showed that 16 cycles saturated line/case coverage in round one. Mock results
are plumbing checks, never evidence of LLM benefit.

Both arms receive the same raw uncovered counters, source text, branch
outcome/polarity, and case-selector predicates where uniquely mapped. An
unmapped point remains in the raw list, and C reports the unmapped count. The egg
engine receives typed two-state Boolean guard expressions from the
RTL extractor. Its bounded rewrite rules and independent Z3 checks justify
two source-distinct groups per version: the complete read-only and write-only
activation guards. These groups remain separate. Event context retains
asynchronous reset versus rising-clock operation; no four-state or sequential
equivalence is claimed. All original source counters, including unsupported
or unmapped ones, remain in the raw denominator. C sees only equivalent
forms from its own frozen version, not RTL from the other variant or any
solver witness.

From the repository root, run:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest discover -s tests -p 'test_queue_bc_pilot.py' -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B scripts/run_queue_bc_pilot.py --mode mock --output results/queue_bc_mock
export OPENAI_API_KEY='your key in your local shell'
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B scripts/run_queue_bc_pilot.py --mode live --output results/queue_bc_live
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B scripts/run_queue_bc_pilot.py --mode replay --replay-calls results/queue_bc_live/calls.jsonl --output results/queue_bc_live_replay
```

The `results/queue_bc_live` directory must not already exist, and the shell
must be able to resolve and reach `api.openai.com`. The adapter
reads `OPENAI_API_KEY` only from the environment. Logs contain prompts,
response text, model identifiers, response IDs, API usage (including cached
input and reasoning output subcounts), validation failures, retries, cycle
vectors, raw coverage, compilation/simulation times, CSV round and target
summaries, and plots. API-reported input plus output tokens is the token
total; subcounts are not added again. Token ROI is newly covered DUT branch
points relative to the common seed per 1,000 API tokens. Compilation and
seed simulation are split evenly across B/C repetitions of each version;
egg preprocessing is assigned to C. The separate ceiling run is excluded
from arm costs and shown in setup metadata. Checker failures remain findings
and coverage still flushes.
