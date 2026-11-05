"""Package complete evidence for a fresh read-only review; no checker edits."""
import argparse
import json
from pathlib import Path

from followup_wbxbar_reference_checker import verify as verify_author
from prepare_wbxbar_reference_review import OUTPUT_BASE, FILES, compact, pack_results, pack_traces, unpack_results
from repair_wbxbar_reference_checker import apply_exact
from probe_wbxbar_cancel_boundary import SCOPE
from run_midterm_fixed import ROOT, sha

PREFIX = '''Fresh independent read-only Claude specification/checker CODE review. Use only this packet, no tools or edits. Return ONLY JSON with ready_for_replay_registration (boolean), findings (list), contract_decision_assessments (list), required_followup (list), limitations (list). Inspect executable code and public contract; do not treat synthetic agreement or author claims as certification. Audit unknown evidence retention, actual property checking and undefined-data assumptions. Assess the reported remaining termination diagnostic independently; a passing test suite cannot override a real reporting defect. Even a positive opinion cannot freeze the checker, replay data or authorize B/C.\n'''


def pack_review_results(results):
    """Intern repeated dictionary paths only; preserve every value and diagnostic."""
    paths, indices = [], {}

    def index(path):
        key = tuple(path)
        if key not in indices:
            indices[key] = len(paths)
            paths.append(path)
        return indices[key]

    records = pack_results(results)
    for entry in records.values():
        if 'value' not in entry:
            entry['set'] = [[index(path), value] for path, value in entry['set']]
            entry['delete'] = [index(path) for path in entry['delete']]
    packed = {'paths': paths, 'records': records}
    if unpack_review_results(packed) != results:
        raise ValueError('Interned result roundtrip failed')
    return packed


def unpack_review_results(packed):
    records = {}
    for name, entry in packed['records'].items():
        records[name] = entry if 'value' in entry else {
            'base': entry['base'],
            'set': [[packed['paths'][i], value] for i, value in entry['set']],
            'delete': [packed['paths'][i] for i in entry['delete']]}
    return unpack_results(records)


