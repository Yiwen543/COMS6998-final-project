"""P14 bounded hash review and pure Python probes. Never execute SV/tools."""
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
from unittest.mock import patch

OWN=Path(__file__).resolve().parent
ROOT=OWN.parents[3]
AUDIT=ROOT/'docs/audits/producer_test2_g1_R04_2026-11-06'
SNAP=AUDIT/'snapshot'
EXPECTED={'phase.json':'8189a3e504e59b9baa3d5ef7d2f1d7e0b625be83fb0cbcc0eb4e3608b0ff7fa8','snapshot-manifest.json':'a61cd8744e44eb599abe331079766215a4860d64b07a3080090f8f29e9e97b0a'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,v):
    with Path(p).open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2)
def forbidden(*a,**kw):raise AssertionError('P14_FORBIDS_REAL_TOOL_PROCESS_SIGNAL_SLEEP')

for name,expected in EXPECTED.items():assert sha(AUDIT/name)==expected
phase=read(AUDIT/'phase.json');manifest=read(AUDIT/'snapshot-manifest.json')
assert len(manifest['files'])==512
drift=[]
for rel,expected in manifest['files'].items():
    assert sha(AUDIT/rel)==expected,rel
    if rel.startswith('snapshot/') and sha(ROOT/rel[9:])!=expected:drift.append(rel[9:])
assert not drift
sources=read(SNAP/phase['source_manifest'])['files'];resolved={}
for rel,expected in sources.items():
    src=SNAP/rel
    if not src.exists() and (ROOT/rel).parent==AUDIT:src=AUDIT/Path(rel).name
    assert sha(src)==sha(ROOT/rel)==expected,rel
    resolved[rel]=src
preserve=read(AUDIT/'preservation-before.json')
for rel,expected in preserve['files'].items():assert sha(ROOT/rel)==expected,rel
index=subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)
assert hashlib.sha256(index).hexdigest()==preserve['index_sha256']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
reg=read(SNAP/phase['registration']);assert sha(SNAP/phase['registration'])=='29dcc2a0781927ac1cc624850c9fdda44625fe468544eae881f4ea86e92cfa31'
assert sha(SNAP/phase['source_manifest'])=='57e79f812133ec94f340009c18227b8bf773515ea571d0b172c9c59e9abd9705'
assert sha(SNAP/reg['native_reuse_manifest'])=='1878bd0ea59e00c67d91f2125cd72031c902283931616de52f0ecdb9a6ccc84b'
assert not any((ROOT/reg[k]).exists() for k in ['pool_state','attempt_lock'])
new=SNAP/'test2/g1_v4';old=ROOT/'test2/g1_v3'
assert [p.name for p in sorted((new/'sources').glob('*.sv')) if sha(p)!=sha(old/'sources'/p.name)]==['physical_tb.sv']
assert sha(new/'runtime.py')==sha(old/'runtime.py') and sha(new/'observations.py')==sha(old/'observations.py')
reuse_manifest=read(new/'native-reuse.json')
assert len(reuse_manifest['unchanged_dependencies'])==23
for x in reuse_manifest['unchanged_dependencies']:assert sha(ROOT/x['old'])==sha(SNAP/x['new'])==x['sha256']
body=(new/'sources/physical_tb.sv').read_text()
assert "step=3'd7" in body and '#0.001;' in body and 'if(k==0) #0.999; else #1;' in body
tick=Fraction(1);schedule=[]
for c in range(4):
    step_tick=tick;tick+=999 if c==0 else 1000;pre=tick;tick+=1000;edge=tick;tick+=1000;post=tick;tick+=1000
    schedule.append(dict(cycle=c,step_tick_ps=int(step_tick),pre_ps=int(pre),posedge_ps=int(edge),post_ps=int(post),fall_ps=int(tick)))
