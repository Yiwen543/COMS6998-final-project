#!/usr/bin/env python3
"""Derive transaction context from observed AXI handshakes and grade violation monitors."""
import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path

from egg_frame_diagnostic_faults import load_corpus as load_controls
from egg_frame_faults import FAULTS, load_corpus
from m3_controller_replay import INPUTS, OUTPUTS
from predicates import ROOT


DATA = ('data_entitlement', 'data_payload', 'data_last')
HEADER = ('header_entitlement', 'header_original', 'header_adjusted', 'header_flags')
PROPERTIES = (*DATA, *HEADER, 'reset_clear', 'drain_complete')
COUNTERS = ('reference_alarms', 'candidate_alarms', 'matched_alarms', 'matched_known', 'missed',
            'false_alarm', 'unknown_both', 'unknown_mismatch', 'ineligible')
PIN_WIDTHS = {name: 1 for name in (*INPUTS, *OUTPUTS)}
PIN_WIDTHS.update(s_data=8, m_data=8, h_length=16, h_original_length=16)


def transfer(valid, ready):
    if valid == 0 or ready == 0:
        return 0
    if valid == ready == 1:
        return 1
    return -1


@dataclass
class Frame:
    data: list = field(default_factory=list)
    done: bool = False


class History:
    """Observed output TLAST and header handshakes advance separate cursors, even on faulty RTL."""
    def __init__(self, initialized=False):
        self.frames = []
        self.data_count = self.header_count = 0
        self.data_index = 1
        self.input_known = self.data_known = self.header_known = initialized

    def advance(self, p):
        data = transfer(p['m_valid'], p['m_ready'])
        header = transfer(p['h_valid'], p['h_ready'])
        inp = transfer(p['s_valid'], p['s_ready'])
        if self.data_known:
            if data == -1 or (data and p['m_last'] == -1):
                self.data_known = False
            elif data:
                if p['m_last']:
                    self.data_count += 1
                    self.data_index = 1
                else:
                    self.data_index += 1
        if self.header_known:
            if header == -1:
                self.header_known = False
            else:
                self.header_count += header
        if self.input_known:
            if inp == -1 or (inp and p['s_last'] == -1):
                self.input_known = False
            elif inp:
                if not self.frames or self.frames[-1].done:
                    self.frames.append(Frame())
                frame = self.frames[-1]
                frame.data.append(p['s_data'])
                frame.done = bool(p['s_last'])
                if len(frame.data) > 12:
                    raise ValueError('accepted input frame exceeds the scoped 12-byte maximum')
        if max(len(self.frames), self.data_count, self.header_count, self.data_index) > 512:
            raise ValueError('frame count or data index exceeds the scoped limit of 512')

    def selected(self, known, cursor):
        if not (self.input_known and known):
            return -1, -1
        if cursor >= len(self.frames):
            return 0, False
        frame = self.frames[cursor]
        return len(frame.data), frame.done

    def snapshot(self, cycle, phase, final, pins):
        data_n, data_done = self.selected(self.data_known, self.data_count)
        header_n, header_done = self.selected(self.header_known, self.header_count)
        byte = -1 if data_n == -1 else 0
        if 1 <= self.data_index <= data_n:
            byte = self.frames[self.data_count].data[self.data_index - 1]
        values = {**pins, 'phase_post': phase == 'post', 'final_sample': final,
                  'input_count': len(self.frames) if self.input_known else -1,
                  'input_open': bool(self.frames and not self.frames[-1].done) if self.input_known else -1,
                  'data_count': self.data_count if self.data_known else -1,
                  'header_count': self.header_count if self.header_known else -1,
                  'data_index': self.data_index if self.data_known else -1,
                  'data_n': data_n, 'data_done': data_done, 'data_byte': byte,
                  'header_n': header_n, 'header_done': header_done}
        known_reset = pins['rst'] != -1
        data_ok = known_reset and self.input_known and self.data_known
        header_ok = known_reset and self.input_known and self.header_known
        # An indeterminate transfer invalidates only the corresponding history.
        # Do not count a history-dependent property as tested until that cursor is known again.
        eligible = {**dict.fromkeys(DATA, data_ok), **dict.fromkeys(HEADER, header_ok),
                    'reset_clear': known_reset, 'drain_complete': data_ok and header_ok}
        return {'cycle': cycle, 'phase': phase, 'values': values, 'eligible': eligible}


