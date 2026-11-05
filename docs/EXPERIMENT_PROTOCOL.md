# Experiment protocol index — 2026-11-04

This document summarizes existing registrations; it does not amend them or authorize a new run. Paths are repository-relative. Missing settings are **待确认**, not inherited from another trial. Evidence labels follow [PROJECT_STATUS.md](PROJECT_STATUS.md).

## Common fairness and measurement contract

1. [C,R] Freeze source/specification/reference/driver/tool flags/raw denominator/target/limits before each comparison. Preserve failures and immutable earlier versions. Judge C vs B primarily; A vs B measures raw coverage value. Repetitions are independent sessions, not deterministic paired outputs.
2. [R] A=spec/RTL/actions/checker/logs; B=A+raw source coverage; C=B+validated equivalent guards/context. P adds nonsemantic filler under its own trajectory. Exact information/selection comes from the trial's renderer, not this summary. No private calibration, solver witnesses, old failing vectors or golden code enters the candidate prompt.
3. [R] Equivalent expressions retain every raw source counter. Preserve source hash/path/line/column/outcome/hierarchy, widths, signedness, complete activation guard and event context. Unsupported/unmapped targets stay explicit; unproven-unreachable counters stay in the denominator. `egg` and Z3 prove limited two-state combinational relations, not reset/sequence correctness.
4. [R] Verilator Coverage-3 raw **line** points include emitted block/case/elsif locations, not a count of textual lines; **branch** points count emitted outcomes; **toggle** points are directional per-bit transitions; **expr** points are emitted Boolean outcomes. Numerator is points with hits>0, denominator is frozen emitted DUT points. Preserve hit counts too. Exclude TB source. Reset/initialization follows each fixed driver and is counted consistently. See `docs/workflow.md` measurement contract and per-run coverage metadata.
5. [R] Record generation/count calls, requested/returned model IDs, retries/failures, API usage, compilation, simulator executions, physical cycles including replay, preprocessing and wall time separately. Cached/reasoning tokens are subsets. Missing usage is unknown. Same token caps ≠ same realized prompt lengths.
6. [R] Original Token ROI = new raw branch points above seed ×1000/API input+output. Report fixed endpoint and preregistered cost-to-target; retain not-reached runs. Test2 has a different numerator (distinct valid mutant kills); do not pool ROIs.
7. [C,R] Freeze candidate outputs before hidden scoring. Claude reference author sees spec/interface; fresh reviewer audits evidence within the declared role. GPT never silently repairs the oracle. Model agreement is not correctness evidence.

## Track S — stimulus generation (historical registrations)

| Registration | Arms/model | Reps × rounds × max new cycles | Seed/settings source |
|---|---|---|---|
| `configs/arbiter_pilot.json`, `fifo_pilot.json` | A/B/C, gpt-6.1-sol | 3×4×32 | seed=6998; 4096 output; older retry cap2; actual logs authoritative |
| `configs/ttc_pilot.json` | A/B/C, gpt-6.1-sol | 3×4×16 | seed=6998; 4096 output |
| `configs/queue_bc_pilot_gpt6sol.json` | B/C, gpt-6-sol, two RTL forms | 3×4×4 per form | seed=6998; six-cycle common seed; 4096 output |
| `configs/divider_abcp_frozen.json` | A/B/P/C, gpt-6.1-sol | 3×4×8 | four-cycle seed;8192 output;P byte-matched, not token-matched |
| `configs/sfifo_stress_abpc_frozen.json` | A/B/P/C, gpt-6.1-sol | 3×6×8 | `configs/sfifo_stress_seed.json`;8192 output;see own token-matching audit |
| `configs/sfifo_minimal_c_exploratory.json` | B-compact/C-full/C-min/P-min, gpt-6.1-sol | 3×6×8 | four-cycle seed;32000 input/8192 output;90s;retry1;own-history API-token P |
| `configs/wbxbar_reference_bc_v1.json` | B/C, gpt-6.1-sol | 3×6×64 | eight-cycle deterministic seed from `scripts/probe_wbxbar_ordinary.py::seed`;32000/16384 tokens;120s;retry1 |

