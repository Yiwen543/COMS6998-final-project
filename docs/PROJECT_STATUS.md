# Project status — 2026-11-04 (America/New_York)

**Current outcome:** original stimulus trials have not established a stable general C-over-B benefit. The separately registered `test2` monitor pilot is complete: fixed-trace detection ties, C costs more tokens. This is limited evidence, not a refutation of E-graphs. The user selected next-stage fixed-stimulus monitor preparation; the new live task is not yet frozen. [S1,S2,S3,S4]

Evidence labels: **[V]** directly inspected/recomputed (original entries: migration audit; latest preparation: explicitly dated below); **[R]** saved report/run evidence inspected, experiment not rerun; **[C]** visible conversation; **[P]** proposed; **[?]** not established. All paths below are repository-relative.

## Latest preparation — 2026-11-04

[V,C] The user's subsequent instruction continues the monitor question under fixed stimuli and matched resource budgets. `docs/test2_phase2_preflight_2026-11-04.md` records a fresh saved-evidence/hash audit and new offline infrastructure calibration, not a rerun of v1. Old3486 freeze members and reference/candidates/scores remained unchanged. New tests:7/7; old25-test suite not rerun.

[V] Separate phase2 preflight registrations v1–v5 retain all failures. Six isolated slots with hierarchical prep all timed out. Flattened48-step/10s-slot BMC on the predeclared saved B′ rep1 candidate completed P0/P4/P5 only; P1/P2/P3 still timed out. Latest8 jobs measured38.683s; no new prove/cover/model/DUT simulation. Historical31 TIMEOUT remain unchanged. See `test2/results/phase2-preflight-v5/report.md`; early control/producer failures remain in v1/v2/v4.

[P] `test2/configs/registration_v2_draft.json` states the next fixed-input monitor contract, roles, matched caps, fresh hidden corpus, every-round freeze and stop gates. It is explicitly non-live with no selected DUT/spec/interface or formal schedule. Next minimum: qualify one multi-cycle request/response task and relevant semantic mapping before APIs. Original stimulus difficulty gates do not silently govern this task; R0/R1/R2 remain separate proposed work.

## Goal and relation to proposal

[R] The formal proposal asks whether semantic E-graph feedback improves RTL verification coverage and Token ROI: A=text/logs, B=raw coverage, C=B+normalized equivalent guards. It proposes CVDP Design Verification/AutoEval-ECov, coverage, Pass@1, tests/calls/tokens. See [proposal](../project_background_reading/E_Graph_Augmented_Tool_in_the_Loop_Agent_for_High_Coverage_RTL_Verification.pdf), pp.1–2. `project_proposal_cn.md` is an earlier multi-topic draft, not the final contract.

[R,C] The implementation first restricted GPT to JSON stimulus, then the user separately authorized `test2`: fixed stimulus, GPT candidate SV monitors, independent Claude reference. This extends verification-quality evaluation but is **not** the same coverage endpoint or an official CVDP Pass@1 measurement. [S1, S5]

[?] Two milestone PDFs differ: `../milestone1.pdf` adds reliability and R0/R1/R2 recovery; `output/pdf/milestone1.pdf` has the older next-steps section. The parent page is visually readable, but its text layer includes old duplicate text. Submission authority is unconfirmed; neither file was edited. Hashes and reading scope: [migration audit](audits/migration_2026-11-04.json).

## Architecture now

| Stage | Implementation/evidence | Boundary |
|---|---|---|
| Pinned fixtures/contracts | `examples/`, `configs/`, provenance/lock files | Different task IDs or syntax variants are not automatically independent IPs |
| Typed extraction and mapping | `scripts/typed_predicates.py`, `slang_guard_adapter.py`, `hierarchy_semantics.py`, `semantic_candidate_scan.py` | Supported subset; unresolved aliases/maps explicit; Yosys/Slang are frontends, egg is not an SV parser |
| Actual equality saturation | `egraph/src/bin/guard_proofs.rs`, bounded Runner, explanations, AstSize; Z3 checks in scanner | Two-state claims with source and event context; not merely an AST pretty-printer |
| Original stimulus loop | `scripts/pilot_model.py`, per-IP runners/JSON drivers, Verilator raw counters, independent checkers | Exact Responses model; fixed checker; cumulative replay cycles counted |
| Independent reference roles | `test2/scripts/reference_role.py`, existing role-specific Claude scripts | Claude CLI with API credentials; isolated author/fresh reviewer; agreement is not proof |
| New property loop | `test2/scripts/runner.py`, `feedback.py`, `monitor.py` | Fixed observations; six passive SV active/ok slots; cannot modify DUT coverage |
| Final evaluation | `test2/scripts/final_score.py`, `score.py`, `formal_witness.py`, `report_live.py` | Candidate freeze before hidden scores; reference eligibility; separate formal statuses |

[V] Audit indexed 259 root Python scripts and 62 root test modules, plus 20 test2 scripts and 4 test modules. It reviewed key paths and reports, not every line of every file. [migration audit](audits/migration_2026-11-04.json)

## Progress and results

