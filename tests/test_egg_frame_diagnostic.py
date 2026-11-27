"""Independent acceptance gates for single-source alarm generation."""
from importlib.util import find_spec
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
BINARY = Path(os.environ.get('CARGO_TARGET_DIR', ROOT / 'egraph/target')) / 'release/egg_diagnostic_forms'
if find_spec('z3'):
    from egg_frame_diagnostic import check_engine, generate, restore
    from egg_frame_terms import REFERENCES


@unittest.skipUnless(find_spec('z3'), 'requires z3-solver')
class Diagnostic(unittest.TestCase):
    def test_reject_changed_source_and_unproved_extraction(self):
        source = '(and rst h_valid)'
        atoms = {'rst': 'rst', 'h_valid': 'h_valid'}
        identity = {'source': source, 'extracted': source, 'explanation': None,
                    'stop_reason': 'Some(Saturated)'}
        self.assertTrue(check_engine(source, source, atoms, identity)['accepted'])
        for field, value in [('source', 'h_valid'), ('extracted', 'h_valid'),
                             ('explanation', 'invalid')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_engine(source, source, atoms, {**identity, field: value})
        self.assertFalse(check_engine(source, source, atoms, {**identity, 'stop_reason': 'Some(NodeLimit(20001))'})['accepted'])
        with self.assertRaisesRegex(ValueError, 'invented'):
            restore('(and rst m_valid)', atoms)

    def test_reject_forged_step(self):
        ref = '(and rst (or h_valid m_valid))'
        candidate = '(or (and rst h_valid) (and rst m_valid))'
        atoms = {atom: atom for atom in ('rst', 'h_valid', 'm_valid')}
        graph = {'source': ref, 'extracted': candidate, 'stop_reason': 'Some(Saturated)',
                 'explanation': ref + '\n(Rewrite=> and-distribute-right ' + candidate + ')'}
        self.assertEqual(len(check_engine(ref, ref, atoms, graph)['checked_steps']), 1)
        with self.assertRaises(ValueError):
            check_engine(ref, ref, atoms, {**graph, 'explanation': graph['explanation'].replace('and-distribute-right', 'double-not')})
        with self.assertRaises(ValueError):
            check_engine('(and rst h_valid)', ref, atoms, graph)

    @unittest.skipUnless(BINARY.is_file(), 'build release egg_diagnostic_forms to test actual extraction')
    def test_actual_source_only_extraction(self):
        result = generate(BINARY)
        self.assertEqual(set(result['properties']), set(REFERENCES))
        for name, item in result['properties'].items():
            with self.subTest(name=name):
                self.assertEqual(set(item['engine_request']), {'term', 'pattern_rules'})
                self.assertTrue(item['accepted'])
                self.assertTrue(item['checked_steps'])
                self.assertEqual(item['equivalence']['status'], 'unsat')
                self.assertTrue(all(c['implication']['status'] == 'unsat' for c in item['clauses']))


if __name__ == '__main__':
    unittest.main()
