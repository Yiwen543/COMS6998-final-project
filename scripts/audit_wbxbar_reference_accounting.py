"""Independent per-round cost/ROI reconstruction; no model or simulator calls."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path

from run_midterm_fixed import sha
from run_spi_core_b_development import token_totals
from wbxbar_reference_experiment import verify_freeze, read


def audit(run, output):
    config = verify_freeze(run / 'freeze.json')
    data = read(run / 'summary.json')
    meta, rows = data['metadata'], data['rows']
    if meta['mode'] != 'live':
        raise ValueError('Live accounting evidence required')
    calls = [json.loads(line) for line in (run / 'calls.jsonl').read_text().splitlines()]
    counts = [json.loads(line) for line in (run / 'counts.jsonl').read_text().splitlines()]
    if len(counts) != len(calls):
        raise ValueError('Count/attempt ledger mismatch')
    for call, count in zip(calls, counts):
        if any(call[k] != count[k] for k in ('arm', 'repetition', 'round', 'attempt')):
            raise ValueError('Count/attempt association mismatch')
        if 'input_tokens' in count and call.get('counted_input_tokens') != count['input_tokens']:
            raise ValueError('Counted input mismatch')
        if call['generation_requested'] and call['counted_input_tokens'] > config['model_limits']['input_tokens']:
            raise ValueError('Input cap violated')
        usage = call['usage']
        for subset, total in [('cached_input_tokens', 'input_tokens'), ('reasoning_output_tokens', 'output_tokens')]:
            if usage.get(subset) is not None and usage.get(total) is not None and usage[subset] > usage[total]:
                raise ValueError('Token subset exceeds total')
        if usage.get('total_tokens') is not None and usage.get('input_tokens') is not None and usage.get('output_tokens') is not None:
            if usage['total_tokens'] != usage['input_tokens'] + usage['output_tokens']:
                raise ValueError('API total inconsistent with input plus output')
    seen = []
    for row in rows:
        rep, arm, rnd = row['repetition'], row['arm'], row['round']
        own = [c for c in calls if (c['repetition'], c['arm']) == (rep, arm) and c['round'] <= rnd]
        tokens = token_totals(own)
        if tokens != row['api_usage_cumulative'] or row['api_tokens'] != tokens['input_tokens'] + tokens['output_tokens']:
            raise ValueError('Cumulative per-session tokens differ')
        if row['attempts'] != len(own) or row['failed_attempts'] != sum(not c['accepted'] for c in own):
            raise ValueError('Attempt accounting differs')
        generated = sum(len(c['actions']) for c in own if c['accepted'])
        if generated != row['unique_generated_cycles']:
            raise ValueError('Generated-cycle accounting differs')
        folder = run / f'rep{rep}-{arm}'
        paths = [folder / 'seed/execution.json'] + [folder / f'round{i}/execution.json' for i in range(1, rnd + 1)]
        executions = [read(p) for p in paths if p.exists()]
        if sum(e['executed_cycles'] for e in executions) != row['executed_cycles_including_replays'] or len(executions) != row['simulator_executions']:
            raise ValueError('Per-session simulator accounting differs')
        if not math.isclose(sum(e['simulation_seconds'] for e in executions), row['simulation_seconds'], abs_tol=1e-9):
            raise ValueError('Simulation-time accounting differs')
        seed = read(folder / 'seed/raw-points.json')
        baseline = sum(p['type'] == 'branch' and p['hits'] > 0 for p in seed)
        newly = row['coverage']['branch']['covered'] - baseline
        if newly != row['new_branch_points']:
            raise ValueError('New branch-point accounting differs')
        expected = 1000 * newly / row['api_tokens'] if row['api_tokens'] else None
        actual = row['token_roi_new_branch_points_per_1000']
        if expected is None and actual is not None or expected is not None and not math.isclose(expected, actual, abs_tol=1e-9):
            raise ValueError('Token ROI differs')
        if sum(c['request_wall_seconds'] for c in own) + row['simulation_seconds'] > row['active_wall_seconds'] + .1:
            raise ValueError('Active wall time omits API/simulation cost')
        if row['checker']['verdict'] != 'scoped_pass' and row['verification_complete']:
            raise ValueError('Unresolved/violating batch marked complete')
        seen.append((rep, arm, rnd))
    finals = [r for r in rows if r['round'] == config['development_budget']['rounds']]
    if sum(r['active_wall_seconds'] for r in finals) + meta['compile_seconds'] > meta['elapsed_seconds'] + .1:
        raise ValueError('Full wall time inconsistent with session/compile accounting')
    result = {'pass': True, 'rounds_checked': len(seen), 'api_generation_calls': meta['api_generation_calls'],
        'api_count_requests': len(counts), 'attempts': len(calls),
        'failed_attempts': sum(not c['accepted'] for c in calls),
        'total_api_usage': token_totals(calls),
        'cached_input_tokens_subset': sum(c['usage'].get('cached_input_tokens') or 0 for c in calls),
        'reasoning_output_tokens_subset': sum(c['usage'].get('reasoning_output_tokens') or 0 for c in calls),
        'final_verdicts': dict(Counter(r['checker']['verdict'] for r in finals)),
        'new_simulations': 0, 'new_model_calls': 0,
        'producer_sha256': sha(Path(__file__)),
        'input_hashes': {str(p.relative_to(run)): sha(p) for p in [run / 'freeze.json', run / 'summary.json', run / 'calls.jsonl', run / 'counts.jsonl']}}
    if output.exists():
        raise ValueError('Never overwrite audit')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'input_hashes'}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    audit(a.run.resolve(), a.output.resolve())
