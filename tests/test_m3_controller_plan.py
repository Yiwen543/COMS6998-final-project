"""Regression controls for which finite Controller obligations can share a solve."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from benchmark_m3_controller import plan, structural_keys


def target(id_, expression, scope="dut.left", event="posedge", original_event="left.clk"):
    return {"id": id_, "compact": expression, "instance_scope": scope,
            "event_context": [event], "original_event_context": [original_event]}


class ControllerPlanning(unittest.TestCase):
    def test_ground_aliases_congruence_and_builtin(self):
        targets = [target("a", "(and (not (not c)) true)"), target("b", "a"),
                   target("c", "(and z c)"), target("d", "(and z a)"), target("e", "(and a z)")]
        # The third RHS must remain in the same explicit equality component.
        rules = [dict(name="first", left="b", right="a", proof_status="unsat"),
                 dict(name="second", left="b", right="c", proof_status="unsat")]
        keys = structural_keys({"targets": targets, "verified_rules": rules})
        grouped = [[t["id"] for t in g] for g in plan(targets, keys)]
        self.assertEqual(grouped, [["a", "b"], ["c", "d"], ["e"]])

    def test_incompatible_observer_context_never_shares(self):
        targets = [target("a", "x"), target("b", "x", scope="dut.right"),
                   target("c", "x", event="combinational"), target("d", "x", original_event="right.clk")]
        self.assertEqual(len(plan(targets, ["same"] * len(targets))), 4)


if __name__ == "__main__":
    unittest.main()
