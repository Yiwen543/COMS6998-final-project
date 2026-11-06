#!/usr/bin/env python3
"""Bounded tool-free Claude author/reviewer; preserve artifacts and role separation.

Author success retains the staged key solely for the already-budgeted review.
Reviewer completion or ANY failed call deletes it. No other model is substituted.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from common import BASE, ROOT, dump, sha
from run_spi_checker_author import validate_source
from run_claude_divider_audit import validate_model, KEY_FILE

def invoke(role, packet, out):
    if role not in ('author','review'):raise ValueError('Unknown role')
    out.mkdir(parents=True,exist_ok=False)
    prompt=(packet/'prompt.txt').read_text()
    (out/'prompt.txt').write_text(prompt)
    meta={'requested_model':'claude-opus-5-5','role':'independent_reference_'+role,
          'prompt_sha256':sha(out/'prompt.txt'),'cli_max_budget_usd':4,'timeout_seconds':600,
          'effort':'low','tools':[],'independent_session':True,'status':'started',
          'usage_status':'unknown_until_complete','script_sha256':sha(Path(__file__))}
    started=time.perf_counter();success=False;consumed=False
    try:
        if not KEY_FILE.exists() or KEY_FILE.stat().st_mode&0o077:raise RuntimeError('Key missing or unsafe permissions')
        env=dict(os.environ)
        for k in list(env):
            if any(x in k for x in ('OPENAI_','ANTHROPIC_','CLAUDE_CODE_USE_')):env.pop(k)
        env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip();consumed=True
        cmd=['claude','--bare','--restricted','--print','--model','claude-opus-5-5',
             '--no-session-persistence','--permission-mode','dontAsk','--tools','',
             '--disable-slash-commands','--strict-mcp-config','--setting-sources','',
             '--max-budget-usd','4','--effort','low','--output-format','stream-json','--verbose',
             '--system-prompt','You are the independent specification reference '+role+'. Use only this packet; no tools.']
        meta['command']=cmd;dump(out/'metadata.json',meta)
        with tempfile.TemporaryDirectory(prefix='test2-claude-') as cwd, (out/'stream.jsonl').open('w') as log, (out/'stderr.log').open('w') as err:
            proc=subprocess.run(cmd,input=prompt,text=True,stdout=log,stderr=err,env=env,cwd=cwd,timeout=600)
        meta['returncode']=proc.returncode
        records=[json.loads(s) for s in (out/'stream.jsonl').read_text().splitlines() if s.strip()]
        finals=[r for r in records if r.get('type')=='result']
        if not finals:raise RuntimeError('No complete Claude result')
        response=finals[-1];dump(out/'response.json',response)
        meta.update(usage=response.get('usage'),model_usage=response.get('modelUsage'),
                    total_cost_usd=response.get('total_cost_usd'),session_id=response.get('session_id'),usage_status='reported_by_CLI')
        if proc.returncode or response.get('is_error'):raise RuntimeError('Claude failed; retained response')
        validate_model(response,'test2 reference '+role)
        body=str(response.get('result','')).strip()
        if body.startswith('```'):body='\n'.join(body.splitlines()[1:-1])
        data=json.loads(body)
        if role=='author':
            if set(data)!={'checker_source','properties','contract_markdown','selftest_source'}:raise ValueError('Author schema')
            validate_source(data['checker_source']);validate_source(data['selftest_source'])
            for name,value in [('checker.py',data['checker_source']),('selftest.py',data['selftest_source']),('contract.md',data['contract_markdown'])]:
                (out/name).write_text(value+'\n')
            dump(out/'properties.json',data['properties'])
            meta['artifact_sha256']={n:sha(out/n) for n in ('checker.py','selftest.py','contract.md','properties.json')}
        else:dump(out/'review.json',data)
        meta['status']='generated_not_validated' if role=='author' else 'review_returned_not_automatically_accepted'
        success=True
    except Exception as e:
        meta.update(status='failed',error_type=type(e).__name__)
        raise
    finally:
        meta['wall_seconds']=time.perf_counter()-started
        if consumed and (role=='review' or not success):KEY_FILE.unlink(missing_ok=True)
        meta['staged_key_retained_for_planned_review']=bool(success and role=='author')
        dump(out/'metadata.json',meta)
    return {k:meta[k] for k in ('status','wall_seconds','total_cost_usd') if k in meta}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--role',choices=['author','review'],required=True)
    p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(invoke(a.role,a.packet.resolve(),a.output.resolve()),indent=2))
