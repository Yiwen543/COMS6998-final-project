"""Two bounded isolated Claude roles; retain key only until review or deadline.

Author sees prepared spec only. Integration prepares review-packet.json after
offline controls; a fresh reviewer can inspect driver/evidence, never rewrite it.
"""
import argparse
import json
import os
import time
from pathlib import Path
from revise_spi_checker_role import call, FILES
from run_spi_checker_author import validate_source
from run_claude_divider_audit import KEY_FILE
from run_midterm_fixed import sha


def run(packet, output):
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise RuntimeError('Missing staged key or unsafe permissions')
    output.mkdir(parents=True, exist_ok=False)
    env={k:v for k,v in os.environ.items() if not k.startswith(('OPENAI_','ANTHROPIC_','CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip()
    (output/'runner-source.py').write_bytes(Path(__file__).read_bytes())
    try:
        data=call((packet/'prompt.txt').read_text(),output/'author',env,'I2C specification checker author')
        if set(data)!={'checker_source','selftest_source','properties','contract_markdown'}:
            raise ValueError('Unexpected checker schema')
        validate_source(data['checker_source']);validate_source(data['selftest_source'])
        candidate=output/'candidate';candidate.mkdir()
        for k,f in [('checker_source','checker.py'),('selftest_source','selftest.py'),('contract_markdown','contract.md')]:
            (candidate/f).write_text(data[k]+'\n')
        (candidate/'properties.json').write_text(json.dumps(data['properties'],indent=2)+'\n')
        (candidate/'authorship.json').write_text(json.dumps({'author':'claude-opus-5-5',
            'artifact_sha256':{f:sha(candidate/f) for f in FILES},'packet_sha256':sha(packet/'packet.json')},indent=2)+'\n')
        print('AUTHOR_COMPLETE; waiting for independently prepared review packet',flush=True)
        deadline=time.monotonic()+1800
        while time.monotonic()<deadline:
            if (output/'skip-review.json').exists():
                print('REVIEW_SKIPPED; reason saved',flush=True);return
            review=output/'review-packet.json'
            if review.exists():
                body=json.loads(review.read_text())
                prompt='Read-only independent checker/driver audit. Do not modify artifacts. Return JSON with ready_for_offline_gate, findings, limitations. Check event false positives, independent controls, spec justification and isolation. No claim of formal proof.\n'+json.dumps(body)
                result=call(prompt,output/'review',env,'I2C independent checker reviewer')
                (output/'review.json').write_text(json.dumps(result,indent=2)+'\n')
                print('REVIEW_COMPLETE',flush=True);return
            time.sleep(2)
        (output/'review-not-run.json').write_text('{"reason":"review packet deadline elapsed"}\n')
    finally:
        KEY_FILE.unlink(missing_ok=True)
        env.pop('ANTHROPIC_API_KEY',None)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();run(a.packet.resolve(),a.output.resolve())
