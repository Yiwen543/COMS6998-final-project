#!/usr/bin/env python3
"""Account for checker-role work separately from experimental LLM stimulus."""
import argparse
import csv
import json
from pathlib import Path


def summarize(base):
    attempts=[]
    for name in ('claude-author-v1','claude-author-v2','revision-v3/author-call',
                 'revision-v3/independent-review','revision-v4/author-call','revision-v4/independent-review'):
        p=base/name/'metadata.json'
        if not p.exists():continue
        m=json.loads(p.read_text());u=m.get('usage')
        attempts.append({'path':name,'status':m['status'],'wall_seconds':m['wall_seconds'],
            'input_tokens':u.get('input_tokens',0) if u else None,
            'cache_creation_input_tokens':u.get('cache_creation_input_tokens',0) if u else None,
            'cache_read_input_tokens':u.get('cache_read_input_tokens',0) if u else None,
            'output_tokens':u.get('output_tokens',0) if u else None,
            'thinking_output_tokens_subset':u.get('output_tokens_details',{}).get('thinking_tokens') if u else None,
            'reported_cost_usd':m.get('total_cost_usd'),
            'models':list((m.get('model_usage') or {}).keys()), 'requested_model':m['requested_model']})
    cal=json.loads((base/'calibration/summary.json').read_text())
    repros=[json.loads((base/n/'evidence.json').read_text()) for n in ('config-switch-reproducer','config-switch-full-reproducer')]
    smoke=json.loads((base/'frozen-driver-smoke/result.json').read_text())
    controls=json.loads((base/'revision-v4/evaluation/control-accounting.json').read_text())
    rows=json.loads((base/'revision-v4/evaluation/summary.json').read_text())['cases']
    metrics={k:sum(a[k] or 0 for a in attempts) for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens','output_tokens','thinking_output_tokens_subset','reported_cost_usd')}
    result={'purpose':'Checker development and offline event qualification, not A/B/C performance results',
        'anthropic_cli_invocations':len(attempts),'completed_responses_with_usage':sum(a['input_tokens'] is not None for a in attempts),
        'attempts_with_unknown_usage':sum(a['input_tokens'] is None for a in attempts),
        'provider_usage_components_known_only':metrics,
        'token_policy':'Keep Anthropic input/cache-creation/cache-read fields separate. Thinking tokens are a subset of output, not an added total. Timed-out usage/cost remains unknown, never imputed as zero.',
        'attempts':attempts,'openai_calls':0,'experimental_stimulus_model_calls':0,
        'compilations':cal['compilations']+smoke['compilations'],
        'simulations':cal['total_simulations']+sum(r['simulations'] for r in repros)+smoke['simulator_executions'],
        'executed_cycles':cal['total_executed_cycles']+sum(r['executed_cycles'] for r in repros)+smoke['executed_cycles'],
        'compile_seconds':cal['compile_seconds']+smoke['compile_seconds'],
        'simulation_seconds':cal['simulation_seconds']+sum(sum(x['simulation_seconds'] for x in r['records'].values()) for r in repros)+smoke['simulation_seconds'],
        'simulation_accounting_scope':'Includes ready-handshake calibration probes, two simulators, 50- and 200-cycle reproducers, and frozen-driver smoke. Repository unit-test simulations are separate validation overhead.',
        'controls':controls,'clean_calibrated_event_cases':[n for n,v in rows.items() if n.startswith('calibration/') and v['verdict']=='scoped_pass' and v['events']],
        'spec_discrepancy_cases':[n for n,v in rows.items() if n.startswith('calibration/') and v['verdict']=='dut_violation'],
        'formal_abcp_ready':False,'primary_blocker':'No proved temporal-event/source-target bindings; previous raw source groups remain easy. Configuration-change switch excluded pending fuller adjudication.'}
    (base/'accounting.json').write_text(json.dumps(result,indent=2)+'\n')
    with (base/'checker-controls.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(controls['controls'][0]));writer.writeheader();writer.writerows(controls['controls'])
    return result


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--base',type=Path,required=True)
    args=cli.parse_args();d=summarize(args.base.resolve())
    print(json.dumps({k:d[k] for k in ('anthropic_cli_invocations','completed_responses_with_usage','attempts_with_unknown_usage',
        'provider_usage_components_known_only','compilations','simulations','executed_cycles','formal_abcp_ready')},indent=2))
