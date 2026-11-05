"""Extra independent identity controls for the Claude-authored abort repair."""
import argparse
import copy
import json
from pathlib import Path
from run_midterm_fixed import sha
from wbxbar_checker_controls import settle, put


def prepare(parent, output):
    manifest = json.loads((parent / 'manifest.json').read_text())
    if sha(parent / 'private-inputs.json') != manifest['inputs_sha256']:
        raise ValueError('Parent controls changed')
    traces = json.loads((parent / 'private-inputs.json').read_text())
    base = 'unresolved/post_abort_forward'
    def add(name, rows, kind, obligation):
        traces[name] = settle(rows)
        manifest['controls'].append(dict(name=name, kind=kind, obligation=obligation, baseline=base))
    rows = copy.deepcopy(traces[base])
    # Re-use the exact already-consumed old request. No new master acceptance.
    for c in (16, 17): rows[c]['pre']['o_scyc'] = 1
    for key in ('o_sstb','o_swe','o_saddr','o_sdata','o_ssel'):
        rows[16]['pre'][key] = rows[13]['pre'][key]
    rows[17]['pre']['i_sack'] = 1
    add('negative/duplicate_aborted_forward', rows, 'single_fault',
        'An aborted identity can justify at most one downstream acceptance; duplicate must fail, despite unresolved timing baseline')
    rows = copy.deepcopy(traces[base])
    rows[16]['pre']['i_reset'] = 1
    rows[17]['pre']['i_reset'] = 1
    add('unresolved/post_abort_then_reset', rows, 'unresolved',
        'A later reset clears old identities but cannot erase the earlier unresolved post-abort observation')
    rows = copy.deepcopy(traces[base])
    # Remove the old forward/return, reset the identity, then present old payload.
    for c in (13, 14):
        for key in rows[c]['pre']:
            if key.startswith('o_s') or key in ('i_sack','i_serr'):rows[c]['pre'][key] = 0
    rows[14]['pre']['i_reset'] = 1
    rows[15]['pre']['i_reset'] = 1
    for c in (17, 18): rows[c]['pre']['o_scyc'] = 1
    for key in ('o_sstb','o_swe','o_saddr','o_sdata','o_ssel'):
        rows[17]['pre'][key] = traces[base][13]['pre'][key]
    rows[18]['pre']['i_sack'] = 1
    add('negative/reset_clears_aborted_identity', rows, 'single_fault',
        'Pre-reset accepted work cannot justify a post-reset downstream request')
    rows = copy.deepcopy(traces[base])
    # A different live master owns an indistinguishable write at the abort edge.
    for c in range(13, len(rows)):put(rows, c, 'i_mcyc', 1, 1, 1)
    for key, width, value in [('i_mstb',1,1),('i_mwe',1,1),('i_maddr',8,4),('i_mdata',32,0x11223344),('i_msel',4,5)]:
        put(rows, 13, key, 1, width, value)
    add('unresolved/live_aborted_ambiguity', rows, 'unresolved',
        'Indistinguishable live and aborted owners require unresolved attribution, not guessed ownership or completion')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'private-inputs.json').write_text(json.dumps(traces, indent=2)+'\n')
    manifest.update(inputs_sha256=sha(output/'private-inputs.json'),
                    parent_manifest_sha256=sha(parent/'manifest.json'), script_sha256=sha(Path(__file__)))
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'controls':len(traces), 'inputs_sha256':manifest['inputs_sha256']}))


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--parent', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a=p.parse_args();prepare(a.parent, a.output)
