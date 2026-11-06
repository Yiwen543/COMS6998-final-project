"""Seal E03 saved evidence only; no tool/version/solver/simulator retry."""
from pathlib import Path
from collections import Counter
from unittest.mock import patch
import hashlib,json,os,re,shutil,subprocess,sys,time
R=Path(__file__).resolve().parents[3];A=Path(__file__).resolve().parent
N=R/'test2/g1_v4';OUT=R/'test2/results/g1-qualification-v4'
PRE=R/'docs/audits/producer_test2_g1_R04_2026-11-06';started=time.monotonic()
sys.path.insert(0,str(N))
from observations import parse_rows,parse_vcd,bind_physical_vcd,signal,selected_native_alarm
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def rel(p):return p.relative_to(R).as_posix()
def write(p,value):
 with p.open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git','--no-optional-locks',*args],cwd=R)
before=read(A/'before-execution.json');entry=read(A/'entry-receipt.json')
reg=read(R/'test2/configs/g1_qualification_registration_v4.json');report=read(OUT/'report.json');pool=read(OUT/'execution-state.json')
plan=read(N/'job-plan.json')['jobs'];labels=read(N/'inputs/controls.json')['cases']
assert entry['exit_code']==1 and pool['halted'] and pool['completed']
assert pool['halt_reason']==report['execution_error']=='Unqualified:NATIVE_EXPECTATION_MISMATCH:QC01:cover'
assert report['status']=='HALTED_WITH_REMAINDER_NOT_RUN'
assert len(plan)==79 and len(report['jobs'])==79
assert all(sha(R/n)==h for n,h in before['files'].items())
assert git('rev-parse','HEAD').decode().strip()==before['actual_HEAD']
assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==before['index_entries_sha256']
protected=read(R/before['protected_history_manifest']);assert all(sha(R/n)==h for n,h in protected['files'].items())
for mp,base in [(PRE/'snapshot-manifest.json',PRE),(N/'source-manifest.json',R),(OUT/'result-manifest.json',OUT)]:
 m=read(mp);assert all(sha(base/n)==h for n,h in m['files'].items()),str(mp)
returned={k:v for k,v in report['jobs'].items() if v['status']=='RETURNED'}
assert len(returned)==7
receipts={};native={};physical={};jobs_audit=[]
for jid,result in returned.items():
 folder=OUT/'jobs'/jid;receipt=read(folder/'receipt.json');receipts[jid]=receipt
 assert receipt['status']=='RETURNED' and receipt['exit_code']==result['exit_code'] and receipt['argv']==result['argv']
 for stream in ['stdout','stderr']:assert sha(folder/(stream+'.log'))==receipt[stream+'_sha256']==result[stream+'_sha256']
 assert not receipt['timed_out'] and not receipt['mandatory_errors']
 assert receipt['inventory']['attempts']==0 and receipt['inventory']['complete'] is False
 assert receipt['elapsed_seconds_including_cleanup']<receipt['job_timeout_cap_seconds']
 jobs_audit.append(dict(id=jid,kind=result['kind'],exit_code=result['exit_code'],timed_out=result['timed_out'],root_elapsed_seconds=receipt['elapsed_seconds_including_cleanup'],root_cap_seconds=receipt['job_timeout_cap_seconds'],receipt_sha256=sha(folder/'receipt.json'),stdout_sha256=sha(folder/'stdout.log'),stderr_sha256=sha(folder/'stderr.log'),mandatory_errors=receipt['mandatory_errors'],inventory_complete=False))
