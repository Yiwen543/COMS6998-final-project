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
STATUS='PREPARED_PENDING_P14'

def sha(p):
    assert p.is_file() and not p.is_symlink(),p
    return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def rel(p):return p.relative_to(ROOT).as_posix()
def write(p,value):
    with p.open('x') as f:f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT)

assert not (AUDIT/'phase.json').exists()
historical_base=read(AUDIT/'preservation-before.json');resume=read(AUDIT/'resumption-baseline.json')
base=dict(historical_base,index_sha256=resume['index_sha256'],staged_changed_paths_count=resume['staged_changed_paths_count'],namespace_start_epoch=resume['started_epoch']);reg=read(REG)
assert git('rev-parse','HEAD').decode().strip()==resume['actual_HEAD']
assert sha(AUDIT/'preservation-before.json')==resume['old_preservation_before_sha256']
assert all(sha(ROOT/p)==s for p,s in base['files'].items())
assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==base['index_sha256']
for key in ['pool_state','attempt_lock']:assert not (ROOT/reg[key]).exists(),key
for key in ['continuation_decision','budget_amendment','user_physical33_authorization']:
    assert sha(ROOT/reg[key])==reg[key+'_sha256'],key
assert reg['continuation_decision_sha256']=='80f69ec8d1ee0a0076dac1daa4a009b1b2e4868c5b2cd41327088a0c7fca889e'
assert reg['budget_amendment_sha256']=='449692ff3a154f5b697a8c80f7e6795a269b488bb5efbfd0f0ab0384539ebc67'
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

suite=RESULT/'preparation-attempt2';summary=read(suite/'summary.json')
assert summary['tests']==17 and summary['passed'] and summary['failures']==summary['errors']==0
for name,s in summary['source_sha256'].items():
    current=REG if name=='registration.json' else NEW/name
    assert sha(current)==sha(suite/'executed-source'/name)==s
cases=sorted(suite.glob('test_*'));assert len(cases)==17
inputs_checked=0
for case in cases:
    assert (case/'result.json').is_file()
    for name,s in read(case/'input-bindings.json').items():
        assert sha(case/'inputs'/name)==s;inputs_checked+=1