assert [r['pre_ps'] for r in schedule]==[1000,5000,9000,13000]
assert [r['posedge_ps'] for r in schedule]==[2000,6000,10000,14000]
assert [r['post_ps'] for r in schedule]==[3000,7000,11000,15000] and tick==16000
work=OWN/'review-copy';work.mkdir(exist_ok=False)
for rel,src in dict(resolved,**{phase['source_manifest']:SNAP/phase['source_manifest'],reg['preparation_snapshot_manifest']:AUDIT/'snapshot-manifest.json'}).items():
    dst=work/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
copy_bindings={rel:sha(work/rel) for rel in resolved}
code=work/'test2/g1_v4';sys.path.insert(0,str(code))
import allocation,budget,runner,native_reuse
from observations import Unqualified
gate_hashes={k+'_sha256':reg[k+'_sha256'] for k in ['continuation_decision','budget_amendment']}
alloc=allocation.load_allocation(work,reg,gate_hashes)
rows=[]
def probe(name,fixture,fn):
    folder=OWN/name;folder.mkdir();write(folder/'fixture.json',fixture)
    result=fn(folder);write(folder/'result.json',result)
    rows.append(dict(name=name,fixture_sha256=sha(folder/'fixture.json'),result_sha256=sha(folder/'result.json'),result=result))
def count_plan(folder):
    b=budget.Budget(folder/'synthetic-ledger.json',reg['caps'],clock=lambda:0.,allocation=alloc)
    assert b.work_deadline==1187 and b.state['reserved']==reg['prior_reserved']
    for j in read(code/'job-plan.json')['jobs']:
        b.reserve(j['kind'],j['id'],j.get('cycles',0));b.terminal(j['id'],{'status':'SYNTHETIC_ONLY'})
    assert b.state['reserved']=={'setup':8,'compile':20,'native':32,'physical':33,'physical_cycles':132}
    try:b.reserve('physical','EXTRA_REFUSE',4)
    except budget.Refuse as e:reason=str(e)
    else:raise AssertionError('PHYSICAL34_ACCEPTED')
    assert reason=='JOB_CAP_physical' and b.state['halted']
    try:b.reserve('native','AFTER_HALT')
    except budget.Refuse:pass
    else:raise AssertionError('AFTER_HALT_ACCEPTED')
    return dict(passed=True,counts=b.state['reserved'],halt_reason=reason,real_dispatches=0)
probe('plan-allocation',{'gate_hashes':gate_hashes,'job_plan_sha256':sha(code/'job-plan.json')},count_plan)
for field,value in [('prior_wall_charge_seconds',0),('attempt_maximum_window_seconds',1200),('prior_reserved',dict(reg['prior_reserved'],physical=0))]:
    changed=copy.deepcopy(reg);changed[field]=value
    def reject(folder,changed=changed):
        try:allocation.load_allocation(work,changed,gate_hashes)
        except allocation.AllocationError as e:return dict(passed=True,outcome='REJECT',reason=str(e))
        raise AssertionError('BAD_ALLOCATION_ACCEPTED')
    probe('reject-'+field,changed,reject)
# A real review_gate on copied metadata; fake review/receipt do not authorize production.
fake_review=dict(phase='P14_REVIEWER_SYNTHETIC_ONLY',status='PASS_WITH_LIMITS',input_identity=dict(producer_manifest_sha256=EXPECTED['snapshot-manifest.json'],registration_sha256=sha(work/phase['registration']),source_manifest_sha256=sha(work/phase['source_manifest']),continuation_decision_sha256=reg['continuation_decision_sha256'],budget_amendment_sha256=reg['budget_amendment_sha256']))
rp=work/'docs/audits/agent_bridge_2026-11-06/P14_FAKE_REVIEW_ONLY.json';write(rp,fake_review)
gate=dict(gate_hashes,record_kind='G1_EXECUTE_R04_AFTER_P14_AND_PHYSICAL33_APPROVAL',stage='EXECUTE',registration_sha256=sha(work/phase['registration']),source_manifest_sha256=sha(work/phase['source_manifest']),preparation_manifest_sha256=EXPECTED['snapshot-manifest.json'],user_authorization_sha256=reg['user_authorization_sha256'],predecessor_pool_sha256=reg['predecessor_pool_sha256'],p14_review_path=str(rp.relative_to(work)),p14_review_sha256=sha(rp))
folder=OWN/'positive-entry';folder.mkdir();write(folder/'fixture.json',gate)
def fake_execute(b,j,folder,env):
    b.reserve(j['kind'],j['id'],j.get('cycles',0));b.terminal(j['id'],{'status':'SYNTHETIC_ONLY'});b.halt('REVIEW_STOP_NO_REAL_EXECUTION')
    return {'status':'SYNTHETIC_ONLY','exit_code':None}
