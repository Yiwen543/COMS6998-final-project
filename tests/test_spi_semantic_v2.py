import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from spi_semantic_v2 import BitVectors, RichAdapter, Unsupported, integer
from spi_netlist_proof import prove
from screen_spi_semantic_v2 import mapping

SLANG = ROOT/'build/tools/oss-cad-20261103/oss-cad-suite/bin/slang'
YOSYS = SLANG.with_name('yosys')


def bvmodel():
    model = object.__new__(BitVectors)
    model.variables, model.definitions, model.memo = {}, {}, {}
    model.expand_aliases = True
    model.active, model.used_aliases = set(), set()
    return model


def const(value, width, signed=False):
    return {'kind': 'constant', 'value': value,
            'type': {'width': width, 'signed': signed, 'four_state': True}}


def unsat(expression):
    result = subprocess.run(['z3', '-in'], input='(set-logic QF_BV)\n(assert '+expression+')\n(check-sat)\n',
                            text=True, capture_output=True, check=True, timeout=10)
    return result.stdout.strip() == 'unsat'


class BitVectorTests(unittest.TestCase):
    def test_sized_constants_and_unknowns(self):
        self.assertEqual(integer("4'shf", 8), 255)
        self.assertEqual(integer("8'sd-1", 8), 255)
        self.assertEqual(integer('-1', 4), 15)
        self.assertEqual(integer("'1", 5), 31)
        with self.assertRaises(Unsupported):
            integer("4'bx001", 4)

    def test_sign_extension_and_truncation(self):
        signed = {'kind': 'Conversion', 'type': const(0, 8)['type'], 'operand': const(15, 4, True)}
        unsigned = {**signed, 'operand': const(15, 4, False)}
        model = bvmodel()
        self.assertTrue(unsat(f'(not (= {model.term(signed)} #xff))'))
        self.assertTrue(unsat(f'(not (= {model.term(unsigned)} #x0f))'))
        narrow = {'kind': 'Conversion', 'type': const(0, 4)['type'], 'operand': const(0x9f, 8)}
        self.assertTrue(unsat(f'(not (= {model.term(narrow)} #xf))'))

    def test_vector_not_not_logical_not_and_signed_order(self):
        model = bvmodel()
        bitwise = {'kind': 'UnaryOp', 'type': const(0, 2)['type'], 'op': 'BitwiseNot', 'operand': const(2, 2)}
        logical = {**bitwise, 'type': const(0, 1)['type'], 'op': 'LogicalNot'}
        self.assertTrue(unsat(f'(not (= {model.term(bitwise)} #b01))'))
        self.assertTrue(unsat(f'(not (= {model.term(logical)} #b0))'))
        comparison = {'kind': 'BinaryOp', 'type': const(0, 1)['type'], 'op': 'LessThan',
                      'left': const(15, 4, True), 'right': const(0, 4, True)}
        self.assertTrue(unsat(f'(not (= {model.term(comparison)} #b1))'))

    def test_packed_field_offset_and_cycle_rejection(self):
        model = bvmodel()
        field = {'kind': 'MemberAccess', 'type': const(0, 4)['type'], 'value': const(0xab, 8), 'bit_offset': 4}
        self.assertTrue(unsat(f'(not (= {model.term(field)} #xa))'))
        variable = {'kind': 'NamedValue', 'type': const(0, 1)['type'], 'symbol': 'a',
                    'declaration': {'source': 'test', 'line': 1}}
        model.definitions[model.name(variable)] = variable
        with self.assertRaisesRegex(Unsupported, 'cycle'):
            model.term(variable)

    def test_false_counter_mapping_is_exact_and_separate(self):
        target = {'outcome': 'cond_else', 'counter_anchor': {'source': 'x', 'line': 1, 'column': 9},
                  'counter_anchor_basis': 'test'}
        point = {'source': 'x', 'line': 1, 'column': 9, 'type': 'branch', 'outcome': 'cond_else', 'hits': 0}
        self.assertEqual(mapping(target, [point])['status'], 'mapped')
        self.assertEqual(mapping(target, [dict(point, outcome='cond_then')])['status'], 'unresolved')
        self.assertEqual(mapping(target, [dict(point, column=8)])['status'], 'unresolved')


class SSATests(unittest.TestCase):
    def make_ast(self, folder, text):
        source = folder/'fixture.sv'
        source.write_text(text)
        ast = folder/'ast.json'
        subprocess.run([str(SLANG), '--top', 'spi_host_fsm', '--ast-json', str(ast),
                        '--ast-json-source-info', '--ast-json-detailed-types', str(source)],
                       capture_output=True, check=True, timeout=20)
        return source, ast

    def test_ssa_priority_and_sizing_against_independent_netlist(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            source, ast = self.make_ast(folder, '''module spi_host_fsm(input logic a,b,
input logic signed [3:0] x,input logic [3:0] y,output logic [7:0] s, output logic [3:0] q, output logic [1:0] p);
always_comb begin q=4'd3; if(a) q=x; else if(b) q=y; end
assign s=$signed(x);
always_comb begin p=0; case(y) 4'd1,4'd2: p=1; 4'd3: p=2; default: p=3; endcase end
endmodule
''')
            net = folder/'net.json'
            subprocess.run([str(YOSYS), '-Q', '-p', f'read_slang --single-unit --top spi_host_fsm {source}; proc; write_json {net}'],
                           capture_output=True, check=True, timeout=30)
            report = prove(ast, net, folder/'proof')
            self.assertEqual(report['status'], 'pass')
            self.assertEqual(len(report['definition_checks']), 3)
            mutant = folder/'mutant.sv'
            mutant.write_text(source.read_text().replace('if(a)', 'if(!a)'))
            wrong_net = folder/'wrong-net.json'
            subprocess.run([str(YOSYS), '-Q', '-p', f'read_slang --single-unit --top spi_host_fsm {mutant}; proc; write_json {wrong_net}'],
                           capture_output=True, check=True, timeout=30)
            rejected = prove(ast, wrong_net, folder/'negative-proof')
            self.assertEqual(rejected['status'], 'unresolved_or_mismatch')
            self.assertTrue(any(row['symbol'] == 'q' and row['z3'] == 'sat' for row in rejected['definition_checks']))

    def test_latch_is_unresolved_not_assumed_zero(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            _, ast = self.make_ast(folder, 'module spi_host_fsm(input a,b, output logic q); always_comb if(a) q=b; endmodule\n')
            adapter = RichAdapter(json.loads(ast.read_text()), 'spi_host_fsm').extract()
            model = BitVectors(adapter, procedural=True)
            self.assertFalse(model.definitions)
            self.assertTrue(any('Not assigned on every path' in row['reason'] for row in model.unresolved))


if __name__ == '__main__':
    unittest.main()
