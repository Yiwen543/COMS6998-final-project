import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from runner import live_gate,develop,mock_candidate,BASE

class RunnerTests(unittest.TestCase):
    def test_live_missing_freeze_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(RuntimeError):live_gate(Path(d)/'missing.json')
    def test_unbound_live_gate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'freeze.json';p.write_text(json.dumps({'status':'reviewed_reference_and_runner_ready','gates':{},'files':{}}))
            with self.assertRaises(ValueError):live_gate(p)
    def test_invalid_candidate_is_feedback_not_crash(self):
        with tempfile.TemporaryDirectory() as d:
            c=mock_candidate(1);c['body']='$finish;'
            feedback,cost=develop(c,BASE/'results/preflight-v2',Path(d))
            self.assertEqual(feedback['status'],'invalid_candidate')
            self.assertEqual(cost['compile_attempts'],0);self.assertEqual(cost['monitor_replays'],0)

if __name__=='__main__':unittest.main()
