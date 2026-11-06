"""R04 preparation metadata sealing only; no real tools or authorization."""
from pathlib import Path
from collections import Counter
import ast,difflib,hashlib,json,shutil,subprocess,time

ROOT=Path(__file__).resolve().parents[3]
AUDIT=Path(__file__).resolve().parent
OLD=ROOT/'test2/g1_v3'
NEW=ROOT/'test2/g1_v4'
RESULT=ROOT/'test2/results/g1-qualification-v4'
REG=ROOT/'test2/configs/g1_qualification_registration_v4.json'
STATUS='PREPARED_PENDING_PHYSICAL33_APPROVAL_AND_P14'

def sha(p):
    assert p.is_file() and not p.is_symlink(),p
    return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def rel(p):return p.relative_to(ROOT).as_posix()
def write(p,value):
    with p.open('x') as f:f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT)

assert not (AUDIT/'phase.json').exists()
base=read(AUDIT/'preservation-before.json');reg=read(REG)
assert all(sha(ROOT/p)==s for p,s in base['files'].items())
assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==base['index_sha256']
for key in ['pool_state','attempt_lock','continuation_decision','budget_amendment']:
    assert not (ROOT/reg[key]).exists(),key
assert reg['continuation_decision_sha256'] is None and reg['budget_amendment_sha256'] is None
assert reg['original_caps']['physical_jobs']==32 and reg['caps']['physical_jobs']==33
semantic=read(ROOT/'docs/audits/producer_test2_g1_R02_2026-11-05/change-and-evidence-map.json')['unchanged_semantic_input_sha256']
unchanged={name:s for name,s in semantic.items() if name!='sources/physical_tb.sv'}
assert len(unchanged)==23 and all(sha(OLD/p)==sha(NEW/p)==s for p,s in unchanged.items())
assert len(list(NEW.glob('sources/*.sv')))==18
assert all(sha(OLD/name)==sha(NEW/name) for name in ['runtime.py','observations.py'])
assert (NEW/'budget.py').read_text().replace("attempt_id='R04_CONDITIONAL_CONTINUATION'","attempt_id='R03_CONTINUATION'")==(OLD/'budget.py').read_text()
old_plan=read(OLD/'job-plan.json');plan=read(NEW/'job-plan.json')
old_plan['jobs']=[j for j in old_plan['jobs'] if j['kind']!='setup' and j['id'] not in ['compile-QC00','QC00-bmc','QC00-cover']]
assert json.dumps(plan).replace('/g1_v4/','/g1_v3/')==json.dumps(old_plan)
assert Counter(j['kind'] for j in plan['jobs'])=={'compile':17,'native':30,'physical':32}
assert sum(j.get('cycles',0) for j in plan['jobs'])==128
for path in NEW.glob('*.py'):ast.parse(path.read_text(),filename=rel(path))
reuse=read(NEW/'native-reuse.json')
assert all(sha(ROOT/p)==s for p,s in reuse['files'].items())
assert sha(ROOT/'test2/results/g1-qualification-v3/build/QC00/model.smt2')=='0d31e016299e8841d685c8f528a20345819aff378c268b089d4033f5b1953636'

suite=RESULT/'preparation-attempt1';summary=read(suite/'summary.json')
assert summary['tests']==16 and summary['passed'] and summary['failures']==summary['errors']==0
for name,s in summary['source_sha256'].items():
    current=REG if name=='registration.json' else NEW/name
    assert sha(current)==sha(suite/'executed-source'/name)==s
cases=sorted(suite.glob('test_*'));assert len(cases)==16
inputs_checked=0
for case in cases:
    assert (case/'result.json').is_file()
    for name,s in read(case/'input-bindings.json').items():
        assert sha(case/'inputs'/name)==s;inputs_checked+=1
