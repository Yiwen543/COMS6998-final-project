#!/usr/bin/env python3
"""Prepare deterministic sources, fixed stimuli, hidden mutants and author packet.

Does not implement a FIFO oracle or call any model. Outputs cannot be overwritten.
"""
import json
import random
import re
import shutil
from common import BASE, ROOT, dump, sha
from sfifo_fixture import validate_actions

def strip_formal(text):
    result, depth, suppressed = [], 0, []
    for line_no, line in enumerate(text.splitlines(keepends=True), 1):
        if depth:
            if re.match(r'\s*`ifn?def\b', line): depth += 1
            if re.match(r'\s*`endif\b', line): depth -= 1
            result.append('\n'); suppressed.append(line_no)
        elif re.match(r'\s*`ifdef\s+FORMAL\b', line):
            depth = 1; result.append('\n'); suppressed.append(line_no)
        else: result.append(line)
    if depth: raise ValueError('Unbalanced FORMAL block')
    return ''.join(result), suppressed

def action(reset=0, wr=0, rd=0, data=0):
    return dict(reset=reset, wr=wr, rd=rd, data=data)

def datasets():
    # Construct fixed stimulus only; no queue oracle or expected outputs here.
    reset = action(reset=1)
    basic = [reset, action(rd=1), action(wr=1, data=17), action(),
             action(wr=1, rd=1, data=39), action(rd=1), action(rd=1)]
    boundary = [reset] + [action(wr=1, data=(i*13+7)%256) for i in range(18)]
    boundary += [action(wr=1, rd=1, data=201)] * 3
    boundary += [action(rd=1) for _ in range(20)] + [action(wr=1, rd=1, data=91)]
    wrap = [reset] + [action(wr=1, data=(i*17+3)%256) for i in range(12)]
    wrap += [action(wr=1, rd=1, data=(i*19+1)%256) for i in range(22)]
    wrap += [reset, reset, action(), action(wr=1, data=241), action(rd=1)]
    fb = [reset, reset] + [action(wr=1, rd=1, data=201)]
    fb += [action(wr=1, data=(i*29+11)%256) for i in range(18)]
    fb += [action(wr=1, rd=1, data=(i*37+1)%256) for i in range(19)]
    fb += [action(rd=1) for _ in range(19)]
    fw = [reset]
    for k in range(3):
        fw += [action(wr=1, data=(i*31+k*47)%256) for i in range(13)]
        fw += [action(rd=1) for _ in range(9)]
        fw += [action(wr=1, rd=1, data=(i*23+k)%256) for i in range(18)]
        fw += [reset, action()]
    rng = random.Random(699802)
    fm = [reset]
    for i in range(160):
        fm.append(reset if i in (53, 109) else action(wr=rng.randrange(2), rd=rng.randrange(2), data=rng.randrange(256)))
    return {name: seq + [action(), action()] for name, seq in
            [('basic', basic), ('boundary', boundary), ('wrap_reset', wrap),
             ('final_boundary', fb), ('final_wrap_reset', fw), ('final_mixed', fm)]}

def mutations(source):
    rules = [
        ('M01', 'read_pointer_step', 'else rd_addr <= rd_addr + 1;', 'else rd_addr <= rd_addr + 2;'),
        ('M02', 'lost_write', 'if (w_wr)\n', "if (w_wr && wr_addr != 5'd3)\n"),
        ('M03', 'reset_empty_flag', "r_empty <= 1'b1;", "r_empty <= 1'b0;"),
        ('M04', 'data_order', 'o_data = mem[rd_addr[LGFLEN-1:0]];', "o_data = mem[rd_addr[LGFLEN-1:0] ^ 4'b0001];"),
        ('M05', 'full_write_admission', 'wire\tw_wr = (i_wr && !o_full);', 'wire\tw_wr = i_wr;'),
        ('M06', 'simultaneous_read_step', "2'b11: rd_addr <= rd_addr + 1;", "2'b11: rd_addr <= rd_addr;")]
    out = []
    for mid, fault, old, new in rules:
        n = source.count(old)
        # M04 deliberately changes only the active asynchronous-read branch.
        if mid == 'M04':
            anchor = 'end else if (OPT_ASYNC_READ)'
            start = source.index(anchor)
            pos = source.index(old, start)
        else:
            if n != 1: raise AssertionError((mid, n))
            pos = source.index(old)
        modified = source[:pos] + new + source[pos+len(old):]
        out.append((mid, modified, dict(fault=fault, line=source[:pos].count('\n')+1,
                                       old=old, new=new, changed_sites=1)))
    return out

