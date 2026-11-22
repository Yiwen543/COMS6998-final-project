"""Finite replay obligations must return the earliest original sample or finite UNSAT."""
from importlib.util import find_spec
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


@unittest.skipUnless(find_spec('z3'), 'requires z3-solver')
class ControllerTraceTests(unittest.TestCase):
    def test_earliest_witness_and_no_state_leak_between_queries(self):
        from m3_controller_solver import FiniteTraceSolver
        solver = FiniteTraceSolver([{'rx': 0, 'tx': 1}, {'rx': 1, 'tx': 1},
                                    {'rx': 1, 'tx': 0}, {'rx': 1, 'tx': 1}], 1000)
        self.assertEqual(solver.first_hit('(and rx tx)'), 1)
        self.assertIsNone(solver.first_hit('(and rx (not rx))'))
        self.assertEqual(solver.first_hit('(not tx)'), 2)
        self.assertEqual(solver.first_hit('(or rx tx)'), 0)

    def test_missing_atom_cannot_silently_become_false(self):
        from m3_controller_solver import FiniteTraceSolver
        with self.assertRaises(ValueError):
            FiniteTraceSolver([{'rx': 1}, {'tx': 1}], 1000)
        with self.assertRaises(ValueError):
            FiniteTraceSolver([{'rx': None}], 1000)
