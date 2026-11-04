import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_minimal_c_ablation as runner
from analyze_minimal_c_ablation import summarize
from pilot_model import ModelResponseError


class Model:
    def __init__(self, responses):
        self.responses = iter(responses)

    def count_input_tokens(self, messages):
        return 12

    def generate(self, messages, context):
        value = next(self.responses)
        if isinstance(value, Exception):
            raise value
        return value


def response(valid=True):
    return {"requested_model": "mock", "returned_model": "mock", "response_id": "test",
            "usage": {"input_tokens": 12, "output_tokens": 3, "cached_input_tokens": 4,
                      "reasoning_output_tokens": 1}, "latency_seconds": .01,
            "parsed": {"actions": [{"reset": 0, "wr": 0, "rd": 0, "data": 0 if valid else 999}]}}


class MinimalRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)
        self.config = json.loads(runner.CONFIG.read_text())
        old = ROOT / "results/sfifo_prompt_ablation_live_20261103/B_compact/rep1"
        prior = json.loads((old / "seed.json").read_text())
        points = runner.points_for(old / "seed.dat")
        self.state = {"arm": "B_compact", "rep": 1, "folder": self.out,
            "prior": prior, "points": points, "denominator": {runner.point_id(p) for p in points},
            "history": [], "calls": [], "counts": [], "executions": 1, "cycles": 4,
            "scheduled_cycles": 4, "terminal": None, "active_seconds": 0, "sim_seconds": 0,
            "log": old / "seed.sim.log"}
        self.semantic = json.loads(runner.SEMANTIC.read_text())
        self.seed = json.loads(runner.SEED.read_text())["actions"]

    def tearDown(self):
        self.tmp.cleanup()

    def run_round(self, model, mode="mock"):
        with patch.object(runner, "simulate", return_value=self.state["prior"]), patch.object(runner, "points_for", return_value=self.state["points"]):
            return runner.one_round(self.state, model, Path("unused"), self.seed,
                self.semantic, self.config, self.out, 1, mode)

    def test_retry_counts_failed_usage_once_without_cached_double_count(self):
        row = self.run_round(Model([response(False), response(True)]))
        self.assertEqual((row["api_tokens"], row["model_calls"], row["failed_attempts"]), (30, 2, 1))
        self.assertEqual((row["executed_cycles"], row["simulator_executions"]), (9, 2))
        self.assertEqual(row["cached_input_tokens"], 8)

    def test_exhaustion_and_incomplete_response_usage_retained(self):
        failure = ModelResponseError("incomplete_response", response(False))
        row = self.run_round(Model([failure, failure]))
        self.assertEqual(row["status"], "no_valid_actions")
        self.assertEqual(row["api_tokens"], 30)
        self.assertEqual(row["executed_cycles"], 4)
        self.assertEqual(self.state["terminal"], "no_valid_actions")
        runner.write(self.out / "metadata.json", {"mode": "mock", "limits": self.config})
        summary, _ = summarize(self.out)
        self.assertEqual(len(summary["sessions"]), 12)
        self.assertEqual(summary["arms"]["B_compact"]["not_reached"], 3)
        self.assertEqual(summary["generation_calls"], 2)

    def test_unknown_timeout_usage_is_not_invented(self):
        row = self.run_round(Model([TimeoutError(), TimeoutError()]))
        self.assertEqual(row["calls_with_unknown_usage"], 2)
        self.assertEqual(row["failed_attempts"], 2)
        self.assertEqual(row["simulator_executions"], 1)

    def test_count_failure_has_ledger_and_no_generation(self):
        model = Model([])
        model.count_input_tokens = lambda m: (_ for _ in ()).throw(TimeoutError())
        row = self.run_round(model, "live")
        self.assertEqual(row["status"], "prompt_count_failed")
        self.assertEqual(row["model_calls"], 0)
        self.assertEqual(row["token_count_requests"], 1)
        self.assertFalse(self.state["counts"][0]["ok"])

    def test_checker_failure_is_valid_dut_evidence(self):
        self.state["prior"] = copy.deepcopy(self.state["prior"])
        self.state["prior"]["checker"]["failures"] = [{"kind": "deliberate_test_control"}]
        row = self.run_round(Model([response(True)]))
        self.assertEqual(row["status"], "ok")
        self.assertEqual(len(row["checker"]["failures"]), 1)

    def test_schedule_and_all_four_own_trajectory_prompts(self):
        order = runner.schedule(self.config)
        self.assertEqual(len(order), 72)
        self.assertEqual(len(set(order)), 72)
        self.assertEqual(order[:4], [(a, 1, 1) for a in runner.ARMS])
        self.assertEqual(order[4][0], "C_full")
        for arm in runner.ARMS:
            value = runner.prompt_for(arm, self.state, self.semantic, 1, self.config)
            payload = json.loads(value[1]["content"])
            self.assertEqual("egg_normalization" in payload, arm != "B_compact")


if __name__ == "__main__":
    unittest.main()
