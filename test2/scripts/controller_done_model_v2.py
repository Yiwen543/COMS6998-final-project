"""Bounded stateless candidate API adapter; no calls without the runner's live grant."""
import hashlib
import json
import time
from common import ROOT
from pilot_model import ModelResponseError,usage_record

MAX_GENERATIONS=72
MAX_COUNTS=72
RESERVE_PER_GENERATION=0.24192  #64k*USD2.5/M short-cache write +8192*USD10/M output


def fingerprint(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


class BoundedModel:
    def __init__(self,config,schema,schema_name,ledger,client=None,max_generations=MAX_GENERATIONS,max_counts=MAX_COUNTS):
        if config.get('model')!='gpt-6.1-sol' or config.get('reasoning_effort')!='low' or config.get('timeout_seconds')!=120 or config.get('max_output_tokens')!=8192:raise ValueError('Registered model settings changed')
        if not 1<=max_generations<=MAX_GENERATIONS or not 1<=max_counts<=MAX_COUNTS:raise ValueError('Invalid local request caps')
        self.config=config;self.schema=schema;self.schema_name=schema_name;self.ledger=ledger;self.max_generations=max_generations;self.max_counts=max_counts
        self.last_count=None;self.halted=None
        self.events=[json.loads(s) for s in ledger.read_text().splitlines() if s.strip()] if ledger.exists() else []
        if any(e['event']=='resource_halt' for e in self.events):self.halted='Previous resource halt'
        if client is None:
            from openai import OpenAI
            key=ROOT/'build/private/midterm-openai-key'
            if not key.is_file() or key.stat().st_mode&0o077:raise ValueError('Secure staged OpenAI credential missing')
            client=OpenAI(api_key=key.read_text().strip(),base_url='https://api.openai.com/v1',timeout=config['timeout_seconds'],max_retries=0)
        self.client=client

    def record(self,event,**values):
        row=dict(event=event,**values);self.events.append(row);self.ledger.parent.mkdir(parents=True,exist_ok=True)
        with self.ledger.open('a') as stream:stream.write(json.dumps(row,sort_keys=True,separators=(',',':'))+'\n')

    def dispatched(self):
        return dict(counts=sum(e['event']=='count_dispatched' for e in self.events),generations=sum(e['event']=='generation_dispatched' for e in self.events))

    def halt(self,reason,record=None):
        self.halted=reason;self.record('resource_halt',reason=reason)
        if record is not None:raise ModelResponseError(reason,record)
        raise ValueError(reason)

    def format(self):return dict(format=dict(type='json_schema',name=self.schema_name,strict=True,schema=self.schema))

    def count_input_tokens(self,messages):
        self.last_count=None
        if self.halted:raise ValueError('Resource halt active')
        if self.dispatched()['counts']>=self.max_counts:self.halt('count_quota_exhausted')
        digest=fingerprint(messages);self.record('count_dispatched',messages_sha256=digest,model=self.config['model'],schema_sha256=fingerprint(self.schema))
        try:
            result=self.client.responses.input_tokens.count(model=self.config['model'],input=messages,reasoning=dict(effort=self.config['reasoning_effort']),text=self.format())
        except Exception as error:self.record('count_error',error_type=type(error).__name__);raise
        n=result.input_tokens
        if type(n)!=int or n<=0:self.halt('invalid_provider_input_count')
        self.last_count=(digest,n);self.record('count_returned',messages_sha256=digest,input_tokens=n);return n

    def generate(self,messages,context):
        if self.halted:raise ValueError('Resource halt active')
        digest=fingerprint(messages)
        if self.last_count is None or self.last_count[0]!=digest:self.halt('generation_without_matching_precount')
        expected=self.last_count[1];self.last_count=None
        if expected>64000:self.halt('input_cap_exceeded_before_generation')
        if self.dispatched()['generations']>=self.max_generations:self.halt('generation_quota_exhausted')
        reserved=(self.dispatched()['generations']+1)*RESERVE_PER_GENERATION
        if reserved>17.5:self.halt('generation_USD_reserve_exhausted')
        self.record('generation_dispatched',messages_sha256=digest,input_tokens_counted=expected,max_output_tokens=8192,requested_service_tier='default',
            reserve_usd=RESERVE_PER_GENERATION,cumulative_reserve_usd=reserved,context=context)
        start=time.perf_counter()
        try:
            response=self.client.responses.create(model=self.config['model'],input=messages,store=False,max_output_tokens=8192,
                reasoning=dict(effort=self.config['reasoning_effort']),text=self.format(),service_tier='default',prompt_cache_options=dict(mode='implicit',ttl='30m'))
        except Exception as error:self.record('generation_error',error_type=type(error).__name__,usage_status='UNKNOWN_NOT_ZERO');raise
        usage=usage_record(response.usage);raw_usage=response.usage.model_dump() if hasattr(response.usage,'model_dump') else response.usage
        record=dict(requested_model=self.config['model'],returned_model=response.model,response_id=response.id,latency_seconds=time.perf_counter()-start,
            status=response.status,incomplete_details=str(response.incomplete_details) if response.incomplete_details else None,
            usage=usage,raw_usage=raw_usage,output_text=response.output_text,requested_service_tier='default',returned_service_tier=getattr(response,'service_tier',None),input_token_count=expected)
        self.record('generation_returned',response_id=response.id,usage=usage,returned_model=response.model,returned_service_tier=record['returned_service_tier'])
        if response.model!=self.config['model']:self.halt('returned_model_mismatch',record)
        if record['returned_service_tier'] not in (None,'default'):self.halt('returned_service_tier_mismatch',record)
        if any(type(usage[k])!=int or usage[k]<0 for k in ('input_tokens','output_tokens','total_tokens')):self.halt('usage_missing_or_invalid',record)
        if usage['input_tokens']!=expected or usage['input_tokens']>64000 or usage['output_tokens']>8192 or usage['total_tokens']!=usage['input_tokens']+usage['output_tokens']:self.halt('actual_token_budget_or_count_mismatch',record)
        for detail,total in [('cached_input_tokens','input_tokens'),('reasoning_output_tokens','output_tokens')]:
            value=usage[detail]
            if value is not None and (type(value)!=int or not 0<=value<=usage[total]):self.halt('invalid_usage_subset',record)
        details=(raw_usage or {}).get('input_tokens_details') or {}
        writes=details.get('cache_write_tokens_details') or {}
        if isinstance(writes,dict) and writes.get('ttl_12h_tokens'):self.halt('unexpected_long_cache_write',record)
        if response.status!='completed':raise ModelResponseError('incomplete_response',record)
        try:record['parsed']=json.loads(response.output_text)
        except (TypeError,ValueError):raise ModelResponseError('invalid_json',record) from None
        return record
