import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from check_egg_regression_dependencies import run


class DependencyAuditTests(unittest.TestCase):
    def test_frozen_scope_edit_and_missing_vs_invalid(self):
        base=ROOT/'results/milestone3/frame-txn-semantic-regression'
        observed=run(base)
        published=json.loads((base/'dependencies.json').read_text())
        self.assertEqual(observed['blocked_requests'],6)
        self.assertEqual(observed['unique_rechecks'],27)
        self.assertEqual(observed['missing_dependency_occurrences'],published['missing_dependency_occurrences'])
        self.assertEqual(observed['missing_dependency_occurrences'],{'invalid_in_current_scope':46,'still_valid_but_absent':6})
        self.assertTrue(observed['scope_edit_exact_dependency_examples'])
        for example in observed['scope_edit_exact_dependency_examples']:
            self.assertEqual(example['status'],'invalid_in_current_scope')
            self.assertEqual(example['typed_check']['guard'],'(eq data_n 5)')
            self.assertNotEqual(example['typed_check']['relation'],'equivalent')
