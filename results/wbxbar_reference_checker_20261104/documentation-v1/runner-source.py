"""Claude-owned documentation-only follow-up and fresh scoped review."""
import argparse
import json
import os
from pathlib import Path

from followup_wbxbar_reference_checker import OUTPUT_BASE, FILES
from probe_wbxbar_cancel_boundary import verify_scope
from repair_wbxbar_reference_checker import apply_exact
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import sha


def run(output):
    verify_scope()
    parent = OUTPUT_BASE / 'termination-v1/candidate'
    review_path = OUTPUT_BASE / 'termination-review-v1/review.json'
    review = json.loads(review_path.read_text())
    if review.get('ready_for_replay_registration') is not True:
        raise ValueError('Code review not ready')
    meta = json.loads((parent / 'metadata.json').read_text())
    source = {f: (parent / f).read_text() for f in FILES}
    if any(sha(parent / f) != meta['artifact_sha256'][f] for f in FILES):
        raise ValueError('Candidate drift')
    if output.exists() or not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise ValueError('Output exists or staged key absent/unsafe')
    output.mkdir(parents=True)
    (output / 'runner-source.py').write_bytes(Path(__file__).read_bytes())
    (output / 'plan.json').write_text(json.dumps({
        'scope': 'Only Claude-authored contract documentation for accepted T2/T4/T5; no functional code/test/properties changes.',
        'planned_calls': 2, 'per_call_cli_budget_usd': 4, 'per_call_timeout_seconds': 600,
        'source_hashes': {str(parent / f): sha(parent / f) for f in FILES},
        'review_sha256': sha(review_path), 'runner_sha256': sha(Path(__file__)),
        'key_policy': 'User authorizes retaining staged key until independent checker validation is complete.'
    }, indent=2) + '\n')
    env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
    try:
        payload = {'current_contract': source['contract.md'], 'checker_source': source['checker.py'], 'accepted_review': review}
        prompt = 'You are the Claude specification checker author. Return ONLY JSON {patches:[{file,before,after}],rationale:[...],contract_decisions:[]}. Only contract.md edits allowed, exact unique substrings. Add the three accepted nonblocking documentation clarifications T2/T4/T5 from this review. No semantic rule, code, test, metric or property change. State exact scope of unknown_tag_records and excluded diagnostics; last processed versus termination cycle; rows_beyond_input_boundary is unprocessed rows for either boundary. Keep all assumptions, exclusions, non-proof claims and existing contract meaning. No tools.\n' + json.dumps(payload, separators=(',', ':'))
        patches = call(prompt, output / 'author-call', env, 'WBXBAR contract documentation author')
        (output / 'patches.json').write_text(json.dumps(patches, indent=2) + '\n')
        if not isinstance(patches, dict) or not patches.get('patches') or any(p.get('file') != 'contract.md' for p in patches['patches']):
            raise ValueError('Documentation author may edit only contract.md')
        updated = apply_exact(source, patches)
        for f in FILES:
            if f != 'contract.md' and source[f] != updated[f]:
                raise ValueError('Functional artifact changed')
        candidate = output / 'candidate'
        candidate.mkdir()
        for f in FILES:
            (candidate / f).write_text(updated[f])
        (candidate / 'metadata.json').write_text(json.dumps({'status': 'documentation_candidate_pending_review',
            'role': 'Claude contract documentation author', 'parent_candidate': str(parent),
            'artifact_sha256': {f: sha(candidate / f) for f in FILES},
            'functional_artifacts_unchanged': ['checker.py', 'selftest.py', 'properties.json'],
            'patch_response_sha256': sha(output / 'patches.json')}, indent=2) + '\n')
        package = {'prior_accepted_review': review, 'before_contract': source['contract.md'],
            'after_contract': updated['contract.md'], 'checker_source': source['checker.py'],
            'author_patches': patches, 'functional_artifacts_unchanged': True}
        prompt = 'Fresh independent read-only Claude documentation review. Return ONLY JSON {ready_for_contract_addendum:boolean,findings:[],limitations:[]}. Verify exact contract changes fulfill accepted T2/T4/T5 without altering specification, assumptions, checker rules, metric definitions, exclusions or readiness meaning. No tools/edits. Prior code review and full158-case evidence remain separately authoritative; this call judges only documentation changes. A positive opinion is not whole-IP proof or permission to run B/C.\n' + json.dumps(package, separators=(',', ':'))
        result = call(prompt, output / 'review-call', env, 'WBXBAR independent contract documentation reviewer')
        (output / 'review.json').write_text(json.dumps(result, indent=2) + '\n')
        valid = isinstance(result, dict) and type(result.get('ready_for_contract_addendum')) is bool and all(isinstance(result.get(k), list) for k in ('findings', 'limitations'))
        validation = {'schema_valid': valid, 'model_readiness': result.get('ready_for_contract_addendum') if valid else None,
            'functional_artifacts_unchanged': True, 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
        (output / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
        return validation
    finally:
        env.pop('ANTHROPIC_API_KEY', None)
        verify_scope()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(run(args.output.resolve()), indent=2))
