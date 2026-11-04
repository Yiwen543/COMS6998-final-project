import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from i2c_netlist_proof import I2CNetlist,prove
from spi_semantic_v2 import Unsupported
from i2c_fixture import action,validate_actions
from prepare_i2c_compact_review import pack,unpack
from independent_i2c_controls import controls


def bits(value,width):return [str((value>>i)&1) for i in range(width)]


class I2CPipeline(unittest.TestCase):
    def reference_cell(self,kind,a,aw,b,bw,yw,sa=False,sb=False):
        c={'type':kind,'parameters':{'A_SIGNED':str(int(sa)),'B_SIGNED':str(int(sb))},
           'connections':{'A':bits(a,aw),'B':bits(b,bw),'Y':list(range(100,100+yw))},
           'port_directions':{'A':'input','B':'input','Y':'output'}}
        net=I2CNetlist({'ports':{},'cells':{'cell':c},'netnames':{}})
        term,width=net.cell('cell')
        signed=sa and sb
        av=a-(1<<aw) if signed and a&(1<<(aw-1)) else a
        bv=b-(1<<bw) if signed and b&(1<<(bw-1)) else b
        expected=(av+bv)&((1<<yw)-1) if kind=='$add' else int(av>bv)
        q='\n'.join(net.macros.values())+f'\n(assert (not (= {term} (_ bv{expected} {width}))))\n(check-sat)'
        return q

    def test_signed_add_compare_widths(self):
        queries=[]
        for kind in ['$add','$gt']:
            for sa,sb in [(False,False),(True,True),(True,False),(False,True)]:
                for a in [0,3,4,7]:
                    for b in [0,1,2,3]:
                        queries.append('(push)\n'+self.reference_cell(kind,a,3,b,2,5,sa,sb)+'\n(pop)')
        p=subprocess.run(['z3','-in'],input='(set-logic QF_BV)\n'+'\n'.join(queries),text=True,capture_output=True,check=True)
        self.assertEqual(p.stdout.splitlines(),['unsat']*128)

    def test_bmux_each_slice_and_bad_width(self):
        for selector in range(8):
            c={'type':'$bmux','parameters':{'WIDTH':'10','S_WIDTH':'11'},
               'connections':{'A':bits(0x93ac,16),'S':bits(selector,3),'Y':[100,101]},
               'port_directions':{'A':'input','S':'input','Y':'output'}}
            net=I2CNetlist({'ports':{},'cells':{'m':c},'netnames':{}});t,w=net.cell('m')
            expected=(0x93ac>>(selector*2))&3
            p=subprocess.run(['z3','-in'],input='\n'.join(net.macros.values())+f'\n(assert (not (= {t} (_ bv{expected} 2))))\n(check-sat)',text=True,capture_output=True,check=True)
            self.assertEqual(p.stdout.strip(),'unsat')
        c['connections']['A'].pop()
        with self.assertRaises(Unsupported):I2CNetlist({'ports':{},'cells':{'m':c},'netnames':{}}).cell('m')

    def test_bad_netlist_detected(self):
        b=ROOT/'results/i2c_event_candidate_20261104'
        net=json.loads((b/'netlist.json').read_text())
        net['modules']['i2c_controller_fsm']['netnames']['sda_o']['bits']=['0']
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'mutated.json';f.write_text(json.dumps(net))
            result=prove(b/'ast.json',f,Path(d)/'proof')
        self.assertNotEqual(result['status'],'pass')
        self.assertTrue(any(x['z3']=='sat' for x in result['definition_checks']))

    def test_action_boundary(self):
        validate_actions({'actions':[action()]},64,initial=False)
        bad=[{'actions':[action(byte=256)]},{'actions':[action(rst_n=True)]},
             {'actions':[action()] *65},{'actions':[dict(action(),checker='disabled')]},
             {'actions':[action(rst_n=0,push=1)]}]
        for x in bad:
            with self.assertRaises(ValueError):validate_actions(x,64,initial=False)

    def test_semantics_and_counter_identity(self):
        b=ROOT/'results/i2c_event_candidate_20261104'
        s=json.loads((b/'certified-guards.json').read_text())
        self.assertEqual(len(s['different_expression_pairs']),9)
        for pair in s['different_expression_pairs']:
            self.assertTrue(pair['egg_same_class']);self.assertEqual(pair['proof'],'unsat')
            a,c=pair['members']
            for m in [a,c]:self.assertEqual(m['mapping']['status'],'mapped')
            self.assertNotEqual((a['target']['line'],a['target']['column']),(c['target']['line'],c['target']['column']))
        self.assertEqual(s['mapped_targets']+s['unresolved_targets'],268)
        self.assertTrue(all(x['valid'] for x in s['clock_reset']))

    def test_role_isolation_and_unchanged_budget(self):
        base=ROOT/'results/i2c_event_candidate_20261104'
        packet=json.loads((base/'spec-packet/packet.json').read_text())
        text=json.dumps(packet)
        for forbidden in ['state_q','tcount_q','tcount_sel','claude-checker','driver-v1','equivalent_pairs']:
            self.assertNotIn(forbidden,text)
        old=json.loads((ROOT/'configs/spi_host_event_screen.json').read_text())
        new=json.loads((ROOT/'configs/i2c_event_screen.json').read_text())
        self.assertEqual(old['development_budget'],new['development_budget'])

    def test_two_simulator_trace_agreement(self):
        base=ROOT/'results/i2c_event_candidate_20261104'
        for name in ['seed','write','stretch','nak_restart','nak_timeout']:
            self.assertEqual(json.loads((base/f'driver-v2/{name}.trace.json').read_text()),
                             json.loads((base/f'driver-icarus-v2/{name}.trace.json').read_text()))

    def test_lossless_review_packing(self):
        for rows in controls().values():self.assertEqual(unpack(pack(rows)),rows)

    def test_checker_evidence_and_frozen_boundary(self):
        from run_i2c_checked import verify_freeze
        m=verify_freeze();self.assertTrue(m['offline_checker_qualified']);self.assertFalse(m['formal_B_eligible'])
        b=ROOT/'results/i2c_event_candidate_20261104/claude-checker-v3'
        from run_midterm_fixed import sha
        e=json.loads((b/'controls-final/evaluation.json').read_text())
        self.assertEqual(e['checker_sha256'],sha(b/'candidate/checker.py'))
        self.assertTrue(all(x['credited_detection'] for x in e['event_controls']))
        self.assertTrue(e['cases']['premature_timeout_stop']['failures'])
        self.assertTrue(e['cases']['missing_nak_status']['unresolved'])
        self.assertTrue(all(x['pass'] for x in e['author_selftests']))

    def test_stale_evaluation_rejected(self):
        from summarize_i2c_screen import summarize
        base=ROOT/'results/i2c_event_candidate_20261104'
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d);(fake/'controls-final').mkdir();(fake/'candidate').mkdir()
            (fake/'candidate/checker.py').write_text('changed')
            (fake/'controls-final/evaluation.json').write_text('{"checker_sha256":"stale"}')
            (fake/'review.json').write_text('{"ready_for_offline_gate":true}')
            with self.assertRaisesRegex(ValueError,'Stale checker evaluation'):summarize(base,fake)


if __name__=='__main__':unittest.main()
