import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import dump, sha
import controller_monitor_live as monitor
import controller_release_live as release
from controller_loop_live import messages, plumbing, verify_task, REG
from controller_score_live import strict_score, measured_tokens
from controller_packet_compact import unpack


class ControllerLiveTests(unittest.TestCase):
    def candidate(self, body):
        return dict(body=body, properties=plumbing(3)['properties'])

    def test_sequential_replay_has_no_unregistered_edge(self):
        rows = json.loads((monitor.TASK/'qualification/observations-v2/verilator/basic/rows.json').read_text())
        candidate = self.candidate("reg [15:0] edges=0; always @(posedge clk) edges<=edges+1; assign active=6'b111111; assign ok={6{edges<=2 || !rst}};")
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); d=root/'compiled'
            self.assertEqual(monitor.compile_monitor(candidate,d)['status'],'complete')
            self.assertEqual(monitor.build_replay(d)['status'],'complete')
            result=monitor.replay(d,rows,root/'out',root/'cache')
            self.assertTrue(result['complete'])
            self.assertEqual(result['samples'],len(rows)*2-1)
            self.assertEqual(result['cycles'],len(rows))
            # This check would fail on a free-running clock's extra initial edge.
            self.assertFalse(any(p['failures'] or p['unknown'] for p in result['properties']))

    def test_passive_boundary_rejects_system_hierarchy_clock_and_input_drive(self):
        for body in ['assign active=dut.foo; assign ok=63;', 'always @(posedge s_valid) begin end', 'assume(1);', 'assign clk=0; assign active=63; assign ok=63;']:
            with self.subTest(body=body), tempfile.TemporaryDirectory() as t:
                try:
                    r=monitor.compile_monitor(self.candidate(body),Path(t)/'compiled')
                except ValueError:
                    continue
                self.assertNotEqual(r['status'],'complete')

    def test_unknown_and_false_alarms_remain_distinct(self):
        rows=json.loads((monitor.TASK/'qualification/observations-v2/verilator/basic/rows.json').read_text())
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for label,body in [('unknown',"assign active=6'b111111; assign ok=6'bxxxxxx;"),('false',"assign active=6'b111111; assign ok=0;")]:
                d=root/label;self.assertEqual(monitor.compile_monitor(self.candidate(body),d)['status'],'complete')
                self.assertEqual(monitor.build_replay(d)['status'],'complete')
                r=monitor.replay(d,rows,root/(label+'-out'),root/'cache')
                self.assertTrue(r['complete'])
                self.assertTrue(r['properties'][0]['unknown'] if label=='unknown' else r['properties'][0]['failures'])

    def snapshots(self,root):
        dump(root/'run.json',{});(root/'calls.jsonl').touch(); result=[]
        for a in release.ARMS:
            for rep in (1,2,3):
                for n in range(1,7):
                    d=root/a/str(rep)/str(n);d.mkdir(parents=True)
                    for name in ['prompt.json','response.json','development-feedback.json','development-cost.json']:
                        dump(d/name,{'test':True})
                    result.append(release.freeze_round(root,d,dict(arm=a,repetition=rep,round=n,session_id=a+str(rep)),'invalid_candidate'))
        return result

    def test_all_round_release_requires_36_and_detects_artifact_tamper(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);rows=self.snapshots(root)
            with self.assertRaises(ValueError):release.release(root,rows[:-1],'mock')
            release.release(root,rows,'mock');self.assertEqual(len(release.verify_release(root)),36)
            (root/release.ARMS[0]/'1/1/prompt.json').write_text('changed')
            with self.assertRaises(ValueError):release.verify_release(root)

    def test_six_sessions_are_independent(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);rows=self.snapshots(root)
            path=root/rows[-1]['snapshot'];d=json.loads(path.read_text());d['session_id']='different';dump(path,d);rows[-1]['sha256']=sha(path)
            with self.assertRaises(ValueError):release.release(root,rows,'mock')

    def test_public_packet_and_own_history_only(self):
        b=messages('B2_raw',1);c=messages('C2_semantic',1)
        self.assertEqual(b[0],c[0]);bd=json.loads(b[1]['content']);cd=json.loads(c[1]['content']);cd.pop('egraph_feedback')
        self.assertEqual(bd,cd)
        for text in ['heldout_01','mutant-catalog','reference/frozen','AGENTS.md','HANDOFF.md']:
            self.assertNotIn(text,json.dumps(c))
        own=plumbing(1);p=json.loads(messages('B2_raw',2,own,{'status':'own'})[1]['content'])
        self.assertEqual(p['previous_candidate'],own);self.assertEqual(p['development_feedback'],{'status':'own'})
        verify_task(json.loads(REG.read_text()))

    def test_state_cap_is_enforced(self):
        c=self.candidate("reg [8192:0] state=0; always @(posedge clk) state<={state[8191:0],s_valid}; assign active=63;assign ok={6{^state}};")
        with tempfile.TemporaryDirectory() as t,self.assertRaises(ValueError):monitor.compile_monitor(c,Path(t)/'compiled')

    def test_compact_packet_is_exactly_reversible(self):
        for arm in release.ARMS:
            old=json.loads((monitor.TASK/'qualification/prompt-audit-v2'/(arm+'.json')).read_text())
            new=json.loads((monitor.TASK/'qualification/prompt-audit-v3'/(arm+'.json')).read_text())
            new['raw_coverage']=unpack(new['raw_coverage'])
            self.assertEqual(old,new)

    def test_early_alarm_and_unknown_never_become_pass_or_kill(self):
        p=lambda failures,unknown:dict(checks=1,failures=failures,unknown=unknown)
        correct=[dict(complete=True,properties=[p([],[]) for _ in range(6)])]
        e=[dict(mutant='M1',trace='t',eligible=True,first_reference_failure=dict(cycle=2,phase='post'))]
        r=dict(complete=True,properties=[p([[1,'post'],[3,'post']],[]) for _ in range(6)])
        self.assertFalse(strict_score(correct,{('M1','t'):r},e,100)['details'][0]['valid_kill'])
        r['properties']=[p([[3,'post']],[[4,'post']]) for _ in range(6)]
        result=strict_score(correct,{('M1','t'):r},e,100)
        self.assertTrue(result['details'][0]['valid_kill']);self.assertTrue(result['details'][0]['unresolved'])
        correct[0]['properties'][0]['unknown']=[[1,'pre']]
        self.assertFalse(strict_score(correct,{('M1','t'):r},e,100)['suite_sound_on_fixed_controls'])
        self.assertIsNone(measured_tokens([dict(arm='B',repetition=1,round=1,generation_request_issued=True,usage=None)],'B',1,1))


if __name__=='__main__':unittest.main()
