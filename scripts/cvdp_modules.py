"""Reviewed adapters for three pinned CVDP input-context RTLs; not a general parser."""
import hashlib
import itertools
import json
from pathlib import Path
from predicates import ROOT

NAMES = ('barrel_shifter', 'caesar_cipher', 'universal_shift_register')
FIELDS = {
    'barrel_shifter': {'data_in': 255, 'shift_bits': 7, 'left_right': 1},
    'caesar_cipher': {'input_char': 255, 'key': 15},
    'universal_shift_register': {'rst': 1, 'mode_sel': 3, 'shift_dir': 1,
                                 'serial_in': 1, 'parallel_in': 255}}


def source(name):
    return f'examples/cvdp/{name}/rtl/{name}.sv'


def verify_source(name):
    folder = ROOT / 'examples/cvdp' / name
    provenance = json.loads((folder / 'provenance.json').read_text())
    for relative, expected in provenance['rtl_sha256'].items():
        if hashlib.sha256((folder / relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f'{name}: RTL changed; review this adapter before using it')
    return provenance


def vector(name, values):
    return dict(zip(FIELDS[name], values))


def initial(name):
    if name == 'barrel_shifter':
        return [vector(name, (0, 0, 0)), vector(name, (36, 1, 0))]
    if name == 'caesar_cipher':
        return [vector(name, (0, 0)), vector(name, (65, 0))]
    return [vector(name, (1, 0, 0, 0, 0)), vector(name, (0, 0, 0, 0, 0))]


def candidates(name):
    # Finite concrete domain for guard witnesses, NOT full sequential reachability.
    if name == 'barrel_shifter':
        values = itertools.product((0, 1, 36, 128, 255), range(8), range(2))
    elif name == 'caesar_cipher':
        values = itertools.product(range(256), (0, 1, 3, 15))
    else:
        values = itertools.product(range(2), range(4), range(2), range(2), (0, 1, 165, 255))
    return [vector(name, v) for v in values]


def expanded_suite(name):
    if name == 'barrel_shifter':
        return [vector(name, v) for v in itertools.product(range(256), range(8), range(2))]
    if name == 'caesar_cipher':
        return [vector(name, v) for v in itertools.product(range(256), range(16))]
    # Each operation begins from a reset and independently loaded state.
    # Covers all 256 prior register values, 4 modes, 2 directions, 2 serial inputs.
    result = []
    for prior, mode, direction, serial in itertools.product(range(256), range(4), range(2), range(2)):
        result.extend([vector(name, (1, 0, 0, 0, 0)),
                       vector(name, (0, 3, 0, 0, prior)),
                       vector(name, (0, mode, direction, serial, 255 - prior))])
    return result


def environment(name, v):
    if name == 'barrel_shifter':
        return {'left': v['left_right']}
    if name == 'caesar_cipher':
        c = v['input_char']
        return {'ge_A': c >= 65, 'ge_Z': c >= 90, 'le_a': c <= 97, 'ge_z': c >= 122}
    return {'reset': v['rst'], 'm0': bool(v['mode_sel'] & 1),
            'm1': bool(v['mode_sel'] & 2), 'left': v['shift_dir']}


def check(name, vectors, traces):
    if len(traces) != len(vectors):
        raise ValueError('Missing simulation trace rows')
    errors, examples, state = 0, [], 0
    for i, (v, actual) in enumerate(zip(vectors, traces)):
        if name == 'barrel_shifter':
            expected = [(v['data_in'] << v['shift_bits']) & 255 if v['left_right']
                        else v['data_in'] >> v['shift_bits']]
        elif name == 'caesar_cipher':
            c = v['input_char']
            base = 65 if 65 <= c <= 90 else 97 if 97 <= c <= 122 else None
            expected = [c if base is None else (c - base + v['key']) % 26 + base]
        else:
            if v['rst']:
                state = 0
            elif v['mode_sel'] == 1:
                state = (((state << 1) | v['serial_in']) & 255 if v['shift_dir']
                         else (state >> 1) | (v['serial_in'] << 7))
            elif v['mode_sel'] == 2:
                state = (((state << 1) | (state >> 7)) & 255 if v['shift_dir']
                         else (state >> 1) | ((state & 1) << 7))
            elif v['mode_sel'] == 3:
                state = v['parallel_in']
            expected = [state, (state >> 7) & 1 if v['shift_dir'] else state & 1]
        if actual != expected:
            errors += 1
            if len(examples) < 8:
                examples.append({'index': i, 'input': v, 'expected': expected, 'actual': actual})
    return {'checks': len(vectors), 'functional_errors': errors,
            'counterexamples': examples, 'scope': 'binary inputs; outputs sampled after settling/posedge, no off-edge reset conformance check'}


def targets(name):
    verify_source(name)
    # Source lines are pinned to the hashes above. Counter identities are reviewed
    # against Verilator 5.052; joins fail closed if a tool version maps differently.
    if name == 'barrel_shifter':
        rows = [('left_path', 9, 'branch', 'if', 'left'),
                ('right_path', 9, 'branch', 'else', '(not left)')]
        atoms = {'left': 'left_right == 1'}
    elif name == 'caesar_cipher':
        upper = '(and ge_A ge_Z)'
        lower = '(and le_a ge_z)'
        rows = [('upper_path', 11, 'line', 'elsif', upper),
                ('lower_path', 13, 'line', 'if', f'(and (not {upper}) {lower})'),
                ('passthrough_path', 13, 'line', 'else', f'(and (not {upper}) (not {lower}))')]
        atoms = {'ge_A': 'input_char >= 65', 'ge_Z': 'input_char >= 90',
                 'le_a': 'input_char <= 97', 'ge_z': 'input_char >= 122'}
    else:
        modes = ['(and (not m1) (not m0))', '(and (not m1) m0)',
                 '(and m1 (not m0))', '(and m1 m0)']
        active = lambda expr: f'(and (not reset) {expr})'
        rows = [('reset_path', 15, 'branch', 'if', 'reset'),
                ('active_path', 15, 'branch', 'else', '(not reset)'),
                ('hold', 20, 'line', 'case', active(modes[0])),
                ('shift_mode', 24, 'line', 'case', active(modes[1])),
                ('shift_right', 25, 'branch', 'if', active(f'(and {modes[1]} (not left))')),
                ('shift_left', 25, 'branch', 'else', active(f'(and {modes[1]} left)')),
                ('rotate_mode', 32, 'line', 'case', active(modes[2])),
                ('rotate_right', 33, 'branch', 'if', active(f'(and {modes[2]} (not left))')),
                ('rotate_left', 33, 'branch', 'else', active(f'(and {modes[2]} left)')),
                ('parallel_load', 40, 'line', 'case', active(modes[3])),
                ('case_default', 44, 'line', 'case', 'false'),
                ('serial_right', 50, 'branch', 'cond_then', '(not left)'),
                ('serial_left', 50, 'branch', 'cond_else', 'left')]
        atoms = {'reset': 'rst == 1', 'm0': 'mode_sel[0]', 'm1': 'mode_sel[1]',
                 'left': 'shift_dir == 1'}
    result = []
    for id_, line, kind, outcome, expr in rows:
        event = ('continuous' if name != 'universal_shift_register' or id_.startswith('serial_')
                 else 'posedge clk; sampled after settling')
        result.append({'id': id_, 'source': source(name), 'line': line,
                       'counter_type': kind, 'counter_outcome': outcome,
                       'compact': expr, 'expanded': expr, 'width': 1, 'logic': 'two_state',
                       'event': event, 'reset_context': 'no reset' if name != 'universal_shift_register'
                       else 'active high asynchronous reset; this driver checks settled posedge outputs',
                       'atom_definitions': atoms})
    return result
