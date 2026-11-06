#!/usr/bin/env python3
"""New trace_done own-history runner. No old runner or freeze is mutated."""
import argparse
import json
import os
from pathlib import Path
import random
import time
import uuid
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG,SOURCE_TASK
from controller_done_packet import NAMES
from controller_done_runtime import HEADER,SCHEMA,compile_monitor,build_replay,replay
from controller_release_live import ARMS,freeze_round,release,verify_release
from pilot_model import OpenAIModel,ModelResponseError

SYSTEM='''Generate a passive SystemVerilog monitor for the supplied frame_task contract.
Return strictJSON body plus exactly6properties P0..P5 with descriptions. The supplied
header includes readonly trace_done. It is0at everypre and everypost except finalpost1.
No rising edge follows this marker: finite-end checks must enable combinationally.
Do not drive inputs or use hierarchy/modules/assumptions/assert/cover/system calls.
Only private bounded state, combinational logic and posedge clk are supported.
Body cap16000UTF8bytes,state8192bits. Use active[j],ok[j]; active1ok0 is an alarm.
Check sound obligations on accepted inputs, presented valids, independent response
channels, reset and finite-end completion. Development tails use32,final tails128.
Unknown observations never establish successful checks. Internal/e-graph terms are
implementation facts, not specification truth or proof of sequential correctness.
You receive only your own last candidate/development feedback. Fixed raw coverage
cannot improve by editing a passive monitor. Hidden outcomes/reference are absent.'''
LIVE_FREEZE=BASE/'configs/controller_done_live_freeze_v1.json'
APPROVAL=BASE/'configs/controller_done_api_authorization_v1.json'


def load(p):return json.loads(Path(p).read_text())


def verify_data():
    reg=load(REG)
    for name,h in reg['sources'].items():
        if sha(ROOT/name)!=h:raise ValueError('DUT source changed')
    if sha(ROOT/reg['reference']['checker'])!=reg['reference']['sha256']:raise ValueError('Independent checker changed')
    ref=load(SOURCE_TASK/'reference/frozen-v2/freeze.json')
    for name,h in ref['artifact_sha256'].items():
        if sha(ROOT/name)!=h:raise ValueError('Reference bound artifact changed')
    f=load(TASK/'evaluation-freeze.json')
    if f['status']!='qualified':raise ValueError('Fresh physical baseline did not qualify')
    for name,h in f['files'].items():
        if sha(ROOT/name)!=h:raise ValueError('Fresh evaluation input changed: '+name)
    p=load(TASK/'public/prompt-packets-v1/audit.json')
    for name,h in p['packets'].items():
        if sha(TASK/'public/prompt-packets-v1'/(name+'.json'))!=h:raise ValueError('Public packet changed')
    return reg


def authorization(scope):
    if not APPROVAL.exists():raise ValueError('No separately approved API stage; live/count closed')
    a=load(APPROVAL)
    if not a.get('user_approved') or a.get('registration_sha256')!=sha(REG) or scope not in a.get('scopes',[]):raise ValueError('API stage not authorized for this registration/scope')
    return a


def live_gate():
    authorization('generation');verify_data()
    if not LIVE_FREEZE.exists():raise ValueError('New live freeze absent')
    f=load(LIVE_FREEZE)
    if not f.get('candidate_live_allowed') or not all(f['gates'].values()):raise ValueError('New live gates incomplete')
    for name,h in f['files'].items():
        if sha(ROOT/name)!=h:raise ValueError('New live input changed')
    return f


def model(reg):
    p=ROOT/'build/private/midterm-openai-key'
    if not p.is_file() or p.stat().st_mode&0o077:raise ValueError('Secure staged OpenAI key missing')
    old=os.environ.get('OPENAI_API_KEY');os.environ['OPENAI_API_KEY']=p.read_text().strip();b=reg['budget']
    try:return OpenAIModel(dict(model=b['model'],reasoning_effort=b['reasoning_effort'],timeout_seconds=b['request_timeout_seconds'],max_output_tokens=b['output_tokens']),SCHEMA,'controller_done_monitor')
    finally:
        if old is None:os.environ.pop('OPENAI_API_KEY',None)
        else:os.environ['OPENAI_API_KEY']=old


def messages(arm,number,previous=None,feedback=None):
    data=load(TASK/'public/prompt-packets-v1'/(arm+'.json'))
    data.update(module_header=HEADER,round=number,previous_candidate=previous,development_feedback=feedback)
    return [dict(role='system',content=SYSTEM),dict(role='user',content=json.dumps(data,sort_keys=True,separators=(',',':')))]


