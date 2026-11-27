"""Independent typed semantic-regression controls for incremental SMT."""
from copy import deepcopy
from hashlib import sha256
from importlib.util import find_spec
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
if find_spec("z3"):
    from egg_regression_smt import IncrementalSMT, classify, fresh_compare, verify_result, verify_direction


@unittest.skipUnless(find_spec("z3"), "requires z3-solver")
class RegressionSMT(unittest.TestCase):
    def test_violation_polarity(self):
        a, b = "m_valid", "(or m_valid h_valid)"
        cases = [(a, a, "equivalent"), (a, b, "strengthened"), (b, a, "weakened"),
                 (a, "h_valid", "incomparable")]
        engine = IncrementalSMT()
        for x, y, expected in cases:
            with self.subTest(x=x, y=y):
                r = engine.compare(x, y, "true")
                self.assertEqual(r["relation"], expected)
                self.assertEqual(fresh_compare(x, y)["relation"], expected)
                self.assertTrue(verify_result(x, y, "true", r))
        self.assertEqual(classify("unknown", "unsat"), "unknown")
        self.assertEqual(classify("unsat", "unknown"), "unknown")

    def test_scope_change_rechecks_same_pair(self):
        a, b = "(eq data_index 4)", "(eq data_index data_n)"
        engine = IncrementalSMT()
        r4 = engine.compare(a, b, "(eq data_n 4)")
        r5 = engine.compare(a, b, "(eq data_n 5)")
        self.assertEqual(r4["relation"], "equivalent")
        self.assertEqual(r5["relation"], "incomparable")
        self.assertEqual(engine.counts["solver_groups"], 2)
        self.assertEqual(engine.counts["direction_checks"], 4)
        self.assertTrue(verify_result(a, b, "(eq data_n 4)", r4))
        self.assertTrue(verify_result(a, b, "(eq data_n 5)", r5))
        with self.assertRaises(ValueError):
            verify_result(a, b, "(eq data_n 5)", r4)
        engine.compare(a, b, "(eq data_n 4)")
        self.assertEqual(engine.counts["direction_checks"], 4)
        self.assertEqual(engine.counts["cache_hits"], 2)

    def test_reverse_and_whitespace_cache_are_safe(self):
        engine = IncrementalSMT()
        a, b = "m_valid", "(or m_valid h_valid)"
        first = engine.compare(a, b)
        reverse = engine.compare("(or   m_valid h_valid)", " m_valid ", " true ")
        self.assertEqual(reverse["relation"], "weakened")
        self.assertEqual(reverse["directions"]["old_only"], first["directions"]["new_only"])
        self.assertEqual(engine.counts["direction_checks"], 2)
        self.assertEqual(engine.counts["guard_checks"], 1)
        self.assertEqual(engine.counts["solver_checks"], 3)
        self.assertEqual(engine.counts["cache_hits"], 2)
        self.assertEqual(engine.counts["guard_cache_hits"], 1)
        first["directions"]["new_only"]["status"] = "unsat"
        self.assertEqual(engine.compare(a, b)["relation"], "strengthened")

    def test_infeasible_guard_not_reported_equivalent(self):
        e = IncrementalSMT()
        for guard in ("(ult m_data 0)", "(ugt m_data 255)", "false"):
            r = e.compare("m_valid", "h_valid", guard)
            self.assertEqual(r["relation"], "infeasible")
            self.assertEqual(r["guard_status"], "unsat")
            self.assertEqual(r["directions"]["old_only"]["status"], "skipped")
            self.assertTrue(verify_result("m_valid", "h_valid", guard, r))
        self.assertEqual(e.counts["direction_checks"], 0)

    def test_receipt_tampering_is_rejected(self):
        a, b, g = "m_valid", "h_valid", "(eq data_n 4)"
        e = IncrementalSMT()
        good = e.compare(a, b, g)
        witness = deepcopy(good)
        witness["directions"]["old_only"]["witness"]["data_n"] = 5
        bad_model = deepcopy(good)
        bad_model["directions"]["new_only"]["witness"]["h_valid"] = False
        bad_bool_type = deepcopy(good)
        bad_bool_type["directions"]["old_only"]["witness"]["m_valid"] = 1
        false_query = deepcopy(good)
        row = false_query["directions"]["old_only"]
        row["smt2"] = false_query["guard_query"]["smt2"]
        row["smt2_sha256"] = sha256(row["smt2"].encode()).hexdigest()
        false_status = deepcopy(good)
        false_status["directions"]["old_only"]["status"] = "unsat"
        false_relation = deepcopy(good)
        false_relation["relation"] = "equivalent"
        for tamper in (witness, bad_model, bad_bool_type, false_query, false_status, false_relation):
            with self.assertRaises(ValueError):
                verify_result(a, b, g, tamper)

    def test_single_direction_fallback(self):
        e = IncrementalSMT()
        a, b = "m_valid", "(or m_valid h_valid)"
        r = e.check_direction(a, b)
        self.assertEqual(r["direction"]["status"], "unsat")
        self.assertTrue(verify_direction(a, b, "true", r))
        self.assertEqual(e.counts["direction_checks"], 1)
        self.assertEqual(e.compare(a, b)["relation"], "strengthened")
        self.assertEqual(e.counts["direction_checks"], 2)
        self.assertEqual(e.counts["cache_hits"], 1)

    def test_invalid_types_and_timeout(self):
        engine = IncrementalSMT()
        for a, b, g in (("(eq m_data data_index)", "true", "true"),
                         ("m_valid", "unknown_signal", "true"),
                         ("true", "true", "(eq m_data 256)")):
            with self.assertRaises(ValueError):
                engine.compare(a, b, g)
        for timeout in (True, 0, -1, 0.5):
            with self.assertRaises(ValueError):
                IncrementalSMT(timeout)


if __name__ == "__main__":
    unittest.main()
