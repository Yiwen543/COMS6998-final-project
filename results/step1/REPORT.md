# Step 1 measured integration result

| Test | Checked cycles | Functional failures | Timing failures | Line points | Branch points | Toggle points |
|---|---:|---:|---:|---|---|---|
| initial | 4 | 0 | 0 | 4/11 | 3/18 | 9/60 |
| refined | 22 | 1 | 1 | 11/11 | 17/18 | 60/60 |
| exhaustive | 65543 | 63232 | 1 | 11/11 | 17/18 | 60/60 |

Each row is one Verilator execution. The refined row includes the four starting cycles.
Icarus independently reproduces the exhaustive checker counts (one additional execution).
Failures detect the unchanged upstream DUT defects; they do not indicate a passing DUT.
All percentages and raw uncovered points are in summary.json. No unreachable points are removed.
This is a deterministic integration demonstration; token ROI and model comparisons remain unmeasured.
