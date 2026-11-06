#!/usr/bin/env python3
"""Read-only acceptance of completed local qualification artifacts, no reruns."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from common import ROOT,dump,sha
from controller_monitor_live import TASK
from controller_formal_diagnostic import harness
from controller_offline_pipeline import integrity,verify_formal_evidence,RUN
from controller_prepare import normalize


def resources(directory):
    result=dict(physical_DUT_simulations=0,physical_cycles=0,physical_simulation_seconds=0.0,
                monitor_replays=0,monitor_cycles=0,monitor_replay_seconds=0.0,
                compile_invocations=0,compile_seconds=0.0,formal_jobs=0,formal_seconds=0.0,
                missing_resource_records=[],witness_statuses={})
    witnesses=[]
    for p in directory.rglob('*.json'):
        if p.name not in ('execution.json','compile.json','iverilog.json','result.json'):continue
        d=json.loads(p.read_text())
        if not isinstance(d,dict):continue
        if p.name=='execution.json':
            result['physical_DUT_simulations']+=1
            if 'cycles' not in d or 'seconds' not in d:result['missing_resource_records'].append(str(p))
            else:result['physical_cycles']+=d['cycles'];result['physical_simulation_seconds']+=d['seconds']
        elif p.name in ('compile.json','iverilog.json'):
            result['compile_invocations']+=1
            if 'seconds' not in d:result['missing_resource_records'].append(str(p))
            else:result['compile_seconds']+=d['seconds']
        elif 'properties' in d and 'execution' in d:
            result['monitor_replays']+=1;result['monitor_cycles']+=d['cycles'];result['monitor_replay_seconds']+=d['execution']['seconds']
        elif 'solver_cap_seconds' in d:
            result['formal_jobs']+=1;result['formal_seconds']+=d['seconds']
        elif 'classification' in d and 'API_calls' in d:witnesses.append(d['status'])
    result['witness_statuses']=dict(Counter(witnesses))
    result['wall_and_component_times_overlap_do_not_add']=True
    return result


def verify(root,out):
    if out.exists():raise FileExistsError('Acceptance output exists')
    completion=json.loads((root/'completion.json').read_text());assert completion['status']=='completed' and completion['formal_mode']=='all'
    assert sha(root/'summary.json')==completion['summary_sha256'] and sha(root/'report.md')==completion['report_sha256']
    freeze_counts=integrity();bindings={};replays=0;cycles=0
    for p in root.rglob('result.json'):
        d=json.loads(p.read_text())
        if 'properties' in d and 'execution' in d:
            compressed=p.parent/'replay.log.gz';raw=gzip.decompress(compressed.read_bytes())
            assert sha(compressed)==d['compressed_log_sha256']
            assert hashlib.sha256(raw).hexdigest()==d['raw_log_sha256']==d['execution']['log_sha256']
            assert d['complete'];replays+=1;cycles+=d['cycles']
            bindings[str(p.relative_to(ROOT))]=sha(p);bindings[str(compressed.relative_to(ROOT))]=sha(compressed)
    cal=root/'formal-calibration';balanced=root/'balanced-correct'
    c=json.loads((cal/'summary.json').read_text());b=json.loads((balanced/'summary.json').read_text())
    assert c['status']=='passed' and len(c['jobs'])==18 and len(b['jobs'])==108
    expected={(arm,rep,slot,mode) for arm in ('B2_raw','C2_semantic') for rep in (1,2,3) for slot in range(6) for mode in ('bmc','prove','cover')}
    assert {(j['arm'],j['repetition'],j['slot'],j['mode']) for j in b['jobs']}==expected
    verify_formal_evidence(cal,c);verify_formal_evidence(balanced,b,True)
    for directory,data in ((cal,c),(balanced,b)):
        for j in data['jobs']:
            d=directory/j['directory'];r=json.loads((d/'result.json').read_text());variant=j.get('variant','cone')
            assert (d/'harness.sv').read_text()==harness(j['slot'],variant)
            assert r['depth']==24 and r['solver_cap_seconds']==(5 if j.get('name','').startswith(('always_','mutant-anchor')) else 10)
            if directory==balanced:assert sha(d/'work/src/dut.v')==sha(TASK/'public/rtl/axis_frame_length_adjust.v')
            for name in ('axis_fifo.v','axis_frame_length_adjust_fifo.v'):
                assert sha(d/'work/src'/name)==sha(TASK/'public/rtl'/name)
            assert sha(d/'work/src/task_top_v3.sv')==sha(TASK/'public/task_top_v3.sv')
            for name in ('result.json','sby.log','job.sby','harness.sv'):
                bindings[str((d/name).relative_to(ROOT))]=sha(d/name)
            if 'witness' in j:
                w=j['witness'];p=d/'physical-witness';saved=json.loads((p/'result.json').read_text());assert saved==w
                if w['status']=='adjudicated':
                    i=json.loads((p/'iverilog/rows.json').read_text());v=json.loads((p/'verilator/rows.json').read_text())
                    prefix=json.loads((p/'reference-prefix-rows.json').read_text())
                    assert normalize(i)==normalize(v) and prefix==i[:w['observed_alarm_state']]
                    oracle=json.loads((p/'reference.json').read_text());assert oracle['verdict']==w['reference_verdict']
                    if oracle['verdict']=='FAIL':assert oracle['failures']
                    traces=list((d/'work').glob('engine_*/trace.vcd'));assert len(traces)==1 and sha(traces[0])==w['witness_sha256']
                    for sim in ('iverilog','verilator'):
                        exe=json.loads((p/sim/'execution.json').read_text());assert sha(p/sim/'simulation.log')==exe['log_sha256']
    proof=json.loads((TASK/'qualification/typed-v5/proof/proof.json').read_text())
    for name,h in proof['hashes'].items():assert sha(Path(name))==h
    e=json.loads((TASK/'qualification/typed-v5/screen/extraction.json').read_text())
    packet=json.loads((TASK/'qualification/prompt-audit-v3/C2_semantic.json').read_text())['egraph_feedback']
    assert all(v==e['atoms'][k] for k,v in packet['typed_atoms'].items())
    migration=json.loads((ROOT/'docs/audits/migration_2026-11-04.json').read_text())
    assert all(sha(ROOT/p)==h for p,h in migration['functional_files_before'].items())
    assert sha(ROOT/'AGENTS.md')==migration['document_sha256']['AGENTS.md']
    assert sha(ROOT/'docs/AGENT_HANDOFF.md')==migration['retained_historical_handoff_sha256']
    assert sha(ROOT/'test2/results/controller-final-v1/scores.json')=='f13161340a46c7360002e54992be0a7aba9c1d47a70fbe6f169bba8952fe2651'
    assert sha(ROOT/'test2/results/live-final-v1/scores.json')=='33003b33a7172d29704f85fa84da10bdbb30aebe78b72d400a4f97b73a2ef338'
    for name in ('build/private/midterm-openai-key','build/private/anthropic-crosscheck-key'):assert not (ROOT/name).exists()
    for p in (root/'sources').glob('*.py'):
        assert sha(p)==sha(ROOT/'test2/scripts'/p.name);bindings[str(p.relative_to(ROOT))]=sha(p)
    costs=resources(root)
    for name in ('controller-formal-diagnostic-v1','controller-physical-witness-replay-v2','controller-formal-diagnostic-v2','controller-balanced-correct-v1','controller-obligations-v1'):
        costs[name]=resources(ROOT/'test2/results'/name)
    result=dict(status='accepted_with_scope',completion_sha256=sha(root/'completion.json'),freeze_members=freeze_counts,
                API_calls=0,new_independent_model_trials=0,new_formal_jobs_in_full_CLI=126,
                formal_statuses=dict(Counter(j['status'] for j in b['jobs'])),
                replay_logs_verified=replays,monitor_cycles_verified=cycles,typed_certificate_dependencies_verified=len(proof['hashes']),
                resources=costs,source_atoms_width_signedness_mapping_preserved=True,
                original_scores_and_migration531files_AGENTS_history_intact=True,staged_keys_absent=True,
                no_whole_monitor_soundness_claim=True,fresh_API_connectivity_not_tested=True,source_sha256=sha(__file__),files=bindings)
    dump(out,result);print(json.dumps({k:v for k,v in result.items() if k not in ('files','resources')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();verify(a.run.resolve(),a.output.resolve())
