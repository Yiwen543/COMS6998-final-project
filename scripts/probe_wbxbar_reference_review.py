"""Synthetic public-pin reproducers for reviewer findings, not a golden checker."""
import argparse
import copy
import json
import sys
from pathlib import Path

from evaluate_wbxbar_reference_checker import isolated
from prepare_wbxbar_reference_review import OUTPUT_BASE, verify, verify_scope
from run_midterm_fixed import ROOT, sha
from wbxbar_checker_controls import empty_rows, put, settle


def build():
    originals = json.loads((OUTPUT_BASE / 'controls-v1/inputs.json').read_text())
    cases = {}

    def add(name, rows, intent, limits=None):
        cases[name] = {'rows': settle(rows), 'limits': limits or {}, 'intent': intent,
                       'expected_verdict': 'not_imposed; independent author/reviewer must decide'}

    def tagged_prefix_then(name):
        rows = copy.deepcopy(originals['new_starvation/unaccepted_err'][:9])
        rows += copy.deepcopy(originals[name][2:])  # No intervening reset: preserve same reset epoch.
        for cycle, row in enumerate(rows):
            row['cycle'] = cycle
        return rows

    add('tag_then_clean_completion', tagged_prefix_then('positive/read'),
        'HR ERR at row 8 then ordinary work, no reset; compare persistence with the next two cases.')
    add('tag_then_exhaustion', tagged_prefix_then('ambiguity/inherently_indistinguishable'),
        'HR ERR precedes later branching-limit exhaustion in the same epoch; retain prior uncertainty evidence.', {'MAX_HYP': 1})
    add('tag_then_membership_death', tagged_prefix_then('negative/read_data'),
        'HR ERR precedes a definite later read-data corruption; disclose discarded epoch evidence without hiding the fault.')
    add('idle_no_error_or_abort', empty_rows(12),
        'Only initial reset and idle: inspect which conditional obligations actually activate, not a new functional verdict.')
    rows = empty_rows(18)
    for cycle in range(4, len(rows)):
        rows[cycle]['pre']['i_mcyc'] = 3
    for cycle in range(4, 9):
        rows[cycle]['pre'].update(i_mstb=3, i_maddr=5 | (5 << 8), i_msel=255)
    for cycle in range(10, len(rows)):
        rows[cycle]['pre']['o_scyc'] = 1
    for cycle in (10, 11):
        rows[cycle]['pre'].update(o_sstb=1, o_saddr=5, o_ssel=15)
    add('many_histories_pending', copy.deepcopy(rows),
        'Ten equal accepted identities and two forwards; check completeness/truncation disclosure of the pending-history display.')
    rows[12]['pre'].update(i_sack=1, i_sdata=0x13579bdf)
    rows[13]['pre'].update(o_mack=1, o_mdata=0x2468ace0)
    add('many_histories_corrupt_return', rows,
        'Wrong returned read value across many histories; inspect witness truncation disclosure and epoch preservation.')
    rows = copy.deepcopy(originals['negative/duplicate_response'])
    add('duplicate_ack_without_env_error', copy.deepcopy(rows),
        'Baseline duplicate ACK; compare its same-row count projection with the next invalid-input boundary case.')
    for cycle in (11, 12, 13):
        for port, width, value in [('i_mcyc', 1, 1), ('i_mstb', 1, 1), ('o_mstall', 1, 1),
                                   ('i_maddr', 8, 4 if cycle < 13 else 5), ('i_msel', 4, 15)]:
            put(rows, cycle, port, 1, width, value)
    add('duplicate_ack_with_same_edge_env_error', rows,
        'At row 13 duplicate master-0 ACK coincides with master-1 stalled address change. Ask Claude to decide K6 count versus mixed-edge semantics explicitly; no label imposed.')
    rows = copy.deepcopy(originals['err_boundary/acceptance_edge'])
    for cycle in range(8, 12):
        rows[cycle]['pre']['i_mcyc'] = 1
        rows[cycle]['pre']['o_scyc'] = 1
    accepted = rows[8]['pre']
    accepted.update(o_sstb=1, o_saddr=accepted['i_maddr'] & 255,
                    o_ssel=accepted['i_msel'] & 15, o_swe=accepted['i_mwe'] & 1,
                    o_sdata=accepted['i_mdata'] & 0xffffffff)
    rows[9]['pre'].update(i_sack=1, i_sdata=0x13579bdf)
    rows[10]['pre'].update(o_mack=1, o_mdata=0x13579bdf)
    add('hr_acceptance_and_forward_same_row', rows,
        'Held request accepts, forwards and receives ERR on row 8, then a slave ACK and a master ACK; ask Claude to resolve/document B2 on an already forwarded entry.')
    return cases


def run(output):
    verify(OUTPUT_BASE / 'code-review-packet-v1')
    review = json.loads((OUTPUT_BASE / 'code-review-v1/review.json').read_text())
    if review['ready_for_replay_registration'] is not False:
        raise ValueError('Expected the retained negative code review')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'builder-source.py').write_bytes(Path(__file__).read_bytes())
    cases = build()
    inputs = output / 'inputs.json'
    inputs.write_text(json.dumps(cases, indent=2) + '\n')
    command = [sys.executable, '-I', str(ROOT / 'scripts/evaluate_wbxbar_reference_checker.py'),
               '--limit-worker', '--candidate', str(OUTPUT_BASE / 'claude-author-v1'),
               '--inputs', str(inputs), '--output', str(output / 'outputs.json')]
    isolated(command, output / 'worker.log')
    results = json.loads((output / 'outputs.json').read_text())
    observations = {}
    for name, result in results.items():
        counts = result.get('counts', {})
        observations[name] = {
            'verdict': result.get('verdict'), 'assumption_violations': result.get('assumption_violations'),
            'failure_categories': [x['category'] for x in result.get('failures', [])],
            'unknown_items': [x['item'] for x in result.get('unresolved', [])],
            'pending_epoch_records': counts.get('pending_alternatives'),
            'property_status': counts.get('property_status'),
            'infrastructure_error': result.get('infrastructure_error')}
    (output / 'observations.json').write_text(json.dumps(observations, indent=2) + '\n')
    manifest = {'status': 'reproduced_on_immutable_candidate_not_golden_labels', 'cases': len(cases),
                'command': command, 'new_API_calls': 0, 'new_DUT_simulations': 0,
                'candidate_sha256': sha(OUTPUT_BASE / 'claude-author-v1/checker.py'),
                'source_hashes': {str(p): sha(p) for p in [Path(__file__), inputs, output / 'outputs.json',
                    OUTPUT_BASE / 'code-review-v1/review.json', OUTPUT_BASE / 'controls-v1/inputs.json']},
                'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    verify_scope()
    return {'cases': len(cases), 'infrastructure_errors': sum(bool(r.get('infrastructure_error')) for r in results.values())}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output.resolve()), indent=2))
