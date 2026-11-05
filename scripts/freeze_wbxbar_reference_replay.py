"""Register and freeze only saved-action replay of the reviewed reference checker."""
import argparse
import json
import subprocess
import sys
import platform
from pathlib import Path

from probe_wbxbar_cancel_boundary import verify_scope
from replay_wbxbar_cancel import verify_replay_freeze
from run_midterm_fixed import ROOT, sha
from wbxbar_experiment import verify_freeze

BASE = ROOT / 'results/wbxbar_reference_checker_20261104'
RUN = ROOT / 'results/wbxbar_exploratory_bc_20261104/live-v1'
PRIOR = ROOT / 'results/wbxbar_abort_contract_20261104/replay-v1'
FILES = ('checker.py', 'selftest.py', 'properties.json', 'contract.md')


def read(path):
    return json.loads(path.read_text())


def hashes(paths):
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(set(paths))}


def verify_registration(path):
    verify_scope()
    r = read(path)
    if r['new_model_calls'] != 0 or r['new_live_experiment_allowed'] is not False:
        raise ValueError('Replay-only registration required')
    for p, digest in r['preserved_hashes'].items():
        if sha(ROOT / p) != digest:
            raise ValueError('Historical evidence changed: ' + p)
    return r


def exact_review(folder, artifact, key):
    value = read(artifact)
    response = read(folder / 'response.json')['result'].strip()
    if response.startswith('```'):
        response = '\n'.join(response.splitlines()[1:-1])
    if json.loads(response) != value or value.get(key) is not True:
        raise ValueError('Review response mismatch or rejected')
    m = read(folder / 'metadata.json')
    if m['status'] != 'complete' or m['requested_model'] != 'claude-opus-5-5' or set(m['model_usage']) != {'claude-opus-5-5'}:
        raise ValueError('Review model/status mismatch')


