"""Versioned evidence assembly for the termination repair; no API call."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from followup_wbxbar_reference_checker import verify as verify_author
from prepare_wbxbar_reference_review import FILES, compact, pack_traces, unpack_traces
from prepare_wbxbar_completion_review import pack_review_results
from repair_wbxbar_reference_checker import apply_exact
from probe_wbxbar_cancel_boundary import SCOPE
from run_midterm_fixed import sha

base = Path(__file__).resolve().parent.parent
run = Path(__file__).resolve().parent
output = base / 'termination-review-packet-v1'
verify_author(base / 'termination-packet-v1')
parent = base / 'completion-v1/candidate'
candidate = run / 'candidate'
patches = json.loads((run / 'patches.json').read_text())
rebuilt = apply_exact({f: (parent / f).read_text() for f in FILES}, patches)
meta = json.loads((candidate / 'metadata.json').read_text())
for f in FILES:
    if rebuilt[f] != (candidate / f).read_text() or sha(candidate / f) != meta['artifact_sha256'][f]:
        raise ValueError('Not exact Claude patch output')
summary = json.loads((run / 'evaluation-original/summary.json').read_text())
normal = json.loads((run / 'evaluation-original/cases.json').read_text())
if not summary['all_control_agreements'] or summary['candidate_sha256'] != meta['artifact_sha256']:
    raise ValueError('Original control gate or candidate binding failed')
body = json.loads((base / 'completion-review-packet-v1/packet.json').read_text())
traces = unpack_traces(body['traces'])
traces.update(body['raw_boundary_traces'])
results = {**normal['cases'], **{'limit/' + n: r for n, r in json.loads((run / 'evaluation-original/limits.json').read_text()).items()}}
inputs = json.loads((run / 'focused-inputs.json').read_text())
supplemental = json.loads((run / 'evaluation-focused/outputs.json').read_text())
for name, case in inputs.items():
    kind, local = name.split('/', 1)
    target = kind + '_recheck/' + local
    if target in traces:
        if traces[target] != case['rows'] or body['case_limits'][target] != case['limits']:
            raise ValueError('Existing trace or limits changed')
    else:
        traces[target] = case['rows']
        body['case_limits'][target] = case['limits']
        body['expectations'].append({'name': target, 'kind': 'supplementary_termination_diagnostic',
            'expected': 'Assess termination retention without duplicate unknowns, suppression of earlier faults, or processing the reset suffix; no new golden rule imposed.'})
    results[target] = supplemental[name]
if set(traces) != set(results) or len(results) != 158:
    raise ValueError('Incomplete new evaluation evidence')
body.update(
    role='Fresh independent Claude review of termination repair',
    candidate={f: (candidate / f).read_text() for f in FILES},
    traces=pack_traces({n: rows for n, rows in traces.items() if not n.startswith('boundary_recheck/')}),
    raw_boundary_traces={n: rows for n, rows in traces.items() if n.startswith('boundary_recheck/')},
    full_checker_results=pack_review_results(results),
    selftest_results=normal['selftests'], worker_errors=normal['errors'],
    latest_prior_review=json.loads((base / 'completion-review-v1/review.json').read_text()),
    questions=[
        'Independently assess N1/N2 repair: pd-only termination preserves the genuine K10 violation and unjudgeable_row, flushes only the unmodified valid-prefix history set, reports pending work, and qualifies prefix statuses. Does it correctly distinguish termination_boundary from input_validity_boundary, reset and batch-end? Check row numbers and closure reason.',
        'Check suspended/dead paths and the reset-suffix diagnostic. Previously flushed tags must not duplicate; prior valid membership failures and refuted evidence must survive; no suffix row may run. Check first-row undefined-output and clean-prefix selftests without inventing reset/liveness guarantees.',
        'Review K12 reporting: pending_at_unjudgeable_row makes K12 unresolved but deliberately is not a batch-end activation. unknown_tag_records currently counts only tags named in TAG_CLAUSE (the new pending record is not in that map). Decide whether the existing metric scope and documentation remain honest, distinguishing historical tags from all unresolved diagnostics; do not silently label this formal coverage.',
        'Current58 author selftests pass; all127 normal+6 limit classifications agree. The25 additional cases are newly evaluated on this exact candidate, not copied results. Preserve the prior accepted scoped read-data/K11/ACK decisions unless the new source reveals a real issue. Full158 traces/results are supplied; disclose which you actually decode and inspect.',
        'Recheck executable code/contract/properties consistency and existing exclusions K5/C1-C4, F1-F8 unproved, repeated HR ERR unknowns. Static/model review is not certification. Identify concrete blocking repairs separately from nonblocking limitations. A positive assessment only allows consideration of a separately registered saved-action replay, never a new B/C trial.',
    ],
    gate_status={'author_selftests_passed': 58, 'author_selftests_total': 58,
        'original_normal_agreements': 127, 'original_limit_agreements': 6,
        'original_control_gate_passed': True, 'additional_diagnostic_cases': 25,
        'checker_validated': False, 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False},
)
body['author_decisions']['termination-v1'] = {k: patches[k] for k in ('rationale', 'contract_decisions')}
body['encoding']['raw_boundary_traces'] = body['encoding']['raw_boundary_traces'].replace('all155', 'all158')
body['encoding']['results'] = body['encoding']['results'].replace('All155', 'All158')
prefix = 'Fresh independent read-only Claude code review. Return ONLY JSON with ready_for_replay_registration (boolean), findings, contract_decision_assessments, required_followup, limitations (all lists). No tools or edits. Assess the exact termination repair against public specification and reviewed contract, not merely test agreement. Do not waive confirmed reporting defects. A positive opinion cannot freeze, replay or authorize B/C.\n'
prompt = prefix + compact(body)
if len(prompt.encode()) > 500000:
    raise ValueError('Review transport byte cap')
output.mkdir(exist_ok=False)
(output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
(output / 'prompt.txt').write_text(prompt)
paths = [SCOPE, Path(__file__), ROOT / 'scripts/review_wbxbar_reference_repair.py',
    ROOT / 'scripts/prepare_wbxbar_completion_review.py', ROOT / 'scripts/revise_spi_checker_role.py',
    run / 'patches.json', candidate / 'metadata.json', *[candidate / f for f in FILES],
    *[run / 'evaluation-original' / f for f in ('summary.json', 'cases.json', 'limits.json')],
    run / 'focused-inputs.json', run / 'inputs-manifest.json', run / 'evaluation-focused/outputs.json',
    base / 'completion-review-packet-v1/packet.json', base / 'completion-review-v1/review.json']
m = {'status': 'prepared_not_called', 'source_hashes': {str(p): sha(p) for p in paths},
    'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
    'bytes': len(prompt.encode()), 'local_transport_byte_cap': 500000,
    'complete_trace_roundtrips': 158, 'complete_result_roundtrips': 158,
    'planned_calls': 1, 'cli_budget_usd': 4, 'timeout_seconds': 600,
    'requested_model': 'claude-opus-5-5', 'original_control_gate_passed': True,
    'offline_gate_passed': False, 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
(output / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n')
print(json.dumps({k: v for k, v in m.items() if k != 'source_hashes'}, indent=2))
