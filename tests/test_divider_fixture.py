"""Arithmetic checker controls, source mapping, and feedback isolation."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from coverage import load  # noqa: E402
from divider_feedback import egg_feedback, messages_for  # noqa: E402
from divider_fixture import schema, validate_actions  # noqa: E402
from run_divider_fixed import DRIVER, SOURCE, simulate  # noqa: E402
from run_midterm_fixed import sha  # noqa: E402


def action(**kwargs):
    return {"rst_n": 1, "start": 0, "dividend": 37, "divisor": 6} | kwargs


def directed():
    seed = json.loads((ROOT / "configs/divider_seed.json").read_text())["actions"]
    return seed + [action(start=1)] + [action() for _ in range(8)] + [
        action(start=1, dividend=0, divisor=0), action(dividend=0, divisor=0),
        action(start=1, dividend=91, divisor=13), action(rst_n=0, start=0)]


class DividerFixtureTests(unittest.TestCase):
    def test_schema_and_independent_arithmetic_controls(self):
        actions = directed()
        self.assertEqual(validate_actions({"actions": actions}, len(actions)), actions)
        self.assertEqual(schema()["properties"]["actions"]["type"], "array")
        for bad in (action(dividend=256), action(start=True), action(extra=1),
                    action(rst_n=0, start=1)):
            with self.assertRaises(ValueError):
                validate_actions({"actions": [action(rst_n=0), bad]}, 2)
        (ROOT / "build").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / "build") as temp:
            for label, source, define in (
                ("reference", ROOT / "tests/rtl/divider_reference.sv", None),
                ("fault", ROOT / "tests/rtl/divider_reference.sv", "DIVIDER_FAULT_REMAINDER"),
                ("original", SOURCE, None)):
                folder = Path(temp) / label
                folder.mkdir()
                binary = folder / "driver.vvp"
                cmd = ["iverilog", "-g2012", "-s", "tb_divider_fixed", "-o", str(binary)]
                if define:
                    cmd.append("-D" + define)
                subprocess.run([*cmd, str(source), str(DRIVER)], cwd=ROOT,
                               check=True, capture_output=True, text=True)
                result = simulate("iverilog", binary, actions, folder, source=source)
                if label == "reference":
                    self.assertEqual(result["checker"]["distinct_defects"], [])
                else:
                    self.assertIn("remainder", result["checker"]["distinct_defects"])

    def test_five_groups_mapped_with_complete_guards_and_isolation(self):
        screen = json.loads((ROOT / "results/midterm_candidate_preflight/divider-next/screen.json").read_text())
        semantic = json.loads((ROOT / "results/midterm_candidate_preflight/divider-next/semantic.json").read_text())
        self.assertEqual(sha(SOURCE), screen["source_sha256"])
        self.assertEqual(screen["qualifying_groups"], 5)
        self.assertEqual(len({g["eclass_local"] for g in screen["groups"]}), 5)
        points = load(ROOT / "results/midterm_candidate_preflight/divider-next/seed.dat",
                      str(SOURCE.relative_to(ROOT)), include_descendants=True)
        enriched = egg_feedback(semantic, screen, points)
        self.assertEqual(len(enriched["equivalent_uncovered_groups"]), 5)
        self.assertIn("posedge", json.dumps(enriched))
        for group in enriched["equivalent_uncovered_groups"]:
            self.assertGreaterEqual(len(group["members"]), 2)
            self.assertTrue(all(member["hits"] == 0 for member in group["members"]))
        result = json.loads((ROOT / "results/midterm_candidate_preflight/divider-next/seed.json").read_text())
        log = (ROOT / "results/midterm_candidate_preflight/divider-next/seed.sim.log").read_text()
        payloads = {arm: json.loads(messages_for(arm, [], result, log, points, semantic, screen, 1, 8)[1]["content"])
                    for arm in ("A", "B", "P", "C")}
        self.assertNotIn("raw_uncovered_dut_coverage", payloads["A"])
        self.assertNotIn("egg_normalization", payloads["B"])
        self.assertEqual(payloads["B"]["raw_uncovered_dut_coverage"],
                         payloads["C"]["raw_uncovered_dut_coverage"])
        self.assertEqual(payloads["B"]["raw_uncovered_dut_coverage"],
                         payloads["P"]["raw_uncovered_dut_coverage"])
        self.assertEqual({k: v for k, v in payloads["C"].items() if k != "egg_normalization"},
                         payloads["B"])
        placebo = payloads["P"]["neutral_length_matched_appendix"]
        self.assertEqual(len(placebo.encode()),
                         len(json.dumps(payloads["C"]["egg_normalization"], sort_keys=True).encode()))
        self.assertNotIn("eclass", placebo.lower())
        self.assertNotIn("guard", placebo.lower())
        self.assertNotIn("calibration", json.dumps(payloads).lower())


if __name__ == "__main__":
    unittest.main()
