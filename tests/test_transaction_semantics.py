import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'tests')]
from test_write_hierarchy import fixture
from transaction_semantics import TransactionAdapter,TransactionBitVectors,ObservationNetlist
from real_parent_screen import replace
import hierarchy_netlist_proof as proof_module

def run_proof(folder,src):
    ast,net=fixture(folder,src);module=json.loads(net.read_text())['modules']['natural_toy']
    class Bound(TransactionAdapter):
        def __init__(self,a,t):super().__init__(a,t,module)
    with replace(proof_module,NaturalAdapter=Bound,NaturalBitVectors=TransactionBitVectors,NaturalNetlist=ObservationNetlist):
        r=proof_module.prove(ast,net,'natural_toy',folder/'proof')
    return r,Bound(json.loads(ast.read_text()),'natural_toy').extract(),module

class TransactionTests(unittest.TestCase):
    def test_ascending_descending_unpacked_layout_and_total_index(self):
        for rng in ('0:1','1:0'):
            src=f'''module natural_toy(input [3:0] x,y,input sel,output [3:0] q);
wire [3:0] a[{rng}];assign a[0]=x;assign a[1]=y;assign q=a[sel];endmodule'''
            with tempfile.TemporaryDirectory() as d:
                r,a,n=run_proof(Path(d),src);self.assertEqual(r['status'],'pass')
                self.assertIn('a',a.array_bindings)

    def test_cached_instance_ports_have_distinct_proven_bindings(self):
        src='''module child(input [3:0] x,output [3:0] q);assign q=~x;endmodule
module natural_toy(input [7:0] x,output [7:0] q);genvar i;
for(i=0;i<2;i=i+1) begin:g child u(.x(x[i*4+:4]),.q(q[i*4+:4]));end endmodule'''
        with tempfile.TemporaryDirectory() as d:
            r,a,n=run_proof(Path(d),src);self.assertEqual(r['status'],'pass')
            self.assertEqual(len(a.instances),2)
            self.assertEqual(len({p['internal_symbol'] for p in a.port_aliases}),4)

    def test_disjoint_procedural_array_bits_and_static_bound_math(self):
        src='''module natural_toy(input [7:0] x,output [7:0] q);
reg [3:0] a[0:1];integer i;
always @* for(i=0;i<2;i=i+1) a[i]=x[i*4+:4];
assign q={a[1],a[0]};endmodule'''
        with tempfile.TemporaryDirectory() as d:
            r,a,n=run_proof(Path(d),src);self.assertEqual(r['status'],'pass')

    def test_separate_procedures_require_disjoint_complete_bits(self):
        src='''module natural_toy(input [3:0] x,output reg [3:0] q);
always @* q[1:0]=x[1:0];always @* q[3:2]=x[3:2];endmodule'''
        with tempfile.TemporaryDirectory() as d:
            r,a,n=run_proof(Path(d),src);self.assertEqual(r['status'],'pass')
        src='''module natural_toy(input [3:0] x,input en,output reg [3:0] q);
always @* if(en) q[1:0]=x[1:0];always @* q[3:2]=x[3:2];endmodule'''
        with tempfile.TemporaryDirectory() as d:
            r,a,n=run_proof(Path(d),src);m=TransactionBitVectors(a,procedural=True)
            self.assertFalse(any(x['lhs']['symbol']=='q' for x in m.definition_sources.values()))
            self.assertTrue(any('Incomplete' in x['reason'] for x in m.unresolved))

    def test_print_is_only_ignored_if_no_outputs(self):
        src='''module natural_toy(input x,output q);initial $display("hello");assign q=~x;endmodule'''
        with tempfile.TemporaryDirectory() as d:
            r,a,n=run_proof(Path(d),src);self.assertEqual(r['status'],'pass')
            self.assertTrue(ObservationNetlist(n).omitted_observers)
            bad=copy.deepcopy(n);c=next(c for c in bad['cells'].values() if c['type']=='$print');c['port_directions']['EN']='output'
            with self.assertRaisesRegex(Exception,'drives a net'):ObservationNetlist(bad)


