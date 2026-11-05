#!/usr/bin/env python3
"""Fixed controller inputs, transport observations and author packet; no oracle."""
import argparse
import json
from pathlib import Path
import random
from common import ROOT, BASE, dump, run, sha
from inventory_natural_coverage import load_all

TASK = BASE / 'tasks/axis_length_v1'
PUBLIC = TASK / 'public'
QUAL = TASK / 'qualification/typed-v4'
SOURCES = [PUBLIC / 'rtl/axis_frame_length_adjust.v', PUBLIC / 'task_top_v3.sv']
INPUTS = ['rst', 's_valid', 's_data', 's_last', 'm_ready', 'h_ready']
OUTPUTS = ['s_ready', 'm_data', 'm_valid', 'm_last', 'h_valid', 'h_pad',
           'h_truncate', 'h_length', 'h_original_length']
FIELDS = ['reset', 'offer', 'data', 'last', 'data_ready', 'status_ready']


def action(**values):
    return {**dict(reset=0, offer=0, data=0, last=0, data_ready=1, status_ready=1), **values}


def sequence(lengths, body_cycles, tail, seed, pressure=False, reset_at=None):
    rng = random.Random(seed)
    offers = [(rng.randrange(256), int(i == length-1)) for length in lengths for i in range(length)]
    result = [action(reset=1), action(reset=1)] + [action() for _ in range(4)]
    for i in range(body_cycles):
        a = action()
        if i < len(offers):
            a.update(offer=1, data=offers[i][0], last=offers[i][1])
        if pressure:
            a.update(data_ready=int(i % 7 not in (1, 2, 3)), status_ready=int(i % 11 not in (2, 3, 4, 5)))
        if reset_at is not None and i == reset_at:
            a = action(reset=1)
        result.append(a)
    return result + [action() for _ in range(tail)]


def datasets():
    dev = {'basic': sequence([4, 6], 10, 32, 699810),
           'boundary_pressure': sequence([1, 4, 8, 10], 26, 32, 699811, True),
           'reset_reuse': sequence([8, 1, 7, 4], 26, 32, 699812, True, 7)}
    final = {f'heldout_{i:02d}': sequence(lengths, 64, 128, 699900+i, True, reset)
             for i, (lengths, reset) in enumerate([
                 ([1, 3, 4, 8, 9, 12], None), ([12, 1, 8, 4, 2], None),
                 ([4, 8, 12, 3, 5], 3), ([8, 12, 1, 4, 7], 15),
                 ([2, 10, 4, 8, 1], 26), ([1, 12, 3, 9, 8], None)], 1)}
    return dev, final


DRIVER = r'''`timescale 1ns/1ps
module tb_natural_inventory;
reg clk=0,rst=0,s_valid=0,s_last=0,m_ready=1,h_ready=1;
reg [7:0] s_data=0;
wire s_ready,m_valid,m_last,h_valid,h_pad,h_truncate;
wire [7:0] m_data;
wire [15:0] h_length,h_original_length;
frame_task dut(.*);
integer fd,n,cycle=0,head=0,tail=0,take,r,o,d,l,m,h;
reg [7:0] data_q[0:511];reg last_q[0:511];
string path;
initial begin
 if(!$value$plusargs("VECTORS=%s",path)) $fatal(1,"missing vectors");
 fd=$fopen(path,"r");if(!fd) $fatal(1,"missing file");
 while(!$feof(fd)) begin
  n=$fscanf(fd,"%d %d %d %d %d %d",r,o,d,l,m,h);
  if(n==6) begin
   if(cycle>=512) $fatal(1,"cycle cap");
   rst=r;m_ready=m;h_ready=h;
   if(rst) begin head=0;tail=0;end
   else if(o) begin data_q[tail]=d;last_q[tail]=l;tail=tail+1;end
   s_valid=(!rst && head<tail);s_data=s_valid?data_q[head]:0;s_last=s_valid?last_q[head]:0;
   #4;take=(!rst && s_valid && s_ready);
   $display("PRE %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle,rst,s_valid,s_data,s_last,m_ready,h_ready,s_ready,m_data,m_valid,m_last,h_valid,h_pad,h_truncate,h_length,h_original_length);
   #1;clk=1;#4;
   $display("POST %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle,s_ready,m_data,m_valid,m_last,h_valid,h_pad,h_truncate,h_length,h_original_length);
   #1;clk=0;if(take) head=head+1;
   $display("QUEUE %0d %0d %0d",cycle,head,tail);cycle=cycle+1;
  end else if(!$feof(fd)) $fatal(1,"malformed vector");
 end
 $display("DRIVER_COMPLETE %0d",cycle);$finish;
end
endmodule
'''


