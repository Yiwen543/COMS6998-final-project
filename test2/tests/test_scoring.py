import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from score import score

def result(failures=None,unknown=None):
    return {'complete':True,'properties':[{'checks':8,'failures':failures or [],'unknown':unknown or []}]+[
        {'checks':0,'failures':[],'unknown':[]} for _ in range(5)]}

class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.e=[{'mutant':'m','trace':'x','eligible':True,'first_reference_failure':{'cycle':2,'phase':'post'}},
                {'mutant':'untriggered','trace':'x','eligible':False,'first_reference_failure':None}]
    def test_false_positive_disqualifies_kills(self):
        r=score([result([[0,'post']])],{('m','x'):result([[3,'post']])},self.e,1000)
        self.assertEqual(r['distinct_mutants_killed'],[])
        self.assertTrue(r['details'][0]['raw_post_violation_alarm'])
    def test_earlier_alarm_not_credited(self):
        r=score([result()],{('m','x'):result([[1,'post']])},self.e,1000)
        self.assertEqual(r['valid_mutant_trace_kills'],0)
    def test_eligibility_unknown_and_roi(self):
        r=score([result()],{('m','x'):result([[2,'post']],[[5,'post']])},self.e,2000)
        self.assertEqual(r['distinct_mutants_killed'],['m'])
        self.assertEqual(r['eligible_mutant_trace_count'],1)
        self.assertEqual(r['distinct_mutant_kills_per_1000_tokens'],.5)
        self.assertTrue(r['details'][0]['unresolved'])
    def test_unknown_correct_is_not_sound(self):
        r=score([result(unknown=[[1,'pre']])],{('m','x'):result([[2,'post']])},self.e,1000)
        self.assertFalse(r['suite_sound_on_fixed_controls']);self.assertEqual(r['valid_mutant_trace_kills'],0)

if __name__=='__main__':unittest.main()
