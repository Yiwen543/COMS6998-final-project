"""Integration regression for the FIFO conversation loop using scripted provider replies.

Set EGG_FIFO_ASSERTION_BINARY to the release egg_assertion_forms executable
to run all three rounds offline. The RTL grader in this isolation test is a stub.
"""
import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_fifo_formal import FAULTS, FIELDS, SPLIT


ARMS = ("raw", "ordinary", "egg")
ORDER = (("raw", "ordinary", "egg"), ("ordinary", "egg", "raw"), ("egg", "raw", "ordinary"))
# Round 1 deliberately misses TLAST in every arm. Distinct legal shapes make
# an accidental swap of two arms' conversation histories observable.
INCOMPLETE = {"raw": [0, 1], "ordinary": [1, 3], "egg": [3, 0]}


def scripted_candidate(arm, round_number):
    if round_number == 1:
        indices = INCOMPLETE[arm]
    elif round_number == 2:
        indices = [*INCOMPLETE[arm], 2]
    else:
        indices = [0, 1, 2, 3]
    return {"obligations": [SPLIT[i] for i in indices],
            "diagnosis": {"field": "none" if round_number == 1 else "TLAST",
                          "step": -1 if round_number == 1 else 5}}


class ScriptedProvider:
    """No credentials, network, or token estimates; what it actually saw is retained."""
    def __init__(self):
        self.calls = []

    def __call__(self, messages, schema):
        round_index, position = divmod(len(self.calls), len(ARMS))
        arm = ORDER[round_index][position]
        candidate = scripted_candidate(arm, round_index + 1)
        self.calls.append((arm, round_index + 1, copy.deepcopy(messages), copy.deepcopy(schema), candidate))
        return {"output": copy.deepcopy(candidate), "usage": None, "id": f"fixture-{arm}-{round_index + 1}"}


def scripted_grade(rtl, obligations, out):
    # For these candidates each term is one stall-guarded field check. This
    # stub tests visibility/control flow; real bounded RTL grading is separate.
    assert set(obligations) <= set(SPLIT)
    models = {"original": {"status": "PASSED", "failed_indices": [], "failed_step": None, "sampled_atoms": None}}
    for design, field in FAULTS.items():
        term = f"(and active {field})"
        failed_indices = [i for i, obligation in enumerate(obligations) if obligation == term]
        atoms = {"active": True, **{name: name == field for name in FIELDS}}
        models[design] = {"status": "FAILED" if failed_indices else "PASSED",
                          "failed_indices": failed_indices, "failed_step": 5 if failed_indices else None,
                          "sampled_atoms": atoms if failed_indices else None}
    return {"bounded_states": 12, "obligations": list(obligations), "models": models}


