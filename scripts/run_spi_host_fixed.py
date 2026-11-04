#!/usr/bin/env python3
"""Replay JSON cycles on the pinned, unmodified OpenTitan SPI controller."""
import argparse
import json
from pathlib import Path
from coverage import load, summary
from run_midterm_fixed import ROOT, invoke, sha
from spi_host_fixture import check, validate_actions, write_vectors

BASE = ROOT/'third_party/opentitan_candidate/hw/ip'
SOURCE = BASE/'spi_host/rtl/spi_host_fsm.sv'
SOURCES = [BASE/p for p in ('prim/rtl/prim_util_pkg.sv', 'spi_host/rtl/spi_host_cmd_pkg.sv',
                            'prim_generic/rtl/prim_flop_en.sv', 'spi_host/rtl/spi_host_fsm.sv')]
FOLDER = ROOT/'examples/heldout_spi_host'
DRIVER = FOLDER/'verif/tb_spi_host_fixed.sv'
TOP = 'tb_spi_host_fixed'


def verify_source():
    pin = json.loads((FOLDER/'provenance.json').read_text())
    for name, digest in pin['sha256'].items():
        if sha(ROOT/name) != digest:
            raise AssertionError('Pinned source or specification changed: '+name)
    return pin


def compile_driver(output, *, mutation_source=None, simulator='verilator'):
    verify_source()
    build = output/'verilator-build'
    sources = SOURCES[:-1]+[mutation_source or SOURCE]
    if simulator == 'iverilog':
        binary = output/f'{TOP}.vvp'
        argv = ['iverilog', '-g2012', '-s', TOP, '-DSYNTHESIS', '-I', BASE/'prim/rtl',
                '-o', binary, *sources, DRIVER]
    elif simulator == 'verilator':
        binary = build/f'V{TOP}'
        argv = ['verilator', '--binary', '--timing', '--coverage-line', '--coverage-toggle',
            '--coverage-expr', '-Wno-fatal', '-Wno-TIMESCALEMOD', '--top-module', TOP,
            '--Mdir', build, '-j', '2', '-DSYNTHESIS', '-I'+str(BASE/'prim/rtl'), *sources, DRIVER]
    else:
        raise ValueError('Unknown simulator')
    seconds, _ = invoke(argv, output/'compile.log', timeout=300)
    return binary, argv, seconds


def simulate(binary, actions, output, name='batch', *, source=SOURCE, simulator='verilator'):
    validate_actions({'actions': actions}, len(actions), require_initial_reset=True)
    vectors, raw = output/f'{name}.vectors', output/f'{name}.dat'
    write_vectors(actions, vectors)
    command = (['vvp', binary] if simulator == 'iverilog' else [binary]) + [f'+VECTORS={vectors}']
    if simulator == 'verilator':
        command.append(f'+verilator+coverage+file+{raw}')
    seconds, log = invoke(command,
                          output/f'{name}.sim.log', timeout=60)
    if f'DRIVER_OK steps={len(actions)}' not in log:
        raise ValueError('Incomplete fixed-driver execution')
    # Checker runs after the complete batch, so failures cannot suppress coverage.
    checked = check(actions, log)
    points = load(raw, str(source.relative_to(ROOT)), include_descendants=True) if simulator == 'verilator' else []
    result = {'simulator': simulator, 'steps': len(actions), 'simulation_seconds': seconds, 'checker': checked,
              'coverage': summary(points) if points else None, 'raw_coverage': str(raw.relative_to(ROOT)) if points else None,
              'coverage_policy': 'All original top-file DUT counters, including initialization/reset. No TB or prim_flop counters. Fresh simulator per cumulative replay.' if points else 'No coverage instrumentation; public-trace cross-check only'}
    (output/f'{name}.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--actions', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--simulator', choices=('verilator', 'iverilog'), default='verilator')
    args = cli.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    actions = validate_actions(json.loads(args.actions.read_text()), 100000, require_initial_reset=True)
    binary, cmd, seconds = compile_driver(out, simulator=args.simulator)
    result = simulate(binary, actions, out, simulator=args.simulator)
    result.update(compile_seconds=seconds, compile_command=list(map(str, cmd)),
                  hashes={str(p.relative_to(ROOT)): sha(p) for p in [*SOURCES, DRIVER, Path(__file__), ROOT/'scripts/spi_host_fixture.py']})
    (out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
