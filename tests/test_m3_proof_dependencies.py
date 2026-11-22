"""Negative controls for extracting dependencies from a proof that actually checks."""
import copy
import itertools
import json
import subprocess
import tempfile
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from m3_proof_dependencies import BUILTINS, ProofChecker, validate_proof_dependencies
from predicates import evaluate, parse


class FlatProofs(unittest.TestCase):
    def setUp(self):
        self.first = "(or (and x true) (not false))"
        self.last = "(or (and true z) true)"
        self.lines = [
            self.first,
            "(or (Rewrite=> and-true x) (not false))",
            "(or x (Rewrite=> not-false true))",
            "(or (Rewrite<= and-true-left (and true x)) true)",
            "(or (and true (Rewrite=> x-alias z)) true)",
        ]
        self.payload = {
            "targets": [{"id": name, "compact": expr, "event_context": ["posedge"]}
                        for name, expr in (("g0", self.first), ("g1", self.last))],
            "verified_rules": [{"name": "x-alias", "left": "x", "right": "z",
                                "event_context": ["posedge"], "proof_status": "unsat"}],
        }
        self.edge = {"left": "g0", "right": "g1", "explanation": "\n".join(self.lines)}
        self.graph = {
            "targets": [{"id": "g0", "eclass_before": 3, "eclass": 7},
                        {"id": "g1", "eclass_before": 5, "eclass": 7}],
            "rewrite_explanations": [self.edge], "ground_rule_count": 1, "stop_reason": "Some(Saturated)",
        }

    def test_checked_nested_forward_and_reverse_dependencies(self):
        result = validate_proof_dependencies(self.payload, self.graph)
        self.assertEqual(result["ground_rules"], ["x-alias"])
        self.assertEqual(result["builtin_rules"], ["and-true", "and-true-left", "not-false"])
        self.assertEqual(result["checked_steps"], 4)
        steps = result["edges"][0]["steps"]
        self.assertEqual([s["path"] for s in steps], [[0], [1], [0], [0, 1]])
        self.assertEqual([s["direction"] for s in steps], ["forward", "forward", "reverse", "forward"])

    def test_builtin_schemas_are_true_for_all_boolean_instantiations(self):
        for name, sides in BUILTINS.items():
            lhs, rhs = (parse(side.replace("?a", "a").replace("?b", "b")) for side in sides)
            for a, b in itertools.product((False, True), repeat=2):
                with self.subTest(rule=name, a=a, b=b):
                    env = {"a": a, "b": b}
                    self.assertEqual(evaluate(lhs, env), evaluate(rhs, env))

    def test_all_six_builtin_patterns_work_in_each_direction(self):
        for name, (lhs, rhs) in BUILTINS.items():
            lhs, rhs = (v.replace("?a", "x").replace("?b", "y") for v in (lhs, rhs))
            for direction, (old, new) in (("=>", (lhs, rhs)), ("<=", (rhs, lhs))):
                p = {"targets": [{"id": 0, "compact": old}, {"id": 1, "compact": new}], "verified_rules": []}
                e = {"left": 0, "right": 1, "explanation": f"{old}\n(Rewrite{direction} {name} {new})"}
                with self.subTest(name=name, direction=direction):
                    self.assertEqual(ProofChecker(p).check(e)["builtin_rules"], [name])

    def test_bad_or_misplaced_step_is_rejected(self):
        bad_steps = [
            "(or x (not false))",  # missing attribution
            "(or (Rewrite=> wrong x) (not false))",
            "(or (Rewrite=> and-true) (not false))",  # missing expression
            "(or (Rewrite<= and-true x) (not false))",  # wrong direction
            "(or (Rewrite=> and-true y) (not false))",  # unrelated substitution
            "(or (Rewrite=> and-true x) true)",  # changes an unmarked sibling
            "(or (Rewrite=> and-true x) (Rewrite=> not-false true))",
            "(or (Rewrite=> and-true (Rewrite=> and-true x)) (not false))",
            "(or (Rewrite=> and-true x) (not false) extra)",
            "(or (Rewrite=> and-true x) (not false)",
        ]
        checker = ProofChecker(self.payload)
        for step in bad_steps:
            with self.subTest(step=step), self.assertRaises(ValueError):
                checker.check({**self.edge, "explanation": "\n".join([self.lines[0], step, *self.lines[2:]])})

    def test_withdrawal_context_and_endpoint_binding(self):
        checker = ProofChecker(self.payload)
        with self.assertRaisesRegex(ValueError, "withdrawn"):
            checker.check(self.edge, allowed_ground_rules=set())
        ctx = copy.deepcopy(self.payload)
        ctx["verified_rules"][0]["event_context"] = ["negedge"]
        with self.assertRaisesRegex(ValueError, "inapplicable"):
            ProofChecker(ctx).check(self.edge)
        with self.assertRaisesRegex(ValueError, "end of proof"):
            checker.check({**self.edge, "explanation": "\n".join(self.lines[:-1])})
        with self.assertRaisesRegex(ValueError, "start of proof"):
            checker.check({**self.edge, "explanation": self.edge["explanation"].replace(self.first, "false", 1)})
        with self.assertRaisesRegex(ValueError, "connectivity"):
            validate_proof_dependencies(self.payload, {**self.graph, "rewrite_explanations": []})

    def test_cli_filters_use_checked_edges_in_stored_orientation(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            # Numeric IDs also survive CLI round-tripping. String guard names
            # use the same path for both args when filtering via rule name.
            p, g = copy.deepcopy(self.payload), copy.deepcopy(self.graph)
            for i in range(2):
                p["targets"][i]["id"] = i
                g["targets"][i]["id"] = i
            g["rewrite_explanations"][0].update(left=0, right=1)
            (d / "input.json").write_text(json.dumps(p))
            (d / "graph.json").write_text(json.dumps(g))
            command = [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts/m3_proof_dependencies.py"),
                       "--input", str(d / "input.json"), "--graph", str(d / "graph.json")]

            def run(*args):
                return subprocess.run([*command, *args], text=True, capture_output=True)

            for opts in [("--using-rule", "x-alias"), ("--using-rule", "not-false"), ("--edge", "1", "0")]:
                result = run(*opts)
                self.assertEqual(result.returncode, 0, result.stderr)
                row = json.loads(result.stdout)
                self.assertEqual((row["stored_edges_checked"], row["matching_edges"]), (1, 1))
                self.assertEqual([row["matches"][0][k] for k in ("left", "right")], [0, 1])
            self.assertEqual(json.loads(run("--using-rule", "de-morgan-or").stdout)["matching_edges"], 0)
            self.assertNotEqual(run("--using-rule", "absent").returncode, 0)
            self.assertNotEqual(run("--edge", "0", "absent").returncode, 0)
            self.assertNotEqual(run("--edge", "0", "1", "--using-rule", "x-alias").returncode, 0)
            g["rewrite_explanations"][0]["explanation"] = "irrelevant"
            (d / "graph.json").write_text(json.dumps(g))
            self.assertNotEqual(run("--using-rule", "de-morgan-or").returncode, 0)

    def test_ambiguous_names_or_uncertified_ground_rules(self):
        for change in ({"name": "double-not"}, {"proof_status": "unknown"}, {"left": "?a"}):
            p = copy.deepcopy(self.payload)
            p["verified_rules"][0].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                ProofChecker(p)


if __name__ == "__main__":
    unittest.main()
