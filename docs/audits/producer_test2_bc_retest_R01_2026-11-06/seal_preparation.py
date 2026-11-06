"""Seal offline retest R01 only. No SDK/client/key/API/tool execution."""
from pathlib import Path
import ast,hashlib,json,shutil,subprocess,time
R=Path(__file__).resolve().parents[3];A=Path(__file__).resolve().parent;N=R/'test2/retest_v1';RESULT=R/'test2/results/controller-done-bc-retest-preparation-v1';REG=R/'test2/configs/controller_done_bc_retest_v1.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
def rel(p):return p.relative_to(R).as_posix()
def write(p,x):
 with p.open('x') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
base=read(A/'before.json');reg=read(REG);full=RESULT/'integration-attempt2';guards=RESULT/'guard-attempt1';s=read(full/'summary.json');g=read(guards/'summary.json')
assert not (A/'phase.json').exists() and not (N/'source-manifest.json').exists()
assert s['status']=='PASS' and s['tests']==19 and s['failures']==s['errors']==0
assert g['passed'] and g['tests']==6 and g['failures']==g['errors']==0
for n,h in g['source_sha256'].items():assert sha(R/n)==sha(guards/'executed-source'/n)==h
full_delta={n:dict(full_suite_sha256=h,final_sha256=sha(R/n)) for n,h in s['source_sha256'].items() if sha(R/n)!=h}
assert set(full_delta)=={'test2/retest_v1/api.py','test2/retest_v1/cli.py','test2/retest_v1/pipeline.py'}
inputs_checked=0
for suite in [RESULT/'integration-attempt1',full,guards]:
 for case in suite.glob('test_*'):
  for n,h in read(case/'input-bindings.json').items():
   p=(case/'SYNTHETIC_ROOT'/n) if suite==guards else (case/'inputs'/n)
   assert sha(p)==h;inputs_checked+=1