| Work | Status and measured conclusion | Evidence |
|---|---|---|
| Arbiter/FIFO/timer pilots | [R] Integrated A/B/C; early saturation. Arbiter repeated violations include two categories (override and reset), not tens of thousands of distinct bugs | `results/step1/REPORT.md`; `results/pilot_live_20261020/REPORT.md`; `results/fifo_live_20261020/REPORT.md`; `results/ttc_live_20261020/REPORT.md` |
| Queue milestone, GPT-6 Sol | [R] C reached target earlier in 2/6 index-matched trials, tied 4/6; final coverage tied. One IP/two syntax forms, no significance or mechanistic attribution | `docs/milestone1_result_report.md`; `results/queue_bc_gpt6sol_20261026/` |
| Divider and synthetic sfifo A/B/P/C | [R] No primary C-over-B advantage in these fixed scopes; divider P was byte-matched, later FIFO P used token matching | `docs/divider_abcp_result_2026-10-30.md`; `docs/sfifo_stress_abpc_result_2026-10-30.md` |
| Minimal C packaging ablation | [R] All 12 sessions target round5; C-min saves15.31% vs C-full but costs2.95% more than B-compact. Not a new IP replication | S3 |
| Natural/multimodule screens | [R] UART/SPI saturated; I2C equivalents already hit by ordinary operations; selected AXI DMA/Flash scopes lacked targets/dependencies. WBXBAR ordinary screen failed. No two independent natural IPs certified through the original full gate | `docs/next_ip_screen_2026-11-03.md`; `docs/spi_semantic_repair_2026-11-04.md`; `docs/i2c_read_preflight_2026-11-04.md`; `docs/real_parent_screen_2026-11-04.md`; `docs/transaction_recovery_screen_2026-11-04.md`; `docs/wbxbar_conditional_index_2026-11-04.md` |
| SPI role-separated checking | [R] Independent controls drove Claude repairs; later safe-driver B failed admission. Two failure traces attributed to one probable same-CS configuration discrepancy, not certified multiple DUT bugs | `docs/spi_failure_attribution_2026-11-04.md` |
| WBXBAR checker and fresh B/C | [V,R] Saved audits pass; all6 reach17/17 raw targets at round1, all6 functional outcomes unresolved (86 final unknown records,0 failures). C total tokens+8.03%; transient toggle gains retained | S2; `results/wbxbar_reference_bc_20261104/live-audit-v1.json`; `live-accounting-audit-v1.json` in same directory |
| test2 fixed-stimulus monitors | [V,R] 36 live calls,0 retries,744,708 tokens. B′/C′ each3 reps, all6/6 observable mutant types, no correct-control alarms. C mean tokens+6.523%. Formal:12 cover PASS,29 mutant counterexamples,31 TIMEOUT; no completed correct-control proof | S1,S4,S5 |
| Agent verdict reliability | [P/partial] Independent checker/control infrastructure and test2 fault detection exist; a full blinded agent-verdict-vs-formal-reference matrix is not established | parent milestone p.2; S1; original request in conversation |
| Recovery R0/R1/R2 | [P] No registered/completed comparison located in configs/scripts/tests during this audit. Hash freezes/replay are not selective rollback evidence | parent milestone p.2; migration audit |

## Open limitations and next decision

- [V,R] test2: one synthetic redundancy FIFO, six faults, three reps, no length placebo; all five semantic source points already hit by development `boundary`. Finite controls and all-correct simulation do not prove oracle/monitor soundness. 24 correct-control formal tasks timed out. [S1,S4]
- [R] WBXBAR unresolved cancellation/ERR attribution and property exclusions remain; do not convert zero alarms into PASS. [S2]
- [R] Restricted typed extraction still has unsupported constructs; eligibility and counter-mapping failures are not model-effect findings. [screen reports above]
- [P,C] The user selected stronger fixed-stimulus monitor evaluation. Qualify and freeze its concrete task independently of new B/C outcomes; do not change an old target/budget to create C gains. Natural stimulus qualification and the reliability/recovery matrix remain separate work.
- [?] Authoritative submitted milestone, current deliverable/deadline and permission to commit/sync this working tree need confirmation. Remote state was not fetched.

## Evidence entry points

- **S1:** [test2 Chinese result report](../test2/results/live-report-v1/report.md), `endpoints.csv`, `formal.csv`, `fault-pairs.csv`, `comparison.json` in that directory.
- **S2:** [fresh WBXBAR report](wbxbar_reference_bc_2026-11-04.md).
- **S3:** [minimal C report](minimal_c_result_2026-11-03.md).
- **S4:** `test2/results/live-report-v1/audit.json`, `final-verification.json`; `test2/results/live-final-v1/scores.json`.
- **S5:** `test2/configs/registration_v1.json`, `phase1_addendum_v1.json`, `live_freeze_v1.json`, `test2/AGENTS.md`.

Old status content is preserved without loss in [pre-migration snapshot](archive/migration_2026-11-04/PROJECT_STATUS.md). Detailed historical repairs remain in [AGENT_HANDOFF.md](AGENT_HANDOFF.md); load only relevant slices. Current restart instructions: [HANDOFF.md](HANDOFF.md).
