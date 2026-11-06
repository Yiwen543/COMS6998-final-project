#!/usr/bin/env python3
"""Fresh fixed physical observations for the versioned final-post-marker study."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import time
from common import ROOT,BASE,dump,run,sha
import controller_prepare as transport
from controller_monitor_live import TASK as SOURCE_TASK
from controller_reference_evaluate import module

TASK=BASE/'tasks/axis_length_done_v1'
REG=BASE/'configs/controller_done_study_v1.json'
SOURCES=[SOURCE_TASK/'public/rtl'/n for n in ('axis_frame_length_adjust.v','axis_fifo.v','axis_frame_length_adjust_fifo.v')]+[SOURCE_TASK/'public/task_top_v3.sv']


def sequence(lengths,body,tail,seed,pressure=False,reset=None):
    rng=random.Random(seed);offers=[(rng.randrange(256),int(i==n-1)) for n in lengths for i in range(n)]
    if len(offers)>body:raise ValueError('Offered sequence exceeds fixed body')
    actions=[transport.action(reset=1),transport.action(reset=1)]+[transport.action() for _ in range(4)]
    for i in range(body):
        a=transport.action()
        if i<len(offers):a.update(offer=1,data=offers[i][0],last=offers[i][1])
        if pressure:a.update(data_ready=int(i%11 not in (1,2,3,4)),status_ready=int(i%13 not in (3,4,5,6,7)))
        if reset is not None and i==reset:a=transport.action(reset=1)
        actions.append(a)
    return actions+[transport.action() for _ in range(tail)]


def datasets():
    dev={'frame_lengths':sequence([1,4,8,12],36,32,6998201),
         'independent_channels':sequence([3,8,2,10],40,32,6998202,True),
         'reset_and_drain':sequence([8,1,12,4],40,32,6998203,True,13)}
    final={f'probe_{i:02}':sequence(lengths,80,128,6999300+i,True,reset)
           for i,(lengths,reset) in enumerate([([1,4,8,12,3,9],None),([12,2,8,5,1,4],None),
               ([8,3,11,4,7,1],9),([4,4,12,1,9,2],23),([2,9,8,6,1,12],37),([12,1,7,4,10,3],None)],1)}
    return dev,final


def mutations(source):
    changes=[('completion_input','handshake_reset','assign s_axis_tready = s_axis_tready_reg;',"assign s_axis_tready = 1'b0;",1),
      ('completion_data','handshake_reset','assign m_axis_tvalid = m_axis_tvalid_reg;',"assign m_axis_tvalid = 1'b0;",1),
      ('completion_status','handshake_reset','assign status_valid = status_valid_reg;',"assign status_valid = 1'b0;",1),
      ('data_last','payload_status','assign m_axis_tlast  = m_axis_tlast_reg;',"assign m_axis_tlast  = m_axis_tlast_reg ^ 1'b1;",1),
      ('status_pad','payload_status','assign status_frame_pad = status_frame_pad_reg;',"assign status_frame_pad = status_frame_pad_reg ^ 1'b1;",1),
      ('status_truncate','payload_status','assign status_frame_truncate = status_frame_truncate_reg;',"assign status_frame_truncate = status_frame_truncate_reg ^ 1'b1;",1),
      ('status_length','payload_status','assign status_frame_length = status_frame_length_reg;',"assign status_frame_length = status_frame_length_reg ^ 16'h0002;",1),
      ('status_original_length','payload_status','assign status_frame_original_length = status_frame_original_length_reg;',"assign status_frame_original_length = status_frame_original_length_reg ^ 16'h0002;",1),
      ('data_rotation','payload_status','assign m_axis_tdata  = m_axis_tdata_reg;','assign m_axis_tdata  = {m_axis_tdata_reg[0],m_axis_tdata_reg[7:1]};',1),
      ('temporary_data','payload_status','m_axis_tdata_reg <= temp_m_axis_tdata_reg;',"m_axis_tdata_reg <= temp_m_axis_tdata_reg ^ 8'h80;",1),
      ('short_counter_step','boundary_guard','short_counter_next = short_counter_reg - KEEP_WIDTH;',"short_counter_next = short_counter_reg - KEEP_WIDTH - 16'd1;",2),
      ('long_counter_step','boundary_guard','long_counter_next = long_counter_reg - KEEP_WIDTH;',"long_counter_next = long_counter_reg - KEEP_WIDTH - 16'd1;",2)]
    faults=[]
    for i,(family,stratum,old,new,nth) in enumerate(changes,1):
        parts=source.split(old)
        if len(parts)<=nth:raise ValueError('Mutation site absent')
        modified=old.join(parts[:nth])+new+old.join(parts[nth:])
        lines=[n for n,(a,b) in enumerate(zip(source.splitlines(),modified.splitlines()),1) if a!=b]
        if len(lines)!=1 or len(source.splitlines())!=len(modified.splitlines()):raise ValueError('Expected exactly one changed line')
        faults.append(dict(id=f'N{i:02}',family=family,stratum=stratum,line=lines[0],text=modified))
    return faults


def prepare():
    reg=json.loads(REG.read_text());TASK.mkdir(parents=True,exist_ok=False)
    for name,h in reg['sources'].items():
        if sha(ROOT/name)!=h:raise ValueError('Original source changed')
    dev,final=datasets();observed=[]
    for split,traces in [('development',dev),('final',final)]:
        folder=TASK/('public/development' if split=='development' else 'private/final')
        for name,actions in traces.items():
            p=folder/(name+'.json');dump(p,dict(actions=actions,require_drained=True,min_tail=32 if split=='development' else 128))
            observed.append(p)
    public=TASK/'public';(public/'driver.sv').write_text(transport.DRIVER)
    (public/'specification.md').write_bytes((SOURCE_TASK/'public/specification_v2.md').read_bytes())
    (public/'observer_contract.md').write_text('''# Final-post marker monitor contract v1

Use the unchanged public DUT pins in specification.md and the supplied module header.
The passive monitor additionally observes readonly trace_done:0 at every pre sample
and all post samples except the final post sample, where it is1. No extra rising
edge follows this marker. Enable finite-end checks combinationally from trace_done
and private state already updated by the final edge. The marker is evaluator
metadata, not a DUT input, truth label, reset or stimulus modification.

Development evaluations require drained=true,min_tail32; final evaluations use
drained=true,min_tail128. Definite failures and unknowns retain their independent
reference meanings; a short tail is never automatically accepted. A presented
valid safety failure is distinct from end-only response/input completion failure.
Independent reference inputs remain exactly the original six inputs/nine outputs;
the marker does not modify the Claude reference function or DUT specification.

Six active/ok slots,body<=16000UTF8bytes,state<=8192bits; readonly public pins,
posedge clk only, no hierarchy/files/assumptions/system calls. Short formal safety
projection explicitly sets trace_done=0 and cannot prove finite completion.
''')
    faults=mutations(SOURCES[0].read_text());catalog=[]
    for f in faults:
        p=TASK/'private/mutants'/(f['id']+'.v');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(f.pop('text'))
        catalog.append(dict(f,source=str(p.relative_to(ROOT)),sha256=sha(p)))
    dump(TASK/'private/mutant-catalog.json',dict(faults=catalog,chosen_before_any_candidate_outcomes=True,new_source_mutations=True,not_unseen_IP=True))
    dump(TASK/'task-config.json',dict(sources=[str(p.relative_to(ROOT)) for p in SOURCES],semantic_directory='test2/tasks/axis_length_fifo_v1/qualification/typed-v5',source_registration=str(REG.relative_to(ROOT)),formal_registration=str(REG.relative_to(ROOT))))
    files=observed+[public/'driver.sv',public/'specification.md',public/'observer_contract.md',TASK/'private/mutant-catalog.json',TASK/'task-config.json',REG]+SOURCES+[ROOT/f['source'] for f in catalog]
    dump(TASK/'input-freeze.json',dict(registration_sha256=sha(REG),generator_sha256=sha(__file__),files={str(p.relative_to(ROOT)):sha(p) for p in files},provider_seed=None,local_seeds=reg['local_seeds'],candidate_live_allowed=False))
    (TASK/'producer.py').write_bytes(Path(__file__).read_bytes())


def measure():
    reg=json.loads(REG.read_text());freeze=json.loads((TASK/'input-freeze.json').read_text())
    if sha(REG)!=freeze['registration_sha256']:raise ValueError('Registered data plan changed')
    for n,h in freeze['files'].items():
        if sha(ROOT/n)!=h:raise ValueError('Frozen new input changed')
    out=TASK/'measurements-v1';out.mkdir(exist_ok=False)
    checker=module(SOURCE_TASK/'reference/frozen-v2/checker.py','independent_done_reference')
    dev,final=datasets();catalog=json.loads((TASK/'private/mutant-catalog.json').read_text())['faults'];records=[];baseline={};started=time.perf_counter()
    transport.configure(TASK)
    for item in [dict(id='correct',source=str(SOURCES[0].relative_to(ROOT)))]+catalog:
        transport.SOURCES=[ROOT/item['source']]+SOURCES[1:]
        traces=list(dev.items())+list(final.items()) if item['id']=='correct' else list(final.items())
        for sim in ('iverilog','verilator'):
            build=out/item['id']/sim;build.mkdir(parents=True)
            binary=build/('obj/Vtb_natural_inventory' if sim=='verilator' else 'driver.vvp')
            cmd=(['verilator','--binary','--timing','--coverage-line','--coverage-toggle','--coverage-expr','-Wno-fatal','--top-module','tb_natural_inventory','--Mdir',binary.parent,'-j','2'] if sim=='verilator' else ['iverilog','-g2012','-s','tb_natural_inventory','-o',binary])
            compilation=run(cmd+transport.SOURCES+[TASK/'public/driver.sv'],build/'compile.log',60);dump(build/'compile.json',compilation)
            if compilation['status']!='complete':
                records.append(dict(source=item['id'],simulator=sim,status='compile_'+compilation['status']));dump(out/'partial.json',records);continue
            for name,actions in traces:
                d=build/name
                try:
                    rows=transport.simulate(sim,binary,actions,d);minimum=32 if name in dev else 128
                    oracle=checker.check_rows(rows,require_drained=True,min_tail=minimum);dump(d/'reference.json',oracle)
                    if item['id']=='correct':baseline[sim,name]=rows
                    safety=[f for f in oracle['failures'] if f['phase'] in ('pre','post')]
                    completion=[f for f in oracle['failures'] if f['phase']=='end' and f['category']=='completion']
                    inp=[f for f in completion if 's_valid still offered' in f['detail']]
                    rec=dict(source=item['id'],simulator=sim,trace=name,split='development' if name in dev else 'final',status='complete',
                             verdict=oracle['verdict'],unknown_records=len(oracle['unknown']),first_safety_failure=safety[0] if safety else None,
                             response_completion=bool([f for f in completion if f not in inp]),input_completion=bool(inp),
                             end_only=bool(completion) and not safety,rows_sha256=sha(d/'rows.json'),reference_sha256=sha(d/'reference.json'),
                             directory=str(d.relative_to(ROOT)),cycles=len(rows),minimum_tail=minimum)
                except Exception as error:rec=dict(source=item['id'],simulator=sim,trace=name,status='infrastructure_error',error_type=type(error).__name__,attempted_cycles=len(actions),cycles=None)
                records.append(rec);dump(out/'partial.json',records)
            print('measured',item['id'],sim,flush=True)
    agreements={name:transport.normalize(baseline.get(('iverilog',name),[]))==transport.normalize(baseline.get(('verilator',name),[])) and ('iverilog',name) in baseline for name in list(dev)+list(final)}
    correct=[r for r in records if r['source']=='correct'];gate=len(correct)==18 and all(r.get('verdict')=='PASS' and not r.get('unknown_records') for r in correct) and all(agreements.values())
    result=dict(status='qualified' if gate else 'baseline_qualification_failed',records=records,dual_correct_agreement=agreements,
                API_calls=0,new_model_trials=0,physical_build_attempts=26,physical_simulation_attempts=sum('trace' in r for r in records),
                completed_physical_cycles=sum(r['cycles'] for r in records if r.get('cycles') is not None),unknown_cycle_cases=sum(r.get('status')=='infrastructure_error' for r in records),wall_seconds=time.perf_counter()-started,
                reference_checker_sha256=sha(SOURCE_TASK/'reference/frozen-v2/checker.py'),registration_sha256=sha(REG),generator_sha256=sha(__file__))
    dump(out/'summary.json',result)
    # Seal all observations before any candidate prompt/monitor run exists.
    members={str(p.relative_to(ROOT)):sha(p) for p in out.rglob('*.json') if p.name not in ('partial.json',)}
    members.update(freeze['files']);dump(TASK/'evaluation-freeze.json',dict(status=result['status'],files=members,input_freeze_sha256=sha(TASK/'input-freeze.json'),reference_checker_sha256=result['reference_checker_sha256'],candidate_results_used=False))
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--measure',action='store_true');a=p.parse_args()
    if a.prepare:prepare()
    if a.measure:measure()
