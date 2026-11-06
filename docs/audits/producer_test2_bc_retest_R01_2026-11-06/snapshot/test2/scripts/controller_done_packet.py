"""Explicit public-only packets for the new trace_done study."""
import copy
import json
from common import ROOT,dump,sha
from controller_done_data import TASK,SOURCE_TASK,REG,SOURCES
from controller_packet import identity,pack_coverage,unpack_coverage,semantic_feedback
from controller_packet_compact import pack,unpack
from controller_monitor_live import ROW_INPUTS,OUTPUTS

NAMES=('frame_lengths','independent_channels','reset_and_drain')


def pack_rows(rows):
    runs=[]
    for row in rows:
        values=[row['inputs'][k] for k in ROW_INPUTS]+[row[p][k] for p in ('pre','post') for k in OUTPUTS]
        if runs and runs[-1][1]==values:runs[-1][0]+=1
        else:runs.append([1,values])
    return dict(encoding='consecutive_observation_runs_v1',columns=['input_'+k for k in ROW_INPUTS]+[p+'_'+k for p in ('pre','post') for k in OUTPUTS],
                cycles=len(rows),runs=runs,decode='Runs are[count,values]. Expand exactly count consecutive cycles per run, cycle numbering starts0. No observation/clock edge removed. trace_done is0for allpre/postexcept finalpost1.')


def unpack_rows(data):
    rows=[]
    for count,values in data['runs']:
        for _ in range(count):
            rows.append(dict(cycle=len(rows),inputs=dict(zip(ROW_INPUTS,values[:6])),pre=dict(zip(OUTPUTS,values[6:15])),post=dict(zip(OUTPUTS,values[15:]))))
    if len(rows)!=data['cycles']:raise ValueError('Observation run count mismatch')
    return rows


def packet(arm):
    if arm not in ('B2_raw','C2_semantic'):raise ValueError('Unknown arm')
    # Allowlist is fixed here: no directory recursion or private/reference reads.
    public=TASK/'public';development={};pointsets=[];allowlist=[]
    for name in NAMES:
        directory=TASK/'measurements-v1/correct/verilator'/name
        rp=directory/'rows.json';cp=directory/'raw-points.json';rows=json.loads(rp.read_text());points=json.loads(cp.read_text())
        encoded=pack_rows(rows)
        if unpack_rows(encoded)!=rows:raise ValueError('Observation information lost')
        development[name]=dict(observations=encoded,require_drained=True,min_tail=32,trace_done='finalpostonly')
        pointsets.append(points);allowlist.extend([rp,cp])
    raw=pack_coverage(pointsets)
    for i,points in enumerate(pointsets):
        if {identity(p):p['hits'] for p in points}!={identity(p):p['hits'] for p in unpack_coverage(raw,i)}:raise ValueError('Source counter changed')
    compact=pack(raw)
    if unpack(compact)!=raw:raise ValueError('Coverage dictionary changed a field')
    data=dict(specification=(public/'specification.md').read_text(),observer_contract=(public/'observer_contract.md').read_text(),
              rtl={str(p.relative_to(SOURCE_TASK/'public')):p.read_text() for p in SOURCES},development=development,
              coverage_trace_order=list(NAMES),raw_coverage=compact)
    if arm=='C2_semantic':data['egraph_feedback']=semantic_feedback()
    return data


def prepare():
    out=TASK/'public/prompt-packets-v1';out.mkdir(parents=True,exist_ok=False)
    b,c=packet('B2_raw'),packet('C2_semantic');common=copy.deepcopy(c);common.pop('egraph_feedback')
    if b!=common:raise ValueError('Common information differs')
    for arm,data in [('B2_raw',b),('C2_semantic',c)]:dump(out/(arm+'.json'),data)
    allow=[TASK/'public/specification.md',TASK/'public/observer_contract.md']+SOURCES
    for name in NAMES:allow.extend([TASK/'measurements-v1/correct/verilator'/name/n for n in ('rows.json','raw-points.json')])
    # Semantic package reads only public-source certificates, never final data.
    allow.extend([SOURCE_TASK/'qualification/typed-v5/screen'/n for n in ('screen.json','extraction.json')])
    dump(out/'audit.json',dict(status='passed',B_C_common_equal=True,raw_counter_count=unpack(b['raw_coverage'])['counter_count'],
         observation_cycles=sum(b['development'][n]['observations']['cycles'] for n in NAMES),C_groups=len(c['egraph_feedback']['groups']),
         explicit_input_files={str(p.relative_to(ROOT)):sha(p) for p in allow},packets={a:sha(out/(a+'.json')) for a in ('B2_raw','C2_semantic')},
         actual_provider_token_count='PENDING_AUTHORIZATION_NO_ESTIMATE_CLAIM',API_calls=0,source_sha256=sha(__file__)))
    return out
