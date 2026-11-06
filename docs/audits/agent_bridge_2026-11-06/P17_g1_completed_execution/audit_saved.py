"""Independent fixed-format saved-evidence analysis. No producer parser imports."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,subprocess
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
A=ROOT/'docs/audits/producer_test2_g1_E04_2026-11-06';S=A/'snapshot'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
def write(p,x):
    with p.open('x') as f:json.dump(x,f,indent=2)
assert sha(A/'phase.json')=='cc5b0539aedef0bdfda9b763935838fafbb154f450535a342fa843c59f5b22e2'
assert sha(A/'snapshot-manifest.json')=='43d9e3cdc21abc79d6dda5b634b24158072d6df6b0a6863e079c4a9e4e219152'
manifest=read(A/'snapshot-manifest.json')['files']
for p,h in manifest.items():assert sha(A/p)==h,p
source=read(S/'test2/g1_v5b/source-manifest.json')['files']
for p,h in source.items():assert sha(S/p)==sha(ROOT/p)==h,p
REG=read(S/'test2/configs/g1_qualification_registration_v5b.json');R=S/REG['result_root'];report=read(R/'report.json');pool=read(R/'execution-state.json')
for n,h in [('execution-state.json','f67ece87c4884f0f5d5ba9211b381405d48fa435973366d85cf101f762e2ab41'),('report.json','4c9792eb3068896cbb74183b11509489d2db7bbf125bc8dfaf046a1b060d21ac'),('result-manifest.json','10c36f87215bc7849fe467f34df0fef91d80880a950456f7dce4362110541d0c')]:assert sha(R/n)==h
rm=read(R/'result-manifest.json')
for n,h in rm['files'].items():assert sha(R/n)==h,n
receipt=read(S/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r05b.json')
assert report['execution_receipt_sha256']==sha(S/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r05b.json')=='82f56b7855e228b43a1f951a2e5d8f7bbd6dd835f1ecce3a5b09678142ae2dcc'
assert sha(S/receipt['p16_review_path'])==receipt['p16_review_sha256']=='317c1d178d1bf3aeccebdb85392e97e00eff022167f5d6169580c470e2849a20'
for k in ['registration_sha256','source_manifest_sha256','continuation_decision_sha256','reuse_manifest_sha256','budget_amendment_sha256']:assert report[k]==receipt[k]
assert receipt['preparation_manifest_sha256']=='f02225f65b42899083ea9b88a1931218b6512aaf71ee36657b176aca149dbf0d'
events=pool['events'];plan=read(S/REG['job_plan'])['jobs'];assert [e['job_id'] for e in events]==[j['id'] for j in plan]==list(report['jobs'])
exitcounts=Counter();observed=Counter();timing=[]
for j,e in zip(plan,events):
    f=R/'jobs'/j['id'];r=read(f/'receipt.json');rr=report['jobs'][j['id']]
    for k,v in r.items():assert rr[k]==v and e[k]==v,(j['id'],k)
    argv=[x.replace('{ROOT}',str(ROOT)).replace('{OUT}',str(ROOT/REG['result_root'])).replace('{JOB}',str(ROOT/REG['result_root']/'jobs'/j['id'])) for x in j['argv']]
    assert argv==r['argv'] and r['status']=='RETURNED' and r['dispatch_attempted'] is True
    assert r['root_exit_knownness']=='KNOWN_FROM_CLEANUP_WAIT' and r['mandatory_errors']==[] and r['timed_out'] is False and r['cleanup_group_kill'] is False
    assert type(r['exit_code']) is int and r['exit_code'] in [0,1]
    for stem in ['stdout','stderr']:assert sha(f/(stem+'.log'))==r[stem+'_sha256']
    assert r['inventory']['attempts']==0 and r['inventory']['complete'] is False and r['child_pid_inventory_complete'] is False
    assert r['inventory']['mode']=='owned_process_group_only' and r['owned_group_probe']=='ABSENT_AT_OWNED_PROBE_NOT_A_CENSUS'
    assert type(r['process_group']) is int and r['process_group']>0
    assert e['reserved_cycles']==j.get('cycles',0)
    assert r['absolute_job_deadline']==min(e['absolute_job_start']+REG['caps'][j['kind']+'_timeout'],pool['start_monotonic']+1180)
    assert 0.25<r['remaining_at_last_dispatch_check']<=REG['caps'][j['kind']+'_timeout']
    assert r['elapsed_seconds_including_cleanup']<=REG['caps'][j['kind']+'_timeout'] and e['terminal_at_elapsed']<1180
    exitcounts[r['exit_code']]+=1;observed[j['kind']]+=1;observed['physical_cycles']+=j.get('cycles',0)
    timing.append({'job':j['id'],'kind':j['kind'],'cleanup_elapsed':r['elapsed_seconds_including_cleanup'],'cap':REG['caps'][j['kind']+'_timeout']})
assert observed==Counter(compile=14,native=28,physical=30,physical_cycles=120)
assert pool['completed'] is True and pool['halted'] is False and pool['reserved']==dict(setup=8,compile=20,native=32,physical=33,physical_cycles=132)
assert pool['prior_reserved']==dict(setup=8,compile=6,native=4,physical=3,physical_cycles=12)
assert pool['prior_conservative_charge_seconds']==15 and pool['current_attempt_window_seconds']==1185
assert abs(pool['cumulative_charged_window_seconds']-15-pool['attempt_elapsed_checkpoint_seconds'])<1e-4
assert abs(pool['cumulative_actual_window_seconds']-11.770645541138947-pool['attempt_elapsed_checkpoint_seconds'])<1e-4
assert pool['cumulative_charged_window_seconds']<1200 and pool['total_elapsed_seconds']<1185
assert len(report['reused_jobs'])==10 and all(x['new_execution'] is False for x in report['reused_jobs'].values())
assert report['status']=='COMPLETE_PENDING_INDEPENDENT_REVIEW'

def vcd(p):
    text=p.read_text();header,body=text.split('$enddefinitions $end',1);scope=[];signals={}
    scale=tuple(re.search(r'\$timescale\s+(\d+)\s*(\w+)\s+\$end',header).groups())
    for line in header.splitlines():
        a=line.split()
        if not a:continue
        if a[0]=='$scope':scope.append(a[2])
        elif a[0]=='$upscope':scope.pop()
        elif a[0]=='$var':signals['.'.join(scope+[a[4]])]=(a[3],int(a[2]))
    values={};states={};tick=0;last=0
    for line in body.splitlines():
        line=line.strip()
        if not line or line.startswith('$'):continue
        if line.startswith('#'):
            states[tick]=values.copy();tick=int(line[1:]);assert tick>=last;last=tick
        elif line[0].lower()=='b':bits,key=line[1:].split();values[key]=bits.lower()
        elif line[0].lower() in '01xz':values[line[1:]]=line[0].lower()
        else:raise AssertionError(('VCD_SYNTAX',line))
    states[tick]=values.copy()
    def value(t,name):
        assert min(states)<=t<=last,(p,t,last)
        candidates=[x for x in signals if x==name or x.endswith('.'+name)];assert len(candidates)==1,(name,candidates)
        key,width=signals[candidates[0]];bits=states[max(k for k in states if k<=t)][key]
        assert len(bits)<=width;return bits.rjust(width,bits[0] if bits[0] in 'xz' else '0')
    return scale,states,last,value

def expr(n,step,q,a,b,rst,en,valid):
    active=int(valid and en and not rst);ok=1
    if n==1:ok=0
    if n==2:ok=int(((a+b)&15)==((a+b)&15))
    if n==3:ok=int(((a+b)&15)==a+b)
    if n==4:ok=int(((a-16 if a&8 else a)<0)==bool(a&8))
    if n==5:ok=int((a<0)==bool(a&8))
    if n==6:active=int(active and a!=0);ok=int(a!=0)
    if n==7:active=0;ok=0
    if n==8:ok=int(q==(0 if step<=1 else step-1))
    if n==9:ok=int(q==step)
    if n==10:active=int(step<4);ok=int(q==(0 if step<=1 else step-1))
    if n==11:active=int(2<=step<4);ok=int(q==(0 if step<=1 else step-1))
    if n==12:ok='x'
    if n==13:ok=1
    if n==15:active=0
    return str(active),str(ok)
def derive(n):
    q=0;rows=[];formal=[]
    for step in range(8):
        a,b,rst,en,valid=[(0,0,1,0,0),(15,1,0,1,1),(8,1,0,1,1),(1,2,0,1,1)][step] if step<4 else (0,0,0,0,0)
        active,ok=expr(n,step,q,a,b,rst,en,valid);formal.append({'cycle':step,'q':format(q,'04b'),'active':active,'ok':ok})
        for phase in ['pre','post']:
            if phase=='post':q=(0 if not rst else (q+1 if en else q)) if n==11 else (0 if rst else (q+1 if en else q))
            active,ok=expr(n,step,q,a,b,rst,en,valid)
            if step<4:rows.append(dict(cycle=step,phase=phase,tick=4000*step+(1000 if phase=='pre' else 3000),q=format(q,'04b'),active=active,ok=ok,marker=str(int(n==14 and step==3 and phase=='post')),a=format(a,'04b'),b=format(b,'04b'),rst=str(rst),en=str(en),valid=str(valid)))
    return rows,formal
labels=read(S/REG['controls'])['cases'];allrows={};matrix=[];counts=Counter();unknownrows=[];bindings=[]
pattern=re.compile(r'^OBS qc=(\d+) cycle=(\d+) phase=(pre|post) tick=(\d+) q=([01xz]{4}) active=([01xz]) ok=([01xz]) marker=([01xz]) a=([01xz]{4}) b=([01xz]{4}) rst=([01xz]) en=([01xz]) valid=([01xz])$',re.M)
for n in range(16):
    cid=f'QC{n:02}';expected,finite=derive(n);label=labels[n]
    assert expected==label['physical_rows_expected_icarus'],cid
    for sim in ['icarus','verilator']:
        f=S/('test2/results/g1-qualification-v4' if n==0 else REG['result_root'])/'jobs'/(cid+'-'+sim)
        text=(f/'stdout.log').read_text();matches=pattern.findall(text);assert len(matches)==len(re.findall('^OBS ',text,re.M))==8
        assert re.search(r'^END qc='+str(n)+r' cycles=4 posedges=4$',text,re.M)
        rows=[];scale,states,last,value=vcd(f/'trace.vcd');assert scale==('1','ps') and last==16000
        edges=[];previous=None
        for tick in sorted(states):
            clock=value(tick,'physical_tb.clk')
            if previous=='0' and clock=='1':edges.append(tick)
            previous=clock
        assert edges==[2000,6000,10000,14000]
        for idx,m in enumerate(matches):
            assert int(m[0])==n;row=dict(zip(['cycle','phase','tick','q','active','ok','marker','a','b','rst','en','valid'],m[1:]));row['cycle']=int(row['cycle']);row['tick']=int(row['tick'])
            for k,v in expected[idx].items():
                if sim=='verilator' and n in [12,13] and k=='ok':assert row[k] in '01'
                else:assert row[k]==v,(cid,sim,idx,k,row[k],v)
            for k in ['a','b','rst','en','valid','marker']:assert value(row['tick'],'physical_tb.'+k)==row[k]
            for k in ['q','active','ok']:assert value(row['tick'],f'physical_tb.units[{n}].u.'+k)==row[k]
            assert value(row['tick'],'physical_tb.clk')==('0' if row['phase']=='pre' else '1')
            assert value(row['tick'],'physical_tb.obs_phase')==('0' if row['phase']=='pre' else '1')
            if 'x' in row['ok']:unknownrows.append({'qc':cid,'simulator':sim,'row':idx,'field':'ok'})
            assert set(''.join(row[k] for k in ['a','b','rst','en','valid']))<=set('01')
            rows.append(row)
        allrows[cid+'-'+sim]=rows
    raw_native={}
    for mode in ['bmc','cover']:
        version='v3' if n==0 else ('v4' if n==1 else 'v5b');f=S/f'test2/results/g1-qualification-{version}/jobs/{cid}-{mode}'
        sourcepath=ROOT/f'test2/g1_{version if n<2 else "v5"}/sources/{cid}_formal.sv'
        rr=read(f/'receipt.json');text=(f/'stdout.log').read_text()+'\n'+(f/'stderr.log').read_text();status=re.findall(r'^##\s+\S+\s+Status: (PASSED|FAILED)$',text,re.M);assert len(status)==1
        assert rr['exit_code']==(0 if status[0]=='PASSED' else 1) and rr['status']=='RETURNED' and not rr['timed_out'] and not rr['mandatory_errors']
        counts['native_'+status[0]]+=1
        lines=[x for x in text.splitlines() if 'Assert failed' in x];assert all(str(sourcepath)+':16.' in x for x in lines)
        assert not (lines and status[0]=='PASSED')
        raw={'tool_status':status[0],'exit':rr['exit_code'],'assertion':'FAILED' if lines else 'NO_FAILURE_REPORTED','stdout_sha256':sha(f/'stdout.log'),'receipt_sha256':sha(f/'receipt.json')}
        prod=(report['reused_jobs'] if n<2 else report['jobs'])[cid+'-'+mode]['native_evidence']
        assert prod['evidence_complete'] and prod['tool_status']==status[0] and prod['process_exit_code']==rr['exit_code'] and prod['assertion_observation']==raw['assertion']
        if mode=='bmc':
            assert '-c' not in rr['argv'];predicted='FAIL' if any(x['active']=='1' and x['ok']=='0' for x in finite) else 'PASS'
            actual='PASS' if status[0]=='PASSED' else 'FAIL';assert n in [12,13] or actual==predicted
            assert actual==prod['native_BMC_status'];counts['BMC_'+actual]+=1;raw['BMC']=actual
        else:
            assert rr['argv'].count('-c')==1
            reached=re.findall(r'Reached cover statement in step (\d+) at formal_top: (.*)',text)
            unreached=[x for x in text.splitlines() if 'Unreached cover statement' in x]
            assert (len(reached),len(unreached)) in [(1,0),(0,1)]
            activation='REACHED' if reached else 'UNREACHED';assert activation==('REACHED' if any(x['active']=='1' for x in finite) else 'UNREACHED')
            assert prod['activation']==activation;counts[activation]+=1;raw['activation']=activation
            if reached:assert str(sourcepath)+':17.' in reached[0][1]
            else:assert str(sourcepath)+':17.' in unreached[0] and status[0]=='FAILED' and not lines
        if (f/'trace.vcd').exists():
            scale,states,last,value=vcd(f/'trace.vcd');assert scale==('1','ns')
            if mode=='cover':
                step=int(reached[0][0]);assert 0<=step<8 and last==10*(step+1)
                assert any(int(value(t,'smt_step'),2)==step and value(t,'formal_top.sampled_active')=='1' for t in states)
            samples=[]
            for tick in sorted(states):
                active=value(tick,'formal_top.sampled_active');ok=value(tick,'formal_top.sampled_ok')
                if active=='1' and ok=='0':samples.append({'tick':tick,'cycle':int(value(tick,'formal_top.sampled_cycle'),2),'q':value(tick,'formal_top.sampled_q')})
            if mode=='bmc' and raw['BMC']=='FAIL' and n not in [12,13]:
                assert samples
                for sample in samples:
                    for sim in ['icarus','verilator']:
                        row=next(x for x in allrows[cid+'-'+sim] if x['phase']=='pre' and x['cycle']==sample['cycle'])
                        assert row['q']==sample['q'] and row['active']=='1' and row['ok']=='0'
                bindings.append({'qc':cid,'sampled_registered_pre':samples,'two_physical_sims_match':True})
            raw['trace_sha256']=sha(f/'trace.vcd')
        raw_native[mode]=raw
    matrix.append({'qc':cid,'title':label['D01_title'],'eligibility':label['eligibility'],'native':raw_native,'physical_runs':2,'rows':16,'phase_rejection_control':n==9,'finite_contract_matched':True,'real_DUT_or_oracle_credit':False})
assert len(unknownrows)==8 and all(x['qc']=='QC12' and x['simulator']=='icarus' for x in unknownrows)
assert counts==Counter(native_PASSED=18,native_FAILED=14,BMC_PASS=10,BMC_FAIL=6,REACHED=14,UNREACHED=2)
for p,h in manifest.items():assert sha(A/p)==h
for p,h in source.items():assert sha(ROOT/p)==h
index=hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)).hexdigest()
assert index==read(A/'before-execution.json')['index_entries_sha256']
write(OWN/'physical-rows.json',allrows)
write(OWN/'independent-analysis.json',{'status':'SAVED_EVIDENCE_CHECKS_PASS','snapshot_members':len(manifest),'source_dependencies':len(source),'result_manifest_members':len(rm['files']),'new_jobs':len(plan),'new_exit_counts':dict(exitcounts),'new_resources':dict(observed),'cumulative_resources':pool['reserved'],'cumulative_actual_checkpoint_seconds':pool['cumulative_actual_window_seconds'],'cumulative_charged_checkpoint_seconds':pool['cumulative_charged_window_seconds'],'current_total_elapsed_seconds':pool['total_elapsed_seconds'],'native_counts':dict(counts),'valid_physical_runs':32,'valid_physical_rows':256,'known_inputs_all_rows':True,'intentional_unknown_rows':unknownrows,'native_physical_pre_bindings':bindings,'control_matrix':matrix,'job_timing':timing,'index_sha256':index,'real_tools_or_experiments':0,'methods':'Independent Python mathematics/log/VCD parser;no producer parser imported;no mock or tool execution.'})
print(json.dumps({'status':'PASS','controls':16,'new_jobs':72,'physical_rows':256,'native':dict(counts),'intentional_unknown_ok_rows':len(unknownrows)}))
