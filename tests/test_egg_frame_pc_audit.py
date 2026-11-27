"""Negative controls for the offline proof-carrying frame feedback audit."""
import json
import os
from pathlib import Path, PurePosixPath
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


class ProofCarryingAuditTests(unittest.TestCase):
    """Independently edit an accepted archive; no test sends a provider request."""

    @classmethod
    def setUpClass(cls):
        from audit_egg_frame_pc import AuditEvidence, audit
        from egg_frame_pc_loop import run
        default = Path(os.environ.get("CARGO_TARGET_DIR", ROOT / "egraph/target")) / "release/egg_diagnostic_forms"
        cls.binary = Path(os.environ.get("EGG_FRAME_PC_BINARY", default))
        if not cls.binary.is_file():
            raise unittest.SkipTest("build egg_diagnostic_forms or set EGG_FRAME_PC_BINARY for the offline audit")
        cls.corpus = ROOT / "results/milestone3/frame-faults"
        if "EGG_FRAME_PC_FIXTURE" in os.environ:
            fixture = Path(os.environ["EGG_FRAME_PC_FIXTURE"])
        else:
            temp = tempfile.TemporaryDirectory()
            cls.addClassCleanup(temp.cleanup)
            fixture = Path(temp.name) / "fixture"
            run(out=fixture, corpus_dir=cls.corpus, binary=cls.binary, mode="fixture", profiles=["historical"],
                replicates=1, rounds=2)
        cls.files = {p.relative_to(fixture).as_posix(): p.read_bytes() for p in fixture.rglob("*") if p.is_file()}
        if "config.json" not in cls.files:
            raise ValueError(f"missing two-round PC fixture under {fixture}")
        cls.cache = AuditEvidence(cls.corpus)
        cls.audit = staticmethod(audit)
        # Each negative control changes a single accepted input or a correlated
        # transcript pair. Establish that the unchanged artifact passes first.
        cls.intact = audit(cls.files, cls.corpus, cls.binary, cache=cls.cache)
        cls.stages = sorted({str(PurePosixPath(path).parent) for path in cls.files if path.endswith("/feedback.txt")})

    def reject(self, changes, why):
        for path, value in changes.items():
            self.assertIn(path, self.files)
            self.assertNotEqual(value, self.files[path], path)
        with self.assertRaisesRegex(ValueError, why):
            self.audit({**self.files, **changes}, self.corpus, self.binary, cache=self.cache)

    def first_stage(self, *, round_name, artifact, contains=None):
        candidates = [s for s in self.stages if s.endswith("/" + round_name)
                      and s + "/" + artifact in self.files and (contains is None or contains in s.split("/"))]
        self.assertTrue(candidates, (round_name, artifact, contains))
        return candidates[0]

    def test_previous_reply_must_be_consumed_by_its_own_arm(self):
        stage = self.first_stage(round_name="round-02", artifact="request.json")
        path = stage + "/request.json"
        request = json.loads(self.files[path])
        history = [m for m in request["messages"] if m["role"] == "assistant"]
        self.assertTrue(history)
        history[-1]["content"] = "{}"
        self.reject({path: json_bytes(request)}, "history|request|messages")

    def test_ambiguous_duplicate_messages_in_request(self):
        stage = self.first_stage(round_name="round-01", artifact="request.json")
        path = stage + "/request.json"
        original = self.files[path].lstrip()
        self.assertTrue(original.startswith(b"{"))
        duplicate = b'{"messages":[{"role":"system","content":"F01"}],' + original[1:]
        self.reject({path: duplicate}, "duplicate JSON field")

    def test_heldout_feedback_and_its_echo_cannot_be_forged_together(self):
        stage = self.first_stage(round_name="round-01", artifact="feedback.txt")
        feedback_path = stage + "/feedback.txt"
        request_path = str(PurePosixPath(stage).parent / "round-02/request.json")
        request = json.loads(self.files[request_path])
        previous = self.files[feedback_path].decode().strip()
        contaminated = previous + "\nHeld-out F01 trace failed at sample 7."
        self.assertIn(previous, request["messages"][-1]["content"])
        request["messages"][-1]["content"] = request["messages"][-1]["content"].replace(previous, contaminated)
        self.reject({feedback_path: (contaminated + "\n").encode(), request_path: json_bytes(request)},
                    "feedback|packet|held.?out|leak")

    def test_private_content_cannot_be_inserted_at_the_same_place_in_every_arm(self):
        stage = self.first_stage(round_name="round-01", artifact="request.json")
        trial = PurePosixPath(stage).parent.parent
        paths = [s + "/request.json" for s in self.stages
                 if s.endswith("/round-01") and PurePosixPath(s).parent.parent == trial]
        self.assertGreaterEqual(len(paths), 2)
        changes = {}
        for path in paths:
            request = json.loads(self.files[path])
            request["messages"][0]["content"] += "\nPrivate F03 grading observation: output ended too late."
            changes[path] = json_bytes(request)
        self.reject(changes, "history|request|messages|prompt|leak")

    def test_cross_arm_history_substitution_is_rejected(self):
        stage = self.first_stage(round_name="round-02", artifact="request.json")
        path = stage + "/request.json"
        trial = PurePosixPath(stage).parent.parent
        other = next(s + "/request.json" for s in self.stages
                     if s.endswith("/round-02") and PurePosixPath(s).parent.parent == trial
                     and self.files[s + "/request.json"] != self.files[path])
        self.reject({path: self.files[other]}, "history|request|messages")

    def test_fixture_rejects_invented_provider_calls_and_fake_receipt_usage(self):
        summary = json.loads(self.files["summary.json"])
        self.assertEqual(summary["provider_api_calls"], 0)
        summary["provider_api_calls"] = 1
        self.reject({"summary.json": json_bytes(summary)}, "summary|call|usage")
        stage = self.first_stage(round_name="round-01", artifact="response.json")
        response_path = stage + "/response.json"
        response = json.loads(self.files[response_path])
        self.assertIsNone(response["usage"])
        response["usage"] = {"input_tokens": 15, "output_tokens": 5, "total_tokens": 20}
        self.reject({response_path: json_bytes(response)}, "usage|fixture|receipt")

    def test_unrelated_unsat_smt_cannot_impersonate_a_typed_receipt(self):
        stage = self.first_stage(round_name="round-02", artifact="oracles.json")
        path = stage + "/oracles.json"
        record = json.loads(self.files[path])
        name = next(k for k, v in record.items() if v["status"] == "unsat")
        record[name]["smt2"] = "(assert false)\n(check-sat)\n"
        self.reject({path: json_bytes(record)}, "not bound to the candidate")

    def test_previous_receipt_cannot_count_as_a_second_response(self):
        first = self.first_stage(round_name="round-01", artifact="response.json")
        second = str(PurePosixPath(first).parent / "round-02/response.json")
        receipt = json.loads(self.files[second])
        receipt["id"] = json.loads(self.files[first + "/response.json"])["id"]
        self.reject({second: json_bytes(receipt)}, "reused response ID|duplicate.*response")

    def test_synthetic_live_envelope_accounting_and_identity(self):
        # Exercise the live-format accounting branch entirely in memory. All
        # token counts and identifiers below are invented test inputs. Neither
        # the file set nor its audit result is published as a live experiment.
        files = dict(self.files)
        config = json.loads(files["config.json"])
        requested, returned = "unit-test-requested", "unit-test-returned"
        config.update(mode="live", provider={"transport": "OpenAI Responses API", "model": requested,
                                            "reasoning_effort": "low", "max_output_tokens": 96})
        files["config.json"] = json_bytes(config)
        paths = sorted(p for p in files if p.endswith("/response.json"))
        totals = {arm: {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0} for arm in config["arms"]}
        for index, path in enumerate(paths, 1):
            receipt = json.loads(files[path])
            arm = PurePosixPath(path).parts[-3]
            usage = {"input_tokens": 140 + index, "output_tokens": 12 + index % 10,
                     "input_tokens_details": {"cached_tokens": 7, "cache_write_tokens": 2},
                     "output_tokens_details": {"reasoning_tokens": 3}}
            usage["total_tokens"] = usage["input_tokens"] + usage["output_tokens"]
            receipt.update(id=f"resp_unit_test_{index}", requested_model=requested, model=returned,
                           status="completed", service_tier="default", dispatch_attempted=True, http_status=200,
                           usage=usage)
            files[path] = json_bytes(receipt)
            for key in totals[arm]:
                totals[arm][key] += usage[key]
        summary = json.loads(files["summary.json"])
        summary.update(mode="live", provider_api_calls=len(paths), provider_usage=totals,
                       requested_model=requested, model=returned)
        files["summary.json"] = json_bytes(summary)

        result = self.audit(files, self.corpus, self.binary, cache=self.cache)
        self.assertTrue(result["passed"])
        self.assertEqual(result["new_api_requests"], 0)
        self.assertEqual(result["provider_api_calls_in_archive"], len(paths))
        self.assertEqual(result["provider_usage"], totals)
        self.assertEqual(result["reported_service_tiers"], ["default"])
        self.assertIsNone(self.intact["live_session_usage"])
        for profile, trials in result["live_session_usage"].items():
            for trial, arms in trials.items():
                for arm, session in arms.items():
                    rounds = session["rounds"]
                    for row in rounds:
                        path = f'{profile}/{trial}/{arm}/round-{row["round"]:02d}/response.json'
                        self.assertEqual(row["usage"], json.loads(files[path])["usage"])
                    first = summary["sessions"][profile][trial][arm]["first_verified_round"]
                    expected = None if first is None else {
                        key: sum(row["usage"][key] for row in rounds[:first])
                        for key in ("input_tokens", "output_tokens", "total_tokens")}
                    self.assertEqual(session["first_verified_round"], first)
                    self.assertEqual(session["usage_to_first_verified"], expected)
        for detail, subset, parent in (("input_tokens_details", "cached_tokens", "input_tokens"),
                                       ("output_tokens_details", "reasoning_tokens", "output_tokens")):
            with self.subTest(subset=subset):
                changed = json.loads(files[paths[0]])
                changed["usage"][detail][subset] = changed["usage"][parent] + 1
                with self.assertRaisesRegex(ValueError, "token subset"):
                    self.audit({**files, paths[0]: json_bytes(changed)}, self.corpus, self.binary, cache=self.cache)
        for field, bad_value, why in (("model", "unit-test-switched", "changed model"),
                                      ("id", json.loads(files[paths[0]])["id"], "reused response ID")):
            with self.subTest(field=field):
                changed = json.loads(files[paths[1]])
                changed[field] = bad_value
                with self.assertRaisesRegex(ValueError, why):
                    self.audit({**files, paths[1]: json_bytes(changed)}, self.corpus, self.binary, cache=self.cache)

    def test_stale_egg_evidence_rejected_even_when_valid_for_a_different_candidate(self):
        stage = self.first_stage(round_name="seed", artifact="certificates.json")
        path = stage + "/certificates.json"
        other = next(s + "/certificates.json" for s in self.stages
                     if s.endswith("/round-01") and PurePosixPath(s).parent == PurePosixPath(stage).parent
                     and self.files[s + "/certificates.json"] != self.files[path])
        self.reject({path: self.files[other]}, "certificate|egg|proof")

    def test_forged_displayed_rewrite_step_fails_even_if_archive_and_prompt_echo_agree(self):
        stage = self.first_stage(round_name="seed", artifact="certificates.json")
        certificate_path, feedback_path = stage + "/certificates.json", stage + "/feedback.txt"
        request_path = str(PurePosixPath(stage).parent / "round-01/request.json")
        certificates = json.loads(self.files[certificate_path])
        property_name = next(name for name, item in certificates.items() if item["public"].get("steps"))
        certificate = certificates[property_name]["public"]
        certificate["steps"][0]["rule"] = "forged-identity"
        previous = self.files[feedback_path].decode().strip()
        packet = json.loads(previous)
        packet["egg_certificates"][property_name] = certificate
        forged = json.dumps(packet, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        request = json.loads(self.files[request_path])
        self.assertIn(previous, request["messages"][-1]["content"])
        request["messages"][-1]["content"] = request["messages"][-1]["content"].replace(previous, forged)
        self.reject({certificate_path: json_bytes(certificates), feedback_path: (forged + "\n").encode(),
                     request_path: json_bytes(request)}, "rule|proof|certificate|packet")


if __name__ == "__main__":
    unittest.main()
