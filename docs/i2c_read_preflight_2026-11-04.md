# I2C READB extension and natural-IP follow-up — 4 November 2026

READB/read-ACK now has a fixed JSON bus driver and a separately authored,
scoped Claude checker. Three read event families have clean calibration
witnesses. **I2C still does not qualify for B development:** every reached
source-distinct equivalent group is already reached by ordinary one-byte
reading or writing. This is an offline target-selection failure, not an
observed B saturation result. No I2C B/C model calls have run.

## Why the previous profile did not enter B

The [write-mode preflight](i2c_role_separated_preflight_2026-11-04.md) proved
nine different-expression pairs and mapped all 18 corresponding source
counters. Its 18 reachable groups were also covered by ordinary writing.
Recovery events existed, but they did not add useful equivalent guard targets.
READB/RCONT were tied off by that old driver. Neither module size nor the
number of proven equalities establishes a useful B/C experiment.

The extension retains the same 8-cycle seed and prospective budget of
3 repetitions × 6 rounds × 64 new cycles. A complete replay has at most
392 cycles. No budget was shortened after seeing a model result.

## Boundary and role separation

- DUT: original `i2c_controller_fsm.sv`, OpenTitan commit
  `0ea5236fe749e70ba18f56ba19c4be982ef46da7`, FifoDepth=64;
  SHA-256 `0da13b6d8185c7bd6c3949f6c28e073292c1682fd1cc10f83457f6285fd16b1a`.
  The RTL and public specification were not edited. Async active-low reset
  and timing settings are preserved. The old write-only freeze still verifies.
- GPT/Codex integration: strict JSON schema, module-based SV driver, passive
  open-drain target, calibration and independent control traces. New fields
  are `read`, `rcont`, and 8-bit `target_data`. Widths, unknown fields,
  incompatible flags and sequence length are checked before execution.
- Claude Opus 5.5 author: public specification excerpts plus the sampling
  interface only; no DUT implementation, private calibration, guard targets
  or B/C outcomes. It wrote the checker, properties, selftests and contract.
- A fresh Claude session reviewed the source and integration evidence without
  editing. Four bounded calls ran: author, review, author repair, review.
  Tools/MCP/session persistence were disabled; CLI budget was $4 per call.
- The checker repair followed development feedback about a contract violation.
  Therefore the author was implementation-blind, **not permanently blind to
  evaluation outcomes**. This is checker development before any model trial.

The target decodes physical START/address/clock/ACK signals; it does not inspect
DUT internal state or FMT flags to decide which read bit to send. Its v2 fix
latches the ninth-bit ACK actually seen on the wire, rather than re-reading
the current JSON ACK setting at a later edge. v1 evidence is retained.

## Checker evidence and remaining limits

The first checker passed its own 17 tests but rejected every nonempty legal
independent baseline: it queued same-row push/flush after inspecting `pre`.
The independent review confirmed a checker error, not a DUT defect. Only an
exact patch returned by Claude was applied. Authorship and parent hashes are
retained in `results/i2c_read_candidate_20261104/claude-v1` and `claude-v2`.

The repaired checker passes 21 author tests and all completed independent and
DUT calibration baselines. Nine independent protocol mutations are rejected;
eight receive verdict `fail`. The extra-STOP mutation produces both property
failures and an assumption violation, so its final verdict is `invalid`.
**Fault attribution is not fully qualified**, even though this trace cannot
pass the integration gate. Nine rejected cases are not nine actual DUT bugs.

Eight further controls corrupt the first RX byte inside four event families,
on both handwritten and DUT-derived traces. Each has a clean positive baseline
with the event, detects corruption, and suppresses event credit. These are
eight cases of one mutation class, not eight distinct defect types. Truncated
reads, missing eventual STOP and FBYTE=0 partial reads remain `pending`.

The second Claude review accepted only the bounded offline profile. Subsequent
integration controls added write-data, read-count, mid-read START/STOP and
address-only stretch cases; those additional results were not reviewed by a
third Claude call. The review disposition is saved separately.

Material limits remain:

- `read_stretch_recovery` only establishes stretching while READB is current;
  it does not establish overlap with a data bit. This family is excluded from
  qualified event targets. Address-only stretch earns no read-stretch event.
- One setup clock rise before START/STOP can mask an isolated extra edge.
- RX-before-pop is a fixture contract, not a proven upstream timing guarantee.
- FBYTE=0 means 256 bytes. Full completion exists only in an author control;
  the bounded DUT replay remains pending.
- No formal proof, analog timing, liveness, arbitration, multiple-controller
  or NACK-recovery assurance is claimed for this read checker.
- A fixed outer gate rejects `ENV_ERROR` and out-of-scope event pulses observed
  in either `pre` or `post`; raw checker failures and observations are retained.

## Reachability and original coverage

All nine v2 calibration traces agree cycle-for-cycle between Verilator and
Icarus. The varied two-byte case reads A6 then 3C, exercising data order.
The clean event windows below are checker observations, not formal covers:

| Event | Window, cycle indices | Status |
| --- | --- | --- |
| Two bytes in one READB | 15–358 | Clean completed event |
| RCONT chain across two READB entries | 15–360 | Clean completed event |
| Read followed by repeated START/write | 15–376 | Clean completed event |
| Stretch while READB current | 15–268 | Clean trace; limited event excluded from qualified targets |

Each full replay executes 392 cycles including initialization/reset. Coverage
is measured only on the original controller DUT, with identical counter
identities across runs. The denominator is **132 line + 116 branch + 209
expression + 820 toggle points = 1,277**. These are Verilator-defined points,
not physical line counts, transactions or independent functional properties.

| Private calibration | Line | Branch | Expression | Toggle |
| --- | ---: | ---: | ---: | ---: |
| Shared seed, 8 cycles | 31/132 | 20/116 | 45/209 | 76/820 |
| Ordinary write | 77/132 | 68/116 | 110/209 | 175/820 |
| Ordinary one-byte read | 98/132 | 92/116 | 146/209 | 222/820 |
| Two-byte read | 102/132 | 93/116 | 146/209 | 228/820 |
| RCONT chain | 101/132 | 93/116 | 146/209 | 224/820 |
| Read then repeated START | 99/132 | 95/116 | 149/209 | 224/820 |
| Stretch while reading | 100/132 | 92/116 | 147/209 | 228/820 |

The existing typed, two-state egg/Z3 proofs are reused only after verifying
the original source and proof artifact hashes. Source mappings are recomputed
against the read profile: 218/268 predicate targets map exactly, 50 remain
unresolved. Unresolved targets and unproven-unreachable coverage points are
not removed from the raw denominator.

25 source-distinct equivalent groups are reached, including 3 nontrivial
groups. **Zero groups add two source counters beyond the ordinary read/write
controls.** The newly reached nontrivial pair is at RTL lines 491 and 808
(read-byte completion). Both original counters are separately 12 on ordinary
read and 24 on two-byte read. These are simulator counter increments, not a
claim of 12/24 received bytes. Repeatedly incrementing an already covered point
does not create a new coverage target.

The prospective source gate requires at least three distinct multistep
event-to-group bindings, including two nontrivial groups. It fails. Formal
A/B/C/placebo readiness remains false; no OpenAI key is needed for this stage.

## Public natural-IP follow-up

Two independent design families were investigated. **Neither is yet qualified**;
the shortlist is not reported as two successful held-out benchmarks.