assert sha(cases[0]/'inputs/physical_tb.sv')==sha(NEW/'sources/physical_tb.sv')
write(AUDIT/'commands-and-checks.json',dict(
    pure_test_command=['PYTHONDONTWRITEBYTECODE=1','.venv/bin/python','test2/g1_v4/r04_tests.py','--record',rel(suite)],
    test_exit_code=0,test_tool_receipt='ed8b71',summary_sha256=sha(suite/'summary.json'),
    unittest_log_sha256=sha(suite/'unittest.log'),tests=16,failures=0,errors=0,seconds=summary['seconds'],
    exact_final_tested_sources=True,final_mutated_inputs_checked=inputs_checked,
    actual_R04_setup_compile_native_physical_process_signal_sleep=0,
    source_timing_arithmetic_is_not_simulator_validation=True,
    approved_entry_and_positive_budget_integration_tested=False,
    old_suites_or_experiments_rerun=False,
    sealing_command=['PYTHONDONTWRITEBYTECODE=1','.venv/bin/python',rel(Path(__file__))],
    sealing_scope='Read/hash/snapshot/Gitmetadata only;no real G1 jobs or permission grant.'))
diff=''.join(difflib.unified_diff((OLD/'sources/physical_tb.sv').read_text().splitlines(True),
    (NEW/'sources/physical_tb.sv').read_text().splitlines(True),fromfile='g1_v3/sources/physical_tb.sv',tofile='g1_v4/sources/physical_tb.sv'))
with (AUDIT/'physical-startup.diff').open('x') as f:f.write(diff)
changes=[]
for path in sorted(NEW.rglob('*')):
    if not path.is_file() or '__pycache__' in path.parts:continue
    name=path.relative_to(NEW);old=OLD/name
    if not old.is_file() or sha(old)!=sha(path):
        changes.append(dict(file=rel(path),before_sha256=sha(old) if old.is_file() else None,
                            after_sha256=sha(path),kind='ONLY_SV_CHANGE' if name.as_posix()=='sources/physical_tb.sv' else 'NECESSARY_R04_GATE_REUSE_METADATA_OR_PURE_TEST'))
write(AUDIT/'change-and-dependency-map.json',dict(status=STATUS,changes=changes,
    changed_SV_files=['sources/physical_tb.sv'],unchanged_semantic_reference_sha256=unchanged,
    unchanged_SV_count=17,unchanged_material_count=23,
    unchanged_runtime_sha256=sha(NEW/'runtime.py'),unchanged_observations_sha256=sha(NEW/'observations.py'),
    budget_change='Attempt-id text only;Allocation imports new proposed caps but actual approval/P14 required before Budget.',
    job_plan_change='Omit7setup plus compile-QC00/QC00-bmc/QC00-cover;otherwise path-normalized argv/order identical.',
    native_reuse_manifest_sha256=sha(NEW/'native-reuse.json'),
    resource_proposal_sha256=sha(AUDIT/'resource-proposal.json'),
    authority_requirements_sha256=sha(AUDIT/'authority-requirements.json'),
    old_rejected_physical_reused=False,SV_repair_experimentally_verified=False))
