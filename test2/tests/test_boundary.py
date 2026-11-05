import json
from pathlib import Path
import sys
import tempfile
import unittest

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'scripts'))
from prepare import strip_formal, datasets, mutations
from preflight import verify_inputs
from monitor import validate, compile_monitor, build_replay, replay
from feedback import messages
from reference_controls import controls
from audit_observations import compare

def plumbing(active="6'b111111",ok="6'b111111"):
    return {'body':f'assign active={active}; assign ok={ok};',
            'properties':[{'id':f'P{i}','description':'plumbing smoke control, not a specification checker'} for i in range(6)]}

class BoundaryTests(unittest.TestCase):
    def test_registered_files(self): verify_inputs()
    def test_formal_removed_line_preserved(self):
        original=(BASE.parent/'examples/heldout_sfifo_stress/rtl/sfifo.v').read_text()
        clean,removed=strip_formal(original)
        self.assertEqual(clean,(BASE/'public/sfifo.v').read_text())
        self.assertEqual(len(clean.splitlines()),len(original.splitlines()))
        self.assertNotIn('assert(',clean); self.assertGreater(len(removed),100)
    def test_fixed_sets_separate(self):
        d=datasets();self.assertEqual(len(d),6)
        dev={json.dumps(v) for k,v in d.items() if not k.startswith('final')}
        final={json.dumps(v) for k,v in d.items() if k.startswith('final')}
        self.assertFalse(dev&final)
    def test_six_single_site_faults(self):
        for _,source,m in mutations((BASE/'public/sfifo.v').read_text()):
            self.assertEqual(m['changed_sites'],1);self.assertNotEqual(source,(BASE/'public/sfifo.v').read_text())
    def test_reference_controls_structural(self):
        c=controls();self.assertEqual(len(c),20)
        self.assertEqual(c['legal_capacity']['rows'][18]['post']['fill'],15)
        self.assertEqual(c['legal_capacity']['rows'][32]['post']['fill'],1)
        self.assertEqual(c['legal_capacity']['rows'][33]['post']['fill'],0)
    def test_candidate_cannot_call_or_assume(self):
        for code in ('$finish;', 'assume(i_wr);','assign active=dut.rd_addr;',
                     '`include "secret"','always @(negedge i_clk) begin end',
                     'always @(posedge i_reset) begin end','force i_wr=0;'):
            c=plumbing();c['body']=code
            with self.assertRaises(ValueError):validate(c)
    def test_property_budget(self):
        c=plumbing();c['properties'].append(c['properties'][0])
        with self.assertRaises(ValueError):validate(c)
    def test_feedback_isolation(self):
        preflight=BASE/'results/preflight-v2'
        b=messages('B_prime',preflight,1);c=messages('C_prime',preflight,1)
        x=json.loads(b[1]['content']);y=json.loads(c[1]['content'])
        semantic=y.pop('egraph_feedback');self.assertEqual(x,y)
        self.assertEqual(len(semantic['equivalent_groups']),2)
        self.assertEqual(sum(len(g['members']) for g in semantic['equivalent_groups']),5)
        self.assertEqual(set(x['development']),{'basic','boundary','wrap_reset'})
        for forbidden in ('final_boundary','final_mixed','mutant_catalog','reference-controls','checker_source','assert(f_fill'):
            self.assertNotIn(forbidden,b[1]['content']);self.assertNotIn(forbidden,c[1]['content'])
    def test_unknown_comparison_not_binary_failure(self):
        a=controls()['legal_order_and_reset']['rows'];b=json.loads(json.dumps(a))
        b[1]['post']['data']=-1
        r=compare(a,b);self.assertEqual(len(r['unknown_differences']),1);self.assertEqual(r['binary_disagreements'],[])
        b[1]['post']['data']=12;r=compare(a,b);self.assertEqual(len(r['binary_disagreements']),1)
    def test_monitor_replay_complete_and_false_alarm(self):
        trace=controls()['legal_order_and_reset']['rows']
        with tempfile.TemporaryDirectory() as tmp:
            for name,c in [('true',plumbing()),('false',plumbing(ok="6'b000000")),('vacuous',plumbing(active="6'b000000"))]:
                d=Path(tmp)/name
                self.assertEqual(compile_monitor(c,d)['status'],'complete')
                self.assertEqual(build_replay(d)['status'],'complete')
                result=replay(d,trace,Path(tmp)/(name+'-run'))
                self.assertTrue(result['complete']);self.assertEqual(result['samples'],19)
                for p in result['properties']:
                    self.assertEqual(len(p['failures']),19 if name=='false' else 0)
                    self.assertEqual(p['vacuous_on_trace'],name=='vacuous')
    def test_input_write_rejected(self):
        c=plumbing();c['body']+='\nassign i_wr=0;'
        with tempfile.TemporaryDirectory() as d:
            try:r=compile_monitor(c,Path(d)/'compile')
            except ValueError:return
            self.assertNotEqual(r['status'],'complete')
    def test_clocked_observer_sampling(self):
        c=plumbing();c['body']="reg sampled_reset=0; always @(posedge i_clk) sampled_reset<=i_reset; assign active=6'b111111; assign ok={6{sampled_reset}};"
        trace=controls()['legal_order_and_reset']['rows']
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)/'monitor';self.assertEqual(compile_monitor(c,d)['status'],'complete')
            self.assertEqual(build_replay(d)['status'],'complete')
            out=Path(tmp)/'replay';self.assertTrue(replay(d,trace,out)['complete'])
            samples=json.loads((out/'samples.json').read_text())
            for r in samples:
                reset=trace[r['cycle']-(r['phase']=='pre')]['action']['reset']
                self.assertEqual(r['ok'],'111111' if reset else '000000')

if __name__=='__main__':unittest.main()
