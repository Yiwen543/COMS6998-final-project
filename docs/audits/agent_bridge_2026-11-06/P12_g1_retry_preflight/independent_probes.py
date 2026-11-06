"""Reviewer probes: exact copied R03 modules, fake children/clock only."""
import copy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

OWN=Path(__file__).resolve().parent
WORK=OWN/'review-copy'
CODE=WORK/'test2/g1_v3'
sys.path.insert(0,str(CODE))
import allocation
import budget
import runtime
import runner
import observations

REG=json.loads((WORK/'test2/configs/g1_qualification_registration_v3.json').read_text())
ALLOC=allocation.load_allocation(WORK,REG)
OUT=OWN/'independent-probes'
OUT.mkdir(exist_ok=False)
ROWS=[]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,value):
    with Path(p).open('x') as f:json.dump(value,f,indent=2)
def forbidden(*args,**kwargs):raise AssertionError('REAL_PROCESS_SIGNAL_SLEEP_FORBIDDEN')
def begin(name,fixture):
    folder=OUT/name;folder.mkdir()
    write(folder/'fixture.json',copy.deepcopy(fixture))
    return folder,sha(folder/'fixture.json')
def finish(name,folder,fixture_sha,result,ok):
    write(folder/'result.json',result)
    ROWS.append(dict(name=name,fixture_sha256=fixture_sha,result_sha256=sha(folder/'result.json'),passed=bool(ok)))

class Clock:
    def __init__(self):self.value=0.0
    def now(self):return self.value
    def advance(self,delta):self.value+=delta

class Child:
    pid=876543210
    def __init__(self,cfg):
        self.cfg=cfg;self.code=0 if cfg.get('exited') else None;self.polls=0;self.waits=0
    def poll(self):
        self.polls+=1
        if self.cfg.get('fail')=='poll':raise PermissionError('REVIEW_POLL_DENIED')
        if not self.cfg.get('pending') and self.polls>=2:self.code=0
        return self.code
    def wait(self,timeout):
        self.waits+=1
        if self.cfg.get('fail')=='wait' or (self.cfg.get('fail')=='cleanup_wait' and self.waits>1):
            raise PermissionError('REVIEW_WAIT_DENIED')
        if self.code is None:raise subprocess.TimeoutExpired('SYNTHETIC',timeout)
        return self.code

def process_case(name,cfg,expected):
    fixture=dict(config=cfg,expected=expected,job=dict(id='review-job',kind='compile',argv=['SYNTHETIC_NEVER_EXECUTABLE']),allocation=asdict(ALLOC),caps=allocation.CUMULATIVE_CAPS)
    folder,fs=begin(name,fixture);clock=Clock()
    b=budget.Budget(folder/'ledger.json',allocation.CUMULATIVE_CAPS,clock=clock.now,allocation=ALLOC)
    clock.value=cfg.get('elapsed',100.0)
    child=Child(cfg);saves=[False];jobfolder=folder/'job'
    original_save=b.save;original_mkdir=Path.mkdir;original_open=Path.open;original_pre=b.pre_dispatch_window
    def delay(stage):
        if cfg.get('delay_stage')==stage and not saves[0]:
            saves[0]=True;clock.advance(cfg.get('delay',7))
    def save():original_save();delay('save')
    def mkdir(path,*a,**kw):
        answer=original_mkdir(path,*a,**kw)
        if path==jobfolder:delay('mkdir')
        return answer
    def open_file(path,*a,**kw):
        answer=original_open(path,*a,**kw)
        if path==jobfolder/'stdout.log':delay('log')
        return answer
    def pre(job_id):delay('closest_precheck');return original_pre(job_id)
    def killpg(pid,signum):
        assert pid==child.pid
        if not signum:
            if cfg.get('fail')=='group':raise PermissionError('REVIEW_GROUP_DENIED')
            if child.code is not None:raise ProcessLookupError()
        else:
            if cfg.get('fail')=='kill':raise PermissionError('REVIEW_KILL_DENIED')
            child.code=-9
    def inventory(pid):
        assert pid==child.pid
        mode=cfg.get('inventory')
        if mode=='permission':raise PermissionError('REVIEW_OPTIONAL_DENIED')
        if mode=='oserror':raise OSError('REVIEW_OPTIONAL_IO')
        if mode=='timeout':clock.advance(.1);raise subprocess.TimeoutExpired('SYNTHETIC_OPTIONAL',.1)
        return []
    b.save=save;b.pre_dispatch_window=pre
    with patch.object(runtime.time,'monotonic',clock.now),patch.object(runtime.time,'sleep',clock.advance),patch.object(runtime.subprocess,'Popen',return_value=child) as dispatch,patch.object(runtime.subprocess,'run',side_effect=forbidden),patch.object(runtime.os,'killpg',side_effect=killpg),patch.object(Path,'mkdir',mkdir),patch.object(Path,'open',open_file):
        receipt=runtime.execute(b,fixture['job'],jobfolder,{},inventory_probe=inventory if cfg.get('inventory') else None)
        calls=dispatch.call_count
        second=None
        if b.state['halted']:
            second=runtime.execute(b,dict(id='after-halt',kind='compile',argv=['SYNTHETIC_NEVER_EXECUTABLE']),folder/'after-halt',{})
            assert dispatch.call_count==calls,'DISPATCH_AFTER_HALT'
    persisted=json.loads((folder/'ledger.json').read_text())
    ok=(receipt['status']==expected['status'] and calls==expected['dispatch'] and b.state['halted']==expected['halt'])
    if cfg.get('inventory'):
        ok=ok and not receipt['inventory']['complete'] and 'Error' in receipt['inventory']['current_error'] or (ok and cfg.get('inventory')=='timeout' and 'TimeoutExpired' in receipt['inventory']['current_error'])
    if calls:
        ok=ok and b.state['reserved']['compile']==1 and b.state['reserved']['setup']==1
    if cfg.get('delay_stage'):
        ok=ok and persisted['halted'] and persisted['reserved']['compile']==1 and receipt['status']=='NOT_RUN'
    finish(name,folder,fs,dict(receipt=receipt,persisted_ledger=persisted,second_after_halt=second,mocked_dispatches=calls,clock=clock.value,expected=expected),ok)

