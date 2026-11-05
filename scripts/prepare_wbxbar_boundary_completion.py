"""Prepare the remaining observed boundary/reporting corrections, not golden code."""
import argparse
import json
from pathlib import Path

from followup_wbxbar_reference_checker import OUTPUT_BASE, FILES, verify as verify_author
from prepare_wbxbar_reference_review import compact, pack_traces, pack_results
from probe_wbxbar_cancel_boundary import SCOPE
from run_midterm_fixed import ROOT, sha

PREFIX = '''You are Claude, the independent specification checker author. Return ONLY JSON with patches (list of {file,before,after}), rationale (list), contract_decisions (list). Allowed files checker.py,selftest.py,properties.json,contract.md. Each before must be a unique nonempty EXACT substring after earlier patches. Preserve check_rows(rows,limits=None), defaults4096/64/256, pure collections/copy/math imports, no I/O/eval/exec/tools/project imports. Make small evidence-driven fixes; do not delete or weaken the failing selftest to obtain a pass. No DUT implementation or actual B/C outcomes are supplied. No freeze/replay/live permission.\n'''


def prepare(output):
    verify_author(OUTPUT_BASE / 'followup-packet-v1')
    parent = OUTPUT_BASE / 'followup-v1/candidate'
    metadata = json.loads((parent / 'metadata.json').read_text())
    for f in FILES:
        if sha(parent / f) != metadata['artifact_sha256'][f]:
            raise ValueError('Current Claude candidate drift')
    prior_packet = json.loads((OUTPUT_BASE / 'followup-packet-v1/packet.json').read_text())
    inputs = json.loads((OUTPUT_BASE / 'followup-v1/focused-inputs.json').read_text())
    results = json.loads((OUTPUT_BASE / 'followup-v1/evaluation-focused/outputs.json').read_text())
    diagnostics = json.loads((OUTPUT_BASE / 'followup-v1/author-test-diagnostic.json').read_text())
    for n, case in diagnostics.items():
        inputs['new_diagnostic/' + n] = {'rows': case['rows'], 'limits': {}}
        results['new_diagnostic/' + n] = case['result']
    evaluated = json.loads((OUTPUT_BASE / 'followup-v1/evaluation-original/cases.json').read_text())
    failures = [x['name'] for x in evaluated['selftests'] if x['pass'] is not True]
    if failures != ['mixed_death_keeps_prefix_tag_open']:
        raise ValueError('Unexpected current selftest failure set')
    body = {
        'specification': prior_packet['specification'], 'approved_reference_design': prior_packet['approved_reference_design'],
        'latest_independent_review': prior_packet['fresh_independent_review'],
        'current_candidate': {f: (parent / f).read_text() for f in FILES},
        'selftest_results': evaluated['selftests'],
        'traces': pack_traces({n: c['rows'] for n, c in inputs.items()}),
        'case_limits': {n: c['limits'] for n, c in inputs.items()},
        'full_results': pack_results(results), 'encoding': prior_packet['encoding'],
        'observed_remaining_issues': [
            'Your mixed_death_keeps_prefix_tag_open test fails: _tag_mixed has first invalid input at8, before the would-be later membership death. _tag_mixed truncated to rows0..7 reports possible_starvation_err@3; adding row8 gives prefix_unresolved but unresolved=[], no membership death. The test exposes a real valid-prefix retention gap. Do not merely change its expected verdict or force the fixture to die earlier. Preserve that case and add a distinct true mixed-death case if useful.',
            'boundary currently preserves row-start tags only for a membership_empty_H reclassified as mixed. Valid-prefix uncertainty also survives any first invalid-input boundary when histories are still active, and schema-validation failures. Preserve a snapshot of genuinely feasible valid-prefix histories before processing the invalid row; do not promote tags created on the invalid row into valid-prefix facts or double-count already emitted tags. All fields must retain original tag cycles and explicit uncertainty classification.',
            'K11_env has raw_activations33 on focused/tag_then_exhaustion, but clause_scope activations/checked/suspended/postdeath are all0 because SUBS has no K11 entry. Environment checks actually execute. Complete its documented scope accounting (including reset/input-validation eligibility if claimed) or explicitly delimit unmeasured subchecks; never silently equate missing instrumentation to zero checking.',
            'The new subobligation accounting looks promising: K7 at the exhaustion case has2 exposures/0 checked/2 suspended and K6_count_bound continues checking. Verify the actual call sites/eligibility, especially after death and at invalid boundary, and ensure units/sub-obligation sums and unknown records are documented and consistent.',
            'contract.md still includes an old proposed P4 paragraph saying all K6 counts at row e stay dut_violation, contradicting the new ACK-only rule. Its old proposed P1 omits the mixed-boundary exception, and the declared status list omits not_activated. Remove or explicitly supersede stale proposals and keep properties.json consistent with the final executable scope.',
            'The new public per-slave FIFO WE rule for undefined read ACK data has live/orphan selftests and no history lookup; preserve explicit assumptions and submitted evidence for independent review. Do not claim the broader semantic or formal obligations are proven.',
        ],
        'constraints': 'All127 normal and6 limit control classifications remain unchanged; 53/54 author tests pass. Keep all successes and the failing test evidence. No budget/driver/DUT/coverage-target changes. Fresh independent code review is still required after offline validation. Only Claude authors functional expected-value or selftest changes.',
        'isolation': 'Current Claude source and17 focused/diagnostic cases only; full133 independent control inputs and all actual experiment results are withheld.'}
    prompt = PREFIX + compact(body)
    if len(prompt.encode()) > 300000:
        raise ValueError('Completion author byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    paths = [SCOPE, Path(__file__), ROOT / 'scripts/followup_wbxbar_reference_checker.py',
             ROOT / 'scripts/repair_wbxbar_reference_checker.py', ROOT / 'scripts/revise_spi_checker_role.py',
             ROOT / 'scripts/run_spi_checker_author.py', parent / 'metadata.json', *[parent / f for f in FILES],
             OUTPUT_BASE / 'followup-v1/focused-inputs.json', OUTPUT_BASE / 'followup-v1/evaluation-focused/outputs.json',
             OUTPUT_BASE / 'followup-v1/evaluation-original/cases.json', OUTPUT_BASE / 'followup-v1/author-test-diagnostic.json',
             OUTPUT_BASE / 'followup-v1/diagnose-author-test.py', OUTPUT_BASE / 'repair-review-v1/review.json']
    m = {'status': 'prepared_not_called', 'parent_candidate': str(parent),
         'source_hashes': {str(p): sha(p) for p in paths}, 'packet_sha256': sha(output / 'packet.json'),
         'prompt_sha256': sha(output / 'prompt.txt'), 'bytes': len(prompt.encode()),
         'complete_trace_roundtrips': len(inputs), 'complete_result_roundtrips': len(results),
         'planned_calls': 1, 'cli_budget_usd': 4, 'timeout_seconds': 600,
         'requested_model': 'claude-opus-5-5', 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    return m


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.output.resolve()), indent=2))
