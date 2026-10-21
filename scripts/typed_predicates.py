"""Fail-closed, two-state predicate extraction from Yosys pre-proc RTLIL.

This is a restricted frontend, not a general SystemVerilog parser. Yosys performs
elaboration; process switch/case trees are read before ``proc`` destroys them.
Every exported path includes all enclosing case arms and the process event set.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path


SRC = re.compile(r'\\src "(.+?):(\d+)\.(\d+)-(\d+)\.(\d+)"')
LITERAL = re.compile(r"(\d+)'([01]+)$")


def _src(line):
    match = SRC.search(line)
    return None if not match else {"file": match[1], "start_line": int(match[2]),
                                    "start_column": int(match[3]), "end_line": int(match[4]),
                                    "end_column": int(match[5])}


def _sexpr(node):
    return node if isinstance(node, str) else f'({node[0]} {" ".join(_sexpr(x) for x in node[1:])})'


def _and(nodes):
    result = "true"
    for node in nodes:
        result = node if result == "true" else ("and", result, node)
    return result


def _or(nodes):
    result = "false"
    for node in nodes:
        result = node if result == "false" else ("or", result, node)
    return result


def _neg(node):
    return ("not", node)


def _literal(raw):
    match = LITERAL.fullmatch(raw)
    if not match:
        raise ValueError(f"unsupported RTLIL case literal: {raw}")
    return len(match[2]), int(match[2], 2)


def _concat_parts(signal):
    return signal[2:-2].split() if signal.startswith("{ ") and signal.endswith(" }") else [signal]


class RTLIL:
    def __init__(self, text, source: Path):
        self.source = source.resolve()
        self.lines = source.read_text().splitlines()
        self.source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        self.cells = {}
        self.widths = {}
        self.signed = {}
        self.atoms = {}
        self.processes = []
        self._parse(text)

    def _parse(self, text):
        lines = text.splitlines()
        modules = [row for row in lines if row.startswith("module ")]
        if len(modules) != 1:
            raise ValueError(f"restricted frontend requires exactly one elaborated module, found {len(modules)}")
        i = 0
        pending_src = None
        while i < len(lines):
            row = lines[i]
            if row.startswith("  attribute "):
                pending_src = _src(row) or pending_src
            elif row.startswith("  wire "):
                tokens = row.split()
                self.widths[tokens[-1]] = int(tokens[tokens.index("width") + 1]) if "width" in tokens else 1
                self.signed[tokens[-1]] = "signed" in tokens
                pending_src = None
            elif row.startswith("  cell "):
                cell = {"type": row.split()[1], "name": row.split()[2], "params": {}, "ports": {}, "source": pending_src}
                i += 1
                while i < len(lines) and lines[i] != "  end":
                    part = lines[i].strip().split(maxsplit=2)
                    if len(part) == 3 and part[0] == "parameter": cell["params"][part[1]] = part[2]
                    if len(part) == 3 and part[0] == "connect": cell["ports"][part[1]] = part[2]
                    i += 1
                if "\\Y" in cell["ports"]:
                    self.cells[cell["ports"]["\\Y"]] = cell
                pending_src = None
            elif row.startswith("  process "):
                block = [row]
                i += 1
                while i < len(lines):
                    block.append(lines[i])
                    if lines[i] == "  end": break
                    i += 1
                self.processes.append((block, pending_src))
                pending_src = None
            i += 1

    def _atom(self, definition):
        canonical = json.dumps(definition, sort_keys=True, separators=(",", ":"))
        name = "p_" + hashlib.sha256(canonical.encode()).hexdigest()[:16]
        if name in self.atoms and self.atoms[name] != definition:
            raise ValueError("atom hash collision")
        self.atoms[name] = definition
        return name

    def _width(self, signal):
        if LITERAL.fullmatch(signal): return int(signal.split("'")[0])
        parts = _concat_parts(signal)
        if len(parts) > 1: return sum(self._width(p) for p in parts)
        match = re.fullmatch(r"(.+) \[(\d+)(?::(\d+))?\]", signal)
        if match: return abs(int(match[2]) - int(match[3] or match[2])) + 1
        if signal in self.widths: return self.widths[signal]
        raise ValueError(f"unknown signal width: {signal}")

    def _signal_signed(self, signal):
        return self.signed.get(signal, False)

    def _bool(self, signal):
        literal = LITERAL.fullmatch(signal)
        if literal:
            return "false" if int(literal[2], 2) == 0 else "true"
        if signal in self.cells:
            cell = self.cells[signal]
            kind, ports, params = cell["type"], cell["ports"], cell["params"]
            if kind in ("$logic_not", "$not") and int(params["\\Y_WIDTH"]) == 1:
                return _neg(self._bool(ports["\\A"]))
            if kind in ("$logic_and", "$and", "$logic_or", "$or") and int(params["\\Y_WIDTH"]) == 1:
                return ("and" if kind.endswith("and") else "or", self._bool(ports["\\A"]), self._bool(ports["\\B"]))
            if kind in ("$eq", "$ne") and int(params["\\Y_WIDTH"]) == 1:
                definition = {"op": "eq", "lhs": ports["\\A"], "rhs": ports["\\B"],
                              "lhs_width": int(params["\\A_WIDTH"]), "rhs_width": int(params["\\B_WIDTH"]),
                              "lhs_signed": bool(int(params["\\A_SIGNED"])),
                              "rhs_signed": bool(int(params["\\B_SIGNED"]))}
                if self._width(definition["lhs"]) != definition["lhs_width"] or self._width(definition["rhs"]) != definition["rhs_width"]:
                    raise ValueError(f"width mismatch in {cell['name']}")
                atom = self._atom(definition)
                return atom if kind == "$eq" else _neg(atom)
            raise ValueError(f"unsupported predicate cell {kind} at {cell['name']}")
        width = self._width(signal)
        return self._atom({"op": "nonzero", "signal": signal, "width": width,
                           "signed": self._signal_signed(signal)})

    def _case_guard(self, signal, cases):
        if not cases: raise ValueError("empty explicit case")
        terms = []
        for raw in cases:
            width, value = _literal(raw)
            if width != self._width(signal): raise ValueError(f"case width mismatch: {raw} vs {signal}")
            if width == 1 and value in (0, 1):
                base = self._bool(signal)
                terms.append(base if value else _neg(base))
            else:
                terms.append(self._atom({"op": "case_eq", "signal": signal, "width": width,
                                         "value": value, "signed": self._signal_signed(signal)}))
        return _or(terms)

    def _case_source(self, switch, case, attr):
        """Yosys case `src` can point at the previous line: bind by literal text."""
        if not case:
            return attr, None
        if len(case) == 1 and _literal(case[0])[0] == 1:
            return attr, None
        if switch["source"] is None: raise ValueError("switch has no source span")
        lo, hi = switch["source"]["start_line"], switch["source"]["end_line"]
        needle = case[0].replace("'", "'[bB]?")
        matches = [(line, m.start()+1) for line in range(lo, hi+1)
                   for m in re.finditer(r"(?<![\w'])" + needle + r"\s*:", self.lines[line-1])]
        if len(matches) != 1:
            raise ValueError(f"case literal {case[0]} has {len(matches)} source matches in switch {lo}-{hi}")
        line, column = matches[0]
        return {"file": str(self.source), "start_line": line, "start_column": column,
                "end_line": line, "end_column": column+len(case[0])-1}, "text_literal"

    def extract(self):
        targets, rejected = [], []
        for block, process_src in self.processes:
            events = sorted(re.findall(r"^    sync (posedge|negedge) (\S+)$", "\n".join(block), re.M))
            context = [f"{edge} {signal}" for edge, signal in events] or ["combinational"]
            stack = []
            pending = None
            for row in block[1:]:
                attr = _src(row)
                if attr is not None:
                    pending = attr
                    continue
                stripped = row.strip()
                if stripped.startswith("attribute "):
                    continue
                indent = len(row) - len(row.lstrip())
                if stripped == "end":
                    if stack and stack[-1]["indent"] == indent: stack.pop()
                    pending = None
                    continue
                if stripped.startswith("switch "):
                    stack.append({"signal": stripped[7:], "source": pending, "indent": indent,
                                  "prior": [], "active": None, "poisoned": False})
                    pending = None
                    continue
                if not (stripped == "case" or stripped.startswith("case ")) or not stack:
                    pending = None
                    continue
                switch = stack[-1]
                raw = stripped[5:].strip()
                cases = raw.split() if raw else []
                try:
                    if switch["poisoned"]:
                        raise ValueError("prior case arm was unsupported; full priority guard unavailable")
                    raw_condition = self._case_guard(switch["signal"], cases) if cases else "true"
                    # Case arms have priority unless proven disjoint. Carry the
                    # negation of every preceding arm even for explicit labels.
                    condition = _and([_neg(_or(switch["prior"])), raw_condition]) if switch["prior"] else raw_condition
                    source, map_method = self._case_source(switch, cases, pending)
                    if source is None: raise ValueError("case has no source mapping")
                    if Path(source["file"]).resolve() != self.source:
                        raise ValueError("source mapping file differs from input")
                    if not (1 <= source["start_line"] <= len(self.lines)):
                        raise ValueError("source line out of range")
                    switch["active"] = condition
                    if cases: switch["prior"].append(raw_condition)
                    guard = _and([s["active"] for s in stack])
                    if any(s["active"] is None for s in stack): raise ValueError("case outside active parent arm")
                    loc = f'{source["start_line"]}:{source["start_column"]}'
                    targets.append({"id": f'{self.source.stem}:{block[0].split()[-1]}:{loc}:{raw or "default"}',
                                    "source": str(self.source), "source_sha256": self.source_hash,
                                    "line": source["start_line"], "column": source["start_column"],
                                    "source_text": self.lines[source["start_line"]-1].strip(),
                                    "source_mapping": map_method or "yosys_src",
                                    "process": block[0].split()[-1], "event_context": context,
                                    "case_value": raw or "default", "switch_signal": switch["signal"],
                                    "compact": _sexpr(guard), "guard_depth": len(stack),
                                    "logic": "two_state_binary", "kind": "explicit_case" if cases else "default_case"})
                except ValueError as exc:
                    switch["active"] = None
                    switch["poisoned"] = True
                    rejected.append({"process": block[0].split()[-1], "rtlil_case": stripped,
                                     "source": pending, "reason": str(exc)})
                pending = None
        return {"source": str(self.source), "source_sha256": self.source_hash,
                "semantics": "two-state binary Boolean guards; event context kept separate",
                "atoms": self.atoms, "targets": targets, "unsupported": rejected}


def extract(source: Path, top: str):
    source = Path(source).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        rtlil = Path(tmp) / "preproc.il"
        script = f'read_verilog -sv {source}; hierarchy -check -top {top}; write_rtlil {rtlil}'
        command = subprocess.run(["yosys", "-Q", "-T", "-q", "-p", script],
                                 text=True, capture_output=True, timeout=60)
        if command.returncode: raise RuntimeError(f"Yosys failed: {command.stderr}")
        result = RTLIL(rtlil.read_text(), source).extract()
        result["yosys_command"] = script
        result["yosys_version"] = subprocess.check_output(["yosys", "-V"], text=True).strip()
        result["yosys_warnings"] = command.stderr.strip().splitlines()
        return result


def group_candidates(extraction, min_depth=4):
    """Potential duplicate paths; proof with egg and Z3 is a separate step."""
    groups = defaultdict(list)
    for target in extraction["targets"]:
        if target["kind"] == "explicit_case" and target["guard_depth"] >= min_depth:
            groups[(tuple(target["event_context"]), target["compact"])].append(target)
    return [rows for rows in groups.values() if len({(r["line"], r["column"]) for r in rows}) >= 2]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--top", required=True)
    args = parser.parse_args()
    print(json.dumps(extract(args.source, args.top), indent=2))
