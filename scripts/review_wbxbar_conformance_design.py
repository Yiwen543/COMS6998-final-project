"""Fresh, bounded design review; cannot authorize implementation or live runs."""
import argparse
import json
import os
from pathlib import Path
from run_midterm_fixed import sha
from prepare_wbxbar_conformance_role import BASE,verify_packet
from probe_wbxbar_cancel_boundary import SCOPE,verify_scope
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE

PREFIX='''Independently review this proposed nondeterministic checker architecture before implementation. No tools or code edits. Return ONLY JSON with findings (list), corrected_contract_requirements (list), required_design_changes (list), and ready_for_implementation (JSON boolean). Do not rubber-stamp the supplied integration questions; assess them against sources and concrete scenarios. Explicitly distinguish a useful design proposal from a proven or implemented algorithm. No approval here authorizes B/C.\n'''


def prepare(output):
    verify_scope();verify_packet(BASE/'claude-design-packet-v1')
    original=json.loads((BASE/'claude-design-packet-v1/packet.json').read_text())
    design=json.loads((BASE/'claude-design-v1/design.json').read_text())
    questions=[
        {'id':'D1','topic':'Unknown alternatives and pass strength','question':'The proposal calls a trace consistent when at least one surviving history is tag-free, even if other viable histories use unknown cancellation. Define separate observable trace-membership, universal checked-property, and hidden-ownership claims. Can this ever promote an unresolved obligation to a stronger pass? Include the old-live identical-identity case and persist uncertainty without guessing an owner.'},
        {'id':'D2','topic':'Exact symmetry','question':'Equal identity, same master/state and unbound data do not by themselves demonstrate a symmetry when FIFO positions differ (e.g. A,B,A). Require a bisimulation or canonical renaming preserving all master/slave order edges, references, multiplicity and future data bindings; do not sort away temporal order.'},
        {'id':'D3','topic':'Component dependency','question':'Shared payload identity is not the only dependency. Master retirement FIFO, slave response FIFO and epoch/cancellation state also couple distinct identities. Define a sound dependency closure and prove local checking/resource-limit fallback does not miss a reachable dependency.'},
        {'id':'D4','topic':'Ghost association and quantification','question':'F3/F4 attach ghost tags to a slave acceptance although physical Wishbone carries no transaction ID. Define how tags are assigned independently, how that assignment is validated, and whether nondeterministic choices are universally or existentially quantified. Do not use an assumed correct mapping to prove correct mapping.'},
        {'id':'D5','topic':'Cancellation bound applicability','question':'C1 with no new acceptance may bound only the quiet interval. It cannot automatically erase identities before future restart, nor does empty output imply empty buffers. Require a restart-safe noninterference claim before releasing old work. Address repeated aborts and avoid one-bit epoch aliasing.'},
        {'id':'D6','topic':'ERR and ghost counter scope','question':'F3 ERR iff unmapped or slave-ERRed appears stronger than K8, which keeps timeout/starvation unexplained errors unknown. Make guards/unknown cases consistent. Also specify widths/overflow invariants for cumulative symbolic counters; an unbounded proof cannot quietly rely on the finite pilot horizon.'},
        {'id':'D7','topic':'Revised expected control labels','question':'K5 withdraws both across-slave and within-slave forward order. Assess old same-slave reordered-write controls separately: public ordering/side-effect assumptions must be explicit. Identify changes before any experimental replay; do not force legacy labels or quietly weaken required data/response guarantees.'}]
    multi=json.loads((BASE.parent/'wbxbar_abort_contract_20261104/controls-v1/private-inputs.json').read_text())
    body={'role':'fresh independent specification-design reviewer','specification':original['specification'],'proposed_design':design,
        'synthetic_controls':original['synthetic_controls'],
        'additional_existing_synthetic_case':{'name':'multi_abort/live_aborted_same_identity','rows':multi['multi_abort/live_aborted_same_identity'],'note':'Independent synthetic control, not a DUT or LLM trace; no verdict supplied.'},
        'integration_questions':questions,
        'exact_fixture_corrections':{'second_read_value':'0x9876fedc (not the design prose 0x98765432)','later_good_read_value':'0x88887777 (not 0x88888877)','later_corrupted_read_value':'0x88887776 (not 0x88888876)'},
        'isolation':'No DUT RTL or actual pin traces, version-specific proof results, prior B/C metrics, coverage groups, witness targeting or experimental model prompts.'}
    prompt=PREFIX+json.dumps(body,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Review byte cap')
    output.mkdir(parents=True,exist_ok=False)
    (output/'packet.json').write_text(json.dumps(body,indent=2)+'\n');(output/'prompt.txt').write_text(prompt)
    m={'status':'prepared_not_called','scope_sha256':sha(SCOPE),'source_sha256':sha(Path(__file__)),'packet_sha256':sha(output/'packet.json'),
       'prompt_sha256':sha(output/'prompt.txt'),'design_sha256':sha(BASE/'claude-design-v1/design.json'),'bytes':len(prompt.encode()),'planned_calls':1,'cli_budget_usd':4}
    (output/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');return m


def verify(folder):
    verify_scope();m=json.loads((folder/'manifest.json').read_text())
    for key,p in [('scope',SCOPE),('source',Path(__file__)),('packet',folder/'packet.json'),('prompt',folder/'prompt.txt'),('design',BASE/'claude-design-v1/design.json')]:
        if sha(p)!=m[key+'_sha256']:raise ValueError('Review packet drift: '+key)
    return m


def run(packet,output):
    verify(packet)
    if output.exists():raise ValueError('Never overwrite a model call')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode&0o077:raise ValueError('Hidden key absent or unsafe')
    env={k:v for k,v in os.environ.items() if not k.startswith(('OPENAI_','ANTHROPIC_','CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip()
    try:
        r=call((packet/'prompt.txt').read_text(),output,env,'WBXBAR independent reference-semantics reviewer')
        (output/'review.json').write_text(json.dumps(r,indent=2)+'\n')
        valid=set(r)=={'findings','corrected_contract_requirements','required_design_changes','ready_for_implementation'} and type(r.get('ready_for_implementation')) is bool
        result={'schema_valid':valid,'review_received':True,'model_readiness':r.get('ready_for_implementation') if valid else None,'automatic_live_permission':False}
        (output/'validation.json').write_text(json.dumps(result,indent=2)+'\n');return result
    finally:
        KEY_FILE.unlink(missing_ok=True);env.pop('ANTHROPIC_API_KEY',None);verify_scope()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','run']);p.add_argument('--output',type=Path,required=True);p.add_argument('--packet',type=Path);a=p.parse_args()
    print(json.dumps(prepare(a.output.resolve()) if a.mode=='prepare' else run(a.packet.resolve(),a.output.resolve()),indent=2))