def snapshots(rows):
    """Yield non-reset PRE before acceptance and every POST after that same rising edge."""
    if not rows:
        raise ValueError('expected a nonempty row list')
    history = History()
    for i, row in enumerate(rows):
        if type(row['cycle']) is not int or row['cycle'] != i:
            raise ValueError('expected consecutive cycles from 0')
        for key, names in [('inputs', INPUTS), ('pre', OUTPUTS), ('post', OUTPUTS)]:
            if row[key].keys() != set(names):
                raise ValueError(f'wrong {key} signal inventory at cycle {i}')
            for name, value in row[key].items():
                if type(value) is not int or not -1 <= value < 1 << PIN_WIDTHS[name]:
                    raise ValueError(f'invalid {key}.{name} at cycle {i}')
        pre = {**row['inputs'], **row['pre']}
        post = {**row['inputs'], **row['post']}
        rst = pre['rst']
        if rst != 1:
            yield history.snapshot(i, 'pre', False, pre)
        if rst == 1:
            history = History(initialized=True)
        elif rst == -1:
            # An unknown synchronous reset can invalidate every epoch cursor.
            history = History()
        else:
            history.advance(pre)
        yield history.snapshot(i, 'post', i + 1 == len(rows), post)


def either(*values):
    if True in values:
        return True
    return None if None in values else False


def both(a, b):
    if a is False or b is False:
        return False
    return None if a is None or b is None else True


def differs(a, b):
    return None if a == -1 or b == -1 else a != b


def oracle(v):
    """Imperative byte selection, frame completion and header checks; no DSL or checker calls."""
    answers = dict.fromkeys(PROPERTIES)
    post = bool(v['phase_post'])
    reset, mvalid, hvalid = (None if v[k] == -1 else bool(v[k]) for k in ('rst', 'm_valid', 'h_valid'))
    answers['reset_clear'] = both(both(reset, post), either(mvalid, hvalid))
    pending = either(*(differs(v[k], 0) for k in ('s_valid', 'm_valid', 'h_valid', 'input_open')),
                     differs(v['data_count'], v['input_count']), differs(v['header_count'], v['input_count']))
    answers['drain_complete'] = both(bool(v['final_sample']), pending)
    if reset is True:
        answers.update(dict.fromkeys(DATA + HEADER, False))
        return answers
    if reset is None:
        return answers
    n, pos = v['data_n'], v['data_index']
    if -1 not in (n, pos, v['data_done'], v['data_count'], v['input_count']):
        in_frame = v['data_count'] < v['input_count']
        received = in_frame and 1 <= pos <= min(n, 8)
        padding = in_frame and v['data_done'] and n < pos <= 4
        entitled = bool(received or padding)
        answers['data_entitlement'] = both(mvalid, not entitled)
        if entitled:
            expected_byte = v['data_byte'] if received else 0
            # Before input TLAST the first seven non-final accepted bytes can
            # be forwarded. Position eight is final even for an open input.
            end = min(8, max(4, n)) if v['data_done'] else 8
            answers['data_payload'] = both(mvalid, differs(v['m_data'], expected_byte))
            answers['data_last'] = both(mvalid, differs(v['m_last'], pos == end))
        else:
            answers.update(dict.fromkeys(('data_payload', 'data_last'), False))
    n = v['header_n']
    if -1 not in (n, v['header_done'], v['header_count'], v['input_count']):
        entitled = v['header_count'] < v['input_count'] and bool(v['header_done'])
        answers['header_entitlement'] = both(hvalid, not entitled)
        if entitled:
            answers['header_original'] = both(hvalid, differs(v['h_original_length'], n))
            answers['header_adjusted'] = both(hvalid, differs(v['h_length'], min(8, max(4, n))))
            answers['header_flags'] = both(hvalid, either(differs(v['h_pad'], n < 4),
                                                         differs(v['h_truncate'], n > 8)))
        else:
            answers.update(dict.fromkeys(('header_original', 'header_adjusted', 'header_flags'), False))
    return answers


