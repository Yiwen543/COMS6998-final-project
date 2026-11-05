"""Controller-only passive ABI, detached replay and slot formal jobs; no oracle."""
import gzip
import hashlib
import json
from pathlib import Path
import re
from common import ROOT, BASE, dump, run, sha
import monitor as fifo_boundary
from controller_prepare import INPUTS as ROW_INPUTS, OUTPUTS

TASK = BASE / 'tasks/axis_length_fifo_v1'
SCHEMA = fifo_boundary.SCHEMA
PINS = {'clk': 1, 'rst': 1, 's_valid': 1, 's_data': 8, 's_last': 1,
        'm_ready': 1, 'h_ready': 1, 's_ready': 1, 'm_data': 8,
        'm_valid': 1, 'm_last': 1, 'h_valid': 1, 'h_pad': 1,
        'h_truncate': 1, 'h_length': 16, 'h_original_length': 16}
HEADER = 'module candidate_monitor(\n' + ',\n'.join(
    'input wire '+(f'[{w-1}:0] ' if w > 1 else '')+n for n, w in PINS.items()) + ',\noutput wire [5:0] active,ok);\n'


def validate(candidate):
    if not isinstance(candidate,dict) or set(candidate)!={'body','properties'}:
        raise ValueError('Expected body and properties only')
    if not isinstance(candidate['body'],str) or len(candidate['body'].encode())>16000:
        raise ValueError('Body exceeds byte limit')
    properties=candidate['properties']
    if not isinstance(properties,list) or len(properties)!=6:
        raise ValueError('Exactly six slots required')
    for i,p in enumerate(properties):
        if not isinstance(p,dict) or set(p)!={'id','description'} or p['id']!=f'P{i}' or not isinstance(p['description'],str) or not 1<=len(p['description'])<=400:
            raise ValueError('Property ID/description invalid')
    code=re.sub(r'/\*.*?\*/|//[^\n]*',' ',candidate['body'],flags=re.S)
    if any(c in code for c in ('`','$','#','"','.', '\\')):
        raise ValueError('System call, hierarchy, preprocessor, delay or escaped identifier')
    if re.search(r'\b(module|endmodule|interface|program|package|bind|import|export|force|release|assert|assume|cover|property|sequence|task|function|fork|join|wait|forever|while|repeat|negedge|disable|specify|primitive|inout|input|output|ref|always_latch)\b',code):
        raise ValueError('Unsupported or boundary-changing construct')
    if '@' in re.sub(r'@\s*(?:\(\s*posedge\s+clk\s*\)|\(\s*\*\s*\)|\*)','',code):
        raise ValueError('Unsupported event control')
    return '`default_nettype none\n'+HEADER+candidate['body']+'\nendmodule\n`default_nettype wire\n'


