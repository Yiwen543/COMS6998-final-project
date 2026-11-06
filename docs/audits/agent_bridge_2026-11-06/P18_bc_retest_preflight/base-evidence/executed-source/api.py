"""Isolated SDK action. Gate/pricing precede any credential access or client."""
from pathlib import Path
import argparse,json,time,os
from resources import Halt,Retryable,require,sha,fingerprint
from gates import authorize

def response_contract(record,expected):
    require(record.get('returned_model')=='gpt-6.1-sol' and record.get('returned_service_tier') in [None,'default'],'MODEL_OR_TIER_CONTRACT')
    usage=record.get('usage') or {}
    require(all(type(usage.get(k)) is int and usage[k]>=0 for k in ['input_tokens','output_tokens','total_tokens']),'USAGE_UNKNOWN_NOT_ZERO')
    require(usage['input_tokens']==expected and expected<=64000 and usage['output_tokens']<=8192 and usage['total_tokens']==expected+usage['output_tokens'],'ACTUAL_TOKEN_BUDGET_OR_COUNT_MISMATCH')
    for sub,total in [('cached_input_tokens','input_tokens'),('reasoning_output_tokens','output_tokens')]:
        value=usage.get(sub);require(value is None or type(value) is int and 0<=value<=usage[total],'USAGE_SUBSET_CONTRACT')
    require(not record.get('long_cache_write'),'UNEXPECTED_12H_CACHE')
    if record.get('provider_status')!='completed':raise Retryable('INCOMPLETE_RESPONSE',record)
    try:value=json.loads(record['output_text'])
    except (ValueError,KeyError,TypeError):raise Retryable('INVALID_RESPONSE_JSON',record) from None
    return value

def verify_reservation(root,reg,request,pricing,clock=time.monotonic,parent_pid=None,group=None):
    """SDK work cannot bypass the single live ledger and supervised worker lease."""
    root=Path(root);out=(root/reg['run_root']).resolve();ledger_path=out/'ledger.json'
    require(Path(request['ledger_path']).resolve()==ledger_path,'WRONG_LIVE_LEDGER')
    require(ledger_path.is_file() and not ledger_path.is_symlink(),'LIVE_LEDGER_REQUIRED');ledger=json.loads(ledger_path.read_text())
    require(ledger['mode']=='live' and not ledger['completed'] and not ledger['halted'],'LIVE_LEDGER_NOT_ACTIVE')
    require(ledger['start_monotonic']==request['stage_start'] and ledger['work_deadline']==request['deadline_monotonic']==request['stage_start']+reg['wall']['stop_work_seconds'],'STAGE_CLOCK_DRIFT')
    require(clock()<ledger['work_deadline'] and ledger['hard_deadline']==request['stage_start']+3600,'STAGE_EXPIRED')
    require(ledger['counts_reserved']<=16 and ledger['generations_reserved']<=12 and ledger['reserved_micro_usd']<=20000000,'LEDGER_LIMIT_DRIFT')
    require(type(request['reservation_index']) is int and 0<=request['reservation_index']<len(ledger['events']),'RESERVATION_REQUIRED')
    event=ledger['events'][request['reservation_index']]
    require(event['kind']==request['kind'] and event.get('dispatch_attempted') is True and event['status']=='DISPATCH_ATTEMPTED','OPEN_RESERVATION_REQUIRED')
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
        json.dump(dict(kind=kind,reservation=index,at_monotonic=time.monotonic(),scope='One SDK action for this reservation;no automatic reuse/refund'),f)


def action(root,execute_path,request_path,result_path):
    root=Path(root);reg=json.loads((root/'test2/configs/controller_done_bc_retest_v1.json').read_text())
    _,pricing=authorize(root,reg,execute_path)  # fees/review/source before credential
    request=json.loads(Path(request_path).read_text());remaining=min(120,request['deadline_monotonic']-time.monotonic());require(remaining>0.05,'API_DEADLINE_BEFORE_CREDENTIAL')
    require(request.get('kind') in ['count','generation'],'UNKNOWN_API_KIND')
    out=verify_reservation(root,reg,request,pricing);claim_reservation(out,request['reservation_index'],request['kind'])
    key=root/'build/private/midterm-openai-key'
    require(key.is_file() and not key.is_symlink() and key.stat().st_mode&0o077==0,'SECURE_STAGED_CREDENTIAL_REQUIRED')
    from openai import OpenAI
    try:client=OpenAI(api_key=key.read_text().strip(),base_url='https://api.openai.com/v1',timeout=remaining,max_retries=0)
    except Exception as error:
        Path(result_path).write_text(json.dumps(dict(status='client_error',error_type=type(error).__name__,request_issued=False,usage=None,actual_cost_usd=None))+'\n');return
    config=reg['API'];params=dict(model=config['model'],input=request['messages'],reasoning=dict(effort='low'),text=dict(format=dict(type='json_schema',name='controller_done_monitor',strict=True,schema=request['schema'])))
    marker=Path(str(result_path)+'.dispatch.json');marker.write_text(json.dumps(dict(dispatch_attempted=True,kind=request['kind'],actual_HTTP_issued='UNKNOWN_UNTIL_PROVIDER_RESPONSE'))+'\n')
    try:
        if request['kind']=='count':
            response=client.responses.input_tokens.count(**params);result=dict(status='completed',input_tokens=response.input_tokens,request_issued=True)
        else:
            response=client.responses.create(**params,store=False,max_output_tokens=8192,service_tier='default',prompt_cache_options=dict(mode='implicit',ttl='30m'))
            raw=response.usage.model_dump() if response.usage is not None else {};details=raw.get('input_tokens_details') or {};output=raw.get('output_tokens_details') or {}
            result=dict(status='completed',provider_status=response.status,returned_model=response.model,returned_service_tier=getattr(response,'service_tier',None),response_id=response.id,output_text=response.output_text,usage=dict(input_tokens=raw.get('input_tokens'),output_tokens=raw.get('output_tokens'),total_tokens=raw.get('total_tokens'),cached_input_tokens=details.get('cached_tokens'),reasoning_output_tokens=output.get('reasoning_tokens')),raw_usage=raw,long_cache_write=bool((details.get('cache_write_tokens_details') or {}).get('ttl_12h_tokens')),request_issued=True)
    except Exception as error:result=dict(status='request_error',error_type=type(error).__name__,usage=None,actual_cost_usd=None,request_issued='UNKNOWN_NOT_ZERO')
    Path(result_path).write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);p.add_argument('--execute',required=True,type=Path);p.add_argument('--request',required=True,type=Path);p.add_argument('--result',required=True,type=Path);a=p.parse_args();action(a.root,a.execute,a.request,a.result)