assert sha(cases[0]/'inputs/physical_tb.sv')==sha(NEW/'sources/physical_tb.sv')
write(AUDIT/'commands-and-checks.json',dict(
    pure_test_command=['PYTHONDONTWRITEBYTECODE=1','.venv/bin/python','test2/g1_v4/r04_tests.py','--record',rel(suite)],
    test_exit_code=0,test_tool_receipt='44b746',summary_sha256=sha(suite/'summary.json'),
    unittest_log_sha256=sha(suite/'unittest.log'),tests=17,failures=0,errors=0,seconds=summary['seconds'],
    exact_final_tested_sources=True,final_mutated_inputs_checked=inputs_checked,
    actual_R04_setup_compile_native_physical_process_signal_sleep=0,
    source_timing_arithmetic_is_not_simulator_validation=True,
    real_approved_allocation_loading_tested=True,approved_entry_and_positive_budget_integration_tested=False,
    predecessor_R01_R03_suites_or_experiments_rerun=False,R04_targeted_suite_rerun_with_final_registration=True,
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
    budget_change='Attempt-id text only;Allocation imports registered caps but actual approval/P14 required before Budget.',
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
    AUDIT/'P14-review-checklist.md',AUDIT/'resource-proposal.json',AUDIT/'authority-requirements.json',
    ROOT/reg['continuation_decision'],ROOT/reg['budget_amendment'],ROOT/reg['user_physical33_authorization'],
    AUDIT/'resumption-baseline.json']
for p in bound:source_inputs[rel(p)]=sha(p)
write(NEW/'source-manifest.json',dict(kind='R04_CONDITIONAL_PREPARATION_NOT_AUTHORIZATION',files=source_inputs,
    status=STATUS,physical33_user_approval='APPROVED_PREEXISTING_EXACT_RECORD_BOUND',
    continuation_decision=reg['continuation_decision_sha256'],independent_review='PENDING_P14',
    SV_startup_fix_measured=False,actual_R04_jobs=0,
    external_approval_note='Actual pre-existing amendment/decision/user hashes are bound now;exact P14+EXECUTE still required. No authority synthesized here.',
    shared_mutable_docs_excluded=True))

report='# R04 resumed startup repair preparation\n\nStatus: **PREPARED_PENDING_P14**. G1 remains NOT_QUALIFIED; no repaired simulator\nrun has occurred. The original E02 QC00 first-row X, rejection and costs remain.\nThe earlier R04 sealer stopped at an assertion expecting approval files absent;\nit created no phase or execution. Actual approval records are now bound, not\nrewritten. Before-resumption copies and the original preparation attempt remain.\n\nOnly physical_tb.sv differs among18SV:initial step7,positive1ps step0 transition,\nfirst999ps wait. Pre ticks1000/5000/9000/13000,edges2000/6000/10000/14000,post\n3000/7000/11000/15000,end16000ps. No extra edge/input,skipped row or X filling.\nSource timing supports the proposed repair but does not prove SV scheduling.\n23 semantic/reference materials,common/all16formal harnesses and runtime/parser\nare unchanged. Saved QC00 frontend+depth8 BMC/cover are conditionally bound as\nREUSED_FROM_E02,not new samples or physical qualification. Rejected physics is\nnever reused. Exact source/SMT/argv/tool/raw evidence dependencies are frozen.\n\nActual pre-existing physical33 user approval,amendment and continuation are bound\nby SHA in registration and source manifest. They authorize only the cumulative\nallocation,not execution without independent P14 and coordinator EXECUTE. New\nplan0setup+17compile+30native+32physical/128cycles gives cumulative8/20/32/33 and132\ncycles. Native reuse failure would require cumulative34 native(+2);stop rather\nthan silently rerun. No physical retry reserve. Prior actual5.197697583s and old\ncharged7.151973250s stay separate;allocation priorcharge8/current1192/work1187\npreserves1200s and is not measured spend. Old pools closed;new pool/lock absent.\n\nResumed final-source suite preparation-attempt2:17/17 PASS,0failures/errors,\n0.07190479105338454s. Old preparation-attempt1 retains16/16 and its own sources.\nChecks include exact dependencies,reuse/refusal,startup arithmetic and a new\npositive loading of actual approval allocation with no claim/ledger;P14 remains\nrequired. All subprocess/run/signal/sleep entry points are blocked by mocks.\nFull approved-entry/ledger integration,SV syntax and dual-simulator eight-row/VCD\nagreement remain untested. No R01-R03 suites or experiments were rerun.\n\nPreservation:all4485 historically protected files unchanged. The old staged10000\nindex record is historical after separately authorized full Git publication;\nresumed preservation instead pins actual HEAD2de33e981d2fffc9739d2ca049fbae1774de1aad\nand current stage0. Original metadata is retained,not silently relabeled. Only\nHANDOFF/STATUS receive additive current notes;their complete old bodies remain.\n\nNext:existing independent P14 checks exact final producer manifest,registration,\nauthority hashes,reuse and budget. Only exact accepted review plus coordinator\nEXECUTE may start one controlled G1 attempt. No model/API,key,paid,install,commit,\npush,cross-IP/raw/B/C or G2–G5 work. Context-only Codex app reads are outside the\ncontrolled preparation;zero research/API/network work is claimed for preparation,\nnot the entire earlier publication or older PPT/web turn. Hallmark material-first,\nreal-facts and bounded-repair organization was used;no UI/RTL proof is implied.\nAll vacuity,four-state,128completion,74witness,C-benefit,billing and earlier\nP04/P05/P06/P05-N1/F1/H1/H2/L1 limits remain.\n'
with (AUDIT/'report.md').open('x') as f:f.write(report)
section='\n\n## Current G1 preparation — R04 sealed, pending P14 (2026-11-06)\n\nR04 **PREPARED_PENDING_P14**;G1 NOT_QUALIFIED. Actual physical33 user approval,\namendment and continuation are now hash-bound;old absence/null drafts are history.\nNo new authority or EXECUTE created. Only physical_tb.sv changes among18SV:step7,\npositive1ps step0 transition,first999ps wait;all pre/edge/post ticks and4edges stay.\nRepair remains unmeasured.23 semantic/reference inputs and runtime/parser unchanged.\nQC00 saved compile1/native2 conditionally REUSED_FROM_E02,not new trial/physics.\n\nFinal-source preparation-attempt2 ran17pure checks:17PASS/0fail/0error,0.071904791s;\nold16-case attempt1 retained. New positive actual-allocation check creates no\nclaim/ledger;P14 still required. New plan0setup/17compile/30native/32physical,\n128cycles;cumulative8/20/32/33,132cycles;prior charge8/current1192/work1187 within1200.\nOld measured5.197697583s/charged7.151973250s retained;no physical retry reserve.\n\nExact phase/report/snapshot-manifest in `docs/audits/producer_test2_g1_R04_2026-11-06/`;\nsource/registration `test2/g1_v4/` and `test2/configs/g1_qualification_registration_v4.json`.\nAll4485 protected historical files unchanged. Actual baseline HEAD2de33e981d2fffc9739d2ca049fbae1774de1aad,\nstage0;old10000-stage preservation record is historical after approved publication,\nnot current staging. All original document bodies/failures/unknowns/freezes retained.\n\nNext:existing independent P14 reads sealed package and exact authority/reuse;\ncoordinator supplies exact EXECUTE only after acceptance. This preparation runs\n0realG1 jobs/modelAPI/key/paid/install/commit/push/cross-IP/raw/B/C;new pool/lock absent.\nSource startup arithmetic is not simulator validation. Hallmark real-facts/minimal\nrepair organization only,no UI/RTLproof. All scientific/128/four-state/vacuity/\n74witness/C-benefit/billing and earlier limitations remain;P2 untouched.\n'
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
for key in ['pool_state','attempt_lock']:assert not (ROOT/reg[key]).exists()
for key in ['continuation_decision','budget_amendment','user_physical33_authorization']:assert sha(ROOT/reg[key])==reg[key+'_sha256']
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
    physical33_authorization=reg['user_physical33_authorization_sha256'],approved_continuation_decision=reg['continuation_decision_sha256'],budget_amendment_sha256=reg['budget_amendment_sha256'],
    P14='PENDING_PREPARATION_REVIEW;ACTUAL_APPROVAL_HASH_BINDINGS_REQUIRED_BEFORE_EXECUTE',
    original_caps=reg['original_caps'],approved_caps=reg['caps'],prior_reserved=reg['prior_reserved'],
    proposed_new_jobs=reg['planned_jobs'],prior_actual_checkpoint_seconds=reg['prior_actual_window_seconds'],
    prior_charged_checkpoint_seconds=reg['prior_charged_checkpoint_seconds'],
    proposed_conservative_charge_seconds=8,proposed_current_window_seconds=1192,proposed_work_cutoff_seconds=1187,
    pure_tests=17,pure_failures=0,pure_errors=0,pure_summary_sha256=sha(suite/'summary.json'),
    pure_tested_final_source=True,real_approved_allocation_loading_tested=True,approved_positive_entry_budget_SV_ABI_exercised=False,
    actual_R04_setup_compile_native_physical_or_probe_jobs=0,controlled_preparation_API_key_network_install_delete_index_mutations=0,context_recovery_codex_app_read_calls=2,
    real_pool_or_lock_created=False,predecessor_R01_R03_tests_experiments_rerun=False,R04_targeted_suite_repeated=True,
    old_protected_files_checked=len(base['files']),old_mismatches=[],index_unchanged=True,
    index_sha256=base['index_sha256'],staged_changed_paths_count=base['staged_changed_paths_count'],
    shared_old_document_bodies_preserved=True,hallmark_usage_sha256=sha(AUDIT/'hallmark-usage.json'),
    elapsed=dict(full_turn_seconds=None,full_turn_knownness='NOT_INSTRUMENTED_NOT_ZERO',
        partial_namespace_span_seconds=time.time()-base['namespace_start_epoch'],
        scope='Preparation including pure tests,not a controlled G1 execution window.'),
    snapshot_manifest=rel(AUDIT/'snapshot-manifest.json'),
    hash_cycle_policy='Manifest hashes phase;phase names successor manifest without hash.',
    next_action='STOP_FOR_EXISTING_P14;NO_REAL_TOOLS_OR_NEW_POOL_BEFORE_EXACT_P14_AND_COORDINATOR_EXECUTE'))
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
    pure_tests=17,failures=0,real_R04_jobs=0,physical33_approved=True),indent=2))
