import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from hierarchy_semantics import HierarchyAdapter,HierarchyBitVectors
from hierarchy_netlist_proof import prove
from screen_write_hierarchy import join_counter,aggregate,clock_context
from probe_write_scopes import configuration,verify
from probe_natural_frontends import TOOLS
from slang_guard_adapter import Unsupported


def fixture(folder,source,top='natural_toy'):
    src=folder/'fixture.sv';src.write_text(source);ast=folder/'ast.json';net=folder/'net.json'
    subprocess.run([str(TOOLS/'slang'),'--top',top,'--ast-json',str(ast),'--ast-json-source-info','--ast-json-detailed-types',str(src)],capture_output=True,check=True)
    ys=folder/'fixture.ys';ys.write_text(f'read_slang --top {top} {src}; proc; flatten; opt_expr; opt_clean; write_json {net}\n')
    subprocess.run([str(TOOLS/'yosys'),'-Q','-T','-s',str(ys)],capture_output=True,check=True)
    return ast,net


def solve(text):
    r=subprocess.run(['z3','-in'],input=text,text=True,capture_output=True,check=True)
    return r.stdout.splitlines()


class HierarchyTests(unittest.TestCase):
    def test_instances_do_not_collide_and_alias_mutation_rejected(self):
        src='''module child(input a,b,output reg q);
always @* begin
 q=0;
 if(a && b) q=1;
end
endmodule
module natural_toy(input en,x,output wire q0,q1,output reg hit);
child u0(.a(en),.b(x),.q(q0));
child u1(.a(en),.b(!x),.q(q1));
always @* begin
 hit=0;
 if(en && x) hit=1;
end
endmodule
'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);original=ast.read_bytes()
            a=HierarchyAdapter(json.loads(original),'natural_toy').extract();m=HierarchyBitVectors(a,procedural=True);h,t,u=m.guards()
            by={v['instance_scope']:v for v in t if v['outcome']=='if'}
            q=[f'(xor {by["u0"]["id"]} {by[""]["id"]})',f'(xor {by["u1"]["id"]} {by[""]["id"]})']
            self.assertEqual(solve(h+'\n'.join('(push)\n(assert '+x+')\n(check-sat)\n(pop)' for x in q)),['unsat','sat'])
            self.assertEqual(ast.read_bytes(),original)
            self.assertEqual(prove(ast,net,'natural_toy',f/'good')['status'],'pass')
            j=json.loads(net.read_text());j['modules']['natural_toy']['netnames']['u0.a']['bits']=j['modules']['natural_toy']['ports']['x']['bits']
            bad=f/'bad.json';bad.write_text(json.dumps(j));self.assertNotEqual(prove(ast,bad,'natural_toy',f/'bad-proof')['status'],'pass')

    def test_full_case_priority_and_statement_position(self):
        src='''module natural_toy(input [1:0] sel,a,b,input en,output reg [1:0] q);
always @* begin
 q=0;
 case(sel)
 a: q=1;
 b: begin if(en) q=2; end
 default: q=0;
 endcase