cases=[
('registered_path_no_scanner',{},'RETURNED',1,False),
('optional_permission_running',{'inventory':'permission'},'RETURNED',1,False),
('optional_permission_exited',{'inventory':'permission','exited':True},'RETURNED',1,False),
('optional_oserror',{'inventory':'oserror'},'RETURNED',1,False),
('optional_timeout',{'inventory':'timeout'},'RETURNED',1,False),
('required_poll_denied',{'fail':'poll','pending':True},'PROTECTION_UNRESOLVED',1,True),
('required_wait_denied',{'fail':'wait'},'PROTECTION_UNRESOLVED',1,True),
('required_group_denied',{'fail':'group'},'PROTECTION_UNRESOLVED',1,True),
('required_kill_denied',{'fail':'kill','pending':True},'PROTECTION_UNRESOLVED',1,True),
('cleanup_wait_denied',{'fail':'cleanup_wait'},'PROTECTION_UNRESOLVED',1,True),
('pending_timeout',{'pending':True},'TIMEOUT',1,True),
('expired_before_reserve',{'elapsed':1193},'NOT_RUN',0,True),
('insufficient_cleanup_window',{'elapsed':1192.9},'NOT_RUN',0,True),
]
for stage in ['save','mkdir','log','closest_precheck']:
    cases.append(('late_'+stage,dict(elapsed=1192,delay_stage=stage,delay=7),'NOT_RUN',0,True))
for name,cfg,status,dispatch,halt in cases:
    process_case(name,cfg,dict(status=status,dispatch=dispatch,halt=halt))

def end_to_end_final_save(name,delay):
    folder,fs=begin(name,dict(final_save_delay=delay,expected_exit=int(delay>1198),scope='EMPTY_SYNTHETIC_PLAN_NOT_EXECUTION_AUTHORITY'))
    repo=folder/'fake-root';repo.mkdir();(repo/'out').mkdir()
    write(repo/'plan.json',{'jobs':[]});write(repo/'receipt.json',{'scope':'REVIEW_FAKE_ONLY'})
    reg=dict(REG,result_root='out',pool_state='out/execution-state.json',attempt_lock='out/attempt.lock',job_plan='plan.json',tools={})
    gate={'source_manifest_sha256':'1'*64,'registration_sha256':'2'*64}
    clock=Clock();original=budget.Budget.save;delayed=[False]
    def save(obj):
        original(obj)
        if obj.state['completed'] and not delayed[0]:
            delayed[0]=True;clock.advance(delay)
    # Budget default clock is captured at import, so provide this fake explicitly.
    def make_budget(path,caps,**kw):return budget.Budget(path,caps,clock=clock.now,**kw)
    with patch.object(runner,'ROOT',repo),patch.object(runner,'review_gate',return_value=(reg,gate,ALLOC)),patch.object(runner,'Budget',side_effect=make_budget),patch.object(runtime.time,'monotonic',clock.now),patch.object(budget.Budget,'save',save),patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden),patch('os.killpg',side_effect=forbidden),patch('time.sleep',side_effect=forbidden):
        code=runner.main(repo/'receipt.json')
    state=json.loads((repo/'out/execution-state.json').read_text())
    finish(name,folder,fs,dict(runner_exit=code,ledger=state),code==int(delay>1198) and state['halted']==(delay>1198) and state['completed'])

