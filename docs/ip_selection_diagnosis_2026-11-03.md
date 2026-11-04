# Why earlier IPs did not isolate a C benefit

The experiments do not show that E-graphs cannot help verification. They do
show several different ways a proposed feedback treatment can have little
opportunity to improve a measured target. The [minimal-C live run](minimal_c_result_2026-11-03.md)
now separates a large avoidable appendix cost from the persistent lack of
primary target-round improvement on the synthetic FIFO.

## Evidence by design

| Design | Evidence | Implication for the next task |
|---|---|---|
| Starter arbiter | Tiny priority space; deterministic search and exhaustive reference solve the coverage problem. Original spec defects remain detected. | Plumbing/defect control, not evidence for model gains. Extra complexity must concern stimulus decisions, not just source lines. |
| Early FIFO/timer | Rapid ceilings or no useful cross-source normalized predicate groups; raw toggle plateaus also contain constant bit directions. | A stateful IP alone does not give C a relevant semantic advantage; separate reachability and representation limits. |
| Queue milestone | C earlier in 2/6 index-paired sessions, four ties; all selected equivalent read/write counters covered after round 1. | Small observed differences are not attributable to later equivalent-guard feedback; decisive targets must remain relevant to C. |
| Iterative divider | Four of five groups hit in round 1, all five by round 2. The decisive last branch at line 51 is outside every C group. B/C target in round 3, C costs about 50% more tokens. | This is a measured group/target mismatch, not simply insufficient IP size. |
| CVDP codec | All eight selected groups reached in round 1 of independent short B trials. | Reject for the intended hard-task population; preserve rejection records. |
| TX UART | Five groups are AST-identical before egg. Three B trials leave only one group incomplete after round 1 and none after round 2. | Little nontrivial normalization opportunity and a failed prospective B gate. |
| Synthetic depth-16 FIFO | Two nontrivial equivalent events at five source sites; members are co-hit in all 72 new rows. All treatments choose similar fill/drain schedules and target round 5. Minimal C reduces appendix tokens but not cycles. | Source redundancy is not automatically planning difficulty. Keep as an integration/packaging regression, not the main generalization benchmark. |

Sources: [milestone](milestone1_result_report.md),
[divider](divider_abcp_result_2026-10-30.md),
[natural-IP screen](next_ip_screen_2026-11-03.md), and
[minimal-C diagnostics](../results/sfifo_minimal_c_live_20261103/mechanism-diagnostics.json).
These are scoped explanations or hypotheses; no hidden model reasoning is
inferred from the generated actions. Final toggle differences remain secondary
observations, including a small higher mean for full C in the latest run.

## Changes justified by the evidence

1. **Align the measured target with available semantic information.** Preserve
   outcome-blind selection and the raw denominator, but require late target
   points to belong to validated groups. For a target-directed variant, show
   the same target IDs to every arm. Do not silently change the broad-coverage
   instruction or import a target-specific result into the old comparison.
2. **Require useful temporal choice.** Prefer at least three events with
   alternative legal schedules: frame commit/rollback, pause/resume under
   backpressure, command change while a previous transfer is completing.
   Independently demonstrate a budget-feasible path with headroom. Increasing
   a FIFO depth only increases mandatory clocks if every arm follows the same
   schedule.
3. **Require nontrivial but sound relationships.** Count AST-identical
   duplicates separately. Keep types, complete guards, event/reset context
   and every source counter. Prove supported Boolean/bit-vector transformations;
   do not treat the existing Boolean-skeleton Z3 check as a general arithmetic
   or sequential equivalence proof.
4. **Diagnose extraction before optimizing extraction cost.** The current
   six-rule engine is narrow. Record missed aliases, expressions and mappings
   separately from proved non-equivalence. Existing small graphs have negligible
   representative-extraction time; there is no evidence yet that an e-boost-like
   exact extraction algorithm is the critical bottleneck.
5. **Do not search until C wins.** Apply the same preregistered B-compact gate
   to each candidate, save exclusions, and never inspect its C outcome during
   selection. A harder selected population must be disclosed. Once frozen,
   retain failed/not-reached repetitions and matched token controls.

## Two independent natural lineages actually screened

The new [parameter manifest](../configs/natural_ip_parameter_screen.json)
pins source/spec hashes and upstream revisions. The screen does not inspect
model outcomes. It elaborates parameter overrides and verifies the resulting
RTLIL parameter values, then reuses the typed extractor, bounded egg and Z3
Boolean pair checks. Parameterized test controls check width changes without
editing RTL. Existing frozen experiment code was not changed for this screen.

