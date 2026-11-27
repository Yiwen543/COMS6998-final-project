"""Controlled proof-carrying request integration; no external calls in tests."""
from importlib.util import find_spec
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
if find_spec('z3'):
    from egg_regression_feedback import Feedback, style, validate_output
    from egg_regression_live import ARCHIVE, SCHEMA, _fixed, _seed, run
    from egg_txn_terms import parse_term

BINARY = os.environ.get('EGG_REGRESSION_BINARY')


@unittest.skipUnless(find_spec('z3'), 'requires z3-solver')
class FeedbackUnitTest(unittest.TestCase):
    def test_refactor_style_is_not_semantic_grading(self):
        self.assertTrue(style(parse_term('(eq 4 data_index)'), 4)['qualified'])
        self.assertFalse(style(parse_term('(and (eq data_index 4) (eq data_n data_index))'), 4)['qualified'])
        # Style can pass although the alarm is inequivalent to the original.
        _, ref, _ = _seed(ARCHIVE)
        result = Feedback(ref, 'raw').assess('(eq data_index 4)', '(eq data_n 4)', 4)['public']
        self.assertTrue(result['style']['qualified'])
        self.assertFalse(result['qualified'])
        self.assertNotEqual(result['reference_relation'], 'equivalent')

    def test_strict_output(self):
        for output in ({'monitor': 'true', 'extra': 1}, {'monitor': 1}, {'monitor': '(eq data_index 65536)'},
                       {'monitor': '(arbitrary-call m_valid)'}, {'monitor': ' ' * 17_000}):
            with self.assertRaises(ValueError):
                validate_output(output)


@unittest.skipUnless(find_spec('z3') and BINARY and Path(BINARY).is_file(),
                     'requires z3 and EGG_REGRESSION_BINARY')
class RegressionLiveIntegration(unittest.TestCase):
    @staticmethod
    def read(path):
        return json.loads(path.read_text())

    def test_fixture_delivers_scope_failure_and_prior_certificate_to_next_request(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'run'
            with patch('egg_regression_live.respond', side_effect=AssertionError('fixture must not call API')):
                result = run(archive=ARCHIVE, binary=BINARY, out=out, mode='fixture', attempts=2)
            self.assertEqual(result['responses'], 12)
            self.assertEqual(result['provider_api_calls'], 0)
            self.assertIsNone(result['provider_usage'])
            for arm in ('raw', 'ordinary', 'egg'):
                stages = result['arms'][arm]['stages']
                self.assertEqual([s['qualified'] for s in stages], [True]*3)
                self.assertEqual([len(s['attempts']) for s in stages], [1, 2, 1])
                self.assertEqual(stages[1]['preflight_relation'], 'incomparable')
                self.assertEqual(stages[1]['attempts'][0]['relation'], 'incomparable')
            egg = result['arms']['egg']
            self.assertEqual(egg['stored_proofs'], 2)
            self.assertEqual(egg['stages'][1]['preflight_egg_lookup_status'], 'blocked')
            self.assertEqual(egg['stages'][2]['attempts'][0]['egg_lookup_status'], 'reused')
            stage2 = out / 'egg' / 'stage-02'
            first = json.loads(self.read(stage2/'attempt-01/request.json')['messages'][-1]['content'])
            second = json.loads(self.read(stage2/'attempt-02/request.json')['messages'][-1]['content'])
            old = first['previous_stage']['last_assessment']['egg']
            self.assertEqual(old['guard'], '(eq data_n 4)')
            self.assertTrue(old['proved'])
            old_ref = old['proof_refs'][0]
            self.assertIn(old_ref, self.read(out/'egg'/'proof_store.json'))
            for request in (first, second):
                current = request['current_assessment']
                self.assertEqual(current['reference_relation'], 'incomparable')
                self.assertFalse(current['qualified'])
                self.assertEqual(current['egg']['lookup_status'], 'blocked')
                self.assertIn(old_ref, {r['entry_id'] for r in current['egg']['blocked_dependencies']})
                self.assertEqual(set(r['status'] for r in current['directions'].values()), {'sat'})
            stage3 = self.read(out/'egg/stage-03/attempt-01/assessment.json')
            self.assertEqual(stage3['public']['egg']['proof_refs'], [old_ref])
            # Factually matched ordinary/egg primitive evidence; raw does not get it.
            ordinary = self.read(out/'ordinary/stage-02/preflight.json')['public']
            egg_preflight = self.read(stage2/'preflight.json')['public']
            self.assertEqual(ordinary['ordinary'], egg_preflight['ordinary'])
            self.assertNotIn('egg', ordinary)
            self.assertNotIn('ordinary', self.read(out/'raw/stage-02/preflight.json')['public'])

    def test_injected_provider_boundary_and_receipt_accounting_without_network(self):
        # Test double exercising LIVE entry; temporary artifacts are never an
        # experiment result or an actual API receipt. No network calls occur.
        called = []
        _, reference, _ = _seed(ARCHIVE)
        def provider(messages, schema):
            self.assertEqual(schema, SCHEMA)
            packet = json.loads(messages[-1]['content'])
            called.append(packet)
            n = 4 if packet['current_guard'] == '(eq data_n 4)' else 5
            return {'id': f'resp_test_{len(called)}', 'model':'mock-model-for-unit-test',
                    'requested_model':'mock-model-for-unit-test', 'http_status': 200,
                    'status':'completed','dispatch_attempted':True,
                    'usage':{'input_tokens':7,'output_tokens':3,'total_tokens':10},
                    'output': {'monitor': _fixed(reference,n)}}
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)/'mock-live'
            summary = run(archive=ARCHIVE,binary=BINARY,out=out,mode='live',attempts=3,
                          provider=provider,provider_config={'model':'mock-model-for-unit-test','max_output_tokens':16})
            self.assertEqual(len(called),9) # early stop, not 27
            self.assertEqual(summary['provider_usage']['total_tokens'],90)
            self.assertEqual(summary['provider_api_calls'],9)
            self.assertTrue(any(x['previous_stage'] and x['previous_stage']['last_assessment'].get('egg')
                                and x['current_assessment'].get('egg',{}).get('lookup_status')=='blocked'
                                for x in called))
