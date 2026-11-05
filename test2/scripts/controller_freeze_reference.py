#!/usr/bin/env python3
"""Freeze reviewed Claude reference and every hidden outcome; never enable live."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import shutil
from common import ROOT, BASE, dump, sha

TASK = BASE / 'tasks/axis_length_fifo_v1'


def first_failure(result):
    phase = {'pre': 0, 'post': 1, 'end': 2}
    failures = result.get('failures', [])
    return min(failures, key=lambda f: (f['cycle'], phase[f['phase']])) if failures else None


def freeze():
    ref = TASK / 'reference'
    review = json.loads((ref / 'review-v2/review.json').read_text())
    if review['decision'] != 'accept_with_scope' or any(f['severity'] == 'blocking' for f in review['findings']):
        raise ValueError('Independent review has not accepted the scope')
    evaluation = json.loads((ref / 'evaluation-v2/evaluations.json').read_text())
    summary = json.loads((ref / 'evaluation-v2/summary.json').read_text())
    if (len(summary['selftests']) < 50 or not all(v is True for v in summary['selftests'].values()) or
            not summary['finite_controls_match'] or len(summary['baseline_verdicts']) != 18 or
            any(v != 'PASS' for v in summary['baseline_verdicts'].values())):
        raise ValueError('Reference selftests/controls/baselines incomplete')
    original = json.loads((TASK / 'input-manifest-v1.json').read_text())
    for name, h in original['files'].items():
        if sha(ROOT / name) != h:
            raise ValueError('Task input changed: ' + name)
    aligned = json.loads((ref / 'alignment-stage-v2.json').read_text())
    for name, h in aligned['files'].items():
        if sha(ROOT / name) != h:
            raise ValueError('Reference contract changed: ' + name)
    source = ref / 'author-strengthen-v1'
    if sha(source / 'checker.py') != evaluation['checker_sha256']:
        raise ValueError('Evaluated checker changed')
    catalog = json.loads((TASK / 'private/mutant-catalog-v1.json').read_text())['faults']
    cases = evaluation['cases']
    eligibility = []
    for f in catalog:
        if sha(ROOT / f['source']) != f['sha256']:
            raise ValueError('Hidden source changed')
        for simulator in ('iverilog', 'verilator'):
            for number in range(1, 7):
                trace = f'heldout_{number:02d}'
                key = f'private/mutant-observations-v1/{f["id"]}/{simulator}/{trace}/rows.json'
                result = cases[key]
                first = first_failure(result)
                sampled = [x for x in result.get('failures', []) if x['phase'] in ('pre', 'post')]
                eligibility.append({'mutant': f['id'], 'stratum': f['stratum'], 'simulator': simulator,
                    'trace': trace, 'reference_verdict': result['verdict'], 'first_failure': first,
                    'sampled_safety_eligible': result['verdict'] == 'FAIL' and bool(sampled),
                    'finite_completion_only': result['verdict'] == 'FAIL' and not sampled,
                    'unknown_records': len(result.get('unknown', [])), 'rows_sha256': sha(TASK / key),
                    'policy': 'PASS here means no reference-confirmed violation on this fixed trace, not mutant equivalence or reachability proof'})
    if len(eligibility) != 144 or len(catalog) != 12:
        raise ValueError('Missing registered fault/trace outcomes')
    out = ref / 'frozen-v2'
    out.mkdir(exist_ok=False)
    for name in ('checker.py', 'selftest.py', 'contract.md', 'properties.json'):
        shutil.copyfile(source / name, out / name)
    shutil.copyfile(ref / 'review-v2/review.json', out / 'review.json')
    dump(out / 'fault-eligibility.json', eligibility)
    dump(out / 'scope-notes.json', {
        'evidence_counts': {'independent_finite_controls': 20, 'correct_trace_controls': 18,
                            'hidden_mutant_trace_cases': 144, 'evaluation_cases_total': 182},
        'review_wording_correction': 'The review calls182 evaluations control cases; only20 are independent synthetic controls. All original review text is preserved.',
        'limits': 'Use only the accepted finite-trace reference scope. Pre samples during reset, post/pre between-edge continuity and channel diagnostics after failure/X have the retained limitations in review.json. No claim of complete oracle soundness or defect freedom.'})
    by_sim = {}
    for sim in ('iverilog', 'verilator'):
        records = [r for r in eligibility if r['simulator'] == sim]
        observable = sorted({r['mutant'] for r in records if r['sampled_safety_eligible']})
        by_sim[sim] = {'raw_faults': len(catalog), 'raw_fault_trace_pairs': len(records),
                       'verdicts': dict(Counter(r['reference_verdict'] for r in records)),
                       'sampled_eligible_pairs': sum(r['sampled_safety_eligible'] for r in records),
                       'observable_faults': observable,
                       'not_activated_or_unresolved_faults_retained': sorted({f['id'] for f in catalog} - set(observable))}
    paths = [TASK / 'input-manifest-v1.json', TASK / 'private/mutant-catalog-v1.json',
             TASK / 'public/specification_v2.md', TASK / 'public/observer_contract_v2.md',
             ref / 'review-v2/review.json', ref / 'evaluation-v2/evaluations.json',
             ref / 'evaluation-v2/summary.json', ref / 'alignment-stage-v2.json',
             TASK / 'qualification/typed-v5/proof/proof.json', TASK / 'qualification/typed-v5/screen/screen.json',
             TASK / 'qualification/typed-v5/screen/egg.json', TASK / 'qualification/formal-v2/summary.json']
    paths += list(out.iterdir())
    paths += list((TASK / 'qualification/observations-v2').glob('*/*/rows.json'))
    paths += list((TASK / 'qualification/observations-v2/verilator').glob('*/raw-points.json'))
    paths += list((TASK / 'private/observations').glob('*/*/rows.json'))
    paths += list((TASK / 'private/mutant-observations-v1').glob('*/*/*/rows.json'))
    paths += [ROOT / f['source'] for f in catalog]
    artifacts = dict(original['files'])
    artifacts.update({str(p.relative_to(ROOT)): sha(p) for p in paths})
    dump(out / 'freeze.json', {'status': 'reviewed_reference_and_hidden_evidence_frozen_not_live',
         'checker_sha256': sha(out / 'checker.py'), 'artifact_sha256': artifacts,
         'independent_review': review['decision'], 'accepted_scope': review['accepted_scope'],
         'review_findings_retained': review['findings'], 'author_selftests': len(summary['selftests']),
         'independent_controls': 20, 'correct_trace_controls': 18, 'faults_raw': 12,
         'fault_observability_by_simulator': by_sim, 'candidate_generation_allowed': False,
         'limitations': ['Finite reference controls and simulation are not a complete proof of checker soundness.',
                        'All unactivated, incomplete and unknown outcomes remain in raw denominators.',
                        'Reference eligibility is not a generated-monitor detection score.']})
    for name, h in artifacts.items():
        if sha(ROOT / name) != h:
            raise ValueError('Post-freeze integrity mismatch')
    # The user authorized keeping this key through repairs/reviews, then cleanup.
    private = ROOT / 'build/private'
    if list(private.glob('controller-key-*')):
        raise RuntimeError('A reference call still owns a credential working copy')
    (private / 'anthropic-crosscheck-key').unlink(missing_ok=True)
    calls = []
    for name in ['author-v1', 'author-repair-v1', 'review-v1', 'author-strengthen-v1', 'review-v2']:
        m = json.loads((ref / name / 'metadata.json').read_text())
        calls.append(dict(artifact=name, **{k: m.get(k) for k in ['role', 'status', 'wall_seconds', 'total_cost_usd', 'session_id', 'usage_status']}))
    dump(TASK / 'qualification/qualification-summary-v1.json', {
         'status': 'offline_task_reference_and_hidden_corpus_qualified',
         'reference_freeze_sha256': sha(out / 'freeze.json'), 'reference_checker_sha256': sha(out / 'checker.py'),
         'reference_calls_including_failure': calls, 'reported_reference_cost_usd': sum(c['total_cost_usd'] for c in calls if c['total_cost_usd'] is not None),
         'unknown_cost_calls': sum(c['total_cost_usd'] is None for c in calls),
         'hidden_observability': by_sim, 'main_staged_key_removed_after_task_completion': not (private / 'anthropic-crosscheck-key').exists(),
         'candidate_live_allowed': False, 'C_B_effect_measured': False,
         'remaining_live_gates': ['New candidate ABI/replay/runner boundary and every-round release tests',
                                  'Actual provider input-token count and final immutable live registration']})
    print((TASK / 'qualification/qualification-summary-v1.json').read_text())


if __name__ == '__main__':
    freeze()
