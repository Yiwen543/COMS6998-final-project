"""Independent proof-store checks, including conditional fact withdrawal and reauthorization."""
from copy import deepcopy
from importlib.util import find_spec
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
if find_spec('z3'):
    from egg_regression_facts import certify, prepare, verify
    from egg_regression_reuse import ProofStore, verify_reuse, _digest


def step(name, replacement, path=(), direction='forward'):
    return {'rule': name, 'path': list(path), 'direction': direction, 'replacement': replacement}


def proof(*steps, ground=()):
    return {'proved': True, 'status': 'checked_derivation', 'used_ground_rules': sorted(ground),
            'stop': 'Some(Saturated)', 'steps': list(steps)}


@unittest.skipUnless(find_spec('z3'), 'requires z3')
class RegressionProofReuseTests(unittest.TestCase):
    def evidence(self, sources, guard='true'):
        prepared = prepare(sources)
        evidence = certify(prepared, guard)
        self.assertTrue(verify(prepared, guard, evidence))
        return prepared, evidence

    def test_transitive_reuse_and_reversed_erasure(self):
        a, b, c = '(and (not (not m_valid)) m_ready)', '(and m_valid m_ready)', '(and m_ready m_valid)'
        p, e = self.evidence([a,b,c])
        store = ProofStore()
        first = store.add(a,b,'true',e,p,proof(step('double-not','m_valid',(0,))))
        second = store.add(b,c,'true',e,p,proof(step('and-commute','(and m_ready m_valid)')))
        # The intermediate b need not occur among the new targets.
        small, es = self.evidence([a,c])
        result = store.lookup(c,a,'true',es,small)
        self.assertTrue(result['proved'])
        self.assertEqual(result['status'],'reused')
        self.assertEqual([x['entry_id'] for x in result['edges']], [second,first])
        self.assertEqual([x['direction'] for x in result['edges']], ['reverse','reverse'])
        self.assertEqual(result['edges'][1]['steps'][0]['replacement'], '(not (not m_valid))')
        self.assertTrue(verify_reuse(c,a,'true',es,small,result,store.entries,verify_current_facts=True))
        altered=deepcopy(result); altered['edges'][1]['steps'][0]['replacement']='h_valid'
        with self.assertRaisesRegex(ValueError,'path edge differs'):
            verify_reuse(c,a,'true',es,small,altered,store.entries)

    def test_real_boundary_dependency_cannot_cross_to_different_guard(self):
        a,b = '(and m_valid (eq data_index 4))','(and m_valid (eq data_index data_n))'
        g4,g5='(eq data_n 4)','(eq data_n 5)'
        p,e=self.evidence([a,b],g4)
        row=next(r for r in e['facts'] if r['right'].startswith('bv_'))
        src,dst=(p['abstracts'][0].split()[-1][:-1],p['abstracts'][1].split()[-1][:-1])
        direction='forward' if (row['left'],row['right'])==(src,dst) else 'reverse'
        store=ProofStore()
        entry_id=store.add(a,b,g4,e,p,proof(step(row['name'],dst,(1,),direction),ground=[row['name']]))
        result=store.lookup(a,b,g4,e,p)
        self.assertEqual(result['status'],'reused')
        other, changed=self.evidence([a,b],g5)
        result=store.lookup(a,b,g5,changed,other)
        self.assertEqual(result['status'],'blocked')
        self.assertFalse(result['proved'])
        self.assertEqual(result['reasons'][0]['entry_id'],entry_id)
        with self.assertRaisesRegex(ValueError,'different guard'):
            store.lookup(a,b,g5,e,p)

    def test_reauthorization_new_context_needs_current_receipt(self):
        a,b='(and m_valid (ult data_n 8))','m_valid'
        g4,g5='(eq data_n 4)','(eq data_n 5)'
        p,e=self.evidence([a,b],g4)
        old=next(r for r in e['facts'] if r['right']=='true')
        store=ProofStore()
        entry_id=store.add(a,b,g4,e,p,proof(step(old['name'],'true',(1,)),step('and-true-right','m_valid'),ground=[old['name']]))
        p2,e2=self.evidence([a,b],g5)
        new=next(r for r in e2['facts'] if r['right']=='true')
        self.assertNotEqual(old['name'],new['name'])
        result=store.lookup(a,b,g5,e2,p2)
        self.assertEqual(result['status'],'revalidated')
        self.assertEqual(result['edges'][0]['entry_id'],entry_id)
        self.assertEqual(result['used_ground_rules'],[new['name']])
        self.assertTrue(verify_reuse(a,b,g5,e2,p2,result,store.entries,verify_current_facts=True))
        tampered=deepcopy(e2); tampered['receipts'][new['name']]['typed_left']='(ult data_n 5)'
        with self.assertRaisesRegex(ValueError,'detached'):
            store.lookup(a,b,g5,tampered,p2)
        corrupt=deepcopy(store.entries)
        corrupt[entry_id]['steps'][-1]['replacement']='m_ready'
        with self.assertRaisesRegex(ValueError,'content'):
            verify_reuse(a,b,g5,e2,p2,result,corrupt)

    def test_hash_recomputation_does_not_authorize_wrong_rule(self):
        a,b='(and true m_valid)','m_valid'
        p,e=self.evidence([a,b])
        store=ProofStore()
        prior=store.add(a,b,'true',e,p,proof(step('and-true-left','m_valid')))
        corrupt=deepcopy(store.entries[prior]); corrupt['steps'][0]['replacement']='h_valid'
        corrupt['atoms']['h_valid']='h_valid'
        digest='proof-'+_digest(corrupt)
        store.entries={digest:corrupt}
        with self.assertRaisesRegex(ValueError,'substitution'):
            store.lookup(a,b,'true',e,p)

    def test_identity_miss_and_no_proof_are_not_negative_theorems(self):
        p,e=self.evidence(['m_valid','m_ready'])
        store=ProofStore()
        result=store.lookup('m_valid','m_ready','true',e,p)
        self.assertEqual((result['proved'],result['status']),(False,'miss'))
        self.assertTrue(verify_reuse('m_valid','m_ready','true',e,p,result,store.entries))
        identity=store.lookup('m_valid','m_valid','true',e,p)
        self.assertEqual((identity['proved'],identity['status']),(True,'identity'))
        with self.assertRaisesRegex(ValueError,'false identity'):
            verify_reuse('m_valid','m_ready','true',e,p,identity,store.entries)
        self.assertIsNone(store.add('m_valid','m_ready','true',e,p,{'proved':False}))


if __name__=='__main__':
    unittest.main()
