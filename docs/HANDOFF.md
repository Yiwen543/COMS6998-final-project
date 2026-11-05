# Project handoff — 2026-11-05, America/New_York

**Start here. Existing-scope end-to-end acceptance is complete; read the new qualification report and preserve all completed runs.** Do not automatically resume old commands. Read this file and PROJECT_STATUS first; open protocol/decisions when needed. Long logs stay on disk.

## Autonomous qualification and end-to-end acceptance — completed 2026-11-05

- User asked autonomous local R&D through end-to-end acceptance. The existing registered monitor workflow and new API-free qualification path have now been implemented and verified; no ordinary stage was left waiting for “continue”. New research API calls0, new independent model samples0, no key requests/installation/commit/push. All previous dirty work preserved. HEADmain00e0dd974d3a910b37de3c029f61e7beeb7953fd,remote unverified.
- **Main entry point/report:** `test2/scripts/controller_offline_pipeline.py`; `test2/results/controller-offline-e2e-fresh-v1/report.md`, `summary.json`, `completion.json`, `acceptance.json`. README documents full fresh and explicit reuse modes. Actual full command: `.venv/bin/python -B test2/scripts/controller_offline_pipeline.py --output test2/results/controller-offline-e2e-fresh-v1 --formal all`; it completed in826.336s. It newly executed18calibration+108balanced formal jobs,1044synthetic candidate-control replays/145152cycles,4end-marker plumbing cases, fresh QF_BV/egg and source/coverage audit. Do not rerun to restore context; use new directory if explicitly reproducing.
- Full current test2 suite freshly passed63tests at `results/controller-offline-full-tests-v1.log`; qualification module9tests passed at `controller-qualification-unit-v2.log`. Historical25-test records remain historical; this63-test invocation actually includes their current modules. No whole-repo test claim.
- New configs: `controller_offline_qualification_v1.json` then limited repairv2; `controller_done_abi_v1.json`; `controller_witness_replay_v1.json`. New modules: obligations, physical_witness, formal_diagnostic, monitor_done, offline_pipeline, offline_verify, witness_replay. Source snapshots in result directories identify actual versions; no original frozen module edits.
-32finite synthetic controls: independent frozen Claude labels9PASS/17FAIL/3UNRESOLVED/3INVALID_INPUT. All36saved candidate programs replayed; final C rep2 misses missing-data/status/both response completion, while all finals miss a source offer blocked until finite end. No final candidate alarms on reference-accepted controls. These are contract-level synthetic examples, not certified physically reachable traces/RTL coverage or new B/C trials. All original scores unchanged.
- Formal diagnosticv1 retains qualification_failed and both unresolved physical-anchor checks: the old bridge used terminal SMT index, while native sampled-assert reports lag actual active/ok failure. v1 source copies remain. v2 directly observes the failing pre state, uses literal input replay in Icarus/Verilator, checks retained SMT pins and the candidate alarm, then sends only the true physical prefix to unchanged Claude checker. Both false controls referencePASS and both M02anchors referenceFAIL. Missing/unknown/unsupported values stay unresolved.
- Smaller cones help full-depth true control and first B reset proof but make the known C3P2 proof time out. Balanced correct-source108 (depth24/10s, interleaved arms) and full fresh reproduction both give50PASS/56TIMEOUT/1UNKNOWN/1unreachedcover. Single-slot prove counts B1/3/2 vs C1/0/2; original retained-profile counts B0/0/0 vs C0/0/1. Properties differ in strength; this shows sensitivity, not a causal new C-effect estimate. No full suite soundness proof; old473timeouts untouched.
- Extra closure audit `results/controller-original-witness-physical-v1/`: all33original BMC FAIL traces rechecked, without rerunning old formal jobs.66physical simulator runs/548cycles,33candidate replays/274cycles; all33 reproduce alarm and receive independent referenceFAIL on actual prefixes. No new unresolved, old labels unchanged. Acceptance verifies prior VCD SHAs and raw logs. This ran after timed formal work to avoid compilation interference.
- End-marker prototype: `public/observer_contract_v3_draft.md` and `controller_monitor_done.py` expose readonly trace_done only finalpost, no DUT input/extra edge. Timing, readonly and pending-final-source checks tested. It is infrastructure plumbing, not a new GPT oracle/experimental candidate or new live LLM interface trial. Independent DUT spec/checker unchanged; livefalse. Any trace_done=0 formal projection is safety-only.
- Actual Coverage-3 denominator3168=110line+176branch+248expr+2634toggle;1989raw points remain unhit across3dev; unproven/unmapped retained.8Cselected source points already hit. Fresh5882QF_BV queries reproduce saved results, all281groundrules UNSAT, actual egg0.11 saturation10iterations and partition match.168typed definition certificates and13dependency hashes audited, not full frontend re-executed; widths/signedness atom mapping preserved. Two-state combinational scope only, not four-state/sequential equivalence or temporal reachability.
- Independent verifier acceptance status accepted_with_scope:1052replay logs/145728monitor cycles checked in full fresh run,126formal jobs/native statuses/source/harness checked, keys absent. Formal and physical compile/cycle/resource ledger preserves failedv1/replay work and flags overlapping wall/component time rather than summing it twice. Parent freezes3486/212/239, old two scores, migration531functional files, AGENTS and retained historical handoff hashes match.
- **Completed:** runnable existing LLM→frozen passive monitor→independent evaluation flow (historical live calls intact), full local qualification/reproduction/63tests/reports. **Partial:** individual properties proven, no whole monitor soundness; end-marker is offline prototype. **Planned/not run:** a newly registered/authorized live end-marker study or token-matched placebo. **Unknown:** general C causality, fresh API connectivity/USD costs, remote publication/submitted milestone authority. These limitations do not become PASS or implemented features.
- Existing-scope acceptance is met; no further paid stage has been opened. A future independent study must be motivated and preregistered, preserve source/oracle/feedback fairness and fresh evaluation boundaries, and request any needed paid authorization/key only when concrete. Do not repeat the saturated old generation merely to seek a positive result.

