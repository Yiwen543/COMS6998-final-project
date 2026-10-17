#!/usr/bin/env python3
"""Offline mechanism audit. Synthetic Boolean cases are NOT RTL performance results."""
import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path
from agent_core import dump, feedback, semantic_groups, simplify, ast_text
from predicates import ROOT, parse, evaluate, extract


def audit(binary):
    # Includes a no-difference control; these are mechanism unit cases, not benchmarks.
    cases = [
        ('commutative-control', '(and a b)', '(and b a)'),
        ('distributive', '(and a (or b c))', '(or (and a b) (and a c))'),
        ('distributive-dual', '(or a (and b c))', '(and (or a b) (or a c))'),
        ('absorption-control', 'a', '(or a (and a b))')]
    targets = []
    for name, left, right in cases:
        for i, expr in enumerate((left, right)):
            targets.append(dict(id=f'{name}-{i}', compact=expr, expanded=expr,
                                width=1, logic='two_state', event='combinational', reset_context='none'))
    def graph_for(ts):
        return json.loads(subprocess.run([str(binary)], input=json.dumps(ts), text=True,
                                        capture_output=True, check=True, timeout=20).stdout)
    graph = graph_for(targets)
    roots = {t['id']: t for t in graph['targets']}
    checks = 0
    for t in targets:
        for bits in itertools.product((False, True), repeat=3):
            env = dict(zip('abc', bits))
            if evaluate(parse(t['compact']), env) != evaluate(parse(roots[t['id']]['representative']), env):
                raise AssertionError(t['id'])
            checks += 1
    exprs = {t['id']: t['compact'] for t in targets}
    c = semantic_groups(targets, exprs, graph)
    d = semantic_groups(targets, exprs)
    actual = extract()
    actual_graph = graph_for(actual)
    points = json.loads((ROOT / 'results/step1/initial-coverage.json').read_text())['points']
    arms = {g: feedback(g, actual, actual_graph, points) for g in 'BCD'}
    encoded = {g: json.dumps(value, sort_keys=True, separators=(',', ':')).encode() for g, value in arms.items()}
    return dict(mode='offline-mechanism-audit-not-LLM-or-RTL-performance',
                exhaustive_boolean_checks=checks, synthetic_egraph_groups=c,
                synthetic_baseline_groups=d, arbiter_feedback=arms,
                arbiter_feedback_bytes={g: len(v) for g, v in encoded.items()},
                arbiter_feedback_sha256={g: hashlib.sha256(v).hexdigest() for g, v in encoded.items()},
                arbiter_C_D_identical=encoded['C'] == encoded['D'],
                egraph_stop_reason=graph['stop_reason'],
                limitation='Synthetic algebra examples establish mechanism only; no coverage or token benefit is established.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output)
    if out.exists():
        parser.error('Choose a new output file')
    out.parent.mkdir(parents=True, exist_ok=True)
    result = audit(ROOT / 'egraph/target/debug/rtl-predicate-egraph')
    dump(out, result)
    print(json.dumps({k: v for k, v in result.items() if k != 'arbiter_feedback'}, indent=2))

if __name__ == '__main__':
    main()
