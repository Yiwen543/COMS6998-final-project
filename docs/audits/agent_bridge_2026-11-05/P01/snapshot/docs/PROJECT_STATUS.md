# Project status — 2026-11-05 (America/New_York)

**Current outcome:** the USD20-authorized trace_done live run has completed36generations/36counts/0retries and released all36rounds.35candidates compile; B rep1 round4 remains invalid (P5 description401>400), with normal next-round recovery. Saved-response replay and both fresh grades are complete; fixed formal evaluation is in progress. Raw-evidence audit/final report remain pending. Historical B/C results, negative findings and old frozen scores remain unchanged.

Evidence labels: **[V]** directly inspected/recomputed (original entries: migration audit; latest preparation: explicitly dated below); **[R]** saved report/run evidence inspected, experiment not rerun; **[C]** visible conversation; **[P]** proposed; **[?]** not established. All paths below are repository-relative.

## Active generation under user USD20 authorization —2026-11-05

[C,V] User authorized<=20 instead of proposed35. New budget-v2 keeps full36normal/max72attempts,64k/8192caps,model/low/sessions/data/prompts/targets. Standard+implicit30mcache confirmed2.5USD/Minputwrite(notadditive),max72generationreserve17.41824;17.5generation+2.5countfees=20. Newprofile registered/frozen/audited,11SDKtests/36mock/replay/independentgradereusepass. Keysreused. Live_v2starting;checkactualprocess/ledgerbeforeanyrerun. No moreapprovalneededwithin20. Continuegeneration→36freeze→replay→grade→fixedformal→analysis/audit,retainingallunknown/negativefindings. Source/currentreport `controller-done-generation-preparation-v2/`;old35profileunexecutedandpreserved.

[V] Live generation finished824.684s:1475813input+78479output=1554292tokens (5165reasoning subset,155022cached-read subset,1320683cache-write tokens). Max43871input/3087output; every actual input equals its provider pre-count. Token-rate estimateUSD4.1022157 for generation only, not invoice; count fees and final bill unknown. Conservative36-call reserve8.70912+count allocation2.5=11.20912, below20. Native development compilation70calls versus71reportedattempts, because static validation rejects the401-character description before tools.105development monitor replays/8050cycles/0newDUTsimulation. Evidence `controller-done-live-analysis-preparation-v2/usage-checkpoint.json`. API-free postprocessor `controller_done_live_post_v2.py` continues replay→two grades→540fixedformaljobs→raw audit; its progress is in controller-done-live-post-v2/.

[R] Both fresh grades each executed5670monitor replays/1184540cycles. Final six candidates all pass18correct controls and detect11/11observable types; safety106/106definite (fullyresolved68exceptBrep2=66), response20/20, input0/10. All10input-eligible pairs overlap earlier safety/referenceunknown and have both earlier and marker alarms, so0/10is eligibility-confounded, not evidence of absent end checks. Btokens740643/C813649,C+9.85711065%; firstall11roundsB2/1/1,C2/2/1. B rep2 has12candidateunknownpairs,10overlapreferenceunknown =>40totalunresolved instead of38. Keep all first-round control failures/oneinvalidround. Formal540schedule running; no overall C conclusion before complete audit.

[V,P] New API-free input-isolation diagnostic registered before physical runs (`controller_done_input_isolation_v1.json`, seed6999401/150cycles/four-siteCOMPOSITE RTLcontrol),4build/4sim/24replay caps,0API. It is post-hoc obligation qualification, not a natural new mutant/independentLLMsample or oldscore update. Physical execution waits until timed formal schedule ends. Current checker necessarily emits short-tail unknown for any final offeredvalid, preserved with definiteFAIL; conditional Claude scope/author+freshreview packets prepared butnotcalled/authorized.

The following sections are retained historical snapshots. Their pending approvals and zero-generation statements describe those earlier preparation stages, not the current run.

## Historical generation readiness —2026-11-05, qualified; USD35 proposal pending at that time

[V] `controller-done-generation-preparation-v1/report.md`/audit.json/qualification.json/completion.json. ActualHEADc25180848ebfe9a1f49da0aa5f579cac913e6428. Scope-v4ACCEPT_SCOPE,noadapter/oraclechanges;secondreviewunused/forbiddenafteracceptance. CumulativeCLIreportedUSD0.532023,8counts/feesunknown,0newGPTcandidate/author. Keysremain0600,norestaging.

