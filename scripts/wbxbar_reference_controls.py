"""Private interface-level controls; never a functional golden checker."""
import argparse
import copy
import json
from pathlib import Path

from prepare_spi_core_checker_review import vector_unpack
from prepare_wbxbar_checker_role import PORTS
from prepare_wbxbar_reference_checker import BASE, OUTPUT_BASE, verify_scope
from run_midterm_fixed import sha
from wbxbar_checker_controls import empty_rows, settle, transfer


def swap_masters(rows):
    result = copy.deepcopy(rows)
    widths = {**PORTS['inputs'], **PORTS['outputs']}
    for row in result:
        for phase in ('pre', 'post'):
            for name, value in row[phase].items():
                if name.startswith(('i_m', 'o_m')) and value is not None:
                    width = widths[name] // 2
                    mask = (1 << width) - 1
                    row[phase][name] = ((value & mask) << width) | (value >> width)
    return result


def prepend_reset(rows, count=3):
    prefix = empty_rows(count)
    for row in prefix:
        row['pre']['i_reset'] = 1
    result = prefix + copy.deepcopy(rows)
    for cycle, row in enumerate(result):
        row['cycle'] = cycle
    return settle(result)


def build():
    verify_scope()
    packet = json.loads((BASE / 'design-patch-packet-v2/packet.json').read_text())
    traces = packet['synthetic_traces']
    originals = {name: [{k: v for k, v in row.items() if k != 'action'}
                        for row in vector_unpack(packed, traces['columns'])]
                 for name, packed in traces['values'].items()}
    design = json.loads((BASE / 'design-patch-v2-retry2/design-location-corrected.json').read_text())
    expected = {entry['name']: entry['expected_status'] for entry in design['control_assessments']}
    if set(expected) != set(originals) or len(originals) != 91:
        raise ValueError('Reviewed control name mismatch')
    inputs = copy.deepcopy(originals)
    accounts = [{'name': name, 'kind': 'reviewed_synthetic', 'expected': expected[name]}
                for name in originals]
    selected = ['positive/read', 'positive/write_mask', 'positive/concurrent',
                'positive/pipeline', 'positive/reset_inflight', 'negative/read_data',
                'negative/duplicate_response', 'negative/post_abort_corrupt_data',
                'ambiguity/later_data_corruption', 'ambiguity/inherently_indistinguishable',
                'new_dependency/overlapping_data_change',
                'new_epoch/two_aborts_then_identical_restart',
                'new_starvation/unaccepted_err', 'new_prefix/earlier_data_change',
                'new_payload/write_disabled_changes',
                'err_boundary/old_live_and_held_request', 'err_boundary/acceptance_edge',
                'err_boundary/cyc_withdrawal_edge']
    for name in selected:
        for transformation, function in [('swap_masters', swap_masters), ('prepend_reset3', prepend_reset)]:
            derived = 'heldback/' + transformation + '/' + name
            inputs[derived] = function(originals[name])
            accounts.append({'name': derived, 'kind': 'metamorphic', 'baseline': name,
                             'transformation': transformation, 'expected': expected[name],
                             'basis': 'Interface master renaming or extra initial reset rows; no arbitration-priority or absolute-cycle rule is in the reviewed contract. Expected global classification is inherited, subject to fresh control review.'})
    defaults = {'MAX_HYP': 4096, 'MAX_LIVE_PER_MASTER': 64, 'MAX_CANCELED_POOL': 256}
    limit_tests = {}
    for name, source, override in [
        ('hypotheses', 'ambiguity/inherently_indistinguishable', {'MAX_HYP': 1}),
        ('live_entries', 'positive/pipeline', {'MAX_LIVE_PER_MASTER': 1}),
        ('canceled_pool', 'multi_abort/third_identity', {'MAX_CANCELED_POOL': 1})]:
        limit_tests[name] = {'rows': copy.deepcopy(originals[source]), 'limits': {**defaults, **override},
                             'expected': 'unresolved', 'basis': 'Declared resource exhaustion; never arbitrary pruning or pass.'}
    rows = copy.deepcopy(limit_tests['hypotheses']['rows'])
    rows[20]['pre'].update(i_mcyc=1, o_mack=1, o_merr=1)
    limit_tests['association_free_fault_after_limit'] = {
        'rows': settle(rows), 'limits': {**defaults, 'MAX_HYP': 1},
        'expected': 'dut_violation', 'basis': 'ACK and ERR simultaneously asserted after history limit; direct pin checks must continue.'}
    for bad in (False, True):
        rows = copy.deepcopy(originals['ambiguity/inherently_indistinguishable'])
        tail = empty_rows(44)[len(rows):]
        rows.extend(tail)
        for cycle in (28, 29):
            rows[cycle]['pre']['i_reset'] = 1
        transfer(rows, accept=33, forward=35, response=36, returned=37, addr=7,
                 read_data=0x13579bdf)
        if bad:
            rows[37]['pre']['o_mdata'] ^= 1
        limit_tests['reset_then_' + ('bad_data' if bad else 'clean_work')] = {
            'rows': settle(rows), 'limits': {**defaults, 'MAX_HYP': 1},
            'expected': 'dut_violation' if bad else 'unresolved',
            'basis': 'Reset resumes association checking but does not erase earlier unresolved history-limit records.'}
    return inputs, accounts, limit_tests


def prepare(output):
    inputs, accounts, limits = build()
    output.mkdir(parents=True, exist_ok=False)
    for name, value in [('inputs.json', inputs), ('accounts.json', accounts), ('limit-tests.json', limits)]:
        (output / name).write_text(json.dumps(value, indent=2) + '\n')
    manifest = {'status': 'prepared_not_evaluated', 'normal_cases': len(inputs),
                'reviewed_cases': 91, 'heldback_metamorphic_cases': len(inputs)-91,
                'limit_cases': len(limits), 'author_packet_contains_these_full_traces': False,
                'control_role': 'GPT synthetic controls and transformations, not functional expected-value code.',
                'not_stimulus_or_target_data': True,
                'hashes': {str(p): sha(p) for p in [Path(__file__),
                    BASE / 'design-patch-packet-v2/packet.json',
                    BASE / 'design-patch-v2-retry2/design-location-corrected.json',
                    output / 'inputs.json', output / 'accounts.json', output / 'limit-tests.json']}}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.output.resolve()), indent=2))
