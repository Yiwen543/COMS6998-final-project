"""Versioned trace_done=0 safety projection physical bridge; independent oracle unchanged."""
import json
from pathlib import Path
import time
from common import ROOT,dump,run,sha
from controller_monitor_live import TASK,PINS,ROW_INPUTS,OUTPUTS
from controller_done_runtime import replay
from controller_prepare import normalize
from controller_reference_evaluate import module


def decode(path,slot):
    scopes=[];ids={};outputs={};checks={};step_id=None;header=True;values={};touched=set();frames={};partial={}
    def flush():
        if step_id in values:
            step=values[step_id]
            if step<0:raise ValueError('Unknown SMT step')
            if set(ids.values())<=touched:frames[step]=dict(values)
            else:partial[step]=set(ids.values())&touched
    for raw in Path(path).read_text().splitlines():
        line=raw.strip();w=line.split()
        if header:
            if line.startswith('$scope '):scopes.append(w[2])
            elif line.startswith('$upscope'):scopes.pop()
            elif line.startswith('$var '):
                if w[4]=='smt_step' and not scopes:step_id=w[3]
                if scopes==['formal_top'] and w[4] in ('active','ok'):
                    if int(w[2])<=slot:raise ValueError('Selected monitor bit absent from VCD')
                    checks[w[4]]=w[3]
                if scopes==['formal_top'] and w[4] in set(ROW_INPUTS)|set(OUTPUTS):
                    if int(w[2])!=PINS[w[4]]:raise ValueError('Formal public pin width changed')
                    target=ids if w[4] in ROW_INPUTS else outputs
                    if w[4] in target:raise ValueError('Duplicate public pin')
                    target[w[4]]=w[3]
            elif line.startswith('$enddefinitions'):header=False
        elif line.startswith('#'):flush()
        elif line.startswith('b'):
            bits,ident=line[1:].split();value=-1 if any(c in bits.lower() for c in 'xz') else int(bits,2)
            if ident==step_id and values.get(step_id)!=value:touched.clear()
            values[ident]=value;touched.add(ident)
        elif line and line[0] in '01xz':
            ident=line[1:];values[ident]=-1 if line[0] in 'xz' else int(line[0]);touched.add(ident)
    flush()
    if set(ids)!=set(ROW_INPUTS) or step_id is None:raise ValueError('Missing formal input pins')
    if len(frames)<2 or sorted(frames)!=list(range(len(frames))):raise ValueError('Incomplete reachable witness')
    if any(s not in frames and (s!=len(frames) or fields) for s,fields in partial.items()):raise ValueError('Truncated input frame')
    inputs=[{k:frames[i][v] for k,v in ids.items()} for i in range(len(frames))]
    if any(v<0 or v>=2**PINS[k] for x in inputs for k,v in x.items()):raise ValueError('Unknown/out-of-range input')
    sampled=[{k:frames[i].get(v,-1) for k,v in outputs.items()} for i in range(len(frames))]
    if set(checks)!=set(('active','ok')):raise ValueError('Selected formal monitor observations absent')
    bad=[i for i in range(1,len(frames)) if all(frames[i].get(v,-1)>=0 for v in checks.values()) and
         (frames[i][checks['active']]>>slot)&1 and not (frames[i][checks['ok']]>>slot)&1]
    if not bad:raise ValueError('No definite selected-slot alarm state in VCD')
    return inputs,sampled,bad[0]


