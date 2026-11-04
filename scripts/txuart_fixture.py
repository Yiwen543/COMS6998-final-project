"""Fixed 8N1 UART stimulus schema and independent public-pin frame checker."""
from __future__ import annotations

import json
from pathlib import Path


def schema() -> dict:
    bit = {"type": "integer", "enum": [0, 1]}
    return {"type": "object", "additionalProperties": False, "required": ["actions"],
            "properties": {"actions": {"type": "array", "items": {
                "type": "object", "additionalProperties": False,
                "required": ["reset", "break", "wr", "data"],
                "properties": {"reset": bit, "break": bit, "wr": bit,
                               "data": {"type": "integer", "minimum": 0, "maximum": 255}}}}}}


def validate_actions(payload, limit: int, *, require_initial_reset: bool = False) -> list[dict]:
    if not isinstance(payload, dict) or set(payload) != {"actions"}:
        raise ValueError("Expected only an actions array")
    actions = payload["actions"]
    if not isinstance(actions, list) or not 1 <= len(actions) <= limit:
        raise ValueError(f"Expected 1..{limit} cycle actions")
    for index, item in enumerate(actions):
        if not isinstance(item, dict) or set(item) != {"reset", "break", "wr", "data"}:
            raise ValueError(f"Invalid action fields at cycle {index}")
        if any(type(item[name]) is not int or item[name] not in (0, 1)
               for name in ("reset", "break", "wr")):
            raise ValueError(f"Invalid control width at cycle {index}")
        if type(item["data"]) is not int or not 0 <= item["data"] <= 255:
            raise ValueError(f"Invalid byte at cycle {index}")
    if require_initial_reset and (len(actions) < 2 or actions[0]["reset"] != 1 or
                                  actions[1]["reset"] != 1):
        raise ValueError("Common seed needs two reset clocks")
    return actions


def write_vectors(actions: list[dict], path: Path) -> None:
    path.write_text("".join(f"{a['reset']} {a['break']} {a['wr']} {a['data']}\n" for a in actions))


def check(actions: list[dict], log: str, *, baud: int = 2) -> dict:
    rows = []
    for line in log.splitlines():
        if not line.startswith("TRACE "):
            continue
        fields = line.split()
        if len(fields) != 9:
            raise ValueError(f"Malformed UART trace: {line}")
        values = [int(x) if x.lower() not in ("x", "z") else None for x in fields[1:]]
        rows.append(dict(zip(("cycle", "reset", "break", "wr", "data",
                              "pre_busy", "busy", "tx"), values)))
    if len(rows) != len(actions) or any(r["cycle"] != i for i, r in enumerate(rows)):
        raise ValueError("UART trace length/order differs from fixed actions")
    failures = []
    for i, (row, action) in enumerate(zip(rows, actions)):
        if any(row[key] != action[key] for key in ("reset", "break", "wr", "data")):
            failures.append({"cycle": i, "category": "driver", "detail": "trace input mismatch"})
        if row["tx"] not in (0, 1) or row["busy"] not in (0, 1):
            failures.append({"cycle": i, "category": "unknown_output"})
        if row["reset"] and row["tx"] != 1:
            failures.append({"cycle": i, "category": "reset_serial_idle"})
        if row["break"] and not row["reset"] and row["tx"] != 0:
            failures.append({"cycle": i, "category": "break_serial_low"})

    # Split at reset and break. They may abort an incomplete frame. Decode
    # completed 8N1 frames from the public pin; internal state is never read.
    segments = []
    segment = []
    for row in rows:
        if row["reset"] or row["break"]:
            if segment:
                segments.append((segment, True))
                segment = []
        else:
            segment.append(row)
    if segment:
        segments.append((segment, False))
    decoded = []
    accepted = []
    for segment, aborted in segments:
        expected = [(r["cycle"], r["data"]) for r in segment
                    if r["wr"] == 1 and r["pre_busy"] == 0]
        accepted.extend(expected)
        cursor = 0
        found = []
        # A break may leave the line low at the start of a segment; require
        # an observed high-to-low edge to call it a new start bit.
        while cursor < len(segment):
            row = segment[cursor]
            previous = segment[cursor-1]["tx"] if cursor else (
                rows[row["cycle"]-1]["tx"] if row["cycle"] else 1)
            if previous == 1 and row["tx"] == 0:
                stop_index = cursor + baud * 9 + baud // 2
                if stop_index >= len(segment):
                    break
                bits = [segment[cursor + baud + baud//2 + baud*k]["tx"]
                        for k in range(8)]
                stop = segment[stop_index]["tx"]
                if any(bit not in (0, 1) for bit in bits) or stop != 1:
                    failures.append({"cycle": row["cycle"], "category": "uart_frame",
                                     "detail": "invalid data or stop bit"})
                else:
                    value = sum(bit << bitno for bitno, bit in enumerate(bits))
                    found.append((row["cycle"], value))
                    decoded.append((row["cycle"], value))
                cursor += baud * 10
            else:
                cursor += 1
        for index, (start_cycle, value) in enumerate(found):
            if index >= len(expected) or value != expected[index][1]:
                failures.append({"cycle": start_cycle, "category": "uart_data",
                                 "actual": value,
                                 "expected": expected[index][1] if index < len(expected) else None})
        if not aborted and len(found) != len(expected):
            failures.append({"cycle": segment[-1]["cycle"], "category": "missing_frame",
                             "accepted": len(expected), "decoded": len(found)})
    return {"checks": len(rows), "accepted_bytes": len(accepted),
            "decoded_frames": len(decoded), "failures": failures,
            "distinct_defects": sorted({f["category"] for f in failures})}


if __name__ == "__main__":
    import sys
    print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())["actions"],
                           Path(sys.argv[2]).read_text()), indent=2))