**AXI-stream frame FIFO:** pinned Alex Forencich `verilog-axis` revision
`48ff7a7e2ef782cf778d47910cf85835c64b1bce`, with depth 16, data width 8,
FRAME_FIFO, DROP_BAD_FRAME, DROP_OVERSIZE_FRAME, PAUSE_ENABLE and FRAME_PAUSE
enabled. Its public [RTL](https://github.com/alexforencich/verilog-axis/blob/48ff7a7e2ef782cf778d47910cf85835c64b1bce/rtl/axis_fifo.v)
and [README](https://github.com/alexforencich/verilog-axis/blob/48ff7a7e2ef782cf778d47910cf85835c64b1bce/README.md)
provide the initial contract material. The repository is superseded by Taxi;
the pinned original is chosen for reproducible frontend compatibility, not
because it is the newest implementation.

Actual result: elaboration passes, **two supported groups, zero nontrivial
egg merges**, 35 unsupported guards. Some group source anchors are assignment
or comment lines and are not validated coverage locations. This configuration
is **not qualified** for a B/C model trial. That is a result about the supported
extraction, not proof that the IP has no useful relations. Inspect source maps
and the unsupported generated/shift predicates before spending on a checker
and live model runs. Evidence: [screen](../results/natural_ip_parameter_screen_20261103/axis_frame_fifo_16/screen.json).

**OpenTitan SPI_HOST FSM:** independent lowRISC lineage, pinned revision
`0ea5236fe749e70ba18f56ba19c4be982ef46da7`, NumCS=2, original RTL and public
[operation specification](https://opentitan.org/book/hw/ip/spi_host/doc/theory_of_operation.html).
The intended events are command segment transitions, TX/RX stall recovery,
and chip-select/configuration changes. These are candidate behaviors, not yet
proved groups or qualified coverage targets.

The existing native Yosys parser fails on package syntax. To move beyond that
blocker, an official OSS CAD Suite Darwin ARM64 release dated 2026-11-03 was
downloaded and SHA-256 checked, then installed only in ignored
`build/tools/oss-cad-20261103/`. Existing simulation and frozen experiment
tools were not replaced. The release is from
[YosysHQ](https://github.com/YosysHQ/oss-cad-suite-build/releases/tag/2026-11-03).

The isolated Yosys **0.70+309** `read_slang --no-proc` path now elaborates the
unmodified controller and generic flip-flop dependency with **zero errors and
warnings**; original Verilator lint also returns zero. The fixed interface is
checked as two chip-select output bits and a 56-bit command input. Original
source attributes survive. Embedded upstream assertion macros are disabled
only for this elaboration probe using SYNTHESIS; no property proof is claimed.

The next integration boundary is explicit: the Slang representation contains
26 flop cells and **zero process sync records**, despite retaining process
trees. The old parser obtains event/reset context from those sync records.
Source spans also follow different conventions. It would be unsound to feed
this output into the old parser and call resulting groups fully guarded.
Implement a separate reviewed adapter that relates flop clock/reset pins and
data dependencies to source predicates, validate it against known sync/async
controls, and audit source polarity/columns against original Verilator counters.
Only then build the independent public-I/O checker and fixed driver and run
reachability/B qualification. Evidence: [frontend probe](../results/natural_ip_parameter_screen_20261103/spi_host_slang/probe.json).

Neither candidate is yet eligible for live generalization results. This turn
performed actual parameterized screening and lifted the SPI package-elaboration
blocker; it did **not** fabricate qualified guard groups, run unvalidated new-IP
stimulus trials, or claim two independent confirmations.

## Reproduction and next gate

Check out the pinned external repositories and required sparse paths listed
in the manifest/probe, then run:

```sh
.venv/bin/python scripts/screen_parameterized_ip.py --manifest configs/natural_ip_parameter_screen.json --output results/natural_ip_parameter_screen_new
.venv/bin/python scripts/probe_spi_host_frontend.py
```

The second command requires the checksum-verified isolated tool release and
writes the dedicated diagnostic directory. The [probe JSON](../results/natural_ip_parameter_screen_20261103/spi_host_slang/probe.json)
records its release URL, digest, exact files, defines and commands.

Keep the existing FIFO as a regression test and use the SPI source/context
adapter as the next implementation priority. For any candidate eventually
passing source/semantic checks, independently review the specification-based
checker and legal-input assumptions, add correct/single-fault controls, and
calibrate/formally cover the targets. Then apply the previously declared
three-repetition B gate before any C run. Broader RTL support and genuinely
discriminating events take priority over another round of prompt trimming.
