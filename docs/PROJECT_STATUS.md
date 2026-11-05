# Project status and repository map — 4 November 2026

**Latest live experiment:** [fresh WBXBAR B/C under the frozen reference checker](wbxbar_reference_bc_2026-11-04.md)
completed all 36 rounds. Both audits pass, with zero retries and 773,454 total API
tokens. All six sessions hit the 17 raw targets in round 1; final line82/86,
branch79/88,expr282/321 tie. C uses43.34% more tokens to target and8.03% more total;
final toggle means B1946.67/C1942.00. Transient C toggle leads in rounds2–3 are
retained, without statistical/causal claims. All six finals remain unresolved
(86unknown records,0checker failures), not passes. Both arms keep3x6x64+8seed;
42simulations/8400cycles,2compiles. The independently frozen Claude checker is
unchanged, all historical evidence preserved, key deleted. No further run launched.

Preceding reliability result: [WBXBAR reference-checker freeze and replay](wbxbar_reference_replay_2026-11-04.md).
**Replay measurement/integrity audit passed; functional outcomes remain unresolved.**
A separate registration/freeze binds the reviewed Claude checker and 895 preserved
historical files. All 42 saved batches/8,360 physical cycles reproduce both prior
public-pin traces and all 2,845 DUT counter identities/values. The six seed batches
are scoped passes, all 36 generated rounds and six final sessions are unresolved.
All 59 repeated original alarms (18 final) have explicit post-abort unknown
counterparts; the new checker reports zero failures and 104 final unknown records.
All rows were processed without resource exhaustion or suspended checking. These
are limited-scope results, not proof of IP correctness. Every session still reaches
17/17 targets in round 1; no new C-over-B evidence. Three integrity/correspondence
tests pass. No model calls, fresh B/C, changed budget or checker edits in this phase.

The preceding [WBXBAR conformance gates](wbxbar_conformance_gate_2026-11-04.md)
passed within the declared checker scope: 58 author selftests, 127+6 controls,
158 evaluated cases and independent code/documentation reviews. The frozen bundle
is `results/wbxbar_reference_replay_20261104/frozen-checker/`.
K5/C1-C4/F1-F8 and other declared exclusions remain. The key was deleted after
that validation. The following paragraphs retain the checker-development history.

An original-RTL observer proves next-edge globally quiet slave outputs, with an
expected failing zero-delay control and two covers; it does not prove empty buffers
or safe cancellation after restart. Claude's first candidate-history design failed
fresh independent review for verdict, ordering, dependency and formal-mapping
issues. The final ERR-boundary design now passes fresh independent review for
implementation only. Eight completed responses cost $4.635883 / 677,889 tokens;
two credential failures and one transport rejection are preserved separately.
Repeated HR ERRs remain unjudged/unknown. Claude has produced a new immutable
candidate: 39 author selftests pass, and classifications agree with 127 independent
synthetic/metamorphic controls plus six resource-limit controls. This is control
agreement, not code certification. The fresh code review returned **not ready for
replay**: evidence loss at exhaustion/dead histories, vacuous property statuses and
undisclosed display truncation were independently reproduced; mixed-edge and B2
decisions still need explicit author/reviewer resolution. Claude's first repair
retains 127+6 expected control classifications but passes only 45/46 author tests:
the old mixed-edge expectation conflicts with proposed K6 rule P4. It improves
unknown-tag retention and discloses truncation, but per-clause checked/unknown/
suspended counts remain absent, and a tagged invalid-boundary diagnostic exposes
inconsistent refutation wording. Review of the complete 144-trace evidence returned
not ready: ACK-specific P4 and display counts are accepted, ERR handling and valid-
prefix tags require repair, and per-property scope must separate actual checking
from suspended/post-death exposure. Two ERR companion controls reproduce the issue;
the following author call improved this to 53/54 selftests but still lost an
unknown ERR at an ordinary invalid-input boundary. The latest completion call
fixes that failure with ten exact Claude patches: **54/54 unchanged selftests and
127+6 original control classifications now pass**. K11 counts 33 actual eligible
row checks in the exhaustion control, with schema/reset checks explicitly outside
that instrumentation. All 17 focused cases and five additional boundary probes
execute without infrastructure errors. Four malformed/input boundaries retain the
old tag; undefined DUT control termination still omits it while reporting the DUT
failure. The fresh review is complete and rejects replay readiness for this
termination path: it also omits pending entries and prefix-qualified statuses.
K11 accounting and the public-FIFO read-data rule are accepted within their stated
scope. The reviewer reports selective inspection, not complete reconstruction of
all 155 cases. Three additional termination controls and a nine-trace targeted
author packet were prepared. The subsequent Claude patch now retains termination
unknowns, pending entries and prefix status without suppressing the DUT failure.
All 58 selftests pass (prior 54 expressions unchanged); all 158 cases reran, with
127+6 original classifications intact. The 154 non-termination outputs match the
parent after excluding two newly added null termination fields. A fresh complete
158-case code review now accepts the targeted repair. Claude added only the three
requested documentation clarifications, and a fresh documentation review accepted
them; checker, selftest and properties hashes are unchanged. There are 31 passing
transport/provenance tests. Eleven implementation-phase calls cost $8.105366 /
1,237,196 tokens, separate from design costs. Two nonblocking documentation edge
cases (invalid-limit unprocessed rows and directly emitted K13 tags) are recorded.
Scoped validation preceded the separately frozen replay reported above.
That checker-development stage had no fresh live B/C; the subsequent new trial is reported above.
Original DUT, driver, 17 target counters, 2,845 denominator and budgets stay
unchanged. This remains a known-easy exploratory reliability control.

