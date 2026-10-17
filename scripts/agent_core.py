"""Feedback adapters and a small Responses API client; no generated code execution."""
import json
import os
import urllib.error
import urllib.request
from collections import Counter
from predicates import parse


SYSTEM = """You choose the next stimulus batch for a fixed RTL verification harness.
The DUT and independent checker are immutable. Return JSON matching the schema.
Use the specification, RTL, previous inputs and permitted feedback to choose useful
new inputs. You may probe specification corner cases as well as uncovered paths.
Follow the fixed simulation_protocol and verification scope supplied in the context.
Do not return RTL, a testbench, shell commands, or private reasoning. The note is
a short description of the intended test. Avoid repeating earlier vectors.
Each simulation replays the configured starter suite then all submitted vectors.
Raw zero-hit counters are retained; they are not automatically reachable.
"""


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def ast_text(node):
    if isinstance(node, str):
        return node
    return '(' + ' '.join([node[0], *(ast_text(x) for x in node[1:])]) + ')'


def ast_size(node):
    return 1 if isinstance(node, str) else 1 + sum(ast_size(x) for x in node[1:])


def simplify(node):
    """Strong ordinary baseline: canonical AC, constants, idempotence, absorption.

    Deliberately has no distributive search or e-classes. Both arms use the same
    downstream encoding and semantic grouping policy.
    """
    if isinstance(node, str):
        return node
    op = node[0]
    args = [simplify(a) for a in node[1:]]
    if op == 'not':
        child = args[0]
        if child in ('true', 'false'):
            return 'false' if child == 'true' else 'true'
        if isinstance(child, tuple) and child[0] == 'not':
            return child[1]
        return ('not', child)
    terms = []
    def flatten(n):
        if isinstance(n, tuple) and n[0] == op:
            for c in n[1:]:
                flatten(c)
        else:
            terms.append(n)
    for arg in args:
        flatten(arg)
    identity, zero = ('true', 'false') if op == 'and' else ('false', 'true')
    if zero in terms:
        return zero
    terms = sorted(set(t for t in terms if t != identity), key=ast_text)
    other = 'or' if op == 'and' else 'and'
    def leaves(n):
        if isinstance(n, tuple) and n[0] == other:
            return leaves(n[1]) + leaves(n[2])
        return [n]
    terms = [t for t in terms if not (isinstance(t, tuple) and t[0] == other
             and any(x in terms for x in leaves(t)))]
    if not terms:
        return identity
    result = terms[-1]
    for term in reversed(terms[:-1]):
        result = (op, term, result)
    return result


def semantic_groups(targets, expressions, graph=None):
    """Hints only: never merge raw counters or change the coverage denominator.

    Equivalence is usable only inside the same sampling/reset/logic context.
    Bounded egg saturation may miss equivalences; a separate proof is not inferred.
    """
    roots = {t['id']: t for t in graph['targets']} if graph else {}
    groups = {}
    for t in targets:
        scope = tuple(t.get(k) for k in ('width', 'logic', 'event', 'reset_context'))
        key = roots[t['id']]['eclass'] if graph else ast_text(simplify(parse(expressions[t['id']])))
        groups.setdefault((scope, key), []).append(t['id'])
    return [ids for ids in groups.values() if len(ids) > 1]


def factor_shared(expressions):
    """Losslessly factor repeated syntax, identically for C and D."""
    trees = {key: parse(value) for key, value in expressions.items()}
    counts = Counter()
    nodes = {}
    def collect(node, seen):
        if isinstance(node, str):
            return
        key = ast_text(node)
        nodes[key] = node
        seen.add(key)
        for child in node[1:]:
            collect(child, seen)
    for tree in trees.values():
        seen = set()
        collect(tree, seen)
        counts.update(seen)
    # Select maximal shared subtrees, rather than listing all nested duplicates.
    candidates = sorted((key for key, count in counts.items()
                         if count > 1 and ast_size(nodes[key]) >= 4),
                        key=lambda key: (-ast_size(nodes[key]), key))
    selected = []
    for key in candidates:
        if not any(key in larger for larger in selected):
            selected.append(key)
        if len(selected) == 16:
            break
    names = {key: f'shared_{i}' for i, key in enumerate(selected)}
    def render(node):
        key = ast_text(node)
        if key in names:
            return names[key]
        if isinstance(node, str):
            return node
        return '(' + ' '.join([node[0], *(render(x) for x in node[1:])]) + ')'
    return ({names[key]: key for key in selected},
            {key: render(tree) for key, tree in trees.items()})


