"""Scoped wrapper around the existing bounded author/fresh-review transport."""
import argparse
import json
from pathlib import Path

import run_i2c_checker_roles as transport
from prepare_wbxbar_checker_role import verify_packet, SCOPE
from run_midterm_fixed import sha


def run(packet, output, prior=None):
    # Fail before touching credentials or invoking any model.
    if prior is None:
        verify_packet(packet)
    else:
        kind = json.loads((packet / 'manifest.json').read_text()).get('role')
        if kind == 'claude_exact_checker_repair':
            from prepare_wbxbar_checker_repair import verify_packet as verify_repair
        elif kind == 'claude_abort_checker_repair':
            from prepare_wbxbar_abort_repair import verify_packet as verify_repair
        else:
            raise ValueError('Unrecognized repair packet role')
        verify_repair(packet, prior)
    original = transport.call
    def call(prompt, path, env, role):
        return original(prompt, path, env, role.replace('I2C', 'WBXBAR'))
    transport.call = call
    try:
        if prior is None:
            transport.run(packet, output)
        else:
            transport.run(packet, output, prior)
    finally:
        transport.call = original
        if output.exists():
            (output / 'role-wrapper.json').write_text(json.dumps({
                'scope_sha256': sha(SCOPE), 'wrapper_sha256': sha(Path(__file__)),
                'transport_sha256': sha(Path(transport.__file__)),
                'role': 'Claude spec-only author; fresh read-only reviewer after independent controls. GPT authors driver/stimulus.',
                'live_B_or_C_authorization': False}, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--prior', type=Path)
    args = parser.parse_args()
    run(args.packet.resolve(), args.output.resolve(), args.prior.resolve() if args.prior else None)
