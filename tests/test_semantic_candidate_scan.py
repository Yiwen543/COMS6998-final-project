"""Semantic gates for flattened aliases and sound case-priority removal."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from preflight_heldout import ENGINE, z3_equivalent  # noqa: E402
from semantic_candidate_scan import scan  # noqa: E402
from typed_predicates import extract  # noqa: E402


class SemanticCandidateScanTests(unittest.TestCase):
    def test_flattened_port_alias_preserves_event_and_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "linked.sv"
            source.write_text("""module child(input clk,rst_n,en,output reg q);
 always @(posedge clk or negedge rst_n) begin
   if(!rst_n) q<=0; else if(en) q<=1;
 end
endmodule
module top(input clk,rst_n,en,output reg a,output wire b);
 child c(.clk(clk),.rst_n(rst_n),.en(en),.q(b));
 always @(posedge clk or negedge rst_n) begin
   if(!rst_n) a<=0; else if(en) a<=1;
 end
endmodule
""")
            if not ENGINE.exists():
                self.skipTest("build Rust egg engine first")
            result = scan(source, "top", flatten=True)
            groups = [g for g in result["groups"] if {m["line"] for m in g["members"]} == {3, 9}]
            self.assertTrue(groups)
            self.assertEqual(["negedge \\rst_n", "posedge \\clk"], groups[0]["event_context"])
            self.assertTrue(result["alias_evidence"])
            self.assertEqual(1, groups[0]["independent_z3_checks"])

    def test_disjoint_priority_is_proved_and_synthetic_fifo_group_expands(self):
        if not ENGINE.exists():
            self.skipTest("build Rust egg engine first")
        source = ROOT / "examples/heldout_sfifo_stress/rtl/sfifo.v"
        result = scan(source, "sfifo", flatten=False)
        self.assertTrue(result["priority_proofs"])
        self.assertEqual({"unsat"}, set(result["priority_proofs"]))
        self.assertTrue(any({96, 129, 179}.issubset({m["line"] for m in g["members"]})
                            for g in result["groups"]))
        self.assertTrue(result["unsupported"])

    def test_flattened_alias_across_two_source_files(self):
        if not ENGINE.exists():
            self.skipTest("build Rust egg engine first")
        with tempfile.TemporaryDirectory() as tmp:
            child = Path(tmp) / "child.sv"
            top = Path(tmp) / "top.sv"
            child.write_text("""module child(input clk,en,output reg q);
 always @(posedge clk) begin
   if(en) q<=1;
 end
endmodule
""")
            top.write_text("""module top(input clk,en,output reg a,output wire b);
 child c(.clk(clk),.en(en),.q(b));
 always @(posedge clk) begin
   if(en) a<=1;
 end
endmodule
""")
            result = scan([top, child], "top", flatten=True)
            groups = [g for g in result["groups"] if
                      {Path(m["source"]).name for m in g["members"]} == {"top.sv", "child.sv"}]
            self.assertTrue(groups)
            self.assertEqual(2, len(result["sources"]))
            self.assertEqual(["posedge \\clk"], groups[0]["event_context"])

    def test_distinct_case_values_stay_distinct(self):
        source = ROOT / "examples/heldout_queue/rtl/queue.sv"
        result = extract(source, "queue")
        read = next(t for t in result["targets"] if t["line"] == 55 and t["case_value"] == "2'01")
        write = next(t for t in result["targets"] if t["line"] == 56 and t["case_value"] == "2'10")
        self.assertFalse(z3_equivalent(read["compact"], write["compact"]))


if __name__ == "__main__":
    unittest.main()
