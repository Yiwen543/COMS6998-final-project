"""Repair boundary, independent controls and lossless review transport regressions."""
import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from prepare_wbxbar_cancel_contract import BASE,PRIOR,verify_packet,verify_registration
from wbxbar_multi_abort_controls import additions
from wbxbar_cancel_validation import expected_outcome
from replay_wbxbar_cancel import approval_ready,verify_replay_freeze
from prepare_spi_core_checker_review import vector_unpack,apply_delta


class CancelBoundaryTests(unittest.TestCase):
    def test_original_evidence_and_fixed_budget(self):
        r=verify_registration()
        self.assertEqual(r['new_stimulus_generation_calls'],0)
        self.assertEqual(r['replay']['batches'],42)
        self.assertEqual(r['replay']['original_physical_cycles'],8360)

    def test_controls_reproducible_and_holdback(self):
        rows,records=additions();stored=json.loads((BASE/'controls-v1/private-inputs.json').read_text())
        self.assertEqual(len(records),23)
        self.assertEqual({n:stored[n] for n in rows},rows)
        self.assertEqual(sum(x['author_example'] for x in records),6)
        packet=json.loads((BASE/'spec-packet-v1/packet.json').read_text())
        self.assertEqual({x['name'] for x in packet['synthetic_scenarios']},{x['name'] for x in records if x['author_example']})
        self.assertEqual(set(packet),{'role','specification','candidate','synthetic_scenarios','isolation'})

    def test_old_checker_limit_exposed_without_old_regressions(self):
        data=json.loads((BASE/'baseline-controls-v1/summary.json').read_text())
        self.assertFalse(data['pass'])
        self.assertTrue(all(x['pass'] for x in data['accounts'] if not x['new']))
        self.assertEqual(sum(not x['pass'] for x in data['accounts']),11)
        failed=[x for x in data['accounts'] if not x['pass']]
        self.assertTrue(all(x['expected']=='unresolved' for x in failed))
        self.assertEqual(sum(x['actual']=='dut_violation' for x in failed),10)
        self.assertEqual([x['name'] for x in failed if x['actual']=='scoped_pass'],['multi_abort/live_aborted_same_identity'])

    def test_review_has_all_original_pin_values(self):
        body=json.loads((BASE/'review-size-preflight-v1/packet.json').read_text());trace=body['traces'];decoded={}
        source=json.loads((BASE/'controls-v1/private-inputs.json').read_text())
        for name,item in trace['values'].items():
            rows=vector_unpack(item['vector'],trace['columns']) if 'vector' in item else apply_delta(decoded[item['base']],item['delta'])
            decoded[name]=rows
            self.assertEqual([{k:v for k,v in r.items() if k!='action'} for r in rows],source[name])
        self.assertEqual(set(decoded),set(source))

    def test_author_packet_tamper_is_rejected(self):
        verify_packet(BASE/'spec-packet-v1',PRIOR)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'packet';shutil.copytree(BASE/'spec-packet-v1',p)
            with (p/'prompt.txt').open('a') as stream:stream.write(' altered')
            with self.assertRaisesRegex(ValueError,'Packet drift'):verify_packet(p,PRIOR)

    def test_truthy_or_failed_review_cannot_freeze(self):
        valid={'pass':True,'accounts':[{'pass':True}]}
        for bad in ('true',1,None,False):
            with self.assertRaises(ValueError):approval_ready(valid,{'ready_for_offline_gate':bad})
        with self.assertRaises(ValueError):approval_ready({'pass':False,'accounts':[{'pass':True}]},{'ready_for_offline_gate':True})
        with self.assertRaises(ValueError):approval_ready({'pass':True,'accounts':[]},{'ready_for_offline_gate':True})

    def test_blanket_uncertainty_does_not_pass_gate(self):
        uncertain={'verdict':'unresolved','unresolved':['unknown'],'failures':[],'assumption_violations':[]}
        self.assertFalse(expected_outcome(uncertain,'scoped_pass'))
        self.assertFalse(expected_outcome(uncertain,'dut_violation'))
        false_failure={'verdict':'dut_violation','failures':['alarm'],'assumption_violations':['illegal input']}
        self.assertFalse(expected_outcome(false_failure,'dut_violation'))
        false_pass={'verdict':'scoped_pass','failures':[],'unresolved':['unsupported'],'assumption_violations':[]}
        self.assertFalse(expected_outcome(false_pass,'scoped_pass'))

    def test_unreviewed_old_freeze_cannot_start_replay(self):
        with self.assertRaisesRegex(ValueError,'Replay-only freeze required'):
            verify_replay_freeze(BASE.parents[1]/'configs/wbxbar_exploratory_bc_freeze_v1.json')


if __name__=='__main__':unittest.main()
