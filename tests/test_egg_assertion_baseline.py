import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_assertion_baseline import canonical_key, compare, term_search, truth_table, verify_path


DIST = {"name": "factor", "left": "(and ?a (or ?b ?c))", "right": "(or (and ?a ?b) (and ?a ?c))"}
COMM = {"name": "comm-and", "left": "(and ?a ?b)", "right": "(and ?b ?a)"}
DOUBLE = {"name": "double-not", "left": "(not (not ?a))", "right": "?a"}


class OrdinaryAssertionBaselines(unittest.TestCase):
    def test_canonical_simplifies_without_distribution(self):
        self.assertEqual(canonical_key("(and ready (and valid ready))"), canonical_key("(and valid ready)"))
        self.assertEqual(canonical_key("(not (and a b))"), canonical_key("(or (not b) (not a))"))
        self.assertEqual(canonical_key("(or a (and b a))"), "a")
        result = compare("(and valid (or ready flush))", "(or (and valid ready) (and valid flush))", [DIST])
        self.assertFalse(result["canonical"]["proved"])
        self.assertTrue(result["search"]["proved"])
        self.assertEqual(result["oracle"]["unequal_assignments"], 0)

    def test_reverse_nested_rule_has_exact_context_and_direction(self):
        left = "(not (or (and valid ready) (and valid flush)))"
        right = "(not (and valid (or ready flush)))"
        result = term_search(left, right, [DIST], budget=2)
        step, = result["steps"]
        self.assertEqual((step["direction"], step["path"]), ("reverse", [0]))
        self.assertTrue(verify_path(left, right, [DIST], [step]))
        with self.assertRaises(ValueError):
            verify_path(left, right, [DIST], [{**step, "path": []}])

    def test_budget_and_size_exhaustion_remain_inconclusive(self):
        left, right = "(and (not (not a)) b)", "(and b a)"
        result = compare(left, right, [COMM, DOUBLE], budget=2)
        self.assertFalse(result["search"]["proved"])
        self.assertEqual(result["search"]["stop_reason"], "term_budget")
        self.assertTrue(result["oracle"]["equivalent"])
        proof = term_search(left, right, [COMM, DOUBLE], budget=100)
        self.assertTrue(proof["proved"])
        self.assertTrue(verify_path(left, right, [COMM, DOUBLE], proof["steps"]))
        self.assertEqual(term_search(left, right, [COMM, DOUBLE], max_term_nodes=2)["stop_reason"], "term_size")

    def test_oracle_counts_every_failure_and_skips_unbounded_inputs(self):
        result = truth_table("(and valid (not ready))", "valid")
        self.assertFalse(result["equivalent"])
        self.assertEqual((result["checked_assignments"], result["unequal_assignments"]), (4, 1))
        self.assertEqual(result["counterexample"], {"valid": True, "ready": True})
        self.assertEqual((result["left_value"], result["right_value"]), (False, True))
        limited = truth_table("a", "b", max_atoms=1)
        self.assertIsNone(limited["equivalent"])
        self.assertIsNone(limited["unequal_assignments"])

    def test_repeated_variable_and_rejected_rule(self):
        idem = {"name": "idem", "left": "(and ?x ?x)", "right": "?x"}
        self.assertFalse(compare("(and a b)", "a", [idem], budget=6)["search"]["proved"])
        with self.assertRaisesRegex(ValueError, "unverified Boolean rewrite"):
            term_search("a", "(not a)", [{"name":"wrong", "left":"?x", "right":"(not ?x)", "proof_status":"unsat"}])
