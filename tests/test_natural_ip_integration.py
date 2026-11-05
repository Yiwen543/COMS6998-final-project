import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from natural_semantics import NaturalAdapter,NaturalBitVectors
from natural_netlist_proof import NaturalNetlist,prove
from probe_natural_frontends import TOOLS,configuration,verify
from run_midterm_fixed import sha


def const(v,w,signed=False):
    return {'kind':'constant','value':v,'type':{'width':w,'signed':signed,'four_state':True}}


def baremodel():
    m=object.__new__(NaturalBitVectors);m.variables={};m.definitions={};m.memo={};m.active=set();m.used_aliases=set();m.expand_aliases=True
    return m


def bits(v,w):return [str((v>>i)&1) for i in range(w)]


class NaturalArithmetic(unittest.TestCase):
    def test_shifts_width_sign_and_large_count(self):
        queries=[];model=baremodel()
        for w,rw in [(4,2),(4,9),(9,4)]:
            for signed in [False,True]:
                for value in [0,1,(1<<w)-1,1<<(w-1)]:
                    for count in [0,1,min((1<<rw)-1,w), (1<<rw)-1]:
                        for op in ['LogicalShiftLeft','LogicalShiftRight','ArithmeticShiftRight']:
                            a=value-(1<<w) if signed and value&(1<<(w-1)) else value
                            expected=(a>>count) if op=='ArithmeticShiftRight' and signed else ((value<<count) if op.endswith('Left') else value>>count)
                            node={'kind':'BinaryOp','type':const(0,w,signed)['type'],'op':op,'left':const(value,w,signed),'right':const(count,rw)}
                            queries.append('(push)\n(assert (not (= '+model.term(node)+f' (_ bv{expected% (1<<w)} {w}))))\n(check-sat)\n(pop)')
        p=subprocess.run(['z3','-in'],input='(set-logic QF_BV)\n'+'\n'.join(queries),text=True,capture_output=True,check=True)
        self.assertEqual(p.stdout.splitlines(),['unsat']*len(queries))

    def test_yosys_shift_assignment_context(self):
        queries=[]
        for kind in ['$shr','$shl','$sshr']:
            for aw,yw,bw in [(4,8,9),(8,4,9),(4,4,2)]:
                for signed in [False,True]:
                    for value in [0,(1<<aw)-1,1<<(aw-1)]:
                        for count in [0,1,(1<<bw)-1]:
                            c={'type':kind,'parameters':{'A_SIGNED':str(int(signed)),'B_SIGNED':'0'},
                                'connections':{'A':bits(value,aw),'B':bits(count,bw),'Y':list(range(100,100+yw))},
                                'port_directions':{'A':'input','B':'input','Y':'output'}}
                            r=NaturalNetlist({'ports':{},'cells':{'cell':c},'netnames':{}});term,w=r.cell('cell')
                            width=max(aw,yw);v=value-(1<<aw) if signed and value&(1<<(aw-1)) else value
                            expected=(v>>count) if kind=='$sshr' and signed else (((v&((1<<width)-1))>>count) if kind!='$shl' else v<<count)
                            queries.append('(push)\n'+'\n'.join(r.macros.values())+f'\n(assert (not (= {term} (_ bv{expected%(1<<w)} {w}))))\n(check-sat)\n(pop)')
        p=subprocess.run(['z3','-in'],input='(set-logic QF_BV)\n'+'\n'.join(queries),text=True,capture_output=True,check=True)
        self.assertEqual(p.stdout.splitlines(),['unsat']*len(queries))


