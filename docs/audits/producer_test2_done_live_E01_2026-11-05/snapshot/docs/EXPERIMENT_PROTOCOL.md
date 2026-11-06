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


## Trace_done controller study v1 —2026-11-05, offline accepted; API closed

`test2/configs/controller_done_study_v1.json` is a new preregistration before new physical measurements, not a revision of old freezes. Identical DUT/spec/Claudechecker/source-counter identities; new seeded3dev/6final actions and12newsingle-line faults. evaluation-freeze sealed prior to candidates. Observer metadata trace_done0everypre/postexceptfinalpost1, no extra DUT edge/input. Dev32/final128 minimum drain tails keep existing checker meaning. Scope reuse requires new independent Claude review before paid candidate stage; GPT never patches oracle.

Report sampled presented-valid safety separately from end-only response debt and final unaccepted input. For safety, no candidate alarm before first independent reference failure; response completion requires finalpost alarm and none earlier. Input definite obligation is separate and may overlap safety; oracle unknown context always retained. Full resolved detection requires complete replay, no oracle/candidate unknown plus no correct-control alarm/unknown across18physical controls. Raw12faults/144pairs remain,11observabletypes/106safetypairs/20responsecompletionpairs/10inputcompletionpairs derived from pre-candidate physical corpus, not C results; categories overlap. No synthetic control becomes RTLcoverage or physical unsoundness evidence. Targetall11 observable types retains NOT_REACHED/unknown costs; never adjusts to C performance.

B=complete raw feedback; C=B+verified E-graphpackage; shared fields identical andlossless, fixedmodel lowgpt-6.1-sol,3ownhistorysessions/arm×6rounds,6slots,16000bodybytes/8192state,64kinput/8192output,120srequest,1failure retry. Actual counts required before generation and perattempt; failures retain costs/missingusage. No placebo, so whole-package comparison only. All36valid/invalid snapshots release before hidden grading; lastcompile-valid selection, no hidden feedback.

Short formal projection trace_done0, depth24/z3/flatten; cone fixed by full-depth infrastructure controls and dual-physical reference anchors.6slots×3modescorrect10s,12faults×6BMC5s =>90jobs/540solverseconds/final,720soveralladmission and remainingdeadline propagated to physical compile/sim/replay. Interleave B/C; no preferential retry/profile selection. FiniteBMC/cover/prove/physical costs separate. End-only activation is expected unreached here; no128cyclecompletionproof. Current540mockjobs504PASS/36coverFAIL only qualify plumbing; no model/effect estimate.

Offline final audit/report `controller-done-acceptance-v4/`:76currenttest2tests,11664rawscorelogs,actualvectors/bits/native statuses and oldfreeze/scorehashes. Component commands ran; new single-command wrapper notyetinvoked asonefreshreproduction. Pending paid preflight proposal `axis_length_done_v1/qualification/api-preflight-v2/proposal.json`:1Claude scope review<=USD4 plus4OpenAIcountcalls/0generation(reserveUSD5, countfeeunconfirmed), totalUSD9proposed. No paid authorization or newlivefreeze exists. Conditional Claude author packet requires separate authorization ifreviewfinds genuineout-of-scopeoracleissue. Hidden terminal staging only afterapproval; retain same key through stage includingfailure, cleanup atstagecompletion.


### Paid preflight v1 failure and bounded v2 recovery proposal

User approved1review/4counts withinUSD9,not generation. OneCLIreview failedENOTFOUND withreportedUSD0/input0/output0/no verdict; preserveUNKNOWN/FAILED. Fouractual counts B44022/66538,C47651/70167(initial/history),bothhistoryover64000. No spending/countretry authorized by those failures; alloriginalattemptslotsconsumed. Never labelpayloadlengths generationusage or unreportedcountfeesUSD0. Keys remain0600 through unresolvedqualification/failures as userrequested.

