"""Token-load placebo isolation with a deterministic fake provider counter."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from token_placebo import match_placebo, replace_egg_with_padding


class TokenPlaceboTests(unittest.TestCase):
    def setUp(self):
        self.c = [{"role": "system", "content": "Common instructions"},
                  {"role": "user", "content": json.dumps({
                      "specification": "fixed", "raw_uncovered_dut_coverage": [{"line": 17}],
                      "egg_normalization": {"eclasses": ["a", "b"]}}, sort_keys=True)}]

    @staticmethod
    def fake_count(messages):
        payload = json.loads(messages[1]["content"])
        if "egg_normalization" in payload:
            return 200
        return 120 + payload["neutral_token_matched_appendix"].count(" x")

    def test_matches_without_semantic_leak(self):
        messages, evidence = match_placebo(self.c, self.fake_count)
        payload = json.loads(messages[1]["content"])
        self.assertEqual(evidence["absolute_delta"], 0)
        self.assertEqual(evidence["count_requests"], 3)
        self.assertNotIn("egg_normalization", payload)
        self.assertEqual(payload["specification"], "fixed")
        self.assertEqual(payload["raw_uncovered_dut_coverage"], [{"line": 17}])
        self.assertNotIn("eclasses", messages[1]["content"])

    def test_fails_closed_when_provider_does_not_match(self):
        with self.assertRaises(RuntimeError):
            match_placebo(self.c, lambda messages: 200 if "egg_normalization" in
                          messages[1]["content"] else 120, max_counts=5)

    def test_matches_nonunit_provider_token_slope(self):
        def count(messages):
            payload = json.loads(messages[1]["content"])
            if "egg_normalization" in payload:
                return 200
            return 120 + payload["neutral_token_matched_appendix"].count(" x") // 2
        _, evidence = match_placebo(self.c, count)
        self.assertLessEqual(evidence["absolute_delta"], 2)

    def test_requires_c_evidence(self):
        with self.assertRaises(ValueError):
            replace_egg_with_padding([self.c[0], {"role": "user", "content": "{}"}], 1)


if __name__ == "__main__":
    unittest.main()
