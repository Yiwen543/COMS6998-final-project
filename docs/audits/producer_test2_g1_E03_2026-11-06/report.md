# G1 E03 — R04 executed once, halted at QC01 cover classification

Status: **EXECUTED_PENDING_P15_SAVED_EVIDENCE_REVIEW**, G1 **NOT_QUALIFIED**.
Exact entry returned1. P14 accepted the frozen R04 preparation with limits;the
unique EXECUTE was used once. No source,parameter,label,gate or budget changed.

QC00 now has two actual accepted eight-row observations,16rows total,with known
reset inputs at pre1000/post3000ps in both Icarus and Verilator. Saved VCD/stdout
checks found0field conflicts,four rising edges2000/6000/10000/14000ps,finalpost15000
and recorded end16000. Both complete row sets match the original table and each
other. This supports the startup initialization/event repair for QC00;it is not
an internal event-queue proof or qualification of the remaining15controls. Old
E02 first-row X remains unchanged. QC00 native compile/BMC/cover are explicitly
REUSED_FROM_E02,not new native samples or valid old physics.

QC01 BMC returned1/FAIL as registered for this negative control;selected known
registered-pre alarm is cycle1,q0000,active1,ok0. QC01 cover returned1;runner wrote
NOT_REACHED and halted against expectedPASS. **Raw log says cover reached step2,
assertion failed step2,StatusFAILED.** Frozen classify_native maps every failed
cover command to NOT_REACHED,so that label cannot establish target unreachability.
Both label and raw failure remain;neither is relabeledPASS. This is an unresolved
classification/expectation issue for P15,new version needed before continuation.
QC01 physical and allQC02–15 jobs remain NOT_RUN. Overall G1 is not accepted.

Actual current0setup/3logicalcompile/2native/2physical,8cycles:7returned,72NOT_RUN.
Five roots exit0;expectednegative BMC and unexpectedcover exit1. No timeout or
mandatory process-protection error. Cumulative setup8/compile6/native4/physical3,
12cycles;remaining0/26/28/30,1012cycles are not restart authority. Old failed runs
and new failed cover stay charged. Registered attempt 6.572940208s;
outer entry 6.676378875s;final cumulative actual checkpoint
11.770645541s versus charged checkpoint
14.572948167s. Original prior actual5.197697583s,
prior conservative charge8s stay separate;no full-turn or post-audit time claim.
Memory not measured;compiler children included in logical roots,full census unknown.

Source/tool/receipt/log hashes,all16case statuses,resources and raw result snapshot
are retained. E01/E02,R04 sealed inputs,all4485protected historical files,index and
HEAD remain unchanged;shared HANDOFF/STATUS only get additive notes. Current
mainHEAD2de33e981d2fffc9739d2ca049fbae1774de1aad is publication HEAD,not old scientific
freeze HEAD. No new version queries,ps,permissions,modelAPI,keys,paid,cross-IP,
raw/B/C,install,commit or push. Pool/lock remain halted/completed;no retry.

Evidence:entry-receipt.json;resources.json;per-qc.json;QC00-saved-physical-check.json;
QC01-native-classification-conflict.json;snapshot-manifest.json. Raw original logs
and VCDs under test2/results/g1-qualification-v4/jobs/ are copied into snapshot.
Reproduction means inspect the saved package;execute_once.py deliberately refuses
an existing pool/lock and must not be rerun to restore context. Next is existing
independent P15 saved-evidence audit only. All four-state/vacuity/128completion/
realDUT/oracle/74witness/C-benefit/billing and earlier scientific limits remain.
