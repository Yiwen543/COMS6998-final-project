#!/usr/bin/env python3
"""Compare two completed dependency runs; report differences, not platform speedups.

The per-run audit validates evidence; this read-only analysis distinguishes
proof/semantic differences from native graph metadata and timing. A different
valid proof on another machine is not itself an invalid result.
"""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf8'))


def audited_run(root):
    audit = read(root / 'audit.json')
    artifacts = ('protocol.json', 'groups.jsonl.gz', 'stores.json', 'summary.json')
    if (not all(audit[k] for k in ('complete', 'all_stores_rebuilt', 'same_non_timing_summary'))
            or audit['native_search_invoked'] or audit['new_api_calls'] != 0
            or audit['evidence_sha256'] != {f: digest(root / f) for f in artifacts}):
        raise ValueError(f'{root}: missing complete matching audit receipt')
    with gzip.open(root / 'groups.jsonl.gz', 'rt', encoding='utf8') as stream:
        groups = [json.loads(line) for line in stream]
    summary = read(root / 'summary.json')
    if (len(groups) != summary['groups'] or not summary['complete']
            or summary['requests'] != audit['requests'] or summary['groups'] != audit['groups']):
        raise ValueError(f'{root}: summary inventory mismatch')
    return read(root / 'protocol.json'), groups, summary, read(root / 'stores.json'), audit


def differences(a, b, path=()):
    if a == b:
        return
    if type(a) is type(b) is dict and a.keys() == b.keys():
        for key in sorted(a):
            yield from differences(a[key], b[key], path + (key,))
    elif type(a) is type(b) is list and len(a) == len(b):
        for index, (left, right) in enumerate(zip(a, b)):
            yield from differences(left, right, path + (index,))
    else:
        yield path


def graph_metadata(path):
    prefix = len(path) >= 6 and path[1] == 'arms' and path[3:5] == ('native', 'graph')
    return prefix and (path[5:] == ('enodes',) or
                       (len(path) == 8 and path[5] == 'targets' and path[7] == 'eclass'))


def summary_metadata(path):
    return (path in (('offline_oracle_seconds',), ('source_validation_seconds',)) or
            (len(path) >= 4 and path[0] == 'workloads' and
             (path[3] in ('wall_seconds', 'native_timing') or path[3:] == ('native_graph_counts', 'enodes_sum'))))


def compare(reference, candidate):
    result = {'scope': 'Archived audited monitor comparisons; timing is descriptive, not a cross-host speedup.',
              'runs': {}, 'physical_report_identical': read(reference / 'physical.json') == read(candidate / 'physical.json')}
    for name in ('primary', 'triage'):
        p, g, s, store, audit = audited_run(reference / name)
        q, h, t, other_store, other_audit = audited_run(candidate / name)
        if any(p[k] != q[k] for k in p if k != 'binary_sha256') or p.keys() != q.keys():
            raise ValueError(f'{name}: not the same frozen experiment')
        gd = list(differences(g, h)); sd = list(differences(s, t))
        indexes = sorted({path[0] for path in gd if path and isinstance(path[0], int)})
        by_path = Counter('/'.join('*' if isinstance(k, int) else k for k in path) for path in gd)
        rows = {}
        for workload, arms in t['workloads'].items():
            rows[workload] = {}
            for arm, row in arms.items():
                old = s['workloads'][workload][arm]
                rows[workload][arm] = {'requests': row['requests'], 'correct': row['correct'],
                    'false_equivalent': row['false_equivalent'], 'typed_checks': row['all_typed_checks'],
                    'native_graphs': row['native_graph_counts'].get('graphs', 0),
                    'native_enodes_reference': old['native_graph_counts'].get('enodes_sum', 0),
                    'native_enodes_candidate': row['native_graph_counts'].get('enodes_sum', 0),
                    'nonidentity_equivalent_with_proof_route': row['nonidentity_equivalent_with_proof_route'],
                    'reference_wall_seconds': old['wall_seconds'], 'candidate_wall_seconds': row['wall_seconds'],
                    'candidate_native_timing': row['native_timing']}
        result['runs'][name] = {'requests': audit['requests'], 'groups': audit['groups'], 'arms': audit['arms'],
            'reference_binary_sha256': p['binary_sha256'], 'candidate_binary_sha256': q['binary_sha256'],
            'same_protocol_except_binary': True, 'final_stores_identical': store == other_store,
            'changed_groups': [{'workload': g[i]['workload'], 'group': g[i]['group']} for i in indexes],
            'group_difference_count': len(gd), 'group_differences_by_field': dict(sorted(by_path.items())),
            'group_differences_only_native_metadata': all(graph_metadata(path) for path in gd),
            'summary_differences_only_timing_or_native_enodes': all(summary_metadata(path) for path in sd),
            'reference_evidence_sha256': audit['evidence_sha256'], 'candidate_evidence_sha256': other_audit['evidence_sha256'],
            'workloads': rows}
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x', encoding='utf8') as stream:
        json.dump(compare(args.reference, args.candidate), stream, indent=2, sort_keys=True)
        stream.write('\n')
