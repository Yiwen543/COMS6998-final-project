"""New-trial descriptive outcomes; retain unresolved and not-reached sessions."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import statistics

from report_wbxbar_bc import report as base_report
from plot_wbxbar_costs import plot
from run_midterm_fixed import sha


def spread(values):
    values = [v for v in values if v is not None]
    return {'n': len(values), 'mean': statistics.mean(values) if values else None,
            'median': statistics.median(values) if values else None,
            'min': min(values) if values else None, 'max': max(values) if values else None}


def report(run):
    base_report(run)
    plot(run)
    data = json.loads((run / 'summary.json').read_text())
    config = json.loads((run / 'freeze.json').read_text())
    endpoints = json.loads((run / 'endpoints.json').read_text())
    rows, finals = data['rows'], []
    for endpoint in endpoints:
        rr = [r for r in rows if r['arm'] == endpoint['arm'] and r['repetition'] == endpoint['repetition']]
        if not rr:
            finals.append({**endpoint, 'final_verdict': 'not run'})
            continue
        last = rr[-1]
        checked = last['checker']
        finals.append({**endpoint, 'session_id': last['session_id'],
            'final_verdict': checked['verdict'], 'final_measurement_round': last['measurement_round'],
            'final_failure_instances': len(checked['failures']),
            'final_unknown_records': len(checked['unresolved']),
            'final_unknown_categories': dict(Counter(x['item'] for x in checked['unresolved'])),
            'final_assumption_violations': len(checked['assumption_violations']),
            'final_checker_scope': checked['counts'].get('checked_scope'),
            'final_property_status': checked['counts'].get('property_status'),
            'final_coverage': last['coverage'], 'api_tokens': last['api_tokens'],
            'executed_cycles': last['executed_cycles_including_replays'],
            'simulation_executions': last['simulator_executions'],
            'functional_diagnostics_are_not_adjudicated_defects': True})
    arms = {}
    for arm in config['arms']:
        group = [f for f in finals if f['arm'] == arm]
        arms[arm] = {'sessions': len(group),
            'final_verdicts': dict(Counter(f['final_verdict'] for f in group)),
            'target_not_reached': sum(f['first_raw_target_round'] == 'not reached' for f in group),
            'checker_complete_not_reached': sum(f['first_checker_complete_target_round'] == 'not reached' for f in group),
            'tokens_to_raw_target_reached_only': spread([f['tokens_at_first_raw_target'] for f in group]),
            'total_api_tokens': spread([f.get('api_tokens') for f in group]),
            'final_branch_points': spread([f['final_branch_covered'] for f in group])}
    result = {'mode': data['metadata']['mode'], 'status': data['metadata']['status'],
        'freeze_sha256': sha(run / 'freeze.json'), 'checker_sha256': config['checker_sha256'],
        'final_sessions': finals, 'arms': arms, 'metadata': data['metadata'],
        'comparison': 'Descriptive C versus B within this separately registered run. Not a historical paired comparison or statistical significance claim.',
        'notes': ['Not-reached and unresolved sessions retained; reached-only cost statistics must be read with not-reached counts.',
                  'Raw coverage is distinct from checker-complete attainment; scoped_pass retains declared exclusions.',
                  'No independent new DUT-defect adjudication. Repeated unknowns/alarms are not distinct defects.']}
    (run / 'reference-result.json').write_text(json.dumps(result, indent=2) + '\n')
    diagnostics = [{'arm': r['arm'], 'repetition': r['repetition'], 'round': r['round'],
        'measurement_fresh': r['measurement_fresh'], 'measurement_round': r['measurement_round'],
        'verdict': r['checker']['verdict'], 'failures': len(r['checker']['failures']),
        'unknowns': len(r['checker']['unresolved']),
        'assumptions': len(r['checker']['assumption_violations']),
        'verification_complete': r['verification_complete']} for r in rows]
    if diagnostics:
        with (run / 'diagnostics.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(diagnostics[0]))
            writer.writeheader(); writer.writerows(diagnostics)
    with (run / 'report.md').open('a') as stream:
        stream.write('\n## Frozen reference-checker outcomes\n\n')
        stream.write('| Arm | Rep | Final verdict | Unknown records | Failure instances |\n|---|---:|---|---:|---:|\n')
        for f in finals:
            stream.write(f"| {f['arm']} | {f['repetition']} | {f['final_verdict']} | {f.get('final_unknown_records', 'not run')} | {f.get('final_failure_instances', 'not run')} |\n")
        stream.write('\nFull unknown lists, property statuses and scope counts remain in each batch result and rounds JSONL. They are never recoded as passes. Final diagnostics are not independently established DUT defects.\n')
    print(json.dumps({'mode': result['mode'], 'status': result['status'], 'arms': arms}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--run', type=Path, required=True)
    report(p.parse_args().run.resolve())
