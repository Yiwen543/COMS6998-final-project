"""Evidence reader for one hash-bound G1 posedge wrapper with cover(active).

No tool invocation. A reached cover and a FAILED tool result can coexist.
This reader grants no qualification or assertion proof.
"""
from pathlib import Path
import hashlib,json,re
from observations import parse_vcd,signal,Unqualified

class EvidenceUnknown(ValueError): pass

def require(ok,reason):
    if not ok:raise EvidenceUnknown(reason)

def digest(path):
    path=Path(path)
    require(path.is_file() and not path.is_symlink(),'MISSING_OR_SYMLINK:'+path.name)
    return hashlib.sha256(path.read_bytes()).hexdigest()

def cover_evidence(folder,source,binding):
    """Keep raw status/exit and activation separate; fail closed on missing evidence.

    binding pins exact saved receipt/log/trace/source bytes and original argv/path.
    UNREACHED means explicitly reported in this finite invocation,not a proof of
    unreachability. NO_FAILURE_REPORTED never means assertions have been proved.
    """
    folder,source=Path(folder),Path(source)
    out=dict(tool_status='UNKNOWN',process_exit_code=None,activation='UNKNOWN',
        assertion_observation='UNKNOWN',raw_reached_steps=[],raw_unreached_count=0,
        evidence_complete=False,qualification_credit=False,issues=[])
    try:
        for name in ['receipt.json','stdout.log','stderr.log']:
            require(digest(folder/name)==binding[name+'_sha256'],'HASH_DRIFT:'+name)
        require(digest(source)==binding['source_sha256'],'SOURCE_HASH_DRIFT')
        receipt=json.loads((folder/'receipt.json').read_text())
        out['process_exit_code']=receipt.get('exit_code')
        require(receipt.get('kind')=='native' and receipt.get('status')=='RETURNED','RECEIPT_NOT_RETURNED_NATIVE')
        require(receipt.get('timed_out') is False and receipt.get('mandatory_errors')==[],'TIMEOUT_OR_PROCESS_ERROR')
        require(receipt.get('root_exit_knownness')=='KNOWN_FROM_CLEANUP_WAIT','UNKNOWN_ROOT_EXIT')
        argv=receipt['argv'];require(argv==binding['argv'],'ARGV_DRIFT')
        require(argv.count('-c')==1 and argv[argv.index('-t')+1]=='8','COVER_MODE_OR_DEPTH')
        for stem in ['stdout','stderr']:
            require(receipt[stem+'_sha256']==binding[stem+'.log_sha256'],'RECEIPT_LOG_HASH_DRIFT')
        text=(folder/'stdout.log').read_text()+'\n'+(folder/'stderr.log').read_text()
        lines=[re.sub(r'^##\s+\S+\s+','',line).strip() for line in text.splitlines()]
        statuses=[line[8:] for line in lines if line.startswith('Status: ')]
        require(len(statuses)==1 and statuses[0] in ['PASSED','FAILED'],'MISSING_OR_MULTIPLE_TOOL_STATUS')
        out['tool_status']=statuses[0]
        require(type(receipt['exit_code']) is int and receipt['exit_code']==(0 if statuses[0]=='PASSED' else 1),'STATUS_EXIT_CONFLICT')
        code=source.read_text();code_lines=code.splitlines()
        covers=[i+1 for i,line in enumerate(code_lines) if line.strip()=='cover(active);']
        asserts=[i+1 for i,line in enumerate(code_lines) if line.strip()=='assert(!active || ok);']
        require(len(covers)==len(asserts)==1 and len(re.findall(r'\bcover\s*\(',code))==1 and len(re.findall(r'\bassert\s*\(',code))==1 and 'always @(posedge clk)' in code,'UNSUPPORTED_WRAPPER')
        logged=re.escape(binding['source_log_path'])
        def desc(kind,line):
            return logged+rf':{line}\.\d+-{line}\.\d+ \(\${kind}\$'+logged+rf':{line}\$\d+\)'
        reached=[line for line in lines if line.startswith('Reached cover statement')]
        unreached=[line for line in lines if line.startswith('Unreached cover statement')]
        assert_lines=[line for line in lines if line.startswith('Assert failed')]
        reach_pattern=r'Reached cover statement in step (\d+) at formal_top: '+desc('cover',covers[0])
        unreached_pattern=r'Unreached cover statement at formal_top: '+desc('cover',covers[0])
        parsed=[re.fullmatch(reach_pattern,line) for line in reached]
        require(all(parsed) and all(re.fullmatch(unreached_pattern,line) for line in unreached),'WRONG_COVER_SOURCE_ID')
        out['raw_reached_steps']=[int(m[1]) for m in parsed]
        out['raw_unreached_count']=len(unreached)
        assert_pattern=r'Assert failed in formal_top: '+desc('assert',asserts[0])+r' \(step (\d+)\)'
        failures=[re.fullmatch(assert_pattern,line) for line in assert_lines]
        require(all(failures),'WRONG_ASSERT_SOURCE_ID')
        out['assertion_observation']='FAILED' if failures else 'NO_FAILURE_REPORTED'
        require(not(failures and statuses[0]=='PASSED'),'ASSERT_FAILURE_WITH_TOOL_PASSED')
        require((len(reached),len(unreached)) in [(1,0),(0,1)],'MISSING_DUPLICATE_OR_CONTRADICTORY_COVER_RECORD')
        if reached:
            require(statuses[0]=='PASSED' or bool(failures),'FAILED_REACHED_WITHOUT_ASSERT_FAILURE_EXPLANATION')
            require(binding.get('trace.vcd_sha256') is not None,'MISSING_REACHED_TRACE_BINDING')
            require(digest(folder/'trace.vcd')==binding['trace.vcd_sha256'],'TRACE_HASH_DRIFT')
            trace_path=argv[argv.index('--dump-vcd')+1]
            require([line for line in lines if line.startswith('Writing trace to VCD file: ')]==['Writing trace to VCD file: '+trace_path],'TRACE_LOG_PATH_CONFLICT')
            vcd=parse_vcd(folder/'trace.vcd');require(vcd['scale']==('1','ns'),'UNSUPPORTED_NATIVE_VCD_SCALE')
            step=out['raw_reached_steps'][0];require(0<=step<8,'REACHED_OUTSIDE_REGISTERED_DEPTH')
            samples=[]
            for tick,state in sorted({tick:state for tick,state in vcd['samples']}.items()):
                bits=signal(vcd,state,'smt_step',32)
                if set(bits)<=set('01') and int(bits,2)==step:
                    samples.append(signal(vcd,state,'formal_top.sampled_active',1))
            require(bool(samples) and all(x=='1' for x in samples),'REACHED_TRACE_ACTIVATION_UNKNOWN_OR_CONFLICT')
            out.update(activation='REACHED',trace_registered_active_at_reported_step=samples)
        else:
            require(statuses[0]=='FAILED' and not failures,'UNREACHED_WITH_CONFLICTING_STATUS_OR_ASSERT_FAILURE')
            require(binding.get('trace.vcd_sha256') is None and not (folder/'trace.vcd').exists(),'UNREACHED_HAS_UNEXPLAINED_TRACE')
            out['activation']='UNREACHED'
        out.update(evidence_complete=True,finite_depth=8)
    except (EvidenceUnknown,Unqualified,OSError,KeyError,ValueError,IndexError) as error:
        out['activation']='UNKNOWN';out['issues'].append(type(error).__name__+':'+str(error))
    return out
