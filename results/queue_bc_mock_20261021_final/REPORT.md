# Held-out CVDP queue matched B/C pilot

Mode: **mock**.

Two independently frozen RTL versions of one IP are compared within-version. B gets every raw uncovered DUT counter; C gets the identical raw array plus egg/Z3-verified full-guard groups. No witness input or calibration sequence enters prompts.

Preregistered line target: 41/41. Three repetitions, four rounds, at most 4 new cycles per round. Each run replays all accepted actions after the same six-cycle reset/idle seed; all replay cycles and simulator executions are counted.

| Version | Arm | Rep | Final line | Branch | Toggle | Distinct defects | API tokens | Cycles | Calls | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| original | B | 1 | 32/41 | 12/14 | 297/408 | 0 | N/A | 64 | 4 | not reached |
| original | B | 2 | 33/41 | 14/14 | 275/408 | 0 | N/A | 64 | 4 | not reached |
| original | B | 3 | 41/41 | 14/14 | 300/408 | 0 | N/A | 64 | 4 | reached |
| original | C | 1 | 32/41 | 12/14 | 297/408 | 0 | N/A | 64 | 4 | not reached |
| original | C | 2 | 33/41 | 14/14 | 275/408 | 0 | N/A | 64 | 4 | not reached |
| original | C | 3 | 41/41 | 14/14 | 300/408 | 0 | N/A | 64 | 4 | reached |
| variant | B | 1 | 32/41 | 12/14 | 297/408 | 0 | N/A | 64 | 4 | not reached |
| variant | B | 2 | 33/41 | 14/14 | 275/408 | 0 | N/A | 64 | 4 | not reached |
| variant | B | 3 | 41/41 | 14/14 | 300/408 | 0 | N/A | 64 | 4 | reached |
| variant | C | 1 | 32/41 | 12/14 | 297/408 | 0 | N/A | 64 | 4 | not reached |
| variant | C | 2 | 33/41 | 14/14 | 275/408 | 0 | N/A | 64 | 4 | not reached |
| variant | C | 3 | 41/41 | 14/14 | 300/408 | 0 | N/A | 64 | 4 | reached |

| Version | B final line mean (range) | C final line mean (range) | B reached target | C reached target | C − B mean line |
|---|---:|---:|---:|---:|---:|
| original | 35.33 (32–41) | 35.33 (32–41) | 1/3 | 1/3 | +0.00 |
| variant | 35.33 (32–41) | 35.33 (32–41) | 1/3 | 1/3 | +0.00 |

| Version | Arm | Mean tokens to line target | Mean branch ROI / 1k tokens | Mean cycles | Mean simulations | Mean wall seconds |
|---|---|---:|---:|---:|---:|---:|
| original | B | N/A | N/A | 24 | 2 | 0.71 |
| original | C | N/A | N/A | 24 | 2 | 0.79 |
| variant | B | N/A | N/A | 24 | 2 | 0.64 |
| variant | C | N/A | N/A | 24 | 2 | 0.72 |

This run is an infrastructure smoke test, **not an LLM outcome**.

The checker asserts valid front data, empty/full, asynchronous reset, synchronous clear, and enable hold against a separate occupancy model. The CVDP prose does not pin down almost-empty/full timing thresholds; those flags are checked on reset/clear and otherwise observed without functional verdict.

Coverage means the number of Verilator Coverage-3 DUT counters with hits > 0: line includes case/block/elsif source points; branch has separate if/else outcomes; expression has reported Boolean outcomes; toggle has separate bit 0→1/1→0 transitions. Testbench counters are excluded. A shared egg class does not transfer a hit between source lines. Expression denominators differ across the two RTL versions, so compare B with C only within the same version. Token ROI is newly covered branch points per 1,000 API-reported input-plus-output tokens; mock mode has no API token ROI.

The typed extraction and egg rewrites cover binary/two-state combinational activation guards only. Each version has 49 extracted targets and 18 unsupported expressions; their records remain in typed-predicates.json. Event context remains separate; every unmapped raw coverage point stays in the prompt and denominator. The common reset/idle seed is replayed in each simulation and counted in executed cycles. The directed ceiling is a separate calibration outside model prompts and arm costs.

All source hashes, tool/model settings, simulator commands, common seed, separate calibration ceiling, per-call logs, saved prompts, raw coverage files, round JSONL/CSV, target costs, and comparison plots are adjacent to this report.
