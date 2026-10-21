"""Timer fixture, feedback isolation, and checker mutation controls."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from coverage import load  # noqa: E402
from ttc_feedback import INITIAL, DUT, SPEC, extract, mapped_evidence, render_messages, validate_actions  # noqa: E402
from ttc_reference import actions as reference_actions  # noqa: E402
from run_ttc_pilot import parse_result  # noqa: E402


class TimerPilotTests(unittest.TestCase):
    def test_action_schema_and_exclusions(self):
        self.assertTrue(validate_actions({"actions": [dict(reset=0, write=1, read=0, addr=15, data=0xffffffff)]}, 1))
        for invalid in (
            dict(reset=0, write=1, read=1, addr=0, data=0),
            dict(reset=1, write=1, read=0, addr=0, data=0),
            dict(reset=0, write=0, read=0, addr=16, data=0),
            dict(reset=0, write=0, read=0, addr=0, data=-1),
            dict(reset=0, write=0, read=0, addr=0, data=True),
        ):
            with self.assertRaises(ValueError):
                validate_actions({"actions": [invalid]}, 1)

    def test_egg_feedback_isolation_and_guards(self):
        if not shutil.which("verilator"):
            self.skipTest("Verilator unavailable")
        targets = extract()
        result = subprocess.run([str(ROOT / "egraph/target/debug/rtl-predicate-egraph")],
                                input=json.dumps(targets), capture_output=True, text=True, check=True)
        graph = json.loads(result.stdout)
        roots = {t["id"]: t["eclass"] for t in graph["targets"]}
        self.assertTrue(all(t["equivalent"] for t in graph["targets"]))
        self.assertNotEqual(roots["irq_clear"], roots["read_status"])
        self.assertNotEqual(roots["interval_reload"], roots["irq_set"])
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            builddir = folder / "verilator-build"
            subprocess.run(["verilator", "-Wno-TIMESCALEMOD", "--cc", "--exe", "--build", "--timing",
                            "--assert", "--coverage-line", "--coverage-toggle", "--coverage-expr",
                            "--top-module", "tb_ttc_counter_lite", "--Mdir", str(builddir), "-j", "2",
                            str(DUT), str(ROOT / "examples/ttc_timer/verif/tb_ttc_counter_lite.sv"),
                            str(ROOT / "scripts/sim_main_ttc.cpp")], check=True, capture_output=True)
            cover = folder / "seed.dat"
            subprocess.run([str(builddir / "Vtb_ttc_counter_lite"), "+MODE=0", "+COLLECT",
                            f"+verilator+coverage+file+{cover}"], check=True, capture_output=True)
            points = load(cover, "examples/ttc_timer/rtl/ttc_counter_lite.sv")
        evidence = mapped_evidence(targets, graph, points)
        self.assertIsNotNone(evidence["shared_dependencies"]["addr_status"]["eclass"])
        messages = {arm: render_messages(arm, SPEC.read_text(), DUT.read_text(), [],
                    {"checks": 5, "read_errors": 0, "interrupt_errors": 0, "timing_errors": 0},
                    "RESULT checks=5", points, targets, graph, 16, 1) for arm in "ABC"}
        bodies = {arm: json.loads(m[1]["content"]) for arm, m in messages.items()}
        self.assertEqual(messages["A"][0], messages["B"][0])
        self.assertEqual(messages["B"][0], messages["C"][0])
        self.assertNotIn("raw_uncovered_dut_coverage", bodies["A"])
        self.assertEqual(bodies["B"]["raw_uncovered_dut_coverage"], bodies["C"]["raw_uncovered_dut_coverage"])
        self.assertNotIn("egg_normalization", bodies["B"])
        self.assertEqual(bodies["C"]["egg_normalization"], evidence)
        for arm in "ABC":
            self.assertEqual(bodies[arm]["initial_stimulus"], INITIAL)
            self.assertNotIn("reference_actions", messages[arm][1]["content"])

    def test_checker_detects_original_async_reset_and_accepts_sync_control(self):
        if not shutil.which("iverilog"):
            self.skipTest("Icarus unavailable")
        source = DUT.read_text()
        self.assertEqual(source.count("posedge clk or posedge reset"), 5)
        ceiling = reference_actions()
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            vectors = folder / "ceiling.vectors"
            vectors.write_text("".join(f"{a['reset']} {a['write']} {a['read']} {a['addr']:x} {a['data']:08x}\n"
                                       for a in ceiling))
            for label, rtl in (("original", source),
                               ("sync-control", source.replace("posedge clk or posedge reset", "posedge clk"))):
                file = folder / f"{label}.sv"
                file.write_text(rtl)
                output = folder / f"{label}.vvp"
                subprocess.run(["iverilog", "-g2012", "-s", "tb_ttc_counter_lite", "-o", str(output),
                                str(file), str(ROOT / "examples/ttc_timer/verif/tb_ttc_counter_lite.sv")], check=True)
                run = subprocess.run(["vvp", str(output), "+MODE=1", "+COLLECT", f"+VECTORS={vectors}"],
                                     capture_output=True, text=True, check=True)
                result = parse_result(run.stdout)
                self.assertEqual(result["checks"], len(INITIAL) + len(ceiling))
                self.assertEqual(result["read_errors"], 0)
                self.assertEqual(result["interrupt_errors"], 0)
                self.assertEqual(result["timing_errors"], 2 if label == "original" else 0)
