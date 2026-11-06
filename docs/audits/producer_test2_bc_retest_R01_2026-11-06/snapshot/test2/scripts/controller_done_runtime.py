"""Integrated marker ABI runtime; immutable prototype compiler is reused."""
import gzip
import hashlib
import json
from pathlib import Path
import re
from common import dump,run,sha
import controller_monitor_done as prototype
from controller_monitor_live import ROW_INPUTS,OUTPUTS,rows_file,SCHEMA

HEADER=prototype.HEADER
PINS=prototype.PINS
compile_monitor=prototype.compile_monitor
build_replay=prototype.build_replay


def check_rows(rows):
    if not rows or len(rows)>512 or [r.get('cycle') for r in rows]!=list(range(len(rows))):raise ValueError('Consecutive bounded rows required')
    for row in rows:
        if set(row)!=set(('cycle','inputs','pre','post')):raise ValueError('Unexpected row fields')
        for section,keys in [('inputs',ROW_INPUTS),('pre',OUTPUTS),('post',OUTPUTS)]:
            if set(row[section])!=set(keys):raise ValueError('Public pin layout changed')
            if any(type(row[section][n])!=int or not -1<=row[section][n]<2**PINS[n] for n in keys):raise ValueError('Out-of-range observation')


def replay(directory,rows,out,cache,trace_done=True,timeout=15):
    check_rows(rows);out=Path(out);out.mkdir(parents=True,exist_ok=False);path,digest=rows_file(rows,cache)
    marker=len(rows)-1 if trace_done else -1
    execution=run(['vvp',directory/'replay.vvp','+ROWS='+str(path),'+LAST='+str(marker)],out/'replay.log',min(15,timeout))
    raw=(out/'replay.log').read_bytes();samples=[]
    for line in raw.decode().splitlines():
        if not line.startswith('MON '):continue
        _,cycle,phase,active,ok=line.split()
        if not re.fullmatch('[01xz]{6}',active) or not re.fullmatch('[01xz]{6}',ok) or phase not in ('pre','post'):raise ValueError('Malformed monitor sample')
        samples.append((int(cycle),phase,active,ok))
    expected=[(r['cycle'],p) for r in rows for p in ('pre','post') if r['cycle'] or p=='post']
    complete=execution['status']=='complete' and b'REPLAY_COMPLETE' in raw and [(s[0],s[1]) for s in samples]==expected
    properties=[]
    for slot in range(6):
        checks=0;failures=[];unknown=[];end_checks=0
        for cycle,phase,active,ok in samples:
            a,k=active[5-slot],ok[5-slot]
            if a not in '01' or a=='1' and k not in '01':unknown.append([cycle,phase])
            elif a=='1':
                checks+=1;end_checks+=int(trace_done and (cycle,phase)==(marker,'post'))
                if k=='0':failures.append([cycle,phase])
        properties.append(dict(id=f'P{slot}',checks=checks,end_sample_checks=end_checks,ordinary_sample_checks=checks-end_checks,
                               failures=failures,unknown=unknown,vacuous_on_trace=checks==0))
    (out/'replay.log.gz').write_bytes(gzip.compress(raw,mtime=0));(out/'replay.log').unlink()
    result=dict(complete=complete,properties=properties,samples=len(samples),cycles=sum(s[1]=='post' for s in samples),attempted_cycles=len(rows),
                execution=execution,rows_sha256=digest,raw_log_sha256=hashlib.sha256(raw).hexdigest(),compressed_log_sha256=sha(out/'replay.log.gz'),
                trace_done_sample=[marker,'post'] if trace_done else None,safety_projection=not trace_done,DUT_inputs_unchanged=True)
    dump(out/'result.json',result);return result
