"""Read-only recomputation of frozen live counters, prompts and API costs."""
import argparse
import json
from pathlib import Path
from coverage import summary
from inventory_natural_coverage import load_all
from preflight_spi_host import identity
from run_midterm_fixed import sha
from run_spi_core_b_development import token_totals
from wbxbar_experiment import verify_freeze, messages, seed, group_status, validate_generated, parse


def audit(run,output):
    c=verify_freeze(run/'freeze.json');d=json.loads((run/'summary.json').read_text());meta=d['metadata']
    calls=[json.loads(l) for l in (run/'calls.jsonl').read_text().splitlines()]
    counts=[json.loads(l) for l in (run/'counts.jsonl').read_text().splitlines()]
    if meta['mode']!='live':raise ValueError('Expected live evidence')
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
                        if a['returned_model']!=c['model_limits']['model']:raise ValueError('Model substitution')
                        if a['counted_input_tokens']>c['model_limits']['input_tokens']:raise ValueError('Input budget')
                        if a['usage']['output_tokens']>c['model_limits']['output_tokens']:raise ValueError('Output budget')
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
    result={'pass':True,'fresh_rounds_checked':checked,'scheduled_rounds':len(d['rows']),
        'api_generation_requests':meta['api_generation_calls'],'api_count_requests':len(counts),
        'api_usage':token_totals(calls),'simulator_executions':len(executions),'executed_cycles':cycle_sum,
        'source_points_per_round':len(denom),'freeze_sha256':sha(run/'freeze.json'),
        'scope':'Recomputes reported evidence; checker diagnostics remain observations, not independently attributed DUT defects.'}
    if output.exists():raise ValueError('Never overwrite audit')
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();audit(a.run.resolve(),a.output.resolve())
