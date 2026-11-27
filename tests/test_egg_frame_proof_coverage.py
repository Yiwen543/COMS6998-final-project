"""Controls for the common-quotient Boolean rule-profile comparison."""
import copy
from collections import Counter
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_frame_proof import SCOPE, typed_oracle
from egg_frame_proof_coverage import check_graph, collect_cases, rule_profiles, variants
from egg_frame_terms import REFERENCES
from m3_proof_dependencies import BUILTINS, validate_pattern_rules


def probe(left, right, rules, *, same_before=False, same_after=True, explanation=None):
    targets = [{"id": key, "compact": term, "event_context": SCOPE}
               for key, term in (("reference", left), ("candidate", right))]
    payload = {"targets": targets, "verified_rules": [], "pattern_rules": rules}
    graph = {
        "targets": [{"id": "reference", "eclass_before": 0, "eclass": 3},
                    {"id": "candidate", "eclass_before": 0 if same_before else 1, "eclass": 3 if same_after else 4}],
        "rewrite_explanations": [], "ground_rule_count": 0, "pattern_rule_count": len(rules),
        "stop_reason": "Some(Saturated)", "iterations": 2, "enodes": 5, "eclasses": 4,
        "engine": "egg 0.11.0",
    }
    if explanation is not None:
        graph["rewrite_explanations"].append(
            {"left": "reference", "right": "candidate", "explanation": explanation})
    return payload, graph


