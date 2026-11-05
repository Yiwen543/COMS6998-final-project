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
    trace=encode(data,{m['name']:m for m in meta})
    for base in trace['base_traces'].values():
        original=base['steps']
        compact=[idx if repeat==1 else [repeat,idx] for repeat,idx in original]
        if [[1,x] if isinstance(x,int) else x for x in compact]!=original:raise ValueError('Single-step encoding roundtrip')
        base['steps']=compact
    source=json.loads((packet/'packet.json').read_text())['specification_and_interface']
    spec={k:source[k] for k in ('scope','interface','requested_events','registered_contract_amendment')}
    doc=ROOT/'third_party/opentitan_candidate/hw/ip/spi_host/doc/theory_of_operation.md'
    # Selected normative sections, including all relevant timing/reset/order text.
    # Other quoted registration/programmer material is retained in the hashed
    # source packet and cited by the amendment, not repeated in this review.
    a=excerpt(doc,[(13,54),(124,145),(194,279),(281,320),(363,377),(395,419),(478,483),(579,585),(629,644),(654,675),(685,702),(729,740)])
    if a['sha256']!=source['authority'][0]['sha256']:raise ValueError('Pinned public specification drift')
    for x in a['excerpts']:
        x['text']=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:m.group(1),x['text'])
        x['text']='\n'.join(re.sub(r' {2,}',' ',l) if '|' in l else l for l in x['text'].splitlines())
    spec['numbered_public_spec_excerpts']=a
    spec['review_scope']='These numbered public sections plus the registered contract/interface define this review. Prior author packet retained separately with complete provenance; register/programmer duplicate descriptions omitted here. Superseded internal ordering paragraphs still visible and explicitly superseded by registered amendment. Markdown link syntax/table alignment compressed only.'
    case_columns=['name','verdict','failures','assumption_violations','unresolved','events','infrastructure_error']
    cases=[[name,*[r.get(k) for k in case_columns[1:]]] for name,r in result['cases'].items()]
    control_columns=['name','kind','baseline','expected','required_event_family','authority','changes']
    control_rows=[[r.get(k) for k in control_columns] for r in meta]
    brief={'case_columns':case_columns,'cases':cases,'control_columns':control_columns,'controls':control_rows,
        'selftests':result['selftests'],'control_counts':result['control_counts'],'worker_errors':result['worker_errors'],
        'event_integrity_errors':result['event_integrity_errors'],
        'successful_events_on_unresolved_cases':result['successful_events_on_unresolved_cases']}
    body={'role':'Fresh independent read-only checker reviewer. No changes, no stimulus generation, no B/C target selection.',
      'task':'Audit CPOL idle-level handling, byte/bit counts, the complete/truncated/dirty TX starvation events, CSID pending offers, RX backpressure, reset and source-derived byte order. Determine ready_for_offline_gate, findings and limitations. Do not presume observed DUT traces correct or selftests sufficient. Check whether declared support is actually validated. Do not authorize B yourself. Report every remaining blocker. This is finite offline validation, not formal proof.',
      'specification_and_interface':spec,'checker_source':(role/'candidate/checker.py').read_text(),'contract':(role/'candidate/contract.md').read_text(),
      'properties_sha256':sha(role/'candidate/properties.json'),'driver_source':(ROOT/'examples/spi_core_integration/verif/tb_spi_core.sv').read_text(),
      'evaluation_json':json.dumps(brief,separators=(',',':')),'traces_json':json.dumps(trace,separators=(',',':')),
      'encoding':'Parse evaluation_json and traces_json once. Evaluation cases/control rows are arrays with named columns. ALL failure/assumption/unresolved/event records are included (no diagnostic truncation); redundant author counts and repetitive accounting metadata stay local. Every input trace is included losslessly. Trace columns are [section,field]. Base first is the vector at start_cycle. Each base step is EITHER an integer change_dictionary_index (repeat=1) OR [repeat,change_dictionary_index]; each repetition increments cycle by1, copies the prior vector, then applies the referenced [column_index,value] changes. Derived: recursively restore base, keep first length rows, apply each changes[index] action/pre/post update. All rows independently roundtrip-tested.',
      'context_corrections':[
        'Prior CPOL1 false positives and missing TX events were independently reproduced. This repair must fix them without skipping meaningful payload/phase checks.',
        'Actual calibration/partial_then_csid_switch is included: new CSID is valid before old CS releases and before new acceptance. A prior reviewer overlooked this real trace; do not repeat that unsupported absence claim.',
        'A prior one-row clock fault also reports underflow in the full ledger; it remains a glitch control, not proof for every timing-clean stall fault.',
        'Old probe/read_asymmetric_full0 used FULLCYC1 launch schedule and is intentionally retained as sampling-ambiguous. Corrected probe/read_full0_aligned is resimulated from its own clock schedule. Treat conservative unresolved separately from false alarms.',
        'Software-reset event pass_unresolved is deliberately excluded from pass counts. Hardware-reset event is a separate supported control.'
      ],
      'integrity':{'checker_sha256':sha(role/'candidate/checker.py'),'controls_sha256':sha(controls/'inputs.json'),
                   'evaluations_sha256':sha(evaluation/'evaluations.json'),'author_packet_sha256':sha(packet/'packet.json')},
      'isolation':'No DUT implementation, upstream scoreboard, guard/group/coverage results or B/C outcomes. Reviewer only sees private controls after the author completes. Neither model may edit measurement, driver or trusted source.'}
    n=len((PREFIX+json.dumps(body)).encode())
    preflight={'prompt_bytes':n,'size_cap_bytes':150000,'all_traces_included':True,'all_diagnostics_included':True,'case_count':len(data),
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
