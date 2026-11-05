"""Prepare a Claude-owned termination-reporting patch from reviewed evidence."""
import argparse
import copy
import json
from pathlib import Path
import sys

from evaluate_wbxbar_reference_checker import isolated
from followup_wbxbar_reference_checker import OUTPUT_BASE, FILES, verify as verify_author
from prepare_wbxbar_completion_review import pack_review_results
from review_wbxbar_reference_repair import verify as verify_review
from probe_wbxbar_cancel_boundary import SCOPE
from run_midterm_fixed import ROOT, sha

PREFIX = '''You are Claude, the independent specification-checker author. Return ONLY JSON with patches (list of {file,before,after}), rationale (list), contract_decisions (list). Allowed files checker.py,selftest.py,properties.json,contract.md. Each before must uniquely and exactly match after earlier patches. Make a targeted repair of the reviewed undefined-DUT-output termination/reporting path only. Keep the genuine DUT failure; do not broaden assumptions, weaken rules, delete tests or invent timeout/cancellation semantics. Preserve pure check_rows(rows,limits=None), current defaults4096/64/256, imports collections/copy/math only, no I/O/eval/exec/tools/project imports. No DUT implementation or actual B/C result is supplied. New candidate only, no freeze/replay/live permission.\n'''


def extra_controls():
    run = OUTPUT_BASE / 'completion-v1'
    focused = json.loads((run / 'focused-inputs.json').read_text())
    boundary = json.loads((run / 'boundary-inputs.json').read_text())
    cases = {}
    for name, source in [('undefined_after_suspension', 'focused/tag_then_exhaustion'),
                         ('undefined_after_valid_membership_failure', 'focused/tag_then_membership_death')]:
        case = copy.deepcopy(focused[source])
        row = copy.deepcopy(case['rows'][-1])
        row['cycle'] += 1
        row['pre']['o_mstall'] = None
        case['rows'].append(row)
        cases[name] = case
    case = copy.deepcopy(boundary['undefined_DUT_control'])
    row = copy.deepcopy(focused['focused/idle_no_error_or_abort']['rows'][0])
    row['cycle'] = case['rows'][-1]['cycle'] + 1
    case['rows'].append(row)
    cases['undefined_with_ignored_reset_suffix'] = case
    return cases


