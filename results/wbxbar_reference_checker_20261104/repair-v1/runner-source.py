"""Commission exact Claude-authored repairs; never silently edit golden logic."""
import argparse
import json
import os
from pathlib import Path

from prepare_wbxbar_reference_review import OUTPUT_BASE, FILES, compact, pack_traces, pack_results, verify as verify_review
from probe_wbxbar_cancel_boundary import SCOPE, verify_scope
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import ROOT, sha
from run_spi_checker_author import validate_source

PREFIX = '''You are Claude, the specification checker author, distinct from GPT driver/stimulus/control authors. Repair your immutable candidate based on the fresh code review and focused synthetic evidence. Return ONLY JSON with patches (list of {file,before,after}), rationale (list), contract_decisions (list). Allowed files checker.py,selftest.py,properties.json,contract.md. Each before is a unique nonempty EXACT substring of the current file after earlier patches. No entire-file rewrite unless essential. Preserve interface check_rows(rows,limits=None) and default4096/64/256. All functional edits must be authored by you. No I/O/tools/project imports, only collections/copy/math imports and builtins, following existing pure-code boundary. Add focused selftests. No DUT implementation or real B/C trajectories/results are supplied. This is a candidate repair only, not certification, freeze, replay or live permission. Decisions extending or clarifying the reviewed contract must be explicitly proposed for a fresh independent review, never claimed as new normative authority.\n'''


