"""Pilot isolation, schema, adapter and semantic accounting checks."""
import json
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from coverage import load, summary
from pilot_feedback import feedback_parts, render_messages, raw_coverage, egg_enrichment
from pilot_model import OpenAIModel, ModelResponseError, MockModel, usage_record, validate_actions
from predicates import extract, parse, evaluate
from run_pilot import target_costs


class PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rtl = (ROOT / "examples/arbiter/rtl/fixed_priority_arbiter.sv").read_text()
        cls.spec = (ROOT / "examples/arbiter/docs/specification.md").read_text()
        cls.points = load(ROOT / "results/step1/initial.dat")
        cls.targets = extract()
        cls.graph = json.loads((ROOT / "results/step1/egraph.json").read_text())
        cls.checker = {"checks": 4, "functional_errors": 0, "timing_errors": 0}

    def messages(self, arm):
        return render_messages(arm, self.spec, self.rtl, [], self.checker,
                               "RESULT checks=4 functional_errors=0 timing_errors=0",
                               self.points, self.targets, self.graph, 32, 1)

    def test_feedback_isolation_and_raw_identity(self):
        a, b, c = (feedback_parts(self.messages(arm)) for arm in "ABC")
        self.assertEqual(self.messages("A")[0], self.messages("B")[0])
        self.assertEqual(self.messages("B")[0], self.messages("C")[0])
        self.assertNotIn("raw_uncovered_dut_coverage", a)
        self.assertNotIn("egg_normalization", a)
        self.assertNotIn("egg_normalization", b)
        self.assertEqual(b["raw_uncovered_dut_coverage"], c["raw_uncovered_dut_coverage"])
        self.assertEqual(len(b["raw_uncovered_dut_coverage"]), sum(p["hits"] == 0 for p in self.points))
        self.assertNotIn("suggested_stimulus", json.dumps(c))
        self.assertNotIn("targeted-vectors", json.dumps(c))
        self.assertNotIn("exhaustive", json.dumps(c).lower())

    def test_egg_preserves_mapping_and_separate_winner_cases(self):
        enrichment = egg_enrichment(self.targets, self.graph, self.points)
        self.assertEqual(enrichment["semantics"].split()[0], "Pure")
        self.assertGreater(len(enrichment["unmapped_uncovered"]), 0)
        self.assertTrue(all(row["bit_width"] == 1 and row["semantics"] == "two_state"
                            for row in enrichment["mapped_uncovered"]))
        classes = {row["target"]: row["eclass"] for row in enrichment["mapped_uncovered"]}
        self.assertNotEqual(classes["req_1"], classes["override_1"])
        self.assertNotEqual(classes["req_1"], classes["req_2"])
        self.assertEqual(summary(self.points)["branch"]["total"], 18)
        self.assertEqual(len(raw_coverage(self.points, self.rtl)), sum(p["hits"] == 0 for p in self.points))

    def test_each_rewrite_rule_is_binary_boolean_sound(self):
        pairs = [
            ("(not (or a b))", "(and (not a) (not b))"),
            ("(not (and a b))", "(or (not a) (not b))"),
            ("(not (not a))", "a"),
            ("(and a true)", "a"),
            ("(and true a)", "a"),
            ("(not false)", "true"),
        ]
        for left, right in pairs:
            for a in (False, True):
                for b in (False, True):
                    env = {"a": a, "b": b}
                    self.assertEqual(evaluate(parse(left), env), evaluate(parse(right), env))

    def test_target_costs_preserve_not_reached(self):
        rows = [{"arm": "A", "repetition": 1, "round": 1, "branch_covered": 4,
                 "cumulative_api_tokens": 100, "cumulative_executed_cycles": 8,
                 "cumulative_simulator_executions": 1, "cumulative_total_wall_seconds": 1.0},
                {"arm": "A", "repetition": 1, "round": 2, "branch_covered": 5,
                 "cumulative_api_tokens": 200, "cumulative_executed_cycles": 20,
                 "cumulative_simulator_executions": 2, "cumulative_total_wall_seconds": 2.0}]
        costs = target_costs(rows, {"arms": ["A"], "repetitions": 1, "target_branch_points": 17})
        self.assertEqual(costs[0]["status"], "not reached")
        self.assertIsNone(costs[0]["first_target_round"])
        self.assertEqual(costs[0]["executed_cycles_at_stop"], 20)

    def test_action_schema_rejects_coercion_and_width_errors(self):
        good = {"actions": [{"reset": 0, "req": 255, "priority_override": 0}]}
        self.assertEqual(validate_actions(good, 32), good["actions"])
        bad = [{"actions": []}, {"actions": [{"reset": True, "req": 0, "priority_override": 0}]},
               {"actions": [{"reset": 0, "req": 256, "priority_override": 0}]},
               {"actions": [{"reset": 0, "req": 0, "priority_override": 0, "extra": 1}]},
               {"actions": good["actions"] * 33}]
        for item in bad:
            with self.assertRaises(ValueError):
                validate_actions(item, 32)

    def test_mock_is_arm_blind_and_tokens_are_not_invented(self):
        mock = MockModel({"seed": 6998, "max_new_cycles": 32})
        left = mock.generate(self.messages("A"), {"arm": "A", "repetition": 1, "round": 1})
        right = mock.generate(self.messages("C"), {"arm": "C", "repetition": 1, "round": 1})
        self.assertEqual(left["parsed"], right["parsed"])
        self.assertIsNone(left["usage"]["total_tokens"])

    def test_openai_adapter_request_and_usage_accounting_without_network(self):
        class Response:
            model = "gpt-6.1-sol"
            id = "resp_test"
            status = "completed"
            incomplete_details = None
            output_text = '{"actions":[{"reset":0,"req":1,"priority_override":0}]}'
            usage = {"input_tokens": 100, "output_tokens": 40, "total_tokens": 140,
                     "input_tokens_details": {"cached_tokens": 20},
                     "output_tokens_details": {"reasoning_tokens": 15}}
        class Client:
            def __init__(self):
                self.kwargs = None
                self.responses = self
            def create(self, **kwargs):
                self.kwargs = kwargs
                return Response()
        model = OpenAIModel.__new__(OpenAIModel)
        model.config = {"model": "gpt-6.1-sol", "max_output_tokens": 4096, "reasoning_effort": "low"}
        model.client = Client()
        result = model.generate(self.messages("A"), {})
        self.assertEqual(result["usage"]["total_tokens"], 140)
        self.assertEqual(result["usage"]["cached_input_tokens"], 20)
        self.assertEqual(result["usage"]["reasoning_output_tokens"], 15)
        self.assertEqual(model.client.kwargs["model"], "gpt-6.1-sol")
        self.assertFalse(model.client.kwargs["store"])
        self.assertEqual(model.client.kwargs["text"]["format"]["type"], "json_schema")
        Response.model = "unexpected-model"
        with self.assertRaises(ModelResponseError):
            model.generate(self.messages("A"), {})

    def test_runner_mock_and_replay_accounting(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            config = json.loads((ROOT / "configs/arbiter_pilot.json").read_text())
            config.update(repetitions=1, rounds=2, max_new_cycles=3)
            path = folder / "config.json"
            path.write_text(json.dumps(config))
            mock, replay = folder / "mock", folder / "replay"
            for mode, output, extra in (("mock", mock, []),
                                        ("replay", replay, ["--replay-calls", str(mock / "calls.jsonl")])):
                subprocess.run([sys.executable, str(ROOT / "scripts/run_pilot.py"),
                                "--mode", mode, "--config", str(path), "--output", str(output), *extra],
                               cwd=ROOT, check=True, capture_output=True, text=True, timeout=90)
            def rows(folder):
                with (folder / "rounds.csv").open() as stream:
                    return list(csv.DictReader(stream))
            first, second = rows(mock), rows(replay)
            self.assertEqual(len(first), 6)
            self.assertEqual(len(second), 6)
            for rows_ in (first, second):
                for arm in "ABC":
                    arm_rows = [r for r in rows_ if r["arm"] == arm]
                    self.assertEqual([int(r["cumulative_executed_cycles"]) for r in arm_rows], [7, 17])
                    self.assertEqual([int(r["cumulative_simulator_executions"]) for r in arm_rows], [1, 2])
                    self.assertTrue(all(r["branch_total"] == "18" for r in arm_rows))
                    self.assertTrue(all(not r["cumulative_api_tokens"] for r in arm_rows))
            self.assertEqual([[r["branch_covered"] for r in first if r["arm"] == a] for a in "ABC"],
                             [[r["branch_covered"] for r in second if r["arm"] == a] for a in "ABC"])
            self.assertEqual(json.loads((replay / "metadata.json").read_text())["evidence_mode"], "mock")


if __name__ == "__main__":
    unittest.main()
