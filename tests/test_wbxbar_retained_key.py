"""The user's retention policy survives success/failure and grants no gate."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import review_wbxbar_retained_key as role
from prepare_wbxbar_reference_checker import OUTPUT_BASE


class RetainedKeyTests(unittest.TestCase):
    def test_success_or_failure_keeps_private_key_and_no_permission(self):
        for fails in (False, True):
            with self.subTest(fails=fails), tempfile.TemporaryDirectory() as folder:
                key = Path(folder) / 'private-key'
                key.write_text('offline-only')
                key.chmod(0o600)
                out = Path(folder) / 'review'
                def fake(prompt, output, env, job):
                    output.mkdir()
                    if fails:
                        raise RuntimeError('offline failure')
                    return {'ready_for_replay_registration': True, 'findings': [], 'contract_decision_assessments': [], 'required_followup': [], 'limitations': []}
                with patch.object(role, 'KEY_FILE', key), patch.object(role, 'call', side_effect=fake) as call:
                    if fails:
                        with self.assertRaisesRegex(RuntimeError, 'offline failure'):
                            role.run(OUTPUT_BASE / 'termination-review-packet-v1', out)
                    else:
                        result = role.run(OUTPUT_BASE / 'termination-review-packet-v1', out)
                        self.assertTrue(result['model_readiness'])
                        self.assertFalse(result['checker_validated'])
                        self.assertFalse(result['replay_allowed'])
                    self.assertEqual(call.call_count, 1)
                self.assertTrue(key.exists())
                self.assertEqual(key.stat().st_mode & 0o777, 0o600)
                self.assertNotIn('offline-only', (out / 'credential-policy.json').read_text())
                self.assertTrue(json.loads((out / 'credential-policy.json').read_text())['retained_after_call'])


if __name__ == '__main__':
    unittest.main()
