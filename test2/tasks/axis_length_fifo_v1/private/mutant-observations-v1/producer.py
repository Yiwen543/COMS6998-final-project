#!/usr/bin/env python3
"""New hidden single-site faults and measurements; labels await Claude truth."""
import argparse
import json
from pathlib import Path
from common import ROOT, BASE, dump, run, sha
import controller_prepare as task

TASK = BASE / 'tasks/axis_length_fifo_v1'


def nth(text, old, new, occurrence):
    parts = text.split(old)
    if len(parts) <= occurrence:
        raise ValueError('Mutation site not found')
    return old.join(parts[:occurrence]) + new + old.join(parts[occurrence:])


def section(text, marker, old, new):
    before, tail = text.split(marker, 1)
    if tail.count(old) != 1:
        raise ValueError('Mutation section is not unique')
    return before + marker + tail.replace(old, new, 1)


def mutations(source):
    definitions = [
        ('boundary_guard', lambda s: nth(s, 'if (long_counter_reg <= word_cnt)', 'if (long_counter_reg < word_cnt)', 2)),
        ('boundary_guard', lambda s: nth(s, 'if (short_counter_reg > word_cnt)', 'if (short_counter_reg >= word_cnt)', 2)),
        ('boundary_guard', lambda s: s.replace('if (short_counter_reg <= KEEP_WIDTH)', 'if (short_counter_reg < KEEP_WIDTH)', 1)),
        ('boundary_guard', lambda s: section(s, 'STATE_TRUNCATE: begin', 'if (s_axis_tlast) begin', 'if (!s_axis_tlast) begin')),
        ('handshake_reset', lambda s: s.replace('status_valid_reg && !status_ready', 'status_valid_reg && status_ready', 1)),
        ('handshake_reset', lambda s: section(s, '// output datapath logic', 'if (m_axis_tready_int_reg) begin', 'if (m_axis_tready) begin')),
        ('handshake_reset', lambda s: s.replace("m_axis_tvalid_reg <= 1'b0;", 'm_axis_tvalid_reg <= m_axis_tvalid_reg;', 1)),
        ('handshake_reset', lambda s: s.replace("temp_m_axis_tvalid_next = 1'b0;", 'temp_m_axis_tvalid_next = temp_m_axis_tvalid_reg;', 1)),
        ('payload_status', lambda s: section(s, 'STATE_PAD: begin', "m_axis_tdata_int = {DATA_WIDTH{1'b0}};", "m_axis_tdata_int = {DATA_WIDTH{1'b1}};")),
        ('payload_status', lambda s: s.replace('m_axis_tdata_reg <= m_axis_tdata_int;', "m_axis_tdata_reg <= m_axis_tdata_int ^ 8'h01;", 1)),
        ('payload_status', lambda s: section(s, 'STATE_TRUNCATE: begin', 'status_frame_original_length_next = frame_ptr_reg+word_cnt;', 'status_frame_original_length_next = frame_ptr_reg+word_cnt+1;')),
        ('payload_status', lambda s: nth(s, 'status_frame_length_next = frame_ptr_reg+word_cnt;', 'status_frame_length_next = frame_ptr_reg+word_cnt+1;', 2))]
    result = []
    for i, (stratum, change) in enumerate(definitions, 1):
        modified = change(source)
        if len(modified.splitlines()) != len(source.splitlines()):
            raise ValueError('Mutation changed line identity')
        changed = [n for n, (a, b) in enumerate(zip(source.splitlines(), modified.splitlines()), 1) if a != b]
        if len(changed) != 1:
            raise ValueError('Expected one changed source line')
        result.append((f'M{i:02d}', stratum, modified, changed[0]))
    return result


def prepare(measure=False):
    task.configure(TASK)
    source = TASK / 'public/rtl/axis_frame_length_adjust.v'
    folder = TASK / 'private/mutants-v1'
    folder.mkdir(exist_ok=False)
    catalog = []
    for mid, stratum, modified, line in mutations(source.read_text()):
        path = folder / (mid+'.v')
        path.write_text(modified)
        catalog.append({'id': mid, 'stratum': stratum, 'changed_lines': [line],
                        'source': str(path.relative_to(ROOT)), 'sha256': sha(path),
                        'eligibility': 'PENDING_INDEPENDENT_REFERENCE'})
    dump(TASK / 'private/mutant-catalog-v1.json', {'faults': catalog,
         'source_sha256': sha(source), 'generator_sha256': sha(Path(__file__)),
         'strata_frozen_before_candidate_outcomes': True, 'unobservable_and_unknown_retained': True})
    if not measure:
        return
    originals = list(task.SOURCES)
    results = []
    for fault in catalog:
        task.SOURCES = [ROOT / fault['source'] if p == source else p for p in originals]
        for sim in ('iverilog', 'verilator'):
            out = TASK / 'private/mutant-observations-v1' / fault['id'] / sim
            out.mkdir(parents=True, exist_ok=False)
            binary = out / ('obj/Vtb_natural_inventory' if sim == 'verilator' else 'driver.vvp')
            cmd = (['verilator', '--binary', '--timing', '--coverage-line', '--coverage-toggle', '--coverage-expr',
                    '-Wno-fatal', '--top-module', 'tb_natural_inventory', '--Mdir', binary.parent, '-j', '2']
                   if sim == 'verilator' else ['iverilog', '-g2012', '-s', 'tb_natural_inventory', '-o', binary])
            info = run(cmd + task.SOURCES + [TASK / 'public/driver.sv'], out / 'compile.log', 180)
            dump(out / 'compile.json', info)
            if info['status'] != 'complete':
                results.append({'fault': fault['id'], 'simulator': sim, 'compile_status': info['status']})
                continue
            for path in sorted((TASK / 'private/final').glob('*.json')):
                actions = json.loads(path.read_text())['actions']
                task.simulate(sim, binary, actions, out / path.stem)
            results.append({'fault': fault['id'], 'simulator': sim, 'compile_status': 'complete'})
        print('Measured hidden fault', fault['id'], flush=True)
    task.SOURCES = originals
    dump(TASK / 'private/mutant-measurements-v1.json', {'results': results,
         'reference_status': 'PENDING_CLAUDE', 'candidate_calls': 0})


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--measure', action='store_true')
    a = p.parse_args()
    prepare(a.measure)
