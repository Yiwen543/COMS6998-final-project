"""Tamper cases for the run-level independent receipt audit (small synthetic fixture)."""
from copy import deepcopy
import gzip
from importlib.util import find_spec
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
if find_spec("z3"):
    from audit_egg_regression import audit
    import run_egg_regression as runner
    from egg_regression_check import check_graph, SATURATED


def case(ident, round_no, left, right, relation, guard="true"):
    return {"id": ident, "round": round_no, "cohort": "synthetic_audit_fixture", "property": "fixture",
            "left": left, "right": right, "guard": guard, "expected_relation": relation}


def fixture_workload():
    # Explicitly authored test inputs; not part of the scientific workload.
    a, b = "(not (not rst))", "rst"
    return [case("a", 0, a, b, "equivalent"),
            case("b", 0, b, "(or rst m_valid)", "strengthened"),
            case("c", 1, a, b, "equivalent"),
            case("d", 2, b, b, "equivalent"),
            case("e", 3, a, b, "equivalent", "(eq data_n 4)")]


def fixture_invoke(request, _binary, _time_counter, _arm):
    # A handcrafted flat explanation exercises independent replay without
    # requiring Cargo in unit tests. Never used for experimental runs.
    by_id = {r["id"]: r["compact"] for r in request["targets"]}
    initial = {name: i for i, name in enumerate(by_id)}
    classes = dict(initial)
    edges = []
    for a, b in request["pairs"]:
        if (by_id[a], by_id[b]) == ("(not (not rst))", "rst"):
            classes[a] = classes[b]
            edges.append({"left": a, "right": b,
                          "explanation": "(not (not rst))\n(Rewrite=> double-not rst)"})
    graph = {"engine": "egg 0.11.0", "context_id": request["context_id"],
             "stop_reason": SATURATED, "iterations": 1, "enodes": 11,
             "eclasses": len(set(classes.values())), "pattern_rule_count": len(request["pattern_rules"]),
             "ground_rule_count": len(request["ground_rules"]),
             "targets": [{"id": k, "eclass_before": initial[k], "eclass": classes[k]} for k in by_id],
             "rewrite_explanations": edges}
    return graph, check_graph(request, graph)


@unittest.skipUnless(find_spec("z3"), "requires z3")
class RegressionAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.base = Path(cls.tmp.name)
        cls.archive = cls.base / "unused-source"
        cls.archive.write_text("small synthetic fixture, not a model archive", encoding="utf8")
        cls.run_dir = cls.base / "run"
        with patch.object(runner, "workload", return_value=fixture_workload()), \
                patch.object(runner, "invoke", side_effect=fixture_invoke):
            runner.run(cls.archive, cls.archive, cls.run_dir)
        with gzip.open(cls.run_dir / "groups.jsonl.gz", "rt", encoding="utf8") as stream:
            cls.groups = [json.loads(line) for line in stream]

    def copy_run(self, name, groups=None, *, summary_edit=None, store_edit=None):
        p = self.base / name
        p.mkdir()
        for fname in ("protocol.json", "summary.json", "proof_store.json"):
            source = json.loads((self.run_dir / fname).read_text(encoding="utf8"))
            if fname == "summary.json" and summary_edit:
                summary_edit(source)
            if fname == "proof_store.json" and store_edit:
                store_edit(source)
            (p / fname).write_text(json.dumps(source), encoding="utf8")
        with gzip.open(p / "groups.jsonl.gz", "wt", encoding="utf8") as stream:
            for group in self.groups if groups is None else groups:
                stream.write(json.dumps(group) + "\n")
        return p

    def check(self, run_dir):
        with patch("audit_egg_regression.workload", return_value=fixture_workload()):
            return audit(run_dir, self.archive)

    def test_clean_and_prior_only_reuse(self):
        result = self.check(self.run_dir)
        self.assertTrue(result["complete"])
        self.assertEqual(result["requests"], 5)
        self.assertEqual(result["proof_store_entries"], 1)
        self.assertEqual(result["native_reruns"], 0)
        self.assertEqual(result["cohorts"]["all"]["arms"]["shared_egg"]["reuse_lookup"],
                         {"miss": 2, "reused": 1, "identity": 1, "revalidated": 1})
        self.assertEqual(result["typed_operational_counts"]["ordinary"]["direction_checks"], 1)

    def test_reject_future_edge_and_changed_scope(self):
        bad = deepcopy(self.groups)
        # This path really is valid in round 1, but no stored proof exists in
        # round 0 before the native graph is supposed to be run.
        bad[0]["requests"][0]["arms"]["shared_egg"]["reuse"] = deepcopy(
            bad[1]["requests"][0]["arms"]["shared_egg"]["reuse"])
        with self.assertRaisesRegex(ValueError, "unknown prior proof"):
            self.check(self.copy_run("future", bad))
        bad = deepcopy(self.groups)
        bad[3]["requests"][0]["arms"]["shared_egg"]["reuse"] = deepcopy(
            bad[1]["requests"][0]["arms"]["shared_egg"]["reuse"])
        with self.assertRaisesRegex(ValueError, "path edge differs"):
            self.check(self.copy_run("stale_scope", bad))

    def test_reject_missing_direction(self):
        bad = deepcopy(self.groups)
        bad[0]["requests"][1]["arms"]["ordinary"]["typed_directions"] = {}
        with self.assertRaisesRegex(ValueError, "wrong hybrid fallback direction"):
            self.check(self.copy_run("missing_direction", bad))

    def test_reject_substituted_endpoint_and_forged_oracle(self):
        bad = deepcopy(self.groups)
        bad[0]["pairwise_graphs"][0]["payload"]["targets"][0]["compact"] = "h_valid"
        with self.assertRaisesRegex(ValueError, "detached from exact request"):
            self.check(self.copy_run("wrong_endpoint", bad))
        bad = deepcopy(self.groups)
        receipt = bad[0]["requests"][1]["oracle"]["directions"]["new_only"]
        receipt["witness"]["rst"] = True # cannot be a new-only witness
        with self.assertRaisesRegex(ValueError, "does not replay"):
            self.check(self.copy_run("forged_witness", bad))

    def test_reject_missing_graph_or_tampered_metrics_store(self):
        bad = deepcopy(self.groups)
        bad.pop()
        with self.assertRaisesRegex(ValueError, "missing expected group"):
            self.check(self.copy_run("missing_group", bad))
        def corrupt_metrics(s):
            s["graphs"]["pairwise_egg"]["graphs"] += 1
        with self.assertRaisesRegex(ValueError, "graph accounting"):
            self.check(self.copy_run("bad_count", summary_edit=corrupt_metrics))
        with self.assertRaisesRegex(ValueError, "proof inventory"):
            self.check(self.copy_run("bad_store", store_edit=lambda s: s.clear()))


if __name__ == "__main__":
    unittest.main()
