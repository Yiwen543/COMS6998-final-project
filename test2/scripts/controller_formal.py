#!/usr/bin/env python3
"""Local public-interface property calibration; never a scoring oracle."""
import argparse
import json
from pathlib import Path
from common import ROOT, BASE, dump, run, sha
import controller_prepare as task


def harness(slot):
    checks = ["if(past && $past(rst)) assert(!m_valid && !h_valid);",
              "if(past && !$past(rst) && $past(m_valid && !m_ready)) assert(m_valid && m_data==$past(m_data) && m_last==$past(m_last));",
              "if(past && !$past(rst) && $past(h_valid && !h_ready)) assert(h_valid && {h_pad,h_truncate,h_length,h_original_length}==$past({h_pad,h_truncate,h_length,h_original_length}));",
              'if(past) assert(1);', 'if(past) assert(0);']
    covers = ["past && $past(rst) && !rst", "past && !$past(rst) && $past(m_valid && !m_ready)",
              "past && !$past(rst) && $past(h_valid && !h_ready)", 'past', 'past']
    if slot not in range(5):
        raise ValueError('Unsupported calibration slot')
    return '''module formal_top(input wire clk);
(* anyseq *) reg rst,s_valid,s_last,m_ready,h_ready;
(* anyseq *) reg [7:0] s_data;
wire s_ready,m_valid,m_last,h_valid,h_pad,h_truncate;
wire [7:0] m_data;wire [15:0] h_length,h_original_length;
frame_task dut(.*);
reg past=0;
always @(posedge clk) begin
 if(!past) assume(rst);
 assume(!rst || !s_valid);
 if(past && !$past(rst) && $past(s_valid && !s_ready) && !rst)
  assume(s_valid && s_data==$past(s_data) && s_last==$past(s_last));
 past<=1;
 ''' + checks[slot] + '\n cover(' + covers[slot] + ');\nend\nendmodule\n'


def execute(out):
    config = json.loads((task.TASK / 'task-config.json').read_text())
    registration = ROOT / config['formal_registration']
    cfg = json.loads(registration.read_text())
    if out.exists():
        raise FileExistsError('Refusing to overwrite a calibration')
    out.mkdir(parents=True)
    results = []
    jobs = [('always_true', 3, 'bmc', 3, 5), ('always_false', 4, 'bmc', 3, 5)]
    jobs += [(name, slot, mode, 24, 10) for slot, name in enumerate(['reset', 'output_stall', 'status_stall'])
             for mode in ['bmc', 'prove', 'cover']]
    for name, slot, mode, depth, timeout in jobs:
        if len(results) == 2 and [r['status'] for r in results] != ['PASS', 'FAIL']:
            break
        d = out / (name+'-'+mode)
        d.mkdir()
        (d / 'harness.sv').write_text(harness(slot))
        files = '\n'.join(str(p) for p in task.SOURCES) + '\n' + str(d / 'harness.sv')
        source_names = ' '.join(p.name for p in task.SOURCES)
        config = f'''[options]
mode {mode}
depth {depth}
timeout {timeout}
[engines]
smtbmc z3
[script]
read -formal -sv {source_names} harness.sv
prep -top formal_top -flatten
[files]
{files}
'''
        (d / 'job.sby').write_text(config)
        result = run(['sby', '-d', d / 'work', d / 'job.sby'], d / 'sby.log', timeout+5)
        status = d / 'work/status'
        result.update(property=name, mode=mode, requested_depth=depth,
                      status=status.read_text().split()[0] if status.exists() else 'TIMEOUT' if result['status']=='timeout' else 'ERROR',
                      scope='Public local interface calibration, not independent full functional truth')
        dump(d / 'result.json', result)
        results.append(result)
    dump(out / 'summary.json', {'status': 'calibration_complete' if len(results)==11 else 'stopped_controls',
         'registration_sha256': sha(registration),
         'script_sha256': sha(Path(__file__)), 'results': results, 'formal_jobs': len(results),
         'seconds': sum(r['seconds'] for r in results), 'reference_pending': True, 'candidate_live_allowed': False})
    print(json.dumps([(r['property'], r['mode'], r['status']) for r in results]))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--task', type=Path, default=task.TASK)
    a = p.parse_args()
    task.configure(a.task)
    execute(a.output.resolve())
