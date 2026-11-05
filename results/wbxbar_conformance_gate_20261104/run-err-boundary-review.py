"""One previously planned review; no design generation or checker mutation."""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from patch_wbxbar_conformance_design import BASE, verify_scope
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import sha

packet = BASE / 'err-boundary-review-packet-v1'
output = BASE / 'err-boundary-review-v1'
verify_scope()
manifest = json.loads((packet / 'manifest.json').read_text())
for path, digest in manifest['source_hashes'].items():
    if sha(Path(path)) != digest:
        raise ValueError('Review source drift')
for name, ext in [('packet', 'json'), ('prompt', 'txt')]:
    if sha(packet / (name + '.' + ext)) != manifest[name + '_sha256']:
        raise ValueError('Review packet drift')
if sha(Path(__file__)) != manifest['runner_sha256']:
    raise ValueError('Review runner drift')
if output.exists():
    raise ValueError('Never overwrite review evidence')
if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
    raise ValueError('Hidden key absent or unsafe')
env = {k: v for k, v in os.environ.items() if not k.startswith(('OPENAI_', 'ANTHROPIC_', 'CLAUDE_CODE_USE_'))}
env['ANTHROPIC_API_KEY'] = KEY_FILE.read_text().strip()
try:
    result = call((packet / 'prompt.txt').read_text(), output, env, 'WBXBAR fresh ERR-boundary and transport-correction reviewer')
    (output / 'review.json').write_text(json.dumps(result, indent=2) + '\n')
    valid = isinstance(result, dict) and set(result) == {'findings', 'required_changes', 'ready_for_implementation'} and type(result.get('ready_for_implementation')) is bool
    status = {'schema_valid': valid, 'model_readiness': result.get('ready_for_implementation') if valid else None,
              'automatic_implementation_permission': False, 'checker_changed': False,
              'live_B_allowed': False, 'live_C_allowed': False}
    (output / 'validation.json').write_text(json.dumps(status, indent=2) + '\n')
    print(json.dumps(status, indent=2))
finally:
    KEY_FILE.unlink(missing_ok=True)
    env.pop('ANTHROPIC_API_KEY', None)
    verify_scope()