def parse(log, actions):
    rows, queues = {}, {}
    def number(v):
        return -1 if any(x in v.lower() for x in 'xz') else int(v)
    for line in log.splitlines():
        fields = line.split()
        if not fields or fields[0] not in ('PRE', 'POST', 'QUEUE'):
            continue
        label, cycle = fields[0], int(fields[1])
        values = [number(x) for x in fields[2:]]
        if label == 'QUEUE':
            queues[cycle] = values
            continue
        keys = INPUTS + OUTPUTS if label == 'PRE' else OUTPUTS
        if len(values) != len(keys):
            raise ValueError('Observation width mismatch')
        row = rows.setdefault(cycle, {'cycle': cycle})
        if label == 'PRE':
            row['inputs'] = dict(zip(INPUTS, values[:len(INPUTS)]))
            values = values[len(INPUTS):]
        row[label.lower()] = dict(zip(OUTPUTS, values))
    if list(rows) != list(range(len(actions))) or len(queues) != len(actions):
        raise ValueError('Incomplete fixed observations')
    pending = []
    for i, a in enumerate(actions):
        if a['reset']:
            pending = []
        elif a['offer']:
            pending.append((a['data'], a['last']))
        expected = pending[0] if pending else (0, 0)
        inp = rows[i]['inputs']
        if inp != dict(rst=a['reset'], s_valid=int(bool(pending) and not a['reset']),
                       s_data=expected[0], s_last=expected[1],
                       m_ready=a['data_ready'], h_ready=a['status_ready']):
            raise ValueError('Input transport mismatch')
        if pending and rows[i]['pre']['s_ready'] == 1:
            pending.pop(0)
        head, tail = queues[i]
        if tail-head != len(pending):
            raise ValueError('Queue transport ledger mismatch')
    return list(rows.values()), len(pending)


def normalize(rows):
    result = []
    for row in rows:
        r = dict(cycle=row['cycle'], inputs=row['inputs'])
        for phase in ('pre', 'post'):
            v = row[phase]
            r[phase] = None if row['cycle'] == 0 and phase == 'pre' else {
                k: (value if k in ('s_ready', 'm_valid', 'h_valid') or
                    v['h_valid' if k.startswith('h_') else 'm_valid'] else None)
                for k, value in v.items()}
        result.append(r)
    return result


def simulate(sim, binary, actions, out):
    out.mkdir(parents=True, exist_ok=False)
    (out / 'vectors.txt').write_text(''.join(' '.join(str(a[k]) for k in FIELDS)+'\n' for a in actions))
    cmd = ([binary] if sim == 'verilator' else ['vvp', binary]) + [f'+VECTORS={out/"vectors.txt"}']
    if sim == 'verilator':
        cmd.append(f'+verilator+coverage+file+{out/"coverage.dat"}')
    info = run(cmd, out / 'simulation.log', 15)
    log = (out / 'simulation.log').read_text()
    if info['status'] != 'complete' or f'DRIVER_COMPLETE {len(actions)}' not in log:
        raise RuntimeError('Incomplete simulator execution')
    rows, pending = parse(log, actions)
    dump(out / 'rows.json', rows)
    info.update(cycles=len(rows), pending_input_bytes=pending, reference_verdict='PENDING_CLAUDE')
    dump(out / 'execution.json', info)
    if sim == 'verilator':
        points = load_all(out / 'coverage.dat', [str(p.relative_to(ROOT)) for p in SOURCES])
        dump(out / 'raw-points.json', points)
    return rows


