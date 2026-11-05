import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from spi_core_checker_controls import reference
from spi_core_interface import FIELDS,OUTPUTS,validate
from summarize_real_parent_screen import transport_violations
from prepare_i2c_compact_review import pack,unpack
from evaluate_spi_core_checker import clean,scoped_pass,successful_events
from prepare_spi_core_checker_review import vector_pack,vector_unpack,delta,apply_delta
from probe_spi_core_checker_followup import cases as followup_cases

class CheckerControlTests(unittest.TestCase):
    def test_reference_clock_and_command_counts(self):
        for payload in ([0xa1],[0xa1,0x3c],[0xa5,0x5a,0xf0]):
            for read in (False,True):
                rows=reference(payload,read);validate({'actions':[r['action'] for r in rows]},392,initial=True)
                self.assertFalse(transport_violations(rows))
                self.assertEqual(sum(r['action']['valid'] and r['pre']['ready'] for r in rows),1)
                rising=[r for r in rows if r['pre']['sck']==0 and r['post']['sck']==1]
                self.assertEqual(len(rising),len(payload)*8)
                self.assertTrue(all(r['post']['csb']==2 for r in rising))
                self.assertEqual(rows[-1]['post']['csb'],3)

    def test_transmitted_and_received_byte_order_from_spec(self):
        payload=[0xa5,0x5a,0xf0]
        for read in (False,True):
            rows=reference(payload,read);edges=[r for r in rows if r['pre']['sck']==0 and r['post']['sck']==1]
            bits=[(r['action']['sd']>>1)&1 if read else r['post']['sd']&1 for r in edges]
            decoded=[sum(b<<(7-i) for i,b in enumerate(bits[j:j+8])) for j in range(0,len(bits),8)]
            self.assertEqual(decoded,payload)
            received=[r['pre']['rx_data'] for r in rows if r['pre']['rx_valid'] and r['action']['rx_ready']]
            self.assertEqual(received,[0xa55af000] if read else [])

    def test_reference_trace_schema_and_lossless_review_encoding(self):
        rows=reference([0xa5],True)
        for i,r in enumerate(rows):
            self.assertEqual(r['cycle'],i);self.assertEqual(set(r['action']),set(FIELDS))
            for side in ('pre','post'):self.assertEqual(set(r[side]),set(OUTPUTS))
        self.assertEqual(unpack(pack(rows)),rows)

    def test_pending_unresolved_and_infrastructure_never_scoped_pass(self):
        good={'verdict':'scoped_pass','failures':[],'assumption_violations':[],'unresolved':[]}
        self.assertTrue(scoped_pass(good))
        self.assertTrue(scoped_pass({**good,'verdict':'pass'}))
        for update in ({'verdict':'pending'},{'verdict':'unresolved'},{'unresolved':['timing']},{'infrastructure_error':'exception'},{'assumption_violations':[{'cycle':1}]},{'failures':[{'cycle':1}]}):
            self.assertFalse(scoped_pass({**good,**update}))

    def test_pending_event_is_not_success(self):
        pending={'family':'rx_backpressure_resume','kind':'pending','start_cycle':10,'end_cycle':None}
        self.assertEqual(successful_events({'events':[pending]}),[])
        self.assertEqual(successful_events({'events':[{**pending,'kind':'pass','end_cycle':30}]}),[{**pending,'kind':'pass','end_cycle':30}])

    def test_vector_and_mutation_review_roundtrip(self):
        rows=reference([0xa5,0x5a],True);columns=[(k,n) for k in ('action','pre','post') for n in rows[0][k]]
        self.assertEqual(vector_unpack(vector_pack(rows,columns),columns),rows)
        changed=copy.deepcopy(rows[:20]);changed[12]['post']['sd']^=1
        self.assertEqual(apply_delta(rows,delta(rows,changed)),changed)

    def test_followup_keeps_seed_budget_and_resimulates_only_one_input_fault(self):
        cases=followup_cases()
        for aa in cases.values():validate({'actions':aa},392,initial=True)
        base,bad=cases['uniform_write_baseline'],cases['withdraw_pending_command']
        self.assertEqual([i for i,(a,b) in enumerate(zip(base,bad)) if a!=b],[28])
        self.assertEqual(bad[28]['valid'],1);self.assertEqual(bad[29]['valid'],0)
        self.assertEqual([i for i,a in enumerate(cases['hardware_abort_restart']) if not a['rst_n']],[0,1,48,49])

if __name__=='__main__':unittest.main()
