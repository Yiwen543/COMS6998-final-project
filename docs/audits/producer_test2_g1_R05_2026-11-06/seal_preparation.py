"""Seal conditional R05 pure preparation; never creates execution authority."""
from pathlib import Path
import ast,hashlib,json,shutil,subprocess,time
R=Path(__file__).resolve().parents[3];A=Path(__file__).resolve().parent;N=R/'test2/g1_v5';RESULT=R/'test2/results/g1-qualification-v5';REG=R/'test2/configs/g1_qualification_registration_v5_draft.json';E=R/'docs/audits/producer_test2_g1_E03_2026-11-06'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
def rel(p):return p.relative_to(R).as_posix()
def write(p,x):
 with p.open('x') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
before=read(A/'before-preparation.json');reuse=read(N/'conditional-reuse.json');summary=read(RESULT/'preparation-attempt2/summary.json');resource=read(A/'conditional-resources.json')
assert not (A/'phase.json').exists() and not (N/'source-manifest.json').exists()
assert summary['passed'] and summary['tests']==13 and summary['failures']==summary['errors']==0
for name,h in summary['source_sha256'].items():assert sha(N/name)==sha(RESULT/'preparation-attempt2/executed-source'/name)==h
inputs_checked=0
for case in sorted((RESULT/'preparation-attempt2').glob('test_*')):
 for n,h in read(case/'input-bindings.json').items():assert sha(case/'inputs'/n)==h;inputs_checked+=1
assert all(sha(R/n)==h for n,h in reuse['files'].items())
assert len(list((N/'sources').glob('*.sv')))==18
assert all(sha(R/p['old'])==sha(R/p['new'])==p['sha256'] for p in reuse['unchanged_hardware_and_input_pairs'])
assert sha(N/'observations.py')==sha(R/'test2/g1_v4/observations.py')
for name,pin in reuse['tool_pins'].items():assert sha(Path(pin['configured']).resolve())==pin['resolved_sha256'],name
for p in N.glob('*.py'):ast.parse(p.read_text(),filename=rel(p))
for root,base in [(E,E),(R/'docs/audits/producer_test2_g1_R04_2026-11-06',R/'docs/audits/producer_test2_g1_R04_2026-11-06')]:
 m=read(root/'snapshot-manifest.json');assert all(sha(base/n)==h for n,h in m['files'].items())