end_to_end_final_save('runner_normal_final_save',0)
end_to_end_final_save('runner_final_save_crosses_cap',1199)

# Full real gate function, on copied metadata and reviewer-owned fake receipts only.
base_gate=dict(record_kind='G1_EXECUTE_CONTINUATION_AFTER_P12',stage='EXECUTE',registration_sha256=sha(WORK/'test2/configs/g1_qualification_registration_v3.json'),source_manifest_sha256=sha(WORK/REG['source_manifest']),user_authorization_sha256=REG['user_authorization_sha256'],preparation_manifest_sha256=sha(WORK/REG['preparation_snapshot_manifest']),continuation_decision_sha256=REG['continuation_decision_sha256'],predecessor_pool_sha256=REG['predecessor_pool_sha256'])
for mode in ['valid','old_receipt','old_review','wrong_preparation','wrong_registration','wrong_continuation','wrong_source','wrong_pool']:
    name='full_gate_'+mode;folder=OUT/name;folder.mkdir()
    review=dict(phase='P12_REVIEWER_SYNTHETIC_GATE_ONLY',status='PASS_WITH_LIMITS',input_identity=dict(producer_manifest_sha256=base_gate['preparation_manifest_sha256'],registration_sha256=base_gate['registration_sha256'],source_manifest_sha256=base_gate['source_manifest_sha256'],continuation_decision_sha256=base_gate['continuation_decision_sha256']))
    gate=copy.deepcopy(base_gate)
    if mode=='old_receipt':gate['record_kind']='G1_EXECUTE_AFTER_READONLY_P10'
    if mode=='old_review':review['phase']='P10B_OLD'
    if mode=='wrong_preparation':review['input_identity']['producer_manifest_sha256']='0'*64
    if mode=='wrong_registration':review['input_identity']['registration_sha256']='0'*64
    if mode=='wrong_continuation':review['input_identity']['continuation_decision_sha256']='0'*64
    if mode=='wrong_source':gate['source_manifest_sha256']='0'*64
    if mode=='wrong_pool':gate['predecessor_pool_sha256']='0'*64
    rp=WORK/'docs/audits/agent_bridge_2026-11-06'/('P12_fake_review_'+mode+'.json')
    write(rp,review);gate.update(p12_review_path=str(rp.relative_to(WORK)),p12_review_sha256=sha(rp))
    write(folder/'review-fixture.json',review);write(folder/'fixture.json',gate);fs=sha(folder/'fixture.json')
    try:
        with patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden):
            runner.review_gate(folder/'fixture.json')
        actual='ACCEPT';error=None
    except (observations.Unqualified,allocation.AllocationError) as e:
        actual='REJECT';error=str(e)
    finish(name,folder,fs,dict(actual=actual,error=error,review_fixture_sha256=sha(folder/'review-fixture.json')),actual==('ACCEPT' if mode=='valid' else 'REJECT'))

for mode in ['zero_prior','expanded_window','wrong_pool_hash','wrong_depth']:
    mutated=copy.deepcopy(REG)
    if mode=='zero_prior':mutated['prior_reserved']['setup']=0
    if mode=='expanded_window':mutated['attempt_maximum_window_seconds']=1200
    if mode=='wrong_pool_hash':mutated['predecessor_pool_sha256']='0'*64
    if mode=='wrong_depth':mutated['native_depth']=9
    name='lineage_'+mode;folder,fs=begin(name,mutated)
    try:
        allocation.load_allocation(WORK,json.loads((folder/'fixture.json').read_text()))
        actual='ACCEPT';error=None
    except allocation.AllocationError as e:actual='REJECT';error=str(e)
    finish(name,folder,fs,dict(actual=actual,error=error),actual=='REJECT')

summary=dict(probes=len(ROWS),passed=sum(r['passed'] for r in ROWS),rows=ROWS,real_tools_processes_signals_sleep=0,scope='PURE_SYNTHETIC_NOT_G1_QUALIFICATION',exact_source_sha256={p.name:sha(p) for p in CODE.glob('*.py')})
write(OUT/'summary.json',summary)
print(json.dumps({k:v for k,v in summary.items() if k not in ['rows','exact_source_sha256']}))
assert all(r['passed'] for r in ROWS),[r['name'] for r in ROWS if not r['passed']]
