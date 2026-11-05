"""Offline audit of actual saved prompts, raw counts, traces and API accounting."""
import argparse
import json
from pathlib import Path

from inventory_natural_coverage import load_all
from probe_spi_core_events import identity
from real_parent_screen import configuration
from run_midterm_fixed import ROOT,sha
from run_spi_core_b_development import messages, token_totals, assess
from spi_core_experiment import group_status,verify_freeze
from spi_core_interface import parse,seed


def audit(folder):
    cfg=verify_freeze(folder/'freeze.json')
    s=json.loads((folder/'summary.json').read_text()); rows=s['rows'];m=s['metadata']
    calls=[json.loads(x) for x in (folder/'calls.jsonl').read_text().splitlines()]
    counts=[json.loads(x) for x in (folder/'counts.jsonl').read_text().splitlines()]
    assert s['mode']=='live' and m['status']=='completed'
    assert len(rows)==18 and all(r['status']=='simulated' for r in rows)
    assert token_totals(calls)==m['api_usage']
    assert len(counts)==m['api_count_requests']
    assert sum(c['generation_requested'] for c in calls)==m['api_generation_calls']
    assert assess(rows,cfg,'live')==s['gate']
    c=configuration('spi_host_core');sources=[str(Path(c['root'])/n) for n in c['sources']]
    denominator={tuple(x) for x in cfg['counter_identities']}
    executions=0;cycles=0;prompt_matches=0;repeated_diagnostics=0;distinct_assumptions=set();decreases=[]
    for rep in range(1,4):
        folder_rep=folder/f'rep{rep}';history=[];previous_counts=None
        for rnd in range(0,7):
            batch=folder_rep/('seed' if rnd==0 else f'round{rnd}')
            if rnd:
                row=next(r for r in rows if r['repetition']==rep and r['round']==rnd)
                accepted=[c for c in calls if c['repetition']==rep and c['round']==rnd and c['accepted']]
                assert len(accepted)==1;call=accepted[0]
                assert call['requested_model']==call['returned_model']==cfg['model_limits']['model']
                assert call['status']=='completed'
                assert call['usage']['input_tokens']<=cfg['model_limits']['input_tokens']
                assert call['usage']['output_tokens']<=cfg['model_limits']['output_tokens']
                rendered=messages(cfg,history,prior,points,trace,rnd)
                stored=json.loads((folder/call['prompt']).read_text())
                # This completed run had no failed/retry prompts. Reject if that changes.
                assert call['attempt']==1 and rendered==stored;prompt_matches+=1
                assert sha(folder/call['prompt'])==call['prompt_sha256']
                history+=call['actions']
            actions=json.loads((batch/'actions.json').read_text())['actions']
            assert actions==seed()+history
            trace=parse((batch/'simulation.log').read_text(),actions)
            assert trace==json.loads((batch/'trace.json').read_text())
            points=load_all(batch/'coverage.dat',sources)
            assert points==json.loads((batch/'raw-points.json').read_text())
            observed={identity(p):p['hits'] for p in points}
            assert set(observed)==denominator and len(points)==len(denominator)
            if previous_counts is not None:
                # Independent processes have separate final settle/evaluation activity.
                # Raw magnitudes are not a persistent accumulating counter. Never
                # max/sum them to manufacture monotonic counts across replays.
                decreases += [{'repetition':rep,'round':rnd,'counter':k,'before':v,'after':observed[k]}
                              for k,v in previous_counts.items() if observed[k]<v]
                assert all(observed[k]>0 for k,v in previous_counts.items() if v>0)
            previous_counts=observed
            prior=json.loads((batch/'result.json').read_text())
            assert prior['checker']==json.loads((batch/'checker-output.json').read_text())['cases']['batch']
            executions+=1;cycles+=len(trace)
            if rnd:
                assert row['coverage']==prior['coverage'] and row['checker']==prior['checker']
                assert row['groups']==group_status(points,cfg['targets'])
                used=[c for c in calls if c['repetition']==rep and c['round']<=rnd]
                assert token_totals(used)==row['api_usage_cumulative']
                for a in row['checker'].get('assumption_violations',[]):
                    repeated_diagnostics+=1;distinct_assumptions.add((rep,a['cycle'],a['category']))
    assert cycles==m['executed_cycles']==m['requested_cycles'] and executions==m['simulation_executions']
    costs=json.loads((folder/'target_cost.json').read_text())
    for cost in costs:
        if cost['reached']:
            row=next(r for r in rows if r['repetition']==cost['repetition'] and r['round']==cost['first_round'])
            assert not row['checker']['assumption_violations']
    result={'status':'pass','scope':'saved evidence integrity/accounting, not proof of DUT/checker correctness',
            'exact_prompt_reconstructions':prompt_matches,'raw_counter_denominator':len(denominator),
            'all_batches_raw_counts_and_trace_checked':executions,'actual_cycles':cycles,
            'covered_point_set_monotone_in_this_run':True,
            'raw_magnitude_decreases':decreases,
            'replayed_assumption_diagnostics':repeated_diagnostics,
            'distinct_assumption_records':sorted(distinct_assumptions),
            'api_usage':m['api_usage'],'development_gate':s['gate']['pass'],
            'openai_staged_key_removed':not (ROOT/'build/private/midterm-openai-key').exists(),
            'new_api_calls':0,'new_simulations':0,'script_sha256':sha(Path(__file__))}
    (folder/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);a=p.parse_args();audit(a.input.resolve())
