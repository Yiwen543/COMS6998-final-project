"""Frozen WBXBAR boundary: measurement/feedback only; Claude owns expected outputs."""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from coverage import summary
from inventory_natural_coverage import load_all
from preflight_spi_host import identity
from prepare_wbxbar_checker_role import verify_scope, SCOPE
from run_midterm_fixed import ROOT, sha
from run_spi_core_b_development import raw_page, diagnostics
from wbxbar_exploratory_driver import FIELDS, seed, action, validate, parse, compile_driver

BASE=ROOT/'results/wbxbar_exploratory_bc_20261104'
STATIC=ROOT/'results/wbxbar_conditional_20261104/screen-v2'
CANDIDATE=BASE/'claude-v3/candidate'
FREEZE=ROOT/'configs/wbxbar_exploratory_bc_freeze_v1.json'
INSTRUCTIONS=('Generate only JSON cycle actions for the fixed original WBXBAR. Change stimulus only. '
    'Maximize original DUT coverage within the stated cycle/token budget. Follow the public specification '
    'and fixed offer interface. Every cumulative batch is replayed from the common seed. There is no '
    'implicit drain. Checker failures and unresolved observations remain evidence. Return only the actions object.')
DRIVER_CONTRACT=('One action is one physical clock cycle. Fields are unsigned packed integers; master 0 '
    'uses the low slice. rst is synchronous active-high reset. offer bit m queues one request for master m; '
    'addr has two 8-bit addresses, data two 32-bit payloads, we two direction bits, sel two 4-bit byte masks. '
    'The driver holds queued STB/payload until pre-edge CYC & STB & !STALL acceptance and keeps CYC high '
    'while queued or accepted work remains. A sampled ERR discards remaining accepted work for that master, '
    'preserves unaccepted offers and inserts one counted low-CYC cycle. Reset discards both kinds of work; '
    'offer must be zero when rst=1. The slave environment never stalls; it returns ACK or ERR one cycle '
    'after acceptance, gated by downstream CYC. slave_error bit s selects ERR for slave s at that response '
    'cycle. Read data is 0xa55a0000 OR the accepted address. Idle actions are real counted cycles. Pending '
    'work survives across appended rounds through cumulative replay. No automatic tail drain is added.')


def schema(limit=64):
    return {'type':'object','additionalProperties':False,'required':['actions'], 'properties':{
        'actions':{'type':'array','minItems':1,'maxItems':limit,'items':{'type':'object',
        'additionalProperties':False,'required':list(FIELDS),'properties':{
            k:{'type':'integer','minimum':0,'maximum':(1<<w)-1} for k,w in FIELDS.items()}}}}}


def validate_generated(payload, limit=64):
    if not isinstance(payload,dict) or set(payload)!={'actions'} or not isinstance(payload['actions'],list):
        raise ValueError('Expected only actions array')
    actions=payload['actions']
    if not 1<=len(actions)<=limit:raise ValueError('New cycle limit')
    validate(seed()+actions)
    return actions


def verify_freeze(path=FREEZE):
    scope,_=verify_scope(); f=json.loads(path.read_text())
    if not f.get('offline_gate_pass'):raise ValueError('Offline gate not passed')
    for k in ('targets','development_budget','model_limits','arms','session_policy'):
        if f[k]!=scope[k]:raise ValueError('Registered setting changed: '+k)
    for p,h in f['hashes'].items():
        if sha(ROOT/p)!=h:raise ValueError('Frozen artifact changed: '+p)
    if not json.loads((BASE/'claude-v3/review.json').read_text())['ready_for_offline_gate']:
        raise ValueError('Independent review not ready')
    return f