def prepare(output, controls_output):
    verify_author(OUTPUT_BASE / 'completion-packet-v1')
    verify_review(OUTPUT_BASE / 'completion-review-packet-v1')
    review_path = OUTPUT_BASE / 'completion-review-v1/review.json'
    review = json.loads(review_path.read_text())
    if review.get('ready_for_replay_registration') is not False:
        raise ValueError('Expected reviewed reporting gap')
    parent = OUTPUT_BASE / 'completion-v1/candidate'
    meta = json.loads((parent / 'metadata.json').read_text())
    for f in FILES:
        if sha(parent / f) != meta['artifact_sha256'][f]:
            raise ValueError('Candidate drift')
    controls_output.mkdir(parents=True, exist_ok=False)
    extras = extra_controls()
    (controls_output / 'inputs.json').write_text(json.dumps(extras, indent=2) + '\n')
    command = [sys.executable, '-I', str(ROOT / 'scripts/evaluate_wbxbar_reference_checker.py'),
        '--limit-worker', '--candidate', str(parent), '--inputs', str(controls_output / 'inputs.json'),
        '--output', str(controls_output / 'outputs.json')]
    (controls_output / 'command.json').write_text(json.dumps(command, indent=2) + '\n')
    isolated(command, controls_output / 'worker.log')
    run = OUTPUT_BASE / 'completion-v1'
    cases = json.loads((run / 'boundary-inputs.json').read_text())
    results = json.loads((run / 'evaluation-boundary/outputs.json').read_text())
    name = 'new_diagnostic/valid_prefix_before_first_invalid_row'
    cases['valid_prefix'] = json.loads((run / 'focused-inputs.json').read_text())[name]
    results['valid_prefix'] = json.loads((run / 'evaluation-focused/outputs.json').read_text())[name]
    cases.update(extras)
    results.update(json.loads((controls_output / 'outputs.json').read_text()))
    if any(r.get('infrastructure_error') for r in results.values()):
        raise ValueError('Diagnostic worker failure')
    origin = json.loads((OUTPUT_BASE / 'completion-packet-v1/packet.json').read_text())
    body = {
        'specification': origin['specification'], 'approved_reference_design': origin['approved_reference_design'],
        'current_candidate': {f: (parent / f).read_text() for f in FILES},
        'fresh_independent_review': review,
        'complete_cases': cases, 'full_results': pack_review_results(results),
        'encoding': 'complete_cases supplies full raw rows and limits; preserve deliberate missing fields and cycle gaps. full_results has paths and records: decode records in insertion order. value is complete JSON; otherwise deep-copy base, delete each paths[index] in delete and assign each [index,value] in set. Empty path replaces root; arrays are whole. No diagnostics or counters omitted.',
        'observations': [
            'Review N1/N2 are independently confirmed. The pd-only row8 records K10 failure + unjudgeable_row but omits possible_starvation_err@3 and the active epoch with2 pending live entries per history; prefix_status=null, K6=checked_not_refuted and K12=not_activated. Keep the DUT failure, retain valid-prefix evidence, report pending work and appropriate prefix-qualified scope.',
            'Undefined DUT output is not an environment violation. Keep input-validity and DUT-termination reasons distinguishable; do not relabel the failure as mixed or input-invalid. A suggested boundary/closure call in the review is an implementation hint, not authority to mislabel termination as reset or normal batch end.',
            'Preserve previous valid-row failures, already-flushed suspended tags without double-counting, and definite refuted-history disclosure. Extra controls append pd-only termination after suspension or after a valid membership failure. A reset suffix after the first unjudgeable row must remain unprocessed. Choose and document faithful prefix snapshot/closure units and termination timing.',
            'Add meaningful author selftests for the reviewed path, including retained tag, pending entries and scope statuses. Current54 selftests and127+6 independent classifications pass; preserve all. Full155 reviewed cases plus3 supplementary controls will rerun before fresh review. Do not just change expected labels.',
            'N3/N4/P4 are accepted by the fresh reviewer; pin-FIFO undefined read data is accepted only as a scoped non-normative assumption. Keep that delimitation, K5/C1-C4 exclusions, F1-F8 unproved status and repeated HR ERR unknowns. No changes to experimental driver/targets/budgets.',
        ],
        'isolation': 'Only9 focused synthetic/prefix/termination traces and current code/spec/review; full133 independent controls, DUT implementation and actual B/C results withheld. GPT supplies controls/transport, Claude alone changes checker rules and selftests.',
    }
    prompt = PREFIX + json.dumps(body, separators=(',', ':'), ensure_ascii=False)
    if len(prompt.encode()) > 300000:
        raise ValueError('Termination author transport cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    paths = [SCOPE, Path(__file__), ROOT / 'scripts/followup_wbxbar_reference_checker.py',
        ROOT / 'scripts/repair_wbxbar_reference_checker.py', ROOT / 'scripts/revise_spi_checker_role.py',
        ROOT / 'scripts/prepare_wbxbar_completion_review.py', ROOT / 'scripts/evaluate_wbxbar_reference_checker.py',
        parent / 'metadata.json', *[parent / f for f in FILES], review_path,
        *[run / (k + '-inputs.json') for k in ('focused', 'boundary')],
        *[run / ('evaluation-' + k) / 'outputs.json' for k in ('focused', 'boundary')],
        controls_output / 'inputs.json', controls_output / 'outputs.json']
    m = {'status': 'prepared_not_called', 'parent_candidate': str(parent),
        'source_hashes': {str(p): sha(p) for p in paths}, 'packet_sha256': sha(output / 'packet.json'),
        'prompt_sha256': sha(output / 'prompt.txt'), 'bytes': len(prompt.encode()),
        'complete_trace_roundtrips': len(cases), 'complete_result_roundtrips': len(results),
        'planned_calls': 1, 'cli_budget_usd': 4, 'timeout_seconds': 600,
        'requested_model': 'claude-opus-5-5', 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    return m


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--controls-output', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(prepare(args.output.resolve(), args.controls_output.resolve()), indent=2))
