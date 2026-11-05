"""Explicit allowlist renderer. No recursive workspace access in model prompts."""
import json
import re
from common import BASE, ROOT, sha
from semantic_candidate_scan import map_true_counter

SYSTEM = '''Write a passive SystemVerilog FIFO monitor from the specification.
Return JSON with body and exactly six properties P0..P5. The fixed wrapper is given.
You may modify only the candidate monitor body and its six descriptions. It is the
object being evaluated, not the reference. Maximize sound specification checks and
useful fault detection. Never assume that an RTL-derived equivalence implies that
the RTL is correct. Do not drive any input, add assumptions or stop simulation.
Use only the supported observer interface. Fixed stimulus and DUT coverage cannot
be improved by changing this monitor. Development feedback concerns this candidate;
there is no access to final evaluation or its outcomes.'''

def pack_rows(rows):
    keys=('fill','full','empty','data')
    return {'columns':['cycle','reset','wr','rd','input_data']+
            [f'{p}_{k}' for p in ('pre','post') for k in keys],
            'rows':[[r['cycle']]+[r['action'][k] for k in ('reset','wr','rd','data')]+
                    [r[p][k] for p in ('pre','post') for k in keys] for r in rows]}

def pack_counters(points):
    keys=('source','line','column','type','outcome','hierarchy','span','hits')
    return {'columns':list(keys),'points':[[p[k] for k in keys] for p in points]}

def pack_shared_counters(pointsets):
    keys=('source','line','column','type','outcome','hierarchy','span')
    identities=[[p[k] for k in keys] for p in pointsets[0]]
    for points in pointsets:
        if [[p[k] for k in keys] for p in points]!=identities:
            raise ValueError('Fixed development denominator changed')
    dictionaries=[]
    for col in range(len(keys)):
        dictionaries.append(list(dict.fromkeys(row[col] for row in identities)))
    indices=[[dictionaries[i].index(v) for i,v in enumerate(row)] for row in identities]
    return {'encoding':'column_dictionary_indices_v1','columns':list(keys),
            'column_values':dictionaries,'counter_rows':indices,
            'meaning':'Row order is counter identity; each trace supplies its own hits array. No counter is merged.'}

def unpack_shared_counters(layout,hits):
    if len(hits)!=len(layout['counter_rows']):raise ValueError('Counter length mismatch')
    return [dict(zip(layout['columns'],[layout['column_values'][i][v] for i,v in enumerate(row)]),hits=n)
            for row,n in zip(layout['counter_rows'],hits)]

def semantic_appendix(semantic,points):
    source=BASE/'public/sfifo.v'
    if sha(source)!=semantic['source_sha256'] or semantic['source']!=str(source):
        raise ValueError('Semantic evidence source mismatch')
    groups=[]; unmapped=[]
    for group in semantic['groups']:
        if not group['requires_egg_rewrite_to_merge']: continue
        members=[]
        for m in group['members']:
            mapping=map_true_counter(m,points)
            if mapping['status']!='mapped':
                unmapped.append({'line':m['line'],'status':mapping['status']});continue
            p=mapping['point']
            members.append({'line':m['line'],'column':p['column'],'type':p['type'],
                'outcome':p['outcome'],'hits':p['hits'],'complete_activation_guard':m['compact'],
                'source_mapping':m['source_mapping']})
        if len(members)==len(group['members']):
            groups.append({'eclass':group['eclass'],'event_context':group['event_context'],
                'representative':group['representative'],'nodes':group['eclass_nodes'],
                'z3_pair_checks':group['independent_z3_checks'],'members':members})
    atoms=set(re.findall(r'p_[a-f0-9]+',json.dumps(groups)))
    return {'scope':semantic['semantics'],'source_sha256':semantic['source_sha256'],
        'engine':semantic['egg'],'typed_atoms':{k:semantic['atoms'][k] for k in sorted(atoms)},
        'equivalent_groups':groups,'unsupported':semantic['unsupported'],
        'unmapped':unmapped,'unresolved_aliases':semantic['unresolved_aliases'],
        'note':'All source counters kept separately. Internal terms describe RTL; candidate interface remains public I/O. No sequential/specification correctness claim.'}

def messages(arm,preflight,round_no,previous=None,feedback=None):
    if arm not in ('B_prime','C_prime'): raise ValueError('Unknown arm')
    from monitor import HEADER
    # Every filename below is a literal allowlist; final/private/reference paths
    # cannot be requested through candidate text or a configurable glob.
    development={};pointsets=[]
    for name in ('basic','boundary','wrap_reset'):
        folder=preflight/'correct_stress/verilator'/name
        rows=json.loads((folder/'rows.json').read_text())
        points=json.loads((folder/'coverage.json').read_text())
        # Public display alias retains all raw identities; on-disk originals kept.
        points=[dict(p,source='sfifo.v',hierarchy=p['hierarchy']) for p in points]
        development[name]={'observations':pack_rows(rows),'raw_dut_coverage_hits':[p['hits'] for p in points]}
        pointsets.append(json.loads((folder/'coverage.json').read_text()))
    display_points=[[dict(p,source='sfifo.v') for p in points] for points in pointsets]
    layout=pack_shared_counters(display_points)
    for points in display_points:
        if unpack_shared_counters(layout,[p['hits'] for p in points])!=points:
            raise AssertionError('Raw counter representation lost information')
    data={'specification':(BASE/'public/specification.md').read_text(),
          'rtl':{'sfifo.v':(BASE/'public/sfifo.v').read_text()},
          'observer_contract':(BASE/'public/observer_contract.md').read_text(),
          'module_header':HEADER,'round':round_no,'development':development,'raw_counter_layout':layout,
          'previous_candidate':previous,'development_feedback':feedback}
    if arm=='C_prime':
        semantic=json.loads((preflight/'semantic.json').read_text())
        data['egraph_feedback']=semantic_appendix(semantic,pointsets[0])
        data['egraph_feedback']['counter_basis']='development.basic; see the same source identities in all three raw development count arrays. Groups are not asserted to be uncovered over the full development corpus.'
    return [{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(data,separators=(',',':'),sort_keys=True)}]
