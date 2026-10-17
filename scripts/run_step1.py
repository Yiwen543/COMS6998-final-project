#!/usr/bin/env python3
"""One measured coverage feedback iteration; no remote model calls."""
import argparse
import json
import os
import platform
import re
import subprocess
import time
from pathlib import Path
from coverage import load, summary, join
from predicates import ROOT, DUT, extract, witness
from eda_build import build_verilator


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def run(command, log, **kwargs):
    start = time.perf_counter()
    proc = subprocess.run([str(x) for x in command], cwd=kwargs.pop('cwd', ROOT),
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=180, **kwargs)
    log.write_bytes(proc.stdout)
    if proc.returncode:
        raise RuntimeError(f'Command failed ({proc.returncode}); see {log}')
    return time.perf_counter() - start, proc.stdout.decode('utf-8', errors='replace')


def result(text):
    m = re.search(r'RESULT checks=(\d+) functional_errors=(\d+) timing_errors=(\d+)', text)
    if not m: raise ValueError('Simulator did not produce a completed checker result')
    return dict(zip(('checks', 'functional_errors', 'timing_errors'), map(int, m.groups())))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results/step1')
    args = parser.parse_args()
    out = (ROOT / args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    targets = extract()
    write_json(out / 'predicates.json', targets)
    env = dict(os.environ, CARGO_HOME=str(ROOT / '.cache/cargo'))
    print('Building pinned egg engine and instrumented DUT...', flush=True)
    run(['cargo', 'build', '--locked', '--offline', '--manifest-path', 'egraph/Cargo.toml'],
        out / 'egg-build.log', env=env)
    proc = subprocess.run([str(ROOT / 'egraph/target/debug/rtl-predicate-egraph')],
                          input=json.dumps(targets), text=True, capture_output=True, check=True, timeout=15)
    graph = json.loads(proc.stdout)
    write_json(out / 'egraph.json', graph)
    binary, build_seconds = build_verilator(ROOT, out, run)
    measurements = []
    def simulate(name, mode, extra=()):
        coverage = out / f'{name}.dat'
        command = [binary, f'+MODE={mode}', '+COLLECT',
                   f'+verilator+coverage+file+{coverage}', *extra]
        elapsed, log = run(command, out / f'{name}.log')
        points = load(coverage)
        data = {'name': name, 'simulator': 'verilator', 'simulator_executions': 1,
                'wall_seconds': elapsed, **result(log), 'coverage': summary(points),
                'input_tokens': None, 'output_tokens': None, 'token_roi': None,
                'token_note': 'Hand-authored integration experiment; no API usage was measured.'}
        write_json(out / f'{name}-coverage.json', {'summary': summary(points), 'points': points})
        measurements.append(data)
        return points

    initial = simulate('initial', 0)
    feedback = join(targets, graph, initial)
    write_json(out / 'feedback.json', feedback)
    vectors = []
    for f in feedback:
        if f['uncovered']:
            stimulus = witness(f['representative'])
            if stimulus is None: raise ValueError(f'Unexpected unreachable target {f["id"]}')
            f['suggested_stimulus'] = {'reset': stimulus[0], 'req': stimulus[1], 'priority_override': stimulus[2]}
            if stimulus not in vectors: vectors.append(stimulus)
    # Independent spec-directed probes: conflicting masks, multi-bit override,
    # active grant -> reset between edges -> synchronous reset recovery.
    vectors.extend([(0, 255, 0), (0, 128, 3), (1, 255, 255), (0, 0, 0)])
    vector_file = out / 'targeted-vectors.txt'
    vector_file.write_text(''.join(f'{rst} {req:02x} {over:02x}\n' for rst, req, over in vectors))
    write_json(out / 'feedback.json', feedback)
    print(f'Refining from uncovered predicates with {len(vectors)} additional vectors...', flush=True)
    refined = simulate('refined', 1, [f'+VECTORS={os.path.relpath(vector_file, ROOT)}'])
    ceiling = simulate('exhaustive', 2)
    # Assert improvement using stable source/outcome identities, never E-class membership.
    def ids(points):
        return {(p['source'], p['line'], p['column'], p['type'], p['outcome']) for p in points if p['hits'] > 0}
    if not ids(initial) < ids(refined): raise AssertionError('Refinement did not add DUT coverage')
    if not all(f['hits'] > 0 for f in join(targets, graph, refined)):
        raise AssertionError('Some targeted priority paths remain uncovered')
    if measurements[0]['functional_errors'] or measurements[0]['timing_errors']:
        raise AssertionError('Small starting test unexpectedly failed')
    if not all(m['functional_errors'] > 0 and m['timing_errors'] > 0 for m in measurements[1:]):
        raise AssertionError('Expected both known specification violations')
    run(['verilator_coverage', '--write-info', str(out / 'exhaustive.info'),
         str(out / 'exhaustive.dat')], out / 'coverage-export.log')
    annotate = out / 'annotated'
    run(['verilator_coverage', '--annotate', str(annotate), '--annotate-min', '1',
         str(out / 'exhaustive.dat')], out / 'coverage-annotate.log')
    # A separate simulator checks portability and independently reproduces failures.
    run(['iverilog', '-g2012', '-s', 'tb_fixed_priority_arbiter', '-o',
         str(ROOT / 'build/arbiter.vvp'), str(DUT),
         'examples/arbiter/verif/tb_fixed_priority_arbiter.sv'], out / 'icarus-compile.log')
    elapsed, log = run(['vvp', str(ROOT / 'build/arbiter.vvp'), '+MODE=2', '+COLLECT'],
                       out / 'icarus.log')
    crosscheck = {'simulator': 'icarus', 'simulator_executions': 1,
                  'wall_seconds': elapsed, **result(log)}
    if any(crosscheck[k] != measurements[-1][k] for k in ('checks','functional_errors','timing_errors')):
        raise AssertionError('Simulators disagree on exhaustive check results')
    versions = {}
    for tool, flag in [('verilator','--version'),('iverilog','-V'),('yosys','-V'),('cargo','--version'),('rustc','--version')]:
        p = subprocess.run([tool, flag], text=True, capture_output=True, check=True)
        versions[tool] = p.stdout.splitlines()[0]
    # Exercise Yosys as a frontend; do not synthesize away source coverage locations.
    netlist_path = json.dumps(str(out / 'yosys-netlist.json'), ensure_ascii=False)
    run(['yosys', '-Q', '-T', '-p',
         f'read_verilog -sv {DUT.relative_to(ROOT)}; hierarchy -check -top fixed_priority_arbiter; proc; check; write_json {netlist_path}'],
         out / 'yosys.log')
    unreachable = [p for p in ceiling if p['hits'] == 0]
    report = {'fixture': json.loads((ROOT/'examples/arbiter/provenance.json').read_text()),
              'platform': platform.platform(), 'versions': versions,
              'verilator_build_seconds': build_seconds,
              'measurements': measurements, 'portability_crosscheck': crosscheck,
              'experiment_simulator_executions': 4,
              'normalization_pairs': len(targets), 'eclasses': len(graph['eclasses']),
              'refinement_policy': 'Deterministic Boolean witness enumeration, not an LLM ablation',
              'remaining_raw_uncovered_points': unreachable,
              'coverage_note': 'Raw DUT counters only. Line is Verilator block/elsif point coverage, not statement count; branch includes ternary outcomes. TB counters excluded. No waiver applied.',
              'limitations': ['Two-state Boolean adapter limited to the pinned arbiter hash',
                  'Last override ternary else is unreachable under nonzero override guard',
                  'No token measurements, Pass@1 estimate, or E-graph benefit claim',
                  'Not the CVDP cid012 or LLM4Cov evaluation harness']}
    write_json(out / 'summary.json', report)
    lines = ['# Step 1 measured integration result', '',
             '| Test | Checked cycles | Functional failures | Timing failures | Line points | Branch points | Toggle points |',
             '|---|---:|---:|---:|---|---|---|']
    for m in measurements:
        cols = [f'{m["coverage"][k]["covered"]}/{m["coverage"][k]["total"]}' for k in ['line','branch','toggle']]
        lines.append(f'| {m["name"]} | {m["checks"]} | {m["functional_errors"]} | {m["timing_errors"]} | ' + ' | '.join(cols) + ' |')
    lines += ['', 'Each row is one Verilator execution. The refined row includes the four starting cycles.',
              'Icarus independently reproduces the exhaustive checker counts (one additional execution).',
              'Failures detect the unchanged upstream DUT defects; they do not indicate a passing DUT.',
              'All percentages and raw uncovered points are in summary.json. No unreachable points are removed.',
              'This is a deterministic integration demonstration; token ROI and model comparisons remain unmeasured.', '']
    (out/'REPORT.md').write_text('\n'.join(lines))
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
