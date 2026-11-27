"""Check transaction DSL, structural snapshot domain, and all nine independent obligations."""
from pathlib import Path
import sys
import unittest

import z3

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_txn_terms import (BOOL_NAMES, BV_WIDTHS, REFERENCES, abstract, domain, evaluate_term,
                           format_term, parse_term, referenced_signals, sample, typed_oracle,
                           validate_snapshot, z3_env, z3_term)
from predicates import evaluate, parse


def blank():
    values = dict.fromkeys(BOOL_NAMES | BV_WIDTHS.keys(), 0)
    return {**values, "data_index": 1}


def independent_spec(e):
    """Use direct word operations and a conditional expected byte/length, not DSL folds."""
    i, n, h = e["data_index"], e["data_n"], e["header_n"]
    live_data = z3.And(e["m_valid"], z3.Not(e["rst"]))
    live_header = z3.And(e["h_valid"], z3.Not(e["rst"]))
    four, eight = z3.BitVecVal(4, 16), z3.BitVecVal(8, 16)

    def length(v):
        return z3.If(z3.ULT(v, 4), four, z3.If(z3.UGT(v, 8), eight, v))

    # Within an open input record only its prefix may already be offered. At byte 8
    # the output terminates even when the remaining input has not yet been accepted.
    available = z3.If(e["data_done"], length(n), z3.If(z3.UGT(n, 8), eight, n))
    data_allowed = z3.And(z3.ULT(e["data_count"], e["input_count"]), i != 0, z3.ULE(i, available))
    header_allowed = z3.And(z3.ULT(e["header_count"], e["input_count"]), e["header_done"])
    byte = z3.If(z3.ULE(i, n), e["data_byte"], z3.BitVecVal(0, 8))
    last = z3.Or(i == 8, z3.And(e["data_done"], i == length(n)))
    idle = z3.And(*(z3.Not(e[name]) for name in ("s_valid", "m_valid", "h_valid", "input_open")),
                  e["data_count"] == e["input_count"], e["header_count"] == e["input_count"])
    return {
        "data_entitlement": z3.And(live_data, z3.Not(data_allowed)),
        "data_payload": z3.And(live_data, data_allowed, e["m_data"] != byte),
        "data_last": z3.And(live_data, data_allowed, e["m_last"] != last),
        "header_entitlement": z3.And(live_header, z3.Not(header_allowed)),
        "header_original": z3.And(live_header, header_allowed, e["h_original_length"] != h),
        "header_adjusted": z3.And(live_header, header_allowed, e["h_length"] != length(h)),
        "header_flags": z3.And(live_header, header_allowed,
                               z3.Or(e["h_pad"] != z3.ULT(h, 4), e["h_truncate"] != z3.UGT(h, 8))),
        "reset_clear": z3.And(e["rst"], e["phase_post"], z3.Or(e["m_valid"], e["h_valid"])),
        "drain_complete": z3.And(e["final_sample"], z3.Not(idle)),
    }


