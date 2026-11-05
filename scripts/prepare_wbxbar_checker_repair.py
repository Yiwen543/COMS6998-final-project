"""Claude-only exact repair: spec, own artifacts and synthetic control feedback."""
import argparse
import json
from pathlib import Path
from prepare_wbxbar_checker_role import packet as specification, verify_scope, SCOPE
from run_midterm_fixed import ROOT, sha

BASE = ROOT / 'results/wbxbar_exploratory_bc_20261104'
FILES = ('checker.py', 'selftest.py', 'properties.json', 'contract.md')
INSTRUCTIONS = '''You are Claude, the original independent checker-author role. Repair only your own checker artifacts.
Return ONLY JSON {patches:[{file,before,after}],rationale:[strings]}. Each before must occur exactly once in its file.
Allowed files: checker.py, selftest.py, properties.json, contract.md. Preserve pure-Python restrictions and check_rows schema.
No driver, RTL, target, budget, stimulus, coverage or evaluation changes. Do not loosen checks to make observed DUT traces pass.
This packet contains public specification, your original artifacts, fresh independent review findings and synthetic control
feedback only. It contains NO DUT implementation, DUT calibration traces or experimental outcomes.
Fix F1 using conservative disposition (a): a mapped ERR not explained by a matching slave ERR is explicitly unresolved,
not scoped_pass or an asserted timeout/starvation mechanism. Retain observed error evidence; do not invent a precise timer.
The unresolved obligation must persist across later reset/restart within the same cumulative batch. Ordinary decoded and
matched slave errors must remain handled. The synthetic early error can be unresolved rather than a positively detected defect.
Fix F6: comparisons of write payload for transfer matching/preservation use only SEL-enabled byte lanes. Preserve address,
direction, SEL and enabled-lane checks; read-data checks stay intact. Do not make all payload matching ambiguous or unchecked.
Update properties and contract consistently, documenting inactive-CYC responses, timing/abort liveness and reset limits.
Update concise selftests for these repairs. Do not silently broaden to unproven timeout/arbitration semantics.
Synthetic feedback is not a required golden implementation. If a control conflicts with public requirements, explain it
instead of weakening a valid rule. A new read-only reviewer will re-evaluate all old and expanded controls.'''


def build(prior):
    verify_scope()
    author = json.loads((prior / 'authorship.json').read_text())
    for name in FILES:
        if sha(prior / name) != author['artifact_sha256'][name]: raise ValueError('Prior checker changed')
    review = json.loads((BASE / 'claude-v1/review.json').read_text())
    controls = json.loads((BASE / 'controls-v5/private-inputs.json').read_text())
    evaluation = json.loads((BASE / 'evaluation-v4/summary.json').read_text())
    names = ['negative/early_unexplained_error', 'unresolved/unclassified_late_error',
             'positive/masked_write_bytes', 'negative/write_data']
    return {'role': 'Claude checker author exact repair', 'specification': specification(),
        'candidate': {name: (prior / name).read_text() for name in FILES},
        'review_findings': [f for f in review['findings'] if f['id'] in ('F1','F2','F4','F6','F7','F9')],
        'synthetic_feedback': {name: {'rows': controls[name], 'checker_result': evaluation['cases'][name]} for name in names},
        'control_scope': 'These hand-constructed controls were independently authored, never generated from DUT RTL/simulation. Expanded held-back validation also covers bus abort/restart, stalls, ERR bursts, ambiguity and pending batches.',
        'independence': 'No DUT implementation, DUT-derived traces, guard/source-target evidence, model stimulus or B/C outcomes.'}


def prepare(prior, output):
    body = build(prior)
    prompt = INSTRUCTIONS + '\n' + json.dumps(body, separators=(',', ':'))
    if len(prompt.encode()) > 150000: raise ValueError('Repair byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    m = {'status': 'prepared_not_called', 'role': 'claude_exact_checker_repair',
         'scope_sha256': sha(SCOPE), 'builder_sha256': sha(Path(__file__)),
         'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
         'prior_authorship_sha256': sha(prior / 'authorship.json'), 'bytes': len(prompt.encode()),
         'max_calls': 2, 'cli_budget_per_call_usd': 4, 'source_hashes': {
             str(p): sha(p) for p in [BASE/'claude-v1/review.json', BASE/'controls-v5/private-inputs.json',
                                      BASE/'evaluation-v4/summary.json']}}
    (output / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    return m


def verify_packet(folder, prior):
    m = json.loads((folder / 'manifest.json').read_text())
    for key, p in [('scope', SCOPE), ('builder', Path(__file__)), ('packet', folder/'packet.json'),
                   ('prompt', folder/'prompt.txt'), ('prior_authorship', prior/'authorship.json')]:
        if m[key+'_sha256'] != sha(p): raise ValueError('Repair provenance drift: ' + key)
    for name, digest in m['source_hashes'].items():
        if sha(Path(name)) != digest: raise ValueError('Repair source drift')
    body = build(prior)
    if json.loads((folder/'packet.json').read_text()) != body: raise ValueError('Repair packet content drift')
    if (folder/'prompt.txt').read_text() != INSTRUCTIONS+'\n'+json.dumps(body,separators=(',',':')):
        raise ValueError('Repair prompt content drift')
    return m


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--prior', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(prepare(a.prior.resolve(), a.output.resolve()), indent=2))
