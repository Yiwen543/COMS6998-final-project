"""Frozen FIFO pilot boundaries, real egg classes, and checker fault controls."""
import json
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fifo_feedback import (DUT, SOURCE, extract, render_messages, validate_actions)
from predicates import evaluate, parse
from run_fifo_pilot import INITIAL, parse_result


class FifoPilotTests(unittest.TestCase):
    def test_validation_and_state_boundary(self):
        actions = [dict(reset=0, push=1, pop=0, data=i) for i in range(8)]
        validate_actions({"actions": actions}, 8, INITIAL)
        with self.assertRaisesRegex(ValueError, "overflow"):
            validate_actions({"actions": actions + [dict(reset=0, push=1, pop=0, data=0)]}, 9, INITIAL)
        validate_actions({"actions": actions + [dict(reset=0, push=1, pop=1, data=255)]}, 9, INITIAL)
        with self.assertRaisesRegex(ValueError, "underflow"):
            validate_actions({"actions": [dict(reset=0, push=0, pop=1, data=0)]}, 1, INITIAL)
        with self.assertRaisesRegex(ValueError, "during reset"):
            validate_actions({"actions": [dict(reset=1, push=1, pop=0, data=0)]}, 1, INITIAL)
        with self.assertRaises(ValueError):
            validate_actions({"actions": [dict(reset=True, push=0, pop=0, data=0)]}, 1, INITIAL)

    def test_egg_semantics_and_isolation(self):
        targets = extract()
        engine = ROOT / "egraph/target/debug/rtl-predicate-egraph"
        if not engine.exists():
            self.skipTest("cargo build --locked --offline --manifest-path egraph/Cargo.toml first")
        graph = json.loads(subprocess.run([str(engine)], input=json.dumps(targets), capture_output=True,
                                          text=True, check=True).stdout)
        self.assertEqual(5, len({x["eclass"] for x in graph["targets"]}))
        self.assertTrue(all(x["equivalent"] for x in graph["targets"]))
        for push in (False, True):
            for pop in (False, True):
                env = {"push_i": push, "pop_i": pop, "msb_diff": False, "low_bits_equal": False}
                for t in targets[:4]:
                    self.assertEqual(evaluate(parse(t["compact"]), env),
                                     evaluate(parse(t["expanded"]), env))
                self.assertEqual(1, sum(evaluate(parse(t["compact"]), env) for t in targets[:4]))
        for msb in (False, True):
            for low in (False, True):
                env = {"push_i": False, "pop_i": False, "msb_diff": msb, "low_bits_equal": low}
                self.assertEqual(msb and low, evaluate(parse(targets[4]["compact"]), env))
                self.assertEqual(msb and low, evaluate(parse(targets[4]["expanded"]), env))
        points = []
        for t in targets:
            points.append({"source": SOURCE, "line": t["line"], "column": 1,
                           "type": t["counter_type"], "outcome": "full conjunction => 1" if t["id"] == "full_pointer_compare" else "case",
                           "hierarchy": "TOP.tb_sync_fifo.dut", "span": None, "hits": 0})
        points.append({"source": SOURCE, "line": 9, "column": 1, "type": "toggle",
                       "outcome": "push_data_i[0]:0->1", "hierarchy": "TOP.tb_sync_fifo.dut", "span": None, "hits": 0})
        checked = {"checks": 4, "functional_errors": 0}
        kwargs = (DUT.read_text(), [], checked, "RESULT checks=4", points, targets, graph, 32, 1)
        a, b, c = [json.loads(render_messages(arm, "spec", *kwargs)[1]["content"]) for arm in "ABC"]
        self.assertNotIn("raw_uncovered_dut_coverage", a)
        self.assertNotIn("egg_normalization", a)
        self.assertEqual(b["raw_uncovered_dut_coverage"], c["raw_uncovered_dut_coverage"])
        self.assertNotIn("egg_normalization", b)
        self.assertEqual(5, len(c["egg_normalization"]["mapped_uncovered"]))
        self.assertEqual(1, c["egg_normalization"]["unmapped_uncovered"]["count"])

    def test_checker_detects_independent_fault_controls(self):
        source = DUT.read_text()
        mutations = {
            "status": source.replace("assign full_o  = (wr_ptr_q[PTR_W]", "assign full_o  = 1'b1 || (wr_ptr_q[PTR_W]"),
            "data": source.replace("assign pop_data_o = fifo_pop_data;", "assign pop_data_o = '0;")}
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            for kind, rtl in mutations.items():
                self.assertNotEqual(source, rtl)
                path = folder / f"{kind}.sv"
                exe = folder / f"{kind}.vvp"
                path.write_text(rtl)
                subprocess.run(["iverilog", "-g2012", "-s", "tb_sync_fifo", "-o", str(exe),
                                str(path), str(ROOT / "examples/fifo/verif/tb_sync_fifo.sv")],
                               capture_output=True, text=True, check=True)
                log = subprocess.run(["vvp", str(exe), "+MODE=0", "+COLLECT"],
                                     capture_output=True, text=True, check=True).stdout
                result = parse_result(log)
                self.assertGreater(result[f"{kind}_errors"], 0)

    def test_mock_replay_and_cycle_accounting(self):
        base = json.loads((ROOT / "configs/fifo_pilot.json").read_text())
        base.update(repetitions=1, rounds=1)
        (ROOT / "build").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / "build", prefix="fifo-pilot-test-") as td:
            folder = Path(td)
            config = folder / "config.json"
            config.write_text(json.dumps(base))
            outputs = []
            for mode in ("mock", "replay"):
                out = folder / mode
                argv = [sys.executable, str(ROOT / "scripts/run_fifo_pilot.py"),
                        "--mode", mode, "--config", str(config), "--output", str(out)]
                if mode == "replay":
                    argv += ["--replay-calls", str(folder / "mock/calls.jsonl")]
                subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, check=True, timeout=120)
                with (out / "rounds.csv").open() as stream:
                    rows = list(csv.DictReader(stream))
                self.assertEqual(3, len(rows))
                self.assertTrue(all(int(row["cumulative_executed_cycles"]) == 36 for row in rows))
                self.assertTrue(all(int(row["cumulative_simulator_executions"]) == 1 for row in rows))
                self.assertTrue(all(row["cumulative_api_tokens"] == "" for row in rows))
                outputs.append(rows)
            for original, replayed in zip(*outputs):
                for field in ("arm", "toggle_covered", "branch_covered", "line_covered",
                              "expr_covered", "functional_bins_mask", "functional_failures"):
                    self.assertEqual(original[field], replayed[field])


if __name__ == "__main__":
    unittest.main()
