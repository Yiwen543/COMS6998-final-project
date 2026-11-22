"""Controls for finite ECO obligations, branch-only differences and unknown outputs."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from m3_eco_replay import check_witness, evaluate_obligations, replace_one, replay, variants


class EcoReplayTests(unittest.TestCase):
    def test_single_omission_obligations(self):
        for bit in range(8):
            data = evaluate_obligations(f"omit_override_bit_{bit}")
            changed = {k for k, r in data["rules"].items() if r["status"] == "sat"}
            self.assertEqual(changed, {"override-nonzero", f"override_{bit}-activation"})
            for pos in range(8):
                # Only one override mask selects the missing bit in isolation.
                # The lowest asserted request bit fixes all lower positions.
                self.assertEqual(data["claims"][f"req_{pos}"]["differing_assignments"], 1 << (7 - pos))
                self.assertEqual(data["claims"][f"override_{pos}"]["differing_assignments"],
                                 256 if pos == bit else 0)
            self.assertEqual(data["rules"]["override-nonzero"]["differing_assignments"], 512)

    def test_equal_port_outputs_still_distinguish_branch(self):
        base = {"path": 8, "grant": 8, "valid": 1, "index": 3}
        changed = dict(base, path=3)
        check_witness("req_3", 0, changed, base, True, False)
        with self.assertRaisesRegex(ValueError, "RTL source/alternate witness disagreement"):
            check_witness("req_3", 0, base, base, True, False)

    @unittest.skipUnless(shutil.which("iverilog") and shutil.which("vvp"), "requires Icarus")
    def test_unknown_output_is_retained_and_rejected(self):
        rtl = replace_one(variants()["baseline"], "grant <= 8'b00000001;", "grant <= 8'bxxxxxxxx;")
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "unknown.log"
            with self.assertRaisesRegex(ValueError, "unknown physical pin"):
                replay(rtl, [(0, 1, 0)], log)
            self.assertIn("xxxxxxxx", log.read_text())
