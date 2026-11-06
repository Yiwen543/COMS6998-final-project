import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from controller_done_adjudication_v3 import adjudicate
from controller_done_score_v3 import adjudicate as wired
from common import BASE,sha
from controller_done_data import TASK


class ScoringV3Tests(unittest.TestCase):
    def label(self,**kw):return {**dict(cycles=5,verdict='FAIL',unknown_records=0,first_safety_failure=None,response_completion=False,input_completion=False,end_only=False),**kw}
    def result(self,failures,unknown=()):return dict(complete=True,properties=[dict(checks=1,failures=list(failures),unknown=list(unknown))])

    def test_real_replay_grader_wires_new_rules(self):self.assertIs(wired,adjudicate)

    def test_marker_only_alarm_cannot_earn_ordinary_safety_credit(self):
        label=self.label(first_safety_failure=dict(cycle=2,phase='post'))
        r=adjudicate(label,self.result([(4,'post')]))
        self.assertFalse(r['definite_detection']['safety']);self.assertTrue(r['marker_only_safety_signal'])
        r=adjudicate(label,self.result([(3,'pre'),(4,'post')]))
        self.assertTrue(r['definite_detection']['safety']);self.assertFalse(r['marker_only_safety_signal'])

    def test_safety_violation_first_at_final_marker_stays_in_denominator(self):
        r=adjudicate(self.label(first_safety_failure=dict(cycle=4,phase='post')),self.result([(4,'post')]))
        self.assertTrue(r['eligible']['safety']);self.assertFalse(r['definite_detection']['safety']);self.assertTrue(r['marker_safety_signal'])

    def test_early_alarm_blocks_both_finite_credits(self):
        label=self.label(end_only=True,response_completion=True,input_completion=True)
        for category in ('response_completion','input_completion'):
            r=adjudicate(label,self.result([(3,'post'),(4,'post')]))
            self.assertFalse(r['definite_detection'][category]);self.assertEqual(r['early_finite_alarm_samples'],1)
            r=adjudicate(label,self.result([(4,'post')]))
            self.assertTrue(r['definite_detection'][category]);self.assertIn('UNATTRIBUTED',r['category_attribution'])

    def test_unknown_context_keeps_definite_and_resolved_separate(self):
        r=adjudicate(self.label(input_completion=True,unknown_records=1),self.result([(4,'post')]))
        self.assertTrue(r['definite_detection']['input_completion']);self.assertFalse(r['fully_resolved_detection']['input_completion'])
        r=adjudicate(self.label(response_completion=True,end_only=True),self.result([(4,'post')],[(1,'post')]))
        self.assertFalse(r['fully_resolved_detection']['response_completion'])

    def test_candidate_prompt_hashes_still_match_actual_successful_counts(self):
        from controller_done_loop_v2 import count_messages
        from common import dump
        import tempfile
        records=json.loads((BASE/'results/controller-done-preflight-v2/counts/summary.json').read_text())['counts']
        with tempfile.TemporaryDirectory() as t:
            for arm,kind,msg in count_messages():
                p=Path(t)/'prompt.json';dump(p,msg);r=next(r for r in records if (r['arm'],r['kind'])==(arm,kind));self.assertEqual(sha(p),r['prompt_sha256']);self.assertTrue(r['within_cap'])


if __name__=='__main__':unittest.main()
