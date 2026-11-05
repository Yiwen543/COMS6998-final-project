"""Prepare a spec-only design review before implementing another functional checker."""
import argparse
import copy
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from wbxbar_checker_controls import empty_rows,transfer,settle
from probe_wbxbar_cancel_boundary import SCOPE,verify_scope

BASE=ROOT/'results/wbxbar_conformance_gate_20261104'
PRIOR=ROOT/'results/wbxbar_abort_contract_20261104/claude-v4/candidate'
FILES=('checker.py','selftest.py','properties.json','contract.md')
INSTRUCTIONS='''You are Claude, independent specification/verification architect. This call designs the next checker contract and formal obligations; DO NOT modify or implement checker, DUT, driver, or stimulus yet. Return ONLY JSON with keys clause_matrix, ownership_algorithm, formal_obligations, synthetic_control_assessments, implementation_plan, unresolved, ready_for_implementation.
The project must resolve three limitations without tailoring rules to DUT implementation: unspecified cancellation propagation, ambiguity that disables an entire reset epoch, and inferred per-master forwarding order across different slaves. Public sources and your prior checker are provided, but NO executable DUT, real trace, coverage, targeting data or model outcomes.
For each clause state source, normative/assumption/inferred/unknown status, executable observables, acceptance semantics and exclusions. Public response-order guarantees do not automatically imply global forward-order guarantees. Distinguish trace consistency under a nondeterministic reference from proof of actual hidden ownership; identical public transactions may be inherently indistinguishable. Never label all ambiguous behavior a pass or silently select one owner. Preserve all feasible histories or prove a sound abstraction; declare a resource limit and unresolved-on-limit behavior without arbitrary pruning. Report property-local uncertainty and resume unrelated checks where justified.
Cancellation requires a sound boundary before old identities can be discarded; idle outputs alone cannot establish empty hidden buffers. Derive version-independent safety obligations from public contract, and separately propose implementation-specific characterization obligations with explicit assumptions. No guessed delay bound, no DUT-derived expected outputs, no assertion assumed to prove itself. Proposed formal properties need nonvacuity and deliberately false controls. Explain which require legal environment assumptions and distinguish bmc evidence from unbounded prove. Reset, ERR, multiple outstanding requests, partial cancellation, duplicate multiplicity and new-epoch read/write data must remain covered.
Synthetic labels are proposed controls only. Challenge unjustified labels with source reasoning. Design discrimination tests for valid cross-slave early forwarding with ordered response retirement, wrong retirement/data, identical requests later distinguished by responses, and faults after or during ambiguity. Maintain all previous justified corruption/duplicate/reset/response controls, identifying any wrongly inferred expected label explicitly.
Before live B/C, require implementation, independent controls, fresh code review, certificates for any extra contract claims, separate freeze and immutable saved-action replay. Keep the original driver and budgets; do not suggest suppressing errors, forcing reset after ambiguity, unique-tag injection or one-outstanding-only traffic as an undisclosed primary-experiment restriction. Such changes would require a separately registered scope and are not authorized by this design packet. Do not optimize the task to make C win.'''


