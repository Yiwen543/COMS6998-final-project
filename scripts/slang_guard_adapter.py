"""Source-preserving two-state predicate adapter for elaborated Slang JSON.

Only lexical activation and total Boolean operators are normalized. Arithmetic,
comparisons and vector truth conversions remain typed opaque atoms. Case arms
retain first-match priority. No temporal or four-state equivalence is claimed.
This adapter intentionally does not replace the frozen native-Yosys frontend.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

from preflight_heldout import ENGINE, ROOT, verify_rewrites, z3_equivalent


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def both(a, b):
    return b if a == 'true' else f'(and {a} {b})'


def any_of(items):
    value = 'false'
    for item in items:
        value = item if value == 'false' else f'(or {value} {item})'
    return value


class Unsupported(ValueError):
    pass


class Adapter:
    def __init__(self, ast, top):
        self.index = {str(n['addr']): n for n in walk(ast) if 'addr' in n}
        matches = [n for n in walk(ast) if n.get('kind') == 'Instance' and n.get('name') == top]
        if len(matches) != 1:
            raise Unsupported('Expected exactly one top instance')
        self.top, self.body = top, matches[0]['body']
        self.atoms, self.targets, self.unsupported = {}, [], []
        self.priority_proofs = []
        self.blocking_writes = set()

    def resolve(self, item):
        seen = set()
        while isinstance(item, str) or item.get('kind') == 'TypeAlias':
            if isinstance(item, dict):
                item = item['target']
            address = item.split()[0]
            if address in seen or address not in self.index:
                raise Unsupported('Unresolved type/symbol reference')
            seen.add(address)
            item = self.index[address]
        return item

    def type_info(self, item):
        item = self.resolve(item)
        kind = item['kind']
        if kind == 'ScalarType':
            return {'width': 1, 'signed': item['isSigned'], 'four_state': item['name'] != 'bit'}
        if kind == 'PackedArrayType':
            base = self.type_info(item['elementType'])
            ends = re.fullmatch(r'\[(-?\d+):(-?\d+)\]', item['range'])
            if not ends:
                raise Unsupported('Unresolved packed range')
            return {**base, 'width': base['width'] * (abs(int(ends[1])-int(ends[2]))+1),
                    'signed': item.get('isSigned', base['signed'])}
        if kind == 'EnumType':
            return self.type_info(item['baseType'])
        if kind == 'PackedStructType':
            return {'width': sum(self.type_info(m['type'])['width'] for m in item['members']
                                 if m['kind'] == 'Field'),
                    'signed': item.get('isSigned', False), 'four_state': True}
        if kind == 'PredefinedIntegerType':
            widths = {'byte': 8, 'shortint': 16, 'int': 32, 'integer': 32, 'longint': 64, 'time': 64}
            if item['name'] not in widths:
                raise Unsupported('Unknown integer type')
            return {'width': widths[item['name']], 'signed': item['name'] != 'time',
                    'four_state': item['name'] in ('integer', 'time')}
        raise Unsupported('Unsupported type '+kind)

    def source(self, node):
        path = node.get('source_file_start', node.get('source_file'))
        line = node.get('source_line_start', node.get('source_line'))
        column = node.get('source_column_start', node.get('source_column'))
        if not path or not line:
            raise Unsupported('Missing source provenance')
        return {'source': path, 'line': line, 'column': column,
                'end_line': node.get('source_line_end', line),
                'end_column': node.get('source_column_end', column)}

    def text(self, node):
        src = self.source(node)
        lines = (ROOT/src['source']).read_text().splitlines()
        chosen = lines[src['line']-1:src['end_line']]
        if len(chosen) == 1:
            return chosen[0][src['column']-1:src['end_column']-1]
        chosen[0] = chosen[0][src['column']-1:]
        chosen[-1] = chosen[-1][:src['end_column']-1]
        return '\n'.join(chosen)

    def typed(self, node):
        kind = node['kind']
        result = {'kind': kind, 'type': self.type_info(node['type'])}
        if kind in ('NamedValue', 'HierarchicalValue'):
            if node['symbol'].split()[0] in self.blocking_writes:
                raise Unsupported('Predicate reads a variable assigned in this procedure; SSA required')
            symbol = self.resolve(node['symbol'])
            if symbol['kind'] in ('EnumValue', 'Parameter', 'LocalParameter'):
                init = symbol.get('initializer')
                value = symbol.get('value', init.get('constant') if init else None)
                if value is None:
                    raise Unsupported('Unresolved constant')
                return {'kind': 'constant', 'type': result['type'], 'value': value}
            # Source declaration identity avoids address instability and collisions.
            result['declaration'] = self.source(symbol)
            result['symbol'] = node['symbol'].split(' ', 1)[1]
            if kind == 'HierarchicalValue':
                raise Unsupported('Hierarchical expression alias not yet proven')
        elif kind in ('IntegerLiteral', 'UnbasedUnsizedIntegerLiteral'):
            result['value'] = node.get('constant', node.get('value'))
            if re.search('[xz]', str(result['value']).lower()):
                raise Unsupported('Four-state literal')
        elif kind in ('UnaryOp', 'Conversion'):
            result['op'] = node.get('op', 'Conversion')
            result['operand'] = self.typed(node['operand'])
        elif kind == 'BinaryOp':
            if node['op'] in ('CaseEquality', 'CaseInequality', 'WildcardEquality', 'WildcardInequality'):
                raise Unsupported('Four-state comparison')
            result.update(op=node['op'], left=self.typed(node['left']), right=self.typed(node['right']))
        elif kind == 'MemberAccess':
            field = self.resolve(node['member'])
            result.update(value=self.typed(node['value']), member=field['name'])
        elif kind == 'ElementSelect':
            result.update(value=self.typed(node['value']), selector=self.typed(node['selector']))
        else:
            raise Unsupported('Unsupported expression '+kind)
        return result

    def atom(self, typed):
        key = 'p_'+hashlib.sha256(json.dumps(typed, sort_keys=True).encode()).hexdigest()[:20]
        if key in self.atoms and self.atoms[key] != typed:
            raise AssertionError('Atom hash collision')
        self.atoms[key] = typed
        return key

    def boolean(self, node):
        info = self.type_info(node['type'])
        if node['kind'] == 'UnaryOp' and (node['op'] == 'LogicalNot' or
                (node['op'] == 'BitwiseNot' and info['width'] == 1)):
            return f"(not {self.boolean(node['operand'])})"
        if node['kind'] == 'BinaryOp':
            op = node['op']
            if op in ('LogicalAnd', 'LogicalOr') or (info['width'] == 1 and op in ('BinaryAnd', 'BinaryOr')):
                tag = 'and' if op in ('LogicalAnd', 'BinaryAnd') else 'or'
                return f"({tag} {self.boolean(node['left'])} {self.boolean(node['right'])})"
        return self.atom({'kind': 'truth_conversion', 'operand': self.typed(node),
                          'semantics': 'nonzero in binary values'})

    def add(self, node, guard, context, depth, outcome, predicate=None, anchor=None):
        src = self.source(node)
        anchor_node = anchor or node
        while anchor_node.get('kind') == 'Conversion':
            anchor_node = anchor_node['operand']
        anchor_src = self.source(anchor_node)
        basis = 'AST statement/arm start'
        if outcome == 'cond_then' and anchor_node['kind'] == 'MemberAccess':
            field = self.resolve(anchor_node['member'])['name']
            if not self.text(anchor_node).endswith('.'+field):
                raise Unsupported('Cannot anchor member-access token')
            anchor_src['line'] = anchor_src['end_line']
            anchor_src['column'] = anchor_src['end_column']-len(field)
            basis = 'AST true arm member-selection identifier token'
        elif outcome == 'cond_then' and anchor_node['kind'] == 'BinaryOp':
            operators = {'Subtract': '-', 'Add': '+', 'Equality': '==', 'Inequality': '!=',
                         'LogicalAnd': '&&', 'LogicalOr': '||', 'BinaryAnd': '&', 'BinaryOr': '|'}
            token = operators.get(anchor_node['op'])
            lhs, rhs = self.source(anchor_node['left']), self.source(anchor_node['right'])
            if token and lhs['end_line'] == rhs['line']:
                line = (ROOT/lhs['source']).read_text().splitlines()[lhs['end_line']-1]
                between = line[lhs['end_column']-1:rhs['column']-1]
                if between.strip() == token:
                    anchor_src['line'] = lhs['end_line']
                    anchor_src['column'] = lhs['end_column']+len(between)-len(between.lstrip())
                    basis = 'AST true arm binary operator token verified between operand spans'
        elif outcome == 'case':
            anchor_src['line'] = anchor_src['end_line']
            line = (ROOT/anchor_src['source']).read_text().splitlines()[anchor_src['line']-1]
            rest = line[anchor_src['end_column']-1:]
            matched = re.match(r'\s*:', rest)
            if not matched:
                raise Unsupported('Case colon token not on final label line')
            anchor_src['column'] = anchor_src['end_column']+len(matched[0])-1
            basis = 'Case arm colon token after final AST label'
        self.targets.append({**src, 'id': f"t{len(self.targets)}", 'compact': guard,
            'source_text': self.text(predicate or node), 'event_context': context,
            'guard_depth': depth, 'outcome': outcome,
            'counter_anchor': anchor_src, 'counter_anchor_basis': basis,
            'source_mapping': 'Slang AST span; raw counter mapping pending'})

    def visit(self, node, guard, context, depth=0):
        if not isinstance(node, dict):
            return
        kind = node.get('kind')
        try:
            if kind in ('Conditional', 'ConditionalOp'):
                if len(node['conditions']) != 1 or set(node['conditions'][0]) != {'expr'}:
                    raise Unsupported('Pattern/multiple condition')
                cond = node['conditions'][0]['expr']
                pred = self.boolean(cond)
                self.add(node if kind == 'Conditional' else cond, both(guard, pred), context,
                         depth+1, 'if' if kind == 'Conditional' else 'cond_then', cond,
                         node['left'] if kind == 'ConditionalOp' else node)
                self.visit(node['ifTrue' if kind == 'Conditional' else 'left'], both(guard, pred), context, depth+1)
                self.visit(node.get('ifFalse' if kind == 'Conditional' else 'right', {}),
                           both(guard, f'(not {pred})'), context, depth+1)
                return
            if kind == 'Case':
                if node['condition'] != 'Normal':
                    raise Unsupported('Wildcard case unsupported')
                previous = []
                for arm in node['items']:
                    eq = any_of([self.atom({'kind': 'case_two_state_eq',
                        'left': self.typed(node['expr']), 'right': self.typed(expr)})
                        for expr in arm['expressions']])
                    # Never discard earlier-arm conditions based merely on unique.
                    active = both(guard, both(f'(not {any_of(previous)})', eq)) if previous else both(guard, eq)
                    self.add(arm['expressions'][0], active, context, depth+1, 'case', arm['expressions'][0], arm['expressions'][-1])
                    self.visit(arm['stmt'], active, context, depth+1)
                    previous.append(eq)
                self.visit(node.get('defaultCase', {}), both(guard, f'(not {any_of(previous)})'), context, depth+1)
                return
            for key, value in node.items():
                if key in ('type', 'timing'):
                    continue
                if isinstance(value, dict):
                    self.visit(value, guard, context, depth)
                elif isinstance(value, list):
                    for child in value:
                        self.visit(child, guard, context, depth)
        except Unsupported as error:
            self.unsupported.append({**self.source(node), 'kind': kind, 'reason': str(error),
                                     'descendants': 'not promoted'})

    def extract(self):
        for member in self.body['members']:
            if member['kind'] == 'ProceduralBlock':
                body = member['body']
                self.blocking_writes = {n['symbol'].split()[0]
                    for a in walk(body) if a.get('kind') == 'Assignment' and not a.get('isNonBlocking', False)
                    for n in walk(a['left']) if n.get('kind') == 'NamedValue'}
                context = ['combinational']
                if member['procedureKind'] != 'AlwaysComb':
                    if body['kind'] != 'Timed':
                        self.unsupported.append({'reason': 'untimed procedure', **self.source(member)})
                        continue
                    timing = body['timing']
                    events = timing.get('events', [timing])
                    context = []
                    for event in events:
                        if event['kind'] != 'SignalEvent' or event['expr']['kind'] != 'NamedValue':
                            raise Unsupported('Unsupported event expression')
                        context.append(event['edge']+':'+event['expr']['symbol'].split(' ', 1)[1])
                self.visit(body, 'true', context)
            elif member['kind'] == 'ContinuousAssign':
                self.blocking_writes = set()
                self.visit(member['assignment'], 'true', ['combinational'])
            elif member['kind'] in ('Instance', 'GenerateBlock', 'GenerateBlockArray'):
                self.unsupported.append({**self.source(member), 'kind': member['kind'],
                    'reason': 'Nested instance/generate source counters not promoted; top counters retained'})
        return self

    def evidence(self):
        rules = verify_rewrites()
        payload = [{'id': t['id'], 'compact': t['compact'], 'expanded': t['compact']} for t in self.targets]
        graph = json.loads(subprocess.run([str(ENGINE)], input=json.dumps(payload), text=True,
            capture_output=True, check=True, timeout=30).stdout)
        roots = {t['id']: t for t in graph['targets']}
        groups = defaultdict(list)
        for t in self.targets:
            groups[(tuple(t['event_context']), roots[t['id']]['eclass'])].append(t)
        merged = []
        for (ctx, ec), members in groups.items():
            if len({(m['source'], m['line'], m['column']) for m in members}) < 2:
                continue
            for m in members[1:]:
                if not z3_equivalent(members[0]['compact'], m['compact']):
                    raise AssertionError('Unproven egg merge')
            merged.append({'event_context': ctx, 'eclass': ec, 'members': members,
                'distinct_expressions': len({m['compact'] for m in members}),
                'representative': roots[members[0]['id']]['representative'],
                'z3_pair_proofs': len(members)-1, 'status': 'semantic_only'})
        return {'schema': 'slang_typed_guard_v1', 'top': self.top,
            'semantics': 'two-state Boolean normalization; typed opaque non-Boolean atoms; no temporal rewriting',
            'targets': self.targets, 'atoms': self.atoms, 'unsupported': self.unsupported,
            'groups': merged, 'rewrite_proofs': rules, 'egg': graph,
            'case_priority': 'All preceding arm exclusions retained, including unique case',
            'coverage': 'Every source counter retained separately; no inferred hit transfer'}


if __name__ == '__main__':
    import argparse
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--ast', type=Path, required=True)
    cli.add_argument('--top', required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    data = Adapter(json.loads(args.ast.read_text()), args.top).extract().evidence()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k: len(data[k]) for k in ('targets', 'atoms', 'groups', 'unsupported')}))
