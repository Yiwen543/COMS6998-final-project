"""Independent FIFO checker, control RTL, and guard provenance checks."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_sfifo_fixed import DRIVER, SOURCE, compile_driver, simulate  # noqa: E402
from run_midterm_fixed import sha  # noqa: E402
from sfifo_fixture import check, schema, validate_actions  # noqa: E402


def action(**kwargs):
    return {"reset": 0, "wr": 0, "rd": 0, "data": 0} | kwargs


def directed():
    seed = json.loads((ROOT / "configs/sfifo_seed.json").read_text())["actions"]
    return (seed + [action(wr=1, data=i + 1) for i in range(8)] +
            [action(wr=1, data=99), action(wr=1, rd=1, data=88)] +
            [action(wr=1, rd=1, data=40 + i) for i in range(5)] +
            [action(rd=1) for _ in range(9)] +
            [action(wr=1, data=201), action(reset=1),
             action(wr=1, data=77), action(rd=1)])


class SfifoFixtureTests(unittest.TestCase):
    def test_schema_and_reset_boundary(self):
        actions = directed()
        self.assertEqual(validate_actions({"actions": actions}, 32), actions)
        self.assertEqual(schema()["properties"]["actions"]["type"], "array")
        for bad in (action(data=256), action(wr=True), action(extra=1),
                    action(reset=1, rd=1)):
            with self.assertRaises(ValueError):
                validate_actions({"actions": [action(reset=1), bad]}, 2)
        with self.assertRaises(ValueError):
            validate_actions({"actions": [action()]}, 1)

    def test_original_and_independent_control_pass_mutant_fails(self):
        actions = directed()
        with tempfile.TemporaryDirectory(dir=ROOT / "build") as temp:
            out = Path(temp)
            for label, source, define in (("original", SOURCE, None),
                                          ("reference", ROOT / "tests/rtl/sfifo_reference.sv", None),
                                          ("bad-data", ROOT / "tests/rtl/sfifo_reference.sv", "SFIFO_FAULT_DATA"),
                                          ("bad-reset", ROOT / "tests/rtl/sfifo_reference.sv", "SFIFO_FAULT_ASYNC_RESET")):
                folder = out / label
                folder.mkdir()
                binary = folder / "driver.vvp"
                cmd = ["iverilog", "-g2012", "-s", "tb_sfifo_fixed", "-o", str(binary)]
                if define:
                    cmd.append("-D" + define)
                subprocess.run([*cmd, str(source), str(DRIVER)], cwd=ROOT,
                               check=True, capture_output=True, text=True)
                result = simulate("iverilog", binary, actions, folder, source=source)
                if label == "bad-data":
                    self.assertIn("data_order", result["checker"]["distinct_defects"])
                elif label == "bad-reset":
                    self.assertTrue({"fill", "empty"} &
                                    set(result["checker"]["distinct_defects"]))
                else:
                    self.assertEqual(result["checker"]["distinct_defects"], [])

    def test_egg_groups_are_source_distinct_reachable_and_separate(self):
        screen = json.loads((ROOT / "results/midterm_candidate_preflight/external-sfifo/screen.json").read_text())
        self.assertEqual(sha(SOURCE), screen["source_sha256"])
        groups = screen["groups"]
        self.assertEqual(len(groups), 2)
        self.assertNotEqual(groups[0]["eclass_local"], groups[1]["eclass_local"])
        for group in groups:
            self.assertTrue(group["qualifies_preflight"])
            self.assertEqual(len({member["line"] for member in group["members"]}), 2)
            for member in group["members"]:
                self.assertEqual(member["seed_coverage"]["hits"], 0)
                self.assertGreater(member["calibration_coverage"]["hits"], 0)
        self.assertEqual({g["members"][0]["case_value"] for g in groups}, {"2'01", "2'10"})


if __name__ == "__main__":
    unittest.main()