[V] Generationconfig/freeze900members/all10gatestrue,permissionseparate. Model/APIguards: gpt-6.1-sol/low/Standard,64k/8192,120s,SDKretry0,onefailure retry,72counts+72generationmax,exactactualusage/subsets/model/tier checks,resourcehalt→remainingNOT_RUN/all36freeze.10offlineSDKguardtestsPASS;36currentmock/replayeach72compiles/108devreplays/8280cycles;5832legacyloggradingreuse/all36caseclassificationsmatchacceptedcore. NoAPIgeneration/networksmokecall. Alloldfreeze/scoreevidenceintact.

[P] Concretecandidate-generation-v1proposal requests newstageUSD35=30generation+5countfeereserve,normal36/max72gens+max72counts;maxconservativetokenreserve28.93824,notinvoice. ExistingUSD9preflightdoesnotauthorizeit. Newgenerationgrantabsent/liveblocked. Afterapprovalreuseexistingkey,executeallgeneration/freeze/replay/grade/formal/reportwithoutordinaryprompts. Formal540jobsshortprojectioncannotprove128completion;allunknown/timeouts/N10/rawdenominatorsretained. B/Cwholepackageonly,noplacebo/puresemanticclaim. NoC-benefitresultyet.

## Shared grading v4 — 2026-11-05, offline verified; independent review pending

[V] Latest report/audit: `controller-done-grade-v4-acceptance/`. Scope-v3 review returned LIMITED_SCOPE,USD0.190426; it confirms earlier5fixes/no oracle revision, identifies new adapter failure-path/report issues. Cumulative3CLIinvocations/reportUSD0.342502,8OpenAIcounts; count fees unknown. No candidate generation/author. Keys retained0600; use require_escalated network.

[V] New shared case/grader v4 registered before fresh/reuse runs. Fixed162-case inventory, non-graded carry, row SHA/cycle/marker/raw-bit binding, full unresolved and explicit per-type FAIL-with-unknown, split ordinary/end-marker credit paths. Fresh5832replays/1218384cycles(83.837s) equal reuse5832logs/0newreplays(18.535s) across36/allcases;9failure-injection tests pass. Initial per-type field-name failure retained and fixed before registration.148HEXvectors match162qualified records. Old3486/212/239 freeze members/two scores/offline-v4 evidence intact; no old test/formal rerun. Ordinary safety0/106, marker-only10,response20/20,input10/10definite0resolved;38unknowns,N10unobserved/raw12/144 remain. No LLM/C-effect claim.

[V,P] Actual token gate still passes B36944/59460,C40573/63089; candidate prompt hashes unchanged. Fresh scope-v4 review packet/caller ready, grantv4 absent. Proposal requests user choice of one or up to2 bounded infrastructure reviews, maxUSD1.80each/600s/total3.60; second only after first LIMITED_SCOPE/no oracle revision and offline repair/gates/new packet. No author/count/generation. Cumulative0.342502+3.60+countreserve5=8.942502<=original9. Existing keys reused. After acceptance, prepare current live freeze/generation checks before separate paid generation request.

## Trace-done study integration — offline accepted2026-11-05; paid preflight pending

[V] Actual current HEADmainc25180848ebfe9a1f49da0aa5f579cac913e6428, initially clean; historical00e0dd9 is not current. New report `test2/results/controller-done-acceptance-v4/report.md` / acceptance.json / resource-ledger.json / target-summary.json. New configuration `controller_done_study_v1.json` and task `axis_length_done_v1` preserve old DUT/spec/Claude checker and all3486/212/239parent members/two old score hashes.

[V] New3dev/6hidden seeded data and12new mutation hashes (no overlap with old mutant hashes) sealed before candidates. Actual26DUTbuilds,162physical runs/33844cycles;18correct PASS/9dual agreements. Raw12types/144fault pairs,11observable types;N10 unobserved retained.38fault-pairs contain oracle unknown context. Fresh tool versions saved. Rawcoverage3168=110line+176branch+248expr+2634toggle;1970unhit acrossnewdev. No newly rerun semantic proof claim.