end
endmodule
'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);a=HierarchyAdapter(json.loads(ast.read_text()),'natural_toy').extract();m=HierarchyBitVectors(a,procedural=True);h,ts,u=m.guards();v={n['symbol']:k for k,n in m.variables.items()}
            t=next(x for x in ts if x['outcome']=='if');expected=f'(and (= {v["sel"]} {v["b"]}) (not (= {v["sel"]} {v["a"]})) (= {v["en"]} #b1))'
            self.assertEqual(solve(h+f'(assert (xor {t["id"]} {expected}))\n(check-sat)'),['unsat'])
            self.assertEqual(prove(ast,net,'natural_toy',f/'proof')['status'],'pass')

    def test_dynamic_select_total_domain_and_out_of_range_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,'module natural_toy(input [3:0] x,input [1:0] i,output y);assign y=x[i];endmodule\n')
            self.assertEqual(prove(ast,net,'natural_toy',f/'proof')['status'],'pass')
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,'module natural_toy(input [2:0] x,input [1:0] i,output y);assign y=x[i];endmodule\n')
            a=HierarchyAdapter(json.loads(ast.read_text()),'natural_toy');m=HierarchyBitVectors(a,procedural=True)
            self.assertTrue(m.unresolved);self.assertFalse(m.definitions)

    def test_clock_alias_not_same_as_reset_or_inversion(self):
        src='''module child(input clk,rst,en,output reg q);
always @(posedge clk or negedge rst) if(!rst) q<=0; else if(en) q<=1;
endmodule
module natural_toy(input clk,rst,en,output q);child u(.clk(clk),.rst(rst),.en(en),.q(q));endmodule
'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);a=HierarchyAdapter(json.loads(ast.read_text()),'natural_toy').extract();n=json.loads(net.read_text())['modules']['natural_toy'];c={'clock':'clk','reset':'rst','reset_active':0}
            clock_context(a,n,c);self.assertEqual(a.targets[0]['event_context'],['PosEdge:clk','NegEdge:rst'])
            bad=copy.deepcopy(n)
            for x in bad['cells'].values():
                if x['type'] in ('$aldff','$adff'):x['parameters']['CLK_POLARITY']='0'
            with self.assertRaises(Unsupported):clock_context(a,bad,c)

    def test_exact_counter_and_shared_iteration_union(self):
        point={'source':'x.sv','line':10,'column':4,'type':'branch','outcome':'if','hierarchy':'tb.dut.u','hits':0}
        t={'id':'t0','source':'x.sv','line':10,'column':4,'instance_scope':'u.gen[0]','counter_anchor':{'source':'x.sv','line':10,'column':4},'counter_anchor_basis':'test','outcome':'if','compact':'p_a','local_compact':'p_a','event_context':['combinational']}
        other={**t,'id':'t1','instance_scope':'u.gen[1]','compact':'p_b','local_compact':'p_b'}
        instances=[{'path':'u'}];maps={x['id']:join_counter(x,[point],instances) for x in [t,other]}
        ts,joined=aggregate([t,other],maps);self.assertEqual(len(ts),1);self.assertEqual(ts[0]['compact'],'(or p_a p_b)');self.assertEqual(len(joined),1)
        bad=copy.deepcopy(t);bad['counter_anchor']['column']+=1;self.assertEqual(join_counter(bad,[point],instances)['status'],'unresolved')
        bad=copy.deepcopy(t);bad['instance_scope']='other';self.assertEqual(join_counter(bad,[point],instances)['status'],'unresolved')

    def test_loop_guard_union_retains_outer_enable(self):
        src="""module natural_toy(input en,input [3:0] x,output reg [2:0] q);
integer i;
always @* begin
 q=0;
 if(en) begin
  for(i=3;i>=0;i=i-1) begin
   if(x[i]) q=i;
  end
 end
end
endmodule
"""
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src);a=HierarchyAdapter(json.loads(ast.read_text()),'natural_toy').extract();m=HierarchyBitVectors(a,procedural=True);h,ts,u=m.guards()
            inner=[t for t in ts if t['line']==7 and t['outcome']=='if'];self.assertEqual(len(inner),4)
            v={n['symbol']:k for k,n in m.variables.items()};union='(or '+' '.join(t['id'] for t in inner)+')'
            expect=f'(and (= {v["en"]} #b1) (not (= {v["x"]} #x0)))'
            self.assertEqual(solve(h+f'(assert (xor {union} {expect}))\n(check-sat)'),['unsat'])
            self.assertEqual(a.loop_unrolls[0]['values'],[3,2,1,0])

    def test_memory_address_mismatch_is_detected(self):
        src="""module natural_toy(input clk,we,input [1:0] addr,input [7:0] data,output wire [7:0] q);
reg [7:0] mem [0:3];
always @(posedge clk) if(we) mem[addr]<=data;
assign q=mem[addr];
endmodule
"""
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=fixture(f,src)
            self.assertEqual(prove(ast,net,'natural_toy',f/'good')['status'],'pass')
            j=json.loads(net.read_text());c=next(x for x in j['modules']['natural_toy']['cells'].values() if x['type']=='$memrd_v2');c['connections']['ADDR']=['0','0']
            bad=f/'bad.json';bad.write_text(json.dumps(j))
            self.assertNotEqual(prove(ast,bad,'natural_toy',f/'bad-proof')['status'],'pass')

    def test_scope_versions_and_unchanged_budget(self):
        c=json.loads((ROOT/'configs/natural_write_scope.json').read_text())
        self.assertEqual(c['development_budget'],{'repetitions':3,'rounds':6,'max_new_cycles':64,'seed_cycles':8})
        self.assertEqual(len({x['family'] for x in c['candidates']}),2)
        for candidate in c['candidates']:verify(candidate)
        self.assertEqual(c['offline_acceptance']['min_source_distinct_groups'],3)

if __name__=='__main__':unittest.main()
