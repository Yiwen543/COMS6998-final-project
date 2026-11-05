"""Audit new reference-checker runs, including full unresolved evidence and session isolation."""
import argparse
import json
import tempfile
import time
from collections import Counter
from pathlib import Path
from coverage import summary
from inventory_natural_coverage import load_all
from preflight_spi_host import identity
from run_midterm_fixed import sha
from run_spi_core_b_development import token_totals
from wbxbar_reference_experiment import verify_freeze, messages, seed, group_status, validate_generated, parse

from wbxbar_reference_experiment import CANDIDATE
from wbxbar_cancel_validation import worker
from run_wbxbar_reference_bc import schedule


def audit(run,output):
    started=time.perf_counter()
    c=verify_freeze(run/'freeze.json');d=json.loads((run/'summary.json').read_text());meta=d['metadata']
    calls=[json.loads(l) for l in (run/'calls.jsonl').read_text().splitlines()]
    counts=[json.loads(l) for l in (run/'counts.jsonl').read_text().splitlines()] if (run/'counts.jsonl').exists() else []
    if meta['mode'] not in ('live','mock','replay'):raise ValueError('Unknown evidence mode')
    if [(r['repetition'],r['round'],r['arm']) for r in d['rows']]!=list(schedule(c)):raise ValueError('Schedule mismatch')
    sessions=meta['session_ids']
    if len(sessions)!=6 or len(set(sessions.values()))!=6:raise ValueError('Sessions not independent')
    for item in calls+d['rows']:
        if item['session_id']!=sessions[f"rep{item['repetition']}-{item['arm']}"]:raise ValueError('Session association mismatch')
    if meta['checker_sha256']!=sha(CANDIDATE/'checker.py'):raise ValueError('Wrong checker used')
    if token_totals(calls)!=meta['api_usage']:raise ValueError('API token totals')
    if len(counts)!=meta['api_count_requests']:raise ValueError('Count-request ledger')
    if sum(r['generation_requested'] for r in calls)!=meta['api_generation_calls']:raise ValueError('Generation ledger')
    manifest=json.loads((run/'shared/manifest.json').read_text())
    denom={tuple(i) for i in c['counter_identities']};sources=manifest['sources']
    executions=list(run.glob('rep*/seed/execution.json'))+list(run.glob('rep*/round*/execution.json'))
    cycle_sum=sum(json.loads(p.read_text())['executed_cycles'] for p in executions)
    if cycle_sum!=meta['executed_cycles'] or len(executions)!=meta['simulation_executions']:raise ValueError('Execution totals')
    checked=0
    for arm in c['arms']:
        for rep in range(1,c['development_budget']['repetitions']+1):
            folder=run/f'rep{rep}-{arm}';history=[];prior_path=folder/'seed'
            for rnd in range(1,c['development_budget']['rounds']+1):
                rr=[r for r in d['rows'] if (r['arm'],r['repetition'],r['round'])==(arm,rep,rnd)]
                if len(rr)!=1:raise ValueError('Scheduled round absent or duplicated')
                row=rr[0];attempts=[r for r in calls if (r['arm'],r['repetition'],r['round'])==(arm,rep,rnd)]
                if not 1<=len(attempts)<=c['model_limits']['max_retries']+1:raise ValueError('Retry budget')
                prior=json.loads((prior_path/'result.json').read_text())
                points=json.loads((prior_path/'raw-points.json').read_text());trace=json.loads((prior_path/'trace.json').read_text())
                expected=messages(c,arm,history,prior,points,trace,rnd)
                accepted=[]
                for a in attempts:
                    prompt=run/a['prompt']
                    if sha(prompt)!=a['prompt_sha256'] or json.loads(prompt.read_text())!=expected:raise ValueError('Rendered prompt drift')
                    if a['accepted']:
                        if meta['mode']=='live' and a['returned_model']!=c['model_limits']['model']:raise ValueError('Model substitution')
                        if meta['mode']=='live' and a['counted_input_tokens']>c['model_limits']['input_tokens']:raise ValueError('Input budget')
                        if meta['mode']=='live' and a['usage']['output_tokens']>c['model_limits']['output_tokens']:raise ValueError('Output budget')
                        if validate_generated(a['parsed'])!=a['actions']:raise ValueError('Action validation drift')
                        accepted.append(a)
                    expected=[*expected,{'role':'user','content':'Previous attempt failed. Return only valid actions within the unchanged schema and cycle budget.'}]
                if len(accepted)>1:raise ValueError('Multiple accepted batches')
                if not accepted:continue
                history.extend(accepted[0]['actions'])
                if row['status']!='simulated':continue
                path=folder/f'round{rnd}';actions=json.loads((path/'actions.json').read_text())['actions']
                if actions!=seed()+history:raise ValueError('Cumulative replay differs')
                points=load_all(path/'coverage.dat',sources)
                if {identity(p) for p in points}!=denom or len(points)!=len(denom):raise ValueError('Denominator drift')
                if points!=json.loads((path/'raw-points.json').read_text()):raise ValueError('Raw counter parsing differs')
                if summary(points)!=row['coverage'] or group_status(points,c['targets'])!=row['groups']:raise ValueError('Reported coverage differs')
                trace,transport=parse((path/'simulation.log').read_text(),actions,manifest['inputs'],manifest['outputs'])
                if transport!=row['transport'] or trace!=json.loads((path/'trace.json').read_text()):raise ValueError('Pin/transport replay differs')
                prior_path=path;checked+=1
    inputs={}
    for execution in executions:
        path=execution.parent;name=str(path.relative_to(run))
        trace=json.loads((path/'trace.json').read_text());inputs[name]=trace
        points=load_all(path/'coverage.dat',sources)
        if len(points)!=len(denom) or {identity(p) for p in points}!=denom or points!=json.loads((path/'raw-points.json').read_text()):raise ValueError('Batch counter drift')
        actions=json.loads((path/'actions.json').read_text())['actions']
        parsed,transport=parse((path/'simulation.log').read_text(),actions,manifest['inputs'],manifest['outputs'])
        if parsed!=trace:raise ValueError('Batch trace drift')
        batch=json.loads((path/'result.json').read_text())
        if transport!=batch['transport'] or summary(points)!=batch['coverage']:raise ValueError('Batch measurement drift')
    with tempfile.TemporaryDirectory(prefix='wbxbar-reference-live-audit-') as folder:
        fresh=worker(CANDIDATE,inputs,Path(folder)/'checker')
    if fresh['errors'] or not all(x['pass'] for x in fresh['selftests']):raise ValueError('Fresh checker audit failed')
    for name,value in fresh['cases'].items():
        path=run/name;batch=json.loads((path/'result.json').read_text())
        if batch['checker']!=value:raise ValueError('Checker result differs: '+name)
        complete=batch['transport']['delivery_complete'] and value['verdict']=='scoped_pass'
        if batch['verification_complete']!=complete:raise ValueError('Unknown treated as complete')
        if path.name!='seed':
            session=path.parent.name;rep=int(session.split('-')[0][3:]);arm=session.split('-')[1];rnd=int(path.name[5:])
            row=next(r for r in d['rows'] if (r['repetition'],r['round'],r['arm'])==(rep,rnd,arm))
            if row['checker']!=value or row['verification_complete']!=complete:raise ValueError('Round checker evidence lost')
    final_rows=[r for r in d['rows'] if r['round']==c['development_budget']['rounds']]
    verify_freeze(run/'freeze.json')
    result={'pass':True, 'mode':meta['mode'], 'new_live_evidence':meta['mode']=='live',
        'checker_batches_reexecuted':len(inputs),'selftests_passed':len(fresh['selftests']),
        'final_verdicts':dict(Counter(r['checker']['verdict'] for r in final_rows)),
        'final_unknown_records':sum(len(r['checker']['unresolved']) for r in final_rows),
        'final_failure_instances':sum(len(r['checker']['failures']) for r in final_rows),
        'independent_session_ids':sessions,'checker_sha256':sha(CANDIDATE/'checker.py'),
        'audit_seconds':time.perf_counter()-started,'fresh_rounds_checked':checked,'scheduled_rounds':len(d['rows']),
        'api_generation_requests':meta['api_generation_calls'],'api_count_requests':len(counts),
        'api_usage':token_totals(calls),'simulator_executions':len(executions),'executed_cycles':cycle_sum,
        'source_points_per_round':len(denom),'freeze_sha256':sha(run/'freeze.json'),
        'scope':'Recomputes new run prompts, counters and frozen checker including unknowns; diagnostics remain observations, not independently adjudicated defects.'}
    if output.exists():raise ValueError('Never overwrite audit')
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();audit(a.run.resolve(),a.output.resolve())
