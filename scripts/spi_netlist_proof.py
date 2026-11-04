"""Independent Yosys-cell QF_BV cross-check of Slang combinational SSA outputs.

Cell semantics follow the installed Yosys simlib.v. FF Q and primary input bits
are unconstrained current values; no sequential or reset behavior is rewritten.
Parallel mux selectors must independently prove one-hot-or-zero before using a
binary mux interpretation. Unsupported/x-valued cells fail closed.
"""
import json
import subprocess
from pathlib import Path

from spi_semantic_v2 import BitVectors, RichAdapter, Unsupported, stable


class Netlist:
    def __init__(self, module):
        self.module = module
        self.primary = {b for p in module['ports'].values() if p['direction'] == 'input' for b in p['bits']}
        self.drivers = {}
        self.macros, self.active, self.onehot, self.used_cells = {}, set(), [], set()
        self.unknown_bits = []
        for name, cell in module['cells'].items():
            if cell['type'] == '$aldff':
                self.primary.update(cell['connections']['Q'])
                continue
            outputs = [p for p, d in cell['port_directions'].items() if d == 'output']
            if outputs != ['Y']:
                raise Unsupported('Unsupported cell output '+cell['type'])
            for i, bit in enumerate(cell['connections']['Y']):
                if bit in self.drivers:
                    raise Unsupported('Multiple netlist drivers')
                self.drivers[bit] = (name, i)

    def bit(self, bit):
        if bit in ('0', '1'):
            return '#b'+bit
        if bit == 'x':
            # A synthesis don't-care is not zero. Universally quantify a fresh
            # binary value; a relevant don't-care prevents an equivalence proof.
            name = f'unknown_{len(self.unknown_bits)}'
            self.unknown_bits.append(name)
            return name
        if isinstance(bit, str):
            raise Unsupported('Unknown netlist bit '+bit)
        if bit in self.primary:
            return f'b{bit}'
        if bit not in self.drivers:
            raise Unsupported('Unconnected netlist bit')
        name, index = self.drivers[bit]
        term, width = self.cell(name)
        return term if width == 1 else f'((_ extract {index} {index}) {term})'

    def word(self, bits):
        items = [self.bit(bit) for bit in reversed(bits)]
        if not items:
            raise Unsupported('Zero-width netlist value')
        result = items[0]
        for item in items[1:]:
            result = f'(concat {result} {item})'
        return result

    def cell(self, name):
        node = self.module['cells'][name]
        width = len(node['connections']['Y'])
        key = 'n_'+stable(name)
        if key in self.macros:
            return key, width
        if name in self.active:
            raise Unsupported('Combinational netlist cycle')
        self.active.add(name)
        self.used_cells.add(name)
        c, p, kind = node['connections'], node['parameters'], node['type']
        def value(port):
            return self.word(c[port])
        def resized(port, size, signed=False):
            return BitVectors.resize(value(port), len(c[port]), size, signed)
        def truth(port):
            return BitVectors.truth(value(port), len(c[port]))
        if kind == '$buf':
            if len(c['A']) != width:
                raise Unsupported('Buffer width mismatch')
            expr = value('A')
        elif kind == '$mux':
            expr = f"(ite (= {value('S')} #b1) {value('B')} {value('A')})"
        elif kind == '$pmux':
            selects = [self.bit(b) for b in c['S']]
            bad = [f'(and (= {a} #b1) (= {b} #b1))' for i, a in enumerate(selects) for b in selects[i+1:]]
            self.onehot.append({'cell': name, 'violation': '(or '+' '.join(bad)+')' if bad else 'false'})
            expr = value('A')
            for i, select in enumerate(selects):
                data = self.word(c['B'][i*width:(i+1)*width])
                expr = f'(ite (= {select} #b1) {data} {expr})'
        elif kind in ('$logic_not', '$reduce_bool', '$reduce_or', '$reduce_and'):
            predicate = truth('A')
            if kind == '$logic_not':
                predicate = f'(not {predicate})'
            elif kind == '$reduce_and':
                predicate = f"(= {value('A')} {BitVectors.literal((1 << len(c['A']))-1, len(c['A']))})"
            expr = BitVectors.resize(BitVectors.bit(predicate), 1, width, False)
        elif kind in ('$logic_and', '$logic_or'):
            tag = 'and' if kind == '$logic_and' else 'or'
            expr = BitVectors.resize(BitVectors.bit(f"({tag} {truth('A')} {truth('B')})"), 1, width, False)
        elif kind in ('$eq', '$ne'):
            signed = int(p['A_SIGNED'], 2) == 1 and int(p['B_SIGNED'], 2) == 1
            size = max(len(c['A']), len(c['B']))
            pred = f"(= {resized('A', size, signed)} {resized('B', size, signed)})"
            expr = BitVectors.resize(BitVectors.bit(pred if kind == '$eq' else f'(not {pred})'), 1, width, False)
        elif kind == '$not':
            expr = f"(bvnot {resized('A', width, int(p['A_SIGNED'], 2) == 1)})"
        elif kind in ('$and', '$or', '$sub'):
            signed = int(p['A_SIGNED'], 2) == 1 and int(p['B_SIGNED'], 2) == 1
            op = {'$and': 'bvand', '$or': 'bvor', '$sub': 'bvsub'}[kind]
            expr = f"({op} {resized('A', width, signed)} {resized('B', width, signed)})"
        else:
            raise Unsupported('Unsupported cell '+kind)
        self.active.remove(name)
        self.macros[key] = f'(define-fun {key} () (_ BitVec {width}) {expr})'
        return key, width

    def symbol(self, typed):
        name = typed['symbol']
        if name not in self.module['netnames']:
            raise Unsupported('Slang symbol absent from Yosys: '+name)
        bits = self.module['netnames'][name]['bits']
        if len(bits) != typed['type']['width']:
            raise Unsupported('Slang/Yosys symbol width mismatch: '+name)
        return self.word(bits)


