"""Blinded read-only attribution of earliest live failures, not checker repair."""
import argparse
import json
import os
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from wbxbar_experiment import verify_freeze,BASE,CANDIDATE,DRIVER_CONTRACT,check_trace
from wbxbar_exploratory_driver import simulate as replay_driver,comparable
from review_spi_core_safe_driver import pack_vectors
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE

INSTRUCTIONS='''Independently diagnose anonymized WBXBAR verification failures. READ ONLY: no tools,
patches, stimulus generation or coverage targeting. The checker was authored by a separate Claude role;
do not assume it correct. Public specification is normative; DUT RTL is diagnostic evidence only.
Use actual pre-edge acceptance, payload/SEL and response ordering, reset/error epochs and buffered work
to distinguish DUT discrepancy, checker false positive, illegal driver input, measurement error and
unresolved specification. Do not force pass or retroactively change a frozen experimental verdict.
For each case identify the earliest causal discrepancy, exact cycle and source/function basis, then
separate cascaded/repeated diagnostics from distinct root-cause hypotheses. Tests reproducing on two
simulators show reproducibility, not specification correctness. Scope exclusions stay explicit.
Return ONLY JSON: {case_findings:[{case_id,classification,confidence,earliest_causal_cycle,evidence,
specification_basis,checker_source_basis,rtl_source_basis,root_cause_hypotheses,cascaded_diagnostics,
unresolved}],distinct_root_cause_summary:[],additional_discriminating_controls:[],limitations:[]}.
No performance-arm labels, semantic groups, source coverage counts, token costs or rankings are provided.
'''


