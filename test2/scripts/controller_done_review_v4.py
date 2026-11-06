"""One separately approved Claude adapter review, USD1.80 cap, no oracle author."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK
from run_claude_divider_audit import validate_model

APPROVAL=BASE/'configs/controller_done_api_authorization_v4.json'
PACKET=TASK/'reference/scope-v4'
OUT=BASE/'results/controller-done-review-v4'
CAP=1.8


def command():
    return ['claude','--bare','--restricted','--print','--model','claude-opus-5-5','--no-session-persistence',
            '--permission-mode','dontAsk','--tools','','--disable-slash-commands','--strict-mcp-config','--setting-sources','',
            '--max-budget-usd',str(CAP),'--effort','low','--output-format','stream-json','--verbose',
            '--system-prompt','You are the independent specification/reference-adapter reviewer. Use only this packet; no tools.']


def verify():
    if not APPROVAL.exists():raise ValueError('No authorization for additional review')
    a=json.loads(APPROVAL.read_text())
    if not a.get('user_approved') or a.get('scopes')!=['reference_review'] or a.get('max_invocations')!=1 or a.get('max_usd')!=CAP:raise ValueError('Review scope/budget mismatch')
    if sha(ROOT/a['proposal'])!=a['proposal_sha256'] or sha(PACKET/'manifest.json')!=a['manifest_sha256']:raise ValueError('Approved packet changed')
    m=json.loads((PACKET/'manifest.json').read_text())
    if sha(PACKET/'prompt.txt')!=m['prompt_sha256']:raise ValueError('Review prompt changed')
    for n,h in m['context_sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Review context changed')
    return a


def invoke():
    verify();key=ROOT/'build/private/anthropic-crosscheck-key'
    if not key.is_file() or key.stat().st_mode&0o077:raise ValueError('Secure staged Anthropic key absent')
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/'request-claim.json').open('x') as f:json.dump(dict(max_invocations=1,max_usd=CAP,producer_sha256=sha(__file__)),f,indent=2)
    prompt=(PACKET/'prompt.txt').read_text();(OUT/'prompt.txt').write_text(prompt);started=time.perf_counter()
    meta=dict(status='started',requested_model='claude-opus-5-5',cli_max_budget_usd=CAP,timeout_seconds=600,tools=[],independent_session=True,
              prompt_sha256=sha(OUT/'prompt.txt'),author_requests=0,generation_requests=0,usage_status='UNKNOWN_UNTIL_COMPLETE',producer_sha256=sha(__file__),command=command())
    dump(OUT/'metadata.json',meta)
    try:
        env={k:v for k,v in os.environ.items() if not any(s in k for s in ('OPENAI_','ANTHROPIC_','CLAUDE_CODE_USE_'))};env['ANTHROPIC_API_KEY']=key.read_text().strip()
        with tempfile.TemporaryDirectory(prefix='controller-review-') as cwd,(OUT/'stream.jsonl').open('w') as log,(OUT/'stderr.log').open('w') as err:
            p=subprocess.run(command(),input=prompt,text=True,stdout=log,stderr=err,env=env,cwd=cwd,timeout=600)
        finals=[json.loads(s) for s in (OUT/'stream.jsonl').read_text().splitlines() if s.strip()]
        finals=[r for r in finals if r.get('type')=='result']
        if not finals:raise RuntimeError('No completed CLI result')
        result=finals[-1];dump(OUT/'response.json',result);meta.update(returncode=p.returncode,total_cost_usd=result.get('total_cost_usd'),usage=result.get('usage'),model_usage=result.get('modelUsage'),session_id=result.get('session_id'),usage_status='reported_by_CLI')
        if p.returncode or result.get('is_error'):raise RuntimeError('CLI failed, evidence retained')
        validate_model(result,'controller adapter review v4');body=str(result.get('result','')).strip()
        if body.startswith('```'):body='\n'.join(body.splitlines()[1:-1])
        dump(OUT/'review.json',json.loads(body));meta['status']='review_returned_not_automatically_accepted'
    except Exception as error:meta.update(status='failed_no_retry',error_type=type(error).__name__)
    finally:
        meta.update(wall_seconds=time.perf_counter()-started,main_staged_key_retained=key.exists());dump(OUT/'metadata.json',meta)
    return meta['status']


if __name__=='__main__':print(invoke())
