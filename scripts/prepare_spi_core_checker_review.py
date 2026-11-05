"""Lossless private-control packing and a byte gate before the one review call."""
import argparse
import copy
import json
from pathlib import Path
from prepare_i2c_compact_review import pack,unpack
from run_midterm_fixed import ROOT,sha

def delta(base,rows):
    if len(rows)>len(base):raise ValueError('Delta cannot append rows')
    changes=[]
    for i,(a,b) in enumerate(zip(base,rows)):
        if a['cycle']!=b['cycle']:raise ValueError('Changed cycle identity')
        d={k:{n:v for n,v in b[k].items() if a[k].get(n)!=v} for k in ('action','pre','post')}
        d={k:v for k,v in d.items() if v}
        if d:changes.append({'index':i,**d})
    return {'length':len(rows),'changes':changes}

def apply_delta(base,d):
    rows=copy.deepcopy(base[:d['length']])
    for x in d['changes']:
        for k in ('action','pre','post'):rows[x['index']][k].update(x.get(k,{}))
    return rows

def vector_pack(rows,columns):
    vectors=[[r[k][n] for k,n in columns] for r in rows];steps=[]
    for prev,cur in zip(vectors,vectors[1:]):
        d=[[i,v] for i,v in enumerate(cur) if prev[i]!=v]
        if steps and steps[-1][1]==d:steps[-1][0]+=1
        else:steps.append([1,d])
    result={'start_cycle':rows[0]['cycle'],'first':vectors[0],'steps':steps}
    if vector_unpack(result,columns)!=rows:raise ValueError('Vector trace roundtrip')
    return result

def vector_unpack(p,columns):
    v=list(p['first']);rows=[]
    def row(c):
        r={'cycle':c,'action':{},'pre':{},'post':{}}
        for (k,n),value in zip(columns,v):r[k][n]=value
        return r
    c=p['start_cycle'];rows.append(row(c))
    for repeat,changes in p['steps']:
        for _ in range(repeat):
            c+=1
            for i,x in changes:v[i]=x
            rows.append(row(c))
    return rows

def prepare(role,controls,evaluation,packet):
    if (role/'review-packet.json').exists():raise ValueError('Review packet already published')
    data=json.loads((controls/'inputs.json').read_text());spec=json.loads((packet/'packet.json').read_text())
    specs=json.loads((controls/'controls.json').read_text());bymeta={c['name']:c for c in specs}
    first=next(iter(data.values()))[0];columns=[(k,n) for k in ('action','pre','post') for n in first[k]]
    originals={n:vector_pack(rs,columns) for n,rs in data.items() if n.startswith(('reference/','calibration/'))};changes={}
    for name,rs in data.items():
        if name in originals:continue
        base=bymeta[name].get('baseline','calibration/partial_then_csid_switch')
        d=delta(data[base],rs)
        if apply_delta(vector_unpack(originals[base],columns),d)!=rs:raise ValueError('Lossless delta mismatch')
        changes[name]={'base':base,**d}
    summary=json.loads((evaluation/'summary.json').read_text());concise=copy.deepcopy(summary)
    # Keep exact counts and explicitly disclose that the reviewer sees only a
    # bounded sample of repetitive diagnostics; full ledger stays on disk.
    for r in concise['cases'].values():
        for key in ('failures','assumption_violations','unresolved','events'):
            v=r[key];r[key+'_total']=len(v);r[key]=v[:4]
    concise['event_integrity_error_total']=len(concise['event_integrity_errors']);concise['event_integrity_errors']=concise['event_integrity_errors'][:4]
    body={'role':'Fresh independent read-only checker reviewer; not the author or stimulus author.',
        'task':'Determine ready_for_offline_gate, findings, limitations. Review public specification, immutable checker, independent hand traces, mutations and actual public traces. Distinguish checker errors, invalid controls, unresolved assumptions and plausible DUT violations. Do not presume actual DUT traces correct. Check payload edge attribution, RX valid/ready packing, CS timing, complete clean event windows, truncated batches and reset. Independent reviewer agreement is not a formal proof. No edits, stimulus generation, target selection or B authorization.',
        'specification_and_interface':spec,
        'checker_source':(role/'candidate/checker.py').read_text(),
        'properties':json.loads((role/'candidate/properties.json').read_text()),
        'contract':(role/'candidate/contract.md').read_text(),
        'fixed_driver_source':(ROOT/'examples/spi_core_integration/verif/tb_spi_core.sv').read_text(),
        'evaluation':concise,'private_control_definitions':specs,
        'trace_columns':columns,'full_base_traces_lossless':originals,'derived_traces_lossless':changes,
        'trace_format':'Base traces: first is a vector indexed by trace_columns [section,field]; cycle=start_cycle. Each step is [repeat,changes] with changes=[[column_index,new_value],...]. Repeat: copy previous vector, increment cycle by1, apply changes. Reconstruct action/pre/post using trace_columns. Derived trace: take first length rows of named base, then update action/pre/post fields at each changes[index]. Every evaluated row reconstructs exactly; no windows replace full traces.',
        'review_limit':'All 28 input traces are available losslessly. For repetitive result diagnostics only first 4 per category/case and first 4 event-integrity errors are included with exact totals. Full evaluations remain local. No DUT implementation, e-graph feedback or B/C results are provided.',
        'integrity':{'checker_sha256':sha(role/'candidate/checker.py'),'controls_sha256':sha(controls/'inputs.json'),'evaluation_sha256':sha(evaluation/'evaluations.json')}}
    prefix='Read-only independent checker/driver audit. Do not modify artifacts. Return JSON with ready_for_offline_gate, findings, limitations. Check event false positives, independent controls, spec justification and isolation. No claim of formal proof.\n'
    size=len((prefix+json.dumps(body)).encode())
    if size>150000:
        with (role/'review-preparation-attempts.jsonl').open('a') as f:f.write(json.dumps({'prompt_bytes':size,'API_sent':False,'reason':'local size cap'})+'\n')
        raise ValueError('Review packet exceeds byte cap: '+str(size))
    preflight={'prompt_bytes':size,'size_cap_bytes':150000,'lossless_roundtrip':True,'case_count':len(data),'builder_sha256':sha(Path(__file__)),'checker_sha256':sha(role/'candidate/checker.py')}
    (role/'review-preflight.json').write_text(json.dumps(preflight,indent=2)+'\n')
    tmp=role/'review-packet.prepared';tmp.write_text(json.dumps(body,separators=(',',':'))+'\n');tmp.rename(role/'review-packet.json')
    print(json.dumps(preflight))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('role','controls','evaluation','packet'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();prepare(a.role.resolve(),a.controls.resolve(),a.evaluation.resolve(),a.packet.resolve())
