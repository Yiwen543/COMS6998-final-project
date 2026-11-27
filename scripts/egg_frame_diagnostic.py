#!/usr/bin/env python3
"""Generate checked, human-readable alarm explanations from a single typed RTL property."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

from egg_frame_diagnostic_baseline import dnf, parse_dnf
from egg_frame_proof import SCOPE, typed_oracle
from egg_frame_terms import REFERENCES, abstract, format_term, parse_term
from m3_proof_dependencies import BUILTINS, ProofChecker, _plain, validate_pattern_rules


# Fixed before observing the diagnostic results. No target DNF appears in a Rust request.
RULES = [{"name": name, "left": left, "right": right} for name, (left, right) in BUILTINS.items()] + [
    {"name": "and-associate-right", "left": "(and (and ?a ?b) ?c)", "right": "(and ?a (and ?b ?c))"},
    {"name": "or-associate-right", "left": "(or (or ?a ?b) ?c)", "right": "(or ?a (or ?b ?c))"},
    {"name": "and-distribute-right", "left": "(and ?a (or ?b ?c))", "right": "(or (and ?a ?b) (and ?a ?c))"},
    {"name": "and-distribute-left", "left": "(and (or ?a ?b) ?c)", "right": "(or (and ?a ?c) (and ?b ?c))"},
    {"name": "and-idempotent", "left": "(and ?a ?a)", "right": "?a"},
    {"name": "or-idempotent", "left": "(or ?a ?a)", "right": "?a"},
]


def _restore(node, atoms):
    if isinstance(node, str):
        if node in ("true", "false"):
            return node
        if node not in atoms:
            raise ValueError(f"invented Boolean atom {node!r}")
        return atoms[node]
    return (node[0], *(_restore(child, atoms) for child in node[1:]))


def restore(source, atoms):
    """Translate only original atom names back to their exact typed pin comparisons."""
    typed = format_term(_restore(_plain(source), atoms))
    parse_term(typed)
    return typed


def _fold(op, terms):
    result = None
    for term in reversed(tuple(terms)):
        result = term if result is None else f"({op} {term} {result})"
    return result if result is not None else {"and": "true", "or": "false"}[op]


def clause_form(clause):
    return _fold("and", (name if truth else f"(not {name})" for name, truth in clause))


def dnf_form(clauses):
    return _fold("or", map(clause_form, clauses))


def check_typed(reference, extracted, clauses, atoms):
    typed = restore(extracted, atoms)
    whole = typed_oracle(reference, typed)["oracle"]
    if whole["status"] != "unsat":
        raise ValueError(f"non-equivalent extracted property: {whole['status']}")
    checked = []
    for clause in clauses:
        text = restore(clause_form(clause), atoms)
        # Reference and (reference or clause) differ precisely on clause ∧ ¬reference.
        query = typed_oracle(reference, f"(or {reference} {text})")["oracle"]
        if query["status"] != "unsat":
            raise ValueError(f"clause is not certified sufficient: {query['status']}")
        checked.append({"clause": text, "literal_count": len(clause), "implication": query})
    # Cross-check that the clauses used to score alarms preserve the extracted expression.
    clause_union = restore(dnf_form(clauses), atoms)
    union = typed_oracle(typed, clause_union)["oracle"]
    if union["status"] != "unsat":
        raise ValueError(f"clause parse changed the extracted expression: {union['status']}")
    return {"typed_expression": typed, "equivalence": whole, "scored_clause_union_equivalence": union,
            "clauses": checked}


def check_engine(reference, source, atoms, engine):
    """Never use extraction as a verification verdict until independent checks pass."""
    if engine["source"] != source:
        # Rust may normalize insignificant whitespace, but must preserve the tree.
        if _plain(engine["source"]) != _plain(source):
            raise ValueError("engine changed requested source")
    if engine["stop_reason"] != "Some(Saturated)" or engine["extracted"] is None:
        return {"accepted": False, "extracted": None, "checked_steps": [], "reason": engine["stop_reason"]}
    extracted = engine["extracted"]
    steps = []
    if _plain(source) != _plain(extracted):
        if not engine["explanation"]:
            raise ValueError("changed extraction without a proof")
        payload = {"targets": [{"id": name, "compact": term, "event_context": SCOPE}
                              for name, term in (("source", source), ("extracted", extracted))],
                   "verified_rules": [], "pattern_rules": RULES}
        proof = ProofChecker(payload, pattern_rules=RULES).check({
            "left": "source", "right": "extracted", "explanation": engine["explanation"]})
        steps = proof["steps"]
    elif engine["explanation"]:
        raise ValueError("identity unexpectedly carries a rewrite explanation")
    clauses = parse_dnf(extracted)
    evidence = check_typed(reference, extracted, clauses, atoms)
    return {"accepted": True, "extracted": extracted, "checked_steps": steps,
            "scored_clause_count": len(clauses), "scored_literal_occurrences": sum(map(len, clauses)),
            **evidence}


def generate(binary):
    binary = Path(binary).resolve(strict=True)
    result = {"schema": 1, "scope": SCOPE, "source_only": True, "api_calls": 0,
              "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
              "rules": RULES, "rule_valuations": validate_pattern_rules(RULES), "properties": {}}
    for label, reference in REFERENCES.items():
        source, atoms = abstract(parse_term(reference))
        request = {"term": source, "pattern_rules": RULES}
        start = time.perf_counter()
        run = subprocess.run([str(binary)], input=json.dumps(request), text=True, capture_output=True,
                             timeout=30, check=True)
        elapsed = time.perf_counter() - start
        graph = json.loads(run.stdout)
        evidence = check_engine(reference, source, atoms, graph)
        ordinary_clauses = dnf(source)
        ordinary = dnf_form(ordinary_clauses)
        ordinary_evidence = check_typed(reference, ordinary, ordinary_clauses, atoms)
        result["properties"][label] = {
            "reference": reference, "source": source, "atoms": {key: format_term(value) for key, value in atoms.items()},
            "engine_request": request, "engine": graph, "engine_seconds": elapsed, **evidence,
            "ordinary": {"source": ordinary, "clause_count": len(ordinary_clauses),
                         "literal_occurrences": sum(map(len, ordinary_clauses)), **ordinary_evidence},
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = generate(args.binary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for name, data in result["properties"].items():
        print(f"{name}: {data['accepted']=}, {data['engine']['stop_reason']}, "
              f"egg clauses={data.get('scored_clause_count')}, ordinary clauses={data['ordinary']['clause_count']}, "
              f"checked steps={len(data['checked_steps'])}")


if __name__ == "__main__":
    main()
