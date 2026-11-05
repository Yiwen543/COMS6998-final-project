"""Lossless shared-dictionary traces for the independent repair reviewer."""
import argparse
import copy
import json
import re
from pathlib import Path
from prepare_spi_core_checker_review import vector_pack, vector_unpack, delta, apply_delta
from run_midterm_fixed import ROOT, sha

PREFIX='Read-only independent checker/driver audit. Do not modify artifacts. Return JSON with ready_for_offline_gate, findings, limitations. Check event false positives, independent controls, spec justification and isolation. No claim of formal proof.\n'


def encode(data, meta):
    first=next(iter(data.values()))[0];columns=[(k,n) for k in ('action','pre','post') for n in first[k]]
    dictionary=[];indices={};bases={};derived={}
    for name,rows in data.items():
        parent=meta[name].get('baseline')
        if parent in data and len(rows)<=len(data[parent]):
            derived[name]={'base':parent,**delta(data[parent],rows)};continue
        p=vector_pack(rows,columns);steps=[]
        for repeat,d in p['steps']:
            key=json.dumps(d,separators=(',',':'))
            if key not in indices:indices[key]=len(dictionary);dictionary.append(d)
            steps.append([repeat,indices[key]])
        bases[name]={**p,'steps':steps}
    def restore(name):
        if name in bases:
            p=bases[name];return vector_unpack({**p,'steps':[[n,dictionary[i]] for n,i in p['steps']]},columns)
        p=derived[name];return apply_delta(restore(p['base']),p)
    for name,rows in data.items():
        if restore(name)!=rows:raise ValueError('Review trace reconstruction: '+name)
    return {'columns':columns,'change_dictionary':dictionary,'base_traces':bases,'derived_traces':derived}


