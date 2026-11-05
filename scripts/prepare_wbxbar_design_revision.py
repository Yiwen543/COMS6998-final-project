"""Lossless synthetic evidence for Claude's reference-semantics revision.

No functional checker is authored or edited here. Both model calls remain
design-only; every live/implementation gate stays closed.
"""
import argparse
import copy
import json
import os
from pathlib import Path

from prepare_spi_core_checker_review import vector_pack, vector_unpack
from prepare_wbxbar_checker_role import PORTS
from prepare_wbxbar_conformance_role import BASE, controls
from probe_wbxbar_cancel_boundary import SCOPE, verify_scope
from review_wbxbar_conformance_design import verify as verify_review_packet
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import sha
from wbxbar_checker_controls import empty_rows, put, settle, transfer
from wbxbar_multi_abort_controls import request, forward

AUTHOR = '''Revise your proposed reference semantics after independent review. This is design only: no checker code, DUT, driver, or stimulus generation. Return ONLY JSON with clause_matrix, ownership_algorithm, formal_obligations, control_assessments (one record per supplied case: name, expected_status, justified_clauses, unresolved_scope), unresolved, ready_for_independent_review (JSON boolean). Use the supplied public sources and exact synthetic rows. Reviewer opinions are fallible; resolve the highlighted factual/logic issues, do not merely copy review prescriptions.
Prefer the smallest sound bounded implementation. A first exact-history implementation without speculative symmetry or partitioning is acceptable if limits and claim scope are explicit. Distinguish nondeterministic trace membership, universal properties and hidden ownership. A passing hypothesis is not universal evidence. Explain how a hypothesis is eliminated without circularly proving a property by assuming it. History-dependent uncertainty persists, including when old and live identical work coexist. No undisclosed unique tagging, one-outstanding restriction, forced reset or budget change.
Provide precise edge processing order, request/response multiplicity, same-edge dependencies, slave-CYC withdrawal and orphan fate, reset and repeated-abort identities, and resource-exhaustion behavior. State which checks remain valid when association reasoning exhausts its resources. Do not discard canceled identities merely because outputs are idle. If a required fact cannot be established, keep it explicitly unresolved, not a guessed deadline or pass.
Formal obligations are targets only. Distinguish the quantifiers for trace existence from universal hidden-property checking; standard safety tools cannot be assumed to supply existential matching strategies. Do not assume the correct mapping, use an RTL oracle, or assume the property being proved. Treat ERR/timeouts and finite counter/epoch overflow consistently. No new certificate is supplied.
All 69 legacy controls, seven earlier new controls and five new ordering/dependency/epoch scenarios are losslessly encoded. Derive labels from actual values and cited clauses. Names and historical labels are not normative authority. Keep justified corruption/duplicate/response checks; explicitly record each formerly inferred ordering label changed and why, before any replay. If scope does not settle a case, mark it unresolved. The author may question control legality; explain the exact pin/edge and source.
No approval in this response authorizes implementation, freeze or B/C. No DUT implementation, actual experiment trace, coverage ranking or calibration target is supplied.\n'''

REVIEW = '''Fresh independent read-only review of a revised reference-semantics design. No tools or code. Return ONLY JSON with findings (list), required_changes (list), ready_for_implementation (JSON boolean). Check the concrete transition and verdict semantics, unresolved obligations, resource limits, exact control values and classifications, cancellation/reset boundaries and formal quantifiers. Do not rubber-stamp a simpler algorithm or invent proof evidence. Identify whether the claimed finite scope is executable without unsound assumptions. No implementation or B/C is authorized automatically.\n'''


