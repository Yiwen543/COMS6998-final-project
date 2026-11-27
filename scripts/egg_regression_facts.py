"""Common, typed context facts for a regression batch and a matched ordinary solver.

No whole-formula equivalence oracle is used when discovering facts. Query reuse
is an in-memory optimization: cached results are bound to the exact typed
obligation, guard, schema, and solver configuration. The audit independently
recreates all discovery queries (with its own optional cache).
"""
from copy import deepcopy
from hashlib import sha256
import json

import z3

from egg_txn_context import _check, _digest, _proposition, _root_literal, _verify_query, TIMEOUT_MS
from egg_txn_terms import BOOL_NAMES, BV_WIDTHS, abstract, format_term, parse_term, z3_env, z3_term
from predicates import parse


SCOPE = "txn-regression-v1: free two-state transaction snapshots with declared unsigned widths"
SCHEMA_SHA256 = _digest({"scope": SCOPE, "bitvectors": BV_WIDTHS, "booleans": sorted(BOOL_NAMES),
                         "operators": "egg_txn_terms:v1: bool-and-or-not-xor-eq-ne; unsigned-ult-ule-ugt-uge"})


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def prepare(sources):
    """Bind any number of original endpoints to one stable primitive namespace."""
    _require(isinstance(sources, (list, tuple)) and len(sources) > 0,
             "expected at least one source")
    endpoints = []
    atoms = {}
    for source in sources:
        projected, bindings = abstract(parse_term(source))
        endpoints.append(projected)
        for name, term in bindings.items():
            rendered = format_term(term)
            _require(atoms.setdefault(name, rendered) == rendered,
                     "conflicting typed primitive binding")
    return {"sources": list(sources), "abstracts": endpoints, "atoms": dict(sorted(atoms.items()))}


def _check_prepared(prepared):
    _require(isinstance(prepared, dict) and set(prepared) == {"sources", "abstracts", "atoms"},
             "malformed source binding")
    _require(prepared == prepare(prepared["sources"]), "typed source binding was modified")


def _guard_node(guard):
    node = parse_term(guard)
    _require(guard == "true" or (isinstance(node, tuple) and len(node) == 3 and
             node[0] in ("ult", "eq", "ugt") and isinstance(node[1], str) and node[1] in BV_WIDTHS
             and type(node[2]) is int and format_term(node) == guard),
             "guard must be true or a canonical unsigned threshold")
    return node


def context_id(guard):
    """A context is a typed semantics and a guard, not a batch or source version."""
    _guard_node(guard)
    return _digest({"scope": SCOPE, "schema_sha256": SCHEMA_SHA256, "guard": guard})


def _cache_key(guard, operation, *typed_sources):
    # Every key binds the exact finite bit-vector language and applicable guard.
    return (SCHEMA_SHA256, guard, operation, tuple(typed_sources), "QF_BV", TIMEOUT_MS,
            z3.get_version_string())


def _receipt(cache, key, expression, counts):
    if cache is not None and key in cache:
        counts["cache_hits"] += 1
        # No mutable reference in a downstream evidence packet can edit the cache.
        return deepcopy(cache[key])
    counts["cache_misses"] += 1
    record, _ = _check(expression)
    if cache is not None and record["status"] != "unknown":
        cache[key] = deepcopy(record)
    return record


def _inventory(prepared):
    roots = {_root_literal(source) for source in prepared["abstracts"]}
    return roots, {name: source for name, source in prepared["atoms"].items() if name.startswith("bv_")}