All listed current model settings use low reasoning; numeric seed6998 in older configs does not establish provider response determinism (`scripts/pilot_model.py` does not send a model seed). Latest WBXBAR has no declared numeric provider seed. No global budget supersedes these differing registrations.

WBXBAR: ZipCPU/wb2axip `2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b`, original `rtl/wbxbar.v` + `skidbuffer.v` + `addrdecode.v`; NM=NS=2, AW8,DW32, timeout16, double-buffer/starvation-timeout/lowpower enabled; full parameters/source hashes in registration. Fixed reviewed checker at `results/wbxbar_reference_replay_20261104/frozen-checker/`; driver in `scripts/wbxbar_exploratory_driver.py`. Denominator2845=86line+88branch+321expr+2350toggle, target17 counters/eight groups. Fresh process/counters each time, cumulative seed+history replay, no added drain. Scoped waiver bypasses failed ordinary/difficulty gate; this remains exploratory. Freeze: `configs/wbxbar_reference_bc_freeze_v1.json`.

Data provenance for earlier CVDP fixtures: `examples/arbiter/provenance.json`, `docs/dataset-lock.json`, `docs/heldout-dataset-lock.json`, `docs/midterm-candidate-lock.json`. Starter is `cvdp_agentic_fixed_arbiter_0001` cid003, not an official executed cid012 benchmark. Natural scopes/revisions are in `configs/real_parent_screen.json`, `transaction_recovery_screen_v1.json` and dated reports. Do not treat all pilots as one official CVDP evaluation.

## Track M — test2 monitor generation (completed, immutable)

