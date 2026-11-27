"""Candidate monitoring keeps arbitrary expressions out of SV and tool failures out of scores."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_fifo_loop_rtl import bmc, candidate_assertions, sample_states


class FifoLoopRtlTests(unittest.TestCase):
    def test_rejects_unbound_terms_and_preserves_duplicate_names(self):
        _, sv = candidate_assertions(["active", "(or active active)"])
        self.assertIn("check_0: assert", sv)
        self.assertIn("check_1: assert", sv)
        for bad in [[], ["(or active)"], ["active); $finish;"], ["m_axis_tready"]]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                candidate_assertions(bad)

    def test_unknown_and_missing_samples_rejected(self):
        vcd = ("$var integer 32 t smt_step $end\n$scope module fifo_stall_formal $end\n"
               "$var wire 5 n7 loop_sample $end\n$upscope $end\n$enddefinitions $end\n"
               "#0\nb0 t\nb10100 n7\n#10\nb1 t\nb10101 n7\n")
        self.assertTrue(sample_states(vcd, 1)[1]["user_changed"])
        with self.assertRaisesRegex(ValueError, "incomplete sampled atoms"):
            sample_states(vcd.replace("10101", "1010x"), 1)
        with self.assertRaisesRegex(ValueError, "incomplete sampled atoms"):
            sample_states(vcd, 2)

    def test_solver_error_never_becomes_formal_counterexample(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            broken = subprocess.CompletedProcess([], 1, "Solver terminated unexpectedly\nStatus: FAILED\n")
            with patch("egg_fifo_loop_rtl.subprocess.run", return_value=broken):
                with self.assertRaisesRegex(RuntimeError, "Inconclusive BMC"):
                    bmc(folder, folder, "original", ["active"])
            self.assertIn("unexpectedly", (folder / "smtbmc.log").read_text())


if __name__ == "__main__":
    unittest.main()