def additions():
    out = {}
    for name, order in [('fifo_order', (0, 1, 2)), ('younger_equal_first', (2, 1, 0))]:
        rows = empty_rows(28)
        for index, addr in enumerate((5, 7, 5)):
            pos = order.index(index)
            transfer(rows, accept=6+index, forward=10+pos, response=13+pos,
                     returned=16+index, addr=addr, read_data=0x11110000+index)
        out['new_aba/' + name] = settle(rows)
    rows = empty_rows(28)
    transfer(rows, accept=6, forward=9, response=12, returned=14,
             addr=5, read_data=0xaaaa0001)
    transfer(rows, master=1, accept=6, forward=10, response=13, returned=15,
             addr=5, read_data=0xbbbb0001)
    transfer(rows, accept=7, forward=11, response=16, returned=17,
             addr=7, read_data=0xcccc0001)
    out['new_dependency/overlapping_distinct'] = settle(rows)
    bad = copy.deepcopy(rows)
    put(bad, 17, 'o_mdata', 0, 32, 0xcccc0002)
    out['new_dependency/overlapping_data_change'] = settle(bad)
    rows = empty_rows(28)
    for start in (6, 10, 14):
        request(rows, start, 6, 0x23456781)
        put(rows, start+1, 'i_mcyc', 0, 1, 1)
    for cycle in range(16, 19):
        put(rows, cycle, 'i_mcyc', 0, 1, 1)
    forward(rows, 16, 6, 0x23456781)
    put(rows, 18, 'o_mack', 0, 1, 1)
    out['new_epoch/two_aborts_then_identical_restart'] = settle(rows)
    return out


def all_controls():
    original = BASE.parent / 'wbxbar_abort_contract_20261104/controls-v1/private-inputs.json'
    rows = json.loads(original.read_text())
    rows.update({name: item['rows'] for name, item in controls().items()})
    rows.update(additions())
    if len(rows) != 81:
        raise ValueError('Unexpected control count or duplicate name')
    for trace in rows.values():
        for cycle, row in enumerate(trace):
            if row['cycle'] != cycle:
                raise ValueError('Noncontiguous synthetic rows')
            for phase, ports in [('pre', {**PORTS['inputs'], **PORTS['outputs']}), ('post', PORTS['outputs'])]:
                if set(row[phase]) != set(ports):
                    raise ValueError('Control pin schema')
                if any(type(row[phase][p]) is not int or not 0 <= row[phase][p] < 1 << width for p, width in ports.items()):
                    raise ValueError('Control pin width')
    return rows


def pack_controls(rows):
    first = next(iter(rows.values()))[0]
    columns = [(phase, name) for phase in ('pre', 'post') for name in first[phase]]
    values = {}
    for name, trace in rows.items():
        normalized = [{**row, 'action': {}} for row in trace]
        values[name] = vector_pack(normalized, columns)
        restored = [{k: v for k, v in row.items() if k != 'action'}
                    for row in vector_unpack(values[name], columns)]
        if restored != trace:
            raise ValueError('Control packing changed pin evidence')
    return {'columns': columns, 'values': values,
            'format': 'first is a vector indexed by columns [pre/post,pin], at start_cycle. For each [repeat,changes] step: repeat times copy the previous vector, increment cycle by 1, apply every [column_index,new_value]. No rows omitted; transfers use pre only. post is not a second transfer.'}


def identity_facts(rows):
    # Pure extraction, not ownership assignment or an expected verdict.
    facts = []
    for row in rows:
        p = row['pre']
        for side, prefix, count in [('master', 'i_m', 2), ('slave', 'o_s', 2)]:
            for index in range(count):
                cyc, stb = (p[prefix + field] >> index & 1 for field in ('cyc', 'stb'))
                stall = p['o_mstall' if side == 'master' else 'i_sstall'] >> index & 1
                if not (cyc and stb and not stall):
                    continue
                sel = p[prefix + 'sel'] >> (4*index) & 15
                data = p[prefix + 'data'] >> (32*index) & 0xffffffff
                mask = sum(255 << (8*lane) for lane in range(4) if sel >> lane & 1)
                facts.append({'cycle': row['cycle'], 'side': side, 'index': index,
                              'we': p[prefix + 'we'] >> index & 1,
                              'address': p[prefix + 'addr'] >> (8*index) & 255,
                              'sel': sel, 'data': data, 'enabled_lane_bits': data & mask})
    return facts


