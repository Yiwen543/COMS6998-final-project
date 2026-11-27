"""Choose shared frame-monitor feedback from development traces and a typed XOR oracle."""
from egg_frame_faults import DEVELOPMENT, TRACES
from egg_frame_observe import environments, parse_monitors, sample, tool_feedback
from egg_frame_terms import BOOL_NAMES, BV_WIDTHS, REFERENCES, referenced_signals


ALIASES = {"original": "original", "F02": "probe_A", "F05": "probe_B"}


def _symbolic(name, reference, candidate, oracle):
    """Replay the complete solver model even when a physical counterexample takes precedence."""
    status = oracle["status"]
    equivalent = {"sat": False, "unsat": True, "unknown": None}
    if status not in equivalent or oracle["equivalent"] is not equivalent[status]:
        raise ValueError(f"{name}: inconsistent typed XOR status")
    if status != "sat":
        if any(oracle[key] is not None for key in ("counterexample", "reference_value", "candidate_value")):
            raise ValueError(f"{name}: a {status} oracle has no counterexample model")
        return None
    values = oracle["counterexample"]
    if not isinstance(values, dict) or values.keys() != BOOL_NAMES | BV_WIDTHS.keys():
        raise ValueError(f"{name}: incomplete symbolic pin assignment")
    for pin in BOOL_NAMES:
        if type(values[pin]) not in (bool, int) or values[pin] not in (0, 1):
            raise ValueError(f"{name}: nonbinary symbolic pin {pin}")
    for pin, width in BV_WIDTHS.items():
        if type(values[pin]) is not int or not 0 <= values[pin] < (1 << width):
            raise ValueError(f"{name}: invalid symbolic bus {pin}")
    left, right = sample(reference, values), sample(candidate, values)
    if left == right or left is not oracle["reference_value"] or right is not oracle["candidate_value"]:
        raise ValueError(f"{name}: symbolic counterexample fails replay")
    return {"origin": "symbolic", "values": dict(values), "reference_value": left, "candidate_value": right}


def _development_observations(corpus, physical, references, candidates):
    selected = {}
    for design in DEVELOPMENT:
        cases = physical["cases"][design]
        if set(cases) != set(TRACES):
            raise ValueError(f"{design}: incorrect development trace inventory")
        for trace in TRACES:
            entry, case = corpus[design, trace], cases[trace]
            if (case["cycles"] != len(entry["rows"]) or case["checker"] != entry["checker"] or
                    case["properties"].keys() != references.keys()):
                raise ValueError(f"{design}/{trace}: physical score and trace disagree")
            first_mismatch = dict.fromkeys(references)
            first_alarm = dict.fromkeys(references)
            alarms = dict.fromkeys(references, 0)
            for cycle, values in environments(entry["rows"]):
                for name, reference in references.items():
                    left, right = sample(reference, values), sample(candidates[name], values)
                    if right is True:
                        alarms[name] += 1
                        if first_alarm[name] is None:
                            first_alarm[name] = cycle
                    if left is None or right is None or left == right or first_mismatch[name] is not None:
                        continue
                    first_mismatch[name] = {"cycle": cycle, "reference": left, "candidate": right}
                    if name not in selected:
                        selected[name] = {"origin": "physical", "design": ALIASES[design], "trace": trace,
                                          "cycle": cycle, "values": values, "reference_value": left,
                                          "candidate_value": right}
            for name, row in case["properties"].items():
                if (first_mismatch[name] != row["first_mismatch"] or alarms[name] != row["candidate_alarms"]
                        or first_alarm[name] != row["first_candidate_alarm"]):
                    raise ValueError(f"{design}/{trace}/{name}: physical score fails PRE replay")
    return selected


def prepare_common(monitors, corpus, oracles, physical):
    """Return model-visible 'public' feedback and full per-property 'observations' for diagnosis.

    A physical counterexample carries observed PRE values, including -1 for unknown
    pins. Both verdicts must be determinate over all completions. A symbolic example
    carries a complete two-state model and makes no claim of RTL reachability.
    """
    references = parse_monitors(REFERENCES)
    candidates = parse_monitors(monitors)
    if oracles.keys() != references.keys():
        raise ValueError("expected a full typed XOR result for each frame property")
    observed = _development_observations(corpus, physical, references, candidates)
    observations, semantic = {}, {}
    for name, reference in references.items():
        oracle = oracles[name]
        symbolic = _symbolic(name, reference, candidates[name], oracle)
        witness = observed.get(name, symbolic)
        if witness is not None and oracle["equivalent"] is True:
            raise ValueError(f"{name}: physical mismatch contradicts typed equivalence")
        observations[name] = witness
        public = None
        if witness is not None:
            pins = referenced_signals(reference) | referenced_signals(candidates[name])
            public = {key: value for key, value in witness.items() if key != "values"}
            public["pins"] = {pin: witness["values"][pin] for pin in sorted(pins)}
        semantic[name] = {"equivalent": oracle["equivalent"], "typed_xor": oracle["status"],
                          "counterexample": public}
    return {"public": {"visible_rtl_observations": tool_feedback(physical), "semantic_review": semantic},
            "observations": observations}
