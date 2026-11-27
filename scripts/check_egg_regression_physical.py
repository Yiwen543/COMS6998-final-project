#!/usr/bin/env python3
"""Replay versioned monitor comparisons on archived native RTL snapshots.

Symbolic classifications are hypotheses supplied by the frozen workload, not
inferred from finite traces. X/Z observations use a *shared* completion when
evaluating directional differences; independent unknown endpoint verdicts do
not imply either agreement or disagreement. The formulas are violation/alarm
predicates, so old-only is a lost alarm and new-only an added alarm relative to
the previous monitor, not necessarily relative to the intended specification.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from egg_txn_observe import ROOT, PROPERTIES, oracle, read_corpora, snapshots, verify_drain_tail
from egg_txn_terms import REFERENCES, parse_term, sample


BASE = ROOT / 'results/milestone3'
COHORTS = {'real_initial', 'real_context', 'controlled_revision', 'controlled_scope'}
RELATIONS = {'equivalent', 'strengthened', 'weakened', 'incomparable', 'unknown'}
SAMPLES = ('guard_false', 'guard_unknown', 'guard_true', 'ineligible')
VERDICTS = ('both_alarm', 'neither_alarm', 'old_only_known', 'new_only_known',
            'both_unknown', 'one_unknown')
DELTAS = ('old_only', 'new_only', 'xor', 'old_ref_old_only', 'old_ref_ref_only',
          'old_ref_xor', 'new_ref_new_only', 'new_ref_ref_only', 'new_ref_xor')
COUNTS = ('snapshots', *SAMPLES, *VERDICTS,
          *(f'{name}_{state}' for name in DELTAS for state in ('true', 'false', 'unknown')),
          'reference_alarms', 'reference_unknown')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _stable_digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique_requests(workload):
    """Select real initial/context comparisons and controlled revisions only.

    Actual repeated unchanged histories are intentionally excluded from this
    physical replay. All request IDs referring to a deduplicated comparison
    remain attached; opposite directional comparisons are not collapsed.
    """
    groups = {}
    ids = set()
    for case in workload:
        if case['cohort'] not in COHORTS:
            continue
        require(case['id'] not in ids, f'duplicate workload request {case["id"]}')
        ids.add(case['id'])
        prop, left, right, guard = (case[k] for k in ('property', 'left', 'right', 'guard'))
        require(prop in PROPERTIES, f'not a physical transaction property: {prop}')
        # Early syntax/type check even if this guard is never observed.
        for source in (left, right, guard):
            parse_term(source)
        expected = case['expected_relation']
        require(expected in RELATIONS, f'unknown predefined relation {expected!r}')
        key = prop, left, right, guard
        if key not in groups:
            groups[key] = {'key': _stable_digest(key), 'property': prop, 'left': left, 'right': right,
                           'guard': guard, 'expected_relation': expected, 'requests': []}
        row = groups[key]
        require(row['expected_relation'] == expected, f'conflicting expected relation for {key}')
        row['requests'].append({'id': case['id'], 'cohort': case['cohort'], 'round': case['round']})
    require(groups, 'no physical comparison requests')
    return list(groups.values())


def _comparisons(a, b):
    """Construct both directed differences and XOR over the same completion."""
    return (("and", a, ("not", b)), ("and", ("not", a), b), ("xor", a, b))


def _compiled(row):
    guard, left, right, ref = (parse_term(t) for t in
                              (row['guard'], row['left'], row['right'], REFERENCES[row['property']]))
    return guard, left, right, ref, (*_comparisons(left, right), *_comparisons(left, ref), *_comparisons(right, ref))


def _state(value):
    return 'unknown' if value is None else 'true' if value else 'false'


def _individual(a, b):
    if a is None or b is None:
        return 'both_unknown' if a is b else 'one_unknown'
    return 'both_alarm' if a and b else 'old_only_known' if a else 'new_only_known' if b else 'neither_alarm'


def classify(row, snap, compiled, memo, expected):
    """Observe one request and the reference; never assume equivalence from this result."""
    prop = row['property']
    if not snap['eligible'][prop]:
        return {'ineligible': 1}, None
    values = snap['values']

    def verdict(term):
        # Reuse deterministic evaluation only for this identical snapshot.
        if term not in memo:
            memo[term] = sample(term, values)
        return memo[term]

    guard, left, right, ref, deltas = compiled
    active = verdict(guard)
    if active is not True:
        return {'guard_' + _state(active): 1}, None
    a, b, r = verdict(left), verdict(right), verdict(ref)
    require(r is expected[prop], f'typed reference differs from the independent oracle for {prop}')
    out = {'guard_true': 1, _individual(a, b): 1, 'reference_alarms': int(r is True),
           'reference_unknown': int(r is None)}
    pairs = ((a, b), (a, r), (b, r))

    def joint(x, y, terms):
        if x is not None and y is not None:
            return x and not y, y and not x, x != y
        # Crucial for partially observed pins: e.g. unknown b vs (not b)
        # are always distinct, while b vs b are equal in *every* completion.
        return tuple(verdict(t) for t in terms)

    observed = tuple(v for i, (x, y) in enumerate(pairs)
                     for v in joint(x, y, deltas[3*i:3*i+3]))
    for name, value in zip(DELTAS, observed, strict=True):
        out[f'{name}_{_state(value)}'] = 1
    aonly, bonly, xor = observed[:3]
    relation = row['expected_relation']
    # These are guards against contradictions with the predeclared control
    # construction, not the source of the semantic classification.
    require(relation != 'equivalent' or xor is False,
            f'physical observation contradicts equivalent expectation for {row["key"]}')
    require(relation != 'strengthened' or aonly is False,
            f'physical observation contradicts stronger alarm expectation for {row["key"]}')
    require(relation != 'weakened' or bonly is False,
            f'physical observation contradicts weaker alarm expectation for {row["key"]}')
    witness = {'cycle': snap['cycle'], 'phase': snap['phase'], 'values': values,
               'old': a, 'new': b, 'reference': r, 'old_only': aonly, 'new_only': bonly, 'xor': xor}
    return out, witness


def _empty():
    return Counter({k: 0 for k in COUNTS})


def _account(counts):
    require(counts['snapshots'] == sum(counts[k] for k in SAMPLES), 'incomplete guard/sample accounting')
    require(counts['guard_true'] == sum(counts[k] for k in VERDICTS), 'incomplete verdict accounting')
    for name in DELTAS:
        require(counts['guard_true'] == sum(counts[f'{name}_{s}'] for s in ('true', 'false', 'unknown')),
                f'incomplete directional accounting for {name}')


def replay(corpus, requests):
    """Score a deduplicated collection of directional comparisons on native rows."""
    compiled = [_compiled(row) for row in requests]
    data = [{'counts': _empty(), 'by_design': {}, 'witnesses': {k: None for k in
             ('old_only', 'new_only', 'xor', 'unknown_xor', 'original_old_only', 'original_new_only',
              'original_xor')}} for _ in requests]
    total = 0
    for (design, trace), entry in sorted(corpus.items()):
        for item in data:
            if design not in item['by_design']:
                item['by_design'][design] = _empty()
        for snap in snapshots(entry['rows']):
            total += 1
            memo, expected = {}, oracle(snap['values'])
            for row, trees, item in zip(requests, compiled, data, strict=True):
                delta, witness = classify(row, snap, trees, memo, expected)
                delta['snapshots'] = 1
                item['counts'].update(delta)
                item['by_design'][design].update(delta)
                if witness is not None:
                    fields = [k for k in ('old_only', 'new_only', 'xor') if witness[k] is True]
                    if design == 'original':
                        fields += ['original_' + k for k in fields]
                    if witness['xor'] is None:
                        fields.append('unknown_xor')
                    for name in fields:
                        if item['witnesses'][name] is None:
                            item['witnesses'][name] = {'design': design, 'trace': trace, **witness}
    for row in data:
        require(row['counts']['snapshots'] == total, 'comparison did not score every snapshot')
        _account(row['counts'])
        for counts in row['by_design'].values():
            _account(counts)
        require(sum(row['by_design'].values(), Counter()) == row['counts'], 'per-design counters mismatch')
        row['physically_distinguishable'] = row['counts']['xor_true'] > 0
        row['known_direction_difference'] = row['counts']['old_only_true'] + row['counts']['new_only_true'] > 0
    return {'traces': len(corpus), 'snapshots': total, 'comparisons': data}


def report_counts(rows, primary, additional):
    counts = {}
    for cohort in sorted(COHORTS) + ['all_unique']:
        subset = [(row, a, b) for row, a, b in zip(rows, primary, additional, strict=True)
                  if cohort == 'all_unique' or any(r['cohort'] == cohort for r in row['requests'])]
        negative = [(r, a, b) for r, a, b in subset if r['expected_relation'] not in ('equivalent', 'unknown')]
        counts[cohort] = {'requests': sum(sum(cohort == 'all_unique' or req['cohort'] == cohort for req in r['requests'])
                                           for r, _, _ in subset),
                          'unique_comparisons': len(subset), 'unique_expected_non_equivalent': len(negative),
                          'primary_distinguishable': sum(a['physically_distinguishable'] for _, a, _ in negative),
                          'additional_distinguishable': sum(b['physically_distinguishable'] for _, _, b in negative),
                          'either_distinguishable': sum(a['physically_distinguishable'] or b['physically_distinguishable']
                                                        for _, a, b in negative),
                          'not_physically_distinguished': [r['key'] for r, a, b in negative if not
                                                          (a['physically_distinguishable'] or b['physically_distinguishable'])]}
    return counts


def run(archive, corpus_path, controls_path, output):
    from egg_regression_workload import workload

    require(not output.exists(), f'output already exists: {output}')
    rows = unique_requests(workload(archive))
    corpus = read_corpora(corpus_path, controls_path)
    verify_drain_tail(corpus)
    primary = {k: v for k, v in corpus.items() if k[0] == 'original' or k[0].startswith('F')}
    additional = {k: v for k, v in corpus.items() if k not in primary}
    first, second = replay(primary, rows), replay(additional, rows)
    by_group = report_counts(rows, first['comparisons'], second['comparisons'])
    report = {'schema': 1, 'complete': True, 'new_api_calls': 0,
              'scope': 'Archived native RTL PRE/POST physical observations only. False guard and unknown guard '
                       'are not treated as active. X/Z differences use the same structural completion; '
                       'true relation is never inferred from traces. Controlled edits are not LLM error evidence.',
              'archive_sha256': file_sha(archive),
              'workload_sha256': _stable_digest(rows),
              'source_sha256': {name: file_sha(ROOT / 'scripts' / name) for name in
                                ('check_egg_regression_physical.py', 'egg_regression_workload.py',
                                 'egg_txn_observe.py', 'egg_txn_terms.py')},
              'corpus_sha256': {p.name: json.loads((p / 'summary.json').read_text())['corpus_sha256']
                                for p in (corpus_path, controls_path) if p is not None},
              'primary': {'traces': first['traces'], 'snapshots': first['snapshots']},
              'additional_controls': {'traces': second['traces'], 'snapshots': second['snapshots']},
              'cohorts': by_group,
              'comparisons': [{**row, 'primary': a, 'additional_controls': b} for row, a, b in
                              zip(rows, first['comparisons'], second['comparisons'], strict=True)]}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as dest:
        json.dump(report, dest, indent=2, sort_keys=True)
        dest.write('\n')
    return report


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', type=Path, default=BASE / 'frame-txn-live/transcript.tar.gz')
    ap.add_argument('--corpus', type=Path, default=BASE / 'frame-faults')
    ap.add_argument('--controls', type=Path, default=BASE / 'frame-diagnostic-faults')
    ap.add_argument('--output', type=Path, required=True, help='new JSON output')
    args = ap.parse_args()
    report = run(args.archive, args.corpus, args.controls, args.output)
    print(json.dumps({'primary': report['primary'], 'additional_controls': report['additional_controls'],
                      'cohorts': report['cohorts']}, indent=2))
