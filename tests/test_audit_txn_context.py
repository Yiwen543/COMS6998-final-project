"""Adversarial mutations of contextual proof artifacts never establish global equivalence."""
from copy import deepcopy
import gzip
import hashlib
from importlib.util import find_spec
import json
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
if find_spec("z3"):
    import egg_txn_context as producer
    from audit_txn_context import _facts, audit_pair, bind_pair, verify_partition
    from egg_txn_context_check import PATTERN_RULES


@unittest.skipUnless(find_spec("z3"), "requires z3-solver")
class AuditContext(unittest.TestCase):
    def setUp(self):
        self.sources = ("(and (eq data_n 4) (eq data_index data_n))", "(and (eq data_n 4) (eq data_index 4))")
        self.prepared = producer.prepare(*self.sources)
        self.plan = producer.contexts(*self.sources, split=True)

    def test_exhaustiveness_and_disjointness_receipts_are_specific_obligations(self):
        for which in ("missing", "order", "duplicate", "weak_receipt", "foreign_guard"):
            with self.subTest(which=which):
                p = deepcopy(self.plan)
                if which == "missing":
                    p["contexts"].pop(1)
                elif which == "order":
                    p["contexts"].reverse()
                elif which == "duplicate":
                    p["contexts"][2] = p["contexts"][0]
                elif which == "weak_receipt":
                    # Both queries are genuinely UNSAT. A fresh status or XOR of two
                    # contradictions is insufficient to bind an archived obligation.
                    p["coverage"] = p["disjoint"][0]["query"]
                else:
                    p["contexts"][0]["feasibility"] = p["contexts"][2]["feasibility"]
                with self.assertRaises(ValueError):
                    verify_partition(self.prepared, p)

    def test_atom_rebinding_forged_unsat_or_crossed_branch_is_rejected(self):
        altered = deepcopy(self.prepared)
        atom = next(name for name in altered["atoms"] if name.startswith("bv_"))
        altered["atoms"][atom] = "false"
        with self.assertRaises(ValueError):
            bind_pair(*self.sources, altered)
        outside, equal, _ = self.plan["contexts"]
        result = producer.certify_facts(self.prepared, equal)
        self.assertGreaterEqual(len(result["facts"]), 2)
        with self.assertRaises(ValueError):
            _facts(self.prepared, outside, result)
        bad = deepcopy(result)
        item = next(iter(bad["receipts"].values()))["query"]
        item["smt2"] = "(set-logic QF_BV)\n(assert false)\n(check-sat)\n"
        item["smt2_sha256"] = hashlib.sha256(item["smt2"].encode()).hexdigest()
        with self.assertRaises(ValueError):
            _facts(self.prepared, equal, bad)

    def test_checked_native_evidence_and_partial_graph_proof(self):
        path = Path(os.environ.get("TXN_CONTEXT_RUN", ROOT / "results/milestone3/frame-txn-context-proof"))
        if not (path / "cases.jsonl.gz").is_file():
            self.skipTest("requires frozen context proof archive")
        with gzip.open(path / "cases.jsonl.gz") as stream:
            row = next(obj for line in stream if (obj := json.loads(line))["case"]["id"] == "C01")
        case, prepared = row["case"], row["prepared"]
        method = row["methods"]["contextual"]
        def check(branches):
            return audit_pair(case["left"], case["right"], prepared, method["plan"], branches, PATTERN_RULES)
        self.assertTrue(check(method["branches"])["proved"])
        missed = deepcopy(method["branches"])
        missed[-1].update(graph=None, proof={"proved": False, "steps": [], "status": "subprocess_timeout",
                                             "stop": "subprocess_timeout", "used_ground_rules": []})
        self.assertFalse(check(missed)["proved"])
        missed[-1]["proof"]["proved"] = True
        with self.assertRaises(ValueError):
            check(missed)
        with self.assertRaises(ValueError):
            check(method["branches"][:-1])
        wrong = deepcopy(method["branches"])
        wrong[1]["payload"]["targets"][0]["compact"] = "true"
        with self.assertRaises(ValueError):
            check(wrong)


if __name__ == "__main__":
    unittest.main()
