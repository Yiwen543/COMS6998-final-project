"""Inclusive API/local reservations and one monotonic stage window;no SDK."""
from pathlib import Path
import hashlib,json,os,time
class Halt(BaseException):
    """Fatal stage cancellation must escape legacy per-case except Exception."""
    pass
class Retryable(RuntimeError):
    def __init__(self,reason,record=None):
        super().__init__(reason);self.record=record


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def fingerprint(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def require(ok,reason):
    if not ok:raise Halt(reason)

def financial_policy(root,reg):
    root=Path(root)
    for key in ['financial_policy','method_addendum','cost_basis','original_authorization','user_zero_count_confirmation']:
        require(sha(root/reg[key])==reg[key+'_sha256'],'FINANCIAL_SOURCE_DRIFT:'+key)
    basis=json.loads((root/reg['cost_basis']).read_text());policy=json.loads((root/reg['financial_policy']).read_text());consent=json.loads((root/reg['user_zero_count_confirmation']).read_text())
    require(consent.get('record_kind')=='USER_EXPLICIT_ZERO_REMOTE_COUNT_METHOD_CONFIRMATION' and consent.get('remote_count_requests')==0 and consent.get('API_USD_hard_max')==20 and consent.get('requires_exact_code_preflight_and_EXECUTE') is True,'USER_ZERO_COUNT_CONFIRMATION_REQUIRED')
    require(basis.get('record_kind')=='BC_RETEST_ZERO_COUNT_VERIFIED_GENERATION_COST_BASIS' and basis.get('status')=='VERIFIED_METHOD_NOT_EXECUTE','VERIFIED_COST_BASIS_REQUIRED')
    require(basis['remote_count_requests_max']==policy['remote_count_requests_max']==reg['API']['max_counts']==0,'REMOTE_COUNT_DISABLED')
    require(basis['per_dispatch_full_context_reserve_micro_usd']==policy['per_dispatch_full_context_reserve_micro_USD']==reg['billing']['per_dispatch_reserve_micro_usd']==5910168,'FULL_CONTEXT_RESERVE_DRIFT')
    require(basis['API_ceiling_micro_usd']==reg['billing']['ceiling_micro_usd']==20000000 and basis['max_generation_attempts']==reg['API']['max_generations']==12,'FINANCIAL_HARD_CAP_DRIFT')
    require(basis['model']==reg['API']['model']=='gpt-6.1-sol' and basis['service_tier']==reg['API']['service_tier']=='default' and basis['reasoning_effort']=='low' and basis['output_tokens_max']==8192,'MODEL_PRICE_SCOPE_DRIFT')
    require(basis['prompt_cache_options']=={'mode':'implicit','ttl':'30m'} and basis['automatic_retries']==0 and basis['provider_tools']==[] and basis['server_context_tokens_bound']==1050000,'FEE_ASSUMPTION_DRIFT')
    require(basis['rates_USD_per_million']['long_context_max_input']==5 and basis['rates_USD_per_million']['long_context_max_output']==15 and basis['regional_uplift_multiplier_used']==1.1,'SETTLEMENT_RATE_DRIFT')
    return dict(generation=5910168,input_times10=55,output_times10=165,ceiling=20000000)

def trusted_success(record):
    require(record.get('provider_status')=='completed','INCOMPLETE_RESPONSE_KEEP_FULL_RESERVE')
    require(record.get('returned_model')=='gpt-6.1-sol' and record.get('returned_service_tier') in [None,'default'],'MODEL_OR_TIER_CONTRACT')
    require(record.get('long_cache_write') is False and record.get('unexpected_output_type') is False,'CACHE_OR_TOOL_CONTRACT')
    usage=record.get('usage') or {}
    require(all(type(usage.get(k)) is int and usage[k]>=0 for k in ['input_tokens','output_tokens','total_tokens']),'USAGE_UNKNOWN_KEEP_FULL_RESERVE')
    require(0<usage['input_tokens']<=64000,'ACTUAL_INPUT_OVER_TARGET_OR_INVALID_NOT_QUALIFIED')
    require(usage['output_tokens']<=8192 and usage['total_tokens']==usage['input_tokens']+usage['output_tokens'],'ACTUAL_OUTPUT_OR_USAGE_CONTRACT')
    for field,total in [('cached_input_tokens','input_tokens'),('reasoning_output_tokens','output_tokens')]:
        value=usage.get(field);require(value is None or type(value) is int and 0<=value<=usage[total],'USAGE_SUBSET_CONTRACT')
    try:parsed=json.loads(record['output_text'])
    except (ValueError,KeyError,TypeError):raise Halt('INVALID_JSON_KEEP_FULL_RESERVE') from None
    require(isinstance(parsed,dict),'RESPONSE_SCHEMA_KEEP_FULL_RESERVE')
    return usage,parsed

class Window:
    def __init__(self,start,reg,clock=time.monotonic):
        self.start=start;self.clock=clock;self.work=start+reg['wall']['stop_work_seconds'];self.hard=start+reg['wall']['total_seconds']
    def remaining(self,cap):
        value=min(cap,self.work-self.clock());require(value>0.05,'WORK_DEADLINE_EXHAUSTED');return value
    def elapsed(self):return self.clock()-self.start

class Ledger:
    def __init__(self,path,reg,pricing,window,mode):
        self.path=Path(path);self.reg=reg;self.pricing=pricing;self.window=window;self.mode=mode
        self.state=dict(total_reservations_micro_usd=0,financial_commitment_micro_usd=0,settled_upper_micro_usd=0,unresolved_reservations_micro_usd=0,unused_reservation_released_micro_usd=0,journal=[],mode=mode,api_dispatch_attempts=0,api_provider_confirmed_requests=0,counts_reserved=0,generations_reserved=0,actual_invoice_usd=None,compile_calls=0,monitor_replays=0,monitor_cycles=0,events=[],halted=None,completed=False,start_monotonic=window.start,hard_deadline=window.hard,work_deadline=window.work)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open('x') as f:json.dump(self.state,f);f.flush();os.fsync(f.fileno())
    def save(self):
        self.state['elapsed_checkpoint_seconds']=self.window.elapsed();p=self.path.with_suffix('.tmp')
        with p.open('x') as f:json.dump(self.state,f,indent=2);f.flush();os.fsync(f.fileno())
        os.replace(p,self.path)
    def halt(self,reason):
        self.state['halted']=self.state['halted'] or reason;self.save()
    def reserve_api(self,kind,context):
        require(kind=='generation','REMOTE_COUNT_DISABLED')
        require(not self.state['halted'],'HALTED');self.window.remaining(120)
        require(self.pricing is not None and self.pricing.get('generation')==5910168,'FULL_CONTEXT_RESERVE_REQUIRED')
        require(self.state['generations_reserved']<12,'API_REQUEST_CAP:generation')
        committed=sum(e['commitment_micro_usd'] for e in self.state['events'])
        require(committed==self.state['financial_commitment_micro_usd'],'FINANCIAL_LEDGER_INVARIANT')
        require(committed+5910168<=20000000,'USD20_PRE_DISPATCH_REFUSAL')
        self.state['generations_reserved']+=1;self.state['total_reservations_micro_usd']+=5910168;self.state['financial_commitment_micro_usd']+=5910168;self.state['unresolved_reservations_micro_usd']+=5910168
        event=dict(kind=kind,context=context,reserved_micro_usd=5910168,commitment_micro_usd=5910168,settled_upper_micro_usd=None,unused_reservation_released_micro_usd=None,status='RESERVED_BEFORE_DISPATCH',request_issued='UNKNOWN_UNTIL_DISPATCH_RECORD',usage=None,actual_cost_usd=None)
        self.state['events'].append(event);index=len(self.state['events'])-1
        self.state['journal'].append(dict(op='RESERVE',index=index,micro_usd=5910168,not_invoice=True));self.save();self.window.remaining(120);return index
    def dispatched(self,index):
        event=self.state['events'][index];event.update(dispatch_attempted=True,status='DISPATCH_ATTEMPTED',request_issued='UNKNOWN_ON_FAILURE' if self.mode=='live' else False,simulated=self.mode!='live')
        if self.mode=='live':self.state['api_dispatch_attempts']+=1
        self.save()
    def api_result(self,index,result):
        if self.mode=='live' and result.get('request_issued') is True:self.state['api_provider_confirmed_requests']+=1
        self.state['events'][index].update(status=result.get('status','UNKNOWN'),result=result,usage=result.get('usage'),actual_cost_usd=None);self.save()
    def settle(self,index,record):
        usage,_=trusted_success(record);event=self.state['events'][index]
        require(event['settled_upper_micro_usd'] is None and event['commitment_micro_usd']==5910168,'DUPLICATE_OR_INVALID_SETTLEMENT')
        upper=(55*usage['input_tokens']+165*usage['output_tokens']+9)//10;require(upper<=5910168,'SETTLEMENT_EXCEEDS_RESERVE')
        released=5910168-upper;event.update(settled_upper_micro_usd=upper,unused_reservation_released_micro_usd=released,commitment_micro_usd=upper,settlement_kind='CONSERVATIVE_USAGE_UPPER_NOT_INVOICE',usage_subsets_may_remain_UNKNOWN=True)
        self.state['settled_upper_micro_usd']+=upper;self.state['unresolved_reservations_micro_usd']-=5910168;self.state['financial_commitment_micro_usd']-=released;self.state['unused_reservation_released_micro_usd']+=released
        self.state['journal'].append(dict(op='SETTLE_UPPER_AND_RELEASE_UNUSED',index=index,reservation_micro_usd=5910168,settled_upper_micro_usd=upper,unused_reservation_released_micro_usd=released,not_refund_or_invoice=True))
        require(sum(e['commitment_micro_usd'] for e in self.state['events'])==self.state['financial_commitment_micro_usd'],'SETTLEMENT_LEDGER_INVARIANT');self.save();return upper

    def reserve_local(self,kind,cycles=0):
        require(not self.state['halted'],'HALTED');cap=self.reg['local']['compile_timeout' if kind=='compile' else 'replay_timeout'];self.window.remaining(cap)
        key='compile_calls' if kind=='compile' else 'monitor_replays';limit=self.reg['local'][key]
        require(self.state[key]<limit,'LOCAL_COUNT_CAP:'+kind)
        require(type(cycles) is int and cycles>=0 and self.state['monitor_cycles']+cycles<=self.reg['local']['monitor_cycles'],'MONITOR_CYCLE_CAP')
        self.state[key]+=1;self.state['monitor_cycles']+=cycles;self.save();return self.window.remaining(cap)
    def finish(self):
        self.state['completed']=True;self.state['elapsed_before_terminal_save']=self.window.elapsed();self.save()
        require(self.window.clock()<=self.window.hard,'TOTAL_WALL_LIMIT_EXCEEDED')
