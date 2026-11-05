"""Prepare a reviewed follow-up and apply only exact Claude source patches."""
import argparse
import copy
import json
import os
from pathlib import Path

from prepare_wbxbar_reference_review import OUTPUT_BASE, FILES, compact, pack_results, pack_traces
from review_wbxbar_reference_repair import verify as verify_review
from repair_wbxbar_reference_checker import apply_exact
from probe_wbxbar_cancel_boundary import SCOPE, verify_scope
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import ROOT, sha
from wbxbar_checker_controls import settle

PREFIX = '''You are Claude, the independent specification-checker author. GPT supplies transport and synthetic controls, not golden logic. Return ONLY JSON with patches (list of {file,before,after}), rationale (list), contract_decisions (list). Allowed files checker.py,selftest.py,properties.json,contract.md. Each before must uniquely and exactly match the current file after earlier patches; never rewrite whole files unnecessarily. Preserve pure check_rows(rows,limits=None), imports limited to collections/copy/math, no I/O/eval/exec/tools/project imports, default limits4096/64/256, fixed interface and roles. Implement the fresh review's targeted repairs, reconcile selftests and documents, and add meaningful companion controls. A claim in a review is not automatically normative authority: resolve factual contradictions and explicitly retain unproved gaps. No DUT RTL, actual B/C results or complete private control corpus is supplied. New candidate only: no freeze, replay or B/C permission.\n'''


def err_controls():
    source = json.loads((OUTPUT_BASE / 'repair-v1/selftest-diagnostic.json').read_text())['cases']['author_mixed_same_edge']['rows']
    cases = {}
    for invalid in (False, True):
        rows = copy.deepcopy(source)
        rows[3]['pre']['o_merr'] = rows[3]['pre']['o_mack']
        rows[3]['pre']['o_mack'] = 0
        if not invalid:
            for k, w in [('i_mwe', 1), ('i_maddr', 8), ('i_msel', 4), ('i_mdata', 32)]:
                mask = (1 << w) - 1
                rows[3]['pre'][k] = (rows[3]['pre'][k] & ~mask) | (rows[2]['pre'][k] & mask)
        name = 'err_same_edge_invalid' if invalid else 'err_clean_baseline'
        cases[name] = {'rows': settle(rows), 'limits': {},
            'expected_after_reviewed_repair': 'input_or_scope_invalid' if invalid else 'dut_violation',
            'expectation_authority': 'repair-review-v1 R2 / required_followup: ERR-driven K6 count at invalid boundary remains mixed; clean baseline continues ordinary error checks.'}
    return cases


