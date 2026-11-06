"""E04 saved-byte audit/seal only;no rerun or new research tool invocation."""
from pathlib import Path
from collections import Counter
from unittest.mock import patch
import hashlib,json,shutil,subprocess,sys,time
R=Path(__file__).resolve().parents[3];A=Path(__file__).resolve().parent;N=R/'test2/g1_v5b';OUT=R/'test2/results/g1-qualification-v5b';PRE=R/'docs/audits/producer_test2_g1_R05B_2026-11-06';started=time.monotonic()
sys.path.insert(0,str(N));sys.path.append(str(R/'test2/g1_v5'))
from observations import parse_rows,parse_vcd,bind_physical_vcd,signal,selected_native_alarm,eligibility,phase_binding
from native_results import read_native,judge_native
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
def rel(p):return p.relative_to(R).as_posix()
def write(p,x):
 with p.open('x') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
before=read(A/'before-execution.json');entry=read(A/'entry-receipt.json');reg=read(R/'test2/configs/g1_qualification_registration_v5b.json');report=read(OUT/'report.json');pool=read(OUT/'execution-state.json');labels=read(R/reg['controls'])['cases'];intents={x['id']:x for x in read(R/reg['interpretation'])['cases']}
assert entry['exit_code']==0 and pool['completed'] and pool['halted'] is False
assert report['status']=='COMPLETE_PENDING_INDEPENDENT_REVIEW' and 'execution_error' not in report
assert len(report['jobs'])==72 and len(report['reused_jobs'])==10 and len(report['controls'])==16
assert all(j['status']=='RETURNED' for j in report['jobs'].values())
assert all(j['new_execution'] is False for j in report['reused_jobs'].values())
assert all(sha(R/n)==h for n,h in before['files'].items())
assert hashlib.sha256(subprocess.check_output(['git','ls-files','--stage','-z'],cwd=R)).hexdigest()==before['index_entries_sha256']
protected=read(R/before['protected_history_manifest']);assert all(sha(R/n)==h for n,h in protected['files'].items())
for file,base in [(PRE/'snapshot-manifest.json',PRE),(N/'source-manifest.json',R),(OUT/'result-manifest.json',OUT)]:
 assert all(sha(base/n)==h for n,h in read(file)['files'].items())
alljobs={**report['jobs'],**report['reused_jobs']};job_rows=[]
for jid,j in report['jobs'].items():
 folder=OUT/'jobs'/jid;receipt=read(folder/'receipt.json');assert receipt['status']=='RETURNED' and receipt['exit_code']==j['exit_code'] and receipt['argv']==j['argv']
 assert receipt['root_exit_knownness']=='KNOWN_FROM_CLEANUP_WAIT' and receipt['inventory']['attempts']==0 and receipt['inventory']['complete'] is False
 assert not receipt['timed_out'] and not receipt['mandatory_errors'] and receipt['elapsed_seconds_including_cleanup']<receipt['job_timeout_cap_seconds']
 for stream in ['stdout','stderr']:assert sha(folder/(stream+'.log'))==receipt[stream+'_sha256']==j[stream+'_sha256']
 job_rows.append(dict(id=jid,kind=j['kind'],exit_code=j['exit_code'],receipt_sha256=sha(folder/'receipt.json'),stdout_sha256=sha(folder/'stdout.log'),stderr_sha256=sha(folder/'stderr.log'),elapsed_seconds=receipt['elapsed_seconds_including_cleanup'],cap_seconds=receipt['job_timeout_cap_seconds'],timed_out=False,mandatory_errors=[]))
