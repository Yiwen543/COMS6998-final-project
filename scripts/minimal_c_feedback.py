"""Exploratory relation-only C renderer. No new claims, witnesses or target hints.

This distills the existing C appendix; it is not lossless reconstruction of
the full appendix. The raw B payload and C's group-selection policy are fixed.
"""
from __future__ import annotations

import copy
import json


def distill_egg(full: dict) -> dict:
    groups = full["equivalent_uncovered_groups"]
    sources = sorted({m["source"] for g in groups for m in g["members"]})
    ids = {source: i for i, source in enumerate(sources)}
    return {
        "claim": "Within each group, complete activation guards at listed source sites are equivalent under binary/two-state semantics and the listed event context. Every source counter is measured separately; no hit transfers between sites.",
        "sources": sources,
        "counter_columns": ["source_id", "line", "column", "counter_type", "outcome", "hits"],
        "groups": [{"event_context": group["event_context"],
                    "equivalent_guard_sites": [[ids[m["source"]], m["line"], m["column"],
                                                 m["counter_type"], m["outcome"], m["hits"]]
                                                for m in group["members"]]}
                   for group in groups],
    }


def minimal_c_messages(c_messages: list[dict]) -> list[dict]:
    messages = copy.deepcopy(c_messages)
    payload = json.loads(messages[1]["content"])
    if "egg_normalization" not in payload:
        raise ValueError("Expected full C evidence")
    if not isinstance(payload.get("raw_uncovered_dut_coverage"), dict):
        raise ValueError("Expected the unchanged compact B base")
    payload["egg_normalization"] = distill_egg(payload["egg_normalization"])
    messages[1]["content"] = json.dumps(payload, sort_keys=True)
    return messages


def common_payload(messages):
    payload = json.loads(messages[1]["content"])
    payload.pop("egg_normalization", None)
    return payload
