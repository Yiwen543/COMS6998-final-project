"""Separate registration and spec-only Claude contract/patch packet, never live outcomes."""
import argparse
import json
import subprocess
from pathlib import Path
from prepare_wbxbar_checker_role import packet as specification, SPEC, SPEC_SHA
from prepare_wbxbar_checker_repair import FILES
from run_midterm_fixed import ROOT, sha
from wbxbar_experiment import verify_freeze

BASE=ROOT/'results/wbxbar_abort_contract_20261104'
OLD=ROOT/'results/wbxbar_exploratory_bc_20261104'
PRIOR=OLD/'claude-v3/candidate'
REG=ROOT/'configs/wbxbar_cancel_contract_v1.json'


def register():
    if REG.exists():raise ValueError('Registration already exists')
    frozen=verify_freeze();manifest={};batches=0
    for folder in sorted((OLD/'live-v1').glob('rep[1-3]-[BC]')):
        for batch in [folder/'seed',*sorted(folder.glob('round[1-6]'))]:
            batches+=1
            for name in ('actions.json','trace.json','result.json','raw-points.json','coverage.dat','execution.json'):
                p=batch/name;manifest[str(p.relative_to(ROOT))]=sha(p)
    if batches!=42:raise ValueError('Expected all six sessions and 42 batches')
    for name in ('calls.jsonl','counts.jsonl','rounds.jsonl','summary.json','metadata.json','freeze.json'):
        p=OLD/'live-v1'/name;manifest[str(p.relative_to(ROOT))]=sha(p)
    mp=BASE/'original-evidence-manifest.json'
    if mp.exists():raise ValueError('Never overwrite original manifest')
    mp.write_text(json.dumps(manifest,indent=2)+'\n')
    paths=[ROOT/'configs/wbxbar_exploratory_bc_freeze_v1.json',PRIOR/'authorship.json',mp,BASE/'controls-v1/manifest.json',BASE/'controls-v1/private-inputs.json']
    reg={'id':'wbxbar_cancel_contract_v1','date':'2026-11-04',
        'purpose':'Post-hoc specification/checker repair and retrospective replay, not a new independent effectiveness experiment.',
        'parent_freeze':'configs/wbxbar_exploratory_bc_freeze_v1.json','prior_checker':str(PRIOR.relative_to(ROOT)),
        'preserved_hashes':{str(p.relative_to(ROOT)):sha(p) for p in paths},
        'experiment_budget':frozen['development_budget'],'model_limits':frozen['model_limits'],
        'new_stimulus_generation_calls':0,'planned_claude_calls':2,'cli_budget_per_call_usd':4,
        'roles':{'Claude':'Public contract, exact checker patch and selftests; fresh read-only reviewer. Author receives no DUT implementation or real trace.',
                 'GPT':'Synthetic controls, integration, fixed-driver saved-action replay, accounting. Never edits checker.'},
        'gate':['Keep all known-clean historical positives and previously detected clean-baseline faults.',
                'Independently review new controls; ambiguous cancellation is unresolved, not a pass.',
                'Preserve ordinary ordering, enabled payload, response, reset and duplicate checks. Separate unresolved-baseline detections.',
                'Worker and selftests pass; fresh Claude review ready; new hashes frozen before retrospective replay.'],
        'replay':{'batches':42,'original_physical_cycles':8360,'simulator':'Original frozen Verilator binary/driver; exact saved JSON; require counters and pins to match.',
                  'costs':'Record replay executions/cycles/wall separately. Original API costs and coverage stay unchanged.',
                  'limits':'Old trajectories used old checker feedback. Reclassification is not a new causal B/C comparison.'},
        'prohibited':['Modify original artifacts','Generate replacement model stimuli','Change DUT, driver, targets, denominator or budgets','Retroactively rewrite old verdicts']}
    REG.write_text(json.dumps(reg,indent=2)+'\n');return reg

INSTRUCTIONS='''You are Claude, an independent public-specification contract and checker author. GPT owns driver/stimulus and independently proposed controls.
First resolve the normative scope in contract.md: cite each rule/section, distinguish authoritative requirements, declared environmental assumptions, inferred requirements, and unknowns. Then repair your prior checker, properties and selftests consistently.
Return ONLY JSON {patches:[{file,before,after}],rationale:[strings]}. Allowed files checker.py,selftest.py,properties.json,contract.md. Each nonempty before must occur exactly once; use exact patches only. Maintain pure Python check_rows(rows) interface and allowed imports collections,copy,math, no I/O/tools/project imports/exec/eval/dunder access.
The question is how to attribute multiple accepted requests when CYC withdrawal cancels a bus cycle: some buffered work may never be seen downstream while another request may appear later. Public sources do not state an exact pipeline or cancellation latency. Determine which observations can be proved illegal and which must remain unresolved. Do not treat a mere identity match as a specification pass.
Review acceptance simultaneous with ERR, partial cancellation, repeated identical identities, live/aborted ownership ambiguity, consumption multiplicity, reset epochs, and stale responses landing on new work. Keep a causal evidence trail with original accept/abort/forward cycles when possible. Never count canceled work as successful completion or successful recovery. Preserve cumulative unresolved observations across resets while clearing request identities.
Do not generalize uncertainty about canceled requests to forgive ordering, payload, response or corruption errors in ordinary live traffic. Preserve enabled-byte SEL comparisons, address/direction/SEL identity, exact live completion data, and classification of unexplained mapped ERR as unresolved. No guessed master/queue ownership, invented grace period, additional input restriction, oracle from implementation, or silent weakening of a check to fit a scenario.
The old author instructions requiring the oldest aborted entry are not normative authority: independently re-examine that assumption. Your own old contract may be incomplete; update the contract AND property support status to match executable semantics. If evidence cannot settle conformance, document unresolved rather than inventing a new DUT obligation. Do not implement speculative unrelated features.
Synthetic traces and labels are proposed independent controls, not golden DUT traces or instructions to force a verdict. Challenge any unjustified label with a cited rule and explanation. Additional held-back controls and a fresh reviewer test the revision before freezing. No DUT RTL, real traces, LLM outputs, coverage, targets, model rankings or previous attribution transcript are supplied. This is a post-hoc checker revision; it cannot turn old trajectories into a newly independent effectiveness trial.'''


