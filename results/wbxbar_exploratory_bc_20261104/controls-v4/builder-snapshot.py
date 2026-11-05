"""Private specification-level hand traces and single-fault controls.

Constructed independently of Claude source and DUT traces. Not a golden model,
not experimental stimulus, not source-target evidence. No DUT/internal state used.
"""
import argparse
import copy
import json
from pathlib import Path
from prepare_wbxbar_checker_role import PORTS
from run_midterm_fixed import sha


def empty_rows(count=24):
    rows = []
    for cycle in range(count):
        pre = dict.fromkeys(list(PORTS['inputs']) + list(PORTS['outputs']), 0)
        pre['i_reset'] = int(cycle < 2)
        rows.append({'cycle': cycle, 'pre': pre, 'post': dict.fromkeys(PORTS['outputs'], 0)})
    return rows


def put(rows, cycle, port, number, width, value):
    mask = ((1 << width) - 1) << (number * width)
    rows[cycle]['pre'][port] = (rows[cycle]['pre'][port] & ~mask) | (value << (number * width))


def settle(rows):
    # Post(k) is the registered output presented before edge(k+1). This is a
    # legal chosen timing trace, not a claim about the implementation's latency.
    for i, row in enumerate(rows):
        following = rows[i+1]['pre'] if i+1 < len(rows) else dict.fromkeys(PORTS['outputs'], 0)
        row['post'] = {k: following[k] for k in PORTS['outputs']}
    return rows


def transfer(rows, master=0, slave=0, accept=8, forward=10, response=11,
             returned=12, addr=3, data=0x12345678, read_data=0xabcdef12, we=0, sel=15, error=False):
    for cycle in range(accept, returned+1): put(rows, cycle, 'i_mcyc', master, 1, 1)
    for port, width, value in [('i_mstb',1,1),('i_mwe',1,we),('i_maddr',8,addr),('i_mdata',32,data),('i_msel',4,sel)]:
        put(rows, accept, port, master, width, value)
    if slave is not None:
        for cycle in range(forward, returned+1): put(rows, cycle, 'o_scyc', slave, 1, 1)
        for port, width, value in [('o_sstb',1,1),('o_swe',1,we),('o_saddr',8,addr),('o_sdata',32,data),('o_ssel',4,sel)]:
            put(rows, forward, port, slave, width, value)
        put(rows, response, 'i_serr' if error else 'i_sack', slave, 1, 1)
        put(rows, response, 'i_sdata', slave, 32, read_data)
    put(rows, returned, 'o_merr' if error else 'o_mack', master, 1, 1)
    put(rows, returned, 'o_mdata', master, 32, read_data)
    return rows


