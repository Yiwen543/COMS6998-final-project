"""Independent negative controls for branch-local egg step replay."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_txn_context_check import check_graph, GOAL_STOP, PATTERN_RULES


def fact(context, left, right):
    digest = sha256(json.dumps([context, left, right], separators=(",", ":")).encode()).hexdigest()[:24]
    return {"name": "ctx-" + digest, "left": left, "right": right, "proof_status": "unsat", "event_context": context}


def payload(left, right, *, context="sample-A", facts=()):
    return {"context_id": context, "targets": [{"id": name, "compact": term, "event_context": context}
            for name,term in (("left",left),("right",right))], "pattern_rules": deepcopy(PATTERN_RULES),
            "ground_rules": list(facts)}


def graph(request, explanation=None, *, merged=True, identical=False, stop=GOAL_STOP):
    edge = [] if explanation is None else [{"left":"left", "right":"right", "explanation":explanation}]
    return {"context_id":request["context_id"],"engine":"egg 0.11.0","stop_reason":stop,
            "iterations":1,"enodes":8,"eclasses":5,"pattern_rule_count":23,
            "ground_rule_count":len(request["ground_rules"]),"targets":[
                {"id":"left","eclass_before":1,"eclass":1},
                {"id":"right","eclass_before":1 if identical else 2,"eclass":1 if merged else 2}],
            "rewrite_explanations":edge}


class ContextGraphCheckTests(unittest.TestCase):
    def test_forward_and_reverse_erasure_with_exact_new_subtree(self):
        request = payload("false", "(and (or a b) false)")
        text = "false\n(Rewrite<= and-false-right (and (or a b) false))"
        result = check_graph(request, graph(request, text))
        self.assertTrue(result["proved"])
        self.assertEqual(result["steps"][0], {"direction":"reverse","path":[],"rule":"and-false-right",
                                              "replacement":"(and (or a b) false)"})
        with self.assertRaisesRegex(ValueError, "substitution"):
            check_graph(request, graph(request, text.replace("and-false-right", "and-false-left")))

    def test_conditional_ground_dependency_and_path(self):
        rule = fact("sample-A","a","true")
        request = payload("(or a b)", "(or true b)", facts=[rule])
        proof = "(or a b)\n(or (Rewrite=> " + rule["name"] + " true) b)"
        result = check_graph(request,graph(request,proof))
        self.assertEqual(result["used_ground_rules"], [rule["name"]])
        self.assertEqual(result["steps"][0]["path"], [0])
        with self.assertRaisesRegex(ValueError, "unknown rewrite"):
            check_graph(request,graph(request,proof.replace(rule["name"], "foreign")))

    def test_scope_label_cannot_carry_stale_fact_or_proof(self):
        rule = fact("sample-A","a","true")
        request = payload("a", "true", facts=[rule])
        proof = "a\n(Rewrite=> " + rule["name"] + " true)"
        other = payload("a", "true", context="sample-B", facts=[rule])
        with self.assertRaisesRegex(ValueError,"wrong context"):
            check_graph(other,graph(other,proof))
        other["ground_rules"][0] = {**rule, "event_context":"sample-B"}
        with self.assertRaisesRegex(ValueError,"fact name"):
            check_graph(other,graph(other,proof))
        transplanted = graph(request,proof)
        transplanted["context_id"] = "sample-B"
        with self.assertRaisesRegex(ValueError,"graph context"):
            check_graph(request,transplanted)

    def test_unrelated_sibling_and_endpoint(self):
        request = payload("(and (or a false) b)", "(and a b)")
        proof = "(and (or a false) b)\n(and (Rewrite=> or-false-right a) b)"
        self.assertTrue(check_graph(request,graph(request,proof))["proved"])
        with self.assertRaisesRegex(ValueError,"another subtree"):
            check_graph(request,graph(request,proof.replace("right a) b)", "right a) a)")))
        changed = payload("(and (or a false) b)","a")
        with self.assertRaisesRegex(ValueError,"endpoint"):
            check_graph(changed,graph(changed,proof))
        with self.assertRaisesRegex(ValueError,"one named rewrite"):
            check_graph(request,graph(request,proof + "\n(and a b)"))

    def test_generic_inventory_must_match_even_when_unused(self):
        request = payload("a","a")
        request["pattern_rules"][2]["right"] = "true"
        with self.assertRaisesRegex(ValueError, "generic rule inventory"):
            check_graph(request,graph(request,identical=True))

    def test_no_graph_saturation_identity_and_hard_limit(self):
        request = payload("a","b")
        self.assertFalse(check_graph(request,None)["proved"])
        for stop, expected in (("Some(Saturated)","saturated_miss"), ("Some(NodeLimit(20017))","limited"),
                               ("Some(TimeLimit(5.012345))","limited")):
            row = check_graph(request,graph(request,merged=False,stop=stop))
            self.assertEqual((row["proved"],row["status"],row["stop"]), (False,expected,stop))
        with self.assertRaisesRegex(ValueError,"require one complete"):
            check_graph(request,graph(request,stop="Some(NodeLimit(20017))"))
        identical = payload("(not a)","(not a)")
        result = check_graph(identical,graph(identical,identical=True,stop="Some(Saturated)"))
        self.assertEqual((result["proved"],result["status"],result["steps"]),(True,"structural_identity",[]))
        request = payload("(not (not a))","a")
        row = check_graph(request,graph(request,"(not (not a))\n(Rewrite=> double-not a)",stop="Some(IterationLimit(20))"))
        self.assertEqual((row["proved"], row["status"], row["stop"]), (True,"checked_derivation","Some(IterationLimit(20))"))

    def test_erased_variable_cannot_change_on_second_occurrence(self):
        request = payload("false","(and a (not b))")
        with self.assertRaisesRegex(ValueError, "substitution"):
            check_graph(request,graph(request,"false\n(Rewrite<= and-complement-right (and a (not b)))"))

    def test_preclass_or_goal_without_merge(self):
        request = payload("a","b")
        with self.assertRaisesRegex(ValueError,"identity"):
            check_graph(request,graph(request,identical=True))
        with self.assertRaisesRegex(ValueError,"goal stop"):
            check_graph(request,graph(request,merged=False))

    @unittest.skipUnless(os.environ.get("EGG_CONTEXT_BINARY"), "set EGG_CONTEXT_BINARY for a native proof")
    def test_native_conditional_rewrite_chain(self):
        rule = fact("sample-A","a","true")
        request = payload("(and a b)", "b", facts=[rule])
        proc = subprocess.run([os.environ["EGG_CONTEXT_BINARY"]], text=True, input=json.dumps(request),
                              capture_output=True, check=True, timeout=20)
        row = check_graph(request,json.loads(proc.stdout))
        self.assertTrue(row["proved"])
        self.assertEqual(row["used_ground_rules"], [rule["name"]])
        self.assertGreaterEqual(len(row["steps"]), 2)


if __name__ == "__main__":
    unittest.main()