def prepare(output):
    verify_author(OUTPUT_BASE / 'completion-packet-v1')
    run = OUTPUT_BASE / 'completion-v1'
    candidate = run / 'candidate'
    previous = OUTPUT_BASE / 'followup-v1/candidate'
    patches = json.loads((run / 'patches.json').read_text())
    rebuilt = apply_exact({f: (previous / f).read_text() for f in FILES}, patches)
    meta = json.loads((candidate / 'metadata.json').read_text())
    for f in FILES:
        if rebuilt[f] != (candidate / f).read_text() or sha(candidate / f) != meta['artifact_sha256'][f]:
            raise ValueError('Not the exact Claude candidate')
    controls = OUTPUT_BASE / 'controls-v1'
    cm = json.loads((controls / 'manifest.json').read_text())
    for path, digest in cm['hashes'].items():
        if sha(Path(path)) != digest:
            raise ValueError('Control provenance drift')
    normal = json.loads((run / 'evaluation-original/cases.json').read_text())
    summary = json.loads((run / 'evaluation-original/summary.json').read_text())
    if summary['candidate_sha256'] != meta['artifact_sha256'] or not summary['all_control_agreements']:
        raise ValueError('Original offline control gate not met')
    body = json.loads((OUTPUT_BASE / 'code-review-packet-v1/packet.json').read_text())
    inputs = {n: {'rows': rows, 'limits': {}} for n, rows in json.loads((controls / 'inputs.json').read_text()).items()}
    limits = json.loads((controls / 'limit-tests.json').read_text())
    inputs.update({'limit/' + n: {'rows': x['rows'], 'limits': x['limits']} for n, x in limits.items()})
    results = {**normal['cases'], **{'limit/' + n: x for n, x in json.loads((run / 'evaluation-original/limits.json').read_text()).items()}}
    for kind in ('focused', 'boundary'):
        cases = json.loads((run / (kind + '-inputs.json')).read_text())
        evaluated = json.loads((run / ('evaluation-' + kind) / 'outputs.json').read_text())
        for n, case in cases.items():
            name = kind + '_recheck/' + n
            inputs[name] = case
            results[name] = evaluated[n]
            body['expectations'].append({'name': name, 'kind': 'focused_diagnostic',
                'expected': 'Assess exact public-contract and evidence-retention semantics independently; no new golden label imposed.'})
    if set(inputs) != set(results) or len(inputs) != 155:
        raise ValueError('Incomplete trace/result set')
    body.update(
        role='Independent fresh Claude reviewer of completion candidate',
        candidate={f: (candidate / f).read_text() for f in FILES},
        traces=pack_traces({n: x['rows'] for n, x in inputs.items() if not n.startswith('boundary_recheck/')}),
        raw_boundary_traces={n: x['rows'] for n, x in inputs.items() if n.startswith('boundary_recheck/')},
        case_limits={n: x['limits'] for n, x in inputs.items()},
        full_checker_results=pack_review_results(results), selftest_results=normal['selftests'], worker_errors=normal['errors'],
        latest_prior_review=json.loads((OUTPUT_BASE / 'repair-review-v1/review.json').read_text()),
        author_decisions={p: {k: json.loads((OUTPUT_BASE / p / 'patches.json').read_text())[k]
                                for k in ('rationale', 'contract_decisions')} for p in ('followup-v1', 'completion-v1')},
        questions=[
            'The unchanged author selftest mixed_death_keeps_prefix_tag_open now passes. Compare valid prefix rows0..7 and first invalid row8, schema failures, mixed death, exhaustion/reset closure and snapshot clearing. Does every feasible valid-prefix tag survive exactly once? Are invalid-row-created tags excluded, including when exhaustion or close_epoch clears rowtags?',
            'The independent undefined_DUT_control probe retains rows0..7 with possible_starvation_err@3, then sets pre.o_mstall=None at8. It returns a pin DUT failure + unjudgeable_row but drops the earlier unknown tag. Decide whether this is a remaining evidence/reporting defect, whether it blocks scoped saved-action replay readiness, and what explicit limitation or author repair is required. The fixed integer JSON driver cannot emit None; this fact does not silently waive checker reporting requirements. Do not suppress the genuine undefined-output failure.',
            'K11_env_checks now counts non-reset processed rows and explicitly excludes schema validation and reset rule3.20 from instrumentation. Check actual eligibility/calls and definitions. Verify all sub-obligation checked/suspended/post-death counts and unknown-record counts; exposure, instrumentation and proof coverage are different quantities.',
            'Independently assess the public-pin per-slave FIFO WE rule for undefined read ACK data, including orphan and live read controls. Validate accepted specification assumptions; do not treat agreement with author fixtures as normative authority. Preserve K5/C1-C4 exclusions, repeated HR ERR unknowns and unproved F1-F8.',
            'Audit contract/properties/source consistency, superseded P1/P4 wording, ACK versus ERR dependencies, history display limits, invalid-row membership death, default resource bounds and existing valid-row failures. The latest selftest file is byte-identical to its parent; the failed test was fixed through code, not its expected label.',
            'All155 complete traces/results and per-case limits are supplied. State whether all are decoded or only sampled. 127 normal+6 limit agreements and54 author selftests pass; 22 additional diagnostic executions are evidence, not a blanket certification. A remaining defect must not be hidden behind these totals.',
        ],
        gate_status={'author_selftests_passed': 54, 'author_selftests_total': 54,
            'original_normal_agreements': 127, 'original_limit_agreements': 6,
            'original_control_gate_passed': True, 'additional_diagnostic_cases': 22,
            'checker_validated': False, 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False},
        isolation='Complete synthetic and author diagnostic evidence only. No DUT implementation, actual B/C traces/results, coverage, target witnesses or performance ranking. No GPT functional checker edits. Full133 independent controls withheld from author, now disclosed to independent reviewer.',
    )
    body['encoding']['raw_boundary_traces'] = 'Five complete uncompressed JSON row lists. Missing keys and non-contiguous cycles are deliberate malformed-input controls: preserve them exactly, never fill defaults or renumber. Combine these with decoded traces for all155 cases.'
    body['encoding']['results'] = 'full_checker_results has paths (an array of dictionary-key paths) and records. Decode records in insertion order: value is complete JSON; otherwise deep-copy the named base, delete each paths[index] named in delete, then replace/add each [index,value] in set at paths[index]. Empty path replaces the root. Arrays are whole values. All155 complete diagnostics/counts/scope fields are retained; only repeated path spelling is interned.'
    prompt = PREFIX + compact(body)
    size = len(prompt.encode())
    if size > 500000:
        raise ValueError('Complete evidence exceeds 500000-byte transport cap: ' + str(size))
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    paths = [SCOPE, Path(__file__), ROOT / 'scripts/review_wbxbar_reference_repair.py',
        ROOT / 'scripts/prepare_wbxbar_reference_review.py', ROOT / 'scripts/revise_spi_checker_role.py',
        run / 'patches.json', candidate / 'metadata.json', *[candidate / f for f in FILES],
        *[run / 'evaluation-original' / f for f in ('summary.json', 'cases.json', 'limits.json')],
        *[controls / f for f in ('manifest.json', 'inputs.json', 'accounts.json', 'limit-tests.json')],
        *[run / (k + '-inputs.json') for k in ('focused', 'boundary')],
        *[run / ('evaluation-' + k) / 'outputs.json' for k in ('focused', 'boundary')],
        OUTPUT_BASE / 'repair-review-v1/review.json', OUTPUT_BASE / 'followup-v1/patches.json',
        OUTPUT_BASE / 'code-review-packet-v1/packet.json']
    manifest = {'status': 'prepared_not_called', 'source_hashes': {str(p): sha(p) for p in paths},
        'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
        'bytes': size, 'local_transport_byte_cap': 500000,
        'complete_trace_roundtrips': 155, 'complete_result_roundtrips': 155,
        'planned_calls': 1, 'cli_budget_usd': 4, 'timeout_seconds': 600,
        'requested_model': 'claude-opus-5-5', 'original_control_gate_passed': True,
        'offline_gate_passed': False, 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(prepare(args.output.resolve()), indent=2))
