"""Gate typed sampled observations and the isolated frame feedback histories."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_frame_llm import ARMS, SEED, assess, fixture_provider, run
from egg_frame_observe import sample
from egg_frame_terms import REFERENCES, parse_term


ROOT = Path(__file__).resolve().parents[1]


class FrameLoopControls(unittest.TestCase):
    def test_unknown_inactive_payload_is_masked_without_coercion(self):
        monitor = parse_term("(and h_valid (ne h_length 4))")
        self.assertIs(sample(monitor, {"h_valid": 0, "h_length": -1}), False)
        self.assertIsNone(sample(monitor, {"h_valid": 1, "h_length": -1}))
        self.assertIs(sample(monitor, {"h_valid": 1, "h_length": 3}), True)
        with self.assertRaises(ValueError):
            sample(monitor, {"h_valid": -1, "h_length": 65536})

    def test_indeterminate_physical_observation_blocks_combined_pass(self):
        physical = {"totals_by_design": {
            "original": {"reference_alarms": 0, "matched_alarms": 0, "missed": 0,
                         "false_alarm": 0, "unknown": 1},
        }}
        with (patch("egg_frame_llm.review", return_value={"equivalent": True}),
              patch("egg_frame_llm.tool_feedback", return_value={})):
            grade, _, _ = assess(REFERENCES, binary=None, arm="raw", physical=physical)
        self.assertEqual(grade["equivalent_properties"], 5)
        self.assertFalse(grade["verified"])

    @unittest.skipUnless(os.environ.get("GUARD_PROOFS_FAST"), "set guard_proofs_fast release executable")
    def test_fixed_seed_and_two_feedback_rounds(self):
        corpus = ROOT / "results/milestone3/frame-faults"
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / "run"
            result = run(corpus_dir=corpus, binary=Path(os.environ["GUARD_PROOFS_FAST"]),
                         out=out, provider=fixture_provider(), mode="fixture", rounds=2)
            self.assertEqual(result["provider_api_calls"], 0)
            for arm in ARMS:
                self.assertEqual(result["seeds"][arm]["inequivalent_properties"], 5)
                self.assertEqual(result["arms"][arm]["first_verified_round"], 1)
                seed_feedback = (out / arm / "seed/feedback.txt").read_text().rstrip()
                path = out / arm / "round-02"
                messages = json.loads((path / "request.json").read_bytes())["messages"]
                self.assertIn(json.dumps(SEED, sort_keys=True), messages[1]["content"])
                self.assertIn(seed_feedback, messages[1]["content"])
                self.assertEqual(json.loads(messages[2]["content"]),
                                 json.loads((out / arm / "round-01/response.json").read_bytes())["output"])
                self.assertEqual(messages[3]["content"], (out / arm / "round-01/feedback.txt").read_text().rstrip()
                                 + "\nSubmit all five monitors again.")
                for code in ("F01", "F02", "F03", "F04", "F05", "F06"):
                    self.assertNotIn(code, json.dumps(messages))
                self.assertEqual("semantic_and_proof_review" in json.loads(seed_feedback), arm != "raw")
            for stage in ("seed", "round-01", "round-02"):
                structured = []
                for arm in ("ordinary", "egg"):
                    data = json.loads((out / arm / stage / "feedback.txt").read_bytes())
                    for value in data["semantic_and_proof_review"].values():
                        value.pop("proof")
                    structured.append(data)
                self.assertEqual(*structured)


if __name__ == "__main__":
    unittest.main()
