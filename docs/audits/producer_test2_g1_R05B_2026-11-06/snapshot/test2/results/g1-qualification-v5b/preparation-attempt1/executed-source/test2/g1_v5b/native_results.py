"""Preserve raw native outcomes and judge only the separately registered targets."""
from pathlib import Path
import hashlib,json,re
from native_evidence import cover_evidence
from observations import need,parse_vcd,signal,Unqualified
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def binding(folder,source):
    folder,source=Path(folder),Path(source);receipt=json.loads((folder/'receipt.json').read_text())
    b={name+'_sha256':sha(folder/name) for name in ['receipt.json','stdout.log','stderr.log']}
    b.update(source_sha256=sha(source),source_log_path=str(source.resolve()),argv=receipt['argv'],**{'trace.vcd_sha256':sha(folder/'trace.vcd') if (folder/'trace.vcd').is_file() else None})
    return b

def _read_native(folder,source,mode):
    folder,source=Path(folder),Path(source)
    if mode=='cover':
        out=cover_evidence(folder,source,binding(folder,source))
        if out['activation']=='REACHED':
            vcd=parse_vcd(folder/'trace.vcd');step=out['raw_reached_steps'][0]
            final_state={tick:state for tick,state in vcd['samples']}[vcd['recorded_last_tick']]
            if vcd['recorded_last_tick']!=10*(step+1) or signal(vcd,final_state,'smt_step',32)!=format(step+1,'032b'):
                out.update(activation='UNKNOWN',evidence_complete=False);out['issues'].append('TRUNCATED_OR_UNSUPPORTED_TRACE_END')
        return out
    receipt=json.loads((folder/'receipt.json').read_text());text=(folder/'stdout.log').read_text()+'\n'+(folder/'stderr.log').read_text()
    statuses=re.findall(r'^##\s+\S+\s+Status:\s*(PASSED|FAILED)\s*$',text,re.M)
    out=dict(tool_status=statuses[0] if len(statuses)==1 else 'UNKNOWN',process_exit_code=receipt.get('exit_code'),assertion_observation='UNKNOWN',evidence_complete=False,qualification_credit=False,issues=[])
    bad=None
    if '-c' in receipt.get('argv',[]) or '-t' not in receipt.get('argv',[]) or receipt['argv'][receipt['argv'].index('-t')+1]!='8':bad='WRONG_BMC_MODE_OR_DEPTH'
    elif len(statuses)!=1:bad='MISSING_OR_MULTIPLE_TOOL_STATUS'
    elif receipt.get('status')!='RETURNED' or receipt.get('timed_out') is not False or receipt.get('mandatory_errors')!=[] or receipt.get('root_exit_knownness')!='KNOWN_FROM_CLEANUP_WAIT':bad='PROCESS_UNRESOLVED'
    elif receipt.get('exit_code')!=(0 if statuses[0]=='PASSED' else 1):bad='STATUS_EXIT_CONFLICT'
    elif any(receipt[stem+'_sha256']!=sha(folder/(stem+'.log')) for stem in ['stdout','stderr']):bad='LOG_HASH_DRIFT'
    else:
        lines=[line for line in text.splitlines() if 'Assert failed' in line]
        source_lines=source.read_text().splitlines();indices=[i+1 for i,line in enumerate(source_lines) if line.strip()=='assert(!active || ok);']
        if len(indices)!=1:bad='UNSUPPORTED_ASSERT_SOURCE'
        else:
            line=indices[0];path=re.escape(str(source.resolve()));desc=path+rf':{line}\.\d+-{line}\.\d+ \(\$assert\$'+path+rf':{line}\$\d+\)'
            pattern=r'^##\s+\S+\s+Assert failed in formal_top: '+desc+r'(?: \(step \d+\))?$'
            if any(re.fullmatch(pattern,x) is None for x in lines):bad='ASSERT_SOURCE_ID'
            elif statuses[0]=='PASSED' and lines:bad='PASSED_WITH_ASSERT_FAILURE'
            elif statuses[0]=='FAILED' and (not lines or not (folder/'trace.vcd').is_file()):bad='FAILED_WITHOUT_ASSERT_WITNESS'
            else:out.update(assertion_observation='FAILED' if lines else 'NO_FAILURE_REPORTED',evidence_complete=True,native_BMC_status='PASS' if statuses[0]=='PASSED' else 'FAIL')
    if bad:out['issues'].append(bad)
    return out

def judge_native(out,mode,intent):
    need(out.get('evidence_complete') is True,'NATIVE_EVIDENCE_UNKNOWN:'+','.join(out.get('issues',[])))
    if mode=='bmc':
        expected=intent['BMC_assertion_expected']
        need(expected=='DIAGNOSTIC_ONLY_ANY_RAW_STATUS' or out['native_BMC_status']==expected,'BMC_EXPECTATION_MISMATCH')
    else:
        need(intent['activation_expected']=='DIAGNOSTIC' or out['activation']==intent['activation_expected'],'ACTIVATION_EXPECTATION_MISMATCH')
        policy=intent['cover_assertion_policy']
        if policy=='FAILED_REQUIRED':need(out['assertion_observation']=='FAILED','NEGATIVE_COVER_ASSERTION_MISMATCH')
        if policy=='NO_FAILURE_ALLOWED':need(out['assertion_observation']=='NO_FAILURE_REPORTED','UNEXPECTED_COVER_ASSERTION_FAILURE')
    return dict(target='ASSERTION_BMC' if mode=='bmc' else 'ACTIVATION_COVER',matched_registered_target=True,raw_tool_status=out['tool_status'],raw_exit_code=out['process_exit_code'],overall_tool_PASS_claimed=out['tool_status']=='PASSED',qualification_credit=False)


def read_native(folder,source,mode):
    try:return _read_native(folder,source,mode)
    except (OSError,ValueError,KeyError,IndexError,Unqualified) as error:
        return dict(tool_status='UNKNOWN',process_exit_code=None,activation='UNKNOWN',assertion_observation='UNKNOWN',evidence_complete=False,qualification_credit=False,issues=[type(error).__name__+':'+str(error)])