## Controller B/C live — completed 2026-11-05

- Read `test2/results/controller-analysis-v1/analysis.md` for Chinese stratified conclusions; `controller-report-v1/report.md` / `audit.json` / `rounds.csv` contain registered metrics. This concrete task is complete. Do not restart completed generation/scoring or request the key again for it. No new paid stage is pending.
- New registration `test2/configs/controller_run_v2.json` SHA256 `dccdd4ae56b9ff9278a456bcc0a1b5934acf33a1c8b43602033cf4dbc1cad370`; immutable `controller_live_freeze_v1.json` SHA256 `f1c9fcdebb0ede38e5756af947d8dceb985808787353572c98024dffb37ed20c`,239 members. Parent run_v1/task_v3 and original packets retained. Independent Claude reference unchanged: checker `b44f32b27c11b968d23fd93ecf8b0d714e773460fc0b505d89adf23df3cd7dee`, freeze `bbac094bcf82eecb44e57fd85a3dbdabb27dd07af00559300617753103ed7c67` (212 members).
- First actual count gate failed before any generation: B79843/C83472 initial; history91952/95581. Full-information common coverage dictionary in `qualification/prompt-audit-v3/` exactly restores v2 packets, all3168 counters and RTL/spec/observations/semantic groups unchanged. New count passed: initial46800/50429; history58909/62538. Both count reports retained;64k cap unchanged, no outcome-based adjustment.
- Nine new tests passed freshly (`controller-live-unit-tests-v2.log`);36-round mock/replay v3 passed. Full mock grading5832 replays/1124640cycles gave0 valid kills. Deep true-control TIMEOUT retained; shallow positive/negative control PASS/FAIL with independent-reference witness classification. Old25-test suite not rerun.
- Live `test2/results/controller-live-v1/` completed36 gpt-6.1-sol/low calls,0retries,1878181tokens;36 live counts plus8 preflight counts. Every count matches API input usage; maxima52563input/2657output, within64000/8192. Each arm3 independent own-history sessions×6 rounds; six slots,16000body bytes/8192state bits. All36 snapshot hashes froze before hidden access. Release SHA256 `8dc3e2d93993c3ac205b028a1006af1421e0dabcf716439b17efb895317fe049`; no hidden feedback/candidate repair. Saved-response replay `controller-live-replay-v1/replay-audit.json` matches all36 prompts/sources/feedback; not independent trials.
- All36 fixed-trace scores:11/11 observable fault types,106/106 eligible simulator/trace pairs, correct controls with0alarms/unknown. Stratified4/4 boundary_guard,3/3 handshake_reset (4raw),4/4 payload_status.12raw faults kept; M08 remains unconfirmed on this fixed corpus. Every session first reaches this ceiling at round1. B total tokens/session301681/301636/304374; C322887/324124/323479; C mean+6.91854%, lower simulation token ROI. No extra simulation benefit.
- Formal `controller-final-v1/`: all540 planned jobs completed, no cap skips;3626.314 measured wall seconds.33PASS=31activation cover+1BMC24+1prove.34FAIL=33independent-reference-confirmed mutant BMC witnesses+1unreached activation cover.473TIMEOUT=434BMC+35prove+4cover. C rep3 P2 status-stall BMC/prove PASS under fixed assumptions; no full six-slot soundness proof. Mutant type counts B0/8/0 vs C6/3/8; both pooled unions8types. C has a descriptive short-formal signal, not established general/pure-semantic benefit. Fixed formal order B then C and wall-clock sensitivity limit interpretation; no placebo,3reps/arm,one inspected IP family.
- Score SHA256 `f13161340a46c7360002e54992be0a7aba9c1d47a70fbe6f169bba8952fe2651`; `completion.json` and `formal-evidence-audit.json` bind completion/evidence. All5832 raw gzip logs and original SHAs verified,1124640cycles. Old3486 freeze members, old checker/scores, migration531 functional files, AGENTS and retained historical handoff unchanged. Main HEAD remains00e0dd974d3a910b37de3c029f61e7beeb7953fd; this agent did not commit/push/fetch. Preserve all prior dirty/untracked work.
- Exploratory read-only source audit `controller-analysis-v1/obligation-audit.json`: C rep2 final lacks128-cycle completion checking yet scores full corpus. This is a property-set coverage gap, not retrospective score invalidation. No added cases executed. Formal complete-pin witness retention/full state/late-step assumption expansion may contribute to timeouts; independent contributions not measured.128-cycle conditions exceed24-step activation window in some slots.
- User authorized one staged OpenAI key retained through count/generation/failures/evaluation. No repeated requests; no key exposure. Functional task/report/audits are complete; final cleanup record is `controller-live-v1/task-completion.json` and docs live audit. Key clearance is verified there after the final integrity check.
- Next minimum: a new API-free qualification registration for specification-obligation/negative-control coverage (presented-valid safety versus delayed/missing-response completion), plus a small fixed-control formal cone/witness-overhead diagnostic. Preserve current freezes/scores. Check the local proof/short-formal signal under balanced order before new paid B/C; do not repeat generation on this saturated corpus. No new experiment has been launched for that proposed task.