def prepare(output):
    verify_review(OUTPUT_BASE / 'repair-review-packet-v1')
    parent = OUTPUT_BASE / 'repair-v1/candidate'
    review_path = OUTPUT_BASE / 'repair-review-v1/review.json'
    review = json.loads(review_path.read_text())
    if review['ready_for_replay_registration'] is not False:
        raise ValueError('Expected retained blocking review')
    origin = json.loads((OUTPUT_BASE / 'spec-packet-v1/packet.json').read_text())
    full_review = json.loads((OUTPUT_BASE / 'repair-review-packet-v1/packet.json').read_text())
    probes = json.loads((OUTPUT_BASE / 'review-repro-v2/inputs.json').read_text())
    rows = {'focused/' + n: x['rows'] for n, x in probes.items()}
    outputs = {'focused/' + n: x for n, x in json.loads((OUTPUT_BASE / 'repair-v1/evaluation-focused/outputs.json').read_text()).items()}
    diagnostic = json.loads((OUTPUT_BASE / 'repair-v1/selftest-diagnostic.json').read_text())['cases']
    for n, x in diagnostic.items():
        rows['diagnostic/' + n] = x['rows']
        outputs['diagnostic/' + n] = x['candidate']
    err = err_controls()
    if err != json.loads((OUTPUT_BASE / 'repair-followup-controls-v1/inputs.json').read_text()):
        raise ValueError('ERR companion control differs from deterministic builder')
    for n, x in err.items():
        rows['companion/' + n] = x['rows']
    outputs.update({'companion/' + n: x for n, x in json.loads((OUTPUT_BASE / 'repair-followup-controls-v1/outputs.json').read_text()).items()})
    body = {
        'specification': origin['specification'], 'approved_reference_design': origin['reviewed_reference_contract'],
        'current_candidate': {f: (parent / f).read_text() for f in FILES},
        'fresh_independent_review': review, 'selftest_results': full_review['selftest_results'],
        'focused_traces': pack_traces(rows), 'focused_results': pack_results(outputs),
        'encoding': full_review['encoding'],
        'companion_control_basis': {n: {k: v for k, v in x.items() if k != 'rows'} for n, x in err.items()},
        'requirements_and_questions': [
            'R2: reviewer accepts ACK-specific P4 and requires the ACK selftest to be updated by you. For ERR-driven K6 count failure at an invalid-input boundary, keep mixed_same_edge. Add ERR clean-baseline and invalid-boundary tests; the supplied pair reproduces the current overstrong verdict. Do not suppress ordinary ERR detection on valid traces.',
            'R3: invalid-row membership death later reclassified as mixed is not a definite refutation. Retain valid-prefix tags as open unknowns with original tag cycles; do not retain contradictory concrete-refutation wording. Definite valid-row deaths still keep diagnostic historical evidence separately and never hide a real failure.',
            'R4: explicitly disclose pre-expansion versus post-expansion snapshot and actual versus projected hypothesis count at exhaustion. Disclose any omitted dying-row tags per event, not just prose.',
            'R5: implement per-clause/sub-obligation activations, actually checked activations, suspended activations, post-death activations, unknown-tag counts, with exact units and eligibility. Split association-free projections from association-dependent checks so checks continuing during suspension retain honest counts. Raw activations are not checked coverage. Preserve exclusions and not_activated behavior; do not claim formal cover/proof.',
            'R7 caveat: its suggested "association-free" undefined-read rule still refers to "any history", so that wording alone does not remove association dependence. Either justify an independent public-pin FIFO projection and test it, or explicitly retain the limited unresolved contract gap permitted by the reviewer. Do not silently call a hypothesis-dependent rule independent. Preserve the integer driver interface and all unsupported-input disclosures.',
            'R8: synchronize properties.json and contract.md including revised ACK/ERR split, activation/scope fields, hr_err_unjudged and accepted versus open P1-P5 decisions. Remove obsolete blocker text only where actually resolved; do not assert new normative authority.',
            'Do not weaken any checker to preserve an old label. Keep exact histories, cancellation multiplicity, original default bounds and prior failures. All133 independent controls plus the focused/diagnostic/companion traces will run before a new review. No partial success overrides a failing selftest or unsettled contract.',
        ],
        'isolation': 'Specification-only author context plus own source, independent review and13 focused/diagnostic/companion traces; no DUT implementation, actual pilot data, target witness, coverage or performance ranking. Full133 independent controls withheld.',
    }
    prompt = PREFIX + compact(body)
    if len(prompt.encode()) > 300000:
        raise ValueError('Follow-up author byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    paths = [SCOPE, Path(__file__), review_path, ROOT / 'scripts/repair_wbxbar_reference_checker.py',
             ROOT / 'scripts/revise_spi_checker_role.py', ROOT / 'scripts/run_spi_checker_author.py',
             *[parent / f for f in FILES], parent / 'metadata.json',
             OUTPUT_BASE / 'repair-v1/evaluation-original/summary.json',
             OUTPUT_BASE / 'repair-v1/evaluation-focused/outputs.json',
             OUTPUT_BASE / 'repair-v1/selftest-diagnostic.json',
             OUTPUT_BASE / 'repair-followup-controls-v1/inputs.json',
             OUTPUT_BASE / 'repair-followup-controls-v1/outputs.json']
    m = {'status': 'prepared_not_called', 'parent_candidate': str(parent),
         'source_hashes': {str(p): sha(p) for p in paths}, 'packet_sha256': sha(output / 'packet.json'),
         'prompt_sha256': sha(output / 'prompt.txt'), 'bytes': len(prompt.encode()),
         'complete_trace_roundtrips': len(rows), 'complete_result_roundtrips': len(outputs),
         'planned_calls': 1, 'cli_budget_usd': 4, 'timeout_seconds': 600,
         'requested_model': 'claude-opus-5-5', 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    return m


def verify(packet):
    verify_scope()
    m = json.loads((packet / 'manifest.json').read_text())
    for path, digest in m['source_hashes'].items():
        if sha(Path(path)) != digest:
            raise ValueError('Follow-up author source drift')
    for name, ext in [('packet', 'json'), ('prompt', 'txt')]:
        if sha(packet / (name + '.' + ext)) != m[name + '_sha256']:
            raise ValueError('Follow-up packet drift')
    parent = Path(m['parent_candidate'])
    metadata = json.loads((parent / 'metadata.json').read_text())
    for f in FILES:
        if sha(parent / f) != metadata['artifact_sha256'][f]:
            raise ValueError('Parent candidate drift')
    return m


def run(packet, output):
    m = verify(packet)
    if output.exists():
        raise ValueError('Never overwrite candidate evidence')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise ValueError('Hidden key absent or unsafe')
    output.mkdir(parents=True)
    (output / 'runner-source.py').write_bytes(Path(__file__).read_bytes())
    parent = Path(m['parent_candidate'])
    env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
    try:
        result = call((packet / 'prompt.txt').read_text(), output / 'author-call', env, 'WBXBAR specification checker follow-up author')
        (output / 'patches.json').write_text(json.dumps(result, indent=2) + '\n')
        updated = apply_exact({f: (parent / f).read_text() for f in FILES}, result)
        candidate = output / 'candidate'
        candidate.mkdir()
        for f, text in updated.items():
            (candidate / f).write_text(text)
        meta = {'status': 'candidate_generated_not_validated', 'role': 'Claude checker author',
                'parent_checker_sha256': sha(parent / 'checker.py'), 'patch_response_sha256': sha(output / 'patches.json'),
                'artifact_sha256': {f: sha(candidate / f) for f in FILES},
                'authorship_policy': 'Only exact Claude-authored patch text; no GPT functional code or selftest edits.'}
        (candidate / 'metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
        return {'candidate': str(candidate), 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
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