def main():
    manifest = BASE/'configs/input_manifest_v1.json'
    if manifest.exists(): raise SystemExit('Prepared inputs already registered; do not overwrite')
    for d in ('public', 'private/mutants', 'private/final', 'public/development', 'reference/author-v1'):
        (BASE/d).mkdir(parents=True, exist_ok=True)
    source = ROOT/'examples/heldout_sfifo_stress/rtl/sfifo.v'
    original = ROOT/'examples/heldout_sfifo/rtl/sfifo.v'
    clean, removed = strip_formal(source.read_text())
    if re.search(r'\b(assert|assume|cover)\s*\(', clean): raise AssertionError('Verification leakage')
    (BASE/'public/sfifo.v').write_text(clean)
    original_clean, _ = strip_formal(original.read_text())
    (BASE/'private/original_noformal.v').write_text(original_clean)
    shutil.copyfile(ROOT/'examples/heldout_sfifo_stress/docs/specification.md', BASE/'public/specification.md')
    shutil.copyfile(ROOT/'examples/heldout_sfifo_stress/verif/tb_sfifo_stress_fixed.sv', BASE/'public/driver.sv')
    catalog = []
    for mid, text, entry in mutations(clean):
        path = BASE/'private/mutants'/f'{mid}.v'; path.write_text(text)
        catalog.append(dict(id=mid, **entry, sha256=sha(path), eligibility='pending_independent_reference'))
    dump(BASE/'private/mutant_catalog.json', catalog)
    for name, actions in datasets().items():
        validate_actions({'actions': actions}, 1024)
        folder = 'private/final' if name.startswith('final_') else 'public/development'
        dump(BASE/folder/f'{name}.json', {'actions': actions})
    author_spec = (BASE/'public/specification.md').read_text()
    abi = (BASE/'public/observer_contract.md').read_text()
    request = '''You are the independent specification-based FIFO reference checker author.
Use ONLY the supplied specification and observation interface. No tools.
You are not the experimental candidate. Do not infer behavior from an implementation.
Return JSON only with exactly checker_source, properties, contract_markdown, selftest_source.
checker_source is pure Python defining check_rows(rows). selftest_source defines run(check_rows).
Allowed imports: collections, copy, math. No file/network/process access or reflection.
Each row: {cycle:int, action:{reset,wr,rd,data}, pre:{fill,full,empty,data}, post:{fill,full,empty,data}}.
Unknown observed values are represented by -1. Empty data is unspecified, not a failure.
Use a specification queue based on inputs and expected occupancy, NEVER DUT flags to decide acceptance.
Initial pre-reset outputs are unspecified. First action must reset; ignore its pre phase but check post.
Check subsequent pre and post states, including synchronous reset timing; reset input is applied before pre.
Acceptance for simultaneous operations is decided from pre-edge expected occupancy.
Report verdict PASS/FAIL/UNRESOLVED/INVALID_INPUT; failures each with cycle, phase, category,
actual, expected; assumption_violations; unresolved; checks; rows_processed; properties.
Illegal fields/widths/reset operations/missing or out-of-order rows must not become PASS.
Undefined checked outputs are UNRESOLVED; preserve previous failures (FAIL dominates unknown).
properties is a list of specification property IDs, scope and supported behavior; no blanket proof claim.
Selftests should test legal/reset/boundary/order behavior and wrong observations without external files.
Return complete source, not patches. Do not write SystemVerilog here.
SPECIFICATION:\n''' + author_spec + '\nOBSERVATION CONTRACT:\n' + abi
    (BASE/'reference/author-v1/prompt.txt').write_text(request)
    public_files = sorted((BASE/'public').rglob('*'))
    private_files = sorted((BASE/'private').rglob('*'))
    dump(manifest, {'registration_sha256': sha(BASE/'configs/registration_v1.json'),
        'source_sha256': sha(source), 'upstream_original_sha256': sha(original),
        'source_transformation': {'operation':'blank FORMAL conditional sections; preserve every other line',
                                  'removed_lines':removed, 'source_line_mapping':'identity'},
        'files': {str(p.relative_to(BASE)): sha(p) for p in public_files+private_files if p.is_file()},
        'author_prompt_sha256':sha(BASE/'reference/author-v1/prompt.txt')})
    print(json.dumps({'status':'inputs_registered_reference_pending','stimulus_lengths':{k:len(v) for k,v in datasets().items()},'mutants':len(catalog)}))

if __name__ == '__main__': main()