def prepare(role, controls, evaluation, packet):
    if (role/'review-packet.json').exists():raise ValueError('Already published')
    data=json.loads((controls/'inputs.json').read_text());meta=json.loads((controls/'controls.json').read_text())
    omitted=[n for n in data if n.startswith('probe/write_speed') and n.endswith(('mode0','mode1'))]
    selected={n:r for n,r in data.items() if n not in omitted}
    trace=encode(selected,{m['name']:m for m in meta})
    spec=json.loads((packet/'packet.json').read_text())['specification_and_interface']
    # Identical public excerpt already occurs in the old and amendment packets.
    # Deduplicate only exact numbered text; no authority is dropped.
    seen=set();authorities=[]
    for a in spec['authority']:
        b=copy.deepcopy(a);b['excerpts']=[]
        for x in a['excerpts']:
            lines=[]
            for line in x['text'].splitlines():
                key=(a['sha256'],line)
                if key not in seen:lines.append(line);seen.add(key)
            if lines:b['excerpts'].append({**x,'text':'\n'.join(lines),'deduplication':'Previously provided identical numbered lines omitted only'})
        if b['excerpts']:authorities.append(b)
    links={}
    for a in authorities:
        for x in a['excerpts']:
            def link(m):
                links[m.group(1)]=m.group(2)
                return m.group(1)
            x['text']=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,x['text'])
            # Table alignment spacing has no normative meaning. Retain every
            # numbered text line and all table cells, not just a prose summary.
            x['text']='\n'.join(re.sub(r' {2,}',' ',l) if '|' in l else l for l in x['text'].splitlines())
    spec['authority']=authorities
    spec['review_formatting']='Only duplicate numbered lines, Markdown link destinations and table alignment spaces compressed. Numbered normative text retained; upstream file hashes/URLs locate originals. Full properties.json not included; complete executable checker and contract included.'
    results=json.loads((evaluation/'summary.json').read_text());brief=copy.deepcopy(results)
    for r in brief['cases'].values():
        for k in ('failures','assumption_violations','unresolved','events'):
            r[k+'_total']=len(r[k]);r[k]=r[k][:(1 if k=='failures' else 3)]
    brief.pop('hashes',None)
    brief.pop('controls',None)  # definitions below; all individual verdicts retained
    for r in brief['cases'].values():
        # Supplementary author's counters are redundant with full trace and result counts.
        # Keep their exact values in the local full evaluation ledger.
        r.pop('counts',None)
    body={'role':'Fresh independent read-only reviewer; never the author or stimulus role',
      'task':'Audit the amended byte-order authority and independent checker. Determine whether it is safe to freeze, not merely whether selftests pass. Check CPOL idle-level changes versus real selected serial edges, TX event omissions, full-cycle RX sampling, pending CSID, false positive recovery and unsupported modes. Do not presume DUT traces correct. Trace corruption is not a formal RTL mutant. Explain any flawed control. Do not rewrite source, select B/C targets, weaken properties, or authorize B yourself.',
      'specification_and_interface':spec,'checker_source':(role/'candidate/checker.py').read_text(),
      'properties_file_sha256':sha(role/'candidate/properties.json'),'contract':(role/'candidate/contract.md').read_text(),
      'driver_source':(ROOT/'examples/spi_core_integration/verif/tb_spi_core.sv').read_text(),
      'evaluation':json.dumps(brief,separators=(',',':')),'control_definitions':meta,'lossless_traces':json.dumps(trace,separators=(',',':')),
      'trace_format':'evaluation and lossless_traces are compact JSON strings, parse once. columns are [section,field]. Base first is the complete vector at start_cycle. Base steps are [repeat,change_dictionary_index]; for each repeat increment cycle by1, copy prior vector, then apply all [column_index,new_value] pairs from the dictionary entry. Derived traces take first length rows of recursively restored base, then update action/pre/post fields at each changes[index]. EVERY INCLUDED input row is present losslessly. Results retain first1 failure and first3 other diagnostics per case, with exact totals; supplementary author counters and duplicated control accounting omitted, full ledger remains local.',
      'review_trace_limit':{'evaluated_cases':len(data),'included_complete_traces':len(selected),'omitted_complete_traces':omitted,
        'reason':'Local byte cap. Omit only six supplemental CPOL0 TX traces with no reported failures; their evaluations and definitions remain. All failing supplemental probes, all hand references and all recovery/negative controls retain full traces. This is not an exhaustive trace review of all47 cases.'},
      'history_correction':'Prior reviewer alleged underflow/clock toggles in the clean TX calibration. Raw evidence did not support that claim: only old byte-order errors, no changes while pre-stalled. Re-check this version without inheriting that conjecture. Event omission is independently observed.',
      'independence':'No DUT implementation or upstream scoreboard, no B/C outcomes; private controls are shown only to reviewer after author completion. New contract is a documented project interpretation of conflicting pinned upstream text plus boundary mapping, not an upstream maintainer erratum.',
      'integrity':{'candidate_sha256':sha(role/'candidate/checker.py'),'controls_sha256':sha(controls/'inputs.json'),'evaluation_sha256':sha(evaluation/'evaluations.json')}}
    size=len((PREFIX+json.dumps(body)).encode())
    preflight={'prompt_bytes':size,'size_cap_bytes':150000,'lossless_roundtrip':True,'case_count':len(data),'included_trace_count':len(selected),'omitted_traces':omitted,'builder_sha256':sha(Path(__file__)),
               'component_bytes':{k:len(json.dumps(v).encode()) for k,v in body.items()}}
    with (role/'review-preparation-attempts.jsonl').open('a') as f:
        f.write(json.dumps({**preflight,'API_sent':False})+'\n')
    (role/'review-preflight.json').write_text(json.dumps(preflight,indent=2)+'\n')
    if size>150000:raise ValueError('Review cap: '+str(size))
    p=role/'review-packet.prepared';p.write_text(json.dumps(body,separators=(',',':'))+'\n');p.rename(role/'review-packet.json')
    print(json.dumps(preflight))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('role','controls','evaluation','packet'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();prepare(a.role.resolve(),a.controls.resolve(),a.evaluation.resolve(),a.packet.resolve())
