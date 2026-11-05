# Decision register — migration snapshot 2026-11-04

This is an evidence-linked summary, not reconstructed verbatim minutes. Historical dates are artifact dates; earlier full assistant/tool transcripts are not all available. Preserve original reports when interpretations change.

| ID | Decision and reason | Status / evidence |
|---|---|---|
| D01 | Keep C vs B primary; A vs B isolates raw-feedback value. A positive C result is a hypothesis, not a required outcome | Accepted; formal proposal pp.1–2; `docs/workflow.md` |
| D02 | Initially fix DUT/reference/driver and let experimental LLM modify JSON stimulus only, to isolate feedback and protect grading | Implemented historically; `scripts/pilot_model.py`, per-IP runners; `docs/milestone1_result_report.md` |
| D03 | Use actual bounded Rust egg and independent two-state rewrite checks; preserve types, guards, context and separate source hits | Implemented subset; `egraph/src/bin/guard_proofs.rs`, `scripts/semantic_candidate_scan.py`; unsupported cases remain |
| D04 | Screen reachable, non-immediate multi-event targets before paid trials; do not choose IPs using C outcomes or shorten budgets after seeing B | Accepted original policy; `docs/natural_write_scope_preflight_2026-11-04.md`, `configs/real_parent_screen.json` |
| D05 | Preserve WBXBAR ordinary-screen rejection, but allow a separately labeled exploratory B/C waiver at user's request | Local exception only; `configs/wbxbar_exploratory_bc_v1.json`; fresh reference trial inherits disclosed easy scope |
| D06 | Separate Claude spec-reference authorship, fresh review and GPT infrastructure/stimulus roles; only Claude repairs its oracle | Current boundary; `test2/scripts/reference_role.py`; `docs/wbxbar_conformance_gate_2026-11-04.md`. Do not retroactively claim all early checkers were Claude-authored |
| D07 | Reattribute existing WBXBAR traces under a separately frozen checker; keep original alarms/results and cumulative cycles/counters | Completed replay, then fresh generation separately; `docs/wbxbar_reference_replay_2026-11-04.md`, `docs/wbxbar_reference_bc_2026-11-04.md` |
| D08 | Check token-length confounding using local placebo variants; byte matching and provider-token matching are distinct | Historical divider byte P vs later FIFO/minimal-C token P; `docs/divider_abcp_result_2026-10-30.md`, `docs/minimal_c_result_2026-11-03.md` |
| D09 | New test2 fixes stimuli and evaluates GPT candidate SV monitors against a separate Claude reference; it is not a renamed old stimulus trial | User request in visible conversation; `test2/AGENTS.md`, `test2/configs/registration_v1.json` |
| D10 | Freeze all final candidates before hidden scoring; retain unknowns/unobservable faults; report simulation and formal separately | Implemented; `test2/scripts/final_score.py`, `score.py`, `formal_witness.py`, addendum and release manifests |
| D11 | test2 no longer optimizes DUT coverage; its ROI is valid distinct mutant kills/1000 API tokens | Implemented; `test2/results/live-report-v1/report.md`; do not numerically pool with old branch-point ROI |
| D12 | Use hashes and explicit artifacts to carry context; preserve old handoff/status rather than replacing historical evidence | This migration only; user request2026-11-04; `docs/archive/migration_2026-11-04/`, audit JSON |
| D13 | Continue test2 fixed-stimulus, matched-budget monitor research; first perform separately registered offline ceiling/formal preflight. Preserve failed controls, producer errors and all old timeouts; keep recovery/verdict research separate | Subsequent user instruction2026-11-04; `docs/test2_phase2_preflight_2026-11-04.md`; `test2/configs/phase2_preflight_v1.json` through v5; future live contract remains `registration_v2_draft.json`, all gates false |

## Decisions still required

- **Q1 — authoritative milestone:** parent `../milestone1.pdf` versus `output/pdf/milestone1.pdf`; the first visibly includes reliability/recovery, the second older future work. Do not silently copy or claim either was submitted. Evidence: PDF hashes in migration audit; page2 read/visual inspection.
- **Q2 — selected axis, pending task:** user chose harder test2 monitor evaluation. One concrete source/spec/interface, fresh hidden corpus, independent reference and matched formal schedule remain to be frozen. No automatic live run follows offline preparation; stimulus qualification and verdict/recovery remain separate.
- **Q3 — publication/state:** entire `test2/` and the historical handoff update were uncommitted at audit start. Confirm when/what to commit/push; remote freshness was not checked. Local branch main is not proof of upload.
- **Q4 — deliverable schedule:** proposal lists Nov6 presentation/Nov23 integration/Dec7 evaluation/Dec18 report; milestone adds Nov9 follow-up. These are document plans, not a freshly confirmed course schedule.

## Interpretations that must remain limited

Small/saturated tasks and redundant feedback are plausible explanations, not proved reasons a model ignored E-graphs. The earlier queue's 2/6 earlier C crossings must not disappear from a general negative summary. Current test2 ties, WBXBAR unresolved results and extraction/screening failures answer different questions. Formal timeouts and scope exclusions must survive future reports.

Recovery R0 (no added runtime checkpoints), R1 (same checkpoints/full restart), R2 (same checkpoints/selective rollback) is planned in the parent milestone/user requests; no completed controlled comparison was located. Neither model agreement nor a successful hash check substitutes for independent specification verification.