# Parse saved bytes under process/signal/sleep refusal mocks. These are not new trials.
with patch('subprocess.Popen',side_effect=AssertionError('NO_NEW_PROCESS')),patch('subprocess.run',side_effect=AssertionError('NO_NEW_RUN')),patch('os.killpg',side_effect=AssertionError('NO_NEW_SIGNAL')),patch('time.sleep',side_effect=AssertionError('NO_SLEEP')):
 for simulator in ['icarus','verilator']:
  jid='QC00-'+simulator;folder=OUT/'jobs'/jid
  rows=parse_rows((folder/'stdout.log').read_text(),labels[0],simulator);vcd=parse_vcd(folder/'trace.vcd');bind_physical_vcd(vcd,rows,labels[0])
  final_states={tick:state for tick,state in vcd['samples']};edges=[];previous=None
  for tick,state in sorted(final_states.items()):
   value=signal(vcd,state,'physical_tb.clk',1)
   if previous=='0' and value=='1':edges.append(tick)
   previous=value
  assert edges==[2000,6000,10000,14000] and vcd['recorded_last_tick']==16000
  assert [x['tick'] for x in rows if x['phase']=='pre']==[1000,5000,9000,13000]
  assert [x['tick'] for x in rows if x['phase']=='post']==[3000,7000,11000,15000]
  physical[simulator]=dict(job=jid,source='NEW_E03_PHYSICAL',rows=rows,accepted_rows=8,cycles=4,rising_edges_ps=edges,recorded_end_ps=vcd['recorded_last_tick'],final_post_ps=rows[-1]['tick'],VCD_stdout_field_mismatches=0,first_pre_known=True,first_post_known=True,trace_sha256=sha(folder/'trace.vcd'))
 assert physical['icarus']['rows']==physical['verilator']['rows']
 alarm=selected_native_alarm(parse_vcd(OUT/'jobs/QC01-bmc/trace.vcd'))
 assert alarm==report['jobs']['QC01-bmc']['selected_registered_pre_alarm']
for mode in ['bmc','cover']:
 folder=OUT/'jobs'/('QC01-'+mode);text=(folder/'stdout.log').read_text()+(folder/'stderr.log').read_text()
 statuses=re.findall(r'Status:\s*(PASSED|FAILED)',text)
 reached=[int(n) for n in re.findall(r'Reached cover statement in step (\d+)',text)]
 native[mode]=dict(job='QC01-'+mode,runner_native_status=report['jobs']['QC01-'+mode]['native_status'],expected=labels[1]['native_BMC_expected' if mode=='bmc' else 'activation_cover_expected'],raw_final_status=statuses[-1] if statuses else None,raw_cover_reached_steps=reached,raw_assert_failed='Assert failed' in text,exit_code=returned['QC01-'+mode]['exit_code'],trace_sha256=sha(folder/'trace.vcd'),selected_registered_pre_alarm=alarm if mode=='bmc' else None)
assert native['bmc']['runner_native_status']=='FAIL' and native['bmc']['expected']=='FAIL'
assert native['cover']['runner_native_status']=='NOT_REACHED' and native['cover']['raw_cover_reached_steps']==[2] and native['cover']['raw_assert_failed'] and native['cover']['raw_final_status']=='FAILED'
conflict=dict(status='UNRESOLVED_RUNNER_CLASSIFICATION_CONFLICT',runner_label='NOT_REACHED',raw_cover_reached=True,raw_reached_step=2,raw_assertion_failed=True,raw_final_status='FAILED',process_exit_code=1,frozen_expected='PASS',old_label_and_failure_retained=True,not_changed_to_PASS=True,not_evidence_of_unreachable_target=True,location='test2/g1_v4/runner.py::classify_native maps every FAILED cover to NOT_REACHED',next='P15 must review saved tool semantics and taxonomy before any new registration/continuation.')
write(A/'QC00-saved-physical-check.json',dict(status='QC00_DUAL_OBSERVATIONS_MATCHED_PENDING_P15',simulators=physical,old_E02_first_row_X_preserved=True,scope='Saved E03 two simulations only;not allQC or scheduler-internal causality proof.'))
write(A/'QC01-native-classification-conflict.json',dict(native=native,conflict=conflict))
per=[]
for c in labels:
 cid=c['id'];row=dict(id=cid,title=c['D01_title'],eligibility=c['eligibility'],expected_native_BMC=c['native_BMC_expected'],expected_activation_cover=c['activation_cover_expected'],phase_binding_expected=c['phase_binding_expected'],completion128_credit=False,real_DUT_or_oracle='UNQUALIFIED',independent_acceptance='PENDING_P15',physical={})
 if cid=='QC00':
  row.update(status='DUAL_PHYSICAL_MATCHED_WITH_EXPLICIT_E02_NATIVE_REUSE',native={k:dict(status='REUSED_FROM_E02',new_execution=False,original_job=report['native_prefix_reuse']['jobs'][cid+'-'+k]['original_job']) for k in ['bmc','cover']})
 elif cid=='QC01':row.update(status='PARTIAL_HALTED_ON_COVER_CLASSIFICATION_CONFLICT',native=native,classification_conflict=conflict)
 else:row.update(status='NOT_RUN',native={k:dict(status='NOT_RUN') for k in ['bmc','cover']})
 for sim in ['icarus','verilator']:
  row['physical'][sim]=dict(status='OBSERVATIONS_MATCHED_PENDING_P15',new_execution=True,rows=8,cycles=4,trace_sha256=physical[sim]['trace_sha256']) if cid=='QC00' else dict(status='NOT_RUN',new_execution=False,reason=pool['halt_reason'])
 per.append(row)
