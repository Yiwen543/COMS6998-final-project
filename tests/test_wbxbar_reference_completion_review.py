"""Verify complete review transport, including deliberately malformed rows."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import review_wbxbar_reference_repair as role
from prepare_wbxbar_reference_review import FILES, unpack_traces
from prepare_wbxbar_completion_review import unpack_review_results
from repair_wbxbar_reference_checker import apply_exact


class CompletionReviewTests(unittest.TestCase):
    def test_all155_traces_outputs_and_limits_survive(self):
        b = role.OUTPUT_BASE
        m = role.verify(b / 'completion-review-packet-v1')
        p = json.loads((b / 'completion-review-packet-v1/packet.json').read_text())
        run = b / 'completion-v1'
        expected = json.loads((b / 'controls-v1/inputs.json').read_text())
        limits = {n: {} for n in expected}
        for n, case in json.loads((b / 'controls-v1/limit-tests.json').read_text()).items():
            expected['limit/' + n] = case['rows']
            limits['limit/' + n] = case['limits']
        outputs = json.loads((run / 'evaluation-original/cases.json').read_text())['cases']
        outputs.update({'limit/' + n: x for n, x in json.loads((run / 'evaluation-original/limits.json').read_text()).items()})
        for kind in ('focused', 'boundary'):
            actual = json.loads((run / ('evaluation-' + kind) / 'outputs.json').read_text())
            for n, case in json.loads((run / (kind + '-inputs.json')).read_text()).items():
                name = kind + '_recheck/' + n
                expected[name] = case['rows']
                limits[name] = case['limits']
                outputs[name] = actual[n]
        decoded = unpack_traces(p['traces'])
        decoded.update(p['raw_boundary_traces'])
        self.assertEqual(decoded, expected)
        self.assertEqual(p['case_limits'], limits)
        self.assertEqual(unpack_review_results(p['full_checker_results']), outputs)
        self.assertEqual(set(expected), {x['name'] for x in p['expectations']})
        self.assertEqual(len(expected), 155)
        self.assertNotIn('i_mcyc', decoded['boundary_recheck/missing_input_field'][8]['pre'])
        self.assertEqual(decoded['boundary_recheck/noncontiguous_cycle'][8]['cycle'], 80)
        self.assertEqual(m['planned_calls'], 1)
        self.assertFalse(m['replay_allowed'])

    def test_exact_claude_patches_and_unchanged_selftests(self):
        b = role.OUTPUT_BASE
        parent = {f: (b / 'followup-v1/candidate' / f).read_text() for f in FILES}
        rebuilt = apply_exact(parent, json.loads((b / 'completion-v1/patches.json').read_text()))
        for f in FILES:
            self.assertEqual(rebuilt[f], (b / 'completion-v1/candidate' / f).read_text())
        self.assertEqual(parent['selftest.py'], rebuilt['selftest.py'])
        evidence = json.loads((b / 'completion-v1/evaluation-original/cases.json').read_text())
        self.assertEqual(len(evidence['selftests']), 54)
        self.assertTrue(all(x['pass'] for x in evidence['selftests']))

    def test_boundary_evidence_tamper_prevents_call(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / 'packet'
            shutil.copytree(role.OUTPUT_BASE / 'completion-review-packet-v1', p)
            body = json.loads((p / 'packet.json').read_text())
            body['raw_boundary_traces'] = {}
            (p / 'packet.json').write_text(json.dumps(body))
            with patch.object(role, 'call') as call:
                with self.assertRaisesRegex(ValueError, 'packet drift'):
                    role.run(p, Path(folder) / 'review')
                call.assert_not_called()


if __name__ == '__main__':
    unittest.main()
