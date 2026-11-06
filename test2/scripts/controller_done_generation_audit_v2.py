"""Read-only audit of qualified generation preparation, not an API authorization."""
import argparse
import collections
import json
from pathlib import Path
import subprocess
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG
from controller_done_generate_v2 import GEN_REG,LIVE_FREEZE,APPROVAL,live_gate,count_messages
from controller_release_live import verify_release


def load(p):return json.loads(p.read_text())


def audit(out):
    f=load(LIVE_FREEZE);g=load(GEN_REG);prep=BASE/'results/controller-done-generation-preparation-v2';q=load(prep/'qualification.json');r=BASE/'results'
    if sha(LIVE_FREEZE)!=q['freeze_sha256'] or sha(GEN_REG)!=f['registration_sha256']:raise ValueError('Qualified freeze changed')
    if f['API_permission_granted_by_this_file'] or not f['ready_for_explicitly_authorized_generation'] or not all(type(v)==bool and v for v in f['gates'].values()):raise ValueError('Freeze gate/permission separation invalid')
    for name,h in f['files'].items():
        if sha(ROOT/name)!=h:raise ValueError('Frozen preparation input changed: '+name)
    review=load(r/'controller-done-review-v4/review.json');m=load(r/'controller-done-review-v4/metadata.json')
    if review['verdict']!='ACCEPT_SCOPE' or review['adapter_changes_required'] or review['oracle_revision_required']:raise ValueError('Reference scope not accepted')
    if load(r/'controller-done-review-v4/summary.json')['conditional_second_used']:raise ValueError('Second review wrongly used after acceptance')
    a=verify_release(r/'controller-done-generation-mock-v2');b=verify_release(r/'controller-done-generation-replay-v2')
    if len(a)!=36 or len(b)!=36:raise ValueError('Current all-round freeze incomplete')
    for x,y in zip(sorted(a,key=lambda x:x['directory']),sorted(b,key=lambda x:x['directory'])):
        for name in ('prompt.json','response.json','development-feedback.json','compiled/candidate.sv'):
            if sha(r/'controller-done-generation-mock-v2'/x['directory']/name)!=sha(r/'controller-done-generation-replay-v2'/y['directory']/name):raise ValueError('Current saved-response replay mismatch')
    actual=load(r/'controller-done-preflight-v2/counts/summary.json')
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        for arm,kind,messages in count_messages():
            p=Path(temp)/'prompt.json';dump(p,messages);rec=next(x for x in actual['counts'] if (x['arm'],x['kind'])==(arm,kind))
            if sha(p)!=rec['prompt_sha256'] or not rec['within_cap']:raise ValueError('Precounted payload no longer current')
    records=load(TASK/'measurements-v1/summary.json')['records'];keys=collections.Counter((x['source'],x['simulator'],x.get('trace')) for x in records)
    if len(keys)!=162 or any(v!=1 for v in keys.values()):raise ValueError('Frozen inventory duplicate/missing')
    score=load(r/'controller-done-generation-grade-v2/scores.json');prior=load(r/'controller-done-grade-v4-fresh/scores.json')
    if score['selected_endpoints']!=prior['selected_endpoints'] or score['costs']['new_monitor_replays']!=0 or score['costs']['reused_monitor_replays']!=5832:raise ValueError('Current independent grade reuse differs')
    for name,h in load(REG)['preserve_old_freezes'].items():
        path=ROOT/name;old=load(path)
        if sha(path)!=h or any(sha(ROOT/n)!=v for n,v in old.get('files',old.get('artifact_sha256',{})).items()):raise ValueError('Old frozen results changed')
    if APPROVAL.exists():raise ValueError('Unexpected candidate generation authorization during preparation')
    try:live_gate()
    except ValueError:pass
    else:raise ValueError('Candidate API unexpectedly open')
    proposal=TASK/'qualification/candidate-generation-v2/proposal.json'
    if sha(proposal)!=q['proposal_sha256'] or load(proposal)['user_approved']:raise ValueError('Paid proposal unexpectedly changed or approved')
    limits=g['API_limits']
    if limits['max_generations']!=72 or limits['max_precounts']!=72 or limits['total_stage_spending_ceiling_usd']!=20 or 72*limits['per_generation_conservative_reserve_usd']>17.5:raise ValueError('Registered request/USD reserve mismatch')
    import openai
    result=dict(status='GENERATION_PREPARATION_ACCEPTED_AWAITING_EXPLICIT_PAID_APPROVAL',current_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        reference_review='ACCEPT_SCOPE',conditional_second_review_used=False,freeze_sha256=sha(LIVE_FREEZE),freeze_members=len(f['files']),all_gates=f['gates'],
        current_mock_rounds=36,current_saved_response_replay_rounds=36,current_grade_reused_logs=5832,new_LLM_trials=0,candidate_generation_API_calls=0,
        actual_preflight_tokens={rec['arm']+'/'+rec['kind']:rec['input_tokens'] for rec in actual['counts']},generation_guard_tests=11,
        real_provider_connectivity_for_generation='Not exercised; no generation permission',OpenAI_SDK=openai.__version__,
        reported_Claude_USD_to_date=round(0.342502+m['total_cost_usd'],6),count_endpoint_USD='UNKNOWN',
        proposed_generation_reserve_USD=17.5,proposed_count_fee_reserve_USD=2.5,proposed_new_stage_ceiling_USD=20,
        actual_billing_scope='Dispatch/token reserve is not a provider invoice; missing costs remain unknown.',
        diagnostic_limits=load(prep/'accepted-review-diagnostics.json'),proposal_sha256=sha(proposal),producer_sha256=sha(__file__),
        next='Only after explicit generation approval create a separate bound grant, reuse staged OpenAI key, run generation/freeze/replay/grade/formal/report without further routine permission.')
    dump(out,result);return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(audit(a.output.resolve())['status'])