1. **AXI DMA read engine.** The [upstream repository](https://github.com/alexforencich/verilog-axi)
   documents burst DMA and optional unaligned transfers. The pinned existing
   checkout is `516bd5dadc3365b7f9e225d2af8fe0b8d804fe53`; `axi_dma_rd.v`
   SHA-256 is `853ff3aedc44ec0c12ef3ae8b84d7559800d372f76832c7c133ed5eecac61dd8`.
   ENABLE_UNALIGNED=1 was selected before any model trial. Slang, Verilator
   lint and Icarus compile probes pass. A separate lexical adapter now accepts
   `always @*` without rewriting RTL or changing edge-triggered contexts.
   It extracts 62 targets: 58 supported by QF_BV, four blocked by unsupported
   logical shifts. Two procedure-local predicates remain unpromoted pending SSA;
   the initial block is also explicitly unsupported. Among 766 same-context
   comparisons, 40 are UNSAT, including 32 different-expression pairs. Only
   15 of those pairs have satisfiable guards; they form four groups, whose
   duplicate sites largely arise from fixed parameter conditions. They have
   **no certified raw-counter mapping, egg integration or temporal witness**.
   No qualification follows from those counts.
   Next candidates are burst splitting with downstream stalls, partial final
   words, and error response followed by a new descriptor. Each needs public
   contract review, independent checker and legal-bus reachability evidence.
   The legacy repository is deprecated in favor of [TAXI](https://github.com/fpganinja/taxi);
   these related implementations must not be counted as independent IPs.
2. **OpenTitan flash protocol/read controller.** Public [theory of operation](https://opentitan.org/book/hw/top_earlgrey/ip_autogen/flash_ctrl/doc/theory_of_operation.html)
   describes FIFO flow control, error handling and hardware/software request
   arbitration. Pinned source/spec/license files were acquired and verified
   against six exact Git blob IDs. The available snapshot is the generated
   `top_englishbreakfast` variant; it is not asserted identical to Earlgrey.
   An actual Slang probe fails because the generated register/top/TLUL/EDN/
   primitive/JTAG dependency closure is incomplete. No type or primitive stubs
   were substituted. Candidate events are FIFO pause/resume and error-fill
   completion followed by a new operation. Their guard groups remain unproven.

This points to the next bottlenecks: supported expression/SSA translation and
exact source mappings for DMA; real package/hierarchy integration for flash.
Only after those gates, legal temporal reachability and a specification checker
should an independent B development trial be funded. Do not select using C,
parameter-only equivalences, or a shorter post hoc budget.

## Accounting and reproduction

`results/i2c_read_candidate_20261104/accounting.json` records 5 compilations,
37 simulator executions and 12,968 executed cycles, including two invalid
stretch-calibration attempts retained as failures. Compilation took 31.37 s;
simulation 1.29 s. Four completed Claude calls cost $1.617639 as reported by
Claude Code, with 149,927 input tokens (including cache creation/read) and
43,401 output tokens. Reasoning tokens are an output subset, not added twice.
Claude call wall time was 402.01 s; this is not total human/integration elapsed
time. One oversized review packet was rejected locally before an API call.
OpenAI generation calls: zero. Temporary Anthropic credentials were removed.

Versions: Verilator 5.050, Icarus 12.0. The development baseline commit is
`c71a3e580646d08fb6496c742b7b42b711179b36`; the workspace contains uncommitted
changes, so artifact hashes in the new offline freeze identify the actual
boundary. The smoke replay passes; 20 I2C-focused automated checks pass.

Run from the repository root, using unused output directories:

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_i2c*.py' -v
.venv/bin/python scripts/calibrate_i2c_reads.py --output build/i2c-read-replay --simulator verilator
.venv/bin/python scripts/calibrate_i2c_reads.py --output build/i2c-read-icarus --simulator iverilog
.venv/bin/python scripts/run_i2c_read_checked.py --actions results/i2c_read_candidate_20261104/driver-v2/multi_read_varied.actions.json --output build/i2c-read-checked
.venv/bin/python scripts/evaluate_i2c_read_checker.py --candidate results/i2c_read_candidate_20261104/claude-v2/candidate --base results/i2c_read_candidate_20261104 --output build/i2c-read-controls
.venv/bin/python scripts/screen_i2c_read_sources.py
.venv/bin/python scripts/legacy_guard_probe.py --ast results/natural_ip_followup_20261104/axi_dma_rd/ast.json --top axi_dma_rd --output build/axi-dma-guard-probe
```

The new offline boundary is `examples/heldout_i2c_read/freeze.json`; its
`formal_B_eligible`, `research_target_qualified` and
`defect_classification_qualified` fields are explicitly false. Detailed source
counts are in `nine-pairs-counters.csv`; checker/review/failed versions are
retained. The natural-IP probes are separate from I2C development accounting.
