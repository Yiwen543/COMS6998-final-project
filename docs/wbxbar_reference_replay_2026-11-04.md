# WBXBAR reference-checker freeze and saved-action replay — 4 November 2026

The separately registered replay and measurement audit **passed**. All 42 saved
B/C batches reproduce the original public-pin traces and all 2,845 raw DUT counter
identities and values. The reviewed reference checker classifies all six final
sessions as **unresolved**, not functional passes. Original experimental results
and the earlier cancellation replay are preserved. This phase made zero model
calls and generated no new stimulus.

## Frozen scope and provenance

The [scoped checker gate](wbxbar_conformance_gate_2026-11-04.md) precedes this
registration. Claude authored and independently reviewed the checker, contract,
properties and selftests. GPT/Codex copied those four files byte for byte, implemented
the freeze/audit/report infrastructure, and replayed the existing fixed driver.
No checker behavior or DUT code was edited in this phase.

| Artifact | SHA-256 |
|---|---|
| `configs/wbxbar_reference_replay_v1.json` | `35b7066816433d4784a2c331ed16d5026c84469bf6e3a1368e424ab0023e61aa` |
| `configs/wbxbar_reference_replay_freeze_v1.json` | `8d3c0b11b8635f281db56d1d4880a30a473cfff876dab1ef884bf557573cb140` |
| Frozen `checker.py` | `682fcf01eb44079cc9814aa66b551cfe40e45756f05fea8d82bbdc703c117a1d` |
| Frozen `contract.md` | `5de9e47953e147600381c1028b21ebeea8427f7c24471302e8d350c39f351868` |
| Frozen `properties.json` | `f4d40ce149ae379e829bb055e80a69b9e8fb3be6e7941b8355eae8828fde0458` |
| Frozen `selftest.py` | `40b17f97746ae7cac2d1a119b8ab24580481e8d87d5a668b44675bb29b86c3ec` |
| Reused original Verilator binary | `5720db4797f9f372ac76f2478ed963ffeb3bf947d9385ed70f11b43a710d35c6` |

The bundle is `results/wbxbar_reference_replay_20261104/frozen-checker/`, copied
from `results/wbxbar_reference_checker_20261104/documentation-v1/candidate/`.
The registration binds **895 historical files**, including the original live
experiment, previous cancellation replay, and both old freezes. Their hashes still
match after replay. The freeze also binds the replay/audit source, original binary,
manifest, reviewed checker evidence and fixed driver dependencies.

Git HEAD was `50d7ee83d61989017e28e981420cd58f4c5f0787`, with a dirty working tree;
artifact hashes identify the actual version. The original compile metadata records
Python 3.13.9, Verilator 5.050, Icarus 12.0, Yosys 0.70+post
(`0c11ea098be065e585a90a06e7b7da49936cf231`), Cargo/Rust 1.99.0 and OpenAI SDK
2.54.0. No recompile, synthesis or model call occurred in this replay; complete
version strings and replay Python/platform are in the new registration.

Original limits remain **3 repetitions × 6 rounds × at most 64 new cycles**, with
an eight-cycle common seed, exact `gpt-6.1-sol`, low reasoning, 32,000 input and
16,384 output tokens, 120-second timeout and at most one retry. These model limits
describe the preserved live experiment; they incurred no new API usage here.
All eight semantic groups and their **17 separate target source counters** remain.

## Execution and audit

For each of six sessions, replay executes the seed and each of six complete
cumulative action batches. Each execution uses the original reset and counter
initialization policy and the same original binary. There are no appended drain
cycles, additional resets or edited actions. Existing initialization/reset activity
stays in the measured counters; no baseline subtraction was introduced.

The independent audit reconstructs vectors from the saved JSON, reparses simulator
output and raw coverage, and compares against both historical runs. It checks:

- Identical actions, complete public-pin traces and driver transport ledgers.
- All **2,845** original DUT counter identities **and hit values**, including zero
  counters. The denominator is line 86 + branch 88 + expression 321 + toggle 2,350;
  testbench code is excluded by the original source filter.