## Previous controller qualification — completed 2026-11-05

- Final Git check: HEAD now `00e0dd974d3a910b37de3c029f61e7beeb7953fd` on main. Commits `274ac21da68b84cb0e514460f21b5aa7cb78bdf3` (test2_phase1) and `00e0dd9...` (test2_phase2) appeared during this session; this agent executed no commit/push/fetch. Preserve this newer state. Final reference/results/docs still include uncommitted/untracked files; do not claim all frozen artifacts belong to that commit. Remote live state unverified.
- Read `docs/test2_controller_qualification_2026-11-05.md`. Selected task: `test2/tasks/axis_length_fifo_v1/`, original verilog-axis frame-length-adjuster FIFO wrapper, byte-wide, MIN4/MAX8, data/header FIFO32/8, reset flush. Latest concrete registration `test2/configs/controller_task_v3.json` binds active contract/reference/input hashes; unchanged original RTL. Direct core rejected on physically replayed status-stall violation; keep `axis_length_v1/` failure evidence.
- Selected scope:168 definition mismatches UNSAT;9 nontrivial mapped groups;3168 raw counters;6 source mappings unresolved retained. Local reset/data-stall/status-stall bmc/prove/cover all PASS (scope only);11jobs/24.492s.3dev+6newhidden correct traces agree across both simulators.12new single-site hidden faults measured; eligibility is reference-dependent, no candidate score yet.
- B/C prompt audit v2 is public-only and shared packet roundtrip retains3168 counters. C-min uses4 predeclared groups. Actual provider token count pending; inputcap64k matched between arms, no placebo/pure-semantic causality claim.
- Claude initial author failed auxiliary-selftest purity; Claude-only repair and first limited review are retained. Contract-aligned author plus fresh review v2 completed:50selftests/20independent controls/18baseline traces matched; accept_with_scope, no blockers, residual limits retained.5CLI calls including failure cost$3.714620 reported. No GPT checker edits.
- Latest reference: `test2/tasks/axis_length_fifo_v1/reference/frozen-v2/`. Checker SHA256 `b44f32b27c11b968d23fd93ecf8b0d714e773460fc0b505d89adf23df3cd7dee`; freeze SHA256 `bbac094bcf82eecb44e57fd85a3dbdabb27dd07af00559300617753103ed7c67`. Summary: `qualification/qualification-summary-v1.json`. No API process remains active; do not rerun completed calls.
- Hidden raw12faults×6traces/simulator retained. Each simulator has53/72 sampled-safety eligible pairs,11observable fault types; M08 has no confirmed violation in this fixed corpus and remains recorded. This is reference observability, not candidate detection. Original old31TIMEOUT and prior6/6 results unchanged.
- User explicitly authorized retaining the main0600 staged key between all necessary reference repairs/reviews until completion. `controller_credentials.py` implements this using disposable per-call copies without changing the old frozen helper. The reference task has now completed and the main staged key was cleared. Never reuse chat keys or expose values.
- Active contract files: `public/specification_v2.md` and `observer_contract_v2.md`; v1 source/results remain.13new controller tests freshly passed; old25-test suite not rerun. Reference scope excludes complete soundness and retains conservative unknown/diagnostic/reset-pre/continuity limits.
- Candidate live is still false: new monitor ABI/replay/runner/every-round snapshot gates and actual API token counts are not yet established. No OpenAI key has been requested for generation.