[V] New trace_done prompt/compile/development/36round freeze/mock/replay/independent score fully integrated; finalpostonly,noextraDUTedge. Each mock/replay108devreplays/8280cycles; each independent grade5832replays/1218384cycles. All36prompts/sources/feedback and grading match. Final arm-blind plumbing detects3types, only2fullyresolved; all6sessions NOT_REACHED(all11). Safety10/106definite(0resolved),responsecompletion20/20,inputcompletion10/10definite(0resolved). N01unknown context retained. No LLM/effect/tokenROI claim.

[V] New540job mock formal schedule completed298.276s:504PASS/36unreachedcoverFAIL. trace_done0 short safety projection is empty for end-only plumbing and cannot prove128cycle completion. Fixed cone profile qualifies from full-depth true/false and physically ref-confirmed mutant controls. Controls v2 retain2TIMEOUT, current v3retain1TIMEOUT; v1 Python result assembly failure retained after1nativePASS. Total555newlocal jobs508PASS/44FAIL/3TIMEOUT;12extra physical witness runs/60cycles. Remaining overall budget now propagates through physical tools; new unit plus7current controls verified without pretending to rerun540.

[V] Current test2 suite freshly76PASS `controller-done-tests-v4.log`. Independent v4audit checks11664gziplogs/2436768scorecycles, rawactive/ok bits, physical HEXvectors/nativeformalstatuses, current/historical execution source and parent freezes. KnownIcarus$finishrootpathdifference normalized explicitly, original SHAs retained. Initial unit/assembly/audit failures and all versions preserved. New single-command reproduction wrapper prepared; its component commands ran, wrapper itself not yet called as one fresh invocation.

[P,U] Concrete preflight `test2/tasks/axis_length_done_v1/qualification/api-preflight-v2/proposal.json`:1Claude-opus-5-5 independent scope review maxUSD4/600s (requested<=3000outputtokens, no separate hard token cap),4OpenAI gpt-6.1-sol input counts/0generation,64kqualification cap; endpoint pricing not explicitly listed, reserveUSD5, proposed totalUSD9. Not approved/called; no keys present/read. Scope-v2 review and conditional author packets prepared; oracle unchanged. If review exceeds current scope, separately authorize Claude new-version author+fresh review. No generation authorization/livefreeze;36..72candidate requests remain closed pending review/count/currentfreeze/paidapproval. B/C would estimate whole feedback package, no placebo/puresemantic claim. No agent install/commit/push.

## Autonomous qualification plan — accepted with scope 2026-11-05

User authorized sustained reversible local work; completed the next minimum task, bridge repair, formal diagnostic, balanced replay, end-marker prototype, source/coverage/semantic audit, complete CLI reproduction and independent acceptance without new API calls. Evidence: `test2/results/controller-offline-e2e-fresh-v1/report.md`, `acceptance.json`;63fresh test2 tests passed. No new model sample or old score rewrite.

| Phase | Status | Actual acceptance evidence |
|---|---|---|
| Audit | Verified | main00e0dd9...,old3486/reference212/controller239 members match; tools recorded, keys absent; migration531functional files and retained history intact. |
| Obligation controls | Completed |32independent checker labels;all36frozen candidates/1044replays/145152cycles; old completion/ABI gaps observed; synthetic controls distinguished from physical reachability and RTL coverage. |
| Formal qualification | Completed with unknowns retained | v1failed bridge preserved,v2strict actual-alarm dual-physical/reference gate passed;108balanced correct-source jobs50PASS/56TIMEOUT/1UNKNOWN/1coverFAIL. B6/C3single-slot prove completions under this profile do not imply stronger properties/general benefit. |
| Offline end-to-end | Completed and freshly reproduced | Full one-command `--formal all`826.336s,126new formal jobs;5882QF_BV queries/281rules/real egg;1052raw replay logs and145728cycles verified.63current test2 tests pass. |
| Original witness closure | Completed | All33original BMCFAIL witnesses physically reproduce and independent referenceFAIL;66physical runs/548cycles, old labels unchanged. |

Verified implementation includes the existing recorded live B/C flow, immutable releases, independent reference evaluation and the new runnable local qualifier. Partial: no whole monitor soundness, end-marker remains offline prototype. Planned/not executed: newly registered live end-marker/placebo study. Unknown: general causal C effect,current API connectivity/USD costs,remote/submission status. Future paid work requires a concrete new proposal/authorization; no paid stage is pending.

Raw coverage is3168actual Verilator counters (110line/176branch/248expr/2634toggle), with1989unhit across fixed development inputs; no behavioral equivalence class is counted as RTL coverage. Existing main simulation comparison remains11/11ties/C tokens+6.919%. Representation-sensitive formal results limit robust causal interpretation of the original local C signal.

