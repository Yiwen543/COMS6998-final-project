"""Descriptive per-session endpoints and cost curves; retain unsuccessful runs."""
import argparse
import csv
import json
from pathlib import Path


def report(run):
    data=json.loads((run/'summary.json').read_text());meta=data['metadata'];rows=data['rows']
    config=json.loads((run/'freeze.json').read_text());flat=[];endpoints=[]
    for r in rows:
        flat.append({k:r[k] for k in ['mode','arm','repetition','round','status','measurement_fresh',
            'measurement_round','api_tokens','attempts','failed_attempts','simulator_executions',
            'executed_cycles_including_replays','unique_generated_cycles','simulation_seconds',
            'active_wall_seconds','functional_diagnostic_count','verification_complete',
            'token_roi_new_branch_points_per_1000']} | {
            'checker_verdict':r['checker']['verdict'],
            'target_hits':sum(h>0 for g in r['groups'] for h in g['raw_source_hits']),
            'complete_groups':sum(g['all_hit'] for g in r['groups']),
            **{kind+'_'+field:r['coverage'][kind][field] for kind in r['coverage'] for field in ['covered','total','percent']}})
    for arm in config['arms']:
        for rep in range(1,config['development_budget']['repetitions']+1):
            rr=[r for r in rows if r['arm']==arm and r['repetition']==rep]
            fresh=[r for r in rr if r['measurement_fresh']]
            hit=next((r for r in fresh if all(g['all_hit'] for g in r['groups'])),None)
            valid=next((r for r in fresh if all(g['all_hit'] for g in r['groups']) and r['verification_complete']),None)
            endpoints.append({'arm':arm,'repetition':rep,'rounds_recorded':len(rr),
                'rounds_measured':len(fresh),'first_raw_target_round':hit['round'] if hit else 'not reached',
                'first_checker_complete_target_round':valid['round'] if valid else 'not reached',
                'tokens_at_first_raw_target':hit['api_tokens'] if hit else None,
                'cycles_at_first_raw_target':hit['executed_cycles_including_replays'] if hit else None,
                'executions_at_first_raw_target':hit['simulator_executions'] if hit else None,
                'active_seconds_at_first_raw_target':hit['active_wall_seconds'] if hit else None,
                'final_branch_covered':fresh[-1]['coverage']['branch']['covered'] if fresh else None,
                'first_round_unhit_groups':sum(not g['all_hit'] for g in fresh[0]['groups']) if fresh else None,
                'later_group_progress':bool(fresh) and sum(g['all_hit'] for g in fresh[-1]['groups'])>sum(g['all_hit'] for g in fresh[0]['groups'])})
    for name,records in [('rounds.csv',flat),('endpoints.csv',endpoints)]:
        if records:
            with (run/name).open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    (run/'endpoints.json').write_text(json.dumps(endpoints,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,2,figsize=(11,7))
    for ax,(x,label) in zip(axes.flat,[('api_tokens','API input + output tokens'),
        ('executed_cycles_including_replays','Executed cycles including replay'),
        ('simulator_executions','Simulator executions'),('active_wall_seconds','Active session seconds; shared compilation separate')]):
        for arm in config['arms']:
            for rep in range(1,config['development_budget']['repetitions']+1):
                rr=[r for r in flat if r['arm']==arm and r['repetition']==rep and r['measurement_fresh'] and r[x] is not None]
                if rr:ax.plot([r[x] for r in rr],[r['branch_percent'] for r in rr],
                    color={'B':'#2066a8','C':'#c24d26'}[arm],linestyle=['-','--',':'][rep-1],marker='.',label=f'{arm}-{rep}')
        ax.set_xlabel(label);ax.set_ylabel('Original DUT branch points hit (%)');ax.grid(alpha=.2)
    if meta['mode']!='live':axes[0,0].text(.5,.5,'No live API tokens\nOffline plumbing only',ha='center',transform=axes[0,0].transAxes)
    handles,labels=axes[0,1].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',ncol=6)
    fig.suptitle('WBXBAR exploratory B/C — '+meta['mode'],y=1.02);fig.tight_layout()
    fig.savefig(run/'coverage-cost.png',dpi=160,bbox_inches='tight');fig.savefig(run/'coverage-cost.pdf',bbox_inches='tight');plt.close(fig)
    lines=[f'# WBXBAR B/C result — {meta["mode"]}', '',
        f'Run status: {meta["status"]}. Model generation requests: {meta["api_generation_calls"]}; token-count requests: {meta["api_count_requests"]}.',
        f'Simulation executions: {meta["simulation_executions"]}; physical cycles: {meta["executed_cycles"]}; compilations: {meta["compilations"]}.', '',
        '| Arm | Rep | Raw target round | Checker-complete target round | Final branch points |',
        '|---|---:|---|---|---:|']
    lines += [f'| {e["arm"]} | {e["repetition"]} | {e["first_raw_target_round"]} | {e["first_checker_complete_target_round"]} | {e["final_branch_covered"]} |' for e in endpoints]
    lines += ['', 'All failed and not-reached sessions are retained. Raw attainment is distinct from a checker-complete batch. '
        'Pending/ambiguous/error-boundary observations do not become verified passes. Repeated diagnostics are not distinct defect types.', '',
        'Token ROI = newly hit original DUT branch points since the seed / API-reported input-plus-output tokens × 1,000. '
        'Cached input and reasoning output are subsets, not added twice. Unknown usage remains flagged in raw logs.', '',
        'This is a known-easy-target exploratory comparison, with three sessions per arm and no length placebo. '
        'No statistical significance or isolated semantic benefit can be claimed from it. '
        'Ordinary offline traffic already reaches all targets. Active session time excludes other interleaved sessions and shared compilation; '
        'full wall/compile/preprocessing accounting is in metadata.json.']
    if meta['mode']!='live':lines+=['','**These are offline checks, not evidence about LLM coverage performance.**']
    (run/'report.md').write_text('\n'.join(lines)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);report(p.parse_args().run.resolve())
