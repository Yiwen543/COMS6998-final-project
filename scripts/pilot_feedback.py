"""Arm-isolated feedback with unmodified source/outcome coverage identities."""
import json
from pathlib import Path

from coverage import join

BASE_INSTRUCTIONS = """You are generating stimulus for a fixed, independent SystemVerilog checker.
Return only JSON matching the required schema: an actions array of cycle actions.
Each action has integer reset (0 or 1), req (0..255), and priority_override (0..255).
The driver applies each action before a rising clock edge. The module's reset is specified as active-high synchronous.
Maximize new DUT execution coverage with few cycles. Exercise varied guards and output transitions.
You may choose only stimulus. Checker, DUT, driver, simulator and coverage denominator are fixed.
Do not assume the RTL is correct: specification violations are useful findings.
Do not include prose, testbench code, or other fields."""

INITIAL = [{"reset": 1, "req": 0, "priority_override": 0},
           {"reset": 0, "req": 0, "priority_override": 0},
           {"reset": 0, "req": 1, "priority_override": 0},
           {"reset": 0, "req": 0, "priority_override": 1}]


def point_id(point):
    return (point["source"], point["line"], point["column"], point["type"],
            point["outcome"], point["hierarchy"], point.get("span"))


def raw_coverage(points, rtl):
    lines = rtl.splitlines()
    return [{"source": p["source"], "line": p["line"], "column": p["column"],
             "counter_type": p["type"], "outcome": p["outcome"], "hits": p["hits"],
             "source_text": lines[p["line"]-1].strip(), "span": p.get("span")}
            for p in points if p["hits"] == 0]


def egg_enrichment(targets, graph, points):
    mapped = join(targets, graph, points)
    classes = {c["id"]: c for c in graph["eclasses"]}
    evidence = []
    for row in mapped:
        if not row["uncovered"]:
            continue
        evidence.append({"target": row["id"], "source": row["source"],
                         "line": row["line"], "counter_type": row["counter_type"],
                         "counter_outcome": row["counter_outcome"],
                         "eclass": row["eclass"], "original_expression": row["compact"],
                         "equivalent_form": row["expanded"],
                         "egg_representative": row["representative"],
                         "eclass_nodes": classes[row["eclass"]]["nodes"],
                         "guards": {"event": row["event"], "reset_context": row["reset_context"],
                                    "selection": "override_any = (priority_override != 0)"},
                         "bit_width": row["width"], "signedness": "unsigned one-bit Boolean",
                         "semantics": row["logic"]})
    mapped_ids = {point_id(row["coverage_point"]) for row in mapped}
    unsupported = [{"source": p["source"], "line": p["line"], "column": p["column"],
                    "type": p["type"], "outcome": p["outcome"]}
                   for p in points if p["hits"] == 0 and point_id(p) not in mapped_ids]
    return {"engine": graph["engine"], "stop_reason": graph["stop_reason"],
            "iterations": graph["iterations"],
            "rules": ["de-morgan-or", "de-morgan-and", "double-not", "and-true",
                      "and-true-left", "not-false"],
            "semantics": "Pure unsigned one-bit two-state Boolean combinational predicates only; no four-state or state-transition equivalence claim.",
            "equivalence_limit": "Only compact and expanded forms of each winner are merged. Distinct winning cases remain distinct E-classes. Coverage locations retain individual hit counts.",
            "mapped_uncovered": evidence, "unmapped_uncovered": unsupported}


def failure_feedback(log, checker):
    lines = [line for line in log.splitlines() if line.startswith(("FUNCTION_FAIL", "TIMING_FAIL"))]
    execution_log = [line for line in log.splitlines() if line.strip() and not line.startswith("RESULT ")]
    return {"checks": checker["checks"], "functional_failure_count": checker["functional_errors"],
            "timing_failure_count": checker["timing_errors"], "first_failures": lines,
            "execution_log_without_coverage_class_bits": execution_log}


def render_messages(arm, spec, rtl, actions_so_far, checker, sim_log, points, targets, graph,
                    max_new_cycles, round_number):
    if arm not in "ABC":
        raise ValueError("Unknown arm")
    common = {"specification": spec, "rtl": rtl,
              "initial_stimulus": INITIAL, "previous_generated_actions": actions_so_far,
              "checker": failure_feedback(sim_log, checker),
              "round": round_number, "max_new_cycles": max_new_cycles}
    if arm in "BC":
        common["raw_uncovered_dut_coverage"] = raw_coverage(points, rtl)
    if arm == "C":
        common["egg_normalization"] = egg_enrichment(targets, graph, points)
    return [{"role": "system", "content": BASE_INSTRUCTIONS},
            {"role": "user", "content": json.dumps(common, ensure_ascii=False, sort_keys=True)}]


def feedback_parts(messages):
    return json.loads(messages[1]["content"])
