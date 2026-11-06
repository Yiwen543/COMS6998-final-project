"""Corrected reviewer-only finalization controls; all native dispatch forbidden."""
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

OWN=Path(__file__).resolve().parent
CODE=OWN/'review-copy/test2/g1_v3'
sys.path.insert(0,str(CODE))
import allocation
import budget
import runner
WORK=OWN/'review-copy'
REG=json.loads((WORK/'test2/configs/g1_qualification_registration_v3.json').read_text())
ALLOC=allocation.load_allocation(WORK,REG)
OUT=OWN/'finalization-probes-v2'
OUT.mkdir(exist_ok=False)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,value):
    with Path(p).open('x') as f:json.dump(value,f,indent=2)
def forbidden(*a,**kw):raise AssertionError('NO_REAL_DISPATCH_SIGNAL_SLEEP')
rows=[]
for name,delay in [('normal',0),('cross_cap',1199)]:
    folder=OUT/name;folder.mkdir();repo=folder/'fake-root';repo.mkdir();(repo/'out').mkdir()
    write(repo/'plan.json',{'jobs':[]})
    write(repo/'labels.json',{'cases':[]})
    write(repo/'receipt.json',{'scope':'SYNTHETIC_REVIEW_FINALIZATION_ONLY'})
    reg=dict(REG,result_root='out',pool_state='out/execution-state.json',attempt_lock='out/attempt.lock',job_plan='plan.json',controls='labels.json',tools={})
    gate={'source_manifest_sha256':'1'*64,'registration_sha256':'2'*64}
    write(folder/'fixture.json',dict(registration=reg,gate=gate,delay=delay,expected_exit=int(bool(delay)),upstream_gate_stubbed=True,empty_plan_only_for_finalization=True))
    fixture_sha=sha(folder/'fixture.json')
    clock=[0.0];delayed=[False];original=budget.Budget.save
    def save(obj):
        original(obj)
        if obj.state['completed'] and not delayed[0]:
            delayed[0]=True;clock[0]+=delay
    def make_budget(path,caps,**kw):return budget.Budget(path,caps,clock=lambda:clock[0],**kw)
    with patch.object(runner,'ROOT',repo),patch.object(runner,'review_gate',return_value=(reg,gate,ALLOC)),patch.object(runner,'Budget',side_effect=make_budget),patch.object(budget.Budget,'save',save),patch('time.monotonic',side_effect=lambda:clock[0]),patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden),patch('os.killpg',side_effect=forbidden),patch('time.sleep',side_effect=forbidden):
        exit_code=runner.main(repo/'receipt.json')
    state=json.loads((repo/'out/execution-state.json').read_text())
    result=dict(exit_code=exit_code,ledger=state,fixture_sha256=fixture_sha,execution_error=json.loads((repo/'out/report.json').read_text()).get('execution_error'))
    expected_reason='FINAL_PERSISTENCE_EXCEEDED_CUMULATIVE_WALL_CAP' if delay else None
    passed=(exit_code==int(bool(delay)) and state['halted']==bool(delay) and state['completed'] and state['halt_reason']==expected_reason and result['execution_error'] is None)
    if delay:
        passed=passed and state['cumulative_charged_window_seconds']==1201 and state['total_elapsed_seconds']==1199
    result['passed']=passed;write(folder/'result.json',result)
    rows.append(dict(name=name,fixture_sha256=fixture_sha,result_sha256=sha(folder/'result.json'),passed=passed,exit_code=exit_code,halt_reason=state['halt_reason']))
write(OUT/'summary.json',dict(probes=2,passed=sum(r['passed'] for r in rows),rows=rows,real_tools_processes_signals_sleep=0))
print(json.dumps(rows))
assert all(r['passed'] for r in rows)
