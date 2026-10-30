"""Construct a neutral control matched to the C prompt's API input tokens.

The caller supplies the exact Responses input-token count operation. Matching
uses the complete request messages and response schema, not UTF-8 bytes or a
local tokenizer approximation. Count requests are separate from model calls.
"""
from __future__ import annotations

import json
from collections.abc import Callable


NEUTRAL_PREFIX = "Neutral formatting appendix. No verification evidence."


def replace_egg_with_padding(c_messages: list[dict], units: int) -> list[dict]:
    if units < 0 or len(c_messages) < 2:
        raise ValueError("Expected nonnegative padding and at least two messages")
    payload = json.loads(c_messages[1]["content"])
    if "egg_normalization" not in payload:
        raise ValueError("C prompt has no egg_normalization field")
    del payload["egg_normalization"]
    payload["neutral_token_matched_appendix"] = NEUTRAL_PREFIX + " x" * units
    return [c_messages[0].copy(), {**c_messages[1], "content": json.dumps(payload, sort_keys=True)},
            *[message.copy() for message in c_messages[2:]]]


def match_placebo(c_messages: list[dict], count: Callable[[list[dict]], int],
                  *, tolerance: int = 2, max_counts: int = 12) -> tuple[list[dict], dict]:
    """Return a neutral P prompt or fail closed if its token load differs.

    `count` must call the model provider's exact input-token endpoint with
    the same model, reasoning settings and structured-output schema as the
    generation request. The repeated single-letter filler contains no DUT
    facts, source locations, predicates or witnesses.
    """
    if tolerance < 0 or max_counts < 3:
        raise ValueError("Invalid matching limits")
    calls = 0

    def measured(messages: list[dict]) -> int:
        nonlocal calls
        if calls >= max_counts:
            raise RuntimeError("Token-count call budget exhausted")
        value = count(messages)
        calls += 1
        if type(value) is not int or value < 0:
            raise ValueError("Invalid API input-token count")
        return value

    target = measured(c_messages)
    base_messages = replace_egg_with_padding(c_messages, 0)
    base = measured(base_messages)
    if base > target + tolerance:
        raise RuntimeError("Neutral placebo baseline exceeds C token load")
    best = (abs(base - target), 0, base, base_messages)
    units = max(0, target - base)
    visited = {0}
    while calls < max_counts and units not in visited:
        visited.add(units)
        candidate = replace_egg_with_padding(c_messages, units)
        actual = measured(candidate)
        if abs(actual - target) < best[0]:
            best = (abs(actual - target), units, actual, candidate)
        if best[0] <= tolerance:
            break
        # " x" normally contributes one token per unit, but the provider
        # count remains authoritative and the loop checks the actual delta.
        if units and actual != base:
            # Estimate the provider's observed tokens per filler unit. This
            # also works for offline fake counters that are byte-based.
            units = max(0, round(units * (target - base) / (actual - base)))
        else:
            units = max(0, units + target - actual)
    if best[0] > tolerance:
        raise RuntimeError(f"Could not match C input tokens: delta={best[0]}")
    _, units, actual, messages = best
    return messages, {"method": "Responses input_tokens.count",
                      "c_input_tokens": target, "placebo_input_tokens": actual,
                      "absolute_delta": abs(actual - target),
                      "padding_units": units, "count_requests": calls,
                      "tolerance_tokens": tolerance}