def prepare(output):
    verify_review(OUTPUT_BASE / 'code-review-packet-v1')
    candidate = OUTPUT_BASE / 'claude-author-v1'
    repro = OUTPUT_BASE / 'review-repro-v2'
    review = OUTPUT_BASE / 'code-review-v1/review.json'
    evidence = json.loads((repro / 'manifest.json').read_text())
    for p, h in evidence['source_hashes'].items():
        if sha(Path(p)) != h:
            raise ValueError('Reproducer drift')
    original = json.loads((OUTPUT_BASE / 'spec-packet-v1/packet.json').read_text())
    probes = json.loads((repro / 'inputs.json').read_text())
    outputs = json.loads((repro / 'outputs.json').read_text())
    transport = json.loads((OUTPUT_BASE / 'code-review-packet-v1/packet.json').read_text())['encoding']
    body = {
        'specification': original['specification'], 'reviewed_reference_contract': original['reviewed_reference_contract'],
        'current_candidate': {f: (candidate / f).read_text() for f in FILES},
        'fresh_independent_review': json.loads(review.read_text()),
        'focused_controls': {n: {k: v for k, v in r.items() if k != 'rows'} for n, r in probes.items()},
        'focused_traces': pack_traces({n: r['rows'] for n, r in probes.items()}),
        'focused_results': pack_results(outputs), 'encoding': transport,
        'integration_questions_not_golden_rules': [
            'F1 reproduced: tag_then_clean_completion retains possible_starvation_err@8; exhaustion@15 and death@19 lose it and omit reset_epoch2. Preserve evidence before losing H, distinguishing pre-suspension feasible uncertainty from histories later refuted by a concrete violation. Do not label a disproved history as a true hidden-owner fact or erase a later fault. Define what the retained epoch record means.',
            'F2: define each clause/subcheck activation unit and checked/unknown/suspended accounting. Idle rows must not masquerade as triggered ERR/cancellation/response properties. Include not_activated where appropriate and per-clause scope, without making zero activation a new DUT violation or a formal-proof claim.',
            'F3 reproduced:90 histories but16 pending/tag displays. State totals, displayed/omitted counts and truncation. The 8-witness cap also needs explicit counts. Do not prune actual histories to make reporting small.',
            'F4 factual caution: the review states both projections count row-e acceptances. In current code K6 nacc explicitly filters x<c; K4 idm includes current-row accepts. Assess them separately with input dependency, valid-prefix and mixed-edge rules. The two duplicate-ACK controls expose the distinction; their labels are not imposed. Resolve the proposed policy explicitly for independent review.',
            'F5: resolve or explicitly scope each self-declared blocker in contract.md: B2 already forwarded on acceptance edge, hypothesis-dependent undefined slave read data, undefined pre DUT control, first-row K13 and other listed decisions. The integer fixed driver cannot emit null, but public checker input scope must be explicit and sound. Never assert unsupported normative certainty.',
            'Keep all reviewed ordinary checks, multiplicity, branching, unknown alternatives, existing exclusions and formal-unproved labels. Full heldback controls will be rerun independently. Keep old candidate and results untouched. No model-generated experiments or witnesses enter this packet.',
        ],
        'provenance': 'Nine focused synthetic probes authored by GPT. The first HR-forward probe incorrectly used SEL15 versus accepted SEL5; v1 is retained as a negative mismatched-identity control, not evidence about B2. The supplied v2 only corrects forward identity to match the accepted tuple and preserves all other eight traces. No DUT traces or B/C data.',
    }
    prompt = PREFIX + compact(body)
    if len(prompt.encode()) > 300000:
        raise ValueError('Repair packet byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    paths = [SCOPE, Path(__file__), ROOT / 'scripts/revise_spi_checker_role.py',
             ROOT / 'scripts/run_spi_checker_author.py', ROOT / 'scripts/prepare_wbxbar_reference_review.py',
             review, repro / 'manifest.json', repro / 'inputs.json', repro / 'outputs.json',
             *[candidate / f for f in FILES]]
    m = {'status': 'prepared_not_called', 'source_hashes': {str(p): sha(p) for p in paths},
         'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
         'bytes': len(prompt.encode()), 'planned_calls': 1, 'cli_budget_usd': 4,
         'timeout_seconds': 600, 'requested_model': 'claude-opus-5-5',
         'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    return m


def verify(packet):
    verify_review(OUTPUT_BASE / 'code-review-packet-v1')
    m = json.loads((packet / 'manifest.json').read_text())
    for p, h in m['source_hashes'].items():
        if sha(Path(p)) != h:
            raise ValueError('Repair source drift')
    for name, ext in [('packet', 'json'), ('prompt', 'txt')]:
        if sha(packet / (name + '.' + ext)) != m[name + '_sha256']:
            raise ValueError('Repair packet drift')
    return m


def apply_exact(sources, result):
    if not isinstance(result, dict) or any(not isinstance(result.get(k), list) for k in ('patches', 'rationale', 'contract_decisions')):
        raise ValueError('Repair response schema')
    updated = dict(sources)
    if not result['patches']:
        raise ValueError('No repair patches')
    for item in result['patches']:
        f, before, after = item['file'], item['before'], item['after']
        if f not in FILES or not isinstance(before, str) or not before or not isinstance(after, str) or updated[f].count(before) != 1:
            raise ValueError('Repair patch must match exactly once; never guess')
        updated[f] = updated[f].replace(before, after, 1)
    validate_source(updated['checker.py'])
    validate_source(updated['selftest.py'])
    json.loads(updated['properties.json'])
    return updated


def run(packet, output):
    verify(packet)
    if output.exists():
        raise ValueError('Never overwrite repair evidence')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise ValueError('Hidden key absent or unsafe')
    output.mkdir()
    (output / 'runner-source.py').write_bytes(Path(__file__).read_bytes())
    env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
    try:
        result = call((packet / 'prompt.txt').read_text(), output / 'author-call', env, 'WBXBAR specification checker author repair')
        (output / 'patches.json').write_text(json.dumps(result, indent=2) + '\n')
        original = OUTPUT_BASE / 'claude-author-v1'
        updated = apply_exact({f: (original / f).read_text() for f in FILES}, result)
        candidate = output / 'candidate'
        candidate.mkdir()
        for f, source in updated.items():
            (candidate / f).write_text(source)
        meta = {'status': 'candidate_generated_not_validated', 'role': 'Claude checker author',
                'parent_checker_sha256': sha(original / 'checker.py'), 'patch_response_sha256': sha(output / 'patches.json'),
                'artifact_sha256': {f: sha(candidate / f) for f in FILES},
                'authorship_policy': 'Only exact Claude-authored patch text; no GPT edits. Decisions require independent review.'}
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
