"""Small R02 pre-seal probes. Not final source acceptance or live execution."""
from pathlib import Path
import copy,hashlib,json,shutil,sys
from unittest.mock import patch
from types import SimpleNamespace
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def write(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2)
OUT=OWN/'R02-preseal-changed-evidence';OUT.mkdir();code=OUT/'executed-source';code.mkdir()
for n in ['api.py','resources.py','gates.py']:shutil.copyfile(ROOT/'test2/retest_v2'/n,code/n)
hashes={p.name:sha(p) for p in code.iterdir()};write(OUT/'source-before.json',hashes)
reg=read(ROOT/'test2/configs/controller_done_bc_retest_v2.json');write(OUT/'observed-registration-not-final.json',reg)
sys.path.insert(0,str(code));import api
from resources import Ledger,Window,Halt
normal={'status':'completed','provider_status':'completed','returned_model':'gpt-6.1-sol','returned_service_tier':'default','long_cache_write':False,'unexpected_output_type':False,'usage':{'input_tokens':64000,'output_tokens':8192,'total_tokens':72192,'cached_input_tokens':None,'reasoning_output_tokens':None},'output_text':'{"body":"SYNTHETIC_NOT_CANDIDATE","properties":[]}','request_issued':True}
cases=[]
for name,field,value,expect in [('valid','returned_service_tier','default','ACCEPT'),('missing_tier','returned_service_tier',None,'REJECT'),('wrong_tier','returned_service_tier','flex','REJECT'),('cache12h','long_cache_write',True,'REJECT')]:
    record=copy.deepcopy(normal);record[field]=value;cases.append({'name':name,'record':record,'expected':expect})
for name,field,value in [('unknown_input','input_tokens',None),('over_input','input_tokens',64001),('bool_input','input_tokens',True),('over_output','output_tokens',8193)]:
    record=copy.deepcopy(normal);record['usage'][field]=value;cases.append({'name':name,'record':record,'expected':'REJECT'})
for c in cases:write(OUT/(c['name']+'.input.json'),{'fixture_only':True,'case':c})
input_hashes={p.name:sha(p) for p in OUT.glob('*.input.json')};write(OUT/'inputs-before.json',input_hashes)
def forbidden(*a,**k):raise AssertionError('NO_REAL_NETWORK_PROCESS_SIGNAL_SLEEP')
results=[]
with patch('socket.create_connection',side_effect=forbidden),patch('socket.socket.connect',side_effect=forbidden),patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden),patch('os.killpg',side_effect=forbidden),patch('time.sleep',side_effect=forbidden):
    for c in cases:
        folder=OUT/('SYNTHETIC_ONLY_'+c['name']);folder.mkdir();b=Ledger(folder/'ledger.json',reg,{'generation':5910168},Window(0,reg,clock=lambda:100),'mock')
        i=b.reserve_api('generation',{'fixture':'SYNTHETIC_NOT_LIVE'});b.dispatched(i);b.api_result(i,c['record'])
        try:upper=b.settle(i,c['record']);actual='ACCEPT';reason=None
        except Halt as e:upper=None;actual='REJECT';reason=str(e)
        saved=read(b.path);results.append({'case':c['name'],'expected':c['expected'],'actual':actual,'reason':reason,'settled_upper':upper,'commitment':saved['financial_commitment_micro_usd'],'fixture_sha256':input_hashes[c['name']+'.input.json'],'source_sha256':hashes['resources.py']})
    assert results[0]['actual']=='ACCEPT' and results[1]['actual']=='ACCEPT'
    assert all(x['actual']=='REJECT' and x['commitment']==5910168 for x in results[2:])
    # Fake transport only; verify fixed host/path,no redirect-follow or retries.
    calls=[]
    class Conn:
        def __init__(self,host,timeout,context):calls.append(['factory',host,timeout])
        def request(self,method,path,body,headers):calls.append(['request',method,path])
        def getresponse(self):return SimpleNamespace(status=302,read=lambda n:forbidden())
        def close(self):calls.append(['close'])
    context=SimpleNamespace(verify_mode=api.ssl.CERT_REQUIRED,check_hostname=True,cert_store_stats=lambda:{'x509_ca':1})
    with patch.object(api.ssl,'create_default_context',return_value=context):
        try:api.post_json(api.request_payload([{'role':'user','content':'SYNTHETIC_PUBLIC'}],{}),'SYNTHETIC_NOT_SECRET',10,Conn)
        except api.HTTPFailure as e:assert e.status==302
        else:raise AssertionError('REDIRECT_MUST_FAIL')
    assert calls==[['factory','api.openai.com',10],['request','POST','/v1/responses'],['close']]
for p,h in input_hashes.items():assert sha(OUT/p)==h
for p,h in hashes.items():assert sha(code/p)==h
write(OUT/'results.json',{'phase':'P18_R02_PRESEAL_CHANGED_PATH_PROBES','status':'CONFIRMED_PRESEAL_CONTRACT_GAP_NOT_FINAL_REVIEW','cases':results,'transport_fake_calls':calls,'observed_missing_tier_releases':5910168-results[1]['commitment'],'final_R02_seal_not_bound':True,'actual_API_key_reads_process_network_SV':0})
print(json.dumps({'status':'PRESEAL_CHECKPOINT','missing_tier_actual':results[1]['actual'],'missing_tier_commitment':results[1]['commitment'],'other_refusals':6,'real_tools':0,'source_sha256':hashes}))
