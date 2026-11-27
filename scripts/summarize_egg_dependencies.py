#!/usr/bin/env python3
"""Compare the two independently audited dependency experiments without rerunning solvers."""
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path

from audit_egg_regression import loads, read
from egg_dependency_workload import digest, require
from run_egg_dependencies import ARMS, TRIAGE_ARMS, without_times


def checked_run(root, arms):
    root = Path(root)
    audit = read(root / 'audit.json')
    require(audit['complete'] and audit['all_stores_rebuilt'] and audit['same_non_timing_summary']
            and not audit['native_search_invoked'] and list(arms) == audit['arms'], 'missing completed audit')
    require(audit['evidence_sha256'] == {f: digest(root / f) for f in ('protocol.json', 'groups.jsonl.gz', 'stores.json', 'summary.json')},
            'archived evidence digest differs from the audited record')
    summary, protocol = read(root / 'summary.json'), read(root / 'protocol.json')
    require(summary['complete'] and summary['new_api_calls'] == 0 and protocol['arms'] == list(arms), 'wrong experiment')
    return summary, protocol, audit


def summarize(primary, triage):
    first, p, a = checked_run(primary, ARMS)
    second, q, b = checked_run(triage, TRIAGE_ARMS)
    require(all(p[k] == q[k] for k in ('archive_sha256', 'live_archive_sha256', 'binary_sha256', 'workloads', 'group_policy', 'rules')),
            'primary and follow-up did not use the same frozen workload/engine')
    require(all(first[k] == second[k] == a[k] == b[k] for k in ('requests', 'groups')), 'mismatched workload size')
    aa, bb = without_times(first), without_times(second)
    table = {}
    for name, cases in p['workloads'].items():
        require(all(aa[name][arm] == bb[name][arm] for arm in ('egg_dependency', 'ordinary_dependency')),
                f'{name}: repeated baseline differs')
        rows = {**first['workloads'][name], **{k: v for k, v in second['workloads'][name].items() if k.endswith('_triage')}}
        require(all(v['correct'] == v['requests'] == len(cases) and not v['false_equivalent'] for v in rows.values()), 'incorrect classifications')
        table[name] = {'requests': len(cases), 'cohorts': dict(Counter(c['cohort'] for c in cases)),
                       'relations': dict(Counter(c['expected_relation'] for c in cases)), 'arms': {}}
        for arm, r in rows.items():
            table[name]['arms'][arm] = {
                'all_typed_checks': r['all_typed_checks'], 'fact_typed_checks': r['fact_typed_checks'],
                'full_discovery_groups': r['fact_counts'].get('full_discovery_groups', 0),
                'native_graphs': r['native_graph_counts'].get('graphs', 0),
                'nonidentity_equivalent': r['nonidentity_equivalent'],
                'nonidentity_equivalent_with_proof_route': r['nonidentity_equivalent_with_proof_route'],
                'nonidentity_equivalent_without_full_target_solver': r['nonidentity_equivalent_without_full_target_solver'],
                'history_scope': r['history_scope'], 'fresh_dependency_queries': r['fact_counts'].get('dependency_misses', 0),
                'dependency_outside_vocabulary_occurrences': r['fact_counts'].get('dependency_outside_vocabulary', 0),
                'triage_checked': r.get('triage_checked', 0), 'triage_discharge': r.get('triage_discharge', 0),
                'wall_seconds_single_run': r['wall_seconds']}
        eager, lazy = (rows[k]['all_typed_checks'] for k in ('egg_eager', 'egg_dependency_triage'))
        table[name]['egg_typed_reduction_from_eager_pct'] = round(100 * (eager - lazy) / eager, 2)
    # Inspect actual warm-path and invalidation costs, without treating
    # different fact query types or native proof replay steps as equal time.
    paths = {}
    with gzip.open(Path(triage) / 'groups.jsonl.gz', 'rt', encoding='utf8') as stream:
        for line in stream:
            g = loads(line)
            if g['workload'] == 'matrix':
                continue
            x = g['arms']['egg_dependency_triage']
            misses = sum(e['evidence']['counts']['cache_misses'] if e['kind'] == 'full_discovery'
                         else e['cache'] == 'miss' for e in x['fact_events'])
            paths.setdefault(g['workload'], []).append({'group': g['group'], 'guard': g['cases'][0]['guard'],
                'fact_cache_misses_including_feasibility': misses, 'native_graph': x['native'] is not None,
                'rows': [{'id': r['id'], 'via': r['via'], 'relation': r['relation'],
                          'triage_relation': r.get('triage', {}).get('relation'),
                          'first_lookup_status': r.get('lookup', {}).get('status'),
                          'replayed_edges': len(r.get('lookup', {}).get('edges', []))} for r in x['rows']]})
    return {'complete': True, 'requests': first['requests'], 'groups': first['groups'], 'new_api_calls': 0,
            'repeated_baseline_non_timing_counts_match': True, 'workloads': table, 'selected_triage_paths': paths,
            'scope': first['scope'], 'timing_note': 'One recorded run per experiment; no statistical wall-time claim.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--primary', type=Path, required=True)
    parser.add_argument('--triage', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = summarize(args.primary, args.triage)
    with args.output.open('x', encoding='utf8') as stream:
        json.dump(result, stream, indent=2, sort_keys=True); stream.write('\n')
