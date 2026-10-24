"""Frozen JSON stimulus contract and isolated B/C queue feedback."""
import json
from pathlib import Path

from pilot_feedback import raw_coverage
from predicates import ROOT

BASE = ROOT / "examples/heldout_queue"
SPEC = BASE / "docs/specification.md"
CHECKER = BASE / "verif/tb_queue_pilot.sv"
VERSIONS = {"original": (BASE / "rtl/queue.sv", "queue"),
            "variant": (BASE / "rtl/queue_variant.sv", "queue_variant")}
FIELDS = ("reset_n", "clear", "enable", "write", "read", "data")
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["actions"],
          "properties": {"actions": {"type": "array", "items": {
              "type": "object", "additionalProperties": False, "required": list(FIELDS),
              "properties": {name: {"type": "integer"} for name in FIELDS}}}}}
INITIAL = ([dict(reset_n=0, clear=0, enable=0, write=0, read=0, data=0)] * 2 +
           [dict(reset_n=1, clear=0, enable=0, write=0, read=0, data=0)] * 4)
INSTRUCTIONS = """You generate only JSON cycle actions for a fixed, independent queue checker.
Every action has integer reset_n, clear, enable, write, read (0 or 1) and data (0..4294967295). Maximum action count is in the request.
The driver applies signals before each rising clock edge. Reset is asynchronous active-low; clear is synchronous; enable gates operations. The module has DEPTH=4 and DBITS=32. The usable capacity is three items under this frozen contract. Write-only is legal below capacity, read-only when nonempty; simultaneous write/read is legal at any occupancy. Reset/clear override operations. To test enable hold, write/read may be asserted while enable is zero.
The checker independently tests valid front data, empty/full, reset, clear, and enable hold. Almost-empty/full normal-operation thresholds are ambiguous in the supplied prose and are observed but not scored beyond reset/clear.
Maximize DUT line/case and other structural coverage using as few cycles as possible. You may change stimulus only. The DUT, checker, driver, and measurement scripts are fixed. A checker failure on faulty RTL is a finding. Return JSON only, with no extra fields or prose."""


def validate_actions(value, limit, prior=None):
    if not isinstance(value, dict) or set(value) != {"actions"} or not isinstance(value["actions"], list):
        raise ValueError("Expected only an actions array")
    actions = value["actions"]
    if not 1 <= len(actions) <= limit:
        raise ValueError(f"Expected 1..{limit} actions")
    count = 0
    for index, item in enumerate((prior or []) + actions):
        if not isinstance(item, dict) or set(item) != set(FIELDS):
            raise ValueError(f"Action {index}: expected exactly {FIELDS}")
        for field, maximum in (("reset_n", 1), ("clear", 1), ("enable", 1),
                               ("write", 1), ("read", 1), ("data", 0xffffffff)):
            if type(item[field]) is not int or not 0 <= item[field] <= maximum:
                raise ValueError(f"Action {index}: {field} must be integer 0..{maximum}")
        if not item["reset_n"] or item["clear"]:
            count = 0
        elif item["enable"]:
            if item["write"] and not item["read"]:
                if count == 3: raise ValueError(f"Action {index}: illegal write-only at full")
                count += 1
            elif item["read"] and not item["write"]:
                if count == 0: raise ValueError(f"Action {index}: illegal read-only at empty")
                count -= 1
    return actions


def mapped_groups(targets, graph, points, atoms, all_targets=None):
    roots = {row["id"]: row for row in graph["targets"]}
    forms = {}
    for target in all_targets or targets:
        key = (roots[target["id"]]["eclass"], tuple(target["event_context"]))
        forms.setdefault(key, set()).add(target["compact"])
    groups = {}
    for target in targets:
        if target["guard_depth"] != 4 or target["case_value"] not in ("2'01", "2'10"):
            continue
        matches = [p for p in points if p["line"] == target["line"] and
                   p["type"] == "line" and p["outcome"] == "case"]
        if len(matches) != 1:
            raise ValueError(f"Missing/ambiguous counter for {target['id']}")
        point = matches[0]
        if point["hits"]:
            continue
        root = roots[target["id"]]
        group = groups.setdefault(root["eclass"], {"eclass": root["eclass"],
                    "event_context": target["event_context"], "complete_guard": target["compact"],
                    "equivalent_guard_forms": sorted(forms[(root["eclass"], tuple(target["event_context"]))]),
                    "egg_representative": root["representative"], "members": []})
        if group["event_context"] != target["event_context"]:
            raise AssertionError("Event contexts merged")
        group["members"].append({"source": str(Path(target["source"]).relative_to(ROOT)),
                                  "line": target["line"], "column": point["column"],
                                  "counter_type": point["type"], "outcome": point["outcome"],
                                  "hits": point["hits"], "case_value": target["case_value"]})
    # Include only atom definitions used by active group guards. These are
    # typed RTL facts, never solver assignments or witness inputs.
    used = {name for group in groups.values() for name in atoms if name in group["complete_guard"]}
    return {"semantics": "binary/two-state Boolean guards only; process event context is separate",
            "groups": list(groups.values()), "typed_atoms": {name: atoms[name] for name in sorted(used)},
            "mapped_uncovered_locations": sum(len(group["members"]) for group in groups.values()),
            "unmapped_uncovered_locations": sum(p["hits"] == 0 for p in points) -
                                              sum(len(group["members"]) for group in groups.values()),
            "note": "Equivalent activation guards never transfer coverage hits between source counters."}


def render_messages(arm, source, prior, checker, log, points, targets, graph, atoms,
                    limit, round_no, all_targets=None):
    if arm not in ("B", "C"):
        raise ValueError("Only B/C arms are configured")
    rtl = source.read_text()
    raw_points = raw_coverage(points, rtl)
    for point in raw_points:
        source_cases = [target for target in targets if target["line"] == point["line"]
                        and point["counter_type"] == "line" and point["outcome"] == "case"
                        and target["kind"] == "explicit_case"]
        if len(source_cases) == 1:
            target = source_cases[0]
            point["raw_predicate"] = f"({target['switch_signal']} == {target['case_value']})"
            point["predicate_provenance"] = "RTL case selector and source literal"
    common = {"specification": SPEC.read_text(), "rtl": rtl, "initial_stimulus": INITIAL,
              "previous_generated_actions": prior, "round": round_no, "max_new_cycles": limit,
              "checker": {"checks": checker["checks"], "data_errors": checker["data_errors"],
                          "occupancy_errors": checker["occupancy_errors"],
                          "reset_errors": checker["reset_errors"], "clear_errors": checker["clear_errors"],
                          "enable_errors": checker["enable_errors"],
                          "first_failures": [line for line in log.splitlines() if "_FAIL" in line][:8],
                          "execution_log": [line for line in log.splitlines() if line.strip() and not line.startswith("RESULT ")]},
              "raw_uncovered_dut_coverage": raw_points}
    if arm == "C":
        common["egg_normalization"] = mapped_groups(targets, graph, points, atoms, all_targets)
    return [{"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": json.dumps(common, ensure_ascii=False, sort_keys=True)}]
