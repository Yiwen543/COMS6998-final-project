"""Check width rejection and the same physical field/threshold semantics across evaluators."""
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_frame_terms import (
    BOOL_NAMES, BV_WIDTHS, REFERENCES, abstract, evaluate_term, format_term, parse_term,
    referenced_signals, sv_term, z3_env, z3_term,
)
from predicates import evaluate, parse


def assignments():
    initial = dict.fromkeys(BOOL_NAMES | BV_WIDTHS.keys(), 0)
    # Every arithmetic boundary, plus sign-bit and maximum unsigned values.
    for n in (0, 3, 4, 5, 8, 9, 32768, 65535):
        length = min(max(4, n), 8)
        row = dict(initial, h_valid=1, h_original_length=n, h_length=length,
                   h_pad=int(n < 4), h_truncate=int(n > 8))
        yield row
        for change in ({"h_pad": 1 - row["h_pad"]}, {"h_truncate": 1 - row["h_truncate"]},
                       {"h_length": (length + 1) % 65536}, {"rst": 1, "h_length": 65535}):
            yield {**row, **change}
    rng = random.Random(6998)
    for _ in range(32):
        yield {**{p: rng.randrange(2) for p in sorted(BOOL_NAMES)},
               **{p: rng.randrange(1 << w) for p, w in BV_WIDTHS.items()}}
    # Isolate every held field and ensure valid drop/stall release/reset are distinguished.
    row = dict(initial, have_prev=1, prev_m_valid=1, m_valid=1, prev_h_valid=1, h_valid=1,
               h_length=4, prev_h_length=4, h_pad=1, prev_h_pad=1)
    yield row
    for p in ("m_valid", "m_data", "m_last", "h_valid", "h_pad", "h_truncate", "h_length", "h_original_length"):
        changed = {**row, p: row[p] ^ 1}
        yield changed
        yield {**changed, "prev_rst": 1}
        yield {**changed, "rst": 1}
        yield {**changed, "prev_m_ready": 1, "prev_h_ready": 1}


def expected(e):
    qualify = bool(e["have_prev"] and not e["prev_rst"] and not e["rst"])

    def lost(c, payload):
        active = qualify and e[f"prev_{c}_valid"] and not e[f"prev_{c}_ready"]
        return bool(active and (not e[f"{c}_valid"] or any(e[p] != e["prev_" + p] for p in payload)))

    active = not e["rst"] and e["h_valid"]
    n = e["h_original_length"]
    return {"data_hold": lost("m", ("m_data", "m_last")),
            "header_hold": lost("h", ("h_pad", "h_truncate", "h_length", "h_original_length")),
            "pad_flag": bool(active and bool(e["h_pad"]) != (n < 4)),
            "truncate_flag": bool(active and bool(e["h_truncate"]) != (n > 8)),
            "clamped_length": bool(active and e["h_length"] != min(max(4, n), 8))}


