"""User-authorized review transport retaining the staged key until validation."""
import argparse
import json
import os
from pathlib import Path

from review_wbxbar_reference_repair import verify
from probe_wbxbar_cancel_boundary import verify_scope
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import sha


def run(packet, output):
    verify(packet)
    if output.exists():
        raise ValueError('Never overwrite review evidence')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise ValueError('Hidden key absent or unsafe')
    env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
    try:
        result = call((packet / 'prompt.txt').read_text(), output, env, 'WBXBAR independent termination-code reviewer')
        (output / 'review.json').write_text(json.dumps(result, indent=2) + '\n')
        valid = isinstance(result, dict) and type(result.get('ready_for_replay_registration')) is bool and all(
            isinstance(result.get(k), list) for k in ('findings', 'contract_decision_assessments', 'required_followup', 'limitations'))
        validation = {'schema_valid': valid, 'model_readiness': result.get('ready_for_replay_registration') if valid else None,
            'checker_validated': False, 'replay_allowed': False, 'live_B_allowed': False, 'live_C_allowed': False}
        (output / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
        return validation
    finally:
        env.pop('ANTHROPIC_API_KEY', None)
        if output.exists():
            (output / 'runner-source.py').write_bytes(Path(__file__).read_bytes())
            (output / 'credential-policy.json').write_text(json.dumps({
                'policy': 'User explicitly authorizes retaining staged key through the checker review/repair cycle; delete after independent validation, not after each call.',
                'retained_after_call': KEY_FILE.exists(), 'key_content_logged': False,
                'runner_sha256': sha(Path(__file__)), 'packet_manifest_sha256': sha(packet / 'manifest.json'),
                'per_call_cli_budget_usd': 4, 'per_call_timeout_seconds': 600,
            }, indent=2) + '\n')
        verify_scope()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.packet.resolve(), args.output.resolve()), indent=2))
