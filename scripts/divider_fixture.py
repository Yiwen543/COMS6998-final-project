"""Public-I/O arithmetic checker and exact JSON stimulus boundary for radix2_div."""
from __future__ import annotations

from pathlib import Path

FIELDS = {"rst_n": 1, "start": 1, "dividend": 8, "divisor": 8}


def schema():
    return {"type": "object", "additionalProperties": False, "required": ["actions"],
            "properties": {"actions": {"type": "array", "items": {
                "type": "object", "additionalProperties": False, "required": list(FIELDS),
                "properties": {field: {"type": "integer"} for field in FIELDS}}}}}


def validate_actions(payload, limit, *, require_initial_reset=True):
    if not isinstance(payload, dict) or set(payload) != {"actions"}:
        raise ValueError("Expected one actions array")
    actions = payload["actions"]
    if not isinstance(actions, list) or not 1 <= len(actions) <= limit:
        raise ValueError(f"Expected 1..{limit} actions")
    for i, action in enumerate(actions):
        if not isinstance(action, dict) or set(action) != set(FIELDS):
            raise ValueError(f"Action {i}: exact fields {sorted(FIELDS)} required")
        for name, width in FIELDS.items():
            if type(action[name]) is not int or not 0 <= action[name] < 1 << width:
                raise ValueError(f"Action {i}: {name} must be an unsigned {width}-bit integer")
        if not action["rst_n"] and action["start"]:
            raise ValueError(f"Action {i}: start while reset asserted")
    if require_initial_reset and actions[0]["rst_n"] != 0:
        raise ValueError("First action must reset the divider")
    return actions


def write_vectors(actions, path: Path):
    validate_actions({"actions": actions}, len(actions))
    path.write_text("".join(" ".join(f"{action[field]:x}" for field in FIELDS) + "\n"
                            for action in actions))


TRACE = ("step", "pre_q", "pre_r", "pre_done", "q", "r", "done")


def parse_trace(log):
    rows = []
    for line in log.splitlines():
        if line.startswith("TRACE "):
            values = line.split()[1:]
            if len(values) != len(TRACE):
                raise ValueError(f"Malformed divider trace: {line}")
            rows.append(dict(zip(TRACE, (-1 if any(ch in value.lower() for ch in "xz")
                                         else int(value, 16) for value in values))))
    return rows


def check(actions, log):
    validate_actions({"actions": actions}, len(actions))
    trace = parse_trace(log)
    if len(trace) != len(actions):
        raise ValueError("Trace/action count mismatch")
    prior = None
    remaining = 0
    op = None
    failures = []
    checks = 0
    for cycle, (action, row) in enumerate(zip(actions, trace)):
        if row["step"] != cycle:
            raise ValueError("Trace step mismatch")

        def require(category, phase, actual, expected):
            nonlocal checks
            checks += 1
            if actual != expected:
                failures.append({"cycle": cycle, "category": category,
                                 "phase": phase, "actual": actual, "expected": expected})

        if not action["rst_n"]:
            for name in ("pre_q", "pre_r", "pre_done", "q", "r", "done"):
                require("async_reset", "pre" if name.startswith("pre") else "post", row[name], 0)
            remaining, op = 0, None
        else:
            if prior is not None:
                for pre, post in (("pre_q", "q"), ("pre_r", "r"), ("pre_done", "done")):
                    require("registered_hold", "pre", row[pre], prior[post])
            if remaining:
                if action["start"]:
                    raise ValueError(f"Action {cycle}: start while divider busy")
                if (action["dividend"], action["divisor"]) != op:
                    raise ValueError(f"Action {cycle}: operands changed while divider busy")
                remaining -= 1
                require("done_timing", "post", row["done"], int(remaining == 0))
                if remaining == 0:
                    dividend, divisor = op
                    require("quotient", "post", row["q"], dividend // divisor)
                    require("remainder", "post", row["r"], dividend % divisor)
                    op = None
            elif action["start"]:
                if action["divisor"] == 0:
                    require("done_timing", "post", row["done"], 1)
                    require("divzero_quotient", "post", row["q"], 255)
                    require("divzero_remainder", "post", row["r"], 255)
                else:
                    op = (action["dividend"], action["divisor"])
                    remaining = 8
                    require("done_timing", "post", row["done"], 0)
                    require("start_quotient", "post", row["q"], 0)
            else:
                require("done_timing", "post", row["done"], 0)
                if prior is not None:
                    require("idle_quotient_hold", "post", row["q"], prior["q"])
                    require("idle_remainder_hold", "post", row["r"], prior["r"])
        prior = row
    return {"checks": checks, "failures": failures,
            "distinct_defects": sorted({f["category"] for f in failures}),
            "pending_operation": bool(remaining), "remaining_edges": remaining}