- Complete execution of **42 batches / 8,360 physical cycles**, with no failed
  simulation attempt or retry. Cumulative prefixes are replayed and counted each time.
- Fresh execution of the frozen checker over all 42 traces reproduces every saved
  checker output; all 58 author selftests pass. No simulator is called by this audit.
- All 895 preserved hashes and the new freeze remain valid.

Three focused automated tests additionally reject historical-file drift, live-call
authorization in a replay registration, and tampered trace/raw-counter evidence.
The diagnostic-correspondence test retains ambiguous and unmatched cases instead
of forcing every old alarm to become a post-abort unknown. The actual replay happens
to have a unique same-cycle/same-slave post-abort counterpart for every old alarm.

One local preparation attempt failed before registration or simulation because a
relative candidate path was not resolved against the repository root. It was fixed
before freezing; the failed attempt is retained in `preparation-attempts.json`.

## Reattribution result

Six seed batches are `scoped_pass`; all **36 generated-round batches** and all
**six final sessions** are `unresolved`. No new checker failure or input-assumption
violation is reported. This is not a proof that the DUT is correct or defect-free.

| Session | Original final verdict | Original final alarm instances | Previous cancellation replay unknown records | New unknown records | New final verdict |
|---|---|---:|---:|---:|---|
| rep1-B | dut_violation | 1 | 4 | 11 | unresolved |
| rep1-C | dut_violation | 7 | 11 | 17 | unresolved |
| rep2-B | dut_violation | 3 | 3 | 15 | unresolved |
| rep2-C | dut_violation | 5 | 10 | 33 | unresolved |
| rep3-B | dut_violation | 2 | 3 | 14 | unresolved |
| rep3-C | unresolved | 0 | 1 | 14 | unresolved |

The **59 repeated original alarm instances across cumulative batches** include
**18 instances in the final batches**; they are not 59 distinct defects. All 59
have a recorded cycle/slave correspondence to `post_abort_forward` uncertainty.
This correspondence is evidence of changed attribution under the reviewed
contract, not independent confirmation or exclusion of a DUT defect.

The six final traces contain **104 unknown records** under the new checker:

| Unknown category | Final-session records |
|---|---:|
| `possible_starvation_err` | 65 |
| `post_abort_forward` | 26 |
| `same_edge_response_after_abort` | 9 |
| `pending_at_batch_end` | 2 |
| `unexplained_mapped_err` | 2 |

The prior cancellation checker recorded 32 final unknowns. The new contract and
recording granularity retain more explicit ERR and history uncertainty; these
totals cannot be compared as defect counts, checker accuracy or LLM effectiveness.
All six final verdicts were already unresolved in that prior replay and remain so.
No new DUT defect type was independently adjudicated in this phase.

All 8,360 rows are processed, including 244 reset rows. All 8,116 non-reset rows
are reported as effective association-checked rows. There are zero suspended rows,
post-history-death rows, resource exhaustions, invalid-input boundaries or undefined-
output termination boundaries in these traces. Therefore this replay's unknowns
are not explained by hitting the checker resource cap. These instrumentation counts
do not replace DUT coverage or establish whole-protocol conformance.

K6 response order and K13 response without CYC remain unresolved in every final
session; K9 cancellation/orphans is unresolved in five, K8 errors in rep2-C, and
K12 batch end in rep1-C/rep2-C. Other included final clauses are
`checked_not_refuted` within the contract. K5 forwarding/side-effect order is excluded;
C1–C4 characterization and F1–F8 formal obligations remain unproved. The contract's
non-normative public-FIFO read-ACK assumption and two nonblocking documentation
edge cases remain explicit. See the per-clause CSV rather than treating a scoped
status as a formal certificate.

## Coverage and cost remain separate from functional status