class TransactionTerms(unittest.TestCase):
    def test_all_reference_formulas_against_independent_word_spec(self):
        e = z3_env()
        expected = independent_spec(e)
        self.assertEqual(tuple(REFERENCES), tuple(expected))
        for name, source in REFERENCES.items():
            with self.subTest(name=name):
                solver = z3.SolverFor("QF_BV")
                term = parse_term(source)
                solver.add(domain(e), z3_term(term, e) != expected[name])
                self.assertEqual(solver.check(), z3.unsat)
                self.assertEqual(term, parse_term(format_term(term)))
                # Satisfiability of both verdicts guards against vacuous obligations.
                for opposite in ("true", "false"):
                    record = typed_oracle(source, opposite)
                    self.assertEqual(record["status"], "sat")
                    values = record["counterexample"]
                    self.assertTrue(validate_snapshot(values))
                    self.assertNotEqual(sample(term, values), opposite == "true")
                    self.assertEqual(sample(term, values), record["reference_value"])
                    prop, atoms = abstract(term)
                    self.assertEqual(evaluate(parse(prop), {k: sample(atom, values) for k, atom in atoms.items()}),
                                     record["reference_value"])

    def test_checked_unsigned_parser_and_opaque_predicate_binding(self):
        for source in ("input_count", "prev_m_valid", "(not s_data)", "(xor m_valid data_byte)",
                       "(ult m_valid false)", "(eq 3 0)", "(ugt header_n m_data)", "(eq 1 h_valid)",
                       "(ule data_byte 256)", "(ne h_length 65536)", "(eq m_data -1)", "(or rst)",
                       "(not rst) else", "(not " * 130 + "true" + ")" * 130):
            with self.subTest(source=source[:60]), self.assertRaises(ValueError):
                parse_term(source)
        ast = parse_term("(and (eq m_valid (xor false h_valid)) (uge h_length 32768))")
        self.assertEqual(referenced_signals(ast), {"m_valid", "h_valid", "h_length"})
        self.assertTrue(evaluate_term(ast, {"m_valid": 1, "h_valid": True, "h_length": 65535}))
        self.assertEqual(abstract(parse_term("(ugt 4 header_n)")), abstract(parse_term("(ult header_n 4)")))
        leaf, table = abstract(parse_term("(eq m_data data_byte)"))
        self.assertEqual(abstract(parse_term("(ne data_byte m_data)")), (f"(not {leaf})", table))
        with self.assertRaises(ValueError):
            sample("(eq m_data 1)", {"m_data": True})

    def test_domain_allows_offending_outputs_and_independent_cursor_overruns(self):
        base = blank()
        for changes in ({"m_valid": 1, "h_valid": 1, "h_length": 65535, "m_data": 255},
                        {"input_count": 1, "data_count": 2, "header_n": 11, "header_done": 1},
                        {"data_count": 512, "header_count": 511, "data_index": 512},
                        {"input_count": 2, "input_open": 1, "data_n": 5, "data_done": 1,
                         "header_count": 1, "header_n": 2}):
            self.assertTrue(validate_snapshot({**base, **changes}))
        bad = ({"data_index": 0}, {"data_index": 513}, {"input_count": 513}, {"input_open": 1},
               {"final_sample": 1}, {"data_n": 1}, {"header_done": 1},
               {"input_count": 1, "data_n": 5, "header_n": 4, "data_done": 1, "header_done": 1},
               {"input_count": 1, "input_open": 1, "data_n": 5, "header_n": 5, "data_done": 1},
               {"input_count": 1, "data_n": 13, "header_n": 13, "data_done": 1, "header_done": 1})
        for changes in bad:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate_snapshot({**base, **changes})
        # The two independent count cursors may point to the same accepted record,
        # or to different records with different sizes.
        self.assertTrue(typed_oracle("(and (eq data_count header_count) (ne data_n header_n))", "false")["equivalent"])
        self.assertFalse(typed_oracle("(and (ne data_count header_count) (ne data_n header_n))", "false")["equivalent"])

    def test_exact_partial_coverage_and_no_vacuous_verdict(self):
        self.assertTrue(sample("(uge data_index 1)", {"data_index": -1}))
        self.assertFalse(sample("(ne data_n 0)", {"input_count": 0}))
        self.assertTrue(sample("phase_post", {"final_sample": True, "phase_post": None}))
        self.assertIsNone(sample("phase_post", {"final_sample": False, "phase_post": -1}))
        self.assertTrue(sample("(eq m_data m_data)", {}))
        self.assertIsNone(sample("(eq m_data data_byte)", {"m_data": 251}))
        # Either cursor can overrun. Spurious output data/header VALID remain observable.
        self.assertTrue(sample(REFERENCES["data_entitlement"], {"rst": 0, "m_valid": 1, "input_count": 0}))
        with self.assertRaisesRegex(ValueError, "no completion"):
            sample("true", {"final_sample": True, "phase_post": False})
        with self.assertRaisesRegex(ValueError, "no completion"):
            sample("true", {"data_index": 0})
        self.assertIsNone(sample("final_sample", {}))

    def test_stall_padding_truncation_reset_and_final_edge(self):
        base = {**blank(), "m_valid": 1, "h_valid": 1, "data_n": 2, "header_n": 2, "input_count": 1,
                "data_byte": 255, "m_data": 255, "h_pad": 1, "h_length": 4, "h_original_length": 2,
                "data_done": 1, "header_done": 1}
        good = [
            base,
            {**base, "data_index": 4, "m_data": 0, "m_last": 1},
            {**base, "data_index": 8, "data_n": 12, "header_n": 12, "h_valid": 0, "m_last": 1},
            {**base, "data_index": 8, "data_n": 8, "header_n": 8, "h_valid": 0, "m_last": 1,
             "input_open": 1, "data_done": 0, "header_done": 0},
        ]
        for values in good:
            self.assertTrue(validate_snapshot(values))
            self.assertFalse(any(sample(t, values) for t in REFERENCES.values()))
        bad = {**base, "input_open": 1, "data_done": 0, "header_done": 0, "data_index": 4}
        alarms = [k for k, t in REFERENCES.items() if sample(t, bad)]
        self.assertEqual(alarms, ["data_entitlement", "header_entitlement"])
        self.assertTrue(sample(REFERENCES["reset_clear"], {**base, "rst": 1, "phase_post": 1}))
        self.assertFalse(sample(REFERENCES["reset_clear"], {**base, "rst": 1}))
        self.assertTrue(sample(REFERENCES["drain_complete"], {**base, "final_sample": 1, "phase_post": 1}))
        self.assertFalse(sample(REFERENCES["drain_complete"], {**blank(), "final_sample": 1, "phase_post": 1}))


if __name__ == "__main__":
    unittest.main()