per=[];raw_native=Counter();bmc_status=Counter();activation=Counter();unknown_observations=[];physical_total=0;new_rows=0;reused_rows=0;new_cycles=0;marker_cases=[];first_input_checks=[];selected_alarm_checks=[]
# Producer saved-byte reparse,not independent review or a fresh tool/physical trial.
with patch('subprocess.Popen',side_effect=AssertionError('NO_NEW_PROCESS')),patch('subprocess.run',side_effect=AssertionError('NO_NEW_RUN')),patch('os.killpg',side_effect=AssertionError('NO_SIGNAL')),patch('time.sleep',side_effect=AssertionError('NO_SLEEP')):
 for case in labels:
  cid=case['id'];index=int(cid[2:]);row=dict(id=cid,title=case['D01_title'],eligibility=case['eligibility'],runner_control=report['controls'][cid],native={},physical={},independent_acceptance='PENDING_P17',qualified_real_DUT_or_oracle=False,completion128_credit=False)
  for mode in ['bmc','cover']:
   version='v3' if index==0 else ('v4' if index==1 else 'v5b');sourceversion='v3' if index==0 else ('v4' if index==1 else 'v5')
   folder=R/f'test2/results/g1-qualification-{version}/jobs/{cid}-{mode}';source=R/f'test2/g1_{sourceversion}/sources/{cid}_formal.sv'
   evidence=read_native(folder,source,mode);judge=judge_native(evidence,mode,intents[cid]);assert evidence==alljobs[cid+'-'+mode]['native_evidence']
   row['native'][mode]=dict(origin='REUSED_FROM_E02' if index==0 else ('REUSED_FROM_E03' if index==1 else 'NEW_E04'),new_execution=index>=2,evidence=evidence,target_judgment=judge,stdout_sha256=sha(folder/'stdout.log'),stderr_sha256=sha(folder/'stderr.log'),receipt_sha256=sha(folder/'receipt.json'),trace_sha256=sha(folder/'trace.vcd') if (folder/'trace.vcd').is_file() else None)
   raw_native[evidence['tool_status']]+=1
   if mode=='bmc':bmc_status[evidence['native_BMC_status']]+=1
   else:activation[evidence['activation']]+=1
  physical_rows={}
  for sim in ['icarus','verilator']:
   version='v4' if index==0 else 'v5b';folder=R/f'test2/results/g1-qualification-{version}/jobs/{cid}-{sim}'
   rows=parse_rows((folder/'stdout.log').read_text(),case,sim);vcd=parse_vcd(folder/'trace.vcd');bind_physical_vcd(vcd,rows,case)
   final_states={tick:state for tick,state in vcd['samples']};edges=[];previous=None
   for tick,state in sorted(final_states.items()):
    clk=signal(vcd,state,'physical_tb.clk',1)
    if previous=='0' and clk=='1':edges.append(tick)
    previous=clk
   assert edges==[2000,6000,10000,14000] and vcd['recorded_last_tick']==16000
   assert [x['tick'] for x in rows if x['phase']=='pre']==[1000,5000,9000,13000]
   assert [x['tick'] for x in rows if x['phase']=='post']==[3000,7000,11000,15000]
   assert all(set(rows[k][f])<=set('01') for k in [0,1] for f in ['a','b','rst','en','valid'])
   first_input_checks.append(dict(id=cid,simulator=sim,first_pre_ps=1000,first_post_ps=3000,inputs_known=True,rows=[rows[0],rows[1]]))
   for obs in rows:
    for field in ['q','active','ok','marker','a','b','rst','en','valid']:
     if set(str(obs[field]))&set('xz'):unknown_observations.append(dict(id=cid,simulator=sim,cycle=obs['cycle'],phase=obs['phase'],field=field,value=obs[field],retained=True,scope='Original expected four-state diagnostic;not discarded/zero-filled.'))
   physical_rows[sim]=rows;physical_total+=len(rows)
   if index==0:reused_rows+=len(rows)
   else:new_rows+=len(rows);new_cycles+=4
   row['physical'][sim]=dict(origin='REUSED_FROM_E03' if index==0 else 'NEW_E04',new_execution=index!=0,rows=rows,cycles=4,edges_ps=edges,final_post_ps=15000,recorded_end_ps=16000,VCD_stdout_mismatches=0,trace_sha256=sha(folder/'trace.vcd'),stdout_sha256=sha(folder/'stdout.log'),receipt_sha256=sha(folder/'receipt.json'))
  if row['native']['bmc']['evidence']['native_BMC_status']=='FAIL' and eligibility(case):
   version='v4' if index==1 else 'v5b';alarm=selected_native_alarm(parse_vcd(R/f'test2/results/g1-qualification-{version}/jobs/{cid}-bmc/trace.vcd'))
   for sim in ['icarus','verilator']:
    physical=next(r for r in physical_rows[sim] if r['phase']=='pre' and r['cycle']==alarm['cycle']);assert all(physical[f]==alarm[f] for f in ['q','active','ok'])
   selected_alarm_checks.append(dict(id=cid,selected_registered_pre_alarm=alarm,both_simulators_match=True,not_a_real_DUT_defect=True))
  assert phase_binding(case)==('REJECT' if case['phase_binding_expected']=='EXPECTED_REJECT' else 'MATCH')
  if cid=='QC14':
   for sim,rows in physical_rows.items():assert [r['marker'] for r in rows]==['0']*7+['1'];marker_cases.append(dict(simulator=sim,final_post_only=True,no_extra_clock=True,completion128_credit=False))
  row['cross_sim_comparison_scope']='Known-bit contract and each trace VCD;QC12/13 ok field remains excluded from Verilator four-state equivalence.'
  row['raw_cross_sim_rows_identical']=physical_rows['icarus']==physical_rows['verilator']
  per.append(row)