class NaturalSSA(unittest.TestCase):
    def fixture(self,folder,text):
        src=folder/'fixture.sv';src.write_text(text);ast=folder/'ast.json';net=folder/'net.json'
        subprocess.run([str(TOOLS/'slang'),'--top','natural_toy','--ast-json',str(ast),'--ast-json-source-info','--ast-json-detailed-types',str(src)],capture_output=True,check=True)
        ys=folder/'fixture.ys';ys.write_text(f'read_slang --top natural_toy {src}; proc; flatten; opt_expr; opt_clean; write_json {net}\n')
        subprocess.run([str(TOOLS/'yosys'),'-Q','-T','-s',str(ys)],capture_output=True,check=True)
        return ast,net

    def test_statement_position_and_sibling_guards(self):
        code='''module natural_toy(input en,input [7:0] x,output reg [7:0] n,output reg [1:0] q);
always @* begin
 n=x+1; q=0;
 if(en) begin
  n=x+2;
  if(n==0) q=1;
 end else begin
  if(n==0) q=2;
 end
end
endmodule
'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=self.fixture(f,code);a=NaturalAdapter(json.loads(ast.read_text()),'natural_toy').extract()
            m=NaturalBitVectors(a,procedural=True);header,ts,u=m.guards();self.assertEqual(u,[])
            v={n['symbol']:k for k,n in m.variables.items()};queries=[]
            for line,expected in [(6,f'(and (= {v["en"]} #b1) (= {v["x"]} #xfe))'),(8,f'(and (= {v["en"]} #b0) (= {v["x"]} #xff))')]:
                t=next(t for t in ts if t['line']==line and t['outcome']=='if')
                queries.append(f'(push)\n(assert (xor {t["id"]} {expected}))\n(check-sat)\n(pop)')
            p=subprocess.run(['z3','-in'],input=header+'\n'.join(queries),text=True,capture_output=True,check=True)
            self.assertEqual(p.stdout.splitlines(),['unsat','unsat'])
            self.assertEqual(prove(ast,net,'natural_toy',f/'proof')['status'],'pass')
            j=json.loads(net.read_text());j['modules']['natural_toy']['netnames']['n']['bits']=['0']*8
            bad=f/'bad.json';bad.write_text(json.dumps(j));self.assertNotEqual(prove(ast,bad,'natural_toy',f/'bad-proof')['status'],'pass')

    def test_packed_fields_nonzero_slice_and_overshift(self):
        code='''module natural_toy(input en,input [7:4] x,input [8:0] shift,output logic [7:0] y,output logic p);
typedef struct packed {logic hi; logic [2:0] lo;} pair_t;
pair_t pair;
always_comb begin
 pair='0;
 if(en) pair.hi=x[7]; else pair.lo=x[6:4];
 y={pair,pair} >> shift;
 p=0;
 if(pair.hi && pair.lo==0) p=1;
end
endmodule
'''
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,net=self.fixture(f,code)
            self.assertEqual(prove(ast,net,'natural_toy',f/'proof')['status'],'pass')

    def test_latch_not_assumed_combinational(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d);ast,_=self.fixture(f,'module natural_toy(input a,b,output reg q);always @* if(a) q=b;endmodule\n')
            a=NaturalAdapter(json.loads(ast.read_text()),'natural_toy').extract();m=NaturalBitVectors(a,procedural=True)
            self.assertFalse(m.definitions);self.assertTrue(m.unresolved)


class NaturalEvidence(unittest.TestCase):
    def test_pinned_sources_and_existing_freezes(self):
        for n in ['axi_dma_rd','flash_ctrl_rd']:verify(configuration(n))
        from run_i2c_checked import verify_freeze
        from run_i2c_read_checked import verify_freeze as read_freeze
        verify_freeze();read_freeze()

    def test_no_mapping_fallback_or_counter_merging(self):
        from screen_spi_semantic_v2 import mapping
        b=ROOT/'results/natural_ip_integration_20261104'
        for folder in ['axi_dma_rd','flash_ctrl_rd_v2']:
            screen=json.loads((b/folder/'screen/screen.json').read_text())
            self.assertFalse(screen['B_allowed']);self.assertEqual(screen['static_candidate_groups'],0)
            points=json.loads((b/folder/'inventory/raw-points.json').read_text())
            self.assertEqual(len(points),screen['raw_dut_denominator'])
            ts=json.loads((b/folder/'screen/extraction.json').read_text())['targets']
            t=next(t for t in ts if screen['mappings'][t['id']]['status']=='mapped')
            self.assertEqual(mapping(t,points)['status'],'mapped')
            bad=copy.deepcopy(t);bad['counter_anchor']['line']+=10000
            self.assertEqual(mapping(bad,points)['status'],'unresolved')


if __name__=='__main__':unittest.main()
