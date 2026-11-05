"""Versioned passive monitor ABI with an evaluation-only final-post marker."""
import gzip
import hashlib
import json
from pathlib import Path
import re
from common import dump,run,sha
import controller_monitor_live as old

PINS={**old.PINS,'trace_done':1}
HEADER=old.HEADER.replace('output wire [5:0] active,ok);','input wire trace_done,\noutput wire [5:0] active,ok);')


def compile_monitor(candidate,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    source=old.validate(candidate).replace(old.HEADER,HEADER,1)
    (out/'candidate.sv').write_text(source);dump(out/'candidate.json',candidate)
    cmd=f'read_verilog -sv {out/"candidate.sv"}; hierarchy -check -top candidate_monitor; proc; opt_clean; check -assert; write_json {out/"netlist.json"}'
    r=run(['yosys','-Q','-T','-p',cmd],out/'yosys.log',60);dump(out/'compile.json',r)
    if r['status']!='complete':return r
    mod=json.loads((out/'netlist.json').read_text())['modules']['candidate_monitor'];seen=set();state=0
    for name,width in PINS.items():
        p=mod['ports'][name]
        if p['direction']!='input' or len(p['bits'])!=width or any(type(b)!=int or b in seen for b in p['bits']):raise ValueError('Readonly input overwritten or aliased')
        seen.update(p['bits'])
    for cell in mod['cells'].values():
        if not cell['type'].startswith('$') or any(s in cell['type'] for s in ('assume','assert','cover','latch','anyseq','anyconst')):raise ValueError('Unsupported monitor primitive')
        if any(d=='output' and any(b in seen for b in cell['connections'][p]) for p,d in cell['port_directions'].items()):raise ValueError('Candidate drives a public input')
        if 'CLK' in cell['connections'] and cell['type'].startswith(('$dff','$sdff','$adff')):
            if cell['connections']['CLK']!=mod['ports']['clk']['bits'] or int(cell['parameters']['CLK_POLARITY'],2)!=1:raise ValueError('Noncanonical monitor clock')
            state+=len(cell['connections']['Q'])
    state+=sum(m['width']*m['size'] for m in mod.get('memories',{}).values())
    if state>8192:raise ValueError('State exceeds8192bits')
    r.update(state_bits=state,source_sha256=sha(out/'candidate.sv'),ABI='final_post_trace_done_v1');dump(out/'compile.json',r)
    return r


def build_replay(directory):
    text=old.replay_source().replace('module replay;','module replay;\nreg trace_done=0;integer last_cycle;')
    text=text.replace('fd=$fopen(path,"r");','if(!$value$plusargs("LAST=%d",last_cycle)) $fatal(1,"Missing final cycle");\n fd=$fopen(path,"r");')
    text=text.replace('rst=v_rst;','trace_done=0;rst=v_rst;')
    text=text.replace('#1;$display("MON %0d post', 'trace_done=(cycle==last_cycle);\n   #1;$display("MON %0d post')
    (directory/'replay.sv').write_text(text)
    r=run(['iverilog','-g2012','-s','replay','-o',directory/'replay.vvp',directory/'candidate.sv',directory/'replay.sv'],directory/'iverilog.log',60)
    dump(directory/'iverilog.json',r);return r


def replay(directory,rows,out,cache):
    out.mkdir(parents=True,exist_ok=False);path,digest=old.rows_file(rows,cache)
    r=run(['vvp',directory/'replay.vvp','+ROWS='+str(path),'+LAST='+str(len(rows)-1)],out/'replay.log',15)
    raw=(out/'replay.log').read_bytes();samples=[]
    for line in raw.decode().splitlines():
        if not line.startswith('MON '):continue
        _,cycle,phase,active,ok=line.split()
        if not re.fullmatch('[01xz]{6}',active) or not re.fullmatch('[01xz]{6}',ok):raise ValueError('Malformed sample')
        samples.append((int(cycle),phase,active,ok))
    expected=[(x['cycle'],p) for x in rows for p in ('pre','post') if x['cycle'] or p=='post']
    complete=r['status']=='complete' and b'REPLAY_COMPLETE' in raw and [(x[0],x[1]) for x in samples]==expected
    props=[]
    for j in range(6):
        checks=0;failures=[];unknown=[]
        for cycle,phase,active,ok in samples:
            a,k=active[5-j],ok[5-j]
            if a not in '01' or a=='1' and k not in '01':unknown.append([cycle,phase])
            elif a=='1':
                checks+=1
                if k=='0':failures.append([cycle,phase])
        props.append(dict(id=f'P{j}',checks=checks,failures=failures,unknown=unknown))
    (out/'replay.log.gz').write_bytes(gzip.compress(raw,mtime=0));(out/'replay.log').unlink()
    result=dict(complete=complete,properties=props,cycles=len(rows),samples=len(samples),execution=r,rows_sha256=digest,
                raw_log_sha256=hashlib.sha256(raw).hexdigest(),compressed_log_sha256=sha(out/'replay.log.gz'),
                trace_done_sample=[len(rows)-1,'post'],DUT_inputs_unchanged=True)
    dump(out/'result.json',result);return result