def prove(ast, netlist, output):
    adapter = RichAdapter(json.loads(ast.read_text()), 'spi_host_fsm').extract()
    model = BitVectors(adapter, procedural=True)
    reference = Netlist(json.loads(netlist.read_text())['modules']['spi_host_fsm'])
    checks = []
    for name, data in model.definition_sources.items():
        expected = model.term(data['rhs'])
        observed = reference.symbol(data['lhs'])
        checks.append({'symbol': data['lhs']['symbol'], 'definition': name,
                       'mismatch': f'(not (= {expected} {observed}))'})
    bindings = []
    for key, typed in model.variables.items():
        bindings.append(f'(assert (= {key} {reference.symbol(typed)}))')
    declarations = '\n'.join(f'(declare-fun b{bit} () (_ BitVec 1))' for bit in sorted(reference.primary) if isinstance(bit, int))
    declarations += '\n'+'\n'.join(f'(declare-fun {name} () (_ BitVec 1))' for name in reference.unknown_bits)
    declarations += '\n'+'\n'.join(f"(declare-fun {key} () (_ BitVec {value['type']['width']}))" for key, value in model.variables.items())
    header = '(set-logic QF_BV)\n(set-option :timeout 10000)\n'+declarations+'\n'+'\n'.join(reference.macros.values())+'\n'+'\n'.join(bindings)+'\n'
    # Check satisfiability first: inconsistent bindings cannot validate a model.
    queries = ['(check-sat)']
    queries += [f"(push)\n(assert {x['violation']})\n(check-sat)\n(pop)" for x in reference.onehot]
    queries += [f"(push)\n(assert {x['mismatch']})\n(check-sat)\n(pop)" for x in checks]
    output.mkdir(parents=True, exist_ok=False)
    (output/'ssa-vs-yosys.smt2').write_text(header+'\n'.join(queries)+'\n')
    proc = subprocess.run(['z3', str(output/'ssa-vs-yosys.smt2')], text=True, capture_output=True, timeout=180, check=True)
    (output/'z3.log').write_text(proc.stdout+proc.stderr)
    statuses = proc.stdout.splitlines()
    if len(statuses) != 1+len(reference.onehot)+len(checks) or statuses[0] != 'sat':
        raise AssertionError('Inconsistent proof environment or invalid Z3 result')
    for row, status in zip(reference.onehot+checks, statuses[1:]):
        row['z3'] = status
    result = {'status': 'pass' if all(x == 'unsat' for x in statuses[1:]) else 'unresolved_or_mismatch',
        'scope': 'Binary combinational equivalence, current FF Q and input bits unconstrained. No temporal assumptions.',
        'environment_satisfiable': True, 'pmux_onehot_checks': reference.onehot,
        'synthesis_dont_care_bits': len(reference.unknown_bits),
        'dont_care_policy': 'Fresh unconstrained binary bits, never replaced by zero; every proof must hold for all assignments',
        'definition_checks': [{k: v for k, v in row.items() if k != 'mismatch'} for row in checks],
        'used_netlist_cells': sorted(reference.used_cells), 'unsupported_procedures': model.unresolved}
    (output/'proof.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    import argparse
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--ast', type=Path, required=True)
    cli.add_argument('--netlist', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    data = prove(args.ast, args.netlist, args.output)
    print(json.dumps({'status': data['status'], 'definitions': len(data['definition_checks']),
                      'pmux': len(data['pmux_onehot_checks'])}))
