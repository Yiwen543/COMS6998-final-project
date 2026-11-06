"""Zero-count fixed-endpoint stdlib HTTPS child;no SDK or implicit retries."""
from pathlib import Path
import argparse,hashlib,http.client,json,os,ssl,stat,time
from resources import Halt,require,sha,fingerprint,trusted_success
from gates import authorize
CA_FILE='/etc/ssl/cert.pem'
PAYLOAD_KEYS={'model','input','reasoning','text','store','max_output_tokens','service_tier','prompt_cache_options'}

def request_payload(messages,schema):
    return dict(model='gpt-6.1-sol',input=messages,reasoning={'effort':'low'},text={'format':{'type':'json_schema','name':'controller_done_monitor','strict':True,'schema':schema}},store=False,max_output_tokens=8192,service_tier='default',prompt_cache_options={'mode':'implicit','ttl':'30m'})
def payload_bytes(payload):return json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def payload_sha(payload):return hashlib.sha256(payload_bytes(payload)).hexdigest()
def estimate(payload):
    size=len(payload_bytes(payload));return dict(kind='ESTIMATE',version='complete_payload_utf8_div2p5_plus4096_v1',UTF8bytes=size,value=(size*2+4)//5+4096,target=64000,not_exact_token_count=True,not_server_input_hardcap=True,payload_sha256=payload_sha(payload))
def response_contract(record,expected=None):return trusted_success(record)[1]

def provider_result(data,status,admission):
    """Keep the provider JSON even if its nested shape cannot be normalized."""
    try:
        usage=data.get('usage') or {};details=usage.get('input_tokens_details') or {};output_details=usage.get('output_tokens_details') or {};outputs=data.get('output') or []
        text=''.join(c.get('text','') for item in outputs if item.get('type')=='message' for c in item.get('content',[]) if c.get('type')=='output_text')
        unexpected=any(item.get('type') not in ['message','reasoning'] for item in outputs)
        return dict(status='completed',HTTP_status=status,provider_status=data.get('status'),returned_model=data.get('model'),returned_service_tier=data.get('service_tier'),response_id=data.get('id'),output_text=text,usage=dict(input_tokens=usage.get('input_tokens'),output_tokens=usage.get('output_tokens'),total_tokens=usage.get('total_tokens'),cached_input_tokens=details.get('cached_tokens'),reasoning_output_tokens=output_details.get('reasoning_tokens')),raw_usage=usage,provider_response=data,long_cache_write=bool((details.get('cache_write_tokens_details') or {}).get('ttl_12h_tokens')),cache_subset_knownness='KNOWN' if details else 'UNKNOWN',unexpected_output_type=unexpected,request_issued=True,input_estimate=admission,remote_count_requests=0)
    except Exception as error:
        return dict(status='request_error',HTTP_status=status,error_type=type(error).__name__,usage=None,provider_response=data,actual_cost_usd=None,request_issued=True,remote_count_requests=0,error_message_omitted_to_protect_credentials=True)

class HTTPFailure(Exception):
    def __init__(self,status):self.status=status

def post_json(payload,credential,timeout,connection_factory=None):
    require(set(payload)==PAYLOAD_KEYS and payload['model']=='gpt-6.1-sol' and payload['service_tier']=='default' and payload['reasoning']=={'effort':'low'} and payload['max_output_tokens']==8192 and payload['prompt_cache_options']=={'mode':'implicit','ttl':'30m'} and payload['store'] is False,'HTTP_REQUEST_CONTRACT')
    require(type(timeout) in [int,float] and 0.05<timeout<=120,'HTTP_DEADLINE_EXHAUSTED')
    context=ssl.create_default_context(cafile=CA_FILE)
    require(context.verify_mode==ssl.CERT_REQUIRED and context.check_hostname and context.cert_store_stats()['x509_ca']>0,'TLS_TRUST_STORE_REQUIRED')
    factory=connection_factory or http.client.HTTPSConnection;connection=factory('api.openai.com',timeout=timeout,context=context)
    try:
        connection.request('POST','/v1/responses',body=payload_bytes(payload),headers={'Authorization':'Bearer '+credential,'Content-Type':'application/json','Accept':'application/json'})
        response=connection.getresponse()
        if not 200<=response.status<300:raise HTTPFailure(response.status)  # no redirect,errorbody or credentials in logs
        body=response.read(8*1024*1024+1);require(len(body)<=8*1024*1024,'HTTP_RESPONSE_TOO_LARGE')
        data=json.loads(body);require(isinstance(data,dict),'MALFORMED_HTTP_RESPONSE');return data,response.status
    finally:connection.close()

def verify_reservation(root,reg,request,pricing,clock=time.monotonic,parent_pid=None,group=None):
    """HTTP work cannot bypass the single live ledger and supervised worker lease."""
    root=Path(root);out=(root/reg['run_root']).resolve();ledger_path=out/'ledger.json'
    require(Path(request['ledger_path']).resolve()==ledger_path,'WRONG_LIVE_LEDGER')
    require(ledger_path.is_file() and not ledger_path.is_symlink(),'LIVE_LEDGER_REQUIRED');ledger=json.loads(ledger_path.read_text())
    require(ledger['mode']=='live' and not ledger['completed'] and not ledger['halted'],'LIVE_LEDGER_NOT_ACTIVE')
    require(ledger['start_monotonic']==request['stage_start'] and ledger['work_deadline']==request['deadline_monotonic']==request['stage_start']+reg['wall']['stop_work_seconds'],'STAGE_CLOCK_DRIFT')
    require(clock()<ledger['work_deadline'] and ledger['hard_deadline']==request['stage_start']+3600,'STAGE_EXPIRED')
    require(ledger['counts_reserved']==0 and ledger['generations_reserved']<=12 and ledger['financial_commitment_micro_usd']<=20000000,'LEDGER_LIMIT_DRIFT')
    require(type(request['reservation_index']) is int and 0<=request['reservation_index']<len(ledger['events']),'RESERVATION_REQUIRED')
    require(ledger['financial_commitment_micro_usd']==sum(e['commitment_micro_usd'] for e in ledger['events'])==ledger['settled_upper_micro_usd']+ledger['unresolved_reservations_micro_usd'],'FINANCIAL_LEDGER_INVARIANT')
    event=ledger['events'][request['reservation_index']]
    require(event['kind']==request['kind'] and event.get('dispatch_attempted') is True and event['status']=='DISPATCH_ATTEMPTED' and event['settled_upper_micro_usd'] is None and event['commitment_micro_usd']==5910168,'OPEN_RESERVATION_REQUIRED')
    require(event['reserved_micro_usd']==pricing[request['kind']] and event['context']['messages_sha256']==fingerprint(request['messages']) and event['context']['schema_sha256']==fingerprint(request['schema']),'RESERVATION_PAYLOAD_OR_PRICE_DRIFT')
    lease_path=Path(str(out)+'-supervision')/'worker-lease.json'
    require(Path(request['lease_path']).resolve()==lease_path and sha(lease_path)==request['lease_sha256'],'API_LEASE_DRIFT')
    lease=json.loads(lease_path.read_text())
    require(lease['start']==request['stage_start'] and lease['out']==str(out) and lease['mode']=='live','API_LEASE_SCOPE')
    require(request['parent_worker_pid']==(os.getppid() if parent_pid is None else parent_pid) and request['stage_pgid']==(os.getpgrp() if group is None else group)==request['parent_worker_pid'],'API_PARENT_GROUP_REQUIRED')
    return out


def claim_reservation(out,index,kind):
    claims=Path(out)/'api-claims';claims.mkdir(exist_ok=True)
    with (claims/(str(index)+'.json')).open('x') as f:
        json.dump(dict(kind=kind,reservation=index,at_monotonic=time.monotonic(),scope='One HTTP action for this reservation;no automatic reuse/refund'),f)


def action(root,execute_path,request_path,result_path):
    root=Path(root);reg=json.loads((root/'test2/configs/controller_done_bc_retest_v2.json').read_text());_,basis=authorize(root,reg,execute_path)
    request=json.loads(Path(request_path).read_text());require(request.get('kind')=='generation','REMOTE_COUNT_DISABLED')
    payload=request_payload(request['messages'],request['schema']);admission=estimate(payload)
    require(admission['value']<=64000,'LOCAL_ESTIMATE_OVER_TARGET_NO_DISPATCH')
    require(request.get('payload_sha256')==admission['payload_sha256'] and request.get('input_estimate')==admission,'REQUEST_ESTIMATE_OR_PAYLOAD_DRIFT')
    out=verify_reservation(root,reg,request,basis)
    ledger=json.loads((out/'ledger.json').read_text());event=ledger['events'][request['reservation_index']]
    require(event['context'].get('payload_sha256')==admission['payload_sha256'],'RESERVATION_PAYLOAD_DRIFT')
    remaining=min(120,request['deadline_monotonic']-time.monotonic());require(remaining>0.05,'API_DEADLINE_BEFORE_CREDENTIAL');claim_reservation(out,request['reservation_index'],'generation')
    key=root/'build/private/midterm-openai-key';require(key.is_file() and not key.is_symlink() and stat.S_IMODE(key.stat().st_mode)==0o600 and key.stat().st_size>0 and not key.parent.is_symlink() and stat.S_IMODE(key.parent.stat().st_mode)==0o700,'SECURE_STAGED_CREDENTIAL_REQUIRED')
    Path(str(result_path)+'.dispatch.json').write_text(json.dumps(dict(dispatch_attempted=True,kind='generation',actual_HTTP_issued='UNKNOWN_UNTIL_PROVIDER_RESPONSE',remote_count_requests=0))+'\n')
    try:
        data,status=post_json(payload,key.read_text().strip(),min(remaining,request['deadline_monotonic']-time.monotonic()))
        result=provider_result(data,status,admission)
    except (Halt,Exception) as error:
        result=dict(status='request_error',error_type=type(error).__name__,HTTP_status=error.status if isinstance(error,HTTPFailure) else None,usage=None,actual_cost_usd=None,request_issued='UNKNOWN_NOT_ZERO',remote_count_requests=0,error_message_omitted_to_protect_credentials=True)
    Path(result_path).write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);p.add_argument('--execute',required=True,type=Path);p.add_argument('--request',required=True,type=Path);p.add_argument('--result',required=True,type=Path);a=p.parse_args();action(a.root,a.execute,a.request,a.result)
