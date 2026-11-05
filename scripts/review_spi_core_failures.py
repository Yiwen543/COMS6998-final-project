"""Read-only, independent Claude attribution of frozen post-pilot failures.

No checker edits, target selection, stimulus generation or experimental reruns.
Uses the existing isolated CLI transport and hidden credential convention.
"""
import argparse
import json
import os
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from spi_core_safe_experiment import verify_freeze,CONTRACT as OFFER_CONTRACT
from spi_core_experiment import CANDIDATE,CONTRACT
from spi_core_safe_runtime import BASE,DRIVER
from spi_core_interface import FIELDS,OUTPUTS
from spi_core_safe_interface import FIELDS as REQUEST,STATE
from real_parent_screen import configuration
from prepare_spi_checker_role import excerpt
from review_spi_core_safe_driver import pack_vectors
from revise_spi_checker_role import call
from run_claude_divider_audit import KEY_FILE

INSTRUCTIONS='''Independently attribute the observed SPI verification failures. READ ONLY; no tools, no patches, no stimulus generation.
You are the diagnostic reviewer, not the stimulus author or the checker-author role. The frozen checker was authored by Claude;
do not assume it is correct. DUT implementation is diagnostic evidence, NEVER normative authority for expected behavior.
Use pinned public specification for obligations, the full actual pre/post public-pin traces for observations, and exact
checker/DUT sources to distinguish root causes from cascaded diagnostics. Cases are anonymized; do not infer performance arms.
For each failure cluster, consider DUT violation, checker defect, driver/measurement defect, specification ambiguity and unresolved.
Pay particular attention to command acceptance versus start/finish, mixed CPHA/CPOL and clock timing, CS kept across adjacent
segments, same-CSID versus changed-CSID configuration, and segment queue ownership of edges. Do not presume any hypothesis wins.
Identify earliest causal discrepancy with exact cycles and source lines/functions. Count repeated failures separately from
distinct root-cause hypotheses. Agreement of two simulators is reproducibility evidence, not proof of correctness.
The positive case does not prove the checker. Prior known scope limits remain; do not quietly exempt new failing behavior.
Return ONLY JSON: {case_findings:[{case_id,classification,confidence,earliest_causal_cycle,evidence,root_cause_hypotheses,
cascaded_diagnostics,specification_basis,checker_source_basis,rtl_source_basis,unresolved}],
distinct_root_cause_summary:[], additional_discriminating_controls:[], checker_fit_for_new_scope:boolean,
required_followup:[], limitations:[]}. Do not change frozen historical verdicts. If a revision is needed, a separate
specification-only author must later implement it and pass independent controls. You cannot authorize B/C here.
'''

def read(p):return json.loads(p.read_text())

