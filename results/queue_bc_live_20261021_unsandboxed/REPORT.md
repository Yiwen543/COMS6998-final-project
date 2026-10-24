# Held-out CVDP queue matched B/C pilot

Mode: **live**.

Two independently frozen RTL versions of one IP are compared within-version. B gets every raw uncovered DUT counter; C gets the identical raw array plus egg/Z3-verified full-guard groups. No witness input or calibration sequence enters prompts.

Preregistered line target: 41/41. Three repetitions, four rounds, at most 4 new cycles per round. Each run replays all accepted actions after the same six-cycle reset/idle seed; all replay cycles and simulator executions are counted.

| Version | Arm | Rep | Final line | Branch | Toggle | Distinct defects | API tokens | Cycles | Calls | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| original | B | 1 | 41/41 | 14/14 | 344/408 | 0 | 82746 | 64 | 4 | reached |
| original | B | 2 | 41/41 | 14/14 | 344/408 | 0 | 82903 | 64 | 4 | reached |
| original | B | 3 | 41/41 | 14/14 | 344/408 | 0 | 82783 | 64 | 4 | reached |
| original | C | 1 | 41/41 | 14/14 | 344/408 | 0 | 84644 | 64 | 4 | reached |
| original | C | 2 | 41/41 | 14/14 | 344/408 | 0 | 84419 | 64 | 4 | reached |
| original | C | 3 | 41/41 | 14/14 | 344/408 | 0 | 84435 | 64 | 4 | reached |
| variant | B | 1 | 41/41 | 14/14 | 344/408 | 0 | 84489 | 64 | 4 | reached |
| variant | B | 2 | 41/41 | 14/14 | 344/408 | 0 | 84697 | 64 | 4 | reached |
| variant | B | 3 | 41/41 | 14/14 | 344/408 | 0 | 84564 | 64 | 4 | reached |
| variant | C | 1 | 41/41 | 14/14 | 344/408 | 0 | 86360 | 64 | 4 | reached |
| variant | C | 2 | 41/41 | 14/14 | 344/408 | 0 | 86479 | 64 | 4 | reached |
| variant | C | 3 | 41/41 | 14/14 | 344/408 | 0 | 86376 | 64 | 4 | reached |

| Version | B final line mean (range) | C final line mean (range) | B reached target | C reached target | C − B mean line |
|---|---:|---:|---:|---:|---:|
| original | 41.00 (41–41) | 41.00 (41–41) | 3/3 | 3/3 | +0.00 |
| variant | 41.00 (41–41) | 41.00 (41–41) | 3/3 | 3/3 | +0.00 |

| Version | Arm | Mean tokens to line target | Mean branch ROI / 1k tokens | Mean cycles | Mean simulations | Mean wall seconds |
|---|---|---:|---:|---:|---:|---:|
| original | B | 73283 | 0.1092 | 42 | 3 | 12.80 |
| original | C | 74902 | 0.1068 | 42 | 3 | 13.45 |
| variant | B | 74966 | 0.1067 | 42 | 3 | 12.67 |
| variant | C | 76721 | 0.1043 | 42 | 3 | 13.20 |

Across 24 paired rounds, C had more toggle points in 2, fewer in 1, and the same count in 21.

Paired B/C action batches were identical in 14/24 round pairs; differing stimulus did not necessarily change measured coverage.

C did not improve line-target attainment: all paired runs reached the target in the same round. C used 1687 more API tokens on average to reach it (paired range 1457–1823). Wall time varied by run. This is a descriptive pilot result, not a statistical-significance claim.

Individual repetitions are descriptive; the pilot is too small for statistical significance.

The checker asserts valid front data, empty/full, asynchronous reset, synchronous clear, and enable hold against a separate occupancy model. The CVDP prose does not pin down almost-empty/full timing thresholds; those flags are checked on reset/clear and otherwise observed without functional verdict.

Coverage means the number of Verilator Coverage-3 DUT counters with hits > 0: line includes case/block/elsif source points; branch has separate if/else outcomes; expression has reported Boolean outcomes; toggle has separate bit 0→1/1→0 transitions. Testbench counters are excluded. A shared egg class does not transfer a hit between source lines. Expression denominators differ across the two RTL versions, so compare B with C only within the same version. Token ROI is newly covered branch points per 1,000 API-reported input-plus-output tokens; mock mode has no API token ROI.

The typed extraction and egg rewrites cover binary/two-state combinational activation guards only. Each version has 49 extracted targets and 18 unsupported expressions; their records remain in typed-predicates.json. Event context remains separate; every unmapped raw coverage point stays in the prompt and denominator. The common reset/idle seed is replayed in each simulation and counted in executed cycles. The directed ceiling is a separate calibration outside model prompts and arm costs.

All source hashes, tool/model settings, simulator commands, common seed, separate calibration ceiling, per-call logs, saved prompts, raw coverage files, round JSONL/CSV, target costs, and comparison plots are adjacent to this report.