def check_trace(trace,out):
    auth=json.loads((CANDIDATE/'authorship.json').read_text())
    for name,h in auth['artifact_sha256'].items():
        if sha(CANDIDATE/name)!=h:raise ValueError('Checker changed')
    inp=out/'checker-input.json';res=out/'checker-output.json'
    inp.write_text(json.dumps({'batch':trace},separators=(',',':'))+'\n')
    command=[sys.executable,'-I',str(ROOT/'scripts/evaluate_spi_checker_candidate.py'),
        '--worker','--candidate',str(CANDIDATE),'--inputs',str(inp),'--output',str(res)]
    env={k:v for k,v in os.environ.items() if not any(s in k for s in ('KEY','TOKEN','SECRET','PASSWORD'))}
    with tempfile.TemporaryDirectory(prefix='wbxbar-check-') as cwd:
        p=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True,timeout=60)
    (out/'checker-worker.log').write_text(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError('Checker process failed')
    d=json.loads(res.read_text())
    if d['errors'] or not all(t['pass'] for t in d['selftests']) or d['cases']['batch'].get('infrastructure_error'):
        raise RuntimeError('Checker infrastructure error')
    return d['cases']['batch']


def simulate(binary,actions,out,manifest,denominator):
    validate(actions);out.mkdir(parents=True,exist_ok=False)
    (out/'actions.json').write_text(json.dumps({'actions':actions},indent=2)+'\n')
    vec=out/'vectors.txt';vec.write_text(''.join(' '.join(format(a[k],'x') for k in FIELDS)+'\n' for a in actions))
    command=list(map(str,[binary,'+VECTORS='+str(vec),'+verilator+coverage+file+'+str(out/'coverage.dat')]))
    start=time.perf_counter()
    try:
        with (out/'simulation.log').open('w') as stream:
            p=subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=30)
        if p.returncode:raise RuntimeError('Simulation failed; partial evidence retained')
    finally:
        log=(out/'simulation.log').read_text()
        execution={'command':command,'simulation_seconds':time.perf_counter()-start,
            'requested_cycles':len(actions),'executed_cycles':sum(l.startswith('PRE ') for l in log.splitlines()),
            'driver_complete':'DRIVER_OK steps='+str(len(actions)) in log}
        (out/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    if not execution['driver_complete']:raise ValueError('Incomplete driver')
    trace,transport=parse(log,actions,manifest['inputs'],manifest['outputs'])
    (out/'trace.json').write_text(json.dumps(trace,separators=(',',':'))+'\n')
    points=load_all(out/'coverage.dat',manifest['sources'])
    (out/'raw-points.json').write_text(json.dumps(points,indent=2)+'\n')
    if len(points)!=len(denominator) or {identity(p) for p in points}!=denominator:
        raise ValueError('DUT denominator changed')
    # Coverage has already been flushed before checking. Violations never abort measurement.
    checked=check_trace(trace,out)
    result={'coverage':summary(points),'checker':checked,'transport':transport,
        'delivery_complete':transport['delivery_complete'],
        'verification_complete':transport['delivery_complete'] and checked['verdict']=='scoped_pass',
        **execution}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result,points,trace


def group_status(points,targets):
    counts={identity(p):p['hits'] for p in points}
    return [{'eclass':g['eclass'],'nontrivial':g['nontrivial'],
        'raw_source_hits':[counts[tuple(i)] for i in g['source_counter_identities']],
        'all_hit':all(counts[tuple(i)]>0 for i in g['source_counter_identities'])} for g in targets]


def semantic_relations(targets):
    screen=json.loads((STATIC/'screen/screen.json').read_text())
    extraction=json.loads((STATIC/'screen/extraction.json').read_text())
    egg=json.loads((STATIC/'screen/egg.json').read_text())
    extracted={t['id']:t for t in extraction['targets']};normal={t['id']:t for t in egg['targets']}
    groups={g['eclass']:g for g in screen['groups']};result=[]
    for target in targets:
        g=groups[target['eclass']];members=[];expressions=[]
        for m in g['members']:
            if m['mapping']['status']!='mapped' or list(identity(m['mapping']['point'])) not in target['source_counter_identities']:continue
            t=extracted[m['id']];n=normal[m['id']]
            if n['eclass']!=g['eclass']:raise ValueError('Eclass drift')
            members.append({'id':m['id'],'counter':list(identity(m['mapping']['point'])),
                'complete_guard':t['compact'],'source_predicate':t['source_text'],
                'instance_scopes':t.get('instance_scopes',[t['instance_scope']]),
                'original_event_context':t['original_event_context']})
            expressions.extend([t['compact'],n['representative']])
        atoms=sorted(set(re.findall(r'p_[a-f0-9]+',' '.join(expressions))))
        ids={m['id'] for m in members}
        result.append({'eclass':g['eclass'],'event_context':g['event_context'],'members':members,
            'representative':normal[members[0]['id']]['representative'],
            'typed_atoms':{a:extraction['atoms'][a] for a in atoms},
            'explanations':[e for e in egg['rewrite_explanations'] if e['left'] in ids and e['right'] in ids]})
    return result


def compact_relations(groups):
    """Lossless shared atom table and short aliases; no semantic selection."""
    groups=json.loads(json.dumps(groups));atoms={}
    for g in groups:
        for k,v in g.pop('typed_atoms').items():
            if k in atoms and atoms[k]!=v:raise ValueError('Atom identity collision')
            atoms[k]=v
    aliases={k:f'a{i}' for i,k in enumerate(sorted(atoms))}
    def rename(value):
        if isinstance(value,str):return re.sub(r'p_[a-f0-9]+',lambda m:aliases[m[0]],value)
        if isinstance(value,list):return [rename(v) for v in value]
        if isinstance(value,dict):return {k:rename(v) for k,v in value.items()}
        return value
    return {'groups':rename(groups),'typed_atoms':{aliases[k]:v for k,v in atoms.items()},
        'atom_ids':{v:k for k,v in aliases.items()}}


def repeated_actions(actions):
    rows=[]
    for action in actions:
        v=[action[k] for k in FIELDS]
        if rows and rows[-1][1]==v:rows[-1][0]+=1
        else:rows.append([1,v])
    return {'encoding':'[repeat_count, field_values]; expand in order, one physical cycle per repetition', 'rows':rows}


def trace_vectors(trace):
    if not trace:return {'columns':[],'rows':[]}
    columns=[(phase,k) for phase in ('pre','post') for k in trace[0][phase]]
    return {'columns':['cycle']+[phase+'.'+k for phase,k in columns],
        'rows':[[r['cycle']]+[r[phase][k] for phase,k in columns] for r in trace]}


def messages(config,arm,generated,prior,points,trace,round_no):
    if arm not in ('B','C'):raise ValueError('Unknown arm')
    scope=config; sources=[ROOT/scope['candidate']['root']/n for n in scope['candidate']['sources']]
    spec=json.loads((BASE/'spec-packet-v1/packet.json').read_text())
    lookup={identity(p):p for p in points}
    target_ids=sorted({tuple(i) for g in scope['targets'] for i in g['source_counter_identities']})
    common={'specification':{k:spec[k] for k in ('scope','authority','parameters','interface')},
        'driver_contract':DRIVER_CONTRACT,'field_widths':FIELDS,
        'rtl':config['rtl_prompt_view'],
        'cycle_field_order':list(FIELDS),'common_seed':[[a[k] for k in FIELDS] for a in seed()],
        'previous_generated_cycles':repeated_actions(generated),
        'round':round_no,'max_new_cycles':scope['development_budget']['max_new_cycles'],
        'total_rounds':scope['development_budget']['rounds'],'checker':diagnostics(prior['checker']),
        'transport':prior['transport'],'verification_complete':prior['verification_complete'],
        'execution_trace':trace_vectors(trace[-16:]),
        'raw_feedback':raw_page(points,sources,round_no,48),
        'registered_source_counters':[lookup[i] for i in target_ids],
        'counter_meaning':'Counts belong to separate original DUT source points. line/branch/expr are tool-defined execution/outcome counters, toggle counts directed signal bit changes; reset and initialization activity are included. Unsupported/unmapped counters remain in the denominator.'}
    if arm=='C':
        pending={g['eclass'] for g in group_status(points,scope['targets']) if not g['all_hit']}
        common['semantic_relations']={'scope':'Two-state combinational predicates only; no four-state or whole-transition proof. Typed atoms retain original types; four_state metadata is not a proof of X/Z equivalence. Clock/reset context is not normalized away. Equivalent predicates never merge source counters.',
            'state_lemma':'For N=0,1, (!grant[N][2] && mgrant[N]) implies unsigned(mindex[N]) <= 2; independently proved on the fixed original transition system without input assumptions. No other state invariant imported.',
            **compact_relations([g for g in config['semantic_relations'] if g['eclass'] in pending])}
    return [{'role':'system','content':INSTRUCTIONS},{'role':'user','content':json.dumps(common,separators=(',',':'))}]
