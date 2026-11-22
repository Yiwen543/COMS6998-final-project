"""Independent ordinary-forest controls; rule names here are hypothetical equalities."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from m3_controller_basis import forest_basis


class BasisControls(unittest.TestCase):
    def test_later_child_merge_makes_earlier_parent_rule_redundant(self):
        expressions = ["(or a b)", "(or a c)", "b", "c", "(and true b)"]
        targets = [{"id": str(i), "compact": expr} for i, expr in enumerate(expressions)]
        rules = [{"name": name, "source_ids": [str(i), str(j)]}
                 for name, i, j in [("parent", 0, 1), ("child", 2, 3), ("boolean_identity", 2, 4)]]
        names, initial = forest_basis({"targets": targets, "verified_rules": rules})
        self.assertEqual(initial, 2)
        self.assertEqual(names, ["child"])

    def test_parent_equalities_do_not_imply_child_equalities(self):
        targets = [{"id": str(i), "compact": s} for i, s in enumerate(
            ["(and a b)", "(and a c)", "b", "c", "(or x b)", "(or x c)"])]
        rules = [{"name": name, "source_ids": [str(i), str(j)]} for name, i, j in
                 [("parents", 0, 1), ("other_parents", 4, 5)]]
        names, _ = forest_basis({"targets": targets, "verified_rules": rules})
        self.assertEqual(names, ["parents", "other_parents"])