assert physical_total==256 and new_rows==240 and reused_rows==16 and new_cycles==120
assert activation==dict(REACHED=14,UNREACHED=2) and all(x['id']=='QC12' and x['simulator']=='icarus' and x['field']=='ok' for x in unknown_observations)
write(A/'per-qc.json',dict(cases=per,overall_qualification='PENDING_P17_NOT_YET_ACCEPTED',registered_cases=16,eligibility_counts=dict(Counter(c['eligibility'] for c in labels)),native_raw_tool_counts=dict(raw_native),native_BMC_counts=dict(bmc_status),activation_counts=dict(activation),unknown_native_evidence=0,NOT_RUN=0,all_legacy_labels_and_failures_retained=True,completion128_credit=False))
write(A/'physical-observations.json',dict(total_valid_rows=256,new_rows=240,reused_rows=16,new_physical_runs=30,reused_physical_runs=2,valid_physical_cycles_in_profile=128,cumulative_including_bad_E02_physical_cycles=132,first_input_checks=first_input_checks,all32_first_input_pairs_match_original_reset=True,first_input_unknown_count=0,intentional_unknown_observations=unknown_observations,unknowns_preserved=len(unknown_observations),VCD_stdout_conflicts=0,edge_counts_each_run=4,post15000_end16000_all32=True,marker_transport=marker_cases,selected_registered_pre_bindings=selected_alarm_checks,four_state_equivalence_not_claimed=['QC12','QC13']))
resources=dict(current_attempt=pool['attempt_reserved'],cumulative=pool['reserved'],caps=pool['caps'],remaining=pool['remaining'],new_roots=72,reused_jobs=10,reuse_is_new_trial=False,new_root_exit_counts=dict(Counter(str(j['exit_code']) for j in report['jobs'].values())),timeouts=0,mandatory_errors=[],NOT_RUN=0,unknown_native=0,raw_native_failed_count=raw_native['FAILED'],raw_native_counts_include4reused=True,current_registered_window_seconds=pool['total_elapsed_seconds'],outer_entry_elapsed_seconds=entry['outer_elapsed_seconds'],prior_actual_window_seconds=pool['prior_actual_window_seconds'],prior_allocation_charge_seconds=15,cumulative_actual_checkpoint_seconds=pool['cumulative_actual_window_seconds'],cumulative_charged_checkpoint_seconds=pool['cumulative_charged_window_seconds'],checkpoint_scope='Separately sampled authoritative ledger values;conservative charge is not actual spend. Post-audit/copy/outer turn excluded.',root_elapsed_by_kind={kind:sum(j['elapsed_seconds'] for j in job_rows if j['kind']==kind) for kind in ['compile','native','physical']},new_setup_or_version_queries=0,tool_versions='E02 version/help evidence reused with runtime binarypins;SMTBMC version UNKNOWN/help-only,make not reprobed;compile outputs may print versions.',memory_total_peak='NOT_MEASURED',inventory_attempts=0,inventory_complete=False,child_count='UNKNOWN',process_limits=['Mandatory owned PGID/poll/wait/deadline/cleanup retained;all72 returned with no mandatory error.','No exhaustive child/detached-descendant census,OS realtime guarantee or timeout-kill-branch exercise.'],jobs=job_rows)
assert pool['attempt_reserved']==dict(setup=0,compile=14,native=28,physical=30,physical_cycles=120)
assert pool['reserved']==dict(setup=8,compile=20,native=32,physical=33,physical_cycles=132)
write(A/'resources.json',resources)
write(A/'preservation-checks.json',dict(historical_files_verified=len(protected['files']),mismatches=[],all_before_bound_files_unchanged=True,old_pools_and_compiled_artifacts_unchanged=True,old_E02_X_and_E03_NOT_REACHED_FAILED_unchanged=True,R05_R05B_sources_and_manifests_unchanged=True,index_unchanged=True,index_sha256=before['index_entries_sha256'],actual_HEAD=before['actual_HEAD'],new_pool_completed=True,new_pool_halted=False,no_retry_or_refund=True,postexecution_new_tool_calls=0))
write(A/'hallmark-usage.json',dict(skill='/Users/yiwenchen/.codex/skills/hallmark/SKILL.md',sha256=sha(Path('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md')),read_reused='Prior actual R04 lines1-150;no new full read claimed',applied=['Lead with actual saved output/counts and exclusions.','Keep failed tool statuses,unreached targets and deliberateX diagnostic visible.','Separate pipeline completion from independent qualification and broader scientific claims.'],UI_workflow_or_RTL_certification=False))
text=f'''# G1 E04 — R05B executed once, complete pending P17

Status **EXECUTED_PENDING_P17_SAVED_EVIDENCE_REVIEW**. Entry returned0 and all72
new roots returned;10old jobs explicitly reused,not new independent trials.
All16registered control observation contracts matched. **Overall G1 qualification
is not yet accepted**;runner completion is not scientific/general correctness.

Actual new0setup/14compile/28native/30physical120cycles. Cumulative includes every
old failed attempt:setup8/compile20/native32/physical33/132cycles,within original
amended caps. Native/physical/setup remaining0,compile12. New roots60exit0 and
12exit1,all raw failures retained. No timeout,mandatory process error,NOT_RUN or
unknownnative in this attempt. Combined native32 incl4reused:rawPASSED18/FAILED14;
BMC10PASS/6FAIL,activation14REACHED/2UNREACHED. Negative controls and four-state
projection diagnostics remain failures where rawtoolFAILED;none becomes toolPASS.

QC01savedcover is still rawFAILED/exit1+REACHED/assertFAILED;oldE03NOT_REACHED
retained in original_job. QC07/15cover explicitlyUNREACHED,vacuous/ineligible,no
correctness/completion credit. QC12/13retain unsupported four-state-equivalence
scope and raw diagnostics. QC09 intentional wrong-phase claim is rejected,not
silently matched. QC14 finalpost marker observed only at15000ps,no extra edge or
DUT input,no128completion credit. Eligibility denominator retains all16:11limited
public,2vacuous,2unsupportedfourstate,1transportonly;not16semantic proof successes.

32valid physical runs across16QC include2reusedQC00E03+30new:256rows=16reused+240
new,128valid physical cycles. Each has exactly4posedge2000/6000/10000/14000ps,
pre1000/5000/9000/13000,post3000/7000/11000/15000,end16000,VCD/stdout0conflicts.
All32first pre/post input tuples match original known reset table. **Eight
intentional IcarusQC12 ok=x observations remain**,not zero-filled/discarded.
VerilatorQC12/13ok projections remain excluded from4state equivalence. Other
known-bit comparisons follow original table;selected eligible nativeBMCfailpre
samples match both simulator pre rows. Old invalidE02firstrowX remains unchanged.

Registered current window{pool['total_elapsed_seconds']:.9f}s;outer capture
{entry['outer_elapsed_seconds']:.9f}s. Final cumulativeactual checkpoint
{pool['cumulative_actual_window_seconds']:.9f}s versuschargedcheckpoint
{pool['cumulative_charged_window_seconds']:.9f}s. Prioractual11.770645541s versus
allocationcharge15 kept separate;window1185/work1180/total1200 unchanged. No full
turn or post-audit time/invoice claim. All root deadlines met;inventory0attempts/
incomplete,childcensus/memory unmeasured,no OS hard-realtime or kill-path proof.
No new versionqueries;fixed toolpins checked within timer. Versions/help/unknowns
reuse E02 evidence rather than newly queried versions.

All4485historical protected files,oldpools/builds/logs/failures,R05/R05Bfreezes and
index unchanged. ActualHEAD2de33e981d2fffc9739d2ca049fbae1774de1aad is publication
HEAD,not oldscientificfreeze HEAD. SharedHANDOFF/STATUS additive notes preserve
completeoldbodies. Newpool completed/not halted,exclusive lock retained;no rerun.
No modelAPI,key,paid,ps,newpermissions,raw/B/C,crossIP,install,commit or push.

Evidence:entry-receipt.json,per-qc.json,physical-observations.json,resources.json,
original report/ledger/manifests/logs/VCDs in snapshot. Producer saved-byte reparse
is not independent review or another physical trial. Next is existing P17 audit
only;no new scientific conclusion until accepted. This finite public4cycle/
depth8suite proves neither128completion,unbounded behavior,realDUT/oracle/monitor
soundness,Cbenefit nor resolution of old74witnesses. All old limits remain.
'''
with (A/'report.md').open('x') as f:f.write(text)
section=f'''\n\n## Current G1 execution — E04 complete, pending P17 (2026-11-06)

ExactP16+EXECUTE R05B ranonce,entry0:72newrootsRETURNED/0NOT_RUN,10jobs reused
explicitnew_executionfalse. All16publiccontrol observationcontracts matched;
G1qualification PENDING_P17,not science/generalcorrectness. New0setup/14compile/
28native/30physical120cycles;cumulative8/20/32/33/132within caps. Native/physical/
setupremaining0;no automaticretry. Root60exit0/12exit1,rawnegativefailuresretained.

Combinednative32incl4reuse:raw18PASSED/14FAILED,BMC10PASS/6FAIL,cover14REACHED/
2UNREACHED. QC01rawFAILED+REACHED+assertFAILED andoldNOT_REACHED retained. QC07/15
vacuous/no credit;QC12/13unsupported4state diagnostics;QC09wrongphase REJECT;
QC14finalpost transportonly/no128. All16denominator retained,not16semantic proofs.
32validdualphysicalruns256rows(incl16reused),4edges2/6/10/14ns,post15/end16ns,
VCD0conflicts,allfirstinputresetknown. Eight intentionalIcarusQC12ok=x rows kept;
oldE02startupX untouched. Physicalprojection exclusions not relabeled correctness.

Currentregistered{pool['total_elapsed_seconds']:.9f}s,cumulativeactual{pool['cumulative_actual_window_seconds']:.9f}s
versuscharged{pool['cumulative_charged_window_seconds']:.9f}s;priorcharge15notspend.
0timeouts/mandatoryerrors/versionqueries/ps;inventoryincomplete,memoryunknown.
E04phase/report/perQC/resources/rawsnapshot in
`docs/audits/producer_test2_g1_E04_2026-11-06/`. Newpoolcompleted/nothalted,lock
retained;all4485historicalfiles/oldpools/R05/R05Bfreezes/index unchanged.
Next existingP17 audits savedbytes before G1qualification claim. No raw/B/C,
modelAPI/key/paid/crossIP/install/commit/push. Originalbodies/allscientific/128/
fourstate/vacuity/74witness/Cbenefit/billinglimits preserved;P2 unchanged.
'''
shared={}
for name in ['HANDOFF.md','PROJECT_STATUS.md']:
 p=R/'docs'/name;old=p.read_bytes();saved=A/'before/docs'/name;saved.parent.mkdir(parents=True,exist_ok=True)
 with saved.open('xb') as f:f.write(old)
 header,body=old.split(b'\n',1);p.write_bytes(header+section.encode()+body);assert p.read_bytes().endswith(body);shared[name]=dict(before_sha256=sha(saved),after_sha256=sha(p),entire_old_body_retained=True)
