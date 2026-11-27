from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

from egg_txn_observe import (COUNTERS, DATA, HEADER, PROPERTIES, ROOT, coverage_report, oracle,
                             read_corpora, score_corpus, snapshots, verify_drain_tail)
from egg_txn_terms import BOOL_NAMES, BV_WIDTHS, REFERENCES


def row(cycle, *, inputs=None, pre=None, post=None):
    drive = {'rst': 0, 's_valid': 0, 's_data': 0, 's_last': 0, 'm_ready': 1, 'h_ready': 1}
    observe = {'s_ready': 1, 'm_valid': 0, 'm_last': 0, 'm_data': 0, 'h_valid': 0,
               'h_length': 0, 'h_original_length': 0, 'h_pad': 0, 'h_truncate': 0}
    return {'cycle': cycle, 'inputs': {**drive, **(inputs or {})},
            'pre': {**observe, **(pre or {})}, 'post': {**observe, **(post or {})}}


def ctx(rows):
    return {(s['cycle'], s['phase']): s for s in snapshots(rows)}


def summaries(rows, candidates=REFERENCES):
    rows = [*rows, *(row(i) for i in range(len(rows), len(rows) + 128))]
    return score_corpus({('test', 'trace'): {'rows': rows, 'checker': {'verdict': 'PASS'}}},
                        candidates)['cases']['test']['trace']['properties']


