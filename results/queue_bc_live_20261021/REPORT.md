# Held-out CVDP queue matched B/C pilot

Mode: **live**.

Two independently frozen RTL versions of one IP are compared within-version. B gets every raw uncovered DUT counter; C gets the identical raw array plus egg/Z3-verified full-guard groups. No witness input or calibration sequence enters prompts.

Preregistered line target: 41/41. Three repetitions, four rounds, at most 4 new cycles per round. Each run replays all accepted actions after the same six-cycle reset/idle seed; all replay cycles and simulator executions are counted.

| Version | Arm | Rep | Final line | Branch | Toggle | Distinct defects | API tokens | Cycles | Calls | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|

| Version | B final line mean (range) | C final line mean (range) | B reached target | C reached target | C − B mean line |
|---|---:|---:|---:|---:|---:|
| original | N/A | N/A | 0/3 | 0/3 | N/A |
| variant | N/A | N/A | 0/3 | 0/3 | N/A |

| Version | Arm | Mean tokens to line target | Mean cycles | Mean simulations | Mean wall seconds |
|---|---|---:|---:|---:|---:|
| original | B | not reached | not reached | not reached | not reached |
| original | C | not reached | not reached | not reached | not reached |
| variant | B | not reached | not reached | not reached | not reached |
| variant | C | not reached | not reached | not reached | not reached |

No valid model responses were accepted, so no DUT stimulus round ran and B/C coverage cannot be compared.

Individual repetitions are descriptive; the pilot is too small for statistical significance.

The checker asserts valid front data, empty/full, asynchronous reset, synchronous clear, and enable hold against a separate occupancy model. The CVDP prose does not pin down almost-empty/full timing thresholds; those flags are checked on reset/clear and otherwise observed without functional verdict.

Coverage means the number of Verilator Coverage-3 DUT counters with hits > 0: line includes case/block/elsif source points; branch has separate if/else outcomes; expression has reported Boolean outcomes; toggle has separate bit 0→1/1→0 transitions. Testbench counters are excluded. A shared egg class does not transfer a hit between source lines. Expression denominators differ across the two RTL versions, so compare B with C only within the same version. Token ROI is newly covered branch points per 1,000 API-reported input-plus-output tokens; mock mode has no API token ROI.

The typed extraction and egg rewrites cover binary/two-state combinational activation guards only. Each version has 49 extracted targets and 18 unsupported expressions; their records remain in typed-predicates.json. Event context remains separate; every unmapped raw coverage point stays in the prompt and denominator. The common reset/idle seed is replayed in each simulation and counted in executed cycles. The directed ceiling is a separate calibration outside model prompts and arm costs.

All source hashes, tool/model settings, simulator commands, common seed, separate calibration ceiling, per-call logs, saved prompts, raw coverage files, round JSONL/CSV, target costs, and comparison plots are adjacent to this report.

Diagnostic only: the sandbox could not resolve api.openai.com. All 144 attempted SDK calls ended in APIConnectionError before any model response or token usage. This aborted run is excluded from the matched B/C comparison.
