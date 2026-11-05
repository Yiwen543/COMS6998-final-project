"""Spec-only abort-boundary repair; never pass attribution RTL/DUT traces to author."""
import argparse
import json
from pathlib import Path
from prepare_wbxbar_checker_role import packet as specification,verify_scope,SCOPE
from prepare_wbxbar_checker_repair import FILES,BASE
from run_midterm_fixed import sha

INSTRUCTIONS='''You are Claude, the original independent checker-author role. Apply an exact, narrowly scoped repair to your own artifacts.
Return ONLY JSON {patches:[{file,before,after}],rationale:[strings]}. Each before occurs exactly once in its allowlisted file.
Allowed files: checker.py, selftest.py, properties.json, contract.md. Preserve pure-Python restrictions, schema and prior fixes.
No DUT, driver, targets, budgets, stimulus or measurement edits. No exact abort-propagation delay is established by public prose.
The reviewer requires this conservative classification repair: keep identities of accepted but unforwarded work when master
CYC is withdrawn. If a later slave acceptance uniquely matches the oldest relevant aborted/unforwarded request, classify it
as unresolved post_abort_forward, with original acceptance/abort/forward evidence. Never count its completion or recovery;
discard its return as old/orphaned work. Consume its identity once so duplicate forwards cannot repeatedly reuse a tombstone.
A request matching neither live work nor retained aborted work still fails. A corrupted enabled write byte, address, SEL or
direction must not be forgiven by abort. Multiple possible live/aborted owners must remain unresolved, not guessed.
No arbitrary one-cycle or multi-cycle cutoff: even a later matching forward is unresolved unless the public spec proves its
status. Reset clears old work identities, while unresolved findings already emitted persist for the cumulative batch.
Document this limited scope. Unexplained mapped ERR remains unresolved; preserve SEL-enabled comparisons and all prior checks.
Add concise selftests for matching aborted forwarding, corrupted forwarding, later forwarding, reset separation and duplicate
identity consumption. The integration role will independently rerun all control versions and both-simulator driver evidence.
Use only the supplied public contract, your own code and independent synthetic hand traces. No DUT implementation or actual
DUT traces are supplied. Do not weaken a valid rule merely to fit a trace; disclose ambiguity or control/spec conflict.'''


def build(prior):
    verify_scope();auth=json.loads((prior/'authorship.json').read_text())
    for name in FILES:
        if sha(prior/name)!=auth['artifact_sha256'][name]:raise ValueError('Prior artifact drift')
    inputs=json.loads((BASE/'controls-v6/private-inputs.json').read_text())
    results=json.loads((BASE/'evaluation-v6/summary.json').read_text())
    names=['unresolved/post_abort_forward','unresolved/late_post_abort_forward',
           'negative/post_abort_corrupt_data','negative/post_abort_unaccepted_address']
    return {'role':'Claude exact checker repair; independent of GPT driver/stimulus',
        'specification':specification(),'candidate':{name:(prior/name).read_text() for name in FILES},
        'review_requirement':'Fresh independent review requests conservative unresolved classification for matching accepted work arriving after upstream abort because no abort-propagation latency is specified. Keep nonmatching requests as violations. Previous ERR and byte-mask fixes were accepted.',
        'synthetic_feedback':{name:{'rows':inputs[name],'checker_result':results['cases'][name]} for name in names},
        'isolation':'No executable DUT, actual DUT traces, internal timing thresholds, source targets, egraph groups or experimental model outcomes. The full attribution review is deliberately NOT included.'}


def prepare(prior,output):
    body=build(prior);prompt=INSTRUCTIONS+'\n'+json.dumps(body,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Repair byte cap')
    output.mkdir(parents=True,exist_ok=False)
    (output/'packet.json').write_text(json.dumps(body,indent=2)+'\n');(output/'prompt.txt').write_text(prompt)
    m={'status':'prepared_not_called','role':'claude_abort_checker_repair','scope_sha256':sha(SCOPE),
       'builder_sha256':sha(Path(__file__)),'packet_sha256':sha(output/'packet.json'),'prompt_sha256':sha(output/'prompt.txt'),
       'prior_authorship_sha256':sha(prior/'authorship.json'),'bytes':len(prompt.encode()),'max_calls':2,'cli_budget_per_call_usd':4,
       'source_hashes':{str(p):sha(p) for p in [BASE/'controls-v6/private-inputs.json',BASE/'evaluation-v6/summary.json']}}
    (output/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');return m


def verify_packet(folder,prior):
    m=json.loads((folder/'manifest.json').read_text())
    for key,p in [('scope',SCOPE),('builder',Path(__file__)),('packet',folder/'packet.json'),
                  ('prompt',folder/'prompt.txt'),('prior_authorship',prior/'authorship.json')]:
        if m[key+'_sha256']!=sha(p):raise ValueError('Abort repair drift: '+key)
    for name,digest in m['source_hashes'].items():
        if sha(Path(name))!=digest:raise ValueError('Abort repair source drift')
    body=build(prior)
    if json.loads((folder/'packet.json').read_text())!=body:raise ValueError('Abort packet content drift')
    if (folder/'prompt.txt').read_text()!=INSTRUCTIONS+'\n'+json.dumps(body,separators=(',',':')):
        raise ValueError('Abort prompt content drift')
    return m


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prior',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    print(json.dumps(prepare(a.prior.resolve(),a.output.resolve()),indent=2))
