"""Frozen action interfaces and specification checks for midterm candidates.

The checker consumes only public top-level I/O traces. It never reads DUT
internals or a benchmark-provided testbench. Action validation is shared by
offline, development, and eventual held-out runs.
"""
from __future__ import annotations

import json
from pathlib import Path


CODEC_FIELDS = {"reset", "enc_data", "enc_control", "dec_valid", "dec_word"}
SEARCH_FIELDS = {"reset", "start", "pause", "key", "write_en", "write_addr", "write_data"}
CODEC_TYPES = {0x1E, 0x33, 0x78, 0x87, 0x99, 0xAA, 0xB4, 0xCC, 0xD2,
               0xE1, 0xFF, 0x2D, 0x4B, 0x55, 0x66}
CODEC_CONTROLS = {0x1E: 0xFF, 0x33: 0x1F, 0x78: 0x01, 0x87: 0xFE,
                  0x99: 0xFE, 0xAA: 0xFC, 0xB4: 0xF8, 0xCC: 0xF0,
                  0xD2: 0xE0, 0xE1: 0xC0, 0xFF: 0x80, 0x2D: 0x1F,
                  0x4B: 0xF1, 0x55: 0x11, 0x66: 0x11}
SPECS = {
    "codec": {"reset": 1, "enc_data": 64, "enc_control": 8, "dec_valid": 1, "dec_word": 66},
    "search": {"reset": 1, "start": 1, "pause": 1, "key": 8,
               "write_en": 1, "write_addr": 3, "write_data": 8},
}


def validate_actions(ip: str, payload: dict, limit: int) -> list[dict]:
    if ip not in SPECS or not isinstance(payload, dict) or set(payload) != {"actions"}:
        raise ValueError("Expected one actions array for a known IP")
    actions = payload["actions"]
    if not isinstance(actions, list) or not 1 <= len(actions) <= limit:
        raise ValueError(f"Expected 1..{limit} actions")
    widths = SPECS[ip]
    for index, action in enumerate(actions):
        if not isinstance(action, dict) or set(action) != set(widths):
            raise ValueError(f"Action {index}: exact fields required: {sorted(widths)}")
        for field, width in widths.items():
            if type(action[field]) is not int or not 0 <= action[field] < (1 << width):
                raise ValueError(f"Action {index}: {field} must be unsigned {width}-bit integer")
        if ip == "search" and action["reset"] and (action["start"] or action["write_en"]):
            raise ValueError(f"Action {index}: no start or write while reset is asserted")
        if ip == "search" and action["start"] and (action["write_en"] or action["pause"]):
            raise ValueError(f"Action {index}: start must be a separate unpaused cycle")
    return actions


def schema(ip: str) -> dict:
    widths = SPECS[ip]
    return {"type": "object", "additionalProperties": False, "required": ["actions"],
            "properties": {"actions": {"type": "array", "items": {
                "type": "object", "additionalProperties": False,
                "required": list(widths),
                "properties": {name: {"type": "integer"}
                               for name, width in widths.items()}}}}}


def write_vectors(ip: str, actions: list[dict], path: Path) -> None:
    validate_actions(ip, {"actions": actions}, len(actions))
    order = list(SPECS[ip])
    path.write_text("".join(" ".join(f"{a[name]:x}" for name in order) + "\n" for a in actions))


def parse_trace(text: str, ip: str) -> list[dict]:
    names = (["step", "pre_reset_enc", "pre_reset_data", "pre_reset_control", "pre_reset_sync", "pre_reset_error",
              "enc", "dec_data", "dec_control", "sync", "error"] if ip == "codec" else
             ["step", "pre_reset_done", "pre_reset_count", "pre_reset_indices", "pre_reset_overflow",
              "done", "count", "indices", "overflow"])
    rows = []
    for line in text.splitlines():
        if line.startswith("TRACE "):
            values = line.split()[1:]
            if len(values) != len(names):
                raise ValueError(f"Malformed {ip} trace: {line}")
            rows.append(dict(zip(names, (int(value, 16) for value in values))))
    return rows


