"""Recheck final source/proof provenance and account for every offline attempt."""
import json
import subprocess
import sys
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from probe_natural_frontends import TOOLS
from probe_write_scopes import verify
from spi_core_safe_experiment import verify_freeze
from preflight_spi_host import identity

BASE=ROOT/'results/transaction_recovery_screen_20261104'
SCOPE=ROOT/'configs/transaction_recovery_screen_v1.json'

def audit():
    scope=json.loads(SCOPE.read_text());old=verify_freeze()
    expected=json.loads((ROOT/'configs/multistep_event_screen_v1.json').read_text())
    for k in ('development_budget','model_limits','development_acceptance','offline_acceptance','roles'):
        assert scope[k]==expected[k],k
    final={};hash_checks=0
    for c in scope['candidates']:
        verify(c);f=BASE/(c['top']+'-final');decision=json.loads((f/'decision.json').read_text());proof=json.loads((f/'proof/proof.json').read_text())
        assert decision['scope_sha256']==sha(SCOPE)
        for name in ('decision.json','proof/proof.json','screen/screen.json'):
            p=f/name
            if not p.exists():continue
            for path,h in json.loads(p.read_text()).get('hashes',{}).items():
                assert sha(Path(path))==h,('provenance',path);hash_checks+=1
        s=json.loads((f/'screen/screen.json').read_text()) if (f/'screen/screen.json').exists() else None
        if s:
            points=json.loads((f/'inventory/raw-points.json').read_text());assert len({identity(p) for p in points})==len(points)==s['raw_dut_denominator']
            membership=json.loads((f/'inventory/exact-counter-membership.json').read_text())
            assert sha(f/'inventory/seed.dat')==membership['raw_sha256']
            for path,h in membership['generated_hashes'].items():assert sha(Path(path))==h;hash_checks+=1
            assert not s['static_count_gate_pass']
        assert not decision['B_allowed'] and not decision['C_allowed'] and decision['model_calls']==0
        final[c['top']]={'status':decision['status'],'proof_status':proof['status'],
            'definition_checks':len(proof.get('definition_checks',[])),
            'definition_mismatches':sum(x['z3']!='unsat' for x in proof.get('definition_checks',[])),
            'unsafe_free_combinational_values':proof.get('unsafe_free_combinational_values',[]),
            'raw_denominator':s['raw_dut_denominator'] if s else None,'mapped':s['mapped'] if s else None,
            'unresolved':s['unresolved'] if s else None,'static_groups':s['static_candidate_groups'] if s else None,
            'nontrivial_groups':s['nontrivial_static_candidates'] if s else None,
            'ordinary_screen':'not run: static admission failed or semantic gate blocked',
            'checker':'not commissioned','B':'not run','C':'not run'}
    attempts=[];frontends=[];compilations=[];simulations=[]
    for p in sorted(BASE.glob('*/decision.json')):
        d=json.loads(p.read_text());f=p.parent;attempts.append({'path':str(f.relative_to(ROOT)),**d})
        probe=f/'probe.json'
        if probe.exists():frontends += [{'path':str(f.relative_to(ROOT)),**r} for r in json.loads(probe.read_text())['runs']]
        inv=f/'inventory/inventory.json'
        if inv.exists():
            i=json.loads(inv.read_text());compilations.append({'path':str(inv.relative_to(ROOT)),'seconds':i['compile_seconds']})
            simulations.append({'path':str(inv.relative_to(ROOT)),'cycles':i['cycles'],'seconds':i['simulation_seconds']})
    versions={}
    commands={'python':[sys.executable,'--version'],'verilator':['verilator','--version'],'icarus':['iverilog','-V'],
              'yosys':[str(TOOLS/'yosys'),'-V'],'slang':[str(TOOLS/'slang'),'--version'],'z3':['z3','--version'],
              'rust':['rustc','--version'],'cargo':['cargo','--version']}
    for k,cmd in commands.items():
        p=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=30);versions[k]=p.stdout.splitlines()[0]
    versions['egg']=json.loads((BASE/'axis_ram_switch-final/screen/egg.json').read_text())['engine']
    versions['egg_binary_sha256']=sha(ROOT/'egraph/target/debug/guard_proofs')
    tests=[]
    for pattern in ('test_transaction*.py','test_multistep_event_screen.py','test_spi_core_safe_driver.py','test_spi_core_safe_accounting.py'):
        cmd=[sys.executable,'-m','unittest','discover','-s','tests','-p',pattern,'-v']
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=180)
        name=pattern.replace('*','_').replace('.py','')+'.log';(BASE/name).write_text(p.stdout+p.stderr)
        tests.append({'pattern':pattern,'returncode':p.returncode,'log':name,'command':cmd})
        if p.returncode:raise ValueError('Test failure: '+name)
    result={'status':'offline_screen_complete_no_candidate_admitted','scope_sha256':sha(SCOPE),
            'script_sha256':sha(Path(__file__)),'final':final,'current_artifact_hash_checks':hash_checks,
            'old_spi_freeze_unchanged':True,'original_budget_unchanged':True,'versions':versions,'tests':tests,
            'accounting':{'screen_attempts':len(attempts),'frontend_invocations':len(frontends),
                          'frontend_failures':sum(x['returncode']!=0 for x in frontends),
                          'inventory_binary_compilations':len(compilations),'inventory_simulator_executions':len(simulations),
                          'inventory_executed_cycles':sum(x['cycles'] for x in simulations),
                          'inventory_compile_seconds':sum(x['seconds'] for x in compilations),
                          'inventory_simulation_seconds':sum(x['seconds'] for x in simulations),
                          'sum_recorded_screen_elapsed_seconds':sum(x['elapsed_seconds'] for x in attempts),
                          'model_calls':0,'api_tokens':0,'api_cost_usd':0,
                          'limits':'Includes all saved failed/revised candidate attempts. Frontends include lint/elaboration, not DUT simulations. Inventory cycles are reset/quiescence only. Unit fixture compilation/proofs are in test logs, not DUT pilot calls. Summed attempt durations are not end-to-end wall time; some jobs ran concurrently. No ordinary traffic, multistep reachability, or B/C trial executed.'},
            'attempts':attempts,'frontends':frontends,'inventory_compilations':compilations,'inventory_simulations':simulations}
    (BASE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ('status','final','accounting','current_artifact_hash_checks','versions')},indent=2))

if __name__=='__main__':audit()
