#!/usr/bin/env python3
"""Export measured run summaries and trajectories; this script makes no API calls."""
import argparse
import csv
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for path in sorted(args.directory.rglob('summary.json')):
        data = json.loads(path.read_text())
        if 'config' not in data or 'group' not in data['config']:
            continue
        config = data['config']
        initial = data.get('initial', {}).get('coverage', {}).get('branch', {})
        final = data.get('final', {}).get('coverage', {}).get('branch', {})
        kind = data.get('coverage_objective', 'branch')
        objective_initial = data.get('initial', {}).get('coverage', {}).get(kind, {})
        objective_final = data.get('final', {}).get('coverage', {}).get(kind, {})
        rows.append({
            'module': data.get('module', 'arbiter'), 'coverage_objective': kind,
            'initial_objective_covered': objective_initial.get('covered'),
            'final_objective_covered': objective_final.get('covered'),
            'raw_objective_total': objective_final.get('total'),
            'new_coverage_points': data.get('new_coverage_points', data.get('new_branch_points')),
            'group': config['group'], 'run_id': config['run_id'],
            'requested_model': config['model'], 'effort': config['effort'],
            'live_api': data['live_api'], 'simulator': data['simulator'],
            'initial_branch_covered': initial.get('covered'),
            'final_branch_covered': final.get('covered'),
            'raw_branch_total': final.get('total'),
            'new_branch_points': data.get('new_branch_points'),
            'api_attempts': data['api_attempts'],
            'simulator_executions': data['simulator_executions'],
            'checked_cycles': data['total_checked_cycles'],
            'input_tokens': data['measured_usage']['input_tokens'] if data['usage_complete'] else None,
            'output_tokens': data['measured_usage']['output_tokens'] if data['usage_complete'] else None,
            'token_roi': data['token_roi'],
            'wall_seconds': data['wall_seconds_including_preparation'],
            'stop_reason': data['stop_reason'],
            'summary_path': str(path)})
    if not rows:
        raise SystemExit('No agent summaries found; request previews are not measurements.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {len(rows)} runs to {args.output}')


if __name__ == '__main__':
    main()
