"""Complete repair-review evidence and fail-closed transport boundaries."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import review_wbxbar_reference_repair as role
from prepare_wbxbar_reference_review import unpack_results, unpack_traces


class RepairedReviewTests(unittest.TestCase):
    def test_all144_cases_and_failed_test_are_preserved(self):
        b = role.OUTPUT_BASE
        packet = b / 'repair-review-packet-v1'
        m = role.verify(packet)
        p = json.loads((packet / 'packet.json').read_text())
        traces = json.loads((b / 'controls-v1/inputs.json').read_text())
        traces.update({'limit/' + n: c['rows'] for n, c in json.loads((b / 'controls-v1/limit-tests.json').read_text()).items()})
        traces.update({'focused/' + n: c['rows'] for n, c in json.loads((b / 'review-repro-v2/inputs.json').read_text()).items()})
        diagnostic = json.loads((b / 'repair-v1/selftest-diagnostic.json').read_text())['cases']
        traces.update({'diagnostic/' + n: c['rows'] for n, c in diagnostic.items()})
        results = json.loads((b / 'repair-v1/evaluation-original/cases.json').read_text())['cases']
        results.update({'limit/' + n: c for n, c in json.loads((b / 'repair-v1/evaluation-original/limits.json').read_text()).items()})
        results.update({'focused/' + n: c for n, c in json.loads((b / 'repair-v1/evaluation-focused/outputs.json').read_text()).items()})
        results.update({'diagnostic/' + n: c['candidate'] for n, c in diagnostic.items()})
        self.assertEqual(unpack_traces(p['traces']), traces)
        self.assertEqual(unpack_results(p['full_checker_results']), results)
        self.assertEqual(len(traces), 144)
        self.assertEqual(set(traces), {c['name'] for c in p['expectations']})
        self.assertEqual([x['name'] for x in p['selftest_results'] if not x['pass']], ['mixed_same_edge_explicit'])
        self.assertFalse(p['gate_status']['offline_gate_passed'])
        self.assertEqual(m['planned_calls'], 1)
        self.assertEqual(m['cli_budget_usd'], 4)

    def test_prompt_tamper_stops_call(self):
        with tempfile.TemporaryDirectory() as folder:
            packet = Path(folder) / 'packet'
            shutil.copytree(role.OUTPUT_BASE / 'repair-review-packet-v1', packet)
            (packet / 'prompt.txt').write_text('tampered')
            with patch.object(role, 'call') as call:
                with self.assertRaisesRegex(ValueError, 'packet drift'):
                    role.run(packet, Path(folder) / 'review')
                call.assert_not_called()

    def test_positive_model_opinion_does_not_override_failed_offline_gate(self):
        with tempfile.TemporaryDirectory() as folder:
            key = Path(folder) / 'offline-key'
            key.write_text('test-only')
            key.chmod(0o600)
            def fake(prompt, output, env, job):
                self.assertNotIn('OPENAI_API_KEY', env)
                self.assertNotIn('ANTHROPIC_BASE_URL', env)
                output.mkdir()
                return {'ready_for_replay_registration': True, 'findings': [], 'contract_decision_assessments': [], 'required_followup': [], 'limitations': []}
            with patch.object(role, 'KEY_FILE', key), patch.object(role, 'call', side_effect=fake) as call, patch.dict(os.environ, {'OPENAI_API_KEY': 'test', 'ANTHROPIC_BASE_URL': 'test'}):
                result = role.run(role.OUTPUT_BASE / 'repair-review-packet-v1', Path(folder) / 'review')
                self.assertTrue(result['model_readiness'])
                self.assertFalse(result['offline_gate_passed'])
                self.assertFalse(result['replay_allowed'])
                self.assertFalse(result['live_B_allowed'])
                self.assertFalse(result['live_C_allowed'])
                self.assertEqual(call.call_count, 1)
            self.assertFalse(key.exists())


if __name__ == '__main__':
    unittest.main()