def check_codec(actions: list[dict], trace: list[dict]) -> dict:
    if len(actions) != len(trace):
        raise ValueError("Trace/action count mismatch")
    failures = []
    checks = 0
    previous = None
    previous_control = None
    for index, (action, observed) in enumerate(zip(actions, trace)):
        if observed["step"] != index:
            raise ValueError("Trace step mismatch")
        def require(category, actual, expected):
            nonlocal checks
            checks += 1
            if actual != expected:
                failures.append({"cycle": index, "category": category,
                                 "actual": actual, "expected": expected})
        if action["reset"]:
            # Top-level specification says active-high synchronous reset. A
            # pre-clock assertion must preserve the previous registered value.
            if previous is not None:
                for short, pre in (("dec_data", "pre_reset_data"),
                                   ("dec_control", "pre_reset_control"), ("sync", "pre_reset_sync"),
                                   ("error", "pre_reset_error")):
                    require("reset_timing", observed[pre], previous[short])
                if previous_control == action["enc_control"]:
                    require("reset_timing", observed["pre_reset_enc"], previous["enc"])
            for short in ("enc", "dec_data", "dec_control", "sync", "error"):
                require("reset_value", observed[short], 0)
        else:
            if action["enc_control"] == 0:
                require("encoder_data", observed["enc"], (1 << 64) | action["enc_data"])
            else:
                require("encoder_control_header", observed["enc"] >> 64, 2)
                data, mask = action["enc_data"], action["enc_control"]
                expected_type = None
                if mask == 0xFF and data in (0x0707070707070707, 0xFEFEFEFEFEFEFEFE):
                    expected_type = 0x1E
                elif mask == 0x1F and data & ((1 << 40) - 1) == 0xFB07070707:
                    expected_type = 0x33
                elif mask == 0x1F and data & ((1 << 40) - 1) == 0x9C07070707:
                    expected_type = 0x2D
                elif mask == 0x01 and data & 0xFF == 0xFB:
                    expected_type = 0x78
                if expected_type is not None:
                    require("encoder_type", (observed["enc"] >> 56) & 0xFF, expected_type)
            if action["dec_valid"]:
                word = action["dec_word"]
                header, payload = word >> 64, word & ((1 << 64) - 1)
                require("decoder_sync", observed["sync"], int(header not in (1, 2)))
                if header == 1:
                    require("decoder_data", observed["dec_data"], payload)
                    require("decoder_control", observed["dec_control"], 0)
                    require("decoder_error", observed["error"], 0)
                elif header == 2:
                    typ = payload >> 56
                    require("decoder_type", observed["dec_control"], CODEC_CONTROLS.get(typ, 0))
                    if typ not in CODEC_TYPES:
                        require("decoder_type_error", observed["error"], 1)
                    elif typ == 0x78:
                        require("decoder_data", observed["dec_data"],
                                ((payload & ((1 << 56) - 1)) << 8) | 0xFB)
            elif previous is not None:
                for short in ("dec_data", "dec_control", "sync", "error"):
                    require("decoder_hold", observed[short], previous[short])
        previous = {key: observed[key] for key in ("enc", "dec_data", "dec_control", "sync", "error")}
        previous_control = action["enc_control"]
    return {"checks": checks, "failures": failures,
            "distinct_defects": sorted({f["category"] for f in failures})}


def check_search(actions: list[dict], trace: list[dict]) -> dict:
    if len(actions) != len(trace):
        raise ValueError("Trace/action count mismatch")
    failures = []
    checks = 0
    memory: list[int | None] = [None] * 8
    prior = None
    busy = False
    search_key = None
    expected_indices = []
    expected_done_step = None
    for index, (action, observed) in enumerate(zip(actions, trace)):
        if observed["step"] != index:
            raise ValueError("Trace step mismatch")
        def require(category, actual, expected):
            nonlocal checks
            checks += 1
            if actual != expected:
                failures.append({"cycle": index, "category": category,
                                 "actual": actual, "expected": expected})
        if action["reset"]:
            if prior is not None:
                for short, pre in (("done", "pre_reset_done"), ("count", "pre_reset_count"),
                                   ("indices", "pre_reset_indices"), ("overflow", "pre_reset_overflow")):
                    require("reset_timing", observed[pre], prior[short])
            for short in ("done", "count", "indices", "overflow"):
                require("reset_value", observed[short], 0)
            busy, expected_done_step, search_key, expected_indices = False, None, None, []
            memory = [None] * 8
        else:
            if action["write_en"]:
                if busy:
                    raise ValueError(f"Action {index}: write while search active")
                memory[action["write_addr"]] = action["write_data"]
            if action["start"]:
                if busy or any(value is None for value in memory):
                    raise ValueError(f"Action {index}: start before full memory initialization or while busy")
                busy = True
                search_key = action["key"]
                expected_indices = [i for i, value in enumerate(memory) if value == search_key]
                # Eight entries, one-cycle synchronous read, then the
                # specified two-cycle completion latency.
                expected_done_step = index + 10
            if busy:
                if action["key"] != search_key:
                    raise ValueError(f"Action {index}: key changed during active search")
                if action["pause"]:
                    expected_done_step += 1
                due = index == expected_done_step
                require("done_timing", observed["done"], int(due))
                if due:
                    require("match_count", observed["count"], min(len(expected_indices), 2))
                    require("match_overflow", observed["overflow"], int(len(expected_indices) > 2))
                    for slot, expected in enumerate(expected_indices[:2]):
                        require("match_index", (observed["indices"] >> (3 * slot)) & 7, expected)
                    busy, expected_done_step = False, None
            else:
                require("done_timing", observed["done"], 0)
        prior = {name: observed[name] for name in ("done", "count", "indices", "overflow")}
    return {"checks": checks, "failures": failures,
            "distinct_defects": sorted({f["category"] for f in failures}),
            "pending_search": busy}


def check(ip: str, actions: list[dict], simulator_text: str) -> dict:
    trace = parse_trace(simulator_text, ip)
    return check_codec(actions, trace) if ip == "codec" else check_search(actions, trace)
