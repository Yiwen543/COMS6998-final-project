import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_midterm_fixed import ROOT, sha
from run_spi_core_b_development import assess, messages, raw_page, token_totals
from spi_core_experiment import BASE, group_status, validate_experimental, verify_freeze
from spi_core_interface import action, seed


class ExperimentTests(unittest.TestCase):
    def test_only_qualified_profile_and_exact_seed(self):
        validate_experimental({'actions':seed()+[action()]},392,initial=True)
        for kw in ({'enable':0},{'sw_reset':1},{'valid':1}, {'tx_data':2**32}):
            with self.assertRaises(ValueError):validate_experimental({'actions':[action(**kw)]},64)
        with self.assertRaises(ValueError):validate_experimental({'actions':[action()]*65},64)

    def test_equivalent_locations_still_need_each_counter(self):
        a={'source':'f','line':1,'column':2,'type':'branch','outcome':'then','hierarchy':'tb.dut.a','hits':7}
        b={**a,'line':2,'hits':0}
        targets=[{'eclass':5,'nontrivial':True,'counter_identities':[
            ['f',1,2,'branch','then','.a'],['f',2,2,'branch','then','.a']]}]
        g=group_status([a,b],targets)[0]
        self.assertEqual(g['raw_source_hits'],[7,0]);self.assertFalse(g['all_hit'])

    def test_raw_paging_preserves_each_instance_and_outcome(self):
        p={'source':'scripts/spi_core_interface.py','line':1,'column':1,'type':'branch',
           'outcome':'then','hierarchy':'tb.dut.a','hits':0}
        points=[p,{**p,'hierarchy':'tb.dut.b'},{**p,'outcome':'else'}, {**p,'type':'toggle'}]
        sources=[ROOT/p['source']]
        first=raw_page(points,sources,1,2);second=raw_page(points,sources,2,2)
        self.assertEqual(first['total_uncovered_eligible'],3)
        self.assertEqual(len({tuple(x[:-1]) for x in first['rows']+second['rows']}),3)

    def test_usage_never_adds_reasoning_and_cache_twice(self):
        calls=[{'usage':{'input_tokens':100,'output_tokens':30,'cached_input_tokens':80,'reasoning_output_tokens':20}},
               {'usage':{'input_tokens':None,'output_tokens':None}}]
        self.assertEqual(token_totals(calls),{'input_tokens':100,'output_tokens':30,'unknown_usage_attempts':1})

    def test_no_mock_acceptance_and_no_missing_or_illegal_repetition_dropped(self):
        cfg={'development_budget':{'repetitions':3,'rounds':2},
             'development_acceptance':{'min_repetitions_with_two_groups_unhit_after_round_one':2,
                                       'min_repetitions_with_later_group_progress':2}}
        rows=[{'repetition':p,'status':'simulated','checker':{'verdict':'inconclusive','assumption_violations':[]},
               'groups':[{'all_hit':r==2},{'all_hit':False}]} for p in range(1,4) for r in range(1,3)]
        self.assertTrue(assess(rows,cfg,'live')['pass'])
        self.assertFalse(assess(rows,cfg,'mock')['pass'])
        self.assertFalse(assess(rows[:-1],cfg,'live')['pass'])
        rows[-1]['checker']['assumption_violations']=['dropped valid']
        self.assertFalse(assess(rows,cfg,'live')['pass'])

    def test_prompt_excludes_private_targets_checkers_and_event_hints(self):
        cfg={'development_budget':{'max_new_cycles':64,'rounds':6},
             'feedback_policy':{'maximum_uncovered_rows':128},'targets':'PRIVATE_GOLD_TARGET'}
        folder=BASE/'spi_core_events-v3/seed'
        points=json.loads((folder/'raw-points.json').read_text());trace=json.loads((folder/'trace.json').read_text())
        prior={'checker':{'verdict':'pass','events':[{'family':'PRIVATE_EVENT_HINT'}],
                          'failures':[],'assumption_violations':[],'unresolved':[]}}
        rendered=messages(cfg,[],prior,points,trace,1);text=json.dumps(rendered)
        self.assertNotIn('PRIVATE_GOLD_TARGET',text);self.assertNotIn('PRIVATE_EVENT_HINT',text)
        common=json.loads(rendered[1]['content'])
        self.assertEqual(len(common['raw_uncovered_dut_coverage']['rows']),128)
        self.assertNotIn('checker_source',common);self.assertNotIn('eclass',common)
        self.assertEqual(len(common['common_seed']),8)

    def test_freeze_detects_tampering_before_use(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as d:
            p=Path(d)/'artifact';p.write_text('original')
            f=Path(d)/'freeze.json';f.write_text(json.dumps({'offline_gate_pass':True,
                    'hashes':{str(p.relative_to(ROOT)):sha(p)}}))
            p.write_text('weakened checker')
            with self.assertRaisesRegex(ValueError,'Frozen artifact changed'):verify_freeze(f)


if __name__=='__main__':unittest.main()