write(A/'per-qc.json',dict(cases=per,qualified_overall=False,new_physical_runs=2,new_native_runs=2,new_setup=0,all_16_QC_retained=True))
resources=dict(current_attempt=dict(setup=0,compile=3,native=2,physical=2,physical_cycles=8),cumulative=pool['reserved'],caps=pool['caps'],remaining=pool['remaining'],registered_attempt_elapsed_seconds=pool['total_elapsed_seconds'],outer_entry_elapsed_seconds=entry['outer_elapsed_seconds'],prior_actual_window_seconds=pool['prior_actual_window_seconds'],prior_conservative_charge_seconds=pool['prior_conservative_charge_seconds'],cumulative_actual_checkpoint_seconds=pool['cumulative_actual_window_seconds'],cumulative_charged_checkpoint_seconds=pool['cumulative_charged_window_seconds'],checkpoint_sampling_note='Separately sampled ledger fields retained exactly;charge8 is not measured spend. Outer capture and postrun audit are not registered solver/simulator time.',jobs_returned=7,root_exit_codes=dict(Counter(str(x['exit_code']) for x in returned.values())),jobs_not_run=72,no_refund_or_automatic_retry=True,new_tool_version_queries=0,version_scope='E02 version/help evidence and fixed binary pins reused;compile logs may print versions. smtbmc version remains UNKNOWN/help-only;make not reprobed.',timeout_count=sum(bool(x['timed_out']) for x in returned.values()),mandatory_process_errors=[],inventory_attempts=0,inventory_complete=False,child_count='UNKNOWN',memory_total_peak='NOT_MEASURED',process_protection_limits=['Owned PGID/poll/wait/deadline protection;all7 returned with no mandatory error.','No exhaustive child/detached-descendant census or OS absolute realtime guarantee.','No timeout/kill fault branch exercised in this execution.'],logical_compile_batch_note='3 roots;internal compiler commands/time included in shared root logs and budget,not a claim of3 total OS processes.',all_root_caps_observed=True,jobs=jobs_audit)
assert resources['current_attempt']==pool['attempt_reserved']
assert resources['cumulative']==dict(setup=8,compile=6,native=4,physical=3,physical_cycles=12)
write(A/'resources.json',resources)
write(A/'preservation-checks.json',dict(protected_historical_files=4485,mismatches=[],R04_manifest_and_source_unchanged=True,original_E01_E02_pools_unchanged=True,original_failure_labels_unchanged=True,index_entries_sha256=before['index_entries_sha256'],index_unchanged=True,staged_paths=0,current_HEAD=before['actual_HEAD'],new_pool_completed=pool['completed'],new_pool_halted=pool['halted'],no_additional_execution_after_halt=True))
write(A/'hallmark-usage.json',dict(skill='/Users/yiwenchen/.codex/skills/hallmark/SKILL.md',sha256=sha(Path('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md')),reused_read_from='R04 resumed preparation SKILL.md lines1-150',fresh_full_read_claimed=False,applied_for=['Lead with exact saved material rather than expected outcomes.','Separate runner label,raw cover reach,assertion failure and process exit.','Use bounded one-attempt execution and one saved-evidence check;invent no success metrics.'],UI_workflow_or_scripts=False,not_RTL_correctness_or_independent_acceptance=True))
text=f'''# G1 E03 — R04 executed once, halted at QC01 cover classification

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
and new failed cover stay charged. Registered attempt {pool['total_elapsed_seconds']:.9f}s;
outer entry {entry['outer_elapsed_seconds']:.9f}s;final cumulative actual checkpoint
{pool['cumulative_actual_window_seconds']:.9f}s versus charged checkpoint
{pool['cumulative_charged_window_seconds']:.9f}s. Original prior actual5.197697583s,
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
'''
with (A/'report.md').open('x') as f:f.write(text)
section=f'''\n\n## Current G1 execution — E03 / R04 halted, pending P15 (2026-11-06)

R04 ran once after exact P14 PASS_WITH_LIMITS and EXECUTE;runner exit1,G1 NOT_QUALIFIED.
QC00 both actual simulators now match8rows each,VCD0conflicts,known first pre/post,
4edges2/6/10/14ns,post15/end16ns;old E02 X retained. QC00 native2+frontend explicitly
REUSED_FROM_E02,not new trials. QC01 BMC expectedFAIL observed. Cover raw reached
step2 AND assertfailed/StatusFAILED/exit1,but frozen classifier wroteNOT_REACHED;
this conflicts with rawreach and cannot proveunreachable. Old label/negative raw
outcome retained,noPASS relabel. Halt reasonNATIVE_EXPECTATION_MISMATCH:QC01:cover.

Current0setup/3compile/2native/2physical8cycles,7returned/72NOT_RUN;QC01physical and
QC02–15 unrun. Cumulative8setup/6compile/4native/3physical12cycles;remaining0/26/28/30,
1012cycles doesnotauthorize restart. Current registered{pool['total_elapsed_seconds']:.9f}s,
cumulativeactual{pool['cumulative_actual_window_seconds']:.9f}s versuscharged{pool['cumulative_charged_window_seconds']:.9f}s;
prioractual5.197697583/charge8 allocation retained. No timeouts/mandatory errors;
0ps/versionqueries,childcensus incomplete,memory unknown,no new permissions.

Exact E03 phase/report/perQC/resources/raw snapshot in
`docs/audits/producer_test2_g1_E03_2026-11-06/`;v4pool halted/completed,lock retained.
All4485historical files,R04sources/registration/old pools/failures/index unchanged;
actual HEAD2de33e981d2fffc9739d2ca049fbae1774de1aad,stage0. P15 next reads saved bytes,
then any continuation needs new exact registration/accepted review/EXECUTE and
cumulative accounting. No retry,API/key/paid/raw/B/C/crossIP/install/commit/push.
All original document bodies and scientific/128/fourstate/vacuity/74witness/C/billing
limits preserved;Hallmark factual-material organization only,noRTL certification.
'''
shared={}
for name in ['HANDOFF.md','PROJECT_STATUS.md']:
 p=R/'docs'/name;old=p.read_bytes();saved=A/'before/docs'/name;saved.parent.mkdir(parents=True,exist_ok=True)
 with saved.open('xb') as f:f.write(old)
 header,body=old.split(b'\n',1);p.write_bytes(header+section.encode()+body);assert p.read_bytes().endswith(body)
 shared[name]=dict(before_sha256=sha(saved),after_sha256=sha(p),entire_old_body_retained=True)
