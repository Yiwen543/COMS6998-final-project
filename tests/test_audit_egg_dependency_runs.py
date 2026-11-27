"""Rebuild the chronological ladder from actual native proof receipts; reject forged reuse."""
from copy import deepcopy
import gzip
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from run_egg_dependencies import Arm


RUN = ROOT / 'results/milestone3/frame-txn-dependency-reuse/triage'


class ArchivedDependencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with gzip.open(RUN / 'groups.jsonl.gz', 'rt', encoding='utf8') as stream:
            cls.ladder = [g for line in stream if (g := json.loads(line))['workload'] == 'ladder']

    def prefix(self, name, n):
        arm = Arm(name, None)  # replay must not invoke the Rust binary
        for g in self.ladder[:n]:
            arm.group(g['cases'], g['arms'][name])
        return arm

    def test_archived_transitive_reuse_and_failed_dependency_triage(self):
        name = 'egg_dependency_triage'
        arm = self.prefix(name, len(self.ladder))
        def record(index):
            return self.ladder[index]['arms'][name]

        cross = record(1)
        row = cross['rows'][0]
        self.assertEqual((row['id'], row['via'], row['lookup']['status']), ('C03', 'history', 'revalidated'))
        edges = row['lookup']['edges']
        self.assertEqual(len(edges), 2)
        self.assertEqual(edges[0]['right'], edges[1]['left'])
        self.assertIsNone(cross['native'])
        misses = [e for e in cross['fact_events'] if e['kind'] == 'dependency' and e['cache'] == 'miss']
        self.assertEqual({(e['typed_left'], e['typed_right'], e['status']) for e in misses},
                         {('(ult data_n 8)', 'true', 'unsat'), ('(ult data_n 9)', 'true', 'unsat')})
        self.assertEqual(len(misses), 2)
        self.assertTrue(any(e['typed_left'] == '(ult data_n 8)' and e['outside_current_atoms'] for e in misses))

        reproof = record(3)['rows'][0]
        self.assertEqual((reproof['id'], reproof['lookup']['status'], reproof['via']), ('C05', 'blocked', 'native_proof'))
        self.assertEqual(reproof['lookup']['blocked'][0]['status'], 'sat')
        self.assertEqual(reproof['triage']['relation'], 'equivalent')
        self.assertIsNotNone(record(3)['native'])
        for i in (4, 5):
            rejected = record(i)['rows'][0]
            self.assertEqual(rejected['triage']['relation'], 'weakened')
            self.assertEqual(rejected['via'], 'triage_typed')
            self.assertIsNone(record(i)['native'])
            self.assertFalse(any(e['kind'] == 'full_discovery' for e in record(i)['fact_events']))
        self.assertEqual(record(6)['rows'][0]['lookup']['status'], 'reused')
        self.assertEqual(record(8)['rows'][0]['relation'], 'infeasible')
        self.assertEqual(arm.summary()['correct'], 10)
        self.assertEqual(arm.summary()['all_typed_checks'], 139)
        self.assertEqual(arm.summary()['nonidentity_equivalent_with_proof_route'], 7)

    def test_archived_ordinary_core_comparator(self):
        arm = self.prefix('ordinary_dependency_triage', len(self.ladder))
        self.assertEqual(arm.summary()['correct'], 10)
        self.assertEqual(arm.summary()['all_typed_checks'], 139)
        self.assertEqual(arm.summary()['nonidentity_equivalent_with_proof_route'], 7)
        self.assertGreater(arm.summary()['boolean_checks']['boolean_core_replay_checks'], 0)
        self.assertEqual(arm.summary()['native_graph_counts'], {})

    def test_reject_corrupted_dependency_receipt_or_path(self):
        name = 'egg_dependency_triage'
        g = self.ladder[1]
        original = g['arms'][name]
        wrong_fact = deepcopy(original)
        dependency = next(e for e in wrong_fact['fact_events'] if e['kind'] == 'dependency')
        dependency['status'] = dependency['query']['status'] = 'sat'
        wrong_path = deepcopy(original)
        wrong_path['rows'][0]['lookup']['edges'][0]['new_guard'] = '(eq data_n 4)'
        missing_edge = deepcopy(original)
        missing_edge['rows'][0]['lookup']['edges'].pop()
        for bad in (wrong_fact, wrong_path, missing_edge):
            with self.subTest(bad=next(iter(bad))):
                arm = self.prefix(name, 1)
                with self.assertRaisesRegex(ValueError, 'archived group evidence differs'):
                    arm.group(g['cases'], bad)

    def test_reject_failed_leaf_as_target_inequality(self):
        name = 'egg_dependency_triage'
        g = self.ladder[3]  # C05: old leaf false, whole target still equivalent
        bad = deepcopy(g['arms'][name])
        row = bad['rows'][0]
        row['triage']['relation'] = 'weakened'
        row['via'], row['relation'] = 'triage_typed', 'weakened'
        with self.assertRaisesRegex(ValueError, 'saved typed result differs|classification'):
            self.prefix(name, 3).group(g['cases'], bad)


if __name__ == '__main__':
    unittest.main()
