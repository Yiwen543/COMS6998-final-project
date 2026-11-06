"""Prepared v2 recovery preflight. No authorization inherited from v1."""
import argparse
import json
from pathlib import Path
import time
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG
from controller_done_loop_v2 import authorization,verify_data,count
from controller_credentials import invoke

OUT=BASE/'results/controller-done-preflight-v2'


def verify(scope):
    a=authorization(scope);verify_data();proposal=ROOT/a['proposal']
    if sha(proposal)!=a['proposal_sha256']:raise ValueError('Approved proposal changed')
    p=json.loads(proposal.read_text())
    if p['registration_sha256']!=sha(REG) or a['generation_requests_allowed']!=0 or a['author_requests_allowed']!=0:raise ValueError('Preflight scope mismatch')
    for n,h in p['count_prompt_sha256'].items():
        if sha(proposal.parent/n)!=h:raise ValueError('Approved count prompt changed')
    manifest=TASK/'reference/scope-v2/manifest.json'
    if sha(manifest)!=a['reference_manifest_sha256']:raise ValueError('Reference packet manifest changed')
    m=json.loads(manifest.read_text())
    for n,h in m['context_sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Reference context changed')
    for n,h in m['packet_sha256'].items():
        if sha(manifest.parent/n/'prompt.txt')!=h:raise ValueError('Reference prompt changed')
    return a


def key_present(name):
    p=ROOT/'build/private'/name
    if not p.is_file() or p.stat().st_mode&0o077:raise ValueError('Secure staged credential absent or unsafe: '+name)


def claim(phase,limit):
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/(phase+'-request-claim.json')
    # A durable exclusive claim precedes any paid operation. Existing claims never retry.
    record=dict(phase=phase,max_invocations=limit,status='reserved_not_yet_called',registration_sha256=sha(REG),producer_sha256=sha(__file__))
    with path.open('x') as stream:json.dump(record,stream,sort_keys=True,indent=2)
    return path


def review():
    a=verify('reference_review')
    if a['claude_max_requests']!=1 or a['claude_max_usd']!=4:raise ValueError('Review budget mismatch')
    key_present('anthropic-crosscheck-key');record=claim('review',1);start=time.perf_counter()
    try:
        result=invoke('review',TASK/'reference/scope-v2/review',OUT/'review')
        status='returned_requires_independent_audit'
    except Exception as error:result=dict(error_type=type(error).__name__);status='failed_no_retry'
    dump(OUT/'review-phase.json',dict(status=status,result=result,wall_seconds=time.perf_counter()-start,
         review_invocations=1,provider_HTTP_request_count=None,provider_HTTP_count_scope='CLI internal requests not directly observed',
         generation_requests=0,author_requests=0,claim_sha256=sha(record),staged_key_retained=True))
    return status


def counts():
    a=verify('token_count')
    if a['openai_max_count_requests']!=4 or a['openai_retries']!=0:raise ValueError('Count budget mismatch')
    key_present('midterm-openai-key');record=claim('count',4);start=time.perf_counter()
    try:
        count(OUT/'counts');result=json.loads((OUT/'counts/summary.json').read_text());status=result['status']
        # Exact approved payloads, not byte/token estimates or an altered feedback package.
        proposal=json.loads((ROOT/a['proposal']).read_text())
        for n,h in proposal['count_prompt_sha256'].items():
            if sha(OUT/'counts'/n)!=h:raise ValueError('Issued count prompt differs from approved payload')
    except Exception as error:result=dict(error_type=type(error).__name__);status='failed_or_unresolved_no_retry'
    dump(OUT/'count-phase.json',dict(status=status,result=result,wall_seconds=time.perf_counter()-start,
         count_invocations_reserved=4,generation_requests=0,claim_sha256=sha(record),staged_key_retained=True))
    return status


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['review','count'],required=True);a=p.parse_args()
    print(review() if a.phase=='review' else counts())
