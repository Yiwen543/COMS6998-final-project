import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'tests')]
from test_write_hierarchy import fixture
from event_scope_semantics import EventAdapter,EventBitVectors,lvalue_bases
from slang_guard_adapter import walk
import real_parent_screen as parent
from screen_multistep_events import SCOPE,configuration
from probe_write_scopes import verify
import probe_frame_ordinary as ordinary

def proof(folder,name='proof'):
    with parent.replace(parent,ParentAdapter=EventAdapter,ParentBitVectors=EventBitVectors):
        return parent.prove('natural_toy',folder,folder/name)

class EventScopeTests(unittest.TestCase):
    def test_loop_index_and_width_are_reads_not_writers(self):
        lhs={'kind':'RangeSelect','value':{'kind':'NamedValue','symbol':'q'},
             'left':{'kind':'NamedValue','symbol':'i'},'right':{'kind':'NamedValue','symbol':'WIDTH'}}
        self.assertEqual([x['symbol'] for x in lvalue_bases(lhs)],['q'])
        src='''module natural_toy(input [3:0] x,output reg [3:0] q);
integer i; always @* begin q=0; for(i=0;i<=3;i=i+1) q[i]=x[i]; end
endmodule
'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);raw=ast.read_bytes()
            (f/'flat-simplified.json').write_bytes(net.read_bytes())
            a=EventAdapter(json.loads(raw),'natural_toy').extract()
            self.assertEqual(a.loop_unrolls[0]['values'],[0,1,2,3])
            self.assertEqual(proof(f)['status'],'pass')
            self.assertEqual(ast.read_bytes(),raw)
            # A real bit-order error must fail the independent netlist check.
            bad=json.loads(net.read_text());bad['modules']['natural_toy']['netnames']['q']['bits'].reverse()
            (f/'flat-simplified.json').write_text(json.dumps(bad))
            self.assertNotEqual(proof(f,'bad-proof')['status'],'pass')

    def test_genuine_loop_body_write_and_unbounded_loop_withheld(self):
        for body,reason in [('for(i=0;i<4;i=i+1) begin q[i]=x[i]; i=i+1; end','actually writes'),
                            ('for(i=0;i<100;i=i+1) q=x;','exceeds64')]:
            with tempfile.TemporaryDirectory() as d:
                ast,_=fixture(Path(d),'module natural_toy(input [3:0] x,output reg [3:0] q); integer i; always @* begin q=0; '+body+' end endmodule')
                a=EventAdapter(json.loads(ast.read_text()),'natural_toy').extract()
                self.assertTrue(any(reason in x['reason'] for x in a.unsupported))

    def test_parameter_pruned_dynamic_condition_retained(self):
        src='''module natural_toy(input en,x,output reg q);parameter ENABLE=0;