def _outcome():
    return {**dict.fromkeys(COUNTERS, 0), 'first_mismatch': None, 'first_unknown_mismatch': None,
            'first_reference_alarm': None, 'first_candidate_alarm': None}


def _accumulate(out, snap, left, right):
    mark = {'cycle': snap['cycle'], 'phase': snap['phase']}
    for label, value in [('reference', left), ('candidate', right)]:
        if value is True:
            out[f'{label}_alarms'] += 1
            if out[f'first_{label}_alarm'] is None:
                out[f'first_{label}_alarm'] = mark
    mismatch = None
    if left is None and right is None:
        out['unknown_both'] += 1
    elif left is None or right is None:
        out['unknown_mismatch'] += 1
        mismatch = 'first_unknown_mismatch'
    elif left == right:
        out['matched_known'] += 1
        out['matched_alarms'] += int(left)
    else:
        out['missed' if left else 'false_alarm'] += 1
        mismatch = 'first_mismatch'
    if mismatch and out[mismatch] is None:
        out[mismatch] = {**mark, 'values': snap['values'], 'reference_value': left, 'candidate_value': right}


def verify_drain_tail(corpus):
    """Require at least 128 final quiet clocks with reset low and both sinks ready on each trace."""
    tails = {}
    for key, entry in corpus.items():
        tail = 0
        for row in reversed(entry['rows']):
            x = row['inputs']
            if (x['rst'], x['s_valid'], x['m_ready'], x['h_ready']) != (0, 0, 1, 1):
                break
            tail += 1
        if tail < 128:
            raise ValueError(f'{key[0]}/{key[1]}: insufficient drain tail ({tail} clocks)')
        tails[key] = tail
    return tails


def score_corpus(corpus, monitors):
    from egg_txn_terms import REFERENCES, parse_term, sample
    if set(REFERENCES) != set(PROPERTIES) or set(monitors) != set(PROPERTIES):
        raise ValueError('expected all nine named transaction properties')
    verify_drain_tail(corpus)
    references = {k: parse_term(REFERENCES[k]) for k in PROPERTIES}
    candidates = {k: parse_term(monitors[k]) for k in PROPERTIES}
    cases, totals = {}, {}
    by_property = {k: dict.fromkeys(COUNTERS, 0) for k in PROPERTIES}
    for (design, trace), entry in sorted(corpus.items()):
        measures = {k: _outcome() for k in PROPERTIES}
        n = 0
        for snap in snapshots(entry['rows']):
            n += 1
            expected = oracle(snap['values'])
            for prop, out in measures.items():
                if not snap['eligible'][prop]:
                    out['ineligible'] += 1
                    continue
                left = sample(references[prop], snap['values'])
                if left is not expected[prop]:
                    raise ValueError(f"{design}/{trace}/{snap['cycle']}/{snap['phase']}/{prop}: "
                                     f"typed reference {left} disagrees with independent oracle {expected[prop]}")
                right = left if references[prop] == candidates[prop] else sample(candidates[prop], snap['values'])
                _accumulate(out, snap, left, right)
        design_total = totals.setdefault(design, dict.fromkeys(COUNTERS, 0))
        for prop, out in measures.items():
            if sum(out[k] for k in ('matched_known', 'missed', 'false_alarm', 'unknown_both',
                                     'unknown_mismatch', 'ineligible')) != n:
                raise ValueError('incomplete sample inventory')
            for k in COUNTERS:
                design_total[k] += out[k]
                by_property[prop][k] += out[k]
        cases.setdefault(design, {})[trace] = {'cycles': len(entry['rows']), 'snapshots': n,
                                              'checker': entry['checker'], 'properties': measures}
    return {'cases': cases, 'totals_by_design': totals, 'totals_by_property': by_property}


