"""Source binding, exact solver selection and an independently evaluated SAT model."""
import importlib.util
from pathlib import Path
import shutil
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from m3_eco_formal import certify_eco, detector_table
from m3_eco_replay import DETECTOR, variants
from m3_guard_inputs import profiles
from predicates import environment, evaluate, parse


@unittest.skipUnless(shutil.which("yosys") and importlib.util.find_spec("z3"),
                     "needs Yosys and the z3-solver Python package")
class EcoFormalTests(unittest.TestCase):
    def test_source_detector_and_counterexample(self):
        source = variants()["omit_override_bit_7"]
        table = detector_table(source)
        self.assertEqual(tuple(bool(i & 0x7f) for i in range(256)), table)
        reports = certify_eco(table, rule_names=[], claim_names=["override_7", "override_0"])
        self.assertEqual(reports["rules"], {})
        self.assertEqual(reports["claims"]["override_0"], {"status": "unsat", "witness": None})
        self.assertEqual(reports["claims"]["override_7"]["status"], "sat")
        trace = reports["claims"]["override_7"]["witness"]
        env = environment(trace["reset"], trace["req"], trace["priority_override"])
        env["override_any"] = table[trace["priority_override"]]
        targets, _, _ = profiles()
        values = [evaluate(parse(t["compact"]), env) for t in targets if t["source_target"] == "override_7"]
        self.assertEqual(values, [False, True])

    def test_unlisted_logic_and_request_dependency_are_rejected(self):
        source = variants()["baseline"]
        # An edit to priority order invalidates the fixed source map.
        with self.assertRaisesRegex(ValueError, "outside the reviewed"):
            detector_table(source.replace("else if (req[0])", "else if (req[7])"))
        # Override zero leaves req[0] unknown. No guessed mask may stand in for it.
        with self.assertRaisesRegex(ValueError, "override alone"):
            detector_table(source.replace(DETECTOR, f"({DETECTOR}) || req[0]"))

    def test_selective_run_invokes_only_requested_queries(self):
        import z3
        table = detector_table(variants()["equivalent_reduction_or"])
        with patch.object(z3.Solver, "check", autospec=True, side_effect=z3.Solver.check) as checks:
            self.assertEqual(certify_eco(table, rule_names=[], claim_names=[]),
                             {"rules": {}, "claims": {}})
            self.assertEqual(checks.call_count, 0)
            data = certify_eco(table, rule_names=["override-nonzero"], claim_names=["req_4"])
            self.assertEqual(data["rules"]["override-nonzero"]["status"], "unsat")
            self.assertEqual(data["claims"]["req_4"]["status"], "unsat")
            self.assertEqual(checks.call_count, 2)
        with self.assertRaisesRegex(ValueError, "Unknown or duplicate"):
            certify_eco(table, claim_names=["req_8"])


if __name__ == "__main__":
    unittest.main()