class FifoLoopTests(unittest.TestCase):
    def test_fixture_and_live_accounting_cannot_be_swapped(self):
        from egg_fifo_loop import run_loop
        for mode, usage in (("live", None), ("fixture", {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0})):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                out = Path(temp) / "run"
                def respond(messages, schema):
                    return {"id": "fake-receipt", "output": scripted_candidate("raw", 1), "usage": usage}
                with self.assertRaisesRegex(ValueError, "usage"):
                    run_loop(rtl=Path(temp) / "unused.v", binary=Path(temp) / "unused-egg",
                             out=out, max_rounds=1, provider=respond, provider_mode=mode, grade=scripted_grade)
                self.assertFalse((out / "summary.json").exists())
                self.assertTrue((out / "raw/round-01/response.json").exists())

    def test_invalid_candidate_gets_revision_feedback_without_running_tools(self):
        from egg_fifo_loop import run_loop
        calls = []
        bad = {"obligations": [], "diagnosis": {"field": "none", "step": -1}}
        def respond(messages, schema):
            calls.append(copy.deepcopy(messages))
            return {"id": f"invalid-{len(calls)}", "output": bad, "usage": None}
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "run"
            with patch("egg_fifo_loop.review", side_effect=AssertionError("invalid candidate reached egg")):
                summary = run_loop(rtl=Path(temp) / "unused.v", binary=Path(temp) / "unused-egg",
                                   out=out, max_rounds=2, provider=respond, grade=scripted_grade)
            for messages in calls[3:]:
                self.assertEqual(json.loads(messages[-2]["content"]), bad)
                self.assertIn("Invalid candidate", messages[-1]["content"])
            self.assertEqual(summary["provider_api_calls"], 0)
            self.assertNotIn("provider_usage", summary)
            for arm in ARMS:
                self.assertIsNone(summary["arms"][arm]["first_verified_round"])
                for assessment in summary["arms"][arm]["rounds"]:
                    self.assertIn("candidate_error", assessment)
                    self.assertFalse(assessment["verified_revision"])

    def test_passing_original_does_not_rescue_weak_assertion_or_inconclusive_grading(self):
        from egg_fifo_loop import assess
        candidate = scripted_candidate("raw", 1)
        grade = scripted_grade(None, candidate["obligations"], None)
        self.assertEqual(grade["models"]["flip_last"]["status"], "PASSED")
        assessment = assess({"equivalent": False}, grade, candidate["diagnosis"], previous=None)
        self.assertTrue(assessment["incorrect_assertion_passed_original"])
        self.assertFalse(assessment["verified_revision"])
        grade["models"]["flip_last"]["status"] = "UNKNOWN"
        with self.assertRaisesRegex(ValueError, "conclusive"):
            assess({"equivalent": False}, grade, candidate["diagnosis"], previous=None)

    def test_failing_original_blocks_mutation_credit_and_nonstall_failure_is_not_a_diagnosis(self):
        from egg_fifo_loop import assess
        failed = {"status": "FAILED", "failed_step": 0, "failed_indices": [0],
                  "sampled_atoms": {"active": False, **{field: False for field in FIELDS}}}
        grade = {"models": {k: copy.deepcopy(failed) for k in ("original", *FAULTS)}}
        fake_diagnosis = {"field": "TLAST", "step": 0}
        assessment = assess({"equivalent": False}, grade, fake_diagnosis, previous=grade)
        self.assertIsNone(assessment["diagnosis_correct"])
        self.assertCountEqual(assessment["faults_failed"], FAULTS)
        self.assertEqual(assessment["faults_caught"], [])
        self.assertFalse(assessment["verified_revision"])
        grade["models"]["original"] = {"status": "PASSED", "failed_step": None, "sampled_atoms": None,
                                       "failed_indices": []}
        # Each missing premise independently prevents attribution to the probe.
        for active, last in ((False, True), (True, False)):
            with self.subTest(active=active, last_changed=last):
                grade["models"]["flip_last"]["sampled_atoms"].update(active=active, last_changed=last)
                trial = assess({"equivalent": False}, grade, fake_diagnosis, previous=grade)
                self.assertIsNone(trial["diagnosis_correct"])

    @unittest.skipUnless(os.environ.get("EGG_FIFO_ASSERTION_BINARY"),
                         "set EGG_FIFO_ASSERTION_BINARY for real egg in the offline loop")
    def test_three_rounds_keep_previous_candidate_and_feedback_private_to_each_arm(self):
        from egg_fifo_loop import run_loop
        provider = ScriptedProvider()
        binary = Path(os.environ["EGG_FIFO_ASSERTION_BINARY"])
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "run"
            run_loop(rtl=Path(temp) / "unused.v", binary=binary, out=out, max_rounds=3, provider=provider,
                     provider_mode="fixture", grade=scripted_grade)
            report = json.loads((out / "summary.json").read_bytes())
            self.assertEqual(report["mode"], "fixture")
            self.assertEqual(report["provider_api_calls"], 0)
            self.assertEqual(set(report["arms"]), set(ARMS))
            self.assertEqual(len(provider.calls), 9)
            first_messages = provider.calls[0][2]
            feedback = {}
            for arm, number, messages, schema, candidate in provider.calls:
                with self.subTest(arm=arm, round=number):
                    assessment = report["arms"][arm]["rounds"][number - 1]
                    self.assertEqual(assessment["incorrect_assertion_passed_original"], number < 3)
                    self.assertEqual(assessment["verified_revision"], number == 3)
                    self.assertEqual(assessment["diagnosis_correct"], True if number == 3 else None)
                    self.assertEqual(schema, provider.calls[0][3])
                    self.assertEqual(messages[:2], first_messages)
                    self.assertEqual([m["role"] for m in messages], ["system", "user"] + ["assistant", "user"] * (number - 1))
                    for internal_name in FAULTS:
                        # The visible mutant is identified only as "diagnostic_probe".
                        self.assertNotIn(internal_name, json.dumps(messages))
                    for earlier in range(1, number):
                        previous = json.loads(messages[2 * earlier]["content"])
                        self.assertEqual(previous, scripted_candidate(arm, earlier))
                        previous_feedback = feedback[arm, earlier]
                        self.assertIn(previous_feedback, messages[2 * earlier + 1]["content"])
                    saved = out / arm / f"round-{number:02d}"
                    for required in ("request.json", "response.json", "assessment.json", "feedback.txt"):
                        self.assertTrue((saved / required).is_file(), required)
                    feedback[arm, number] = (saved / "feedback.txt").read_text().strip()
                    payload = json.loads(feedback[arm, number])
                    self.assertEqual("sampled_boolean_truth_table" in payload, arm != "raw")
                    self.assertEqual("named_rewrite_search" in payload, arm != "raw")
                    if arm != "raw":
                        self.assertEqual(payload["named_rewrite_search"]["method"],
                                         "egg" if arm == "egg" else "ordinary_bounded_tree_search")
            # An incorrect test double that always returned the same feedback
            # would fail to reveal an arm swap, even with separate history lists.
            self.assertNotEqual(feedback["raw", 1], feedback["egg", 1])


if __name__ == "__main__":
    unittest.main()
