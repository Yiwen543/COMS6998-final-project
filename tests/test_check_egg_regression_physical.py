from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

from check_egg_regression_physical import (BASE, _compiled, classify, replay, report_counts,
                                           unique_requests)
from egg_regression_workload import workload
from egg_txn_observe import oracle, snapshots


def controlled_sample(valid=-1):
    ins = {'rst': 1, 's_valid': 0, 's_last': 0, 'm_ready': 1, 'h_ready': 1, 's_data': 0}
    outs = {'s_ready': 0, 'm_valid': valid, 'm_last': 0, 'm_data': 0,
            'h_valid': 0, 'h_pad': 0, 'h_truncate': 0, 'h_length': 0, 'h_original_length': 0}
    rows = [{'cycle': 0, 'inputs': ins, 'pre': dict(outs), 'post': dict(outs)}]
    return rows, next(snapshots(rows))


def request(left, right, relation='equivalent', guard='true', **kwargs):
    return {'id': 'R0', 'cohort': 'controlled_revision', 'round': 0,
            'property': 'reset_clear', 'left': left, 'right': right,
            'guard': guard, 'expected_relation': relation, **kwargs}


class PhysicalRegressionTest(unittest.TestCase):
    def test_unknown_verdicts_shared_completion_distinguishes_complements(self):
        rows, _ = controlled_sample()
        pair = unique_requests([request('m_valid', '(not m_valid)', 'incomparable')])
        result = replay({('original', 'synth'): {'rows': rows}}, pair)['comparisons'][0]
        self.assertEqual(result['counts']['both_unknown'], 1)
        self.assertEqual(result['counts']['xor_true'], 1)
        self.assertEqual(result['counts']['old_only_unknown'], 1)
        self.assertEqual(result['counts']['new_only_unknown'], 1)
        self.assertTrue(result['physically_distinguishable'])
        self.assertFalse(result['known_direction_difference'])
        self.assertEqual(result['witnesses']['original_xor']['values']['m_valid'], -1)

    def test_unknown_equal_endpoints_are_jointly_equal(self):
        rows, _ = controlled_sample()
        pair = unique_requests([request('m_valid', '(or m_valid false)')])
        result = replay({('original', 'synth'): {'rows': rows}}, pair)['comparisons'][0]
        self.assertEqual(result['counts']['both_unknown'], 1)
        self.assertEqual(result['counts']['xor_false'], 1)
        self.assertFalse(result['physically_distinguishable'])

    def test_unknown_guard_not_conflated_with_false_or_active(self):
        _, snap = controlled_sample()
        row, = unique_requests([request('true', 'false', 'weakened', guard='m_valid')])
        result, witness = classify(row, snap, _compiled(row), {}, oracle(snap['values']))
        self.assertEqual(result, {'guard_unknown': 1})
        self.assertIsNone(witness)
        row, = unique_requests([request('true', 'false', 'weakened', guard='false')])
        self.assertEqual(classify(row, snap, _compiled(row), {}, oracle(snap['values']))[0], {'guard_false': 1})

    def test_polarity_and_independent_reference_check(self):
        rows, _ = controlled_sample(valid=1)
        row, = unique_requests([request('(and rst m_valid)', 'false', 'weakened')])
        result = replay({('original', 'synth'): {'rows': rows}}, [row])['comparisons'][0]['counts']
        self.assertEqual(result['old_only_true'], 1)
        self.assertEqual(result['new_ref_ref_only_true'], 1)
        self.assertEqual(result['old_ref_xor_false'], 1)
        reversed_row, = unique_requests([request('(and rst m_valid)', 'false', 'strengthened')])
        with self.assertRaisesRegex(ValueError, 'stronger'):
            replay({('original', 'synth'): {'rows': rows}}, [reversed_row])

    def test_population_dedup_preserves_order_provenance_and_cohorts(self):
        cases = [request('false', 'true', 'strengthened'),
                 request('false', 'true', 'strengthened', id='R1', cohort='controlled_scope'),
                 request('true', 'false', 'weakened', id='R2'),
                 request('true', 'true', id='R3', cohort='real_history')]
        rows = unique_requests(cases)
        self.assertEqual(len(rows), 2)
        self.assertEqual([req['id'] for req in rows[0]['requests']], ['R0', 'R1'])
        corpus = {('original', 'synth'): {'rows': controlled_sample()[0]}}
        primary = replay(corpus, rows)['comparisons']
        additional = replay({}, rows)['comparisons']
        counts = report_counts(rows, primary, additional)
        self.assertEqual(counts['all_unique']['requests'], 3)
        self.assertEqual(counts['all_unique']['unique_comparisons'], 2)
        self.assertEqual(counts['all_unique']['either_distinguishable'], 2)
        with self.assertRaisesRegex(ValueError, 'conflicting'):
            unique_requests(cases + [request('false', 'true', 'weakened', id='R4')])

    def test_frozen_source_coverage(self):
        rows = unique_requests(workload(BASE / 'frame-txn-live/transcript.tar.gz'))
        requests = [r for row in rows for r in row['requests']]
        self.assertEqual(len(requests), 62)
        self.assertEqual({x['cohort'] for x in requests},
                         {'real_initial', 'real_context', 'controlled_revision', 'controlled_scope'})


if __name__ == '__main__':
    unittest.main()
