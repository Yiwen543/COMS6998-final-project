import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from controller_prepare import TASK, PUBLIC, DRIVER, datasets, normalize, parse


class ControllerTaskTests(unittest.TestCase):
    def test_fixed_sets_are_deterministic_and_separate(self):
        a, b = datasets()
        self.assertEqual((a, b), datasets())
        self.assertFalse({json.dumps(x) for x in a.values()} & {json.dumps(x) for x in b.values()})
        for traces, tail in [(a, 32), (b, 128)]:
            for actions in traces.values():
                self.assertLessEqual(len(actions), 512)
                self.assertTrue(all(x['reset'] == x['offer'] == 0 and x['data_ready'] == x['status_ready'] == 1
                                    for x in actions[-tail:]))

    def test_transport_parser_preserves_x_and_rejects_forged_source(self):
        log = ('PRE 0 1 0 0 0 1 1 0 x 0 x 0 x x x x\n'
               'POST 0 0 x 0 x 0 x x x x\nQUEUE 0 0 0\n')
        actions = [{'reset': 1, 'offer': 0, 'data': 0, 'last': 0, 'data_ready': 1, 'status_ready': 1}]
        rows, pending = parse(log, actions)
        self.assertEqual(pending, 0)
        self.assertEqual(rows[0]['post']['m_data'], -1)
        with self.assertRaises(ValueError):
            parse(log.replace('PRE 0 1 0 0 0', 'PRE 0 1 1 0 0'), actions)

    def test_cross_sim_comparison_ignores_only_unspecified_payload(self):
        log = ('PRE 0 1 0 0 0 1 1 0 0 0 0 0 0 0 0 0\n'
               'POST 0 0 0 0 0 0 0 0 0 0\nQUEUE 0 0 0\n')
        action = {'reset': 1, 'offer': 0, 'data': 0, 'last': 0, 'data_ready': 1, 'status_ready': 1}
        rows, _ = parse(log, [action])
        other = copy.deepcopy(rows)
        other[0]['post']['m_data'] = -1
        self.assertEqual(normalize(rows), normalize(other))
        other[0]['post']['m_valid'] = -1
        self.assertNotEqual(normalize(rows), normalize(other))

    def test_slang_certified_groups_have_original_distinct_mappings(self):
        root = TASK / 'qualification/typed-v4'
        proof = json.loads((root / 'proof/proof.json').read_text())
        self.assertEqual(proof['status'], 'pass')
        self.assertFalse(proof['unsafe_free_combinational_values'])
        screen = json.loads((root / 'screen/screen.json').read_text())
        groups = [g for g in screen['groups'] if g['nontrivial_static_candidate']]
        self.assertGreaterEqual(len(groups), 1)
        for group in groups:
            self.assertGreaterEqual(len({(m['source'], m['line'], m['column']) for m in group['members']}), 2)
            self.assertTrue(all(m['guard_sat'] == m['guard_not_sat'] == 'sat' for m in group['members']))


if __name__ == '__main__':
    unittest.main()