- Registration: `test2/configs/registration_v1.json` + `phase1_addendum_v1.json`; final authority `live_freeze_v1.json` binds3486 files. Input manifest's top-level `source_sha256` names the **pre-sanitization stress source**; final public DUT has its own hash below. Earlier manifest status strings are historical, not proof live is pending.
- DUT: `test2/public/sfifo.v`, a disclosed synthetic stress variant of ZipCPU sfifo; BW8,LGFLEN4/depth16, OPT_ASYNC_READ1, OPT_WRITE_ON_FULL0, OPT_READ_ON_EMPTY0. Sync active-high reset; two-state; empty data unspecified; no read/write while reset. SHA256 `c46c18eb5f35489ed242d0e21fcea01e997c022356a21fae3ccb4f74a72288d0`.
- Provenance: `examples/heldout_sfifo/rtl/sfifo.v` original → `examples/heldout_sfifo_stress/rtl/sfifo.v` synthetic variant → FORMAL sections blanked with line identity. `test2/scripts/prepare.py` and input manifest document transformation. Upstream is wb2axip `2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b:rtl/sfifo.v`; this audit read that local Git object and confirmed SHA `76a653781f1ecca1c1da92c4e5105ecd5d0f832b13cbfd31300ec88d9947e0c1` matches the preserved original. See `docs/sfifo_bc_development_2026-10-30.md` and migration audit. Correspondence evidence: `test2/results/source-sanitization-proof-v1/equivalence.log` (157 cells reported proven; not a spec proof).
- Spec/driver/ABI: `test2/public/specification.md`, `driver.sv`, `observer_contract.md`; project-fixed contract, not a claim of verbatim public spec. At full+simultaneous only read accepted; at empty+simultaneous only write accepted; otherwise independent expected pre-occupancy admission.
- Independent reference: `test2/reference/frozen-v1/checker.py` SHA256 `53cff0d05aa9c48a71aec72cecfba265a13fe4baa2a4d9a72b3cef4d6b201337`. Claude source is not the GPT candidate. Reference review `review-v1/review.json`, scope/contracts and controls retained. Six hidden single-site mutants and final inputs in `test2/private/`.
- Inputs: fixed dev basic9/boundary45/wrap_reset42 cycles; final61/129/163, including two idle tails each. `test2/scripts/prepare.py::datasets` uses local `random.Random(699802)` for final_mixed; no provider seed is supplied. JSON files and hashes, rather than re-running generation, are authoritative.
- Arms: B′=spec/RTL/three dev observations/all400 raw counters/common compilation+development feedback; C′=B′+egg-derived groups/full guards. No A or P in this new pilot. Renderer `test2/scripts/feedback.py` is explicit allowlist. Candidate has six active/ok slots, readonly public pins, state≤8192bits, body≤16000bytes; arbitrary UVM/SVA and DUT edits are excluded.
- Budget: gpt-6.1-sol/low, each arm3 independent sessions×6 rounds,32000 input/8192 output tokens,120s request,one retry;≤one token-count request/attempt; compile60s, replay15s. Save exact prompts/calls/rounds; select last schema/boundary/compile-valid candidate, then freeze **all six** before final release. Hidden outcomes never feed repairs.
- Fixed raw denominator400=22line+24branch+16expr+338toggle. Fresh offline DUT observations include reset/init consistently; model rounds only replay observations, so raw coverage cannot improve. Original and stress forms are one IP, not two independent designs.
- Score: require complete correct-control replay with no alarms/unknown; score only oracle-confirmed observable fault/trace pairs; alarm at/after first reference violation. Verilator16/18 and Icarus15/18 eligible, all6 mutant types represented. Preserve2 unactivated M05 traces/simulator and Icarus M02 boundary unresolved. Distinct kills count once; unknown outputs never become PASS.
- Formal schedule: after freeze, each candidate two correct implementations×(bmc,prove,cover)+six mutant bmc=12 jobs. Z3, depth48,60s/job; initial reset and reset⇒no R/W. `cover` concerns active signals only; PASS not soundness. BMC finite PASS not full proof; TIMEOUT/ERROR/UNKNOWN retained. Decoded counterexamples go to frozen reference, not candidate-defined truth.
- E-graph: real egg0.11 bounded saturation; six binary rewrite checks; two mapped nontrivial groups/five separate source points91/161,96/129/179. Unsupported/else mappings explicit. Full developer dataset already covers those five points. No solver stimulus or final witness supplied to GPT.

## Track M phase2 — separately registered offline preparation

User subsequently authorized API-free test2 preparation on2026-11-04. `test2/configs/phase2_preflight_v1.json` through `phase2_preflight_v5.json` bind the saved evidence, deterministic first-candidate selection, public DUT, assumptions, fixed slot schedule and resource caps. No API calls/new DUT simulations; no old scoring changes. All early control failures and the v4 producer error are retained.

Latest v5: predeclared B′ rep1 only, six separate BMC48/10s jobs (60s total solver cap), two plumbing controls at3 steps/5s (70s total cap plus fixed process grace). Same assumptions/parameters as the frozen harness, `prep -flatten` removes irrelevant logic. P0/P4/P5 bounded PASS; P1/P2/P3 TIMEOUT. These are infrastructure observations, not B/C effects, unbounded proofs or new reference truth. See `docs/test2_phase2_preflight_2026-11-04.md` and `test2/results/phase2-preflight-v5/`.

`test2/configs/registration_v2_draft.json` is a future study contract with equal draft caps, fresh hidden faults/traces, independent Claude reference and every-round candidate snapshots. `live_allowed=false`; no executable entrypoint; task/spec/interface and formal schedule unset; all live gates false. Do not repurpose the frozen v1 runner for this draft. Bind a new registration/runner/live freeze only after one task passes offline feasibility and independent reference gates. No requirement here imports the original stimulus ordinary-unhit/B-before-C gate.

## Track M controller task — 2026-11-05

