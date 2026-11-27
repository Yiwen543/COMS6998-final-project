"""Independently grade every frozen label and verify provenance / chronology."""

from collections import Counter
from importlib.util import find_spec
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
if find_spec("z3"):
    import z3
    from audit_egg_fifo_live import read_archive
    from egg_regression_workload import (ARCHIVE, ARCHIVE_INVENTORY_SHA256, PROPERTIES,
                                         TYPED_SCHEMA_SHA256, _archive_inventory, inventory,
                                         load_versions, workload)
    from egg_regression_facts import context_id
    from egg_txn_terms import parse_term, z3_env, z3_term


@unittest.skipUnless(find_spec("z3"), "requires z3-solver")
class FrozenRegressionWorkload(unittest.TestCase):
    def test_predetermined_inventory_and_no_solver_selection(self):
        # No oracle answer is used when selecting cases or assigning labels.
        with patch.object(z3, "SolverFor", side_effect=AssertionError("no solver during freeze")), \
                patch.object(z3, "Solver", side_effect=AssertionError("no solver during freeze")):
            rows = workload()
        self.assertEqual(rows, workload())
        stats = inventory(rows)
        self.assertEqual(stats["total_requests"], 224)
        self.assertEqual(stats["independent_llm_initial_suites"], 3)
        self.assertEqual(stats["original_response_receipts"], 21)
        self.assertEqual({k: v["requests"] for k, v in stats["cohorts"].items()}, {
            "real_initial": 27, "real_context": 9, "real_history": 162,
            "controlled_revision": 20, "controlled_scope": 6})
        self.assertEqual(stats["cohorts"]["real_initial"]["identical_source_formulas"], 9)
        self.assertEqual(stats["cohorts"]["real_history"]["identical_source_formulas"], 162)
        self.assertEqual({c["property"] for c in rows}, set(PROPERTIES))

    def test_real_archive_provenance_and_history(self):
        versions = load_versions(ARCHIVE)
        self.assertEqual(len({v["response_id"] for v in versions.values()}), 21)
        self.assertEqual(len({v["request_sha256"] for k, v in versions.items() if k.endswith("/initial")}), 1)
        self.assertEqual(len({v["response_sha256"] for v in versions.values()}), 21)
        by_path = {v["source"]: v for v in versions.values()}
        seen = Counter()
        for row in workload():
            if row["cohort"].startswith("real_"):
                for side in ("left", "right"):
                    version = by_path[row[side + "_source"]]
                    self.assertEqual(row[side], version["monitors"][row["property"]])
                    for key in ("response_id", "request_sha256", "response_sha256"):
                        self.assertEqual(row[side + "_" + key], version[key])
            if row["cohort"] == "real_history":
                seen[row["right_response_id"]] += 1
                right = row["right_source"]
                self.assertEqual(row["left_source"], right.replace("/round-02/", "/round-01/") if row["round"] == 3
                                 else right.split("/")[0] + "/initial/response.json")
        self.assertEqual(len(seen), 18)
        self.assertEqual(set(seen.values()), {9})

    def test_frozen_member_content_hash_binds_archive(self):
        files = read_archive(ARCHIVE)
        self.assertEqual(_archive_inventory(files), ARCHIVE_INVENTORY_SHA256)
        files["trial-01/initial/response.json"] += b"\n"
        with patch("egg_regression_workload.read_archive", return_value=files):
            with self.assertRaisesRegex(ValueError, "frozen source"):
                load_versions(ARCHIVE)

    def test_scope_edit_is_explicit_and_current_query_has_one_guard(self):
        rows = workload()
        for row in rows:
            self.assertEqual(row["scope_id"], context_id(row["guard"]))
            self.assertEqual(row["previous_scope_id"], context_id(row["previous_guard"]))
            self.assertEqual(row["typed_schema_sha256"], TYPED_SCHEMA_SHA256)
            self.assertEqual(row["scope_changed"], row["scope_id"] != row["previous_scope_id"])
        edit = [r for r in rows if r["control"] in {"certify-at-four", "scope-edit-four-to-five", "restore-four-scope"}]
        self.assertEqual([r["expected_relation"] for r in edit], ["equivalent", "incomparable", "equivalent"])
        self.assertEqual(len({(r["left"], r["right"]) for r in edit}), 1)
        self.assertEqual(edit[0]["scope_id"], edit[1]["previous_scope_id"])
        self.assertEqual(edit[1]["scope_id"], edit[2]["previous_scope_id"])
        self.assertEqual(edit[2]["scope_id"], edit[0]["scope_id"])

    def test_independent_full_width_oracle_validates_every_frozen_label(self):
        env = z3_env()
        for row in workload():
            with self.subTest(request=row["id"]):
                guard, left, right = [z3_term(parse_term(row[k]), env) for k in ("guard", "left", "right")]
                solver = z3.SolverFor("QF_BV")
                solver.set(timeout=5000)
                solver.add(guard)
                self.assertEqual(solver.check(), z3.sat)
                statuses = []
                for expression in (z3.And(left, z3.Not(right)), z3.And(right, z3.Not(left))):
                    solver.push()
                    solver.add(expression)
                    statuses.append(str(solver.check()))
                    solver.pop()
                label = {("unsat", "unsat"): "equivalent", ("unsat", "sat"): "strengthened",
                         ("sat", "unsat"): "weakened", ("sat", "sat"): "incomparable"}[tuple(statuses)]
                self.assertEqual(label, row["expected_relation"])


if __name__ == "__main__":
    unittest.main()
