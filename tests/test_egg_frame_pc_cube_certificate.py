from copy import deepcopy
from importlib.util import find_spec
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
if find_spec("z3"):
    import egg_frame_pc_cube_certificate as proof
    from egg_frame_pc_diagnosis import diagnose

BINARY = Path(os.environ.get("CARGO_TARGET_DIR", ROOT / "egraph/target")) / "release/egg_cube_proofs"


@unittest.skipUnless(find_spec("z3"), "requires z3-solver")
class CubeCertificates(unittest.TestCase):
    @staticmethod
    def example():
        return diagnose("(or h_valid h_pad)", {"h_valid": 1, "h_pad": 0}, True)

    @unittest.skipUnless(BINARY.is_file(), "requires release egg_cube_proofs")
    def test_real_engine_reduces_cube_not_full_candidate(self):
        candidate = "(or (and h_valid h_pad) (and h_valid (not h_pad)))"
        d = diagnose(candidate, {"h_valid": 1, "h_pad": None}, True)
        # A contaminated diagnostic must fail closed before engine/public output.
        with self.assertRaisesRegex(ValueError, "diagnosis not bound"):
            proof.certify_cube({**d, "heldout": "must_not_appear"}, BINARY)
        result = proof.certify_cube(d, BINARY)
        public = result["public"]
        self.assertEqual(public["status"], "checked_rewrite")
        self.assertEqual(public["cube"], [["h_valid", True]])
        self.assertEqual(public["restricted_source"], "(or (and true h_pad) (and true (not h_pad)))")
        self.assertTrue(proof.replay_public_cube(public))
        self.assertTrue(proof.verify_cube_certificate(d, result))
        self.assertNotIn("must_not_appear", str(result))
        self.assertEqual(set(result["evidence"]["engine_request"]), {"term", "pattern_rules"})
        negative = diagnose("(and h_valid (ult h_original_length 256))", {"h_valid": 1, "h_original_length": 257}, False)
        signed = proof.certify_cube(negative, BINARY)
        self.assertFalse(signed["public"]["candidate_value"])
        self.assertEqual(signed["public"]["restricted_source"], "(not (and h_valid false))")
        self.assertTrue(proof.verify_cube_certificate(negative, signed))
        identity = proof.certify_cube(diagnose("h_pad", {"h_pad": 1}, True), BINARY)["public"]
        self.assertEqual((identity["status"], identity["steps"], identity["rules"]), ("checked_identity", [], []))

    def test_reversed_variable_erasure_requires_explicit_matching_replacement(self):
        d = self.example()
        bound = proof._bound(d)
        start = bound["restricted_source"]
        self.assertEqual(start, "(or true h_pad)")
        # A valid alternate derivation, including the reverse of or(true,?a)->true.
        graph = {"source": start, "target": "true", "merged": True, "stop_reason": "Some(NodeLimit(20000))",
                 "iterations": 2, "enodes": 7, "eclasses": 4,
                 "explanation": start + "\n(or (Rewrite<= or-true-left (or true h_pad)) h_pad)"
                                "\n(or (Rewrite=> or-true-left true) h_pad)\n(Rewrite=> or-true-left true)"}
        req = {"term": start, "pattern_rules": proof.RULES}
        result = proof._assess(bound, req, graph, "completed")
        public = result["public"]
        self.assertEqual(public["status"], "checked_rewrite")
        self.assertEqual(public["steps"][0], {"rule": "or-true-left", "direction": "reverse",
                                              "path": [0], "replacement": "(or true h_pad)"})
        self.assertTrue(proof.verify_cube_certificate(d, result))
        for mutate in [
                lambda r: r["public"]["steps"][0].update(replacement="(or false h_pad)"),
                lambda r: r["public"]["steps"][0].update(replacement="(or true m_valid)"),
                lambda r: r["public"]["steps"][0].update(path=[1, -1]),
                lambda r: r["public"]["rules"][0].update(right="false"),
                lambda r: r["public"].update(restricted_source="true"),
                lambda r: r["public"]["atoms"].update(h_pad="m_valid"),
                lambda r: r["public"].update(cube=[["h_pad", True]]),
                lambda r: r["evidence"]["engine_request"].update(target="hidden"),
                lambda r: r["evidence"]["engine"].update(explanation=start + "\n(Rewrite=> or-true-left false)"),
        ]:
            forged = deepcopy(result)
            mutate(forged)
            with self.assertRaises(ValueError):
                proof.verify_cube_certificate(d, forged)
        forged = deepcopy(d)
        forged["oracle"]["typed_implication"]["smt2"] += "(assert false)"
        with self.assertRaisesRegex(ValueError, "receipt changed"):
            proof.verify_cube_certificate(forged, result)
        for budget in ("MAX_CHARS", "MAX_STEPS"):
            with patch.object(proof, budget, 1):
                limited = proof._assess(bound, req, graph, "completed")
                self.assertEqual(limited["public"], {"status": "unavailable", "reason": "complete_proof_exceeds_budget"})

    def test_partial_and_timeout_do_not_publish_a_proof(self):
        partial = diagnose("rst", {"rst": None}, True)
        self.assertEqual(proof.certify_cube(partial, Path("unused"))["public"]["reason"], "no_sufficient_common_cube")
        d = self.example()
        with patch.object(proof.subprocess, "run", side_effect=subprocess.TimeoutExpired("egg", 30)):
            result = proof.certify_cube(d, Path(sys.executable))
        self.assertEqual(result["public"], {"status": "unavailable", "reason": "engine_process_timeout"})
        self.assertIsNone(result["evidence"]["engine"])
        self.assertTrue(proof.verify_cube_certificate(d, result))
        bound = proof._bound(d)
        request = {"term": bound["restricted_source"], "pattern_rules": proof.RULES}
        graph = {"source": request["term"], "target": "true", "merged": False, "stop_reason": "Some(TimeLimit(5.1))",
                 "explanation": None, "iterations": 1, "enodes": 4, "eclasses": 4}
        self.assertEqual(proof._assess(bound, request, graph, "completed")["public"]["reason"], "engine_resource_limit")
        graph.update(merged=True)
        with self.assertRaisesRegex(ValueError, "without an explanation"):
            proof._assess(bound, request, graph, "completed")

    def test_erasing_axioms_are_exhaustively_verified(self):
        schemas, rows = proof._rules(proof.RULES)
        self.assertEqual(len(schemas), 19)
        self.assertEqual(sum(rows.values()), 40)
        for lhs, rhs in [("(or false ?a)", "true"), ("?a", "?b")]:
            with patch.object(proof, "_TRIPLES", [("injected", lhs, rhs)]):
                with self.assertRaises(ValueError):
                    proof._rules([{"name": "injected", "left": lhs, "right": rhs}])
