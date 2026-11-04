"""One bounded tool-free read-only call after local packet validation."""
import json
import os
from run_midterm_fixed import ROOT,sha
from run_claude_divider_audit import KEY_FILE
from revise_spi_checker_role import call


def run():
    role=ROOT/'results/i2c_event_candidate_20261104/claude-checker-v3'
    prep=role/'compact-review'
    gate=json.loads((prep/'preflight.json').read_text())
    if not gate['lossless_roundtrip'] or sha(prep/'prompt.txt')!=gate['prompt_sha256'] or (prep/'prompt.txt').stat().st_size>150000:
        raise ValueError('Packet preflight mismatch')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:raise ValueError('Staged key missing or unsafe')
    env={k:v for k,v in os.environ.items() if not k.startswith(('OPENAI_','ANTHROPIC_','CLAUDE_CODE_USE_'))}
    try:
        env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip()
        r=call((prep/'prompt.txt').read_text(),role/'review-compact',env,'I2C independent final read-only reviewer')
        (role/'review.json').write_text(json.dumps(r,indent=2)+'\n')
        print(json.dumps({'completed':True,'ready_for_offline_gate':r.get('ready_for_offline_gate')}))
    finally:
        KEY_FILE.unlink(missing_ok=True);env.pop('ANTHROPIC_API_KEY',None)


if __name__=='__main__':run()
