"""Complete control traces/results in a bounded independent timing review."""
import argparse
import json
import re
from pathlib import Path
from prepare_spi_core_repair_review import encode, PREFIX
from prepare_spi_checker_role import excerpt
from run_midterm_fixed import ROOT,sha


def prepare(role,controls,evaluation,packet):
    if (role/'review-packet.json').exists():raise ValueError('Review already published')
    data=json.loads((controls/'inputs.json').read_text());meta=json.loads((controls/'controls.json').read_text())
    result=json.loads((evaluation/'summary.json').read_text())
    # Retain all new event/config controls and independent mode witnesses. The
    # redundant ordinary probes were fully reviewed in v3; keep their complete
    # verdicts here and disclose every omitted raw trace, never hide a failure.
    redundant={n for n in data if n.startswith('probe/write_speed') or n in {
        'reference/write1','reference/read1','reference/write2','reference/read2','reference/write4','reference/read4'}}
    referenced={m['baseline'] for m in meta if 'baseline' in m}
    omitted=sorted(n for n in redundant-referenced if result['cases'][n]['verdict']=='pass' and not result['cases'][n]['events'])
    selected={n:rs for n,rs in data.items() if n not in omitted}
    trace=encode(selected,{m['name']:m for m in meta})
    for base in trace['base_traces'].values():
        original=base['steps']
        compact=[idx if repeat==1 else [repeat,idx] for repeat,idx in original]
        if [[1,x] if isinstance(x,int) else x for x in compact]!=original:raise ValueError('Single-step encoding roundtrip')
        base['steps']=compact
    column_index={tuple(c):i for i,c in enumerate(trace['columns'])}
    for derived in trace['derived_traces'].values():
        original=derived['changes'];compact=[];restored=[]
        for row in original:
            changes=[[column_index[(section,field)],value] for section in ('action','pre','post') for field,value in row.get(section,{}).items()]
            compact.append([row['index'],changes]);back={'index':row['index']}
            for index,value in changes:
                section,field=trace['columns'][index];back.setdefault(section,{})[field]=value
            restored.append(back)
        if restored!=original:raise ValueError('Column delta roundtrip')
        derived['changes']=compact
    source=json.loads((packet/'packet.json').read_text())['specification_and_interface']
    spec={k:source[k] for k in ('scope','interface','requested_events','registered_contract_amendment')}
    doc=ROOT/'third_party/opentitan_candidate/hw/ip/spi_host/doc/theory_of_operation.md'
    # Selected normative sections, including all relevant timing/reset/order text.
    # Other quoted registration/programmer material is retained in the hashed
    # source packet and cited by the amendment, not repeated in this review.
    a=excerpt(doc,[(24,42),(194,279),(281,320),(363,377),(395,419),(478,483),(579,585),(629,644),(654,675)])
    if a['sha256']!=source['authority'][0]['sha256']:raise ValueError('Pinned public specification drift')
    for x in a['excerpts']:
        x['text']=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:m.group(1),x['text'])
        x['text']='\n'.join(re.sub(r' {2,}',' ',l) if '|' in l else l for l in x['text'].splitlines())
    spec['numbered_public_spec_excerpts']=a
    spec['review_scope']='These selected numbered public sections plus the registered contract/interface define this review. Prior author packet retains complete provenance, introductory material, register/programmer duplicates and the superseded internal MSB paragraphs; those are not repeated here. This review sees the registered order correction and normative timing/flow-control text. Markdown link syntax/table alignment compressed only.'
    case_columns=['name','verdict','failures','assumption_violations','unresolved','events','infrastructure_error']
    cases=[[name,*[r.get(k) for k in case_columns[1:]]] for name,r in result['cases'].items()]
    control_columns=['name','kind','baseline','expected','required_event_family','forbidden_event_family','forbidden_success_event_family','authority','changes']
    control_rows=[[r.get(k) for k in control_columns] for r in meta]
    brief={'case_columns':case_columns,'cases':cases,'control_columns':control_columns,'controls':control_rows,
        'selftests':result['selftests'],'control_counts':result['control_counts'],'worker_errors':result['worker_errors'],
        'event_integrity_errors':result['event_integrity_errors'],
        'successful_events_on_unresolved_cases':result['successful_events_on_unresolved_cases']}
    # Intern repeated diagnostic/control strings, preserving all records.
    # This is readable dictionary coding, not opaque binary compression.
    strings=[];string_ids={}
    def intern(s):
        if s not in string_ids:string_ids[s]=len(strings);strings.append(s)
        return {'$text':string_ids[s]}
    def walk(x):
        if isinstance(x,str) and len(x)>60:return intern(x)
        if isinstance(x,list):return [walk(v) for v in x]
        if isinstance(x,dict):return {k:walk(v) for k,v in x.items()}
        return x
    original_brief=brief;brief=walk(brief)
    def restore(x):
        if isinstance(x,dict) and set(x)=={'$text'}:return strings[x['$text']]
        if isinstance(x,list):return [restore(v) for v in x]
        if isinstance(x,dict):return {k:restore(v) for k,v in x.items()}
        return x
    if restore(brief)!=original_brief:raise ValueError('Result string roundtrip')
    brief['text_dictionary']=strings
    body={'role':'Fresh independent read-only checker reviewer. No changes, no stimulus generation, no B/C target selection.',
      'task':'Audit CPOL idle handling, byte/bit counts, complete/truncated/dirty and NO-STALL event controls, CSID/config changes, RX backpressure and source-derived byte order. Determine ready_for_offline_gate for a LIMITED supported event checker: stable sampling, data segments, and hardware reset only. Dummy segments and software-reset completion remain explicitly unresolved, not passes; do not certify the whole IP. Preserve known DUT/spec conflicts, do not turn true violations into checker false alarms. Require no false recovery from flags alone or benign refill/drain delays. Check whether support claims are validated. Do not authorize B, edit source or treat finite controls as formal proof.',
      'specification_and_interface':spec,'checker_source':(role/'candidate/checker.py').read_text(),'contract':(role/'candidate/contract.md').read_text(),
      'properties_sha256':sha(role/'candidate/properties.json'),'driver_source':(ROOT/'examples/spi_core_integration/verif/tb_spi_core.sv').read_text(),
      'input_schema_validator_source':(ROOT/'scripts/spi_core_interface.py').read_text(),
      'evaluation_json':json.dumps(brief,separators=(',',':')),'traces_json':json.dumps(trace,separators=(',',':')),
      'encoding':'Parse evaluation_json and traces_json once. Evaluation {$text:N} means text_dictionary[N]; substitute recursively. Cases/control rows use named columns. ALL diagnostics included. Redundant counters/accounting metadata stay local. Every INCLUDED trace lossless. Trace columns=[section,field]. Base first=vector at start_cycle; step is integer dictionary-index (repeat1) OR [repeat,index]. For each repeat, increment cycle, copy prior vector, apply change_dictionary[index] pairs [column_index,value]. Derived: restore base, keep first length rows, apply changes [row_index,[[column_index,value],...]]. All layers and included rows roundtrip-tested.',
      'trace_review_limit':{'evaluated_cases':len(data),'complete_traces_included':len(selected),'omitted_complete_traces':omitted,
        'reason':'Local byte cap. Only redundant passing ordinary probes/references omitted; their complete diagnostics remain. All new vacuity/prefix/config controls, faults and baseline dependencies included. Independent hand-mode matrix still included. Omitted raw traces existed in full in the archived v3 review; this reviewer must not claim to have inspected them.'},
      'context_corrections':[
        'Prior CPOL1 false positives and missing TX events were independently reproduced. This repair must fix them without skipping meaningful payload/phase checks.',
        'Actual calibration/partial_then_csid_switch is included: new CSID is valid before old CS releases and before new acceptance. A prior reviewer overlooked this real trace; do not repeat that unsupported absence claim.',
        'A prior one-row clock fault also reports underflow in the full ledger; it remains a glitch control, not proof for every timing-clean stall fault.',
        'Old probe/read_asymmetric_full0 used FULLCYC1 launch schedule and is intentionally retained as sampling-ambiguous. Corrected probe/read_full0_aligned is resimulated from its own clock schedule. Treat conservative unresolved separately from false alarms.',
        'Software-reset event pass_unresolved is deliberately excluded from pass counts. Hardware-reset event is a separate supported control.'
        ,'The Python validator runs before vector files/simulation, rejects out-of-width/illegal integers, and all merged control actions pass it. SV part-selects do not imply experimental LLM input can bypass validation; never recommend silently masking bad inputs.'
        ,'boundary/same_csid_config_change has legal input and no all-CS-high gap on the unchanged DUT. Pinned public theory241-249 requires the gap. Keep its checker failure as a spec/implementation conflict, not a waived property. No production bug conclusion is asserted without upstream confirmation.'
      ],
      'integrity':{'checker_sha256':sha(role/'candidate/checker.py'),'controls_sha256':sha(controls/'inputs.json'),
                   'evaluations_sha256':sha(evaluation/'evaluations.json'),'author_packet_sha256':sha(packet/'packet.json')},
      'isolation':'No DUT implementation, upstream scoreboard, guard/group/coverage results or B/C outcomes. Reviewer only sees private controls after the author completes. Neither model may edit measurement, driver or trusted source.'}
    if (controls/'prefix-audit.json').exists():
        body['prefix_expectation_change_audit']=json.loads((controls/'prefix-audit.json').read_text())
        body['prefix_audit_task']='Independently judge this control correction; do not assume it is justified just because revised expectations pass. Original85-case evaluation reported3 missing events at cutoffs where elapsed integer clocks equal the nominal half-period. New controls retain those exact traces but only forbid false success there; additional prefixes one cycle later require a pending/failed episode after strictly witnessed overdue SCK. Original expectations and3 failures remain archived. No model stimulus budget, DUT or checker changed. Reject the gate if this is weakening a justified obligation rather than resolving flag-only evidence ambiguity.'
    n=len((PREFIX+json.dumps(body)).encode())
    preflight={'prompt_bytes':n,'size_cap_bytes':150000,'all_traces_included':not omitted,'included_trace_count':len(selected),'omitted_traces':omitted,'all_diagnostics_included':True,'case_count':len(data),
        'lossless_roundtrip':True,'builder_sha256':sha(Path(__file__)),'component_bytes':{k:len(json.dumps(v).encode()) for k,v in body.items()}}
    with (role/'review-preparation-attempts.jsonl').open('a') as f:f.write(json.dumps({**preflight,'API_sent':False})+'\n')
    (role/'review-preflight.json').write_text(json.dumps(preflight,indent=2)+'\n')
    if n>150000:raise ValueError('Local byte cap: '+str(n))
    tmp=role/'review-packet.prepared';tmp.write_text(json.dumps(body,separators=(',',':'))+'\n');tmp.rename(role/'review-packet.json')
    print(json.dumps(preflight))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('role','controls','evaluation','packet'):p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args();prepare(a.role.resolve(),a.controls.resolve(),a.evaluation.resolve(),a.packet.resolve())
