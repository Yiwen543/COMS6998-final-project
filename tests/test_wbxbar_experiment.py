"""Feedback isolation, preserved accounting and fixed scope tests."""
import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from wbxbar_experiment import (BASE, STATIC, action, seed, schema, validate_generated,
    verify_freeze, messages, semantic_relations, group_status, compact_relations, repeated_actions)
from run_wbxbar_bc import schedule
from pilot_model import usage_record
from run_spi_core_b_development import token_totals


class WbxbarExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=json.loads((BASE/'offline-gate-v4/offline-config.json').read_text())
        cls.points=json.loads((STATIC/'inventory/raw-points.json').read_text())
        cls.prior={'checker':{'verdict':'unresolved','failures':[],'assumption_violations':[],
            'unresolved':[{'item':'test_unresolved'}]},'transport':{'cycles':8},'verification_complete':False}

    def test_common_information_is_identical(self):
        b=messages(self.config,'B',[],self.prior,self.points,[],1)
        c=messages(self.config,'C',[],self.prior,self.points,[],1)
        self.assertEqual(b[0],c[0]);body=json.loads(c[1]['content'])
        relations=body.pop('semantic_relations')
        self.assertEqual(json.loads(b[1]['content']),body)
        self.assertEqual(len(relations['groups']),8)
        self.assertNotIn('witness',json.dumps(body).lower())
        self.assertEqual(body['checker']['unresolved']['total'],1)

    def test_all_original_counters_are_separate(self):
        rel=semantic_relations(self.config['targets'])
        wanted={tuple(i) for g in self.config['targets'] for i in g['source_counter_identities']}
        actual={tuple(m['counter']) for g in rel for m in g['members']}
        self.assertEqual(wanted,actual);self.assertEqual(len(actual),17)
        points=copy.deepcopy(self.points)
        for p in points:p['hits']=0
        self.assertFalse(any(g['all_hit'] for g in group_status(points,self.config['targets'])))
        # One member executing does not mark the whole equivalent group executed.
        first=next(iter(wanted))
        from preflight_spi_host import identity
        next(p for p in points if identity(p)==first)['hits']=1
        self.assertFalse(any(g['all_hit'] for g in group_status(points,self.config['targets'])))

    def test_strict_action_validation(self):
        self.assertEqual(validate_generated({'actions':[action()]}),[action()])
        bad=[{'actions':[action(offer=4)]},{'actions':[action(rst=True)]},
             {'actions':[action(rst=1,offer=1)]},{'actions':[action(extra=1)]},
             {'actions':[]},{'actions':[action()]*65},{'actions':[action()],'checker':'disable'}]
        for value in bad:
            with self.subTest(value=str(value)[:80]),self.assertRaises(ValueError):validate_generated(value)
        self.assertEqual(schema()['properties']['actions']['maxItems'],64)

    def test_interleaving_and_equal_limits(self):
        planned=list(schedule(self.config));self.assertEqual(len(planned),36)
        self.assertEqual(planned[:4],[(1,1,'B'),(1,1,'C'),(1,2,'B'),(1,2,'C')])
        self.assertEqual(planned[12:14],[(2,1,'C'),(2,1,'B')])
        for arm in ('B','C'):self.assertEqual(sum(a==arm for _,_,a in planned),18)

    def test_changed_budget_cannot_be_rehashed_into_freeze(self):
        changed=copy.deepcopy(self.config);changed['development_budget']['rounds']=2
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json';p.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError,'Registered setting changed'):verify_freeze(p)

    def test_cached_and_reasoning_not_double_counted(self):
        u=usage_record({'input_tokens':100,'output_tokens':40,'total_tokens':140,
            'input_tokens_details':{'cached_tokens':80},'output_tokens_details':{'reasoning_tokens':30}})
        t=token_totals([{'usage':u}]);self.assertEqual(t['input_tokens']+t['output_tokens'],140)

    def test_compacted_relations_restore_exact_guards(self):
        original=semantic_relations(self.config['targets']);packed=compact_relations(original)
        def restore(v):
            if isinstance(v,str):return re.sub(r'\ba\d+\b',lambda m:packed['atom_ids'][m[0]],v)
            if isinstance(v,list):return [restore(x) for x in v]
            if isinstance(v,dict):return {k:restore(x) for k,x in v.items()}
            return v
        for before,after in zip(original,restore(packed['groups'])):
            self.assertEqual({k:v for k,v in before.items() if k!='typed_atoms'},after)
            for key,atom in before['typed_atoms'].items():
                alias=next(k for k,v in packed['atom_ids'].items() if v==key)
                self.assertEqual(packed['typed_atoms'][alias],atom)

    def test_all_preprocessed_code_and_actions_preserved(self):
        view=self.config['rtl_prompt_view']['sources'];expected={};source=None
        for line in (BASE/'offline-gate-v4/preprocessed.v').read_text().splitlines():
            d=re.fullmatch(r'`line (\d+) "([^"]+)" \d+',line)
            if d:source=d[2];continue
            if line.strip():expected.setdefault(source,[]).append(line.strip())
        actual={k:[s.split(':',1)[1] for s in v.splitlines()] for k,v in view.items()}
        self.assertEqual(expected,actual)
        actions=[action()]*3+[action(offer=1,addr=3)]+[action()]*2
        packed=repeated_actions(actions)
        from wbxbar_experiment import FIELDS
        decoded=[dict(zip(FIELDS,v)) for count,v in packed['rows'] for _ in range(count)]
        self.assertEqual(actions,decoded)
        rendered=messages(self.config,'B',[action()]*320,self.prior,self.points,[],6)
        history=json.loads(rendered[1]['content'])['previous_generated_cycles']
        self.assertEqual(history['omitted_earlier_cycles'],256)
        self.assertEqual(sum(n for n,_ in history['rows']),64)


if __name__=='__main__':unittest.main()
