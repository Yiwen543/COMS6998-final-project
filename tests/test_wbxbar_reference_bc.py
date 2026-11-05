"""Reference-checker binding, common feedback, immutable budget and stateless API."""
import copy
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import wbxbar_reference_experiment as new
import wbxbar_experiment as old
from run_wbxbar_reference_bc import run, schedule
from pilot_model import OpenAIModel


class ReferenceBCTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = new.read(new.BASE / 'offline-config.json')
        cls.batch = new.ROOT / 'results/wbxbar_reference_replay_20261104/replay-v1/rep1-B/round6'
        cls.trace = new.read(cls.batch / 'trace.json')
        cls.checked = new.read(cls.batch / 'checker-output.json')
        cls.points = new.read(cls.batch / 'raw-points.json')

    def test_old_scope_and_new_checker_are_bound(self):
        original = old.verify_freeze()
        registered = new.verify_registration()
        for name in new.FIXED_FIELDS:
            self.assertEqual(registered[name], original[name], name)
        self.assertNotEqual(registered['checker_sha256'], original['checker_sha256'])
        self.assertEqual(registered['checker_sha256'], new.sha(new.CANDIDATE / 'checker.py'))

    def test_simulation_and_worker_body_are_unchanged(self):
        self.assertEqual(inspect.getsource(new.simulate), inspect.getsource(old.simulate))
        self.assertEqual(inspect.getsource(new.check_trace), inspect.getsource(old.check_trace))
        self.assertIs(new.compile_driver, old.compile_driver)
        self.assertIs(new.messages, old.messages)

    def test_actual_worker_uses_reference_not_old_checker(self):
        with tempfile.TemporaryDirectory() as folder:
            result = new.check_trace(self.trace, Path(folder))
        self.assertEqual(result, self.checked)
        self.assertEqual(result['verdict'], 'unresolved')
        self.assertGreater(len(result['unresolved']), 8)
        self.assertEqual(new.read(new.ROOT / 'results/wbxbar_exploratory_bc_20261104/live-v1/rep1-B/round6/result.json')['checker']['verdict'], 'dut_violation')

    def test_feedback_keeps_equal_unresolved_information(self):
        prior = {'checker': self.checked, 'transport': {}, 'verification_complete': False}
        original = copy.deepcopy(prior)
        b = new.messages(self.config, 'B', [], prior, self.points, self.trace, 1)
        c = new.messages(self.config, 'C', [], prior, self.points, self.trace, 1)
        common = json.loads(c[1]['content'])
        common.pop('semantic_relations')
        self.assertEqual(json.loads(b[1]['content']), common)
        self.assertEqual(b[0], c[0])
        self.assertEqual(common['checker']['unresolved']['total'], len(self.checked['unresolved']))
        self.assertEqual(common['checker']['unresolved']['first_eight'], self.checked['unresolved'][:8])
        self.assertFalse(common['verification_complete'])
        self.assertEqual(prior, original)

    def test_budget_checker_and_permission_tamper_rejected(self):
        for key in ('development_budget', 'checker_candidate', 'live_B_allowed'):
            changed = copy.deepcopy(self.config)
            if key == 'development_budget':
                changed[key]['rounds'] = 1
            elif key == 'checker_candidate':
                changed[key] = str(old.CANDIDATE.relative_to(new.ROOT))
            else:
                changed[key] = True
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'bad.json'
                path.write_text(json.dumps(changed))
                with self.assertRaises(ValueError):
                    new.verify_freeze(path)

    def test_offline_config_cannot_launch_live(self):
        with patch('run_wbxbar_reference_bc.OpenAIModel') as model:
            with self.assertRaisesRegex(ValueError, 'Final live freeze required'):
                run(SimpleNamespace(config=new.BASE / 'offline-config.json', mode='live'))
            model.assert_not_called()

    def test_original_schedule_and_schema_preserved(self):
        items = list(schedule(self.config))
        self.assertEqual(len(items), 36)
        self.assertEqual(items[:2], [(1, 1, 'B'), (1, 1, 'C')])
        self.assertEqual(items[12:14], [(2, 1, 'C'), (2, 1, 'B')])
        for arm in ('B', 'C'):
            self.assertEqual(sum(a == arm for _, _, a in items), 18)
        self.assertEqual(new.schema(), old.schema())
        self.assertEqual(new.seed(), old.seed())

    def test_api_requests_are_stateless_and_exact_model(self):
        adapter = OpenAIModel.__new__(OpenAIModel)
        adapter.config = {**self.config['model_limits'], 'max_output_tokens': self.config['model_limits']['output_tokens']}
        adapter.schema, adapter.schema_name = new.schema(), 'wbxbar_offers'
        adapter.client = Mock()
        adapter.client.responses.input_tokens.count.return_value = SimpleNamespace(input_tokens=12)
        adapter.client.responses.create.return_value = SimpleNamespace(model='gpt-6.1-sol', id='offline-test',
            status='completed', incomplete_details=None, output_text=json.dumps({'actions': [new.action()]}),
            usage={'input_tokens': 10, 'output_tokens': 4, 'total_tokens': 14,
                   'input_tokens_details': {'cached_tokens': 8}, 'output_tokens_details': {'reasoning_tokens': 2}})
        messages = [{'role': 'user', 'content': 'offline fixture'}]
        self.assertEqual(adapter.count_input_tokens(messages), 12)
        output = adapter.generate(messages, {})
        request = adapter.client.responses.create.call_args.kwargs
        self.assertNotIn('previous_response_id', request)
        self.assertNotIn('conversation', request)
        self.assertFalse(request['store'])
        self.assertEqual(request['model'], 'gpt-6.1-sol')
        self.assertEqual(request['max_output_tokens'], 16384)
        self.assertEqual(output['usage']['input_tokens'] + output['usage']['output_tokens'], 14)


if __name__ == '__main__':
    unittest.main()
