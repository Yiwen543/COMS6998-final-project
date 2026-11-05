"""Evidence transport and credential boundaries, not checker semantics."""
import copy
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import prepare_wbxbar_reference_review as review


class ReferenceReviewTests(unittest.TestCase):
    def test_full_evidence_roundtrips(self):
        b = review.OUTPUT_BASE
        packet = b / 'code-review-packet-v1'
        manifest = review.verify(packet)
        body = json.loads((packet / 'packet.json').read_text())
        inputs = json.loads((b / 'controls-v1/inputs.json').read_text())
        limits = json.loads((b / 'controls-v1/limit-tests.json').read_text())
        inputs.update({'limit/' + n: x['rows'] for n, x in limits.items()})
        results = json.loads((b / 'evaluation-v1/cases.json').read_text())['cases']
        results.update({'limit/' + n: x for n, x in json.loads((b / 'evaluation-v1/limits.json').read_text()).items()})
        self.assertEqual(review.unpack_traces(body['traces']), inputs)
        self.assertEqual(review.unpack_results(body['full_checker_results']), results)
        self.assertEqual(len(inputs), 133)
        self.assertEqual(set(inputs), {x['name'] for x in body['expectations']})
        self.assertLessEqual(manifest['bytes'], manifest['byte_cap'])
        for f in review.FILES:
            self.assertEqual(body['candidate'][f], (b / 'claude-author-v1' / f).read_text())
        self.assertFalse(manifest['replay_allowed'])
        self.assertFalse(manifest['live_B_allowed'])
        self.assertFalse(manifest['live_C_allowed'])

    def test_generic_delta_does_not_hide_removals_arrays_or_type_changes(self):
        base = {'d': {'old': 0, 'kept': True}, 'a': [1, 2, 3], 'z': None}
        target = {'d': {'kept': 1, 'new': 'x'}, 'a': [1], 'z': {'nested': False}}
        original = copy.deepcopy(base)
        sets, deletes = review.changes(base, target)
        self.assertEqual(review.patch(base, sets, deletes), target)
        self.assertEqual(base, original)
        self.assertEqual(review.patch(base, *review.changes(base, None)), None)

    def test_packet_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'packet'
            shutil.copytree(review.OUTPUT_BASE / 'code-review-packet-v1', target)
            (target / 'prompt.txt').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'packet drift'):
                review.verify(target)

    def test_one_readonly_call_cleans_key_even_on_failure(self):
        packet = review.OUTPUT_BASE / 'code-review-packet-v1'
        for fails in (False, True):
            with tempfile.TemporaryDirectory() as folder:
                key = Path(folder) / 'test-key'
                key.write_text('offline-test-value')
                key.chmod(0o600)
                output = Path(folder) / 'review'
                def fake_call(prompt, destination, env, role):
                    self.assertEqual(env['ANTHROPIC_API_KEY'], 'offline-test-value')
                    self.assertNotIn('ANTHROPIC_BASE_URL', env)
                    self.assertNotIn('OPENAI_API_KEY', env)
                    destination.mkdir()
                    if fails:
                        raise RuntimeError('offline failure')
                    return {'ready_for_replay_registration': True, 'findings': [], 'limitations': [], 'required_followup': []}
                with patch.object(review, 'KEY_FILE', key), patch.object(review, 'call', side_effect=fake_call) as call, patch.dict(os.environ, {'OPENAI_API_KEY': 'test', 'ANTHROPIC_BASE_URL': 'test'}):
                    if fails:
                        with self.assertRaisesRegex(RuntimeError, 'offline failure'):
                            review.run(packet, output)
                    else:
                        result = review.run(packet, output)
                        self.assertTrue(result['schema_valid'])
                        self.assertFalse(result['automatic_replay_permission'])
                        self.assertFalse(result['live_C_allowed'])
                    self.assertEqual(call.call_count, 1)
                self.assertFalse(key.exists())


if __name__ == '__main__':
    unittest.main()
