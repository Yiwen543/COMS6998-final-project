"""Lossless evidence packet and one fresh read-only review of the Claude checker."""
import argparse
import copy
import json
import os
from pathlib import Path

from prepare_spi_core_checker_review import vector_pack, vector_unpack, delta, apply_delta
from prepare_wbxbar_reference_checker import OUTPUT_BASE, FILES, verify as verify_author
from probe_wbxbar_cancel_boundary import SCOPE, verify_scope
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import ROOT, sha

PREFIX = '''Fresh independent specification-checker CODE review. Use only this packet; no tools or edits. Return ONLY JSON with ready_for_replay_registration (boolean), findings (list), limitations (list), required_followup (list). Examine executable code against the public specification and reviewed reference contract, not just agreement with synthetic labels. Reject incorrect control labels as well as incorrect checker behavior. Passing controls is not proof. A positive review permits consideration of a separate saved-action replay freeze only, never B/C or a whole-IP correctness claim.\n'''
# This full code audit includes 133 complete traces/results, unlike the earlier
# design-only packets. The local transport cap is separate from frozen B/C input
# limits and the unchanged one-call $4 reviewer budget. Nothing is truncated.
PACKET_BYTE_CAP = 300000


def compact(value):
    return json.dumps(value, separators=(',', ':'), ensure_ascii=False)


def changes(base, value, path=()):
    """Explicit path replacements; arrays are whole values, never index-shift edits."""
    if type(base) is not type(value):
        return [[list(path), value]], []
    if isinstance(base, dict):
        sets, deletes = [], []
        for key in base.keys() - value.keys():
            deletes.append(list(path + (key,)))
        for key in value:
            if key not in base:
                sets.append([list(path + (key,)), value[key]])
            else:
                s, d = changes(base[key], value[key], path + (key,))
                sets.extend(s)
                deletes.extend(d)
        return sets, sorted(deletes)
    return ([], []) if base == value else ([[list(path), value]], [])


def patch(base, sets, deletes):
    value = copy.deepcopy(base)
    for path in deletes:
        parent = value
        for key in path[:-1]:
            parent = parent[key]
        del parent[path[-1]]
    for path, replacement in sets:
        if not path:
            value = copy.deepcopy(replacement)
            continue
        parent = value
        for key in path[:-1]:
            parent = parent[key]
        parent[path[-1]] = copy.deepcopy(replacement)
    return value


def pack_results(records):
    packed, decoded = {}, {}
    for name, value in records.items():
        best = {'value': value}
        for prior, base in decoded.items():
            sets, deletes = changes(base, value)
            option = {'base': prior, 'set': sets, 'delete': deletes}
            if len(compact(option)) < len(compact(best)):
                best = option
        packed[name] = best
        decoded[name] = value
    if unpack_results(packed) != records:
        raise ValueError('Result roundtrip failed')
    return packed


def unpack_results(packed):
    decoded = {}
    for name, entry in packed.items():
        decoded[name] = copy.deepcopy(entry['value']) if 'value' in entry else patch(
            decoded[entry['base']], entry['set'], entry['delete'])
    return decoded


def pack_traces(records):
    first = next(iter(records.values()))[0]
    columns = [(kind, key) for kind in ('pre', 'post') for key in first[kind]]
    packed, decoded = {}, {}
    for name, rows in records.items():
        full = [{**r, 'action': {}} for r in rows]
        best = {'vector': vector_pack(full, columns)}
        for prior, base in decoded.items():
            if len(base) < len(full) or any(a['cycle'] != b['cycle'] for a, b in zip(base, full)):
                continue
            option = {'base': prior, 'delta': delta(base, full)}
            if len(compact(option)) < len(compact(best)):
                best = option
        packed[name] = best
        decoded[name] = full
    result = {'columns': columns, 'values': packed}
    if unpack_traces(result) != records:
        raise ValueError('Trace roundtrip failed')
    return result


