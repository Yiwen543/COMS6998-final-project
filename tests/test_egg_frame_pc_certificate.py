"""Candidate polarity, exact common cube, compact proof replay, and fail-closed evidence."""
from copy import deepcopy
from importlib.util import find_spec
import json
import os
from pathlib import Path
import sys
import subprocess
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
BINARY = Path(os.environ.get("CARGO_TARGET_DIR", ROOT / "egraph/target")) / "release/egg_diagnostic_forms"
if find_spec("z3"):
    from egg_frame_pc_certificate import certify, replay_public, verify_certificate
    from egg_frame_pc_diagnosis import diagnose


@unittest.skipUnless(find_spec("z3") and BINARY.is_file(), "requires Z3 and the release diagnostic egg binary")
class CandidateCertificates(unittest.TestCase):
    @staticmethod
    def example():
        return diagnose("(and h_valid (or h_pad h_truncate))",
                        {"h_valid": True, "h_pad": True, "h_truncate": False}, True)

    def test_actual_proof_and_provenance(self):
        diagnosis = self.example()
        diagnosis["reference"] = diagnosis["heldout"] = "secret_do_not_show"
        result = certify(diagnosis, BINARY)
        public = result["public"]
        self.assertEqual(public["status"], "checked_rewrite")
        self.assertEqual(public["steps"], [{"direction": "forward", "rule": "and-distribute-right", "path": []}])
        self.assertTrue(replay_public(public))
        self.assertTrue(verify_certificate(diagnosis, result))
        self.assertEqual(set(result["evidence"]["engine_request"]), {"term", "pattern_rules"})
        self.assertNotIn("secret_do_not_show", json.dumps(result))
        false = diagnose("(and h_valid (ult h_original_length 256))", {"h_valid": 1, "h_original_length": 257}, False)
        negative = certify(false, BINARY)["public"]
        self.assertFalse(negative["candidate_value"])
        self.assertEqual(negative["cube"], false["cube"])
        self.assertEqual(negative["rules"][0]["name"], "de-morgan-and")
        self.assertTrue(replay_public(negative))

    def test_tampering_cannot_be_reported_as_checked(self):
        diagnosis = self.example()
        valid = certify(diagnosis, BINARY)
        for mutate in [
                lambda d: d["public"]["steps"][0].update(path=[0]),
                lambda d: d["public"].update(cube=[["h_valid", True]]),
                lambda d: d["public"]["atoms"].update(h_valid="m_valid"),
                lambda d: d["evidence"]["engine_request"].update(target="hidden"),
                lambda d: d["evidence"]["engine"].update(explanation="")]:
            changed = deepcopy(valid)
            mutate(changed)
            with self.assertRaises(ValueError):
                verify_certificate(diagnosis, changed)
        for mutate in [
                lambda d: d["sample"].update(h_valid=False),
                lambda d: d["atoms"].update(h_valid="m_valid"),
                lambda d: d.update(cube=[["h_valid", True]]),
                lambda d: d.update(typed_source="h_valid")]:
            changed = deepcopy(diagnosis)
            mutate(changed)
            with self.assertRaises(ValueError):
                verify_certificate(changed, valid)

    def test_external_limit_receipt_and_invalid_graph(self):
        diagnosis = self.example()

        def timeout(*args, **kwargs):
            kwargs["stdout"].write(b"incomplete egg output")
            raise subprocess.TimeoutExpired(args[0], kwargs["timeout"])

        with patch("egg_frame_pc_certificate.subprocess.run", side_effect=timeout):
            limited = certify(diagnosis, BINARY)
            self.assertEqual(limited["public"], {"status": "unavailable", "reason": "engine_timeout"})
            self.assertTrue(verify_certificate(diagnosis, limited))
            limited["evidence"]["tool_event"]["sha256"] = "f" * 64
            with self.assertRaises(ValueError):
                verify_certificate(diagnosis, limited)
        with patch("egg_frame_pc_certificate.MAX_RAW_BYTES", 1):
            oversized = certify(diagnosis, BINARY)
            self.assertEqual(oversized["public"]["reason"], "raw_output_limit")
            self.assertTrue(verify_certificate(diagnosis, oversized))
        full = certify(diagnosis, BINARY)
        full["evidence"]["engine"]["literal_count"] += 1
        with self.assertRaisesRegex(ValueError, "costs"):
            verify_certificate(diagnosis, full)
        # Even when the downstream typed checker signals its explicit depth bound,
        # the original full named proof must replay before a limit may be reported.
        with patch("egg_frame_pc_certificate.check_engine", side_effect=ValueError("term nesting exceeds 128 levels")):
            deep = certify(diagnosis, BINARY)
            self.assertEqual(deep["public"]["reason"], "typed_depth_limit")
            self.assertTrue(deep["evidence"]["checked_steps"])
            deep["evidence"]["engine"]["explanation"] = deep["evidence"]["engine"]["explanation"].replace(
                "and-distribute-right", "forged-lemma")
            with self.assertRaisesRegex(ValueError, "unknown"):
                verify_certificate(diagnosis, deep)

    def test_identity_unavailable_and_complete_proof_budget(self):
        identity = diagnose("(and h_valid h_pad)", {"h_valid": 1, "h_pad": 1}, True)
        public = certify(identity, BINARY)["public"]
        self.assertEqual((public["status"], public["steps"], public["rules"]), ("checked_identity", [], []))
        self.assertTrue(replay_public(public))
        missing = diagnose("(or (and h_valid h_pad) (and (not h_pad) h_valid))", {"h_valid": 1, "h_pad": 1}, True)
        refused = certify(missing, BINARY)
        self.assertEqual(refused["public"], {"status": "unavailable", "reason": "dnf_lacks_exact_common_cube"})
        self.assertTrue(verify_certificate(missing, refused))
        for field in ("MAX_STEPS", "MAX_CHARS"):
            with patch("egg_frame_pc_certificate." + field, 0):
                limited = certify(self.example(), BINARY)
                self.assertEqual(limited["public"], {"status": "unavailable", "reason": "complete_proof_exceeds_budget"})
                self.assertTrue(limited["evidence"]["engine"]["explanation"])
                self.assertTrue(verify_certificate(self.example(), limited))
        unknown = diagnose("h_ready", {"h_ready": None}, False)
        with patch("egg_frame_pc_certificate.subprocess.run", side_effect=AssertionError):
            self.assertEqual(certify(unknown, None)["public"]["reason"], "no_sufficient_common_cube")


if __name__ == "__main__":
    unittest.main()
