import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from controller_obligations import fixtures
from controller_monitor_live import TASK
from controller_reference_evaluate import module
from controller_formal_diagnostic import harness
from controller_physical_witness import decode
import controller_monitor_done as done
from controller_loop_live import plumbing
from controller_monitor_live import ROW_INPUTS,PINS


class QualificationTests(unittest.TestCase):
    def vcd(self,states=11,omit=None,truncate=False,unknown=False):
        header=['$var integer 32 t smt_step $end','$scope module formal_top $end']
        for i,name in enumerate(ROW_INPUTS):
            if name!=omit:header.append(f'$var wire {PINS[name]} i{i} {name} $end')
        header+=['$var wire 6 a active $end','$var wire 6 o ok $end','$upscope $end','$enddefinitions $end']
        for step in range(states):
            header += [f'#{step*10}',f'b{step:b} t']
            for i,name in enumerate(ROW_INPUTS):
                if name==omit:continue
                header.append(f'b{int(step==0 and name=="rst"):b} i{i}')
            header += ['bxxxxxx a' if unknown else 'b111111 a','b000000 o' if step==9 else 'b111111 o']
        header += [f'#{states*10}',f'b{states:b} t']
        if truncate:header.append('b0 i0')
        return '\n'.join(header)+'\n'

    def test_finite_controls_match_independent_reference_without_an_oracle_patch(self):
        checker=module(TASK/'reference/frozen-v2/checker.py','frozen_reference_test')
        for name,c in fixtures().items():
            with self.subTest(case=name):
                r=checker.check_rows(c['rows'],require_drained=c['require_drained'],min_tail=c['min_tail'])
                self.assertEqual(r['verdict'],c['expected_verdict'])

    def test_completion_is_distinct_from_sampled_safety(self):
        checker=module(TASK/'reference/frozen-v2/checker.py','frozen_reference_completion_test')
        for name in ('missing_data_response','missing_status_response','missing_both_response','input_never_accepted'):
            c=fixtures()[name];r=checker.check_rows(c['rows'],require_drained=True,min_tail=128)
            self.assertEqual(r['verdict'],'FAIL')
            self.assertTrue(r['failures']);self.assertTrue(all(x['phase']=='end' for x in r['failures']))
        for c in fixtures().values():
            self.assertFalse(c['physically_reached'])

    def test_tail_and_unknown_are_never_counted_as_pass(self):
        checker=module(TASK/'reference/frozen-v2/checker.py','frozen_reference_unknown_test')
        for name in ('final_tail_32_not_128','unknown_payload','unknown_status'):
            c=fixtures()[name]
            self.assertEqual(checker.check_rows(c['rows'],require_drained=True,min_tail=128)['verdict'],'UNRESOLVED')

    def test_output_retention_variant_preserves_all_formal_logic(self):
        retained=harness(0,'retained');cone=harness(0,'cone')
        self.assertEqual(retained.replace('(* keep *) wire','wire'),cone)
        self.assertEqual(cone.count('(* anyseq, keep *)'),2)
        self.assertIn('assume(frame_bytes<11 || s_last)',cone)

    def test_native_assert_reporting_delay_does_not_shift_replay_alarm(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'trace.vcd';p.write_text(self.vcd());inputs,sampled,alarm=decode(p,4)
        self.assertEqual(alarm,9)
        self.assertEqual(len(inputs),11)
        self.assertLess(alarm,len(inputs)-1)
        self.assertEqual(sampled,[{}]*11)

    def test_missing_truncated_or_unknown_witness_never_gets_invented_inputs(self):
        for options in [dict(omit='h_ready'),dict(truncate=True),dict(unknown=True)]:
            with self.subTest(options=options),tempfile.TemporaryDirectory() as temp:
                p=Path(temp)/'trace.vcd';p.write_text(self.vcd(**options))
                with self.assertRaises(ValueError):decode(p,4)

    def test_end_marker_is_visible_once_at_final_post_with_no_extra_edge(self):
        c=plumbing(3);c['body']="assign active={6{trace_done}};assign ok=0;"
        rows=fixtures()['legal_exact']['rows']
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);d=root/'monitor'
            self.assertEqual(done.compile_monitor(c,d)['status'],'complete')
            self.assertEqual(done.build_replay(d)['status'],'complete')
            r=done.replay(d,rows,root/'replay',root/'cache')
            self.assertTrue(r['complete']);self.assertEqual(r['cycles'],len(rows))
            for p in r['properties']:
                self.assertEqual(p['checks'],1);self.assertEqual(p['failures'],[[len(rows)-1,'post']]);self.assertFalse(p['unknown'])

    def test_end_marker_exposes_blocked_final_offer_without_a_new_oracle(self):
        c=plumbing(3);c['body']="assign active={6{trace_done}};assign ok={6{!s_valid}};"
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);d=root/'monitor';self.assertEqual(done.compile_monitor(c,d)['status'],'complete');done.build_replay(d)
            for name,expected in [('legal_exact',False),('input_never_accepted',True),('missing_status_response',False)]:
                r=done.replay(d,fixtures()[name]['rows'],root/name,root/'cache')
                self.assertEqual(bool(r['properties'][0]['failures']),expected)

    def test_end_marker_cannot_be_driven_by_candidate(self):
        c=plumbing(3);c['body']='assign trace_done=0;assign active=0;assign ok=63;'
        with tempfile.TemporaryDirectory() as temp:
            try:r=done.compile_monitor(c,Path(temp)/'monitor')
            except ValueError:return
            self.assertNotEqual(r['status'],'complete')


if __name__=='__main__':unittest.main()
