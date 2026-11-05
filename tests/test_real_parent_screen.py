import copy
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'tests')]
from test_write_hierarchy import fixture,solve
from real_parent_semantics import ParentAdapter,ParentBitVectors
from real_parent_screen import prove,configuration,verify,SCOPE
from spi_core_interface import action,validate,seed
from probe_spi_core_events import cases,identity
from prepare_spi_core_checker_role import prepare
from summarize_real_parent_screen import transport_violations
import run_spi_core_checker_roles as roles

class RealParentTests(unittest.TestCase):
    def test_concatenated_child_output_direction_and_bit_order(self):
        src='''module child(input [7:0] x,output [7:0] q);assign q=x;endmodule
module natural_toy(input [7:0] x,output [3:0] hi,lo,output hit);
child u(.x(x),.q({hi,lo}));assign hit=(hi==4'h8)&&(lo==4'h1);endmodule
'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);raw=ast.read_bytes()
            (f/'flat-simplified.json').write_bytes(net.read_bytes())
            r=prove('natural_toy',f,f/'proof');self.assertEqual(r['status'],'pass')
            self.assertEqual(ast.read_bytes(),raw)
            bad=json.loads(net.read_text());bits=bad['modules']['natural_toy']['netnames']['lo']['bits'];bits.reverse()
            (f/'flat-simplified.json').write_text(json.dumps(bad))
            self.assertNotEqual(prove('natural_toy',f,f/'bad-proof')['status'],'pass')

    def test_all_packed_bits_assigned_with_last_write_priority(self):
        src='''module natural_toy(input [3:0] x,output reg [3:0] q,output hit);
always @* begin q[0]=x[1];q[3:1]=x[3:1];q[0]=x[0];end
assign hit=(q==4'h9);endmodule
'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);(f/'flat-simplified.json').write_bytes(net.read_bytes())
            self.assertEqual(prove('natural_toy',f,f/'proof')['status'],'pass')
            a=ParentAdapter(json.loads(ast.read_text()),'natural_toy').extract();m=ParentBitVectors(a,procedural=True)
            self.assertFalse(m.unresolved)

    def test_unassigned_packed_bit_never_assumed_zero(self):
        src='''module natural_toy(input en,input [2:0] x,output reg [3:0] q,output reg hit);
always @* begin q[2:0]=x;hit=0;if(en && q[3]) hit=1;end
endmodule
'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src)
            a=ParentAdapter(json.loads(ast.read_text()),'natural_toy').extract();m=ParentBitVectors(a,procedural=True)
            self.assertTrue(m.unresolved or a.unsupported)
            self.assertFalse(any(v['lhs']['symbol']=='q' for v in m.definition_sources.values()))

    def test_packed_insert_does_not_erase_incomplete_initial_value(self):
        info={'width':4,'signed':False,'four_state':True};part={'kind':'constant','type':{**info,'width':1},'value':1}
        n=ParentBitVectors.packed_insert({'kind':'Uninitialized','type':info},part,0,info)
        self.assertEqual(n['value']['kind'],'Uninitialized')
        for i in range(1,4):n=ParentBitVectors.packed_insert(n,part,i,info)
        self.assertEqual(n['kind'],'Concatenation')

    def test_scope_hashes_and_original_budget(self):
        scope=json.loads(SCOPE.read_text());old=json.loads((ROOT/'configs/natural_write_scope.json').read_text())
        self.assertEqual(scope['development_budget'],old['development_budget'])
        self.assertEqual(scope['development_acceptance'],old['development_acceptance'])
        for c in scope['candidates']:verify(configuration(c['top']))
        self.assertEqual(scope['offline_acceptance']['min_source_distinct_groups'],3)

    def test_driver_schema_and_private_calibration_budget(self):
        for a in cases().values():validate({'actions':a},392,initial=True)
        for change in ({'tx_data':1<<32},{'valid':True},{'speed':3},{'speed':1,'write':1,'read':1},{'sr_wr_ready_i':1}):
            a={**action(),**change}
            with self.assertRaises(ValueError):validate({'actions':[a]},64)
        with self.assertRaises(ValueError):validate({'actions':seed()[1:]},392,initial=True)

    def test_raw_counter_instances_remain_separate(self):
        p={'source':'packer.sv','line':1,'column':2,'type':'branch','outcome':'if','hierarchy':'tb.dut.u0'}
        self.assertEqual(identity(p),identity({**p,'hierarchy':'other_tb.dut.u0'}))
        self.assertNotEqual(identity(p),identity({**p,'hierarchy':'tb.dut.u1'}))

    def test_author_packet_is_spec_interface_only(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'packet';prepare(p);packet=json.loads((p/'packet.json').read_text())
            self.assertEqual(set(packet),{'role','scope','authority','interface','requested_events','isolation'})
            self.assertTrue(all(x['source'].endswith('/doc/theory_of_operation.md') for x in packet['authority']))
            self.assertNotIn('u_fsm.',(p/'prompt.txt').read_text())
            self.assertNotIn('eclass',(p/'prompt.txt').read_text())
            self.assertLess((p/'prompt.txt').stat().st_size,150000)

    def test_input_transport_cannot_drop_blocked_command_or_tx(self):
        first={'cycle':0,'action':action(valid=1,tx_valid=1,tx_data=55),'pre':{'ready':0,'tx_ready':0}}
        good={'cycle':1,'action':copy.deepcopy(first['action']),'pre':{'ready':1,'tx_ready':1}}
        self.assertEqual(transport_violations([first,good]),[])
        bad=copy.deepcopy(good);bad['action'].update(valid=0,tx_data=54)
        self.assertEqual(len(transport_violations([first,bad])),2)
        reset=copy.deepcopy(bad);reset['action'].update(rst_n=0,tx_valid=0)
        self.assertEqual(transport_violations([first,reset]),[])

    def test_live_wrapper_reuses_transport_without_calling_models_in_tests(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'packet';out=Path(d)/'out';prepare(p)
            def fake_run(packet,output,prior):
                output.mkdir();roles.transport.call('test',output,{},'I2C specification checker author')
            with patch.object(roles.transport,'run',side_effect=fake_run) as run,patch.object(roles.transport,'call',return_value={}) as call:
                roles.run(p,out);self.assertEqual(call.call_args.args[3],'SPI core specification checker author')
                self.assertIs(roles.transport.call,call)
                (p/'prompt.txt').write_text('tampered')
                with self.assertRaises(ValueError):roles.run(p,Path(d)/'bad')
                self.assertEqual(run.call_count,1)

if __name__=='__main__':unittest.main()
