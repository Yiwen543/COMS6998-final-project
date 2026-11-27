import hashlib
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_frame_pc_diagnosis import diagnose, verify_cube, verify_diagnosis_record
from egg_frame_terms import BOOL_NAMES

try:
    import z3
except ImportError:
    z3 = None


@unittest.skipUnless(z3 is not None, "requires z3-solver")
class CandidateDiagnosisTests(unittest.TestCase):
    def test_known_positive_and_independent_full_width_replay(self):
        d = diagnose("(and h_valid (ult h_original_length 4))",
                     {"h_valid": 1, "h_original_length": 3, "m_data": 255}, True)
        self.assertEqual(d["public"]["status"], "sufficient")
        self.assertEqual(d["public"]["literal_count"], 2)
        self.assertEqual({(t["term"], t["value"]) for t in d["public"]["sufficient_literals"]},
                         {("(ult h_original_length 4)", True), ("h_valid", True)})
        self.assertEqual(set(d["sample"]), {"h_valid", "h_original_length"})
        q = d["oracle"]["typed_implication"]
        self.assertEqual(hashlib.sha256(q["smt2"].encode()).hexdigest(), q["smt2_sha256"])
        self.assertIn("(_ BitVec 16)", q["smt2"])
        solver = z3.Solver()
        solver.from_string(q["smt2"])
        self.assertEqual(solver.check(), z3.unsat)

    def test_false_verdict_uses_negated_candidate(self):
        d = diagnose("(and h_valid (ult h_original_length 4))",
                     {"h_valid": 1, "h_original_length": 65535}, False)
        self.assertTrue(d["typed_source"].startswith("(not (and "))
        self.assertEqual(d["public"], {"status": "sufficient", "candidate_value": False, "literal_count": 1,
            "sufficient_literals": [{"term": "(ult h_original_length 4)", "value": False}]})
        self.assertEqual(d["oracle"]["status"], "unsat")
        self.assertEqual(diagnose("false", {}, False)["cube"], [])

    def test_unknown_and_correlation_are_not_treated_as_known_values(self):
        d = diagnose("(or rst h_valid)", {"rst": -1, "h_valid": 1}, True)
        self.assertEqual(d["cube"], [["h_valid", True]])
        self.assertIsNone(d["sample"]["rst"])
        self.assertIsNone(d["assignment"]["rst"])
        partial = diagnose("(or rst h_valid)", {"h_valid": 0}, False)
        self.assertEqual(partial["public"]["status"], "sample_unknown")
        self.assertIsNone(partial["cube"])
        mismatch = diagnose("rst", {"rst": False}, True)
        self.assertEqual(mismatch["public"]["status"], "sample_mismatch")
        self.assertIsNone(mismatch["cube"])
        # Global word-level tautology, but neither independent comparison is known.
        correlated = diagnose("(or (ult h_length 4) (uge h_length 4))", {"h_length": None}, True)
        self.assertTrue(correlated["oracle"]["signed_source_at_sample"])
        self.assertEqual(correlated["public"]["status"], "unknown")
        self.assertIsNone(correlated["oracle"]["typed_implication"])
        # This *one primitive* is determinate, for every value of an unknown 16-bit bus.
        reflexive = diagnose("(eq h_length h_length)", {"h_length": -1}, True)
        self.assertEqual(reflexive["public"]["literal_count"], 1)

    def test_tampered_literal_sign_or_insufficient_observed_cube(self):
        spec = "(and rst h_valid)"
        vals = {"rst": 1, "h_valid": 1}
        # rst alone happens to match this row; a fresh unrestricted row refutes it.
        self.assertEqual(verify_cube(spec, [["rst", True]], vals)["status"], "sat")
        for forged in ([["rst", False]], [["m_valid", True]], [["rst", 1]],
                       [["rst", True], ["rst", True]]):
            with self.subTest(forged=forged), self.assertRaises(ValueError):
                verify_cube(spec, forged, vals)
        counterfeit = {"status": "sufficient", "cube": (("rst", True),), "size": 1}
        with patch("egg_frame_pc_diagnosis.minimum_cube", return_value=counterfeit):
            with self.assertRaisesRegex(ValueError, "does not imply"):
                diagnose(spec, vals, True)
        with self.assertRaises(ValueError):
            diagnose("rst", {"rst": True, "reference": True}, True)

    def test_receipt_ast_binding_accepts_printer_only_not_arbitrary_unsat(self):
        fresh = diagnose("(and rst h_valid)", {"rst": True, "h_valid": True}, True)
        archived = deepcopy(fresh)
        q = archived["oracle"]["typed_implication"]
        q["smt2"] = "; equivalent printer whitespace\n" + q["smt2"]
        q["smt2_sha256"] = hashlib.sha256(q["smt2"].encode()).hexdigest()
        self.assertTrue(verify_diagnosis_record(archived, fresh))
        q["smt2"] = "(assert false)\n(check-sat)\n"
        q["smt2_sha256"] = hashlib.sha256(q["smt2"].encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, "assertion AST differs"):
            verify_diagnosis_record(archived, fresh)

    def test_atom_limit_is_explicit(self):
        names = sorted(BOOL_NAMES)[:13]
        text = names[0]
        for n in names[1:]:
            text = f"(or {text} {n})"
        d = diagnose(text, dict.fromkeys(names, True), True)
        self.assertEqual(d["public"]["status"], "atom_limit")
        self.assertEqual(d["public"]["sufficient_literals"], [])
        self.assertIsNone(d["public"]["literal_count"])
        self.assertIsNone(d["cube"])
