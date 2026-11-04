import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_txuart_b_development import evaluate_gate, group_hits, messages


class TxuartDevelopmentTests(unittest.TestCase):
    def test_prompt_has_raw_feedback_but_no_calibration(self):
        seed = json.loads((ROOT / "configs/txuart_seed.json").read_text())["actions"]
        prior = {"checker": {"checks": 4, "distinct_defects": [], "failures": []}}
        rendered = messages(seed, [], prior, "", [], 1, 16)
        payload = json.loads(rendered[1]["content"])
        self.assertIn("raw_uncovered_dut_coverage", payload)
        self.assertNotIn("egraph", rendered[1]["content"].lower())
        self.assertNotIn("calibration", rendered[1]["content"].lower())
        self.assertNotIn("target_groups", rendered[1]["content"].lower())

    def test_gate_uses_fixed_first_round_and_later_progress(self):
        config = json.loads((ROOT / "configs/txuart_b_development.json").read_text())
        screen = {"qualifying_groups": 5}
        rows = []
        for rep in range(1, 4):
            rows.append({"repetition": rep, "round": 1,
                         "target_groups": [{"all_hit": False} for _ in range(3)]})
            rows.append({"repetition": rep, "round": 2,
                         "target_groups": [{"all_hit": True}, {"all_hit": False},
                                           {"all_hit": False}]})
        self.assertTrue(evaluate_gate(rows, config, screen)["passed"])
        for row in rows:
            if row["round"] == 2:
                row["target_groups"] = [{"all_hit": False} for _ in range(3)]
        self.assertFalse(evaluate_gate(rows, config, screen)["passed"])

    def test_original_locations_count_separately(self):
        screen = {"groups": [{"qualifies": True, "eclass": 7,
                              "members": [{"seed_coverage": {"point": {
                                  "source": "rtl.v", "line": line, "column": 0,
                                  "type": "branch", "outcome": "if"}}}
                                  for line in (10, 20)]}]}
        points = [{"source": "rtl.v", "line": line, "column": 0,
                   "type": "branch", "outcome": "if", "hits": hit}
                  for line, hit in ((10, 1), (20, 0))]
        result = group_hits(points, screen)
        self.assertEqual(result[0]["raw_counter_hits"], [1, 0])
        self.assertFalse(result[0]["all_hit"])


if __name__ == "__main__":
    unittest.main()
