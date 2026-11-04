import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from coverage import load
from run_sfifo_stress_fixed import SOURCE
from sfifo_prompt_ablation_feedback import egg_feedback, messages_for, pack_raw, unpack_raw
from sfifo_stress_feedback import raw_feedback


class SfifoPromptAblationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.points = load(ROOT / "results/midterm_candidate_preflight/sfifo-stress/seed.dat",
                          str(SOURCE.relative_to(ROOT)), include_descendants=True)
        path = ROOT / "results/sfifo_prompt_ablation_preflight/semantic.json"
        if not path.exists():
            raise unittest.SkipTest("Run semantic_candidate_scan on sfifo stress first")
        cls.semantic = json.loads(path.read_text())
        cls.prior = {"checker": {"checks": 4, "distinct_defects": [], "failures": []}}

    def test_raw_packing_roundtrips_every_point(self):
        original = raw_feedback(self.points)
        self.assertEqual(original, unpack_raw(pack_raw(original)))
        self.assertLess(len(json.dumps(pack_raw(original))), len(json.dumps(original)))

    def test_common_payload_and_feedback_isolation(self):
        payloads = {}
        for arm in ("B_full", "B_compact", "P_compact", "C_compact"):
            prompt = messages_for(arm, [], self.prior, "", self.points,
                                  self.semantic, 1, 8)
            payloads[arm] = json.loads(prompt[1]["content"])
        common = {key: value for key, value in payloads["B_full"].items()
                  if key != "raw_uncovered_dut_coverage"}
        for arm in ("B_compact", "P_compact", "C_compact"):
            other = {key: value for key, value in payloads[arm].items()
                     if key not in ("raw_uncovered_dut_coverage", "egg_normalization")}
            self.assertEqual(common, other)
            self.assertEqual(payloads["B_full"]["raw_uncovered_dut_coverage"],
                             unpack_raw(payloads[arm]["raw_uncovered_dut_coverage"]))
        self.assertNotIn("egg_normalization", payloads["B_compact"])
        self.assertNotIn("egg_normalization", payloads["P_compact"])

    def test_c_groups_are_nontrivial_mapped_and_keep_all_locations(self):
        feedback = egg_feedback(self.semantic, self.points)
        groups = feedback["equivalent_uncovered_groups"]
        self.assertEqual([{91, 161}, {96, 129, 179}],
                         [set(m["line"] for m in g["members"]) for g in groups])
        self.assertTrue(all(g["equivalent_expression_count"] > 1 for g in groups))
        self.assertTrue(all(m["hits"] == 0 for g in groups for m in g["members"]))
        self.assertEqual(5, sum(len(g["members"]) for g in groups))
        self.assertTrue(feedback["incomplete_source_mappings"])


if __name__ == "__main__":
    unittest.main()