Concrete scope: `test2/configs/controller_task_v2.json`, `test2/tasks/axis_length_fifo_v1/`. Original verilog-axis revision48ff7a7e2ef782cf778d47910cf85835c64b1bce, byte stream, KEEP/ID/DEST/USER disabled, MIN4/MAX8, data/header FIFO32/8, input frames1..12bytes, independent data/status channels, synchronous reset cancellation. Direct-core status-stall FAIL and prior frontend/definition failures remain separate evidence. No original RTL edits.

Active reference contract: `public/specification_v2.md`, `observer_contract_v2.md`. Claude writes the checker; GPT does not patch it.50selftests/20independent controls/18correct traces plus fresh review yield scoped acceptance, not complete soundness. Reference frozen in `reference/frozen-v2/`; all unknown/diagnostic/reset-pre/continuity limits retained. Newhidden12faults×6traces×2simulators kept; each simulator53/72eligible pairs and11observable fault types, one unconfirmed retained. No candidate score yet.

Local formal qualification is11jobs/100s solver cap including two controls; selected three public interface properties pass bmc/prove/cover. Future candidate schedule is6slots×3modes×10s on correct source plus12faults×6slots×bmc×5s, total540s/candidate (common overallcap720), depth24/z3/flatten. No arm-specific retry/resource increase. BMC/cover/unbounded local proof remain distinct.

Shared candidate budget is3independent sessions×6rounds/arm, gpt-6.1-sol low,64k input/8192output,120s, retry1; new larger-hierarchy budget declared before new B/C outcomes. Source/state caps remain16000bytes/8192bits. Public-only B/C packets retain3168 raw counters; C-min adds4predeclared certified guard groups. Actual provider tokens and new ABI/runner/all-round-release gates remain pending; candidate live false. Never launch the old FIFO runner for this task.

User2026-11-05 explicitly authorized keeping the main staged Anthropic key through needed repairs/reviews until completion. A new adapter leaves the immutable old caller unchanged and uses per-call0600 copies. The reference task has completed; key cleanup occurred afterwards.5CLI role calls including the initial failure cost$3.714620 as reported, with all artifacts retained.

## Environment and recovery limits

[V] Local environment checked2026-11-04: Python3.13.9, OpenAI SDK2.54.0, Verilator5.050, Icarus12.0, Yosys0.70+post, SBY0.70, Z3 CLI5.1.0, Cargo1.99.0. Saved run versions: `test2/results/preflight-v2/versions.json`; current commands/exit codes: `docs/audits/migration_2026-11-04.json`. egg version is locked in `egraph/Cargo.lock`. Historical OpenTitan jobs used an isolated OSS CAD/Slang environment; do not assume the default Yosys reproduces all those frontends.

[P] Reliability and R0/R1/R2 recovery need their own registration, assumptions, fault-free controls and metrics. Hash/schema guards and replay logs alone do not establish agent diagnosis accuracy or recovery success. No new APIs/experiments are authorized by this summary.

## Controller B/C live v2 — authorized 2026-11-05

User authorized running matched B/C after new replay/snapshot/token gates. `controller_run_v2.json` and `controller_live_freeze_v1.json` bind a new scope; old freezes and Claude checker remain untouched. First actual count failed with zero candidate calls; common coverage dictionary re-encoding is exactly reversible and has no selection/truncation. Second count passed unchanged64k cap. Every real attempt is counted before generation; cap failures remain ungenerated, not successful trials.

All36 candidates including invalid/missing outcomes freeze before hidden scoring; selected final is last compile-valid, never best hidden score. Six stateless own-history sessions,3 per arm,6 rounds,low gpt-6.1-sol,64k/8192,120s,one failure retry. Simulation covers all frozen rounds; formal uses six selected finals only. Scoring requires no correct-control alarms/unknowns and an eligible pair with no candidate alarm before reference onset. Report12 raw/11 observable faults,106 eligible simulator-trace pairs, three predeclared strata, all-round cost-to-all11 and missing usage/not-reached states. A definite faulty-trace detection may coexist with explicitly retained unknowns.