assert read(RESULT/'integration-attempt1/summary.json')['failures']==1
for p in N.glob('*.py'):ast.parse(p.read_text(),filename=rel(p))
oldfreeze=read(R/'test2/configs/controller_done_generation_freeze_v2.json')['files']
assert all(not n.startswith('build/private/') and not n.endswith('/.env') for n in oldfreeze)
assert all(sha(R/n)==h for n,h in oldfreeze.items())
assert all(sha(R/n)==h for n,h in base['protected'].items())
assert hashlib.sha256(subprocess.check_output(['git','ls-files','--stage','-z'],cwd=R)).hexdigest()==base['index_sha256']
grant=R/'docs/audits/agent_bridge_2026-11-06/BC_retest_v1/user-authorization.json';assert sha(grant)=='3efe3f6da7a320486317cc90da2453f6f6ae4bf0ce1f148341479032fafe9232'
assert reg['billing']['count_reserve_micro_usd'] is None and reg['EXECUTE'] is None
assert not (R/reg['run_root']).exists() and not Path(str(R/reg['run_root'])+'-supervision').exists()
# Candidate boundaries are a field/file allowlist,not the broader maintainer freeze.
public=R/'test2/tasks/axis_length_done_v1/public/prompt-packets-v2'
write(N/'prompt-boundary.json',dict(policy='Only fixed public packet/header/system plus own lastcandidate/devfeedback;never maintainer/reference/private/final/skills',packet_files={rel(public/(a+'.json')):sha(public/(a+'.json')) for a in ['B2_raw','C2_semantic']},static_fields=['old.SYSTEM','old public packet','runtime.HEADER','round1..3'],dynamic_fields=['own previous_candidate','own development_feedback'],provider_tools=[],C_only_extra='egraph_feedback',grader_inputs_not_provider_inputs=True))
mockdir=full/'test_13_full_final_mock_and_replay_shared_grade/inputs/cohort';replaydir=full/'test_13_full_final_mock_and_replay_shared_grade/inputs/replay';mock=read(mockdir/'summary.json');replay=read(replaydir/'summary.json')
assert (mock['snapshots'],mock['finals'],mock['compile_calls'],mock['monitor_replays'],mock['monitor_cycles'])==(6,2,12,990,204444)
assert replay['actual_API_requests']==mock['actual_API_requests']==0
assert [r['unresolved_pairs'] for r in read(mockdir/'grade/scores.json')['rounds']]==[38]*6
write(A/'checks-and-deltas.json',dict(initial18_failures=1,initial_error_scope='Relative outputpath caused sharedgrader providerValueError/all162unresolved;retained. Normalized out.resolve,not score expectations.',repaired19=dict(command='PYTHONDONTWRITEBYTECODE=1 .venv/bin/python test2/retest_v1/tests.py --record test2/results/controller-done-bc-retest-preparation-v1/integration-attempt2',tool_receipts=['eb6c42','57ba85'],tests=19,failures=0,seconds=s['seconds'],source_sha256=s['source_sha256']),final6=dict(command='PYTHONDONTWRITEBYTECODE=1 .venv/bin/python test2/retest_v1/guard_tests.py --record test2/results/controller-done-bc-retest-preparation-v1/guard-attempt1',tool_receipt='43f7d8',tests=6,failures=0,seconds=g['seconds'],source_sha256=g['source_sha256']),full_suite_to_final_source_delta=full_delta,full_mock_rerun_after_parent_stop_instruction=False,not_one_final25case_suite=True,final_mutated_inputs_checked=inputs_checked,fullmock=mock,replay=replay,actual_API_SDK_keycontent_process_signal_SV_calls=0,live_owned_process_SDK_branch_exercised=False,billing_gate='UNKNOWN_COUNT_FEES_FAIL_CLOSED',credential_metadata_only=True,oldfreeze_members_verified=len(oldfreeze),oldfreeze_mismatches=[],index_unchanged=True))
write(A/'hallmark-usage.json',dict(skill='/Users/yiwenchen/.codex/skills/hallmark/SKILL.md',sha256=sha(Path('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md')),read_reused='Actual prior R04 lines1-150;not a fresh fullread',applied=['Use exact saved mock/negative evidence and explicit source-version deltas.','Keep feeunknown and realAPI0 visible;no invented live metrics.','Bounded minimumadapter/targeted checks;do not expand UI/G1framework.'],UI_workflow_executed=False,not_RTL_or_provider_billing_certification=True))
report=f'''# B/C old-benchmark retest R01 offline preparation

Status **PREPARED_API_BLOCKED_COUNT_FEES_UNKNOWN_AND_EXACT_PRECHECK_EXECUTE**.
Actual SDK/client/API/key-content/process/signal/SV calls0. User explicitly
approved B/C1sessionx3rounds,old published benchmark retest,API<=USD20. It is not
new hidden data. Actual authorization3efe3f6d... is bound,not an EXECUTE. Key has
been staged by user;metadata-only regular/nonempty0600,parent0700,not read/hashed.
Do not ask again or use it before fee/review/EXECUTE gates.

Newadapter sources in test2/retest_v1 parameterize6snapshots/2session/final sets,
fix B1,C1,C2,B2,B3,C3 order and ownhistory;reuse old public packets/ABI/Claudeoracle/
DUT/sharedv4grader. All6valid/invalid/NOT_RUN freeze before scoring. Raw12/N10,
38oracleunknowncontexts and safety/endmarker distinctions retained. No oldformal
540/74witness/DUT/newnative run. Onepass<=12compile/990replay/204444monitorcycles.
Offline replay mock-only;no second realtool pass silently added. Existing old
files/configs/results/P2/PDF/G1 remain unchanged.

Inclusive integer-microUSD ledger reserves before dispatch and never refunds
failed/timeout/unknown costs. Max12generation/16counts incl4preflight+perattempt.
Per request64k/8192/120s,gpt-6.1-sol/low/default,SDKretry0,manualfailure retry<=1.
At the supplied conservative241920microUSD/generation:6normal upperUSD1.45152,
12maxupperUSD2.90304 generation reserve. **Count fees/overall actual fees UNKNOWN**;
not a bill or permission to spend while unknown. The full possible count+generation
reserve must be verified<=USD20 before SDK construction/key access/dispatch.
No freecount/old2.5reserve assumption;parent's zero-count alternative is separate,
not accepted/integrated here.

One parent monotonic3600s window starts before runtime gates,work3590,parentforced
cleanup3595. Owned PGID includes API/localchildren,perchildmin(cap,remainingwork).
Workerlease bindsparent/start/group;SDK action requires liveledger/openreservation/
message-schema-price binding/exclusiveclaim. Fatal Halt escapes oldper-case catches.
Cancellation retains972plannedcases unresolved/recorded. Parent cleanup failures
or observed overtime are not success. No OS/filesystem hard-realtime,adversarial
childcensus or whole-host guarantee;actual new process/SDK branch not exercised.

Saved preliminarymock had6snapshots/2finals/12fakecompile/990fakereplays/204444cycles.
Initial18tests retained1failure:relativeoutputpath caused percaseValueError and
162unresolved. Outputpath normalization repaired it. Revised19/19PASS,
{s['seconds']:.9f}s,fullmock/replay each preserves38unknown/round and identical endpoints;
allfailed retrypath12gen/16count reservations retained,missing/unknown neverPASS.
After that,only api/cli/pipeline gained lease/reservation/payload/resource-release
protections;final6targeted checksPASS,{g['seconds']:.9f}s. Exact copies/hashes/deltas
saved. Per parent's instruction no completedfullmock was repeated. This is not
one final-source25case suite;independentreview must assess finaldelta. Allfake
reservations/results are fixtures,not measuredAPIusage/cost orLLM/SV evidence.

Newfee/review/EXECUTE records absent. Parent may resolve pricing or adopt reviewed
new zero-count version later;do not silently modify this sealed R01. Sharedcurrent
HANDOFF/STATUS appended with fulloldbodies retained. ActualHEAD2de33e981d2fffc9739d2ca049fbae1774de1aad,
stage0,newsource uncommitted/unpushed. No oldbudget reset,installation or Gitwrite.
Next:existing independentreview on exact finalsource plus billingblock;no live
until concrete billing and matching EXECUTE. All prior scientific/128/fourstate/
vacuity/74witness/Ccausality/invoice/unknown/negative limits remain.
'''
with (A/'report.md').open('x') as f:f.write(report)
section='''\n\n## Current same-IP B/C retest — R01 prepared, billing/EXECUTE blocked (2026-11-06)

User explicitly approved oldbenchmark B/C1sessionx3rounds,totalAPI<=USD20;B1israw
first,C addsEgraph. New `test2/retest_v1/` and
`test2/configs/controller_done_bc_retest_v1.json` prepare6snapshots/2finals,
B1C1C2B2B3C3,ownhistory,allroundfreeze thenoldsharedv4grading. Knownpublishedcorpus
retest,notfreshhidden. OldDUT/Claudeoracle/driver/ABI/labels/3168packetrawcount/
raw12/N10/38unknowns unchanged;noformal540/74witness/G1rerun orcrossIP.

Max12generation/16counts(4preflight),64kinput/8192output/120s,SDKretry0,onefailure
retry/round. Suppliedconservativegenerationreserve6normal<=USD1.45152/12max<=2.90304;
countfeesUNKNOWN:wholeAPIUSD20coverage notyetverified. Therefore **before SDK,
keyread or dispatch live FAIL_CLOSED**. Parentzero-countalternative not accepted
or substituted. Actual userauthorization3efe3f6d... isnotEXECUTE. User securekey
metadata confirmedpresent/nonempty0600,parent0700;no contentsread/hash,retain
throughstage,no repeatrequest. ActualAPI/SDK/newSV/process0 inpreparation.

One livepass<=12compile/990monitorreplays/204444cycles,0newDUT/native/setup. Parent
3600s window includesgates/API/local/cleanup;work3590/parentstop3595,perchildremaining
cap;PGIDlease+ledgerpayload/price/exclusiveclaim. Failed/unknownreservednotrefunded;
cancelledgradingretains972case denominator. OSrealtime/fullchildcensus notproved.
Initial18/1FAILretained(pathnormalization issue);repaired19PASS fullmock/replay
preserves38unknowns/round;final6guardchecksPASS. Final3sourcefiles have documented
lease/resource delta after19;fullmock notrepeatedperparent,nofakefinal25suiteclaim.

Exact `docs/audits/producer_test2_bc_retest_R01_2026-11-06/phase.json` /manifest/
report/review-prompt. Independentprecheck and defensiblebilling plus exactEXECUTE
still required;no liveautomatically. Alloldbody/P2/PDF/G1/pools/freezes/index kept;
actualHEAD2de33e981d2fffc9739d2ca049fbae1774de1aad,newwork uncommitted/unpushed.
'''
shared={}
for name in ['HANDOFF.md','PROJECT_STATUS.md']:
 p=R/'docs'/name;old=p.read_bytes();saved=A/'before/docs'/name;saved.parent.mkdir(parents=True,exist_ok=True)
 with saved.open('xb') as f:f.write(old)
 header,body=old.split(b'\n',1);p.write_bytes(header+section.encode()+body);assert p.read_bytes().endswith(body)
 shared[name]=dict(before_sha256=sha(saved),after_sha256=sha(p),entire_old_body_retained=True,suffix_sha256=hashlib.sha256(body).hexdigest())
