#!/usr/bin/env python3
"""Matched transaction-monitor synthesis with one shared unassisted candidate per trial."""
import argparse
from functools import partial
import hashlib
import json
import os
from pathlib import Path

from egg_fifo_loop_provider import ProviderError, respond
from egg_frame_faults import DEVELOPMENT, TRACES, load_corpus
from egg_frame_pc_loop import ARMS, _validate_receipt, compact, packet_metrics, save
from egg_txn_terms import REFERENCES, abstract, parse_term, referenced_signals, sample, typed_oracle
from egg_txn_observe import score_corpus
from egg_txn_certificate import diagnose, certify
from predicates import ROOT

TASK_ID = 'frame-transaction-v1'
SYSTEM = ('You verify the original AXI Frame Length Adjuster specification. Generate passive violation monitors only. '
          'Do not change the RTL, the specification, or the trusted ghost tracker. '
          'A supplied diagnostic or proof explains only the current candidate and its observed polarity, not the specification.')
TASK = '''The pinned frame_task is an 8-bit AXI stream frame length adjuster with MIN=4 and MAX=8, and independent output data/header FIFOs. Every accepted nonempty input frame has at most 12 bytes. A transfer occurs only when valid and ready are both high. Synchronous reset discards all pending frames and partial input. The adjusted output frame retains input bytes in order up to eight, appends zero bytes to reach four if short, and marks only its final output beat with TLAST. Header presentation must correspond in order to a completed accepted input frame, with its exact original length, clamped length, pad and truncate flags. Header and data consumers can progress independently.
A trusted passive ghost tracker is supplied; do NOT invent extra state or expected-value signals. At PRE, the ghost reflects only strictly earlier rising edges; at POST, it includes the current edge's transfers/reset. A presented output must be correct even when ready is low. No same-edge PRE bypass from input. Counts describe observed transfers, not correctness: input_count is the number of nonempty frames started by accepted input beats since reset (includes the latest incomplete frame); data_count is the number of observed output data TLAST transfers; header_count is the number of observed header transfers. These are independent zero-based frame cursors; a cursor may be past input_count in a faulty trace. data_index is the one-based next output beat position within its observed frame. data_n/data_done are the currently accepted byte count and completion (input TLAST seen) of the input frame at the data cursor. header_n/header_done are the corresponding raw record at the header cursor. When a cursor is out of range, its n=0 and done=false; data_byte is the accepted input byte at the indicated data position when available, otherwise unspecified. input_open means the newest accepted frame is not completed. The tracker does not calculate expected adjusted length, output bytes, TLAST or flags. phase_post marks POST, final_sample marks the last POST of a finite trace; end-of-trace completion is not an unconditional liveness assertion. Unknown X/Z pins may be unobservable; scoring keeps those cases separately.
Write nine Boolean violation formulas, true exactly when each named property is violated:
- data_entitlement: outside reset, a presented data beat must be justified by previously accepted input data in that frame or completed short-frame padding, and be within the maximum adjusted length. No output from nonexistent frames or beyond accepted prefix before completion.
- data_payload: for a justified presented data beat outside reset, the byte must preserve the corresponding accepted input byte, or be zero if it is a padding byte.
- data_last: for a justified presented data beat outside reset, TLAST must indicate exactly the correct final adjusted position. This includes an early truncation boundary at eight even before input TLAST arrives, and padding short completed frames to four.
- header_entitlement: outside reset, a presented header must refer to the completed accepted frame at its own cursor, not just any input frame.
- header_original: for a justified presented header outside reset, report the corresponding true accepted original length.
- header_adjusted: for a justified presented header outside reset, report that true accepted length clamped to [4,8], not merely a value in the allowed range or a function of the DUT's untrusted reported original length.
- header_flags: for a justified presented header outside reset, both flags must be correct for the true accepted original frame length (pad strictly below four, truncate strictly above eight).
- reset_clear: immediately after a reset edge (POST only), both output valids must be low; PRE while reset is asserted is not the post-edge state.
- drain_complete: at final_sample require no remaining offered input, no visible output valids, no partial input frame, and independent data and header completion counts equal the started input count. The finite testbench separately checks a sufficient quiet drain tail.
Pin Booleans: rst,s_valid,s_last,s_ready,m_valid,m_last,m_ready,h_valid,h_ready,h_pad,h_truncate. Extra Booleans: phase_post,final_sample,input_open,data_done,header_done. Unsigned 8-bit buses: s_data,m_data,data_byte. Unsigned 16-bit buses: h_length,h_original_length,input_count,data_count,header_count,data_index,data_n,header_n. Allowed binary Boolean operators and,or,xor; unary not; same-type eq,ne; unsigned ult,ule,ugt,uge; decimal constants in operand width; true,false. All expressions must be fully parenthesized S-expressions, binary operators have exactly two operands. A Boolean violation is not an assertion success.
Submit exactly the nine named monitors. Feedback, if present later, contains actual PRE/POST development observations or a two-state symbolic snapshot counterexample (not necessarily reachable on RTL); candidate diagnoses and checked restricted-cube certificates, if present, justify the current candidate only. Held-out observations are never in feedback.'''
SCHEMA = {'type':'object','properties':{'monitors':{'type':'object','properties':{k:{'type':'string'} for k in REFERENCES},'required':list(REFERENCES),'additionalProperties':False}},'required':['monitors'],'additionalProperties':False}

