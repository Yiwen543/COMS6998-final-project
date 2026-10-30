"""Check B/C information isolation and original source counter identities."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from coverage import load  # noqa: E402
from run_sfifo_fixed import SOURCE  # noqa: E402
from sfifo_feedback import egg_feedback, messages_for  # noqa: E402


class SfifoFeedbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(dir=ROOT / "build")
        cls.run_dir = Path(cls.temp.name) / "mock"
        subprocess.run([sys.executable, "-B",
                        str(ROOT / "scripts/run_sfifo_bc_development.py"),
                        "--mode", "mock", "--output", str(cls.run_dir)],
                       cwd=ROOT, check=True, capture_output=True, text=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_b_and_c_share_raw_feedback_and_c_has_real_egg_evidence(self):
        data = self.run_dir
        semantic = json.loads((data / "C/semantic.json").read_text())
        result = json.loads((data / "B/seed.json").read_text())
        points = load(data / "B/seed.dat", str(SOURCE.relative_to(ROOT)), include_descendants=True)
        log = (data / "B/seed.sim.log").read_text()
        b = json.loads(messages_for("B", [], result, log, points, None, 1, 8)[1]["content"])
        c = json.loads(messages_for("C", [], result, log, points, semantic, 1, 8)[1]["content"])
        self.assertNotIn("egg_normalization", b)
        self.assertEqual(b, {key: value for key, value in c.items() if key != "egg_normalization"})
        self.assertEqual(len(c["egg_normalization"]["equivalent_uncovered_groups"]), 2)
        self.assertEqual(len({g["eclass"] for g in
                              c["egg_normalization"]["equivalent_uncovered_groups"]}), 2)
        self.assertTrue(c["egg_normalization"]["engine"].lower().find("egg") >= 0)
        self.assertNotIn("calibration", json.dumps(c).lower())
        self.assertNotIn("witness", json.dumps(c).lower())
        self.assertEqual({p["line"] for p in c["raw_uncovered_dut_coverage"]
                          if p["line"] in (90, 91, 156, 157)}, {90, 91, 156, 157})
        filled_points = load(data / "B/round1-attempt1.dat", str(SOURCE.relative_to(ROOT)),
                             include_descendants=True)
        self.assertEqual(egg_feedback(semantic, filled_points)["equivalent_uncovered_groups"], [])

    def test_mock_is_arm_blind_and_separate_from_live(self):
        calls = [json.loads(line) for line in
                 (self.run_dir / "calls.jsonl").read_text().splitlines()]
        b = [call for call in calls if call["arm"] == "B"]
        c = [call for call in calls if call["arm"] == "C"]
        self.assertEqual([item["actions"] for item in b], [item["actions"] for item in c])
        self.assertTrue(all(item["mode"] == "mock" and
                            item["usage"]["input_tokens"] is None for item in calls))


if __name__ == "__main__":
    unittest.main()
