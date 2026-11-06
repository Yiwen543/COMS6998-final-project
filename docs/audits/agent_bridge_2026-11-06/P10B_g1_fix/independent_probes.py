"""Independent R02 regression probes. All OS process/sleep/signal entries fake."""
from pathlib import Path
import sys,json,hashlib,copy,types,shutil
P=Path(__file__).resolve().parent
S=P/'exec_tree/test2/g1_v2';sys.path.insert(0,str(S))
import budget as bm,runtime as rt,observations as ob
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
O=P/'independent-probes';O.mkdir(exist_ok=False)
CAPS=json.loads((P/'exec_tree/test2/configs/g1_qualification_registration_v2.json').read_text())['caps']
SOURCE={n:H(S/n) for n in ['budget.py','runtime.py','observations.py']}
rows=[]
def put(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def bind(d):
    b={str(p.relative_to(d/'inputs')):H(p) for p in (d/'inputs').rglob('*') if p.is_file()}
    put(d/'input-bindings-before.json',{'input_sha256':b,'source_sha256':SOURCE});return b
def timer(name,initial=1194,stage=None,delay=0,pending=False,cleanup_unknown=False,expected_calls=0,expected_status='NOT_RUN'):
    d=O/name;d.mkdir();(d/'inputs').mkdir()
    config={'initial':initial,'delay_stage':stage,'delay':delay,'pending':pending,'cleanup_unknown':cleanup_unknown,'expected_mock_Popen_calls':expected_calls,'expected_status':expected_status,'clock_origin':0,'kind':'compile'}
    put(d/'inputs/config.json',config);put(d/'inputs/caps.json',CAPS);inputs=bind(d)
    clock=[0.0];b=bm.Budget(d/'synthetic-budget.json',copy.deepcopy(CAPS),clock=lambda:clock[0]);clock[0]=initial;calls=[];signals=[];delayed=[False];checks=[0]
    original_save=b.save;original_window=b.pre_dispatch_window
    def advance(where):
        if stage==where and not delayed[0]:clock[0]+=delay;delayed[0]=True
    def save():original_save();advance('save')
    def window(j):
        checks[0]+=1
        if checks[0]==2:advance('last_check')
        return original_window(j)
    b.save=save;b.pre_dispatch_window=window
    class FS:
        def __init__(self,p):self.p=p
        def __truediv__(self,n):return FS(self.p/n)
        def mkdir(self,**kw):self.p.mkdir(**kw);advance('mkdir')
        def open(self,mode):
            f=self.p.open(mode)
            if self.p.name=='stdout.log':advance('stdout_open')
            if self.p.name=='stderr.log':advance('stderr_open')
            return f
        def exists(self):return self.p.exists()
        def read_bytes(self):return self.p.read_bytes()
    class FakeTimeout(Exception):pass
    class Child:
        pid=777777
        def __init__(self,argv,**kw):
            self.returncode=None if pending or cleanup_unknown else 0
            calls.append({'virtual_elapsed':clock[0],'argv':argv,'remaining_at_launch':min(initial+20,1195)-clock[0]})
        def poll(self):return self.returncode
        def wait(self,timeout=None):
            assert timeout is None or timeout>0
            if cleanup_unknown:raise FakeTimeout()
            return self.returncode
    child=[None]
    def popen(*a,**kw):child[0]=Child(*a,**kw);return child[0]
    def killpg(pid,sig):
        assert child[0] is not None and pid==child[0].pid
        signals.append(sig)
        if child[0].returncode is not None and not cleanup_unknown:raise ProcessLookupError()
        if sig:child[0].returncode=-9
    def monitor(*a,**kw):clock[0]+=0.02;return types.SimpleNamespace(stdout='',returncode=0)
    saved=(rt.subprocess,rt.os,rt.time)
    rt.subprocess=types.SimpleNamespace(Popen=popen,run=monitor,TimeoutExpired=FakeTimeout)
    rt.os=types.SimpleNamespace(killpg=killpg)
    rt.time=types.SimpleNamespace(monotonic=lambda:clock[0],sleep=lambda sec:clock.__setitem__(0,clock[0]+sec))
    result=None;error=None
    try:result=rt.execute(b,{'kind':'compile','id':name,'argv':['MOCK_ONLY_NO_EXECUTABLE']},FS(d/'job'),{})
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:rt.subprocess,rt.os,rt.time=saved
    reattempt_refused=restart_refused=None
    if b.state['halted']:
        try:b.reserve('native','after-halt')
        except bm.Refuse:reattempt_refused=True
        try:bm.Budget(d/'synthetic-budget.json',CAPS,clock=lambda:clock[0])
        except FileExistsError:restart_refused=True
    after={str(p.relative_to(d/'inputs')):H(p) for p in (d/'inputs').rglob('*') if p.is_file()};assert after==inputs
    x={'case':name,'config':config,'mock_Popen_calls':len(calls),'calls':calls,'receipt':result,'error':error,'budget_state':copy.deepcopy(b.state),'final_virtual_clock':clock[0],'global_origin_unchanged':b.start==0,'reattempt_refused':reattempt_refused,'same_path_restart_refused':restart_refused,'source_sha256':SOURCE,'input_binding_sha256':H(d/'input-bindings-before.json'),'real_tool_process_sleep_signal_calls':0}
    x['expectation_met']=error is None and len(calls)==expected_calls and result['status']==expected_status and b.start==0
    if expected_calls==0 and initial<1195:x['expectation_met'] &= b.state['reserved']['compile']==1 and b.event(name)['dispatch_state']=='CHARGED_NOT_DISPATCHED' and b.state['halted']
    if expected_calls:x['expectation_met'] &= all(c['remaining_at_launch']>0.25 for c in calls) and result['absolute_job_deadline']==min(initial+20,1195)
    if pending:x['expectation_met'] &= clock[0]<=initial+20
    if expected_status!='RETURNED':x['expectation_met'] &= reattempt_refused is True and restart_refused is True
    put(d/'result.json',x);rows.append(x);print(name,result['status'] if result else error,'Popen',len(calls),'expected',x['expectation_met'])
timer('original-save-crossing',stage='save',delay=7)
timer('mkdir-crossing',stage='mkdir',delay=7)
timer('stdout-open-crossing',stage='stdout_open',delay=7)
timer('stderr-open-crossing',stage='stderr_open',delay=7)
timer('closest-pre-Popen-check-crossing',stage='last_check',delay=7)
timer('already-expired',initial=1196)
timer('insufficient-cleanup-window',initial=1194.9)
timer('normal-baseline',initial=100,expected_calls=1,expected_status='RETURNED')
timer('ordinary-timeout-original-deadline',initial=100,stage='save',delay=4,pending=True,expected_calls=1,expected_status='TIMEOUT')
timer('cleanup-unresolved-is-halt',initial=100,cleanup_unknown=True,expected_calls=1,expected_status='CLEANUP_UNRESOLVED')
# Reuse original P10 serialized bytes (not producer-generated replacements).
P10=P.parent/'P10_g1_registration/analytic-preflight'
def vcd_case(name,fixture,mutation=None,row_mutation=None,expected='REJECT',reason=None,query=None):
    d=O/name;d.mkdir();(d/'inputs').mkdir()
    path=d/'inputs/trace.vcd';shutil.copy2(P10/fixture,path)
    if mutation:path.write_text(mutation(path.read_text()))
    allrows=json.loads((P10/'rows.json').read_text());obs=copy.deepcopy(allrows['QC00'])
    if row_mutation:row_mutation(obs)
    put(d/'inputs/rows.json',obs);put(d/'inputs/case.json',{'id':'QC00'})
    put(d/'inputs/expectation.json',{'status':expected,'reason':reason,'state_query':query,'original_fixture_sha256':H(P10/fixture)})
    inputs=bind(d);actual='ACCEPT';error=None
    try:
        v=ob.parse_vcd(path)
        if query is None:ob.bind_physical_vcd(v,copy.deepcopy(obs),{'id':'QC00'})
        else:ob.state_at(v,query)
    except Exception as e:actual='REJECT';error=type(e).__name__+':'+str(e)
    assert inputs=={str(p.relative_to(d/'inputs')):H(p) for p in (d/'inputs').rglob('*') if p.is_file()}
    x={'case':name,'actual':actual,'expected':expected,'error':error,'input_binding_sha256':H(d/'input-bindings-before.json'),'fixture_sha256':H(path),'source_sha256':SOURCE,'expectation_met':actual==expected and (reason is None or reason in (error or '')),'actual_tools':0}
    put(d/'result.json',x);rows.append(x);print(name,actual,error)
vcd_case('exact-P10-complete','full-observer-vcd.vcd',expected='ACCEPT')
vcd_case('exact-P10-truncated-tail','full-observer-vcd-truncated-before-post15.vcd',reason='VCD_TIME_COVERAGE_MISSING')
def missing_head(t):
    header,body=t.split('$enddefinitions $end',1);body='#4000\n'+body.split('#4000\n',1)[1];return header+'$enddefinitions $end\n'+body
vcd_case('missing-head','full-observer-vcd.vcd',mutation=missing_head,reason='VCD_TIME_COVERAGE_MISSING')
vcd_case('unknown-q','full-observer-vcd.vcd',mutation=lambda t:t.replace('b0000 (','bxxxx (',1),reason='VCD_ROW_OUTPUT:q')
vcd_case('missing-signal','full-observer-vcd.vcd',mutation=lambda t:t.replace('$var wire 4 ! a $end\n','',1),reason='VCD_SIGNAL_AMBIGUOUS_OR_ABSENT')
vcd_case('phase-shift','full-observer-vcd.vcd',row_mutation=lambda r:r[1].update(phase='pre'),reason='VCD_ROW_CLOCK_PHASE')
vcd_case('query-after-EOF','full-observer-vcd.vcd',query=16001,reason='VCD_TIME_COVERAGE_MISSING')
put(O/'summary.json',{'scope':'Independent R02 pure mocks and original P10 fixture-byte regression; no actual OS lifecycle guarantee','probe_count':len(rows),'failed_expectations':[x['case'] for x in rows if not x['expectation_met']],'cases':rows,'real_tool_calls':0})
assert all(x['expectation_met'] for x in rows)

