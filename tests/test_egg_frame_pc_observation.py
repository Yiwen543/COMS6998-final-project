import copy
from importlib.util import find_spec
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from egg_frame_faults import DESIGNS, TRACES
from egg_frame_observe import score_corpus
from egg_frame_pc_observation import prepare_common
from egg_frame_terms import BOOL_NAMES, BV_WIDTHS, REFERENCES

if find_spec("z3"):
    from egg_frame_proof import typed_oracle


def _row(cycle, **changes):
    inputs = {"rst": 0, "s_valid": 0, "s_data": 0, "s_last": 0, "m_ready": 0, "h_ready": 0}
    pre = {"s_ready": 0, "m_data": 0, "m_last": 0, "m_valid": 0, "h_valid": 0,
           "h_length": 4, "h_original_length": 4, "h_pad": 0, "h_truncate": 0}
    pre.update(changes)
    return {"cycle": cycle, "inputs": inputs, "pre": pre, "post": dict(pre)}


def _case_data():
    return {(design, trace): {"rows": [_row(i) for i in range(4)],
                              "checker": {"verdict": "PASS", "failures": []}}
            for design in DESIGNS for trace in TRACES}


def _query(monitors):
    return {n: typed_oracle(r, monitors[n])["oracle"] for n, r in REFERENCES.items()}


@unittest.skipUnless(find_spec("z3"), "requires z3-solver")
class FrameCounterexampleSelection(unittest.TestCase):
    def test_development_order_first_cycle_and_public_projection(self):
        corpus = _case_data()
        monitors = {**REFERENCES, "pad_flag": "false", "truncate_flag": "false"}
        # An original trace at cycle 2 outranks both a later trace and a probe at cycle 1.
        for design, trace, cycle in [("original", TRACES[0], 2), ("original", TRACES[0], 3),
                                     ("original", TRACES[1], 1), ("F02", TRACES[0], 1)]:
            corpus[design, trace]["rows"][cycle] = _row(cycle, h_valid=1, h_pad=1)
        for design in ("F02", "F05"):
            corpus[design, TRACES[2]]["rows"][3] = _row(3, h_valid=1, h_truncate=1)
        score = score_corpus(corpus, monitors)
        data = prepare_common(monitors, corpus, _query(monitors), score)
        packet = data["public"]
        self.assertEqual(set(packet["visible_rtl_observations"]), {"original", "probe_A", "probe_B"})
        pad = packet["semantic_review"]["pad_flag"]["counterexample"]
        self.assertEqual((pad["design"], pad["trace"], pad["cycle"]), ("original", TRACES[0], 2))
        self.assertEqual(pad["pins"], {"h_valid": 1, "rst": 0, "h_pad": 1, "h_original_length": 4})
        self.assertEqual((pad["origin"], pad["reference_value"], pad["candidate_value"]),
                         ("physical", True, False))
        self.assertEqual(data["observations"]["truncate_flag"]["design"], "probe_A")
        self.assertEqual(data["observations"]["pad_flag"]["values"].keys(), BOOL_NAMES | BV_WIDTHS.keys())
        self.assertIsNone(data["observations"]["header_hold"])
        self.assertIsNone(packet["semantic_review"]["header_hold"]["counterexample"])

    def test_held_out_only_mismatch_falls_back_to_symbolic(self):
        corpus = _case_data()
        monitors = {**REFERENCES, "pad_flag": "false"}
        entry = corpus["F04", TRACES[0]]
        entry["rows"][1] = _row(1, h_valid=1, h_pad=1)
        entry["checker"] = {"verdict": "FAIL", "failures": [{"detail": "held-out-only-sentinel"}]}
        score = score_corpus(corpus, monitors)
        # The include list permits no accidental access to the held-out raw rows.
        del corpus["F04", TRACES[0]]
        oracle = _query(monitors)
        data = prepare_common(monitors, corpus, oracle, score)
        witness = data["observations"]["pad_flag"]
        self.assertEqual(witness["origin"], "symbolic")
        self.assertEqual(witness["values"], oracle["pad_flag"]["counterexample"])
        self.assertTrue(witness["reference_value"])
        self.assertFalse(witness["candidate_value"])
        public = data["public"]["semantic_review"]["pad_flag"]["counterexample"]
        self.assertEqual(set(public), {"origin", "reference_value", "candidate_value", "pins"})
        for text in ("held-out-only-sentinel", "F01", "F02", "F03", "F04", "F05", "F06"):
            self.assertNotIn(text, json.dumps(data["public"]))

    def test_unknown_completion_and_determinate_masked_unknown(self):
        corpus = _case_data()
        rows = corpus["original", TRACES[0]]["rows"]
        rows[1] = _row(1, m_data=-1)
        rows[2] = _row(2, m_data=7)
        monitors = {**REFERENCES, "pad_flag": "(eq m_data 7)", "truncate_flag": "(or true (eq m_data 7))"}
        data = prepare_common(monitors, corpus, _query(monitors), score_corpus(corpus, monitors))
        first = data["public"]["semantic_review"]["pad_flag"]["counterexample"]
        self.assertEqual((first["cycle"], first["pins"]["m_data"]), (2, 7))
        masked = data["public"]["semantic_review"]["truncate_flag"]["counterexample"]
        self.assertEqual((masked["cycle"], masked["pins"]["m_data"]), (1, -1))
        self.assertFalse(masked["reference_value"])
        self.assertTrue(masked["candidate_value"])

    def test_raises_for_stale_physical_score_bad_model_and_contradictory_unsat(self):
        corpus = _case_data()
        corpus["original", TRACES[0]]["rows"][1] = _row(1, h_valid=1, h_pad=1)
        monitors = {**REFERENCES, "pad_flag": "false"}
        score = score_corpus(corpus, monitors)
        oracle = _query(monitors)
        bad_score = copy.deepcopy(score)
        bad_score["cases"]["original"][TRACES[0]]["properties"]["pad_flag"]["first_mismatch"] = None
        with self.assertRaisesRegex(ValueError, "fails PRE replay"):
            prepare_common(monitors, corpus, oracle, bad_score)
        bad_oracle = copy.deepcopy(oracle)
        bad_oracle["pad_flag"]["counterexample"]["rst"] = True
        with self.assertRaisesRegex(ValueError, "fails replay"):
            prepare_common(monitors, corpus, bad_oracle, score)
        bad_oracle["pad_flag"] = typed_oracle("false", "false")["oracle"]
        with self.assertRaisesRegex(ValueError, "contradicts typed equivalence"):
            prepare_common(monitors, corpus, bad_oracle, score)

    def test_unknown_oracle_is_inconclusive_but_can_have_a_physical_witness(self):
        monitors = {**REFERENCES, "pad_flag": "false", "data_hold": "false"}
        corpus = _case_data()
        corpus["F05", TRACES[1]]["rows"][1] = _row(1, h_valid=1, h_pad=1)
        oracles = _query(monitors)
        for name in ("pad_flag", "data_hold"):
            oracles[name] = {"status": "unknown", "equivalent": None, "counterexample": None,
                             "reference_value": None, "candidate_value": None}
        data = prepare_common(monitors, corpus, oracles, score_corpus(corpus, monitors))
        result = data["public"]["semantic_review"]
        self.assertIsNone(result["pad_flag"]["equivalent"])
        self.assertEqual(result["pad_flag"]["counterexample"]["design"], "probe_B")
        self.assertIsNone(result["data_hold"]["counterexample"])


if __name__ == "__main__":
    unittest.main()
