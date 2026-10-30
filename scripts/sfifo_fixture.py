"""Specification-derived public-I/O contract for pinned ZipCPU sfifo.

The caller selects a power-of-two capacity (8 by default, 16 for the stress
variant). Async front read, no write on full, no read on empty. Binary/two-state
simulation only. Expected contents come from public handshakes, never DUT
pointers or storage.
"""
from __future__ import annotations

import json
from pathlib import Path

FIELDS = {"reset": 1, "wr": 1, "rd": 1, "data": 8}
CAPACITY = 8


def schema() -> dict:
    return {"type": "object", "additionalProperties": False, "required": ["actions"],
            "properties": {"actions": {"type": "array", "items": {
                "type": "object", "additionalProperties": False, "required": list(FIELDS),
                "properties": {name: {"type": "integer"} for name in FIELDS}}}}}


def validate_actions(payload: dict, limit: int, *, require_initial_reset: bool = True) -> list[dict]:
    if not isinstance(payload, dict) or set(payload) != {"actions"}:
        raise ValueError("Expected only an actions array")
    actions = payload["actions"]
    if not isinstance(actions, list) or not 1 <= len(actions) <= limit:
        raise ValueError(f"Expected 1..{limit} actions")
    for i, action in enumerate(actions):
        if not isinstance(action, dict) or set(action) != set(FIELDS):
            raise ValueError(f"Action {i}: exact fields required: {sorted(FIELDS)}")
        for name, width in FIELDS.items():
            if type(action[name]) is not int or not 0 <= action[name] < 1 << width:
                raise ValueError(f"Action {i}: {name} must be an unsigned {width}-bit integer")
        if action["reset"] and (action["wr"] or action["rd"]):
            raise ValueError(f"Action {i}: read/write during reset is outside frozen contract")
    if require_initial_reset and actions[0]["reset"] != 1:
        raise ValueError("First action must synchronously reset the FIFO")
    return actions


def write_vectors(actions: list[dict], path: Path) -> None:
    validate_actions({"actions": actions}, len(actions))
    path.write_text("".join(" ".join(f"{action[field]:x}" for field in FIELDS) + "\n"
                            for action in actions))


TRACE = ("step", "pre_fill", "pre_full", "pre_empty", "pre_data",
         "post_fill", "post_full", "post_empty", "post_data")


def parse_trace(log: str) -> list[dict]:
    def parse_hex(field: str) -> int:
        # Icarus reports uninitialized empty-storage data as x. The checker
        # deliberately ignores empty data; an x in a checked field fails.
        return -1 if any(char in field.lower() for char in "xz") else int(field, 16)

    rows = []
    for line in log.splitlines():
        if line.startswith("TRACE "):
            fields = line.split()[1:]
            if len(fields) != len(TRACE):
                raise ValueError(f"Malformed FIFO trace: {line}")
            rows.append(dict(zip(TRACE, (parse_hex(field) for field in fields))))
    return rows


def check(actions: list[dict], log: str, *, capacity: int = CAPACITY) -> dict:
    if type(capacity) is not int or capacity < 2 or capacity & (capacity - 1):
        raise ValueError("FIFO capacity must be a power of two >= 2")
    validate_actions({"actions": actions}, len(actions))
    rows = parse_trace(log)
    if len(rows) != len(actions):
        raise ValueError("Trace/action count mismatch")
    queue: list[int] = []
    failures: list[dict] = []
    checks = 0
    for cycle, (action, row) in enumerate(zip(actions, rows)):
        if row["step"] != cycle:
            raise ValueError("Trace step mismatch")

        def require(category: str, phase: str, actual: int, expected: int):
            nonlocal checks
            checks += 1
            if actual != expected:
                failures.append({"cycle": cycle, "category": category, "phase": phase,
                                 "actual": actual, "expected": expected})

        # Observe after inputs settle, before active edge. A synchronous reset
        # cannot change these state-derived outputs before the rising edge.
        for phase in ("pre", "post"):
            if phase == "post":
                if action["reset"]:
                    queue.clear()
                else:
                    # Handshakes use pre-edge occupancy. At full, simultaneous
                    # read/write only reads. At empty, it only writes.
                    pre_count = len(queue)
                    pop = bool(action["rd"] and pre_count > 0)
                    push = bool(action["wr"] and pre_count < capacity)
                    if pop:
                        queue.pop(0)
                    if push:
                        queue.append(action["data"])
            require("fill", phase, row[f"{phase}_fill"], len(queue))
            require("full", phase, row[f"{phase}_full"], int(len(queue) == capacity))
            require("empty", phase, row[f"{phase}_empty"], int(len(queue) == 0))
            if queue:
                require("data_order", phase, row[f"{phase}_data"], queue[0])
    return {"checks": checks, "failures": failures,
            "distinct_defects": sorted({item["category"] for item in failures})}