# Frozen offline plumbing workload. Not a model-generated seed and not a claimed LLM result.
FIXTURE_INITIAL = {
    'data_entitlement': '(and (not rst) (and m_valid (uge data_count input_count)))',
    'data_payload': '(and (not rst) (and m_valid (ne m_data data_byte)))',
    'data_last': '(and (not rst) (and m_valid (xor m_last (eq data_index data_n))))',
    'header_entitlement': '(and (not rst) (and h_valid (uge header_count input_count)))',
    'header_original': '(and (not rst) (and h_valid (ne h_original_length header_n)))',
    'header_adjusted': '(and (not rst) (and h_valid (or (ult h_length 4) (ugt h_length 8))))',
    'header_flags': '(and (not rst) (and h_valid (or (xor h_pad (ult h_original_length 4)) (xor h_truncate (ugt h_original_length 8)))))',
    'reset_clear': '(and rst (or m_valid h_valid))',
    'drain_complete': '(and final_sample (or s_valid (or m_valid h_valid)))',
}
PARTIAL = ('data_entitlement','data_payload','header_entitlement','reset_clear')
ALIASES = {'original':'original','F02':'probe_A','F05':'probe_B'}
NEXT = '\nSubmit all nine monitors again.'


def fixture_revision(turn):
    if turn not in (0,1,2,3):
        raise ValueError('unsupported fixture turn')
    result = dict(FIXTURE_INITIAL)
    for k in (() if turn==0 else PARTIAL if turn==1 else REFERENCES):
        result[k] = REFERENCES[k]
    return result


def validate(output):
    if not isinstance(output,dict) or set(output)!={'monitors'} or not isinstance(output['monitors'],dict) or set(output['monitors'])!=set(REFERENCES):
        raise ValueError('submit exactly the nine monitor strings')
    result = output['monitors']
    for name in REFERENCES:
        term = result[name]
        if not isinstance(term,str) or not term.strip() or len(term)>4096:
            raise ValueError(f'{name}: expected nonempty expression at most 4096 characters')
        try:
            _, atoms = abstract(parse_term(term))
        except (ValueError,RecursionError) as exc:
            raise ValueError(f'{name}: {exc}') from exc
        if len(atoms)>48:
            raise ValueError(f'{name}: more than 48 distinct abstract atoms')
    return result


