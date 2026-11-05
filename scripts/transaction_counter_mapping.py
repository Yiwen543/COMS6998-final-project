"""Exact generated-instance membership of Verilator shared source counters.

The runtime groups by all non-hierarchy metadata (including specialization page).
Wildcard hierarchies are display summaries, NEVER membership patterns. Original
raw points/counters remain unchanged. Missing/partial membership is unresolved.
"""
import json
import re
from pathlib import Path
from collections import defaultdict
from run_midterm_fixed import sha
from preflight_spi_host import identity
from screen_write_hierarchy import module_scope

FIELDS=('f','l','n','page','o','S','fsm_var','fsm_from','fsm_to','fsm_tag')

def fingerprint(fields):
    return tuple(str(fields.get(k,'')) for k in FIELDS)

class CounterRegistry:
    def __init__(self,raw,build,points):
        self.records={};self.generated_hashes={};self.unresolved=[]
        raw_rows=[]
        for line in raw.read_text().splitlines()[1:]:
            match=re.fullmatch(r"C '(.*)' (\d+)",line)
            if not match:raise ValueError('Unknown raw coverage format')
            f=dict(p.split('\x02',1) for p in match[1].split('\x01') if p)
            if 'dut' in f.get('h','').split('.') and f['t']!='toggle':raw_rows.append(f)
        by=defaultdict(list)
        pattern=re.compile(r'->__vlCoverInsert\((.*?)\);',re.S)
        for path in sorted(build.glob('*.cpp')):
            content=path.read_text();matches=pattern.findall(content)
            if not matches:continue
            self.generated_hashes[str(path.resolve())]=sha(path)
            for call in matches:
                args=re.findall(r'\s*("(?:\\.|[^"\\])*"|[^,\s][^,]*)(?:,|$)',call)
                args=[x.strip() for x in args]
                if len(args)!=14:raise ValueError('Unknown generated coverage insertion signature')
                if args[2]!='true':continue # duplicate local/global insertions have identical metadata
                try:
                    src=json.loads(args[3]);line=int(args[4]);column=int(args[5])
                    values=[json.loads(x) for x in args[6:]]
                except (ValueError,json.JSONDecodeError) as e:raise ValueError('Nonliteral generated source metadata') from e
                hierarchy,page,outcome,span,*fsm=values
                hierarchy=hierarchy.lstrip('.')
                if 'dut' not in hierarchy.split('.'):continue
                f=dict(zip(FIELDS,[src,line,column,page,outcome,span,*fsm]))
                by[fingerprint(f)].append(hierarchy)
        for p in points:
            if p['type']=='toggle':continue
            rows=[f for f in raw_rows if f['f']==p['source'] and int(f['l'])==p['line'] and int(f.get('n',0))==p['column'] and f['t']==p['type'] and f.get('o','')==p['outcome'] and f['h']==p['hierarchy']]
            if len(rows)!=1:raise ValueError('Raw identity collision or missing row (page cannot be discarded)')
            row=rows[0];members=sorted(set(by[fingerprint(row)]))
            if not members:self.unresolved.append({'point':p,'reason':'No exact generated metadata membership'});continue
            # Another raw row with the same grouping metadata must not be silently collapsed.
            if sum(fingerprint(f)==fingerprint(row) for f in raw_rows)!=1:raise ValueError('Per-instance/custom grouping requires explicit support')
            self.records[identity(p)]={'point':p,'page':row['page'],'members':members,
                'member_scopes':['.'.join(x.split('.')[x.split('.').index('dut')+1:]) for x in members]}
        self.manifest={'raw_sha256':sha(raw),'generated_hashes':self.generated_hashes,
            'basis':'Exact filename/line/column/page/comment/span/FSM fields from generated local insertion and raw row; runtime groups non-hierarchy metadata. No wildcard matching.',
            'records':list(self.records.values()),'unresolved':self.unresolved}

    def join(self,original,target,points,instances):
        scope=module_scope(target,instances)
        selected=[p for p in points if identity(p) in self.records and scope in self.records[identity(p)]['member_scopes']]
        # Reuse the exact source/outcome matcher, providing the already-certified
        # subset under the target scope. Restore the ORIGINAL point immediately.
        copies=[{**p,'hierarchy':'tb_natural_inventory.dut'+('.'+scope if scope else '')} for p in selected]
        result=original(target,copies,instances)
        if result['status']=='mapped':
            idx=copies.index(result['point']);p=selected[idx];record=self.records[identity(p)]
            result={**result,'point':p,'generated_instance_members':record['member_scopes'],'specialization_page':record['page'],
                'basis':result['basis']+'; exact generated specialization/membership, no wildcard inference'}
        return result

    def aggregate(self,original,targets,maps,instances):
        groups=defaultdict(list)
        for t in targets:
            mp=maps[t['id']]
            if mp['status']=='mapped':groups[identity(mp['point'])].append(t)
        for key,ts in groups.items():
            present={module_scope(t,instances) for t in ts};required=set(self.records[key]['member_scopes'])
            if present!=required:
                for t in ts:maps[t['id']]={'status':'unresolved','reason':'Not all physical-counter instance guards available',
                    'present':sorted(present),'required':sorted(required),'original_mapping':maps[t['id']]}
        return original(targets,maps)