def read_corpora(directory, controls=None):
    corpus = load_corpus(directory)
    if controls:
        for key, entry in load_controls(controls).items():
            if key in corpus:
                if key[0] != 'original' or entry != corpus[key]:
                    raise ValueError(f'conflicting physical trace {key}')
            else:
                corpus[key] = entry
    return corpus


def coverage_report(scores):
    """Compare detection by entire trace/design. Repeated alarms may follow one wrong frame boundary."""
    by_design = {}
    for design, cases in scores['cases'].items():
        traces = {}
        for name, case in cases.items():
            props = case['properties']
            traces[name] = {'checker_verdict': case['checker']['verdict'],
                            'checker_failure_categories': sorted({x['category'] for x in case['checker']['failures']}),
                            'cycles': case['cycles'], 'snapshots': case['snapshots'],
                            'properties': {p: {k: v for k, v in counts.items()
                                               if k in ('reference_alarms', 'first_reference_alarm',
                                                        'matched_known', 'unknown_both', 'ineligible')}
                                           for p, counts in props.items()}}
        detected = {p for case in cases.values() for p, row in case['properties'].items() if row['reference_alarms']}
        by_design[design] = {'detected_properties': sorted(detected), 'checker_failed': any(
            x['checker_verdict'] == 'FAIL' for x in traces.values()), 'traces': traces}
    groups = {'original': ['original'], 'functional': [f.id for f in FAULTS],
              'diagnostic_controls': ['D01', 'D02', 'D03']}
    comparisons = {}
    for group, designs in groups.items():
        members = [d for d in designs if d in by_design]
        if not members:
            continue
        outcomes = {(d, t): (any(p['reference_alarms'] for p in case['properties'].values()),
                             case['checker_verdict']) for d in members for t, case in by_design[d]['traces'].items()}
        comparisons[group] = {
            'designs': members, 'cases': len(outcomes),
            'positive_designs': [d for d in members if by_design[d]['detected_properties']],
            'checker_failed_designs': [d for d in members if by_design[d]['checker_failed']],
            'positive_traces': sum(active for active, _ in outcomes.values()),
            'checker_failed_traces': sum(v == 'FAIL' for _, v in outcomes.values()),
            'disagreements': [{'design': d, 'trace': t, 'property_alarm': active, 'checker_verdict': v}
                              for (d, t), (active, v) in outcomes.items() if v != ('FAIL' if active else 'PASS')],
        }
    return {'comparison': comparisons, 'designs': by_design, 'totals_by_design': scores['totals_by_design'],
            'totals_by_property': scores['totals_by_property']}


def main():
    from egg_txn_terms import REFERENCES
    ap = argparse.ArgumentParser(description=__doc__)
    default = ROOT / 'results/milestone3'
    ap.add_argument('--corpus', type=Path, default=default / 'frame-faults')
    ap.add_argument('--diagnostic-controls', action='store_true', help='add nine distinct port-control traces')
    ap.add_argument('--controls', type=Path, default=default / 'frame-diagnostic-faults')
    ap.add_argument('--output', required=True, type=Path, help='new JSON report')
    args = ap.parse_args()
    controls = args.controls if args.diagnostic_controls else None
    corpus = read_corpora(args.corpus, controls)
    result = coverage_report(score_corpus(corpus, REFERENCES))
    for (design, trace), tail in verify_drain_tail(corpus).items():
        result['designs'][design]['traces'][trace]['quiet_ready_tail'] = tail
    result.update(cases=len(corpus), references=REFERENCES, corpus_sha256={
        p.name: json.loads((p / 'summary.json').read_bytes())['corpus_sha256']
        for p in (args.corpus, controls) if p is not None})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as dest:
        json.dump(result, dest, indent=2, sort_keys=True)
        dest.write('\n')


if __name__ == '__main__':
    main()
