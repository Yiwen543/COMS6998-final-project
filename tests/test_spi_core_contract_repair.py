import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from spi_core_contract_controls import reference
from prepare_spi_core_repair_review import encode
from prepare_spi_core_checker_review import vector_unpack,apply_delta
from spi_core_interface import validate,action
from summarize_real_parent_screen import transport_violations
from spi_core_independent_modes import hand
from evaluate_spi_core_checker import evaluate
from run_midterm_fixed import sha


class ContractRepairTests(unittest.TestCase):
    def test_schema_rejects_values_that_sv_would_truncate(self):
        for field,value in [('csid',2),('speed',7),('length',1<<20),('clkdiv',1<<16),('lead',16),('tx_be',16),('rst_n',2),('tx_data',-1),('valid',True)]:
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):validate({'actions':[action(**{field:value})]},1)

    def test_evaluator_rejects_silent_event_omission_end_to_end(self):
        # Deliberately defective MOCK checker tests the measurement boundary,
        # not a replacement for Claude's production expected-output logic.
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);cand=p/'candidate';ctrl=p/'controls';cand.mkdir();ctrl.mkdir()
            (cand/'checker.py').write_text("def check_rows(rows):\n    return {'verdict':'pass','failures':[],'assumption_violations':[],'unresolved':[],'events':[],'counts':{}}\n")
            (cand/'selftest.py').write_text('def run(check_rows):\n    return []\n')
            (cand/'authorship.json').write_text(json.dumps({'artifact_sha256':{f:sha(cand/f) for f in ('checker.py','selftest.py')}}))
            (ctrl/'inputs.json').write_text(json.dumps({'triggered':hand(starve=True)}))
            (ctrl/'controls.json').write_text(json.dumps([{'name':'triggered','kind':'independent_positive','required_event_family':'tx_starvation_resume'}]))
            (ctrl/'manifest.json').write_text(json.dumps({f+'_sha256':sha(ctrl/(f+'.json')) for f in ('inputs','controls')}))
            r=evaluate(cand,ctrl,p/'evaluation')
            self.assertEqual(r['cases']['triggered']['verdict'],'pass')
            self.assertEqual(len(r['event_integrity_errors']),1)
            self.assertEqual(r['event_integrity_errors'][0]['required_event_family'],'tx_starvation_resume')
            self.assertFalse(r['B_allowed'])
            (cand/'checker.py').write_text("def check_rows(rows):\n    return {'verdict':'pass','failures':[],'assumption_violations':[],'unresolved':[],'events':[{'family':'tx_starvation_resume','kind':'pass','start_cycle':10,'end_cycle':30}],'counts':{}}\n")
            (cand/'authorship.json').write_text(json.dumps({'artifact_sha256':{f:sha(cand/f) for f in ('checker.py','selftest.py')}}))
            (ctrl/'inputs.json').write_text(json.dumps({'no_stall':hand()}))
            (ctrl/'controls.json').write_text(json.dumps([{'name':'no_stall','kind':'observational_positive','forbidden_event_family':'tx_starvation_resume'}]))
            (ctrl/'manifest.json').write_text(json.dumps({f+'_sha256':sha(ctrl/(f+'.json')) for f in ('inputs','controls')}))
            r=evaluate(cand,ctrl,p/'false-event-evaluation')
            self.assertEqual(len(r['event_integrity_errors']),1)
            self.assertEqual(r['event_integrity_errors'][0]['forbidden_event_family'],'tx_starvation_resume')

    def test_independent_modes_sample_correct_bits_and_idle_not_counted(self):
        for mode in range(4):
            for speed in range(3):
                rs=hand(mode,speed);self.assertFalse(transport_violations(rs))
                pol=mode>>1;phase=mode&1;w=1<<speed;mask=(1<<w)-1
                selected=[r for r in rs if r['pre']['csb']==2 and r['post']['csb']==2 and r['pre']['sck']!=r['post']['sck']]
                sample=[r for r in selected if r['post']['sck']==(pol if phase else 1-pol)]
                val=0
                for r in sample:val=(val<<w)|(r['pre']['sd']&mask)
                self.assertEqual(val,0xa55a3c);self.assertEqual(len(selected),48//w)
                self.assertTrue(all(b['cycle']-a['cycle']>=2 for a,b in zip(selected,selected[1:])))
                idle=[r for r in rs if r['pre']['csb']==3 and r['post']['csb']==3 and r['pre']['sck']!=r['post']['sck']]
                self.assertEqual(len(idle),pol)

    def test_starvation_inputs_and_trailing_resume_are_independent(self):
        rs=hand(starve=True);self.assertFalse(transport_violations(rs))
        stalled=[r for r in rs if r['pre']['tx_stall']]
        self.assertTrue(stalled);self.assertTrue(all(r['pre']['sck']==r['post']['sck']==1 for r in stalled))
        accepted=[r['cycle'] for r in rs if r['action']['tx_valid'] and r['pre']['tx_ready']]
        self.assertEqual(len(accepted),2)
        resume=next(r['cycle'] for r in rs if r['cycle']>accepted[1] and r['pre']['sck']!=r['post']['sck'])
        self.assertGreater(resume,accepted[1]);self.assertEqual(rs[resume]['post']['sck'],0)

    def test_asymmetric_words_and_padding(self):
        p=[0xa5,0x5a,0x3c,0xc3]
        for n in (1,2,3,4):
            for rd in (False,True):
                rs=reference(p[:n],rd);validate({'actions':[r['action'] for r in rs]},392,initial=True)
                self.assertFalse(transport_violations(rs))
                rising=[r for r in rs if r['pre']['sck']==0 and r['post']['sck']==1]
                bits=[(r['action']['sd']>>1)&1 if rd else r['pre']['sd']&1 for r in rising]
                decoded=[sum(bit<<(7-i) for i,bit in enumerate(bits[j:j+8])) for j in range(0,len(bits),8)]
                self.assertEqual(decoded,p[:n])
                expected=sum(b<<(8*i) for i,b in enumerate(p[:n]))
                words=[r['pre']['rx_data'] for r in rs if r['pre']['rx_valid'] and r['action']['rx_ready']]
                self.assertEqual(words,[expected] if rd else [])

    def test_sparse_enabled_lanes_and_bit_order(self):
        rs=reference([0xd4,0xb2],lanes=[0,2]);a=next(r['action'] for r in rs if r['action']['tx_valid'])
        self.assertEqual(a['tx_be'],5);self.assertEqual(a['tx_data'],0x00b200d4)
        with self.assertRaises(ValueError):reference([1,2],lanes=[2,0])

    def test_review_dictionary_and_nested_delta_are_lossless(self):
        a=reference([0xa5],True);b=json.loads(json.dumps(a));b[20]['post']['csb']=0;c=b[:22]
        data={'base':a,'fault':b,'cut':c};meta={'base':{},'fault':{'baseline':'base'},'cut':{'baseline':'fault'}}
        p=encode(data,meta)
        def restore(n):
            if n in p['base_traces']:
                v=p['base_traces'][n];return vector_unpack({**v,'steps':[[r,p['change_dictionary'][i]] for r,i in v['steps']]},p['columns'])
            v=p['derived_traces'][n];return apply_delta(restore(v['base']),v)
        self.assertEqual({n:restore(n) for n in data},data)

if __name__=='__main__':unittest.main()
