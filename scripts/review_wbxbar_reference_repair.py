"""Fresh review of exact Claude repairs, failing selftest and complete evidence."""
import argparse
import json
import os
from pathlib import Path

from prepare_wbxbar_reference_review import OUTPUT_BASE, FILES, compact, pack_results, pack_traces, unpack_traces
from repair_wbxbar_reference_checker import verify as verify_repair, apply_exact
from probe_wbxbar_cancel_boundary import SCOPE, verify_scope
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import ROOT, sha

PREFIX = '''Fresh independent read-only Claude review. Return ONLY JSON with ready_for_replay_registration (boolean), findings (list), contract_decision_assessments (list), required_followup (list), limitations (list). No edits/tools. The repaired candidate has a FAILED author selftest and unresolved reporting requirements: do not treat control agreement as certification. Adjudicate proposed P1-P5 against public sources and the prior reviewed contract; never simply accept GPT integration questions or Claude author assertions. Identify exact minimal author corrections and valid control expectations. A positive opinion cannot override failing offline gates, freeze anything, or authorize B/C.\n'''


def prepare(output):
    verify_repair(OUTPUT_BASE / 'repair-packet-v1')
    repair = OUTPUT_BASE / 'repair-v1'
    candidate = repair / 'candidate'
    previous = OUTPUT_BASE / 'claude-author-v1'
    patches = json.loads((repair / 'patches.json').read_text())
    rebuilt = apply_exact({f: (previous / f).read_text() for f in FILES}, patches)
    metadata = json.loads((candidate / 'metadata.json').read_text())
    for f in FILES:
        if rebuilt[f] != (candidate / f).read_text() or sha(candidate / f) != metadata['artifact_sha256'][f]:
            raise ValueError('Candidate is not exact Claude patch result')
    body = json.loads((OUTPUT_BASE / 'code-review-packet-v1/packet.json').read_text())
    traces = unpack_traces(body['traces'])
    normal = json.loads((repair / 'evaluation-original/cases.json').read_text())
    limits = json.loads((repair / 'evaluation-original/limits.json').read_text())
    results = {**normal['cases'], **{'limit/' + n: r for n, r in limits.items()}}
    focused = json.loads((OUTPUT_BASE / 'review-repro-v2/inputs.json').read_text())
    focused_results = json.loads((repair / 'evaluation-focused/outputs.json').read_text())
    for n, case in focused.items():
        name = 'focused/' + n
        traces[name] = case['rows']
        results[name] = focused_results[n]
        body['expectations'].append({'name': name, 'kind': 'focused_synthetic_no_imposed_label',
                                     **{k: v for k, v in case.items() if k != 'rows'}})
    diagnostics = json.loads((repair / 'selftest-diagnostic.json').read_text())['cases']
    for n, case in diagnostics.items():
        name = 'diagnostic/' + n
        traces[name] = case['rows']
        results[name] = case['candidate']
        body['expectations'].append({'name': name, 'kind': 'author_selftest' if n.startswith('author_') else 'additional_synthetic',
                                     'expected': 'not imposed; assess boundary and evidence semantics independently'})
    if set(traces) != set(results):
        raise ValueError('Missing result or trace')
    body.update(
        role='Fresh independent repaired-checker and proposed-contract reviewer',
        candidate={f: (candidate / f).read_text() for f in FILES},
        traces=pack_traces(traces), full_checker_results=pack_results(results),
        selftest_results=normal['selftests'], worker_errors=normal['errors'],
        prior_code_review=json.loads((OUTPUT_BASE / 'code-review-v1/review.json').read_text()),
        author_rationale=patches['rationale'], proposed_contract_decisions=patches['contract_decisions'],
        diagnostic_prior_results={n: c['prior'] for n, c in diagnostics.items()},
        integration_questions=[
            'The old mixed_same_edge_explicit author selftest still expects input_or_scope_invalid; P4 keeps K6 count failure and now yields dut_violation plus same-edge unknown. No selftest was edited by GPT. Independently decide whether this test expectation or the new rule is wrong, with precise input dependencies. K6 uses prior acceptances but HR classification uses current held/accept conditions; do not assume all ERR and ACK cases have identical dependency.',
            'P2 adds raw clause_activations but still no per-clause checked/unknown/suspended counts. The tag_then_exhaustion trace reports K7 activations after the association checks have stopped. Does the report meet the reviewed scope requirements? Specify activation versus checked sub-obligations and suspended/unknown accounting rather than an unqualified activation counter.',
            'The tagged invalid-boundary diagnostic has input_or_scope_invalid and mixed_same_edge at19 but discarded_epoch_evidence calls its histories refuted by a concrete contradiction. Is this consistent with the contract withholding DUT judgment at that boundary? The original possible_starvation_err@8 is absent from unresolved. Distinguish tentative/refuted historical evidence from cumulative valid-prefix uncertainty.',
            'P1 expressly omits tags created in a dying row. Evaluate this limitation, row-start snapshots and projected pre-expansion history counts at resource exhaustion. Do not label invalid-row refutation as proved.',
            'Check all P1-P5 decisions, stale blocker text, unchanged properties.json, selftest consistency and actual code. The core 127+6 classifications still agree, but one of46 author tests fails; therefore offline gate is false. All 144 complete raw traces/results are supplied, not just selected successes. State whether your review fully decodes them or spot-checks.',
        ],
        gate_status={'author_selftests_passed': sum(x['pass'] is True for x in normal['selftests']),
                     'author_selftests_total': len(normal['selftests']),
                     'original_control_agreements': 127, 'limit_control_agreements': 6,
                     'offline_gate_passed': False, 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False},
    )
    prompt = PREFIX + compact(body)
    if len(prompt.encode()) > 500000:
        raise ValueError('Complete repaired-code review byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    paths = [SCOPE, Path(__file__), ROOT / 'scripts/prepare_wbxbar_reference_review.py', ROOT / 'scripts/revise_spi_checker_role.py',
             repair / 'patches.json', candidate / 'metadata.json', *[candidate / f for f in FILES],
             repair / 'evaluation-original/summary.json', repair / 'evaluation-original/cases.json',
             repair / 'evaluation-original/limits.json', repair / 'evaluation-focused/outputs.json',
             repair / 'selftest-diagnostic.json', repair / 'diagnose-selftest.py',
             OUTPUT_BASE / 'review-repro-v2/inputs.json', OUTPUT_BASE / 'code-review-packet-v1/packet.json',
             OUTPUT_BASE / 'code-review-v1/review.json']
    m = {'status': 'prepared_not_called', 'source_hashes': {str(p): sha(p) for p in paths},
         'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
         'bytes': len(prompt.encode()), 'local_transport_byte_cap': 500000,
         'complete_trace_roundtrips': len(traces), 'complete_result_roundtrips': len(results),
         'planned_calls': 1, 'cli_budget_usd': 4, 'timeout_seconds': 600,
         'requested_model': 'claude-opus-5-5', 'offline_gate_passed': False,
         'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    return m


def verify(packet):
    verify_repair(OUTPUT_BASE / 'repair-packet-v1')
    m = json.loads((packet / 'manifest.json').read_text())
    for p, h in m['source_hashes'].items():
        if sha(Path(p)) != h:
            raise ValueError('Repaired review source drift')
    for name, ext in [('packet', 'json'), ('prompt', 'txt')]:
        if sha(packet / (name + '.' + ext)) != m[name + '_sha256']:
            raise ValueError('Repaired review packet drift')
    return m


def run(packet, output):
    verify(packet)
    if output.exists():
        raise ValueError('Never overwrite review')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise ValueError('Hidden key absent or unsafe')
    env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
    try:
        result = call((packet / 'prompt.txt').read_text(), output, env, 'WBXBAR independent repaired-code reviewer')
        (output / 'review.json').write_text(json.dumps(result, indent=2) + '\n')
        (output / 'runner-source.py').write_bytes(Path(__file__).read_bytes())
        valid = isinstance(result, dict) and type(result.get('ready_for_replay_registration')) is bool and all(
            isinstance(result.get(k), list) for k in ('findings', 'contract_decision_assessments', 'required_followup', 'limitations'))
        validation = {'schema_valid': valid, 'model_readiness': result.get('ready_for_replay_registration') if valid else None,
                      'offline_gate_passed': False, 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
        (output / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
        return validation
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
    print(json.dumps(prepare(args.output.resolve()) if args.mode == 'prepare' else run(args.packet.resolve(), args.output.resolve()), indent=2))