def prepare(out):
    run=BASE/'b-live-v1';f=verify_freeze(run/'freeze.json')
    if read(run/'audit.json')['status']!='pass':raise ValueError('Saved evidence audit incomplete')
    c=configuration('spi_host_core');root=ROOT/c['root']
    columns=[*[('request',k) for k in REQUEST],*[('action',k) for k in FIELDS],
        *[('pre',k) for k in OUTPUTS],*[('post',k) for k in OUTPUTS],*[('queue',k) for k in STATE if k!='cycle']]
    vectors={};evaluation={};hashes={};case_map={}
    # Order is independent of measured coverage or token results.
    for alias,rep in [('case_x',3),('case_y',1),('case_z',2)]:
        p=run/f'rep{rep}/round6';requests=read(p/'requests.json')['actions'];trace=read(p/'trace.json');queue=read(p/'transport.json')
        v=[]
        for a,t,q in zip(requests,trace,queue):
            obj={'request':a,'action':t['action'],'pre':t['pre'],'post':t['post'],'queue':q}
            v.append([obj[section][k] for section,k in columns])
        assert len(requests)==len(trace)==len(queue)==len(v)
        vectors[alias]=v;r=read(p/'result.json')
        evaluation[alias]={k:r[k] for k in ('checker','transport','delivery_complete','verification_complete','executed_cycles')}
        case_map[alias]={'repetition':rep,'round':6,'path':str(p.relative_to(ROOT))}
        hashes.update({str((p/n).relative_to(ROOT)):sha(p/n) for n in ('requests.json','trace.json','transport.json','result.json')})
    source_paths=[CONTRACT,OFFER_CONTRACT,DRIVER,CANDIDATE/'checker.py',CANDIDATE/'contract.md',
        *[root/p for p in c['sources']]]
    # Keep direct upstream text separate from project interpretation.
    authority=excerpt(root/'hw/ip/spi_host/doc/theory_of_operation.md',[(91,145),(194,320),(363,377),(395,419),(478,483),(579,585),(629,675)])
    body={'role':'fresh independent diagnostic reviewer; no model-performance or coverage evidence',
      'DUT_revision':c['revision'],'public_authority':authority,
      'public_authority_url':'https://github.com/lowRISC/opentitan/blob/'+c['revision']+'/hw/ip/spi_host/doc/theory_of_operation.md',
      'sources':{str(p.relative_to(ROOT)):p.read_text() for p in source_paths},
      'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in source_paths},
      'trace_columns':columns,'complete_traces':pack_vectors(vectors),'evaluations':evaluation,
      'encoding':'Each first vector is cycle 0. Each [repeat,index] copies the preceding row and applies [column,value] changes from change_dictionary for repeat cycles. Full traces were losslessly roundtrip checked.',
      'sampling':'Input drive at clock-low; pre at +4ns, posedge +5ns, post +9ns, negedge +10ns. Handshake is pre.valid AND pre.ready. Command/TX offers enqueue once; accepted head replaced only next cycle. Hardware reset active-low asynchronous. No hidden drain.',
      'transport_oracle_scope':'The separate Python transport oracle is not reprinted or independently validated in this packet. Actual fixed SV driver and complete request/pin/queue traces are supplied for direct checking.',
      'diagnostic_reproducibility':{'case_x':'Full original Verilator trace, queue and checker verdict equal separately replayed Icarus.',
           'case_z':'Full original Verilator trace, queue and checker verdict equal separately replayed Icarus.',
           'case_y':'Positive live Verilator control; no additional Icarus replay of this particular case supplied.'},
      'limits':['Frozen checker supports two-state Standard/Dual/Quad with restrictions; dummy/software-reset completion outside this experiment.',
                'Byte-lane order follows registered public-parent mapping interpretation, not disputed older component prose; contract in sources records it.',
                'No coverage values, guard target groups, model prompts, API usage, performance rankings or proposed new targets supplied.'],
      'author_separation':'Reviewer may see RTL for diagnosis. Any later checker author receives public spec/interface and general findings only, not these traces or implementation.'}
    prompt=INSTRUCTIONS+json.dumps(body,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Local packet cap: '+str(len(prompt.encode())))
    out.mkdir(parents=True,exist_ok=False)
    (out/'packet.json').write_text(json.dumps(body,separators=(',',':'))+'\n');(out/'prompt.txt').write_text(prompt)
    (out/'private-case-map.json').write_text(json.dumps(case_map,indent=2)+'\n')
    manifest={'prompt_sha256':sha(out/'prompt.txt'),'packet_sha256':sha(out/'packet.json'),
       'source_hashes':body['source_hashes'],'trace_hashes':hashes,'builder_sha256':sha(Path(__file__)),
       'prompt_bytes':len(prompt.encode()),'full_trace_rows':sum(map(len,vectors.values())),
       'model':'claude-opus-5-5','calls_max':1,'cli_budget_usd':4,'read_only':True}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('source_hashes','trace_hashes')}))

def run(packet,out):
    m=read(packet/'manifest.json')
    for n in ('packet','prompt'):
        if sha(packet/('packet.json' if n=='packet' else 'prompt.txt'))!=m[n+'_sha256']:raise ValueError('Packet drift')
    for p,h in {**m['source_hashes'],**m['trace_hashes']}.items():
        if sha(ROOT/p)!=h:raise ValueError('Evidence drift: '+p)
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:raise ValueError('Hidden key absent or unsafe permissions')
    env={k:v for k,v in os.environ.items() if not k.startswith(('OPENAI_','ANTHROPIC_','CLAUDE_CODE_USE_'))}
    env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip()
    try:
        result=call((packet/'prompt.txt').read_text(),out,env,'SPI frozen failure attribution reviewer')
        (out/'review.json').write_text(json.dumps(result,indent=2)+'\n');(out/'packet-manifest.json').write_bytes((packet/'manifest.json').read_bytes())
        print(json.dumps({'status':'review_returned','case_findings':len(result.get('case_findings',[]))}))
    finally:KEY_FILE.unlink(missing_ok=True);env.pop('ANTHROPIC_API_KEY',None)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['prepare','live'],required=True)
    p.add_argument('--packet',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.mode=='prepare':prepare(a.output.resolve())
    else:run(a.packet.resolve(),a.output.resolve())