## Latest phase2 preparation — 2026-11-04

- User selected the fixed-stimulus, matched-budget monitor question again; do not replace it with agent verdict/R0-R1-R2 work. New offline work is separately registered in `test2/configs/phase2_preflight_v1.json` through `phase2_preflight_v5.json`; all prohibit API calls/live generation.
- Analysis and next task: `docs/test2_phase2_preflight_2026-11-04.md`. Latest actual calibration: `test2/results/phase2-preflight-v5/report.md` and `formal-calibration.json`. New producer: `test2/scripts/phase2_preflight.py`; new 7-test module: `test2/tests/test_phase2_preflight.py` (7/7 freshly passed; old 25-test suite not rerun).
- Saved v1 freeze3486 items, reference, all six candidates/scoring copies and report/release bindings matched before/after. Old results remain 6/6 each, C tokens+6.523%, formal31 TIMEOUT. v1 final data are calibration only, never a fresh hidden test set.
- New calibration used only the predeclared first saved candidate B′ rep1 and public correct DUT. Splitting without flatten:6 TIMEOUT. Split+flatten at48-step BMC/10s per slot: P0/P4/P5 bounded PASS; P1/P2/P3 TIMEOUT. No unbounded proof, new model repetition or new DUT simulation. v5 has8 jobs,38.683 measured seconds including tools/controls.
- Preserve failed preflights: v1 true-control TIMEOUT; v2 too-short negative control also PASS; both stopped before candidate slots. v4 stopped on JNY telemetry schema error after one control, before candidates. v3/v5 raw jobs retained. There were21 new formal jobs across all five versions; exact v4 Python duration is missing, not zero. Each run saves its actual `producer.py` source and SHA.
- `test2/configs/registration_v2_draft.json` is a non-executable future monitor-study contract (`live_allowed=false`, task/spec/interface/formal schedule unbound, all gates false). Equal budget draft, fresh hidden corpus, Claude-independent reference, source-mapped semantics and every-round candidate snapshots must be bound before live. No new oracle or final corpus was created.
- **Next minimum task:** one multi-cycle request/response task feasibility packet: source/spec/interface, task-relevant semantic mapping, fixed development observations, independently reviewable legal controls and decomposed formal schedule. Do not rerun these preflights to restore context. Request a key only when a concrete authorized API stage is ready, via the existing terminal hidden staging flow.

