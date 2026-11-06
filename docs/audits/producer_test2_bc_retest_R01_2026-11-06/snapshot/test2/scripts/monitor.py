"""Restricted SV candidate ABI, detached replay, fixed formal harness; no oracle."""
import json
import re
from pathlib import Path
from common import BASE, dump, run, sha

HEADER = '''module candidate_monitor(
input wire i_clk, i_reset, i_wr, i_rd,
input wire [7:0] i_data, o_data,
input wire [4:0] o_fill,
input wire o_full, o_empty,
output wire [5:0] active, ok);
'''
INPUTS = {'i_clk':1,'i_reset':1,'i_wr':1,'i_rd':1,'i_data':8,
          'o_data':8,'o_fill':5,'o_full':1,'o_empty':1}
SCHEMA = {'type':'object','additionalProperties':False,'required':['body','properties'],
          'properties':{'body':{'type':'string'},'properties':{'type':'array','items':{
              'type':'object','additionalProperties':False,'required':['id','description'],
              'properties':{'id':{'type':'string'},'description':{'type':'string'}}}}}}

def validate(candidate):
    if not isinstance(candidate,dict) or set(candidate)!={'body','properties'}:
        raise ValueError('Expected body and properties only')
    body=candidate['body']
    if not isinstance(body,str) or len(body.encode())>16000:
        raise ValueError('Body exceeds byte limit')
    properties=candidate['properties']
    if not isinstance(properties,list) or len(properties)!=6:
        raise ValueError('Exactly six property slots required')
    for i,p in enumerate(properties):
        if not isinstance(p,dict) or set(p)!={'id','description'} or p['id']!=f'P{i}' or not isinstance(p['description'],str) or not 1<=len(p['description'])<=400:
            raise ValueError('Property ID/description invalid')
    # Remove comments for lexical checks only, never execute preprocessing.
    code=re.sub(r'/\*.*?\*/|//[^\n]*',' ',body,flags=re.S)
    if any(c in code for c in ('`','$','#','"','.', '\\')):
        raise ValueError('System call, hierarchy, preprocessor, delay or escaped identifier')
    banned=r'\b(module|endmodule|interface|program|package|bind|import|export|force|release|assert|assume|cover|property|sequence|task|function|fork|join|wait|forever|while|repeat|negedge|disable|specify|primitive|inout|input|output|ref)\b'
    if re.search(banned,code): raise ValueError('Unsupported or boundary-changing construct')
    # All explicit event controls must be the one clock or combinational.
    stripped=re.sub(r'@\s*(?:\(\s*posedge\s+i_clk\s*\)|\(\s*\*\s*\)|\*)','',code)
    if '@' in stripped: raise ValueError('Unsupported event control')
    if re.search(r'\balways_latch\b',code): raise ValueError('Latches unsupported')
    return HEADER+body+'\nendmodule\n'

def compile_monitor(candidate,out):
    out=Path(out); out.mkdir(parents=True,exist_ok=False)
    source=validate(candidate)
    (out/'candidate.sv').write_text(source); dump(out/'candidate.json',candidate)
    cmd=f'read_verilog -sv {out/"candidate.sv"}; hierarchy -check -top candidate_monitor; proc; opt_clean; check -assert; write_json {out/"netlist.json"}'
    info=run(['yosys','-Q','-T','-p',cmd],out/'yosys.log',60)
    dump(out/'compile.json',info)
    if info['status']!='complete':
        dump(out/'compile.json',info); return info
    module=json.loads((out/'netlist.json').read_text())['modules']['candidate_monitor']
    seen=set()
    for name,width in INPUTS.items():
        p=module['ports'][name]
        if p['direction']!='input' or len(p['bits'])!=width or any(type(x)!=int or x in seen for x in p['bits']):
            raise ValueError('Input port overwritten or aliased')
        seen.update(p['bits'])
    clk=module['ports']['i_clk']['bits']
    state=0
    for cell in module['cells'].values():
        if not cell['type'].startswith('$'): raise ValueError('Untrusted module instance')
        if any(tag in cell['type'] for tag in ('assume','assert','cover','latch','anyconst','anyseq')):
            raise ValueError('Untrusted formal primitive or latch')
        for port,direction in cell['port_directions'].items():
            if direction=='output' and any(bit in seen for bit in cell['connections'][port]):
                raise ValueError('Candidate drives an input')
        if 'CLK' in cell['connections'] and cell['type'].startswith(('$dff','$sdff','$adff')):
            if cell['connections']['CLK']!=clk or int(cell['parameters']['CLK_POLARITY'],2)!=1:
                raise ValueError('Noncanonical observer clock')
            state+=len(cell['connections']['Q'])
    for memory in module.get('memories',{}).values(): state+=memory['width']*memory['size']
    if state>8192: raise ValueError('Observer state exceeds cap')
    info.update(state_bits=state,source_sha256=sha(out/'candidate.sv'),status='complete')
    dump(out/'compile.json',info)
    return info

