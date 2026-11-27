"""Grade generated FIFO monitors and render only the development data assigned to each arm."""
import json

from egg_assertion_baseline import term_search, truth_table
from egg_fifo_assertion_forms import BUDGETS, MAX_TERM_NODES, RULES, checked_egg, disjoin
from egg_fifo_formal import BUNDLED, FIELDS, render
from predicates import parse


ARMS = ("raw", "ordinary", "egg")
ATOMS = frozenset(("active", *FIELDS))


def validate_obligations(obligations):
    """Accept one to four distinct, bounded formulas that the original RTL runner can render."""
    if not isinstance(obligations, list) or not 1 <= len(obligations) <= 4:
        raise ValueError("expected one to four violation expressions")
    expressions = set()
    for text in obligations:
        if not isinstance(text, str) or not 1 <= len(text) <= 400 or not text.strip():
            raise ValueError("each violation expression must be a nonempty string of at most 400 characters")
        try:
            expression = parse(text)
            render(expression)  # Enforce the exact same typed atom/operator inventory as the SV harness.
        except (IndexError, KeyError, ValueError) as exc:
            raise ValueError("invalid Boolean expression or unknown FIFO sample atom") from exc
        if expression in expressions:
            raise ValueError("duplicate violation expression")
        expressions.add(expression)


def review(obligations, *, binary, arm):
    """Offline grading covers every arm. Only the selected proof method is actually run."""
    if arm not in ARMS:
        raise ValueError(f"unknown feedback arm {arm!r}")
    validate_obligations(obligations)
    combined = disjoin(obligations)
    oracle = truth_table(BUNDLED, combined, max_atoms=len(ATOMS))
    if set(oracle["atoms"]) != ATOMS or oracle["stop_reason"] != "exhaustive" or oracle["checked_assignments"] != 32:
        raise ValueError("the common FIFO oracle did not exhaust the five-atom domain")
    proof, evidence = None, None
    if arm == "ordinary":
        evidence = term_search(BUNDLED, combined, RULES, max(BUDGETS), max_term_nodes=MAX_TERM_NODES)
        proof = {"method": "ordinary_bounded_tree_search", "proved": evidence["proved"],
                 "stop": evidence["stop_reason"], "steps": [
                     {key: step[key] for key in ("rule", "direction", "path")} for step in evidence["steps"]],
                 "budget_distinct_terms": max(BUDGETS), "max_term_nodes": MAX_TERM_NODES}
    elif arm == "egg":
        evidence = checked_egg(binary, BUNDLED, combined)
        audit = evidence["egg_audit"]
        steps = [s for edge in audit["edges"] for s in edge["steps"]] if audit is not None else []
        proof = {"method": "egg", "proved": evidence["egg_proved"], "stop": evidence["egg_graph"]["stop_reason"],
                 "steps": steps}
    if proof and proof["proved"] and not oracle["equivalent"]:
        raise ValueError("a named proof contradicted the exhaustive Boolean oracle")
    return {"arm": arm, "obligations": list(obligations), "candidate_union": combined,
            "equivalent": oracle["equivalent"], "counterexample": oracle["counterexample"],
            "oracle": oracle, "proof": proof, "evidence": evidence}


def _visible_rtl(rtl, count, *, show_samples):
    bound = rtl["bounded_states"]
    if type(bound) is not int or bound < 1:
        raise ValueError("invalid physical checker bound")
    visible = {"bounded_states": bound}
    # Explicit selection keeps the hidden model name, file paths, mutant outcomes
    # and internal signals out of development feedback.
    for physical, label in (("original", "original"), ("flip_last", "diagnostic_probe")):
        record = rtl["models"][physical]
        status = record["status"]
        if status not in ("PASSED", "FAILED"):
            raise ValueError(f"inconclusive RTL check on {label}")
        indices, step = record["failed_indices"], record["failed_step"]
        if not isinstance(indices, list) or any(type(i) is not int or not 0 <= i < count for i in indices):
            raise ValueError("invalid RTL failure index")
        shown = {"status": status}
        visible[label] = shown
        if status == "PASSED":
            if indices or step is not None:
                raise ValueError("inconsistent passed RTL check")
        else:
            if not indices or type(step) is not int or not 0 <= step < bound:
                raise ValueError("incomplete failed RTL check")
            shown.update(failed_obligation_indices_zero_based=indices, failed_step=step)
            if show_samples:
                sample = record["sampled_atoms"]
                if (not isinstance(sample, dict) or set(sample) != ATOMS or
                        any(type(value) is not bool for value in sample.values())):
                    raise ValueError("expected exactly the five sampled FIFO Boolean values")
                shown["sampled_atoms"] = sample
        if "log_excerpt" in record:
            excerpt = record["log_excerpt"]
            check_step = bound - 1 if status == "PASSED" else step
            allowed = {f"Checking assertions in step {check_step}..", f"Status: {status}"}
            allowed.update(f"Assert failed in fifo_stall_formal: check_{i}" for i in indices)
            if (not isinstance(excerpt, list) or not 1 <= len(excerpt) <= 3 or
                    any(not isinstance(line, str) or line not in allowed for line in excerpt)):
                raise ValueError("invalid native RTL diagnostic excerpt")
            shown["log_excerpt"] = excerpt
    return visible


def feedback(review_result, rtl_result, arm):
    """Bounded text sent on the next independent round; full evidence stays in the run record."""
    if arm not in ARMS or review_result["arm"] != arm:
        raise ValueError("feedback arm differs from the graded candidate")
    if rtl_result["obligations"] != review_result["obligations"]:
        raise ValueError("RTL checks and semantic review describe different candidate obligations")
    result = {"rtl_bounded_checks": _visible_rtl(rtl_result, len(review_result["obligations"]), show_samples=arm != "raw")}
    if arm != "raw":
        oracle = review_result["oracle"]
        proof = review_result["proof"]
        semantic = {"equivalent": oracle["equivalent"], "checked_assignments": oracle["checked_assignments"]}
        if oracle["counterexample"] is not None:
            semantic["counterexample"] = {"atoms": oracle["counterexample"], "spec_violation": oracle["left_value"],
                                          "candidate_violation": oracle["right_value"]}
        result["sampled_boolean_truth_table"] = semantic
        result["named_rewrite_search"] = {
            "method": proof["method"], "proof_found": proof["proved"], "stop": proof["stop"],
            "total_steps": len(proof["steps"]), "first_steps": proof["steps"][:4],
        }
    return json.dumps(result, sort_keys=True, separators=(",", ":"))
