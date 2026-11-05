#!/usr/bin/env python3
"""Separate safe-driver B runner; copied accounting loop, immutable parent helpers.

The registered resource budget and acceptance function are unchanged. Does not
repair old model output or start C on a failed development gate.
"""
import argparse
import json
import os
import time
from pathlib import Path
from pilot_model import OpenAIModel,ModelResponseError,ReplayModel,usage_record
from run_midterm_b_development import KEY_FILE,append
from run_midterm_fixed import ROOT,sha
from run_pilot import versions
from run_spi_core_b_development import assess,token_totals
from spi_core_experiment import group_status
from spi_core_safe_experiment import (FREEZE,verify_freeze,compile_driver,simulate,
    messages,experiment_schema,validate_experimental,seed,action)

def run(args):
    config=verify_freeze(args.config)
    if args.mode=='live' and not config.get('live_B_allowed'):
        raise ValueError('Independent Claude transport review/final freeze required before live B')
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter(); rows=[]; calls=[]; consumed=False; model=None
    settings={**config['model_limits'],'max_output_tokens':config['model_limits']['output_tokens']}
    meta={'mode':args.mode,'arm':'B','scope':'protocol-safe offer SPI core; separately registered development',
          'freeze_sha256':sha(args.config),'versions':versions(),'compilations':0,'api_generation_calls':0,
          'api_count_requests':0,'compile_seconds':0,'status':'started','model_settings':settings,
          'simulation_executions':0,'executed_cycles':0,'requested_cycles':0,'simulation_seconds':0,
          'source_mode':None,'egraph_preprocessing_seconds_this_run':0}
    (out/'freeze.json').write_bytes(args.config.read_bytes())
    (out/'runner-source.py').write_bytes(Path(__file__).read_bytes())
    try:
        if args.mode=='live':
            if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
                raise RuntimeError('Private staged OpenAI key missing or unsafe permissions')
            consumed=True
            os.environ['OPENAI_API_KEY']=KEY_FILE.read_text().strip()
            try:model=OpenAIModel(settings,schema=experiment_schema(64),schema_name='spi_core_safe_offers')
            finally:os.environ.pop('OPENAI_API_KEY',None)
        elif args.mode=='replay':
            if not args.replay:raise ValueError('Replay requires --replay calls.jsonl')
            model=ReplayModel(args.replay);meta['source_mode']=model.source_mode
            meta['replay_source_sha256']=sha(args.replay)
        meta['compilations']+=1
        compile_start=time.perf_counter()
        try:binary,cmd,seconds=compile_driver(out/'shared')
        finally:meta['compile_seconds']=time.perf_counter()-compile_start
        meta['compile_command']=cmd
        denominator={tuple(i) for i in config['counter_identities']}
        for rep in range(1,config['development_budget']['repetitions']+1):
            repstart=time.perf_counter(); folder=out/f'rep{rep}';folder.mkdir()
            history=[];rep_calls=[];cycles=0;executions=0;sim_seconds=0

            def execute(aa, path):
                nonlocal cycles,executions,sim_seconds
                verify_freeze(args.config)
                executions+=1;meta['simulation_executions']+=1;meta['requested_cycles']+=len(aa)
                t=time.perf_counter()
                try:return simulate(binary,aa,path,denominator)
                finally:
                    epath=path/'execution.json'
                    if epath.exists():
                        ex=json.loads(epath.read_text());n=ex['executed_cycles'];sec=ex['simulation_seconds']
                    else:n=0;sec=time.perf_counter()-t
                    cycles+=n;sim_seconds+=sec;meta['executed_cycles']+=n;meta['simulation_seconds']+=sec

            prior,points,trace=execute(seed(),folder/'seed')
            measurement_round=0
            baseline_branch=sum(p['hits']>0 and p['type']=='branch' for p in points)
            for rnd in range(1,config['development_budget']['rounds']+1):
                roundstart=time.perf_counter();rendered=messages(config,history,prior,points,trace,rnd);accepted=None
                for attempt in range(1,settings['max_retries']+2):
                    prompt=folder/f'prompt-{rnd}-{attempt}.json';prompt.write_text(json.dumps(rendered,indent=2)+'\n')
                    rec={'mode':args.mode,'arm':'B','repetition':rep,'round':rnd,'attempt':attempt,
                         'accepted':False,'requested_model':settings['model'] if model else 'mock-idle',
                         'usage':usage_record(None),'settings':settings,'prompt':str(prompt.relative_to(out)),
                         'prompt_sha256':sha(prompt),'generation_requested':False}
                    t=time.perf_counter()
                    try:
                        if args.mode=='live':
                            count_start=time.perf_counter();meta['api_count_requests']+=1
                            try:
                                count=model.count_input_tokens(rendered)
                                append(out/'counts.jsonl',{'repetition':rep,'round':rnd,'attempt':attempt,
                                    'input_tokens':count,'seconds':time.perf_counter()-count_start})
                            except Exception as error:
                                append(out/'counts.jsonl',{'repetition':rep,'round':rnd,'attempt':attempt,
                                    'error_type':type(error).__name__,'seconds':time.perf_counter()-count_start})
                                raise
                            rec['counted_input_tokens']=count
                            if count>settings['input_tokens']:raise ValueError('Input token cap exceeded')
                            verify_freeze(args.config)
                            meta['api_generation_calls']+=1;rec['generation_requested']=True
                            rec.update(model.generate(rendered,{}))
                        elif args.mode=='replay':
                            rec.update(model.generate(rendered,{'arm':'B','repetition':rep,'round':rnd}))
                            rec['source_usage']=rec['usage'];rec['usage']=usage_record(None)
                        else:
                            data={'actions':[action() for _ in range(64)]}
                            rec.update(returned_model='mock-idle',response_id=f'mock-{rep}-{rnd}',
                                       output_text=json.dumps(data),parsed=data)
                        accepted=validate_experimental(rec['parsed'],64)
                        rec.update(accepted=True,actions=accepted)
                    except ModelResponseError as error:rec.update(error.record,validation_failure=error.reason)
                    except Exception as error:
                        rec.update(error_type=type(error).__name__,http_status=getattr(error,'status_code',None))
                        if isinstance(error,ValueError):rec['validation_failure']=str(error)
                    finally:
                        rec['request_wall_seconds']=time.perf_counter()-t
                        calls.append(rec);rep_calls.append(rec);append(out/'calls.jsonl',rec)
                    if accepted is not None:break
                    rendered=[*rendered,{'role':'user','content':'Previous attempt failed. Return only schema-conforming actions within the stated profile and budget.'}]
                status='no_valid_actions'
                if accepted is not None:
                    history.extend(accepted)
                    try:
                        prior,points,trace=execute(seed()+history,folder/f'round{rnd}')
                        measurement_round=rnd
                        status='simulated'
                    except Exception as error:
                        append(out/'failures.jsonl',{'repetition':rep,'round':rnd,
                            'stage':getattr(error,'stage','validation_or_integrity'),
                            'error_type':type(error).__name__,'detail':str(error)[:1000]})
                        status='simulation_failed'
                tokens=token_totals(rep_calls); total=tokens['input_tokens']+tokens['output_tokens']
                newly=sum(p['hits']>0 and p['type']=='branch' for p in points)-baseline_branch
                row={'mode':args.mode,'arm':'B','repetition':rep,'round':rnd,'status':status,
                     'measurement_fresh':status=='simulated','measurement_round':measurement_round,
                     'measurement_note':None if status=='simulated' else 'Coverage/checker/groups below are the last successful measurement, not this failed round.',
                     'coverage':prior['coverage'],'checker':prior['checker'],
                     'transport':prior['transport'],'delivery_complete':prior['delivery_complete'],
                     'verification_complete':prior['verification_complete'],
                     'failure_diagnostic_count':len(prior['checker'].get('failures',[])),
                     'distinct_failure_categories':sorted({f.get('category','unspecified') for f in prior['checker'].get('failures',[]) if isinstance(f,dict)}),
                     'groups':group_status(points,config['targets']),'api_usage_cumulative':tokens,
                     'api_tokens':total if args.mode=='live' else None,
                     'token_roi_new_branch_points_per_1000':1000*newly/total if args.mode=='live' and total else None,
                     'new_branch_points':newly,'attempts':len(rep_calls),
                     'failed_attempts':sum(not c['accepted'] for c in rep_calls),
                     'simulator_executions':executions,'executed_cycles_including_replays':cycles,
                     'unique_generated_cycles':len(history),'simulation_seconds':sim_seconds,
                     'round_wall_seconds':time.perf_counter()-roundstart,
                     'repetition_wall_seconds':time.perf_counter()-repstart,'elapsed_run_seconds':time.perf_counter()-start}
                rows.append(row);append(out/'rounds.jsonl',row)
                print(f"SPI-core safe B {args.mode} rep {rep} round {rnd}: {status}; unhit groups={sum(not g['all_hit'] for g in row['groups'])}; verdict={prior['checker']['verdict']}",flush=True)
                if status=='simulation_failed':break
        meta['status']='completed'
    except Exception as error:
        meta.update(status='failed',error_type=type(error).__name__)
        raise
    finally:
        meta.update(elapsed_seconds=time.perf_counter()-start,api_usage=token_totals(calls))
        (out/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
        (out/'summary.json').write_text(json.dumps({'mode':args.mode,'gate':assess(rows,config,args.mode),
                                                   'metadata':meta,'rows':rows},indent=2)+'\n')
        if consumed:KEY_FILE.unlink(missing_ok=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['mock','live','replay'],required=True)
    p.add_argument('--config',type=Path,default=FREEZE);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--replay',type=Path);run(p.parse_args())
