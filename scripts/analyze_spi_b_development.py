#!/usr/bin/env python3
"""Summarize a completed SPI B development run without modifying its evidence."""
import argparse
import csv
import json
from pathlib import Path


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def analyze(run):
    metadata = json.loads((run/'metadata.json').read_text())
    summary = json.loads((run/'summary.json').read_text())
    screen = json.loads((run/'input-screen.json').read_text())
    rows = read_jsonl(run/'rounds.jsonl')
    calls = read_jsonl(run/'calls.jsonl')
    counts = read_jsonl(run/'counts.jsonl')
    nontrivial = {g['eclass'] for g in screen['groups'] if g['nontrivial_egg_group']}
    input_tokens = sum((c.get('usage') or {}).get('input_tokens') or 0 for c in calls)
    output_tokens = sum((c.get('usage') or {}).get('output_tokens') or 0 for c in calls)
    repetitions, table, source_rows = [], [], []
    for rep in range(1, metadata['config']['repetitions']+1):
        rounds = [r for r in rows if r['repetition'] == rep]
        if not rounds:
            repetitions.append({'repetition': rep, 'status': 'not_run', 'nontrivial_target_round': 'not reached'})
            continue
        first, last = rounds[0], rounds[-1]
        hit_round = next((r['round'] for r in rounds if all(g['all_hit'] for g in r['groups']
                                                        if g['eclass'] in nontrivial)), None)
        repetitions.append({'repetition': rep, 'rounds_recorded': len(rounds),
            'groups_unhit_round_one': sum(not g['all_hit'] for g in first['groups']),
            'nontrivial_unhit_round_one': sum(not g['all_hit'] for g in first['groups'] if g['eclass'] in nontrivial),
            'nontrivial_target_round': hit_round if hit_round is not None else 'not reached',
            'final_coverage': last['coverage'], 'api_tokens': last['api_tokens'],
            'executed_cycles': last['executed_cycles_including_replays'],
            'simulations': last['simulator_executions'],
            'input_assumption_violations': sum(len(r['checker']['assumption_violations']) for r in rounds),
            'repeated_checker_failures_across_executions': sum(len(r['checker']['failures']) for r in rounds),
            'distinct_defect_categories': sorted({c for r in rounds for c in r['checker']['distinct_defects']})})
        for row in rounds:
            record = {k: row[k] for k in ('repetition', 'round', 'status', 'api_tokens', 'calls', 'failed_attempts',
                'executed_cycles_including_replays', 'simulator_executions', 'simulation_seconds', 'elapsed_run_seconds')}
            for kind, counter in row['coverage'].items():
                record[kind+'_covered'], record[kind+'_total'] = counter['covered'], counter['total']
            record['groups_unhit'] = sum(not g['all_hit'] for g in row['groups'])
            record['nontrivial_groups_unhit'] = sum(not g['all_hit'] for g in row['groups'] if g['eclass'] in nontrivial)
            seed_branch = screen['seed_coverage']['branch']['covered']
            record['new_branch_points'] = row['coverage']['branch']['covered']-seed_branch
            record['token_roi'] = 1000*record['new_branch_points']/row['api_tokens'] if row['api_tokens'] else None
            table.append(record)
        for group in screen['groups']:
            if not group['qualified_source_group']:
                continue
            members = [m for m in group['members'] if m['id'] in group['qualified_member_ids']]
            for index, member in enumerate(members):
                found = next((r['round'] for r in rounds if next(g for g in r['groups'] if g['eclass'] == group['eclass'])['raw_source_hits'][index] > 0), None)
                point = member['mapping']['point']
                source_rows.append({'repetition': rep, 'group': group['eclass'], 'nontrivial_group': group['nontrivial_egg_group'],
                    **{k: point[k] for k in ('source', 'line', 'column', 'type', 'outcome', 'hierarchy')},
                    'first_hit_round': found if found is not None else 'not reached'})
    if metadata['mode'] == 'live' and sum(r.get('api_tokens', 0) or 0 for r in repetitions) != input_tokens+output_tokens:
        raise AssertionError('Per-call tokens disagree with cumulative per-repetition totals')
    late = sum(r.get('nontrivial_unhit_round_one', 0) >= 1 for r in repetitions)
    result = {'mode': metadata['mode'], 'original_B_gate': summary['gate'],
        'nontrivial_readiness_repetitions': late, 'required_nontrivial_readiness_repetitions': 2,
        'ready_for_formal_abcp': metadata['mode'] == 'live' and summary['gate']['passed'] and late >= 2,
        'repetitions': repetitions, 'api_input_tokens': input_tokens, 'api_output_tokens': output_tokens,
        'api_total_tokens': input_tokens+output_tokens,
        'cached_input_tokens_subset': sum((c.get('usage') or {}).get('cached_input_tokens') or 0 for c in calls),
        'reasoning_output_tokens_subset': sum((c.get('usage') or {}).get('reasoning_output_tokens') or 0 for c in calls),
        'calls_with_unknown_usage': sum((c.get('usage') or {}).get('input_tokens') is None for c in calls),
        'api_generation_requests': metadata['api_model_calls'], 'token_count_requests': metadata['count_requests'],
        'recorded_attempts': len(calls), 'accepted_attempts': sum(c.get('accepted', False) for c in calls),
        'failed_attempts': sum(not c.get('accepted', False) for c in calls),
        'compilations': metadata['compilations'], 'compile_seconds': metadata['compile_seconds'],
        'total_simulations': sum(r.get('simulations', 0) for r in repetitions),
        'total_executed_cycles': sum(r.get('executed_cycles', 0) for r in repetitions),
        'simulation_seconds': sum(r['simulation_seconds'] for r in rows
                                  if r['round'] == metadata['config']['rounds']),
        'total_wall_seconds': summary['elapsed_seconds'],
        'token_count_wall_seconds': sum(c['seconds'] for c in counts),
        'model_latency_seconds': sum(c.get('latency_seconds', 0) for c in calls),
        'models_returned': sorted({c.get('returned_model') for c in calls if c.get('returned_model')}),
        'interpretation': 'B-only development, not a C-versus-B effect estimate. Cached/reasoning tokens are subsets, not extra totals.'}
    return result, table, source_rows


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--run', type=Path, required=True)
    args = cli.parse_args()
    run = args.run.resolve()
    result, rows, sources = analyze(run)
    (run/'analysis.json').write_text(json.dumps(result, indent=2)+'\n')
    for name, records in [('rounds.csv', rows), ('source_first_hits.csv', sources)]:
        with (run/name).open('w') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 4, figsize=(16, 3.4))
    for rep in sorted({r['repetition'] for r in rows}):
        items = [r for r in rows if r['repetition'] == rep]
        for ax, field, xlabel in zip(axes, ['api_tokens', 'executed_cycles_including_replays', 'simulator_executions',
                                          'elapsed_run_seconds'],
                                   ['API input + output tokens', 'Executed cycles (all replays)', 'Simulator executions',
                                    'Elapsed run seconds (sequential reps)']):
            ax.plot([r[field] for r in items], [r['branch_covered'] for r in items], marker='o', label=f'B repetition {rep}')
            ax.set_xlabel(xlabel)
            ax.set_ylabel('Covered original DUT branch points / 160')
            ax.grid(alpha=.25)
    axes[0].legend(fontsize=8)
    fig.suptitle('SPI controller: B-only development (no C trial)')
    fig.tight_layout()
    fig.savefig(run/'coverage_cost.png', dpi=180)
    plt.close(fig)
    print(json.dumps({k: result[k] for k in ('ready_for_formal_abcp', 'api_total_tokens', 'api_generation_requests',
        'total_simulations', 'total_executed_cycles')}, indent=2))


if __name__ == '__main__':
    main()
