"""Exact E01 runtime path only, all tool/ps/signal/sleep interfaces are fake."""
from pathlib import Path
import json,hashlib,types,sys,copy
P=Path(__file__).resolve().parent;S=P/'runtime-copy';sys.path.insert(0,str(S))
import runtime as rt,budget as bm
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
O=P/'permission-probes';O.mkdir(exist_ok=False)
caps=json.loads((P/'probe-input-caps.json').read_text())
cases=[]
for name,denied,exit_before_cleanup in [('baseline-monitor-available',False,False),('permission-denied-running-child',True,False),('permission-denied-child-exit-race',True,True)]:
    d=O/name;d.mkdir();(d/'inputs').mkdir()
    config={'origin':'PURE_PYTHON_PERMISSIONERROR_PATH_NOT_REAL_YOSYS_RESULT','permission_denied':denied,'fake_child_exits_before_cleanup':exit_before_cleanup,'expected_status':'ERROR' if denied else 'RETURNED','real_process_tool_query_sleep_signal_calls':0}
    job={'id':'setup-yosys','kind':'setup','argv':['/opt/homebrew/bin/yosys','-V'],'cycles':0}
    for n,v in [('config.json',config),('caps.json',caps),('job.json',job)]:(d/'inputs'/n).write_text(json.dumps(v,indent=2)+'\n')
    inputs={str(p.relative_to(d/'inputs')):H(p) for p in (d/'inputs').iterdir()};binding={'input_sha256':inputs,'source_sha256':{n:H(S/n) for n in ['runtime.py','budget.py']}}
    (d/'input-bindings-before.json').write_text(json.dumps(binding,indent=2)+'\n')
    clock=[0.0];b=bm.Budget(d/'synthetic-budget.json',copy.deepcopy(caps),clock=lambda:clock[0]);clock[0]=100.0
    launches=[];monitor_attempts=[];signals=[];children=[]
    class Child:
        pid=777777
        def __init__(self,argv,**kwargs):self.returncode=None;launches.append(list(argv));children.append(self)
        def poll(self):return self.returncode
        def wait(self,timeout=None):assert timeout is None or timeout>0;return self.returncode
    def ps(*args,**kwargs):
        monitor_attempts.append({'argv':args[0],'virtual_elapsed':clock[0]})
        if denied:
            if exit_before_cleanup:children[0].returncode=0
            raise PermissionError(1,'Operation not permitted','/bin/ps')
        return types.SimpleNamespace(returncode=0,stdout='777777 1 777777 MOCK_CHILD\n')
    def kill(pid,sig):
        assert pid==777777;signals.append(sig)
        if children[0].returncode is not None:raise ProcessLookupError()
        if sig:children[0].returncode=-9
    def fake_sleep(sec):clock[0]+=sec;children[0].returncode=0
    saved=(rt.subprocess,rt.os,rt.time)
    rt.subprocess=types.SimpleNamespace(Popen=Child,run=ps,TimeoutExpired=TimeoutError)
    rt.os=types.SimpleNamespace(killpg=kill)
    rt.time=types.SimpleNamespace(monotonic=lambda:clock[0],sleep=fake_sleep)
    try:receipt=rt.execute(b,copy.deepcopy(job),d/'job',{})
    finally:rt.subprocess,rt.os,rt.time=saved
    after={str(p.relative_to(d/'inputs')):H(p) for p in (d/'inputs').iterdir()};assert inputs==after
    result={'case':name,'origin':config['origin'],'receipt':receipt,'budget_state':copy.deepcopy(b.state),'mock_Popen_calls':len(launches),'mock_monitor_attempts':monitor_attempts,'mock_group_signal_arguments':signals,'simulated_child_returncode_after_cleanup':children[0].returncode,'input_binding_sha256':H(d/'input-bindings-before.json'),'actual_OS_tool_process_query_sleep_signal_calls':0}
    result['expected_path_met']=len(launches)==1 and len(monitor_attempts)==1 and receipt['status']==config['expected_status'] and b.state['reserved']['setup']==1 and b.state['halted']==denied
    if denied:result['expected_path_met'] &= receipt['exit_code'] is None and receipt['monitor_calls']==0 and receipt['error']=="PermissionError:[Errno 1] Operation not permitted: '/bin/ps'"
    assert result['expected_path_met']
    (d/'result.json').write_text(json.dumps(result,indent=2)+'\n');cases.append(result)
    print(name,receipt['status'],'root receipt exit',receipt['exit_code'],'halt',b.state['halted'],'mock cleanup kill',receipt['cleanup_group_kill'])
(O/'summary.json').write_text(json.dumps({'scope':'Independent fake-only localization,not runtime repair or real retry','cases':cases,'probe_count':len(cases),'actual_tool_query_process_sleep_signal_calls':0},indent=2)+'\n')

