#!/usr/bin/env python3
"""Single-fault negative controls on disposable copies; original DUT stays pinned."""
import argparse
import json
from pathlib import Path
from calibrate_spi_host import cases
from run_midterm_fixed import ROOT, sha
from run_spi_host_fixed import SOURCE, compile_driver, simulate, verify_source

MUTATIONS = {
    'lost_last_write': ("assign last_write_o      = (byte_cntr_early == 'h0) & wr_en_o & sr_wr_ready_i;",
                        "assign last_write_o = 1'b0;", 'mode_0_0_0_01', 'segment_last_flag'),
    'inverted_serial_clock': ('assign sck_o = sck_q;', 'assign sck_o = ~sck_q;',
                             'mode_0_0_0_01', 'asynchronous_reset'),
    'unmasked_write_stall': ('assign wr_en_o     = wr_en_internal & ~stall;',
                            'assign wr_en_o = wr_en_internal;', 'stall_pause', 'stall_controls_not_suppressed'),
}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output', type=Path, default=ROOT/'results/spi_host_preflight_20261104/negative_controls')
    args = cli.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    verify_source()
    original_hash = sha(SOURCE)
    text = SOURCE.read_text()
    records = []
    for name, (before, after, case, expected) in MUTATIONS.items():
        if text.count(before) != 1:
            raise AssertionError('Mutation must change exactly one named site')
        folder = out/name
        folder.mkdir()
        source = folder/'spi_host_fsm_mutant.sv'
        source.write_text(text.replace(before, after))
        binary, command, seconds = compile_driver(folder, mutation_source=source)
        result = simulate(binary, cases()[case], folder, source=source)
        detected = expected in result['checker']['distinct_defects']
        record = {'name': name, 'scope': 'single-fault negative control, never experimental RTL',
            'change': {'before': before, 'after': after}, 'source_sha256': sha(source),
            'calibration_case': case, 'expected_category': expected, 'detected': detected,
            'repeated_failures': len(result['checker']['failures']),
            'distinct_defects': result['checker']['distinct_defects'],
            'executed_cycles': result['steps'], 'compile_seconds': seconds,
            'simulation_seconds': result['simulation_seconds'], 'compile_command': list(map(str, command)),
            'raw_coverage_written': (folder/'batch.dat').exists()}
        records.append(record)
        (out/'summary.json').write_text(json.dumps({'original_source_sha256': original_hash,
            'controls': records, 'all_detected': all(r['detected'] for r in records)}, indent=2)+'\n')
        print(name, 'detected='+str(detected), flush=True)
    if sha(SOURCE) != original_hash:
        raise AssertionError('Original DUT changed')
    if not all(r['detected'] and r['raw_coverage_written'] for r in records):
        raise AssertionError('Negative control or coverage flush failed')


if __name__ == '__main__':
    main()
