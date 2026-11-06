"""Lossless public column encoding; preserves every observation and coverage field."""
import copy
import json
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG
from controller_done_packet import unpack_rows,pack_rows


def compact(value):return json.dumps(value,separators=(',',':'),sort_keys=True)


def encode_column(values):
    runs=[]
    for v in values:
        if runs and runs[-1][1]==v:runs[-1][0]+=1
        else:runs.append([1,v])
    # Deterministic shortest JSON representation, independent of B/C outcomes.
    return min([['raw',values],['rle',runs]],key=lambda v:len(compact(v)))


def decode_column(encoded):
    kind,values=encoded
    if kind=='raw':return copy.deepcopy(values)
    if kind=='rle':return [copy.deepcopy(v) for n,v in values for _ in range(n)]
    raise ValueError('Unknown column encoding')


def columns(rows):
    if not rows:return dict(count=0,columns=[])
    if any(len(r)!=len(rows[0]) for r in rows):raise ValueError('Ragged rows')
    return dict(count=len(rows),columns=[encode_column(list(v)) for v in zip(*rows)])


def expand(data):
    if data['count']==0:return []
    cols=[decode_column(v) for v in data['columns']]
    if any(len(v)!=data['count'] for v in cols):raise ValueError('Column count mismatch')
    return [list(v) for v in zip(*cols)]


def coverage(data):
    d=copy.deepcopy(data);ordinary=d.pop('ordinary');toggles=d.pop('toggle')
    # Column compression also handles nested bit descriptions and hit-vector IDs.
    return dict(encoding='coverage_columns_v2',dictionary=d,ordinary=columns(ordinary),toggle=columns([v[0]+v[1:2]+v[2] for v in toggles]),
                decode='Restore dictionary first. Expand ordinary columns into rows. Each toggle row has6sitefields,bitdescription,3hitvectorIDs; restore [site,bitdescription,IDs]. raw=[raw,values]; rle=[rle,[[repeat,value],...]]. All ordering and fields are retained.')


def restore_coverage(data):
    d=copy.deepcopy(data['dictionary']);d['ordinary']=expand(data['ordinary']);d['toggle']=[]
    for row in expand(data['toggle']):d['toggle'].append([row[:6],row[6],row[7:]])
    return d


def observations(data):
    rows=unpack_rows(data);matrix=[]
    # Exactly the same public column order as the v1 observation codec.
    for row in rows:
        matrix.append([row['inputs'][n.removeprefix('input_')] if n.startswith('input_') else row[n.split('_',1)[0]][n.split('_',1)[1]] for n in data['columns']])
    return dict(encoding='observation_columns_v2',columns=data['columns'],values=columns(matrix),
                decode='Expand raw/RLE columns to consecutive observations,cycle starts0; first6inputs,next9pre,last9post. All cycles preserved,trace_done only finalpost1,no extraedge.')


def restore_observations(data):
    matrix=expand(data['values']);runs=[]
    for row in matrix:
        if runs and runs[-1][1]==row:runs[-1][0]+=1
        else:runs.append([1,row])
    # Preserve the original v1 codec metadata byte-for-byte as well.
    template=pack_rows([]);template.update(columns=data['columns'],runs=runs,cycles=len(matrix));return template


def restore(packet):
    d=copy.deepcopy(packet);d['raw_coverage']=restore_coverage(d['raw_coverage'])
    for trace in d['development'].values():trace['observations']=restore_observations(trace['observations'])
    return d


def prepare():
    origin=TASK/'public/prompt-packets-v1';out=TASK/'public/prompt-packets-v2';out.mkdir(exist_ok=False);audit={};packets={}
    for arm in ('B2_raw','C2_semantic'):
        old=json.loads((origin/(arm+'.json')).read_text());new=copy.deepcopy(old);new['raw_coverage']=coverage(old['raw_coverage'])
        for trace in new['development'].values():trace['observations']=observations(trace['observations'])
        if restore(new)!=old:raise ValueError('Public information lost')
        dump(out/(arm+'.json'),new);packets[arm]=new;audit[arm]=dict(full_roundtrip=True,old_bytes=len(compact(old).encode()),new_bytes=len(compact(new).encode()),sha256=sha(out/(arm+'.json')))
    common=copy.deepcopy(packets['C2_semantic']);common.pop('egraph_feedback')
    if common!=packets['B2_raw']:raise ValueError('Shared B/C package differs')
    dump(out/'audit.json',dict(status='passed',B_C_common_equal=True,raw_counter_count=3168,observation_cycles=230,C_groups=4,
         packets={a:v['sha256'] for a,v in audit.items()},arms=audit,source_sha256=sha(__file__),parent_audit_sha256=sha(origin/'audit.json'),actual_provider_token_count='PENDING_NEW_AUTHORIZATION',API_calls=0,
         policy='No DUT/spec/oracle/guard/semantic group/counter/row/seed/budget/target change. Shorter common lossless representation only; failed v1 counts retained.'))
    return out


if __name__=='__main__':print(prepare())