source=dict(oldfreeze)
for p in N.rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts:source[rel(p)]=sha(p)
for p in [REG,grant,A/'review-prompt.md',A/'authorization-scope.json',R/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/G1-final-acceptance-p17.json']:source[rel(p)]=sha(p)
assert not any(n.startswith('build/private/') for n in source)
write(N/'source-manifest.json',dict(status='OFFLINE_PREPARED_LIVE_BLOCKED',files=source,credentials_excluded=True,shared_mutable_docs_excluded=True,pricing_and_future_EXECUTE='External exactreview/hash-bound records required;UNKNOWN fees block first SDK/key/dispatch.',scope='Maintainer/source/grader dependency freeze;not the candidate promptallowlist.'))
write(A/'phase.json',dict(phase='BC_RETEST_R01_OFFLINE_ADAPTER_PREPARATION',status='PREPARED_API_BLOCKED_COUNT_FEES_UNKNOWN_AND_EXACT_PRECHECK_EXECUTE',actual_HEAD=base['HEAD'],registration=rel(REG),registration_sha256=sha(REG),source_manifest=rel(N/'source-manifest.json'),source_manifest_sha256=sha(N/'source-manifest.json'),user_authorization_sha256=sha(grant),normal_generations=6,max_generations=12,max_counts=16,max_tokens=[64000,8192],API_ceiling_USD=20,generation_conservative_reserves_USD={'normal_max':1.45152,'with_retries_max':2.90304},count_fee='UNKNOWN_FAIL_CLOSED',actual_invoice_USD=None,API_requests=0,SDK_clients_constructed=0,credential_content_read_or_hashed=False,credential_metadata_checked=True,real_SV_tools_process_signal_calls=0,local_pass_caps={'compile':12,'monitor_replays':990,'monitor_cycles':204444,'DUT':0,'native':0},global_runtime_wall_seconds=3600,stopped_work_seconds=3590,parent_cleanup_seconds=5,initial_tests={'cases':18,'failures':1},repaired_integration_tests={'cases':19,'failures':0,'seconds':s['seconds']},final_guard_tests={'cases':6,'failures':0,'seconds':g['seconds']},final_fullsuite_rerun=False,source_delta_after_fullmock=list(full_delta),independent_precheck=None,pricing_record=None,EXECUTE=None,actual_live_root_exists=False,oldfreeze_members_verified=len(oldfreeze),old_mismatches=[],index_unchanged=True,shared_document_additions=shared,partial_preparation_seconds=time.time()-base['started_epoch'],partial_time_scope='Offline coding/pure fakechecks,not the future one-shot live60min clock or measuredwholeturn.',snapshot_manifest=rel(A/'snapshot-manifest.json'),next='STOP_FOR_EXACT_INDEPENDENT_PRECHECK;COUNTFEES_MUST_RESOLVE_OR_NEW_REVIEWED_ZEROCOUNT_VERSION_BEFORE_LIVE'))
snapshot=A/'snapshot';snapshot.mkdir()
paths=[*N.rglob('*'),REG,*RESULT.rglob('*'),*[R/n for n in source],R/'docs/HANDOFF.md',R/'docs/PROJECT_STATUS.md']
for p in paths:
 if not p.is_file() or '__pycache__' in p.parts:continue
 assert not p.is_symlink() and not p.is_relative_to(R/'build/private');target=snapshot/rel(p);target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():assert sha(target)==sha(p)
 else:shutil.copy2(p,target)
assert all(sha(R/n)==h for n,h in base['protected'].items())
assert all(sha(R/n)==h for n,h in oldfreeze.items())
assert hashlib.sha256(subprocess.check_output(['git','ls-files','--stage','-z'],cwd=R)).hexdigest()==base['index_sha256']
files={p.relative_to(A).as_posix():sha(p) for p in A.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
write(A/'snapshot-manifest.json',dict(status='OFFLINE_PREPARED_LIVE_BLOCKED',files=files,file_count=len(files),excluded=['snapshot-manifest.json(selfhash)','__pycache__','Allbuild/private credential files'],scope='Exact R01source and versioned pure/mock/replay evidence;no live API/SV execution or fee determination.'))
print(json.dumps(dict(status='R01_SEALED_OFFLINE_API_BLOCKED',phase_sha256=sha(A/'phase.json'),snapshot_manifest_sha256=sha(A/'snapshot-manifest.json'),registration_sha256=sha(REG),source_manifest_sha256=sha(N/'source-manifest.json'),snapshot_files=len(files),source_members=len(source),API=0,SDK=0,real_SV_tools=0,secret_read_or_hashed=False,live_root_absent=True,count_fee='UNKNOWN'),indent=2))
