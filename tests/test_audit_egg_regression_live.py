import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from audit_egg_regression_live import audit


ARCHIVE = ROOT/'results/milestone3/frame-txn-regression-live/transcript.tar.gz'
LIVE = 'live-20261125-173313'


class RegressionLiveAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        with tarfile.open(ARCHIVE) as tar:
            tar.extractall(self.root, filter='data')

    @staticmethod
    def mutate(path, change):
        value = json.loads(path.read_text())
        change(value)
        path.write_text(json.dumps(value))

    def test_actual_completed_live_and_proof_lifecycle(self):
        report = audit(self.root/LIVE)
        self.assertTrue(report['complete'])
        self.assertEqual(report['audited_summary']['provider_api_calls'], 9)
        self.assertEqual(report['audited_summary']['provider_usage']['total_tokens'], 18087)
        self.assertEqual(report['unique_qualified_monitor_strings'], 2)
        self.assertTrue(all(x['same_qualified_text'] for x in report['stage_comparison']))
        egg = report['checked_history']['egg']
        self.assertEqual(egg['counts']['native_steps'], 46)
        self.assertEqual(egg['counts']['lookup_reused'], 1)
        self.assertEqual(egg['counts']['lookup_blocked'], 2)
        self.assertEqual([len(c['historical_proof_refs_sent']) for c in egg['calls']], [0, 1, 1])
        self.assertEqual([c['recheck']['relation'] for c in report['blocked_dependency_rechecks']],
                         ['incomparable', 'incomparable'])
        self.assertEqual(egg['calls'][0]['after_egg']['proof_refs'], egg['calls'][2]['after_egg']['proof_refs'])

    def test_authored_fixture_separate_from_live(self):
        report = audit(self.root/'fixture')
        self.assertEqual(report['mode'], 'fixture')
        self.assertEqual(report['audited_summary']['responses'], 12)
        self.assertEqual(report['audited_summary']['provider_api_calls'], 0)
        self.assertIsNone(report['audited_summary']['provider_usage'])
        self.assertTrue(all(x['responses'] == 4 for x in report['audited_summary']['arms'].values()))

    def test_prompt_cannot_omit_prior_proof(self):
        run = self.root/LIVE
        path = run/'egg/stage-02/attempt-01/request.json'
        def change(data):
            task = json.loads(data['messages'][1]['content'])
            task['previous_stage']['last_assessment']['egg']['proof_refs'] = []
            data['messages'][1]['content'] = json.dumps(task, sort_keys=True, separators=(',', ':'))
        self.mutate(path, change)
        with self.assertRaisesRegex(ValueError, 'serialized request'):
            audit(run)

    def test_stale_proof_cannot_be_claimed_as_reused(self):
        run = self.root/LIVE
        path = run/'egg/stage-02/preflight.json'
        self.mutate(path, lambda d: d['private']['egg']['lookup'].update(status='reused', proved=True))
        with self.assertRaisesRegex(ValueError, 'chronological prefix'):
            audit(run)

    def test_usage_summary_cannot_invent_tokens(self):
        run = self.root/LIVE
        self.mutate(run/'summary.json', lambda d: d['provider_usage'].update(total_tokens=1))
        with self.assertRaisesRegex(ValueError, 'global summary'):
            audit(run)


if __name__ == '__main__':
    unittest.main()
