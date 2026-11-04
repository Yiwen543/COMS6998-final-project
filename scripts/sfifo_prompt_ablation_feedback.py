"""Lossless raw-counter packing and proven semantic feedback for FIFO ablation."""
from __future__ import annotations

import json

from semantic_candidate_scan import map_true_counter
from sfifo_stress_feedback import INSTRUCTIONS, SPEC, SEED, raw_feedback
from run_sfifo_stress_fixed import SOURCE
from run_midterm_fixed import ROOT
from sfifo_fixture import FIELDS


def pack_raw(rows: list[dict]) -> dict:
    sources = sorted({row["source"] for row in rows})
    source_ids = {source: i for i, source in enumerate(sources)}
    predicates = {f'{source_ids[row["source"]]}:{row["line"]}': row["source_text"]
                  for row in rows}
    packed = {"encoding": "lossless_source_line_dictionary_v1",
              "sources": sources,
              "predicates_by_source_id_and_line": predicates,
              "point_columns": ["source_id", "line", "column", "counter_type", "outcome", "hits"],
              "points": [[source_ids[row["source"]], row["line"], row["column"],
                          row["counter_type"], row["outcome"], row["hits"]]
                         for row in rows]}
    if unpack_raw(packed) != rows:
        raise AssertionError("Raw counter packing was not lossless")
    return packed


def unpack_raw(packed: dict) -> list[dict]:
    if packed["point_columns"] != ["source_id", "line", "column", "counter_type", "outcome", "hits"]:
        raise ValueError("Unexpected raw counter schema")
    sources, predicates = packed["sources"], packed["predicates_by_source_id_and_line"]
    return [{"source": sources[row[0]], "line": row[1], "column": row[2],
             "counter_type": row[3], "outcome": row[4], "hits": row[5],
             "source_text": predicates[f"{row[0]}:{row[1]}"]}
            for row in packed["points"]]


def egg_feedback(semantic: dict, points: list[dict]) -> dict:
    source_name = str(SOURCE.relative_to(ROOT))
    if semantic["source"] != str(SOURCE.resolve()):
        raise AssertionError("Semantic evidence refers to a different RTL file")
    groups = []
    incomplete_mappings = []
    for group in semantic["groups"]:
        if not group["requires_egg_rewrite_to_merge"]:
            continue
        members = []
        for member in group["members"]:
            mapped = map_true_counter(member, points)
            if mapped["status"] != "mapped":
                incomplete_mappings.append({"eclass": group["eclass"],
                                            "source": source_name, "line": member["line"],
                                            "status": mapped["status"],
                                            "reason": mapped.get("reason")})
                members = []
                break
            point = mapped["point"]
            members.append({"source": source_name, "line": member["line"],
                            "column": point["column"], "counter_type": point["type"],
                            "outcome": point["outcome"], "hits": point["hits"],
                            "complete_activation_guard": member["compact"],
                            "source_mapping": member["source_mapping"]})
        if members and any(member["hits"] == 0 for member in members):
            groups.append({"eclass": group["eclass"],
                           "event_context": group["event_context"],
                           "equivalent_expression_count": group["distinct_input_expressions"],
                           "representative": group["representative"],
                           "eclass_nodes": group["eclass_nodes"],
                           "independent_z3_pair_checks": group["independent_z3_checks"],
                           "members": members})
    return {"engine": semantic["egg"]["engine"],
            "semantics": "binary/two-state guards only; no four-state, sequential, or cross-clock equivalence claim",
            "source_sha256": semantic["source_sha256"],
            "typed_atoms": semantic["atoms"],
            "equivalent_uncovered_groups": groups,
            "incomplete_source_mappings": incomplete_mappings,
            "unsupported_extraction": semantic["unsupported"],
            "unresolved_aliases": semantic["unresolved_aliases"]}


def messages_for(arm: str, history: list[dict], result: dict, log: str,
                 points: list[dict], semantic: dict, round_no: int, limit: int) -> list[dict]:
    if arm not in ("B_full", "B_compact", "P_compact", "C_compact"):
        raise ValueError("Unknown ablation arm")
    payload = {"specification": SPEC.read_text(),
               "rtl": {str(SOURCE.relative_to(ROOT)): SOURCE.read_text()},
               "initial_stimulus": json.loads(SEED.read_text())["actions"],
               "previous_generated_actions": history,
               "round": round_no, "max_new_cycles": limit,
               "stimulus_fields_and_widths": FIELDS,
               "checker": {"checks": result["checker"]["checks"],
                           "distinct_defects": result["checker"]["distinct_defects"],
                           "first_failures": result["checker"]["failures"][:8],
                           "execution_log": [line for line in log.splitlines()
                                             if line.startswith("TRACE ")][-40:]}}
    raw = raw_feedback(points)
    payload["raw_uncovered_dut_coverage"] = raw if arm == "B_full" else pack_raw(raw)
    if arm == "C_compact":
        payload["egg_normalization"] = egg_feedback(semantic, points)
    return [{"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": json.dumps(payload, sort_keys=True)}]
