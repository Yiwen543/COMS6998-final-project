"""Add typed QF_BV reasoning to the frozen Slang source-counter adapter.

This module does not edit RTL, remove counters, or generate stimulus. Sequential
outputs and procedural-combinational outputs are free current-state values;
only unique, acyclic continuous assignments are expanded. All equivalences are
two-state, same-event-context claims, never temporal reachability claims.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path

from slang_guard_adapter import Adapter, Unsupported, both, walk


def stable(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:20]


def integer(value, width):
    value = str(value).replace('_', '')
    if re.fullmatch(r'-?\d+', value):
        return int(value) % (1 << width)
    match = re.fullmatch(r"(\d+)?'([sS]?)([bBoOdDhH])(-?[0-9a-fA-F]+)", value)
    if match:
        number = int(match[4], {'b': 2, 'o': 8, 'd': 10, 'h': 16}[match[3].lower()])
        literal_width = int(match[1]) if match[1] else max(32, width)
        number %= 1 << literal_width
        if match[2] and number & (1 << (literal_width-1)):
            number -= 1 << literal_width
        return number % (1 << width)
    if value in ("'0", "'1"):
        return 0 if value == "'0" else (1 << width)-1
    raise Unsupported('Unresolved/four-state integer literal: '+value)


class RichAdapter(Adapter):
    def resolve(self, item):
        seen = set()
        while True:
            if isinstance(item, dict):
                if item.get('kind') != 'TypeAlias':
                    return item
                item = item['target']
                continue
            address = item.split()[0]
            if address in seen or address not in self.index:
                raise Unsupported('Unresolved/cyclic type reference')
            seen.add(address)
            item = self.index[address]

    def typed(self, node):
        if node['kind'] == 'Call' and node.get('subroutine') in ('$signed', '$unsigned') and len(node['arguments']) == 1:
            operand = self.typed(node['arguments'][0])
            info = self.type_info(node['type'])
            if info['width'] != operand['type']['width']:
                raise Unsupported('Signing cast changes width unexpectedly')
            return {'kind': 'Conversion', 'type': info, 'operand': operand, 'op': node['subroutine']}
        if node['kind'] == 'ConditionalOp':
            if len(node['conditions']) != 1 or set(node['conditions'][0]) != {'expr'}:
                raise Unsupported('Pattern conditional expression')
            return {'kind': 'ConditionalOp', 'type': self.type_info(node['type']),
                    'condition': self.typed(node['conditions'][0]['expr']),
                    'left': self.typed(node['left']), 'right': self.typed(node['right'])}
        result = super().typed(node)
        if result['kind'] in ('IntegerLiteral', 'UnbasedUnsizedIntegerLiteral', 'constant'):
            result = {'kind': 'constant', 'type': result['type'],
                      'value': integer(result['value'], result['type']['width'])}
        elif result['kind'] == 'MemberAccess':
            result['bit_offset'] = self.resolve(node['member'])['bitOffset']
        return result

    def visit(self, node, guard, context, depth=0):
        if not isinstance(node, dict) or node.get('kind') not in ('Conditional', 'ConditionalOp'):
            return super().visit(node, guard, context, depth)
        try:
            kind = node['kind']
            if len(node['conditions']) != 1 or set(node['conditions'][0]) != {'expr'}:
                raise Unsupported('Pattern/multiple condition')
            cond = node['conditions'][0]['expr']
            pred = self.boolean(cond)
            self.add(node if kind == 'Conditional' else cond, both(guard, pred), context,
                     depth+1, 'if' if kind == 'Conditional' else 'cond_then', cond,
                     node['left'] if kind == 'ConditionalOp' else node)
            false = copy.deepcopy(self.targets[-1])
            false.update(id=f't{len(self.targets)}', compact=both(guard, f'(not {pred})'),
                         source_text='!('+self.text(cond)+')',
                         outcome='else' if kind == 'Conditional' else 'cond_else')
            # Verilator's opposite-polarity branch counter uses the true counter
            # anchor + 1, not the location of the source 'else' keyword. Joining
            # still requires an exact actual counter; absent counters stay absent.
            false['counter_anchor']['column'] += 1
            false['counter_anchor_basis'] += '; opposite polarity +1 (requires exact raw counter)'
            self.targets.append(false)
            self.visit(node['ifTrue' if kind == 'Conditional' else 'left'], both(guard, pred), context, depth+1)
            self.visit(node.get('ifFalse' if kind == 'Conditional' else 'right', {}),
                       both(guard, f'(not {pred})'), context, depth+1)
        except Unsupported as error:
            self.unsupported.append({**self.source(node), 'kind': node.get('kind'),
                                     'reason': str(error), 'descendants': 'not promoted'})


class BitVectors:
    def __init__(self, adapter, *, expand_aliases=True, procedural=False):
        self.adapter = adapter
        self.expand_aliases = expand_aliases
        self.variables, self.definitions, self.definition_sources = {}, {}, {}
        self.unresolved = []
        self.used_aliases = set()
        self.memo, self.active = {}, set()
        self._collect_definitions()
        if procedural:
            self._collect_procedures()

    @staticmethod
    def name(node):
        return 'v_'+stable({'declaration': node['declaration'], 'symbol': node['symbol'], 'type': node['type']})

    def _collect_definitions(self):
        drivers = {}
        for n in walk(self.adapter.body):
            if n.get('kind') == 'Assignment':
                for lhs in walk(n['left']):
                    if lhs.get('kind') == 'NamedValue':
                        drivers.setdefault(lhs['symbol'], []).append(n)
        saved = self.adapter.blocking_writes
        self.adapter.blocking_writes = set()
        try:
            for n in self.adapter.body['members']:
                if n['kind'] != 'ContinuousAssign':
                    continue
                assign = n['assignment']
                if assign['left']['kind'] != 'NamedValue' or len(drivers.get(assign['left']['symbol'], [])) != 1:
                    self.unresolved.append({'source': self.adapter.source(n), 'reason': 'not a unique whole-signal continuous driver'})
                    continue
                try:
                    lhs, rhs = self.adapter.typed(assign['left']), self.adapter.typed(assign['right'])
                    if lhs['type']['width'] != rhs['type']['width']:
                        raise Unsupported('Unelaborated assignment sizing')
                    key = self.name(lhs)
                    self.definitions[key] = rhs
                    self.definition_sources[key] = {'lhs': lhs, 'rhs': rhs, 'source': self.adapter.source(n),
                                                    'source_text': self.adapter.text(assign)}
                except Unsupported as error:
                    self.unresolved.append({'source': self.adapter.source(n), 'reason': str(error)})
        finally:
            self.adapter.blocking_writes = saved

    def _collect_procedures(self):
        procedures = [n for n in self.adapter.body['members'] if n['kind'] == 'ProceduralBlock']
        owners = {}
        for index, proc in enumerate(procedures):
            for assign in walk(proc):
                if assign.get('kind') == 'Assignment':
                    for n in walk(assign['left']):
                        if n.get('kind') == 'NamedValue':
                            owners.setdefault(n['symbol'], set()).add(index)
        saved = self.adapter.blocking_writes
        self.adapter.blocking_writes = set()
        try:
            for index, proc in enumerate(procedures):
                if proc['procedureKind'] != 'AlwaysComb':
                    continue
                assigned = {n['symbol']: self.adapter.typed(n) for a in walk(proc)
                            if a.get('kind') == 'Assignment' for n in walk(a['left'])
                            if n.get('kind') == 'NamedValue'}
                try:
                    if any(len(owners[symbol]) != 1 for symbol in assigned):
                        raise Unsupported('Multiple procedural writers')
                    initial = {self.name(n): {'kind': 'Uninitialized', 'type': n['type']} for n in assigned.values()}
                    final = self._statement(proc['body'], initial)
                    for node in assigned.values():
                        key = self.name(node)
                        rhs = final[key]
                        if any(n.get('kind') == 'Uninitialized' for n in walk(rhs)):
                            self.unresolved.append({'source': self.adapter.source(proc), 'signal': node['symbol'],
                                'reason': 'Not assigned on every path; no latch assumption allowed'})
                            continue
                        if key in self.definitions:
                            raise Unsupported('Procedural and continuous multiple drivers')
                        self.definitions[key] = rhs
                        self.definition_sources[key] = {'lhs': node, 'rhs': rhs,
                            'source': self.adapter.source(proc), 'source_text': self.adapter.text(proc['body']),
                            'method': 'blocking SSA; full ordered if/case; all paths assigned'}
                except Unsupported as error:
                    self.unresolved.append({'source': self.adapter.source(proc), 'reason': str(error)})
        finally:
            self.adapter.blocking_writes = saved

    def _expression(self, node, environment):
        typed = self.adapter.typed(node)
        def replace(n):
            if isinstance(n, dict):
                if n.get('kind') == 'NamedValue' and self.name(n) in environment:
                    return environment[self.name(n)]
                return {k: replace(v) for k, v in n.items()}
            if isinstance(n, list):
                return [replace(x) for x in n]
            return n
        return replace(typed)

    @staticmethod
    def _merge(condition, yes, no):
        return {k: yes[k] if yes[k] == no[k] else {'kind': 'ConditionalOp', 'type': yes[k]['type'],
                  'condition': condition, 'left': yes[k], 'right': no[k]} for k in yes}

    def _statement(self, node, environment):
        env = dict(environment)
        if not node:
            return env
        kind = node['kind']
        if kind == 'Block':
            return self._statement(node['body'], env)
        if kind == 'List':
            for item in node['list']:
                env = self._statement(item, env)
            return env
        if kind == 'Empty':
            return env
        if kind == 'ExpressionStatement':
            a = node['expr']
            if a['kind'] != 'Assignment' or a.get('isNonBlocking') or a['left']['kind'] != 'NamedValue':
                raise Unsupported('SSA supports whole-variable blocking assignments only')
            lhs = self.adapter.typed(a['left'])
            rhs = self._expression(a['right'], env)
            if lhs['type']['width'] != rhs['type']['width']:
                raise Unsupported('SSA assignment sizing mismatch')
            env[self.name(lhs)] = rhs
            return env
        if kind == 'Conditional':
            if len(node['conditions']) != 1 or set(node['conditions'][0]) != {'expr'}:
                raise Unsupported('SSA pattern condition')
            c = self._expression(node['conditions'][0]['expr'], env)
            return self._merge(c, self._statement(node['ifTrue'], env),
                               self._statement(node.get('ifFalse'), env))
        if kind == 'Case':
            if node['condition'] != 'Normal':
                raise Unsupported('SSA wildcard case')
            sel = self._expression(node['expr'], env)
            result = self._statement(node.get('defaultCase'), env)
            for item in reversed(node['items']):
                choices = [{'kind': 'BinaryOp', 'type': {'width': 1, 'signed': False, 'four_state': True},
                    'op': 'Equality', 'left': sel, 'right': self._expression(expr, env)} for expr in item['expressions']]
                condition = choices[0]
                for choice in choices[1:]:
                    condition = {'kind': 'BinaryOp', 'type': condition['type'], 'op': 'LogicalOr',
                                 'left': condition, 'right': choice}
                result = self._merge(condition, self._statement(item['stmt'], env), result)
            return result
        raise Unsupported('Unsupported SSA statement '+kind)

    @staticmethod
    def literal(value, width):
        return f'(_ bv{value % (1 << width)} {width})'

    @staticmethod
    def truth(term, width):
        return f'(not (= {term} (_ bv0 {width})))'

    @staticmethod
    def bit(condition):
        return f'(ite {condition} #b1 #b0)'

    @staticmethod
    def resize(term, old, new, signed):
        if old == new:
            return term
        if new < old:
            return f'((_ extract {new-1} 0) {term})'
        return f"((_ {'sign_extend' if signed else 'zero_extend'} {new-old}) {term})"

    def term(self, node):
        kind, width = node['kind'], node['type']['width']
        if kind == 'constant':
            return self.literal(node['value'], width)
        if kind == 'NamedValue':
            name = self.name(node)
            self.variables[name] = node
            if self.expand_aliases and name in self.definitions:
                if name in self.active:
                    raise Unsupported('Combinational alias cycle')
                self.used_aliases.add(name)
                if name not in self.memo:
                    self.active.add(name)
                    try:
                        self.memo[name] = self.term(self.definitions[name])
                    finally:
                        self.active.remove(name)
                return self.memo[name]
            return name
        if kind == 'Conversion':
            source = node['operand']['type']
            return self.resize(self.term(node['operand']), source['width'], width, source['signed'])
        if kind == 'MemberAccess':
            offset = node['bit_offset']
            if offset < 0 or offset+width > node['value']['type']['width']:
                raise Unsupported('Invalid packed field offset')
            return f"((_ extract {offset+width-1} {offset}) {self.term(node['value'])})"
        if kind == 'ElementSelect':
            # Variable/out-of-range indexing has four-state semantics; reject it.
            selector = node['selector']
            while selector['kind'] == 'Conversion':
                selector = selector['operand']
            if selector['kind'] != 'constant' or not 0 <= selector['value'] < node['value']['type']['width']:
                raise Unsupported('Dynamic or out-of-range element select')
            i = selector['value']
            return f"((_ extract {i} {i}) {self.term(node['value'])})"
        if kind == 'ConditionalOp':
            c = self.truth(self.term(node['condition']), node['condition']['type']['width'])
            branches = [self.resize(self.term(node[k]), node[k]['type']['width'], width,
                                    node[k]['type']['signed']) for k in ('left', 'right')]
            return f'(ite {c} {branches[0]} {branches[1]})'
        if kind == 'UnaryOp':
            operand, op = node['operand'], node['op']
            term, ow = self.term(operand), operand['type']['width']
            if op == 'LogicalNot':
                return self.bit(f'(= {term} (_ bv0 {ow}))')
            if op in ('BitwiseNot', 'Minus'):
                if ow != width:
                    raise Unsupported('Unary sizing mismatch')
                return f"({'bvnot' if op == 'BitwiseNot' else 'bvneg'} {term})"
            if op in ('BitwiseAnd', 'BitwiseOr'):
                condition = f'(= {term} {self.literal((1 << ow)-1, ow)})' if op == 'BitwiseAnd' else self.truth(term, ow)
                return self.bit(condition)
            raise Unsupported('Unsupported unary '+op)
        if kind == 'BinaryOp':
            l, r, op = node['left'], node['right'], node['op']
            a, b = self.term(l), self.term(r)
            aw, bw = l['type']['width'], r['type']['width']
            if op in ('LogicalAnd', 'LogicalOr'):
                return self.bit(f"({'and' if op == 'LogicalAnd' else 'or'} {self.truth(a, aw)} {self.truth(b, bw)})")
            if aw != bw:
                raise Unsupported('Binary operands not elaborated to equal width')
            if op in ('Equality', 'Inequality'):
                eq = f'(= {a} {b})'
                return self.bit(eq if op == 'Equality' else f'(not {eq})')
            if op in ('LessThan', 'LessThanEqual', 'GreaterThan', 'GreaterThanEqual'):
                signed = l['type']['signed'] and r['type']['signed']
                suffix = {'LessThan': 'lt', 'LessThanEqual': 'le', 'GreaterThan': 'gt', 'GreaterThanEqual': 'ge'}[op]
                return self.bit(f"(bv{'s' if signed else 'u'}{suffix} {a} {b})")
            arithmetic = {'Add': 'bvadd', 'Subtract': 'bvsub', 'BinaryAnd': 'bvand',
                          'BinaryOr': 'bvor', 'BinaryXor': 'bvxor', 'Multiply': 'bvmul'}
            if op in arithmetic and width == aw:
                return f'({arithmetic[op]} {a} {b})'
            raise Unsupported('Unsupported binary '+op)
        raise Unsupported('Unsupported typed term '+kind)

    def atom(self, atom):
        if atom['kind'] == 'truth_conversion':
            node = atom['operand']
            return self.truth(self.term(node), node['type']['width'])
        if atom['kind'] == 'case_two_state_eq':
            left, right = atom['left'], atom['right']
            if left['type']['width'] != right['type']['width']:
                raise Unsupported('Case operand width mismatch')
            return f'(= {self.term(left)} {self.term(right)})'
        raise Unsupported('Unknown predicate atom')

    def guards(self):
        definitions, supported, unsupported = {}, [], []
        for target in self.adapter.targets:
            try:
                for name in set(re.findall(r'p_[0-9a-f]+', target['compact'])):
                    if name not in definitions:
                        definitions[name] = self.atom(self.adapter.atoms[name])
                supported.append(target)
            except Unsupported as error:
                unsupported.append({'id': target['id'], 'reason': str(error)})
        declarations = '\n'.join(f"(declare-fun {k} () (_ BitVec {n['type']['width']}))" for k, n in sorted(self.variables.items()))
        atoms = '\n'.join(f'(define-fun {k} () Bool {v})' for k, v in sorted(definitions.items()))
        guards = '\n'.join(f"(define-fun {t['id']} () Bool {t['compact']})" for t in supported)
        header = '(set-logic QF_BV)\n(set-option :timeout 100)\n'+declarations+'\n'+atoms+'\n'+guards+'\n'
        return header, supported, unsupported


def pair_audit(adapter, output, *, expand_aliases=True, procedural=False):
    solver = BitVectors(adapter, expand_aliases=expand_aliases, procedural=procedural)
    header, supported, unsupported = solver.guards()
    pairs = [(a, b) for i, a in enumerate(supported) for b in supported[i+1:]
             if a['event_context'] == b['event_context'] and
             (a['source'], a['line'], a['column']) != (b['source'], b['line'], b['column'])]
    commands = []
    for a, b in pairs:
        commands.append(f'(push)\n(assert (xor {a["id"]} {b["id"]}))\n(check-sat)\n(pop)')
    path = output/'pairs.smt2'
    path.write_text(header+'\n'.join(commands)+'\n')
    result = subprocess.run(['z3', str(path)], capture_output=True, text=True, timeout=180, check=True)
    (output/'pairs-z3.log').write_text(result.stdout+result.stderr)
    statuses = result.stdout.splitlines()
    if len(statuses) != len(pairs) or any(s not in ('sat', 'unsat', 'unknown') for s in statuses):
        raise AssertionError('Unexpected Z3 pair response')
    equivalent = [{'left': a['id'], 'right': b['id'], 'source_expressions_differ': a['compact'] != b['compact']}
                  for (a, b), status in zip(pairs, statuses) if status == 'unsat']
    return {'supported_targets': supported, 'unsupported_targets': unsupported,
            'implementation_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'procedural_ssa_enabled': procedural, 'continuous_aliases_enabled': expand_aliases,
            'counts': {status: statuses.count(status) for status in ('sat', 'unsat', 'unknown')},
            'equivalent_pairs': equivalent, 'variables': solver.variables,
            'continuous_definitions': solver.definition_sources,
            'used_aliases': sorted(solver.used_aliases), 'unresolved_definitions': solver.unresolved,
            'pair_order': [[a['id'], b['id']] for a, b in pairs], 'statuses': statuses,
            'proof_scope': 'All binary valuations of free inputs/current-state/procedural outputs; only acyclic unique continuous definitions substituted. No state invariant or reachability assumption.'}


if __name__ == '__main__':
    import argparse
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--ast', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--no-aliases', action='store_true')
    cli.add_argument('--procedural', action='store_true')
    args = cli.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if (args.output/'audit.json').exists():
        raise SystemExit('Refuse to overwrite completed evidence')
    adapter = RichAdapter(json.loads(args.ast.read_text()), 'spi_host_fsm').extract()
    result = pair_audit(adapter, args.output, expand_aliases=not args.no_aliases, procedural=args.procedural)
    (args.output/'audit.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.output/'extraction.json').write_text(json.dumps({'targets': adapter.targets,
        'atoms': adapter.atoms, 'unsupported': adapter.unsupported}, indent=2)+'\n')
    print(json.dumps({'targets': len(adapter.targets), 'counts': result['counts'],
        'nontrivial_pairs': sum(p['source_expressions_differ'] for p in result['equivalent_pairs']),
        'unsupported': result['unsupported_targets']}, indent=2))