Previous reliability result: [WBXBAR cancellation contract revision and replay](wbxbar_cancel_contract_2026-11-04.md). Claude v4 passed 69 independent controls, 22 selftests and a fresh limited-scope review; a separate replay-only freeze precedes all 42 saved-action replays. Every original pin and raw counter matches. All 36 generated rounds are now unresolved; five final violation verdicts become unresolved and the sixth stays unresolved, never pass. All 59 repeated old diagnostics (18 final instances) explicitly map to same-cycle/same-slave post-abort uncertainty. Original results and resource limits remain unchanged. Two Claude calls cost $0.960882 / 156,817 tokens; replay adds 42 executions / 8,360 cycles, zero new stimulus generation. Remaining limits include inferred cross-slave forwarding order, ownership ambiguity and unproved cancellation timing. The staged key is deleted.

Latest completed experiment: [completed exploratory WBXBAR B/C pilot](wbxbar_exploratory_bc_result_2026-11-04.md).
All 36 live rounds passed the raw-evidence audit: exact gpt-6.1-sol, no retries,
770,531 API tokens, 42 simulations and 8,360 cycles. All six sessions reach the
17 original targets in round 1; final line 82/86 and branch 79/88 tie. C costs
43.30% more mean tokens to target and 7.21% more total tokens. First-round toggle
mean is higher by 68 counters; final median ties (mean difference 4/2350).
This is the user-authorized known-easy exploratory control, not a retroactive
pass of the original difficulty screen, and it has no length-matched placebo.

Functional conclusions remain unresolved. Five final frozen verdicts say
`dut_violation`, one `unresolved`; no session reaches checker-complete attainment.
A fresh anonymous Claude read-only attribution and two Icarus diagnostic replays
(400 separately counted cycles) are followed by external tracing of the unchanged
checker. All 18 final routing diagnostics match a unique accepted request in a
non-head aborted queue position; the head-only matcher rejects them. This is one
shared checker attribution limitation, not 18 proven DUT defects. No checker or
historical verdict was changed. There are zero confirmed new DUT defect types.
A new specification-only Claude checker revision and controls must precede any
further trial; do not simply rerun this flawed boundary hoping for C gain.
Seven Claude development/diagnostic calls total $3.035072 / 443,589 tokens. Both
staged keys were deleted; original DUT, budgets and source denominators remain.
Thirty-one focused checks, complete mock/replay and all 36 live-round accounting
checks passed. The report includes per-session costs, CSVs, raw evidence and plots.

Earlier public-IP screen: [WBXBAR conditional index](wbxbar_conditional_index_2026-11-04.md)
separately registers and proves `!grant[N][2] && mgrant[N] => mindex[N] <= 2`
on the original transition system, with no protocol assumptions. The stronger
mgrant-only assertion fails and is retained. Base/induction, nonvacuity and
negative controls certify only the actual conditional domain. All 109 definition
checks pass; 91 exact mappings yield 8 static groups (6 nontrivial), while 34
unresolved mappings and 16 unsupported event-context targets remain explicit.
All 2,845 raw DUT counters remain. Forty-four ordinary cases have matching
dual-simulator meaningful traces; all 17 group-member counters are already hit
by isolated mapped/unmapped reads. The ordinary gate therefore rejects this
scope before checker, multistep calibration or B/C. Forty-two tests pass, with
310 provenance entries checked and old freezes unchanged. API calls/cost are
zero; the original 3×6×64 budget and roles remain. Next selection must isolate
source predicates that depend on multistep completion, not merely arbitration.

