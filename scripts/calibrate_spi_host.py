#!/usr/bin/env python3
"""Private-to-calibration SPI sequences; never import into experimental prompts."""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT
from run_spi_host_fixed import compile_driver, simulate
from spi_host_fixture import action


def cases():
    reset = [action(rst_n=0), action(rst_n=0), action()]
    result = {}
    for speed in range(3):
        for cpha in range(2):
            for cpol in range(2):
                for read, write in ((1, 0), (0, 1), *(([(1, 1)]) if speed == 0 else [])):
                    a = action(speed=speed, cpha=cpha, cpol=cpol, read=read, write=write,
                               length=2, csid=1, clkdiv=1, lead=2, trail=2, idle=2)
                    result[f'mode_{speed}_{cpha}_{cpol}_{read}{write}'] = reset+[dict(a, valid=1)]+[a]*180
    result['stall_pause'] = reset+[action(valid=1, write=1, read=1, length=3)]+[
        action(tx_ready=int(not 10 <= i <= 25), rx_ready=int(not 28 <= i <= 45), enable=int(not 3 <= i <= 6))
        for i in range(120)]+[action()]*80
    for name, extra in [('software_abort', {'sw_reset': 1}), ('async_abort', {'rst_n': 0})]:
        result[name] = reset+[action(valid=1, write=1, read=1, length=3)]+[action()]*9+[
            action(**extra)]+[action()]*4+[action(valid=1, write=1)]+[action()]*50
    result['dummy'] = reset+[action(valid=1, length=4)]+[action()]*30
    result['keep_cs'] = reset+[action(valid=1, write=1, keep_cs=1)]+[action()]*30+[
        action(valid=1, read=1)]+[action()]*50
    result['full_cycle'] = reset+[action(valid=1, read=1, full_cycle=1, clkdiv=2)]+[action()]*100
    return result


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--simulator', choices=('verilator', 'iverilog'), default='verilator')
    args = cli.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    binary, cmd, seconds = compile_driver(out, simulator=args.simulator)
    results = {}
    for name, actions in cases().items():
        (out/f'{name}.actions.json').write_text(json.dumps({'actions': actions}, indent=2)+'\n')
        results[name] = simulate(binary, actions, out, name, simulator=args.simulator)
    seed = json.loads((ROOT/'examples/heldout_spi_host/seed.json').read_text())['actions']
    results['seed'] = simulate(binary, seed, out, 'seed', simulator=args.simulator)
    (out/'summary.json').write_text(json.dumps({'compile_seconds': seconds,
        'compile_command': list(map(str, cmd)), 'cases': results}, indent=2)+'\n')
    print(json.dumps({k: {'cycles': v['steps'], 'checker': v['checker']['verdict'],
        'failures': len(v['checker']['failures']), 'categories': v['checker']['distinct_defects'],
        'assumptions': v['checker']['assumption_violations']} for k, v in results.items()}, indent=2))


if __name__ == '__main__':
    main()