def certify(prepared, guard, cache=None):
    """Discover a signed primitive forest once for all endpoints in this context.

    Constant and pair queries are local leaf obligations. If both primitives
    are standalone roots, or a root primitive is compared against a standalone
    constant, that direct goal is not queried as a fact. This conservatively
    excludes possible direct goals even when the requested pair list is a subset.
    """
    _check_prepared(prepared)
    cid = context_id(guard)
    env = z3_env()
    guard_formula = z3_term(_guard_node(guard), env)
    roots, sources = _inventory(prepared)
    atoms = {name: z3_term(parse_term(source), env) for name, source in sources.items()}
    counts = dict(eligible_atoms=len(atoms), feasibility_queries=1, constant_queries=0,
                  pair_queries=0, skipped_direct_pairs=0, sat=0, unsat=0, unknown=0,
                  cache_hits=0, cache_misses=0)
    feasibility = _receipt(cache, _cache_key(guard, "feasibility"), guard_formula, counts)
    _require(feasibility["status"] in ("sat", "unsat"), "unknown context feasibility")
    facts, receipts = [], {}
    result = {"context_id": cid, "guard": guard, "feasibility": feasibility,
              "facts": facts, "receipts": receipts, "counts": counts}
    if feasibility["status"] == "unsat":
        return result

    def try_fact(left, right, right_source, right_formula, counter):
        counts[counter] += 1
        left_source = sources[left]
        query = z3.And(guard_formula, z3.Xor(atoms[left], right_formula))
        record = _receipt(cache, _cache_key(guard, "primitive-xor", left_source, right_source),
                          query, counts)
        counts[record["status"]] += 1
        if record["status"] != "unsat":
            return False
        name = "ctx-" + _digest([cid, left, right])[:24]
        _require(name not in receipts, "local fact identifier collision")
        facts.append({"name": name, "left": left, "right": right,
                      "event_context": cid, "proof_status": "unsat"})
        receipts[name] = {"guard": guard, "typed_left": left_source,
                          "typed_right": right_source, "query": record}
        return True

    remaining = []
    for atom in atoms:
        if atom in roots and roots & {"true", "false"}:
            counts["skipped_direct_pairs"] += 1
            remaining.append(atom)
            continue
        for fixed in (True, False):
            text = "true" if fixed else "false"
            if try_fact(atom, text, text, z3.BoolVal(fixed), "constant_queries"):
                break
        else:
            remaining.append(atom)

    representatives = []
    for atom in remaining:
        for rep in representatives:
            if atom in roots and rep in roots:
                counts["skipped_direct_pairs"] += 1
                continue
            if try_fact(atom, rep, sources[rep], atoms[rep], "pair_queries"):
                break
            if try_fact(atom, f"(not {rep})", f"(not {sources[rep]})", z3.Not(atoms[rep]), "pair_queries"):
                break
        else:
            representatives.append(atom)
    return result


def verify(prepared, guard, evidence, cache=None):
    """Independently rediscover every obligation and check all proof receipts.

    `cache` if given must be an independent audit-only cache, initially empty
    and consumed in the same batch order as production. Otherwise each batch
    is independently cold-checked, and logical query counts and cache totals
    (but not the prior-history hit/miss split) are checked. The input evidence
    is never inserted into the audit cache.
    """
    fresh = certify(prepared, guard, cache)
    _require(isinstance(evidence, dict) and set(evidence) == set(fresh), "unexpected evidence schema")
    _require(all(evidence[key] == fresh[key] for key in ("context_id", "guard", "facts")),
             "changed context or discovery rule inventory")
    _verify_query(evidence["feasibility"], fresh["feasibility"])
    counts = evidence["counts"]
    expected = fresh["counts"]
    _require(isinstance(counts, dict) and set(counts) == set(expected) and
             all(type(n) is int and n >= 0 for n in counts.values()), "malformed discovery counters")
    for key in counts:
        if cache is not None or key not in ("cache_hits", "cache_misses"):
            _require(counts[key] == expected[key], "discovery count mismatch")
    _require(counts["cache_hits"] + counts["cache_misses"] == counts["feasibility_queries"] +
             counts["constant_queries"] + counts["pair_queries"], "cache accounting mismatch")
    _require(isinstance(evidence["receipts"], dict) and set(evidence["receipts"]) == set(fresh["receipts"]),
             "missing or extra typed fact receipt")
    for name, check in fresh["receipts"].items():
        saved = evidence["receipts"][name]
        _require(isinstance(saved, dict) and set(saved) == set(check) and
                 all(saved[key] == check[key] for key in ("guard", "typed_left", "typed_right")),
                 "typed premise scope or source binding mismatch")
        _verify_query(saved["query"], check["query"])
    return True


