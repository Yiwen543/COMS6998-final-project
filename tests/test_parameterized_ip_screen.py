import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from screen_parameterized_ip import extract_configured


class ParameterScreenTests(unittest.TestCase):
    def test_override_is_observed_in_elaboration_and_source_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            source=root/'probe.sv'
            content='module probe #(parameter N=2)(input clk, input [N-1:0] a, output reg q);\nalways @(posedge clk) if (a == 0) q <= 1; else q <= 0;\nendmodule\n'
            source.write_text(content)
            result,status=extract_configured([source],'probe',{'N':5},root/'out')
            self.assertEqual(status['verified_parameters'],{'N':5})
            self.assertEqual(source.read_text(),content)
            self.assertIn(str(source.resolve()), result['sources'])
            self.assertIn('wire width 5 input', (root/'out/preproc.il').read_text())

    def test_invalid_parameter_fields_rejected_before_shell_or_tool(self):
        with self.assertRaises(ValueError):
            extract_configured([],'probe',{'N;bad':2},Path('unused'))
        with self.assertRaises(ValueError):
            extract_configured([],'probe',{'N':'2'},Path('unused'))


if __name__=='__main__':
    unittest.main()