assert sha(E/'snapshot-manifest.json')==before['E03_snapshot_manifest_sha256']
old=read(R/'docs/audits/producer_test2_g1_R04_2026-11-06/preservation-before.json');assert all(sha(R/n)==h for n,h in old['files'].items())
assert hashlib.sha256(subprocess.check_output(['git','ls-files','--stage','-z'],cwd=R)).hexdigest()==before['index_entries_sha256']
assert all(sha(R/'docs'/n)==h for n,h in before['shared_docs_sha256'].items())
assert not any((RESULT/n).exists() for n in ['execution-state.json','attempt.lock'])
assert not (N/'runner.py').exists() and read(REG)['execution_allowed'] is False
write(A/'checks.json',dict(pure_tests=13,failures=0,errors=0,seconds=summary['seconds'],test_command='PYTHONDONTWRITEBYTECODE=1 .venv/bin/python test2/g1_v5/pure_tests.py --record test2/results/g1-qualification-v5/preparation-attempt2',tool_receipt='801299',case_inputs_checked=inputs_checked,two_actual_saved_log_cases=True,synthetic_unknown_cases=10,synthetic_unreached_format_control=1,no_new_QC_or_RTL_coverage=True,initial_failed_launch_retained='preparation-incidents.json',old_suites_experiments_rerun=False,real_G1_setup_compile_native_physical_calls=0,process_signal_sleep_blocked_during_tests=True,hardware_files_unchanged=18,input_tables_unchanged=3,protected_old_files=len(old['files']),all_hash_mismatches=[],source_tool_pins_checked_as_bytes_only=True,new_version_queries=0,source_primary_reference=dict(path='/opt/homebrew/Cellar/yosys/0.70/bin/yosys-smtbmc',sha256=sha(Path('/opt/homebrew/Cellar/yosys/0.70/bin/yosys-smtbmc')),lines='1934-1983: reached is logged before assertion-failure break;1500-1507: assertion failure logging'),shared_docs_untouched=True,index_unchanged=True,new_pool_lock_or_authority_created=False))
write(A/'hallmark-usage.json',dict(skill='/Users/yiwenchen/.codex/skills/hallmark/SKILL.md',sha256=sha(Path('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md')),reused_actual_read='R04 resumed SKILL.md lines1-150;not a fresh full read',applied=['Use real saved evidence as material,not invented PASS metrics.','Separate original labels,raw status,activation and qualification.','One narrow parser repair and focused verification batch;no UI or new framework.'],UI_scripts_or_certification=False,not_RTL_or_independent_qualification=True))
report=f'''# R05 conditional pure preparation

Status: **PREPARED_CONDITIONAL_PENDING_P15_AND_NEW_AUTHORITY**.
Scientific qualification remains **BLOCKED/NOT_QUALIFIED**. No runner/pool/lock,
actual tool invocation or budget authority was created. SharedHANDOFF/STATUS were
intentionally left unchanged during parallel P15 review.

New single-cover reader keeps raw tool status and exit separate from activation
REACHED/UNREACHED/UNKNOWN and assertion observation. Exact sourceID/log/receipt/
argv/trace hashes and sampled activation at reported SMT step are required.
Missing,contradictory,unsupported or unbound records remain UNKNOWN. No failure
becomes toolPASS,no absent failure line becomes assertion proof. UNREACHED is a
finite invocation report,not unbounded unreachability or128completion.

Two actual saved cases pass reader checks:E02QC00 PASSED/exit0+REACHED and
E03QC01 FAILED/exit1+REACHED+assertFAILED. Oldv4NOT_REACHED/rawFAILED unchanged.
Ten synthetic unknown controls and one synthetic-unreached format control are
explicitly fixtures,not new realQC observations,physical tests orRTLcoverage.
Final suite13/13PASS,0fail/error,{summary['seconds']:.9f}s. Initial entry launch failed
before any testcase because recordparent absent;incident and exact old source
retained,then parent creation repaired. Final testcase sources/inputs/logs saved.
No older suite/experiment was rerun. Process/run/signal/sleep blocked in tests.

18SV/3inputtables and physical parser matchv4byte-for-byte. No hardware,stimulus,
label,oracle,model,toolflags or threshold changed. Original coverPASS label stays;
activation-only interpretation and negative-control assertion handling require
explicit independent review before integration. This is a reader prototype,not
an implemented executable R05 pipeline or a completed G1 qualification.

Conditionalreuse binds163saved files,E02QC00native plusE03sharedphysicalbuilds,
QC00dualsim,QC01frontend/BMC/cover logs/models/receipts and exact compiled binaries.
New conditional plan72remaining jobs=0setup+14compile+28native+30physical/120cycles;
projected cumulative8/20/32/33/132,within existing caps if all reuse is accepted.
Prior cumulative8/6/4/3/12 retained. Actual checkpoint{resource['prior_actual_checkpoint_seconds']:.9f}s
and charged checkpoint{resource['prior_charged_checkpoint_seconds']:.9f}s remain separate.
Proposed conservative15/current1185 is not authority,measured spend or reset.
Any unsafe reuse requires stopping and reporting concrete extra cost.

Needed from coordinator:exact P15review/hash and accepted reuse/interpretation,
new immutable continuation allocation bound to E03pool
{resource['prior_pool_sha256']},all prior counts/checkpoints,actual new window/caps.
Then wire only necessary new runner/report gates and obtain independent preflight
of final source/registration/preparation hashes before any exact EXECUTE. No fake
positive authority/approval was constructed. Native/physical caps have no retry
reserve under this conditional full-completion plan.

OldE01/E02/E03/v4/R04/failures/sourcefreezes/index unchanged;all4485historical files
verified. No modelAPI/key/paid/raw/B/C/crossIP/install/commit/push. New diagnostics
are saved-byte parses,not independent trials. All vacuity/four-state/128completion/
realDUT/oracle/74witness/C-benefit/billing and prior scientific limits remain.
'''
with (A/'report.md').open('x') as f:f.write(report)
source_files={rel(p):sha(p) for p in N.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
for p in [REG,A/'conditional-resources.json']:source_files[rel(p)]=sha(p)
write(N/'source-manifest.json',dict(status='CONDITIONAL_PURE_PREPARATION_NOT_EXECUTION',files=source_files,external_immutable_dependencies=reuse['files'],execution_allowed=False,scope='New parser/sources/tests/draftplan;references exact retained E02/E03 dependencies. P15/new authority and full integration still pending.'))
write(A/'phase.json',dict(phase='G1_R05_CONDITIONAL_PURE_PARSER_PREPARATION',status='PREPARED_CONDITIONAL_PENDING_P15_AND_NEW_AUTHORITY',scientific_qualification='BLOCKED_NOT_QUALIFIED',actual_HEAD=before['actual_HEAD'],registration=rel(REG),registration_sha256=sha(REG),source_manifest=rel(N/'source-manifest.json'),source_manifest_sha256=sha(N/'source-manifest.json'),conditional_reuse_sha256=sha(N/'conditional-reuse.json'),E03_manifest_sha256=sha(E/'snapshot-manifest.json'),old_E03_pool_sha256=resource['prior_pool_sha256'],P15_review_sha256=None,new_authority_sha256=None,EXECUTE=None,real_execution_entrypoint=None,conditional_new_counts=resource['proposed_new'],conditional_cumulative=resource['projected_cumulative'],prior_charge15_window1185_status='PROPOSED_ONLY_PENDING_EXACT_ROOT_AUTHORITY',pure_tests=13,pure_failures=0,pure_errors=0,pure_summary_sha256=sha(RESULT/'preparation-attempt2/summary.json'),initial_launch_failure_retained=True,real_new_G1_jobs=0,old_files_verified=len(old['files']),shared_docs_modified=False,index_unchanged=True,model_API_key_paid_raw_B_C_crossIP_commit_push=0,partial_preparation_seconds=time.time()-before['start_epoch'],partial_time_scope='Metadata/pure preparation only;not registered execution budget or full-turn elapsed.',snapshot_manifest=rel(A/'snapshot-manifest.json'),next='STOP_PURE_CHECKPOINT;ROOT_P15_AND_EXACT_NEW_AUTHORITY_BEFORE_FINAL_INTEGRATION_AND_PREFLIGHT'))
snapshot=A/'snapshot';snapshot.mkdir()
for p in [*N.rglob('*'),REG,*RESULT.rglob('*')]:
 if not p.is_file() or '__pycache__' in p.parts:continue
 assert not p.is_symlink();target=snapshot/rel(p);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
files={p.relative_to(A).as_posix():sha(p) for p in A.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
write(A/'snapshot-manifest.json',dict(status='CONDITIONAL_PURE_PENDING_P15',files=files,file_count=len(files),external_immutable_dependencies=reuse['files'],excluded=['snapshot-manifest.json(self-hash)','__pycache__'],scope='R05 pure sources/tests/conditional plan;old E02/E03 external dependencies verified and retained in existing packages.'))
print(json.dumps(dict(status='R05_PURE_PREPARATION_SEALED_BLOCKED_PENDING_P15',phase_sha256=sha(A/'phase.json'),snapshot_manifest_sha256=sha(A/'snapshot-manifest.json'),registration_draft_sha256=sha(REG),source_manifest_sha256=sha(N/'source-manifest.json'),pure_tests=13,failures=0,real_new_G1_jobs=0,snapshot_files=len(files),external_files=len(reuse['files']),new_authority_created=False),indent=2))
