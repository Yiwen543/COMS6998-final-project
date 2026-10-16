"""Validate the semantic bridge independently of simulator hit counts."""
import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from predicates import ROOT, DUT, extract, parse, evaluate, environment
from coverage import load, summary, join

class SemanticTests(unittest.TestCase):
    def test_predicates_match_priority_oracle_and_equivalent_forms(self):
        # Exhaust all relevant input bits (irrelevant opposite masks factored out).
        for target in extract():
            compact, expanded = map(parse, [target['compact'], target['expanded']])
            for reset, mask, opposite_nonzero in itertools.product(range(2), range(256), range(2)):
                req, over = (mask, opposite_nonzero) if target['kind'] == 'req' else (opposite_nonzero, mask)
                selected = over if over else req
                winner = ((selected & -selected).bit_length() - 1) if selected else -1
                expected = not reset and winner == target['index'] and ((over == 0) == (target['kind'] == 'req'))
                env = environment(reset, req, over)
                self.assertEqual(evaluate(compact, env), expected, target['id'])
                self.assertEqual(evaluate(expanded, env), expected, target['id'])

    def test_egg_has_real_classes_and_separate_winning_predicates(self):
        proc = subprocess.run([str(ROOT/'egraph/target/debug/rtl-predicate-egraph')],
                              input=json.dumps(extract()), text=True, capture_output=True, check=True)
        graph = json.loads(proc.stdout)
        self.assertEqual(len({t['eclass'] for t in graph['targets']}), 16)
        self.assertTrue(all(t['equivalent'] for t in graph['targets']))
        self.assertGreater(len(graph['eclasses']), 16)
        by_id = {c['id']:c for c in graph['eclasses']}
        self.assertTrue(any(len(c['nodes']) > 1 for c in graph['eclasses']))
        for c in graph['eclasses']:
            for n in c['nodes']:
                self.assertTrue(all(child in by_id for child in n['children']))

    def test_last_override_else_is_unreachable(self):
        for override in range(256):
            self.assertFalse(override != 0 and not any(override & (1 << i) for i in range(8)))

    def test_coverage_parser_excludes_tb_and_does_not_waive_zeroes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'sample.dat'
            p.write_text("# SystemC::Coverage-3\n" +
                "C '\x01f\x02examples/arbiter/rtl/fixed_priority_arbiter.sv\x01l\x0230\x01n\x0257\x01t\x02branch\x01o\x02cond_else\x01h\x02TOP.tb_fixed_priority_arbiter.dut' 0\n" +
                "C '\x01f\x02examples/arbiter/verif/tb_fixed_priority_arbiter.sv\x01l\x0210\x01t\x02line\x01h\x02TOP.tb_fixed_priority_arbiter' 999\n")
            points = load(p)
            self.assertEqual(summary(points)['branch'], {'covered':0,'total':1,'percent':0.0})
            with self.assertRaises(ValueError): join(extract(), {'targets':[]}, points)

    def test_checker_accepts_spec_conforming_control_and_rejects_each_defect(self):
        # Derived controls exist only in build/; benchmark source stays immutable.
        tb = ROOT/'examples/arbiter/verif/tb_fixed_priority_arbiter.sv'
        original = DUT.read_text()
        sync = original.replace('@(posedge clk or posedge reset)', '@(posedge clk)')
        fixed = sync.replace('grant <= priority_override;', "grant <= priority_override & (~priority_override + 8'd1);")
        variants = [('conforming',fixed,0,0), ('override_only',sync,63232,0),
                    ('reset_only',fixed.replace('@(posedge clk)', '@(posedge clk or posedge reset)'),0,1)]
        folder=ROOT/'build/checker-controls'
        folder.mkdir(parents=True,exist_ok=True)
        for name, rtl, functional, timing in variants:
            source=folder/f'{name}.sv'
            source.write_text(rtl)
            executable=folder/f'{name}.vvp'
            subprocess.run(['iverilog','-g2012','-s','tb_fixed_priority_arbiter','-o',str(executable),str(source),str(tb)],check=True,capture_output=True)
            proc=subprocess.run(['vvp',str(executable),'+COLLECT'],check=True,capture_output=True,text=True)
            (folder/f'{name}.log').write_text(proc.stdout)
            self.assertIn(f'functional_errors={functional} timing_errors={timing}',proc.stdout)
        # Default standalone mode must return failure for the original DUT.
        executable=folder/'original.vvp'
        subprocess.run(['iverilog','-g2012','-s','tb_fixed_priority_arbiter','-o',str(executable),str(DUT),str(tb)],check=True,capture_output=True)
        proc=subprocess.run(['vvp',str(executable)],capture_output=True,text=True)
        self.assertNotEqual(proc.returncode,0)
        self.assertIn('Specification violations detected',proc.stdout)

if __name__ == '__main__':
    unittest.main()
