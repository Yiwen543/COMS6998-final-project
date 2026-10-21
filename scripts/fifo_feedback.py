"""Frozen FIFO source map and arm-isolated feedback for the CVDP context IP."""
import hashlib
import json

from coverage import join
from pilot_feedback import point_id, raw_coverage
from predicates import ROOT

DUT = ROOT / "examples/fifo/rtl/sync_fifo.sv"
SPEC = ROOT / "examples/fifo/docs/specification.md"
CHECKER = ROOT / "examples/fifo/verif/tb_sync_fifo.sv"
SOURCE = str(DUT.relative_to(ROOT))
INITIAL = [dict(reset=1, push=0, pop=0, data=0),
           dict(reset=0, push=1, pop=0, data=0x11),
           dict(reset=0, push=0, pop=1, data=0),
           dict(reset=0, push=0, pop=0, data=0)]
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["actions"],
          "properties": {"actions": {"type": "array", "items": {
              "type": "object", "additionalProperties": False,
              "required": ["reset", "push", "pop", "data"],
              "properties": {key: {"type": "integer"} for key in ("reset", "push", "pop", "data")}}}}}

BASE = """You are generating only cycle stimuli for a fixed, independent FIFO checker.
Return JSON with an actions array; each action has integer reset, push, pop (each 0 or 1) and data (0..255).
The driver applies actions before rising edges. Reset is active-high asynchronous. Push/pop must be 0 during reset.
Never pop when occupancy is zero; never push when occupancy is eight unless also popping. Simultaneous push/pop is legal only when nonempty. Reset clears occupancy. Begin from the supplied occupancy after prior actions.
Maximize new DUT execution coverage with few cycles; vary data bits, operation cases, full/empty, pointer wrap and reset during operation.
Only stimulus is under your control. DUT, checker, driver and coverage measurement are frozen. Report no prose or extra JSON fields."""


def validate_actions(value, limit, prior):
    if not isinstance(value, dict) or set(value) != {"actions"} or not isinstance(value["actions"], list):
        raise ValueError("Expected only an actions array")
    actions = value["actions"]
    if not 1 <= len(actions) <= limit:
        raise ValueError(f"Expected 1..{limit} actions")
    count = occupancy(prior)
    for i, action in enumerate(actions):
        if not isinstance(action, dict) or set(action) != {"reset", "push", "pop", "data"}:
            raise ValueError(f"Action {i}: expected reset, push, pop, data only")
        for field, top in (("reset", 1), ("push", 1), ("pop", 1), ("data", 255)):
            if type(action[field]) is not int or not 0 <= action[field] <= top:
                raise ValueError(f"Action {i}: {field} must be integer 0..{top}")
        if action["reset"]:
            if action["push"] or action["pop"]:
                raise ValueError(f"Action {i}: no operations during reset")
            count = 0
        else:
            if action["pop"] and count == 0:
                raise ValueError(f"Action {i}: underflow")
            if action["push"] and count == 8 and not action["pop"]:
                raise ValueError(f"Action {i}: overflow")
            count += action["push"] - action["pop"]
    return actions


def occupancy(actions):
    count = 0
    for action in actions:
        count = 0 if action["reset"] else count + action["push"] - action["pop"]
    return count


def extract():
    provenance = json.loads((ROOT / "examples/fifo/provenance.json").read_text())
    if hashlib.sha256(DUT.read_bytes()).hexdigest() != provenance["rtl_sha256"]:
        raise ValueError("FIFO DUT hash changed; review source mapping")
    lines = DUT.read_text().splitlines()
    expected = {48: "2'b01", 50: "2'b10", 52: "2'b11", 57: "default:", 70: "assign full_o"}
    for line, fragment in expected.items():
        if fragment not in lines[line - 1]:
            raise ValueError(f"FIFO source map shifted at {line}")
    # Case arms are mutually exclusive behavioral cases. The two forms for
    # each arm are Boolean-equivalent under binary, one-bit input semantics.
    cases = [("push_only", 48, "(not (or (not push_i) pop_i))", "(and push_i (not pop_i))"),
             ("pop_only", 50, "(not (or push_i (not pop_i)))", "(and (not push_i) pop_i)"),
             ("both", 52, "(not (or (not push_i) (not pop_i)))", "(and push_i pop_i)"),
             ("idle", 57, "(not (or push_i pop_i))", "(and (not push_i) (not pop_i))")]
    targets = [{"id": name, "source": SOURCE, "line": line,
                "counter_type": "line", "counter_outcome": "case",
                "compact": compact, "expanded": expanded, "width": 1,
                "logic": "two_state", "event": "always_comb case",
                "guards": {"reset": "not in this combinational case; operation contract excludes push/pop during reset"},
                "dependencies": ["push_i", "pop_i"]}
               for name, line, compact, expanded in cases]
    targets.append({"id": "full_pointer_compare", "source": SOURCE, "line": 70,
                    "counter_type": "expr", "counter_outcome": "=> 1",
                    "compact": "(not (or (not msb_diff) (not low_bits_equal)))",
                    "expanded": "(and msb_diff low_bits_equal)", "width": 1,
                    "logic": "two_state", "event": "continuous combinational output",
                    "guards": {"msb_diff": "wr_ptr_q[3] != rd_ptr_q[3]",
                               "low_bits_equal": "wr_ptr_q[2:0] == rd_ptr_q[2:0]"},
                    "dependencies": ["4-bit unsigned wr_ptr_q", "4-bit unsigned rd_ptr_q"]})
    return targets


