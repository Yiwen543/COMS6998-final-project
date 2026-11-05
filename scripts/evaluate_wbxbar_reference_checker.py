"""Audit an immutable Claude candidate on private synthetic controls only."""
import argparse
import copy
import json
import os
import resource
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate_spi_checker_candidate import load_candidate
from prepare_wbxbar_reference_checker import OUTPUT_BASE, verify_scope
from run_midterm_fixed import ROOT, sha


def matches(result, expected):
    if result.get('infrastructure_error') or result.get('verdict') != expected:
        return False
    required = ('failures', 'assumption_violations', 'unresolved', 'events')
    if any(not isinstance(result.get(key), list) for key in required) or not isinstance(result.get('counts'), dict):
        return False
    failures, invalid, unknown = (result[key] for key in required[:3])
    if expected == 'input_or_scope_invalid':
        return bool(invalid)
    if expected == 'dut_violation':
        if not failures:
            return False
        if invalid:
            # A later invalid suffix must not erase a definite valid-prefix fault.
            if not all(isinstance(x, dict) and type(x.get('cycle')) is int for x in invalid + failures):
                return False
            return any(x['cycle'] < min(e['cycle'] for e in invalid) for x in failures)
        return True
    if failures or invalid:
        return False
    return bool(unknown) if expected == 'unresolved' else not unknown


def limit_worker(candidate, inputs, output):
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    checker = load_candidate(candidate / 'checker.py')['check_rows']
    results = {}
    for name, case in json.loads(inputs.read_text()).items():
        try:
            results[name] = checker(copy.deepcopy(case['rows']), limits=copy.deepcopy(case['limits']))
        except Exception as error:
            results[name] = {'infrastructure_error': type(error).__name__, 'detail': str(error)}
    output.write_text(json.dumps(results, indent=2) + '\n')


def isolated(command, log):
    env = {k: v for k, v in os.environ.items() if not any(part in k for part in ('KEY', 'TOKEN', 'SECRET', 'PASSWORD'))}
    with tempfile.TemporaryDirectory(prefix='wbxbar-reference-eval-') as cwd:
        run = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, timeout=60)
    log.write_text(run.stdout + run.stderr)
    if run.returncode:
        raise RuntimeError('Checker worker failed; retained log ' + str(log))


def evaluate(candidate, output):
    verify_scope()
    metadata = json.loads((candidate / 'metadata.json').read_text())
    for name, digest in metadata['artifact_sha256'].items():
        if sha(candidate / name) != digest:
            raise ValueError('Claude candidate edited before evaluation')
    controls = OUTPUT_BASE / 'controls-v1'
    manifest = json.loads((controls / 'manifest.json').read_text())
    for name, digest in manifest['hashes'].items():
        if sha(Path(name)) != digest:
            raise ValueError('Private control provenance drift')
    output.mkdir(parents=True, exist_ok=False)
    commands = [
        [sys.executable, '-I', str(ROOT / 'scripts/evaluate_spi_checker_candidate.py'), '--worker',
         '--candidate', str(candidate), '--inputs', str(controls / 'inputs.json'), '--output', str(output / 'cases.json')],
        [sys.executable, '-I', str(Path(__file__).resolve()), '--limit-worker',
         '--candidate', str(candidate), '--inputs', str(controls / 'limit-tests.json'), '--output', str(output / 'limits.json')]]
    (output / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
    isolated(commands[0], output / 'cases-worker.log')
    isolated(commands[1], output / 'limits-worker.log')
    results = json.loads((output / 'cases.json').read_text())
    limits = json.loads((output / 'limits.json').read_text())
    rows = []
    for case in json.loads((controls / 'accounts.json').read_text()):
        actual = results['cases'][case['name']]
        rows.append({**case, 'actual': actual.get('verdict'), 'agreement': matches(actual, case['expected']),
                     'infrastructure_error': actual.get('infrastructure_error')})
    limit_rows = []
    for name, case in json.loads((controls / 'limit-tests.json').read_text()).items():
        limit_rows.append({'name': name, 'expected': case['expected'], 'actual': limits[name].get('verdict'),
                           'agreement': matches(limits[name], case['expected']),
                           'counts': limits[name].get('counts'), 'infrastructure_error': limits[name].get('infrastructure_error')})
    selftests = results['selftests']
    selftests_ok = isinstance(selftests, list) and bool(selftests) and all(x.get('pass') is True for x in selftests)
    summary = {'status': 'offline_control_agreement_not_certification',
               'candidate_sha256': metadata['artifact_sha256'], 'controls_manifest_sha256': sha(controls / 'manifest.json'),
               'selftests': selftests, 'selftests_ok': selftests_ok, 'worker_errors': results['errors'],
               'cases': rows, 'limit_cases': limit_rows,
               'normal_agreements': sum(x['agreement'] for x in rows), 'normal_total': len(rows),
               'limit_agreements': sum(x['agreement'] for x in limit_rows), 'limit_total': len(limit_rows),
               'all_control_agreements': selftests_ok and not results['errors'] and all(x['agreement'] for x in rows + limit_rows),
               'new_DUT_simulations': 0, 'new_API_calls': 0, 'fresh_code_review_required': True,
               'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    verify_scope()
    return {key: summary[key] for key in ('selftests_ok', 'normal_agreements', 'normal_total', 'limit_agreements', 'limit_total', 'all_control_agreements')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--inputs', type=Path)
    parser.add_argument('--limit-worker', action='store_true')
    args = parser.parse_args()
    if args.limit_worker:
        limit_worker(args.candidate.resolve(), args.inputs.resolve(), args.output.resolve())
    else:
        print(json.dumps(evaluate(args.candidate.resolve(), args.output.resolve()), indent=2))
