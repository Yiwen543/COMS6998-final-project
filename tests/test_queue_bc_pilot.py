"""Queue contract, checker controls, feedback isolation, and replay accounting."""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from queue_feedback import CHECKER, INITIAL, VERSIONS, render_messages, validate_actions  # noqa: E402
from queue_reference import actions as reference_actions  # noqa: E402
from run_queue_bc_pilot import parse_result  # noqa: E402
from typed_predicates import extract  # noqa: E402


class QueuePilotTests(unittest.TestCase):
    def test_stimulus_schema_and_occupancy_boundary(self):
        def a(**changes):
            action = dict(reset_n=1, clear=0, enable=1, write=0, read=0, data=0)
            action.update(changes)
            return action

        full = [a(write=1, data=i + 1) for i in range(3)]
        validate_actions({"actions": full}, 3)
        with self.assertRaisesRegex(ValueError, "illegal write-only"):
            validate_actions({"actions": [a(write=1)]}, 1, full)
        with self.assertRaisesRegex(ValueError, "illegal read-only"):
            validate_actions({"actions": [a(read=1)]}, 1)
        validate_actions({"actions": [a(write=1, read=1)]}, 1, full)
        validate_actions({"actions": [a(write=1, read=1)]}, 1)
        validate_actions({"actions": [a(enable=0, write=1, read=1)]}, 1)
        validate_actions({"actions": [a(clear=1), a(write=1)]}, 2, full)
        for bad in (a(data=2**32), a(write=True), a(unknown=1)):
            with self.assertRaises(ValueError):
                validate_actions({"actions": [bad]}, 1)
        with self.assertRaises(ValueError):
            validate_actions({"actions": [a(), a()]}, 1)

    def test_feedback_isolation_and_full_guard_mapping(self):
        engine = ROOT / "build/queue-cargo/debug/rtl-predicate-egraph"
        subprocess.run(["cargo", "build", "--locked", "--offline", "--manifest-path",
                        "egraph/Cargo.toml", "--target-dir", "build/queue-cargo"],
                       cwd=ROOT, capture_output=True, text=True, check=True)
        source, top = VERSIONS["original"]
        extraction = extract(source, top)
        targets = extraction["targets"]
        payload = [{"id": row["id"], "compact": row["compact"],
                    "expanded": row["compact"]} for row in targets]
        graph = json.loads(subprocess.run([str(engine)], input=json.dumps(payload),
                                          capture_output=True, text=True, check=True).stdout)
        selected = [row for row in targets if row["guard_depth"] == 4 and
                    row["case_value"] in ("2'01", "2'10")]
        points = [{"source": str(source.relative_to(ROOT)), "line": row["line"],
                   "column": 1, "type": "line", "outcome": "case", "hits": 0,
                   "hierarchy": "TOP.tb_queue_pilot.dut", "span": None} for row in selected]
        points.append({"source": str(source.relative_to(ROOT)), "line": 1,
                       "column": 1, "type": "line", "outcome": "", "hits": 0,
                       "hierarchy": "TOP.tb_queue_pilot.dut", "span": None})
        checker = {key: 0 for key in ("data_errors", "occupancy_errors", "reset_errors",
                                     "clear_errors", "enable_errors")}
        checker["checks"] = len(INITIAL)
        inputs = (source, [], checker, "RESULT checks=6", points, targets, graph,
                  extraction["atoms"], 4, 1, targets)
        b, c = [render_messages(arm, *inputs) for arm in ("B", "C")]
        self.assertEqual(b[0], c[0])
        b_data, c_data = [json.loads(row[1]["content"]) for row in (b, c)]
        self.assertEqual(b_data, {key: val for key, val in c_data.items()
                                  if key != "egg_normalization"})
        groups = c_data["egg_normalization"]["groups"]
        self.assertEqual([6, 6], sorted(len(group["members"]) for group in groups))
        self.assertEqual({"2'01", "2'10"},
                         {group["members"][0]["case_value"] for group in groups})
        self.assertEqual(1, c_data["egg_normalization"]["unmapped_uncovered_locations"])
        self.assertEqual(13, len(b_data["raw_uncovered_dut_coverage"]))
        self.assertEqual(12, sum(point.get("raw_predicate") is not None for point in
                                 b_data["raw_uncovered_dut_coverage"]))
        self.assertNotIn("witness", json.dumps(c_data).lower())

    def test_checker_detects_independent_fault_controls(self):
        source = (ROOT / "examples/heldout_queue/verif/queue_spec_control.sv").read_text()
        mutations = {
            "data_errors": ("assign q_o = data[0];", "assign q_o = '0;"),
            "fallthrough": ("if (count == 0) data[0] <= d_i;",
                            "if (count == 0) data[0] <= '0;"),
            "occupancy_errors": ("assign empty_o = count == 0;", "assign empty_o = 1'b1;"),
            "reset_errors": ("always @(posedge clk_i or negedge rst_ni)", "always @(posedge clk_i)"),
            "clear_errors": ("end else if (clr_i) begin", "end else if (1'b0 && clr_i) begin"),
            "enable_errors": ("end else if (ena_i) begin", "end else begin"),
        }
        with tempfile.TemporaryDirectory(prefix="queue-check-") as directory:
            folder = Path(directory)
            vector = folder / "actions.txt"
            vector.write_text("".join(
                f"{a['reset_n']} {a['clear']} {a['enable']} {a['write']} {a['read']} {a['data']:08x}\n"
                for a in reference_actions()))
            for defect, (old, new) in mutations.items():
                self.assertIn(old, source)
                rtl = folder / f"{defect}.sv"
                binary = folder / f"{defect}.vvp"
                rtl.write_text(source.replace(old, new, 1))
                subprocess.run(["iverilog", "-g2012", "-s", "tb_queue_pilot",
                                "-DDUT_MODULE=queue_spec_control", "-o", str(binary),
                                str(rtl), str(CHECKER)], capture_output=True,
                               text=True, check=True)
                proc = subprocess.run(["vvp", str(binary), "+MODE=1", "+COLLECT",
                                       f"+VECTORS={vector}"], capture_output=True,
                                      text=True, check=True)
                observed = parse_result(proc.stdout)
                self.assertGreater(observed["data_errors" if defect == "fallthrough" else defect], 0, defect)

    def test_mock_replay_and_cycle_accounting(self):
        config = json.loads((ROOT / "configs/queue_bc_pilot.json").read_text())
        config.update(repetitions=1, rounds=1)
        (ROOT / "build").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / "build", prefix="queue-pilot-") as directory:
            folder = Path(directory)
            config_path = folder / "config.json"
            config_path.write_text(json.dumps(config))
            tables = []
            for mode in ("mock", "replay"):
                out = folder / mode
                argv = [sys.executable, "-B", str(ROOT / "scripts/run_queue_bc_pilot.py"),
                        "--mode", mode, "--config", str(config_path), "--output", str(out)]
                if mode == "replay":
                    argv += ["--replay-calls", str(folder / "mock/calls.jsonl")]
                subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                               check=True, timeout=180)
                with (out / "rounds.csv").open() as stream:
                    rows = list(csv.DictReader(stream))
                self.assertEqual(4, len(rows))
                self.assertTrue(all(int(row["cumulative_executed_cycles"]) == 10 for row in rows))
                self.assertTrue(all(int(row["cumulative_simulator_executions"]) == 1 for row in rows))
                self.assertTrue(all(row["cumulative_api_tokens"] == "" for row in rows))
                tables.append(rows)
            for first, second in zip(*tables):
                for field in ("version", "arm", "line_covered", "branch_covered",
                              "toggle_covered", "expr_covered", "functional_failures"):
                    self.assertEqual(first[field], second[field])


if __name__ == "__main__":
    unittest.main()
