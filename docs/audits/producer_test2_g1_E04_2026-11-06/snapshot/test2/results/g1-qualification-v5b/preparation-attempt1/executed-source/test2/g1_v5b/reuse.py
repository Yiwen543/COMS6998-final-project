"""Exact immutable reuse of accepted E02/E03 artifacts;no new trial."""
from pathlib import Path
import hashlib,json
from observations import need,parse_rows,parse_vcd,bind_physical_vcd,selected_native_alarm
from e02_native_reuse import load_reuse as e02_reuse
from native_results import read_native,judge_native
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def metadata(root,reg):
    root=Path(root);m=json.loads((root/reg['reuse_manifest']).read_text());old=json.loads((root/'test2/configs/g1_qualification_registration_v4.json').read_text())
    for name,h in m['files'].items():need((root/name).is_file() and not (root/name).is_symlink() and sha(root/name)==h,'REUSE_HASH_DRIFT:'+name)
    for pair in m['unchanged_hardware_and_input_pairs']:need(sha(root/pair['new'])==sha(root/pair['old'])==pair['sha256'],'REUSE_SOURCE_DRIFT')
    need(reg['tools']==old['tools']==m['tool_pins'],'REUSE_TOOL_PINS')
    prefix=e02_reuse(root,old)
    report=json.loads((root/'test2/results/g1-qualification-v4/report.json').read_text())
    plan=json.loads((root/'test2/g1_v4/job-plan.json').read_text())['jobs'];byid={j['id']:j for j in plan}
    names=['compile-icarus-shared','compile-verilator-shared','QC00-icarus','QC00-verilator','compile-QC01','QC01-bmc','QC01-cover']
    for name in names:
        original=report['jobs'][name];folder=root/'test2/results/g1-qualification-v4/jobs'/name;receipt=json.loads((folder/'receipt.json').read_text())
        argv=[x.replace('{ROOT}',str(root)).replace('{OUT}',str(root/'test2/results/g1-qualification-v4')).replace('{JOB}',str(folder)) for x in byid[name]['argv']]
        need(original['status']=='RETURNED' and receipt['status']=='RETURNED' and original['argv']==receipt['argv']==argv,'REUSE_JOB_OR_ARGV')
        need(not receipt['timed_out'] and not receipt['mandatory_errors'],'REUSE_PROCESS_UNRESOLVED')
    return dict(prefix=prefix,E03_report=report,manifest=m)

def decode(root,reg,verified):
    root=Path(root);labels=json.loads((root/reg['controls']).read_text())['cases'];intents={x['id']:x for x in json.loads((root/reg['interpretation']).read_text())['cases']}
    jobs=dict(verified['prefix']['jobs']);physical={};alarms={};controls={}
    for name,old in verified['E03_report']['jobs'].items():
        if old['status']=='RETURNED':jobs[name]=dict(status='REUSED_FROM_E03',new_execution=False,original_job=old)
    for cid,version in [('QC00','v3'),('QC01','v4')]:
        for mode in ['bmc','cover']:
            folder=root/f'test2/results/g1-qualification-{version}/jobs/{cid}-{mode}';source=root/f'test2/g1_{version}/sources/{cid}_formal.sv'
            evidence=read_native(folder,source,mode);judge=judge_native(evidence,mode,intents[cid]);jobs[cid+'-'+mode].update(native_evidence=evidence,target_judgment=judge,new_execution=False)
            if mode=='bmc' and evidence['native_BMC_status']=='FAIL':alarms[cid]=selected_native_alarm(parse_vcd(folder/'trace.vcd'))
    for sim in ['icarus','verilator']:
        folder=root/'test2/results/g1-qualification-v4/jobs'/('QC00-'+sim)
        rows=parse_rows((folder/'stdout.log').read_text(),labels[0],sim);bind_physical_vcd(parse_vcd(folder/'trace.vcd'),rows,labels[0]);physical[('QC00',sim)]=rows
    controls['QC00']=dict(status='EXPECTED_CONTROL_OBSERVATIONS_MATCHED',evidence_origin='REUSED_E02_NATIVE_AND_E03_PHYSICAL',new_independent_trial=False,eligibility=labels[0]['eligibility'],completion128_credit=False,qualified_real_DUT_or_oracle=False)
    return dict(jobs=jobs,physical=physical,native_alarms=alarms,controls=controls)
