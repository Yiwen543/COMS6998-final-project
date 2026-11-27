"""Controls for width-correct grading and evidence that is separate from that grading."""
from importlib.util import find_spec
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
BINARY = Path(os.environ.get("CARGO_TARGET_DIR", ROOT / "egraph/target")) / "release/guard_proofs_fast"
if find_spec("z3"):
    import z3
    from egg_frame_proof import review, typed_oracle
    from egg_frame_terms import REFERENCES, evaluate_term, parse_term


@unittest.skipUnless(find_spec("z3"), "requires z3-solver")
class FrameProof(unittest.TestCase):
    def test_full_width_counterexample_replays(self):
        left = "(and h_valid (ult h_original_length 256))"
        result = review(left, "h_valid", arm="raw", binary=None)
        sample = result["counterexample"]
        self.assertIsNone(result["proof"])
        self.assertFalse(result["equivalent"])
        self.assertTrue(sample["h_valid"])
        self.assertGreaterEqual(sample["h_original_length"], 256)
        self.assertLess(sample["h_original_length"], 65536)
        for key in ("reference", "candidate"):
            self.assertEqual(evaluate_term(parse_term(result[key]), sample), result[key + "_value"])
        with self.assertRaises(ValueError):
            review("(ult m_data 256)", "true", arm="raw", binary=None)
        for name, term in REFERENCES.items():
            with self.subTest(property=name):
                self.assertTrue(review(term, term, arm="raw", binary=None)["equivalent"])

    def test_reused_full_xor_bound_to_exact_input(self):
        reference, candidate = "(and h_valid (ult h_length 256))", "h_valid"
        common = typed_oracle(reference, candidate)
        self.assertFalse(common["oracle"]["equivalent"])
        with patch("egg_frame_proof._oracle", side_effect=AssertionError("repeated full typed query")):
            raw = review(reference, candidate, arm="raw", binary=None, common=common)
            ordinary = review(reference, candidate, arm="ordinary", binary=None, common=common)
            self.assertEqual(raw["oracle"], ordinary["oracle"])
            self.assertTrue(ordinary["oracle_reused"])
            raw["counterexample"]["h_length"] = 0
            self.assertGreaterEqual(common["oracle"]["counterexample"]["h_length"], 256)
            for ref, target, timeout, receipt in [
                    (candidate, reference, 5000, common), (reference, candidate + " ", 5000, common),
                    (reference, candidate, 99, common), (reference, candidate, 5000, dict(common))]:
                with self.subTest(candidate=target, timeout=timeout), self.assertRaisesRegex(ValueError, "bound"):
                    review(ref, target, arm="raw", binary=None, timeout_ms=timeout, common=receipt)
            if BINARY.is_file():
                egg = review(reference, candidate, arm="egg", binary=BINARY, common=common)
                self.assertEqual(ordinary["oracle"], egg["oracle"])
                self.assertEqual(ordinary["evidence"]["verified_rules"], egg["evidence"]["verified_rules"])

    def test_local_certificates_and_root_pair_omission(self):
        left, right = "(ult h_original_length 256)", "(ule h_original_length 255)"
        naked = review(left, right, arm="ordinary", binary=None)
        self.assertTrue(naked["equivalent"])
        self.assertFalse(naked["proof"]["proved"])
        self.assertEqual(naked["evidence"]["verified_rules"], [])
        self.assertIn("skipped", naked["evidence"]["primitive_pair_checks"][0])
        for expr, relation in [(right, "equal"), ("(not (uge h_original_length 256))", "complement")]:
            with self.subTest(derived=relation):
                result = review(f"(and h_valid {left})", f"(and h_valid {expr})", arm="ordinary", binary=None)
                self.assertTrue(result["equivalent"])
                self.assertTrue(result["proof"]["proved"])
                self.assertEqual(len(result["evidence"]["verified_rules"]), 1)
                query = result["evidence"]["primitive_pair_checks"][0]["queries"][-1]
                self.assertEqual((query["relation"], query["status"]), (relation, "unsat"))
                solver = z3.Solver()
                solver.from_string(query["smt2"])
                self.assertEqual(solver.check(), z3.unsat)

    def test_ordinary_is_complete_on_abstract_booleans(self):
        left, right = "(and rst (or h_valid m_valid))", "(or (and rst h_valid) (and rst m_valid))"
        result = review(left, right, arm="ordinary", binary=None)
        self.assertTrue(result["equivalent"])
        self.assertTrue(result["proof"]["proved"])
        self.assertFalse(result["proof"]["canonical_match"])
        self.assertEqual(result["evidence"]["abstract_xor"]["status"], "unsat")
        self.assertEqual(result["evidence"]["verified_rules"], [])

    def test_incomplete_or_forged_egg_cannot_prove(self):
        targets = [{"id": name, "eclass": 0, "eclass_before": i} for i, name in enumerate(("reference", "candidate"))]
        graph = {"ground_rule_count": 0, "targets": targets, "stop_reason": "Some(NodeLimit(20001))",
                 "rewrite_explanations": []}

        def synthetic(mode):
            return subprocess.CompletedProcess([], 0, json.dumps(graph), json.dumps({"mode": mode}))

        left, right = "(and h_valid true)", "h_valid"
        with patch("egg_frame_proof.subprocess.run", return_value=synthetic("indexed")):
            result = review(left, right, arm="egg", binary=Path(__file__))
        self.assertTrue(result["equivalent"])
        self.assertFalse(result["proof"]["proved"])
        self.assertIsNone(result["evidence"]["egg_audit"])
        graph["stop_reason"] = "Some(Saturated)"
        with patch("egg_frame_proof.subprocess.run", return_value=synthetic("indexed")), self.assertRaisesRegex(
                ValueError, "missing proof connectivity"):
            review(left, right, arm="egg", binary=Path(__file__))
        with patch("egg_frame_proof.subprocess.run", return_value=synthetic("ordinary")), self.assertRaisesRegex(
                ValueError, "unexpected egg mode"):
            review(left, right, arm="egg", binary=Path(__file__))

    @unittest.skipUnless(BINARY.is_file(), "requires release guard_proofs_fast")
    def test_real_egg_proof_and_saturated_miss(self):
        left = "(and h_valid (ult h_original_length 256))"
        right = "(and h_valid (ule h_original_length 255))"
        result = review(left, right, arm="egg", binary=BINARY)
        self.assertTrue(result["equivalent"])
        self.assertTrue(result["proof"]["proved"])
        self.assertEqual(result["evidence"]["egg_audit"]["checked_steps"], 1)
        self.assertEqual(len(result["evidence"]["egg_audit"]["ground_rules"]), 1)
        left, right = "(and rst (or h_valid m_valid))", "(or (and rst h_valid) (and rst m_valid))"
        result = review(left, right, arm="egg", binary=BINARY)
        self.assertTrue(result["equivalent"])
        self.assertFalse(result["proof"]["proved"])
        self.assertEqual(result["proof"]["stop"], "Some(Saturated)")


if __name__ == "__main__":
    unittest.main()
