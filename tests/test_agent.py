"""Offline tests for budget accounting, feedback parity and API response handling."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from agent_core import (ast_text, factor_shared, feedback, output_json, request_body,
                        usage_counts, validate_batch)
from predicates import ROOT, extract, parse, evaluate, environment
from run_agent import Config, experiment

TARGETS = extract()
GRAPH = json.loads((ROOT / 'results/step1/egraph.json').read_text())
POINTS = json.loads((ROOT / 'results/step1/initial-coverage.json').read_text())['points']


def vector(over):
    return {'target_id': 'spec_probe', 'reset': 0, 'req': 0, 'priority_override': over}


def response(vectors, status='completed'):
    return {'id': 'offline-test-response', 'model': 'test-double', 'status': status,
            'usage': {'input_tokens': 10, 'output_tokens': 3,
                      'output_tokens_details': {'reasoning_tokens': 2}},
            'output': [{'type': 'message', 'content': [
                {'type': 'output_text', 'text': json.dumps({'note': 'test', 'vectors': vectors})}]}]}


class Provider:
    is_live = False
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []
    def generate(self, body):
        self.requests.append(body)
        return next(self.responses)


class Simulator:
    name = 'test-double-not-RTL-simulation'
    targets = TARGETS
    graph = GRAPH
    def prepare(self, out, group):
        return {'test_double': True}
    def simulate(self, vectors, folder):
        folder.mkdir(exist_ok=True)
        points = copy.deepcopy(POINTS)
        for v in vectors:
            env = environment(v['reset'], v['req'], v['priority_override'])
            for t in TARGETS:
                if evaluate(parse(t['compact']), env):
                    for p in points:
                        if (p['line'], p['type'], p['outcome']) == (
                                t['line'], t['counter_type'], t['counter_outcome']):
                            p['hits'] += 1
        return {'checker': {'checks': 4 + len(vectors), 'functional_errors': 0,
                            'timing_errors': 0},
                'points': points, 'log': 'test-double only', 'simulation_seconds': 0}


def expand(node, definitions):
    if isinstance(node, str):
        return expand(parse(definitions[node]), definitions) if node in definitions else node
    return (node[0], *(expand(n, definitions) for n in node[1:]))


class FeedbackTests(unittest.TestCase):
    def test_a_has_no_counter_leak_and_bcd_have_same_source_targets(self):
        self.assertEqual(feedback('A', TARGETS, GRAPH, POINTS), {})
        arms = [feedback(g, TARGETS, GRAPH, POINTS) for g in 'BCD']
        for arm in arms:
            self.assertEqual(len(arm['uncovered_targets']), 14)
            self.assertEqual(arm['raw_dut_coverage'], arms[0]['raw_dut_coverage'])
            self.assertNotIn('suggested_stimulus', json.dumps(arm))
        metadata = lambda arm: [{k: v for k, v in t.items() if k != 'predicate'}
                               for t in arm['uncovered_targets']]
        self.assertEqual(metadata(arms[0]), metadata(arms[1]))
        self.assertEqual(metadata(arms[0]), metadata(arms[2]))

    def test_factored_feedback_preserves_all_legal_mask_semantics(self):
        by_id = {t['id']: t for t in TARGETS}
        for group in 'BCD':
            data = feedback(group, TARGETS, GRAPH, POINTS)
            definitions = data.get('shared_conditions', {})
            for t in data['uncovered_targets']:
                original = by_id[t['id']]
                raw = parse(original['compact'])
                rendered = expand(parse(t['predicate']), definitions)
                for reset in range(2):
                    for mask in range(256):
                        for opposite in range(2):
                            req, over = ((mask, opposite) if original['kind'] == 'req'
                                         else (opposite, mask))
                            env = environment(reset, req, over)
                            self.assertEqual(evaluate(raw, env), evaluate(rendered, env),
                                             (group, t['id'], reset, mask, opposite))

    def test_requests_only_differ_in_feedback(self):
        config = Config()
        common = {'rtl': 'fixed', 'specification': 'fixed', 'previous_vectors': []}
        requests = []
        for group in 'BCD':
            context = {**common, **feedback(group, TARGETS, GRAPH, POINTS)}
            body = request_body(config, context, TARGETS, 16)
            requests.append(body)
        without_input = lambda r: {k: v for k, v in r.items() if k != 'input'}
        self.assertEqual(without_input(requests[0]), without_input(requests[1]))
        self.assertEqual(without_input(requests[0]), without_input(requests[2]))
        self.assertEqual(requests[0]['input'][0], requests[1]['input'][0])


class ResponseTests(unittest.TestCase):
    def test_rejects_bool_out_of_range_unknown_target_and_extra_fields(self):
        for key, value in [('reset', True), ('req', 256), ('priority_override', -1),
                           ('target_id', 'invented')]:
            data = {'note': 'x', 'vectors': [{**vector(2), key: value}]}
            with self.assertRaises(ValueError):
                validate_batch(data, TARGETS, 16)
        with self.assertRaises(ValueError):
            validate_batch({'note': '', 'vectors': [{**vector(2), 'code': 'bad'}]}, TARGETS, 16)

    def test_incomplete_and_refusal_do_not_parse_as_vectors(self):
        with self.assertRaises(ValueError):
            output_json(response([vector(2)], status='incomplete'))
        refused = response([])
        refused['output'][0]['content'] = [{'type': 'refusal', 'refusal': 'No'}]
        with self.assertRaises(ValueError):
            output_json(refused)

    def test_reasoning_tokens_are_not_double_counted(self):
        usage = usage_counts(response([vector(2)]))
        self.assertEqual(usage['total_tokens'], 13)
        self.assertEqual(usage['reasoning_tokens'], 2)


class ControllerTests(unittest.TestCase):
    def run_case(self, config, responses):
        provider = Provider(responses)
        with tempfile.TemporaryDirectory() as tmp:
            record = experiment(config, Simulator(), provider, Path(tmp))
            saved = json.loads((Path(tmp) / 'summary.json').read_text())
            self.assertEqual(saved['stop_reason'], record['stop_reason'])
            return record, provider.requests

    def test_multiround_replay_cost_and_new_coverage(self):
        record, requests = self.run_case(Config(max_rounds=2),
                                        [response([vector(2)]), response([vector(4)])])
        self.assertEqual(record['simulator_executions'], 3)
        self.assertEqual(record['total_checked_cycles'], 4 + 5 + 6)
        self.assertEqual(record['new_branch_points'], 2)
        self.assertEqual(record['measured_usage']['total_tokens'], 26)
        self.assertIsNone(record['token_roi'])
        second = json.loads(requests[1]['input'][1]['content'])
        self.assertEqual(second['previous_submitted_vectors_replayed_each_run'], [vector(2)])

    def test_cycle_budget_charges_replayed_cycles(self):
        record, _ = self.run_case(Config(max_rounds=5, max_checked_cycles=9),
                                  [response([vector(2)])])
        self.assertEqual(record['stop_reason'], 'cycle_budget')
        self.assertEqual(record['api_attempts'], 1)
        self.assertEqual(record['total_checked_cycles'], 9)

    def test_invalid_response_usage_is_counted_and_error_reaches_next_turn(self):
        bad = response([vector(2)], status='incomplete')
        record, requests = self.run_case(Config(max_rounds=2),
                                        [bad, response([vector(2)])])
        self.assertEqual(record['rounds'][0]['status'], 'invalid_response')
        self.assertEqual(record['measured_usage']['total_tokens'], 26)
        self.assertEqual(record['simulator_executions'], 2)
        self.assertIn('not completed', json.loads(requests[1]['input'][1]['content'])['last_response_error'])

    def test_plateau_stops_without_waiving_unreachable_counters(self):
        record, _ = self.run_case(Config(max_rounds=5, plateau_rounds=2),
                                  [response([vector(2)])] * 3)
        self.assertEqual(record['stop_reason'], 'coverage_plateau')
        self.assertEqual(record['api_attempts'], 3)
        self.assertEqual(record['initial']['coverage']['branch']['total'],
                         record['final']['coverage']['branch']['total'])

    def test_token_threshold_checked_between_requests(self):
        record, _ = self.run_case(Config(stop_after_tokens=10),
                                  [response([vector(2)])])
        self.assertEqual(record['stop_reason'], 'observed_token_threshold')
        self.assertEqual(record['measured_usage']['total_tokens'], 13)

    def test_api_failure_is_saved_without_retries(self):
        class FailingProvider(Provider):
            def generate(self, body):
                raise RuntimeError('network failed')
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                experiment(Config(), Simulator(), FailingProvider([]), Path(tmp))
            record = json.loads((Path(tmp) / 'summary.json').read_text())
            self.assertEqual(record['api_attempts'], 1)
            self.assertFalse(record['usage_complete'])
            self.assertEqual(record['stop_reason'], 'error')


if __name__ == '__main__':
    unittest.main()
