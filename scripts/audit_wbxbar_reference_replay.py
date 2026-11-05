"""Audit pins/counters/accounting independently of checker attribution changes."""
import argparse
from collections import Counter
import csv
import json
import re
import tempfile
import time
from pathlib import Path

from freeze_wbxbar_reference_replay import verify_registration, read, PRIOR
from replay_wbxbar_cancel import verify_replay_freeze
from run_midterm_fixed import ROOT, sha
from inventory_natural_coverage import load_all
from preflight_spi_host import identity
from wbxbar_exploratory_driver import FIELDS, parse, validate
from wbxbar_cancel_validation import worker


def categories(result, field, key):
    return dict(Counter(x[key] for x in result[field]))


def correlate(failure, after):
    """Evidence links only; absence or ambiguity must remain explicit."""
    slave = re.search(r'slave (\d+)', failure['detail'])
    candidates = []
    for i, u in enumerate(after['unresolved']):
        other = re.search(r'slave (\d+)', u['detail'])
        if u['cycle'] == failure['cycle'] and u['item'] == 'post_abort_forward' and slave and other and slave.group(1) == other.group(1):
            candidates.append(i)
    same_edge = [i for i, f in enumerate(after['failures']) if f['cycle'] == failure['cycle']]
    status = 'unique_post_abort_unknown' if len(candidates) == 1 else 'multiple_post_abort_unknowns' if candidates else 'same_cycle_new_failure' if same_edge else 'no_direct_same_cycle_match'
    return {'status': status, 'unresolved_indices': candidates, 'new_failure_indices': same_edge,
            'claim': 'Cycle/slave correspondence only, not independent confirmation or exclusion of a DUT defect.'}


