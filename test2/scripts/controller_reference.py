#!/usr/bin/env python3
"""Stage-gated Claude reference calls for the new controller; never candidates."""
import argparse
import json
from pathlib import Path
from common import ROOT, BASE, dump, sha
from reference_role import invoke

TASK = BASE / 'tasks/axis_length_fifo_v1'


def verify_files(files):
    for name, h in files.items():
        if sha(ROOT / name) != h:
            raise ValueError('Reference-stage input changed: ' + name)


def prepare_stage():
    formal = json.loads((TASK / 'qualification/formal-v2/summary.json').read_text())
    expected = [('always_true', 'bmc', 'PASS'), ('always_false', 'bmc', 'FAIL')]
    expected += [(name, mode, 'PASS') for name in ('reset', 'output_stall', 'status_stall')
                 for mode in ('bmc', 'prove', 'cover')]
    if [(r['property'], r['mode'], r['status']) for r in formal['results']] != expected:
        raise ValueError('Local interface calibration not ready')
    observed = json.loads((TASK / 'qualification/observations-v2/summary.json').read_text())
    if not all(observed['dual_simulator_agreement'].values()):
        raise ValueError('Defined observations differ across simulators')
    decision = json.loads((TASK / 'qualification/typed-v5/decision.json').read_text())
    if decision['status'] != 'semantic_gate_pass':
        raise ValueError('Semantic source gate incomplete')
    manifest = json.loads((TASK / 'input-manifest-v1.json').read_text())
    verify_files(manifest['files'])
    packet = TASK / 'reference/author-packet-v1'
    m = json.loads((packet / 'manifest.json').read_text())
    if sha(packet / 'prompt.txt') != m['prompt_sha256']:
        raise ValueError('Author prompt changed')
    inputs = [BASE / 'configs/controller_task_v2.json', TASK / 'input-manifest-v1.json',
              TASK / 'qualification/formal-v2/summary.json', TASK / 'qualification/typed-v5/decision.json',
              TASK / 'qualification/observations-v2/summary.json', packet / 'prompt.txt', packet / 'manifest.json',
              BASE / 'scripts/reference_role.py', Path(__file__)]
    files = dict(manifest['files'])
    files.update({str(p.relative_to(ROOT)): sha(p) for p in inputs})
    path = TASK / 'reference/stage-v1.json'
    if path.exists():
        raise FileExistsError('Reference stage already prepared')
    dump(path, {'status': 'ready_for_reference_author_only', 'reference_author_allowed': True,
         'candidate_generation_allowed': False, 'files': files,
         'author_calls': 1, 'fresh_review_calls': 1, 'max_usd_per_call': 4,
         'key_file': 'build/private/anthropic-crosscheck-key',
         'prompt_allowlist': ['specification.md', 'observer_contract.md'],
         'functional_reference_status': 'not_created_yet', 'script_sha256': sha(Path(__file__))})
    print(json.dumps({'stage': str(path), 'author_ready': True, 'candidate_generation_allowed': False}))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--prepare-stage', action='store_true')
    p.add_argument('--role', choices=['author', 'review'])
    a = p.parse_args()
    if a.prepare_stage:
        if a.role:
            raise ValueError('Prepare and call are separate operations')
        prepare_stage()
        return
    if not a.role:
        p.error('Choose --prepare-stage or --role')
    stage = json.loads((TASK / 'reference/stage-v1.json').read_text())
    verify_files(stage['files'])
    if a.role == 'author':
        if not stage['reference_author_allowed']:
            raise ValueError('Author stage not ready')
        packet = TASK / 'reference/author-packet-v1'
    else:
        packet = TASK / 'reference/review-packet-v1'
        m = json.loads((packet / 'manifest.json').read_text())
        if sha(packet / 'prompt.txt') != m['prompt_sha256']:
            raise ValueError('Review prompt changed')
    print(json.dumps(invoke(a.role, packet, TASK / 'reference' / (a.role+'-v1'))))


if __name__ == '__main__':
    main()
