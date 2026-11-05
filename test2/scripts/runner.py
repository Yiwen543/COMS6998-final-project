#!/usr/bin/env python3
"""B'/C' development loop. Fixed traces only; final scoring is a separate release.

Mock/replay are offline. Live requires a reviewed reference and explicit live freeze.
This file does not open held-out stimuli, mutants, or reference code for prompts.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import uuid
from common import BASE, ROOT, dump, sha
from feedback import messages
from monitor import SCHEMA, validate, compile_monitor, build_replay, replay
from preflight import verify_inputs
from pilot_model import OpenAIModel, ModelResponseError, usage_record

def append(path,value):
    with path.open('a') as f:f.write(json.dumps(value,sort_keys=True)+'\n')

def live_gate(path):
    if not path.exists():raise RuntimeError('No live freeze: independent reference review and observability gates remain pending')
    freeze=json.loads(path.read_text())
    if freeze.get('status')!='reviewed_reference_and_runner_ready':raise ValueError('Live freeze not accepted')
    required=['reference_review','reference_controls','fault_observability','semantic_mapping','runner_accounting','feedback_isolation','formal_bridge','final_release']
    if set(freeze.get('gates',{}))!=set(required) or not all(v is True for v in freeze['gates'].values()):raise ValueError('Missing live gate')
    files=freeze.get('files',{})
    from final_score import verify_reference
    ref=verify_reference()
    required_files=set(ref['artifact_sha256']) | {
        'test2/reference/frozen-v1/freeze.json','test2/configs/registration_v1.json',
        'test2/scripts/runner.py','test2/scripts/monitor.py','test2/scripts/feedback.py',
        'test2/scripts/score.py','test2/scripts/final_score.py','test2/scripts/formal_witness.py',
        'scripts/pilot_model.py'}
    if not required_files<=set(files):raise ValueError('Live freeze omits a required reference or evaluation artifact')
    if not files or files.get('test2/scripts/runner.py')!=sha(Path(__file__)):
        raise ValueError('Runner not bound to freeze')
    for name,digest in files.items():
        if not (ROOT/name).resolve().is_relative_to(ROOT):raise ValueError('Frozen path outside repository')
        if sha(ROOT/name)!=digest:raise ValueError('Frozen artifact changed: '+name)
    return freeze

def mock_candidate(round_no):
    # Arm-blind plumbing controls deliberately include false alarms and vacuity.
    active="6'b000000" if round_no==2 else "6'b111111"
    ok="6'b000000" if round_no==1 else "6'b111111"
    return {'body':f'assign active={active};assign ok={ok};',
            'properties':[{'id':f'P{i}','description':'offline plumbing, not a FIFO property'} for i in range(6)]}

def diagnostics(path):
    # Keep replay stable: avoid compiler wall/CPU timing and output-directory IDs.
    text=path.read_text().replace(str(path.parent),'CANDIDATE_DIR')
    lines=[s for s in text.splitlines() if any(k in s.lower() for k in ('error','warning','syntax'))]
    return '\n'.join(lines)[-6000:] or 'Compiler failed; see retained raw diagnostic log.'

def develop(candidate,trace_root,out):
    started=time.perf_counter();feedback={};compile_attempts=0;compile_seconds=0;replay_seconds=0;replays=0;executed_cycles=0
    try:
        validate(candidate)
        compile_attempts+=1
        info=compile_monitor(candidate,out/'compiled')
        compile_seconds+=info['seconds']
        if info['status']!='complete':
            feedback={'status':'compile_error','log':diagnostics(out/'compiled/yosys.log')}
        else:
            compile_attempts+=1
            iverilog=build_replay(out/'compiled')
            compile_seconds+=iverilog['seconds']
            if iverilog['status']!='complete':
                feedback={'status':'compile_error','log':diagnostics(out/'compiled/iverilog.log')}
            else:
                feedback={'status':'compiled','development':{}}
                for name in ('basic','boundary','wrap_reset'):
                    rows=json.loads((trace_root/'correct_stress/verilator'/name/'rows.json').read_text())
                    replays+=1
                    result=replay(out/'compiled',rows,out/name)
                    executed_cycles+=result['cycles']
                    replay_seconds+=result['execution']['seconds']
                    feedback['development'][name]={'complete':result['complete'],
                        'properties':[dict(id=p['id'],checks=p['checks'],failure_count=len(p['failures']),
                            first_failures=p['failures'][:8],unknown_count=len(p['unknown']),
                            first_unknown=p['unknown'][:8]) for p in result['properties']]}
    except ValueError as e:feedback={'status':'invalid_candidate','reason':str(e)}
    except Exception as e:feedback={'status':'infrastructure_error','type':type(e).__name__}
    compile_seconds=sum(json.loads(p.read_text())['seconds'] for p in
                        (out/'compiled/compile.json',out/'compiled/iverilog.json') if p.exists())
    cost={'compile_attempts':compile_attempts,'monitor_replays':replays,
          'compile_seconds':compile_seconds,'monitor_replay_seconds':replay_seconds,
          'replayed_cycles':executed_cycles,
          'wall_seconds':time.perf_counter()-started}
    dump(out/'development-feedback.json',feedback);dump(out/'development-cost.json',cost)
    return feedback,cost

def execute(mode,out,preflight,replay_source=None):
    started=time.perf_counter()
    config=json.loads((BASE/'configs/registration_v1.json').read_text())
    if mode=='live':live_gate(BASE/'configs/live_freeze_v1.json')
    verify_inputs();out.mkdir(parents=True,exist_ok=False)
    config_hash=sha(BASE/'configs/registration_v1.json')
    saved={}
    if mode=='replay':
        source_meta=json.loads((replay_source/'run.json').read_text())
        for line in (replay_source/'calls.jsonl').read_text().splitlines():
            r=json.loads(line)
            if r.get('parsed') is not None:saved[r['arm'],r['repetition'],r['round']]=r
    model=OpenAIModel(config,SCHEMA,'fifo_monitor') if mode=='live' else None
    sessions={(arm,rep):{'id':str(uuid.uuid4()),'previous':None,'feedback':None,'selected':None}
              for arm in config['arms'] for rep in range(1,config['repetitions']+1)}
    dump(out/'run.json',{'mode':mode,'config':config,'config_sha256':config_hash,
        'runner_sha256':sha(Path(__file__)),
        'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in
                        (BASE/'scripts/monitor.py',BASE/'scripts/feedback.py',ROOT/'scripts/pilot_model.py')},
        'shared_preflight':str(preflight),'preflight_summary_sha256':sha(preflight/'summary.json'),
        'session_ids':{f'{a}/{r}':s['id'] for (a,r),s in sessions.items()},
        'replay_origin':source_meta['mode'] if mode=='replay' else None,
        'provider_tools':[],'provider_conversation':'none; stateless explicit own-history only'})
    for round_no in range(1,config['rounds']+1):
        for rep in range(1,config['repetitions']+1):
            arms=config['arms'] if (round_no+rep)%2==0 else list(reversed(config['arms']))
            for arm in arms:
                if mode=='live':live_gate(BASE/'configs/live_freeze_v1.json')
                session=sessions[arm,rep];context={'mode':mode,'arm':arm,'repetition':rep,'round':round_no,'session_id':session['id']}
                d=out/arm/f'rep{rep}'/f'round{round_no}';d.mkdir(parents=True)
                prompt=messages(arm,preflight,round_no,session['previous'],session['feedback'])
                dump(d/'prompt.json',prompt);parsed=None
                for attempt in range(config['max_retries']+1 if mode=='live' else 1):
                    record=dict(context,attempt=attempt+1,prompt_sha256=sha(d/'prompt.json'),settings=config,
                                count_request_issued=False,generation_request_issued=False)
                    start=time.perf_counter()
                    try:
                        if mode=='live':
                            record['count_request_issued']=True
                            before=time.perf_counter();count=model.count_input_tokens(prompt)
                            record.update(input_token_count=count,count_latency_seconds=time.perf_counter()-before)
                            if count>config['max_input_tokens']:raise ValueError('Input token cap exceeded; no truncation')
                            record['generation_request_issued']=True
                            record.update(model.generate(prompt,context));parsed=record['parsed']
                        elif mode=='mock':
                            parsed=mock_candidate(round_no)
                            record.update(requested_model='mock-plumbing',returned_model='mock-plumbing',
                                status='completed',usage=usage_record(None),parsed=parsed,output_text=json.dumps(parsed))
                        else:
                            original=saved.get((arm,rep,round_no))
                            if original is None:raise ValueError('Replay round missing saved response')
                            if original['prompt_sha256']!=sha(d/'prompt.json'):raise ValueError('Replay prompt mismatch')
                            parsed=original['parsed']
                            record.update(requested_model='replay',returned_model='replay',usage=usage_record(None),
                                original_usage=original.get('usage'),parsed=parsed,output_text=original.get('output_text'),status='completed')
                        record['accepted_response']=True
                    except ModelResponseError as e:
                        record.update(e.record);record.update(accepted_response=False,error_type=e.reason)
                    except Exception as e:
                        record.update(accepted_response=False,error_type=type(e).__name__)
                    record['attempt_wall_seconds']=time.perf_counter()-start
                    append(out/'calls.jsonl',record)
                    if record.get('accepted_response'):break
                if parsed is None:
                    feedback={'status':'generation_unresolved'};cost={'compile_attempts':0,'compile_seconds':0,'monitor_replays':0,'monitor_replay_seconds':0,'replayed_cycles':0,'wall_seconds':0}
                else:
                    session['previous']=parsed
                    feedback,cost=develop(parsed,preflight,d)
                    if feedback['status']=='compiled':session['selected']=str(d/'compiled')
                session['feedback']=feedback
                append(out/'rounds.jsonl',dict(context,feedback=feedback,**cost))
    finals=[]
    for (arm,rep),session in sessions.items():
        selected=session['selected'];p=Path(selected) if selected else None
        finals.append({'arm':arm,'repetition':rep,'session_id':session['id'],'candidate_dir':selected,
            'candidate_sha256':sha(p/'candidate.sv') if p else None,
            'metadata_sha256':sha(p/'candidate.json') if p else None,'status':'frozen' if p else 'invalid'})
    dump(out/'final-candidates.json',{'mode':mode,'not_live_evidence':mode!='live','final_scoring_started':False,'candidates':finals})
    records=[json.loads(s) for s in (out/'rounds.jsonl').read_text().splitlines()]
    result={'mode':mode,'rounds':len(records),'compile_attempts':sum(r['compile_attempts'] for r in records),
            'wall_seconds':time.perf_counter()-started,
            'monitor_replays':sum(r['monitor_replays'] for r in records),'replayed_cycles':sum(r['replayed_cycles'] for r in records),
            'api_model_calls':sum(json.loads(s)['generation_request_issued'] for s in (out/'calls.jsonl').read_text().splitlines()),
            'final_scoring_started':False,'raw_dut_simulations_this_run':0}
    dump(out/'summary.json',result);return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['mock','replay','live'],required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--preflight',type=Path,required=True)
    p.add_argument('--replay-source',type=Path)
    a=p.parse_args();staged=ROOT/'build/private/midterm-openai-key';consumed=False
    try:
        if a.mode=='live':
            live_gate(BASE/'configs/live_freeze_v1.json')
            if not os.environ.get('OPENAI_API_KEY'):
                if not staged.exists() or staged.stat().st_mode&0o077:raise RuntimeError('Hidden key missing or unsafe')
                os.environ['OPENAI_API_KEY']=staged.read_text().strip();consumed=True
        print(json.dumps(execute(a.mode,a.output.resolve(),a.preflight.resolve(),a.replay_source.resolve() if a.replay_source else None),indent=2))
    finally:
        if consumed:staged.unlink(missing_ok=True);os.environ.pop('OPENAI_API_KEY',None)
