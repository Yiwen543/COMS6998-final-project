#!/usr/bin/env python3
"""GPT-authored private event calibration; no checker generation or model prompts.

Public ready pins terminate held command offers. All probe/replay executions
are separately accounted; this helper is never imported by live stimulus runners.
"""
import argparse
import json
from pathlib import Path

from run_midterm_fixed import ROOT, sha
from run_spi_host_fixed import compile_driver, simulate, FOLDER, SOURCE, DRIVER
from spi_host_fixture import action, parse


def calibrate(output):
    output.mkdir(parents=True, exist_ok=False)
    build = output/'compile-verilator'
    build.mkdir()
    binary, cmd, seconds = compile_driver(build)
    ibuild = output/'compile-iverilog'
    ibuild.mkdir()
    ibinary, icmd, iseconds = compile_driver(ibuild, simulator='iverilog')
    seed = json.loads((FOLDER/'seed.json').read_text())['actions']
    records = []
    metadata = {'role': 'GPT stimulus/integration; Claude independently authors checker',
        'scope': 'Offline private reachability/calibration, never experimental stimulus',
        'dut_sha256': sha(SOURCE), 'driver_sha256': sha(DRIVER), 'generator_sha256': sha(Path(__file__)),
        'compilations': 2, 'compile_seconds': seconds+iseconds,
        'commands': [list(map(str, cmd)), list(map(str, icmd))]}

    def execute(actions, name, simulator='verilator', probe=False):
        folder = output/name
        folder.mkdir()
        (folder/'actions.json').write_text(json.dumps({'actions':actions},indent=2)+'\n')
        result = simulate(binary if simulator=='verilator' else ibinary, actions, folder,
                          simulator=simulator)
        rows = parse((folder/'batch.sim.log').read_text(), actions)
        (folder/'rows.json').write_text(json.dumps(rows, separators=(',',':'))+'\n')
        records.append({'name':name,'simulator':simulator,'probe':probe,'cycles':len(actions),
            'simulation_seconds':result['simulation_seconds'],
            'legacy_checker_verdict':result['checker']['verdict'],
            'legacy_checker_is_not_new_oracle':True})
        return rows

    probes = 0
    def offer(prefix, **fields):
        nonlocal probes
        probes += 1
        command = action(valid=1, **fields)
        actions = prefix+[dict(command) for _ in range(96)]
        rows = execute(actions, f'offer-probe-{probes}', probe=True)
        hit = next((r['cycle'] for r in rows[len(prefix):] if r['pre']['ready']), None)
        if hit is None:
            raise RuntimeError('No handshake in bounded calibration offer; retained as unresolved')
        return actions[:hit+1]

    candidates = {}
    for name, phases in [('tx_recovery',[action(tx_ready=0)]*24+[action()]*110),
                         ('rx_recovery',[action(rx_ready=0)]*24+[action()]*110),
                         ('tx_rx_recovery',[action(tx_ready=0)]*24+[action()]*14+
                                           [action(rx_ready=0)]*24+[action()]*110)]:
        candidates[name] = offer(list(seed), write=1, read=1, length=3)+[action()]*9+phases
    for kind in ('software','asynchronous'):
        prefix = offer(list(seed), write=1, read=1, length=7)+[action()]*9
        reset = action(sw_reset=1) if kind=='software' else action(rst_n=0)
        prefix += [reset]*2+[action()]*4
        candidates[kind+'_abort_restart'] = offer(prefix, write=1, read=1, length=1)+[action()]*100
    for kind, changes in [('csid', {'csid':1}),
                          ('configuration', {'cpol':1,'clkdiv':1,'idle':2,'lead':2,'trail':2})]:
        prefix = offer(list(seed), write=1, length=1, keep_cs=1)+[action()]*40
        candidates[kind+'_switch'] = offer(prefix, read=1, length=1, **changes)+[action()]*150
    for name, actions in candidates.items():
        assert len(actions)-len(seed) <= 384, name
        vr = execute(actions, name)
        ir = execute(actions, name+'-iverilog', 'iverilog')
        if vr != ir:
            raise AssertionError('Public simulator trace mismatch: '+name)
    metadata.update(executions=records, total_simulations=len(records),
        total_executed_cycles=sum(x['cycles'] for x in records),
        simulation_seconds=sum(x['simulation_seconds'] for x in records),
        candidate_cases=list(candidates), all_public_traces_agree=True,
        max_candidate_cycles=max(map(len,candidates.values())))
    (output/'summary.json').write_text(json.dumps(metadata, indent=2)+'\n')
    return metadata


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args()
    data=calibrate(args.output.resolve())
    print(json.dumps({k:v for k,v in data.items() if k not in ('executions','commands')},indent=2))