New `controller_done_prompt_v2.json` only changes shared lossless columnserialization, before anyadditionalpaidcall. Allsource/spec/checker/counters/observations/semanticgroups/seeds/targets/caps and same16kbody+6×400descriptions+18khistorystress stay fixed. Bothpacketrestorations canonicalJSONexact. New36mock/replay and5testsqualifycodec/plumbing; allprograms identicalprior mock,gradesreusedexplicitly,noindependentLLMtrial/newscoreclaim. ActualnewtokensUNKNOWN. Proposedrecovery grantv2 requiresadditional1ClaudeCLIreview(samepacket,elevatednetwork)+4counts,combinedUSD9ceiling,countfeesstillunconfirmed. No newgrant/request exists; originalnegativegatepreserved.


### Recovery counts and Claude-informed scoring v3

RecoveryfouractualcountsPASS(B36944/59460,C40573/63089),sameprobe/64kcap/payloadschema. ReviewLIMITED_SCOPErequiresadapterchangesbutnooraclerevision;reportedUSD0.152076(firstfailedCLIreported0);countfeesunknown. Noacceptedfullreview/livegenerationclaim.

New`controller_done_scoring_v3.json`registeredbeforefreshgrades/controls. Safetycreditrequiresordinary(non-finalmarker)sampleat/afterreferenceonset,noearlieralarm;marker-onlysignalkeptseparatelyanddenominatorsunchanged. Finiteinput/responsecreditrequiresfinalpostalarmandnoearlieralarm,explicitANY_SLOTUNATTRIBUTEDcaseeligibilitystrata,notmonitorcategoryproof. Per-typeoracleunknownco-presencepreserved. Newwitnessreportsreferenceprefixthroughpost(S-1)separatelyfromreproducedpre(S)selectedalarm;no genericcandidatefalsealarm/selectedalarmconfirmationwithoutsame-sample/categoryreference. Referencefailures/unknowns/positions/categoriesretained;noGPToracleextension.

Freshgrader5832replays/1218384cyclesmatchtwoexistingsealed-logrescoringpathsall36/all5832casemetrics;new6testsPASS/7controlsqualifywith2TIMEOUTretained. Oldgradesunchanged. Newordinarysafety0/106forend-onlymock,separatemarker-only10;response20/20,input10/10definite0resolved/rawunknownsunchanged. NoLLM/effectproof. Candidatepromptsunchangedsoactualcountsremainvalid,perattemptcountstillrequired.

Nextproposedpaidstageonly1additionalfreshclaude-opus-5-5scope-v3review,CLIhardUSD3.80/600s,requested<=3000outputtokens(nohardtokencap),0count/generation/author. Reported0.152076+max3.80+countreserve5=8.952076<=original9. Grantv3absent;explicitadditional-invocationapprovalrequired. Existingkeysretainedthroughunresolvedpreflight;useelevatednetworkwithoutTLSdisable.


### Shared grading v4 and bounded review continuation

Scope-v3 review LIMITED_SCOPE confirms earlier fixes/no oracle change, identifies failure-path/reporting gaps. New scoring_v4 preregistration uses one shared case/binding/summary core for fresh/reuse. Keep all162 planned cases, including missing references/candidates/saved results; carry non-graded records. Check file/canonical row hashes, cycles and final marker; raw evidence mismatch stays unresolved. Both paths explicitly report FAIL-with-oracle-unknown per type, full unresolved totals and ordinary-versus-unattributed-end credit paths. Nine injection tests and fresh5832replays/1218384cycles vs5832 reused logs agree acrossall36/allcases; old evidence unchanged.

Further proposed review allowance: user may approve one or at most2 fresh reviews, each maxUSD1.80/600s/no tools, total3.60. Second conditional on first LIMITED_SCOPE with adapter changes/no oracle revision and completed versioned offline repair/tests/audit/new linked packet; never after acceptance, no automatic transport retry. Scientific inputs/targets/caps unchanged. No author/count/generation allowed. ReportedCLI0.342502+max3.60+countfee reserve5=8.942502within original9; actual count fees remain unknown. Additional request-count approval still required; keys retained through unresolved preflight.


### Accepted scope and generation v1 readiness —2026-11-05

Scope-v4 independent review ACCEPT_SCOPE/no required adapter/oracle changes,USD0.189521. Do not use the conditional second review slot after acceptance. Four low diagnostics remain explicit; fixed sealed inventory162keys is unique. Cumulative CLI reported0.532023;count fees unknown. Accepted grader/witness unchanged.