original_digest=runner.digest
pins={str(Path(v['configured']).resolve()):v['resolved_sha256'] for v in reg['tools'].values()}
def digest(path):return pins[str(path)] if str(path) in pins else original_digest(path)
(work/reg['result_root']).mkdir(parents=True,exist_ok=True)
with patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden),patch('os.killpg',side_effect=forbidden),patch('time.sleep',side_effect=forbidden),patch.object(runner,'execute',side_effect=fake_execute),patch.object(runner,'digest',side_effect=digest):
    result=runner.main(folder/'fixture.json')
state=read(work/reg['pool_state']);assert result==1 and state['halt_reason']=='REVIEW_STOP_NO_REAL_EXECUTION'
assert state['reserved']=={'setup':8,'compile':4,'native':2,'physical':1,'physical_cycles':4}
assert state['completed'] and state['halted']
write(folder/'result.json',dict(passed=True,runner_exit=result,synthetic_only=True,host_binary_digest_stubbed=True,ledger=state))
rows.append(dict(name='positive-entry',fixture_sha256=sha(folder/'fixture.json'),result_sha256=sha(folder/'result.json'),passed=True))
prior_hash=sha(work/reg['pool_state'])
try:
    with patch('subprocess.Popen',side_effect=forbidden):runner.main(folder/'fixture.json')
except FileExistsError:pass
else:raise AssertionError('DUPLICATE_ATTEMPT_ACCEPTED')
assert sha(work/reg['pool_state'])==prior_hash
sys.argv=[str(code/'r04_tests.py'),'--record',str(OWN/'fresh-r04-tests')]
try:runpy.run_path(str(code/'r04_tests.py'),run_name='__main__')
except SystemExit as e:assert e.code==0
fresh=read(OWN/'fresh-r04-tests/summary.json');assert (fresh['tests'],fresh['failures'],fresh['errors'])==(17,0,0)
for rel,expected in copy_bindings.items():assert sha(work/rel)==expected
for rel,expected in manifest['files'].items():assert sha(AUDIT/rel)==expected
assert not any((ROOT/reg[k]).exists() for k in ['pool_state','attempt_lock'])
write(OWN/'checks.json',dict(actual_HEAD=head,producer_phase_sha256=EXPECTED['phase.json'],producer_manifest_sha256=EXPECTED['snapshot-manifest.json'],snapshot_bindings=512,source_bindings=len(sources),protected_files=len(preserve['files']),index_sha256=hashlib.sha256(index).hexdigest(),current_snapshot_drift=drift,schedule_arithmetic_only=schedule,SV_fix_actually_executed=False,code_copy_original_bindings_unchanged=True,probe_results=rows,duplicate_attempt_refused=True,fresh_targeted_suite=dict(tests=17,failures=0,errors=0,summary_sha256=sha(OWN/'fresh-r04-tests/summary.json')),real_R04_pool_lock_uncreated=True,real_tools_processes_signals_sleep=0))
print(json.dumps(dict(status='PASS_PURE_PREFLIGHT_CHECKS_NOT_SV_QUALIFICATION',snapshot=512,sources=len(sources),protected=len(preserve['files']),fresh_pure_tests=17,independent_probes=len(rows),duplicate_refused=True,real_G1_jobs=0)))
