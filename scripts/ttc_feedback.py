"""Hash-guarded, two-state predicate feedback for the CVDP lite timer."""
import hashlib
import json

from coverage import join
from pilot_feedback import point_id, raw_coverage
from predicates import ROOT

DUT = ROOT / "examples/ttc_timer/rtl/ttc_counter_lite.sv"
SPEC = ROOT / "examples/ttc_timer/docs/specification.md"
CHECKER = ROOT / "examples/ttc_timer/verif/tb_ttc_counter_lite.sv"
SOURCE = str(DUT.relative_to(ROOT))
INITIAL = [dict(reset=1, write=0, read=0, addr=0, data=0),
           dict(reset=0, write=1, read=0, addr=1, data=4),
           dict(reset=0, write=1, read=0, addr=3, data=5),
           dict(reset=0, write=0, read=1, addr=1, data=0),
           dict(reset=0, write=0, read=0, addr=0, data=0)]
FIELDS = ("reset", "write", "read", "addr", "data")
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["actions"],
          "properties": {"actions": {"type": "array", "items": {
              "type": "object", "additionalProperties": False, "required": list(FIELDS),
              "properties": {key: {"type": "integer"} for key in FIELDS}}}}}
BASE = """Generate only cycle stimuli for a fixed, independent timer checker. Return JSON with an actions array.
Each action has integer reset, write, read (each 0 or 1), addr (0..15), data (0..4294967295).
The driver applies actions before rising clock edges. Reset is specified active-high synchronous. No simultaneous read/write or bus operation during reset.
Register addresses: 0 count (read only), 1 match (16-bit), 2 reload (16-bit), 3 control (enable bit 0, interval bit 1, interrupt enable bit 2), 4 status (read, write clears interrupt), 5 prescaler (4-bit). Read output is registered.
Maximize new DUT execution coverage in few cycles. Exercise prescaled count, match/interrupt, interval reload, status clear, register reads, and diverse data bit toggles. Use short match values when the cycle budget is small.
Only stimulus is under your control. DUT, checker, driver, simulator, and coverage denominator are frozen. A checker rejection of faulty RTL is a finding. Return no prose or extra fields."""


def validate_actions(value, limit, prior=None):
    if not isinstance(value, dict) or set(value) != {"actions"} or not isinstance(value["actions"], list):
        raise ValueError("Expected only an actions array")
    actions = value["actions"]
    if not 1 <= len(actions) <= limit:
        raise ValueError(f"Expected 1..{limit} actions")
    for i, a in enumerate(actions):
        if not isinstance(a, dict) or set(a) != set(FIELDS):
            raise ValueError(f"Action {i}: expected exactly {FIELDS}")
        for key, maximum in (("reset", 1), ("write", 1), ("read", 1),
                             ("addr", 15), ("data", 0xffffffff)):
            if type(a[key]) is not int or not 0 <= a[key] <= maximum:
                raise ValueError(f"Action {i}: {key} must be integer 0..{maximum}")
        if a["write"] and a["read"]:
            raise ValueError(f"Action {i}: simultaneous bus read/write excluded")
        if a["reset"] and (a["write"] or a["read"]):
            raise ValueError(f"Action {i}: bus access during reset excluded")
    return actions


def extract():
    source = DUT.read_text()
    provenance = json.loads((DUT.parent.parent / "provenance.json").read_text())
    if hashlib.sha256(DUT.read_bytes()).hexdigest() != provenance["rtl_sha256"]:
        raise ValueError("Timer DUT hash changed; review source map")
    lines = source.splitlines()
    for line, fragment in {41: "interval_mode && match_flag", 44: "count != match_value",
                           64: "match_flag && interrupt_enable", 66: "axi_addr == ADDR_STATUS",
                           81: "ADDR_MATCH_VALUE", 82: "ADDR_RELOAD_VALUE",
                           88: "ADDR_PRESCALER", 99: "ADDR_COUNT",
                           103: "ADDR_STATUS", 105: "default:"}.items():
        if fragment not in lines[line - 1]:
            raise ValueError(f"Timer source map shifted at {line}")
    # Comparisons on 4/16-bit values are single, typed atoms. Egg proves only
    # the surrounding Boolean identity, not arithmetic or sequential behavior.
    specs = [
        ("interval_reload", 41, "expr", "(interval_mode==1 && match_flag==1) => 1",
         "(not (or (not interval_mode) (not match_flag)))", "(and interval_mode match_flag)",
         ["interval_mode", "match_flag"]),
        ("irq_set", 64, "expr", "(match_flag==1 && interrupt_enable==1) => 1",
         "(not (or (not match_flag) (not interrupt_enable)))", "(and match_flag interrupt_enable)",
         ["match_flag", "interrupt_enable"]),
        ("irq_clear", 66, "expr", "(axi_write_en==1 && (axi_addr == ADDR_STATUS)==1) => 1",
         "(not (or (not axi_write_en) (not addr_status)))", "(and axi_write_en addr_status)",
         ["axi_write_en", "addr_status"]),
        ("count_equal_hold", 44, "branch", "else", "(not (not count_equal_match))",
         "count_equal_match", ["count_equal_match"]),
        ("read_status", 103, "line", "case", "(not (or (not axi_read_en) (not addr_status)))",
         "(and axi_read_en addr_status)", ["axi_read_en", "addr_status"]),
        ("read_count", 99, "line", "case", "(not (or (not axi_read_en) (not addr_count)))",
         "(and axi_read_en addr_count)", ["axi_read_en", "addr_count"]),
        ("write_reload", 82, "line", "case", "(not (or (not axi_write_en) (not addr_reload)))",
         "(and axi_write_en addr_reload)", ["axi_write_en", "addr_reload"]),
        ("write_prescaler", 88, "line", "case", "(not (or (not axi_write_en) (not addr_prescaler)))",
         "(and axi_write_en addr_prescaler)", ["axi_write_en", "addr_prescaler"]),
    ]
    return [dict(id=name, source=SOURCE, line=line, counter_type=kind,
                 counter_outcome=outcome, compact=compact, expanded=expanded,
                 width=1, signedness="unsigned Boolean", logic="two_state",
                 event="posedge clk; combinational guard only",
                 guards={"reset": "reset=0 at sampled edge",
                         "address_atoms": "addr_status=(4-bit axi_addr == 4'h4); addr_count=(4-bit axi_addr == 4'h0); addr_reload=(4-bit axi_addr == 4'h2); addr_prescaler=(4-bit axi_addr == 4'h5)",
                         "count_equal_match": "16-bit unsigned count == 16-bit unsigned match_value"},
                 dependencies=deps) for name, line, kind, outcome, compact, expanded, deps in specs]


