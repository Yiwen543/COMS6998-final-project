"""Summarize the audited retrospective replay; never launch a model or simulator."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path

from coverage import summary
from freeze_wbxbar_reference_replay import ROOT, PRIOR, read, sha, verify_registration
from preflight_spi_host import identity
from replay_wbxbar_cancel import verify_replay_freeze


def write_csv(path, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def report(run, audit, output):
    frozen, original = verify_replay_freeze(run / 'freeze.json')
    reg = verify_registration(ROOT / frozen['registration'])
    result, records = read(audit / 'audit.json'), read(audit / 'batches.json')
    if result['pass'] is not True or result['freeze_sha256'] != sha(run / 'freeze.json'):
        raise ValueError('Matching successful replay audit required')
    targets = {tuple(i) for group in original['targets'] for i in group['source_counter_identities']}
    scopes = read(audit / 'property-scope-by-batch.json')
    rows, clauses, hashes = [], [], {}
    finals_unknown, prior_unknown = Counter(), Counter()
    for record in records:
        name = record['session'] + '/' + record['batch']
        batch = run / name
        for artifact, field in [('trace.json', 'trace_sha256'), ('raw-points.json', 'raw_counters_sha256')]:
            if sha(batch / artifact) != record[field]:
                raise ValueError('Audited artifact changed: ' + name + '/' + artifact)
        raw = read(batch / 'raw-points.json')
        before = read(PRIOR / name / 'checker-output.json')
        after = read(batch / 'checker-output.json')
        if after['counts'] != scopes[name] or after['verdict'] != record['reference_verdict']:
            raise ValueError('Audited checker output changed: ' + name)
        if len(after['unresolved']) != record['new_unknown_instances'] or len(after['failures']) != record['new_failure_instances']:
            raise ValueError('Audited diagnostics changed: ' + name)
        counts = {identity(p): p['hits'] for p in raw}
        row = {k: record[k] for k in ['session', 'batch', 'cycles', 'original_verdict',
            'cancellation_replay_verdict', 'reference_verdict', 'original_failure_instances',
            'new_failure_instances', 'new_unknown_instances', 'new_assumption_instances']}
        row['prior_unknown_instances'] = len(before['unresolved'])
        for kind, metrics in summary(raw).items():
            for field, value in metrics.items():
                row[kind + '_' + field] = value
        row.update(targets_covered=sum(counts[t] > 0 for t in targets), targets_total=len(targets))
        row['target_reached'] = row['targets_covered'] == row['targets_total']
        checked = after['counts']['checked_scope']
        row.update({key: checked[key] for key in ['processed_rows', 'nonreset_rows',
            'effective_association_checked_rows', 'suspended_rows', 'rows_after_membership_death',
            'rows_beyond_input_boundary']})
        row['resource_exhaustions'] = len(checked['exhaustions'])
        row['input_boundary_present'] = after['counts']['input_validity_boundary'] is not None
        row['termination_boundary_present'] = after['counts']['termination_boundary'] is not None
        rows.append(row)
        for clause, status in after['counts']['property_status'].items():
            data = after['counts']['clause_scope'].get(clause, {})
            clauses.append({'session': record['session'], 'batch': record['batch'],
                'clause': clause, 'status': status,
                **{key: data.get(key) for key in ['raw_activations', 'activations', 'checked_activations',
                    'suspended_activations', 'post_death_activations', 'unknown_tag_records']}})
        if record['batch'] == 'round6':
            finals_unknown.update(x['item'] for x in after['unresolved'])
            prior_unknown.update(x['item'] for x in before['unresolved'])
        for path in [batch / 'raw-points.json', batch / 'trace.json', batch / 'checker-output.json',
                     PRIOR / name / 'checker-output.json']:
            hashes[str(path.relative_to(ROOT))] = sha(path)
    finals = [row for row in rows if row['batch'] == 'round6']
    first_hits = {session: next((int(r['batch'][5:]) if r['batch'] != 'seed' else 0
                    for r in rows if r['session'] == session and r['target_reached']), None)
                  for session in sorted({r['session'] for r in rows})}
    meta = read(run / 'metadata.json')
    for path in [audit / 'audit.json', audit / 'batches.json', audit / 'property-scope-by-batch.json',
                 run / 'metadata.json', run / 'freeze.json', Path(__file__)]:
        hashes[str(path.resolve().relative_to(ROOT))] = sha(path)
    result_summary = {
        'scope': 'Retrospective reattribution, not fresh matched B/C or formal certification.',
        'measurement_audit_pass': True, 'final_sessions': finals,
        'final_unknown_categories': dict(finals_unknown), 'final_unknown_records': sum(finals_unknown.values()),
        'prior_final_unknown_categories': dict(prior_unknown),
        'prior_final_unknown_records': sum(prior_unknown.values()),
        'first_target_round': first_hits,
        'all_batches_scope': {key: sum(r[key] for r in rows) for key in ['cycles', 'processed_rows',
            'nonreset_rows', 'effective_association_checked_rows', 'suspended_rows',
            'rows_after_membership_death', 'rows_beyond_input_boundary', 'resource_exhaustions',
            'input_boundary_present', 'termination_boundary_present', 'new_assumption_instances']},
        'extra_replay_cost': meta,
        'audit_wall_seconds': result['audit_wall_seconds'],
        'new_model_calls': 0, 'new_live_BC_allowed': False,
        'git_commit': reg['git_commit'], 'working_tree_dirty_at_freeze': reg['working_tree_dirty'],
        'input_hashes': hashes,
        'counting_notes': [
            'All-round totals repeat cumulative prefixes; final-session records are reported separately.',
            'Unknown records and clause activations are not distinct defect types or DUT source coverage.',
            'No hit is recorded as null; unfinished sessions are retained.',
            'Original live costs are unchanged; replay and audit costs are additional retrospective work.'],
    }
    output.mkdir(parents=True, exist_ok=False)
    write_csv(output / 'metrics.csv', rows)
    write_csv(output / 'final-sessions.csv', finals)
    write_csv(output / 'property-scope.csv', clauses)
    (output / 'summary.json').write_text(json.dumps(result_summary, indent=2) + '\n')
    print(json.dumps({k: result_summary[k] for k in ['measurement_audit_pass', 'final_unknown_records',
        'prior_final_unknown_records', 'first_target_round', 'all_batches_scope', 'new_model_calls']}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--audit', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    report(a.run.resolve(), a.audit.resolve(), a.output.resolve())
