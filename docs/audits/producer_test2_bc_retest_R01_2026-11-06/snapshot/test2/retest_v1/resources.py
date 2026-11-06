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

def verified_pricing(record,reg,live=True):
    require(isinstance(record,dict),'COUNT_PRICE_UNKNOWN')
    if live:
        require(record.get('record_kind')=='BC_RETEST_VERIFIED_INCLUSIVE_API_PRICING' and record.get('status')=='VERIFIED','PRICING_NOT_VERIFIED')
        require(record.get('provider')=='OpenAI' and record.get('model')==reg['API']['model'],'PRICING_SERVICE_MISMATCH')
        require(record.get('coverage')=={'generation':True,'input_token_count':True} and bool(record.get('official_evidence')),'PRICING_COVERAGE_UNKNOWN')
    count=record.get('count_reserve_micro_usd');gen=record.get('generation_reserve_micro_usd')
    require(type(count) is int and count>=0,'COUNT_PRICE_UNKNOWN')
    require(type(gen) is int and gen==reg['billing']['generation_reserve_micro_usd'],'GEN_PRICE_UNKNOWN_OR_DRIFT')
    maximum=reg['API']['max_counts']*count+reg['API']['max_generations']*gen
    require(maximum<=reg['billing']['ceiling_micro_usd'],'FULL_STAGE_RESERVES_EXCEED_USD20')
    return dict(count=count,generation=gen,maximum_micro_usd=maximum)

class Window:
    def __init__(self,start,reg,clock=time.monotonic):
        self.start=start;self.clock=clock;self.work=start+reg['wall']['stop_work_seconds'];self.hard=start+reg['wall']['total_seconds']
    def remaining(self,cap):
        value=min(cap,self.work-self.clock());require(value>0.05,'WORK_DEADLINE_EXHAUSTED');return value
    def elapsed(self):return self.clock()-self.start

class Ledger:
    def __init__(self,path,reg,pricing,window,mode):
        self.path=Path(path);self.reg=reg;self.pricing=pricing;self.window=window;self.mode=mode
        self.state=dict(mode=mode,api_dispatch_attempts=0,api_provider_confirmed_requests=0,counts_reserved=0,generations_reserved=0,reserved_micro_usd=0,actual_invoice_usd=None,compile_calls=0,monitor_replays=0,monitor_cycles=0,events=[],halted=None,completed=False,start_monotonic=window.start,hard_deadline=window.hard,work_deadline=window.work)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.path.open('x') as f:json.dump(self.state,f);f.flush();os.fsync(f.fileno())
    def save(self):
        self.state['elapsed_checkpoint_seconds']=self.window.elapsed();p=self.path.with_suffix('.tmp')
        with p.open('x') as f:json.dump(self.state,f,indent=2);f.flush();os.fsync(f.fileno())
        os.replace(p,self.path)
    def halt(self,reason):
        self.state['halted']=self.state['halted'] or reason;self.save()
    def reserve_api(self,kind,context):
        require(not self.state['halted'],'HALTED');self.window.remaining(120)
        require(kind in ['count','generation'],'UNKNOWN_API_KIND')
        require(self.pricing is not None and type(self.pricing.get('count')) is int,'COUNT_PRICE_UNKNOWN')
        key='counts_reserved' if kind=='count' else 'generations_reserved';cap=self.reg['API']['max_counts' if kind=='count' else 'max_generations']
        require(self.state[key]<cap,'API_REQUEST_CAP:'+kind)
        amount=self.pricing[kind];require(self.state['reserved_micro_usd']+amount<=self.reg['billing']['ceiling_micro_usd'],'USD20_RESERVE_EXHAUSTED')
        self.state[key]+=1;self.state['reserved_micro_usd']+=amount
        event=dict(kind=kind,context=context,reserved_micro_usd=amount,status='RESERVED_BEFORE_DISPATCH',request_issued='UNKNOWN_UNTIL_DISPATCH_RECORD',usage=None,actual_cost_usd=None)
        self.state['events'].append(event);self.save();self.window.remaining(120);return len(self.state['events'])-1
    def dispatched(self,index):
        event=self.state['events'][index];event.update(dispatch_attempted=True,status='DISPATCH_ATTEMPTED',request_issued='UNKNOWN_ON_FAILURE' if self.mode=='live' else False,simulated=self.mode!='live')
        if self.mode=='live':self.state['api_dispatch_attempts']+=1
        self.save()
    def api_result(self,index,result):
        if self.mode=='live' and result.get('request_issued') is True:self.state['api_provider_confirmed_requests']+=1
        self.state['events'][index].update(status=result.get('status','UNKNOWN'),result=result,usage=result.get('usage'),actual_cost_usd=None);self.save()
    def reserve_local(self,kind,cycles=0):
        require(not self.state['halted'],'HALTED');cap=self.reg['local']['compile_timeout' if kind=='compile' else 'replay_timeout'];self.window.remaining(cap)
        key='compile_calls' if kind=='compile' else 'monitor_replays';limit=self.reg['local'][key]
        require(self.state[key]<limit,'LOCAL_COUNT_CAP:'+kind)
        require(type(cycles) is int and cycles>=0 and self.state['monitor_cycles']+cycles<=self.reg['local']['monitor_cycles'],'MONITOR_CYCLE_CAP')
        self.state[key]+=1;self.state['monitor_cycles']+=cycles;self.save();return self.window.remaining(cap)
    def finish(self):
        self.state['completed']=True;self.state['elapsed_before_terminal_save']=self.window.elapsed();self.save()
        require(self.window.clock()<=self.window.hard,'TOTAL_WALL_LIMIT_EXCEEDED')