## Controller live stage — completed 2026-11-05

[V] Read `test2/results/controller-analysis-v1/analysis.md` and `controller-report-v1/report.md`. New immutable freeze239 files, old3486/new-reference212 matched. Nine new tests passed; all36 saved-response replay matches;5832 scoring logs/1124640cycles verified. No new DUT simulation. Old25-test suite not rerun.

[V] Actual token gate v1 failed before generation. Identical lossless dictionary re-encoding retains all3168 counters/RTL/spec/observations and unchanged C groups; count v2 passed. New `controller_run_v2.json` retains parent configurations and failed evidence.36generation requests/0retries,44count requests,1878181tokens. All actual usage caps pass; no hidden scoring before all36 snapshots froze.

[V] B/C each3×6 rounds: all11/11observable types and106/106eligible pairs,0correct-control alarms/unknown. Boundary4/4,handshake3/3(4raw),payload4/4;12raw faults retained including unconfirmed M08. Cost-to-target round1 for all6; C mean input+output tokens+6.91854%, with no simulation detection gain.

[V] Formal540jobs, no skipped jobs,3626.314s measured wall.473TIMEOUT;31activation cover PASS;1BMC24 PASS;1prove PASS;33reference-confirmed mutant counterexamples;1unreached cover. C rep3 P2 proves status-stall stability under fixed assumptions, not full monitor correctness. Per-session confirmed mutant types B0/8/0 vs C6/3/8, pooled union8/8. Descriptive formal improvement is limited by3reps,whole-package/no-placebo comparison, fixed B-then-C formal order and wall-time sensitivity.

[V,P] Source-only diagnosis finds C rep2 omits128-cycle completion checking despite full score. Keep primary scores unchanged. Next minimum is API-free obligation/negative-control qualification and a small fixed-control formal cone/witness diagnostic before further paid B/C. No new experiment launched. Key retained throughout this concrete task, with final cleanup recorded after verification. HEAD00e0dd9..., no agent commit/push/fetch; preserve dirty work.

## Earlier controller qualification — 2026-11-05

[V] Final local HEAD is `00e0dd974d3a910b37de3c029f61e7beeb7953fd`. Two commits (test2_phase1/test2_phase2) appeared during this session; the agent did not run commit/push/fetch. New completion artifacts remain partly untracked. Artifact hashes, not an assertion that all files belong to HEAD, identify the actual run; remote live state is unverified.

[V,C] The requested minimum task is complete: original verilog-axis frame-length-adjuster FIFO controller, fixed byte interface/specification, MIN4/MAX8, data/header FIFO32/8, independent data/status pressure and reset flush. Direct-core scope rejected on a status-stall counterexample reproduced by both simulators; no DUT/checker weakening. See `docs/test2_controller_qualification_2026-11-05.md`.

[V] Selected scope:168 combinational definition checks certified;9 nontrivial groups;142 mapped/6 unresolved targets;3168 raw counters retained. Local reset/output-stall/status-stall bmc/prove/cover PASS (11jobs including positive/negative plumbing controls,24.492s), not whole-design correctness. New3dev/6hidden correct traces agree in both simulators.

[V,R] Claude-only reference authorship/repair and fresh review completed. Contract-v2 reference `test2/tasks/axis_length_fifo_v1/reference/frozen-v2/` has50selftests/20independent finite controls/18correct traces and scoped acceptance, with conservative unknown/diagnostic/reset-pre/continuity limits retained.5CLI role calls including failure reported$3.714620. User authorized key retention between calls; the reference task finished and its main staged key was then cleared.

[V] All12 new single-site faults and144fault/trace/simulator outcomes retained. Each simulator has53/72 eligible sampled violations,11observable fault types; one has no reference-confirmed violation on this fixed corpus. These are eligibility data, not generated-monitor detection scores. No new B/C call or C advantage measured.

[P] Next minimum: new passive-monitor ABI/replay/runner boundary and every-round release tests, actual provider token-count check, then a new live freeze. Shared budget draft uses64k input for this larger original hierarchy, equal across arms; C-min adds4 certified groups, all selected source points already hit in development boundary traces. No placebo/pure-semantic causal claim. Candidate live remains false.

## Earlier preparation — 2026-11-04

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