def verify_registration():
    r=json.loads(REG.read_text());verify_freeze()
    for p,h in r['preserved_hashes'].items():
        if sha(ROOT/p)!=h:raise ValueError('Registered original drift: '+p)
    if r['new_stimulus_generation_calls']!=0 or r['experiment_budget']!=json.loads((OLD/'live-v1/freeze.json').read_text())['development_budget']:
        raise ValueError('Replay scope or budget drift')
    m=json.loads((BASE/'original-evidence-manifest.json').read_text())
    for p,h in m.items():
        if sha(ROOT/p)!=h:raise ValueError('Original evidence drift: '+p)
    return r


def build():
    verify_registration()
    spec=specification()
    if sha(SPEC)!=SPEC_SHA:raise ValueError('PDF drift')
    pages=[]
    for page in (31,32,33,34,35,36,37):
        text=subprocess.run(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(SPEC),'-'],check=True,capture_output=True,text=True).stdout
        pages.append({'pdf_page':page,'text':text})
    spec['wishbone_primary_text']={'file_sha256':SPEC_SHA,'pages':pages,'note':'Full relevant pages; distinguish standard and pipelined rules. Figures extracted as text may lose alignment; no exact latency inferred from figure text.'}
    spec['supplementary_abort_prose']={
        'source':'https://zipcpu.com/blog/2019/07/17/crossbar.html','locations':'discussion of bus abort; Returning data',
        'checked_date':'2026-11-04','authority_level':'Older explanatory article, not a version-specific cancellation timing contract',
        'paraphrase':'The author describes dropping CYC after an error to abort outstanding work; pending transactions have uncertain status. Slave-side cycle withdrawal follows upstream abort. No further response should be attributed to the aborted master cycle. The prose does not specify which buffered requests survive partial propagation or a fixed bound on observing residual forwarding. Code examples are excluded from this specification-only packet.'}
    auth=json.loads((PRIOR/'authorship.json').read_text())
    for f in FILES:
        if sha(PRIOR/f)!=auth['artifact_sha256'][f]:raise ValueError('Checker drift')
    m=json.loads((BASE/'controls-v1/manifest.json').read_text())
    if sha(BASE/'controls-v1/private-inputs.json')!=m['inputs_sha256']:raise ValueError('Controls drift')
    traces=json.loads((BASE/'controls-v1/private-inputs.json').read_text())
    selected=[x for x in m['new_controls'] if x['author_example']]
    return {'role':'independent Claude specification author; post-hoc versioned revision',
        'specification':spec,'candidate':{f:(PRIOR/f).read_text() for f in FILES},
        'synthetic_scenarios':[{**x,'rows':traces[x['name']]} for x in selected],
        'isolation':'No executable DUT, real DUT trace, stimulus model prompt/response, original alarm counts, arm name, target counter, semantic group or performance outcome. Synthetic labels require independent source-based assessment.'}


def prepare(output):
    body=build();prompt=INSTRUCTIONS+'\n'+json.dumps(body,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Author byte cap')
    output.mkdir(parents=True,exist_ok=False)
    (output/'packet.json').write_text(json.dumps(body,indent=2)+'\n');(output/'prompt.txt').write_text(prompt)
    m={'role':'claude_cancel_contract_repair','status':'prepared_not_called',
        'registration_sha256':sha(REG),'builder_sha256':sha(Path(__file__)),
        'packet_sha256':sha(output/'packet.json'),'prompt_sha256':sha(output/'prompt.txt'),
        'prior_authorship_sha256':sha(PRIOR/'authorship.json'),'controls_sha256':sha(BASE/'controls-v1/manifest.json'),
        'bytes':len(prompt.encode()),'calls_planned_max':2,'cli_budget_per_call_usd':4}
    (output/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');return m


def verify_packet(folder,prior):
    if prior.resolve()!=PRIOR:raise ValueError('Unregistered prior')
    m=json.loads((folder/'manifest.json').read_text())
    for key,p in [('registration',REG),('builder',Path(__file__)),('packet',folder/'packet.json'),('prompt',folder/'prompt.txt'),('prior_authorship',PRIOR/'authorship.json'),('controls',BASE/'controls-v1/manifest.json')]:
        if m[key+'_sha256']!=sha(p):raise ValueError('Packet drift: '+key)
    body=build()
    if json.loads((folder/'packet.json').read_text())!=body or (folder/'prompt.txt').read_text()!=INSTRUCTIONS+'\n'+json.dumps(body,separators=(',',':')):raise ValueError('Packet content drift')
    return m


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--register',action='store_true');a=p.parse_args()
    if a.register:register()
    print(json.dumps(prepare(a.output.resolve()),indent=2))