write(A/'phase.json',dict(phase='G1_E04_R05B_EXECUTED_ONCE_COMPLETE_PENDING_P17',status='EXECUTED_PENDING_P17_SAVED_EVIDENCE_REVIEW',scientific_qualification='PENDING_P17_NOT_GENERAL_CORRECTNESS',entry_exit_code=0,entry_receipt_sha256=sha(A/'entry-receipt.json'),actual_HEAD=before['actual_HEAD'],registration_sha256=sha(R/'test2/configs/g1_qualification_registration_v5b.json'),preparation_manifest_sha256=sha(PRE/'snapshot-manifest.json'),P16_review_sha256=sha(R/'docs/audits/agent_bridge_2026-11-06/P16_g1_preflight/review.json'),EXECUTE_sha256=sha(R/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r05b.json'),final_pool_sha256=sha(OUT/'execution-state.json'),report_sha256=sha(OUT/'report.json'),result_manifest_sha256=sha(OUT/'result-manifest.json'),current_reserved=pool['attempt_reserved'],cumulative_reserved=pool['reserved'],current_window_seconds=pool['total_elapsed_seconds'],cumulative_actual_checkpoint_seconds=pool['cumulative_actual_window_seconds'],cumulative_charged_checkpoint_seconds=pool['cumulative_charged_window_seconds'],new_returned_roots=72,raw_root_exit_counts={'0':60,'1':12},reused_jobs=10,control_contracts_observed=16,valid_physical_runs=32,valid_rows=256,new_rows=240,reused_rows=16,all_first_input_rows_known=True,intentional_unknown_Icarus_QC12_ok_rows=8,raw_native_status_counts=dict(raw_native),BMC_counts=dict(bmc_status),activation_counts=dict(activation),timeouts=0,NOT_RUN=0,unknown_native_evidence=0,pool_completed=True,pool_halted=False,index_unchanged=True,shared_document_additions=shared,postrun_audit_seconds_before_snapshot=time.monotonic()-started,postrun_scope='Saved-byte reparse/hash/copy;not independentreview/newphysicaltrial or registered execution time.',snapshot_manifest=rel(A/'snapshot-manifest.json'),next='STOP_FOR_EXISTING_P17_SAVED_EVIDENCE_AUDIT;NO_RAW_B_C_API_OR_ADDITIONAL_G1_RUN'))
snapshot=A/'snapshot';snapshot.mkdir()
source=read(N/'source-manifest.json')['files'];paths=[*OUT.rglob('*'),*[R/n for n in source],N/'source-manifest.json',PRE/'phase.json',PRE/'snapshot-manifest.json',R/'docs/audits/agent_bridge_2026-11-06/P16_g1_preflight/review.json',R/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r05b.json',R/'docs/HANDOFF.md',R/'docs/PROJECT_STATUS.md']
for p in paths:
 if not p.is_file() or '__pycache__' in p.parts:continue
 assert not p.is_symlink();target=snapshot/rel(p);target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():assert sha(target)==sha(p)
 else:shutil.copy2(p,target)
assert all(sha(R/n)==h for n,h in before['files'].items())
assert all(sha(R/n)==h for n,h in protected['files'].items())
assert hashlib.sha256(subprocess.check_output(['git','ls-files','--stage','-z'],cwd=R)).hexdigest()==before['index_entries_sha256']
files={p.relative_to(A).as_posix():sha(p) for p in A.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
write(A/'snapshot-manifest.json',dict(status='EXECUTED_PENDING_P17_SAVED_EVIDENCE_REVIEW',files=files,file_count=len(files),excluded=['snapshot-manifest.json(self-hash)','__pycache__'],scope='One exact E04 execution plus saved-byte producer audit;not independent G1 acceptance.'))
print(json.dumps(dict(status='E04_SEALED_COMPLETE_PENDING_P17',files=len(files),phase_sha256=sha(A/'phase.json'),snapshot_manifest_sha256=sha(A/'snapshot-manifest.json'),pool_sha256=sha(OUT/'execution-state.json'),current=pool['attempt_reserved'],cumulative=pool['reserved'],new_jobs=72,reused=10,controls=16,valid_rows=256,new_rows=240,unknown_native=0,NOT_RUN=0,intentional_unknown_rows=len(unknown_observations)),indent=2))
