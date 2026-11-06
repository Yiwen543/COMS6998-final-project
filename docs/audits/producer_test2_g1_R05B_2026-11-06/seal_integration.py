"""Seal new R05B integration evidence and additive progress;no actual tools."""
from pathlib import Path
import ast,hashlib,json,shutil,subprocess,time
R=Path(__file__).resolve().parents[3];A=Path(__file__).resolve().parent;N=R/'test2/g1_v5b';RESULT=R/'test2/results/g1-qualification-v5b';REG=R/'test2/configs/g1_qualification_registration_v5b.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
def rel(p):return p.relative_to(R).as_posix()
def write(p,x):
 with p.open('x') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
base=read(A/'before-preparation.json');reg=read(REG);suite=RESULT/'preparation-attempt1';summary=read(suite/'summary.json')
assert summary['tests']==11 and summary['passed'] and summary['failures']==summary['errors']==0
assert not (A/'phase.json').exists() and not (N/'source-manifest.json').exists()
for n,h in summary['source_sha256'].items():assert sha(R/n)==sha(suite/'executed-source'/n)==h
inputs=0
for case in suite.glob('test_*'):
 for n,h in read(case/'input-bindings.json').items():assert sha(case/'inputs'/n)==h;inputs+=1
for name,expected in [('producer_test2_g1_R05_2026-11-06',base['old_R05_manifest_sha256']),('producer_test2_g1_E03_2026-11-06',base['old_E03_manifest_sha256'])]:
 folder=R/'docs/audits'/name;m=read(folder/'snapshot-manifest.json');assert sha(folder/'snapshot-manifest.json')==expected and all(sha(folder/n)==h for n,h in m['files'].items())