def unpack_traces(packed):
    decoded = {}
    for name, entry in packed['values'].items():
        decoded[name] = vector_unpack(entry['vector'], packed['columns']) if 'vector' in entry else apply_delta(
            decoded[entry['base']], entry['delta'])
    return {name: [{k: v for k, v in r.items() if k != 'action'} for r in rows] for name, rows in decoded.items()}


def prepare(output):
    verify_scope()
    verify_author(OUTPUT_BASE / 'spec-packet-v1')
    candidate, evaluation, controls = [OUTPUT_BASE / s for s in ('claude-author-v1', 'evaluation-v1', 'controls-v1')]
    metadata = json.loads((candidate / 'metadata.json').read_text())
    for name, digest in metadata['artifact_sha256'].items():
        if sha(candidate / name) != digest:
            raise ValueError('Candidate drift')
    cm = json.loads((controls / 'manifest.json').read_text())
    for path, digest in cm['hashes'].items():
        if sha(Path(path)) != digest:
            raise ValueError('Control provenance drift')
    summary = json.loads((evaluation / 'summary.json').read_text())
    if summary['candidate_sha256'] != metadata['artifact_sha256'] or summary['controls_manifest_sha256'] != sha(controls / 'manifest.json'):
        raise ValueError('Evaluation binding mismatch')
    original = json.loads((OUTPUT_BASE / 'spec-packet-v1/packet.json').read_text())
    cases = json.loads((evaluation / 'cases.json').read_text())
    limits = json.loads((controls / 'limit-tests.json').read_text())
    limit_results = json.loads((evaluation / 'limits.json').read_text())
    inputs = json.loads((controls / 'inputs.json').read_text())
    inputs.update({'limit/' + name: case['rows'] for name, case in limits.items()})
    all_results = {**cases['cases'], **{'limit/' + name: r for name, r in limit_results.items()}}
    if set(inputs) != set(all_results):
        raise ValueError('Missing evaluated case')
    expectations = json.loads((controls / 'accounts.json').read_text())
    expectations += [{'name': 'limit/' + name, **{k: v for k, v in case.items() if k != 'rows'}} for name, case in limits.items()]
    body = {
        'role': 'Independent fresh Claude code reviewer; no author conversation state',
        'specification': original['specification'],
        'reviewed_reference_contract': original['reviewed_reference_contract'],
        'candidate': {f: (candidate / f).read_text() for f in FILES},
        'expectations': expectations,
        'traces': pack_traces(inputs),
        'full_checker_results': pack_results(all_results),
        'encoding': {
            'traces': 'Decode values in insertion order. vector: first holds columns values at start_cycle. Each [repeat,changes] step applies indexed assignments then emits a row and increments cycle, repeated as specified. delta: deep-copy earlier named base truncated to length; changes update action/pre/post dictionaries at each row index. action is empty placeholder. No pins or cycles omitted.',
            'results': 'Decode in insertion order. value is complete JSON. Otherwise deep-copy earlier named base, remove every delete path, then replace/add every set [path,value]. Paths are dictionary-key lists; arrays are replaced whole. Empty path replaces root. All diagnostics, counts, clauses and unknown records are preserved exactly; no sampling.',
        },
        'selftest_results': cases['selftests'], 'worker_errors': cases['errors'],
        'questions': [
            'Audit exact-history branching/aliasing, multiplicity, per-master retirement and per-slave responses, SEL projection, same-edge order, canceled/orphan identities and all HR ERR alternatives. Does any unknown alternative become a pass or erase an independent fault?',
            'Are pre-invalid-prefix faults, same-edge mixed faults, reset persistence of unknowns and default resource exhaustion implemented faithfully? Does suspension retain all required association-free checks and restart them correctly after reset?',
            'Do reported per-clause statuses and checked/unknown/suspended scope match actual executed checks? Distinguish aggregate nonreset row exposure from clause activation counts. Are truncated history displays and existential ownership labels disclosed clearly?',
            'Assess the 36 heldback transformations and 6 lowered-limit tests independently, including label validity. Same verdict alone is insufficient: inspect diagnostics and scope. Author selftests are not independent certification.',
            'Verify contract.md and properties.json match code, including inferred K6/K13, excluded K5/C1-C4, repeated HR ERR unknowns and unproved formal targets. Do not invent timeout or cancellation bounds.',
        ],
        'isolation': 'No DUT implementation, actual B/C traces, prompt/coverage/target results, calibration witnesses or performance ranking. Original 91 synthetic labels were reviewed before implementation; 36 heldback transformations and 6 resource tests were generated independently. No new DUT simulation or GPT stimulus call. No functional Claude source edits by GPT.',
    }
    prompt = PREFIX + compact(body)
    size = len(prompt.encode())
    if size > PACKET_BYTE_CAP:
        raise ValueError('Review byte cap: ' + str(size))
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    paths = [SCOPE, Path(__file__), ROOT / 'scripts/prepare_spi_core_checker_review.py',
             ROOT / 'scripts/revise_spi_checker_role.py', ROOT / 'scripts/evaluate_wbxbar_reference_checker.py',
             OUTPUT_BASE / 'spec-packet-v1/manifest.json', candidate / 'metadata.json', *[candidate / f for f in FILES],
             *[controls / f for f in ('manifest.json', 'inputs.json', 'accounts.json', 'limit-tests.json')],
             *[evaluation / f for f in ('summary.json', 'cases.json', 'limits.json', 'commands.json')]]
    manifest = {'status': 'prepared_not_called', 'source_hashes': {str(p): sha(p) for p in paths},
                'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
                'bytes': size, 'byte_cap': PACKET_BYTE_CAP, 'complete_trace_roundtrips': len(inputs),
                'complete_result_roundtrips': len(all_results), 'planned_calls': 1, 'cli_budget_usd': 4,
                'requested_model': 'claude-opus-5-5', 'timeout_seconds': 600,
                'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def verify(packet):
    verify_scope()
    verify_author(OUTPUT_BASE / 'spec-packet-v1')
    m = json.loads((packet / 'manifest.json').read_text())
    for path, digest in m['source_hashes'].items():
        if sha(Path(path)) != digest:
            raise ValueError('Review source drift: ' + path)
    for name, ext in [('packet', 'json'), ('prompt', 'txt')]:
        if sha(packet / (name + '.' + ext)) != m[name + '_sha256']:
            raise ValueError('Review packet drift')
    return m


def run(packet, output):
    verify(packet)
    if output.exists():
        raise ValueError('Never overwrite review evidence')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise ValueError('Hidden key absent or unsafe')
    env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
    try:
        result = call((packet / 'prompt.txt').read_text(), output, env, 'WBXBAR fresh reference checker code reviewer')
        (output / 'review.json').write_text(json.dumps(result, indent=2) + '\n')
        (output / 'runner-source.py').write_bytes(Path(__file__).read_bytes())
        valid = isinstance(result, dict) and type(result.get('ready_for_replay_registration')) is bool and all(
            isinstance(result.get(k), list) for k in ('findings', 'limitations', 'required_followup'))
        validation = {'schema_valid': valid, 'review_received': True,
                      'model_ready_for_replay_registration': result.get('ready_for_replay_registration') if valid else None,
                      'automatic_replay_permission': False, 'live_B_allowed': False, 'live_C_allowed': False}
        (output / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
        return validation
    finally:
        KEY_FILE.unlink(missing_ok=True)
        env.pop('ANTHROPIC_API_KEY', None)
        verify_scope()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prepare', 'run'])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--packet', type=Path)
    args = parser.parse_args()
    print(json.dumps(prepare(args.output.resolve()) if args.mode == 'prepare'
                     else run(args.packet.resolve(), args.output.resolve()), indent=2))
