# Controller monitor B/C — completed 2026-11-05

Main Chinese analysis: [分层评估](../test2/results/controller-analysis-v1/analysis.md). Registered metrics: [report](../test2/results/controller-report-v1/report.md), [CSV](../test2/results/controller-report-v1/rounds.csv), [audit](../test2/results/controller-analysis-v1/analysis.json).

36actual gpt-6.1-sol/low requests,0retries;3sessions×6rounds/arm,64000input/8192output matched caps. Actual usage1,878,181tokens, all counts agree. Failed original packet token gate is retained; common lossless dictionary representation exactly restores full information before any generation. New run_v2/live-freeze_v1 leaves old freezes and independent Claude reference unchanged.

Every candidate from round1 detects11/11observable types,106/106eligible pairs, no correct-control alarm/unknown. Raw12 retained, M08 unconfirmed. C mean tokens+6.919%; no simulation gain and lower token ROI.

Formal540jobs/3626.314s:473TIMEOUT,31cover PASS,1BMC PASS,1prove PASS,33reference-confirmed mutant counterexamples,1unreached cover. Confirmed types/repetition B0/8/0 vs C6/3/8; pooled union8/8. C rep3 P2 status-stall proves under fixed assumptions. This supports only a limited descriptive short-formal signal:3reps/arm,one inspected family,no placebo,fixed B-then-C formal order. No complete monitor soundness proof.

Source-only inspection found C rep2 lacks128-cycle completion checking despite full current score. This diagnoses a score ceiling/property-set coverage gap; no original score changes or extra cases. Next minimum: API-free obligation/negative-control qualification and a fixed-control formal cone/witness diagnostic before further paid work.

Fresh verification:9new tests;36exact saved-response replay matches;5832raw scoring logs/1124640cycles;540formal jobs and33independent witness records;old3486freeze files,oldreference/scores,migration531functional files and retained AGENTS/history hashes intact. No old experiment rerun,commit,push or tool installation. Key cleanup occurs after final task verification and is recorded in the completion audit.

## Subsequent API-free qualification (2026-11-05)

User authorized continuous reversible local R&D. New registration `controller_offline_qualification_v1.json` and limited bridge repairv2 preserve all old scores.32synthetic finite controls receive9PASS/17FAIL/3UNRESOLVED/3INVALID_INPUT from the same frozen independent Claude checker. All36 candidates replay1044times/145152cycles. Final C rep2 misses three missing-response cases; all finals miss a permanently blocked source offer at finite end. These are reference-conformance/completeness controls, not automatically physically reachable DUT traces or RTL coverage.

Formal diagnosticv1 retains its failed witness-alignment gate. v2 finds the actual active/ok alarm state before the native delayed report, physically replays literal inputs with Icarus/Verilator, and requires both retained SMT-output agreement and candidate-alarm reproduction before using the independent reference. Both M02 variants produce referenceFAIL; false controls produce referencePASS. No invented post state/output or oracle patch.

A smaller cone improves full-depth constanttrue and the first B reset property, while the known C status-stall proof times out under the cone profile. A balanced108-job correct-source replay gives50PASS/56TIMEOUT/1UNKNOWN/1unreachedcover, with6B and3C single-slot prove completions. This is another formal representation on the same candidates, not new model trials or a rewrite of old473timeouts. It weakens a robust causal interpretation of the original local C proof signal; selected properties have different strengths.

`controller_monitor_done.py` and observer_contract_v3_draft.md provide a tested readonly final-post trace_done prototype. It does not alter DUT pins, clock count, original observations or reference function. It is not yet a new live LLM interface trial. Safety projection with trace_done=0 cannot prove completion.

The current63-test test2 suite freshly passed. The new one-entry offline CLI and explicit evidence-reuse integration passed at `results/controller-offline-e2e-v1/`; it freshly replays5882QF_BV queries/281rules and real egg partition, audits168typed certificates without rerunning the full frontend, and records raw Coverage-3 totals110line/176branch/248expr/2634toggle.1989points remain unhit across development; all8C-selected points already hit. A full fresh `--formal all` single-command reproduction completed at `results/controller-offline-e2e-fresh-v1/` in826.336s. It executed126formal jobs and independently verified1052replay logs/145728cycles; acceptance is accepted_with_scope. Both fresh and prior balanced profiles have50PASS/56TIMEOUT/1UNKNOWN/1coverFAIL. All33original mutant BMC witnesses were additionally physically rechecked in66simulator runs/548cycles and independently confirmed, preserving all original labels.


The existing-scope runnable workflow is now accepted locally. Read the full qualification report at `test2/results/controller-offline-e2e-fresh-v1/report.md`; its manifest separates complete, partial, planned and unknown items. New live end-marker experiments, broad causal E-graph benefit and whole-monitor soundness are not claimed. No additional API calls, tools installed or commits/pushes occurred.