assert sha(N/'runtime.py')==sha(R/'test2/g1_v4/runtime.py')
assert (N/'budget.py').read_text().replace("attempt_id='R05_CUMULATIVE_CONTINUATION'","attempt_id='R04_CONDITIONAL_CONTINUATION'")==(R/'test2/g1_v4/budget.py').read_text()
assert sha(N/'e02_native_reuse.py')==sha(R/'test2/g1_v4/native_reuse.py')
for p in N.glob('*.py'):ast.parse(p.read_text(),filename=rel(p))
old=read(R/'docs/audits/producer_test2_g1_R04_2026-11-06/preservation-before.json');assert all(sha(R/n)==h for n,h in old['files'].items())
assert hashlib.sha256(subprocess.check_output(['git','ls-files','--stage','-z'],cwd=R)).hexdigest()==base['index_sha256']
assert not any((RESULT/n).exists() for n in ['execution-state.json','attempt.lock'])
reuse=read(R/reg['reuse_manifest']);assert all(sha(R/n)==h for n,h in reuse['files'].items())
write(A/'checks.json',dict(pure_command='PYTHONDONTWRITEBYTECODE=1 .venv/bin/python test2/g1_v5b/integration_tests.py --record test2/results/g1-qualification-v5b/preparation-attempt1',test_tool_receipt='5444f1',tests=11,failures=0,errors=0,seconds=summary['seconds'],final_tested_source=True,final_mutated_inputs_checked=inputs,old_R05_13_tests_and_error_preserved=True,old_E03_R04_v4_unchanged=True,runtime_identical=True,budget_change='Attempt-id text only',E02_reuse_reader_identical=True,hardware18_and_input3_unchanged=True,new_actual_jobs=0,new_real_pool_lock_or_EXECUTE=False,positive_full_P16_entry_exercised=False,full_72_job_mock_or_actual_execution=False,old_suite_or_experiment_rerun=False,all4485_protected_old_files_unchanged=True,index_unchanged=True))
write(A/'hallmark-usage.json',dict(skill='/Users/yiwenchen/.codex/skills/hallmark/SKILL.md',sha256=sha(Path('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md')),read_reused='R04 resumed lines1-150;no new full read claimed',applied=['Keep raw material/status distinct from activation/qualification.','Use small exact repair,real saved evidence and bounded focused checks.','Record missing future execution evidence rather than invented full success.'],UI_workflow_executed=False,not_RTL_or_independent_certification=True))
report=f'''# R05B integrated continuation preparation

Status **PREPARED_PENDING_P16**,G1 **BLOCKED/NOT_QUALIFIED**. No actual tool,pool,
lock or EXECUTE created. This is a new integration namespace;sealed R05pure145
files/13checks/initial error,E03/v4 and all old scientific evidence are unchanged.

P15-R1 is addressed by raw tool/exit,activation and assertion fields. QC01saved
cover remains FAILED/exit1,REACHED/assertFAILED;oldNOT_REACHED stays in original_job.
Registration interpretation is based on unchanged singlecover source and original
labels. BMC assertion expectation remains separate;cover tests activation,with
explicit negative/positive assertion-observation policies. No FAILED becomes
PASSED,no missing/truncated/error/timeout evidence meets a target. Cover VCD
terminal sentinel is checked in the integration without modifying sealed R05.

Exact reused E02three and E03seven jobs retain all old charges and new_execution
false. Source/log/receipt/VCD/SMT/build/executable/tool bindings verified. New
trace/output paths only;old physical binaries are read only. All18SV,stimulus,
labels,guards,timing,flags/tools and physical parser stay byte-identical. Runtime
identical,budget attempt-id only;no specification oracle edited.

Actual R05allocationSHA{reg['continuation_decision_sha256']} binds closed E03pool
{reg['predecessor_pool_sha256']},prior setup8/compile6/native4/physical3/12cycles,
actual11.770645541138947s versuscharged14.572948167100549s. Allocation charge15/
current1185/work1180 keeps original1200 and is not measured spend/reset. Planned
72roots=0setup+14compile+28native+30physical120cycles;final8/20/32/33/132. Native/
physical retry reserve0;unsafe reuse/new failure stays charged and stops. No
setup/versionquery,ps or new permissions. Existing mandatory PGID/poll/kill/wait/
deadline protections retained;childcensus and OS realtime/memory limits remain.

New final-source suite11/11PASS,0fail/error,{summary['seconds']:.9f}s. Checks actual
allocation and10reuse jobs,savednegativecover,exactremainingplan,unknown judgment,
missingP16/oldgate beforeclaim,countreset,binarydrift,syntheticledger caps,
truncatedcoverVCD and missingBMCwitness. All subprocess/run/signal/sleep blocked.
Not a full72job mock or real G1 run;no positive P16 approval fabricated. Future
source/tool/phase problems remain possible. Old tests/experiments not rerun.

Final registration/source/preparation manifest requires independent P16 binding;
then coordinator exact EXECUTE is necessary. No automatic execution after sealing.
SharedHANDOFF/STATUS get additive notes only,with complete old bodies retained.
No API/key/paid/raw/B/C/crossIP/install/commit/push. Four-state/vacuity/128completion/
realDUT/oracle/74witness/C-benefit/billing and earlier limits remain. P2 unchanged.
'''
with (A/'report.md').open('x') as f:f.write(report)
section=f'''\n\n## Current G1 preparation — R05B integrated, pending P16 (2026-11-06)

P15 found only P15-R1 classifier issue;E03evidence/resources accepted withlimits.
R05B newnamespace integrates sealedR05reader without editing R05/E03/v4. QC01
rawFAILED/exit1,activationREACHED/assertFAILED are separate;oldNOT_REACHED preserved.
All18SV/inputs/labels/flags/tools/timing/guards unchanged;runtimeidentical,budget
attempt-idonly. Ten E02/E03reusedjobs explicitnew_executionfalse,oldinvalidphysics
neverreused;allraw/SMT/binary/build/receipt/sourcehashesbound,newoutputs-only.

Actual R05allocationcharge15/current1185/work1180 inherits8setup/6compile/4native/
3physical12cycles,actual11.770645541s versuscharged14.572948167s;notreset/spend15s.
New72roots0setup/14compile/28native/30physical120cycles -> cumulative8/20/32/33/132.
No native/physicalretryreserve. G1stillBLOCKED_NOT_QUALIFIED;newpool/lock absent.
New11pureintegrationchecksPASS(0.057237125s),notfullmock/actualrun orP16acceptance.

Exact `docs/audits/producer_test2_g1_R05B_2026-11-06/phase.json` /snapshot-manifest;
source `test2/g1_v5b/`,reg `test2/configs/g1_qualification_registration_v5b.json`.
Next existing P16 must bind finalmanifest/reg/source/reuse/actualdecision/amendment;
coordinator exactEXECUTE onlyafteracceptance. No actualSVtools/API/key/paid/raw/B/C/
crossIP/install/commit/push. All4485historicalfiles,R05pure145files/13checks/error,
E03/oldfailures/unknowns/index preserved,actualHEAD2de33e981d2fffc9739d2ca049fbae1774de1aad.
Fulloldbodies and allscientific/128/fourstate/vacuity/74witness/C/billinglimits retained.
'''
shared={}
for name in ['HANDOFF.md','PROJECT_STATUS.md']:
 p=R/'docs'/name;oldbytes=p.read_bytes();saved=A/'before/docs'/name;saved.parent.mkdir(parents=True,exist_ok=True)
 with saved.open('xb') as f:f.write(oldbytes)
 header,body=oldbytes.split(b'\n',1);p.write_bytes(header+section.encode()+body);assert p.read_bytes().endswith(body);shared[name]=dict(before_sha256=sha(saved),after_sha256=sha(p),entire_old_body_retained=True)
