"""Transaction diagnoses bind physical values and typed expressions to replayable candidate-only proofs."""
from copy import deepcopy
import hashlib
from importlib.util import find_spec
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
BINARY = Path(os.environ.get("CARGO_TARGET_DIR", ROOT / "egraph/target")) / "release/egg_cube_proofs"
if find_spec("z3"):
    import z3
    import egg_txn_certificate as proof
    from egg_txn_terms import DOMAIN_NAMES


def disjunction(terms):
    result = terms[-1]
    for term in reversed(terms[:-1]):
        result = f"(or {term} {result})"
    return result


@unittest.skipUnless(find_spec("z3"), "requires z3-solver")
class TransactionDiagnoses(unittest.TestCase):
    def test_signed_widths_and_observed_polarity(self):
        candidate = "(and (ult h_length 256) (not (ult data_byte 128)))"
        d = proof.diagnose(candidate, {"h_length": 255, "data_byte": 255, "m_data": 77}, True)
        self.assertEqual(d["public"]["status"], "sufficient")
        self.assertEqual(set(d["sample"]), {"h_length", "data_byte"} | set(DOMAIN_NAMES))
        self.assertEqual({(r["term"], r["value"]) for r in d["public"]["sufficient_literals"]},
                         {("(ult h_length 256)", True), ("(ult data_byte 128)", False)})
        receipt = d["oracle"]["typed_implication"]
        self.assertEqual(receipt["smt2_sha256"], hashlib.sha256(receipt["smt2"].encode()).hexdigest())
        self.assertIn("(_ BitVec 16)", receipt["smt2"])
        self.assertIn("(_ BitVec 8)", receipt["smt2"])
        solver = z3.Solver()
        solver.from_string(receipt["smt2"])
        self.assertEqual(solver.check(), z3.unsat)
        # The false 8-bit comparison settles the signed monitor even with the Boolean pin unknown.
        d = proof.diagnose("(and phase_post (ult data_byte 128))", {"data_byte": 255}, False)
        self.assertFalse(d["public"]["candidate_value"])
        self.assertEqual(d["public"]["sufficient_literals"], [{"term": "(ult data_byte 128)", "value": False}])
        with self.assertRaises(ValueError):
            proof.diagnose("(ult data_byte 256)", {"data_byte": 255}, True)

    def test_unknown_is_never_published_as_a_cube(self):
        for sample in ({}, {"phase_post": None}, {"phase_post": -1}):
            with self.subTest(sample=sample):
                d = proof.diagnose("phase_post", sample, False)
                self.assertEqual(d["public"]["status"], "sample_unknown")
                self.assertIsNone(d["cube"])
                self.assertEqual(proof.certify(d, None)["public"]["status"], "unavailable")
        # All legal completions of a final sample are POST, even with the phase flag unobserved.
        inferred = proof.diagnose("phase_post", {"final_sample": True}, True)
        self.assertIsNone(inferred["sample"]["phase_post"])
        self.assertEqual(inferred["cube"], [["phase_post", True]])
        self.assertNotIn("final_sample", inferred["oracle"]["typed_implication"]["smt2"])
        mismatch = proof.diagnose("phase_post", {"phase_post": 0}, True)
        self.assertEqual(mismatch["public"]["status"], "sample_mismatch")
        self.assertIsNone(mismatch["cube"])

    def test_all_sixteen_literals_necessary_and_seventeenth_atom_exceeds_limit(self):
        terms = tuple(f"(eq h_length {n})" for n in range(16))
        # With an independent atom per comparison any omitted column can refute the false OR.
        # The actual word binds every comparison to False on this observed value.
        d = proof.diagnose(disjunction(terms), {"h_length": 300}, False)
        self.assertEqual(d["public"]["status"], "sufficient")
        self.assertEqual(d["public"]["literal_count"], len(terms))
        self.assertEqual(d["cube"], [[p, False] for p in sorted(d["atoms"])])
        d = proof.diagnose(disjunction(terms), {"h_length": 7}, True)
        self.assertEqual(d["public"]["literal_count"], 1)
        self.assertEqual(d["public"]["sufficient_literals"][0]["value"], True)
        d = proof.diagnose(disjunction((*terms, "(eq h_length 16)")), {"h_length": 300}, False)
        self.assertEqual(d["public"]["status"], "atom_limit")
        self.assertIsNone(d["cube"])
        self.assertEqual(proof.certify(d, None)["public"]["status"], "unavailable")


