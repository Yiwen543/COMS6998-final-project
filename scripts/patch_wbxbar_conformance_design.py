"""Exact Claude-authored JSON design patches and fresh review, never checker edits."""
import argparse
import copy
import json
import os
from pathlib import Path

from prepare_wbxbar_design_revision import BASE, all_controls, pack_controls
from probe_wbxbar_cancel_boundary import SCOPE, verify_scope
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import sha
from wbxbar_checker_controls import empty_rows, put, settle, transfer

AUTHOR = '''You are the independent Claude specification-design author, repairing your design after fresh review. Design only, no checker code. Return ONLY JSON with patches, control_assessments_additions, rationale, ready_for_review (boolean). patches contains {path,before,after}; path is an array of exact existing JSON object keys or list indices in previous_design. before must equal the full value at that path. Apply patches in order. For new controls append assessments separately as control_assessments_additions: {name,expected_status,justified_clauses,unresolved_scope}. Do not repeat unchanged sections or all 81 old assessments. Address only the findings and independently justified corrections; all previous rules remain unless explicitly patched. Do not accept reviewer factual errors, infer latency or timing merely from DUT option names, or turn possible starvation into a proven explanation. Unknown remains unknown.
Resolve unaccepted held-request ERR versus ACK, temporal precedence of DUT/environment failures, identity-only payload comparisons, declared scope/exclusions, sound counters after resource exhaustion, and measurable suspended checking. Earlier definite violations cannot disappear when input later becomes invalid. Later conclusions must respect the validity boundary; a same-edge mixed fault needs explicit ordering/uncertainty. Analyze the actual rows and primary sources; proposed control descriptions are not verdict instructions. Reference-membership is not hidden ownership proof. Preserve matched budgets and no live permission. No RTL/actual experiments/proof results are supplied.\n'''
REVIEW = '''Fresh independent read-only review of the patched specification design. Return ONLY JSON {findings:[...],required_changes:[...],ready_for_implementation:boolean}. Assess whether the declared finite checker scope is executable and sound enough to implement, without implying formal certification or readiness for B/C. Inspect starvation ERR versus invented ACK, valid-prefix versus invalid-suffix verdicts, cancellation/identity ambiguity, field masks, same-edge handling, resource limits and explicit exclusions. Verify cited cycles using the supplied pre-edge event ledger and full lossless rows; do not treat post observations as transfers. Reviewer and author prose are fallible. No tools/code edits.\n'''


def additions():
    out = {}
    for response in ('err', 'ack'):
        rows = empty_rows(28)
        for c in range(6, 9):
            rows[c]['pre'].update(i_mcyc=1, i_mstb=1, i_mwe=1,
                                  i_maddr=5, i_mdata=0x12345678, i_msel=5, o_mstall=1)
        rows[8]['pre']['o_m' + response] = 1
        out['new_starvation/unaccepted_' + response] = settle(rows)
    for corrupt in (False, True):
        rows = transfer(empty_rows(28), accept=6, forward=8, response=9, returned=10)
        if corrupt:
            rows[10]['pre']['o_mdata'] ^= 1
        rows[15]['pre'].update(i_mcyc=1, i_mstb=1, i_maddr=5, i_msel=15, o_mstall=1)
        rows[16]['pre'].update(i_mcyc=1, i_mstb=1, i_maddr=7, i_msel=15, o_mstall=1)
        out['new_prefix/' + ('earlier_data_change' if corrupt else 'clean_before_invalid_input')] = settle(rows)
    for mode in ('read_data_changes', 'write_disabled_changes', 'write_enabled_changes'):
        we = int(mode.startswith('write'))
        rows = transfer(empty_rows(28), accept=6, forward=10, response=11,
                        returned=12, we=we, sel=5)
        for c in (8, 9):
            for port in ('o_scyc', 'o_sstb', 'o_swe', 'o_saddr', 'o_sdata', 'o_ssel'):
                rows[c]['pre'][port] = rows[10]['pre'][port]
            rows[c]['pre']['i_sstall'] = 1
        rows[9]['pre']['o_sdata'] ^= 1 if mode != 'write_disabled_changes' else 0xff00
        out['new_payload/' + mode] = settle(rows)
    return out


def event_ledger(rows):
    events = []
    for row in rows:
        p = row['pre']
        for event, bits in (
            ('master_accept', p['i_mcyc'] & p['i_mstb'] & ~p['o_mstall']),
            ('slave_accept', p['o_scyc'] & p['o_sstb'] & ~p['i_sstall']),
            ('slave_ack_pin', p['i_sack']), ('slave_err_pin', p['i_serr']),
            ('master_ack_pin', p['o_mack']), ('master_err_pin', p['o_merr'])):
            for port in (0, 1):
                if bits >> port & 1:
                    events.append({'cycle': row['cycle'], 'event': event, 'port': port})
    return events


