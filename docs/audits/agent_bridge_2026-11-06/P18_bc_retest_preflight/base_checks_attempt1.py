"""R01 base checkpoint: saved hashes,small release/lease/supervisor fixtures only."""
from pathlib import Path
import copy,hashlib,json,shutil,sys
from unittest.mock import patch
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3];A=ROOT/'docs/audits/producer_test2_bc_retest_R01_2026-11-06';S=A/'snapshot'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
def write(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2)
assert sha(A/'snapshot-manifest.json')=='f11203621b0cec51861d423c360d7e95f9bbecee904921dd9dfc82d5a406fa32'
m=read(A/'snapshot-manifest.json')['files']
for n,h in m.items():assert sha(A/n)==h,n
source=read(S/'test2/retest_v1/source-manifest.json')['files']
for n,h in source.items():assert sha(S/n)==h,n
OUT=OWN/'base-evidence';OUT.mkdir();CODE=OUT/'executed-source';CODE.mkdir()
for n in ['resources.py','release.py','api.py','supervision.py']:shutil.copyfile(S/'test2/retest_v1'/n,CODE/n)
write(OUT/'source-before.json',{p.name:sha(p) for p in CODE.glob('*.py')})
sys.path.insert(0,str(CODE))
import release,api,supervision
from resources import Halt,Window,fingerprint
reg=read(S/'test2/configs/controller_done_bc_retest_v1.json')
probes=[]
def refusal(fn,reason):
    try:fn()
    except (Halt,Exception) as e:assert reason in str(e),(reason,str(e));return str(e)
    raise AssertionError('EXPECTED_REFUSAL:'+reason)
def forbidden(*a,**k):raise AssertionError('NO_REAL_PROCESS_SIGNAL_SLEEP')
boundary=read(S/'test2/retest_v1/prompt-boundary.json');packets={}
for n,h in boundary['packet_files'].items():assert sha(S/n)==h;packets[Path(n).stem]=read(S/n)
b,c=packets['B2_raw'],copy.deepcopy(packets['C2_semantic']);extra=c.pop('egraph_feedback');assert b==c
probes.append({'name':'public_packet_only_C_extra','passed':True,'C_only':'egraph_feedback'})
records=read(S/'test2/tasks/axis_length_done_v1/measurements-v1/summary.json')['records'];assert len(records)==162 and sum(bool(x['unknown_records']) for x in records)==38
development=[r for r in records if r['source']=='correct' and r['simulator']=='verilator' and r['split']=='development']
assert len(development)==3
assert 6*(sum(r['cycles'] for r in records)+sum(r['cycles'] for r in development))==204444
assert 6*(len(records)+len(development))==990
saved=OUT/'saved-mock-checks.json';saved_rows=[]
for run in ['cohort','replay']:
    p=S/f'test2/results/controller-done-bc-retest-preparation-v1/integration-attempt2/test_13_full_final_mock_and_replay_shared_grade/inputs/{run}/grade/scores.json'
    scores=read(p);assert len(scores['rounds'])==6
    assert all(len(r['cases'])==162 and r['oracle_unknown_pairs']==38 for r in scores['rounds'])
    saved_rows.append({'run':run,'sha256':sha(p),'rounds':6,'inventory_perround':162,'oracle_unknown_perround':38})