New generation registration/freeze binds900inputs/evidence,readiness only. B/C3sessionsx6rounds,gpt-6.1-sol/low,service_tierdefault(Standard),in_memorycache/storefalse,officialendpoint,64kinput/8192output/120s,SDKretry0,onefailure retry. Normal36/max72generation,max72exactprecounts. Persistentdispatch ledger,actualusage/subset/model/tier verification; returned contract violations haltallfurtherAPIrequests,remainingroundsNOT_RUN/frozen. Missingfailedusage neverzero. Actualinputcountpayloadsunchanged/B36944/59460,C40573/63089;perattemptcountsmandatory.

TenofflineAPIguardtests,current36mock/replay/sourcefeedback equality,independent5832legacyloggrade reuse andoldfreeze/scoreauditspass. No realcandidategenerationyet. NewproposalUSD35(30generation+5countfeereserve) requires separate explicitgrant; oldUSD9preflightnotreused. At checkedrates localreserve0.40192/gen/max28.93824,notproviderinvoice. Full36freeze beforehiddengrading,6finalsx90shortformaljobs,720sperfinaldeadline;allnegative/unknown/notreachedresultsandcostsremain. Whole Cpackage comparison only, no tokenplacebo or puresemantic causalclaim. Existingkeysretainedthroughgeneration/audit/evaluationincludingfailures,withoutrepeatedstaging.

## Candidate generation budget v2 — authorized and running, 2026-11-05

The user explicitly authorized this stage at <=USD20. New generation_v2 / freeze_v2 / authorization_v2 preserve all trials, prompts, scientific inputs, model and token caps; the older USD35 proposal remains unexecuted. Pin GPT6 implicit cache TTL30m using prompt_cache_options, Standard tier. At the checked rates, cache-write input is USD2.5/M (replaces the ordinary input rate), cached reads USD0.10/M, output USD10/M. Reserve USD0.24192 for every dispatched generation, including failed attempts; 72 full-cap attempts reserve USD17.41824. Generation allocation17.5 plus count-fee allocation2.5 equals20. Normal36 full-cap calls reserve8.70912. Provider count fees and invoice remain unknown; these allocations are not observed charges. No 12h cache writes, extra Claude calls, changed trial counts, or hidden-outcome tuning. Eleven offline API guard tests and the new900-member freeze qualified before real calls. All36 rounds must freeze before hidden evaluation. Existing staged keys remain private through generation/audit/evaluation; no repeated staging request.

### Completed execution and review boundary

Actual36generation/36counts/0retry,1554292tokens. Token-rate estimateUSD4.1022157 generation-only; count fees and invoice unknown. B/C each3sessions×6rounds, all36released before grading. Fixed end score11/11observabletypes each; C+9.85711065%tokens. All original unknowns, first-round false controls and one invalid metadata round retained. Description400cap was not explicit inprompt/schema; do not infer semantic advantage from that invalid round or edit it retrospectively.

Fixed formal540native jobs completed75PASS/104FAIL/361TIMEOUT. Earlier physical prefixFAIL types B3/0/3,C7/6/0 by repetition; pooled3vs7 is a secondary scope, with74unresolved physical witness validations and no same-sample/category oracle confirmation. trace_done0 projection and local trivial proofs remain distinct from128cycle completion. Post-hoc input-only physical obligation control is separately registered, composite/artificial, qualified with4simulations/600cycles and24monitorreplays/3600cycles; all6end monitors alarm, reference short-tailunknown retained. Never merge it into original12faults/144pairs or claim new independentLLM evidence.

Producer audit v3 verified11340rawscorelogs/2369080cycles,900+old3937frozenmembers and old scores. Original v2 read-only audit failedcatalog-schema lookup; preserved, fixed by new audit_v3 reading actual frozen mutant catalog, without rerunning native experiments/model calls. Coordination packageP01 at docs/audits/agent_bridge_2026-11-05/P01/manifest.json is **independent review pending**, not accepted by the producer. Keep keys until review/task closure; this coordination authorizes no new paid calls, deletion, installation, commit or push.
