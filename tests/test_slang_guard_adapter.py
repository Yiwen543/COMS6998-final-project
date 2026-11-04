import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from slang_guard_adapter import Adapter, Unsupported, walk

SLANG = ROOT/'build/tools/oss-cad-20261103/oss-cad-suite/bin/slang'
FIXTURE = '''module probe(input logic clk,rst,a,b,input logic signed [3:0] x,input logic [3:0] y, output logic [5:0] q);
always_ff @(posedge clk or negedge rst) if(!rst) q[0]<=0; else if(a && b) q[0]<=1;
always_ff @(posedge clk or negedge rst) if(!rst) q[1]<=0; else if(!(!a || !b)) q[1]<=1;
always_ff @(posedge clk) if(!rst) q[2]<=0; else if(a && b) q[2]<=1;
always_comb begin
q[3]=0; if(a) begin if(b) q[3]=1; end
q[4]=0; if(~x) q[4]=1;
q[5]=0; case(y) 4'd1: if(a) q[5]=1; 4'd2: if(a) q[5]=1; default: q[5]=0; endcase
end
endmodule
'''


class SlangTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        root = Path(cls.temp.name)
        (root/'probe.sv').write_text(FIXTURE)
        subprocess.run([str(SLANG), '--top', 'probe', '--ast-json', str(root/'ast.json'),
                        '--ast-json-source-info', '--ast-json-detailed-types', str(root/'probe.sv')],
                       capture_output=True, check=True, timeout=30)
        cls.a = Adapter(json.loads((root/'ast.json').read_text()), 'probe').extract()
        cls.data = cls.a.evidence()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_rewrite_and_sync_reset_context(self):
        groups = [g for g in self.data['groups'] if g['distinct_expressions'] > 1]
        self.assertEqual(len(groups), 1)
        self.assertEqual({m['line'] for m in groups[0]['members']}, {2, 3})
        self.assertNotIn(4, {m['line'] for m in groups[0]['members']})
        self.assertEqual(groups[0]['z3_pair_proofs'], 1)

    def test_vector_not_and_signed_width_preserved(self):
        atoms = [a for a in self.data['atoms'].values() if 'BitwiseNot' in str(a)]
        self.assertEqual(len(atoms), 1)
        self.assertEqual(atoms[0]['operand']['type']['width'], 4)
        self.assertTrue(atoms[0]['operand']['type']['signed'])
        target = next(t for t in self.data['targets'] if t['line'] == 7)
        self.assertFalse(target['compact'].startswith('(not '))

    def test_complete_nested_and_case_guards(self):
        nested = [t for t in self.data['targets'] if t['line'] == 6]
        self.assertEqual(nested[1]['guard_depth'], 2)
        self.assertTrue(nested[1]['compact'].startswith('(and '))
        cases = [t for t in self.data['targets'] if t['outcome'] == 'case']
        self.assertEqual(len(cases), 2)
        self.assertIn('(not ', cases[1]['compact'])
        self.assertNotEqual(cases[0]['compact'], cases[1]['compact'])
        self.assertFalse(self.data['unsupported'])

    def test_blocking_assignment_requires_ssa(self):
        node = next(n for n in walk(self.a.body) if n.get('kind') == 'NamedValue' and n['symbol'].endswith(' a'))
        original = self.a.blocking_writes
        try:
            self.a.blocking_writes = {node['symbol'].split()[0]}
            with self.assertRaisesRegex(Unsupported, 'SSA required'):
                self.a.boolean(node)
        finally:
            self.a.blocking_writes = original


if __name__ == '__main__':
    unittest.main()
