"""Hash-bound reuse of saved QC00 native prefix;never reuse rejected physical."""
from pathlib import Path
import hashlib,json
from observations import need


def digest(path):
    path=Path(path);need(path.is_file() and not path.is_symlink(),'REUSE_MISSING_FILE:'+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_reuse(root,reg):
    root=Path(root);m=json.loads((root/reg['native_reuse_manifest']).read_text())
    need(m['status']=='CONDITIONAL_NATIVE_PREFIX_REUSE_NOT_NEW_EXECUTION','REUSE_STATUS')
    for path,expected in m['files'].items():need(digest(root/path)==expected,'REUSE_HASH_DRIFT:'+path)
    for pair in m['unchanged_dependencies']:
        need(digest(root/pair['new'])==digest(root/pair['old'])==pair['sha256'],'NATIVE_DEPENDENCY_CHANGED:'+pair['new'])
    need(reg['profile']==m['profile'] and reg['native_depth']==m['native_depth']==8,'REUSE_PROFILE_DEPTH')
    need(reg['prior_reserved']==m['prior_reserved'],'REUSE_PRIOR_COST_NOT_INHERITED')
    for name,pin in m['tool_pins'].items():
        need(all(reg['tools'][name][key]==value for key,value in pin.items()),'REUSE_TOOL_PIN:'+name)
    report=json.loads((root/m['old_report']).read_text());pool=json.loads((root/m['old_pool']).read_text())
    need(pool['halted'] is True and pool['completed'] is True,'REUSE_OLD_POOL_NOT_CLOSED')
    need(report['execution_error']=='Unqualified:PHYSICAL_EXPECTED_MISMATCH:a','REJECTED_PHYSICAL_HISTORY_CHANGED')
    jobs={}
    for name in ['compile-QC00','QC00-bmc','QC00-cover']:
        actual=report['jobs'][name]
        need(actual['status']=='RETURNED' and actual['exit_code']==0 and actual['argv']==m['argv'][name],'REUSE_JOB_BINDING:'+name)
        if name!='compile-QC00':
            need(actual['native_status']=='PASS','REUSE_NATIVE_NOT_PASS')
            need(actual['argv'][actual['argv'].index('-t')+1]=='8','REUSE_DEPTH_NOT8')
        jobs[name]=dict(status='REUSED_FROM_E02',new_execution=False,original_job=actual)
    frontend=' '.join(m['argv']['compile-QC00'])
    need('common.sv' in frontend and 'QC00_formal.sv' in frontend and 'physical_tb.sv' not in frontend,'PHYSICAL_IN_NATIVE_CONE')
    return dict(status='REUSED_FROM_E02',jobs=jobs,manifest_sha256=digest(root/reg['native_reuse_manifest']),
        new_compile_jobs=0,new_native_jobs=0,new_physical_jobs=0,
        original_costs_already_inherited=True,rejected_QC00_physical_reused=False,
        full_QC_qualification=False,completion128_credit=False)
