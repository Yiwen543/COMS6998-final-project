"""Verify group-local facts, scoped caching, and matched propositional checks."""
from copy import deepcopy
from hashlib import sha256
from importlib.util import find_spec
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
if find_spec("z3"):
    from egg_regression_facts import OrdinarySession, certify, context_id, ordinary, prepare, verify


@unittest.skipUnless(find_spec("z3"), "requires z3-solver")
class RegressionFacts(unittest.TestCase):
    sources = ("(and m_valid (eq data_index data_n))",
               "(and m_valid (eq data_index 4))",
               "(and (eq data_index data_n) m_valid)")

    def test_common_context_and_independent_cache_replay(self):
        p = prepare(self.sources)
        guard = "(eq data_n 4)"
        cache, audit = {}, {}
        initial = certify(p, guard, cache)
        self.assertTrue(verify(p, guard, initial, audit))
        self.assertTrue(any(row["right"].startswith("bv_") for row in initial["facts"]))
        self.assertEqual(initial["counts"]["cache_hits"], 0)
        self.assertGreater(initial["counts"]["cache_misses"], 0)
        warm = certify(p, guard, cache)
        self.assertEqual(warm["counts"]["cache_misses"], 0)
        self.assertEqual(warm["counts"]["cache_hits"], initial["counts"]["cache_misses"])
        self.assertEqual(initial["facts"], warm["facts"])
        self.assertTrue(verify(p, guard, warm, audit))
        self.assertTrue(verify(p, guard, warm))
        session = OrdinarySession(p, warm)
        for endpoint in p["abstracts"]:
            self.assertEqual(session.compare(p["abstracts"][0], endpoint)["relation"], "equivalent")
        changed = certify(p, "(eq data_n 5)", cache)
        self.assertEqual(changed["counts"]["cache_hits"], 0)
        self.assertTrue(verify(p, "(eq data_n 5)", changed, audit))
        self.assertNotEqual(changed["context_id"], warm["context_id"])
        comparison = ordinary(p, changed, *p["abstracts"][:2])
        self.assertEqual(comparison["relation"], "unknown")
        self.assertEqual(comparison["old_only"], "sat")
        self.assertEqual(comparison["new_only"], "sat")
        with self.assertRaises(ValueError):
            verify(p, "(eq data_n 5)", warm)

    def test_no_whole_literal_goal_smuggling(self):
        p = prepare(["(eq data_index data_n)", "(eq data_index 4)", "(eq data_n 4)", "true"])
        result = certify(p, "(eq data_n 4)")
        self.assertEqual(result["facts"], [])
        self.assertGreater(result["counts"]["skipped_direct_pairs"], 0)
        self.assertTrue(verify(p, "(eq data_n 4)", result))

    def test_guard_empty_is_explicit_and_no_fact(self):
        p = prepare(self.sources)
        result = certify(p, "(ult m_data 0)")
        self.assertEqual(result["feasibility"]["status"], "unsat")
        self.assertEqual(result["facts"], [])
        self.assertTrue(verify(p, "(ult m_data 0)", result))
        comparison = ordinary(p, result, *p["abstracts"][:2])
        self.assertTrue(comparison["vacuous"])
        self.assertEqual(comparison["old_only"], "unsat")
        self.assertEqual(comparison["new_only"], "unsat")

    def test_guard_and_source_validation(self):
        for guard in ("(eq data_n 65536)", "(eq data_n m_data)", "(eq 4 data_n)", "(or m_valid s_valid)", "false", "(eq data_n 04)"):
            with self.assertRaises(ValueError, msg=guard):
                context_id(guard)
        p = prepare(self.sources)
        p["abstracts"][0] = "true"
        with self.assertRaises(ValueError):
            certify(p, "true")

    def test_tampered_smt_and_counters_rejected_and_no_cache_alias(self):
        p, guard, cache = prepare(self.sources), "(eq data_n 4)", {}
        f = certify(p, guard, cache)
        fact = next(iter(f["receipts"]))
        tampered = deepcopy(f)
        q = tampered["receipts"][fact]["query"]
        q["smt2"] = "(set-logic QF_BV)\n(assert false)\n(check-sat)\n"
        q["smt2_sha256"] = sha256(q["smt2"].encode()).hexdigest()
        with self.assertRaises(ValueError):
            verify(p, guard, tampered)
        tampered = deepcopy(f)
        tampered["counts"]["cache_hits"] += 1
        with self.assertRaises(ValueError):
            verify(p, guard, tampered)
        tampered = deepcopy(f)
        tampered["counts"]["cache_hits"] += 1
        tampered["counts"]["cache_misses"] -= 1
        with self.assertRaises(ValueError):
            verify(p, guard, tampered, {})
        original_receipt = deepcopy(f["receipts"][fact])
        f["receipts"][fact]["query"]["smt2"] = "forged"
        warm = certify(p, guard, cache)
        self.assertEqual(warm["receipts"][fact], original_receipt)

    def test_ordinary_implication_status_not_typed_sat(self):
        p = prepare(["(and m_valid m_ready)", "m_valid"])
        result = certify(p, "true")
        relation = ordinary(p, result, *p["abstracts"])
        self.assertEqual(relation["old_only"], "unsat")
        self.assertEqual(relation["new_only"], "sat")
        self.assertEqual(relation["relation"], "unknown")
        with self.assertRaises(ValueError):
            ordinary(p, result, "false", p["abstracts"][0])


if __name__ == "__main__":
    unittest.main()
