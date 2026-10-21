"""Regression checks for complete guards, typed atoms, and conservative grouping."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from preflight_heldout import ORIGINAL, VARIANT, z3_equivalent  # noqa: E402
from typed_predicates import extract, group_candidates  # noqa: E402


class TypedPredicateTests(unittest.TestCase):
    def test_queue_full_guard_and_source_distinct_groups(self):
        original = extract(ORIGINAL, "queue")
        variant = extract(VARIANT, "queue_variant")
        for result in (original, variant):
            groups = group_candidates(result)
            self.assertEqual([(6, "2'01"), (6, "2'10")],
                             sorted((len(g), g[0]["case_value"]) for g in groups))
            self.assertTrue(result["unsupported"])
            for group in groups:
                self.assertEqual(6, len({row["line"] for row in group}))
                self.assertTrue(all(row["guard_depth"] == 4 for row in group))
                self.assertTrue(all(row["event_context"] == ["negedge \\rst_ni", "posedge \\clk_i"]
                                    for row in group))
                self.assertTrue(all(row["source_mapping"] == "text_literal" for row in group))
                self.assertTrue(all(z3_equivalent(group[0]["compact"], row["compact"]) for row in group[1:]))
        a = next(t for t in original["targets"] if t["line"] == 124)
        b = next(t for t in variant["targets"] if t["line"] == 124)
        self.assertNotEqual(a["compact"], b["compact"])
        self.assertTrue(z3_equivalent(a["compact"], b["compact"]))

    def test_width_signedness_and_event_context(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            source = folder / "typed.sv"
            source.write_text("""module typed(input logic clk, rst,
  input logic signed [3:0] a, b, output logic q);
  always @(posedge clk or negedge rst) begin
    if (!rst) q <= 0;
    else if (a == b) q <= 1;
  end
endmodule
""")
            async_result = extract(source, "typed")
            eq_atoms = [atom for atom in async_result["atoms"].values() if atom["op"] == "eq"]
            self.assertEqual(1, len(eq_atoms))
            self.assertEqual((4, 4, True, True),
                             (eq_atoms[0]["lhs_width"], eq_atoms[0]["rhs_width"],
                              eq_atoms[0]["lhs_signed"], eq_atoms[0]["rhs_signed"]))
            async_path = next(t for t in async_result["targets"] if t["line"] == 5 and t["case_value"] == "1'1")
            self.assertEqual(["negedge \\rst", "posedge \\clk"], async_path["event_context"])
            source.write_text(source.read_text().replace("posedge clk or negedge rst", "posedge clk"))
            sync_result = extract(source, "typed")
            sync_path = next(t for t in sync_result["targets"] if t["line"] == 5 and t["case_value"] == "1'1")
            self.assertEqual(["posedge \\clk"], sync_path["event_context"])
            self.assertEqual(async_path["compact"], sync_path["compact"])
            self.assertNotEqual(async_path["event_context"], sync_path["event_context"])

    def test_selected_counters_are_zero_hit_and_separate(self):
        path = ROOT / "results/heldout_queue_preflight/selection.json"
        if not path.exists():
            self.skipTest("run scripts/preflight_heldout.py to create counters")
        result = json.loads(path.read_text())
        self.assertEqual(24, result["selected_zero_hit_source_counters"])
        self.assertEqual(2, len(result["selected_groups"]))
        self.assertNotEqual(result["selected_groups"][0]["eclass"],
                            result["selected_groups"][1]["eclass"])
        for group in result["selected_groups"]:
            self.assertEqual(12, len(group["members"]))
            self.assertEqual(11, len(group["independent_z3_checks"]))
            self.assertTrue(all(member["coverage_point"]["hits"] == 0 for member in group["members"]))

    def test_screening_provenance(self):
        path = ROOT / "results/heldout_queue_preflight/screening.json"
        if not path.exists():
            self.skipTest("run scripts/screen_cvdp_candidates.py to create screening record")
        screen = json.loads(path.read_text())
        self.assertEqual(68, screen["records_screened"])
        self.assertEqual(["cvdp_agentic_queue_0007"],
                         [row["id"] for row in screen["results"] if row["status"] == "qualifies"])
        self.assertEqual(2, len(next(row for row in screen["results"]
                                     if row["id"] == "cvdp_agentic_queue_0007")["qualifying_groups"]))


if __name__ == "__main__":
    unittest.main()
