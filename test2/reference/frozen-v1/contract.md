# Reference checker contract

- Model: specification queue (depth 16, 8-bit) driven only by actions and expected occupancy; DUT flags never decide acceptance.
- Row 0 must have reset=1; its pre phase is ignored, its post is checked (empty queue).
- Every later pre and post is checked: fill, full, empty, and data when expected nonempty. Empty data is unspecified.
- Reset is synchronous: pre of a reset cycle reflects the previous queue; post is empty.
- Acceptance decided from pre-edge expected occupancy: rd if n>0, wr if n<16; simultaneous ops both accepted when 0<n<16; at full only read, at empty only write.
- INVALID_INPUT: non-list/empty input, extra/missing fields, non-integer or out-of-range values (inputs may not be -1), reset with wr/rd, first action not reset, missing/out-of-order cycles (must be consecutive from first). Processing stops.
- Observed -1 on a checked field is recorded as unresolved. Verdict: FAIL if any failure (dominates unknown), else UNRESOLVED if any unresolved, else PASS.
- Output: verdict, failures (cycle, phase, category, field, actual, expected), assumption_violations, unresolved, checks, rows_processed, properties.
- Scope: checks only the listed properties on supplied observations; no claim of complete proof of DUT correctness.

