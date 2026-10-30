"""Depth-16 public-I/O FIFO contract and late source guard controls."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_sfifo_stress_fixed import DRIVER, ORIGINAL, SOURCE, simulate
from sfifo_fixture import validate_actions


def action(**kwargs):
    return {"reset": 0, "wr": 0, "rd": 0, "data": 0} | kwargs


class SfifoStressFixtureTests(unittest.TestCase):
    def test_original_variant_reference_pass_and_fault_control_fails(self):
        seed = json.loads((ROOT / "configs/sfifo_stress_seed.json").read_text())["actions"]
        actions = (seed + [action(wr=1, data=i + 1) for i in range(16)] +
                   [action(wr=1, data=99), action(wr=1, rd=1, data=77)] +
                   [action(rd=1) for _ in range(18)] +
                   [action(wr=1, data=55), action(reset=1)])
        validate_actions({"actions": actions}, len(actions))
        with tempfile.TemporaryDirectory(dir=ROOT / "build") as tmp:
            for label, source, define in (
                ("original", ORIGINAL, None), ("variant", SOURCE, None),
                ("reference", ROOT / "tests/rtl/sfifo_reference.sv", None),
                ("fault-data", ROOT / "tests/rtl/sfifo_reference.sv", "SFIFO_FAULT_DATA")):
                folder = Path(tmp) / label
                folder.mkdir()
                binary = folder / "driver.vvp"
                command = ["iverilog", "-g2012", "-s", "tb_sfifo_stress_fixed", "-o", str(binary)]
                if define:
                    command.append("-D" + define)
                subprocess.run([*command, str(source), str(DRIVER)], cwd=ROOT,
                               text=True, capture_output=True, check=True)
                result = simulate("iverilog", binary, actions, folder, "directed", source)
                defects = result["checker"]["distinct_defects"]
                if label == "fault-data":
                    self.assertIn("data_order", defects)
                else:
                    self.assertEqual(defects, [], label)

    def test_late_groups_have_independent_source_counters(self):
        screen = json.loads((ROOT / "results/midterm_candidate_preflight/sfifo-stress/screen.json").read_text())
        self.assertEqual(screen["qualifying_groups"], 4)
        late = [group for group in screen["groups"] if group["late_guard"]]
        self.assertEqual(len(late), 2)
        self.assertEqual({tuple(m["line"] for m in group["members"]) for group in late},
                         {(91, 161), (96, 179)})
        for group in late:
            self.assertEqual(group["z3_pair_checks"], 1)
            self.assertEqual(len({(m["line"], m["seed_coverage"]["column"])
                                  for m in group["members"]}), 2)
            for member in group["members"]:
                self.assertEqual(member["seed_coverage"]["type"], "branch")
                self.assertEqual(member["seed_coverage"]["outcome"], "if")
                self.assertEqual(member["seed_coverage"]["hits"], 0)
                self.assertGreater(member["calibration_coverage"]["hits"], 0)


if __name__ == "__main__":
    unittest.main()