def plumbing(n):
    body="assign active=6'b111111;assign ok=6'b111111;"
    if n==1:body='assign active=63;assign ok=0;'
    elif n==2:body='assign active=0;assign ok=63;'
    elif n==6:body='''reg [15:0] offered, data_frames, status_frames;
always @(posedge clk) begin
 if (rst) begin offered<=0;data_frames<=0;status_frames<=0;end
 else begin
  if(s_valid && s_ready && s_last) offered<=offered+16'd1;
  if(m_valid && m_ready && m_last) data_frames<=data_frames+16'd1;
  if(h_valid && h_ready) status_frames<=status_frames+16'd1;
 end
end
assign active={3'b000,{3{trace_done}}};
assign ok={3'b111,(status_frames>=offered),(data_frames>=offered),(!s_valid)};'''
    return dict(body=body,properties=[dict(id=f'P{i}',description='Arm-blind infrastructure plumbing only; not an LLM trial or oracle') for i in range(6)])


def develop(candidate,directory,cache):
    start=time.perf_counter();calls=0;cycles=0;compile_secs=0.;replay_secs=0.
    try:
        calls+=1;c=compile_monitor(candidate,directory/'compiled');compile_secs+=c['seconds']
        if c['status']!='complete':
            text=(directory/'compiled/yosys.log').read_text().replace(str(directory),'ROUND_DIR')
            feedback=dict(status='compile_error',log='\n'.join(x for x in text.splitlines() if any(w in x.lower() for w in ('error','warning','syntax')))[-6000:])
        else:
            calls+=1;r=build_replay(directory/'compiled');compile_secs+=r['seconds']
            if r['status']!='complete':feedback=dict(status='compile_error',log='Replay compiler failed; raw log retained')
            else:
                feedback=dict(status='compiled',development={})
                for name in NAMES:
                    rows=load(TASK/'measurements-v1/correct/verilator'/name/'rows.json');r=replay(directory/'compiled',rows,directory/name,cache)
                    cycles+=r['cycles'];replay_secs+=r['execution']['seconds']
                    feedback['development'][name]=dict(complete=r['complete'],trace_done_sample=r['trace_done_sample'],properties=[dict(id=p['id'],checks=p['checks'],end_sample_checks=p['end_sample_checks'],failure_count=len(p['failures']),first_failures=p['failures'][:8],unknown_count=len(p['unknown']),first_unknown=p['unknown'][:8]) for p in r['properties']])
    except ValueError as error:feedback=dict(status='invalid_candidate',reason=str(error))
    except Exception as error:feedback=dict(status='infrastructure_error',error_type=type(error).__name__)
    cost=dict(compilation_tool_invocations=calls,compile_seconds=compile_secs,monitor_replays=len(feedback.get('development',{})),replayed_cycles=cycles,replay_seconds=replay_secs,wall_seconds=time.perf_counter()-start)
    dump(directory/'development-feedback.json',feedback);dump(directory/'development-cost.json',cost);return feedback,cost


def append(path,row):
    with path.open('a') as f:f.write(json.dumps(row,sort_keys=True,separators=(',',':'))+'\n')