write(saved,saved_rows);probes.append({'name':'saved_inventory_unknown_cost_caps','passed':True,'inventory':162,'oracle_unknown':38,'max_monitor_replays':990,'max_monitor_cycles':204444,'saved19_not_rerun':True})
with patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden),patch('os.killpg',side_effect=forbidden),patch('time.sleep',side_effect=forbidden):
    out=OUT/'SYNTHETIC_RELEASE_NOT_LIVE';out.mkdir();(out/'calls.jsonl').touch();write(out/'run.json',{'mode':'mock','fixture':'REVIEWER_SYNTHETIC_NOT_EXECUTION'});snapshots=[]
    for arm,n in reg['schedule']:
        d=out/arm/'rep1'/f'round{n}';d.mkdir(parents=True)
        valid=(arm=='B2_raw' and n in [1,3]) or (arm=='C2_semantic' and n==2)
        if valid:
            f=d/'compiled';f.mkdir();(f/'candidate.sv').write_text('SYNTHETIC_NOT_SV');write(f/'candidate.json',{'fixture':'NOT_MODEL_OUTPUT'});(f/'replay.vvp').write_text('SYNTHETIC_NOT_EXECUTABLE')
        write(d/'input.json',{'fixture':'SYNTHETIC','status':'compiled' if valid else 'NOT_RUN'})
        snapshots.append(release.freeze(out,d,{'arm':arm,'round':n,'repetition':1,'session_id':arm+'-review-synthetic'},'compiled' if valid else 'NOT_RUN'))
    write(OUT/'release-inputs-before.json',{str(p.relative_to(out)):sha(p) for p in out.rglob('*') if p.is_file()})
    missing=refusal(lambda:release.release(out,snapshots[:-1],'mock',reg),'ALL_SIX_SNAPSHOTS_REQUIRED')
    finals=release.release(out,snapshots,'mock',reg);assert [x['selected_round'] for x in finals]==[3,2];assert len(release.verify(out,reg))==6
    before=sha(out/'release.json');dup=refusal(lambda:release.release(out,snapshots,'mock',reg),'RELEASE_EXISTS');assert sha(out/'release.json')==before
    # A deliberately new mutated copy;leave executed baseline fixture unchanged.
    mutated=OUT/'SYNTHETIC_RELEASE_TAMPER';shutil.copytree(out,mutated);p=mutated/'B2_raw/rep1/round3/compiled/candidate.sv';p.write_text('SYNTHETIC_TAMPER')
    write(OUT/'tamper-inputs-before.json',{str(p.relative_to(mutated)):sha(p) for p in mutated.rglob('*') if p.is_file()})
    tamper=refusal(lambda:release.verify(mutated,reg),'ROUND_ARTIFACT_DRIFT')
    probes.append({'name':'release_before_grading_last_compiled_and_refusals','passed':True,'selected_rounds':[3,2],'missing':missing,'duplicate':dup,'tamper':tamper,'realcompiles':0})
    synth=OUT/'SYNTHETIC_ROOT_NOT_AUTHORITY';out=synth/reg['run_root'];out.mkdir(parents=True);lease=Path(str(out)+'-supervision')/'worker-lease.json';lease.parent.mkdir();write(lease,{'start':0,'out':str(out),'mode':'live','fixture':'SYNTHETIC_NOT_EXECUTION'})
    msg=[{'role':'user','content':'SYNTHETIC'}];schema={'fixture':True};event={'kind':'count','status':'DISPATCH_ATTEMPTED','dispatch_attempted':True,'reserved_micro_usd':1000,'context':{'messages_sha256':fingerprint(msg),'schema_sha256':fingerprint(schema)}}
    ledger={'mode':'live','completed':False,'halted':None,'start_monotonic':0,'work_deadline':3590,'hard_deadline':3600,'counts_reserved':1,'generations_reserved':0,'reserved_micro_usd':1000,'events':[event],'fixture':'SYNTHETIC_NOT_DISPATCH_PROOF'};write(out/'ledger.json',ledger)
    request={'kind':'count','ledger_path':str(out/'ledger.json'),'stage_start':0,'deadline_monotonic':3590,'reservation_index':0,'messages':msg,'schema':schema,'lease_path':str(lease),'lease_sha256':sha(lease),'parent_worker_pid':222,'stage_pgid':222}
    variants=[('valid',request,None)]
    for name,changes,expected in [('wrong_clock',{'stage_start':10},'STAGE_CLOCK_DRIFT'),('wrong_group',{'stage_pgid':333},'API_PARENT_GROUP_REQUIRED')]:variants.append((name,{**request,**changes},expected))
    bad=copy.deepcopy(request);bad['messages'][0]['content']='ALTERED';variants.append(('wrong_payload',bad,'RESERVATION_PAYLOAD_OR_PRICE_DRIFT'))
    for name,r,expected in variants:write(OUT/('lease-'+name+'-before.json'),{'fixture_only':True,'request':r,'expected':expected})
    results=[]
    for name,r,expected in variants:
        fn=lambda:api.verify_reservation(synth,reg,r,{'count':1000},clock=lambda:100,parent_pid=222,group=222)
        if expected:actual=refusal(fn,expected)
        else:assert fn()==out;actual='VALID_METADATA_ONLY'
        results.append({'fixture':name,'actual':actual})
    api.claim_reservation(out,0,'count');claim=sha(out/'api-claims/0.json');refusal(lambda:api.claim_reservation(out,0,'count'),'File exists');assert sha(out/'api-claims/0.json')==claim
    probes.append({'name':'saved_R01_lease_payload_clock_and_exclusiveclaim','passed':True,'results':results,'scope':'Metadatafunctions only;not liveAPI authorization orR02pricingacceptance'})
    class Clock:
        def __init__(self):self.t=0
        def __call__(self):return self.t
        def sleep(self,x):self.t+=x
    for name,timeout in [('normal',False),('deadline',True)]:
        f=OUT/('SYNTHETIC_SUPERVISOR_'+name);f.mkdir();clock=Clock();window=Window(0,reg,clock=clock);calls=[]
        class Process:
            pid=777;returncode=None if timeout else 0
            def poll(self):return self.returncode
            def wait(self,timeout=None):calls.append('wait');return self.returncode
        proc=Process()
        def popen(*a,**kw):assert kw['start_new_session'] is True;calls.append('Popen_FAKE');return proc
        def killpg(pid,sig):
            assert pid==777;calls.append('killpg_FAKE_'+str(sig))
            if proc.returncode is not None:raise ProcessLookupError()
            if sig:proc.returncode=-int(sig)
        result=supervision.owned_stage(['SYNTHETIC_NOT_TOOL'],f,reg,window,{},clock=clock,sleep=clock.sleep,popen=popen,killpg=killpg)
        assert result['within_total_wall'] and not result['mandatory_errors'] and result['deadline_forced_stop']==timeout
        if timeout:assert clock.t>=3595 and result['returncode']==-15 and 'SIGTERM_OWNED_STAGE_GROUP' in result['cleanup']
        write(f/'fake-calls.json',{'scope':'PURE_OBJECTS_NO_PROCESS_SIGNAL_OR_SLEEP','calls':calls,'result':result});probes.append({'name':'owned_stage_'+name,'passed':True,'result':result})
for n,h in read(OUT/'source-before.json').items():assert sha(CODE/n)==h
for n,h in m.items():assert sha(A/n)==h,n
write(OUT/'summary.json',{'status':'BASE_SCOPE_CHECKPOINT_PASS_WITH_LIMITS_NOT_LIVE_ACCEPTANCE','producer_manifest_sha256':sha(A/'snapshot-manifest.json'),'snapshot_members':len(m),'source_dependencies':len(source),'probes':probes,'real_process_signal_sleep_API_key_compile_sim_native':0,'full19suite_rerun':False,'R02_draft_read':False,'remaining':'FinalR02source/reg/prep/costbasis/policyidentitiesandnewHTTP/budget/delaysmustbereviewedbeforeanyEXECUTE'})
print(json.dumps({'status':'BASE_CHECKPOINT_ONLY','probe_groups':len(probes),'snapshot_members':len(m),'source_dependencies':len(source),'real_tools':0}))
