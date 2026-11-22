"""Hash-guarded structural adapter for the pinned arbiter; not a general SV parser."""
import hashlib
import json
import re
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DUT = ROOT / 'examples/arbiter/rtl/fixed_priority_arbiter.sv'

def fold(op, terms):
    if not terms:
        return 'false' if op == 'or' else 'true'
    if len(terms) == 1:
        return terms[0]
    return f'({op} {terms[0]} {fold(op, terms[1:])})'

def selection(kind, index):
    atoms = [f'{kind}{i}' for i in range(index)]
    common = '(and (not reset) (not override_any))' if kind == 'req' else '(and (not reset) override_any)'
    compact = f'(and {common} (and {kind}{index} (not {fold("or", atoms)})))'
    expanded = f'(and {common} (and {kind}{index} {fold("and", [f"(not {a})" for a in atoms])}))'
    return compact, expanded

def extract():
    provenance = json.loads((ROOT / 'examples/arbiter/provenance.json').read_text())
    if hashlib.sha256(DUT.read_bytes()).hexdigest() != provenance['rtl_sha256']:
        raise ValueError('DUT changed: this adapter requires a reviewed source map for the new RTL')
    text = DUT.read_text()
    targets = []
    for kind, pattern in [('req', r'else if \(req\[(\d)\]\)'),
                          ('override', r'priority_override\[(\d)\] \?')]:
        matches = list(re.finditer(pattern, text))
        if [int(m[1]) for m in matches] != list(range(8)):
            raise ValueError('Unsupported priority chain')
        for m in matches:
            index = int(m[1])
            compact, expanded = selection(kind, index)
            targets.append({'id': f'{kind}_{index}', 'kind': kind, 'index': index,
                'source': str(DUT.relative_to(ROOT)), 'line': text[:m.start()].count('\n') + 1,
                'counter_type': 'line' if kind == 'req' else 'branch',
                'counter_outcome': ('if' if index == 7 else 'elsif') if kind == 'req' else 'cond_then',
                'compact': compact, 'expanded': expanded,
                'width': 1, 'logic': 'two_state', 'event': 'posedge clk',
                'reset_context': 'RTL also triggers on posedge reset; specification requires synchronous reset'})
    return targets

def parse(expr):
    tokens = re.findall(r'\(|\)|[^\s()]+', expr)
    def read(pos):
        token = tokens[pos]
        if token != '(':
            return token, pos + 1
        op = tokens[pos+1]
        args = []
        pos += 2
        while tokens[pos] != ')':
            node, pos = read(pos)
            args.append(node)
        if op not in ('not', 'and', 'or') or len(args) != (1 if op == 'not' else 2):
            raise ValueError('Unsupported Boolean expression')
        return (op, *args), pos + 1
    node, pos = read(0)
    if pos != len(tokens):
        raise ValueError('Trailing expression tokens')
    return node

def evaluate(ast, env):
    if isinstance(ast, str):
        if ast == 'true': return True
        if ast == 'false': return False
        return bool(env[ast])
    if ast[0] == 'not': return not evaluate(ast[1], env)
    if ast[0] == 'and': return evaluate(ast[1], env) and evaluate(ast[2], env)
    return evaluate(ast[1], env) or evaluate(ast[2], env)

def environment(reset, req, override):
    return {'reset': reset, 'override_any': override != 0,
            **{f'req{i}': bool(req & (1 << i)) for i in range(8)},
            **{f'override{i}': bool(override & (1 << i)) for i in range(8)}}

def witness(expr):
    ast = parse(expr)
    # Enumerate concrete legal binary inputs, preserving the override_any relation.
    for reset in (0, 1):
        for override in range(256):
            for req in range(256):
                if evaluate(ast, environment(reset, req, override)):
                    return reset, req, override
    return None

@cache
def _atom_tables():
    """One truth-table bit per legal arbiter input, in scalar witness order."""
    # The table index is reset[0], override[7:0], req[7:0] concatenated.
    assignments = 1 << 17
    tables = {'false': 0, 'true': (1 << assignments) - 1, 'override_any': 0}
    signals = [f'req{i}' for i in range(8)] + [f'override{i}' for i in range(8)] + ['reset']
    for bit, name in enumerate(signals):
        # The bit is low for a run of 2**bit indices, then high for as many.
        run = 1 << bit
        pattern = ((1 << run) - 1) << run
        period = run * 2
        while period < assignments:
            pattern |= pattern << period
            period *= 2
        tables[name] = pattern
        if name.startswith('override'):
            tables['override_any'] |= pattern
    return tables


def _truth_table(ast, atoms):
    if isinstance(ast, str):
        return atoms[ast]
    lhs = _truth_table(ast[1], atoms)
    if ast[0] == 'not':
        return atoms['true'] ^ lhs
    rhs = _truth_table(ast[2], atoms)
    return lhs & rhs if ast[0] == 'and' else lhs | rhs


def witness_fast(expr):
    """First legal (reset, req, override) for a pure two-state arbiter guard."""
    matches = _truth_table(parse(expr), _atom_tables())
    if not matches:
        return None
    first = (matches & -matches).bit_length() - 1
    return first >> 16, first & 255, (first >> 8) & 255


if __name__ == '__main__':
    print(json.dumps(extract(), indent=2))