def execute(mode,out,replay_source=None):
    reg=verify_data()
    if mode=='live':live_gate()
    out.mkdir(parents=True,exist_ok=False);client=model(reg) if mode=='live' else None;saved={}
    if mode=='replay':
        verify_release(replay_source)
        for line in (replay_source/'calls.jsonl').read_text().splitlines():
            r=json.loads(line)
            if r.get('accepted_response'):saved[r['arm'],r['repetition'],r['round']]=r
    states={(a,r):dict(id=str(uuid.uuid4()),previous=None,feedback=None) for a in ARMS for r in (1,2,3)}
    dump(out/'run.json',dict(mode=mode,registration_sha256=sha(REG),data_freeze_sha256=sha(TASK/'evaluation-freeze.json'),runner_sha256=sha(__file__),session_ids={f'{a}/{r}':s['id'] for (a,r),s in states.items()},provider_tools=[],provider_history='Own last candidate/public development only',replay_origin=str(replay_source) if replay_source else None,trace_done='finalpostonly'))
    (out/'calls.jsonl').touch();snapshots=[];costs=[];start=time.perf_counter()
    for number in range(1,7):
        for rep in (1,2,3):
            for arm in (ARMS if (number+rep)%2==0 else tuple(reversed(ARMS))):
                if mode=='live':live_gate()
                state=states[arm,rep];ctx=dict(mode=mode,arm=arm,repetition=rep,round=number,session_id=state['id'])
                d=out/arm/f'rep{rep}'/f'round{number}';d.mkdir(parents=True)
                prompt=messages(arm,number,state['previous'],state['feedback']);dump(d/'prompt.json',prompt);parsed=None
                for attempt in range(2 if mode=='live' else 1):
                    row=dict(ctx,attempt=attempt+1,prompt_sha256=sha(d/'prompt.json'),generation_request_issued=False,count_request_issued=False,accepted_response=False)
                    try:
                        if mode=='live':
                            row['count_request_issued']=True;row['input_token_count']=client.count_input_tokens(prompt)
                            if row['input_token_count']>reg['budget']['input_tokens']:
                                row['status']='input_cap_exceeded_no_generation';append(out/'calls.jsonl',row);break
                            row['generation_request_issued']=True;row.update(client.generate(prompt,ctx));parsed=row['parsed']
                        elif mode=='mock':parsed=plumbing(number);row.update(parsed=parsed,usage=None,status='completed',requested_model='mock-plumbing',returned_model='mock-plumbing')
                        else:
                            old=saved.get((arm,rep,number))
                            if old is None:row['status']='replayed_unresolved'
                            else:
                                if old['prompt_sha256']!=sha(d/'prompt.json'):raise ValueError('Saved prompt/own-history mismatch')
                                parsed=old['parsed'];row.update(parsed=parsed,usage=None,original_usage=old.get('usage'),status='completed')
                        row['accepted_response']=parsed is not None
                    except ModelResponseError as error:row.update(error.record,status='model_response_error',error_type=error.reason)
                    except Exception as error:
                        if mode!='live':raise
                        row.update(status='request_or_infrastructure_error',error_type=type(error).__name__)
                    append(out/'calls.jsonl',row)
                    if parsed is not None or mode!='live':break
                dump(d/'response.json',parsed)
                if parsed is None:
                    feedback=dict(status='generation_unresolved');cost=dict(compilation_tool_invocations=0,monitor_replays=0,replayed_cycles=0,replay_seconds=0,compile_seconds=0,wall_seconds=0)
                    dump(d/'development-feedback.json',feedback);dump(d/'development-cost.json',cost)
                else:state['previous']=parsed;feedback,cost=develop(parsed,d,out/'development-row-cache')
                state['feedback']=feedback;costs.append(cost);snapshots.append(freeze_round(out,d,ctx,feedback['status']))
                print(mode,arm,rep,number,feedback['status'],flush=True)
    release(out,snapshots,mode);records=[json.loads(x) for x in (out/'calls.jsonl').read_text().splitlines()]
    summary=dict(mode=mode,frozen_rounds=len(snapshots),generation_requests=sum(r['generation_request_issued'] for r in records),count_requests=sum(r['count_request_issued'] for r in records),wall_seconds=time.perf_counter()-start,compiled_invocations=sum(c['compilation_tool_invocations'] for c in costs),monitor_replays=sum(c['monitor_replays'] for c in costs),replayed_cycles=sum(c['replayed_cycles'] for c in costs),new_DUT_simulations=0,hidden_scoring_started=False,not_new_model_evidence=mode!='live')
    dump(out/'summary.json',summary);return summary


def count_messages():
    rng=random.Random(699856)
    body='assign active=63;assign ok=63;';body+='/*'+''.join(rng.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(16000-len(body)-4))+'*/'
    previous=dict(body=body,properties=[dict(id=f'P{i}',description=''.join(rng.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(400))) for i in range(6)])
    feedback=dict(status='compile_error',log=''.join(rng.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(18000)))
    return [(arm,kind,msg) for arm in ARMS for kind,msg in [('initial',messages(arm,1)),('history_probe',messages(arm,6,previous,feedback))]]


def count(out):
    authorization('token_count');reg=verify_data();out.mkdir(parents=True,exist_ok=False);client=model(reg);records=[]
    # Four requests only, with failures recorded; no silent retry or generation.
    for arm,kind,msg in count_messages():
        p=out/(arm+'-'+kind+'.json');dump(p,msg);start=time.perf_counter();r=dict(arm=arm,kind=kind,count_request_issued=True,generation_request_issued=False,prompt_sha256=sha(p))
        try:
            n=client.count_input_tokens(msg);r.update(input_tokens=n,within_cap=n<=64000,status='completed')
        except Exception as error:r.update(input_tokens=None,within_cap=False,status='count_unresolved',error_type=type(error).__name__)
        r['seconds']=time.perf_counter()-start;records.append(r);dump(out/'partial.json',records)
    dump(out/'summary.json',dict(status='passed' if all(r['within_cap'] for r in records) else 'input_cap_exceeded',counts=records,count_requests=4,generation_requests=0,registration_sha256=sha(REG)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['mock','replay','live','count'],required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--replay-source',type=Path);a=p.parse_args()
    if a.mode=='count':count(a.output.resolve())
    else:execute(a.mode,a.output.resolve(),a.replay_source.resolve() if a.replay_source else None)