def mapped_evidence(targets, graph, points):
    # The full expression has a long, version-specific outcome; find it by
    # inspected Verilator expression polarity while retaining the exact point.
    adapted = []
    for t in targets:
        item = dict(t)
        if item["id"] == "full_pointer_compare":
            matches = [p for p in points if p["line"] == 70 and p["type"] == "expr" and p["outcome"].endswith("=> 1")]
            if len(matches) != 1:
                raise ValueError("Expected one full-expression true counter")
            item["counter_outcome"] = matches[0]["outcome"]
        adapted.append(item)
    mapped = join(adapted, graph, points)
    evidence = [{"id": row["id"], "source": row["source"], "line": row["line"],
                 "counter_type": row["counter_type"], "counter_outcome": row["counter_outcome"],
                 "hits": row["hits"], "eclass": row["eclass"], "compact": row["compact"],
                 "expanded": row["expanded"], "representative": row["representative"],
                 "guards": row["guards"], "dependencies": row["dependencies"],
                 "width": row["width"], "logic": row["logic"]}
                for row in mapped if row["uncovered"]]
    mapped_ids = {point_id(row["coverage_point"]) for row in mapped}
    unmapped = [p for p in points if p["hits"] == 0 and point_id(p) not in mapped_ids]
    by_type = {kind: sum(p["type"] == kind for p in unmapped)
               for kind in sorted({p["type"] for p in unmapped})}
    return {"engine": graph["engine"], "iterations": graph["iterations"],
            "stop_reason": graph["stop_reason"],
            "rewrites": ["de-morgan-or", "de-morgan-and", "double-not", "and-true", "and-true-left", "not-false"],
            "semantics": "Two-state unsigned one-bit Boolean abstraction only; 4-bit pointer comparisons are preserved as atomic guards. No four-state, sequential, reset, or memory equivalence is claimed.",
            "equivalence_scope": "Only the two forms of each predicate merge. Case arms remain distinct. Each source counter retains its own hits.",
            "mapped_uncovered": evidence,
            "unmapped_uncovered": {"count": len(unmapped), "by_type": by_type,
                                    "source_lines": sorted({p["line"] for p in unmapped}),
                                    "note": "All unmapped points and exact outcomes remain in raw_uncovered_dut_coverage; no normalization claim applies."}}


def render_messages(arm, spec, rtl, prior, checker, log, points, targets, graph, max_new_cycles, round_no):
    if arm not in "ABC":
        raise ValueError("Unknown feedback arm")
    common = {"specification": spec, "rtl": rtl, "initial_stimulus": INITIAL,
              "previous_generated_actions": prior, "current_occupancy": occupancy(INITIAL + prior),
              "round": round_no, "max_new_cycles": max_new_cycles,
              "checker": {"checks": checker["checks"], "functional_errors": checker["functional_errors"],
                          "first_failures": [line for line in log.splitlines() if line.startswith(("STATUS_FAIL", "DATA_FAIL"))],
                          "execution_log": [line for line in log.splitlines() if not line.startswith("RESULT ")]}}
    if arm in "BC":
        common["raw_uncovered_dut_coverage"] = raw_coverage(points, rtl)
    if arm == "C":
        common["egg_normalization"] = mapped_evidence(targets, graph, points)
    return [{"role": "system", "content": BASE},
            {"role": "user", "content": json.dumps(common, ensure_ascii=False, sort_keys=True)}]
