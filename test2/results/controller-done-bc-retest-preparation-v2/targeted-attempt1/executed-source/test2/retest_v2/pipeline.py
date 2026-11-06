"""Six-round old-benchmark retest adapter;shared old monitor ABI/grader unchanged."""
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
import gzip,json,os,sys,time,uuid
from resources import Halt,Retryable,Window,Ledger,require,sha,fingerprint
from release import freeze,release,verify,ARMS
from gates import authorize
from api import response_contract,request_payload,estimate
from supervision import child
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'test2/scripts'));sys.path.insert(0,str(ROOT/'scripts'))
import controller_done_generate_v2 as old
import controller_done_runtime as runtime
import controller_monitor_done as prototype
import controller_done_grade_v4 as grader
from controller_done_packet import NAMES

def load(p):return json.loads(Path(p).read_text())
def dump(p,x):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def append(p,x):
    with Path(p).open('a') as f:f.write(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n')
def clean_env(out):return dict(PATH='/opt/homebrew/bin:/usr/bin:/bin',LC_ALL='C',LANG='C',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(out/'tmp'))
def local_admissions():
    return {arm:estimate(request_payload(old.messages(arm,1),runtime.SCHEMA)) for arm in ARMS}


def mock_candidate():return dict(body="assign active=6'h3f;assign ok=6'h3f;",properties=[dict(id=f'P{i}',description='Mock plumbing,not an LLM trial or oracle') for i in range(6)])

class APIClient:
    def __init__(self,out,reg,ledger,window,mode,execute=None):self.out=out;self.reg=reg;self.ledger=ledger;self.window=window;self.mode=mode;self.execute=execute;self.last=None
    def call(self,kind,messages,context,directory):
        require(kind=='generation','REMOTE_COUNT_DISABLED');directory.mkdir(parents=True,exist_ok=False)
        admission=estimate(request_payload(messages,runtime.SCHEMA));dump(directory/'input-estimate.json',admission);require(admission['value']<=64000,'LOCAL_ESTIMATE_OVER_TARGET_NO_DISPATCH')
        index=self.ledger.reserve_api(kind,{**context,'messages_sha256':fingerprint(messages),'schema_sha256':fingerprint(runtime.SCHEMA),'payload_sha256':admission['payload_sha256'],'input_estimate':admission});self.ledger.dispatched(index);self.last_index=index
        if self.mode=='mock':
            n=1000
            result=dict(status='completed',provider_status='completed',returned_model='gpt-6.1-sol',returned_service_tier='default',output_text=json.dumps(mock_candidate()),usage=dict(input_tokens=n,output_tokens=25,total_tokens=n+25,cached_input_tokens=0,reasoning_output_tokens=0),long_cache_write=False,unexpected_output_type=False,input_estimate=admission)
            result['simulated_contract_fixture']=True
            dump(directory/'result.json',result)
        else:
            request=dict(kind='generation',messages=messages,schema=runtime.SCHEMA,payload_sha256=admission['payload_sha256'],input_estimate=admission,deadline_monotonic=self.window.work,stage_start=self.window.start,ledger_path=str(self.ledger.path.resolve()),reservation_index=index,parent_worker_pid=os.getpid(),stage_pgid=os.getpgrp(),lease_path=str(self.window.lease_path),lease_sha256=sha(self.window.lease_path))
            dump(directory/'request.json',request);result_path=directory/'result.json'
            cmd=[sys.executable,'-B',str(Path(__file__).parent/'api.py'),'--root',str(ROOT),'--execute',str(self.execute),'--request',str(directory/'request.json'),'--result',str(result_path)]
            try:process=child(cmd,directory/'child.log',120,self.window,clean_env(self.out))
            except Exception as error:
                self.ledger.halt('API_SUPERVISION_ERROR:'+type(error).__name__);raise Halt('API_SUPERVISION_ERROR') from None
            result=load(result_path) if result_path.is_file() else dict(status='request_error',usage=None,error_type='NO_API_RESULT',request_issued='UNKNOWN_NOT_ZERO')
            result['child_status']=process['status']
        self.ledger.api_result(index,result)
        if result['status']!='completed':raise Halt('HTTP_FAILURE_OR_UNKNOWN_USAGE_KEEP_FULL_RESERVE')
        return result
    def generate(self,messages,context,directory):
        record=self.call('generation',messages,context,directory)
        parsed=response_contract(record);self.ledger.settle(self.last_index,record)
        return record,parsed

class Tools:
    def __init__(self,out,ledger,window,mode):self.out=out;self.ledger=ledger;self.window=window;self.mode=mode
    def run(self,argv,log,timeout=60,cwd=ROOT):
        name=Path(str(argv[0])).name;require(name in ['yosys','iverilog','vvp'],'UNREGISTERED_LOCAL_TOOL')
        cycles=0
        if name=='vvp':
            rows=next(str(a)[6:] for a in argv if str(a).startswith('+ROWS='));cycles=len(Path(rows).read_text().splitlines())
        allowed=self.ledger.reserve_local('replay' if name=='vvp' else 'compile',cycles)
        if self.mode=='mock' or self.mode=='replay-mock':
            require(name=='vvp','FAKE_COMPILE_USES_EXPLICIT_STUB');text=''.join(f'MON {i} {phase} 111111 111111\n' for i in range(cycles) for phase in ['pre','post'] if i or phase=='post')+'REPLAY_COMPLETE\n';Path(log).write_text(text)
            return dict(argv=[str(x) for x in argv],returncode=0,status='complete',seconds=0.0,log_sha256=sha(log),fake_tool=True)
        try:return child(argv,log,min(timeout,allowed),self.window,clean_env(self.out))
        except Exception as error:
            self.ledger.halt('LOCAL_SUPERVISION_ERROR:'+type(error).__name__);raise Halt('LOCAL_SUPERVISION_ERROR') from None
    def compile(self,candidate,directory):
        if self.mode not in ['mock','replay-mock']:return prototype.compile_monitor(candidate,directory)
        source=prototype.old.validate(candidate).replace(prototype.old.HEADER,prototype.HEADER,1);directory.mkdir(parents=True,exist_ok=False);self.ledger.reserve_local('compile');(directory/'candidate.sv').write_text(source);dump(directory/'candidate.json',candidate)
        result=dict(status='complete',seconds=0.0,source_sha256=sha(directory/'candidate.sv'),mock_not_SV_compilation=True);dump(directory/'compile.json',result);return result
    def build(self,directory):
        if self.mode not in ['mock','replay-mock']:return prototype.build_replay(directory)
        self.ledger.reserve_local('compile');(directory/'replay.vvp').write_bytes(b'MOCK_NOT_EXECUTABLE');return dict(status='complete',seconds=0.0,mock_not_SV_compilation=True)
    @contextmanager
    def scope(self,reg):
        with patch.object(prototype,'run',self.run),patch.object(runtime,'run',self.run),patch.object(grader,'verify_release',lambda root:verify(root,reg)):
            yield

def develop(candidate,directory,tools):
    try:
        c=tools.compile(candidate,directory/'compiled')
        if c['status']!='complete':return dict(status='compile_error',log=(directory/'compiled/yosys.log').read_text()[-6000:])
        c=tools.build(directory/'compiled')
        if c['status']!='complete':return dict(status='compile_error',log='Replay compiler failed;raw log retained')
        feedback=dict(status='compiled',development={})
        for name in NAMES:
            rows=load(old.TASK/'measurements-v1/correct/verilator'/name/'rows.json');r=runtime.replay(directory/'compiled',rows,directory/name,tools.out/'development-row-cache')
            feedback['development'][name]=dict(complete=r['complete'],trace_done_sample=r['trace_done_sample'],properties=[dict(id=p['id'],checks=p['checks'],end_sample_checks=p['end_sample_checks'],failure_count=len(p['failures']),first_failures=p['failures'][:8],unknown_count=len(p['unknown']),first_unknown=p['unknown'][:8]) for p in r['properties']])
        return feedback
    except ValueError as error:return dict(status='invalid_candidate',reason=str(error))


def interrupted_grade(out,reg,reason):
    """Retain every planned case as unresolved if cancellation prevents grading."""
    labels=grader.inventory(load(old.TASK/'measurements-v1/summary.json')['records'])
    progress=load(out/'grade/progress.json').get('rounds',[]) if (out/'grade/progress.json').is_file() else []
    done={(r['arm'],r['repetition'],r['round']):r for r in progress};rounds=[]
    for snap in sorted(verify(out,reg),key=lambda r:(r['round'],r['repetition'],r['arm'])):
        key=(snap['arm'],snap['repetition'],snap['round'])
        if key in done:rounds.append(done[key]);continue
        cases=[grader.unresolved(label,'NOT_RUN_OR_UNRECORDED_AFTER_STAGE_HALT') for label in labels]
        rounds.append(dict(arm=key[0],repetition=key[1],round=key[2],candidate_status=snap['status'],**grader.summarize(cases),cases=cases))
    dump(out/'interrupted-grade.json',dict(status='INCOMPLETE_ALL_PLANNED_DENOMINATORS_RETAINED',reason=reason,rounds=rounds,planned_case_pairs=6*len(labels),remaining_not_pass=True,not_new_model_evidence=load(out/'run.json')['mode']!='live'))


def execute_stage(out,mode,reg,window,pricing=None,execute=None,replay_source=None,client_factory=APIClient):
    out=Path(out).resolve()
    if mode=='live':
        require(out.resolve()==(ROOT/reg['run_root']).resolve(),'LIVE_ROOT_DRIFT');_,pricing=authorize(ROOT,reg,execute)
        require(getattr(window,'lease_path',None) is not None,'SUPERVISED_WORKER_LEASE_REQUIRED')
    else:require(out.resolve()!=(ROOT/reg['run_root']).resolve(),'OFFLINE_MUST_NOT_CLAIM_LIVE_ROOT')
    old.verify_data();out.mkdir(parents=True,exist_ok=False);(out/'tmp').mkdir()
    ledger=Ledger(out/'ledger.json',reg,pricing,window,mode);tools=Tools(out,ledger,window,mode)
    client=client_factory(out,reg,ledger,window,mode,execute) if mode in ['live','mock'] else None
    saved={};source_mode=None
    if mode=='replay':
        verify(replay_source,reg);source_mode=load(replay_source/'run.json')['mode'];require(source_mode=='mock','OFFLINE_REPLAY_ONLY_FROM_MOCK_NO_EXTRA_LIVE_TOOLS');tools.mode='replay-mock'
        for row in map(json.loads,(replay_source/'calls.jsonl').read_text().splitlines()):
            if row.get('accepted_response'):saved[row['arm'],row['round']]=row
    states={a:dict(id=str(uuid.uuid4()),previous=None,feedback=None) for a in ARMS};snapshots=[]
    dump(out/'run.json',dict(mode=mode,benchmark='KNOWN_PUBLISHED_OLD_CORPUS_RETEST',registration_sha256=sha(ROOT/'test2/configs/controller_done_bc_retest_v2.json'),session_ids={a:s['id'] for a,s in states.items()},provider_tools=[],provider_history='Own last candidate/dev feedback only',not_new_model_evidence=mode!='live',replay_origin=str(replay_source) if replay_source else None))
    (out/'calls.jsonl').touch();scores=None;halt=None
    with tools.scope(reg):
        try:
            admissions=local_admissions();dump(out/'local-admissions.json',admissions)
            require(all(value['value']<=64000 for value in admissions.values()),'INITIAL_ESTIMATE_OVER_TARGET_NO_DISPATCH')
        except Halt as error:halt=type(error).__name__+':'+str(error);ledger.halt(halt)
        for arm,number in reg['schedule']:
            state=states[arm];ctx=dict(mode=mode,arm=arm,repetition=1,round=number,session_id=state['id']);d=out/arm/'rep1'/f'round{number}';d.mkdir(parents=True)
            prompt=old.messages(arm,number,state['previous'],state['feedback']);dump(d/'prompt.json',prompt);parsed=None
            if not halt:
                for attempt in range(1,3):
                    event_start=len(ledger.state['events']);row=dict(ctx,attempt=attempt,prompt_sha256=sha(d/'prompt.json'),accepted_response=False,generation_request_issued=False,count_request_issued=False)
                    try:
                        if mode=='replay':
                            original=saved.get((arm,number));require(original is not None and original['prompt_sha256']==sha(d/'prompt.json'),'REPLAY_PROMPT_OR_RESPONSE_MISSING');parsed=original['parsed'];row.update(status='replayed',original_usage=original.get('usage'),parsed=parsed)
                        else:
                            row['count_request_issued']=False;row['input_estimate']=estimate(request_payload(prompt,runtime.SCHEMA))
                            response,parsed=client.generate(prompt,ctx,d/f'attempt{attempt}'/'generation');row.update(response,parsed=parsed)
                        row['accepted_response']=parsed is not None
                    except Retryable as error:
                        row.update(error.record or {});row.update(status='retryable_failure',error=str(error),actual_cost_usd=None)
                        row.setdefault('usage',None)
                    except Halt as error:halt=type(error).__name__+':'+str(error);ledger.halt(halt);row.update(status='resource_or_contract_halt',error=halt,usage=None,actual_cost_usd=None)
                    events=ledger.state['events'][event_start:]
                    row['count_request_issued']=False
                    row['generation_request_issued']=mode=='live' and any(e['kind']=='generation' and e.get('dispatch_attempted') for e in events)
                    row['request_count_semantics']='Conservative explicit HTTP dispatch attempts;HTTP issuance/cost unknown on failures.'
                    append(out/'calls.jsonl',row)
                    if parsed is not None or halt or mode=='replay':break
            if halt:feedback=dict(status='NOT_RUN_OR_UNRESOLVED',reason=halt)
            elif parsed is None:feedback=dict(status='generation_unresolved')
            else:
                state['previous']=parsed
                try:feedback=develop(parsed,d,tools)
                except Halt as error:halt=type(error).__name__+':'+str(error);ledger.halt(halt);feedback=dict(status='LOCAL_RESOURCE_HALT',reason=halt)
            dump(d/'response.json',parsed);dump(d/'development-feedback.json',feedback);state['feedback']=feedback
            snapshots.append(freeze(out,d,ctx,feedback['status']))
        release(out,snapshots,mode,reg)
        if not halt:
            try:
                window.remaining(1);scores=grader.execute(out,out/'grade');require(len(scores['rounds'])==6,'SCORING_ROUNDS_MISSING')
            except Halt as error:halt=type(error).__name__+':'+str(error);ledger.halt(halt)
    if halt:
        if window.clock()<window.hard-5:interrupted_grade(out,reg,halt)
        else:dump(out/'grading-termination.json',dict(status='INCOMPLETE',planned_rounds=6,planned_case_pairs=972,unwritten_cases_remain_unresolved=True))
    ledger.finish();summary=dict(status='COMPLETE_WITH_UNRESOLVED_RETAINED' if scores is not None else 'INCOMPLETE_PRESERVED',halt=halt,mode=mode,not_new_model_evidence=mode!='live',snapshots=6,finals=2,actual_generation_tokens=None,actual_generation_usage_scope='Raw per-attempt ledger authoritative;ESTIMATE not fresh exact count;unknown usage never zero',actual_API_requests=0 if mode!='live' else None,confirmed_provider_responses=ledger.state['api_provider_confirmed_requests'],API_dispatch_attempts=ledger.state['api_dispatch_attempts'],request_reservations=dict(counts=ledger.state['counts_reserved'],generations=ledger.state['generations_reserved']),compile_calls=ledger.state['compile_calls'],monitor_replays=ledger.state['monitor_replays'],monitor_cycles=ledger.state['monitor_cycles'],remote_count_requests=0,input_admission='LOCAL_ESTIMATE_NOT_SERVER_HARD_CAP',financial_commitment_micro_usd=ledger.state['financial_commitment_micro_usd'],settled_upper_micro_usd=ledger.state['settled_upper_micro_usd'],unresolved_reservations_micro_usd=ledger.state['unresolved_reservations_micro_usd'],new_DUT_simulations=0,new_native_jobs=0,actual_invoice_usd=None,global_elapsed_seconds=window.elapsed(),old_results_overwritten=False)
    dump(out/'summary.json',summary)
    dump(out/'resource-release.json',dict(mode=mode,files={n:sha(out/n) for n in ['ledger.json','calls.jsonl','summary.json','release.json']},actual_invoice_usd=None,unknown_costs_never_zero=True))
    return summary
