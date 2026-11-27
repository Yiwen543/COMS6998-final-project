"""Score typed violation monitors on real PRE samples of the full frame_task wrapper."""
from functools import lru_cache

from egg_frame_terms import BOOL_NAMES, BV_WIDTHS, REFERENCES, evaluate_term, parse_term, referenced_signals, z3_term


def environments(rows):
    """Expose consecutive PRE values; the first, pre-initialization PRE is excluded."""
    previous = None
    for index, row in enumerate(rows):
        if row["cycle"] != index:
            raise ValueError("nonconsecutive observation rows")
        current = {**row["inputs"], **row["pre"]}
        if previous is not None:
            values = {"have_prev": True, **current, **{"prev_" + key: val for key, val in previous.items()}}
            if set(values) != BOOL_NAMES | BV_WIDTHS.keys():
                raise ValueError("frame_task observation inventory changed")
            yield index, values
        previous = current


@lru_cache(maxsize=65536)
def _evaluate_sample(term, bindings):
    values = dict(bindings)
    if -1 not in values.values():
        return evaluate_term(term, values)
    # Inactive payload wires may be X/Z. Evaluate over all two-state
    # completions of the unknown pins; only credit a determinate verdict.
    import z3
    symbolic = {}
    for name, value in bindings:
        if name in BOOL_NAMES:
            if type(value) not in (int, bool) or value not in (-1, 0, 1):
                raise ValueError(f"invalid observed Boolean {name}")
            symbolic[name] = z3.Bool(name) if value == -1 else z3.BoolVal(bool(value))
        else:
            width = BV_WIDTHS[name]
            if type(value) is not int or not -1 <= value < 1 << width:
                raise ValueError(f"invalid observed unsigned {width}-bit value {name}")
            symbolic[name] = z3.BitVec(name, width) if value == -1 else z3.BitVecVal(value, width)
    expr = z3.simplify(z3_term(term, symbolic))
    if z3.is_true(expr):
        return True
    if z3.is_false(expr):
        return False
    solver = z3.Solver()
    solver.add(expr)
    positive = solver.check()
    solver = z3.Solver()
    solver.add(z3.Not(expr))
    negative = solver.check()
    if positive == z3.unsat and negative == z3.sat:
        return False
    if negative == z3.unsat and positive == z3.sat:
        return True
    if positive != z3.sat or negative != z3.sat:
        raise RuntimeError("inconclusive sample completion query")
    return None


def sample(term, values):
    names = referenced_signals(term)
    return _evaluate_sample(term, tuple(sorted((name, values[name]) for name in names)))


def parse_monitors(monitors):
    if not isinstance(monitors, dict) or monitors.keys() != REFERENCES.keys():
        raise ValueError("supply exactly the five named violation monitors")
    terms = {}
    for name in REFERENCES:
        value = monitors[name]
        if not isinstance(value, str) or not 1 <= len(value) <= 2400:
            raise ValueError(f"{name}: expected a nonempty term with at most 2400 characters")
        try:
            terms[name] = parse_term(value)
        except (ValueError, RecursionError) as exc:
            raise ValueError(f"{name}: {exc}") from exc
    return terms


def compare_samples(rows, references, candidates):
    results = {}
    data = list(environments(rows))
    for name in references:
        outcome = dict(reference_alarms=0, candidate_alarms=0, matched_known=0, missed=0,
                       false_alarm=0, unknown=0, matched_alarms=0, first_candidate_alarm=None,
                       first_reference_alarm=None, first_mismatch=None)
        for cycle, env in data:
            left = sample(references[name], env)
            right = sample(candidates[name], env)
            if left is True:
                outcome["reference_alarms"] += 1
                if outcome["first_reference_alarm"] is None:
                    outcome["first_reference_alarm"] = cycle
            if right is True:
                outcome["candidate_alarms"] += 1
                if outcome["first_candidate_alarm"] is None:
                    outcome["first_candidate_alarm"] = cycle
            if left is None or right is None:
                outcome["unknown"] += 1
                continue
            if left == right:
                outcome["matched_known"] += 1
                outcome["matched_alarms"] += int(left)
                continue
            outcome["missed" if left else "false_alarm"] += 1
            if outcome["first_mismatch"] is None:
                outcome["first_mismatch"] = {"cycle": cycle, "reference": left, "candidate": right}
        if sum(outcome[key] for key in ("matched_known", "missed", "false_alarm", "unknown")) != len(data):
            raise ValueError("incomplete sample comparison")
        results[name] = outcome
    return results


def score_corpus(corpus, monitors):
    reference_terms = parse_monitors(REFERENCES)
    candidate_terms = parse_monitors(monitors)
    cases = {}
    for (design, scenario), entry in sorted(corpus.items()):
        case = {
            "cycles": len(entry["rows"]),
            "checker": entry["checker"],
            "properties": compare_samples(entry["rows"], reference_terms, candidate_terms),
        }
        cases.setdefault(design, {})[scenario] = case
    counts = {}
    for design, scenarios in cases.items():
        observations = [row for case in scenarios.values() for row in case["properties"].values()]
        counts[design] = {key: sum(row[key] for row in observations) for key in (
            "reference_alarms", "candidate_alarms", "matched_known", "missed", "false_alarm", "unknown", "matched_alarms"
        )}
    return {"cases": cases, "totals_by_design": counts}


def tool_feedback(score):
    """Expose actual tool judgments for the frozen development subset only."""
    visible = {}
    for design, alias in (("original", "original"), ("F02", "probe_A"), ("F05", "probe_B")):
        visible[alias] = {}
        for scenario, case in score["cases"][design].items():
            checker = case["checker"]
            visible[alias][scenario] = {
                "observed_cycles": case["cycles"],
                "transaction_checker": checker["verdict"],
                "first_transaction_failure": (checker["failures"] or [None])[0],
                "candidate_alarms": {name: [row["candidate_alarms"], row["first_candidate_alarm"]]
                                     for name, row in case["properties"].items()},
            }
    return visible