Previously: [transaction/recovery screening](transaction_recovery_screen_2026-11-04.md)
preregisters original Wishbone firewall/crossbar and an AXIS packet RAM switch,
with the original 3×6×64 budget and role separation. New checked array, cached
instance, memory-cut and generated-counter membership adapters pass 13 new
checks plus 18 regressions; old SPI freezes are unchanged. Firewall has 0
eligible groups; RAM switch has 2 trivial groups, below the unchanged gate.
Crossbar was blocked on an unproved state-index bound (`m_stall`), rather
than being classified as a negative IP result. No ordinary traffic, new checker,
B or C was run. All 18 offline attempts are retained; model/API cost is zero.
A separately registered state-domain proof was the next crossbar action and is
completed above; no key is needed until static and ordinary screening pass.

Previously completed: [independent SPI failure attribution](spi_failure_attribution_2026-11-04.md)
used one read-only Claude call ($0.437321, 74,472 tokens). Six single-variable
controls agree across Verilator/Icarus and support a probable same-CSID
configuration-change/held-CS DUT discrepancy with checker diagnostic cascades.
Two reviewer acceptance-cycle errors are corrected from raw ledgers; the
original response and checker remain unchanged. An existing upstream issue
corroborates the behavior but has no maintainer confirmation. All historical
verdicts and freezes are retained; no new checker certification is claimed.

The separately [registered event screen](multistep_event_screen_2026-11-04.md)
keeps the original 3×6×64 budget and requires targets that ordinary transactions
do not hit. New exact-lvalue/static-loop adaptations pass independent Yosys/Z3
checks. AXI FIFO has zero eligible static groups; frame length adjustment plus
FIFOs has six nontrivial groups, all hit by ordinary single frames without
deliberate backpressure. Both configurations are rejected before checker/API
investment. Eighteen focused checks pass. No new B/C run or OpenAI call;
the Anthropic staging file was deleted. Next selection must distinguish
multistep events at actual source counters, not only provide semantic redundancy.

Previously, the separately preregistered [safe-offer SPI driver](spi_core_safe_driver_2026-11-04.md)
passed thirteen dual-simulator controls, four real faulty-SV controls, ten tests
and complete mock/replay. Two read-only Claude audits ($0.909992 total) accept
the limited new B freeze. The original checker, targets, denominator and
3×6×64 budget remain fixed; waiting is not free. The fresh [live B run](spi_core_safe_b_development_2026-11-04.md)
completed 18 calls, 518,275 API tokens, 21 simulations and 2,308 actual cycles.
All three repetitions are input-legal but have just one target group left after
round 1 and reach all 17 in round 2: the original discrimination gate fails,
so C is not started. Final checker verdicts are pass/fail/fail. Two separately
accounted Icarus replays (416 cycles) reproduce the failures; attribution was
unresolved at that stage and is investigated above. Ordinary calibration covers 16/17
groups, and the remaining shared stall group measures entry rather than completed
recovery. The next candidate must offer multiple genuinely event-specific source
targets, not just more modules or syntactic equivalents. The new transport version
is not pooled with old direct-pin results; both staged credentials were removed.

Previous live result: [integrated SPI core B development](spi_core_b_development_2026-11-04.md)
completed all 18 GPT-6.1-Sol calls under the original 3×6×64 budget.
Repetitions 1/2 legally hit all 17 target groups in rounds 4/3. Repetition 3
withdrew a pending command at cycle 174; its raw round-6 target hits are retained
but do not count as legal attainment. The unchanged all-repetitions-valid gate
therefore fails, and C/A/B/P are not started. This is a stimulus transport
failure, not a DUT defect or evidence against E-graph feedback. The run used
524,720 API tokens, 21 simulations and 2,394 actual cycles. Prompts, raw counts,
CSV, target-cost censoring and plots are saved; staged OpenAI credentials were
deleted. That failure motivated the separate safe-offer version above.