def prepare(registration, freeze, bundle):
    scope = verify_scope()
    original = verify_freeze()
    gate = read(BASE / 'scoped-validation.json')
    if not gate.get('scoped_checker_gate_passed') or not gate.get('ready_for_replay_registration') or gate.get('blocking_findings'):
        raise ValueError('Scoped checker gate not passed')
    for p, digest in gate['evidence_sha256'].items():
        if sha(Path(p)) != digest:
            raise ValueError('Gate evidence drift')
    source = (ROOT / gate['candidate']).resolve()
    if any(sha(source / f) != gate['artifact_sha256'][f] for f in FILES):
        raise ValueError('Candidate drift')
    exact_review(BASE / 'termination-review-v1', BASE / 'termination-review-v1/review.json', 'ready_for_replay_registration')
    exact_review(BASE / 'documentation-v1/review-call', BASE / 'documentation-v1/review.json', 'ready_for_contract_addendum')
    if any(p.exists() for p in (registration, freeze, bundle)):
        raise ValueError('Never overwrite registration, freeze or candidate')
    binary = Path(read(RUN / 'rep1-B/round1/execution.json')['command'][0])
    old_meta = read(RUN / 'metadata.json')
    saved_batches = [RUN / f'rep{rep}-{arm}' / batch for rep in (1, 2, 3) for arm in ('B', 'C')
        for batch in ['seed'] + ['round' + str(i) for i in range(1, 7)]]
    if sum(len(read(p / 'actions.json')['actions']) for p in saved_batches) != 8360:
        raise ValueError('Saved cycle schedule differs')
    historical = [p for root in (RUN, PRIOR) for p in root.rglob('*') if p.is_file()]
    historical += [ROOT / 'configs/wbxbar_exploratory_bc_freeze_v1.json', ROOT / 'configs/wbxbar_cancel_replay_freeze_v1.json']
    reg = {'id': 'wbxbar_reference_replay_v1', 'status': 'preregistered_retrospective_replay_only',
        'source_run': str(RUN.relative_to(ROOT)), 'prior_cancel_replay': str(PRIOR.relative_to(ROOT)),
        'purpose': 'Reattribute saved actions using the independently reviewed exact-history reference checker; do not reinterpret this as newly generated B/C evidence.',
        'candidate_source': str(source.relative_to(ROOT)), 'scoped_gate_sha256': sha(BASE / 'scoped-validation.json'),
        'schedule': {'repetitions': [1, 2, 3], 'arms': ['B', 'C'], 'batches': ['seed'] + ['round' + str(i) for i in range(1, 7)], 'executions': 42, 'executed_cycles': 8360},
        'development_budget': scope['development_budget'], 'model_limits': scope['model_limits'],
        'targets': original['targets'], 'counter_identities': original['counter_identities'],
        'roles': scope['roles'], 'reset_policy': old_meta['simulation_policy'],
        'new_model_calls': 0, 'new_live_experiment_allowed': False, 'no_new_stimulus': True,
        'attribution_policy': 'Retain every raw verdict, failure, assumption and unknown. Match prior alarms only when evidence supports it; unmatched or changed categories are not silently called DUT fixes. Distinguish repeated diagnostics, categories and independently confirmed defects.',
        'stop_policy': 'Stop on incomplete simulation, changed pins, changed counter identities/counts, checker infrastructure errors, or frozen evidence drift; preserve partial logs.',
        'preserved_hashes': hashes(historical), 'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'working_tree_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True)),
        'tool_versions_from_original_compile': old_meta['versions'], 'binary_sha256': sha(binary),
        'replay_runtime': {'python': sys.version, 'platform': platform.platform()}}
    registration.write_text(json.dumps(reg, indent=2) + '\n')
    verify_registration(registration)
    bundle.mkdir(parents=True)
    for f in FILES:
        (bundle / f).write_bytes((source / f).read_bytes())
    (bundle / 'authorship.json').write_text(json.dumps({'role': 'Claude specification checker and contract authors',
        'source_candidate': str(source.relative_to(ROOT)), 'artifact_sha256': {f: sha(bundle / f) for f in FILES},
        'transport_only': 'Byte-for-byte bundle for existing replay worker; no GPT functional or contract edits.',
        'scoped_gate_sha256': sha(BASE / 'scoped-validation.json')}, indent=2) + '\n')
    paths = [registration, Path(__file__), ROOT / 'scripts/audit_wbxbar_reference_replay.py',
        ROOT / 'scripts/replay_wbxbar_cancel.py', ROOT / 'scripts/wbxbar_cancel_validation.py',
        ROOT / 'scripts/evaluate_spi_checker_candidate.py', ROOT / 'scripts/run_spi_checker_author.py',
        ROOT / 'scripts/wbxbar_exploratory_driver.py', ROOT / 'scripts/inventory_natural_coverage.py',
        ROOT / 'scripts/preflight_spi_host.py', binary, RUN / 'shared/manifest.json',
        BASE / 'scoped-validation.json', bundle / 'authorship.json', *[bundle / f for f in FILES],
        BASE / 'termination-review-v1/review.json', BASE / 'documentation-v1/review.json']
    frozen = {'status': 'frozen_for_retrospective_replay_only', 'registration': str(registration.relative_to(ROOT)),
        'candidate': str(bundle.relative_to(ROOT)), 'original_run': str(RUN.relative_to(ROOT)),
        'binary': str(binary.relative_to(ROOT)), 'new_model_stimulus_calls': 0, 'new_live_experiment_allowed': False,
        'attribution_scope': 'Reviewed reference-contract scope only; preserve all uncertainty and exclusions. No whole-IP proof or new B/C efficacy claim.',
        'hashes': hashes(paths), 'limits': gate['limitations'], 'nonblocking_documentation_notes': gate['nonblocking_documentation_notes']}
    freeze.write_text(json.dumps(frozen, indent=2) + '\n')
    verify_replay_freeze(freeze)
    return {'registration_sha256': sha(registration), 'freeze_sha256': sha(freeze), 'preserved_files': len(reg['preserved_hashes']), 'candidate_sha256': sha(bundle / 'checker.py')}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ('registration', 'freeze', 'bundle'):
        p.add_argument('--' + name, type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(prepare(a.registration.resolve(), a.freeze.resolve(), a.bundle.resolve()), indent=2))
