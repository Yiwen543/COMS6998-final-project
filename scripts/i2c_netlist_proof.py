"""I2C extension of the frozen SPI cell reference, following Yosys simlib.v.

Binary combinational checking only; no sequential invariants are assumed.
"""
from spi_netlist_proof import Netlist
from spi_semantic_v2 import BitVectors, Unsupported, stable


class I2CBitVectors(BitVectors):
    def term(self, node):
        if node['kind'] == 'ElementSelect' and node['selector']['kind'] != 'constant':
            v, s = node['value'], node['selector']
            # Explicit pinned [7:0] port layout; no inference for ascending ranges.
            if v.get('symbol') != 'fmt_byte_i' or v['type']['width'] != 8 or s['type']['width'] != 3 or s['type']['signed'] or node['type']['width'] != 1:
                raise Unsupported('Unproved dynamic index range/layout')
            word, index = self.term(v), self.term(s)
            return f'((_ extract 0 0) (bvlshr {word} ((_ zero_extend 5) {index})))'
        return super().term(node)


class I2CNetlist(Netlist):
    def cell(self, name):
        node = self.module['cells'][name]
        kind = node['type']
        if kind not in ('$add', '$gt', '$bmux'):
            return super().cell(name)
        c, p = node['connections'], node['parameters']
        width = len(c['Y'])
        key = 'n_' + stable(name)
        if key in self.macros:
            return key, width
        if name in self.active:
            raise Unsupported('Combinational netlist cycle')
        self.active.add(name)
        self.used_cells.add(name)
        if kind == '$bmux':
            sw = len(c['S'])
            if len(c['A']) != width * 2**sw or int(p['WIDTH'], 2) != width or int(p['S_WIDTH'], 2) != sw:
                raise Unsupported('Malformed binary mux widths')
            expr = self.word(c['A'][:width])
            if sw:
                selector = self.word(c['S'])
                for i in range(1, 2**sw):
                    data = self.word(c['A'][i*width:(i+1)*width])
                    expr = f'(ite (= {selector} {BitVectors.literal(i, sw)}) {data} {expr})'
        else:
            signed = bool(int(p['A_SIGNED'], 2) and int(p['B_SIGNED'], 2))
            size = width if kind == '$add' else max(len(c['A']), len(c['B']))
            a, b = [BitVectors.resize(self.word(c[x]), len(c[x]), size, signed) for x in ('A','B')]
            if kind == '$add':
                expr = f'(bvadd {a} {b})'
            else:
                op = 'bvsgt' if signed else 'bvugt'
                expr = BitVectors.resize(BitVectors.bit(f'({op} {a} {b})'), 1, width, False)
        self.active.remove(name)
        self.macros[key] = f'(define-fun {key} () (_ BitVec {width}) {expr})'
        return key, width


import json
import subprocess
from pathlib import Path
from spi_semantic_v2 import RichAdapter

def prove(ast, netlist, output):
    adapter = RichAdapter(json.loads(ast.read_text()), 'i2c_controller_fsm').extract()
    model = I2CBitVectors(adapter, procedural=True)
    reference = I2CNetlist(json.loads(netlist.read_text())['modules']['i2c_controller_fsm'])
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