def compile_monitor(candidate, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    (out / 'candidate.sv').write_text(validate(candidate))
    dump(out / 'candidate.json', candidate)
    command = f'read_verilog -sv {out/"candidate.sv"}; hierarchy -check -top candidate_monitor; proc; opt_clean; check -assert; write_json {out/"netlist.json"}'
    result = run(['yosys', '-Q', '-T', '-p', command], out / 'yosys.log', 60)
    dump(out / 'compile.json', result)
    if result['status'] != 'complete':
        return result
    module = json.loads((out / 'netlist.json').read_text())['modules']['candidate_monitor']
    seen = set()
    for name, width in PINS.items():
        port = module['ports'][name]
        if port['direction'] != 'input' or len(port['bits']) != width or any(type(b) is not int or b in seen for b in port['bits']):
            raise ValueError('Input overwritten or aliased')
        seen.update(port['bits'])
    state = 0
    for cell in module['cells'].values():
        if not cell['type'].startswith('$') or any(t in cell['type'] for t in ('assume', 'assert', 'cover', 'latch', 'anyconst', 'anyseq')):
            raise ValueError('Untrusted primitive, instance or latch')
        if any(direction == 'output' and any(b in seen for b in cell['connections'][port])
               for port, direction in cell['port_directions'].items()):
            raise ValueError('Candidate drives public input')
        if 'CLK' in cell['connections'] and cell['type'].startswith(('$dff', '$sdff', '$adff')):
            if cell['connections']['CLK'] != module['ports']['clk']['bits'] or int(cell['parameters']['CLK_POLARITY'], 2) != 1:
                raise ValueError('Noncanonical observer clock')
            state += len(cell['connections']['Q'])
    state += sum(m['width'] * m['size'] for m in module.get('memories', {}).values())
    if state > 8192:
        raise ValueError('Observer state exceeds8192bits')
    result.update(state_bits=state, source_sha256=sha(out / 'candidate.sv'))
    dump(out / 'compile.json', result)
    return result


def replay_source():
    decl = '\n'.join('reg '+(f'[{w-1}:0] ' if w > 1 else '')+n+'=0;' for n, w in PINS.items())
    variables = ['cycle'] + ['v_'+n for n in ROW_INPUTS] + [p+'_'+n for p in ('pre', 'post') for n in OUTPUTS]
    before = '\n'.join(f'{n}=v_{n};' for n in ROW_INPUTS)
    before += '\n'+'\n'.join(f'{n}=pre_{n};' for n in OUTPUTS)
    after = '\n'.join(f'{n}=post_{n};' for n in OUTPUTS)
    return '''`timescale 1ns/1ps
module replay;
''' + decl + '''
wire [5:0] active,ok;
candidate_monitor monitor(.*);
string path;
integer fd,n;
integer ''' + ','.join(variables) + ''';
initial begin
 if(!$value$plusargs("ROWS=%s",path)) $fatal(1,"Missing rows");
 fd=$fopen(path,"r");if(!fd) $fatal(1,"Missing file");
 while(!$feof(fd)) begin
  n=$fscanf(fd,"''' + ' '.join(['%h']*len(variables)) + '\\n",'+','.join(variables)+''');
  if(n==''' + str(len(variables)) + ''') begin
''' + before + '''
   #4;if(cycle>0) $display("MON %0d pre %06b %06b",cycle,active,ok);
   #1;clk=1;#1;
''' + after + '''
   #1;$display("MON %0d post %06b %06b",cycle,active,ok);
   #3;clk=0;
  end else if(n!=-1) $fatal(1,"Malformed rows");
 end
 $display("REPLAY_COMPLETE");$finish;
end
endmodule
'''


def build_replay(directory):
    (directory / 'replay.sv').write_text(replay_source())
    result = run(['iverilog', '-g2012', '-s', 'replay', '-o', directory / 'replay.vvp',
                  directory / 'candidate.sv', directory / 'replay.sv'], directory / 'iverilog.log', 60)
    dump(directory / 'iverilog.json', result)
    return result


def rows_file(rows, cache):
    cache.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(rows, separators=(',', ':'), sort_keys=True).encode()
    digest = hashlib.sha256(raw).hexdigest()
    path = cache / (digest+'.hex')
    if not path.exists():
        lines = []
        for row in rows:
            vals = [row['cycle']] + [row['inputs'][k] for k in ROW_INPUTS] + [row[p][k] for p in ('pre', 'post') for k in OUTPUTS]
            lines.append(' '.join('x' if v == -1 else f'{v:x}' for v in vals))
        path.write_text('\n'.join(lines)+'\n')
    return path, digest


def replay(directory, rows, out, cache):
    out.mkdir(parents=True, exist_ok=False)
    path, digest = rows_file(rows, cache)
    info = run(['vvp', directory / 'replay.vvp', '+ROWS='+str(path)], out / 'replay.log', 15)
    raw = (out / 'replay.log').read_bytes()
    samples = []
    for line in raw.decode().splitlines():
        if not line.startswith('MON '):
            continue
        _, cycle, phase, active, ok = line.split()
        if not re.fullmatch('[01xz]{6}', active) or not re.fullmatch('[01xz]{6}', ok):
            raise ValueError('Malformed monitor sample')
        samples.append((int(cycle), phase, active, ok))
    expected = [(r['cycle'], p) for r in rows for p in ('pre', 'post') if r['cycle'] or p == 'post']
    complete = info['status'] == 'complete' and b'REPLAY_COMPLETE' in raw and [(x[0], x[1]) for x in samples] == expected
    properties = []
    for slot in range(6):
        checks, failures, unknown = 0, [], []
        for cycle, phase, active, ok in samples:
            a, k = active[5-slot], ok[5-slot]
            if a not in '01' or (a == '1' and k not in '01'):
                unknown.append([cycle, phase])
            elif a == '1':
                checks += 1
                if k == '0':
                    failures.append([cycle, phase])
        properties.append(dict(id=f'P{slot}', checks=checks, failures=failures, unknown=unknown, vacuous_on_trace=checks == 0))
    (out / 'replay.log.gz').write_bytes(gzip.compress(raw, mtime=0))
    (out / 'replay.log').unlink()
    result = dict(complete=complete, properties=properties, samples=len(samples), cycles=sum(x[1] == 'post' for x in samples),
                  attempted_cycles=len(rows), execution=info, rows_sha256=digest, raw_log_sha256=hashlib.sha256(raw).hexdigest(),
                  compressed_log_sha256=sha(out / 'replay.log.gz'))
    (out / 'result.json').write_text(json.dumps(result, separators=(',', ':'), sort_keys=True)+'\n')
    return result


def formal_harness(slot):
    if slot not in range(6):
        raise ValueError('Slot must be0..5')
    return '''module formal_top(input wire clk);
(* anyseq *) reg rst,s_valid,s_last,m_ready,h_ready;
(* anyseq *) reg [7:0] s_data;
(* keep *) wire s_ready,m_valid,m_last,h_valid,h_pad,h_truncate;
(* keep *) wire [7:0] m_data;
(* keep *) wire [15:0] h_length,h_original_length;
wire [5:0] active,ok;
frame_task dut(.*);
candidate_monitor monitor(.*);
reg past=0;
reg [3:0] frame_bytes=0;
always @(posedge clk) begin
 if(!past) assume(rst);
 assume(!rst || !s_valid);
 if(past && !$past(rst) && $past(s_valid && !s_ready) && !rst)
  assume(s_valid && s_data==$past(s_data) && s_last==$past(s_last));
 if(rst) frame_bytes<=0;
 else if(s_valid && s_ready) begin
  assume(frame_bytes<11 || s_last);
  if(s_last) frame_bytes<=0; else frame_bytes<=frame_bytes+1;
 end
 past<=1;
 if(past) begin
''' + f'  assert(!active[{slot}] || ok[{slot}]);\n  cover(active[{slot}]);\n' + ''' end
end
endmodule
'''


def formal_job(directory, source, out, slot, mode, timeout, depth=24):
    out.mkdir(parents=True, exist_ok=False)
    (out / 'harness.sv').write_text(formal_harness(slot))
    public = TASK / 'public'
    sources = [source, public / 'rtl/axis_fifo.v', public / 'rtl/axis_frame_length_adjust_fifo.v', public / 'task_top_v3.sv']
    # Mutant sources use stable local alias so command/semantics stay identical.
    files = 'dut.v '+str(sources[0])+'\n'+'\n'.join(str(p) for p in sources[1:])
    files += '\ncandidate.sv '+str(directory / 'candidate.sv')+'\nharness.sv '+str(out / 'harness.sv')
    config = f'''[options]
mode {mode}
depth {depth}
timeout {timeout}
[engines]
smtbmc z3
[script]
read -formal -sv dut.v axis_fifo.v axis_frame_length_adjust_fifo.v task_top_v3.sv candidate.sv harness.sv
prep -top formal_top -flatten
[files]
{files}
'''
    (out / 'job.sby').write_text(config)
    result = run(['sby', '-d', out / 'work', out / 'job.sby'], out / 'sby.log', timeout+5)
    status = out / 'work/status'
    result.update(slot=slot, mode=mode, depth=depth, solver_cap_seconds=timeout,
                  status=status.read_text().split()[0] if status.exists() else 'TIMEOUT' if result['status']=='timeout' else 'ERROR',
                  bounded_pass_is_not_unbounded_proof=True, scope='Relative to fixed DUT and legal-source assumptions; independent reference adjudicates witnesses')
    dump(out / 'result.json', result)
    return result
