from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

from check_txn_context_physical import BASE, BRANCHES, active, load_terms, replay, symbolic
from egg_frame_faults import load_corpus


def boundary_rows(valid, last):
    rows = []
    for i in range(5):
        pins = {'rst': int(i == 0), 's_valid': int(i > 0), 's_last': int(i == 4),
                'm_ready': 1, 'h_ready': 1, 's_data': 100 + i}
        pre = {'s_ready': 1, 'm_valid': int(i >= 2), 'm_last': 0, 'm_data': i,
               'h_valid': 0, 'h_pad': 0, 'h_truncate': 0, 'h_length': 0, 'h_original_length': 0}
        post = dict(pre)
        if i == 4:
            post.update(m_valid=valid, m_last=last)
        rows.append({'cycle': i, 'inputs': pins, 'pre': pre, 'post': post})
    return rows


class TransactionContextPhysicalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terms = load_terms(BASE / 'frame-txn-live/transcript.tar.gz')

    def test_typed_branches_and_frozen_control(self):
        result = symbolic(self.terms)
        for other in ('T2', 'T3'):
            self.assertEqual([q['status'] for q in result[other].values()], ['unsat'] * 4)
        self.assertEqual({k: q['status'] for k, q in result['C08'].items()},
                         {'all': 'sat', 'short': 'unsat', 'boundary': 'sat', 'long': 'unsat'})

    def test_same_unknown_last_completion_exposes_complements(self):
        rows = boundary_rows(1, -1)
        branch = replay({('synth', 'data'): {'rows': rows}}, self.terms)['branches']['boundary']
        control = branch['pairs_vs_T1']['C08']
        self.assertEqual((branch['active'], control['both_unknown'], control['xor_true']), (1, 1, 1))
        self.assertEqual(control['false_alarm'] + control['missed'], 0)
        self.assertIsNone(control['first_mismatch'])
        self.assertEqual(control['first_xor_true']['phase'], 'post')
        self.assertEqual(control['first_xor_true']['values']['m_last'], -1)
        for ident in ('T2', 'T3'):
            pair = branch['pairs_vs_T1'][ident]
            self.assertEqual((pair['both_unknown'], pair['xor_false'], pair['xor_unknown']), (1, 1, 0))

    def test_unknown_valid_keeps_a_partially_observable_activation(self):
        rows = boundary_rows(-1, 1)
        branch = replay({('synth', 'valid'): {'rows': rows}}, self.terms)['branches']['boundary']
        self.assertEqual((branch['active'], branch['active_unknown']), (0, 1))
        pair = branch['pairs_vs_T1']['C08']
        self.assertEqual((pair['one_unknown'], pair['xor_unknown'], pair['xor_true']), (1, 1, 0))

    def test_unselected_frames_do_not_activate_and_native_control_loses_real_tlast(self):
        report = replay(load_corpus(BASE / 'frame-faults'), self.terms)
        self.assertEqual(report['snapshots'], 12712)
        branches = report['branches']
        self.assertEqual([branches[b]['active'] for b in BRANCHES], [934, 815, 3330])
        self.assertEqual(branches['short']['no_selected_frame'], 6086)
        self.assertFalse(active({'rst': 0, 'm_valid': 1, 'data_index': 1, 'data_n': 0,
                                 'data_count': 2, 'input_count': 2, 'data_done': False}))
        control = branches['boundary']['pairs_vs_T1']['C08']
        self.assertEqual((control['false_alarm'], control['missed'], control['active_mismatch']), (52, 4, 56))
        self.assertEqual(control['first_missed']['design'], 'F03')
        self.assertEqual(sum(v['boundary']['C08_false_alarms'] for v in report['cases']['original'].values()), 8)


if __name__ == '__main__':
    unittest.main()
