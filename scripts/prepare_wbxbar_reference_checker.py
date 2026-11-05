"""Commission an isolated Claude checker from the reviewed reference contract.

This wrapper reuses existing bounded authorship transport and never edits the
generated functional code or authorizes replay/live stimulus generation.
"""
import argparse
import json
import os
from pathlib import Path

from prepare_wbxbar_conformance_role import BASE, PRIOR
from probe_wbxbar_cancel_boundary import SCOPE, verify_scope
from run_midterm_fixed import ROOT, sha
from run_spi_checker_author import invoke

OUTPUT_BASE = ROOT / 'results/wbxbar_reference_checker_20261104'
FILES = ('checker.py', 'selftest.py', 'properties.json', 'contract.md')
PREFIX = '''You are Claude, the independent specification-based functional checker author. GPT implements fixed JSON driver/stimulus and independent validation; you author every functional expected-value rule. Implement the reviewed reference contract, not the previous checker's obsolete matching algorithm. No DUT implementation, real experiment trace, private calibration, coverage or arm outcomes are supplied. This is implementation only, not permission to freeze or run B/C.
Return ONLY JSON with exactly checker_source, selftest_source, properties, contract_markdown. checker_source defines pure Python check_rows(rows, limits=None). rows are complete cumulative public-pin traces, each {cycle,pre,post}; ignore any extra action field. Preserve the public interface and widths from the specification. Return JSON-serializable failures[{cycle,category,detail}], assumption_violations, unresolved, events, verdict and counts. Allowed global verdicts: scoped_pass, dut_violation, input_or_scope_invalid, unresolved. Additional per-clause/prefix statuses go in counts/property_status, not new global verdict strings. A same-edge mixed fault must remain explicit and not be silently discarded. Empty events is acceptable; never invent a recovery event or hidden ownership proof.
Use only collections, copy, math imports and builtins. No I/O, tools, filesystem, network, subprocess, eval/exec, project imports, dynamic attribute access or dunder attributes. No classes are needed. The existing worker will validate source and run it in a separate resource-limited process. selftest_source defines run(check_rows), returning [{name,pass}]. Tests must build their own positive, corruption, ambiguity and resource-limit examples; no hardcoded case names/cycles in the checker. properties lists {id,requirement,source,assumptions,support_status} and matches executable behavior. Formal obligations remain unproved targets.
Implement exact explicit histories, no speculative quotient or partition. Keep multiplicity, typed identity masks, master/slave FIFO references, cancellation/orphan states, generic unknown-tag propagation, exact edge processing order and ERR alternatives. Preserve violations before later invalid input. Do not erase cumulative uncertainty at reset. Include per-clause checked/unknown/suspended scope, pending alternatives, input-validity boundary and declared exclusions in counts. Reports must state that repeated HR ERRs during one held request are not judged; they stay unknown. All scoped_pass claims exclude K5 and unproved characterization C1-C4.
Default limits are exactly the reviewed MAX_HYP=4096, MAX_LIVE_PER_MASTER=64 and MAX_CANCELED_POOL=256. The optional limits dictionary accepts these same names for DEVELOPMENT SELFTESTS ONLY, validates positive integer values, and does not change defaults. Frozen live callers will pass only rows, never model-supplied limits. Lower limits in tests to exercise exhaustion without huge traces. No arbitrary history pruning or invented latency. If an implementation detail is not settled by the reviewed contract, document it as an implementation blocker rather than silently changing semantics or returning a vacuous pass.
The prior checker files are reuse material for parsing/interface/masks only. The reviewed reference contract supersedes older whole-epoch ambiguity suppression and unsupported forwarding-order assumptions. No original artifact is overwritten. Independent controls and a fresh code review will judge the candidate before any new freeze/replay.\n'''


def prepare(output):
    verify_scope()
    review_path = BASE / 'err-boundary-review-v1/review.json'
    review = json.loads(review_path.read_text())
    if review.get('ready_for_implementation') is not True:
        raise ValueError('Reviewed design not ready for implementation')
    design_path = BASE / 'design-patch-v2-retry2/design-location-corrected.json'
    design = json.loads(design_path.read_text())
    source_packet = json.loads((BASE / 'design-patch-packet-v2/packet.json').read_text())
    # Withhold full control traces, expected case assessments and DUT outcomes.
    contract = {k: v for k, v in design.items() if k not in ('control_assessments', 'ready_for_independent_review')}
    body = {'role': 'Claude independent reference checker implementation',
            'specification': source_packet['specification'], 'reviewed_reference_contract': contract,
            'design_review': review, 'prior_claude_artifacts': {f: (PRIOR / f).read_text() for f in FILES},
            'isolation': 'No DUT RTL, actual model-generated stimulus, actual experiment trace, coverage, target witnesses or private full synthetic controls. Prior design review contains illustrative synthetic observations only.',
            'validation_boundary': 'Candidate only. Independent controls, code review, separate freeze and saved-action replay are required before any live B/C. Never alter the existing experimental budget or driver.'}
    prompt = PREFIX + json.dumps(body, separators=(',', ':'))
    if len(prompt.encode()) > 150000:
        raise ValueError('Author byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    paths = [SCOPE, Path(__file__), review_path, design_path,
             BASE / 'design-patch-v2-retry2/location-correction-audit.json',
             ROOT / 'scripts/run_spi_checker_author.py', *[PRIOR / f for f in FILES]]
    scope = json.loads(SCOPE.read_text())
    manifest = {'status': 'prepared_not_called', 'source_hashes': {str(p): sha(p) for p in paths},
                'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
                'bytes': len(prompt.encode()), 'planned_author_calls': 1, 'cli_budget_usd': 4,
                'timeout_seconds': 600, 'implementation_role': 'Claude',
                'original_experiment_budget': scope['development_budget'],
                'original_model_limits': scope['model_limits'],
                'candidate_only': True, 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def verify(packet):
    verify_scope()
    manifest = json.loads((packet / 'manifest.json').read_text())
    for path, digest in manifest['source_hashes'].items():
        if sha(Path(path)) != digest:
            raise ValueError('Checker implementation packet source drift')
    for name, ext in [('packet', 'json'), ('prompt', 'txt')]:
        if sha(packet / (name + '.' + ext)) != manifest[name + '_sha256']:
            raise ValueError('Checker implementation packet drift')
    return manifest


def run(packet, output):
    manifest = verify(packet)
    if output.exists():
        raise ValueError('Never overwrite checker evidence')
    # Prevent inherited alternative credentials/provider settings in this process.
    saved = {k: v for k, v in os.environ.items() if k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
    for key in saved:
        os.environ.pop(key)
    try:
        result = invoke(packet, output, manifest['cli_budget_usd'], manifest['timeout_seconds'])
        return {'author_status': result['status'], 'candidate_only': True,
                'live_B_allowed': False, 'live_C_allowed': False}
    finally:
        os.environ.update(saved)
        verify_scope()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prepare', 'run'])
    parser.add_argument('--packet', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.output.resolve()) if args.mode == 'prepare'
                     else run(args.packet.resolve(), args.output.resolve()), indent=2))