def grade(oracles,physical):
    counts=physical['totals_by_design']
    keys=('missed','false_alarm','unknown_both','unknown_mismatch','ineligible','matched_known','reference_alarms','candidate_alarms','matched_alarms')
    total={k:sum(x[k] for x in counts.values()) for k in keys}
    refs=[d for d,x in sorted(counts.items()) if d!='original' and x['reference_alarms']]
    result={'equivalent_properties':sum(x['equivalent'] is True for x in oracles.values()),
            'inequivalent_properties':sum(x['equivalent'] is False for x in oracles.values()),
            'unresolved_properties':sum(x['equivalent'] is None for x in oracles.values()),
            'matched_reference_faults':[d for d in refs if counts[d]['matched_alarms']],
            'reference_detectable_faults':refs, **total}
    # Intrinsic unknown/unobservable snapshots remain explicit, not credited as known pass.
    result['verified']=(result['equivalent_properties']==len(REFERENCES) and
                        total['missed']==total['false_alarm']==total['unknown_mismatch']==0)
    return result


def prepare_common(monitors,oracles,physical):
    """Only the pre-fixed development cases can contribute public real observations."""
    visible,selected = {},{}
    fields=('reference_alarms','candidate_alarms','missed','false_alarm','unknown_both','unknown_mismatch','ineligible')
    for design in DEVELOPMENT:
        alias=ALIASES[design]
        totals={n:{k:0 for k in fields} for n in REFERENCES};cycles=0
        for scenario in TRACES:
            case=physical['cases'][design][scenario];cycles+=case['cycles']
            for name, row in case['properties'].items():
                for k in fields:totals[name][k]+=row[k]
                if name not in selected and row['first_mismatch'] is not None:
                    selected[name]={'origin':'physical','design':alias,'trace':scenario,**row['first_mismatch']}
        visible[alias]={'cycles':cycles,'traces':len(TRACES),'properties':totals}
    observations,review={},{}
    for name,reference in REFERENCES.items():
        oracle=oracles[name]
        if oracle['status'] not in ('sat','unsat','unknown') or oracle['equivalent'] is not {'sat':False,'unsat':True,'unknown':None}[oracle['status']]:
            raise ValueError('inconsistent typed oracle')
        symbol=None
        if oracle['status']=='sat':
            symbol={'origin':'symbolic','values':oracle['counterexample'],'reference_value':oracle['reference_value'],'candidate_value':oracle['candidate_value']}
        if symbol is not None:
            a,b=sample(parse_term(reference),symbol['values']),sample(parse_term(monitors[name]),symbol['values'])
            if a is not symbol['reference_value'] or b is not symbol['candidate_value'] or a==b or a is None or b is None:
                raise ValueError('archived symbolic counterexample does not replay')
        witness=selected.get(name,symbol)
        public=None
        if witness is not None:
            a,b=sample(parse_term(reference),witness['values']),sample(parse_term(monitors[name]),witness['values'])
            if a is not witness['reference_value'] or b is not witness['candidate_value'] or a==b or a is None or b is None or oracle['equivalent'] is True:
                raise ValueError('common observation is not a valid mismatch')
            public={k:v for k,v in witness.items() if k!='values'}
            # Full raw ghost context, no expected values or reference expression.
            public['pins']=witness['values']
        observations[name]=witness
        review[name]={'equivalent':oracle['equivalent'],'typed_xor':oracle['status'],'counterexample':public}
    return {'public':{'visible_rtl_observations':visible,'semantic_review':review},'observations':observations}


