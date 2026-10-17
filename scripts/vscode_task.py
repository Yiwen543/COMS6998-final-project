#!/usr/bin/env python3
"""VS Code task entrypoints with a stable cwd and explicit local tool paths."""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['doctor', 'step1', 'preview', 'smoke',
                                         'test-agent', 'test-all', 'cvdp'])
    parser.add_argument('--group', choices=list('ABCD'), default='C')
    parser.add_argument('--model', default='gpt-6.1-sol')
    parser.add_argument('--module', choices=['barrel_shifter', 'caesar_cipher', 'universal_shift_register'])
    args = parser.parse_args()
    env = dict(os.environ)
    env['PATH'] = os.pathsep.join(['/opt/homebrew/bin', '/usr/local/bin',
                                  env.get('PATH', os.defpath)])
    env['CARGO_HOME'] = str(ROOT / '.cache/cargo')
    python = ROOT / '.venv/bin/python'
    if not python.exists():
        python = Path(sys.executable)
    commands = {
        'doctor': [str(python), 'scripts/doctor.py'],
        'test-agent': [str(python), '-m', 'unittest', 'discover', '-s', 'tests',
                       '-p', 'test_agent.py', '-v'],
        'test-all': [str(python), '-m', 'unittest', 'discover', '-s', 'tests', '-v']}
    if args.action in commands:
        return subprocess.run(commands[args.action], cwd=ROOT, env=env).returncode
    if args.action == 'smoke' and not env.get('OPENAI_API_KEY'):
        parser.error('Set OPENAI_API_KEY, or use the VS Code Agent task password prompt.')
    label = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + str(os.getpid())
    output = ROOT / 'results/vscode' / (args.action + '-' + label)
    relative_output = str(output.relative_to(ROOT))
    if args.action == 'cvdp':
        command = [str(python), 'scripts/run_cvdp_suite.py', '--output', relative_output]
    elif args.action == 'step1':
        command = [str(python), 'scripts/run_step1.py', '--output', relative_output]
    else:
        runner = 'scripts/run_cvdp_agent.py' if args.module else 'scripts/run_agent.py'
        command = [str(python), runner, '--group', args.group,
                   '--model', args.model, '--output', relative_output]
        if args.module:
            command += ['--module', args.module]
        if args.action == 'preview':
            command.append('--dry-run')
        else:
            command += ['--effort', 'medium', '--max-rounds', '1', '--batch-size', '4',
                        '--run-id', label]
    print('Project:', ROOT, flush=True)
    print('Output:', output, flush=True)
    completed = subprocess.run(command, cwd=ROOT, env=env)
    output.mkdir(parents=True, exist_ok=True)
    # Record configuration only. Never persist API-key environment values.
    (output / 'task.json').write_text(json.dumps({
        'action': args.action, 'module': args.module, 'group': args.group if args.action not in ('step1', 'cvdp') else None,
        'model': args.model if args.action not in ('step1', 'cvdp') else None,
        'exit_code': completed.returncode, 'output': str(output),
        'workspace': str(ROOT)}, indent=2) + '\n')
    if completed.returncode == 0:
        latest = ROOT / 'results/vscode' / ('latest-' + args.action + '.json')
        latest.write_text(json.dumps({'output': str(output)}, indent=2) + '\n')
    return completed.returncode


if __name__ == '__main__':
    raise SystemExit(main())