def feedback(group, targets, graph, points):
    from coverage import join
    if group == 'A':
        return {}
    raw = [{k: p[k] for k in ('source', 'line', 'column', 'type', 'outcome', 'hits')}
           for p in points]
    # Use an identity graph to share exactly the same source join for B/C/D.
    identity = {'targets': [{'id': t['id']} for t in targets]}
    joined = join(targets, identity, points)
    pending = [t for t in joined if t['uncovered']]
    expressions = {t['id']: t['compact'] for t in pending}
    if group == 'C':
        roots = {t['id']: t for t in graph['targets']}
        for key in expressions:
            if not roots[key]['equivalent']:
                raise ValueError('Unverified graph representative')
            expressions[key] = roots[key]['representative']
    elif group == 'D':
        expressions = {key: ast_text(simplify(parse(expr)))
                       for key, expr in expressions.items()}
    definitions, rendered = factor_shared(expressions) if group in ('C', 'D') else ({}, expressions)
    result = {'raw_dut_coverage': raw, 'uncovered_targets': []}
    if group in ('C', 'D'):
        groups = semantic_groups(pending, expressions, graph if group == 'C' else None)
        if groups:
            result['equivalent_target_groups'] = groups
    if definitions:
        result['shared_conditions'] = definitions
    for t in pending:
        result['uncovered_targets'].append({
            'id': t['id'], 'source': t['source'], 'line': t['line'],
            'counter_type': t['counter_type'], 'counter_outcome': t['counter_outcome'],
            'width': t['width'], 'logic': t['logic'], 'event': t['event'],
            'reset_context': t['reset_context'], 'predicate': rendered[t['id']]})
    return result


def response_schema(targets, batch_size, input_fields=None):
    input_fields = input_fields or {"reset": 1, "req": 255, "priority_override": 255}
    vector = {
        'type': 'object', 'additionalProperties': False,
        'properties': {
            'target_id': {'type': 'string', 'enum': [t['id'] for t in targets] + ['spec_probe']},
            **{key: {'type': 'integer', 'minimum': 0, 'maximum': high}
               for key, high in input_fields.items()}},
        'required': ['target_id', *input_fields]}
    return {'type': 'object', 'additionalProperties': False,
            'properties': {
                'note': {'type': 'string'},
                'vectors': {'type': 'array', 'minItems': 1, 'maxItems': batch_size,
                            'items': vector}},
            'required': ['note', 'vectors']}


def validate_batch(data, targets, batch_size, input_fields=None):
    input_fields = input_fields or {"reset": 1, "req": 255, "priority_override": 255}
    if not isinstance(data, dict) or set(data) != {'note', 'vectors'}:
        raise ValueError('Response must contain only note and vectors')
    if not isinstance(data['note'], str) or len(data['note']) > 2000:
        raise ValueError('note must be a short string')
    vectors = data['vectors']
    if not isinstance(vectors, list) or not 1 <= len(vectors) <= batch_size:
        raise ValueError(f'Expected 1 to {batch_size} vectors')
    ids = {t['id'] for t in targets} | {'spec_probe'}
    for v in vectors:
        if not isinstance(v, dict) or set(v) != {'target_id', *input_fields}:
            raise ValueError('Unexpected vector fields')
        if not isinstance(v['target_id'], str) or v['target_id'] not in ids:
            raise ValueError('Unknown target_id')
        for key, high in input_fields.items():
            if type(v[key]) is not int or not 0 <= v[key] <= high:
                raise ValueError(f'{key} must be an integer in 0..{high}')
    return vectors


def request_body(config, context, targets, batch_size, input_fields=None):
    return {
        'model': config.model,
        'reasoning': {'effort': config.effort},
        'store': False,
        'max_output_tokens': config.max_output_tokens,
        'input': [
            {'role': 'system', 'content': SYSTEM},
            {'role': 'user', 'content': json.dumps(context, ensure_ascii=False)}],
        'text': {'format': {'type': 'json_schema', 'name': 'stimulus_batch',
                            'strict': True, 'schema': response_schema(targets, batch_size, input_fields)}}}


def output_json(response):
    if response.get('status') != 'completed':
        raise ValueError(f"Model response not completed: {response.get('status')}")
    text = []
    for item in response.get('output', []):
        if item.get('type') != 'message':
            continue
        for content in item.get('content', []):
            if content.get('type') == 'refusal':
                raise ValueError('Model refused this request')
            if content.get('type') == 'output_text':
                text.append(content['text'])
    if not text:
        raise ValueError('Model returned no output_text')
    return json.loads(''.join(text))


def usage_counts(response):
    usage = response.get('usage')
    if not isinstance(usage, dict):
        return None
    counts = [usage.get(k) for k in ('input_tokens', 'output_tokens')]
    if any(type(v) is not int or v < 0 for v in counts):
        return None
    # Reasoning tokens are already included in output_tokens.
    return {'input_tokens': counts[0], 'output_tokens': counts[1],
            'total_tokens': sum(counts),
            'cached_tokens': (usage.get('input_tokens_details') or {}).get('cached_tokens'),
            'reasoning_tokens': (usage.get('output_tokens_details') or {}).get('reasoning_tokens')}


class OpenAIProvider:
    is_live = True

    def __init__(self, timeout=120):
        self.key = os.environ.get('OPENAI_API_KEY')
        if not self.key:
            raise ValueError('Set OPENAI_API_KEY in your terminal before a live run.')
        self.timeout = timeout

    def generate(self, body):
        req = urllib.request.Request('https://api.openai.com/v1/responses',
            data=json.dumps(body).encode(),
            headers={'Authorization': 'Bearer ' + self.key,
                     'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as stream:
                return json.load(stream)
        except urllib.error.HTTPError as error:
            # Do not persist request headers or credentials. No hidden paid retries.
            raise RuntimeError(f'OpenAI HTTP {error.code}; request was not retried') from None