always @* begin q=0;if(ENABLE) q=1;else if(en) q=x;end endmodule'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);(f/'flat-simplified.json').write_bytes(net.read_bytes())
            a=EventAdapter(json.loads(ast.read_text()),'natural_toy').extract()
            self.assertEqual(len(a.constant_branch_elaboration),1)
            self.assertEqual(a.constant_branch_elaboration[0]['selected'],'ifFalse')
            self.assertTrue(any(n.get('kind')=='Conditional' for n in walk(a.body)))
            self.assertEqual(proof(f)['status'],'pass')

    def test_descending_signed_induction_and_zero_iterations(self):
        src='''module natural_toy(input [3:0] x,output reg [3:0] q);
integer i,j;always @* begin q=0;for(i=3;i> -1;i=i-1) q[i]=x[i];for(j=0;j>0;j=j+1) q=0;end endmodule'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);(f/'flat-simplified.json').write_bytes(net.read_bytes())
            a=EventAdapter(json.loads(ast.read_text()),'natural_toy').extract()
            self.assertEqual([x['values'] for x in a.loop_unrolls],[[3,2,1,0],[]])
            self.assertEqual(proof(f)['status'],'pass')

    def test_no_budget_change_and_sources_pinned(self):
        new=json.loads(SCOPE.read_text());old=json.loads((ROOT/'configs/spi_core_safe_b_development_v1.json').read_text())
        # The source preregistration uses explicit budget fields. No model call.
        self.assertEqual(new['development_budget'],{'repetitions':3,'rounds':6,'max_new_cycles':64,'seed_cycles':8})
        self.assertEqual(new['development_acceptance'],old['development_acceptance'])
        self.assertFalse(new['B_allowed']);self.assertFalse(new['C_allowed'])
        for c in new['candidates']:verify(configuration(c['top']))

    def test_ordinary_schema_and_queue_corruption_detection(self):
        base=ROOT/'results/multistep_event_screen_20261104'
        ports=json.loads((base/'axis_frame_length_adjust_fifo-v6/netlist.json').read_text())['modules']['axis_frame_length_adjust_fifo']['ports']
        _,ins,outs=ordinary.driver(ports,configuration('axis_frame_length_adjust_fifo'))
        for name,actions in ordinary.cases().items():
            ordinary.validate(actions)
            log=(base/'frame-ordinary-v4'/name/'verilator/simulation.log').read_text()
            rows,accepted=ordinary.parse(log,actions,ins,outs)
            self.assertEqual(len(accepted),sum(a['offer'] for a in actions))
            self.assertEqual(len(rows),len(actions))
            c=configuration('axis_frame_length_adjust_fifo')
            for i,row in enumerate(rows[:8]):
                for k in ins:
                    expected=int(i<2) if k=='rst' else c['seed_inputs'].get(k,0)
                    self.assertEqual(row['action'][k],expected,(i,k))
        bad=copy.deepcopy(actions);bad[-1]['offer']=True
        with self.assertRaises(ValueError):ordinary.validate(bad)
        bad=copy.deepcopy(actions);bad[-1]['data']=256
        with self.assertRaises(ValueError):ordinary.validate(bad)
        # An actual held-payload mutation is rejected, even if outputs agree.
        lines=log.splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('PRE 8 '))
        fields=lines[i].split();fields[2+ins.index('s_axis_tdata')]='99';lines[i]=' '.join(fields)
        with self.assertRaisesRegex(ValueError,'transport/input'):ordinary.parse('\n'.join(lines),actions,ins,outs)
        with self.assertRaisesRegex(ValueError,'Incomplete trace'):ordinary.parse('\n'.join(s for s in log.splitlines() if not s.startswith('QUEUE 8 ')),actions,ins,outs)

    def test_static_equivalence_is_not_event_qualification(self):
        base=ROOT/'results/multistep_event_screen_20261104'
        s=json.loads((base/'axis_frame_length_adjust_fifo-v6/decision.json').read_text())
        o=json.loads((base/'frame-ordinary-v4/summary.json').read_text())
        self.assertEqual(s['static_groups'],6)
        self.assertEqual(o['eligible_event_groups'],[])
        self.assertEqual(o['gate'],'reject_before_checker')
        self.assertFalse(o['B_allowed']);self.assertFalse(o['C_allowed'])
        self.assertFalse(o['checker_called']);self.assertEqual(o['model_calls'],0)

    def test_failure_review_packet_is_lossless_and_isolated(self):
        from review_spi_core_failures import prepare
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'packet';prepare(p)
            manifest=json.loads((p/'manifest.json').read_text())
            packet=json.loads((p/'packet.json').read_text())
            self.assertEqual(manifest['full_trace_rows'],596)
            self.assertLess(manifest['prompt_bytes'],150000)
            self.assertTrue(manifest['read_only'])
            # Explicitly exclude the fields used by experiment selection.
            def keys(value):
                if isinstance(value,dict):
                    for k,v in value.items():yield k;yield from keys(v)
                elif isinstance(value,list):
                    for v in value:yield from keys(v)
            self.assertFalse(set(keys(packet)) & {'coverage','targets','groups','input_tokens','output_tokens'})

if __name__=='__main__':unittest.main()
