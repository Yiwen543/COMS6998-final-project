import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from preflight_spi_host import map_counter, resolve_clock_alias
from run_spi_host_b_development import require_gate, evaluate, messages, group_status


class SpiPreflightTests(unittest.TestCase):
    def test_exact_mapping_no_line_only_fallback(self):
        target = {'outcome': 'cond_then', 'counter_anchor': {'source': 'x.sv', 'line': 3, 'column': 7}}
        point = {'source': 'x.sv', 'line': 3, 'column': 7, 'type': 'branch', 'outcome': 'cond_then', 'hits': 0}
        self.assertEqual(map_counter(target, [point])['status'], 'mapped')
        self.assertEqual(map_counter(target, [dict(point, column=8)])['status'], 'unresolved')
        self.assertEqual(map_counter(target, [point, point])['status'], 'unresolved')
        self.assertEqual(map_counter(target, [dict(point, outcome='cond_else')])['status'], 'unresolved')

    def test_buffer_alias_evidence_and_fail_closed(self):
        net = {'cells': {'buf': {'type': '$buf', 'parameters': {'WIDTH': '1'},
                                'connections': {'A': [2], 'Y': [100]}}}}
        result, evidence = resolve_clock_alias([100], net)
        self.assertEqual(result, [2])
        self.assertEqual(len(evidence), 1)
        net['cells']['buf']['connections']['A'] = [100]
        with self.assertRaises(AssertionError):
            resolve_clock_alias([100], net)

    def test_static_gate_prevents_live_and_mock_never_qualifies(self):
        config = json.loads((ROOT/'configs/spi_host_b_development.json').read_text())
        screen = {'qualified_for_model_trial': False, 'qualified_source_groups': 7, 'qualified_rewrite_groups': 0}
        with self.assertRaisesRegex(ValueError, 'Static gate failed'):
            require_gate(screen, config)
        self.assertFalse(evaluate([], config, False)['passed'])

    def test_prompt_excludes_semantic_and_calibration_evidence(self):
        prompt = messages([], [], {'checker': {'failures': []}}, '', [], 1, 8)
        data = json.loads(prompt[1]['content'])
        self.assertEqual(set(data), {'specification', 'rtl', 'cycle_field_order', 'common_seed',
            'previous_generated_cycles', 'round', 'max_new_cycles', 'checker', 'execution_log',
            'raw_uncovered_dut_coverage'})
        self.assertNotIn('calibration_hits', prompt[1]['content'])
        self.assertNotIn('eclass', prompt[1]['content'])

    def test_equivalent_sites_do_not_share_hits(self):
        point = {'source': 'x.sv', 'line': 3, 'column': 7, 'type': 'branch', 'outcome': 'if', 'hierarchy': 'tb.dut', 'hits': 1}
        second = dict(point, line=4, hits=0)
        screen = {'groups': [{'qualified_source_group': True, 'qualified_member_ids': ['a', 'b'],
            'eclass': 7, 'members': [{'id': name, 'line': p['line'], 'mapping': {'point': p}}
                                   for name, p in [('a', point), ('b', second)]]}]}
        group = group_status([point, second], screen)[0]
        self.assertEqual(group['raw_source_hits'], [1, 0])
        self.assertFalse(group['all_hit'])


if __name__ == '__main__':
    unittest.main()