## Workspace and state — historical migration snapshot

- Repository root: `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project`
- Parent workspace: `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project`
- Shell zsh; branch main; HEAD `acd220ace9c02a6b5f0d98bde15bcfaf70ae2a60`. No fetch, commit or push in migration; remote currency **unconfirmed**.
- Before migration: modified `docs/AGENT_HANDOFF.md`; untracked entire `test2/`. Preserve both. Migration adds/updates the five compact docs, snapshots and audit JSON; exact final status is in audit JSON/`git status --short`.
- Prior test2 generation/final/report processes exited0; no new model or simulator was launched during migration. This is a recorded workflow state, not an inventory of every process on the computer.
- Both staged key files absent when checked: `build/private/midterm-openai-key`, `build/private/anthropic-crosscheck-key`. Never print key contents or reuse plaintext chat credentials.

## Current result, limits, and evidence

[R,V] Test2 is complete:36 gpt-6.1-sol calls/0retries, B′/C′ each3×6 rounds. Each final candidate detects6/6 observable injected mutants, no correct-control alarms/unknown; C mean tokens128038.33 vs B120197.67 (+6.523%). Fixed input/coverage, one synthetic FIFO, no placebo; not a general conclusion about E-graphs.

[R,V] Formal72 jobs:12 PASS(all activation cover),29 mutant counterexamples(B14/C15, same5 distinct fault types),31 TIMEOUT including all24 correct-control bmc/prove. No complete correct-control proof. Icarus M02 boundary remains reference-unresolved; unactivated M05 pairs retained.

[R,V] Previous WBXBAR:17/17 raw targets in round1 for all6, all6 final checker outcomes unresolved/86 unknown records,0 failures. Do not call these passes. Smaller queue GPT-6 Sol pilot had2/6 earlier C crossings, so do not erase local positive observations.

See [PROJECT_STATUS](PROJECT_STATUS.md), [protocol](EXPERIMENT_PROTOCOL.md), [decisions](DECISIONS.md). Full historical `AGENT_HANDOFF.md` is retained; do not preload its1050+lines.

## Exact paths to start from

| Purpose | Absolute path |
|---|---|
| Latest human result | `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/live-report-v1/report.md` |
| Audit/CSV/plots | `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/live-report-v1/` |
| Calls/prompts/final candidates | `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/live-v1/` |
| Hidden scores/formal logs | `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/results/live-final-v1/` |
| Immutable live freeze | `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/configs/live_freeze_v1.json` |
| Independent reference | `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/reference/frozen-v1/` |
| Registration and fixed interface | `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/test2/configs/registration_v1.json`; `test2/public/` under the same root |
| Latest original-track report | `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/docs/wbxbar_reference_bc_2026-11-04.md` |
| Migration evidence | `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/docs/audits/migration_2026-11-04.json` |

Freeze SHA256 `7f2be65ac1b8013d614c5391b49e6cde2b821dbaca6f3e8bae609e63ed67b912`; reference checker SHA256 `53cff0d05aa9c48a71aec72cecfba265a13fe4baa2a4d9a72b3cef4d6b201337`. Full source/scoring hashes are in manifests; read selected keys, not the whole large JSON. In this audit3486 live-freeze files matched. Frozen experimental code must not be edited in place.

## Environment and reproducible commands