@unittest.skipUnless(find_spec("z3") and BINARY.is_file(), "requires z3-solver and the release cube engine")
class TransactionProofs(unittest.TestCase):
    @staticmethod
    def negative():
        return proof.diagnose("(and phase_post (ult h_original_length 256))", {"h_original_length": 32768}, False)

    def test_candidate_only_real_rewrite_and_identity(self):
        d = self.negative()
        c = proof.certify(d, BINARY)
        public = c["public"]
        self.assertEqual(public["status"], "checked_rewrite")
        self.assertFalse(public["candidate_value"])
        self.assertEqual(public["restricted_source"], "(not (and phase_post false))")
        self.assertEqual(public["target"], "true")
        self.assertTrue(public["steps"])
        request = c["evidence"]["engine_request"]
        self.assertEqual(set(request), {"term", "pattern_rules"})
        self.assertEqual(request["term"], public["restricted_source"])
        self.assertTrue(proof.replay_public(public))
        self.assertTrue(proof.verify_certificate(d, c))
        d = proof.diagnose("phase_post", {"phase_post": True}, True)
        result = proof.certify(d, BINARY)
        self.assertEqual((result["public"]["status"], result["public"]["steps"]), ("checked_identity", []))
        self.assertTrue(proof.verify_certificate(d, result))

    def test_tampering_rejected_even_if_substituted_query_is_unsat(self):
        original = self.negative()
        cert = proof.certify(original, BINARY)
        for key, change in [
                ("source", lambda d: d.update(source="true")),
                ("sample", lambda d: d["sample"].update(h_original_length=3)),
                ("atom", lambda d: d["atoms"].update(phase_post="input_open"))]:
            altered = deepcopy(original)
            change(altered)
            with self.subTest(key=key), self.assertRaises(ValueError):
                proof.verify_certificate(altered, cert)
        altered = deepcopy(original)
        receipt = altered["oracle"]["typed_implication"]
        receipt["smt2"] = "(set-logic QF_BV)\n(assert false)\n(check-sat)\n"
        receipt["smt2_sha256"] = hashlib.sha256(receipt["smt2"].encode()).hexdigest()
        with self.assertRaises(ValueError):
            proof.verify_certificate(altered, cert)
        for key, change in [
                ("replacement", lambda p: p["steps"][0].update(replacement="phase_post")),
                ("rule", lambda p: p["rules"][0].update(right="phase_post")),
                ("binding", lambda p: p["atoms"].update(phase_post="input_open")),
                ("residual", lambda p: p.update(restricted_source="true"))]:
            altered = deepcopy(cert)
            change(altered["public"])
            with self.subTest(key=key), self.assertRaises(ValueError):
                proof.replay_public(altered["public"])
            with self.subTest(archive_key=key), self.assertRaises(ValueError):
                proof.verify_certificate(original, altered)

    def test_independent_limits_preserve_private_proof(self):
        for field in ("MAX_STEPS", "MAX_CHARS"):
            with self.subTest(budget=field), patch.object(proof, field, 0):
                d = self.negative()
                cert = proof.certify(d, BINARY)
                self.assertEqual(cert["public"], {"status": "unavailable", "reason": "complete_proof_exceeds_budget"})
                self.assertTrue(cert["evidence"]["engine"]["explanation"])
                self.assertTrue(proof.verify_certificate(d, cert))


if __name__ == "__main__":
    unittest.main()
