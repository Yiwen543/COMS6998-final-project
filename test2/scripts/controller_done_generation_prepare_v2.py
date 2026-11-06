"""Seal current qualified inputs and a reviewable paid proposal; never invokes APIs."""
import json
from pathlib import Path
import subprocess
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG
from controller_done_generate_v2 import GEN_REG,LIVE_FREEZE,APPROVAL,count_messages
from controller_done_loop_v2 import verify_data
from controller_release_live import verify_release

OUT=BASE/'results/controller-done-generation-preparation-v2'


def load(path):return json.loads(path.read_text())


def prepare():
    verify_data();reg=load(GEN_REG);r=BASE/'results';review=load(r/'controller-done-review-v4/review.json')
    gates=dict(reference_scope_accepted=review['verdict']=='ACCEPT_SCOPE' and review['adapter_changes_required'] is False and review['oracle_revision_required'] is False,
               current_mock_replay=load(OUT/'mock-replay-audit.json')['status']=='passed',shared_grader=load(r/'controller-done-grade-v4-acceptance/audit.json')['status']=='OFFLINE_SHARED_GRADING_VERIFIED_FRESH_REVIEW_PENDING',
               fixed_inventory_unique=load(OUT/'accepted-review-diagnostics.json')['frozen_inventory_unique'],formal_profile_controls=load(r/'controller-done-formal-controls-v4/summary.json')['status']=='passed')
    a=verify_release(r/'controller-done-generation-mock-v2');b=verify_release(r/'controller-done-generation-replay-v2')
    for x in a:
        y=next(y for y in b if (x['arm'],x['repetition'],x['round'])==(y['arm'],y['repetition'],y['round']))
        for name in ('prompt.json','response.json','development-feedback.json','compiled/candidate.sv'):
            if sha(r/'controller-done-generation-mock-v2'/x['directory']/name)!=sha(r/'controller-done-generation-replay-v2'/y['directory']/name):raise ValueError('Current own-history mock/replay mismatch')
    fresh=load(r/'controller-done-grade-v4-fresh/scores.json');reused=load(r/'controller-done-generation-grade-v2/scores.json')
    gates['current_programs_independently_graded']=fresh['selected_endpoints']==reused['selected_endpoints'] and len(reused['rounds'])==36
    counts=load(r/'controller-done-preflight-v2/counts/summary.json');gates['actual_provider_counts']=counts['status']=='passed' and len(counts['counts'])==4
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        for arm,kind,msg in count_messages():
            p=Path(temp)/'prompt.json';dump(p,msg);rec=next(x for x in counts['counts'] if (x['arm'],x['kind'])==(arm,kind))
            if sha(p)!=rec['prompt_sha256'] or not rec['within_cap']:raise ValueError('Current counted payload changed')
    test=r/'controller-done-generation-v2-unit-v2.log';gates['eleven_API_guard_tests']='Ran 11 tests' in test.read_text() and test.read_text().rstrip().endswith('OK')
    gates['prompt_isolation_and_lossless_codec']=load(TASK/'public/prompt-packets-v2/audit.json')['B_C_common_equal']
    gates['all_old_freezes_scores_preserved']=True
    members={}
    def add(path):members[str(Path(path).relative_to(ROOT))]=sha(path)
    for name,h in load(REG)['preserve_old_freezes'].items():
        path=ROOT/name;f=load(path)
        if sha(path)!=h:raise ValueError('Old manifest changed')
        for n,v in f.get('files',f.get('artifact_sha256',{})).items():
            if sha(ROOT/n)!=v:raise ValueError('Old frozen member changed')
        add(path)
        # Relevant controller/reference artifacts, not the unrelated old FIFO corpus.
        if name!='test2/configs/live_freeze_v1.json':
            for n in f.get('files',f.get('artifact_sha256',{})):add(ROOT/n)
    old=load(r/'controller-done-acceptance-v4/acceptance.json')
    for n,h in old['old_scores'].items():
        if sha(ROOT/n)!=h:raise ValueError('Old score changed')
        add(ROOT/n)
    for n,h in load(TASK/'evaluation-freeze.json')['files'].items():
        if sha(ROOT/n)!=h:raise ValueError('Current physical input changed')
        add(ROOT/n)
    for folder in ('public/prompt-packets-v2','reference/scope-v4'):
        for path in (TASK/folder).rglob('*'):
            if path.is_file():add(path)
    sources=['controller_done_generate_v2.py','controller_done_model_v2.py','controller_done_runtime.py','controller_monitor_done.py','controller_monitor_live.py','controller_release_live.py','controller_done_data.py','controller_done_packet.py','controller_done_codec_v2.py','controller_done_case_v4.py','controller_done_grade_v4.py','controller_done_formal_v3.py','controller_done_witness_v3.py','controller_reference_evaluate.py','common.py']
    for n in sources:add(BASE/'scripts'/n)
    add(ROOT/'scripts/pilot_model.py');add(BASE/'tests/test_controller_done_generation_v2.py');add(test)
    for path in [GEN_REG,REG,BASE/'configs/controller_done_prompt_v2.json',BASE/'configs/controller_done_scoring_v4.json',TASK/'input-freeze.json',TASK/'evaluation-freeze.json',
                 r/'controller-done-review-v4/review.json',r/'controller-done-review-v4/metadata.json',r/'controller-done-review-v4/summary.json',
                 r/'controller-done-preflight-v2/counts/summary.json',r/'controller-done-grade-v4-acceptance/audit.json',r/'controller-done-grade-v4-acceptance/vector-audit.json',
                 r/'controller-done-formal-controls-v4/summary.json',r/'controller-done-generation-mock-v2/release.json',r/'controller-done-generation-replay-v2/release.json',r/'controller-done-generation-grade-v2/scores.json',
                 OUT/'accepted-review-diagnostics.json',OUT/'mock-replay-audit.json',r/'controller-done-environment-v1.json']:
        add(path)
    for n,h in reg['code_sha256'].items():
        if sha(BASE/'scripts'/n)!=h:raise ValueError('Registered generation/grade code changed')
    if not all(type(v)==bool and v for v in gates.values()):raise ValueError('Qualification gates incomplete')
    if LIVE_FREEZE.exists():raise FileExistsError('New generation freeze already exists')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dump(LIVE_FREEZE,dict(ready_for_explicitly_authorized_generation=True,API_permission_granted_by_this_file=False,gates=gates,files=members,current_HEAD=head,registration_sha256=sha(GEN_REG),
         scope='Whole B/C feedback package; fixed physical data. Short trace_done0 formal projection cannot prove128cycle completion. Unknowns/timeouts and low diagnostic limitations retained.',producer_sha256=sha(__file__)))
    proposal=TASK/'qualification/candidate-generation-v2';proposal.mkdir(exist_ok=False)
    dump(proposal/'proposal.json',dict(status='PREPARED_NOT_AUTHORIZED',user_approved=False,registration_sha256=sha(GEN_REG),qualification_freeze_sha256=sha(LIVE_FREEZE),gates=gates,run_directory=reg['run_directory'],
        model='gpt-6.1-sol',reasoning_effort='low',service_tier='default(Standard)',sessions_per_arm=3,rounds_per_session=6,normal_generation_requests=36,max_generation_requests_including_retry=72,max_precount_requests=72,
        max_manual_failure_retries=1,SDK_retries=0,input_tokens_per_attempt=64000,output_tokens_per_attempt=8192,timeout_seconds=120,
        generation_reserve_usd=17.5,count_fee_reserve_usd=2.5,total_stage_spending_ceiling_usd=20,max_generation_token_reserve_usd=17.41824,
        pricing_rates_usd_per_million=reg['pricing_rates_usd_per_million'],pricing_sources=reg['pricing_sources'],
        billing_scope='Local dispatch/token guard under explicitStandardtier at checkedprices. Realinvoice/countfees notreturned; reserves arenotmeasuredUSD. Preserveunknownfailedrequestcosts.',
        halt_policy=reg['runtime_halt'],stimulus='Fixed frozen dev/final traces,passivemonitors;no extraDUTinput/clock',
        evaluation='All36snapshotsbeforeprivategrading;sharedgrader_v4,correctcontrol/ordinarysafety/unattributedfinite/unknown/invalid/notreachedseparate;B/Cwholepackage,no placebo',
        local_formal='540fixedjobs,depth24,z3,10s correct/5smutant,720s perfinal overall inclphysicalwitness;interleavedB/C;projectionnot128cyclecompletionproof',
        oracle_author_requests=0,additional_Claude_review_requests=0,credentials='ExistingsecurestagedOpenAIkey;no restaging;retainthroughgeneration/audit/evaluationincludingfailures',
        conditional_second_review_used=False,accepted_reference_review_sha256=sha(r/'controller-done-review-v4/review.json')))
    dump(OUT/'qualification.json',dict(status='QUALIFIED_NOT_API_AUTHORIZED',gates=gates,freeze_sha256=sha(LIVE_FREEZE),freeze_members=len(members),proposal_sha256=sha(proposal/'proposal.json'),
        generation_API_calls=0,additional_count_API_calls=0,conditional_second_Claude_call_used=False,current_HEAD=head,producer_sha256=sha(__file__)))
    return OUT


if __name__=='__main__':print(prepare())