The preceding [SPI core checker v4 and limited freeze](spi_core_checker_freeze_2026-11-04.md)
fixes CPOL edge attribution and false recovery events through Claude-authored
patches and independent controls. All 26 independent positives pass; 13/14
single faults are detected, with missing RX explicitly inconclusive. The reviewer
accepts the limited scope, not whole-IP certification. Three clean, in-budget
multistep events and 17 seed-zero source groups (8 nontrivial) qualify. The exact
checker, JSON driver, all 3,107 original counters, target subset and original
3×6×64 development budget are frozen. Full mock/replay agree exactly and make
no live-performance claim. It admitted the B development trial above, not C.
Software-reset/dummy completion and other checker
limitations remain documented. SPI is still a previously explored family.

The preceding [SPI core contract repair](spi_core_contract_repair_2026-11-04.md)
registers low-byte-first core semantics using pinned public register/programmer
intent and parent boundary mapping, retaining the conflicting internal prose.
One Claude patch and fresh review cost $0.808042 (123,369 API tokens).
Byte order and pending-CSID checks pass, but CPOL idle-edge attribution and
TX-starvation event omission still block freezing. The evaluator now rejects
missing required events; expanded independent mode controls reproduce both
checker issues. Thirty new dual-simulator executions preserve all 3,107 raw
counter identities. At that historical stage B/C were disabled; v3/v4 followed.

The preceding [independent SPI core checker audit](spi_core_checker_audit_2026-11-04.md)
completed one Claude author and one independent review call, with $1.580242
reported cost. Four independent hand positives and all 11 author selftests pass,
but the checker cannot be frozen: the pinned documentation and actual core have
opposite byte order, and checker pending-CSID/event accounting needs repair.
Post-review causal input and in-flight hardware-reset controls were executed;
one reviewer DUT-underflow conjecture was rejected against full traces. No
OpenAI/B call followed, credentials were deleted, and B remains disabled.

The preceding [real-parent integration screen](real_parent_screen_2026-11-04.md)
uses preregistered original AXI DMA, SPI core and AXI-Lite I2C parents. SPI core
passes static semantics/mapping with 20 groups, 9 nontrivial; its public-pin
driver has matching dual-simulator observations and passing input transport
checks. That stage admitted independent checker construction, **not B**. Ordinary
controls hit 16/20 groups and TX/RX backpressure shares one stall group, so
multistep target discrimination remains unestablished. AXI has zero qualifying
groups; I2C has unsupported expressions; full Flash remains deferred for
multiclock/PHY dependencies. 45 relevant preflight tests passed. That stage had
no live calls; the prepared spec/interface packet was used by the audit above.
Budgets are unchanged.

The preceding [fixed DMA-write / Flash program-arbiter screen](natural_write_scope_preflight_2026-11-04.md)
found 0 / 1 / 0 eligible groups. Those negative results are retained. Neither
Flash units nor repeated scopes within the SPI family count as independent IPs.

## Research contract

The proposal asks whether execution coverage and E-graph-normalized semantic
feedback improve an LLM's RTL verification coverage and Token ROI over text-only
and raw-coverage feedback. The controlled comparison is **C versus B**; A versus
B tests the value of coverage feedback. P is an added token-matched placebo for
prompt-length effects. Coverage always refers to original DUT source counters,
not the number of E-classes. The independent specification checker, RTL, JSON
driver, simulator options and denominator are fixed within each trial.

| Proposal stage | Current evidence | Remaining boundary |
| --- | --- | --- |
| Initial stimulus and structural parsing | CVDP arbiter starter; Yosys pre-`proc` typed guards; Rust `egg` with bounded saturation and Z3-checked two-state rewrites | Unsupported SystemVerilog expressions remain explicit; this is not a general RTL semantic model |
| Coverage-guided execution | Verilator DUT-only line, branch, expression and toggle counters; Icarus checker controls; fixed JSON cycle driver and independent replay | Tool-specific counter meanings and unreachable points remain in the raw denominator |
| E-graph refinement | Frozen A/B/P/C model feedback and saved prompts, API usage, cycles and simulator calls | No general C-over-B gain has been shown |
| Evaluation | Arbiter/FIFO/timer historical pilots, queue B/C milestone, controlled divider/FIFO stress A/B/P/C trials, and exploratory B-full/B-compact/P/C prompt ablation; Claude reviews of earlier frozen trials | Too few independent natural IPs and near-saturated targets for a general effect estimate; free-form assertion generation and CVDP Pass@1 are not measured |

