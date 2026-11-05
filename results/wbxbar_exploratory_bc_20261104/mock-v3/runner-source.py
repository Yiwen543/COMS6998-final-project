#!/usr/bin/env python3
"""Matched, interleaved exploratory B/C. No difficulty-based C selection."""
import argparse
import json
import os
import time
from pathlib import Path
from pilot_model import OpenAIModel, ModelResponseError, ReplayModel, usage_record
from run_midterm_b_development import KEY_FILE, append
from run_midterm_fixed import sha
from run_pilot import versions
from run_spi_core_b_development import token_totals
from wbxbar_experiment import (FREEZE, verify_freeze, compile_driver, simulate,
    messages, schema, validate_generated, seed, action, group_status)


def schedule(config):
    b=config['development_budget']
    for rep in range(1,b['repetitions']+1):
        for rnd in range(1,b['rounds']+1):
            for arm in (('B','C') if rep%2 else ('C','B')):yield rep,rnd,arm


def run(args):
    config=verify_freeze(args.config)
    if args.mode=='live' and not all(config.get('live_'+a+'_allowed') for a in config['arms']):
        raise ValueError('Final live freeze required')
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter();calls=[];rows=[];states={};consumed=False;model=None
    settings={**config['model_limits'],'max_output_tokens':config['model_limits']['output_tokens']}
    meta={'mode':args.mode,'scope':config['id'],'freeze_sha256':sha(args.config),
        'versions':versions(),'model_settings':settings,'status':'started',
        'compilations':0,'compile_seconds':0,'simulation_executions':0,'executed_cycles':0,
        'requested_cycles':0,'simulation_seconds':0,'api_generation_calls':0,'api_count_requests':0,
        'egraph_preprocessing_seconds_this_run':0,'egraph_preprocessing':'Reused frozen offline artifacts; historical preprocessing reported separately.',
        'simulation_policy':'Fresh cumulative seed+actions replay; all physical cycles counted; no extra drain.',
        'independent_sessions':'Responses calls have no conversation or previous_response_id; only own-arm history is rendered.'}
    (out/'freeze.json').write_bytes(args.config.read_bytes())
    (out/'runner-source.py').write_bytes(Path(__file__).read_bytes())
    try:
        if args.mode=='live':
            if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
                raise RuntimeError('Private staged OpenAI key missing or unsafe permissions')
            consumed=True;os.environ['OPENAI_API_KEY']=KEY_FILE.read_text().strip()
            try:model=OpenAIModel(settings,schema=schema(),schema_name='wbxbar_offers')
            finally:os.environ.pop('OPENAI_API_KEY',None)
        elif args.mode=='replay':
            if not args.replay:raise ValueError('Replay requires calls.jsonl')
            model=ReplayModel(args.replay);meta.update(source_mode=model.source_mode,replay_source_sha256=sha(args.replay))
        compile_start=time.perf_counter()
        try:binaries,manifest=compile_driver(out/'shared')
        finally:
            meta['compile_seconds']=time.perf_counter()-compile_start
            meta['compilations']=sum(1 for _ in (out/'shared').glob('*/compile.log'))
        meta['compile_commands']=manifest['compilations']
        denominator={tuple(i) for i in config['counter_identities']}
        def execute(state,actions,path):
            verify_freeze(args.config)
            meta['simulation_executions']+=1;state['executions']+=1
            meta['requested_cycles']+=len(actions);t=time.perf_counter()
            try:return simulate(binaries['verilator'],actions,path,manifest,denominator)
            finally:
                p=path/'execution.json'
                e=json.loads(p.read_text()) if p.exists() else {'executed_cycles':0,'simulation_seconds':time.perf_counter()-t}
                meta['executed_cycles']+=e['executed_cycles'];state['cycles']+=e['executed_cycles']
                meta['simulation_seconds']+=e['simulation_seconds'];state['sim_seconds']+=e['simulation_seconds']
        for rep,rnd,arm in schedule(config):
            roundstart=time.perf_counter();key=(rep,arm)
            if key not in states:
                folder=out/f'rep{rep}-{arm}';folder.mkdir()
                state={'folder':folder,'history':[],'calls':[],'cycles':0,'executions':0,
                    'sim_seconds':0,'active_wall_seconds':0,'measurement_round':0}
                state['prior'],state['points'],state['trace']=execute(state,seed(),folder/'seed')
                state['baseline_branch']=sum(p['hits']>0 and p['type']=='branch' for p in state['points'])
                states[key]=state
            state=states[key];folder=state['folder']
            rendered=messages(config,arm,state['history'],state['prior'],state['points'],state['trace'],rnd)
            accepted=None
            for attempt in range(1,settings['max_retries']+2):
                prompt=folder/f'prompt-{rnd}-{attempt}.json';prompt.write_text(json.dumps(rendered,indent=2)+'\n')
                rec={'mode':args.mode,'arm':arm,'repetition':rep,'round':rnd,'attempt':attempt,
                    'accepted':False,'requested_model':settings['model'],'usage':usage_record(None),
                    'settings':settings,'prompt':str(prompt.relative_to(out)),'prompt_sha256':sha(prompt),
                    'generation_requested':False}
                t=time.perf_counter()
                try:
                    if args.mode=='live':
                        count_start=time.perf_counter();meta['api_count_requests']+=1
                        count_record={'arm':arm,'repetition':rep,'round':rnd,'attempt':attempt}
                        try:
                            count=model.count_input_tokens(rendered);count_record['input_tokens']=count
                        except Exception as error:
                            count_record['error_type']=type(error).__name__;raise
                        finally:
                            count_record['seconds']=time.perf_counter()-count_start;append(out/'counts.jsonl',count_record)
                        rec['counted_input_tokens']=count
                        if count>settings['input_tokens']:raise ValueError('Input token cap exceeded')
                        verify_freeze(args.config);meta['api_generation_calls']+=1;rec['generation_requested']=True
                        rec.update(model.generate(rendered,{}))
                    elif args.mode=='replay':
                        rec.update(model.generate(rendered,{'arm':arm,'repetition':rep,'round':rnd}))
                        rec['source_usage']=rec['usage'];rec['usage']=usage_record(None)
                    else:
                        # Arm-blind plumbing-only mock; never reported as model evidence.
                        data={'actions':[action() for _ in range(config['development_budget']['max_new_cycles'])]}
                        rec.update(requested_model='mock-idle',returned_model='mock-idle',
                            response_id=f'mock-{arm}-{rep}-{rnd}',output_text=json.dumps(data),parsed=data)
                    accepted=validate_generated(rec['parsed'],config['development_budget']['max_new_cycles'])
                    rec.update(accepted=True,actions=accepted)
                except ModelResponseError as error:rec.update(error.record,validation_failure=error.reason)
                except Exception as error:
                    rec.update(error_type=type(error).__name__,http_status=getattr(error,'status_code',None))
                    if isinstance(error,ValueError):rec['validation_failure']=str(error)
                finally:
                    rec['request_wall_seconds']=time.perf_counter()-t
                    calls.append(rec);state['calls'].append(rec);append(out/'calls.jsonl',rec)
                if accepted is not None:break
                rendered=[*rendered,{'role':'user','content':'Previous attempt failed. Return only valid actions within the unchanged schema and cycle budget.'}]
            status='no_valid_actions'
            if accepted is not None:
                state['history'].extend(accepted)
                try:
                    state['prior'],state['points'],state['trace']=execute(state,seed()+state['history'],folder/f'round{rnd}')
                    state['measurement_round']=rnd;status='simulated'
                except Exception as error:
                    append(out/'failures.jsonl',{'arm':arm,'repetition':rep,'round':rnd,
                        'stage':'simulation_or_measurement','error_type':type(error).__name__,'detail':str(error)[:1000]})
                    status='simulation_failed'
            state['active_wall_seconds']+=time.perf_counter()-roundstart
            prior=state['prior'];tokens=token_totals(state['calls']);total=tokens['input_tokens']+tokens['output_tokens']
            newly=sum(p['hits']>0 and p['type']=='branch' for p in state['points'])-state['baseline_branch']
            row={'mode':args.mode,'arm':arm,'repetition':rep,'round':rnd,'status':status,
                'measurement_fresh':status=='simulated','measurement_round':state['measurement_round'],
                'coverage':prior['coverage'],'checker':prior['checker'],'transport':prior['transport'],
                'verification_complete':prior['verification_complete'],'groups':group_status(state['points'],config['targets']),
                'api_usage_cumulative':tokens,'api_tokens':total if args.mode=='live' else None,
                'token_roi_new_branch_points_per_1000':1000*newly/total if args.mode=='live' and total else None,
                'new_branch_points':newly,'attempts':len(state['calls']),
                'failed_attempts':sum(not c['accepted'] for c in state['calls']),
                'functional_diagnostic_count':len(prior['checker'].get('failures',[])),
                'distinct_failure_categories':sorted({f['category'] for f in prior['checker'].get('failures',[])}),
                'simulator_executions':state['executions'],'executed_cycles_including_replays':state['cycles'],
                'unique_generated_cycles':len(state['history']),'simulation_seconds':state['sim_seconds'],
                'active_wall_seconds':state['active_wall_seconds'],'elapsed_run_seconds':time.perf_counter()-start}
            rows.append(row);append(out/'rounds.jsonl',row)
            print(f"WBXBAR {args.mode} {arm} rep{rep} round{rnd}: {status}; groups={sum(g['all_hit'] for g in row['groups'])}/8; {prior['checker']['verdict']}",flush=True)
        meta['status']='completed' if all(r['status']=='simulated' for r in rows) else 'completed_with_failed_rounds'
    except Exception as error:
        meta.update(status='failed',error_type=type(error).__name__);raise
    finally:
        meta.update(elapsed_seconds=time.perf_counter()-start,api_usage=token_totals(calls))
        (out/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
        (out/'summary.json').write_text(json.dumps({'metadata':meta,'rows':rows},indent=2)+'\n')
        if consumed:KEY_FILE.unlink(missing_ok=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['mock','live','replay'],required=True)
    p.add_argument('--config',type=Path,default=FREEZE);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--replay',type=Path);run(p.parse_args())
