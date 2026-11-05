"""Evaluate immutable Claude source with private controls and original DUT traces."""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from run_midterm_fixed import ROOT, sha


def evaluate(candidate, controls, output):
    authorship = json.loads((candidate / 'authorship.json').read_text())
    for name, digest in authorship['artifact_sha256'].items():
        if sha(candidate / name) != digest: raise ValueError('Author artifact changed: ' + name)
    manifest = json.loads((controls / 'manifest.json').read_text())
    if manifest['inputs_sha256'] != sha(controls / 'private-inputs.json'):
        raise ValueError('Private control drift')
    data = json.loads((controls / 'private-inputs.json').read_text())
    ordinary = ROOT / 'results/wbxbar_conditional_20261104/ordinary-v1'
    for row in json.loads((ordinary / 'summary.json').read_text())['cases']:
        trace = json.loads((ordinary / row['case'] / 'verilator/trace.json').read_text())
        data['dut/' + row['case']] = [{k: t[k] for k in ('cycle','pre','post')} for t in trace]
    output.mkdir(parents=True, exist_ok=False)
    inputs = output / 'private-inputs.json'
    inputs.write_text(json.dumps(data, separators=(',', ':')) + '\n')
    command = [sys.executable, '-I', str(ROOT / 'scripts/evaluate_spi_checker_candidate.py'),
               '--worker', '--candidate', str(candidate), '--inputs', str(inputs),
               '--output', str(output / 'evaluations.json')]
    env = {k:v for k,v in os.environ.items() if not any(x in k for x in ('KEY','TOKEN','SECRET','PASSWORD'))}
    with tempfile.TemporaryDirectory(prefix='wbxbar-checker-eval-') as cwd:
        result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, timeout=60)
    (output / 'worker.log').write_text(result.stdout + result.stderr)
    if result.returncode: raise RuntimeError('Checker worker failed; log retained')
    evaluated = json.loads((output / 'evaluations.json').read_text())
    clean = lambda r: not any(r.get(k) for k in ('failures','assumption_violations','infrastructure_error'))
    passed = lambda r: clean(r) and r.get('verdict') == 'scoped_pass' and not r.get('unresolved')
    accounts = []
    for control in manifest['controls']:
        r = evaluated['cases'][control['name']]
        row = {**control, 'verdict': r.get('verdict'), 'no_false_alarm': clean(r),
               'scoped_pass': passed(r), 'failures': len(r.get('failures', [])),
               'assumptions': len(r.get('assumption_violations', [])),
               'infrastructure_error': r.get('infrastructure_error')}
        if control['kind'] == 'single_fault':
            baseline = evaluated['cases'][control['baseline']]
            row['baseline_scoped_pass'] = passed(baseline)
            row['credited_detection'] = passed(baseline) and bool(r.get('failures')) and not r.get('assumption_violations') and not r.get('infrastructure_error')
        if control['kind'] == 'incomplete':
            row['pending_explicit'] = bool(r.get('unresolved')) and r.get('verdict') != 'scoped_pass'
        if control['kind'] == 'invalid_environment':
            row['input_violation_recognized'] = bool(r.get('assumption_violations'))
        accounts.append(row)
    summary = {'status': 'evaluated_not_frozen', 'checker_sha256': sha(candidate / 'checker.py'),
        'checker_author': authorship['author'], 'control_author': 'GPT/Codex',
        'selftests': evaluated['selftests'], 'worker_errors': evaluated['errors'], 'controls': accounts,
        'cases': evaluated['cases'], 'live_B_allowed': False, 'live_C_allowed': False,
        'counts': {'hand_positives': sum(c['kind']=='positive' for c in accounts),
                   'positive_no_false_alarm': sum(c['kind']=='positive' and c['no_false_alarm'] for c in accounts),
                   'positive_scoped_pass': sum(c['kind']=='positive' and c['scoped_pass'] for c in accounts),
                   'single_faults': sum(c['kind']=='single_fault' for c in accounts),
                   'credited_detections': sum(c.get('credited_detection',False) for c in accounts),
                   'actual_dut_traces': sum(n.startswith('dut/') for n in data),
                   'actual_dut_clean': sum(n.startswith('dut/') and clean(r) for n,r in evaluated['cases'].items()),
                   'infrastructure_errors': sum(bool(r.get('infrastructure_error')) for r in evaluated['cases'].values())},
        'hashes': {str(p):sha(p) for p in [candidate/'authorship.json', candidate/'checker.py',
                    controls/'manifest.json', inputs, Path(__file__), ROOT/'scripts/evaluate_spi_checker_candidate.py']},
        'limits': 'Hand positives/control validity must be independently reviewed. Actual DUT traces are observations, never presumed golden. No source-target proof, new DUT simulation, live stimulus call or checker edit here.'}
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary['counts'], indent=2))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ('candidate','controls','output'): parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    evaluate(args.candidate.resolve(), args.controls.resolve(), args.output.resolve())