All six sessions still hit all **17/17 targets in round 1**. Every final session has
line **82/86**, branch **79/88**, and expression **282/321**. Final toggle counts are
**1,952/2,350** except rep3-B at **1,940/2,350**. Every underlying counter value—not
just these percentages—is unchanged. Equal predicate groups retain separate source
locations. These remain tool-defined instrumentation points, not all source lines,
all feasible paths or specification properties.

| Additional retrospective work | Measured value |
|---|---:|
| Simulator executions / executed cycles | 42 / 8,360 |
| Compilation / model generation calls | 0 / 0 |
| Simulation subprocess wall time | 1.628692 s |
| Replay wall time, including checker work | 3.472051 s |
| Separate audit wall time | 2.238581 s |
| Model API cost | $0 |

The wall-time rows overlap: simulation time is included in replay time. These costs
are additional retrospective work and do not replace the original live experiment's
costs. Preparation, tests and report writing are outside these measured intervals.
Existing curves need no recalculation because neither original coverage nor live
usage changed; the new per-batch and per-session CSVs document this explicitly.

This replay adds **no C-over-B efficacy evidence**. Historical model requests saw
the old checker feedback, so relabeling their outcomes cannot create a new matched
experiment under the new checker. WBXBAR also remains a known-easy exploratory
control: both arms already reached all registered source targets in round 1.

## Reproduction and next decision

From the repository root, the exact commands used were:

```sh
.venv/bin/python scripts/freeze_wbxbar_reference_replay.py --registration configs/wbxbar_reference_replay_v1.json --freeze configs/wbxbar_reference_replay_freeze_v1.json --bundle results/wbxbar_reference_replay_20261104/frozen-checker
.venv/bin/python scripts/replay_wbxbar_cancel.py replay --freeze configs/wbxbar_reference_replay_freeze_v1.json --output results/wbxbar_reference_replay_20261104/replay-v1
.venv/bin/python scripts/audit_wbxbar_reference_replay.py --run results/wbxbar_reference_replay_20261104/replay-v1 --output results/wbxbar_reference_replay_20261104/audit-v1
.venv/bin/python scripts/report_wbxbar_reference_replay.py --run results/wbxbar_reference_replay_20261104/replay-v1 --audit results/wbxbar_reference_replay_20261104/audit-v1 --output results/wbxbar_reference_replay_20261104/report-v1
.venv/bin/python -m unittest discover -s tests -p 'test_wbxbar_reference_replay.py' -v
```

The freeze and output directories are write-once. Reuse the existing freeze and
choose fresh replay/audit/report output paths for reproduction; do not overwrite
the preserved evidence. The audit reads both historical runs and original binary.

Evidence index:

- [Audit JSON](../results/wbxbar_reference_replay_20261104/audit-v1/audit.json) and
  [old-alarm correspondence](../results/wbxbar_reference_replay_20261104/audit-v1/diagnostic-correspondence.json).
- [All-batch metrics](../results/wbxbar_reference_replay_20261104/report-v1/metrics.csv),
  [final sessions](../results/wbxbar_reference_replay_20261104/report-v1/final-sessions.csv),
  [property scope](../results/wbxbar_reference_replay_20261104/report-v1/property-scope.csv),
  and [summary with input hashes](../results/wbxbar_reference_replay_20261104/report-v1/summary.json).
- [Original live result](wbxbar_exploratory_bc_result_2026-11-04.md) and
  [prior cancellation replay](wbxbar_cancel_contract_2026-11-04.md) remain intact.

The replay audit prerequisite is now satisfied. A fresh B/C run would require a
separate registration/freeze using this checker, independent fresh model sessions,
unchanged budget and explicit handling of unresolved functional outcomes. It would
measure fresh stimulus generation under the revised feedback, without backdating
the original trials. No new B/C run is authorized by this replay-only freeze and none
was launched. Because the target is already easy, another such run should be framed
as a reliability/feedback control, not a search for a favorable C result. Stronger
cancellation or timeout claims still require independently justified contracts or
formal evidence; they must not be invented to eliminate unknown records.
