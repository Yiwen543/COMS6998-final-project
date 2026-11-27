#!/usr/bin/env python3
"""Post-hoc native-trace checks of the ACTUAL scoped live monitor replies.

Independently audit the transcript first; deduplicate the qualified original
formula strings, then compare each against the original full-domain monitor
under the two guards and the unrestricted domain. Finite observations never
establish the symbolic classification or unrestricted RTL correctness.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from audit_egg_regression_live import audit
from check_egg_regression_physical import BASE, replay, require
from egg_regression_smt import fresh_compare, verify_result
from egg_regression_workload import ARCHIVE, load_versions
from egg_txn_observe import read_corpora


def run(run_dir, archive, corpus_path, controls_path):
    checked = audit(run_dir, archive)
    require(checked['mode'] == 'live', 'use actual live replies, not authored fixture controls')
    reference = load_versions(archive)['trial-01/initial']['monitors']['data_last']
    candidates = {}
    for item in checked['receipt_order']:
        group = checked['checked_history'][item['arm']]['calls']
        call = next(c for c in group if c['stage'] == item['stage'] and c['attempt'] == item['attempt'])
        if call['qualified']:
            candidates.setdefault(call['candidate'], []).append({**item, 'guard':
                checked['stage_comparison'][item['stage']-1]['guard']})
    require(candidates, 'no qualified original live monitor')
    rows = []
    for candidate, occurrences in candidates.items():
        ident = sha256(candidate.encode()).hexdigest()
        for guard in ('(eq data_n 4)', '(eq data_n 5)', 'true'):
            result = fresh_compare(reference, candidate, guard)
            verify_result(reference, candidate, guard, result)
            require(result['guard_status'] == 'sat' and result['relation'] != 'unknown', 'unresolved live comparison')
            require(not any(o['guard'] == guard for o in occurrences) or result['relation'] == 'equivalent',
                    'qualified monitor not equivalent in its actual assigned guard')
            rows.append({'key': sha256((ident+'\0'+guard).encode()).hexdigest(), 'candidate_sha256': ident,
                         'property': 'data_last', 'left': reference, 'right': candidate, 'guard': guard,
                         'expected_relation': result['relation'], 'actual_response_occurrences': occurrences,
                         'typed_comparison': result})
    corpus = read_corpora(corpus_path, controls_path)
    primary = {k: v for k, v in corpus.items() if k[0] == 'original' or k[0].startswith('F')}
    additional = {k: v for k, v in corpus.items() if k not in primary}
    a, b = replay(primary, rows), replay(additional, rows)
    for row, left, right in zip(rows, a['comparisons'], b['comparisons'], strict=True):
        for observed in (left, right):
            require(observed['counts']['old_ref_xor_true'] == 0 and observed['counts']['old_ref_xor_unknown'] == 0,
                    'archived original monitor disagrees with independent imperative reference')
        row['primary'], row['additional_controls'] = left, right
    return {'complete': True, 'new_api_calls': 0,
            'scope': 'Existing original and controlled functional RTL traces; only data_last monitor semantics, not full DUT formal verification.',
            'seed_archive_sha256': checked['original_archive_sha256'],
            'live_member_sha256': checked['member_sha256'],
            'unique_live_qualified_monitors': len(candidates), 'qualified_reply_occurrences': sum(map(len, candidates.values())),
            'corpus_sha256': {p.name: json.loads((p/'summary.json').read_text())['corpus_sha256']
                              for p in (corpus_path, controls_path)},
            'primary': {k: a[k] for k in ('traces', 'snapshots')},
            'additional_controls': {k: b[k] for k in ('traces', 'snapshots')}, 'comparisons': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--archive', type=Path, default=ARCHIVE)
    parser.add_argument('--corpus', type=Path, default=BASE/'frame-faults')
    parser.add_argument('--controls', type=Path, default=BASE/'frame-diagnostic-faults')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.run_dir, args.archive, args.corpus, args.controls)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')
    print(f"Checked {result['unique_live_qualified_monitors']} distinct live monitor strings on "
          f"{result['primary']['traces']} + {result['additional_controls']['traces']} native RTL traces.")