Use repository `.venv/bin/python` (Python3.13.9/OpenAI2.54.0); do not rely on the user's terminal exporting variables to the app. Default tools resolve through `/opt/homebrew/bin`: Verilator5.050,Icarus12.0,Yosys0.70+post,SBY0.70,Z3 CLI5.1.0,Cargo1.99.0. Claude executable `/Users/yiwenchen/.local/bin/claude`; installed executable is not a current API-access test. Slang/OpenTitan old flows use their own recorded OSS-CAD environment. `build/`, `third_party/`, `.venv/`, Rust target and credentials are ignored local dependencies, so a clone alone may not reproduce everything.

Commands below are for a later requested check; migration did **not** run them:

```sh
cd /Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project
# Small test2 suite; may invoke local compiler tools and write temporary controls:
.venv/bin/python -m unittest discover -s test2/tests -v
# Recompute audit/report from saved evidence; no API or simulation, NEW directory required:
.venv/bin/python test2/scripts/report_live.py --run test2/results/live-v1 --final test2/results/live-final-v1 --output test2/results/handoff-report-reproduction
# Offline response replay; DOES compile/replay, not an independent new model repetition:
.venv/bin/python test2/scripts/runner.py --mode replay --preflight test2/results/preflight-v2 --replay-source test2/results/live-v1 --output test2/results/handoff-replay-reproduction
# Expensive:72 formal jobs at60s caps; do not run merely to resume context:
.venv/bin/python test2/scripts/final_score.py --run test2/results/live-v1 --preflight test2/results/preflight-v2 --output test2/results/handoff-final-reproduction --formal
```

Do not run `make test`, `make step1`, `make setup`, cleanup or new live calls automatically: those can build, simulate, overwrite generated output or install components. `prepare.py` rejects already-prepared inputs; do not regenerate hidden data.

## Verification record (do not upgrade old evidence to a fresh test)

| Date (ET) | Actual check/result | Evidence and scope |
|---|---|---|
| 2026-11-04, preceding visible turn | `python -m unittest discover -s test2/tests -v`:25/25,exit0 | Visible tool output;4test modules. Not a whole-repo regression and not rerun during migration |
| 2026-11-04, preceding run | generation, final scoring and report exited0; prompt/count/score audits passed | `test2/results/live-v1/summary.json`; `live-final-v1/summary.json`; `live-report-v1/audit.json`, `final-verification.json` |
| 2026-11-04, historical WBXBAR | Saved audit pass;58selftests/36rounds checked | `results/wbxbar_reference_bc_20261104/live-audit-v1.json`; not rerun now |
| 2026-11-04, migration | File/hash/path/config/report audit and tool-version queries only; no API/experiment/test suite | `docs/audits/migration_2026-11-04.json`; final document checks recorded there |

## Next smallest task and questions

**Next minimum task:** use the latest phase2 section above and the separate feasibility plan. The user's subsequent instruction authorized API-free monitor preparation and settled the research axis; it did not authorize changing old freezes or running a live stage from an incomplete draft.

1. Which milestone is the submitted authority: parent `milestone1.pdf` or repo `output/pdf/milestone1.pdf`? They differ; the parent includes reliability/R0-R1-R2. Exact hashes are in audit JSON.
2. Research axis is now selected by the user: harder fixed-stimulus monitor evaluation. Concrete task/source and live gates remain unbound; formal-grounded agent diagnosis/recovery stays separate proposed work.
3. When should uncommitted test2 and these docs be committed/synced? Current remote state and course deadline need confirmation.

Conversation access limitation: the current context retains many earlier user requests and recent test2 tool outputs, but not a complete earlier assistant/tool transcript. The external shared ChatGPT history was not reopened in this migration. For older claims use linked artifacts, not memory; missing proof/metadata stays unknown. Skills and this handoff are maintainer material, never model experiment inputs.

New chat can reduce carried history but does not guarantee speed/cost savings. Read only relevant files and bounded summaries; this migration did not test CLI/UI `/compact`, `/new` or `/fork` behavior and does not create a new chat.
