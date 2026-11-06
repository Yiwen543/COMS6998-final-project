import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import ROOT,sha
from controller_done_data import TASK,REG,SOURCES,datasets,mutations
from controller_done_packet import packet,pack_rows,unpack_rows,NAMES
from controller_done_loop import messages,plumbing,authorization,verify_data,execute,count
from controller_done_runtime import compile_monitor,build_replay,replay,check_rows
from controller_done_score import adjudicate,token_cost,evaluate
from controller_done_formal import harness
from controller_done_witness import remaining
from controller_obligations import fixtures
from controller_release_live import verify_release


class DoneStudyTests(unittest.TestCase):
    def label(self,**kw):return dict(dict(cycles=5,verdict='FAIL',unknown_records=0,first_safety_failure=None,response_completion=False,input_completion=False,end_only=False),**kw)

    def result(self,failures=(),unknown=(),complete=True):
        return dict(complete=complete,properties=[dict(checks=1,failures=list(failures),unknown=list(unknown))])

    def test_frozen_data_and_independent_checker(self):
        self.assertEqual(verify_data()['id'],'controller_done_study_v1')
        s=json.loads((TASK/'measurements-v1/summary.json').read_text())
        self.assertEqual(s['status'],'qualified');self.assertEqual(s['physical_simulation_attempts'],162)
        self.assertTrue(all(s['dual_correct_agreement'].values()));self.assertEqual(s['new_model_trials'],0)
        self.assertEqual({r['verdict'] for r in s['records'] if r['source']=='correct'},{'PASS'})
        self.assertEqual({r['verdict'] for r in s['records'] if r['source']=='N10'},{'PASS'})

    def test_seeded_inputs_and_mutations_match_registration(self):
        import hashlib
        reg=json.loads(REG.read_text());dev,final=datasets()
        self.assertEqual((len(dev),len(final)),(3,6));self.assertEqual(datasets(),(dev,final))
        for split,values in [('development',dev),('final',final)]:
            for n,a in values.items():self.assertEqual(hashlib.sha256(json.dumps(a,sort_keys=True,separators=(',',':')).encode()).hexdigest(),reg['input_geometry_sha256'][split][n])
        for m,r in zip(mutations(SOURCES[0].read_text()),reg['fault_catalogue']):
            self.assertEqual(hashlib.sha256(m['text'].encode()).hexdigest(),r['mutant_sha256'])

    def test_lossless_counter_and_rows_common_packet_and_prompt_isolation(self):
        b,c=packet('B2_raw'),packet('C2_semantic');self.assertEqual(c.pop('egraph_feedback')['groups'].__len__(),4);self.assertEqual(b,c)
        for n in NAMES:
            rows=json.loads((TASK/'measurements-v1/correct/verilator'/n/'rows.json').read_text());self.assertEqual(unpack_rows(pack_rows(rows)),rows)
        msg=json.dumps(messages('C2_semantic',1))
        for forbidden in ('reference/frozen','private/','probe_01','N01.v','AGENTS.md','check_rows','expected_verdict'):
            self.assertNotIn(forbidden,msg)
        from controller_packet_compact import unpack
        self.assertEqual(unpack(b['raw_coverage'])['counter_count'],3168)

    def test_marker_once_finalpost_no_edge_and_projection_absent(self):
        c=plumbing(3);c['body']='assign active={6{trace_done}};assign ok=0;';rows=fixtures()['legal_exact']['rows']
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);d=root/'candidate';self.assertEqual(compile_monitor(c,d)['status'],'complete');self.assertEqual(build_replay(d)['status'],'complete')
            r=replay(d,rows,root/'end',root/'cache');p=replay(d,rows,root/'projection',root/'cache',trace_done=False)
            self.assertEqual(r['cycles'],len(rows));self.assertEqual(r['samples'],2*len(rows)-1)
            for s in r['properties']:self.assertEqual(s['failures'],[[len(rows)-1,'post']]);self.assertEqual(s['end_sample_checks'],1)
            self.assertTrue(all(x['vacuous_on_trace'] for x in p['properties']));self.assertEqual(p['cycles'],len(rows))

    def test_marker_drive_and_malformed_input_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            c=plumbing(3);c['body']="assign trace_done=1'b1;assign active=63;assign ok=63;"
            self.assertNotEqual(compile_monitor(c,Path(t)/'candidate')['status'],'complete')
        rows=copy.deepcopy(fixtures()['legal_exact']['rows']);rows[0]['inputs']['s_data']=256
        with self.assertRaises(ValueError):check_rows(rows)

    def test_completion_needs_final_post_and_no_earlier_alarm(self):
        l=self.label(response_completion=True,end_only=True)
        self.assertTrue(adjudicate(l,self.result([(4,'post')]))['fully_resolved_detection']['response_completion'])
        for failure in ([(4,'pre')],[(3,'post'),(4,'post')]):self.assertFalse(adjudicate(l,self.result(failure))['definite_detection']['response_completion'])

    def test_safety_onset_and_unknown_not_erased(self):
        l=self.label(first_safety_failure=dict(cycle=2,phase='post'))
        self.assertTrue(adjudicate(l,self.result([(2,'post')]))['definite_detection']['safety'])
        self.assertFalse(adjudicate(l,self.result([(2,'pre'),(3,'post')]))['definite_detection']['safety'])
        r=adjudicate(self.label(input_completion=True,unknown_records=1),self.result([(4,'post')]))
        self.assertTrue(r['definite_detection']['input_completion']);self.assertFalse(r['fully_resolved_detection']['input_completion']);self.assertEqual(r['oracle_unknown_records'],1)
        self.assertFalse(adjudicate(l,self.result([(2,'post')],complete=False))['definite_detection']['safety'])
        self.assertTrue(adjudicate(self.label(verdict='PASS'),self.result([(4,'post')]))['physical_reference_PASS_alarm'])

    def test_missing_usage_not_zero_and_retry_costs_retained(self):
        a=dict(generation_request_issued=True,count_request_issued=True,usage=dict(input_tokens=10,output_tokens=2))
        self.assertEqual(token_cost([a,a])['actual_total_tokens'],24)
        self.assertIsNone(token_cost([a,dict(generation_request_issued=True)])['actual_total_tokens'])
        self.assertIsNone(token_cost([])['actual_total_tokens'])

    def test_live_and_count_closed_before_key_or_model(self):
        for scope in ('token_count','generation'):
            with self.assertRaises(ValueError):authorization(scope)
        with tempfile.TemporaryDirectory() as t,patch('controller_done_loop.model',side_effect=AssertionError('must not access key')):
            with self.assertRaises(ValueError):execute('live',Path(t)/'live')

    def test_hidden_grading_requires_full_release_first(self):
        with tempfile.TemporaryDirectory() as t,patch('controller_done_score.verify_data',side_effect=AssertionError('private access')):
            with self.assertRaises(FileNotFoundError):evaluate(Path(t)/'missing',Path(t)/'out')

    def test_count_stage_keeps_failure_and_issues_only_four_fake_requests(self):
        from unittest.mock import Mock
        client=Mock();client.count_input_tokens.side_effect=[12000,18000,RuntimeError('fake count failure'),20000]
        with tempfile.TemporaryDirectory() as t,patch('controller_done_loop.authorization'),patch('controller_done_loop.model',return_value=client):
            count(Path(t)/'counts');r=json.loads((Path(t)/'counts/summary.json').read_text())
        self.assertEqual(client.count_input_tokens.call_count,4);self.assertEqual(r['count_requests'],4);self.assertEqual(r['generation_requests'],0)
        self.assertEqual(r['counts'][2]['status'],'count_unresolved');self.assertFalse(r['counts'][2]['within_cap'])

    def test_formal_projection_only_and_retention_logic_same(self):
        retained=harness(0,'retained');cone=harness(0)
        self.assertEqual(retained.replace('(* keep *) wire','wire'),cone)
        self.assertIn("wire trace_done=1'b0",cone);self.assertIn('assume(frame_bytes<11 || s_last)',cone)

    def test_physical_witness_tools_share_the_remaining_total_budget(self):
        with patch('controller_done_witness.time.monotonic',return_value=100):
            self.assertEqual(remaining(None,60),60)
            self.assertEqual(remaining(102,60),2)
            with self.assertRaises(TimeoutError):remaining(99,60)


if __name__=='__main__':unittest.main()