def driver():
    decl='\n'.join('reg '+(f'[{w-1}:0] ' if w>1 else '')+n+'=0;' for n,w in PINS.items() if n=='clk' or n in ROW_INPUTS)
    decl+='\n'+'\n'.join('wire '+(f'[{PINS[n]-1}:0] ' if PINS[n]>1 else '')+n+';' for n in OUTPUTS)
    return '''`timescale 1ns/1ps
module literal_replay;
'''+decl+'''
frame_task dut(.*);
string path;integer fd,n,cycle=0;
integer '''+','.join('v_'+n for n in ROW_INPUTS)+''';
initial begin
 if(!$value$plusargs("INPUTS=%s",path)) $fatal(1,"Missing inputs");
 fd=$fopen(path,"r");if(!fd) $fatal(1,"Missing file");
 while(!$feof(fd)) begin
  n=$fscanf(fd,"'''+ ' '.join(['%d']*len(ROW_INPUTS))+'\\n",'+','.join('v_'+n for n in ROW_INPUTS)+''');
  if(n==6) begin
'''+ '\n'.join(n+'=v_'+n+';' for n in ROW_INPUTS)+'''
   #4;$display("PRE %0d '''+' '.join(['%0d']*(len(ROW_INPUTS)+len(OUTPUTS)))+'",cycle,'+','.join(ROW_INPUTS+OUTPUTS)+''');
   #1;clk=1;#2;
   $display("POST %0d '''+' '.join(['%0d']*len(OUTPUTS))+'",cycle,'+','.join(OUTPUTS)+''');
   #3;clk=0;cycle=cycle+1;
  end else if(n!=-1) $fatal(1,"Malformed inputs");
 end
 $display("LITERAL_COMPLETE %0d",cycle);$finish;
end
endmodule
'''


def build(source,sim,out,timeout=60):
    out.mkdir(parents=True,exist_ok=False);(out/'driver.sv').write_text(driver())
    binary=out/('obj/Vliteral_replay' if sim=='verilator' else 'literal.vvp')
    sources=[source,TASK/'public/rtl/axis_fifo.v',TASK/'public/rtl/axis_frame_length_adjust_fifo.v',TASK/'public/task_top_v3.sv',out/'driver.sv']
    argv=(['verilator','--binary','--timing','-Wno-fatal','--top-module','literal_replay','--Mdir',binary.parent,'-j','2'] if sim=='verilator' else ['iverilog','-g2012','-s','literal_replay','-o',binary])
    r=run(argv+sources,out/'compile.log',min(60,timeout));dump(out/'compile.json',r)
    if r['status']!='complete':raise ValueError('Literal replay compilation failed: '+sim)
    return binary


def physical(binary,sim,inputs,out,timeout=15):
    out.mkdir(parents=True,exist_ok=False)
    (out/'inputs.txt').write_text(''.join(' '.join(str(x[k]) for k in ROW_INPUTS)+'\n' for x in inputs))
    cmd=([binary] if sim=='verilator' else ['vvp',binary])+['+INPUTS='+str(out/'inputs.txt')]
    r=run(cmd,out/'simulation.log',min(15,timeout));text=(out/'simulation.log').read_text();rows={}
    if r['status']!='complete' or f'LITERAL_COMPLETE {len(inputs)}' not in text:raise ValueError('Incomplete physical replay')
    def number(v):return -1 if any(c in v.lower() for c in 'xz') else int(v)
    for line in text.splitlines():
        w=line.split()
        if not w or w[0] not in ('PRE','POST'):continue
        phase=w[0].lower();i=int(w[1]);vals=[number(x) for x in w[2:]];row=rows.setdefault(i,dict(cycle=i))
        if phase=='pre':row['inputs']=dict(zip(ROW_INPUTS,vals[:6]));vals=vals[6:]
        if len(vals)!=len(OUTPUTS):raise ValueError('Physical pin count changed')
        row[phase]=dict(zip(OUTPUTS,vals))
    if sorted(rows)!=list(range(len(inputs))):raise ValueError('Missing physical row')
    rows=[rows[i] for i in range(len(inputs))]
    if any(row['inputs']!=inp for row,inp in zip(rows,inputs)):raise ValueError('Literal formal inputs changed in transport')
    dump(out/'rows.json',rows);dump(out/'execution.json',dict(r,cycles=len(rows)))
    return rows


def legal_inputs(inputs,rows):
    if inputs[0]['rst']!=1:raise ValueError('No initial reset')
    count=0
    for i,x in enumerate(inputs):
        if x['rst']:
            if x['s_valid']:raise ValueError('Source offered during reset')
            count=0;continue
        if i and not inputs[i-1]['rst'] and inputs[i-1]['s_valid'] and rows[i-1]['pre']['s_ready']==0:
            if any(x[k]!=inputs[i-1][k] for k in ('s_valid','s_data','s_last')):raise ValueError('Blocked source offer changed')
        if x['s_valid'] and rows[i]['pre']['s_ready']==1:
            count+=1
            if count>12 or count==12 and not x['s_last']:raise ValueError('Frame length assumption violated')
            if x['s_last']:count=0


