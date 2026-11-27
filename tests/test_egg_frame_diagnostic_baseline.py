import itertools
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_frame_diagnostic_baseline import dnf, evaluate_clause, evaluate_dnf, minimum_cube, parse_dnf
from egg_frame_terms import REFERENCES, abstract, parse_term
from predicates import evaluate, parse


class DiagnosticBaselines(unittest.TestCase):
    def test_push_negation_distribute_and_prune(self):
        source = "(not (or (not armed) (and valid ready)))"
        expected = ((("armed", True), ("ready", False)), (("armed", True), ("valid", False)))
        self.assertEqual(dnf(source), expected)
        redundant = "(or (or (and a b) (and b a)) (or a (and x (not x))))"
        self.assertEqual(dnf(redundant), ((("a", True),),))
        self.assertEqual(dnf("(and (not false) (or true x))"), ((),))
        self.assertEqual(dnf("(and a (and b (not a)))"), ())

    def test_claimed_dnf_must_already_have_valid_grammar(self):
        ok = "(or (and armed (not ready)) (and (and valid valid) changed))"
        self.assertEqual(parse_dnf(ok), dnf(ok))
        for s in ("(and a (or b c))", "(not (not a))", "(not (and a b))",
                  "(or true (and a (or b c)))", "(xor a b)", ")", "(or a)"):
            with self.subTest(s=s), self.assertRaises(ValueError):
                parse_dnf(s)

    def test_partial_rows_never_assume_unknowns(self):
        s = "(or (and a b) (and a (not b)))"
        for unknown in (None, -1):
            sampled = {"a": 1, "b": unknown}
            self.assertIsNone(evaluate_clause(dnf(s)[0], sampled))
            self.assertIsNone(evaluate_dnf(dnf(s), sampled))
            answer = minimum_cube(s, sampled)
            self.assertEqual(answer["cube"], (("a", True),))
            self.assertEqual((answer["consistent_assignments"], answer["positive_assignments"]), (2, 2))
            self.assertEqual(minimum_cube("(and a b)", sampled)["status"], "unknown")
        self.assertEqual(minimum_cube(s, {"a": 0})["status"], "false")
        self.assertEqual(minimum_cube("(or a (not a))", {})["cube"], ())
        self.assertEqual(minimum_cube("true", {})["size"], 0)
        self.assertIsNone(minimum_cube("false", {})["cube"])
        with self.assertRaises(ValueError):
            minimum_cube(s, {"a": 7})

    def test_exact_smallest_certificate_and_tie_break(self):
        # Compare all positive and partial assignments against direct completion enumeration.
        names = ("a", "b", "c", "d")
        source = "(or (and a b) (or (and (not a) c) d))"
        tree = parse(source)
        rows = [(values, evaluate(tree, dict(zip(names, values)))) for values in itertools.product((False, True), repeat=4)]
        for values in itertools.product((False, True, None), repeat=4):
            sampled = dict(zip(names, values))
            known = [i for i, v in enumerate(values) if v is not None]
            all_subsets = itertools.chain.from_iterable(itertools.combinations(known, n) for n in range(len(known) + 1))
            expected = next((tuple((names[i], values[i]) for i in subset) for subset in all_subsets
                             if all(outcome for row, outcome in rows if all(row[i] == values[i] for i in subset))), None)
            self.assertEqual(minimum_cube(source, sampled)["cube"], expected)
        self.assertEqual(minimum_cube("(or z a)", {"z": True, "a": True})["cube"], (("a", True),))

    def test_12_atom_limit_has_no_optimistic_status(self):
        source = "a0"
        for i in range(1, 12):
            source = f"(and {source} a{i})"
        values = {f"a{i}": True for i in range(13)}
        answer = minimum_cube(source, values)
        self.assertEqual((answer["size"], answer["atom_count"]), (12, 12))
        result = minimum_cube(f"(and {source} a12)", values)
        self.assertEqual(result["status"], "atom_limit")
        self.assertIsNone(result["cube"])

    def test_dnf_matches_original_frame_projection_on_all_independent_rows(self):
        for name, formula in REFERENCES.items():
            source, atoms = abstract(parse_term(formula))
            clauses = dnf(source)
            tree = parse(source)
            for values in itertools.product((False, True), repeat=len(atoms)):
                row = dict(zip(atoms, values))
                self.assertEqual(evaluate_dnf(clauses, row), evaluate(tree, row), name)