def prepare(run,out):
    c=verify_freeze(run/'freeze.json')
    if not json.loads((run/'audit.json').read_text())['pass']:raise ValueError('Live evidence audit missing')
    rows=json.loads((run/'summary.json').read_text())['rows']
    chosen=[]
    # Earliest observed failing batch in each arm; no coverage-based choice.
    for arm in sorted(c['arms']):
        r=next((r for r in rows if r['arm']==arm and r['measurement_fresh'] and r['checker']['failures']),None)
        if r:chosen.append(run/f"rep{r['repetition']}-{arm}"/f"round{r['round']}")
    if not chosen:raise ValueError('No live checker failure to attribute')
    out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((run/'shared/manifest.json').read_text())
    cases={};evaluations={};private={};hashes={};replays=[]
    # Reverse alphabetical arm order only to avoid a conventional label ordering.
    for index,path in enumerate(reversed(chosen)):
        alias=f'case_{index+1}'
        actions=json.loads((path/'actions.json').read_text())['actions']
        trace=json.loads((path/'trace.json').read_text())
        other,transport=replay_driver(run/'shared/iverilog/tb.vvp','iverilog',actions,out/alias,manifest)
        if comparable(trace,manifest['outputs'])!=comparable(other,manifest['outputs']):raise ValueError('Diagnostic simulator discrepancy')
        checked=check_trace(other,out/alias)
        original=json.loads((path/'result.json').read_text())
        if checked!=original['checker']:raise ValueError('Checker differs on Icarus replay')
        cases[alias]=trace;evaluations[alias]=original['checker'];private[alias]=str(path.relative_to(ROOT))
        for name in ['actions.json','trace.json','result.json']:hashes[str((path/name).relative_to(ROOT))]=sha(path/name)
        ex=json.loads((out/alias/'execution.json').read_text());replays.append({'case':alias,**ex})
    controls=json.loads((BASE/'controls-v7/private-inputs.json').read_text())
    cases['control_read']=controls['positive/read'];cases['control_masked_write']=controls['positive/masked_write_bytes']
    evals=json.loads((BASE/'evaluation-v8/summary.json').read_text())['cases']
    evaluations['control_read']=evals['positive/read'];evaluations['control_masked_write']=evals['positive/masked_write_bytes']
    first=next(iter(cases.values()))[0];columns=[(phase,k) for phase in ['pre','post'] for k in first[phase]]
    vectors={name:[[r[phase][k] for phase,k in columns] for r in trace] for name,trace in cases.items()}
    sources=[CANDIDATE/'checker.py',CANDIDATE/'contract.md',CANDIDATE/'properties.json',run/'shared/tb_natural_inventory.sv']
    body={'role':'fresh independent diagnostic reviewer','specification':json.loads((BASE/'spec-packet-v1/packet.json').read_text()),
        'driver_contract':DRIVER_CONTRACT,'sources':{p.name:p.read_text() for p in sources},
        'DUT':c['rtl_prompt_view'],'trace_columns':[phase+'.'+k for phase,k in columns],
        'traces':pack_vectors(vectors),'evaluations':evaluations,
        'encoding':'First vector is cycle0. For each [repeat, dictionary_index], increment cycle, copy previous vector and apply indexed column/value changes. Every case roundtrips exactly. Empty/inactive values are preserved, not invented.',
        'sampling':'Inputs driven while clock low; pre sampled +4ns, posedge +5ns, post +9ns. Handshake uses pre. Reset synchronous active-high.',
        'reproduction':'Both failing full batches independently replayed through the same fixed driver in Icarus. Meaningful pin traces and complete checker outputs agree with Verilator. Additional simulations are diagnostic, not experimental model rounds.',
        'limits':'Selected earliest failing batch per arm, anonymized. Does not claim to explain every later diagnostic. Hand controls are independent fixtures, not a whole-IP golden model. No coverage/arm/cost evidence or counterexamples are sent to stimulus generation.'}
    prompt=INSTRUCTIONS+json.dumps(body,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Review byte cap: '+str(len(prompt.encode())))
    (out/'packet.json').write_text(json.dumps(body,separators=(',',':'))+'\n')
    (out/'prompt.txt').write_text(prompt)
    (out/'private-case-map.json').write_text(json.dumps(private,indent=2)+'\n')
    (out/'diagnostic-replays.json').write_text(json.dumps({'executions':len(replays),
        'executed_cycles':sum(e['cycles'] for e in replays),'runs':replays},indent=2)+'\n')
    m={'prompt_bytes':len(prompt.encode()),'trace_rows':sum(map(len,cases.values())),
        'prompt_sha256':sha(out/'prompt.txt'),'packet_sha256':sha(out/'packet.json'),
        'hashes':{**hashes,**{str(p.relative_to(ROOT)):sha(p) for p in sources}},
        'model':'claude-opus-5-5','calls_max':1,'cli_budget_usd':4,'read_only':True}
    (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({k:v for k,v in m.items() if k!='hashes'}))


def review(packet,out):
    m=json.loads((packet/'manifest.json').read_text())
    for n in ['prompt','packet']:
        if sha(packet/(n+('.txt' if n=='prompt' else '.json')))!=m[n+'_sha256']:raise ValueError('Packet drift')
    for p,h in m['hashes'].items():
        if sha(ROOT/p)!=h:raise ValueError('Evidence drift')
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode&0o077:raise ValueError('Hidden key missing or unsafe')
    env={k:v for k,v in os.environ.items() if not k.startswith(('OPENAI_','ANTHROPIC_','CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip()
    try:
        result=call((packet/'prompt.txt').read_text(),out,env,'WBXBAR frozen failure attribution reviewer')
        (out/'review.json').write_text(json.dumps(result,indent=2)+'\n')
        (out/'packet-manifest.json').write_bytes((packet/'manifest.json').read_bytes())
        print(json.dumps({'status':'review_returned','findings':len(result.get('case_findings',[]))}))
    finally:KEY_FILE.unlink(missing_ok=True);env.pop('ANTHROPIC_API_KEY',None)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['prepare','live'],required=True)
    p.add_argument('--run',type=Path);p.add_argument('--packet',type=Path);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.mode=='prepare':prepare(a.run.resolve(),a.output.resolve())
    else:review(a.packet.resolve(),a.output.resolve())
