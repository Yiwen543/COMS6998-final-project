"""Source-bound proof checks for the optional two-target early stopping mode."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from m3_proof_dependencies import ProofChecker

BINARY = Path(os.environ.get("CARGO_TARGET_DIR", ROOT / "egraph/target")) / "release/egg_assertion_forms"
RULE = {"name": "commute-and", "left": "(and ?x ?y)", "right": "(and ?y ?x)"}


def payload(left, right):
    terms = (("left", left), ("right", right))
    return {"pattern_rules": [RULE], "verified_rules": [], "targets": [
        {"id": name, "event_context": "posedge clk", "compact": text} for name, text in terms]}


def invoke(data, *flags, check=True):
    return subprocess.run([BINARY, *flags], input=json.dumps(data), capture_output=True, text=True, check=check)


@unittest.skipUnless(BINARY.is_file(), "requires release egg_assertion_forms")
class EarlyStopping(unittest.TestCase):
    def test_actual_proof_in_default_and_early_modes(self):
        data = payload("(and a b)", "(and b a)")
        default = json.loads(invoke(data).stdout)
        early = json.loads(invoke(data, "--stop-on-merge").stdout)
        self.assertEqual(set(default), set(early))
        self.assertEqual(default["stop_reason"], "Some(Saturated)")
        self.assertEqual(early["stop_reason"], 'Some(Other("TargetsMerged"))')
        for graph in (default, early):
            left, right = graph["targets"]
            self.assertNotEqual(left["eclass_before"], right["eclass_before"])
            self.assertEqual(left["eclass"], right["eclass"])
            edge, = graph["rewrite_explanations"]
            replay = ProofChecker(data, pattern_rules=[RULE]).check(edge)
            self.assertEqual(replay["pattern_rules"], ["commute-and"])

    def test_identity_distinct_and_wrong_scope(self):
        data = payload("a", "a")
        equal = json.loads(invoke(data, "--stop-on-merge").stdout)
        self.assertEqual(equal["stop_reason"], 'Some(Other("TargetsMerged"))')
        self.assertEqual(equal["rewrite_explanations"], [])
        data["targets"][1]["compact"] = "b"
        separate = json.loads(invoke(data, "--stop-on-merge").stdout)
        self.assertEqual(separate["stop_reason"], "Some(Saturated)")
        self.assertNotEqual(separate["targets"][0]["eclass"], separate["targets"][1]["eclass"])
        data["targets"][1]["event_context"] = "negedge clk"
        self.assertNotEqual(invoke(data, "--stop-on-merge", check=False).returncode, 0)
        data["targets"].pop()
        self.assertNotEqual(invoke(data, "--stop-on-merge", check=False).returncode, 0)


if __name__ == "__main__":
    unittest.main()