# Phase names successor manifest without its hash;manifest binds phase.
write(A/'phase.json',dict(phase='G1_E03_R04_EXECUTED_ONCE_HALTED_PENDING_P15',status='EXECUTED_PENDING_P15_SAVED_EVIDENCE_REVIEW',scientific_qualification='NOT_QUALIFIED',execution_error=pool['halt_reason'],entry_exit_code=entry['exit_code'],entry_receipt_sha256=sha(A/'entry-receipt.json'),actual_HEAD=before['actual_HEAD'],registration_sha256=sha(R/'test2/configs/g1_qualification_registration_v4.json'),R04_preparation_manifest_sha256=sha(PRE/'snapshot-manifest.json'),P14_review_sha256=sha(R/'docs/audits/agent_bridge_2026-11-06/P14_g1_startup_preflight/review.json'),EXECUTE_sha256=sha(R/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r04.json'),final_pool_sha256=sha(OUT/'execution-state.json'),report_sha256=sha(OUT/'report.json'),result_manifest_sha256=sha(OUT/'result-manifest.json'),current_reserved=pool['attempt_reserved'],cumulative_reserved=pool['reserved'],current_window_seconds=pool['total_elapsed_seconds'],cumulative_actual_checkpoint_seconds=pool['cumulative_actual_window_seconds'],cumulative_charged_checkpoint_seconds=pool['cumulative_charged_window_seconds'],returned=7,NOT_RUN=72,complete_dual_QC=['QC00'],partial_QC=['QC01'],remaining_QC_not_run=[f'QC{i:02}' for i in range(2,16)],cover_classification_conflict=conflict,native_prefix_reuse='REUSED_FROM_E02_NOT_NEW_TRIAL',source_and_history_mismatches=[],pool_halted_completed=True,no_automatic_retry=True,model_API_key_paid_crossIP_raw_B_C_commit_push=0,index_unchanged=True,shared_document_additions=shared,postrun_audit_seconds_before_snapshot=time.monotonic()-started,postrun_scope='Saved-byte parsing/hash/copy only;not registered G1 execution or a fresh experiment.',snapshot_manifest=rel(A/'snapshot-manifest.json'),next='STOP_FOR_EXISTING_P15_SAVED_EVIDENCE_AUDIT;NO_ADDITIONAL_REAL_JOBS'))
# Snapshot actual result tree and all frozen inputs/lineages,without symlinks/caches.
snapshot=A/'snapshot';snapshot.mkdir()
copy_paths=[p for p in OUT.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
source=read(N/'source-manifest.json');copy_paths += [R/n for n in source['files']]
copy_paths += [N/'source-manifest.json',R/'test2/configs/g1_qualification_registration_v4.json',PRE/'snapshot-manifest.json',PRE/'phase.json',R/'docs/audits/agent_bridge_2026-11-06/P14_g1_startup_preflight/review.json',R/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r04.json',R/'docs/HANDOFF.md',R/'docs/PROJECT_STATUS.md']
for p in copy_paths:
 assert not p.is_symlink();target=snapshot/rel(p);target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():assert sha(target)==sha(p)
 else:shutil.copy2(p,target)
assert all(sha(R/n)==h for n,h in protected['files'].items())
assert all(sha(R/n)==h for n,h in before['files'].items())
assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==before['index_entries_sha256']
files={p.relative_to(A).as_posix():sha(p) for p in sorted(A.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
write(A/'snapshot-manifest.json',dict(status='EXECUTED_PENDING_P15_SAVED_EVIDENCE_REVIEW',files=files,file_count=len(files),excluded=['snapshot-manifest.json(self-hash)','__pycache__'],scope='One E03 actual run and saved-byte audit with exact R04/native-reuse lineage;not independent acceptance.'))
print(json.dumps(dict(status='E03_SEALED_PENDING_P15_G1_NOT_QUALIFIED',files=len(files),phase_sha256=sha(A/'phase.json'),snapshot_manifest_sha256=sha(A/'snapshot-manifest.json'),pool_sha256=sha(OUT/'execution-state.json'),current=pool['attempt_reserved'],cumulative=pool['reserved'],jobs_returned=7,NOT_RUN=72,QC00_dual_rows=16,QC01_raw_cover_reached_step=2,QC01_raw_final_status='FAILED',frozen_runner_label='NOT_REACHED',source_history_index_unchanged=True),indent=2))