def prepare(output):
    verify_scope()
    verify_review_packet(BASE / 'design-review-packet-v1')
    initial = json.loads((BASE / 'claude-design-packet-v1/packet.json').read_text())
    traces = all_controls()
    body = {
        'role': 'Claude original specification-design author revision; no checker code',
        'specification': initial['specification'],
        'previous_design': json.loads((BASE / 'claude-design-v1/design.json').read_text()),
        'independent_review': json.loads((BASE / 'design-review-v1/review.json').read_text()),
        'synthetic_traces': pack_controls(traces),
        'exact_identity_facts': identity_facts(traces['multi_abort/live_aborted_same_identity']),
        'integration_cautions': [
            'Reviewer R8 waffles on whether m1 matches the canceled request. The attached mechanically extracted values and original packed rows are authoritative; assess enabled SEL bytes explicitly. Do not copy its uncertain constants.',
            'Reviewer R6 proposes directional ERR implications. They still need live/uncanceled response applicability, simultaneous timeout precedence and no invented deadline. A slave ACK alone may not justify an unconditional master no-ERR assertion.',
            'Reviewer R5 mixes universal association properties and existential trace acceptance. Specify the actual checked claim and whether an SMT safety harness can express it. A failed arbitrary association is not automatically a DUT failure.',
            'Old full-controller prove results are not supplied. Every proposed formal item remains unimplemented and unproved. The current public contract can leave cancellation provenance unknown.'
        ],
        'isolation': 'No DUT code, actual model trajectories, calibration targets, original B/C results, coverage or proof outcomes. Historical synthetic names do not mandate verdicts.'}
    prompt = AUTHOR + json.dumps(body, separators=(',', ':'))
    if len(prompt.encode()) > 150000:
        raise ValueError('Revision prompt exceeds byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    sources = [SCOPE, Path(__file__), BASE / 'claude-design-v1/design.json',
               BASE / 'design-review-v1/review.json',
               BASE.parent / 'wbxbar_abort_contract_20261104/controls-v1/private-inputs.json']
    manifest = {'status': 'prepared_not_called', 'hashes': {str(p): sha(p) for p in sources},
                'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
                'bytes': len(prompt.encode()), 'synthetic_cases': len(traces),
                'rows': sum(map(len, traces.values())), 'new_cases': 5,
                'planned_calls_max': 2, 'cli_budget_per_call_usd': 4,
                'implementation_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def verify(packet):
    verify_scope()
    manifest = json.loads((packet / 'manifest.json').read_text())
    for path, digest in manifest['hashes'].items():
        if sha(Path(path)) != digest:
            raise ValueError('Revision source drift: ' + path)
    for name in ('packet', 'prompt'):
        if sha(packet / (name + ('.json' if name == 'packet' else '.txt'))) != manifest[name + '_sha256']:
            raise ValueError('Revision packet drift: ' + name)
    return manifest


def run(packet, output):
    verify(packet)
    if output.exists():
        raise ValueError('Never overwrite a model attempt')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise ValueError('Hidden key absent or unsafe')
    env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
    output.mkdir(parents=True)
    try:
        design = call((packet / 'prompt.txt').read_text(), output / 'author', env, 'WBXBAR specification-design revision author')
        (output / 'design.json').write_text(json.dumps(design, indent=2) + '\n')
        expected = {'clause_matrix', 'ownership_algorithm', 'formal_obligations', 'control_assessments', 'unresolved', 'ready_for_independent_review'}
        if not isinstance(design, dict) or set(design) != expected or type(design['ready_for_independent_review']) is not bool:
            raise ValueError('Revision response schema; no paid format retry')
        body = json.loads((packet / 'packet.json').read_text())
        review_body = {key: body[key] for key in ('specification', 'synthetic_traces', 'exact_identity_facts', 'integration_cautions', 'isolation')}
        review_body['revised_design'] = design
        review_prompt = REVIEW + json.dumps(review_body, separators=(',', ':'))
        if len(review_prompt.encode()) > 150000:
            raise ValueError('Fresh review exceeds byte cap; no call made')
        result = call(review_prompt, output / 'review', env, 'WBXBAR fresh revised-design reviewer')
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
