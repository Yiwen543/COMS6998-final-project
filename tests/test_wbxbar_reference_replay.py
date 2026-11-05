"""Fail closed on preserved-evidence drift without forcing attribution labels."""
import json
from pathlib import Path
import sys
import tempfile
import shutil
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import freeze_wbxbar_reference_replay as role
from audit_wbxbar_reference_replay import correlate
import audit_wbxbar_reference_replay as audit_role


class ReferenceReplayTests(unittest.TestCase):
    def test_replay_audit_rejects_trace_and_counter_tampering(self):
        source = role.ROOT / 'results/wbxbar_reference_replay_20261104/replay-v1'
        records = json.loads((source / 'comparison.json').read_text())
        first = Path(records[0]['session']) / records[0]['batch']
        for artifact in ('trace.json', 'raw-points.json'):
            with self.subTest(artifact=artifact), tempfile.TemporaryDirectory() as folder:
                run = Path(folder) / 'run'
                run.mkdir()
                for name in ('freeze.json', 'comparison.json', 'metadata.json'):
                    shutil.copyfile(source / name, run / name)
                shutil.copytree(source / first, run / first)
                data = json.loads((run / first / artifact).read_text())
                data.pop()
                (run / first / artifact).write_text(json.dumps(data))
                with patch.object(audit_role, 'worker') as worker:
                    with self.assertRaisesRegex(ValueError, 'Public pin mismatch|Raw source counter mismatch'):
                        audit_role.audit(run, Path(folder) / 'audit')
                    worker.assert_not_called()

    def test_registration_rejects_history_drift_and_live_calls(self):
        with tempfile.TemporaryDirectory() as folder:
            evidence, reg = Path(folder) / 'evidence', Path(folder) / 'registration.json'
            evidence.write_text('original')
            r = {'new_model_calls': 0, 'new_live_experiment_allowed': False,
                 'preserved_hashes': {str(evidence): role.sha(evidence)}}
            reg.write_text(json.dumps(r))
            with patch.object(role, 'verify_scope'):
                self.assertEqual(role.verify_registration(reg), r)
                evidence.write_text('changed')
                with self.assertRaisesRegex(ValueError, 'Historical evidence changed'):
                    role.verify_registration(reg)
                r['new_model_calls'] = 1
                reg.write_text(json.dumps(r))
                with self.assertRaisesRegex(ValueError, 'Replay-only'):
                    role.verify_registration(reg)

    def test_old_alarm_is_not_forced_to_match_unknown(self):
        before = {'cycle': 9, 'detail': 'slave 0 routing failure'}
        after = {'unresolved': [], 'failures': []}
        self.assertEqual(correlate(before, after)['status'], 'no_direct_same_cycle_match')
        after['unresolved'] = [{'cycle': 9, 'item': 'post_abort_forward', 'detail': 'slave 0 post-abort'}]
        self.assertEqual(correlate(before, after)['status'], 'unique_post_abort_unknown')
        after['unresolved'] *= 2
        self.assertEqual(correlate(before, after)['status'], 'multiple_post_abort_unknowns')
        after = {'unresolved': [], 'failures': [{'cycle': 9}]}
        self.assertEqual(correlate(before, after)['status'], 'same_cycle_new_failure')


if __name__ == '__main__':
    unittest.main()
