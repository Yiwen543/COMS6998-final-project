"""Differential controls for the pinned arbiter's bit-parallel witness search."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from predicates import _atom_tables, _truth_table, environment, evaluate, extract, parse, witness, witness_fast


class WitnessTests(unittest.TestCase):
    def test_legal_assignment_tables(self):
        # Populate independent expected bytes in the original nested-loop order.
        states = 2 * 256 * 256
        expr = parse('(and (or req3 override7) (not (and reset override_any)))')
        expected = {name: bytearray(states // 8) for name in environment(0, 0, 0)}
        expected['expression'] = bytearray(states // 8)
        assignments = itertools.product(range(2), range(256), range(256))
        for index, (reset, override, req) in enumerate(assignments):
            values = environment(reset, req, override)
            values['expression'] = evaluate(expr, values)
            byte, bit = divmod(index, 8)
            for name, high in values.items():
                if high:
                    expected[name][byte] |= 1 << bit
        atoms = _atom_tables()
        actual = dict(atoms, expression=_truth_table(expr, atoms))
        for name, value in expected.items():
            self.assertEqual(actual[name].to_bytes(states // 8, 'little'), value, name)

    def test_first_witness_matches_scalar(self):
        guards = [target[form] for target in extract() for form in ('compact', 'expanded')]
        guards += [
            'true', 'false', '(and req1 (not req1))',
            '(and override7 (not override_any))', '(and reset (and override7 req7))',
            '(or req7 override0)',
        ]
        for guard in guards:
            with self.subTest(guard=guard):
                self.assertEqual(witness_fast(guard), witness(guard))


if __name__ == '__main__':
    unittest.main()
