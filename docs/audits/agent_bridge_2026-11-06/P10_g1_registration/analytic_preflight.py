"""Independent public arithmetic/state preflight only; no SV compiler/tool."""
from pathlib import Path
import json,hashlib,re,sys,copy
P=Path(__file__).resolve().parent;S=P/'exec_tree/test2/g1_v1';sys.path.insert(0,str(S))
import observations as ob
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
O=P/'analytic-preflight';O.mkdir(exist_ok=False)
labels=json.loads((S/'inputs/controls.json').read_text())['cases']
pins=[(0,0,1,0,0),(15,1,0,1,1),(8,1,0,1,1),(1,2,0,1,1)]+[(0,0,0,0,0)]*4
def evaluate(n,step,q):
    a,b,rst,en,valid=pins[step]
    active=int(bool(valid and en and not rst));pre=0 if step<=1 else step-1;post=step
    vals=[1,0,int(((a+b)&15)==((a+b)&15)),int(((a+b)&15)==a+b),int((a-16 if a>=8 else a)<0)==int(a>=8),int((a<0)==(a>=8)),int(a!=0),0,int(q==pre),int(q==post),int(q==pre),int(q==pre),'x',1,1,1]
    if n==6:active=int(bool(valid and en and not rst and a!=0))
    if n in (7,15):active=0
    if n==10:active=int(step<4)
    if n==11:active=int(2<=step<4)
    return active,str(int(vals[n])) if vals[n]!='x' else 'x'
rows_by={};formal=[];mismatches=[]
for n,c in enumerate(labels):
    q=0;rows=[];native_states=[]
    for step in range(8):
        a,b,rst,en,valid=pins[step]
        active,ok=evaluate(n,step,q)
        native_states.append({'cycle':step,'q':q,'active':active,'ok':ok})
        preq=q
        if (not rst if n==11 else rst):q=0
        elif en:q=(q+1)&15
        if step<4:
            for phase,value,tick in [('pre',preq,step*4000+1000),('post',q,step*4000+3000)]:
                act,val=evaluate(n,step,value)
                rows.append({'cycle':step,'a':format(a,'04b'),'b':format(b,'04b'),'rst':str(rst),'en':str(en),'valid':str(valid),'phase':phase,'tick':tick,'q':format(value,'04b'),'active':str(act),'ok':val,'marker':str(int(n==14 and step==3 and phase=='post'))})
    rows_by[c['id']]=rows
    if rows!=c['physical_rows_expected_icarus']:mismatches.append({'case':c['id'],'field':'icarus','derived':rows,'producer':c['physical_rows_expected_icarus']})
    if n not in (12,13) and rows!=c['physical_expected_verilator']:mismatches.append({'case':c['id'],'field':'verilator'})
    fail=[x['cycle'] for x in native_states if x['active']==1 and x['ok']=='0']
    activecycles=[x['cycle'] for x in native_states if x['active']==1]
    expected='DIAGNOSTIC_ONLY_ANY_RAW_STATUS' if n in (12,13) else 'FAIL' if fail else 'PASS'
    cover='PASS' if activecycles else 'NOT_REACHED'
    if (expected,cover)!=(c['native_BMC_expected'],c['activation_cover_expected']):mismatches.append({'case':c['id'],'field':'formal'})
    formal.append({'case':c['id'],'derived_BMC_class':expected,'source_four_state_ok_unknown':n==12,'derived_cover':cover,'first_active_cycle':activecycles[0] if activecycles else None,'first_definite_negative_pre':fail[0] if fail else None,'native_states':native_states,'scope':'Fixed scheduled inputs + initial0,8sample steps;not universal unconstrained input proof;actual native2state QC12/13 unsupported.'})
normalized=[]
for n in range(16):
    t=(S/'sources'/('QC%02d_formal.sv'%n)).read_text();assert '.ID('+str(n)+')' in t;normalized.append(t.replace('.ID('+str(n)+')','.ID(REVIEW_ID)'))
