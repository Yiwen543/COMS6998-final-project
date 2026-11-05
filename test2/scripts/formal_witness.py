"""Strict Yosys-SMTBMC public-pin VCD decoder for this fixed FIFO harness only."""
import json
from pathlib import Path
import shutil
import sys
from common import BASE,dump,run,sha

PORTS={'i_reset':1,'i_wr':1,'i_rd':1,'i_data':8,'o_fill':5,'o_full':1,'o_empty':1,'o_data':8}

def decode(path):
    scopes=[];identifiers={};step_id=None;header=True;values={};snapshots={};touched=set();partial={}
    def flush():
        if step_id in values:
            step=values[step_id]
            if step<0:raise ValueError('Unknown SMT step')
            required=set(identifiers.values())
            if required<=touched:snapshots[step]=dict(values)
            else:partial[step]=required & touched
    for raw in path.read_text().splitlines():
        line=raw.strip()
        if header:
            words=line.split()
            if line.startswith('$scope '):scopes.append(words[2])
            elif line.startswith('$upscope'):scopes.pop()
            elif line.startswith('$var '):
                name=words[4]
                if name=='smt_step' and not scopes:step_id=words[3]
                if scopes==['formal_top'] and name in PORTS:
                    if int(words[2])!=PORTS[name] or name in identifiers:raise ValueError('VCD port layout changed')
                    identifiers[name]=words[3]
            elif line.startswith('$enddefinitions'):header=False
        elif line.startswith('#'):flush()
        elif line.startswith('b'):
            bits,ident=line[1:].split()
            if ident==step_id and values.get(step_id)!=int(bits,2):touched.clear()
            values[ident]=-1 if any(x in bits.lower() for x in 'xz') else int(bits,2)
            touched.add(ident)
        elif line and line[0] in '01xz' and not line.startswith('$'):
            values[line[1:]]=-1 if line[0] in 'xz' else int(line[0])
    flush()
    if set(identifiers)!=set(PORTS) or step_id is None:raise ValueError('Required formal public pins absent')
    steps=sorted(snapshots)
    if len(steps)<2 or steps!=list(range(len(steps))):raise ValueError('Not a complete reachable BMC witness')
    # SMTBMC emits a terminal smt_step/clock marker without another port sample.
    # Do not invent a post state by carrying prior values into that marker.
    for step,fields in partial.items():
        if step not in snapshots and (step!=len(steps) or fields):
            raise ValueError('Truncated/incomplete formal port frame')
    pins=[{k:snapshots[i][v] for k,v in identifiers.items()} for i in steps]
    rows=[]
    for i in range(len(pins)-1):
        a,b=pins[i:i+2]
        action={k:a['i_'+k] for k in ('reset','wr','rd','data')}
        if any(v<0 for v in action.values()) or action['reset'] and (action['wr'] or action['rd']):
            raise ValueError('Witness does not satisfy frozen input assumptions')
        rows.append({'cycle':i,'action':action,
            'pre':{k:a['o_'+k] for k in ('fill','full','empty','data')},
            'post':{k:b['o_'+k] for k in ('fill','full','empty','data')}})
    if rows[0]['action']['reset']!=1:raise ValueError('Witness missing initial reset')
    return rows

def adjudicate(job_dir,reference_dir):
    out=job_dir/'witness-review';out.mkdir(exist_ok=False)
    paths=sorted((job_dir/'work').glob('engine_*/trace.vcd'))
    result={'status':'unresolved','classification':'no complete reachable trace.vcd', 'reference_evaluations':0}
    try:
        if len(paths)!=1:raise ValueError('Expected one reachable SMT witness; unsupported layout retained')
        shutil.copyfile(paths[0],out/'trace.vcd')
        rows=decode(out/'trace.vcd');dump(out/'inputs.json',{'formal_witness':rows})
        command=[sys.executable,'-I',BASE/'scripts/evaluate_reference.py','--worker','--candidate',reference_dir,
                 '--inputs',out/'inputs.json','--output',out/'oracle.json']
        info=run(command,out/'oracle.log',60);result['reference_evaluations']=1
        if info['status']!='complete':raise ValueError('Independent witness oracle did not complete')
        oracle=json.loads((out/'oracle.json').read_text())['cases']['formal_witness']
        classification={'PASS':'candidate_false_alarm_on_this_legal_formal_trace',
                        'FAIL':'reference_confirmed_DUT_violation_on_this_formal_trace',
                        'UNRESOLVED':'unresolved_reference_observations',
                        'INVALID_INPUT':'invalid_witness_interface'}.get(oracle['verdict'],'infrastructure_error')
        result.update(status='adjudicated' if oracle['verdict'] in ('PASS','FAIL') else 'unresolved',
                      classification=classification,oracle_verdict=oracle['verdict'],
                      rows=len(rows),reference_seconds=info['seconds'],witness_sha256=sha(out/'trace.vcd'))
    except Exception as e:result.update(error_type=type(e).__name__,detail=str(e))
    dump(out/'result.json',result);return result
