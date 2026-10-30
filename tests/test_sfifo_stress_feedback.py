"""A/B/C information isolation and P's own-trajectory construction."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from coverage import load
from run_sfifo_stress_fixed import SOURCE
from sfifo_stress_feedback import messages_for
from token_placebo import match_placebo


class SfifoStressFeedbackTests(unittest.TestCase):
    def test_arm_information_and_placebo(self):
        folder = ROOT / "results/midterm_candidate_preflight/sfifo-stress"
        screen = json.loads((folder / "screen.json").read_text())
        semantic = json.loads((folder / "semantic.json").read_text())
        seed = json.loads((folder / "seed.json").read_text())
        points = load(folder / "seed.dat", str(SOURCE.relative_to(ROOT)), include_descendants=True)
        log = (folder / "seed.sim.log").read_text()
        own_history = [{"reset": 0, "wr": 1, "rd": 0, "data": 123}]
        a = json.loads(messages_for("A", own_history, seed, log, points, None, None, 2, 8)[1]["content"])
        b = json.loads(messages_for("B", own_history, seed, log, points, None, None, 2, 8)[1]["content"])
        c_messages = messages_for("C", own_history, seed, log, points, semantic, screen, 2, 8)
        c = json.loads(c_messages[1]["content"])
        self.assertNotIn("raw_uncovered_dut_coverage", a)
        self.assertNotIn("egg_normalization", a)
        self.assertIn("raw_uncovered_dut_coverage", b)
        self.assertNotIn("egg_normalization", b)
        self.assertEqual(b["raw_uncovered_dut_coverage"], c["raw_uncovered_dut_coverage"])
        self.assertEqual(c["previous_generated_actions"], own_history)
        self.assertEqual(len(c["egg_normalization"]["equivalent_uncovered_groups"]), 4)
        placebo, evidence = match_placebo(
            c_messages, lambda m: len(m[1]["content"]) + len(m[0]["content"]))
        p = json.loads(placebo[1]["content"])
        self.assertEqual(p["previous_generated_actions"], own_history)
        self.assertEqual(p["raw_uncovered_dut_coverage"], b["raw_uncovered_dut_coverage"])
        self.assertNotIn("egg_normalization", p)
        self.assertLessEqual(evidence["absolute_delta"], 2)
        self.assertNotIn("calibration", c_messages[1]["content"])
        self.assertNotIn("calibration", placebo[1]["content"])


if __name__ == "__main__":
    unittest.main()
