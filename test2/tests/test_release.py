import json
from pathlib import Path
import sys
import tempfile
import shutil
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import BASE
from final_score import verify_reference,verify_candidates
from formal_witness import decode

class ReleaseTests(unittest.TestCase):
    def test_reference_hash_binding(self):
        r=verify_reference()
        self.assertEqual(r['independent_control_cases'],24)
        self.assertEqual((r['eligible_pairs_two_state'],r['eligible_pairs_icarus']),(16,15))
    def test_all_candidates_must_freeze(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'final-candidates.json').write_text(json.dumps({'candidates':[]}))
            with self.assertRaises(ValueError):verify_candidates(p)
    def test_modified_final_candidate_rejected(self):
        origin=BASE/'results/mock-v2'
        data=json.loads((origin/'final-candidates.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for i,c in enumerate(data['candidates']):
                target=root/f'candidate{i}';target.mkdir()
                for name in ('candidate.sv','candidate.json'):
                    shutil.copyfile(Path(c['candidate_dir'])/name,target/name)
                c['candidate_dir']=str(target)
            (root/'final-candidates.json').write_text(json.dumps(data))
            verify_candidates(root)
            p=root/'candidate0/candidate.sv';p.write_text(p.read_text()+'\n// changed after freeze\n')
            with self.assertRaises(ValueError):verify_candidates(root)
    def test_mock_final_is_not_model_evidence(self):
        x=json.loads((BASE/'results/mock-final-v1/summary.json').read_text())
        self.assertTrue(x['not_a_model_effectiveness_result'])
        rows=json.loads((BASE/'results/mock-final-v1/scores.json').read_text())
        for r in rows:
            for s,v in r['simulation'].items():
                self.assertEqual(v['distinct_mutants_killed'],[])
                self.assertIsNone(v['distinct_mutant_kills_per_1000_tokens'])
                self.assertEqual(v['eligible_mutant_trace_count'],16 if s=='verilator' else 15)
    def test_vcd_terminal_marker_not_a_real_cycle(self):
        p=BASE/'results/formal-witness-validation-v2/witness-review/trace.vcd'
        rows=decode(p);self.assertEqual(len(rows),2)
        self.assertEqual(rows[-1]['post']['data'],239)
    def test_vcd_partial_port_frame_rejected(self):
        p=BASE/'results/formal-witness-validation-v2/witness-review/trace.vcd'
        with tempfile.TemporaryDirectory() as d:
            q=Path(d)/'truncated.vcd';q.write_text(p.read_text()+'\nb00000000 n35\n')
            with self.assertRaises(ValueError):decode(q)

if __name__=='__main__':unittest.main()
