"""Frozen starting errors and scripted revisions for the frame monitor feedback comparison."""
import argparse
from functools import cache
import hashlib
import json
from pathlib import Path
import tarfile

from egg_frame_llm import SEED
from egg_frame_terms import REFERENCES


def _edit(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"expected exactly one seed source anchor {old!r}")
    return text.replace(old, new)


_PRESENT = "(and (not rst) h_valid)"
_TRANSFER = "(and (and (not rst) h_valid) h_ready)"

# These are candidate violation expressions. The public specification is unchanged.
SEEDS = {
    "historical": dict(SEED),
    "mixed": {
        "data_hold": "(and (and have_prev (and (not prev_rst) (not rst))) "
                     "(and (and prev_s_valid (not prev_m_ready)) (or (not m_valid) (ne m_data prev_m_data))))",
        "header_hold": "(and (and have_prev (and (not prev_rst) (not rst))) "
                       "(and (and prev_h_valid (not prev_h_ready)) (and h_valid "
                       "(or (ne h_pad prev_h_pad) (or (ne h_length prev_h_length) "
                       "(ne h_original_length prev_h_original_length))))))",
        "pad_flag": f"(and {_TRANSFER} (xor h_pad (ult h_length 4)))",
        "truncate_flag": f"(and {_TRANSFER} (xor h_truncate (uge h_original_length 8)))",
        "clamped_length": f"(and {_TRANSFER} (or (ult h_length 4) (ugt h_length 8)))",
    },
    "corner": {
        "data_hold": f"(and (not prev_m_last) {REFERENCES['data_hold']})",
        "header_hold": "(and (and have_prev (and (not prev_rst) (not rst))) "
                       "(and (and prev_h_valid (not prev_h_ready)) "
                       "(or (not h_valid) (or (and (ne h_pad prev_h_pad) (ne h_truncate prev_h_truncate)) "
                       "(or (ne h_length prev_h_length) (ne h_original_length prev_h_original_length))))))",
        "pad_flag": f"(and {_PRESENT} (xor h_pad (and (ugt h_original_length 0) (ult h_original_length 4))))",
        "truncate_flag": f"(and (ule h_original_length 255) {REFERENCES['truncate_flag']})",
        "clamped_length": _edit(REFERENCES["clamped_length"], "(ule h_original_length 8)", "(ult h_original_length 8)"),
    },
}

PARTIAL_REPAIRS = ("data_hold", "pad_flag")
ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "results/milestone3/frame-monitor-loop-live/transcript.tar.gz"
FINAL_MEMBER = "frame-live-20261124-194933/egg/round-02/response.json"
FINAL_HASH = "79b6aa2088814e4e288069df23c2458a283e9d194ab4960a1970abc0deb66a0d"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@cache
def _archived_final():
    # An already published historical spelling. The fixture makes no provider calls.
    with tarfile.open(ARCHIVE) as archive:
        response = json.load(archive.extractfile(FINAL_MEMBER))
    monitors = response["output"]["monitors"]
    if monitors.keys() != REFERENCES.keys() or digest(monitors) != FINAL_HASH:
        raise ValueError("archived final frame monitor set differs from the frozen workload")
    return monitors


def fixture_revision(profile, round_number):
    """Return a fresh monitor dict; 0=seed, 1=two repaired properties, 2–3=the same final response."""
    if profile not in SEEDS:
        raise ValueError(f"unknown seed profile {profile!r}")
    if type(round_number) is not int or round_number not in (0, 1, 2, 3):
        raise ValueError("fixture round must be 0, 1, 2 or 3")
    monitors = SEEDS[profile].copy()
    if round_number:
        final = _archived_final()
        for name in PARTIAL_REPAIRS if round_number == 1 else REFERENCES:
            monitors[name] = final[name]
    return monitors


def audit(out):
    """Grade the already-fixed inputs, independently of any prompts or model responses."""
    import z3
    from egg_frame_diagnostic_faults import load_corpus as load_diagnostic
    from egg_frame_faults import load_corpus
    from egg_frame_observe import score_corpus
    from egg_frame_proof import typed_oracle
    from egg_frame_terms import abstract, parse_term, referenced_signals

    base = ROOT / "results/milestone3"
    main = load_corpus(base / "frame-faults")
    diagnostic = load_diagnostic(base / "frame-diagnostic-faults")
    corpus_hashes = {name: json.loads((base / name / "summary.json").read_bytes())["corpus_sha256"]
                     for name in ("frame-faults", "frame-diagnostic-faults")}
    # Original occurs in both native runs; close that control before counting it once.
    if any(main[k] != v for k, v in diagnostic.items() if k[0] == "original"):
        raise ValueError("duplicate original replay differs")
    corpus = {**main, **diagnostic}
    groups = {"development": {"original", "F02", "F05"}, "held_out": {"F01", "F03", "F04", "F06"},
              "diagnostic": {"D01", "D02", "D03"}}
    if set.union(*groups.values()) != {k[0] for k in corpus}:
        raise ValueError("observation inventory changed")
    profiles = {}
    for profile, monitors in SEEDS.items():
        score = score_corpus(corpus, monitors)
        properties = {}
        for name, reference in REFERENCES.items():
            answer = typed_oracle(reference, monitors[name])["oracle"]
            if answer["status"] != "sat":
                raise ValueError(f"frozen starting error failed the independent oracle: {profile}/{name}")
            ref_ast, cand_ast = parse_term(reference), parse_term(monitors[name])
            atoms = abstract(ref_ast)[1].keys() | abstract(cand_ast)[1].keys()
            pins = referenced_signals(ref_ast) | referenced_signals(cand_ast)
            by_group = {}
            for group, designs in groups.items():
                records = [row["properties"][name] for d in sorted(designs) for row in score["cases"][d].values()]
                by_group[group] = {k: sum(r[k] for r in records) for k in
                                   ("reference_alarms", "matched_alarms", "missed", "false_alarm", "unknown", "matched_known")}
            physical_difference = any(x["missed"] or x["false_alarm"] for x in by_group.values())
            properties[name] = {"typed_xor": answer["status"], "reference_value": answer["reference_value"],
                                "candidate_value": answer["candidate_value"],
                                "two_state_assignment": {k: answer["counterexample"][k] for k in sorted(pins)},
                                "union_boolean_atoms": len(atoms), "mismatch_on_observed_pins": physical_difference,
                                "native_samples_by_group": by_group}
        profiles[profile] = {"seed_sha256": digest(monitors), "properties": properties}
    output = {"profile_order": list(SEEDS), "profiles": profiles, "fixture_round_1_repairs": list(PARTIAL_REPAIRS),
              "fixture_round_2_archive_member": FINAL_MEMBER, "fixture_round_2_sha256": FINAL_HASH,
              "group_designs": {k: sorted(v) for k, v in groups.items()}, "profile_set_sha256": digest(SEEDS),
              "reference_sha256": digest(REFERENCES), "native_corpus_sha256": corpus_hashes,
              "z3_version": z3.get_full_version(), "unique_native_cases": len(corpus),
              "complete": True, "provider_calls": 0}
    with out.open("x") as stream:
        stream.write(json.dumps(output, indent=2) + "\n")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True, metavar="NEW_JSON_FILE")
    args = parser.parse_args()
    data = audit(args.audit)
    print(f"Audited {len(data['profiles'])} frozen five-property seed sets at {args.audit}")
