"""Controls for the common FIFO grader and development-data visibility."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_fifo_formal import SPLIT
from egg_fifo_loop_feedback import ATOMS, feedback, review, validate_obligations


class CandidateReview(unittest.TestCase):
    def test_exact_five_atom_domain_and_gated_input(self):
        for bad in [[], ["true"], ["rst"], ["not_a_fifo_pin"], ["(not active active)"], ["(and active"],
                    ["(not active)", "(not   active)"], ["active" * 93], [SPLIT[0]] * 5]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                validate_obligations(bad)
        with patch("egg_fifo_loop_feedback.term_search", side_effect=AssertionError), \
             patch("egg_fifo_loop_feedback.checked_egg", side_effect=AssertionError):
            missing = review([SPLIT[0]], binary=None, arm="raw")
            complete = review(list(SPLIT), binary=None, arm="raw")
        self.assertEqual(missing["oracle"]["checked_assignments"], 32)
        self.assertFalse(missing["equivalent"])
        self.assertEqual(set(missing["counterexample"]), ATOMS)
        self.assertTrue(complete["equivalent"])
        self.assertIsNone(complete["counterexample"])

    def test_feedback_has_no_heldout_or_private_evidence(self):
        obligations = [SPLIT[0]]
        receipt = review(obligations, binary=None, arm="raw")
        sample = {key: key in ("active", "last_changed") for key in ATOMS}
        lines = ["Checking assertions in step 3..", "Assert failed in fifo_stall_formal: check_0", "Status: FAILED"]
        grade = {"obligations": obligations, "bounded_states": 12, "models": {
            "original": {"status": "PASSED", "failed_indices": [], "failed_step": None},
            "flip_last": {"status": "FAILED", "failed_indices": [0], "failed_step": 3,
                          "sampled_atoms": sample, "witness": "secret-path", "log_excerpt": lines},
            "flip_user": {"arbitrary": "never send"},
        }}
        raw = feedback(receipt, grade, "raw")
        visible = json.loads(raw)
        self.assertEqual(set(visible), {"rtl_bounded_checks"})
        self.assertEqual(visible["rtl_bounded_checks"]["diagnostic_probe"]["failed_step"], 3)
        self.assertNotIn("sampled_atoms", raw)
        self.assertEqual(visible["rtl_bounded_checks"]["diagnostic_probe"]["log_excerpt"], lines)
        with patch("egg_fifo_loop_feedback.term_search", return_value={
                "proved": False, "stop_reason": "term_budget", "steps": []}):
            ordinary = review(obligations, binary=None, arm="ordinary")
        structured = feedback(ordinary, grade, "ordinary")
        verdict = json.loads(structured)
        self.assertEqual(verdict["rtl_bounded_checks"]["diagnostic_probe"]["sampled_atoms"], sample)
        self.assertTrue(verdict["sampled_boolean_truth_table"]["counterexample"])
        self.assertEqual(verdict["rtl_bounded_checks"]["diagnostic_probe"]["log_excerpt"], lines)
        self.assertFalse(verdict["named_rewrite_search"]["proof_found"])
        for emitted in (raw, structured):
            for forbidden in ("flip_last", "flip_user", "private_mutant", "secret-path", "never send"):
                self.assertNotIn(forbidden, emitted)
        grade["models"]["flip_last"]["sampled_atoms"] = {**sample, "private_mutant": True}
        with self.assertRaisesRegex(ValueError, "five sampled"):
            feedback(ordinary, grade, "ordinary")
        grade["models"]["flip_last"]["log_excerpt"] = ["Status: FAILED in secret-path"]
        with self.assertRaisesRegex(ValueError, "diagnostic excerpt"):
            feedback(receipt, grade, "raw")
        with self.assertRaisesRegex(ValueError, "different candidate"):
            feedback(receipt, dict(grade, obligations=list(SPLIT)), "raw")

    def test_inconclusive_search_is_not_a_disproof(self):
        with patch("egg_fifo_loop_feedback.checked_egg", return_value={
                "egg_audit": None, "egg_proved": False, "egg_graph": {"stop_reason": "Some(IterationLimit(20))"}}):
            result = review(list(SPLIT), binary=None, arm="egg")
        self.assertTrue(result["equivalent"])
        self.assertFalse(result["proof"]["proved"])
        self.assertIsNone(result["counterexample"])
        self.assertIn("IterationLimit", result["proof"]["stop"])


if __name__ == "__main__":
    unittest.main()