REPLAY = '''`timescale 1ns/1ps
module replay;
reg i_clk=0;
always #5 i_clk=~i_clk;
reg i_reset=0,i_wr=0,i_rd=0,o_full=0,o_empty=1;
reg [7:0] i_data=0,o_data=0;
reg [4:0] o_fill=0;
wire [5:0] active,ok;
candidate_monitor monitor(.*);
string path;
integer fd,n,cycle,r,w,d,data,pf,pfull,pe,pdata,qf,qfull,qe,qdata;
initial begin
  if (!$value$plusargs("ROWS=%s",path)) $fatal(1,"Missing rows");
  fd=$fopen(path,"r");
  if(fd==0) $fatal(1,"Missing rows file");
  while (!$feof(fd)) begin
    n=$fscanf(fd,"%h %h %h %h %h %h %h %h %h %h %h %h %h\\n",
      cycle,r,w,d,data,pf,pfull,pe,pdata,qf,qfull,qe,qdata);
    if(n==13) begin
      @(negedge i_clk);
      i_reset=r[0];i_wr=w[0];i_rd=d[0];i_data=data[7:0];
      o_fill=pf[4:0];o_full=pfull[0];o_empty=pe[0];o_data=pdata[7:0];
      #1;
      if(cycle>0) $display("MON %0d pre %06b %06b",cycle,active,ok);
      @(posedge i_clk);
      #1;o_fill=qf[4:0];o_full=qfull[0];o_empty=qe[0];o_data=qdata[7:0];
      #1;$display("MON %0d post %06b %06b",cycle,active,ok);
    end else if(n!=-1) $fatal(1,"Malformed rows");
  end
  $fclose(fd);$display("REPLAY_COMPLETE");$finish;
end
endmodule
'''

def build_replay(candidate_dir):
    d=Path(candidate_dir); (d/'replay.sv').write_text(REPLAY)
    result=run(['iverilog','-g2012','-s','replay','-o',d/'replay.vvp',d/'candidate.sv',d/'replay.sv'],d/'iverilog.log',60)
    dump(d/'iverilog.json',result)
    return result

def replay(candidate_dir,trace,out):
    d=Path(candidate_dir); out=Path(out); out.mkdir(parents=True,exist_ok=False)
    lines=[]
    for r in trace:
        vals=[r['cycle']]+[r['action'][k] for k in ('reset','wr','rd','data')]
        vals += [r[p][k] for p in ('pre','post') for k in ('fill','full','empty','data')]
        lines.append(' '.join('x' if v==-1 else f'{v:x}' for v in vals))
    (out/'rows.hex').write_text('\n'.join(lines)+'\n')
    info=run(['vvp',d/'replay.vvp',f'+ROWS={out/"rows.hex"}'],out/'replay.log',15)
    log=(out/'replay.log').read_text(); observations=[]
    for line in log.splitlines():
        if not line.startswith('MON '): continue
        _,cycle,phase,active,ok=line.split()
        if not re.fullmatch('[01xz]{6}',active+'' ) or not re.fullmatch('[01xz]{6}',ok):
            raise ValueError('Malformed candidate sample')
        observations.append({'cycle':int(cycle),'phase':phase,'active':active,'ok':ok})
    expected=[(r['cycle'],p) for r in trace for p in ('pre','post') if r['cycle'] or p=='post']
    complete=info['status']=='complete' and 'REPLAY_COMPLETE' in log and [(r['cycle'],r['phase']) for r in observations]==expected
    stats=[]
    for slot in range(6):
        checks=0; failures=[]; unknown=[]
        for r in observations:
            a,k=r['active'][5-slot],r['ok'][5-slot]
            if a not in '01' or (a=='1' and k not in '01'): unknown.append([r['cycle'],r['phase']])
            elif a=='1':
                checks+=1
                if k=='0': failures.append([r['cycle'],r['phase']])
        stats.append({'id':f'P{slot}','checks':checks,'failures':failures,'unknown':unknown,'vacuous_on_trace':checks==0})
    result={'complete':complete,'properties':stats,'samples':len(observations),
            'cycles':sum(r['phase']=='post' for r in observations),'attempted_cycles':len(trace),'execution':info}
    dump(out/'samples.json',observations);dump(out/'result.json',result)
    return result

def formal_harness():
    # Same observer body, fixed legal inputs. No upstream DUT FORMAL assertions.
    return '''module formal_top(input wire i_clk);
(* anyseq *) reg i_reset, i_wr, i_rd;
(* anyseq *) reg [7:0] i_data;
wire [7:0] o_data; wire [4:0] o_fill; wire o_full,o_empty;
wire [5:0] active,ok;
sfifo #(.BW(8),.LGFLEN(4),.OPT_ASYNC_READ(1),.OPT_WRITE_ON_FULL(0),.OPT_READ_ON_EMPTY(0)) dut(.*);
candidate_monitor monitor(.*);
reg initialized=0;
always @(posedge i_clk) begin
  if(!initialized) assume(i_reset);
  assume(!i_reset || (!i_wr && !i_rd));
  initialized<=1;
  if(initialized) begin
    assert((active & ~ok)==0);
    cover(active[0]);cover(active[1]);cover(active[2]);
    cover(active[3]);cover(active[4]);cover(active[5]);
  end
end
endmodule
'''

def run_formal(candidate_dir,source,out,mode):
    if mode not in ('bmc','prove','cover'): raise ValueError('Formal mode')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    (out/'harness.sv').write_text(formal_harness())
    # Exact text, no caller-supplied assumptions; local file aliases are portable.
    config=f'''[options]
mode {mode}
depth 48
timeout 60
[engines]
smtbmc z3
[script]
read -formal -sv dut.v candidate.sv harness.sv
prep -top formal_top
[files]
dut.v {source}
candidate.sv {Path(candidate_dir)/'candidate.sv'}
harness.sv {out/'harness.sv'}
'''
    (out/'job.sby').write_text(config)
    result=run(['sby','-d',out/'work',out/'job.sby'],out/'sby.log',70)
    status=out/'work/status'
    result.update(mode=mode,depth=48,status=status.read_text().strip().split()[0] if status.exists() else 'TIMEOUT' if result['status']=='timeout' else 'ERROR',
                  scope='relative to fixed DUT/assumptions; not independent specification truth',
                  bounded_no_counterexample_is_not_proof=True)
    dump(out/'result.json',result)
    return result
