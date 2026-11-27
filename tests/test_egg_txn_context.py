"""Controls for guard selection, scoped primitive discovery and the complete ordinary solver."""
from copy import deepcopy
from importlib.util import find_spec
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
if find_spec("z3"):
    from egg_txn_context import certify_facts, contexts, ordinary, prepare, verify_facts, verify_partition


@unittest.skipUnless(find_spec("z3"), "requires z3-solver")
class ContextEvidence(unittest.TestCase):
    def test_substitution_needs_a_boundary_guard(self):
        sources = ("(and (eq data_n 4) (eq data_index data_n))", "(and (eq data_n 4) (eq data_index 4))")
        p = prepare(*sources)
        full = contexts(*sources, split=False)
        single = full["contexts"][0]
        self.assertIs(verify_partition(full, p), True)
        self.assertEqual(ordinary(p, single, certify_facts(p, single))["status"], "sat")
        plan = contexts(*sources, split=True)
        self.assertEqual(plan["threshold"], {"variable": "data_n", "width": 16, "value": 4})
        for ctx in plan["contexts"]:
            f = certify_facts(p, ctx)
            self.assertIs(verify_facts(p, ctx, f), True)
            self.assertTrue(ordinary(p, ctx, f)["equivalent"])
        equal = plan["contexts"][1]
        alias = certify_facts(p, equal)
        self.assertTrue(any(x["right"].startswith("bv_") for x in alias["facts"]))
        with self.assertRaises(ValueError):
            verify_facts(p, plan["contexts"][2], alias)
        altered = deepcopy(alias)
        altered["counts"]["constant_queries"] += 1
        with self.assertRaises(ValueError):
            verify_facts(p, equal, altered)

    def test_byte_extremes_are_vacuous_only_in_the_empty_region(self):
        for limit, index in ((0, 0), (255, 2)):
            sources = (f"(and (eq m_data {limit}) (eq data_byte m_data))",
                       f"(and (eq m_data {limit}) (eq data_byte {limit}))")
            p, plan = prepare(*sources), contexts(*sources, split=True)
            self.assertEqual(plan["threshold"]["width"], 8)
            self.assertEqual([i for i, ctx in enumerate(plan["contexts"]) if ctx["feasibility"]["status"] == "unsat"],
                             [index])
            ctx = plan["contexts"][index]
            f = certify_facts(p, ctx)
            self.assertEqual(f["facts"], [])
            self.assertTrue(ordinary(p, ctx, f)["vacuous"])
            without = deepcopy(plan)
            without["contexts"].pop(index)
            with self.assertRaises(ValueError):
                verify_partition(without, p)

    def test_complement_is_certified_but_standalone_endpoints_excluded(self):
        # Values less than four complement values at least four across the entire 16-bit word.
        lhs, rhs = "(and m_valid (ult data_n 4))", "(and m_valid (not (uge data_n 4)))"
        p, ctx = prepare(lhs, rhs), contexts(lhs, rhs, split=False)["contexts"][0]
        f = certify_facts(p, ctx)
        self.assertTrue(any(rule["right"].startswith("(not bv_") for rule in f["facts"]))
        self.assertEqual(ordinary(p, ctx, f)["status"], "unsat")
        for lhs, rhs in (("(ult data_n 4)", "(ule data_n 3)"), ("(uge m_data 0)", "true"),
                         ("(ult m_data 0)", "true")):
            p, ctx = prepare(lhs, rhs), contexts(lhs, rhs, split=False)["contexts"][0]
            f = certify_facts(p, ctx)
            self.assertEqual(f["facts"], [])
            self.assertGreater(f["counts"]["skipped_direct_pairs"], 0)


if __name__ == "__main__":
    unittest.main()