class BoundaryRegressions(unittest.TestCase):
    def test_dynamic_part_select_bound_is_proved_not_truncated(self):
        good='''module natural_toy(input [15:0] x,input [1:0] i,output [3:0] q);
assign q=x[i*4+:4];endmodule'''
        with tempfile.TemporaryDirectory() as d:
            r,a,n=run_proof(Path(d),good);self.assertEqual(r['status'],'pass')
            self.assertTrue(a.range_proofs)
        bad='''module natural_toy(input [11:0] x,input [1:0] i,output [3:0] q);
assign q=x[i*4+:4];endmodule'''
        with tempfile.TemporaryDirectory() as d:
            r,a,n=run_proof(Path(d),bad);m=TransactionBitVectors(a,procedural=True)
            self.assertFalse(any(x['lhs']['symbol']=='q' for x in m.definition_sources.values()))
            self.assertTrue(any('range not independently proved' in x['reason'] for x in m.unresolved))

    def test_same_source_memories_are_independent_instance_cuts(self):
        src='''module child(input clk,we,input [1:0] addr,input [3:0] x,output [3:0] q);
reg [3:0] mem[0:3];always @(posedge clk) if(we) mem[addr]<=x;
assign q=mem[addr];endmodule
module natural_toy(input clk,input [1:0] we,addr,input [7:0] x,output [7:0] q);
child u0(clk,we[0],addr,x[3:0],q[3:0]);child u1(clk,we[1],addr,x[7:4],q[7:4]);endmodule'''
        with tempfile.TemporaryDirectory() as d:
            r,a,n=run_proof(Path(d),src);self.assertEqual(r['status'],'pass')
            m=TransactionBitVectors(a,procedural=True)
            for row in m.definition_sources.values():m.term(row['rhs'])
            reads=[v for v in m.variables.values() if v['kind']=='MemoryRead']
            self.assertEqual(len({v['symbol'] for v in reads}),2)
            self.assertEqual({v['memory'] for v in reads},{'u0.mem','u1.mem'})

    def test_mutated_output_binding_fails_independent_proof(self):
        src='''module natural_toy(input [3:0] x,y,output [7:0] q);
wire [3:0] a[0:1];assign a[0]=x;assign a[1]=y;assign q={a[0],a[1]};endmodule'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);j=json.loads(net.read_text());module=j['modules']['natural_toy']
            class Bound(TransactionAdapter):
                def __init__(self,a,t):super().__init__(a,t,module)
            module['netnames']['q']['bits']=list(reversed(module['netnames']['q']['bits']))
            net.write_text(json.dumps(j))
            with replace(proof_module,NaturalAdapter=Bound,NaturalBitVectors=TransactionBitVectors,NaturalNetlist=ObservationNetlist):
                r=proof_module.prove(ast,net,'natural_toy',f/'bad-proof')
            self.assertNotEqual(r['status'],'pass')
            self.assertTrue(any(x['z3']=='sat' for x in r['definition_checks']))


class SignedBoundTests(unittest.TestCase):
    def test_signed_negative_index_is_not_small_unsigned_offset(self):
        from transaction_semantics import bounded_query
        header='(set-logic QF_BV)\n(declare-fun i () (_ BitVec 2))'
        with self.assertRaisesRegex(Exception,'range not independently proved'):
            bounded_query(header,'i',2,15,signed=True)
        self.assertEqual(bounded_query(header,'i',2,15,signed=False)['z3'],'unsat')

    def test_ascending_packed_index_not_silently_reversed(self):
        src='module natural_toy(input [0:3] x,input [1:0] i,output q);assign q=x[i];endmodule'
        with tempfile.TemporaryDirectory() as d:
            r,a,n=run_proof(Path(d),src);m=TransactionBitVectors(a,procedural=True)
            self.assertFalse(any(x['lhs']['symbol']=='q' for x in m.definition_sources.values()))
            self.assertTrue(any('Ascending dynamic' in x['reason'] for x in m.unresolved))

if __name__=='__main__':unittest.main()