class Evaluator:
    def __init__(self,corpus,binary):
        self.corpus=corpus;self.binary=binary
        self.cache,self.oracles,self.diagnoses,self.certificates={},{},{},{}

    def common(self,monitors):
        key=tuple(monitors[n] for n in REFERENCES)
        if key not in self.cache:
            physical=score_corpus(self.corpus,monitors)
            oracles={}
            for n,ref in REFERENCES.items():
                p=(ref,monitors[n]);
                if p not in self.oracles:self.oracles[p]=typed_oracle(*p)
                oracles[n]=self.oracles[p]
            common=prepare_common(monitors,oracles,physical)
            self.cache[key]=(physical,oracles,common,grade(oracles,physical))
        return key,self.cache[key]

    def stage(self,output,arm,path):
        try:
            monitors=validate(output)
        except ValueError as exc:
            result={'candidate_error':str(exc),'verified':False}
            text='Invalid candidate: '+str(exc)
        else:
            key,(physical,oracles,common,result)=self.common(monitors)
            for file,data in [('physical-score',physical),('oracles',oracles),('common',common)]:save(path/(file+'.json'),data)
            packet=dict(common['public'])
            if arm!='raw':
                if key not in self.diagnoses:
                    self.diagnoses[key]={n:diagnose(monitors[n],obs['values'],obs['candidate_value']) for n,obs in common['observations'].items() if obs is not None}
                diags=self.diagnoses[key];save(path/'diagnoses.json',diags)
                packet['candidate_diagnoses']={n:d['public'] for n,d in diags.items()}
                if arm=='egg':
                    if key not in self.certificates:self.certificates[key]={n:certify(d,self.binary) for n,d in diags.items()}
                    certs=self.certificates[key];save(path/'certificates.json',certs)
                    packet['egg_certificates']={n:c['public'] for n,c in certs.items()}
            text=compact(packet)
        save(path/'assessment.json',result)
        (path/'feedback.txt').write_text(text+'\n',encoding='utf-8')
        return result,text


def initial_messages():return [{'role':'system','content':SYSTEM},{'role':'user','content':TASK}]


def append(history,output,packet):
    history.extend([{'role':'assistant','content':json.dumps(output,sort_keys=True)}, {'role':'user','content':packet+NEXT}])


