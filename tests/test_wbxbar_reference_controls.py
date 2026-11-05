"""Check control transformations and provenance; no functional golden model."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import wbxbar_reference_controls as controls


class ReferenceControlTests(unittest.TestCase):
    def test_transformations_preserve_payloads_and_original_evidence(self):
        inputs, accounts, limits = controls.build()
        self.assertEqual((len(inputs), len(accounts), len(limits)), (127, 127, 6))
        self.assertEqual(inputs, json.loads((controls.OUTPUT_BASE / 'controls-v1/inputs.json').read_text()))
        for case in accounts:
            if case['kind'] != 'metamorphic':
                continue
            original = inputs[case['baseline']]
            changed = inputs[case['name']]
            if case['transformation'] == 'swap_masters':
                self.assertEqual(controls.swap_masters(changed), original)
            else:
                self.assertEqual(len(changed), len(original)+3)
                self.assertTrue(all(row['pre']['i_reset'] for row in changed[:3]))
                for old, new in zip(original, changed[3:]):
                    self.assertEqual(new['cycle'], old['cycle']+3)
                    self.assertEqual(new['pre'], old['pre'])
                    self.assertEqual(new['post'], old['post'])
        for case in limits.values():
            self.assertIn(case['expected'], ('unresolved', 'dut_violation'))
            self.assertTrue(all(type(v) is int and v > 0 for v in case['limits'].values()))

    def test_author_packet_excludes_full_control_inputs_and_case_table(self):
        packet = json.loads((controls.OUTPUT_BASE / 'spec-packet-v1/packet.json').read_text())
        self.assertNotIn('synthetic_traces', packet)
        self.assertNotIn('control_assessments', packet['reviewed_reference_contract'])
        self.assertNotIn('heldback/swap_masters', json.dumps(packet))


if __name__ == '__main__':
    unittest.main()