def audit(run, output):
    start = time.perf_counter()
    frozen, original = verify_replay_freeze(run / 'freeze.json')
    registration = verify_registration(ROOT / frozen['registration'])
    source = ROOT / frozen['original_run']
    records = read(run / 'comparison.json')
    meta = read(run / 'metadata.json')
    if meta['status'] != 'complete' or meta['new_model_calls'] != 0 or meta['compilations'] != 0:
        raise ValueError('Replay incomplete or unexpected model/compilation work')
    expected = {(f'rep{rep}-{arm}', batch) for rep in (1, 2, 3) for arm in ('B', 'C')
                for batch in ['seed'] + ['round' + str(i) for i in range(1, 7)]}
    if {(r['session'], r['batch']) for r in records} != expected or len(records) != 42:
        raise ValueError('Replay schedule mismatch')
    manifest = read(source / 'shared/manifest.json')
    denominator = {tuple(x) for x in original['counter_identities']}
    inputs, rows, correspondence, scopes, new_failures = {}, [], [], {}, []
    cycles = 0
    for record in records:
        name = record['session'] + '/' + record['batch']
        current, old, prior = run / name, source / name, PRIOR / name
        if (current / 'actions.json').read_bytes() != (old / 'actions.json').read_bytes():
            raise ValueError('Changed saved actions: ' + name)
        actions = read(current / 'actions.json')['actions']
        validate(actions)
        vectors = ''.join(' '.join(format(a[k], 'x') for k in FIELDS) + '\n' for a in actions)
        if (current / 'vectors.txt').read_text() != vectors:
            raise ValueError('Changed vectors: ' + name)
        log = (current / 'simulation.log').read_text()
        trace, transport = parse(log, actions, manifest['inputs'], manifest['outputs'])
        if any(trace != read(p / 'trace.json') for p in (current, old, prior)):
            raise ValueError('Public pin mismatch: ' + name)
        raw = load_all(current / 'coverage.dat', manifest['sources'])
        if len(raw) != len(denominator) or {identity(x) for x in raw} != denominator or any(raw != read(p / 'raw-points.json') for p in (current, old, prior)):
            raise ValueError('Raw source counter mismatch: ' + name)
        execution = read(current / 'execution.json')
        count = sum(x.startswith('PRE ') for x in log.splitlines())
        if count != len(actions) or count != execution['executed_cycles'] or count != record['cycles']:
            raise ValueError('Cycle accounting mismatch: ' + name)
        if 'DRIVER_OK steps=' + str(count) not in log:
            raise ValueError('Incomplete driver: ' + name)
        cycles += count
        inputs[name] = trace
        before = read(old / 'result.json')
        previous = read(prior / 'checker-output.json')
        after = read(current / 'checker-output.json')
        if transport != record['transport'] or transport != before['transport']:
            raise ValueError('Transport ledger mismatch: ' + name)
        if before['checker']['verdict'] != record['old_verdict'] or after['verdict'] != record['new_verdict']:
            raise ValueError('Verdict summary mismatch')
        for key, field in [('new_failures', 'failures'), ('new_unresolved', 'unresolved'), ('new_assumption_violations', 'assumption_violations')]:
            if record[key] != len(after[field]):
                raise ValueError('Checker count mismatch')
        scopes[name] = after['counts']
        row = {'session': record['session'], 'batch': record['batch'], 'cycles': count,
            'original_verdict': before['checker']['verdict'], 'cancellation_replay_verdict': previous['verdict'],
            'reference_verdict': after['verdict'], 'original_failure_instances': len(before['checker']['failures']),
            'new_failure_instances': len(after['failures']), 'new_unknown_instances': len(after['unresolved']),
            'new_assumption_instances': len(after['assumption_violations']),
            'new_failure_categories': categories(after, 'failures', 'category'),
            'new_unknown_categories': categories(after, 'unresolved', 'item'),
            'new_assumption_categories': categories(after, 'assumption_violations', 'category'),
            'trace_sha256': sha(current / 'trace.json'), 'raw_counters_sha256': sha(current / 'raw-points.json'),
            'pins_equal_both_prior_runs': True, 'raw_counters_equal_both_prior_runs': True}
        rows.append(row)
        for failure in before['checker']['failures']:
            correspondence.append({'session': record['session'], 'batch': record['batch'], 'original_failure': failure,
                                   'reference_mapping': correlate(failure, after)})
        new_failures.extend({'session': record['session'], 'batch': record['batch'], 'failure': x} for x in after['failures'])
    if cycles != 8360 or cycles != meta['executed_cycles'] or meta['simulator_executions'] != 42:
        raise ValueError('Total replay accounting mismatch')
    with tempfile.TemporaryDirectory(prefix='wbxbar-reference-replay-audit-') as temp:
        fresh = worker(ROOT / frozen['candidate'], inputs, Path(temp) / 'checker')
    if fresh != read(run / 'checker/evaluations.json') or fresh['errors'] or not all(x['pass'] for x in fresh['selftests']):
        raise ValueError('Fresh checker execution mismatch or failure')
    for name, result in fresh['cases'].items():
        if result != read(run / name / 'checker-output.json'):
            raise ValueError('Per-batch checker result drift')
    verify_registration(ROOT / frozen['registration'])
    verify_replay_freeze(run / 'freeze.json')
    finals = [r for r in rows if r['batch'] == 'round6']
    rounds = [r for r in rows if r['batch'] != 'seed']
    summary = {'pass': True, 'scope': 'Replay measurement/integrity and exact checker execution; not independent DUT-defect attribution.',
        'batches_checked': 42, 'generated_round_batches': 36, 'raw_DUT_counters_per_batch': len(denominator),
        'simulator_executions': 42, 'executed_cycles': cycles, 'compilations': 0, 'new_model_calls': 0,
        'new_simulations_in_audit': 0, 'checker_batches_reexecuted_in_audit': 42, 'checker_selftests_passed': len(fresh['selftests']),
        'all_historical_hashes_preserved': True, 'historical_files_checked': len(registration['preserved_hashes']),
        'verdicts_all_batches': dict(Counter(r['reference_verdict'] for r in rows)),
        'verdicts_generated_rounds': dict(Counter(r['reference_verdict'] for r in rounds)),
        'final_verdicts': dict(Counter(r['reference_verdict'] for r in finals)), 'finals': finals,
        'original_repeated_failure_instances': len(correspondence),
        'original_final_failure_instances': sum(x['batch'] == 'round6' for x in correspondence),
        'old_alarm_correspondence': dict(Counter(x['reference_mapping']['status'] for x in correspondence)),
        'new_repeated_failure_instances': len(new_failures),
        'new_failure_categories': dict(Counter(x['failure']['category'] for x in new_failures)),
        'confirmed_new_DUT_defect_types': 0, 'defect_note': 'Raw checker categories are not confirmed defect types; no independent new-defect adjudication was performed.',
        'freeze_sha256': sha(run / 'freeze.json'), 'checker_sha256': sha(ROOT / frozen['candidate'] / 'checker.py'),
        'audit_source_sha256': sha(Path(__file__)), 'audit_wall_seconds': time.perf_counter() - start,
        'original_generation_budget_unchanged': True, 'primary_live_metrics_unchanged': True, 'new_live_BC_allowed': False}
    output.mkdir(parents=True, exist_ok=False)
    for name, value in [('audit', summary), ('batches', rows), ('diagnostic-correspondence', correspondence),
                        ('new-failure-instances', new_failures), ('property-scope-by-batch', scopes)]:
        (output / (name + '.json')).write_text(json.dumps(value, indent=2) + '\n')
    fields = [k for k in rows[0] if not isinstance(rows[0][k], dict)]
    with (output / 'batches.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({k: v for k, v in summary.items() if k != 'finals'}, indent=2))
    return summary


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    audit(a.run.resolve(), a.output.resolve())