def _checked_assumptions(prepared, evidence):
    """Check premise bindings after the caller has independently verified receipts."""
    _check_prepared(prepared)
    cid = context_id(evidence["guard"])
    _require(cid == evidence["context_id"], "wrong context in common facts")
    _require(evidence["feasibility"]["status"] in ("sat", "unsat"), "unknown feasibility")
    vacuous = evidence["feasibility"]["status"] == "unsat"
    _require(not vacuous or not evidence["facts"], "infeasible context must not have facts")
    roots, sources = _inventory(prepared)
    assumptions = []
    names = set()
    for fact in evidence["facts"]:
        name, left, right = (fact[k] for k in ("name", "left", "right"))
        rhs = parse(right)
        _require(name not in names and name == "ctx-" + _digest([cid, left, right])[:24], "wrong fact name")
        names.add(name)
        endpoint = _root_literal(right)
        _require(left in sources and endpoint is not None and left != endpoint and
                 (endpoint in sources or endpoint in ("true", "false")) and
                 not (left in roots and endpoint in roots) and
                 not (left in roots and endpoint in ("true", "false") and roots & {"true", "false"}),
                 "not a permitted original primitive premise")
        if isinstance(rhs, tuple):
            _require(len(rhs) == 2 and rhs[0] == "not" and isinstance(rhs[1], str) and rhs[1] in sources,
                     "malformed complemented primitive")
            typed_right = f"(not {sources[rhs[1]]})"
        else:
            typed_right = sources.get(rhs, rhs)
        receipt = evidence["receipts"][name]
        _require(fact["event_context"] == cid and fact["proof_status"] == "unsat" and
                 receipt["guard"] == evidence["guard"] and receipt["typed_left"] == sources[left] and
                 receipt["typed_right"] == typed_right and receipt["query"]["status"] == "unsat" and
                 receipt["query"]["smt2_sha256"] == sha256(receipt["query"]["smt2"].encode()).hexdigest(),
                 "unbound or malformed typed premise receipt")
        assumptions.append(_proposition(left) == _proposition(rhs))
    _require(names == set(evidence["receipts"]), "missing or extra premise receipt")
    return assumptions, vacuous


class OrdinarySession:
    """Complete incremental propositional baseline with the same trusted local facts.

    SAT in this over-approximation is not typed SAT or a reachable RTL witness.
    The caller performs a typed fallback for unsupported conclusions. The
    evidence must be produced by certify() or checked by verify() first.
    """
    def __init__(self, prepared, evidence):
        self.endpoints = set(prepared["abstracts"])
        assumptions, self.vacuous = _checked_assumptions(prepared, evidence)
        self.solver = z3.SolverFor("QF_BV")
        self.solver.set(timeout=TIMEOUT_MS)
        self.solver.add(*assumptions)
        if self.vacuous:
            self.solver.add(z3.BoolVal(False))

    def compare(self, left_abstract, right_abstract):
        _require(left_abstract in self.endpoints and right_abstract in self.endpoints,
                 "comparison must use original abstract endpoints")
        lhs, rhs = (_proposition(parse(text)) for text in (left_abstract, right_abstract))
        statuses = {}
        for name, formula in (("old_only", z3.And(lhs, z3.Not(rhs))),
                              ("new_only", z3.And(rhs, z3.Not(lhs)))):
            self.solver.push()
            self.solver.add(formula)
            statuses[name] = str(self.solver.check())
            self.solver.pop()
        equivalent = all(statuses[k] == "unsat" for k in ("old_only", "new_only"))
        return {**statuses, "relation": "equivalent" if equivalent else "unknown", "vacuous": self.vacuous}


def ordinary(prepared, evidence, left_abstract, right_abstract):
    """Convenience one-pair entry point; use OrdinarySession for batch reuse."""
    return OrdinarySession(prepared, evidence).compare(left_abstract, right_abstract)