assert len(set(normalized))==1
truth=[{'a':a,'b':b,'sum4':(a+b)&15,'full5':a+b,'low4_equality':True,'zeroextended_full_equality':((a+b)&15)==a+b} for a in range(16) for b in range(16)]
signed=[{'a':a,'signed4':a-16 if a>=8 else a,'signed_negative_matches_msb':((a-16 if a>=8 else a)<0)==bool(a&8),'unsigned_negative_matches_msb':(a<0)==bool(a&8)} for a in range(16)]
assert all(x['signed_negative_matches_msb'] for x in signed)
for name,value in [('rows.json',rows_by),('formal-classes.json',formal),('arithmetic-truth-table.json',truth),('signedness-truth-table.json',signed)]: (O/name).write_text(json.dumps(value,indent=2)+'\n')
# Full observer phase timing, including post3/7/11/15ns transitions.
case=copy.deepcopy(labels[0]);rows=rows_by['QC00'];names=['a','b','rst','en','valid','marker','clk','q','active','ok','obs_phase'];ids={n:chr(33+i) for i,n in enumerate(names)};width={n:4 if n in ('a','b','q') else 1 for n in names}
head=['$timescale 1 ps $end','$scope module physical_tb $end']
for n in [n for n in names if n not in ('q','active','ok')]:head.append('$var wire '+str(width[n])+' '+ids[n]+' '+n+' $end')
head+=['$scope module units[0] $end','$scope module u $end']
for n in ['q','active','ok']:head.append('$var wire '+str(width[n])+' '+ids[n]+' '+n+' $end')
head+=['$upscope $end','$upscope $end','$upscope $end','$enddefinitions $end']
events=[]
for row in rows:
    state={k:row[k] for k in ['a','b','rst','en','valid','marker','q','active','ok']};state.update(clk='0' if row['phase']=='pre' else '1',obs_phase='0')
    events.append((row['tick']-1000,state.copy()))
    if row['phase']=='post':events.append((row['tick'],dict(state,obs_phase='1')))
events.append((16000,dict(events[-1][1],clk='0')));events.sort(key=lambda x:x[0])
probes=[]
for name,es,expect in [('full-observer-vcd',events,'ACCEPT'),('full-observer-vcd-truncated-before-post15',[x for x in events if x[0]<15000],'REJECT')]:
    lines=head.copy()
    for tick,state in es:
        lines.append('#'+str(tick))
        for n,v in state.items():lines.append(('b'+v+' '+ids[n]) if width[n]>1 else v+ids[n])
    f=O/(name+'.vcd');f.write_text('\n'.join(lines)+'\n')
    actual='ACCEPT';error=None
    try:ob.bind_physical_vcd(ob.parse_vcd(f),copy.deepcopy(rows),copy.deepcopy(case))
    except Exception as e:actual='REJECT';error=type(e).__name__+':'+str(e)
    probes.append({'case':name,'expected':expect,'actual':actual,'error':error,'vcd_sha256':H(f),'vcd_last_tick':max(x[0] for x in es),'last_required_observation_tick':15000,'rows_sha256':H(O/'rows.json'),'source_sha256':H(S/'observations.py')})
summary={'scope':'Independent analytic preflight;zero toolchain/version/compile/native/physical/oracle calls','controls':16,'physical_rows_icarus_checked':128,'physical_rows_known_verilator_checked':112,'unsupported_verilator_cases':['QC12','QC13'],'arithmetic_pairs':256,'signed_values':16,'formal_harnesses_same_except_ID':True,'label_mismatches':mismatches,'full_phase_vcd_probes':probes,'source_sha256':{n:H(S/n) for n in ['sources/common.sv','sources/physical_tb.sv','observations.py','inputs/controls.json','inputs/stimulus.json']}}
(O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary));assert not mismatches