def controls():
    cases={}
    rows=empty_rows(28)
    transfer(rows,accept=6,forward=10,response=11,returned=12,addr=5,read_data=0x1234abcd)
    transfer(rows,slave=1,accept=7,forward=9,response=10,returned=13,addr=0x15,read_data=0x9876fedc)
    cases['cross_slave/early_forward_ordered_retirement']={'rows':settle(rows),'proposed':'must not report violation solely for cross-slave forwarding order; architect decides supported scoped pass vs unresolved'}
    rows=copy.deepcopy(rows);rows[12]['pre']['o_mdata']=0x9876fedc;rows[13]['pre']['o_mdata']=0x1234abcd
    cases['cross_slave/wrong_retirement_data']={'rows':settle(rows),'proposed':'detect wrong returned data/order; distinct data makes the fault externally observable'}
    rows=empty_rows(28)
    transfer(rows,accept=6,forward=8,response=9,returned=10,addr=5,read_data=0x1234abcd)
    transfer(rows,master=1,accept=6,forward=9,response=10,returned=11,addr=5,read_data=0x9876fedc)
    cases['ambiguity/identical_requests_later_responses']={'rows':settle(rows),'proposed':'keep feasible ownership candidates; explicitly distinguish observable trace consistency from hidden-owner proof'}
    rows=copy.deepcopy(rows)
    transfer(rows,accept=15,forward=17,response=18,returned=19,addr=7,read_data=0x88887777)
    cases['ambiguity/followed_by_distinct_work']={'rows':settle(rows),'proposed':'do not disable checking of independent subsequent work for the whole reset epoch'}
    bad=copy.deepcopy(rows);bad[19]['pre']['o_mdata']=0x88887776
    cases['ambiguity/later_data_corruption']={'rows':settle(bad),'proposed':'detect uniquely observable new read-data corruption despite previous ambiguity'}
    bad=copy.deepcopy(rows);bad[17]['pre']['o_saddr']=12
    cases['ambiguity/later_unaccepted_address']={'rows':settle(bad),'proposed':'detect a forward with no valid live or canceled identity; previous ambiguity cannot hide it'}
    rows=empty_rows(28)
    transfer(rows,accept=6,forward=8,response=9,returned=10,addr=5,read_data=0x1234abcd)
    transfer(rows,master=1,accept=6,forward=9,response=10,returned=11,addr=5,read_data=0x1234abcd)
    cases['ambiguity/inherently_indistinguishable']={'rows':settle(rows),'proposed':'do not claim actual ownership uniquely established; identical observations cannot supply absent transaction tags'}
    return cases


def prepare(output):
    verify_scope();auth=json.loads((PRIOR/'authorship.json').read_text())
    for f in FILES:
        if sha(PRIOR/f)!=auth['artifact_sha256'][f]:raise ValueError('Prior checker drift')
    spec=json.loads((ROOT/'results/wbxbar_abort_contract_20261104/spec-packet-v1/packet.json').read_text())['specification']
    body={'role':'Independent Claude normative contract and checker architecture; no code edits in this stage',
        'specification':spec,'prior_claude_artifacts':{f:(PRIOR/f).read_text() for f in FILES},'synthetic_controls':controls(),
        'questions':['Specify sound local property status and resource-bounded candidate ownership accounting.',
                     'Specify how to handle cross-slave forwarding independently of ordered responses, with no unjustified rule.',
                     'Specify cancellation safety/progress obligations that can actually be validated and assumptions needed; do not infer buffer emptiness from public idle.',
                     'Identify exactly what remains unknowable through the public interface and how it limits any pass claim.'],
        'isolation':'No DUT implementation, actual pins, previous performance, E-graph target or observed version-specific proof bound. GPT provides integration/scenarios, not expected checker code.'}
    prompt=INSTRUCTIONS+'\n'+json.dumps(body,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Byte cap')
    output.mkdir(parents=True,exist_ok=False)
    (output/'packet.json').write_text(json.dumps(body,indent=2)+'\n');(output/'prompt.txt').write_text(prompt)
    m={'status':'prepared_no_call','role':'Claude contract/architecture before implementation','registration_sha256':sha(SCOPE),
        'builder_sha256':sha(Path(__file__)),'packet_sha256':sha(output/'packet.json'),'prompt_sha256':sha(output/'prompt.txt'),
        'prior_authorship_sha256':sha(PRIOR/'authorship.json'),'bytes':len(prompt.encode()),'planned_model_calls':1,'cli_budget_usd':4,'timeout_seconds':600,
        'not_included':['DUT RTL','actual trace','B/C outcome','formal characterization result'],'live_B_allowed':False,'live_C_allowed':False}
    (output/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');return m


def verify_packet(output):
    verify_scope();m=json.loads((output/'manifest.json').read_text())
    for k,p in [('registration',SCOPE),('builder',Path(__file__)),('packet',output/'packet.json'),('prompt',output/'prompt.txt'),('prior_authorship',PRIOR/'authorship.json')]:
        if sha(p)!=m[k+'_sha256']:raise ValueError('Packet drift: '+k)
    return m


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(prepare(a.output.resolve()),indent=2))
