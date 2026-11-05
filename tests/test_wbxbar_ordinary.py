"""Adversarial checks of transport evidence, not a DUT functional checker."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from probe_wbxbar_ordinary import cases, validate, driver, parse, comparable
from prove_wbxbar_index import configuration

BASE = ROOT / 'results/wbxbar_conditional_20261104'


class OrdinaryTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, c = configuration()
        ports = json.loads((BASE / 'screen-v2/netlist.json').read_text())['modules']['wbxbar']['ports']
        _, cls.ins, cls.outs = driver(c, ports)
        cls.actions = cases()['isolated_m0_d0_w1']
        cls.log = (BASE / 'ordinary-v1/isolated_m0_d0_w1/iverilog/simulation.log').read_text()

    def test_illegal_width_type_fields_and_seed_rejected(self):
        for field, value in [('data', 1 << 64), ('offer', -1), ('we', True), ('rst', '0')]:
            actions = copy.deepcopy(self.actions)
            actions[8][field] = value
            with self.assertRaises(ValueError): validate(actions)
        actions = copy.deepcopy(self.actions)
        actions[8]['extra'] = 1
        with self.assertRaises(ValueError): validate(actions)
        with self.assertRaises(ValueError): validate(self.actions[1:])
        with self.assertRaises(ValueError): validate(self.actions + [self.actions[-1]] * 392)

    def test_saved_transport_is_complete(self):
        trace = parse(self.log, self.actions, self.ins, self.outs)
        self.assertEqual(len(trace), len(self.actions))
        self.assertTrue(comparable(trace, self.outs))

    def test_corrupt_payload_rejected(self):
        lines = self.log.splitlines()
        index = next(i for i, line in enumerate(lines) if line.startswith('PRE 8 '))
        fields = lines[index].split()
        field = 2 + (self.ins + self.outs).index('i_mdata')
        fields[field] = format(int(fields[field], 16) ^ 1, 'x')
        lines[index] = ' '.join(fields)
        with self.assertRaisesRegex(ValueError, 'Input driver/JSON mismatch'):
            parse('\n'.join(lines), self.actions, self.ins, self.outs)

    def test_corrupt_acceptance_ledger_rejected(self):
        lines = self.log.splitlines()
        index = next(i for i, line in enumerate(lines) if line.startswith('QUEUE 8 0 '))
        fields = lines[index].split()
        fields[3] = str(int(fields[3]) + 1)
        lines[index] = ' '.join(fields)
        with self.assertRaisesRegex(ValueError, 'Transport ledger disagreement'):
            parse('\n'.join(lines), self.actions, self.ins, self.outs)

    def test_missing_cycle_rejected(self):
        log = '\n'.join(line for line in self.log.splitlines() if not line.startswith(('PRE 8 ', 'POST 8 ')))
        with self.assertRaisesRegex(ValueError, 'Incomplete trace'):
            parse(log, self.actions, self.ins, self.outs)

    def test_unknown_active_payload_is_not_masked(self):
        trace = parse(self.log, self.actions, self.ins, self.outs)
        row = next(t for t in trace if t['pre']['o_mack'])
        row['pre']['o_mdata'] = None
        with self.assertRaisesRegex(ValueError, 'Unknown meaningful output'):
            comparable(trace, self.outs)


if __name__ == '__main__':
    unittest.main()