def run(*,corpus_dir,binary,out,mode,trials,rounds,provider=None,provider_config=None):
    if mode not in ('live','fixture') or type(trials) is not int or not 1<=trials<=5 or type(rounds) is not int or not 1<=rounds<=3:
        raise ValueError('invalid experiment budget')
    if mode=='fixture' and (provider is not None or provider_config is not None):raise ValueError('fixture never uses a provider')
    if mode=='live' and (not callable(provider) or not isinstance(provider_config,dict) or
                        not provider_config.get('model') or type(provider_config.get('max_output_tokens')) is not int or
                        not 16<=provider_config['max_output_tokens']<=4096):raise ValueError('invalid live provider/budget')
    binary=Path(binary).resolve(strict=True);out=Path(out);corpus_dir=Path(corpus_dir)
    corpus=load_corpus(corpus_dir)
    config={'schema':1,'mode':mode,'task':TASK_ID,'arms':list(ARMS),'trials':trials,'repair_rounds':rounds,'provider':provider_config,
            'corpus_sha256':json.loads((corpus_dir/'summary.json').read_text())['corpus_sha256'],
            'visible_designs':list(DEVELOPMENT),'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest()}
    out.mkdir(parents=True,exist_ok=False);save(out/'config.json',config)
    evaluator=Evaluator(corpus,binary)
    if mode=='fixture':
        for turn in range(rounds+1):evaluator.common(fixture_revision(turn))
    keys=('input_tokens','output_tokens','total_tokens')
    initial_usage={k:0 for k in keys} if mode=='live' else None
    usage={arm:{k:0 for k in keys} for arm in ARMS} if mode=='live' else None
    ids,models,sessions=set(),set(),{}
    seq=0

    def call(path,messages,turn,arm,trial):
        nonlocal seq
        save(path/'request.json',{'messages':messages,'response_schema':SCHEMA});seq+=1
        try:
            if mode=='fixture':response={'id':f'fixture-txn-{seq:03d}','output':{'monitors':fixture_revision(turn)},'usage':None,'dispatch_attempted':False}
            else:response=provider([dict(m) for m in messages],SCHEMA)
        except ProviderError as exc:
            save(path/'provider-error.json',{'error':str(exc),'receipt':exc.receipt})
            save(out/'incomplete.json',{'completed_responses':len(ids),'attempted_steps':seq,'trial':trial,'arm':arm,'round':turn,'initial_usage':initial_usage,'completed_usage':usage})
            raise
        save(path/'response.json',response)
        if mode=='fixture':
            if response['id'] in ids or response['usage'] is not None or response['dispatch_attempted'] is not False:raise ValueError('fixture receipt')
            ids.add(response['id'])
        else:
            _validate_receipt(response,mode,provider_config,ids,models)
            total=initial_usage if arm=='initial' else usage[arm]
            for k in keys:total[k]+=response['usage'][k]
        return response['output']

    for t in range(1,trials+1):
        trial=f'trial-{t:02d}';folder=out/trial
        path=folder/'initial';path.mkdir(parents=True)
        seed=call(path,initial_messages(),0,'initial',trial)
        history,previous,arms={},{},{}
        seed_result=None
        for arm in ARMS:
            path=folder/arm/'seed';path.mkdir(parents=True)
            result,text=evaluator.stage(seed,arm,path)
            if seed_result is None:seed_result=result
            elif seed_result!=result:raise ValueError('shared initial grading differs')
            history[arm]=initial_messages();append(history[arm],seed,text);previous[arm]=text
            arms[arm]={'seed':result,'rounds':[],'first_verified_round':0 if result['verified'] else None,'delivered':[]}
        save(folder/'initial'/'assessment.json',seed_result)
        for turn in range(1,rounds+1):
            offset=(t-1+turn-1)%len(ARMS)
            for arm in ARMS[offset:]+ARMS[:offset]:
                path=folder/arm/f'round-{turn:02d}';path.mkdir()
                arms[arm]['delivered'].append(packet_metrics(previous[arm]))
                output=call(path,history[arm],turn,arm,trial)
                result,text=evaluator.stage(output,arm,path)
                append(history[arm],output,text);previous[arm]=text
                arms[arm]['rounds'].append(result)
                if result['verified'] and arms[arm]['first_verified_round'] is None:arms[arm]['first_verified_round']=turn
        sessions[trial]={'initial':seed_result,'arms':arms}
    if len(ids)!=trials*(1+len(ARMS)*rounds):raise ValueError('incomplete run')
    result={'schema':1,'mode':mode,'task':TASK_ID,'trials':trials,'repair_rounds':rounds,'responses':len(ids),
            'provider_api_calls':len(ids) if mode=='live' else 0,'initial_usage':initial_usage,'provider_usage':usage,'sessions':sessions}
    if mode=='live':result.update(requested_model=provider_config['model'],model=next(iter(models)))
    save(out/'summary.json',result);return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--corpus',type=Path,default=ROOT/'results/milestone3/frame-faults');p.add_argument('--binary',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--trials',type=int,choices=range(1,6),default=1);p.add_argument('--rounds',type=int,choices=(1,2,3),default=2)
    m=p.add_mutually_exclusive_group(required=True);m.add_argument('--fixture',action='store_true');m.add_argument('--live',action='store_true')
    p.add_argument('--model');p.add_argument('--reasoning-effort',choices=('minimal','low','medium','high'));p.add_argument('--max-output-tokens',type=int,default=4096)
    a=p.parse_args()
    if a.live and (not a.model or not os.environ.get('OPENAI_API_KEY','').strip()):p.error('--live requires model and configured OPENAI_API_KEY')
    if not 16<=a.max_output_tokens<=4096:p.error('invalid token budget')
    config={'model':a.model,'reasoning_effort':a.reasoning_effort,'max_output_tokens':a.max_output_tokens,'transport':'OpenAI Responses API'} if a.live else None
    provider=partial(respond,model=a.model,reasoning_effort=a.reasoning_effort,max_output_tokens=a.max_output_tokens) if a.live else None
    print(f'{a.trials*(1+3*a.rounds)} planned responses (one unassisted generation per trial)',flush=True)
    r=run(corpus_dir=a.corpus,binary=a.binary,out=a.output,mode='live' if a.live else 'fixture',trials=a.trials,rounds=a.rounds,provider=provider,provider_config=config)
    print(f"{r['responses']} {r['mode']} responses, {r['provider_api_calls']} provider calls")

if __name__=='__main__':main()