The [Milestone 1 report](milestone1_result_report.md) describes the queue B/C
trial. The latest [divider](divider_abcp_result_2026-10-30.md) and
[FIFO stress](sfifo_stress_abpc_result_2026-10-30.md) reports preserve the
four-arm trials and their limitations. The FIFO stress design is a disclosed,
equivalence-checked synthetic redundancy variant of ZipCPU `sfifo`, not a
naturally redundant held-out CVDP design. The current result is a null C-versus-B
comparison on those two controlled trials, not a refutation of E-graphs.

The [3 November exploratory prompt ablation](sfifo_prompt_ablation_result_2026-11-03.md)
used the same synthetic FIFO with an expanded five-source-counter target.
All 12 sessions reached it in round 5. B-compact retained all raw evidence and
saved 7.0% of target-cost tokens; C-compact cost 21.4% more than B-compact
without improving target rounds. Here "C-compact" packs the **B base** but still
includes the full semantic appendix. The new minimal-C renderer shortens that
appendix; its [18 archived-prompt previews](../results/minimal_c_preview_20261103/preview.json)
are offline artifacts with zero model calls, not new model results.

The subsequent [minimal-C live ablation](minimal_c_result_2026-11-03.md) used
fresh interleaved B-compact/C-full/C-min/P-min sessions. All twelve reached
the target in round 5. C-min reduced C-full's token cost by 15.3%, but remained
2.95% above B-compact. All 72 calls and 84 replayed simulations were validated;
final toggle counts vary and are reported separately. Failure retention,
per-request counting and own-trajectory placebo matching are implemented in
the new runner. This supersedes the earlier offline-only status.

The [natural-IP screen](next_ip_screen_2026-11-03.md) rejected TX UART after
three B repetitions reached all five groups by round 2 and failed the
preregistered first-round gate. The codec was already saturated in round 1.
AXI VFIFO encoder and flattened linear-search groups remain provisional;
OpenTitan candidates require frontend/source-map work. No new pair of
independent natural IPs has passed every gate.

A [parameterized follow-up screen](ip_selection_diagnosis_2026-11-03.md)
found no nontrivial supported groups in the selected natural frame-FIFO
configuration. An isolated checksum-verified OSS CAD Suite now elaborates
the original OpenTitan SPI_HOST FSM. The subsequent
[SPI preflight](spi_host_preflight_2026-11-04.md) implements the Slang typed AST
adapter with 109 exact source-counter joins and 26 clock/reset connection checks.
Its fixed JSON driver and scoped specification checker pass 35 identical public
traces on Verilator and Icarus and detect three injected single faults. Seven
seed-zero groups were calibrated, but none required a rewrite in that first
adapter. The [semantic repair and live B follow-up](spi_semantic_repair_2026-11-04.md)
adds typed combinational SSA and independent Yosys-cell proofs (68 definitions),
then saturates Z3-certified design-specific rules in egg. It maps 186 of 199
targets and finds two qualified nontrivial groups among nine qualified source
groups. All three B repetitions hit all nine groups in round 1, so the original
development gate fails and no formal A/B/C/P trial follows. The live run has
18 successful generation calls, 21 simulations, 2,346 replay cycles and 388,818
API tokens; 94 repository tests and the saved-evidence recheck pass. General
hierarchical guards, exact sample timing and full formal checker validation
remain open. This is B-only screening evidence, not a C-effect estimate.

The [role-separated event milestone](spi_role_separated_events_2026-11-04.md)
adds a separately authored Claude checker with unchanged SV driver/RTL and
GPT-authored private calibration. Independent controls caught checker errors
that its own tests missed; only exact Claude patches were applied. The final
scoped checker passes independent positive controls and detects 10/12 retained
external mutation controls (two outside declared scope), with a fresh Claude review.
Three event families have clean calibrated examples; same-CS configuration
switching remains a reproduced spec/implementation discrepancy, not qualified
event evidence. The subsequent [I2C role-separated preflight](i2c_role_separated_preflight_2026-11-04.md)
certifies all nine different-expression pairs, binds their 18 source counters,
and maps 218/268 predicate targets. A Claude-authored scoped write-mode checker
and fixed GPT/Codex bus driver validate three multistep events on both simulators.
However, all 18 reachable equivalent source groups already execute in an ordinary
one-byte write; zero late-specific groups qualify. No I2C B or C run was started. Formal A/B/C readiness stays false: temporal-event/source
bindings and independent-IP qualification remain unresolved. See
`examples/heldout_spi_host_events/freeze.json` and
`results/spi_host_event_checker_20261104/accounting.json` for the exact boundary
and development costs; those costs are separate from stimulus-model pilots.

