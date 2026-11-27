#!/usr/bin/env python3
"""Score DNF monitor explanations on actual consecutive PRE samples of frame_task."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from egg_frame_diagnostic import RULES, check_engine, dnf_form, restore
from egg_frame_diagnostic_baseline import dnf, evaluate_clause, minimum_cube, parse_dnf
from egg_frame_faults import load_corpus
from egg_frame_observe import environments, sample
from egg_frame_terms import REFERENCES, abstract, format_term, parse_term, referenced_signals
from predicates import ROOT


METHODS = ("ordinary", "egg")


def _prepare(generated):
    properties = generated["properties"]
    if properties.keys() != REFERENCES.keys() or generated["rules"] != RULES:
        raise ValueError("expected the frozen frame properties and reviewed rewrite rules")
    prepared = {}
    for name, reference in REFERENCES.items():
        row = properties[name]
        tree = parse_term(reference)
        source, atoms = abstract(tree)
        if (row["reference"] != reference or row["source"] != source or
                row["atoms"] != {key: format_term(val) for key, val in atoms.items()}):
            raise ValueError(f"{name}: generated predicate differs from the frozen reference")
        checked = check_engine(reference, source, atoms, row["engine"])
        if any(row.get(key) != checked[key] for key in ("accepted", "extracted", "checked_steps")):
            raise ValueError(f"{name}: cached extraction differs from replayed engine evidence")
        clauses = dnf(source)
        ordinary = dnf_form(clauses)
        if row["ordinary"]["source"] != ordinary:
            raise ValueError(f"{name}: ordinary DNF differs from independent recomputation")
        methods = {"ordinary": (clauses, parse_term(restore(ordinary, atoms)))}
        if checked["accepted"]:
            # Evaluate the entire written expression at pin level. Only the explanation
            # collapses duplicate literals, contradictions and subsumed clauses.
            text = checked["extracted"]
            methods["egg"] = (parse_dnf(text), parse_term(restore(text, atoms)))
        prepared[name] = (tree, source, atoms, methods)
    return prepared


def _literal_records(cube, atoms):
    if cube is None:
        return None
    return [{"term": format_term(atoms[name]), "value": polarity} for name, polarity in cube]


def _sample_result(prepared, env, counts, need_example):
    reference, source, atoms, methods = prepared
    expected = sample(reference, env)
    counts["samples"] += 1
    counts["unknown_source"] += expected is None
    counts["positive"] += expected is True
    assignment = exact = example = None
    if expected is True:
        assignment = {name: sample(atom, env) for name, atom in atoms.items()}
        counts["positive_partial_atoms"] += None in assignment.values()
        exact = minimum_cube(source, assignment)
        counts["exact_" + exact["status"]] += 1
        if exact["size"] is not None:
            counts["exact_size", exact["size"]] += 1
        if need_example:
            example = {"observed_pins": {name: env[name] for name in sorted(referenced_signals(reference))},
                       "exact_minimum": _literal_records(exact["cube"], atoms), "methods": {}}
    for method in METHODS:
        if method not in methods:
            counts[method, "unavailable"] += 1
            counts[method, "positive_unavailable"] += expected is True
            continue
        clauses, tree = methods[method]
        observed = sample(tree, env)
        if expected is None or observed is None:
            category = "both_unknown" if expected is observed else "different_determinacy"
        else:
            category = "known_agreement" if expected == observed else "known_mismatch"
        counts[method, category] += 1
        if expected is not True:
            continue
        active = [clause for clause in clauses if evaluate_clause(clause, assignment) is True]
        counts[method, "true_clauses"] += len(active)
        if not active:
            counts[method, "positive_without_true_clause"] += 1
            if need_example:
                example["methods"][method] = None
            continue
        smallest = min(active, key=lambda clause: (len(clause), clause))
        width = len(smallest)
        counts[method, "positive_with_true_clause"] += 1
        counts[method, "width", width] += 1
        if exact["size"] is not None:
            if width < exact["size"]:
                raise ValueError(f"{method}: observed true clause shorter than exhaustive minimum")
            counts[method, "at_minimum" if width == exact["size"] else "above_minimum"] += 1
        if need_example:
            example["methods"][method] = {"true_clause_count": len(active),
                                          "shortest": _literal_records(smallest, atoms)}
    return example


def _stats(counts):
    methods = {}
    for name in METHODS:
        fields = ("known_agreement", "known_mismatch", "both_unknown", "different_determinacy",
                  "unavailable", "true_clauses", "positive_with_true_clause", "positive_without_true_clause",
                  "positive_unavailable", "at_minimum", "above_minimum")
        method = {key: counts[name, key] for key in fields}
        method["shortest_true_clause_sizes"] = {
            str(key[2]): counts[key] for key in counts if isinstance(key, tuple) and key[:2] == (name, "width")
        }
        if (sum(method[k] for k in fields[:5]) != counts["samples"] or
                sum(method[k] for k in ("positive_with_true_clause", "positive_without_true_clause",
                                        "positive_unavailable")) != counts["positive"]):
            raise ValueError(f"{name}: missing sample decisions")
        methods[name] = method
    return {"samples": counts["samples"], "positive": counts["positive"], "unknown_source": counts["unknown_source"],
            "positive_with_unknown_atoms": counts["positive_partial_atoms"],
            "exact_minimum_status": {k: counts["exact_" + k] for k in ("sufficient", "false", "unknown", "atom_limit")},
            "exact_minimum_sizes": {str(k[1]): counts[k] for k in counts
                                    if isinstance(k, tuple) and k[0] == "exact_size"}, "methods": methods}


def score(corpus, generated):
    """Score {(design,trace): {'rows': ...}} against validated generated.json properties.

    Disjunction verdicts use typed two-state completions of unknown sampled pins. A clause
    is usable for an explanation only when each literal is determined by the observation.
    The exhaustive minimum ranges over independent Boolean atoms of the source predicate.
    """
    prepared = _prepare(generated)
    by_pair = defaultdict(Counter)
    examples, row_count = {}, 0
    for (design, trace), entry in sorted(corpus.items()):
        rows = entry["rows"]
        row_count += len(rows)
        for cycle, env in environments(rows):
            for name, prop in prepared.items():
                first = (design, name) not in examples
                example = _sample_result(prop, env, by_pair[design, name], first)
                if example is not None:
                    examples[design, name] = {"design": design, "property": name,
                                              "trace": trace, "cycle": cycle, **example}
    by_design, by_property, total = defaultdict(Counter), defaultdict(Counter), Counter()
    for (design, name), counts in by_pair.items():
        by_design[design].update(counts)
        by_property[name].update(counts)
        total.update(counts)
    if total["samples"] != (row_count - len(corpus)) * len(prepared):
        raise ValueError("inconsistent consecutive PRE sample count")
    return {"scope": "Cubes certify the observed monitor value over independent Boolean atoms. "
                     "Root-cause attribution requires evidence about the RTL change.",
            "observation_rows": row_count, "trace_count": len(corpus), "totals": _stats(total),
            "by_design": {k: _stats(v) for k, v in sorted(by_design.items())},
            "by_property": {k: _stats(v) for k, v in sorted(by_property.items())},
            "by_design_property": {design: {name: _stats(by_pair[design, name]) for name in prepared}
                                   for design in sorted(by_design)},
            "examples": [examples[k] for k in sorted(examples)]}


def combined_corpus(originals, controls):
    from egg_frame_diagnostic_faults import load_corpus as load_controls
    corpus = load_corpus(originals)
    for key, entry in load_controls(controls).items():
        if key in corpus:
            if key[0] != "original" or corpus[key]["rows"] != entry["rows"]:
                raise ValueError(f"conflicting RTL observations {key}")
        else:
            corpus[key] = entry
    return corpus


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    result_root = ROOT / "results/milestone3"
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, default=result_root / "frame-faults")
    parser.add_argument("--controls", type=Path, default=result_root / "frame-diagnostic-faults")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sources = (args.generated, args.corpus / "observations.jsonl.gz", args.controls / "observations.jsonl.gz")
    report = score(combined_corpus(args.corpus, args.controls), json.loads(args.generated.read_bytes()))
    report["sha256"] = dict(zip(("generated", "original_fault_traces", "diagnostic_control_traces"),
                                (hashlib.sha256(path.read_bytes()).hexdigest() for path in sources)))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
