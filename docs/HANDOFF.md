# New-chat handoff — 2026-11-04, America/New_York

**Start here. Current task is test2 phase2 preparation, explicitly authorized after the migration. No live stage is waiting for a key.** Do not automatically resume old commands or request credentials. Read this file and PROJECT_STATUS first; open protocol/decisions when needed. Long logs stay on disk.

## Latest phase2 preparation — 2026-11-04

- User selected the fixed-stimulus, matched-budget monitor question again; do not replace it with agent verdict/R0-R1-R2 work. New offline work is separately registered in `test2/configs/phase2_preflight_v1.json` through `phase2_preflight_v5.json`; all prohibit API calls/live generation.
- Analysis and next task: `docs/test2_phase2_preflight_2026-11-04.md`. Latest actual calibration: `test2/results/phase2-preflight-v5/report.md` and `formal-calibration.json`. New producer: `test2/scripts/phase2_preflight.py`; new 7-test module: `test2/tests/test_phase2_preflight.py` (7/7 freshly passed; old 25-test suite not rerun).
- Saved v1 freeze3486 items, reference, all six candidates/scoring copies and report/release bindings matched before/after. Old results remain 6/6 each, C tokens+6.523%, formal31 TIMEOUT. v1 final data are calibration only, never a fresh hidden test set.
- New calibration used only the predeclared first saved candidate B′ rep1 and public correct DUT. Splitting without flatten:6 TIMEOUT. Split+flatten at48-step BMC/10s per slot: P0/P4/P5 bounded PASS; P1/P2/P3 TIMEOUT. No unbounded proof, new model repetition or new DUT simulation. v5 has8 jobs,38.683 measured seconds including tools/controls.
- Preserve failed preflights: v1 true-control TIMEOUT; v2 too-short negative control also PASS; both stopped before candidate slots. v4 stopped on JNY telemetry schema error after one control, before candidates. v3/v5 raw jobs retained. There were21 new formal jobs across all five versions; exact v4 Python duration is missing, not zero. Each run saves its actual `producer.py` source and SHA.
- `test2/configs/registration_v2_draft.json` is a non-executable future monitor-study contract (`live_allowed=false`, task/spec/interface/formal schedule unbound, all gates false). Equal budget draft, fresh hidden corpus, Claude-independent reference, source-mapped semantics and every-round candidate snapshots must be bound before live. No new oracle or final corpus was created.
- **Next minimum task:** one multi-cycle request/response task feasibility packet: source/spec/interface, task-relevant semantic mapping, fixed development observations, independently reviewable legal controls and decomposed formal schedule. Do not rerun these preflights to restore context. Request a key only when a concrete authorized API stage is ready, via the existing terminal hidden staging flow.

## Workspace and state

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
