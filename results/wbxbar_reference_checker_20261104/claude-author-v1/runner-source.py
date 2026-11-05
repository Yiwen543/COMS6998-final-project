#!/usr/bin/env python3
"""Invoke isolated, tool-free Claude Code checker authorship; preserve raw output."""
import argparse
import ast
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

from run_midterm_fixed import ROOT, sha
from run_claude_divider_audit import KEY_FILE, validate_model


def validate_source(source):
    tree = ast.parse(source)
    prohibited = {'open', 'exec', 'eval', 'compile', '__import__', 'getattr', 'setattr', 'delattr', 'globals', 'locals', 'input', 'breakpoint'}
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            modules = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module]
            if any(m not in ('collections', 'copy', 'math') for m in modules):
                raise ValueError('Non-pure import in candidate checker')
        if isinstance(n, ast.Name) and n.id in prohibited:
            raise ValueError('Prohibited operation in candidate checker')
        if isinstance(n, ast.Attribute) and n.attr.startswith('__'):
            raise ValueError('Dunder attribute in candidate checker')
    return tree


def invoke(packet, output, budget, timeout):
    prompt = (packet/'prompt.txt').read_text()
    metadata = {'requested_model': 'claude-opus-5-5', 'role': 'specification_checker_author',
        'prompt_sha256': sha(packet/'prompt.txt'), 'tools': [], 'budget_usd': budget,
        'timeout_seconds': timeout, 'independent_session': True, 'status': 'started',
        'script_sha256':sha(Path(__file__)), 'effort':'low',
        'usage_status':'unknown_until_complete; timeout is not zero-cost'}
    output.mkdir(parents=True, exist_ok=False)
    (output/'prompt.txt').write_text(prompt)
    (output/'runner-source.py').write_bytes(Path(__file__).read_bytes())
    metadata_path = output/'metadata.json'
    metadata_path.write_text(json.dumps(metadata, indent=2)+'\n')
    consumed = False
    started = time.perf_counter()
    try:
        if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
            raise RuntimeError('Missing hidden key or unsafe permissions')
        env = dict(os.environ)
        env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
        consumed = True
        # No OpenAI credentials or inherited alternative provider settings.
        for k in list(env):
            if k.startswith(('OPENAI_', 'ANTHROPIC_BASE_URL', 'CLAUDE_CODE_USE_')):
                env.pop(k)
        command = ['claude', '--bare', '--restricted', '--print', '--model', 'claude-opus-5-5',
            '--no-session-persistence', '--permission-mode', 'dontAsk', '--tools', '',
            '--disable-slash-commands', '--strict-mcp-config', '--setting-sources', '',
            '--max-budget-usd', str(budget), '--effort', 'low', '--output-format', 'stream-json', '--verbose',
            '--system-prompt', 'You are an independent specification-driven verification checker author. Use only the supplied packet; no external tools.']
        metadata['command']=command
        with tempfile.TemporaryDirectory(prefix='spi-checker-role-') as cwd, \
                (output/'stream.jsonl').open('w') as stdout, (output/'stderr.log').open('w') as stderr:
            process = subprocess.run(command, input=prompt, text=True, stdout=stdout, stderr=stderr,
                                     cwd=cwd, env=env, timeout=timeout, check=False)
        metadata.update(returncode=process.returncode, command=command)
        if process.returncode:
            raise RuntimeError('Claude process failed; see recorded response')
        records=[json.loads(line) for line in (output/'stream.jsonl').read_text().splitlines() if line.strip()]
        results=[r for r in records if r.get('type')=='result']
        if not results:
            raise RuntimeError('No complete result in Claude stream')
        response=results[-1]
        (output/'response.json').write_text(json.dumps(response,indent=2)+'\n')
        validate_model(response, 'SPI checker authorship')
        metadata.update(model_usage=response.get('modelUsage'), usage=response.get('usage'),
                        total_cost_usd=response.get('total_cost_usd'), session_id=response.get('session_id'),
                        usage_status='reported_by_Claude_Code')
        if response.get('is_error'):
            raise RuntimeError('Claude returned an error')
        body = str(response.get('result','')).strip()
        if body.startswith('```'):
            body = '\n'.join(body.splitlines()[1:-1])
        data = json.loads(body)
        if set(data) != {'checker_source','properties','contract_markdown','selftest_source'}:
            raise ValueError('Unexpected checker artifact schema')
        validate_source(data['checker_source'])
        validate_source(data['selftest_source'])
        for name, value in [('checker.py',data['checker_source']), ('selftest.py',data['selftest_source']),
                            ('contract.md',data['contract_markdown'])]:
            (output/name).write_text(value+'\n')
        (output/'properties.json').write_text(json.dumps(data['properties'], indent=2)+'\n')
        metadata.update(status='candidate_generated_not_validated',
            artifact_sha256={name:sha(output/name) for name in ('checker.py','selftest.py','contract.md','properties.json')})
    except Exception as error:
        metadata.update(status='failed', error_type=type(error).__name__)
        raise
    finally:
        metadata['wall_seconds'] = time.perf_counter()-started
        metadata_path.write_text(json.dumps(metadata, indent=2)+'\n')
        if consumed:
            KEY_FILE.unlink(missing_ok=True)
    return metadata


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--packet', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--max-budget-usd', type=float, default=4)
    cli.add_argument('--timeout-seconds', type=int, default=600)
    args = cli.parse_args()
    print(json.dumps(invoke(args.packet.resolve(), args.output.resolve(), args.max_budget_usd, args.timeout_seconds), indent=2))
