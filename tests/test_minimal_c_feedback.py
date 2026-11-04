import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from minimal_c_feedback import common_payload, minimal_c_messages


class MinimalCFeedbackTests(unittest.TestCase):
    def test_preserves_common_information_and_exact_source_hits(self):
        folder = ROOT / "results/sfifo_prompt_ablation_live_20261103/C_compact/rep1"
        for round_no, count in ((1, 5), (4, 2), (6, 0)):
            full = json.loads((folder / f"prompt-C_compact-{round_no}-1.json").read_text())
            minimal = minimal_c_messages(full)
            self.assertEqual(common_payload(full), common_payload(minimal))
            a = json.loads(full[1]["content"])["egg_normalization"]
            b = json.loads(minimal[1]["content"])["egg_normalization"]
            expected = [(g["event_context"], [(m["line"], m["column"], m["counter_type"],
                                               m["outcome"], m["hits"])
                                              for m in g["members"]])
                        for g in a["equivalent_uncovered_groups"]]
            actual = [(g["event_context"], [tuple(m[1:]) for m in g["equivalent_guard_sites"]])
                      for g in b["groups"]]
            self.assertEqual(expected, actual)
            self.assertEqual(count, sum(len(x[1]) for x in actual))
            self.assertNotIn("typed_atoms", b)
            self.assertNotIn("eclass_nodes", json.dumps(b))
            self.assertEqual(full[0], minimal[0])

    def test_rejects_non_c_payload(self):
        with self.assertRaises(ValueError):
            minimal_c_messages([{"role": "system", "content": ""},
                                {"role": "user", "content": "{}"}])


if __name__ == "__main__":
    unittest.main()
