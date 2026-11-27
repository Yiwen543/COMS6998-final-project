"""Freeze the candidate deck and grade its scripted repairs with an independent pin-level spec."""
from pathlib import Path
import sys
import unittest

import z3

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_frame_llm import SEED
from egg_frame_pc_seeds import FINAL_HASH, SEEDS, digest, fixture_revision
from egg_frame_terms import REFERENCES, abstract, parse_term, z3_env, z3_term


def independent_monitors(e):
    def stable(channel, payload):
        active = z3.And(e["have_prev"], z3.Not(e["prev_rst"]), z3.Not(e["rst"]),
                        e[f"prev_{channel}_valid"], z3.Not(e[f"prev_{channel}_ready"]))
        preserved = z3.And(e[f"{channel}_valid"], *(e[name] == e["prev_" + name] for name in payload))
        return z3.And(active, z3.Not(preserved))

    length = e["h_original_length"]
    valid = z3.And(e["h_valid"], z3.Not(e["rst"]))
    short, long = z3.ULT(length, 4), z3.UGT(length, 8)
    clamp = z3.If(short, z3.BitVecVal(4, 16), z3.If(long, z3.BitVecVal(8, 16), length))
    return {"data_hold": stable("m", ("m_data", "m_last")),
            "header_hold": stable("h", ("h_pad", "h_truncate", "h_length", "h_original_length")),
            "pad_flag": z3.And(valid, e["h_pad"] != short),
            "truncate_flag": z3.And(valid, e["h_truncate"] != long),
            "clamped_length": z3.And(valid, e["h_length"] != clamp)}


class SeedWorkload(unittest.TestCase):
    def test_frozen_seed_identity_order_and_atom_budget(self):
        self.assertEqual(list(SEEDS), ["historical", "mixed", "corner"])
        self.assertEqual(SEEDS["historical"], SEED)
        self.assertEqual(digest(SEEDS), "d1e0336ae61e200934675df1bdda4067e260c27e77435c45456e44acbe7bbcaa")
        for profile, seed in SEEDS.items():
            self.assertEqual(seed.keys(), REFERENCES.keys())
            for name, text in seed.items():
                ref_atoms = abstract(parse_term(REFERENCES[name]))[1]
                cand_atoms = abstract(parse_term(text))[1]
                self.assertLessEqual(len(ref_atoms.keys() | cand_atoms.keys()), 12, (profile, name))

    def test_scripted_counts_by_independent_full_width_z3(self):
        env = z3_env()
        independent = independent_monitors(env)
        for profile in SEEDS:
            for turn, correct in enumerate((set(), {"data_hold", "pad_flag"}, set(REFERENCES), set(REFERENCES))):
                monitors = fixture_revision(profile, turn)
                for name, text in monitors.items():
                    with self.subTest(profile=profile, turn=turn, property=name):
                        solver = z3.Solver()
                        solver.set(timeout=5000)
                        solver.add(z3_term(parse_term(text), env) != independent[name])
                        self.assertEqual(solver.check(), z3.unsat if name in correct else z3.sat)
                if turn >= 2:
                    self.assertEqual(digest(monitors), FINAL_HASH)

    def test_fixture_rounds_do_not_mutate_each_other(self):
        for turn in (0, 1, 2, 3):
            first = fixture_revision("mixed", turn)
            first.pop("data_hold")
            self.assertIn("data_hold", fixture_revision("mixed", turn))
        for profile, turn in [("missing", 0), ("mixed", 4), ("mixed", True)]:
            with self.assertRaises(ValueError):
                fixture_revision(profile, turn)


if __name__ == "__main__":
    unittest.main()