source_inputs={rel(p):sha(p) for p in sorted(NEW.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
for name,s in reuse['files'].items():source_inputs[name]=s
bound=[REG,ROOT/reg['user_authorization'],ROOT/reg['first_pool'],ROOT/reg['predecessor_pool'],
    ROOT/reg['predecessor_phase'],ROOT/reg['predecessor_review'],
    ROOT/'docs/audits/agent_bridge_2026-11-06/P13_g1_retry_execution/review.md',
    ROOT/'docs/audits/agent_bridge_2026-11-06/P13_g1_retry_execution/budget-feasibility.json',
    AUDIT/'P14-review-checklist.md',AUDIT/'resource-proposal.json',AUDIT/'authority-requirements.json']
for p in bound:source_inputs[rel(p)]=sha(p)
write(NEW/'source-manifest.json',dict(kind='R04_CONDITIONAL_PREPARATION_NOT_AUTHORIZATION',files=source_inputs,
    status=STATUS,physical33_user_approval='PENDING_NOT_INFERRED',
    continuation_decision='ABSENT_PENDING_COORDINATOR',independent_review='PENDING_P14',
    SV_startup_fix_measured=False,actual_R04_jobs=0,
    external_approval_note='Later actual amendment/decision hashes must be independently bound by exact P14+EXECUTE. Not synthesized here.',
    shared_mutable_docs_excluded=True))

report='''# R04 conditional startup repair preparation

Status: PREPARED_PENDING_PHYSICAL33_APPROVAL_AND_P14. G1 remains BLOCKED/NOT_QUALIFIED.
P13 failure/evidence accepted only with limits;all E01/E02/R03/P12/P13 originals,
old111pure cases,scores/checker/freezes/unknowns and Git index are preserved.

Only physical_tb.sv changes among18SV:step7,time-positive1ps transition tostep0,
first999ps wait. Source arithmetic preserves all pre/edge/post times,16ns end,
four posedges,marker phase and exact old input/label tables. No #0 assumption,
X filling,first-row omission or new DUT clock. Actual dual-simulator startup
behavior,syntax and ABI are NOT_TESTED;no measured repair claim.

23 materials including common/all16formal harnesses are unchanged. Saved QC00
SMT/Yosys compile1 and BMC+cover2 are conditionally hash-bound for explicit
REUSED_FROM_E02,not new samples or physics. Old rejected physical remains rejected.
New plan79roots=0setup+17compile+30native+32physical/128cycles. Cumulative projected
setup8/compile20/native32/physical33/cycles132. Original physical cap32 permits only
31new runs,so full32new physical cannot execute without actual +1 approval. If
native reuse is invalid,cumulative native34(+2) and compile21 must be rerouted;
there is no automatic fallback. resource-proposal.json records arithmetic and
failure conditions,not authorization.

Proposed prior conservative charge8s covers recorded7.151973249856383 but is not
actual spend. Prior actual checkpoint5.197697583120316 stays separate. Current
proposed1192/work1187 preserves total1200. Old E01/E02 pools stay halted/completed;
new pool/lock remain absent. Budget only changes attempt-id text;new allocation
loads actual narrow physical33 amendment/continuation and exact inherited lineages
before any lock. No actual approval document or EXECUTE has been manufactured.

16pure checks PASS,0fail/error,0.071835s;exact Python/reg/plan/reuse source and
final-mutated inputs are saved. Checks cover source time arithmetic,unchanged
dependencies/old native prefix,drift refusals,resource lower bound,missing/unapproved
authority/P14/old receipts,actual-entry0claim and synthetic X rejection. Real
Popen/run/killpg/sleep are forbidden mocks. Approved-entry success,new positive
Budget integration and complete dual-simulator/replay execution remain untested.
No old suite/experiment or production parser of the old physical trace was rerun.

Next: existing P14 incremental preparation review. Parent already handles user
physical33 decision;producer asks no duplicate question. A code-only precheck
without actual decision/amendment hashes cannot execute. Later P14 input_identity
must bind new producer manifest/registration plus those actual authority hashes;
then coordinator supplies exact EXECUTE. No real tool probe/version/build/sim,
pool/lock/API/key/network/install/delete/index/commit/push/G2–G5/PPT/newagent/chat.
P12-N1 earlier-turn PPT/web scope remains disclosed;R04 zero-network applies to
this controlled preparation only. All vacuity/four-state/128completion/74witness/
selected-sample/C-benefit/billing/P04/P05/P06/P05-N1/F1/H1/H2/L1 limits remain.
'''
with (AUDIT/'report.md').open('x') as f:f.write(report)
section='''

## Current G1 repair preparation — R04 / pending physical33 approval and P14 (2026-11-06)

R04 **PREPARED_PENDING_PHYSICAL33_APPROVAL_AND_P14**;G1 remains BLOCKED/NOT_QUALIFIED. New `test2/g1_v4/` changes only physical_tb.sv among18SV:step7 then positive1ps step0 transition,first999ps wait. Source arithmetic keeps all0..3pre/posedge/post times,16ns end/4posedge/marker;no#0,Xfilling or skipped row. Startup fix NOT_MEASURED:0real version/compile/native/physical/probe jobs.23semantic-reference materials/common/all16formal harnesses and runtime/observations unchanged.

Exact saved QC00 SMT/frontend compile1 and nativeBMC+cover2 conditionally REUSED_FROM_E02,not new executions;all original costs inherited and rejected physical never reused. New proposal0setup/17compile/30native/32physical128cycles -> cumulative8/20/32/33runs132cycles. Physical32->33 remains pending parent's user question;noapproval/EXECUTE fabricated,no duplicate question. If reuse invalid,native cumulative34 needs +2 and rerouting,nofallback. Prior actual5.197697583s vs charged7.151973250s retained;proposed charge8/current1192/work1187 keeps total1200,not actual8s spend. Both old pools stayclosed,new pool/lock absent.

New16pure source/metadata/refusal tests PASS(0.071835s),noSV scheduling/ABI or approved full-entry validation. Saved source/final-mutated fixtures/logs retained;old111mock history/E01/E02/R03/P12/P13/rawX/unknown/scores/checker/index unchanged. Exact `docs/audits/producer_test2_g1_R04_2026-11-06/phase.json` / `snapshot-manifest.json`,resource-proposal andauthority-requirements. Existing P14 next reviews preparation;actual authority hashes must later be bound by P14+coordinator EXECUTE. Stophere,no realtools/API/key/network/install/delete/index/commit/push/G2–G5/PPT/newagent/chat. Hallmark reused precisely,noUI/RTLproof. Prior P12-N1 oldturn PPT/web scope remains,not claiming whole oldturn G1-only. All scientific/128/fourstate/vacuity/74witness/C/billing and historical limits andold document bodies preserved.
'''
shared={}
for name in ['HANDOFF.md','PROJECT_STATUS.md']:
    path=ROOT/'docs'/name;before=path.read_bytes();saved=AUDIT/'before/docs'/name
    saved.parent.mkdir(parents=True,exist_ok=True)
    with saved.open('xb') as f:f.write(before)
    header,body=before.split(b'\n',1);path.write_bytes(header+section.encode()+body)
    assert path.read_bytes().endswith(body)
    shared[name]=dict(before_sha256=sha(saved),after_sha256=sha(path),entire_old_body_retained=True)
assert all(sha(ROOT/p)==s for p,s in base['files'].items())
assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==base['index_sha256']
for key in ['pool_state','attempt_lock','continuation_decision','budget_amendment']:assert not (ROOT/reg[key]).exists()
write(AUDIT/'preservation-checks.json',dict(protected_files=len(base['files']),mismatches=[],
    index_sha256=base['index_sha256'],index_unchanged=True,staged_changed_paths_count=base['staged_changed_paths_count'],
    shared_document_additions=shared,old_E01_pool_sha256=sha(ROOT/reg['first_pool']),
    old_E02_pool_sha256=sha(ROOT/reg['predecessor_pool']),old_pools_immutable=True,
    new_real_pool_or_lock_created=False,actual_authority_files_created=False))
write(AUDIT/'phase.json',dict(phase='G1_R04_CONDITIONAL_STARTUP_REPAIR_PREPARATION',status=STATUS,
    actual_HEAD=git('rev-parse','HEAD').decode().strip(),branch=git('branch','--show-current').decode().strip(),
    scientific_qualification='BLOCKED_NOT_QUALIFIED',
    P13_review_sha256=reg['predecessor_review_sha256'],predecessor_E02_phase_sha256=reg['predecessor_phase_sha256'],
    predecessor_E02_pool_sha256=reg['predecessor_pool_sha256'],predecessor_E01_pool_sha256=reg['first_pool_sha256'],
    original_user_grant_sha256=reg['user_authorization_sha256'],
    registration=rel(REG),registration_sha256=sha(REG),source_manifest=rel(NEW/'source-manifest.json'),
    source_manifest_sha256=sha(NEW/'source-manifest.json'),physical_tb_sha256=sha(NEW/'sources/physical_tb.sv'),
    native_reuse_manifest_sha256=sha(NEW/'native-reuse.json'),
    changed_SV_files=1,unchanged_SV_files=17,unchanged_semantic_reference_materials=23,
    SV_fix_measured=False,native_reuse='CONDITIONAL_REUSED_FROM_E02_NOT_NEW_EXECUTION',
    resource_proposal_sha256=sha(AUDIT/'resource-proposal.json'),
    authority_requirements_sha256=sha(AUDIT/'authority-requirements.json'),
    physical33_authorization='PENDING_NOT_GRANTED',approved_continuation_decision='ABSENT',
    P14='PENDING_PREPARATION_REVIEW;ACTUAL_APPROVAL_HASH_BINDINGS_REQUIRED_BEFORE_EXECUTE',
    original_caps=reg['original_caps'],proposed_caps=reg['caps'],prior_reserved=reg['prior_reserved'],
    proposed_new_jobs=reg['planned_jobs'],prior_actual_checkpoint_seconds=reg['prior_actual_window_seconds'],
    prior_charged_checkpoint_seconds=reg['prior_charged_checkpoint_seconds'],
    proposed_conservative_charge_seconds=8,proposed_current_window_seconds=1192,proposed_work_cutoff_seconds=1187,
    pure_tests=16,pure_failures=0,pure_errors=0,pure_summary_sha256=sha(suite/'summary.json'),
    pure_tested_final_source=True,approved_positive_entry_budget_SV_ABI_exercised=False,
    actual_R04_setup_compile_native_physical_or_probe_jobs=0,actual_API_key_network_install_delete_index_mutations=0,
    real_pool_or_lock_created=False,old_tests_experiments_rerun=False,
    old_protected_files_checked=len(base['files']),old_mismatches=[],index_unchanged=True,
    index_sha256=base['index_sha256'],staged_changed_paths_count=base['staged_changed_paths_count'],
    shared_old_document_bodies_preserved=True,hallmark_usage_sha256=sha(AUDIT/'hallmark-usage.json'),
    elapsed=dict(full_turn_seconds=None,full_turn_knownness='NOT_INSTRUMENTED_NOT_ZERO',
        partial_namespace_span_seconds=time.time()-base['namespace_start_epoch'],
        scope='Preparation including pure tests,not a controlled G1 execution window.'),
    snapshot_manifest=rel(AUDIT/'snapshot-manifest.json'),
    hash_cycle_policy='Manifest hashes phase;phase names successor manifest without hash.',
    next_action='STOP_FOR_EXISTING_P14;NO_REAL_TOOLS_OR_NEW_POOL_BEFORE_ACTUAL_PHYSICAL33_APPROVAL_AND_EXACT_REVIEW_EXECUTE'))
snapshot=AUDIT/'snapshot';snapshot.mkdir()
copies=[*NEW.rglob('*'),REG,*RESULT.rglob('*'),*bound,*[ROOT/p for p in reuse['files']],
    ROOT/'docs/HANDOFF.md',ROOT/'docs/PROJECT_STATUS.md']
for p in copies:
    if not p.is_file() or '__pycache__' in p.parts:continue
    assert not p.is_symlink();target=snapshot/rel(p);target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():assert sha(target)==sha(p)
    else:shutil.copy2(p,target)
files={p.relative_to(AUDIT).as_posix():sha(p) for p in sorted(AUDIT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
write(AUDIT/'snapshot-manifest.json',dict(status=STATUS,files=files,file_count=len(files),symlinks={},
    excluded=['snapshot-manifest.json(self-hash)','__pycache__'],scope='R04 candidate/source/pure refusal evidence and bounded saved-native dependencies;not authorization.'))
print(json.dumps(dict(status=STATUS,phase_sha256=sha(AUDIT/'phase.json'),
    snapshot_manifest_sha256=sha(AUDIT/'snapshot-manifest.json'),registration_sha256=sha(REG),
    source_manifest_sha256=sha(NEW/'source-manifest.json'),physical_tb_sha256=sha(NEW/'sources/physical_tb.sv'),
    native_reuse_sha256=sha(NEW/'native-reuse.json'),files=len(files),protected_files=len(base['files']),
    pure_tests=16,failures=0,real_R04_jobs=0,physical33_approved=False),indent=2))
