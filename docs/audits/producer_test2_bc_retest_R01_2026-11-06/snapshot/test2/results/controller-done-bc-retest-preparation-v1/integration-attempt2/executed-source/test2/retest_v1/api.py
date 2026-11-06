"""Isolated SDK action. Gate/pricing precede any credential access or client."""
from pathlib import Path
import argparse,json,time
from resources import Halt,Retryable,require
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

def action(root,execute_path,request_path,result_path):
    root=Path(root);reg=json.loads((root/'test2/configs/controller_done_bc_retest_v1.json').read_text())
    authorize(root,reg,execute_path)  # fees/whole-stage/review/source must pass first
    request=json.loads(Path(request_path).read_text());remaining=min(120,request['deadline_monotonic']-time.monotonic());require(remaining>0.05,'API_DEADLINE_BEFORE_CREDENTIAL')
    require(request.get('kind') in ['count','generation'],'UNKNOWN_API_KIND')
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
