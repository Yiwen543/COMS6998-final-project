"""Universal rule qualification and independent flat proof replay for assertion forms."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from m3_proof_dependencies import ProofChecker, validate_pattern_rules, validate_proof_dependencies


FACTOR = {"name": "factor",
          "left": "(or (and ?a ?b) (and ?a ?c))", "right": "(and ?a (or ?b ?c))"}
COMMUTE = {"name": "commute", "left": "(or ?x ?y)", "right": "(or ?y ?x)"}
CONSTANT = {"name": "not-true", "left": "(not true)", "right": "false"}


class AssertionPatterns(unittest.TestCase):
    def setUp(self):
        # ?a binds an expression, not just a leaf. The second step is a reverse
        # rule in an inner subtree, underneath the application of the first.
        lhs = "(or (and (not a) b) (and (not a) c))"
        rhs = "(and (not a) (or b c))"
        self.rules = [FACTOR, COMMUTE, CONSTANT]
        targets = [{"id": "source", "compact": lhs, "event_context": ["posedge clk"]},
                   {"id": "assertion", "compact": "(and (not a) (or c b))", "event_context": ["posedge clk"]}]
        self.payload = {"targets": targets, "pattern_rules": self.rules, "verified_rules": []}
        edge = {"left": "source", "right": "assertion", "explanation": "\n".join([
            lhs, f"(Rewrite=> factor {rhs})", "(and (not a) (Rewrite<= commute (or c b)))",
        ])}
        self.graph = {
            "targets": [{"id": "source", "eclass_before": 11, "eclass": 20},
                        {"id": "assertion", "eclass_before": 12, "eclass": 20}],
            "rewrite_explanations": [edge], "stop_reason": "Some(Saturated)",
            "ground_rule_count": 0, "pattern_rule_count": len(self.rules),
        }

    def test_universal_and_local_evidence_are_distinct(self):
        self.assertEqual(validate_pattern_rules(self.rules), {"factor": 8, "commute": 4, "not-true": 1})
        audit = validate_proof_dependencies(self.payload, self.graph, pattern_rules=self.rules)
        self.assertEqual(audit["pattern_truth_table_rows"], validate_pattern_rules(self.rules))
        self.assertEqual(audit["pattern_rules"], ["commute", "factor"])
        self.assertEqual(audit["ground_rules"], [])
        self.assertEqual(audit["builtin_rules"], [])
        self.assertEqual(audit["edges"][0]["steps"], [
            {"rule": "factor", "direction": "forward", "path": []},
            {"rule": "commute", "direction": "reverse", "path": [1]},
        ])

    def test_reject_false_and_non_generic_before_replaying_any_proofs(self):
        for rule in [dict(FACTOR, right="(and ?a (and ?b ?c))"),
                     dict(COMMUTE, left="(or ?x (not ?x))", right="true"),  # unmatched reverse variable
                     dict(COMMUTE, left="foo", right="foo"),                # literal design atom
                     dict(CONSTANT, right="(Rewrite=> fake false)"),       # assertion as rule
                     dict(COMMUTE, right="(xor ?x ?y)"),
                     dict(COMMUTE, name="x y"), dict(COMMUTE, left=False)]:
            with self.subTest(rule=rule), self.assertRaises(ValueError):
                validate_pattern_rules([rule])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_pattern_rules([FACTOR, FACTOR])

    def test_only_supplied_inventory_is_active(self):
        with self.assertRaisesRegex(ValueError, "inventory"):
            validate_proof_dependencies(self.payload, self.graph, pattern_rules=[FACTOR])
        with self.assertRaisesRegex(ValueError, "inventory"):
            validate_proof_dependencies(self.payload, self.graph)
        with self.assertRaisesRegex(ValueError, "pattern rule count"):
            validate_proof_dependencies(self.payload, dict(self.graph, pattern_rule_count=5), pattern_rules=self.rules)
        p = dict(self.payload, verified_rules=[dict(name="x", left="x", right="y", proof_status="unsat")])
        with self.assertRaisesRegex(ValueError, "ground rules"):
            ProofChecker(p, pattern_rules=self.rules)
        edge = deepcopy(self.graph["rewrite_explanations"][0])
        edge["explanation"] = edge["explanation"].replace("Rewrite=> factor", "Rewrite=> de-morgan-or")
        with self.assertRaisesRegex(ValueError, "unknown or inapplicable"):
            ProofChecker(self.payload, pattern_rules=self.rules).check(edge)

    def test_missing_scope_or_typed_context_mismatch_is_rejected(self):
        p = deepcopy(self.payload)
        for t in p["targets"]:
            t.pop("event_context")
        with self.assertRaisesRegex(ValueError, "explicit event contexts"):
            validate_proof_dependencies(p, self.graph, pattern_rules=self.rules)
        # Python's numeric equality would otherwise consider these identical.
        for t, v in zip(p["targets"], [True, 1], strict=True):
            t["event_context"] = {"sample": v}
        with self.assertRaisesRegex(ValueError, "ineligible proof endpoints"):
            validate_proof_dependencies(p, self.graph, pattern_rules=self.rules)

    def test_no_variable_capture_cross_step_or_event(self):
        # A different second occurrence of ?a invalidates the factorization.
        p, g = deepcopy(self.payload), deepcopy(self.graph)
        old = p["targets"][0]["compact"]
        new = old.replace("(and (not a) c)", "(and a c)")
        p["targets"][0]["compact"] = new
        e = g["rewrite_explanations"][0]
        e["explanation"] = e["explanation"].replace(old + "\n", new + "\n")
        with self.assertRaisesRegex(ValueError, "does not justify"):
            validate_proof_dependencies(p, g, pattern_rules=self.rules)
        e["explanation"] = self.graph["rewrite_explanations"][0]["explanation"].replace(
            "(or b c)))\n", "(or b c)))\nfalse\n")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            ProofChecker(self.payload, pattern_rules=self.rules).check(e)
        p = deepcopy(self.payload)
        p["targets"][1]["event_context"] = ["negedge clk"]
        with self.assertRaisesRegex(ValueError, "crosses event contexts"):
            ProofChecker(p, pattern_rules=self.rules).check(self.graph["rewrite_explanations"][0])


if __name__ == "__main__":
    unittest.main()