def mapped_evidence(targets, graph, points):
    mapped = join(targets, graph, points)
    classes = {c["id"]: c["nodes"] for c in graph["eclasses"]}
    shared_atoms = {}
    for name in ("addr_status", "match_flag"):
        matches = [cid for cid, nodes in classes.items() if any(node["op"] == name and
                   not node["children"] for node in nodes)]
        if len(matches) != 1:
            raise AssertionError(f"Expected one egg E-class for shared atom {name}")
        shared_atoms[name] = matches[0]
    evidence = [{"id": row["id"], "source": row["source"], "line": row["line"],
                 "counter_type": row["counter_type"], "counter_outcome": row["counter_outcome"],
                 "hits": row["hits"], "eclass": row["eclass"],
                 "compact": row["compact"], "expanded": row["expanded"],
                 "representative": row["representative"], "eclass_nodes": classes[row["eclass"]],
                 "guards": row["guards"], "dependencies": row["dependencies"],
                 "width": row["width"], "signedness": row["signedness"]}
                for row in mapped if row["uncovered"]]
    mapped_ids = {point_id(row["coverage_point"]) for row in mapped}
    unmapped = [p for p in points if p["hits"] == 0 and point_id(p) not in mapped_ids]
    return {"engine": graph["engine"], "iterations": graph["iterations"],
            "stop_reason": graph["stop_reason"],
            "rewrites": ["de-morgan-or", "de-morgan-and", "double-not", "and-true", "and-true-left", "not-false"],
            "semantics": "Two-state one-bit Boolean guards only. Typed 4-bit address and 16-bit count comparisons remain atomic. No four-state, clock, reset, arithmetic, or state-transition equivalence is claimed.",
            "shared_dependencies": {"addr_status": {"eclass": shared_atoms["addr_status"],
                                                   "guards": ["irq_clear", "read_status"]},
                                    "match_flag": {"eclass": shared_atoms["match_flag"],
                                                   "guards": ["interval_reload", "irq_set"]}},
            "equivalence_scope": "Only compact and expanded forms of a predicate merge. Read and write status guards, and the two uses of match_flag, are distinct full expressions sharing child atoms. Every source counter remains separate.",
            "mapped_uncovered": evidence,
            "unmapped_uncovered": {"count": len(unmapped),
                                    "by_type": {kind: sum(p["type"] == kind for p in unmapped) for kind in sorted({p["type"] for p in unmapped})},
                                    "source_lines": sorted({p["line"] for p in unmapped}),
                                    "note": "All unsupported points remain in raw coverage and its denominator."}}


def render_messages(arm, spec, rtl, prior, checker, log, points, targets, graph, max_new_cycles, round_no):
    if arm not in "ABC":
        raise ValueError("Unknown feedback arm")
    common = {"specification": spec, "rtl": rtl, "initial_stimulus": INITIAL,
              "previous_generated_actions": prior, "round": round_no,
              "max_new_cycles": max_new_cycles,
              "checker": {"checks": checker["checks"],
                          "read_errors": checker["read_errors"],
                          "interrupt_errors": checker["interrupt_errors"],
                          "timing_errors": checker["timing_errors"],
                          "first_failures": [line for line in log.splitlines() if line.startswith(("READ_FAIL", "IRQ_FAIL", "TIMING_FAIL"))],
                          "execution_log": [line for line in log.splitlines() if not line.startswith("RESULT ")]}}
    if arm in "BC":
        common["raw_uncovered_dut_coverage"] = raw_coverage(points, rtl)
    if arm == "C":
        common["egg_normalization"] = mapped_evidence(targets, graph, points)
    return [{"role": "system", "content": BASE},
            {"role": "user", "content": json.dumps(common, ensure_ascii=False, sort_keys=True)}]
