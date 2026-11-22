"""The guard certifier must reject changed reset and priority conditions."""
import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from m3_guard_inputs import certify, oracle


@unittest.skipUnless(shutil.which("z3"), "needs the Z3 command-line solver")
class GuardCertificates(unittest.TestCase):
    def test_sat_counterexamples_block_publication(self):
        mutations = [
            ("missing-reset", "(and (not override_any) req0)", oracle("req", 0)),
            ("missing-priority", "(and (not reset) override2)", oracle("override", 2)),
        ]
        for check in mutations:
            with self.subTest(name=check[0]), self.assertRaisesRegex(ValueError, ": sat$"):
                certify([check], "z3")