def remaining(deadline,cap):
    seconds=cap if deadline is None else min(cap,deadline-time.monotonic())
    if seconds<=0:raise TimeoutError('Witness total budget exhausted')
    return seconds


def adjudicate(job,candidate,source,slot,out,cache,deadline=None):
    out.mkdir(parents=True,exist_ok=False)
    result=dict(status='unresolved',classification='Physical witness not yet validated',API_calls=0,trace_done=0,finite_completion_proved=False)
    try:
        paths=list((job/'work').glob('engine_*/trace.vcd'))
        if len(paths)!=1:raise ValueError('Expected exactly one reachable BMC witness')
        inputs,sampled,alarm_state=decode(paths[0],slot)
        # Native sampled assertions can be reported one step after active/ok fail.
        # Use directly observed monitor pins, never infer failure from terminal size.
        inputs=inputs[:alarm_state+1];sampled=sampled[:alarm_state+1]
        dump(out/'formal-inputs.json',inputs)
        both={}
        for sim in ('iverilog','verilator'):
            key=cache/sha(source)/sim
            binary=key/('obj/Vliteral_replay' if sim=='verilator' else 'literal.vvp')
            if not binary.exists():binary=build(source,sim,key,remaining(deadline,60))
            both[sim]=physical(binary,sim,inputs,out/sim,remaining(deadline,15))
            legal_inputs(inputs,both[sim])
        if normalize(both['iverilog'])!=normalize(both['verilator']):raise ValueError('Physical simulators disagree on meaningful pins')
        rows=both['iverilog']
        for i,frame in enumerate(sampled):
            if i==0:continue
            for k,v in frame.items():
                meaningful=k in ('s_ready','m_valid','h_valid') or rows[i]['pre']['h_valid' if k.startswith('h_') else 'm_valid']==1
                if meaningful and (v<0 or rows[i]['pre'][k]!=v):raise ValueError('Retained SMT output differs from physical replay')
        r=replay(candidate,rows,out/'candidate-replay',cache/'monitor-rows',trace_done=False,timeout=remaining(deadline,15))
        if not r['complete'] or [alarm_state,'pre'] not in r['properties'][slot]['failures']:
            raise ValueError('Formal selected-slot alarm not reproduced at observed failing physical pre sample')
        checker=module(TASK/'reference/frozen-v2/checker.py','physical_witness_claude_reference')
        # The last formal state is a failing pre sample, not an extra accepted edge.
        # Reference receives physical observations only through the previous edge.
        prefix=rows[:alarm_state];oracle=checker.check_rows(prefix,require_drained=False,min_tail=32)
        dump(out/'reference-prefix-rows.json',prefix);dump(out/'reference.json',oracle)
        classification={'PASS':'reference_PASS_on_prefix_through_post_previous_cycle','FAIL':'reference_FAIL_on_prefix_unattributed_to_selected_alarm','UNRESOLVED':'reference_UNRESOLVED_on_prefix','INVALID_INPUT':'invalid_physical_interface'}[oracle['verdict']]
        result.update(status='physically_reproduced_prefix_checked' if oracle['verdict'] in ('PASS','FAIL') else 'unresolved',classification=classification,reference_verdict=oracle['verdict'],
                      selected_alarm=dict(cycle=alarm_state,phase='pre',slot=slot,category='UNATTRIBUTED'),
                      reference_failures=oracle['failures'],reference_unknown=oracle['unknown'],
                      reference_last_sample=dict(cycle=alarm_state-1,phase='post'),reference_confirmed_selected_alarm=False,
                      candidate_false_alarm_claim=False,DUT_violation_on_reference_prefix=oracle['verdict']=='FAIL',
                      selected_alarm_reference_agreement='UNRESOLVED: checker evaluated only earlier prefix; no same-sample/category attribution',
                      physical_simulators_agree=True,formal_alarm_reproduced=True,formal_states=len(inputs),reference_rows=len(prefix),
                      observed_alarm_state=alarm_state,
                      physical_cycles=2*len(inputs),candidate_monitor_cycles=r['cycles'],witness_sha256=sha(paths[0]),retained_outputs_checked=sorted(sampled[0]))
    except Exception as error:result.update(error_type=type(error).__name__,detail=str(error))
    dump(out/'result.json',result);return result
