"""Semantic safety and fair-budget regression checks; never calls a model API."""
import copy
import itertools
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from agent_core import simplify, semantic_groups
from predicates import parse, evaluate
from compare_experiments import compare


class SemanticTests(unittest.TestCase):
    def test_baseline_preserves_truth_tables(self):
        cases = ['(and a true)', '(or a false)', '(not (not a))',
                 '(and a (or a b))', '(or a (and a b))',
                 '(and (and b a) (and a c))', '(not (and a b))',
                 '(and false a)', '(or true a)']
        for expr in cases:
            original = parse(expr)
            for bits in itertools.product((0, 1), repeat=3):
                env = dict(zip('abc', bits))
                self.assertEqual(evaluate(original, env), evaluate(simplify(original), env))

    def test_equal_logic_different_sampling_context_is_not_grouped(self):
        targets = [dict(id='a', event='posedge clk', width=1, logic='two_state'),
                   dict(id='b', event='negedge clk', width=1, logic='two_state')]
        graph = {'targets': [dict(id='a', eclass=1), dict(id='b', eclass=1)]}
        self.assertEqual(semantic_groups(targets, {'a': 'x', 'b': 'x'}, graph), [])

    def test_budget_snapshot_excludes_overshoot_and_rejects_unfair_runs(self):
        c = dict(live_api=True, usage_complete=True, dut_sha256='dut', tb_sha256='tb',
                 config=dict(group='C', model='same', run_id='r1'), stop_reason='round_budget',
                 initial={'coverage': {'branch': {'covered': 3, 'total': 18}}},
                 measured_usage={'total_tokens': 200}, rounds=[
                     dict(status='completed', round=1, cumulative_measured_tokens=80,
                          coverage={'branch': {'covered': 5, 'total': 18}}, batch_size=2),
                     dict(status='completed', round=2, cumulative_measured_tokens=200,
                          coverage={'branch': {'covered': 10, 'total': 18}}, batch_size=2)])
        d = copy.deepcopy(c)
        d['config']['group'] = 'D'
        result = compare(c, d, 100)
        self.assertEqual(result['C']['new_branch_points'], 2)
        self.assertEqual(result['C']['last_completed_round_within_budget'], 1)
        self.assertEqual(result['C']['total_observed_tokens_including_overshoot'], 200)
        c_line, d_line = copy.deepcopy(c), copy.deepcopy(d)
        for record in (c_line, d_line):
            record['coverage_objective'] = 'line'
            record['initial']['coverage'] = {'line': {'covered': 3, 'total': 18}}
            for row in record['rounds']:
                row['coverage'] = {'line': row['coverage']['branch']}
        line_result = compare(c_line, d_line, 100)
        self.assertEqual(line_result['C']['new_coverage_points'], 2)
        self.assertIsNone(line_result['C']['new_branch_points'])
        self.assertIsNone(line_result['paired_new_branch_difference_C_minus_D'])
        d_line['checker_sha256'] = 'changed-checker'
        with self.assertRaises(ValueError):
            compare(c_line, d_line, 100)
        d['config']['model'] = 'different'
        with self.assertRaises(ValueError):
            compare(c, d, 100)
        d['config']['model'] = 'same'
        d['live_api'] = False
        with self.assertRaises(ValueError):
            compare(c, d, 100)
