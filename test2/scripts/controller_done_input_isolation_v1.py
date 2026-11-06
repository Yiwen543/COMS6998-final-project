"""API-free post-hoc physical obligation control; never changes the B/C score."""
import argparse
import gzip
import json
from pathlib import Path
import time
from common import ROOT, BASE, dump, run, sha
import controller_prepare as transport
from controller_done_data import TASK, SOURCE_TASK, SOURCES, sequence
from controller_done_runtime import replay
from controller_done_case_v4 import grade
from controller_reference_evaluate import module
from controller_release_live import verify_release

REG=BASE/'configs/controller_done_input_isolation_v1.json'
PACKAGE=TASK/'qualification/input-completion-isolation-v1/physical-control-v1'
LIVE=BASE/'results/controller-done-live-v2'


def load(p):return json.loads(p.read_text())


def prepare():
    verify_release(LIVE);PACKAGE.mkdir(parents=True,exist_ok=False)
    source=SOURCES[0].read_text();changes=[('assign s_axis_tready = s_axis_tready_reg;',"assign s_axis_tready = 1'b0;",1),
        ('m_axis_tvalid_int = s_axis_tvalid;','m_axis_tvalid_int = s_axis_tvalid && s_axis_tready;',2),
        ('m_axis_tvalid_int = s_axis_tvalid && s_axis_tlast;','m_axis_tvalid_int = s_axis_tvalid && s_axis_tlast && s_axis_tready;',1)]
    for before,after,count in changes:
        if source.count(before)!=count:raise ValueError('Source mapping changed')
        source=source.replace(before,after)
    control=PACKAGE/'blocked_input_control.v';control.write_text(source)
    actions=sequence([1],16,128,6999401);dump(PACKAGE/'actions.json',dict(seed=6999401,actions=actions,require_drained=True,min_tail=128))
    checker=SOURCE_TASK/'reference/frozen-v2/checker.py'
    inputs=[control,PACKAGE/'actions.json',TASK/'public/driver.sv',checker,*SOURCES,Path(__file__).resolve()]
    reg=dict(status='REGISTERED_BEFORE_NEW_PHYSICAL_RUNS',API_calls_allowed=False,
        kind='Post-hoc diagnostic of already frozen candidates; composite physical RTL obligation control, not a new natural mutation or independent LLM trial',
        reason='Original input stratum all overlaps earlier safety and unavoidable quiet-tail unknown; preserve all old outcomes',
        source_changes=[dict(before=x,after=y,occurrences=n) for x,y,n in changes],
        expected_scope='Correct source PASS/zero unknown; blocked control only definite final unaccepted input FAIL plus retained drain_tail_short UNKNOWN, no earlier safety or response debt',
        strict_qualification=['Both simulators physically agree','No earlier sampled safety failure on blocked source','No response completion failure on blocked source','Final offered-valid fail present','Unavoidable short-tail unknown retained'],
        actual_new_cases=1,seed=6999401,actions=len(actions),physical_build_cap=4,physical_simulation_cap=4,
        compile_seconds=60,simulate_seconds=15,candidate_replay_cap=24,independent_new_model_trials=0,
        release_sha256=sha(LIVE/'release.json'),files={str(p.relative_to(ROOT)):sha(p) for p in inputs})
    if REG.exists():raise ValueError('Registration already exists')
    dump(REG,reg);dump(PACKAGE/'input-freeze.json',dict(registration_sha256=sha(REG),files=reg['files']))