Formal assumes initial reset, reset implies no source offer, blocked-source stability until reset, and1..12 accepted bytes/frame. Depth24,per-slot mode budgets and global720s cap remain matched. Reference-adjudicated reachable BMC witnesses differ from induction failures; cover/finite BMC/proof never pooled. Retain the staged OpenAI key through this concrete task, then clean it after report/audit completion.

### Controller live v2 completion

Completion artifacts: `test2/results/controller-live-v1/`, `controller-final-v1/`, `controller-report-v1/`, `controller-analysis-v1/`. All36 freezes precede final scoring.36generation/0retry,44count calls,1878181tokens; actual caps pass. All36 reach fixed-corpus11/11types and106/106eligible pairs at round1; raw12 and M08 unconfirmed remain. C mean tokens+6.91854%.

All540formal jobs retained:473TIMEOUT,31cover PASS,1BMC PASS,1prove PASS,33reference-confirmed mutant BMC FAIL,1unreached cover FAIL. Local proof is C rep3 P2 status-stall only. Both arm pooled fault unions8; per-session B0/8/0 vs C6/3/8 are descriptive, not complete soundness/general causal evidence. Correct-control acceptance remains finite. Source-obligation omission in C rep2 is exploratory and does not change scores. Reports/audits preserve full role/source/input boundaries, global caps and raw log hashes. No automatic rerun follows completion.

## Autonomous offline qualification v2 — 2026-11-05

Registration `test2/configs/controller_offline_qualification_v2.json` preserves v1 failed witness alignment and all previous freezes. It authorizes no API/model calls. Controls are explicit synthetic finite observations, frozen before all36 old candidate replays; independent checker labels9legal/17FAIL/3unknown/3invalid. Reference-accepted examples are not automatically physically reachable, so their alarms cannot alone prove DUT-relative unsoundness. Obligation control recall is not RTL coverage and never rewrites the registered mutant score.

Formal variants retain or remove output keep attributes with identical logic/legal-source assumptions; all inputs kept for strict transport decoding. Depth24,5s controls/known mutant anchor,10s selected probes;18jobs/150declared solver-seconds, overall360s. Probes disclose deterministic first B reset plus known positive C status-stall anchor; anchor selection is diagnostic, not outcome-blind C-effect estimation. v2 physical bridge verifies observed active/ok failure time rather than terminal native assert-report step. Missing/unknown/unsupported input/output or mismatched physical alarm stays unresolved. Dual simulators reconstruct actual outputs from literal inputs; no carried/fabricated terminal post.

After passing controls and physical reference anchors, all6finals×6slots×bmc/prove/cover use the cone profile,24steps/10s each,108jobs/1080solver-seconds, interleaved B/C order. No arm-specific retries, candidate edits or old status relabel. The single-command fresh reproduction repeats this local qualification on frozen programs; it is not a new LLM sample. Current tests are freshly executed separately from historical test counts.

`controller_done_abi_v1.json` is an offline-only prototype: trace_done exactly at finalpost, no extra DUT edge/input. It exposes finite evaluation termination, with independent check_rows unchanged. Unknown tails do not become PASS. A future trace_done=0 formal projection has safety-only scope. New live study remains unregistered/unauthorized by this prototype.

### Offline acceptance and closure

Full fresh CLI actual command/output: `controller_offline_pipeline.py --output test2/results/controller-offline-e2e-fresh-v1 --formal all`,826.336s;126local formal jobs and63separate current test2 tests. Explicit evidence-reuse invocation remains separately labeled. Raw logs/versions/source/native status are bound in acceptance.json; component timing overlaps wall timing and must not be added twice.

`controller_witness_replay_v1.json` registers all33original BMCFAIL witnesses, no outcome-based subset. It ran after timed checks, physically reconstructed literal inputs in both simulators and reproduced actual candidate alarms; all33independent checker verdicts FAIL.66physical runs/548cycles and33monitor replays/274cycles are diagnostic costs, not new independent LLM trials, RTL coverage gains or old formal reruns. All old scores/timeouts remain unchanged.
