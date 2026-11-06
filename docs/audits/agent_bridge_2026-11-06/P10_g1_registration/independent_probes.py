"""P10 independent preflight probes; no real subprocess/clock sleep/tool call."""
from pathlib import Path
import sys,json,hashlib,types,copy
P=Path(__file__).resolve().parent
SRC=P/'exec_tree/test2/g1_v1';sys.path.insert(0,str(SRC))
import budget as bm, runtime as rt, observations as ob
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
O=P/'independent-probes';O.mkdir(exist_ok=False)
CAPS=json.loads((P/'exec_tree/test2/configs/g1_qualification_registration_v1.json').read_text())['caps']
def put(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
records=[]
def timer_probe(name,at,delay,expected_launches):
    d=O/name;d.mkdir();clock=[0];calls=[];b=bm.Budget(d/'synthetic-budget.json',CAPS,clock=lambda:clock[0]);clock[0]=at
    old_save=b.save;once=[False]
    def delayed_save():
        if not once[0] and b.state['events']:
            once[0]=True;clock[0]+=delay
        old_save()
    b.save=delayed_save
    class Child:
        pid=999999
        returncode=0
        def __init__(self,argv,**kw):calls.append({'argv':argv,'virtual_dispatch_elapsed':clock[0]})
        def poll(self):return 0
        def wait(self,timeout=None):return 0
    def no_group(*args):raise ProcessLookupError()
    def prohibited(*args,**kwargs):raise AssertionError('REAL_CHILD_OR_PS_OR_SLEEP_PROHIBITED')
    saved=(rt.subprocess,rt.os,rt.time)
    rt.subprocess=types.SimpleNamespace(Popen=Child,run=prohibited,TimeoutExpired=TimeoutError)
    rt.os=types.SimpleNamespace(killpg=no_group)
    rt.time=types.SimpleNamespace(monotonic=lambda:clock[0],sleep=prohibited)
    receipt=None;error=None
    try:receipt=rt.execute(b,{'id':name,'kind':'setup','cycles':0,'argv':['SYNTHETIC_NEVER_EXECUTED']},d/'job',{})
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:rt.subprocess,rt.os,rt.time=saved
    x={'case':name,'clock_before_reserve':at,'simulated_reservation_persistence_delay':delay,'expected_launches':expected_launches,'actual_mock_launches':len(calls),'mock_calls':calls,'receipt':receipt,'error':error,'halted':b.state['halted'],'actual_OS_processes_spawned':0,'source_sha256':{n:H(SRC/n) for n in ['budget.py','runtime.py']}}
    put(d/'result.json',x);records.append(x)
timer_probe('normal-dispatch',100,0,1)
timer_probe('already-expired-refused',1196,0,0)
timer_probe('deadline-crossed-during-reservation',1194,7,0)
# Analytically valid QC00 trajectory. The negative fixture removes the post15ns
# observer transition and final edge; all previously bound signal values remain.
case=json.loads((SRC/'inputs/controls.json').read_text())['cases'][0]
ids={n:chr(33+i) for i,n in enumerate(['a','b','rst','en','valid','marker','clk','q','active','ok','obs_phase'])}
width={'a':4,'b':4,'q':4,**{n:1 for n in ids if n not in ('a','b','q')}}
head=['$timescale 1 ps $end','$scope module physical_tb $end']
for n in ['a','b','rst','en','valid','marker','clk','obs_phase']:head.append('$var wire '+str(width[n])+' '+ids[n]+' '+n+' $end')
head+=['$scope module units[0] $end','$scope module u $end']
for n in ['q','active','ok']:head.append('$var wire '+str(width[n])+' '+ids[n]+' '+n+' $end')
head+=['$upscope $end','$upscope $end','$upscope $end','$enddefinitions $end']
events=[]
for row in case['physical_rows_expected_icarus']:
    tick=row['tick']-1000 # changed values already stable one ns before observation
    state={k:row[k] for k in ['a','b','rst','en','valid','marker','q','active','ok']}
    state.update(clk='0' if row['phase']=='pre' else '1',obs_phase='0' if row['phase']=='pre' else '1')
    # obs_phase becomes1 at actual post observation rather than at edge.
    state['obs_phase']='0'
    events.append((tick,state))
# Include real observer phase transitions at15ns and final clock0 at16ns.
events += [(15000,dict(events[-1][1],obs_phase='1')),(16000,dict(events[-1][1],clk='0',obs_phase='1'))]
events.sort(key=lambda x:x[0])
def encode(es):
    parts=head.copy()
    for tick,state in es:
        parts.append('#'+str(tick))
        for n,v in state.items():parts.append(('b'+v+' '+ids[n]) if width[n]>1 else v+ids[n])
    return '\n'.join(parts)+'\n'
for name,es,expected in [('complete-vcd',events,'ACCEPT'),('truncated-vcd-before-final-observation',[x for x in events if x[0]<15000],'REJECT')]:
    d=O/name;d.mkdir();f=d/'synthetic-trace.vcd';f.write_text(encode(es));put(d/'expected-rows.json',case['physical_rows_expected_icarus'])
    error=None;actual='ACCEPT'
    try:ob.bind_physical_vcd(ob.parse_vcd(f),copy.deepcopy(case['physical_rows_expected_icarus']),copy.deepcopy(case))
    except Exception as e:actual='REJECT';error=type(e).__name__+':'+str(e)
    x={'case':name,'expected':expected,'actual':actual,'error':error,'last_vcd_tick':max(t for t,_ in es),'last_required_observation_tick':15000,'fixture_sha256':H(f),'rows_sha256':H(d/'expected-rows.json'),'source_sha256':H(SRC/'observations.py'),'actual_tool_calls':0};put(d/'result.json',x);records.append(x)
put(O/'summary.json',{'scope':'Pure mock timer and synthetic VCD parser preflight,not toolchain qualification','records':records,'mismatches':[x['case'] for x in records if ('expected_launches' in x and x['expected_launches']!=x['actual_mock_launches']) or ('expected' in x and x['expected']!=x['actual'])]})
for x in records:print(json.dumps(x))