class TransactionObservationTest(unittest.TestCase):
    def test_same_edge_no_bypass_and_independent_observed_boundaries(self):
        rows = [
            row(0, inputs={'rst': 1}),
            row(1, inputs={'s_valid': 1, 's_data': 40}, pre={'m_valid': 1, 'm_last': 1}),
            row(2, inputs={'s_valid': 1, 's_data': 99, 's_last': 1}),
            row(3, pre={'h_valid': 1}),
        ]
        s = ctx(rows)
        self.assertNotIn((0, 'pre'), s)
        self.assertTrue(oracle(s[1, 'pre']['values'])['data_entitlement'])
        after = s[1, 'post']['values']
        self.assertEqual((after['input_count'], after['input_open'], after['data_count'], after['data_n'],
                          after['header_count'], after['header_n'], after['header_done']),
                         (1, True, 1, 0, 0, 1, False))
        self.assertTrue(s[1, 'post']['eligible']['data_payload'])
        self.assertEqual(s[2, 'pre']['values']['header_n'], 1)
        self.assertEqual(s[2, 'post']['values']['header_n'], 2)
        self.assertTrue(s[2, 'post']['values']['header_done'])
        self.assertEqual(s[3, 'pre']['values']['header_count'], 0)
        self.assertEqual(s[3, 'post']['values']['header_count'], 1)
        self.assertEqual(sum(snap['values']['final_sample'] for snap in s.values()), 1)
        self.assertTrue(s[3, 'post']['values']['final_sample'])
        # The fabricated wrong output boundary advanced the output counter; no
        # checker verdict, expected payload/TLAST/length, or monitor result is exposed.
        self.assertEqual(set(after), BOOL_NAMES | BV_WIDTHS.keys())
        self.assertNotIn('expected', ' '.join(after))

    def test_input_backpressure_does_not_append_and_observed_index_not_clamped(self):
        rows = [row(0, inputs={'rst': 1}),
                row(1, inputs={'s_valid': 1, 's_data': 42}, pre={'s_ready': 0}),
                row(2, inputs={'s_valid': 1, 's_data': 42, 's_last': 1})]
        rows.extend(row(i, pre={'m_valid': 1, 'm_last': 0}) for i in range(3, 12))
        s = ctx(rows)
        self.assertEqual(s[1, 'post']['values']['input_count'], 0)
        val = s[2, 'post']['values']
        self.assertEqual((val['data_count'], val['data_n'], val['data_index'], val['data_byte']), (0, 1, 1, 42))
        val = s[11, 'post']['values']
        self.assertEqual((val['data_count'], val['data_n'], val['data_index'], val['data_byte']), (0, 1, 10, 0))

    def test_unknown_cursors_are_channel_local_until_reset(self):
        rows = [row(0, inputs={'rst': 1}),
                row(1, inputs={'s_valid': 1, 's_last': 1}, pre={'m_valid': 1, 'm_last': -1}),
                row(2, inputs={'rst': 1}, post={'h_valid': 1}), row(3, pre={'h_valid': -1}),
                row(4, inputs={'s_valid': -1}, pre={'s_ready': 0}),
                row(5, inputs={'s_valid': 1, 's_last': -1}), row(6, inputs={'rst': -1}),
                row(7, inputs={'rst': 1})]
        s = ctx(rows)
        self.assertTrue(all(not s[1, 'post']['eligible'][k] for k in DATA))
        self.assertTrue(all(s[1, 'post']['eligible'][k] for k in HEADER))
        self.assertFalse(s[1, 'post']['eligible']['drain_complete'])
        self.assertTrue(s[2, 'post']['eligible']['reset_clear'])
        self.assertTrue(oracle(s[2, 'post']['values'])['reset_clear'])
        self.assertTrue(all(s[3, 'post']['eligible'][k] for k in DATA))
        self.assertFalse(any(s[3, 'post']['eligible'][k] for k in HEADER))
        self.assertTrue(s[4, 'post']['eligible']['data_payload'])
        self.assertEqual(s[5, 'post']['values']['input_open'], -1)
        self.assertFalse(any(s[6, 'post']['eligible'].values()))
        self.assertTrue(all(s[7, 'post']['eligible'].values()))
        prop = summaries(rows)
        self.assertGreater(prop['data_payload']['ineligible'], 0)
        self.assertEqual(prop['reset_clear']['reference_alarms'], 1)
        self.assertEqual(prop['reset_clear']['ineligible'], 2)

    def test_x_data_is_unknown_only_if_needed_and_mismatch_carries_real_context(self):
        rows = [row(0, inputs={'rst': 1}),
                row(1, inputs={'s_valid': 1, 's_data': -1, 's_last': 1},
                    post={'m_valid': 1, 'm_data': 90}),
                row(2, pre={'m_valid': 1, 'm_data': 90}, post={'m_valid': 1, 'm_data': 90})]
        props = summaries(rows, {**REFERENCES, 'data_payload': 'false'})
        payload = props['data_payload']
        self.assertEqual(payload['unknown_mismatch'], 2)
        self.assertEqual(payload['unknown_both'], 0)
        first = payload['first_unknown_mismatch']
        self.assertEqual((first['cycle'], first['phase'], first['reference_value'], first['candidate_value']),
                         (1, 'post', None, False))
        self.assertEqual(first['values']['data_byte'], -1)
        # After transferring the unknown input byte the current byte is padding;
        # an incorrect 90 is definitely a mismatch with zero.
        self.assertEqual(payload['missed'], 1)
        self.assertEqual(payload['first_mismatch']['phase'], 'post')
        self.assertEqual(payload['first_mismatch']['values']['data_index'], 2)
        self.assertEqual(summaries(rows)['data_payload']['unknown_both'], 2)

    def test_invalid_scope_and_reset_before_epoch(self):
        rows = [row(0), row(1, inputs={'rst': 1})]
        s = ctx(rows)
        self.assertFalse(s[0, 'pre']['eligible']['data_entitlement'])
        self.assertTrue(all(s[1, 'post']['eligible'].values()))
        with self.assertRaisesRegex(ValueError, '12-byte'):
            list(snapshots([row(0, inputs={'rst': 1})] +
                           [row(i, inputs={'s_valid': 1}) for i in range(1, 14)]))
        with self.assertRaisesRegex(ValueError, '512'):
            list(snapshots([row(0, inputs={'rst': 1})] + [row(i, pre={'m_valid': 1}) for i in range(1, 513)]))
        with self.assertRaisesRegex(ValueError, 'invalid inputs'):
            list(snapshots([row(0, inputs={'s_data': 256})]))

    def test_scoring_requires_full_quiet_drain(self):
        rows = [row(0, inputs={'rst': 1}), *(row(i) for i in range(1, 129))]
        key = ('synthetic', 'drain')
        corpus = {key: {'rows': rows, 'checker': {'verdict': 'PASS'}}}
        self.assertEqual(verify_drain_tail(corpus), {key: 128})
        rows[1]['inputs']['m_ready'] = 0
        with self.assertRaisesRegex(ValueError, '127 clocks'):
            score_corpus(corpus, REFERENCES)
        rows[-1]['inputs']['h_ready'] = -1
        with self.assertRaisesRegex(ValueError, '0 clocks'):
            verify_drain_tail(corpus)

    def test_frozen_physical_case_coverage(self):
        base = ROOT / 'results/milestone3'
        corpus = read_corpora(base / 'frame-faults', base / 'frame-diagnostic-faults')
        self.assertEqual(len(corpus), 30)
        report = coverage_report(score_corpus(corpus, REFERENCES))
        for group, cases, failures in [('original', 3, 0), ('functional', 18, 13), ('diagnostic_controls', 9, 8)]:
            row = report['comparison'][group]
            self.assertEqual((row['cases'], row['positive_traces'], row['checker_failed_traces'], row['disagreements']),
                             (cases, failures, failures, []))
        original = report['totals_by_design']['original']
        self.assertEqual(original['matched_known'], 1816 * len(PROPERTIES))
        self.assertTrue(all(original[k] == 0 for k in COUNTERS if k != 'matched_known'))
        self.assertEqual(set(report['designs']['F01']['detected_properties']), {'data_payload'})
        self.assertEqual(set(report['designs']['F02']['detected_properties']), {'header_flags'})
        self.assertIn('reset_clear', report['designs']['F06']['detected_properties'])


if __name__ == '__main__':
    unittest.main()
