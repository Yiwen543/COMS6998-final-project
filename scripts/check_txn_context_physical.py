#!/usr/bin/env python3
"""Replay the live data_last spellings and a frozen four-byte TLAST control on native observations."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

from audit_egg_fifo_live import read_archive, require
from egg_txn_loop import validate
from egg_txn_observe import ROOT, oracle, read_corpora, snapshots
from egg_txn_terms import REFERENCES, parse_term, sample, typed_oracle


BASE = ROOT / 'results/milestone3'
REPLIES = {
    'T1': ('trial-01/initial/response.json', 'b932bcda249dc3d5008086ced05276b056a21ca3b96695fa4135fe9f8e4221e1'),
    'T2': ('trial-02/initial/response.json', '7ef25c2f64a390c25c58f24a5d7ea09e45a6a910969552a48a1a962bf6713c38'),
    'T3': ('trial-03/initial/response.json', 'eb768ed4c14b5e44d5b68226a2c4d01ee1b8be872dac640888bf57cb0a8258a0'),
}
BRANCHES = {'short': '(ult data_n 4)', 'boundary': '(eq data_n 4)', 'long': '(ugt data_n 4)'}
COMPARISONS = ('T2', 'T3', 'C08')
BEFORE, AFTER = '(uge data_n 4)', '(ugt data_n 4)'


def load_terms(archive):
    files = read_archive(archive)
    config = json.loads(files['config.json'])
    require(config['mode'] == 'live' and config['trials'] == 3, 'expected the three-trial live run')
    terms = {}
    for key, (member, digest) in REPLIES.items():
        raw = files[member]
        require(hashlib.sha256(raw).hexdigest() == digest, f'changed live reply {member}')
        terms[key] = validate(json.loads(raw)['output'])['data_last']
    require(terms['T1'].count(BEFORE) == 1, 'expected the one frozen C08 boundary anchor')
    terms['C08'] = terms['T1'].replace(BEFORE, AFTER)
    return terms


def symbolic(terms):
    # Gating both violation expressions by the same branch checks their XOR exactly
    # when its guard is true. Physical evidence for branch activation is separate.
    queries = {}
    for other in COMPARISONS:
        queries[other] = {}
        for key, guard in {'all': None, **BRANCHES}.items():
            a, b = terms['T1'], terms[other]
            if guard:
                a, b = f'(and {guard} {a})', f'(and {guard} {b})'
            query = typed_oracle(a, b)
            expected = 'sat' if other == 'C08' and key in ('all', 'boundary') else 'unsat'
            require(query['status'] == expected, f'{other}/{key}: unexpected typed XOR {query["status"]}')
            queries[other][key] = query
    return queries


def active(v):
    # Eligibility already establishes the data cursor. Check entitlement using the
    # selected accepted input bytes, then combine it with reset and VALID in four states.
    idx, n = v['data_index'], v['data_n']
    permitted = (v['data_count'] < v['input_count'] and 1 <= idx <= 8
                 and (idx <= n or (v['data_done'] and idx <= 4)))
    if not permitted or v['rst'] == 1 or v['m_valid'] == 0:
        return False
    return None if v['rst'] == -1 or v['m_valid'] == -1 else True


def empty_branch():
    keys = ('eligible', 'pre', 'post', 'no_selected_frame', 'active', 'active_unknown', 'active_pre', 'active_post',
            'active_input_done', 'active_done_fourth_byte', 'reference_alarms', 'active_reference_alarms',
            'reference_unknown')
    pair_keys = ('known_equal', 'both_unknown', 'one_unknown', 'false_alarm', 'missed',
                 'active_equal_known', 'active_both_unknown', 'active_one_unknown', 'active_mismatch',
                 'xor_false', 'xor_true', 'xor_unknown')
    return {**dict.fromkeys(keys, 0), 'pairs_vs_T1': {k: {**dict.fromkeys(pair_keys, 0), 'first_mismatch': None,
                                                          'first_unknown_difference': None, 'first_xor_true': None,
                                                          'first_false_alarm': None, 'first_missed': None}
                                                     for k in COMPARISONS}}


def observe(branch, design, trace, snap, answers, deltas, enabled):
    v = snap['values']
    left = answers['T1']
    branch['eligible'] += 1
    branch[snap['phase']] += 1
    branch['no_selected_frame'] += v['data_n'] == 0
    branch['reference_alarms'] += left is True
    branch['reference_unknown'] += left is None
    branch['active_unknown'] += enabled is None
    if enabled is True:
        branch['active'] += 1
        branch['active_' + snap['phase']] += 1
        branch['active_input_done'] += v['data_done']
        branch['active_done_fourth_byte'] += bool(v['data_done'] and v['data_index'] == 4)
        branch['active_reference_alarms'] += left is True
    for other, counters in branch['pairs_vs_T1'].items():
        right = answers[other]
        witness = None
        if left is None and right is None:
            category, active_category = 'both_unknown', 'active_both_unknown'
        elif left is None or right is None:
            category, active_category = 'one_unknown', 'active_one_unknown'
            witness = 'first_unknown_difference'
        elif left == right:
            category, active_category = 'known_equal', 'active_equal_known'
        else:
            category, active_category = ('missed' if left else 'false_alarm'), 'active_mismatch'
            witness = 'first_mismatch'
        counters[category] += 1
        if enabled is True:
            counters[active_category] += 1
        delta = deltas[other]
        counters['xor_unknown' if delta is None else 'xor_true' if delta else 'xor_false'] += 1
        fields = [witness] if witness else []
        if witness == 'first_mismatch':
            fields.append('first_' + category)
        if delta is True:
            fields.append('first_xor_true')
        for name in fields:
            if counters[name] is None:
                counters[name] = {'design': design, 'trace': trace, 'cycle': snap['cycle'], 'phase': snap['phase'],
                                  'values': v, 'T1': left, other: right, 'xor': delta, 'active': enabled}


def replay(corpus, terms):
    trees = {k: parse_term(source) for k, source in terms.items()}
    reference = parse_term(REFERENCES['data_last'])
    # Compare both sides on the SAME completion of any X/Z pins. Two individually
    # unknown verdicts can agree identically, or differ for every resolution.
    xors = {k: parse_term(f"(xor {terms['T1']} {terms[k]})") for k in COMPARISONS}
    report = {'traces': len(corpus), 'snapshots': 0, 'ineligible': 0,
              'branches': {k: empty_branch() for k in BRANCHES}, 'cases': {}}
    for (design, trace), entry in sorted(corpus.items()):
        case = {k: {'eligible': 0, 'active': 0, 'reference_alarms': 0, 'C08_false_alarms': 0, 'C08_missed': 0}
                for k in BRANCHES}
        report['cases'].setdefault(design, {})[trace] = case
        for snap in snapshots(entry['rows']):
            report['snapshots'] += 1
            if not snap['eligible']['data_last']:
                report['ineligible'] += 1
                continue
            v = snap['values']
            n = v['data_n']
            require(n >= 0, 'eligible data frame has unknown length')
            key = 'short' if n < 4 else 'long' if n > 4 else 'boundary'
            answers = {k: sample(tree, v) for k, tree in trees.items()}
            left = sample(reference, v)
            require(oracle(v)['data_last'] is left and all(answers[k] is left for k in REPLIES),
                    f'{design}/{trace}/{snap["cycle"]}/{snap["phase"]}: live/typed/imperative TLAST disagreement')
            enabled = active(v)
            deltas = {k: sample(tree, v) for k, tree in xors.items()}
            require(deltas['T2'] is False and deltas['T3'] is False,
                    f'{design}/{trace}: live formulas differ on a shared pin completion')
            expected_control = enabled if n == 4 and v['data_done'] and v['data_index'] == 4 else False
            require(deltas['C08'] is expected_control, f'{design}/{trace}: control differs from frozen boundary')
            observe(report['branches'][key], design, trace, snap, answers, deltas, enabled)
            metrics = case[key]
            metrics['eligible'] += 1
            metrics['active'] += enabled is True
            metrics['reference_alarms'] += left is True
            metrics['C08_false_alarms'] += left is False and answers['C08'] is True
            metrics['C08_missed'] += left is True and answers['C08'] is False
    require(sum(b['eligible'] for b in report['branches'].values()) + report['ineligible'] == report['snapshots'],
            'physical branch totals do not account for all PRE/POST snapshots')
    return report


def run(archive, corpus_path, controls_path, output):
    require(not output.exists(), f'output already exists: {output}')
    terms = load_terms(archive)
    # Loading both corpora verifies the three archived originals match exactly.
    corpus = read_corpora(corpus_path, controls_path)
    primary = {key: value for key, value in corpus.items() if key[0] == 'original' or key[0].startswith('F')}
    extra = {key: value for key, value in corpus.items() if key not in primary}
    queries = symbolic(terms)
    report = {
        'scope': 'Native PRE/POST snapshots; active means non-reset valid data presentation justified by its input record.',
        'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'property': 'data_last',
        'replies': {k: {'member': path, 'sha256': digest} for k, (path, digest) in REPLIES.items()},
        'terms': terms, 'C08': {'source': 'T1', 'before': BEFORE, 'after': AFTER},
        'branch_guards': BRANCHES,
        'symbolic': {k: {scope: q['status'] for scope, q in by_scope.items()} for k, by_scope in queries.items()},
        'physical': {'primary': replay(primary, terms)},
        'corpus_sha256': {corpus_path.name: json.loads((corpus_path / 'summary.json').read_bytes())['corpus_sha256']},
    }
    if controls_path:
        report['physical']['additional_controls'] = replay(extra, terms)
        report['corpus_sha256'][controls_path.name] = json.loads((controls_path / 'summary.json').read_bytes())['corpus_sha256']
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        stage = Path(tmp) / 'report'
        stage.mkdir()
        for name, obj in [('summary', report), ('queries', queries)]:
            (stage / f'{name}.json').write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')
        stage.rename(output)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=BASE / 'frame-txn-live/transcript.tar.gz')
    parser.add_argument('--corpus', type=Path, default=BASE / 'frame-faults')
    parser.add_argument('--controls', type=Path, help='optional frame-diagnostic-faults directory; original traces deduplicated')
    parser.add_argument('--output', type=Path, required=True, help='new result directory')
    args = parser.parse_args()
    result = run(args.archive, args.corpus, args.controls, args.output)
    for group, observations in result['physical'].items():
        print(group, {k: b['active'] for k, b in observations['branches'].items()})
