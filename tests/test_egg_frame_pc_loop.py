"""Synthetic transport controls; these tests never dispatch a real Responses call."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from egg_fifo_loop_provider import ProviderError
from egg_frame_pc_loop import ARMS, run
from egg_frame_pc_seeds import fixture_revision

BINARY = Path(os.environ.get('CARGO_TARGET_DIR', ROOT / 'egraph/target')) / 'release/egg_diagnostic_forms'
CORPUS = ROOT / 'results/milestone3/frame-faults'
CONFIG = {'model': 'unit-test-model', 'reasoning_effort': 'low', 'max_output_tokens': 3072, 'transport': 'OpenAI Responses API'}


@unittest.skipUnless(BINARY.is_file(), 'build release egg_diagnostic_forms for actual local evidence')
class PCTransportControls(unittest.TestCase):
    def test_bad_candidate_returns_error_and_receipt_remains_counted(self):
        calls = []

        def fake_provider(messages, schema):
            calls.append(messages)
            monitors = fixture_revision('historical', 2)
            if len(messages) == 2:
                monitors['header_hold'] += ')'
            return {'id': f'resp_mock_{len(calls)}', 'output': {'monitors': monitors}, 'requested_model': CONFIG['model'],
                    'model': CONFIG['model'], 'status': 'completed', 'http_status': 200, 'dispatch_attempted': True,
                    'usage': {'input_tokens': 100, 'output_tokens': 20, 'total_tokens': 120}}

        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'run'
            result = run(corpus_dir=CORPUS, binary=BINARY, out=folder, mode='live', profiles=['historical'],
                         replicates=1, rounds=2, provider=fake_provider, provider_config=CONFIG)
            self.assertEqual(len(calls), 6)  # mock dispatch count only
            self.assertEqual(result['responses'], 6)
            for arm in ARMS:
                arm_dir = folder / 'historical' / 'trial-01' / arm
                first, second = arm_dir / 'round-01', arm_dir / 'round-02'
                self.assertFalse((first / 'oracles.json').exists())
                self.assertFalse((first / 'certificates.json').exists())
                self.assertIn('candidate_error', json.loads((first / 'assessment.json').read_text()))
                request = json.loads((second / 'request.json').read_text())
                self.assertIn('Invalid candidate:', request['messages'][-1]['content'])
                self.assertTrue(json.loads((second / 'assessment.json').read_text())['verified'])
                self.assertEqual(result['provider_usage'][arm]['total_tokens'], 240)

    def test_provider_error_keeps_partial_run_without_claiming_complete(self):
        def fake_failure(messages, schema):
            raise ProviderError('unit test transport failure', {'dispatch_attempted': True, 'http_status': 429, 'usage': None})

        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'run'
            with self.assertRaises(ProviderError):
                run(corpus_dir=CORPUS, binary=BINARY, out=folder, mode='live', profiles=['historical'],
                    replicates=1, rounds=2, provider=fake_failure, provider_config=CONFIG)
            self.assertFalse((folder / 'summary.json').exists())
            partial = json.loads((folder / 'incomplete.json').read_text())
            self.assertEqual(partial['attempted_steps'], 1)
            self.assertEqual(partial['completed_responses'], 0)
            self.assertTrue((folder / 'historical/trial-01/raw/round-01/provider-error.json').exists())


if __name__ == '__main__':
    unittest.main()