def author_packet(out):
    out.mkdir(parents=True, exist_ok=False)
    payload = {'specification': (PUBLIC / 'specification.md').read_text(),
               'observer_contract': (PUBLIC / 'observer_contract.md').read_text()}
    instructions = '''Write an independent pure Python reference checker from only this specification/interface.
No tools, implementation, mutant sources, held-out trajectories, candidate monitor or model rankings are supplied.
Return JSON only with checker_source, properties, contract_markdown, selftest_source.
checker_source must define check_rows(rows, require_drained=False) with the documented result schema.
Import only collections, copy or math. No file/network/process access, introspection or dunder attributes.
selftest_source must define run(checker_module), returning a dict of boolean test results and never raising on expected invalid input.
Include positive controls and deliberately wrong payload/status/stability/reset cases, partial-stream and unknown/malformed controls.
Do not use DUT flags/state as expected contents. Public valid/ready defines transfers, not expected payload.
Support known input prefixes before end-of-input frame; independent ordered status/data channels; reset epochs.
Preserve earlier failures in the presence of unknowns. Do not mistake finite controls for proof.
If the contract is ambiguous, retain it as a blocking scope finding in contract_markdown instead of inventing behavior.
PACKET:\n'''
    text = instructions + json.dumps(payload, separators=(',', ':'), sort_keys=True)
    (out / 'prompt.txt').write_text(text)
    dump(out / 'manifest.json', {'prompt_sha256': sha(out / 'prompt.txt'),
         'allowed_files': ['specification.md', 'observer_contract.md'],
         'source_sha256': {k: sha(PUBLIC / k) for k in ('specification.md', 'observer_contract.md')},
         'excluded': ['RTL', 'mutants', 'evaluation trajectories', 'semantic proofs', 'candidate artifacts', 'skills']})


def prepare(out):
    if out.exists():
        raise FileExistsError('Refusing to overwrite measurements')
    cfg = json.loads((BASE / 'configs/controller_qualification_v4.json').read_text())
    for p, h in cfg['candidates'][0]['source_hashes'].items():
        if sha(ROOT / p) != h:
            raise ValueError('Registered source changed')
    out.mkdir(parents=True)
    driver = PUBLIC / 'driver.sv'
    if driver.exists() and driver.read_text() != DRIVER:
        raise ValueError('Existing driver differs')
    driver.write_text(DRIVER)
    dev, final = datasets()
    for split, data in [('development', dev), ('final', final)]:
        folder = PUBLIC / 'development' if split == 'development' else TASK / 'private/final'
        folder.mkdir(exist_ok=False)
        for name, actions in data.items():
            dump(folder / (name+'.json'), {'actions': actions, 'require_drained': True})
    files = SOURCES + [driver, PUBLIC / 'specification.md', PUBLIC / 'observer_contract.md']
    files += list((PUBLIC / 'development').glob('*.json')) + list((TASK / 'private/final').glob('*.json'))
    dump(TASK / 'input-manifest-v1.json', {'status': 'fixed_inputs_before_measurements_reference_pending',
         'source_registration_sha256': sha(BASE / 'configs/controller_qualification_v4.json'),
         'files': {str(p.relative_to(ROOT)): sha(p) for p in files},
         'generator_sha256': sha(Path(__file__)), 'provider_seed': None,
         'local_dataset_seeds': [699810, 699811, 699812] + list(range(699901, 699907)),
         'candidate_calls_allowed': False})
    builds = {}
    all_rows = {}
    for sim in ('iverilog', 'verilator'):
        build = out / sim
        build.mkdir()
        binary = build / ('obj/Vtb_natural_inventory' if sim == 'verilator' else 'driver.vvp')
        cmd = (['verilator', '--binary', '--timing', '--coverage-line', '--coverage-toggle', '--coverage-expr',
                '-Wno-fatal', '--top-module', 'tb_natural_inventory', '--Mdir', binary.parent, '-j', '2']
               if sim == 'verilator' else ['iverilog', '-g2012', '-s', 'tb_natural_inventory', '-o', binary])
        info = run(cmd + SOURCES + [driver], build / 'compile.log', 180)
        dump(build / 'compile.json', info)
        if info['status'] != 'complete':
            raise RuntimeError('Controller compile failed: ' + sim)
        builds[sim] = info
        for split, data in [('development', dev), ('final', final)]:
            for name, actions in data.items():
                # Held-out observations remain private; no candidate packet opens them.
                dest = build / name if split == 'development' else TASK / 'private/observations' / sim / name
                all_rows[sim, name] = simulate(sim, binary, actions, dest)
    agrees = {name: normalize(all_rows['iverilog', name]) == normalize(all_rows['verilator', name])
              for name in list(dev) + list(final)}
    dump(out / 'summary.json', {'status': 'measurements_complete_reference_pending', 'dual_simulator_agreement': agrees,
         'compilations': builds, 'new_simulations': 2*(len(dev)+len(final)),
         'cycles': 2*sum(map(len, list(dev.values())+list(final.values()))), 'model_calls': 0,
         'reference_verdicts': 'PENDING_CLAUDE', 'live_allowed': False})
    author_packet(TASK / 'reference/author-packet-v1')
    print((out / 'summary.json').read_text())


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    prepare(args.output.resolve())
