"""Reject stale or semantically mismatched receipts without changing archived evidence."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from m3_coverage_waiver import EVIDENCE_FILES, ROOT, check_waiver


class WaiverReceipt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        source = ROOT / "results/milestone3/coverage-waiver"
        self.receipt = self.dir / "waiver.json"
        shutil.copyfile(source / "waiver.json", self.receipt)
        (self.dir / "original").mkdir()
        for name in EVIDENCE_FILES:
            shutil.copyfile(source / "original" / name, self.dir / "original" / name)
        self.bound = json.loads(self.receipt.read_bytes())["binding"]

    def modify(self, name, data):
        (self.dir / "original" / name).write_bytes(data)
        receipt = json.loads(self.receipt.read_bytes())
        receipt["evidence_sha256"][name] = hashlib.sha256(data).hexdigest()
        self.receipt.write_text(json.dumps(receipt))

    def test_good_receipt_and_stale_context_or_live_hits(self):
        self.assertEqual(check_waiver(self.receipt, self.bound, 0), [])
        for hits in (1, -1, True):
            with self.subTest(hits=hits):
                self.assertTrue(check_waiver(self.receipt, self.bound, hits))
        changed = dict(self.bound, source_guard="false")
        self.assertIn("source_guard", check_waiver(self.receipt, changed, 0))
        receipt = json.loads(self.receipt.read_bytes())
        receipt["binding"]["extra_assumption"] = "rst is always asserted"
        self.receipt.write_text(json.dumps(receipt))
        self.assertIn("extra_assumption", check_waiver(self.receipt, self.bound, 0))

    def test_rehashed_incorrect_solver_statement_or_transcript(self):
        self.modify("direct.z3", b"sat\n")
        self.modify("premise.smt2", b"(assert false)\n(check-sat)\n")
        errors = check_waiver(self.receipt, self.bound, 0)
        self.assertIn("incorrect query or verdict: direct", errors)
        self.assertIn("incorrect query or verdict: premise", errors)

    def test_rehashed_invalid_proof_step(self):
        graph = json.loads((self.dir / "original/egg-proof.json").read_bytes())
        old = graph["rewrite_explanations"][0]["explanation"]
        graph["rewrite_explanations"][0]["explanation"] = old.replace("Rewrite=>", "Rewrite<=")
        self.modify("egg-proof.json", json.dumps(graph).encode())
        self.assertTrue(any("invalid archived proof" in msg for msg in check_waiver(self.receipt, self.bound, 0)))

    def test_missing_evidence_rejects_even_if_binding_is_current(self):
        (self.dir / "original/direct.smt2").unlink()
        self.assertIn("evidence changed: direct.smt2", check_waiver(self.receipt, self.bound, 0))


if __name__ == "__main__":
    unittest.main()
