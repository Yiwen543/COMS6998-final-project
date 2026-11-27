import copy
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from egg_dependency_reuse import FactAuthority, CoreSession, CoreStore, ScopedMemory, includes, targeted_lookup
from egg_regression_facts import prepare
from egg_regression_reuse import ProofStore
from egg_regression_smt import fresh_compare
from collections import Counter


P='m_valid'
Q='(and (ult data_n 8) m_valid)'
R='(and (ult data_n 9) m_valid)'
G4='(eq data_n 4)'
G5='(eq data_n 5)'
G8='(eq data_n 8)'


def ground(evidence,typed):
    return next(n for n,r in evidence['receipts'].items() if r['typed_left']==typed and r['typed_right']=='true')


def step(rule,path,replacement,direction='forward'):
    return {'rule':rule,'direction':direction,'path':path,'replacement':replacement}


class DependencyReuseTests(unittest.TestCase):
    def seed(self,*,ladder=False):
        auth=FactAuthority();store=ProofStore();p=prepare([P,Q,R] if ladder else [P,Q])
        e=auth.discover(p,G4)
        q=ground(e,'(ult data_n 8)')
        qa=next(n for n,t in p['atoms'].items() if t=='(ult data_n 8)')
        proof={'proved':True,'steps':[step(q,[0],'true'),step('and-true-left',[],P)],'used_ground_rules':[q]}
        ident=store.add(Q,P,G4,e,p,proof)
        if ladder:
            r=ground(e,'(ult data_n 9)')
            proof={'proved':True,'steps':[step(r,[0],'true'),step('and-true-left',[],P),
                   step('and-true-left',[],'(and true m_valid)','reverse'),step(q,[0],qa,'reverse')],
                   'used_ground_rules':sorted((q,r))}
            store.add(R,Q,G4,e,p,proof)
        return auth,store,ident

    def test_targeted_cross_guard_and_cache_ablation(self):
        auth,store,ident=self.seed();p=prepare([P,Q]);auth.feasibility(G5)
        blocked=targeted_lookup(store,auth,P,Q,G5,p,False)
        self.assertEqual(blocked['status'],'blocked')
        self.assertEqual(blocked['blocked'][0]['status'],'missing')
        self.assertEqual(auth.counts['dependency_misses'],0)
        ok=targeted_lookup(store,auth,P,Q,G5,p,True)
        self.assertEqual(ok['status'],'revalidated');self.assertEqual(auth.counts['dependency_misses'],1)
        self.assertEqual(ok['edges'][0]['entry_id'],ident);self.assertEqual(ok['edges'][0]['direction'],'reverse')
        self.assertNotEqual(ok['edges'][0]['used_ground_rules'],[d['rule']['name'] for d in store.entries[ident]['dependencies']])
        again=targeted_lookup(store,auth,P,Q,G5,p,False)
        self.assertEqual(again['status'],'revalidated');self.assertEqual(auth.counts['dependency_misses'],1)
        auth.feasibility(G8);bad=targeted_lookup(store,auth,P,Q,G8,p,True)
        self.assertEqual(bad['status'],'blocked');self.assertEqual(bad['blocked'][0]['status'],'sat')
        self.assertFalse(bad['proved']);self.assertEqual(fresh_compare(P,Q,G8)['relation'],'weakened')
        auth.feasibility(G4);back=targeted_lookup(store,auth,P,Q,G4,p,True)
        self.assertEqual(back['status'],'reused');self.assertEqual(auth.counts['dependency_misses'],2)

    def test_intermediate_atom_outside_current_vocabulary_and_blocked_true_goal(self):
        auth,store,_=self.seed(ladder=True);p=prepare([P,R]);auth.feasibility(G5)
        reuse=targeted_lookup(store,auth,P,R,G5,p,True)
        self.assertEqual(reuse['status'],'revalidated');self.assertEqual(len(reuse['edges']),2)
        self.assertGreater(auth.counts['dependency_outside_vocabulary'],0)
        self.assertEqual(auth.counts['dependency_misses'],2)
        auth.feasibility(G8);miss=targeted_lookup(store,auth,P,R,G8,p,True)
        self.assertEqual(miss['status'],'blocked');self.assertFalse(miss['proved'])
        self.assertEqual(fresh_compare(P,R,G8)['relation'],'equivalent')

    def test_no_path_does_not_probe_unrelated_dependencies(self):
        auth,store,_=self.seed();auth.feasibility(G5)
        result=targeted_lookup(store,auth,P,'h_valid',G5,prepare([P,'h_valid']),True)
        self.assertEqual(result['status'],'miss');self.assertEqual(auth.counts['dependency_requests'],0)

    def test_tampered_proof_and_infeasible_guard_rejected(self):
        auth,store,ident=self.seed();p=prepare([P,Q]);auth.feasibility(G5)
        saved=copy.deepcopy(store.entries[ident]);store.entries[ident]['steps'][0]['replacement']='false'
        with self.assertRaisesRegex(ValueError,'content'):
            targeted_lookup(store,auth,P,Q,G5,p,True)
        store.entries[ident]=saved
        g='(ult data_n 0)';self.assertEqual(auth.feasibility(g)['status'],'unsat')
        with self.assertRaisesRegex(ValueError,'feasible'):
            targeted_lookup(store,auth,P,Q,g,p,True)

    def test_ordinary_actual_unsat_core_reauthorization(self):
        auth=FactAuthority();p=prepare([P,Q]);e=auth.discover(p,G4);counts=Counter()
        session=CoreSession(p,e,counts);core=session.compare(P,Q)
        self.assertEqual({v['status'] for v in core.values()},{'unsat'})
        store=CoreStore(counts);ident=store.add({'id':'c1','guard':G4,'left':P,'right':Q},p,e,core)
        self.assertEqual(len(store.entries[ident]['dependencies']),1)
        auth.feasibility(G5);res=targeted_lookup(store,auth,P,Q,G5,p,True,kind='ordinary')
        self.assertEqual(res['status'],'revalidated');self.assertEqual(counts['boolean_core_replay_checks'],1)
        auth.feasibility(G8);bad=targeted_lookup(store,auth,P,Q,G8,p,True,kind='ordinary')
        self.assertEqual(bad['status'],'blocked');self.assertEqual(bad['blocked'][0]['status'],'sat')

    def test_direct_subscope_inclusion(self):
        self.assertTrue(includes('true',G4));self.assertTrue(includes('(ult data_n 8)',G5))
        self.assertFalse(includes(G4,G5));self.assertFalse(includes('(ult data_n 8)','(eq header_n 5)'))
        memory=ScopedMemory(True);case={'id':'known','guard':'(ult data_n 8)','left':P,'right':Q}
        memory.add(case)
        self.assertEqual(memory.lookup({**case,'id':'other','guard':G5},audit=True),['known'])
        self.assertIsNone(memory.lookup({**case,'id':'other','guard':G8},audit=True))


if __name__=='__main__':
    unittest.main()
