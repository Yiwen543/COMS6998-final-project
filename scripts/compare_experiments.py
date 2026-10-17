#!/usr/bin/env python3
"""Compare live C/D runs at a common observed token budget, retaining overshoot."""
import argparse
import json
from pathlib import Path
from agent_core import dump


def snapshot(record, budget):
    if not record['live_api'] or not record['usage_complete']:
        raise ValueError('Comparison requires live runs with complete usage')
    eligible = [r for r in record['rounds'] if r.get('status') == 'completed'
                and r['cumulative_measured_tokens'] <= budget]
    last = eligible[-1] if eligible else None
    coverage = last['coverage'] if last else record['initial']['coverage']
    kind = record.get('coverage_objective', 'branch')
    initial = record['initial']['coverage'][kind]['covered']
    return {'coverage_objective': kind, 'new_coverage_points': coverage[kind]['covered'] - initial,
            'new_branch_points': coverage[kind]['covered'] - initial if kind == 'branch' else None,
            'coverage': coverage, 'last_completed_round_within_budget': last['round'] if last else 0,
            'tokens_at_snapshot': last['cumulative_measured_tokens'] if last else 0,
            'duplicate_inputs': sum(r.get('duplicate_input_count', 0) for r in eligible),
            'submitted_vectors': sum(r['batch_size'] for r in eligible),
            'total_observed_tokens_including_overshoot': record['measured_usage']['total_tokens'],
            'stop_reason': record['stop_reason'], 'preparation': record.get('preparation')}


def compare(c, d, budget):
    # run_id labels a paired repetition; it does not force identical API randomness.
    for key in ('dut_sha256', 'tb_sha256'):
        if c[key] != d[key]:
            raise ValueError(f'Mismatched {key}')
    if c.get('checker_sha256') != d.get('checker_sha256'):
        raise ValueError('Mismatched independent checker hash')
    if c.get('coverage_objective', 'branch') != d.get('coverage_objective', 'branch'):
        raise ValueError('Mismatched coverage objective')
    for key in c['config']:
        if key != 'group' and c['config'][key] != d['config'][key]:
            raise ValueError(f'Mismatched config: {key}')
    if (c['config']['group'], d['config']['group']) != ('C', 'D'):
        raise ValueError('Expected C then D')
    if c['stop_reason'] == 'error' or d['stop_reason'] == 'error':
        raise ValueError('Errored runs require separate failure analysis')
    cs, ds = snapshot(c, budget), snapshot(d, budget)
    return {'common_token_budget': budget, 'C': cs, 'D': ds,
            'paired_new_coverage_difference_C_minus_D': cs['new_coverage_points'] - ds['new_coverage_points'],
            'paired_new_branch_difference_C_minus_D': (cs['new_branch_points'] - ds['new_branch_points']
                if cs['coverage_objective'] == 'branch' else None),
            'initial_requests_identical': (
                c['rounds'][0]['request_sha256'] == d['rounds'][0]['request_sha256']
                if c['rounds'] and d['rounds']
                and c['rounds'][0].get('request_sha256')
                and d['rounds'][0].get('request_sha256') else None),
            'interpretation': 'One paired run is descriptive only; repeat across held-out designs before causal claims.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--c', required=True, type=Path)
    p.add_argument('--d', required=True, type=Path)
    p.add_argument('--tokens', required=True, type=int)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    if a.tokens <= 0 or a.output.exists():
        p.error('Use a positive budget and a new output file')
    result = compare(json.loads(a.c.read_text()), json.loads(a.d.read_text()), a.tokens)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    dump(a.output, result)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