def execute(out):
    # Avoid competing for CPU with the already registered timed formal schedule.
    if not (BASE/'results/controller-done-live-formal-v2/summary.json').exists():raise ValueError('Finish the fixed formal schedule before new physical tools')
    reg=load(REG);freeze=load(PACKAGE/'input-freeze.json')
    if sha(REG)!=freeze['registration_sha256']:raise ValueError('Registration changed')
    for n,h in freeze['files'].items():
        if sha(ROOT/n)!=h:raise ValueError('Frozen control input changed: '+n)
    verify_release(LIVE)
    if sha(LIVE/'release.json')!=reg['release_sha256']:raise ValueError('Candidate release changed')
    out.mkdir(parents=True,exist_ok=False);start=time.monotonic();records=[];observations={};builds=simulations=0
    checker=module(SOURCE_TASK/'reference/frozen-v2/checker.py','independent_input_isolation_reference')
    actions=load(PACKAGE/'actions.json')['actions'];transport.configure(TASK)
    for name,source in [('correct',SOURCES[0]),('blocked_control',PACKAGE/'blocked_input_control.v')]:
        transport.SOURCES=[source]+SOURCES[1:]
        for sim in ('iverilog','verilator'):
            d=out/name/sim;d.mkdir(parents=True);binary=d/('obj/Vtb_natural_inventory' if sim=='verilator' else 'driver.vvp')
            argv=(['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr','-Wno-fatal','--top-module','tb_natural_inventory','--Mdir',binary.parent,'-j','2'] if sim=='verilator' else ['iverilog','-g2012','-s','tb_natural_inventory','-o',binary])
            builds+=1;c=run(argv+transport.SOURCES+[TASK/'public/driver.sv'],d/'compile.log',60);dump(d/'compile.json',c)
            if c['status']!='complete':records.append(dict(source=name,simulator=sim,status='compile_'+c['status']));continue
            try:
                simulations+=1;rows=transport.simulate(sim,binary,actions,d/'observation');oracle=checker.check_rows(rows,require_drained=True,min_tail=128)
                dump(d/'observation/reference.json',oracle);observations[name,sim]=rows
                failures=oracle['failures'];safety=[f for f in failures if f['phase'] in ('pre','post')]
                completion=[f for f in failures if f['phase']=='end' and f['category']=='completion'];inp=[f for f in completion if 's_valid still offered' in f['detail']]
                rec=dict(source=name,simulator=sim,trace='isolated_offer_seed6999401',status='complete',verdict=oracle['verdict'],unknown_records=len(oracle['unknown']),
                    first_safety_failure=safety[0] if safety else None,response_completion=bool([f for f in completion if f not in inp]),input_completion=bool(inp),
                    end_only=bool(completion) and not safety,rows_sha256=sha(d/'observation/rows.json'),directory=str((d/'observation').relative_to(ROOT)),cycles=len(rows),
                    failures=failures,unknown=oracle['unknown'])
            except Exception as e:rec=dict(source=name,simulator=sim,status='infrastructure_unresolved',error_type=type(e).__name__)
            records.append(rec);dump(out/'physical-progress.json',records)
    correct=[r for r in records if r['source']=='correct'];blocked=[r for r in records if r['source']=='blocked_control']
    agreements={name:all((name,s) in observations for s in ('iverilog','verilator')) and transport.normalize(observations.get((name,'iverilog'),[]))==transport.normalize(observations.get((name,'verilator'),[])) for name in ('correct','blocked_control')}
    gates=dict(correct=len(correct)==2 and all(r.get('verdict')=='PASS' and r.get('unknown_records')==0 for r in correct),dual_physical_agreement=all(agreements.values()),
        isolated_input=len(blocked)==2 and all(r.get('verdict')=='FAIL' and r.get('input_completion') and not r.get('first_safety_failure') and not r.get('response_completion') for r in blocked),
        unavoidable_unknown_retained=len(blocked)==2 and all(r.get('unknown_records') and all(u['category']=='drain_tail_short' for u in r.get('unknown',[])) for r in blocked))
    dump(out/'physical-freeze.json',dict(qualified=all(gates.values()),records=records,gates=gates,files={str(p.relative_to(ROOT)):sha(p) for p in out.rglob('*.json') if p.name!='physical-progress.json'}))
    candidates=[];replays=cycles=0
    if all(gates.values()):
        for selected in load(LIVE/'final-candidates.json')['candidates']:
            cases=[]
            if not selected['directory']:candidates.append({**selected,'status':'candidate_unavailable'});continue
            for label in records:
                rows=observations[label['source'],label['simulator']];d=out/'candidate-replays'/selected['arm']/f"rep{selected['repetition']}"/label['source']/label['simulator']
                r=replay(LIVE/selected['directory'],rows,d,out/'row-cache');replays+=1;cycles+=r['cycles']
                case=grade(label,(ROOT/label['directory']/'rows.json').read_bytes(),r,gzip.decompress((d/'replay.log.gz').read_bytes()));cases.append(case)
            control_ok=all(c['status']=='graded' and not c['is_unresolved'] and c['alarm_samples_including_marker']==0 for c in cases if c['source']=='correct')
            candidates.append(dict(arm=selected['arm'],repetition=selected['repetition'],selected_round=selected['selected_round'],diagnostic_two_correct_controls_ok=control_ok,
                blocked_end_alarm_no_earlier_pairs=sum(c['status']=='graded' and c['marker_alarm'] and not c['early_finite_alarm_samples'] for c in cases if c['source']=='blocked_control'),
                blocked_unknown_pairs=sum(c['is_unresolved'] for c in cases if c['source']=='blocked_control'),cases=cases))
    result=dict(status='PHYSICAL_INPUT_OBLIGATION_CONTROL_QUALIFIED' if all(gates.values()) else 'QUALIFICATION_FAILED_PRESERVED',gates=gates,records=records,
        candidates=candidates,dual_agreements=agreements,physical_builds=builds,physical_simulations=simulations,
        physical_simulations_completed=sum(r.get('status')=='complete' for r in records),unknown_physical_cycle_attempts=simulations-sum(r.get('status')=='complete' for r in records),
        physical_cycles=sum(r.get('cycles',0) for r in records),candidate_replays=replays,candidate_replay_cycles=cycles,wall_seconds=time.monotonic()-start,
        API_calls=0,new_model_trials=0,old_scores_changed=False,not_a_new_registered_BC_effect='Post-hoc artificial composite obligation control only; do not add a mutation ID/coverage or change old scores',
        registration_sha256=sha(REG),release_sha256=sha(LIVE/'release.json'),producer_sha256=sha(__file__))
    dump(out/'summary.json',result);verify_release(LIVE);print(result['status'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
    if a.prepare:prepare()
    elif a.output:execute(a.output.resolve())
    else:p.error('Choose --prepare or --output')
