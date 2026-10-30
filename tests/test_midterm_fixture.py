"""Independent reference outputs and one-fault controls for fixed checkers."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from midterm_fixture import check_codec, check_search, validate_actions
from run_midterm_b_development import messages_for, raw_feedback
from coverage import load


class FixtureTests(unittest.TestCase):
    def test_schema_widths_and_exact_fields(self):
        codec = dict(reset=0, enc_data=0, enc_control=0, dec_valid=0, dec_word=0)
        validate_actions("codec", {"actions": [codec]}, 1)
        for bad in (dict(codec, enc_data=1 << 64), dict(codec, extra=1),
                    dict(codec, reset=True), dict(codec, dec_word=1 << 66)):
            with self.assertRaises(ValueError):
                validate_actions("codec", {"actions": [bad]}, 1)
        with self.assertRaises(ValueError):
            validate_actions("codec", {"actions": [codec, codec]}, 1)

    def test_codec_spec_reference_and_single_fault(self):
        actions = [dict(reset=1, enc_data=0, enc_control=0, dec_valid=0, dec_word=0),
                   dict(reset=0, enc_data=0x1234, enc_control=0, dec_valid=1,
                        dec_word=(1 << 64) | 0x1234)]
        zero = dict(enc=0, dec_data=0, dec_control=0, sync=0, error=0)
        trace = [dict(step=0, pre_reset_enc=0, pre_reset_data=0, pre_reset_control=0,
                      pre_reset_sync=0, pre_reset_error=0, **zero),
                 dict(step=1, pre_reset_enc=0, pre_reset_data=0, pre_reset_control=0,
                      pre_reset_sync=0, pre_reset_error=0, enc=(1 << 64) | 0x1234,
                      dec_data=0x1234, dec_control=0, sync=0, error=0)]
        self.assertEqual(check_codec(actions, trace)["failures"], [])
        faulty = copy.deepcopy(trace)
        faulty[1]["dec_data"] = 0
        self.assertEqual(check_codec(actions, faulty)["distinct_defects"], ["decoder_data"])

    def test_search_reference_and_single_fault(self):
        zero = dict(reset=0, start=0, pause=0, key=90, write_en=0,
                    write_addr=0, write_data=0)
        actions = [dict(zero, reset=1)]
        actions += [dict(zero, write_en=1, write_addr=i,
                         write_data=90 if i in (1, 3, 5) else i) for i in range(8)]
        actions += [dict(zero, start=1)] + [dict(zero) for _ in range(12)]
        trace = []
        for i in range(len(actions)):
            done = int(i == 19)
            trace.append(dict(step=i, pre_reset_done=0, pre_reset_count=0,
                              pre_reset_indices=0, pre_reset_overflow=0,
                              done=done, count=2 if done else 0,
                              indices=0x19 if done else 0, overflow=done))
        self.assertEqual(check_search(actions, trace)["failures"], [])
        faulty = copy.deepcopy(trace)
        faulty[19]["indices"] = 0x11
        self.assertEqual(check_search(actions, faulty)["distinct_defects"], ["match_index"])
        early = copy.deepcopy(trace)
        early[10]["done"] = 1
        early[10]["count"] = 2
        early[10]["indices"] = 0x19
        early[10]["overflow"] = 1
        self.assertIn("done_timing", check_search(actions, early)["distinct_defects"])

    def test_development_b_feedback_is_raw_only(self):
        root = Path(__file__).resolve().parents[1]
        for ip, slug in (("codec", "heldout_codec64"), ("search", "heldout_linear_search")):
            sources = sorted((root / "examples" / slug / "rtl").glob("*.sv"))
            dat = root / "results/midterm_candidate_preflight" / slug / "seed.dat"
            points = [point for source in sources for point in
                      load(dat, str(source.relative_to(root)), include_descendants=True)]
            checked = {"checker": {"checks": 0, "failures": [], "distinct_defects": []}}
            messages = messages_for(ip, [], checked, "", points, sources, 1, 32)
            payload = json.loads(messages[1]["content"])
            self.assertIn("raw_uncovered_dut_coverage", payload)
            self.assertNotIn("egg_normalization", payload)
            self.assertNotIn("calibration", json.dumps(payload).lower())
            self.assertEqual(payload["raw_uncovered_dut_coverage"], raw_feedback(points, sources))


if __name__ == "__main__":
    unittest.main()