class FrameProofCoverageTests(unittest.TestCase):
    def test_frozen_source_inventories_and_fixture_deduplication(self):
        cases, old_indexed = collect_cases()
        keys = {(c["cohort"], c["reference"], c["candidate"]) for c in cases}
        self.assertEqual(len(keys), len(cases))
        self.assertEqual(Counter(c["cohort"] for c in cases),
                         {"live_final": 5, "live_seed": 5, "generated": 18, "fixture_revisions": 6})
        for row in cases:
            self.assertEqual(row["reference"], REFERENCES[row["field"]])
            self.assertIs(row["expected"], row["cohort"] != "live_seed")
        fixtures = [c for c in cases if c["cohort"] == "fixture_revisions"]
        self.assertEqual(Counter(len(c["sources"]) for c in fixtures), {1: 2, 2: 4})
        self.assertEqual(set(old_indexed), set(REFERENCES))
        self.assertEqual({name for name, row in old_indexed.items() if not row["proved"]},
                         {"data_hold", "header_hold"})

    def test_profiles_preserve_old_rules_and_only_add_truth_table_valid_schemas(self):
        profiles = rule_profiles()
        self.assertEqual(set(profiles), {"base", "assoc", "ac_dist"})
        inventories = {name: {r["name"]: (r["left"], r["right"]) for r in records}
                       for name, records in profiles.items()}
        self.assertEqual(inventories["base"], BUILTINS)
        for small, large in (("base", "assoc"), ("assoc", "ac_dist")):
            self.assertLess(inventories[small].items(), inventories[large].items())
        for name, rules in profiles.items():
            with self.subTest(profile=name):
                self.assertEqual(set(validate_pattern_rules(rules)), set(inventories[name]))

    def test_variations_preserve_full_width_semantics_and_are_deterministic(self):
        families = set()
        for name, reference in REFERENCES.items():
            cases = variants(reference)
            self.assertEqual(cases, variants(reference))
            self.assertTrue({"reassociate", "reorder", "demorgan"} <= set(cases))
            self.assertEqual(len(cases), len(set(cases.values())))
            for kind, candidate in cases.items():
                with self.subTest(property=name, family=kind):
                    self.assertNotEqual(reference, candidate)
                    self.assertEqual(typed_oracle(reference, candidate)["oracle"]["status"], "unsat")
            families.update(cases)
        self.assertEqual(families, {"reassociate", "reorder", "demorgan", "distribute"})

    def test_identity_is_not_a_named_derivation(self):
        rules = rule_profiles()["base"]
        source = "(and (not rst) h_valid)"
        payload, graph = probe(source, source, rules, same_before=True)
        identity = check_graph(payload, graph, rules)
        self.assertEqual((identity["status"], identity["proved"], identity["steps"]),
                         ("structural_identity", True, []))

        left, right = "(not (not h_valid))", "h_valid"
        payload, graph = probe(left, right, rules, explanation=left + "\n(Rewrite=> double-not h_valid)")
        for stop in ("Some(Saturated)", "Some(NodeLimit(20001))"):
            graph["stop_reason"] = stop
            result = check_graph(payload, graph, rules)
            self.assertEqual((result["status"], result["proved"], result["stop"]), ("checked_derivation", True, stop))
            self.assertEqual(result["steps"], [{"rule": "double-not", "direction": "forward", "path": []}])

    def test_no_derivation_on_miss_or_resource_limit(self):
        rules = rule_profiles()["base"]
        payload, graph = probe("rst", "h_valid", rules, same_after=False)
        for stop, status in (("Some(Saturated)", "saturated_miss"), ("Some(IterationLimit(20))", "limited"),
                             ("Some(NodeLimit(20001))", "limited"), ("Some(TimeLimit(5.0001))", "limited")):
            with self.subTest(stop=stop):
                graph["stop_reason"] = stop
                result = check_graph(payload, graph, rules)
                self.assertEqual((result["status"], result["proved"], result["stop"]), (status, False, stop))

    def test_early_stop_requires_opt_in_and_independent_merge_evidence(self):
        rules = rule_profiles()["base"]
        left, right = "(not (not h_valid))", "h_valid"
        payload, graph = probe(left, right, rules, explanation=left + "\n(Rewrite=> double-not h_valid)")
        graph["stop_reason"] = 'Some(Other("TargetsMerged"))'
        checked = check_graph(payload, graph, rules, stop_on_merge=True)
        self.assertEqual((checked["status"], checked["proved"], checked["saturated_proved"]),
                         ("checked_derivation", True, False))
        self.assertEqual(checked["steps"], [{"rule": "double-not", "direction": "forward", "path": []}])
        with self.assertRaises(ValueError):
            check_graph(payload, graph, rules, stop_on_merge=False)
        graph["rewrite_explanations"] = []
        for before, after in ((1, 3), (0, 3), (1, 4)):
            # Respectively a missing proof, falsely claimed input identity, and a spurious early-stop signal.
            with self.subTest(before=before, after=after):
                graph["targets"][1].update(eclass_before=before, eclass=after)
                with self.assertRaises(ValueError):
                    check_graph(payload, graph, rules, stop_on_merge=True)
        graph["stop_reason"] = 'Some(Other("TargetsMergedLater"))'
        with self.assertRaises(ValueError):
            check_graph(payload, graph, rules, stop_on_merge=True)

    def test_forged_or_unallowlisted_proofs_are_rejected_even_after_limit(self):
        rules = rule_profiles()["base"]
        left = "(not (not h_valid))"
        payload, graph = probe(left, "h_valid", rules, explanation=left + "\n(Rewrite=> double-not h_valid)")
        for stop in ("Some(Saturated)", "Some(NodeLimit(20001))"):
            graph["stop_reason"] = stop
            for fault in ("omit-proof", "unregistered-rule", "bad-instantiation", "fabricated-identity",
                          "wrong-rule-count", "invented-stop", "cross-context"):
                with self.subTest(stop=stop, fault=fault):
                    bad_payload, bad_graph = copy.deepcopy(payload), copy.deepcopy(graph)
                    if fault == "omit-proof":
                        bad_graph["rewrite_explanations"] = []
                    elif fault == "unregistered-rule":
                        bad_graph["rewrite_explanations"][0]["explanation"] = left + "\n(Rewrite=> unjustified h_valid)"
                    elif fault == "bad-instantiation":
                        # The right term is now genuinely inequivalent. A named rule alone cannot prove the edge.
                        bad_payload["targets"][1]["compact"] = "rst"
                        bad_graph["rewrite_explanations"][0]["explanation"] = left + "\n(Rewrite=> double-not rst)"
                        self.assertEqual(typed_oracle(left, "rst")["oracle"]["status"], "sat")
                    elif fault == "fabricated-identity":
                        bad_graph["targets"][1]["eclass_before"] = bad_graph["targets"][0]["eclass_before"]
                    elif fault == "wrong-rule-count":
                        bad_graph["pattern_rule_count"] = 0
                    elif fault == "invented-stop":
                        bad_graph["stop_reason"] = "success"
                    else:
                        bad_payload["targets"][1]["event_context"] = "negedge"
                    with self.assertRaises(ValueError):
                        check_graph(bad_payload, bad_graph, rules)

    @unittest.skipUnless(os.environ.get("EGG_FIFO_ASSERTION_BINARY"),
                         "set EGG_FIFO_ASSERTION_BINARY to run the real engine")
    def test_same_pair_on_real_binary_changes_only_with_associativity(self):
        binary = Path(os.environ["EGG_FIFO_ASSERTION_BINARY"])
        a = "(and (and rst h_valid) m_valid)"
        b = "(and rst (and h_valid m_valid))"
        for profile, expected in (("base", "saturated_miss"), ("assoc", "checked_derivation")):
            rules = rule_profiles()[profile]
            payload, _ = probe(a, b, rules)
            result = subprocess.run([binary], input=json.dumps(payload), capture_output=True,
                                    text=True, check=True, timeout=20)
            checked = check_graph(payload, json.loads(result.stdout), rules)
            self.assertEqual(checked["status"], expected)

    @unittest.skipUnless(os.environ.get("EGG_FIFO_ASSERTION_BINARY"),
                         "set EGG_FIFO_ASSERTION_BINARY to run the real engine")
    def test_real_stop_on_merge_returns_identity_or_replayable_proof(self):
        binary = Path(os.environ["EGG_FIFO_ASSERTION_BINARY"])
        rules = rule_profiles()["base"]
        for left, right, status in (("h_valid", "h_valid", "structural_identity"),
                                    ("(not (not h_valid))", "h_valid", "checked_derivation")):
            with self.subTest(status=status):
                payload, _ = probe(left, right, rules)
                run = subprocess.run([binary, "--stop-on-merge"], input=json.dumps(payload), capture_output=True,
                                     text=True, check=True, timeout=20)
                checked = check_graph(payload, json.loads(run.stdout), rules, stop_on_merge=True)
                self.assertEqual((checked["stop"], checked["status"]), ('Some(Other("TargetsMerged"))', status))
                self.assertTrue(checked["proved"])
                self.assertFalse(checked["saturated_proved"])


if __name__ == "__main__":
    unittest.main()