class FrameTerms(unittest.TestCase):
    def test_parse_rejects_malformed_or_ill_typed_inputs(self):
        bad = ["", "(unknown a b)", "(not rst s_valid)", "(and rst)", "(and rst prev_foo)",
               "(eq 3 4)", "(eq h_valid 1)", "(and rst h_length)", "(ule h_valid prev_h_valid)",
               "(eq m_data h_length)", "(ugt m_data 256)", "(ult s_data -1)", "h_length", "5",
               "(not rst) h_valid", "(not rst", "prev_have_prev", ")",
               "(not " * 130 + "true" + ")" * 130]
        for source in bad:
            with self.subTest(source=source[:30]), self.assertRaises(ValueError):
                parse_term(source)
        node = parse_term("(and h_valid (uge h_original_length 65535))")
        self.assertEqual(parse_term(format_term(node)), node)
        self.assertEqual(referenced_signals(node), {"h_valid", "h_original_length"})
        with self.assertRaises(ValueError):
            evaluate_term(node, {"h_valid": 1, "h_original_length": -1})
        with self.assertRaises(ValueError):
            evaluate_term(node, {"h_valid": 2, "h_original_length": 3})

    def test_python_and_boolean_projection_against_pin_level_oracle(self):
        forms = {name: parse_term(s) for name, s in REFERENCES.items()}
        projected = {}
        for k, ast in forms.items():
            text, mapping = abstract(ast)
            projected[k] = parse(text), mapping
        for row in assignments():
            want = expected(row)
            for k, ast in forms.items():
                self.assertEqual(evaluate_term(ast, row), want[k], k)
                terms, mapping = projected[k]
                actual = evaluate(terms, {key: evaluate_term(v, row) for key, v in mapping.items()})
                self.assertEqual(actual, want[k], k)
        self.assertEqual(abstract(parse_term("(ugt 4 h_original_length)")),
                         abstract(parse_term("(ult h_original_length 4)")))
        pos, atoms = abstract(parse_term("(eq h_length 4)"))
        neg, neg_atoms = abstract(parse_term("(ne 4 h_length)"))
        self.assertEqual(neg, f"(not {pos})")
        self.assertEqual(atoms, neg_atoms)
        self.assertTrue(evaluate_term(parse_term("(eq (not h_valid) (xor false true))"), {"h_valid": 0}))

    def test_unrestricted_z3_oracle(self):
        try:
            import z3
        except ImportError:
            self.skipTest("needs the z3-solver Python package")
        e = z3_env()
        qualify = z3.And(e["have_prev"], z3.Not(e["prev_rst"]), z3.Not(e["rst"]))

        def lost(c, payload):
            return z3.And(qualify, e[f"prev_{c}_valid"], z3.Not(e[f"prev_{c}_ready"]),
                          z3.Or(z3.Not(e[f"{c}_valid"]), *(e[p] != e["prev_" + p] for p in payload)))

        n = e["h_original_length"]
        active = z3.And(z3.Not(e["rst"]), e["h_valid"])
        bounded = z3.If(z3.ULT(n, 4), z3.BitVecVal(4, 16), z3.If(z3.UGT(n, 8), z3.BitVecVal(8, 16), n))
        want = {"data_hold": lost("m", ("m_data", "m_last")),
                "header_hold": lost("h", ("h_pad", "h_truncate", "h_length", "h_original_length")),
                "pad_flag": z3.And(active, e["h_pad"] != z3.ULT(n, 4)),
                "truncate_flag": z3.And(active, e["h_truncate"] != z3.UGT(n, 8)),
                "clamped_length": z3.And(active, bounded != e["h_length"])}
        for name, spec in REFERENCES.items():
            solver = z3.Solver()
            solver.add(z3_term(parse_term(spec), e) != want[name])
            self.assertEqual(solver.check(), z3.unsat, name)
        with self.assertRaises(ValueError):
            z3_term(parse_term("(eq h_length 4)"), {"h_length": z3.BitVec("wrong", 8)})

    @unittest.skipUnless(shutil.which("iverilog") and shutil.which("vvp"), "needs Icarus Verilog")
    def test_sv_matches_independent_oracle(self):
        rows = list(assignments())
        lines = ["module samples;"]
        for k in sorted(BOOL_NAMES):
            lines.append(f"reg {k};")
        for k, width in BV_WIDTHS.items():
            lines.append(f"reg [{width-1}:0] {k};")
        monitor = ", ".join(sv_term(parse_term(s)) for s in REFERENCES.values())
        lines.append("initial begin")
        for row in rows:
            lines.extend(f"{k} = {v};" for k, v in row.items())
            lines.append('#1; $display("%b", {' + monitor + '});')
        lines.extend(["end", "endmodule"])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rtl = root / "sample.sv"
            rtl.write_text("\n".join(lines))
            exe = root / "a.vvp"
            subprocess.run(["iverilog", "-g2012", "-o", exe, rtl], check=True, capture_output=True)
            observed = subprocess.check_output(["vvp", exe], text=True).splitlines()
        self.assertEqual(observed, ["".join(str(int(x)) for x in expected(r).values()) for r in rows])