source={rel(p):sha(p) for p in N.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
source.update(read(R/'test2/g1_v5/source-manifest.json')['files']);source.update(reuse['files'])
paths=[REG,R/'test2/g1_v5/source-manifest.json',A/'P16-review-checklist.md']
for key in ['user_authorization','user_physical33_authorization','budget_amendment','first_pool','E02_pool','predecessor_pool','predecessor_phase','predecessor_manifest','predecessor_review','continuation_decision']:paths.append(R/reg[key])
paths.append(R/'docs/audits/agent_bridge_2026-11-06/P15_g1_R04_execution/continuation-feasibility.json')
for p in paths:source[rel(p)]=sha(p)
write(N/'source-manifest.json',dict(status='PREPARED_PENDING_P16_NOT_EXECUTE',files=source,shared_mutable_docs_excluded=True,scope='Exact new R05B sources,old immutable reader/hardware/reuse/artifacts and actual authority;P16+EXECUTE still required.'))
write(A/'phase.json',dict(phase='G1_R05B_INTEGRATED_CONTINUATION_PREPARATION',status='PREPARED_PENDING_P16',scientific_qualification='BLOCKED_NOT_QUALIFIED',actual_HEAD=base['actual_HEAD'],registration=rel(REG),registration_sha256=sha(REG),source_manifest=rel(N/'source-manifest.json'),source_manifest_sha256=sha(N/'source-manifest.json'),reuse_manifest_sha256=sha(R/reg['reuse_manifest']),continuation_decision_sha256=reg['continuation_decision_sha256'],budget_amendment_sha256=reg['budget_amendment_sha256'],P15_review_sha256=reg['predecessor_review_sha256'],E03_pool_sha256=reg['predecessor_pool_sha256'],old_R05_manifest_sha256=base['old_R05_manifest_sha256'],prior_reserved=reg['prior_reserved'],prior_actual_checkpoint_seconds=reg['prior_actual_window_seconds'],prior_charged_checkpoint_seconds=reg['prior_charged_checkpoint_seconds'],prior_allocation_charge_seconds=15,current_attempt_max_seconds=1185,work_cutoff_seconds=1180,planned_new=dict(setup=0,compile=14,native=28,physical=30,physical_cycles=120),pure_tests=11,pure_failures=0,pure_errors=0,pure_summary_sha256=sha(suite/'summary.json'),actual_new_G1_jobs=0,new_pool_or_lock=False,P16=None,EXECUTE=None,all_old_source_evidence_preserved=True,index_unchanged=True,shared_document_additions=shared,full_positive_entry_or_complete72_mock_exercised=False,partial_preparation_seconds=time.time()-base['start_epoch'],partial_time_scope='Offline implementation/pure checks;not G1 execution budget or fullturntime.',snapshot_manifest=rel(A/'snapshot-manifest.json'),next='STOP_FOR_EXISTING_P16;NO_REAL_EXECUTION_BEFORE_EXACT_ACCEPTANCE_AND_COORDINATOR_EXECUTE'))
snapshot=A/'snapshot';snapshot.mkdir()
for p in [*N.rglob('*'),REG,*RESULT.rglob('*'),*[R/n for n in source],R/'docs/HANDOFF.md',R/'docs/PROJECT_STATUS.md']:
 if not p.is_file() or '__pycache__' in p.parts:continue
 assert not p.is_symlink();target=snapshot/rel(p);target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():assert sha(target)==sha(p)
 else:shutil.copy2(p,target)
files={p.relative_to(A).as_posix():sha(p) for p in A.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
write(A/'snapshot-manifest.json',dict(status='PREPARED_PENDING_P16',files=files,file_count=len(files),excluded=['snapshot-manifest.json(self-hash)','__pycache__'],scope='Exact R05B integration,pure tests and hash-bound reused dependencies;not EXECUTE or G1 qualification.'))
print(json.dumps(dict(status='R05B_SEALED_PENDING_P16',phase_sha256=sha(A/'phase.json'),snapshot_manifest_sha256=sha(A/'snapshot-manifest.json'),registration_sha256=sha(REG),source_manifest_sha256=sha(N/'source-manifest.json'),reuse_manifest_sha256=sha(R/reg['reuse_manifest']),files=len(files),source_files=len(source),pure_tests=11,actual_G1_jobs=0,new_pool_lock=False),indent=2))