def prepare(output):
    verify_scope()
    parent = BASE / 'design-revision-v1'
    previous_packet = json.loads((BASE / 'design-revision-packet-v1/packet.json').read_text())
    rows = all_controls()
    rows.update(additions())
    body = {k: previous_packet[k] for k in ('specification', 'exact_identity_facts', 'isolation')}
    body.update(previous_design=json.loads((parent / 'design.json').read_text()),
                independent_review=json.loads((parent / 'review.json').read_text()),
                synthetic_traces=pack_controls(rows), new_control_names=list(additions()),
                pre_edge_event_ledgers={name: event_ledger(rows[name]) for name in [*additions(), 'new_epoch/two_aborts_then_identical_restart']},
                integration_cautions=[
                    'Review F6 is factually wrong: exact pre rows give accepts6/10/14, slave forward16, slave ACK17, master ACK18. The packed decoder round-trips to those same rows. Keep original data and correct review prose, not the trace.',
                    'F1 suggests possible starvation before acceptance. The header does not establish its exact phase or timing. Classify unknown unless justified; do not assume every no-entry ERR is legitimate or treat fabricated ACK equally.',
                    'F3 cannot establish OPT_DBLBUFFER extra latency from its name alone. K6 checks active-cycle retirement; an inactive-CYC raw ACK does not automatically supply an independent K6 violation. Derive the exact declared scope from sources.',
                    'Changing a property in a negative control can legitimately test the harness, but a trivial reset failure does not establish nonvacuous transaction sensitivity. Distinguish property-harness controls from RTL/trace mutation detection.',
                    'All 81 old cases remain unchanged. Seven new synthetic scenarios are for contract development only. No new checker, original-result edit, stimulus or budget modification.'])
    prompt = AUTHOR + json.dumps(body, separators=(',', ':'))
    if len(prompt.encode()) > 150000:
        raise ValueError('Author byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    paths = [SCOPE, Path(__file__), parent / 'design.json', parent / 'review.json']
    manifest = {'status': 'prepared_not_called', 'hashes': {str(p): sha(p) for p in paths},
                'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
                'bytes': len(prompt.encode()), 'cases': len(rows), 'new_cases': 7,
                'planned_calls_max': 2, 'cli_budget_per_call_usd': 4,
                'automatic_implementation_permission': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def verify(packet):
    verify_scope()
    manifest = json.loads((packet / 'manifest.json').read_text())
    for path, digest in manifest['hashes'].items():
        if sha(Path(path)) != digest:
            raise ValueError('Patch source drift')
    for name, ext in [('packet', 'json'), ('prompt', 'txt')]:
        if sha(packet / (name + '.' + ext)) != manifest[name + '_sha256']:
            raise ValueError('Patch packet drift')
    return manifest


def apply_patches(original, response, new_names):
    if set(response) != {'patches', 'control_assessments_additions', 'rationale', 'ready_for_review'} or type(response['ready_for_review']) is not bool:
        raise ValueError('Design patch response schema')
    result = copy.deepcopy(original)
    for patch in response['patches']:
        path = patch['path']
        if not isinstance(path, list) or not path or path[0] not in original:
            raise ValueError('Patch path outside design')
        obj = result
        for key in path[:-1]:
            obj = obj[key]
        key = path[-1]
        if isinstance(obj, list) and (type(key) is not int or key < 0 or key >= len(obj)):
            raise ValueError('Invalid list patch index')
        if obj[key] != patch['before']:
            raise ValueError('Exact patch before mismatch; never guess')
        obj[key] = patch['after']
    extra = response['control_assessments_additions']
    if not isinstance(extra, list) or len(extra) != len(new_names) or {r['name'] for r in extra} != set(new_names):
        raise ValueError('New control assessment coverage')
    result['control_assessments'].extend(extra)
    old_names = {c['name'] for c in original['control_assessments']}
    if len(result['control_assessments']) != len(old_names) + len(new_names) or {c['name'] for c in result['control_assessments']} != old_names | set(new_names):
        raise ValueError('Historical control assessments lost or duplicated')
    return result


def run(packet, output):
    verify(packet)
    if output.exists():
        raise ValueError('Never overwrite model evidence')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise ValueError('Hidden key absent or unsafe')
    env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
    output.mkdir(parents=True)
    try:
        body = json.loads((packet / 'packet.json').read_text())
        response = call((packet / 'prompt.txt').read_text(), output / 'author', env, 'WBXBAR exact specification-design patch author')
        (output / 'patches.json').write_text(json.dumps(response, indent=2) + '\n')
        design = apply_patches(body['previous_design'], response, body['new_control_names'])
        (output / 'design.json').write_text(json.dumps(design, indent=2) + '\n')
        review_body = {k: body[k] for k in ('specification', 'synthetic_traces', 'pre_edge_event_ledgers', 'integration_cautions', 'isolation')}
        review_body['patched_design'] = design
        prompt = REVIEW + json.dumps(review_body, separators=(',', ':'))
        if len(prompt.encode()) > 150000:
            raise ValueError('Review byte cap; no call made')
        result = call(prompt, output / 'review', env, 'WBXBAR fresh exact-design-patch reviewer')
        (output / 'review.json').write_text(json.dumps(result, indent=2) + '\n')
        valid = isinstance(result, dict) and set(result) == {'findings', 'required_changes', 'ready_for_implementation'} and type(result.get('ready_for_implementation')) is bool
        status = {'schema_valid': valid, 'model_readiness': result.get('ready_for_implementation') if valid else None,
                  'automatic_implementation_permission': False, 'live_B_allowed': False, 'live_C_allowed': False}
        (output / 'validation.json').write_text(json.dumps(status, indent=2) + '\n')
        return status
    finally:
        KEY_FILE.unlink(missing_ok=True)
        env.pop('ANTHROPIC_API_KEY', None)
        verify_scope()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prepare', 'run'])
    parser.add_argument('--packet', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.output.resolve()) if args.mode == 'prepare'
                     else run(args.packet.resolve(), args.output.resolve()), indent=2))
