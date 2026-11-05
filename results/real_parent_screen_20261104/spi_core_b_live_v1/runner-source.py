#!/usr/bin/env python3
"""B-only development of original integrated SPI core; mock and replay isolated.

Budgets/gates come from the original preregistration. Never starts C itself.
"""
import argparse
import json
import os
import time
from collections import Counter
from pathlib import Path

from pilot_model import OpenAIModel, ModelResponseError, ReplayModel, usage_record
from probe_spi_core_events import identity
from real_parent_screen import configuration
from run_midterm_b_development import KEY_FILE, append
from run_midterm_fixed import ROOT, sha
from run_pilot import versions
from spi_core_experiment import (CONTRACT, FREEZE, compile_driver, simulate,
    experiment_schema, validate_experimental, verify_freeze, group_status)
from spi_core_interface import FIELDS, OUTPUTS, action, seed

INSTRUCTIONS = ('Generate only JSON cycle actions for the fixed original SPI core. Change stimulus only. '
    'Maximize original DUT coverage under the fixed cycle/token budget. Follow the public contract. '
    'Checker failures on faulty RTL are evidence; do not suppress them. Every cumulative batch is '
    'replayed from the fixed seed; there is no implicit drain. Return the actions object only.')


def raw_page(points, sources, round_no, limit):
    names = sorted(str(p.relative_to(ROOT)) for p in sources)
    lines = {n:(ROOT/n).read_text().splitlines() for n in names}
    hierarchy = sorted({identity(p)[-1] for p in points})
    candidates = sorted((p for p in points if p['hits']==0 and p['type'] in ('line','branch','expr')),key=identity)
    count = min(limit,len(candidates))
    start = ((round_no-1)*limit)%len(candidates) if candidates else 0
    selected = [candidates[(start+i)%len(candidates)] for i in range(count)]
    return {'sources':names,'hierarchy_suffixes':hierarchy,
            'columns':['source_index','line','column','type','outcome','hierarchy_index','hits','source_text'],
            'total_uncovered_eligible':len(candidates),'page_offset':start,'page_limit':limit,
            'rows':[[names.index(p['source']),p['line'],p['column'],p['type'],p['outcome'],
                     hierarchy.index(identity(p)[-1]),p['hits'],lines[p['source']][p['line']-1]] for p in selected],
            'meaning':'Original separate Verilator counters; type/outcome identify counter kind/polarity. Source text is a raw line, not an inferred complete activation guard. No source-counter merging.'}


def diagnostics(checked):
    result = {'verdict':checked['verdict']}
    for key in ('failures','assumption_violations','unresolved'):
        items = checked.get(key,[])
        if not isinstance(items,list):items=[items]
        result[key]={'total':len(items),'first_eight':items[:8]}
    return result


def messages(config, generated, prior, points, trace, round_no):
    c = configuration('spi_host_core')
    sources = [ROOT/c['root']/n for n in c['sources']]
    common = {'specification':CONTRACT.read_text(),
        'rtl':{str(p.relative_to(ROOT)):p.read_text() for p in sources},
        'cycle_field_order':list(FIELDS),'field_widths':FIELDS,
        'common_seed':[[a[k] for k in FIELDS] for a in seed()],
        'previous_generated_cycles':[[a[k] for k in FIELDS] for a in generated],
        'round':round_no,'max_new_cycles':config['development_budget']['max_new_cycles'],
        'total_rounds':config['development_budget']['rounds'],
        'checker':diagnostics(prior['checker']),
        'execution_trace':{'columns':['cycle',*['input.'+k for k in FIELDS],
                                    *['pre.'+k for k in OUTPUTS],*['post.'+k for k in OUTPUTS]],
            'rows':[[r['cycle'],*[r['action'][k] for k in FIELDS],
                     *[r['pre'][k] for k in OUTPUTS],*[r['post'][k] for k in OUTPUTS]] for r in trace[-16:]]},
        'raw_uncovered_dut_coverage':raw_page(points,sources,round_no,config['feedback_policy']['maximum_uncovered_rows'])}
    return [{'role':'system','content':INSTRUCTIONS},
            {'role':'user','content':json.dumps(common,separators=(',',':'))}]


def assess(rows, config, mode):
    details=[]
    for rep in range(1,config['development_budget']['repetitions']+1):
        rs=[r for r in rows if r['repetition']==rep]
        complete = len(rs)==config['development_budget']['rounds'] and all(r['status']=='simulated' for r in rs)
        # DUT failures and a legitimately pending batch are not infrastructure failure.
        legal = complete and all(not r['checker'].get('assumption_violations') for r in rs)
        first=sum(not g['all_hit'] for g in rs[0]['groups']) if rs else None
        final=sum(not g['all_hit'] for g in rs[-1]['groups']) if rs else None
        details.append({'repetition':rep,'complete':complete,'legal':legal,
            'first_round_unhit_groups':first,'final_unhit_groups':final,
            'not_immediately_saturated':legal and first>=2,
            'later_group_progress':legal and final<first,
            'final_verdict':rs[-1]['checker']['verdict'] if rs else None})
    gate=config['development_acceptance']
    passed=mode=='live' and all(d['complete'] and d['legal'] for d in details) and \
        sum(d['not_immediately_saturated'] for d in details)>=gate['min_repetitions_with_two_groups_unhit_after_round_one'] and \
        sum(d['later_group_progress'] for d in details)>=gate['min_repetitions_with_later_group_progress']
    return {'pass':passed,'repetitions':details,'mock_or_replay_is_not_new_live_evidence':mode!='live',
            'C_started':False,'next':'Independent formal trial preparation only if live B passes; do not change original budget to favor C.'}


def token_totals(calls):
    # cached/reasoning fields are subsets, never added again.
    return {'input_tokens':sum((c['usage']['input_tokens'] or 0) for c in calls),
            'output_tokens':sum((c['usage']['output_tokens'] or 0) for c in calls),
            'unknown_usage_attempts':sum(c['usage']['input_tokens'] is None for c in calls)}


def run(args):
    config=verify_freeze(args.config)
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter(); rows=[]; calls=[]; consumed=False; model=None
    settings={**config['model_limits'],'max_output_tokens':config['model_limits']['output_tokens']}
    meta={'mode':args.mode,'arm':'B','scope':'original spi_host_core integration; development only',
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
            try:model=OpenAIModel(settings,schema=experiment_schema(64),schema_name='spi_core_actions')
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
                        status='simulated'
                    except Exception as error:
                        append(out/'failures.jsonl',{'repetition':rep,'round':rnd,'stage':'simulation_or_measurement',
                                                   'error_type':type(error).__name__})
                        status='simulation_failed'
                tokens=token_totals(rep_calls); total=tokens['input_tokens']+tokens['output_tokens']
                newly=sum(p['hits']>0 and p['type']=='branch' for p in points)-baseline_branch
                row={'mode':args.mode,'arm':'B','repetition':rep,'round':rnd,'status':status,
                     'coverage':prior['coverage'],'checker':prior['checker'],
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
                print(f"SPI-core B {args.mode} rep {rep} round {rnd}: {status}; unhit groups={sum(not g['all_hit'] for g in row['groups'])}; verdict={prior['checker']['verdict']}",flush=True)
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
