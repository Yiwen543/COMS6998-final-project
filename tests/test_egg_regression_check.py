"""Multi-target proof audit, with rejection of mixed scopes and unrequested edges."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_regression_check import check_graph, GOAL_STOP, PATTERN_RULES, SATURATED


def fact(context, left, right):
    digest = sha256(json.dumps([context, left, right], separators=(",", ":")).encode()).hexdigest()[:24]
    return {"name": "ctx-" + digest, "left": left, "right": right,
            "proof_status": "unsat", "event_context": context}


def payload(terms, pairs, *, context="scope-A", facts=()):
    return {"context_id": context, "targets": [{"id": name, "compact": term, "event_context": context}
            for name, term in terms.items()], "pattern_rules": deepcopy(PATTERN_RULES),
            "ground_rules": list(facts), "pairs": pairs}


def edge(a, b, explanation):
    return {"left": a, "right": b, "explanation": explanation}


def graph(request, classes, edges, *, before=None, stop=SATURATED):
    if before is None:
        before = list(range(len(classes)))
    return {"context_id": request["context_id"], "engine": "egg 0.11.0", "stop_reason": stop,
            "iterations": 1, "enodes": 8, "eclasses": 5, "pattern_rule_count": 23,
            "ground_rule_count": len(request["ground_rules"]), "targets": [
                {"id": row["id"], "eclass_before": a, "eclass": b}
                for row, a, b in zip(request["targets"], before, classes, strict=True)],
            "rewrite_explanations": edges}


class RegressionGraphTests(unittest.TestCase):
    def setUp(self):
        self.fact1 = fact("scope-A", "a", "b")
        self.fact2 = fact("scope-A", "b", "c")
        self.request = payload({"a": "a", "b": "b", "c": "c", "d": "d"},
                               [["a", "c"], ["c", "b"], ["c", "d"]], facts=[self.fact1, self.fact2])
        self.edges = [edge("a", "c", f"a\n(Rewrite=> {self.fact1['name']} b)\n(Rewrite=> {self.fact2['name']} c)"),
                      edge("c", "b", f"c\n(Rewrite<= {self.fact2['name']} b)")]
        self.graph = graph(self.request, [0, 0, 0, 3], self.edges)

    def test_partial_results_and_per_pair_dependencies(self):
        checked = check_graph(self.request, self.graph)
        self.assertEqual(set(checked), {("a", "c"), ("c", "b"), ("c", "d")})
        self.assertTrue(checked["a", "c"]["proved"])
        self.assertEqual(checked["a", "c"]["used_ground_rules"], sorted([self.fact1["name"], self.fact2["name"]]))
        self.assertEqual(checked["c", "b"]["used_ground_rules"], [self.fact2["name"]])
        self.assertEqual(checked["c", "d"]["status"], "saturated_miss")
        self.assertFalse(checked["c", "d"]["proved"])

    def test_shared_ground_inventory_without_auxiliary_target(self):
        request = payload({"left": "a", "right": "c"}, [["left", "right"]], facts=[self.fact1, self.fact2])
        proof = edge("left", "right", self.edges[0]["explanation"])
        checked = check_graph(request, graph(request, [0, 0], [proof], stop=GOAL_STOP))
        self.assertTrue(checked["left", "right"]["proved"])
        stale = deepcopy(request)
        stale["context_id"] = "scope-B"
        for t in stale["targets"]: t["event_context"] = "scope-B"
        with self.assertRaisesRegex(ValueError, "wrong context"):
            check_graph(stale, None)
        for f in stale["ground_rules"]: f["event_context"] = "scope-B"
        with self.assertRaisesRegex(ValueError, "fact name"):
            check_graph(stale, None)

    def test_unrequested_or_missing_edges_rejected(self):
        for edges in [self.edges[:1], [*self.edges, edge("a", "b", "a\n(Rewrite=> whatever b)")],
                      [*self.edges, self.edges[0]], [*self.edges[:1], edge("b", "c", "b\n(Rewrite=> whatever c)")]]:
            with self.subTest(edges=edges), self.assertRaises(ValueError):
                check_graph(self.request, graph(self.request, [0, 0, 0, 3], edges))
        with self.assertRaisesRegex(ValueError, "goal stop"):
            check_graph(self.request, graph(self.request, [0, 0, 0, 3], self.edges, stop=GOAL_STOP))
        with self.assertRaisesRegex(ValueError, "unknown rewrite"):
            broken = deepcopy(self.graph)
            broken["rewrite_explanations"][1]["explanation"] = "c\n(Rewrite<= fake b)"
            check_graph(self.request, broken)

    def test_nonidentical_target_before_class_not_trusted(self):
        with self.assertRaisesRegex(ValueError, "initial structural identity"):
            check_graph(self.request, graph(self.request, [0, 0, 0, 3], self.edges, before=[1, 1, 2, 3]))
        identity = payload({"x0": "(and a b)", "x1": "(and a b)", "y": "a"}, [["x0", "x1"]])
        good = graph(identity, [1, 1, 3], [], before=[1, 1, 3], stop=GOAL_STOP)
        row = check_graph(identity, good)["x0", "x1"]
        self.assertEqual(row["status"], "structural_identity")
        with self.assertRaisesRegex(ValueError, "split"):
            check_graph(identity, graph(identity, [1, 2, 3], [], before=[1, 1, 3]))

    def test_non_graph_and_bad_pairs_ground_shape(self):
        self.assertFalse(any(row["proved"] for row in check_graph(self.request, None).values()))
        for pairs in [[['a','c'],['c','a']], [['x','a']], [['a','a']], []]:
            bad = {**self.request, "pairs": pairs}
            with self.assertRaises(ValueError):
                check_graph(bad, None)
        for invalid in [fact("scope-A", "true", "b"), fact("scope-A", "a", "(not true)"),
                        fact("scope-A", "a", "(or b c)"), fact("scope-A", "and", "b"),
                        {**self.fact1, "proof_status": "sat"}]:
            with self.assertRaises(ValueError):
                check_graph({**self.request, "ground_rules": [invalid]}, None)

    @unittest.skipUnless(os.environ.get("EGG_REGRESSION_BINARY"), "set EGG_REGRESSION_BINARY for native proof")
    def test_native_multiple_edges_and_distinct_pair(self):
        proc = subprocess.run([os.environ["EGG_REGRESSION_BINARY"]], text=True, input=json.dumps(self.request),
                              capture_output=True, check=True, timeout=20)
        checked = check_graph(self.request, json.loads(proc.stdout))
        self.assertEqual([row["proved"] for row in checked.values()], [True, True, False])
        self.assertEqual(checked["a", "c"]["used_ground_rules"], sorted([self.fact1["name"], self.fact2["name"]]))
        request = payload({"left": "a", "right": "c"}, [["left", "right"]], facts=[self.fact1, self.fact2])
        proc = subprocess.run([os.environ["EGG_REGRESSION_BINARY"]], text=True, input=json.dumps(request),
                              capture_output=True, check=True, timeout=20)
        self.assertTrue(check_graph(request, json.loads(proc.stdout))["left", "right"]["proved"])


if __name__ == "__main__":
    unittest.main()
