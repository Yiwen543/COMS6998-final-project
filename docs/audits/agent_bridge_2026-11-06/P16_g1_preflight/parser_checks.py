"""P16 parser checkpoint only. No runner, allocation or real jobs."""
from pathlib import Path
import copy,hashlib,json,re,shutil,subprocess,sys
from unittest.mock import patch
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
AUDIT=ROOT/'docs/audits/producer_test2_g1_R05_2026-11-06';SNAP=AUDIT/'snapshot'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,v):
    with Path(p).open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2)
assert sha(AUDIT/'snapshot-manifest.json')=='3671383dc106f18c463038ee82b1f222ad3d73f7275da4e58829c09bd1adb7e6'
manifest=read(AUDIT/'snapshot-manifest.json')
for rel,h in manifest['files'].items():assert sha(AUDIT/rel)==h
for rel,h in manifest['external_immutable_dependencies'].items():assert sha(ROOT/rel)==h
original_index=hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)).hexdigest()
code=OWN/'parser-source';code.mkdir(exist_ok=False)
for name in ['native_evidence.py','observations.py']:shutil.copyfile(SNAP/'test2/g1_v5'/name,code/name)
sys.path.insert(0,str(code));from native_evidence import cover_evidence
def forbidden(*a,**k):raise AssertionError('NO_REAL_PROCESS_SIGNAL_SLEEP')
rows=[]
cases=[('saved_QC00','QC00',None,'REACHED'),('saved_QC01','QC01',None,'REACHED'),('exit_conflict','QC01','exit','UNKNOWN'),('wrong_cover_identity','QC01','identity','UNKNOWN'),('missing_final_status','QC01','status','UNKNOWN'),('missing_cover_record','QC01','cover','UNKNOWN'),('missing_trace','QC01','trace','UNKNOWN'),('duplicate_cover','QC01','duplicate','UNKNOWN'),('missing_assert_explanation','QC01','assert','UNKNOWN'),('wrong_mode','QC01','mode','UNKNOWN')]
for name,qc,mutation,expected in cases:
    folder=OWN/name;folder.mkdir();inputs=folder/'inputs';inputs.mkdir()
    version='v3' if qc=='QC00' else 'v4';old=ROOT/f'test2/results/g1-qualification-{version}/jobs/{qc}-cover';source=ROOT/f'test2/g1_{version}/sources/{qc}_formal.sv'
    for filename in ['receipt.json','stdout.log','stderr.log','trace.vcd']:shutil.copyfile(old/filename,inputs/filename)
    shutil.copyfile(source,inputs/'source.sv')
    receipt=read(inputs/'receipt.json');argv=copy.deepcopy(receipt['argv']);text=(inputs/'stdout.log').read_text()
    if mutation=='exit':receipt['exit_code']=0
    if mutation=='identity':text=text.replace(qc+'_formal.sv','QC02_formal.sv')
    if mutation=='status':text='\n'.join(x for x in text.splitlines() if 'Status:' not in x)+'\n'
    if mutation=='cover':text='\n'.join(x for x in text.splitlines() if 'Reached cover statement' not in x)+'\n'
    if mutation=='trace':(inputs/'trace.vcd').unlink()
    if mutation=='duplicate':text+='\n'+next(x for x in text.splitlines() if 'Reached cover statement' in x)+'\n'
    if mutation=='assert':text='\n'.join(x for x in text.splitlines() if 'Assert failed' not in x)+'\n'
    if mutation=='mode':argv.remove('-c');receipt['argv']=argv
    # Freeze final-mutated bytes and rebind before validation; no post-run resealing.
    (inputs/'stdout.log').write_text(text)
    if mutation:
        receipt['stdout_sha256']=sha(inputs/'stdout.log');receipt['stderr_sha256']=sha(inputs/'stderr.log')
        (inputs/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    binding=dict(source_log_path=str(source),source_sha256=sha(inputs/'source.sv'),argv=argv,fixture_origin='ACTUAL_SAVED_BYTES' if mutation is None else 'SYNTHETIC_REBOUND_'+mutation)
    for filename in ['receipt.json','stdout.log','stderr.log','trace.vcd']:binding[filename+'_sha256']=sha(inputs/filename) if (inputs/filename).exists() else None
    write(inputs/'binding.json',binding)
    hashes={str(p.relative_to(inputs)):sha(p) for p in inputs.iterdir() if p.is_file()};write(folder/'inputs-before.json',hashes)
    with patch('subprocess.Popen',side_effect=forbidden),patch('subprocess.run',side_effect=forbidden),patch('os.killpg',side_effect=forbidden),patch('time.sleep',side_effect=forbidden):result=cover_evidence(inputs,inputs/'source.sv',binding)
    assert result['activation']==expected and result['evidence_complete']==(expected=='REACHED') and result['qualification_credit'] is False,(name,result)
    if name=='saved_QC01':assert result['tool_status']=='FAILED' and result['process_exit_code']==1 and result['assertion_observation']=='FAILED' and result['raw_reached_steps']==[2]
    if name=='saved_QC00':assert result['tool_status']=='PASSED' and result['process_exit_code']==0 and result['assertion_observation']=='NO_FAILURE_REPORTED'
    assert all(sha(inputs/rel)==h for rel,h in hashes.items())
    write(folder/'result.json',result);rows.append(dict(case=name,expected=expected,activation=result['activation'],inputs_manifest_sha256=sha(folder/'inputs-before.json'),result_sha256=sha(folder/'result.json')))
for rel,h in manifest['files'].items():assert sha(AUDIT/rel)==h
assert sha(code/'native_evidence.py')==sha(SNAP/'test2/g1_v5/native_evidence.py')
assert original_index==hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)).hexdigest()
write(OWN/'parser-checks.json',dict(status='PARSER_STAGE_CHECKS_PASS_NOT_EXECUTE_ACCEPTANCE',producer_manifest_sha256=sha(AUDIT/'snapshot-manifest.json'),producer_phase_sha256=sha(AUDIT/'phase.json'),sealed_members=len(manifest['files']),external_dependencies=len(manifest['external_immutable_dependencies']),parser_sha256=sha(code/'native_evidence.py'),source_parser_copy_unchanged=True,independent_probes=rows,index_unchanged=True,current_integration_not_reviewed=True,real_G1_jobs_API_tools=0))
print(json.dumps(dict(status='PARSER_ONLY_PASS_WITH_LIMITS',sealed_members=len(manifest['files']),independent_probes=len(rows),EXECUTE_accepted=False)))
