"""Independent bounded R05B metadata/caller probes. Never dispatch a real job."""
from pathlib import Path
import copy,hashlib,json,shutil,subprocess,sys
from unittest.mock import patch
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
AUDIT=ROOT/'docs/audits/producer_test2_g1_R05B_2026-11-06';SNAP=AUDIT/'snapshot'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
def write(p,x):
    with Path(p).open('x') as f:json.dump(x,f,indent=2)
def inventory():
    m=read(AUDIT/'snapshot-manifest.json');s=read(SNAP/'test2/g1_v5b/source-manifest.json')
    for n,h in m['files'].items():assert sha(AUDIT/n)==h,n
    for n,h in s['files'].items():assert sha(ROOT/n)==h,n
    return {'snapshot':len(m['files']),'dependencies':len(s['files'])}
assert sha(AUDIT/'snapshot-manifest.json')=='f02225f65b42899083ea9b88a1931218b6512aaf71ee36657b176aca149dbf0d'
assert sha(AUDIT/'phase.json')=='132e2a8e081e65cf5983c8dcab7754294922c6bb07d0f6146d896902d42da21d'
before=inventory();index_before=hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)).hexdigest()
OUT=OWN/'integration-evidence';OUT.mkdir();CODE=OUT/'executed-source'
for directory in ['g1_v5b','g1_v5']:
    src=SNAP/'test2'/directory;dest=CODE/'test2'/directory;dest.mkdir(parents=True)
    for p in src.glob('*.py'):shutil.copyfile(p,dest/p.name)
code_hashes={str(p.relative_to(CODE)):sha(p) for p in CODE.rglob('*.py')};write(OUT/'executed-source-sha256.json',code_hashes)
sys.path[:0]=[str(CODE/'test2/g1_v5b'),str(CODE/'test2/g1_v5')]
import runner,reuse,native_results,contracts
from observations import Unqualified
from allocation import load_allocation,AllocationError
from budget import Budget
REG=read(SNAP/'test2/configs/g1_qualification_registration_v5b.json');runner.ROOT=ROOT
def forbidden(*a,**k):raise AssertionError('FORBIDDEN_REAL_PROCESS_SIGNAL_SLEEP')
probes=[]
def passed(name,details):probes.append(dict(name=name,passed=True,details=details))
def refusal(fn,reason):
    try:fn()
    except Exception as e:
        assert reason in str(e),(reason,str(e));return type(e).__name__+':'+str(e)
    raise AssertionError('Expected refusal '+reason)
with patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden),patch('os.killpg',side_effect=forbidden),patch('time.sleep',side_effect=forbidden):
    alloc=load_allocation(ROOT,REG,{'continuation_decision_sha256':REG['continuation_decision_sha256']})
    verified=reuse.metadata(ROOT,REG);decoded=reuse.decode(ROOT,REG,verified)
    write(OUT/'saved-reuse-decoded.json',dict(jobs=decoded['jobs'],controls=decoded['controls'],native_alarms=decoded['native_alarms'],physical={str(k):v for k,v in decoded['physical'].items()}))
    assert len(decoded['jobs'])==10 and all(j['new_execution'] is False for j in decoded['jobs'].values())
    cover=decoded['jobs']['QC01-cover']['native_evidence'];assert (cover['tool_status'],cover['process_exit_code'],cover['activation'],cover['assertion_observation'])==('FAILED',1,'REACHED','FAILED')
    assert decoded['jobs']['QC01-cover']['original_job']['native_status']=='NOT_REACHED'
    assert 'QC00-icarus' not in decoded['prefix'] if 'prefix' in decoded else True
    assert all(j.get('status')!='REUSED_FROM_E02' for k,j in decoded['jobs'].items() if 'icarus' in k or 'verilator' in k)
    passed('actual_ten_job_reuse_and_QC01_layered_outcomes',{'jobs':list(decoded['jobs']),'raw_cover':cover})
    plan=read(ROOT/REG['job_plan']);contracts.registration_contract(ROOT,REG,read(ROOT/REG['user_authorization']),plan)
    oldplan=read(SNAP/'test2/g1_v4/job-plan.json')['jobs'];report=read(ROOT/'test2/results/g1-qualification-v4/report.json');expected=[]
    for j in oldplan:
        if report['jobs'][j['id']]['status']!='NOT_RUN':continue
        j=copy.deepcopy(j);j['argv']=[x.replace('/g1_v4/','/g1_v5/') for x in j['argv']]
        if j['kind']=='physical':j['argv']=[x.replace('{OUT}/build/','{ROOT}/test2/results/g1-qualification-v4/build/') for x in j['argv']]
        expected.append(j)
    assert plan['jobs']==expected
    passed('exact_remaining72_plan_and_original_order_flags',{'compile':14,'native':28,'physical':30,'cycles':120})
    intents=read(ROOT/REG['interpretation'])['cases'];rejections=[]
    for intent in intents:
        for mode in ['bmc','cover']:
            rejections.append(refusal(lambda:native_results.judge_native({'evidence_complete':False,'issues':['INDEPENDENT_UNKNOWN']},mode,intent),'NATIVE_EVIDENCE_UNKNOWN'))
    write(OUT/'unknown-intents-input.json',{'intents':intents,'evidence':{'evidence_complete':False,'issues':['INDEPENDENT_UNKNOWN']}})
    passed('UNKNOWN_cannot_pass_any_of32_registered_targets',rejections)
    identities=dict(registration_sha256=sha(ROOT/'test2/configs/g1_qualification_registration_v5b.json'),source_manifest_sha256=sha(ROOT/REG['source_manifest']),preparation_manifest_sha256=sha(AUDIT/'snapshot-manifest.json'),continuation_decision_sha256=REG['continuation_decision_sha256'],predecessor_pool_sha256=REG['predecessor_pool_sha256'],reuse_manifest_sha256=sha(ROOT/REG['reuse_manifest']),user_authorization_sha256=REG['user_authorization_sha256'],budget_amendment_sha256=REG['budget_amendment_sha256'])
    g=dict(record_kind='G1_EXECUTE_R05B_AFTER_P16',stage='EXECUTE',**identities)
    r=dict(phase='P16_SYNTHETIC_UNIT_INPUT_NOT_A_REVIEW',status='PASS_WITH_LIMITS',input_identity={('producer_manifest_sha256' if k=='preparation_manifest_sha256' else k):v for k,v in identities.items()})
    # Deliberately never save this acceptance-shaped unit input as a review/receipt.
    contracts.gate_contract(g,r,identities)
    negative=[]
    for key in ['producer_manifest_sha256','registration_sha256','source_manifest_sha256','continuation_decision_sha256','reuse_manifest_sha256','budget_amendment_sha256']:
        bad=copy.deepcopy(r);bad['input_identity'][key]='0'*64
        negative.append(refusal(lambda:contracts.gate_contract(g,bad,identities),'P16_BINDING_DRIFT'))
    negative.append(refusal(lambda:contracts.gate_contract(g,{},identities),'P16_ACCEPTANCE_REQUIRED'))
    passed('pure_exact_identity_gate_positive_and7_refusals',negative)
    synthetic=OUT/'synthetic-budget';synthetic.mkdir();b=Budget(synthetic/'ledger.json',REG['caps'],clock=lambda:100.0,allocation=alloc,started_at=100.0)
    assert b.state['reserved']==REG['prior_reserved'] and b.attempt_window==1185 and b.work_deadline==1280
    passed('actual_allocation_in_synthetic_ledger',{'prior':b.state['reserved'],'prior_charge':15,'window':1185,'work':1180})
    # Minimal positive caller exercise: actual saved reuse + synthetic QC01 pair,
    # then intentional compile failure. Not scientific or full72 evidence.
    run=OUT/'synthetic-caller';run.mkdir();reg=copy.deepcopy(REG)
    reg.update(result_root=str(run.relative_to(ROOT)),pool_state=str((run/'execution-state.json').relative_to(ROOT)),attempt_lock=str((run/'attempt.lock').relative_to(ROOT)))
    receipt=OUT/'NOT_EXECUTE_synthetic_input.json';write(receipt,{'fixture_origin':'SYNTHETIC_CALLER_ONLY_NOT_AUTHORIZATION'})
    calls=[];labels=read(ROOT/REG['controls'])['cases']
    def fake_execute(budget,job,folder,env):
        budget.reserve(job['kind'],job['id'],job.get('cycles',0));folder.mkdir();(folder/'stdout.log').write_text('SYNTHETIC_NO_SIMULATION\n');(folder/'trace.vcd').write_text('SYNTHETIC_NOT_A_VCD\n')
        out=dict(status='RETURNED',exit_code=1 if job['kind']=='compile' else 0)
        budget.terminal(job['id'],out);calls.append(job['id']);return out
    def synthetic_rows(text,case,sim):return copy.deepcopy(case['physical_rows_expected_icarus'])
    with patch.object(runner,'review_gate',return_value=(reg,identities,alloc,verified)),patch.object(runner,'execute',side_effect=fake_execute),patch.object(runner,'parse_rows',side_effect=synthetic_rows),patch.object(runner,'parse_vcd',return_value={'SYNTHETIC':True}),patch.object(runner,'bind_physical_vcd',return_value=None):
        code=runner.main(receipt)
    result=read(run/'report.json');ledger=read(run/'execution-state.json')
    assert code==1 and calls==['QC01-icarus','QC01-verilator','compile-QC02']
    assert 'QC01' in result['controls'] and result['controls']['QC01']['native_origin']=='REUSED_E03'
    assert ledger['reserved']==dict(setup=8,compile=7,native=4,physical=5,physical_cycles=20)
    assert ledger['halted'] and ledger['completed'] and 'SETUP_OR_COMPILATION_FAILED' in ledger['halt_reason']
    assert sum(x['status']=='NOT_RUN' for x in result['jobs'].values())==69
    passed('minimal_positive_caller_reuse_phase_binding_then_persistent_halt',{'execute_calls':calls,'exit':code,'remaining_not_run':69,'synthetic_only':True,'parsers_stubbed_no_SV_evidence':True})
    passed('exclusive_claim_refuses_duplicate',refusal(lambda:runner.claim_attempt(run/'attempt.lock',{}),'File exists'))
for name,h in code_hashes.items():assert sha(CODE/name)==h
after=inventory();index_after=hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)).hexdigest();assert index_after==index_before
assert not (ROOT/REG['pool_state']).exists() and not (ROOT/REG['attempt_lock']).exists()
write(OUT/'summary.json',dict(status='INDEPENDENT_INTEGRATION_PROBES_PASS',probe_groups=probes,before=before,after=after,index_sha256=index_after,source_unchanged=True,real_pool_lock_absent=True,real_G1_jobs=0,producer_tests_not_rerun=True,scope='SAVED_EVIDENCE_AND_SYNTHETIC_CALLER_NOT_QUALIFICATION'))
print(json.dumps(dict(status='PASS',probe_groups=len(probes),snapshot=after['snapshot'],dependencies=after['dependencies'],real_G1_jobs=0)))