def controls():
    traces, manifest = {}, []
    def add(name, rows, kind, obligation, base=None):
        traces[name] = settle(rows)
        manifest.append({'name': name, 'kind': kind, 'obligation': obligation, 'baseline': base})
    add('positive/read', transfer(empty_rows()), 'positive', 'Read response/payload conservation')
    add('positive/write_mask', transfer(empty_rows(), we=1, sel=5), 'positive', 'Write payload and byte enables')
    add('positive/slave_error', transfer(empty_rows(), error=True), 'positive', 'Slave ERR propagation, not a successful read')
    add('positive/unmapped', transfer(empty_rows(), slave=None, addr=0x20, error=True), 'positive', 'Documented unmapped-address error without slave request')
    rows = transfer(empty_rows())
    transfer(rows, master=1, slave=1, accept=9, forward=11, response=12, returned=13, addr=0x14, read_data=0x55aa6600)
    add('positive/concurrent', rows, 'positive', 'Two different destinations and response owners')
    rows = transfer(empty_rows())
    transfer(rows, accept=9, forward=11, response=12, returned=13, addr=4, read_data=0x55667788)
    add('positive/pipeline', rows, 'positive', 'Consecutive accepts, slave accept/response overlap, ACK while STB is low')
    rows = transfer(empty_rows())
    transfer(rows, accept=12, forward=14, response=15, returned=16, addr=5, read_data=0x44332211)
    add('positive/accept_and_return', rows, 'positive', 'Master acceptance and earlier response on the same edge')
    rows = transfer(empty_rows(), master=1, slave=1, addr=0x12)
    add('positive/master1', rows, 'positive', 'Upper public packed port slices')
    rows = transfer(empty_rows())
    rows[15]['pre']['i_reset'] = 1
    rows[16]['pre']['i_reset'] = 1
    transfer(rows, accept=18, forward=20, response=21, returned=22, addr=6, read_data=0x11223344)
    add('positive/reset_then_new', rows, 'positive', 'New transaction after completed work and synchronous reset')
    rows = transfer(empty_rows())
    for row in rows[11:]:
        row['pre'] = dict.fromkeys(list(PORTS['inputs']) + list(PORTS['outputs']), 0)
    rows[11]['pre'].update(i_reset=1, o_scyc=1)
    rows[12]['pre']['i_reset'] = 1
    transfer(rows, accept=16, forward=18, response=19, returned=20, addr=6, read_data=0x10203040)
    add('positive/reset_inflight', rows, 'positive', 'Reset cancels outstanding work; new epoch completes independently')
    def mutate(name, base, cycle, port, value, obligation):
        rows = copy.deepcopy(traces[base]); rows[cycle]['pre'][port] = value
        add('negative/' + name, rows, 'single_fault', obligation, base)
    mutate('read_data', 'positive/read', 12, 'o_mdata', 0xabcdef13, 'Wrong returned read data')
    mutate('write_data', 'positive/write_mask', 10, 'o_sdata', 0x12345679, 'Wrong forwarded write payload')
    mutate('write_mask', 'positive/write_mask', 10, 'o_ssel', 15, 'Wrong forwarded byte mask')
    mutate('address', 'positive/read', 10, 'o_saddr', 4, 'Wrong forwarded address')
    mutate('direction', 'positive/read', 10, 'o_swe', 1, 'Read changed to write')
    rows = copy.deepcopy(traces['positive/read'])
    rows[10]['pre']['o_sstb'] = 0
    rows[11]['pre']['i_sack'] = 0  # Environment does not acknowledge a request never forwarded.
    add('negative/missing_forward', rows, 'single_fault', 'Fabricated master completion without forwarding or slave response', 'positive/read')
    mutate('wrong_owner', 'positive/concurrent', 12, 'o_mack', 2, 'Response delivered to wrong master')
    rows = copy.deepcopy(traces['positive/read'])
    put(rows, 13, 'i_mcyc', 0, 1, 1);put(rows, 13, 'o_mack', 0, 1, 1)
    add('negative/duplicate_response', rows, 'single_fault', 'No response without outstanding accepted work', 'positive/read')
    rows = copy.deepcopy(traces['positive/slave_error'])
    rows[12]['pre']['o_merr'] = 0; rows[12]['pre']['o_mack'] = 1
    add('negative/error_as_success', rows, 'single_fault', 'Slave error cannot become success', 'positive/slave_error')
    mutate('stale_after_reset', 'positive/reset_inflight', 14, 'o_mack', 1, 'Stale response in a reset-cleared epoch')
    mutate('stale_into_new_epoch', 'positive/reset_inflight', 16, 'o_mack', 1, 'Premature completion of new accepted work before forwarding/response, after reset')
    rows = empty_rows()
    rows[8]['pre'].update(i_mcyc=1, i_mstb=1, i_maddr=3, i_msel=15)
    rows[9]['pre'].update(i_mcyc=1, o_merr=1)
    add('negative/early_unexplained_error', rows, 'single_fault',
        'Mapped request fails one cycle after first activity without slave ERR or elapsed OPT_TIMEOUT=16; requires independent review of timeout applicability', 'positive/read')
    rows = copy.deepcopy(traces['positive/read'])
    rows[12]['pre']['o_mack'] = 0
    for row in rows[13:]:row['pre']['i_mcyc'] = 1  # Remain pending; do not silently abort.
    add('incomplete/missing_return', rows, 'incomplete', 'No complete/scoped pass with unretired work; no invented liveness deadline', 'positive/read')
    rows = copy.deepcopy(traces['positive/read'][:12])
    add('incomplete/truncated', rows, 'incomplete', 'Pending response at end must remain explicit', 'positive/read')
    rows = copy.deepcopy(traces['positive/read'])
    rows[8]['pre']['o_mstall'] = 1
    rows[9]['pre'].update(i_mcyc=1, i_mstb=1, i_maddr=7, i_msel=15)
    add('invalid/master_changes_stalled_payload', rows, 'invalid_environment', 'Changing stalled request is an external assumption violation', 'positive/read')
    return traces, manifest


def prepare(output):
    traces, manifest = controls()
    output.mkdir(parents=True, exist_ok=False)
    (output / 'private-inputs.json').write_text(json.dumps(traces, indent=2) + '\n')
    result = {'scope': 'Independent hand-constructed public-protocol controls; no DUT/Claude source or target evidence used.',
              'never_model_stimulus': True, 'controls': manifest,
              'authority': 'Wishbone B4 pp31–38; public WBXBAR interface/README intent in spec-packet-v1. Chosen trace delays are test fixtures, not asserted implementation latency.',
              'credit': 'Positive requires no functional/assumption errors and declared obligations checked; negative only credited with clean baseline and valid environment; incomplete must retain pending/unresolved, never success. Disputed controls require independent review, not forced checker changes.',
              'script_sha256': sha(Path(__file__)), 'inputs_sha256': sha(output / 'private-inputs.json')}
    (output / 'manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    result = prepare(parser.parse_args().output.resolve())
    print(json.dumps({'controls': len(result['controls']), 'inputs_sha256': result['inputs_sha256']}))