The [READB/read-ACK extension](i2c_read_preflight_2026-11-04.md) adds a separate
read-capable driver and Claude-authored scoped checker. Independent controls
caught and repaired same-row push/flush ordering, with the failed version
retained. Nine calibration traces agree between simulators; multi-byte reads,
RCONT chaining and read/restart are witnessed. All 25 reached equivalent groups
(three nontrivial) already execute in ordinary read/write controls: zero new
multistep-specific groups qualify. B/C remain unrun, budgets unchanged. The
checker rejects nine protocol mutations, but one extra-STOP verdict remains
misclassified as invalid; no full fault-attribution or formal guarantee follows.
Twenty I2C-focused checks and the frozen smoke replay pass. AXI DMA legacy
`always @*` extraction and an exact-source flash-controller dependency probe
provide two separate follow-up families, not two qualified benchmarks.

The [AXI DMA / Flash integration](natural_ip_integration_2026-11-04.md) has now
closed 29 exact pinned Flash dependencies and implemented typed shifts, packed
updates and statement-position SSA. Independent Yosys encodings validate 68 DMA
and 13 Flash top-level combinational definitions. Source joins are 64/68 and
25/29; all 3,404 DMA and 1,592 Flash DUT counters remain separate. Both fixed
read-submodule scopes fail the static dynamic-group gate (zero qualified groups),
so no new checker, B or C calls ran. This is not a rejection of the full IP
families. Flash's original SV still fails Icarus package syntax; its explicitly
lowered-netlist reset smoke matches original-RTL Verilator. Seven new tests and
twenty existing I2C regression checks pass; general hierarchical path guards and
legal multistep targets remain work before expanding these scopes.

Open-source formal work is underway: the [candidate preflight](midterm_candidate_preflight_2026-10-30.md)
records SymbiYosys BMC/cover/prove tasks on selected fixed candidates, and the
FIFO stress report records fixed-configuration Yosys equivalence. These claims
are scoped to their saved assumptions and configurations; neither coverage nor
finite-depth BMC is a complete correctness proof.

## Canonical locations

| Directory | Keep | Regenerate or discard |
| --- | --- | --- |
| `examples/` | Pinned RTL, specifications, fixed drivers/checkers and provenance | Local compiled simulation products |
| `scripts/`, `egraph/src/`, `egraph/Cargo.lock`, `configs/`, `tests/` | Pipeline, rewrite engine, frozen settings, automated checks | Python bytecode and Cargo `target/` |
| `docs/`, `output/pdf/` | Proposal mapping, dated reports, freeze manifests and submitted milestone PDF | Temporary PDF render files |
| `results/` | Historical live evidence, raw DUT counters, accepted actions, rendered prompts, summaries, plots, replay validations and Claude audit dispositions | `verilator-build/`, `plot-cache/`, `mplconfig/`, `cache/` |
| `build/`, `.cache/`, `.venv/` | Local working environment only; all Git-ignored | Disposable compilation and download output; never commit credentials |
| `project_background_reading/`, `third_party/` | Original readings and pinned external source checkout | Finder metadata |

Older mock and development results remain where reports cite them. They are
labelled as mock/development and never pooled with formal live results. The
clean-up removes disposable compiler objects and caches without altering saved
prompts, call envelopes, original coverage data or frozen experiment settings.

## Next experiment

Keep the two tracks separate: use the known FIFO for the exploratory
minimal-C packaging diagnostic, and qualify new natural IPs for generalization.
The [project review](project_review_2026-11-03.md) records the proposed arms,
remaining runner checks, candidate shortlist, and limits of the current
Boolean-skeleton Z3 proofs. A shorter appendix alone is not evidence of better
coverage or an extraction-algorithm bottleneck.

Screen at least two **natural**, independent FIFO/controller IPs for multiple
seed-uncovered, source-distinct, complete activation guards that are genuinely
equivalent after typed normalization. Establish independent specification
checkers, legal-input assumptions, formal or calibrated reachability and an
outcome-blind target. Reject only immediate B saturation in a separate
development gate. Freeze source/checker/driver/denominator and budgets before
the A/B/P/C trial. Preserve failures and unreachable raw points, and include a
read-only independent audit. A larger or multi-module IP alone is not a
selection criterion.

## Local verification

From the repository root, `make doctor`, `make test`, and `make step1` exercise
the starter without API keys. `make test` builds the pinned Rust engine offline
and runs the expanded Python suite. The dated result
reports contain exact replay commands for the controlled pilots. New live calls
require separately staged credentials and a new output directory.
