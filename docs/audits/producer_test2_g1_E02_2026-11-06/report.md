# G1 E02 — exact R03 execution halted on physical-row mismatch

Status: **EXECUTED_PENDING_P13_SAVED_EVIDENCE_REVIEW**. Outcome: **HALTED_ON_QC00_PHYSICAL_EXPECTATION_MISMATCH**.
Exact P12 acceptance and coordinator receipt were checked before the single registered
entry. Runner exit1; stdout/stderr for the entry are empty, while every job has
original raw logs/receipts. No code, label, pin, flag or limit was changed, and no
retry, extra version/smoke/compiler/process probe or permission escalation occurred.

## Observed execution

13 roots returned0:7setup,3logical compile batches,1BMC,1activation cover,1Icarus
physical run. QC00 BMC depth8 PASS; activation cover reached step2. These do not
complete QC00: Icarus cycle0 pre/post shows a/b=xxxx,rst/en/valid=x,active/ok=x
where the fixed table expects known reset inputs. The first parser refusal is
PHYSICAL_EXPECTED_MISMATCH:a at cycle0 pre/tick1000, expected0000/observedxxxx.
All raw X values remain.8OBS rows and END4cycles agree with saved VCD's4posedge
ticks2000/6000/10000/14000; no physical rows were accepted. QC00 Verilator and all
later QC jobs were NOT_RUN. Root return0 is distinct from adapter rejection.

Time-zero scheduling of the declaration-initialized step and always@* stimulus
is a source-based candidate explanation only. It was not experimentally isolated;
no simulator-bug conclusion, code repair, oracle change or rerun is made here.

| QC | Declared scope | Formal compile | BMC | Cover | Icarus | Verilator | Full result |
|---|---|---|---|---|---|---|---|
| QC00 | LIMITED_PUBLIC_CONTROL | RETURNED | PASS | PASS | RETURNED | NOT_RUN | PARTIAL_REJECTED_PHYSICAL_EXPECTATION |
| QC01 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC02 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC03 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC04 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC05 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC06 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC07 | INELIGIBLE_VACUOUS | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC08 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC09 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC10 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC11 | LIMITED_PUBLIC_CONTROL | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC12 | UNSUPPORTED_FOUR_STATE_EQUIVALENCE | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC13 | UNSUPPORTED_FOUR_STATE_EQUIVALENCE | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC14 | TRANSPORT_ONLY | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| QC15 | INELIGIBLE_VACUOUS | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |

Complete qualified QC0; partial/rejected QC1; wholly NOT_RUN QC15. The16 declared
eligibilities above are not16 observations. QC07/15 vacuity,QC12/13 unsupported
four-state equivalence,QC14 finalpost transport remain exclusions and NOT_RUN.
No dual-simulator binding,128-cycle/unbounded completion,realDUT/oracle/monitor
soundness or C-benefit conclusion follows.

## Resource accounting

Current reservations/dispatches: setup7,compile3,native2,physical1/4cycles.
Cumulative including E01: setup8,compile3,native2,physical1/4cycles. Remaining
counters setup0,compile29,native30,physical31/1020cycles do not authorize restart.
Original32/32/32 roots,1024cycles and1200seconds caps remain;make version was not
reprobed. Actual internal compiler child count is UNKNOWN; raw commands are retained.

Current recorded window 5.151964417193s; latest checkpoint
5.151972874999s. Historical measured window
0.045724458061s differs from conservative prior charge2s.
Saved cumulative actual checkpoint 5.197697583120s;
charged checkpoint 7.151973249856s. Original fields
are separately sampled,not forced equal. Memory unmeasured. Full preparation/closure
turn elapsed is unmeasured,not0; prior R03 partial1466.678545s and P12 approx575.6s
are separate preparation/review. Resource-summary retains exact values.

All13 receipts show owned-group probe absent at its sampling point,0mandatory
errors,0timeouts/cleanup kills and0external inventory attempts. This is limited
observed process evidence,not an exhaustive child census or OS hard realtime
guarantee. API/count/generation/Claude/key/network/install/delete/index changes0
for this controlled G1 execution/E02 sealing path.

## Versions, provenance and next checkpoint

Tool-versions.json records actual version text from saved outputs:Yosys0.70+post,
Z3 5.1.0,Icarus/vvp12.0,Verilator5.050,Appleclang21.0.0. smtbmc help returned0 but
did not report a version:actual version UNKNOWN. Make remains NOT_REPROBED.
No standalone diagnostic was run to fill either unknown.

P12-N1 scope sidecar preserves P12a:the earlier combined preparation turn diverted
into historical PPT/web reads. Earlier network=0 is scoped to controlled G1
preparation,not the entire old turn. No frozen R03 original was edited.

Actual entry/exit and tool receipts:runner-command.json. Per-QC table,raw
observation refusal,VCDs,all76NOT_RUN,ledger,raw result manifest,source bindings
and exact original logs/build files are saved in this snapshot. Prior pure
fixtures in the shared result root are explicitly distinguished from2 new
actual job VCDs. No old tests/experiments/companion audits were rerun.

Next: existing P13 independently reviews this saved evidence with0additional real
jobs. Stop here; no pool reset/refund/retry/newprofile. Further routing requires
coordinator accounting of cumulative remaining resources under the original grant.
All old scores/timeouts/unknowns,P04/P05/P06/P05-N1/F1/selected-sample/category/
128completion/H1/H2/L1/74witness/billing/R0-R1-R2 limitations remain.
