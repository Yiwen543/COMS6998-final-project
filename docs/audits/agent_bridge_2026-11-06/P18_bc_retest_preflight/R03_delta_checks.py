"""Exact R03 P18-R1 delta only. No API,keys,SV,base suite or G1 execution."""
from pathlib import Path
import copy,difflib,hashlib,json,shutil,sys
from unittest.mock import patch
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
A=ROOT/'docs/audits/producer_test2_bc_retest_R03_2026-11-06';S=A/'snapshot';OLD=ROOT/'docs/audits/producer_test2_bc_retest_R02_2026-11-06/snapshot'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def write(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2)
assert sha(A/'phase.json')=='78125b2fa85eadecbab7b5dedb6ad1ad4357a057ce25cb8c55e81a0eb66c0832'
assert sha(A/'snapshot-manifest.json')=='b4fcdc5d5c8656e90785294814502af31f78c32839ab266e55414a16d6e9aca6'
assert sha(OWN/'review.json')=='380dc2deabf0a8972d5c1db46b0475ab8a1b0c241b89ff66657f329e31a36d9b'
manifest=read(A/'snapshot-manifest.json')['files'];reg=read(S/'test2/configs/controller_done_bc_retest_v3.json');source=read(S/reg['source_manifest'])['files']
for n,h in manifest.items():assert sha(A/n)==h,n
for n,h in source.items():assert sha(ROOT/n)==h,n
OUT=OWN/'R03-delta-evidence';OUT.mkdir();code=OUT/'executed-source';code.mkdir()
diffs={}
for name in ['resources.py','api.py','gates.py','pipeline.py','cli.py','release.py','supervision.py']:
    old=(OLD/'test2/retest_v2'/name).read_text();new=(S/'test2/retest_v3'/name).read_text();normalized=new.replace('retest_v3','retest_v2').replace('retest-v3','retest-v2').replace('V3','V2')
    expected=old.replace("record.get('returned_service_tier') in [None,'default']","record.get('returned_service_tier')=='default'") if name=='resources.py' else old
    assert normalized==expected,name
    diffs[name]={'old_sha256':sha(OLD/'test2/retest_v2'/name),'new_sha256':sha(S/'test2/retest_v3'/name),'normalized_diff':list(difflib.unified_diff(old.splitlines(),normalized.splitlines()))}
for n in ['resources.py','api.py','gates.py']:shutil.copyfile(S/'test2/retest_v3'/n,code/n)
codehashes={p.name:sha(p) for p in code.iterdir()};write(OUT/'source-before.json',codehashes)
oldreg=read(OLD/'test2/configs/controller_done_bc_retest_v2.json');changed=sorted(k for k in set(oldreg)|set(reg) if oldreg.get(k)!=reg.get(k));assert changed==['id','preparation_manifest','repair_of','run_root','source_manifest','status']
write(OUT/'mechanical-diff.json',{'runtime':diffs,'registration_changed_keys':changed,'nootherfunctionalchanges':True})
sys.path.insert(0,str(code));import api
from resources import Ledger,Window,Halt
original=read(OWN/'R02-preseal-changed-evidence/missing_tier.input.json')['case']['record']
provider=dict(status='completed',model=original['returned_model'],service_tier=None,usage={k:original['usage'][k] for k in ['input_tokens','output_tokens','total_tokens']},output=[{'type':'message','content':[{'type':'output_text','text':original['output_text']}]}])
cases=[]
for name,tier in [('missing','ABSENT'),('null',None),('nondefault','flex'),('default','default')]:
    data=copy.deepcopy(provider)
    if tier=='ABSENT':del data['service_tier']
    else:data['service_tier']=tier
    p=OUT/(name+'.input.json');write(p,{'fixture_only':True,'raw_provider':data,'expected':'ACCEPT' if name=='default' else 'HALT_FULL_RESERVE'})
    cases.append((name,p,sha(p)))
write(OUT/'inputs-before.json',{p.name:h for _,p,h in cases})
def forbidden(*a,**k):raise AssertionError('NO_REAL_PROCESS_NETWORK_SIGNAL_SLEEP')
results=[]
with patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden),patch('socket.create_connection',side_effect=forbidden),patch('socket.socket.connect',side_effect=forbidden),patch('os.killpg',side_effect=forbidden),patch('time.sleep',side_effect=forbidden):
    for name,p,h in cases:
        data=read(p)['raw_provider'];record=api.provider_result(data,200,{'kind':'ESTIMATE','fixture_only':True});folder=OUT/('SYNTHETIC_ONLY_'+name);folder.mkdir();ledger=Ledger(folder/'ledger.json',reg,{'generation':5910168},Window(0,reg,clock=lambda:100),'mock')
        index=ledger.reserve_api('generation',{'fixture_only':True});ledger.dispatched(index);ledger.api_result(index,record)
        try:
            parsed=api.response_contract(record);upper=ledger.settle(index,record);actual='ACCEPT'
        except Halt as error:
            ledger.halt(str(error));parsed=None;upper=None;actual='HALT_FULL_RESERVE'
        saved=read(ledger.path);assert actual==read(p)['expected']
        assert saved['events'][0]['result']['provider_response']==data and saved['compile_calls']==saved['monitor_replays']==0
        if name=='default':assert upper==487168 and saved['financial_commitment_micro_usd']==487168 and [x['op'] for x in saved['journal']]==['RESERVE','SETTLE_UPPER_AND_RELEASE_UNUSED'] and parsed is not None
        else:assert saved['halted']=='MODEL_OR_TIER_CONTRACT' and saved['financial_commitment_micro_usd']==5910168 and saved['settled_upper_micro_usd']==saved['unused_reservation_released_micro_usd']==0 and [x['op'] for x in saved['journal']]==['RESERVE'] and parsed is None
        results.append({'case':name,'input_sha256':h,'actual':actual,'commitment_microUSD':saved['financial_commitment_micro_usd'],'settled_upper':upper,'raw_provider_JSON_preserved':True,'SV_compiles':0,'actual_API':0})
for _,p,h in cases:assert sha(p)==h
for n,h in codehashes.items():assert sha(code/n)==h
for n,h in manifest.items():assert sha(A/n)==h
for n,h in source.items():assert sha(ROOT/n)==h
assert sha(OWN/'review.json')=='380dc2deabf0a8972d5c1db46b0475ab8a1b0c241b89ff66657f329e31a36d9b'
assert not (ROOT/reg['run_root']).exists() and not Path(str(ROOT/reg['run_root'])+'-supervision').exists()
write(OUT/'results.json',{'status':'EXACT_R03_DELTA_PROBES_PASS','tests':4,'passed':4,'results':results,'snapshot_members':len(manifest),'source_dependencies':len(source),'old_R02_review_unchanged':True,'producer4tests_not_rerun':True,'R01_R02_base_G1_not_rerun':True,'real_API_secret_network_SV_process_signal':0,'limitation':'Independent normalization/contract/ledger probes;full pipeline caller checks reuse saved producer4 plus byteverifiedunchangedcaller.'})
print(json.dumps({'status':'PASS','tests':4,'snapshot_members':len(manifest),'source_dependencies':len(source),'old_R02_review_unchanged':True,'real_tools':0}))
