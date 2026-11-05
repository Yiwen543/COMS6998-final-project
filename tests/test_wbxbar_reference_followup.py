"""Check reviewed follow-up evidence and exact-patch role isolation."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import followup_wbxbar_reference_checker as role
from prepare_wbxbar_reference_review import unpack_results, unpack_traces


class FollowupTests(unittest.TestCase):
    def test_control_reproduction_and13_full_roundtrips(self):
        b = role.OUTPUT_BASE
        p = json.loads((b / 'followup-packet-v1/packet.json').read_text())
        m = role.verify(b / 'followup-packet-v1')
        companions = role.err_controls()
        self.assertEqual(companions, json.loads((b / 'repair-followup-controls-v1/inputs.json').read_text()))
        original = json.loads((b / 'repair-v1/selftest-diagnostic.json').read_text())['cases']
        traces = {'diagnostic/' + n: c['rows'] for n, c in original.items()}
        results = {'diagnostic/' + n: c['candidate'] for n, c in original.items()}
        traces.update({'focused/' + n: c['rows'] for n, c in json.loads((b / 'review-repro-v2/inputs.json').read_text()).items()})
        results.update({'focused/' + n: c for n, c in json.loads((b / 'repair-v1/evaluation-focused/outputs.json').read_text()).items()})
        traces.update({'companion/' + n: c['rows'] for n, c in companions.items()})
        results.update({'companion/' + n: c for n, c in json.loads((b / 'repair-followup-controls-v1/outputs.json').read_text()).items()})
        self.assertEqual(unpack_traces(p['focused_traces']), traces)
        self.assertEqual(unpack_results(p['focused_results']), results)
        self.assertEqual(len(traces), 13)
        self.assertEqual(m['planned_calls'], 1)
        self.assertEqual(m['cli_budget_usd'], 4)
        self.assertFalse(m['replay_allowed'])
        self.assertIn('association-free', p['requirements_and_questions'][4])

    def test_tampered_prompt_stops_call(self):
        with tempfile.TemporaryDirectory() as folder:
            packet = Path(folder) / 'packet'
            shutil.copytree(role.OUTPUT_BASE / 'followup-packet-v1', packet)
            (packet / 'prompt.txt').write_text('tamper')
            with patch.object(role, 'call') as call:
                with self.assertRaisesRegex(ValueError, 'packet drift'):
                    role.run(packet, Path(folder) / 'output')
                call.assert_not_called()

    def test_exact_parent_patch_with_cleanup_and_no_live_permission(self):
        parent = role.OUTPUT_BASE / 'repair-v1/candidate'
        source = (parent / 'checker.py').read_text()
        result = {'patches': [{'file': 'checker.py', 'before': 'DEFAULT_LIMITS =',
                              'after': '# offline transport-only mock\nDEFAULT_LIMITS ='}],
                  'rationale': [], 'contract_decisions': []}
        with tempfile.TemporaryDirectory() as folder:
            key = Path(folder) / 'offline-key'
            key.write_text('test-only')
            key.chmod(0o600)
            output = Path(folder) / 'new-candidate'
            def fake(prompt, call_output, env, job):
                self.assertNotIn('OPENAI_API_KEY', env)
                self.assertNotIn('ANTHROPIC_BASE_URL', env)
                call_output.mkdir()
                return result
            with patch.object(role, 'KEY_FILE', key), patch.object(role, 'call', side_effect=fake) as call, patch.dict(os.environ, {'OPENAI_API_KEY': 'test', 'ANTHROPIC_BASE_URL': 'test'}):
                info = role.run(role.OUTPUT_BASE / 'followup-packet-v1', output)
                self.assertEqual(call.call_count, 1)
                self.assertFalse(info['replay_allowed'])
                self.assertFalse(info['live_B_allowed'])
                self.assertFalse(info['live_C_allowed'])
            self.assertFalse(key.exists())
            self.assertEqual((parent / 'checker.py').read_text(), source)
            self.assertEqual((output / 'candidate/checker.py').read_text(), source.replace('DEFAULT_LIMITS =', '# offline transport-only mock\nDEFAULT_LIMITS =', 1))


if __name__ == '__main__':
    unittest.main()
